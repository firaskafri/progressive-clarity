"""Build and verify the deterministic Claude.ai custom-Skill archive."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.package_claude_common import (
    build_archive,
    parse_simple_frontmatter,
    print_archive_report,
    read_regular_file,
    sha256,
    split_skill,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".claude-plugin" / "plugin.json"
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
DIST_DIR = ROOT / "dist"
SKILL_NAME = "progressive-clarity"
LICENSE = "Apache-2.0"
PACKAGED_DESCRIPTION = (
    "Use for ordinary user-facing factual answers, explanations, recommendations, "
    "comparisons, decisions, status updates, and summaries that need three concise, "
    "additive views with safe stopping points."
)
CLAUDE_AI_DESCRIPTION_LIMIT = 200
ALLOWED_CLAUDE_AI_FIELDS = {"name", "description", "license"}
EXPECTED_SKILL_FILES = ("LICENSE", "SKILL.md")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def load_package_version() -> str:
    """Read the package version shared with the Claude plugin manifest."""
    manifest_bytes = read_regular_file(MANIFEST_PATH, "Claude plugin manifest")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if not isinstance(manifest, dict) or manifest.get("name") != SKILL_NAME:
        raise ValueError("Claude plugin manifest name must match the skill")
    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        raise ValueError("Claude plugin manifest version must use semantic versioning")
    return version


def load_canonical_source() -> tuple[bytes, bytes, bytes, dict[str, str]]:
    """Read and validate the canonical skill inputs without changing them."""
    if SKILL_DIR.is_symlink() or not SKILL_DIR.is_dir():
        raise ValueError(f"canonical skill directory must be a directory: {SKILL_DIR}")
    actual_entries = sorted(path.name for path in SKILL_DIR.iterdir())
    if actual_entries != sorted(EXPECTED_SKILL_FILES):
        raise ValueError(
            "canonical skill directory must contain exactly: "
            + ", ".join(EXPECTED_SKILL_FILES)
        )

    skill_bytes = read_regular_file(SKILL_DIR / "SKILL.md", "canonical SKILL.md")
    license_bytes = read_regular_file(SKILL_DIR / "LICENSE", "canonical LICENSE")
    frontmatter_bytes, body_bytes = split_skill(skill_bytes)
    frontmatter = parse_simple_frontmatter(frontmatter_bytes)
    if set(frontmatter) != ALLOWED_CLAUDE_AI_FIELDS:
        raise ValueError(
            "canonical skill frontmatter must contain name, description, and license"
        )
    if frontmatter["name"] != SKILL_DIR.name:
        raise ValueError("canonical skill name must match its parent directory")
    if not 1 <= len(frontmatter["description"]) <= 1024:
        raise ValueError("canonical skill description must contain 1-1024 characters")
    if frontmatter["license"] != LICENSE:
        raise ValueError(f"canonical skill license must be {LICENSE}")
    if not body_bytes.strip():
        raise ValueError("canonical skill body must not be empty")
    return skill_bytes, body_bytes, license_bytes, frontmatter


def generate_packaged_skill(canonical_body: bytes) -> bytes:
    """Generate the Claude.ai frontmatter while preserving the canonical body."""
    if not 1 <= len(PACKAGED_DESCRIPTION) <= CLAUDE_AI_DESCRIPTION_LIMIT:
        raise ValueError(
            "packaged description must contain no more than "
            f"{CLAUDE_AI_DESCRIPTION_LIMIT} characters"
        )

    frontmatter = (
        "---\n"
        f"name: {SKILL_NAME}\n"
        f"description: {PACKAGED_DESCRIPTION}\n"
        f"license: {LICENSE}\n"
        "---\n"
    ).encode("utf-8")
    packaged_skill = frontmatter + canonical_body
    generated_frontmatter_bytes, generated_body = split_skill(packaged_skill)
    generated_frontmatter = parse_simple_frontmatter(generated_frontmatter_bytes)

    if set(generated_frontmatter) != ALLOWED_CLAUDE_AI_FIELDS:
        raise ValueError("packaged skill contains unsupported Claude.ai frontmatter")
    if generated_frontmatter["name"] != SKILL_NAME:
        raise ValueError("packaged skill name must match its root folder")
    if generated_frontmatter["description"] != PACKAGED_DESCRIPTION:
        raise ValueError("packaged skill description changed during generation")
    if generated_frontmatter["license"] != LICENSE:
        raise ValueError("packaged skill license metadata changed during generation")
    if generated_body != canonical_body:
        raise ValueError("packaged skill body differs from the canonical body")

    return packaged_skill


def main() -> int:
    """Build the custom-Skill archive and print its reproducible inventory."""
    version = load_package_version()
    canonical_skill, canonical_body, license_bytes, canonical_frontmatter = (
        load_canonical_source()
    )
    packaged_skill = generate_packaged_skill(canonical_body)
    entries = {
        "progressive-clarity/LICENSE": license_bytes,
        "progressive-clarity/SKILL.md": packaged_skill,
    }
    archive_path = DIST_DIR / f"{SKILL_NAME}-claude-ai-skill-{version}.zip"
    build_archive(archive_path, entries)

    print(f"packaged_description={PACKAGED_DESCRIPTION}")
    print(f"packaged_description_chars={len(PACKAGED_DESCRIPTION)}")
    print(f"canonical_description_chars={len(canonical_frontmatter['description'])}")
    print(f"canonical_skill_sha256={sha256(canonical_skill)}")
    print(f"canonical_body_sha256={sha256(canonical_body)}")
    print(f"packaged_body_sha256={sha256(split_skill(packaged_skill)[1])}")
    print(f"canonical_license_sha256={sha256(license_bytes)}")
    print_archive_report(ROOT, archive_path, entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
