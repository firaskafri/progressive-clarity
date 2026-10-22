"""Build and verify the deterministic Claude plugin archive."""

from __future__ import annotations

import re
import struct
import zlib
from pathlib import Path

from tools.package_common import (
    CANONICAL_LICENSE,
    RELEASE_VERSION,
    SEMVER_PATTERN,
    load_canonical_skill_source,
    parse_json_object,
    print_archive_report,
    read_regular_file,
    write_archive,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".claude-plugin" / "plugin.json"
ICON_PATH = ROOT / ".claude-plugin" / "icon.png"
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
DIST_DIR = ROOT / "dist"
PLUGIN_NAME = "progressive-clarity"
AUTHOR = {
    "name": "Firas Kafri",
    "url": "https://github.com/firaskafri",
}
HOMEPAGE = "https://firaskafri.com/progressive-clarity/"
REPOSITORY = "https://github.com/firaskafri/progressive-clarity"
LICENSE = CANONICAL_LICENSE
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
PLUGIN_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_ICON_BYTES = 2_000_000


def load_manifest() -> tuple[dict[str, object], bytes]:
    """Load and validate the tracked Claude plugin manifest."""
    manifest_bytes = read_regular_file(MANIFEST_PATH, "Claude plugin manifest")
    manifest = parse_json_object(manifest_bytes, "Claude plugin manifest")
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
    if version != RELEASE_VERSION:
        raise ValueError(f"plugin version must be {RELEASE_VERSION}")
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


def load_icon() -> bytes:
    """Check the directory icon's PNG header, dimensions, and size limit."""
    content = read_regular_file(ICON_PATH, "Claude plugin icon")
    if len(content) >= MAX_ICON_BYTES:
        raise ValueError("Claude plugin icon must be under 2 MB")
    if (
        len(content) < 45
        or content[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        or content[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82"
        or zlib.crc32(content[12:29]) != struct.unpack(">I", content[29:33])[0]
    ):
        raise ValueError("Claude plugin icon must have a valid PNG header and trailer")
    width, height = struct.unpack(">II", content[16:24])
    if width != height or not 512 <= width <= 2048:
        raise ValueError("Claude plugin icon must be square and 512-2048 pixels")
    return content


def source_entries(
    manifest: dict[str, object], manifest_bytes: bytes,
) -> dict[str, bytes]:
    """Select only the validated prompt-only plugin inputs and listing icon."""
    if parse_json_object(manifest_bytes, "Claude plugin manifest") != manifest:
        raise ValueError("Claude manifest data and validated bytes do not match")
    canonical = load_canonical_skill_source(SKILL_DIR, root=ROOT)
    return {
        ".claude-plugin/icon.png": load_icon(),
        ".claude-plugin/plugin.json": manifest_bytes,
        "skills/progressive-clarity/LICENSE": canonical.license,
        "skills/progressive-clarity/SKILL.md": canonical.skill,
    }


def main() -> int:
    """Build the plugin archive and print its reproducible inventory."""
    manifest, manifest_bytes = load_manifest()
    entries = source_entries(manifest, manifest_bytes)
    archive_path = (
        DIST_DIR
        / f"{manifest['name']}-claude-plugin-{manifest['version']}.zip"
    )
    write_archive(archive_path, entries)
    print_archive_report(ROOT, archive_path, entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
