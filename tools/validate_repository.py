"""Validate the frozen Progressive Clarity repository and skill package."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pc_core.model import (
    AT_A_GLANCE_MAX_NON_WARNING_WORDS,
    THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS,
)
from tools.package_claude_plugin import load_manifest as load_claude_manifest
from tools.package_claude_skill import (
    PACKAGE_VERSION as CLAUDE_SKILL_VERSION,
)
from tools.package_claude_skill import generate_packaged_skill
from tools.package_common import (
    RELEASE_VERSION,
    load_canonical_skill_source,
    parse_json_object,
)
from tools.package_openai_plugin import load_manifest, source_entries


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
PYPROJECT_PATH = ROOT / "pyproject.toml"
FROZEN_FILES = {
    Path("SPEC.md"): (
        "27a75963599cbb156e910d9ee6fc1b6b741c23cde2ddd094bc733edc67443aa7"
    ),
    Path("skills/progressive-clarity/SKILL.md"): (
        "2379f0cf3e8b9ccbfd0a7553b0843097f3fddc764cbc758160b80127377b6c21"
    ),
    Path("evals/cases.json"): (
        "9e10cc2191b33ca7f5a99e4f22659039de1f8c9f563440155175851616fd16d2"
    ),
}
EXPECTED_SCHEMA_VERSION = "5.0.0"
EXPECTED_SUITE_ID = (
    "progressive-clarity-v0.4-topic-oriented-advisory-host-acceptance"
)
EXPECTED_CASE_IDS = tuple(f"T{number:02d}" for number in range(1, 11))
EXPECTED_REPEAT_CASE_IDS = ("T04", "T05")
EXPECTED_TOTALS_PER_HOST = {
    "sessions": 14,
    "scored_assistant_responses": 29,
}
EXPECTED_PACKAGE_VERSION = RELEASE_VERSION
EXPECTED_WORD_COUNT_METHOD = (
    "deterministic-pc-core-v4 for full responses; "
    "focused responses have no protocol hard cap"
)
FACT_REFERENCE_FIELDS = {
    "required_fact_ids",
    "optional_fact_ids",
    "required_step_order",
}
EXPECTED_SKILL_FILES = {Path("LICENSE"), Path("SKILL.md")}
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_NAMES = {".editorconfig", ".gitignore", "LICENSE"}
IGNORED_REPOSITORY_PARTS = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
}
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
TEST_DOCSTRING_FIELDS = ("Name:", "Description:", "Assumptions:", "Expectations:")


def repository_files() -> list[Path]:
    """Return repository files while excluding Git internals."""
    return sorted(
        (
            path
            for path in ROOT.rglob("*")
            if not (
                set(path.relative_to(ROOT).parts) & IGNORED_REPOSITORY_PARTS
            )
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
        anchors = anchor_cache.get(resolved)
        if anchors is None:
            try:
                anchors = markdown_anchors(resolved)
            except (OSError, UnicodeError) as exc:
                errors.append(
                    f"{relative_source}: cannot inspect link target {target}: {exc}"
                )
                return
            anchor_cache[resolved] = anchors
        fragment = unquote(parsed.fragment).lower()
        if fragment not in anchors:
            errors.append(f"{relative_source}: missing link anchor: {target}")


def validate_relative_links(errors: list[str]) -> None:
    """Check relative destinations and anchors in Markdown links."""
    anchor_cache: dict[Path, set[str]] = {}
    for source in sorted(ROOT.rglob("*.md")):
        if set(source.relative_to(ROOT).parts) & IGNORED_REPOSITORY_PARTS:
            continue
        try:
            text = markdown_without_fences(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(
                f"{source.relative_to(ROOT)}: cannot inspect Markdown links: {exc}"
            )
            continue
        matches = list(LINK_PATTERN.finditer(text))
        matches.extend(REFERENCE_LINK_PATTERN.finditer(text))
        for match in matches:
            validate_link(source, match.group("target"), anchor_cache, errors)


def validate_distributions(errors: list[str]) -> None:
    """Validate package inputs and coordinated distribution versions."""
    versions: dict[str, object] = {
        "Claude.ai Skill": CLAUDE_SKILL_VERSION,
    }
    try:
        openai, openai_bytes = load_manifest()
        source_entries(openai, openai_bytes)
    except (OSError, ValueError) as exc:
        errors.append(f"OpenAI plugin: {exc}")
    else:
        versions["OpenAI plugin"] = openai.get("version")

    try:
        claude, _manifest_bytes = load_claude_manifest()
    except (OSError, ValueError) as exc:
        errors.append(f"Claude plugin: {exc}")
    else:
        versions["Claude plugin"] = claude.get("version")

    try:
        canonical = load_canonical_skill_source(SKILL_DIR, root=ROOT)
        generate_packaged_skill(canonical.body)
    except (OSError, ValueError) as exc:
        errors.append(f"Claude.ai Skill: {exc}")

    for label, version in versions.items():
        if version != EXPECTED_PACKAGE_VERSION:
            errors.append(
                f"{label}: version must be {EXPECTED_PACKAGE_VERSION!r}, "
                f"got {version!r}"
            )


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
                    f"skills/progressive-clarity/{relative_path}: "
                    "executable bit forbidden"
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
        suite = parse_json_object(path.read_bytes(), "evals/cases.json")
    except (OSError, ValueError) as exc:
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
    if protocol.get("version") != "0.4":
        errors.append("evals/cases.json: protocol version must be 0.4")
    if protocol.get("sha256") != expected_protocol_hash:
        errors.append("evals/cases.json: protocol hash does not match frozen SPEC.md")

    scope = suite.get("scope")
    if not isinstance(scope, dict):
        errors.append("evals/cases.json: scope must be an object")
        scope = {}
    if scope.get("conformance_surface") != "Advisory prompt-only host behavior":
        errors.append(
            "evals/cases.json: scope must identify Advisory host behavior"
        )
    for field in (
        "human_outcome_claims",
        "semantic_completeness_claims",
        "hidden_state_claims",
    ):
        if scope.get(field) is not False:
            errors.append(f"evals/cases.json: scope.{field} must be false")

    word_count = suite.get("word_count")
    if (
        not isinstance(word_count, dict)
        or word_count.get("method") != EXPECTED_WORD_COUNT_METHOD
    ):
        errors.append(
            "evals/cases.json: word_count method does not match pc-core v4"
        )
        word_count = {}
    expected_budgets = {
        "at_a_glance_max_non_warning_words": (
            AT_A_GLANCE_MAX_NON_WARNING_WORDS
        ),
        "through_in_context_max_non_warning_words_per_response": (
            THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS
        ),
        "at_depth_hard_cap": None,
    }
    if word_count.get("full_budgets") != expected_budgets:
        errors.append(
            "evals/cases.json: full_budgets do not match pc-core constants"
        )

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
            presentation = expected.get("presentation")
            if presentation not in {"focused", "full", "control", "non_fit"}:
                errors.append(
                    f"evals/cases.json: {case_id} turn {turn.get('turn')} "
                    "presentation must be focused, full, control, or non_fit"
                )
            rendered_views = expected.get("rendered_views")
            expected_views = (
                ["At a glance", "In context", "At depth"]
                if presentation == "full"
                else []
            )
            if rendered_views != expected_views:
                errors.append(
                    f"evals/cases.json: {case_id} turn {turn.get('turn')} "
                    f"rendered_views must be {expected_views}"
                )
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
    stale_contract = re.compile(
        r"\b(?:Progressive mode|Verbose mode|sticky mode|one-off view)\b",
        re.IGNORECASE,
    )
    stale_allowlist = {
        Path("docs/openai-plugin.md"),
        Path("docs/verification.md"),
    }
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
        if stale_contract.search(text) and relative_path not in stale_allowlist:
            errors.append(
                f"{relative_path}: removed presentation-state terminology "
                "appears outside historical evidence"
            )


def test_docstring_problem(docstring: str) -> str | None:
    """Return why a test docstring violates the four-field ordered contract."""
    lines = [line.strip() for line in docstring.splitlines() if line.strip()]
    positions: list[int] = []
    for field in TEST_DOCSTRING_FIELDS:
        matches = [
            index for index, line in enumerate(lines) if line.startswith(field)
        ]
        if len(matches) != 1:
            return f"must contain exactly one {field}"
        positions.append(matches[0])
    if positions != sorted(positions):
        return (
            "fields must appear in Name, Description, Assumptions, "
            "Expectations order"
        )
    if positions[0] != 0:
        return "Name must be the first non-empty docstring field"
    return None


def validate_test_docstrings(errors: list[str]) -> None:
    """Require the documented test intent contract at every requested level."""
    tests_dir = ROOT / "tests"
    for path in sorted(tests_dir.glob("*.py")):
        relative_path = path.relative_to(ROOT)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            errors.append(f"{relative_path}: cannot parse tests ({exc})")
            continue
        module_docstring = ast.get_docstring(tree, clean=False) or ""
        problem = test_docstring_problem(module_docstring)
        if problem:
            errors.append(
                f"{relative_path}: module docstring {problem}"
            )
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_docstring = ast.get_docstring(node, clean=False) or ""
                problem = test_docstring_problem(class_docstring)
                if problem:
                    errors.append(
                        f"{relative_path}:{node.lineno}: class {node.name} "
                        f"docstring {problem}"
                    )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("test_"):
                    continue
                case_docstring = ast.get_docstring(node, clean=False) or ""
                problem = test_docstring_problem(case_docstring)
                if problem:
                    errors.append(
                        f"{relative_path}:{node.lineno}: test {node.name} "
                        f"docstring {problem}"
                    )


def validate_python_package(errors: list[str]) -> None:
    """Validate the installable standard-library pc-core package contract."""
    try:
        data = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"pyproject.toml: invalid project metadata ({exc})")
        return
    build = data.get("build-system")
    project = data.get("project")
    tool = data.get("tool")
    hatch = tool.get("hatch") if isinstance(tool, dict) else None
    hatch_build = hatch.get("build") if isinstance(hatch, dict) else None
    targets = (
        hatch_build.get("targets") if isinstance(hatch_build, dict) else None
    )
    wheel = targets.get("wheel") if isinstance(targets, dict) else None
    sdist = targets.get("sdist") if isinstance(targets, dict) else None
    if build != {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",
    }:
        errors.append("pyproject.toml: expected the reviewed hatchling build backend")
    if not isinstance(project, dict):
        errors.append("pyproject.toml: project metadata must be an object")
        return
    expected = {
        "name": "progressive-clarity-core",
        "version": EXPECTED_PACKAGE_VERSION,
        "description": (
            "Deterministic mechanics for topic-oriented Progressive Clarity"
        ),
        "requires-python": ">=3.11",
        "dependencies": [],
        "license": "Apache-2.0",
        "license-files": ["LICENSES/Apache-2.0.txt"],
        "authors": [{"name": "Firas Kafri"}],
        "urls": {
            "Homepage": "https://firaskafri.com/progressive-clarity/",
            "Repository": "https://github.com/firaskafri/progressive-clarity",
        },
        "scripts": {"pc-core": "pc_core.cli:main"},
    }
    for field, expected_value in expected.items():
        if project.get(field) != expected_value:
            errors.append(
                f"pyproject.toml: project.{field} must be {expected_value!r}"
            )
    if wheel != {"packages": ["pc_core"]}:
        errors.append("pyproject.toml: wheel must contain only pc_core")
    if sdist != {
        "include": [
            "/LICENSES/Apache-2.0.txt",
            "/pc_core",
            "/pyproject.toml",
        ]
    }:
        errors.append("pyproject.toml: unexpected sdist inventory")


def _hook_entry(
    hooks: object,
    event: str,
    location: str,
    errors: list[str],
) -> dict[str, object] | None:
    if not isinstance(hooks, dict):
        return None
    entries = hooks.get(event)
    if (
        not isinstance(entries, list)
        or len(entries) != 1
        or not isinstance(entries[0], dict)
    ):
        errors.append(f"{location}.{event}: expected exactly one hook object")
        return None
    return entries[0]


def _read_host_template(
    path: Path,
    label: str,
    errors: list[str],
) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: invalid JSON ({exc})")
        return None


def _validate_cursor_template(cursor: object, errors: list[str]) -> None:
    if (
        not isinstance(cursor, dict)
        or set(cursor) != {"version", "hooks"}
        or cursor.get("version") != 1
    ):
        errors.append(
            "adapters/cursor/hooks.json: expected version and hooks only"
        )
    cursor_hooks = cursor.get("hooks") if isinstance(cursor, dict) else None
    if not isinstance(cursor_hooks, dict) or set(cursor_hooks) != {
        "afterAgentResponse",
        "stop",
    }:
        errors.append(
            "adapters/cursor/hooks.json: expected afterAgentResponse and stop only"
        )
    cursor_after = _hook_entry(
        cursor_hooks,
        "afterAgentResponse",
        "adapters/cursor/hooks.json",
        errors,
    )
    expected_after = {
        "command": ".pc-core/venv/bin/pc-core hook cursor-after-response",
        "timeout": 10,
    }
    if cursor_after is not None and cursor_after != expected_after:
        errors.append(
            "adapters/cursor/hooks.json: invalid afterAgentResponse hook"
        )
    cursor_stop = _hook_entry(
        cursor_hooks,
        "stop",
        "adapters/cursor/hooks.json",
        errors,
    )
    expected_stop = {
        "command": ".pc-core/venv/bin/pc-core hook cursor-stop",
        "loop_limit": 1,
        "timeout": 10,
    }
    if cursor_stop is not None and cursor_stop != expected_stop:
        errors.append("adapters/cursor/hooks.json: invalid bounded stop hook")


def _validate_claude_template(claude: object, errors: list[str]) -> None:
    if not isinstance(claude, dict) or set(claude) != {"$schema", "hooks"}:
        errors.append(
            "adapters/claude-code/settings.json: expected $schema and hooks only"
        )
        return
    claude_hooks = claude.get("hooks")
    if not isinstance(claude_hooks, dict) or set(claude_hooks) != {"Stop"}:
        errors.append(
            "adapters/claude-code/settings.json: expected one Stop hook"
        )
        return
    if claude.get("$schema") != (
        "https://json.schemastore.org/claude-code-settings.json"
    ):
        errors.append("adapters/claude-code/settings.json: unexpected $schema")
    stop_groups = claude_hooks["Stop"]
    if (
        not isinstance(stop_groups, list)
        or len(stop_groups) != 1
        or not isinstance(stop_groups[0], dict)
        or set(stop_groups[0]) != {"hooks"}
    ):
        errors.append(
            "adapters/claude-code/settings.json: expected one Stop hook group"
        )
        return
    claude_stop = _hook_entry(
        {"Stop": stop_groups[0]["hooks"]},
        "Stop",
        "adapters/claude-code/settings.json",
        errors,
    )
    expected_claude_stop = {
        "type": "command",
        "command": ".pc-core/venv/bin/pc-core hook claude-stop",
        "timeout": 10,
    }
    if claude_stop is not None and claude_stop != expected_claude_stop:
        errors.append("adapters/claude-code/settings.json: invalid Stop hook")


def validate_host_templates(errors: list[str]) -> None:
    """Validate project-local Cursor and Claude hook schemas independently."""
    templates = (
        (
            ROOT / "adapters" / "cursor" / "hooks.json",
            "adapters/cursor/hooks.json",
            _validate_cursor_template,
        ),
        (
            ROOT / "adapters" / "claude-code" / "settings.json",
            "adapters/claude-code/settings.json",
            _validate_claude_template,
        ),
    )
    for path, label, validate in templates:
        template = _read_host_template(path, label, errors)
        if template is not None:
            validate(template, errors)


def main() -> int:
    """Run all repository validations and report every failure."""
    errors: list[str] = []
    validate_frozen_files(errors)
    validate_whitespace(errors)
    validate_relative_links(errors)
    validate_distributions(errors)
    validate_skill_package(errors)
    validate_evaluation_suite(errors)
    validate_terminology(errors)
    validate_test_docstrings(errors)
    validate_python_package(errors)
    validate_host_templates(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
