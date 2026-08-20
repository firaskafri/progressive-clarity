"""Build and verify the deterministic OpenAI skills-only plugin archive."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from tools.package_common import (
    RELEASE_VERSION,
    SEMVER_PATTERN,
    load_canonical_skill_source,
    parse_json_object,
    read_regular_file,
    sha256,
    write_archive,
)

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
EXPECTED_PLUGIN_NAME = "progressive-clarity"
ASSET_FIELDS = ("composerIcon", "logo")
MIN_IMAGE_DIMENSION = 48
MAX_IMAGE_DIMENSION = 4096
MAX_IMAGE_BYTES = 5 * 1024 * 1024
FORBIDDEN_SVG_ELEMENTS = frozenset(
    {"a", "foreignobject", "iframe", "image", "script", "style", "use"}
)
PLUGIN_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

def load_manifest() -> tuple[dict[str, object], bytes]:
    """Load and validate the tracked plugin manifest."""
    manifest_bytes = read_regular_file(MANIFEST_PATH, "OpenAI plugin manifest")
    manifest = parse_json_object(manifest_bytes, "OpenAI plugin manifest")
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
    if (
        not isinstance(name, str)
        or not PLUGIN_NAME_PATTERN.fullmatch(name)
        or name != EXPECTED_PLUGIN_NAME
    ):
        raise ValueError("plugin name does not match the canonical package identity")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        raise ValueError("plugin version must be semantic versioning")
    if version != RELEASE_VERSION:
        raise ValueError(f"plugin version must be {RELEASE_VERSION}")
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
    return manifest, manifest_bytes


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


def validate_svg_asset(source: bytes, path: Path) -> None:
    """Validate the documented OpenAI square-image constraints."""
    if len(source) > MAX_IMAGE_BYTES:
        raise ValueError(f"plugin asset exceeds 5 MiB: {path}")
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        raise ValueError(f"plugin asset is not valid XML: {path} ({exc})") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise ValueError(f"plugin asset root must be svg: {path}")
    for element in root.iter():
        element_name = element.tag.rsplit("}", 1)[-1].casefold()
        if element_name in FORBIDDEN_SVG_ELEMENTS:
            raise ValueError(
                f"plugin asset contains active SVG element {element_name}: {path}"
            )
        for attribute, value in element.attrib.items():
            attribute_name = attribute.rsplit("}", 1)[-1].casefold()
            if (
                attribute_name.startswith("on")
                or attribute_name == "href"
                or "url(" in value.casefold()
            ):
                raise ValueError(
                    f"plugin asset contains active SVG attribute: {path}"
                )

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
        raise ValueError(f"plugin asset dimensions must be 48-4096 pixels: {path}")


def source_entries(
    manifest: dict[str, object],
    manifest_bytes: bytes,
) -> dict[str, bytes]:
    """Return the only files permitted in the published archive."""
    if parse_json_object(
        manifest_bytes,
        "OpenAI plugin manifest",
    ) != manifest:
        raise ValueError(
            "OpenAI manifest data and validated bytes do not match"
        )
    if (
        ASSET_DIR.is_symlink()
        or not ASSET_DIR.is_dir()
        or not ASSET_DIR.resolve().is_relative_to(ROOT.resolve())
    ):
        raise ValueError(
            "plugin asset directory must be a regular in-repository "
            f"directory: {ASSET_DIR}"
        )
    canonical = load_canonical_skill_source(SKILL_DIR, root=ROOT)

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

    entries = {".codex-plugin/plugin.json": manifest_bytes}
    for source in assets.values():
        source_bytes = read_regular_file(source, "plugin asset")
        validate_svg_asset(source_bytes, source)
        entries[source.relative_to(ROOT).as_posix()] = source_bytes
    canonical_files = {
        "LICENSE": canonical.license,
        "SKILL.md": canonical.skill,
    }
    for filename, content in canonical_files.items():
        entries[f"skills/progressive-clarity/{filename}"] = content
    return entries

def build_archive(output_dir: Path = DIST_DIR) -> tuple[Path, dict[str, bytes]]:
    """Build, verify, and atomically publish one normalized archive."""
    manifest, manifest_bytes = load_manifest()
    entries = source_entries(manifest, manifest_bytes)
    archive_name = f"{manifest['name']}-openai-plugin-{manifest['version']}.zip"
    archive_path = output_dir / archive_name

    write_archive(archive_path, entries)
    return archive_path, entries


def main(argv: list[str] | None = None) -> int:
    """Build the archive and print its reproducible inventory."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DIST_DIR,
        help="Directory for the generated plugin archive.",
    )
    args = parser.parse_args(argv)

    archive_path, entries = build_archive(args.output_dir.resolve())
    try:
        display_path = archive_path.relative_to(ROOT)
    except ValueError:
        display_path = archive_path
    print(f"archive={display_path}")
    print(f"archive_sha256={sha256(archive_path.read_bytes())}")
    for name in sorted(entries):
        print(f"entry={name} sha256={sha256(entries[name])} bytes={len(entries[name])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
