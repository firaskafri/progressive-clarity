"""Build and verify the deterministic OpenAI skills-only plugin archive."""

from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"
SKILL_DIR = ROOT / "skills" / "progressive-clarity"
ASSET_DIR = ROOT / "assets"
DIST_DIR = ROOT / "dist"
EXPECTED_MANIFEST_KEYS = {
    "name",
    "version",
    "description",
    "author",
    "skills",
    "interface",
}
EXPECTED_INTERFACE_KEYS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "composerIcon",
    "logo",
}
PUBLISHER_NAME = "FIRAS HASHEM AHMAD AL KAFRI"
ASSET_FIELDS = ("composerIcon", "logo")
EXPECTED_SKILL_FILES = ("SKILL.md", "LICENSE")
MIN_IMAGE_DIMENSION = 48
MAX_IMAGE_DIMENSION = 4096
MAX_IMAGE_BYTES = 5 * 1024 * 1024
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
    """Load and validate the tracked plugin manifest."""
    if MANIFEST_PATH.is_symlink() or not MANIFEST_PATH.is_file():
        raise ValueError("plugin manifest must be a regular file")
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
    author = manifest["author"]
    skills = manifest["skills"]
    interface = manifest["interface"]
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
    if author != {"name": PUBLISHER_NAME}:
        raise ValueError("author.name must match the verified publisher identity")
    if skills != "./skills/":
        raise ValueError("plugin skills must resolve to the root ./skills/ directory")
    if not isinstance(interface, dict) or set(interface) != EXPECTED_INTERFACE_KEYS:
        raise ValueError(
            "plugin interface must contain exactly: "
            + ", ".join(sorted(EXPECTED_INTERFACE_KEYS))
        )
    if interface["developerName"] != PUBLISHER_NAME:
        raise ValueError(
            "interface.developerName must match author.name and the verified identity"
        )
    for field in ("displayName", "shortDescription", "longDescription"):
        value = interface[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"interface.{field} must be a non-empty string")
    if len(interface["shortDescription"]) > 30:
        raise ValueError(
            "interface.shortDescription must meet the 30-character directory limit"
        )
    for field in ASSET_FIELDS:
        asset_path(interface[field])
    return manifest


def asset_path(value: object) -> Path:
    """Resolve one direct asset reference inside the plugin root."""
    if not isinstance(value, str) or not value.startswith("./assets/"):
        raise ValueError("plugin asset paths must start with ./assets/")
    relative_path = Path(value.removeprefix("./"))
    if len(relative_path.parts) != 2 or relative_path.suffix.lower() != ".svg":
        raise ValueError("plugin assets must be direct SVG files under ./assets/")
    resolved = (ROOT / relative_path).resolve()
    if resolved.parent != ASSET_DIR.resolve():
        raise ValueError(f"plugin asset path escapes ./assets/: {value}")
    return resolved


def validate_svg_asset(path: Path) -> None:
    """Validate the documented OpenAI square-image constraints."""
    if path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError(f"plugin asset exceeds 5 MiB: {path}")
    try:
        root = ET.fromstring(path.read_bytes())
    except ET.ParseError as exc:
        raise ValueError(f"plugin asset is not valid XML: {path} ({exc})") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise ValueError(f"plugin asset root must be svg: {path}")

    try:
        width = float(root.attrib["width"])
        height = float(root.attrib["height"])
        view_box = tuple(float(value) for value in root.attrib["viewBox"].split())
    except (KeyError, ValueError) as exc:
        raise ValueError(f"plugin asset dimensions must be numeric: {path}") from exc
    if len(view_box) != 4:
        raise ValueError(f"plugin asset viewBox must contain four numbers: {path}")
    view_width, view_height = view_box[2:]
    if width != height or view_width != view_height or width != view_width:
        raise ValueError(
            f"plugin asset dimensions must be square and consistent: {path}"
        )
    if not MIN_IMAGE_DIMENSION <= width <= MAX_IMAGE_DIMENSION:
        raise ValueError(
            f"plugin asset dimensions must be 48-4096 pixels: {path}"
        )


def source_entries(manifest: dict[str, object]) -> dict[str, bytes]:
    """Return the only files permitted in the published archive."""
    actual_skill_entries = sorted(path.name for path in SKILL_DIR.iterdir())
    if actual_skill_entries != sorted(EXPECTED_SKILL_FILES):
        raise ValueError(
            "canonical skill contents changed; expected only "
            + ", ".join(EXPECTED_SKILL_FILES)
        )

    interface = manifest["interface"]
    if not isinstance(interface, dict):
        raise ValueError("plugin interface must be an object")
    assets = {field: asset_path(interface[field]) for field in ASSET_FIELDS}
    actual_asset_entries = sorted(path.name for path in ASSET_DIR.iterdir())
    expected_asset_entries = sorted(path.name for path in assets.values())
    if actual_asset_entries != expected_asset_entries:
        raise ValueError(
            "plugin asset contents changed; expected only "
            + ", ".join(expected_asset_entries)
        )

    entries = {".codex-plugin/plugin.json": MANIFEST_PATH.read_bytes()}
    for source in assets.values():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"plugin asset must be a regular file: {source}")
        validate_svg_asset(source)
        entries[source.relative_to(ROOT).as_posix()] = source.read_bytes()
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
    """Confirm archive inventory, metadata, and bytes match canonical output."""
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if names != sorted(entries):
            raise ValueError(f"unexpected archive inventory: {names}")
        if archive.comment:
            raise ValueError("archive comment must be empty")
        for name, expected_bytes in entries.items():
            info = archive.getinfo(name)
            if (
                info.date_time != ARCHIVE_TIMESTAMP
                or info.compress_type != zipfile.ZIP_STORED
                or info.create_system != 3
                or info.external_attr >> 16 != 0o100644
                or info.extra
                or info.comment
            ):
                raise ValueError(f"packaged metadata is not normalized: {name}")
            if archive.read(name) != expected_bytes:
                raise ValueError(f"packaged bytes differ from source: {name}")


def main() -> int:
    """Build the archive, verify it, and print its reproducible inventory."""
    manifest = load_manifest()
    entries = source_entries(manifest)
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
