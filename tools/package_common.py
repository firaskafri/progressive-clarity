"""Deterministic file and ZIP helpers shared by distribution packagers."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from types import MappingProxyType
from typing import Mapping


ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
REGULAR_FILE_MODE = 0o100644
ZIP_CREATE_SYSTEM = 3
RELEASE_VERSION = "0.4.3"
CANONICAL_LICENSE = "Apache-2.0"
CANONICAL_SKILL_FILES = ("LICENSE", "SKILL.md")
CANONICAL_SKILL_FIELDS = frozenset({"name", "description", "license"})
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


@dataclass(frozen=True)
class CanonicalSkillSource:
    """Validated canonical Skill bytes and parsed metadata."""

    skill: bytes
    body: bytes
    license: bytes
    frontmatter: Mapping[str, str]


def sha256(data: bytes) -> str:
    """Return the SHA-256 digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def _unique_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    parsed: dict[str, object] = {}
    for key, value in pairs:
        if key in parsed:
            raise ValueError("JSON objects must not contain duplicate members")
        parsed[key] = value
    return parsed


def _reject_json_constant(_value: str) -> object:
    raise ValueError("JSON must not contain non-standard numeric constants")


def parse_json_object(source: bytes, label: str) -> dict[str, object]:
    """Parse one strict UTF-8 JSON object used by package metadata."""
    try:
        value = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} must be valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def split_skill(source: bytes) -> tuple[bytes, bytes]:
    """Split a UTF-8 SKILL.md into frontmatter and byte-preserved body."""
    if not source.startswith(b"---\n"):
        raise ValueError("SKILL.md must start with an LF-delimited frontmatter marker")
    closing_marker = source.find(b"\n---\n", 4)
    if closing_marker < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    frontmatter = source[4:closing_marker]
    body = source[closing_marker + len(b"\n---\n") :]
    frontmatter.decode("utf-8")
    body.decode("utf-8")
    return frontmatter, body


def parse_simple_frontmatter(frontmatter: bytes) -> dict[str, str]:
    """Parse the scalar YAML subset used by the canonical and generated skill."""
    fields: dict[str, list[str]] = {}
    styles: dict[str, str] = {}
    current_key: str | None = None

    for line in frontmatter.decode("utf-8").splitlines():
        if line.startswith((" ", "\t")):
            if current_key is None or not line.strip():
                raise ValueError("invalid frontmatter continuation")
            fields[current_key].append(line.strip())
            continue

        if ":" not in line:
            raise ValueError(f"invalid frontmatter field: {line!r}")
        key, raw_value = line.split(":", 1)
        if not key or key in fields:
            raise ValueError(f"invalid or duplicate frontmatter key: {key!r}")
        current_key = key
        value = raw_value.strip()
        if value in {">", ">-", "|", "|-"}:
            styles[key] = value[0]
            fields[key] = []
        else:
            fields[key] = [value]

    parsed: dict[str, str] = {}
    for key, values in fields.items():
        if styles.get(key) == "|":
            parsed[key] = "\n".join(values)
        else:
            parsed[key] = " ".join(values)
    return parsed


def read_regular_file(path: Path, label: str) -> bytes:
    """Read one required regular file without following a symlink."""
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"{label} must be a regular file: {path}") from exc
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError(f"{label} must be a regular file: {path}")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            return handle.read()
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def load_canonical_skill_source(
    skill_dir: Path,
    *,
    root: Path | None = None,
) -> CanonicalSkillSource:
    """Read and validate the canonical Skill directory once."""
    if (
        skill_dir.is_symlink()
        or not skill_dir.is_dir()
        or (
            root is not None
            and not skill_dir.resolve().is_relative_to(root.resolve())
        )
    ):
        raise ValueError(
            f"canonical skill directory must be a directory: {skill_dir}"
        )
    actual_entries = sorted(path.name for path in skill_dir.iterdir())
    if actual_entries != sorted(CANONICAL_SKILL_FILES):
        raise ValueError(
            "canonical skill directory must contain exactly: "
            + ", ".join(CANONICAL_SKILL_FILES)
        )

    skill = read_regular_file(skill_dir / "SKILL.md", "canonical SKILL.md")
    license_bytes = read_regular_file(skill_dir / "LICENSE", "canonical LICENSE")
    if root is not None:
        expected_license = read_regular_file(
            root / "LICENSES" / "Apache-2.0.txt",
            "repository Apache-2.0 license",
        )
        if license_bytes != expected_license:
            raise ValueError(
                "canonical LICENSE bytes differ from LICENSES/Apache-2.0.txt"
            )
    frontmatter_bytes, body = split_skill(skill)
    frontmatter = parse_simple_frontmatter(frontmatter_bytes)
    if set(frontmatter) != CANONICAL_SKILL_FIELDS:
        raise ValueError(
            "canonical skill frontmatter must contain name, description, and license"
        )
    if frontmatter["name"] != skill_dir.name:
        raise ValueError("canonical skill name must match its parent directory")
    if not 1 <= len(frontmatter["description"]) <= 1024:
        raise ValueError(
            "canonical skill description must contain 1-1024 characters"
        )
    if frontmatter["license"] != CANONICAL_LICENSE:
        raise ValueError(
            f"canonical skill license must be {CANONICAL_LICENSE}"
        )
    if not body.strip():
        raise ValueError("canonical skill body must not be empty")
    return CanonicalSkillSource(
        skill=skill,
        body=body,
        license=license_bytes,
        frontmatter=MappingProxyType(frontmatter),
    )


def validate_entry_name(name: str) -> None:
    """Reject archive names that are ambiguous or can escape extraction roots."""
    if not isinstance(name, str):
        raise ValueError("archive entry names must be strings")
    raw_parts = name.split("/")
    if (
        not name
        or "\\" in name
        or "\x00" in name
        or PurePosixPath(name).is_absolute()
        or bool(PureWindowsPath(name).drive)
        or any(part in {"", ".", ".."} for part in raw_parts)
    ):
        raise ValueError(f"unsafe archive entry name: {name!r}")


def _validate_entries(entries: dict[str, bytes]) -> None:
    if not entries:
        raise ValueError("archive inventory must not be empty")
    for name, content in entries.items():
        validate_entry_name(name)
        if not isinstance(content, bytes):
            raise ValueError(f"archive entry content must be bytes: {name!r}")


def zip_info(name: str) -> zipfile.ZipInfo:
    """Create normalized ZIP metadata for one regular file."""
    validate_entry_name(name)
    info = zipfile.ZipInfo(name, date_time=ARCHIVE_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = ZIP_CREATE_SYSTEM
    info.external_attr = (REGULAR_FILE_MODE & 0xFFFF) << 16
    return info


def verify_archive(archive_path: Path, entries: dict[str, bytes]) -> None:
    """Confirm inventory, integrity, metadata, and bytes for one archive."""
    _validate_entries(entries)
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if names != sorted(entries) or len(names) != len(set(names)):
            raise ValueError(f"unexpected archive inventory: {names}")
        if archive.comment:
            raise ValueError("archive comment must be empty")
        if corrupt_entry := archive.testzip():
            raise ValueError(f"archive integrity check failed: {corrupt_entry}")

        for name, expected_bytes in entries.items():
            info = archive.getinfo(name)
            if (
                info.date_time != ARCHIVE_TIMESTAMP
                or info.compress_type != zipfile.ZIP_STORED
                or info.create_system != ZIP_CREATE_SYSTEM
                or info.external_attr >> 16 != REGULAR_FILE_MODE
                or info.extra
                or info.comment
            ):
                raise ValueError(f"archive metadata is not normalized: {name}")
            if archive.read(name) != expected_bytes:
                raise ValueError(f"archive bytes differ from source: {name}")


def write_archive(archive_path: Path, entries: dict[str, bytes]) -> None:
    """Atomically build and verify a deterministic archive."""
    _validate_entries(entries)

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = tempfile.NamedTemporaryFile(
        dir=archive_path.parent,
        prefix=f".{archive_path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary_path = Path(temporary_file.name)
    temporary_file.close()
    try:
        with zipfile.ZipFile(temporary_path, mode="w") as archive:
            for name in sorted(entries):
                archive.writestr(zip_info(name), entries[name])
        os.chmod(temporary_path, REGULAR_FILE_MODE & 0o777)
        verify_archive(temporary_path, entries)
        os.replace(temporary_path, archive_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def print_archive_report(
    root: Path,
    archive_path: Path,
    entries: dict[str, bytes],
) -> None:
    """Print stable artifact and entry metadata for release verification."""
    archive_bytes = archive_path.read_bytes()
    print(f"archive={archive_path.relative_to(root)}")
    print(f"archive_sha256={sha256(archive_bytes)}")
    print(f"archive_bytes={len(archive_bytes)}")
    for name in sorted(entries):
        data = entries[name]
        print(f"entry={name} sha256={sha256(data)} bytes={len(data)}")
