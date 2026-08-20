"""Build and verify the deterministic Claude.ai custom-Skill archive."""

from __future__ import annotations

from pathlib import Path

from tools.package_common import (
    CANONICAL_LICENSE,
    CANONICAL_SKILL_FIELDS,
    RELEASE_VERSION,
    load_canonical_skill_source,
    parse_simple_frontmatter,
    print_archive_report,
    sha256,
    split_skill,
    write_archive,
)

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
DIST_DIR = ROOT / "dist"
SKILL_NAME = "progressive-clarity"
PACKAGE_VERSION = RELEASE_VERSION
LICENSE = CANONICAL_LICENSE
PACKAGED_DESCRIPTION = (
    "Topic-oriented clarity for facts and explained controlling text. Keep simple "
    "facts focused; use three views with predominantly new deeper information for "
    "orientation and checkpoints."
)
CLAUDE_AI_DESCRIPTION_LIMIT = 200


def generate_packaged_skill(canonical_body: bytes) -> bytes:
    """Generate the Claude.ai frontmatter while preserving the canonical body."""
    if not isinstance(canonical_body, bytes) or not canonical_body.strip():
        raise ValueError("canonical Skill body must be non-empty bytes")
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
    ).encode()
    packaged_skill = frontmatter + canonical_body
    generated_frontmatter_bytes, generated_body = split_skill(packaged_skill)
    generated_frontmatter = parse_simple_frontmatter(generated_frontmatter_bytes)

    if set(generated_frontmatter) != CANONICAL_SKILL_FIELDS:
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
    canonical = load_canonical_skill_source(SKILL_DIR, root=ROOT)
    packaged_skill = generate_packaged_skill(canonical.body)
    entries = {
        "progressive-clarity/LICENSE": canonical.license,
        "progressive-clarity/SKILL.md": packaged_skill,
    }
    archive_path = DIST_DIR / f"{SKILL_NAME}-claude-ai-skill-{PACKAGE_VERSION}.zip"
    write_archive(archive_path, entries)

    print(f"packaged_description={PACKAGED_DESCRIPTION}")
    print(f"packaged_description_chars={len(PACKAGED_DESCRIPTION)}")
    print(
        "canonical_description_chars="
        f"{len(canonical.frontmatter['description'])}"
    )
    print(f"canonical_skill_sha256={sha256(canonical.skill)}")
    print(f"canonical_body_sha256={sha256(canonical.body)}")
    print(f"packaged_body_sha256={sha256(split_skill(packaged_skill)[1])}")
    print(f"canonical_license_sha256={sha256(canonical.license)}")
    print_archive_report(ROOT, archive_path, entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
