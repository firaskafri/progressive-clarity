"""Build and verify the deterministic OpenAI skills-only plugin archive."""

from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
DIST_DIR = ROOT / "dist"
EXPECTED_MANIFEST_KEYS = {"name", "version", "description", "skills"}
EXPECTED_SKILL_FILES = ("SKILL.md", "LICENSE")
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
PLUGIN_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def sha256(data: bytes) -> str:
    """Return the SHA-256 digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict[str, object]:
    """Load and validate the tracked minimal plugin manifest."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("plugin manifest must be a JSON object")
    if set(manifest) != EXPECTED_MANIFEST_KEYS:
        raise ValueError(
            "plugin manifest must contain exactly: "
            + ", ".join(sorted(EXPECTED_MANIFEST_KEYS))
        )

    name = manifest["name"]
    version = manifest["version"]
    description = manifest["description"]
    skills = manifest["skills"]
    if not isinstance(name, str) or not PLUGIN_NAME_PATTERN.fullmatch(name):
        raise ValueError("plugin name does not meet OpenAI package-name rules")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        raise ValueError("plugin version must be semantic versioning")
    if (
        not isinstance(description, str)
        or not description.strip()
        or len(description) > 1024
    ):
        raise ValueError("plugin description must contain 1-1024 characters")
    if skills != "./skills/":
        raise ValueError("plugin skills must resolve to the root ./skills/ directory")
    return manifest


def source_entries() -> dict[str, bytes]:
    """Return the only files permitted in the published archive."""
    actual_skill_entries = sorted(path.name for path in SKILL_DIR.iterdir())
    if actual_skill_entries != sorted(EXPECTED_SKILL_FILES):
        raise ValueError(
            "canonical skill contents changed; expected only "
            + ", ".join(EXPECTED_SKILL_FILES)
        )

    entries = {
        ".codex-plugin/plugin.json": MANIFEST_PATH.read_bytes(),
    }
    for filename in EXPECTED_SKILL_FILES:
        source = SKILL_DIR / filename
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"canonical skill source must be a regular file: {source}")
        entries[f"skills/progressive-clarity/{filename}"] = source.read_bytes()
    return entries


def zip_info(name: str) -> zipfile.ZipInfo:
    """Create normalized ZIP metadata for one regular file."""
    info = zipfile.ZipInfo(name, date_time=ARCHIVE_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = (0o100644 & 0xFFFF) << 16
    return info


def verify_archive(archive_path: Path, entries: dict[str, bytes]) -> None:
    """Confirm archive paths and bytes exactly match the tracked sources."""
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if names != sorted(entries):
            raise ValueError(f"unexpected archive inventory: {names}")
        for name, expected_bytes in entries.items():
            if archive.read(name) != expected_bytes:
                raise ValueError(f"packaged bytes differ from source: {name}")


def main() -> int:
    """Build the archive, verify it, and print its reproducible inventory."""
    manifest = load_manifest()
    entries = source_entries()
    archive_name = f"{manifest['name']}-openai-plugin-{manifest['version']}.zip"
    archive_path = DIST_DIR / archive_name
    temporary_path = archive_path.with_suffix(".zip.tmp")

    DIST_DIR.mkdir(exist_ok=True)
    try:
        with zipfile.ZipFile(temporary_path, mode="w") as archive:
            for name in sorted(entries):
                archive.writestr(zip_info(name), entries[name])
        os.replace(temporary_path, archive_path)
    finally:
        temporary_path.unlink(missing_ok=True)

    verify_archive(archive_path, entries)
    print(f"archive={archive_path.relative_to(ROOT)}")
    print(f"archive_sha256={sha256(archive_path.read_bytes())}")
    for name in sorted(entries):
        print(f"entry={name} sha256={sha256(entries[name])} bytes={len(entries[name])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
