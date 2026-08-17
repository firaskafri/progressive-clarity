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
    Path("SPEC.md"): "ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d",
    Path("skills/progressive-clarity/SKILL.md"): (
        "5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562"
    ),
    Path("evals/cases.json"): (
        "4c27a740e2e02e54f97889618397a6417c82e089b9bb44919b92642e59289680"
    ),
}
EXPECTED_SCHEMA_VERSION = "2.0.0"
EXPECTED_SUITE_ID = "progressive-clarity-v0.1-two-mode-acceptance"
EXPECTED_CASE_IDS = tuple(f"M{number:02d}" for number in range(1, 12))
EXPECTED_REPEAT_CASE_IDS = ("M02", "M05", "M06", "M08", "M11")
EXPECTED_TOTALS_PER_HOST = {
    "sessions": 21,
    "scored_assistant_responses": 39,
}
EXPECTED_TOTALS_BOTH_HOSTS = {
    "sessions": 42,
    "scored_assistant_responses": 78,
}
FACT_REFERENCE_FIELDS = {
    "required_fact_ids",
    "optional_fact_ids",
    "required_step_order",
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


def validate_fact_references(
    node: object,
    location: str,
    fact_ids: set[str],
    referenced: set[str],
    errors: list[str],
) -> None:
    """Validate every fact-reference list, including nested stopping points."""
    if isinstance(node, list):
        for index, item in enumerate(node):
            validate_fact_references(
                item,
                f"{location}[{index}]",
                fact_ids,
                referenced,
                errors,
            )
        return
    if not isinstance(node, dict):
        return

    required = node.get("required_fact_ids")
    optional = node.get("optional_fact_ids")
    if isinstance(required, list) and isinstance(optional, list):
        overlap = {
            value
            for value in required
            if isinstance(value, str) and value in optional
        }
        if overlap:
            errors.append(
                f"evals/cases.json: {location} repeats facts as required and "
                f"optional {sorted(overlap)}"
            )

    for key, value in node.items():
        child_location = f"{location}.{key}"
        if key not in FACT_REFERENCE_FIELDS:
            validate_fact_references(
                value,
                child_location,
                fact_ids,
                referenced,
                errors,
            )
            continue
        if not isinstance(value, list):
            errors.append(
                f"evals/cases.json: {child_location} must be a fact-id list"
            )
            continue
        references = [
            reference
            for reference in value
            if isinstance(reference, str) and reference
        ]
        if len(references) != len(value):
            errors.append(
                f"evals/cases.json: {child_location} contains a non-string "
                "or empty fact reference"
            )
        if len(references) != len(set(references)):
            errors.append(
                f"evals/cases.json: {child_location} has duplicate fact references"
            )
        unknown = set(references) - fact_ids
        if unknown:
            errors.append(
                f"evals/cases.json: {child_location} references unknown facts "
                f"{sorted(unknown)}"
            )
        referenced.update(references)


def validate_evaluation_suite(errors: list[str]) -> None:
    """Validate the frozen schema, totals, and referential constraints."""
    path = ROOT / "evals" / "cases.json"
    try:
        suite = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"evals/cases.json: invalid JSON ({exc})")
        return

    if suite.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        errors.append(
            "evals/cases.json: schema_version must be "
            f"{EXPECTED_SCHEMA_VERSION}"
        )
    if suite.get("suite_id") != EXPECTED_SUITE_ID:
        errors.append(f"evals/cases.json: suite_id must be {EXPECTED_SUITE_ID}")

    expected_protocol_hash = FROZEN_FILES[Path("SPEC.md")]
    protocol = suite.get("protocol")
    if not isinstance(protocol, dict):
        errors.append("evals/cases.json: protocol must be an object")
        protocol = {}
    if protocol.get("path") != "SPEC.md":
        errors.append("evals/cases.json: protocol path must be SPEC.md")
    if protocol.get("version") != "0.1 draft":
        errors.append("evals/cases.json: protocol version must be 0.1 draft")
    if protocol.get("sha256") != expected_protocol_hash:
        errors.append("evals/cases.json: protocol hash does not match frozen SPEC.md")

    policy = suite.get("run_policy")
    if not isinstance(policy, dict):
        errors.append("evals/cases.json: run_policy must be an object")
        policy = {}
    cases = suite.get("cases")
    if not isinstance(cases, list):
        errors.append("evals/cases.json: cases must be a list")
        return
    repeat_ids = policy.get("repeat_case_ids", [])
    if not isinstance(repeat_ids, list) or not all(
        isinstance(case_id, str) for case_id in repeat_ids
    ):
        errors.append("evals/cases.json: repeat_case_ids must be a string list")
        repeat_ids = []
    if len(repeat_ids) != len(set(repeat_ids)):
        errors.append("evals/cases.json: duplicate repeat_case_ids")
    if tuple(repeat_ids) != EXPECTED_REPEAT_CASE_IDS:
        errors.append(
            "evals/cases.json: repeat_case_ids must be "
            f"{list(EXPECTED_REPEAT_CASE_IDS)}"
        )

    case_id_sequence: list[str] = []
    all_fact_ids: set[str] = set()
    computed_sessions = 0
    computed_responses = 0
    for case_index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(
                f"evals/cases.json: cases[{case_index}] must be an object"
            )
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("evals/cases.json: case missing string id")
            continue
        if case_id in case_id_sequence:
            errors.append(f"evals/cases.json: duplicate case id {case_id}")
        case_id_sequence.append(case_id)

        expected_runs = (
            policy.get("repeat_runs_per_host")
            if case_id in repeat_ids
            else policy.get("default_runs_per_host")
        )
        if case.get("runs_per_host") != expected_runs:
            errors.append(
                f"evals/cases.json: {case_id} runs_per_host does not match run policy"
            )
        runs_per_host = case.get("runs_per_host")
        if (
            not isinstance(runs_per_host, int)
            or isinstance(runs_per_host, bool)
            or runs_per_host < 1
        ):
            errors.append(
                f"evals/cases.json: {case_id} runs_per_host must be a positive integer"
            )
            runs_per_host = 0
        computed_sessions += runs_per_host

        facts = case.get("source_facts", [])
        if not isinstance(facts, list):
            errors.append(
                f"evals/cases.json: {case_id} source_facts must be a list"
            )
            facts = []
        fact_ids: list[str] = []
        for fact_index, fact in enumerate(facts):
            if not isinstance(fact, dict):
                errors.append(
                    f"evals/cases.json: {case_id} source_facts[{fact_index}] "
                    "must be an object"
                )
                continue
            fact_id = fact.get("id")
            fact_text = fact.get("text")
            if not isinstance(fact_id, str) or not fact_id:
                errors.append(
                    f"evals/cases.json: {case_id} source_facts[{fact_index}] "
                    "missing string id"
                )
            else:
                fact_ids.append(fact_id)
            if not isinstance(fact_text, str) or not fact_text:
                errors.append(
                    f"evals/cases.json: {case_id} source_facts[{fact_index}] "
                    "missing string text"
                )
        if len(fact_ids) != len(set(fact_ids)):
            errors.append(f"evals/cases.json: {case_id} has duplicate fact ids")
        duplicates = set(fact_ids) & all_fact_ids
        if duplicates:
            errors.append(
                f"evals/cases.json: globally duplicate fact ids {sorted(duplicates)}"
            )
        all_fact_ids.update(fact_ids)

        turns = case.get("turns", [])
        if not isinstance(turns, list):
            errors.append(f"evals/cases.json: {case_id} turns must be a list")
            turns = []
        computed_responses += runs_per_host * len(turns)
        turn_numbers = [
            turn.get("turn") if isinstance(turn, dict) else None for turn in turns
        ]
        if turn_numbers != list(range(1, len(turns) + 1)):
            errors.append(
                f"evals/cases.json: {case_id} turn numbers are not sequential"
            )
        referenced: set[str] = set()
        for turn_index, turn in enumerate(turns):
            if not isinstance(turn, dict):
                errors.append(
                    f"evals/cases.json: {case_id} turns[{turn_index}] "
                    "must be an object"
                )
                continue
            expected = turn.get("expected", {})
            if not isinstance(expected, dict):
                errors.append(
                    f"evals/cases.json: {case_id} turn {turn.get('turn')} "
                    "expected must be an object"
                )
                continue
            validate_fact_references(
                expected,
                f"{case_id} turn {turn.get('turn')} expected",
                set(fact_ids),
                referenced,
                errors,
            )
        unused = set(fact_ids) - referenced
        if unused:
            errors.append(
                f"evals/cases.json: {case_id} has unreferenced facts {sorted(unused)}"
            )

    if tuple(case_id_sequence) != EXPECTED_CASE_IDS:
        errors.append(
            "evals/cases.json: case ids must be "
            f"{list(EXPECTED_CASE_IDS)} in order"
        )
    case_ids = set(case_id_sequence)
    unknown_repeat_ids = set(repeat_ids) - case_ids
    if unknown_repeat_ids:
        errors.append(
            f"evals/cases.json: unknown repeat case ids {sorted(unknown_repeat_ids)}"
        )

    computed_per_host = {
        "sessions": computed_sessions,
        "scored_assistant_responses": computed_responses,
    }
    if computed_per_host != EXPECTED_TOTALS_PER_HOST:
        errors.append(
            "evals/cases.json: cases compute unexpected per-host totals "
            f"{computed_per_host}"
        )
    if policy.get("initial_round_totals_per_host") != EXPECTED_TOTALS_PER_HOST:
        errors.append(
            "evals/cases.json: initial_round_totals_per_host must be "
            f"{EXPECTED_TOTALS_PER_HOST}"
        )
    if policy.get("initial_round_totals_both_hosts") != EXPECTED_TOTALS_BOTH_HOSTS:
        errors.append(
            "evals/cases.json: initial_round_totals_both_hosts must be "
            f"{EXPECTED_TOTALS_BOTH_HOSTS}"
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
