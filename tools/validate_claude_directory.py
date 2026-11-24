"""Validate the isolated source submitted to Anthropic's plugin directory."""

from __future__ import annotations

import re
from pathlib import Path

from tools.package_common import parse_json_object, read_regular_file


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY_ROOT = ROOT / "claude-directory" / "progressive-clarity"
DIRECTORY_VERSION = "0.5.2"
EXPECTED_FILES = frozenset(
    {
        ".claude-plugin/icon.png",
        ".claude-plugin/plugin.json",
        "README.md",
        "skills/progressive-clarity/LICENSE",
        "skills/progressive-clarity/SKILL.md",
    }
)
README_WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")


def _regular_file_inventory(directory_root: Path) -> set[str]:
    """Return the relative regular-file inventory without following links."""
    if directory_root.is_symlink() or not directory_root.is_dir():
        raise ValueError("Claude directory source must be a regular directory")

    files: set[str] = set()
    for path in directory_root.rglob("*"):
        if path.is_symlink():
            raise ValueError(
                "Claude directory source must not contain symbolic links: "
                f"{path.relative_to(directory_root)}"
            )
        if path.is_file():
            files.add(path.relative_to(directory_root).as_posix())
        elif not path.is_dir():
            raise ValueError(
                "Claude directory source contains an unsupported entry: "
                f"{path.relative_to(directory_root)}"
            )
    return files


def validate_directory_source(root: Path = ROOT) -> None:
    """Require a minimal, copy-verified, scanner-safe directory source."""
    directory_root = root / "claude-directory" / "progressive-clarity"
    inventory = _regular_file_inventory(directory_root)
    if inventory != EXPECTED_FILES:
        raise ValueError(
            "Claude directory source inventory differs: "
            f"expected {sorted(EXPECTED_FILES)}, got {sorted(inventory)}"
        )

    root_manifest_bytes = read_regular_file(
        root / ".claude-plugin" / "plugin.json",
        "repository Claude plugin manifest",
    )
    directory_manifest_bytes = read_regular_file(
        directory_root / ".claude-plugin" / "plugin.json",
        "directory Claude plugin manifest",
    )
    root_manifest = parse_json_object(
        root_manifest_bytes,
        "repository Claude plugin manifest",
    )
    directory_manifest = parse_json_object(
        directory_manifest_bytes,
        "directory Claude plugin manifest",
    )
    expected_manifest = dict(root_manifest)
    expected_manifest["version"] = DIRECTORY_VERSION
    if directory_manifest != expected_manifest:
        raise ValueError(
            "directory manifest must match the repository manifest except for "
            f"version {DIRECTORY_VERSION}"
        )

    identical_files = {
        ".claude-plugin/icon.png": ".claude-plugin/icon.png",
        "skills/progressive-clarity/LICENSE": "skills/progressive-clarity/LICENSE",
        "skills/progressive-clarity/SKILL.md": "skills/progressive-clarity/SKILL.md",
    }
    for directory_name, canonical_name in identical_files.items():
        directory_bytes = read_regular_file(
            directory_root / directory_name,
            f"directory {directory_name}",
        )
        canonical_bytes = read_regular_file(
            root / canonical_name,
            f"canonical {canonical_name}",
        )
        if directory_bytes != canonical_bytes:
            raise ValueError(
                f"directory {directory_name} differs from {canonical_name}"
            )

    readme = read_regular_file(
        directory_root / "README.md",
        "directory README",
    ).decode("utf-8")
    if len(README_WORD_PATTERN.findall(readme)) < 40:
        raise ValueError("directory README must contain at least 40 prose words")
    if "```" in readme:
        raise ValueError("directory README must remain prose-only")


def main() -> int:
    """Validate the tracked directory source."""
    validate_directory_source()
    print(
        "Claude directory source validated: "
        f"claude-directory/progressive-clarity ({DIRECTORY_VERSION})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
