"""Validate the frozen Progressive Clarity repository and skill package."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
FROZEN_FILES = {
    Path("SPEC.md"): "90ccf39dc5cf91e895fb3cf2f1f788cba80daea94e1f07435748083c55bb4096",
    Path("skills/progressive-clarity/SKILL.md"): (
        "4167d7fa89d008453b223d2ff33a2182096abefaffeab4698a65a6ce23bdbaae"
    ),
    Path("evals/cases.json"): (
        "b5c2becc53e6e7e167878de3f4f84451fd0d446c38ac4d5e6df74eaeef42cbd4"
    ),
}
EXPECTED_SKILL_FILES = {Path("LICENSE"), Path("SKILL.md")}
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".editorconfig", ".gitignore", "LICENSE"}
LINK_PATTERN = re.compile(
    r"!?\[[^\]]*]\((?P<target><[^>]+>|[^)\s]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\)"
)
REFERENCE_LINK_PATTERN = re.compile(r"(?m)^\s{0,3}\[[^\]]+]:\s*(?P<target><[^>]+>|\S+)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FRONTMATTER_FIELD_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")
LEGACY_CUE_PATTERN = re.compile(
    r"(?im)(?:\*\*)?(?:Why it matters|The big picture|What changes|"
    r"The constraint|What's next|What’s next):(?:\*\*)?"
)


def repository_files() -> list[Path]:
    """Return repository files while excluding Git internals."""
    return sorted(
        (
            path
            for path in ROOT.rglob("*")
            if ".git" not in path.relative_to(ROOT).parts
            and not path.is_symlink()
            and path.is_file()
        ),
        key=lambda path: path.as_posix(),
    )


def validate_frozen_files(errors: list[str]) -> None:
    """Confirm that the canonical inputs still match their frozen hashes."""
    for relative_path, expected_hash in FROZEN_FILES.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"{relative_path}: missing frozen file")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(
                f"{relative_path}: SHA-256 {actual_hash} does not match {expected_hash}"
            )


def validate_whitespace(errors: list[str]) -> None:
    """Check UTF-8 text files for repository whitespace invariants."""
    for path in repository_files():
        if path.suffix not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        relative_path = path.relative_to(ROOT)
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative_path}: not valid UTF-8 ({exc})")
            continue
        if "\r" in text:
            errors.append(f"{relative_path}: contains a carriage return")
        if raw and not raw.endswith(b"\n"):
            errors.append(f"{relative_path}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                errors.append(f"{relative_path}:{line_number}: trailing whitespace")
            if "\t" in line:
                errors.append(f"{relative_path}:{line_number}: tab character")


def markdown_without_fences(text: str) -> str:
    """Remove fenced-code content before checking Markdown links and headings."""
    kept_lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if fence is None and marker in {"```", "~~~"}:
            fence = marker
            kept_lines.append("")
        elif fence is not None and stripped.startswith(fence):
            fence = None
            kept_lines.append("")
        elif fence is None:
            kept_lines.append(line)
        else:
            kept_lines.append("")
    return "\n".join(kept_lines)


def markdown_anchors(path: Path) -> set[str]:
    """Return GitHub-style anchors for headings in one Markdown file."""
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    text = markdown_without_fences(path.read_text(encoding="utf-8"))
    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        heading = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", match.group(2))
        heading = re.sub(r"<[^>]+>|[`*_~]", "", heading).strip().lower()
        slug = re.sub(r"[^\w\s-]", "", heading)
        slug = re.sub(r"\s+", "-", slug)
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def validate_link(
    source: Path, raw_target: str, anchor_cache: dict[Path, set[str]], errors: list[str]
) -> None:
    """Validate one relative Markdown link target."""
    target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return
    relative_source = source.relative_to(ROOT)
    if parsed.path.startswith("/"):
        errors.append(f"{relative_source}: repository link must be relative: {target}")
        return
    target_path = source if not parsed.path else source.parent / unquote(parsed.path)
    resolved = target_path.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        errors.append(f"{relative_source}: link escapes repository: {target}")
        return
    if not resolved.exists():
        errors.append(f"{relative_source}: missing link target: {target}")
        return
    if parsed.fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
        anchors = anchor_cache.setdefault(resolved, markdown_anchors(resolved))
        fragment = unquote(parsed.fragment).lower()
        if fragment not in anchors:
            errors.append(f"{relative_source}: missing link anchor: {target}")


def validate_relative_links(errors: list[str]) -> None:
    """Check relative destinations and anchors in Markdown links."""
    anchor_cache: dict[Path, set[str]] = {}
    for source in sorted(ROOT.rglob("*.md")):
        if ".git" in source.relative_to(ROOT).parts:
            continue
        text = markdown_without_fences(source.read_text(encoding="utf-8"))
        matches = list(LINK_PATTERN.finditer(text))
        matches.extend(REFERENCE_LINK_PATTERN.finditer(text))
        for match in matches:
            validate_link(source, match.group("target"), anchor_cache, errors)


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    """Read the small standard frontmatter subset used by the frozen skill."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append("skills/progressive-clarity/SKILL.md: missing frontmatter")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append("skills/progressive-clarity/SKILL.md: unclosed frontmatter")
        return {}

    fields: dict[str, str] = {}
    current_key: str | None = None
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        if line[0].isspace():
            if current_key is None:
                errors.append(
                    f"skills/progressive-clarity/SKILL.md:{line_number}: "
                    "orphaned frontmatter continuation"
                )
            else:
                fields[current_key] += f"\n{line.strip()}"
            continue
        match = FRONTMATTER_FIELD_PATTERN.fullmatch(line)
        if not match:
            errors.append(
                f"skills/progressive-clarity/SKILL.md:{line_number}: "
                "invalid top-level frontmatter field"
            )
            current_key = None
            continue
        current_key = match.group(1)
        if current_key in fields:
            errors.append(
                f"skills/progressive-clarity/SKILL.md:{line_number}: "
                f"duplicate frontmatter field {current_key}"
            )
        fields[current_key] = match.group(2) or ""
    return fields


def validate_skill_package(errors: list[str]) -> None:
    """Enforce the instruction-only frozen package shape and frontmatter."""
    if not SKILL_DIR.is_dir():
        errors.append("skills/progressive-clarity: missing skill directory")
        return

    actual_files: set[Path] = set()
    for path in SKILL_DIR.rglob("*"):
        relative_path = path.relative_to(SKILL_DIR)
        if path.is_symlink():
            errors.append(
                f"skills/progressive-clarity/{relative_path}: symlink forbidden"
            )
            continue
        if any(part.lower() in {"scripts", "tools"} for part in relative_path.parts):
            errors.append(
                f"skills/progressive-clarity/{relative_path}: scripts/tools forbidden"
            )
        if path.is_file():
            actual_files.add(relative_path)
            if path.stat().st_mode & 0o111:
                errors.append(
                    f"skills/progressive-clarity/{relative_path}: executable bit forbidden"
                )

    if actual_files != EXPECTED_SKILL_FILES:
        missing = sorted(EXPECTED_SKILL_FILES - actual_files)
        unexpected = sorted(actual_files - EXPECTED_SKILL_FILES)
        if missing:
            errors.append(f"skills/progressive-clarity: missing files: {missing}")
        if unexpected:
            errors.append(f"skills/progressive-clarity: unexpected files: {unexpected}")

    skill_path = SKILL_DIR / "SKILL.md"
    if not skill_path.is_file():
        return
    fields = parse_frontmatter(skill_path.read_text(encoding="utf-8"), errors)
    if set(fields) != {"name", "description", "license"}:
        errors.append(
            "skills/progressive-clarity/SKILL.md: frontmatter fields must be "
            "name, description, and license only"
        )
    if fields.get("name") != SKILL_DIR.name:
        errors.append(
            "skills/progressive-clarity/SKILL.md: name must match its directory"
        )
    if fields.get("license") != "Apache-2.0":
        errors.append("skills/progressive-clarity/SKILL.md: license must be Apache-2.0")
    description = fields.get("description", "")
    description = re.sub(r"^(?:>-?|[|]-?)\s*", "", description)
    if not description.strip():
        errors.append(
            "skills/progressive-clarity/SKILL.md: description must not be empty"
        )


def validate_evaluation_suite(errors: list[str]) -> None:
    """Validate JSON syntax and the suite's declared referential constraints."""
    path = ROOT / "evals" / "cases.json"
    try:
        suite = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"evals/cases.json: invalid JSON ({exc})")
        return

    expected_protocol_hash = FROZEN_FILES[Path("SPEC.md")]
    if suite.get("protocol", {}).get("sha256") != expected_protocol_hash:
        errors.append("evals/cases.json: protocol hash does not match frozen SPEC.md")

    policy = suite.get("run_policy", {})
    cases = suite.get("cases", [])
    repeat_ids = policy.get("repeat_case_ids", [])
    if len(repeat_ids) != len(set(repeat_ids)):
        errors.append("evals/cases.json: duplicate repeat_case_ids")

    case_ids: set[str] = set()
    all_fact_ids: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("evals/cases.json: case missing string id")
            continue
        if case_id in case_ids:
            errors.append(f"evals/cases.json: duplicate case id {case_id}")
        case_ids.add(case_id)

        expected_runs = (
            policy.get("repeat_runs_per_host")
            if case_id in repeat_ids
            else policy.get("default_runs_per_host")
        )
        if case.get("runs_per_host") != expected_runs:
            errors.append(
                f"evals/cases.json: {case_id} runs_per_host does not match run policy"
            )

        facts = case.get("source_facts", [])
        fact_ids = [fact.get("id") for fact in facts if isinstance(fact, dict)]
        if len(fact_ids) != len(set(fact_ids)):
            errors.append(f"evals/cases.json: {case_id} has duplicate fact ids")
        duplicates = set(fact_ids) & all_fact_ids
        if duplicates:
            errors.append(
                f"evals/cases.json: globally duplicate fact ids {sorted(duplicates)}"
            )
        all_fact_ids.update(fact_ids)

        turns = case.get("turns", [])
        turn_numbers = [turn.get("turn") for turn in turns if isinstance(turn, dict)]
        if turn_numbers != list(range(1, len(turns) + 1)):
            errors.append(
                f"evals/cases.json: {case_id} turn numbers are not sequential"
            )
        referenced: set[str] = set()
        for turn in turns:
            expected = turn.get("expected", {})
            required = expected.get("required_fact_ids", [])
            optional = expected.get("optional_fact_ids", [])
            references = required + optional
            if len(references) != len(set(references)):
                errors.append(
                    f"evals/cases.json: {case_id} turn {turn.get('turn')} "
                    "has duplicate fact references"
                )
            unknown = set(references) - set(fact_ids)
            if unknown:
                errors.append(
                    f"evals/cases.json: {case_id} turn {turn.get('turn')} "
                    f"references unknown facts {sorted(unknown)}"
                )
            referenced.update(references)
        unused = set(fact_ids) - referenced
        if unused:
            errors.append(
                f"evals/cases.json: {case_id} has unreferenced facts {sorted(unused)}"
            )

    unknown_repeat_ids = set(repeat_ids) - case_ids
    if unknown_repeat_ids:
        errors.append(
            f"evals/cases.json: unknown repeat case ids {sorted(unknown_repeat_ids)}"
        )


def validate_terminology(errors: list[str]) -> None:
    """Keep source and third-party terminology in their documented contexts."""
    checks = (
        (
            re.compile(r"layered(?:\s+|-)brevity", re.IGNORECASE),
            {Path("PROVENANCE.md")},
            "legacy method name",
        ),
        (
            re.compile(
                r"\b(?:smart\s+brevity|axios(?:'s)?|AXIOS HQ LLC)\b", re.IGNORECASE
            ),
            {Path("ACKNOWLEDGEMENTS.md"), Path("LICENSE.md")},
            "third-party terminology",
        ),
    )
    for path in repository_files():
        if path.suffix not in {".json", ".md"}:
            continue
        relative_path = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for pattern, allowed_paths, label in checks:
            if pattern.search(text) and relative_path not in allowed_paths:
                errors.append(f"{relative_path}: {label} appears outside its allowlist")
        if LEGACY_CUE_PATTERN.search(text):
            errors.append(f"{relative_path}: legacy cue label is forbidden")
        if re.search(r"(?i)\bLayer [012]\b|\bSafe to leave\b", text):
            errors.append(f"{relative_path}: legacy layer terminology is forbidden")
        if re.search(r"(?im)^#{1,6}\s+Go deeper\s*$", text):
            errors.append(f"{relative_path}: legacy depth heading is forbidden")


def main() -> int:
    """Run all repository validations and report every failure."""
    errors: list[str] = []
    validate_frozen_files(errors)
    validate_whitespace(errors)
    validate_relative_links(errors)
    validate_skill_package(errors)
    validate_evaluation_suite(errors)
    validate_terminology(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
