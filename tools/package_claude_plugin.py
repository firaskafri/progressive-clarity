"""Build and verify the deterministic Claude plugin archive."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.package_claude_common import (
    build_archive,
    parse_simple_frontmatter,
    print_archive_report,
    read_regular_file,
    split_skill,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".claude-plugin" / "plugin.json"
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
DIST_DIR = ROOT / "dist"
PLUGIN_NAME = "progressive-clarity"
AUTHOR = {
    "name": "Firas Kafri",
    "url": "https://github.com/firaskafri",
}
HOMEPAGE = "https://github.com/firaskafri/progressive-clarity#readme"
REPOSITORY = "https://github.com/firaskafri/progressive-clarity"
LICENSE = "Apache-2.0"
SKILLS_PATH = "./skills/progressive-clarity/"
EXPECTED_MANIFEST_KEYS = {
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "skills",
}
EXPECTED_SKILL_FILES = ("LICENSE", "SKILL.md")
PLUGIN_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def load_manifest() -> tuple[dict[str, object], bytes]:
    """Load and validate the tracked Claude plugin manifest."""
    manifest_bytes = read_regular_file(MANIFEST_PATH, "Claude plugin manifest")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Claude plugin manifest must be a JSON object")
    if set(manifest) != EXPECTED_MANIFEST_KEYS:
        raise ValueError(
            "Claude plugin manifest must contain exactly the supported fields: "
            + ", ".join(sorted(EXPECTED_MANIFEST_KEYS))
        )

    name = manifest["name"]
    version = manifest["version"]
    description = manifest["description"]
    keywords = manifest["keywords"]
    if (
        not isinstance(name, str)
        or len(name) > 64
        or not PLUGIN_NAME_PATTERN.fullmatch(name)
    ):
        raise ValueError("plugin name must be 1-64 lowercase kebab-case characters")
    if name != PLUGIN_NAME:
        raise ValueError(f"plugin name must remain {PLUGIN_NAME!r}")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        raise ValueError("plugin version must use semantic versioning")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("plugin description must be a non-empty string")
    if (
        not isinstance(keywords, list)
        or not keywords
        or any(not isinstance(value, str) or not value for value in keywords)
    ):
        raise ValueError("plugin keywords must be a non-empty string array")

    expected_values: dict[str, object] = {
        "author": AUTHOR,
        "homepage": HOMEPAGE,
        "repository": REPOSITORY,
        "license": LICENSE,
        "skills": SKILLS_PATH,
    }
    for field, expected in expected_values.items():
        if manifest[field] != expected:
            raise ValueError(f"plugin {field} must be {expected!r}")

    return manifest, manifest_bytes


def load_canonical_skill() -> tuple[bytes, bytes]:
    """Validate and read the canonical skill and license without modification."""
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
    if set(frontmatter) != {"name", "description", "license"}:
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

    return skill_bytes, license_bytes


def main() -> int:
    """Build the plugin archive and print its reproducible inventory."""
    manifest, manifest_bytes = load_manifest()
    skill_bytes, license_bytes = load_canonical_skill()
    entries = {
        ".claude-plugin/plugin.json": manifest_bytes,
        "skills/progressive-clarity/LICENSE": license_bytes,
        "skills/progressive-clarity/SKILL.md": skill_bytes,
    }
    archive_path = (
        DIST_DIR
        / f"{manifest['name']}-claude-plugin-{manifest['version']}.zip"
    )
    build_archive(archive_path, entries)
    print_archive_report(ROOT, archive_path, entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
