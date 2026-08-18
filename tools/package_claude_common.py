"""Deterministic ZIP helpers shared by Claude distribution packagers."""

from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path, PurePosixPath


ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
REGULAR_FILE_MODE = 0o100644


def sha256(data: bytes) -> str:
    """Return the SHA-256 digest for bytes."""
    return hashlib.sha256(data).hexdigest()


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
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} must be a regular file: {path}")
    return path.read_bytes()


def validate_entry_name(name: str) -> None:
    """Reject archive names that are ambiguous or can escape extraction roots."""
    path = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"unsafe archive entry name: {name!r}")


def zip_info(name: str) -> zipfile.ZipInfo:
    """Create normalized ZIP metadata for one regular file."""
    validate_entry_name(name)
    info = zipfile.ZipInfo(name, date_time=ARCHIVE_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = (REGULAR_FILE_MODE & 0xFFFF) << 16
    return info


def verify_archive(archive_path: Path, entries: dict[str, bytes]) -> None:
    """Confirm inventory, integrity, metadata, and bytes for one archive."""
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
                or info.create_system != 3
                or info.external_attr >> 16 != REGULAR_FILE_MODE
                or info.extra
                or info.comment
            ):
                raise ValueError(f"archive metadata is not normalized: {name}")
            if archive.read(name) != expected_bytes:
                raise ValueError(f"archive bytes differ from source: {name}")


def build_archive(archive_path: Path, entries: dict[str, bytes]) -> None:
    """Atomically build and verify a deterministic archive."""
    if not entries:
        raise ValueError("archive inventory must not be empty")
    for name in entries:
        validate_entry_name(name)

    archive_path.parent.mkdir(exist_ok=True)
    temporary_path = archive_path.with_suffix(f"{archive_path.suffix}.tmp")
    try:
        with zipfile.ZipFile(temporary_path, mode="w") as archive:
            for name in sorted(entries):
                archive.writestr(zip_info(name), entries[name])
        os.replace(temporary_path, archive_path)
    finally:
        temporary_path.unlink(missing_ok=True)

    verify_archive(archive_path, entries)


def print_archive_report(root: Path, archive_path: Path, entries: dict[str, bytes]) -> None:
    """Print stable artifact and entry metadata for release verification."""
    archive_bytes = archive_path.read_bytes()
    print(f"archive={archive_path.relative_to(root)}")
    print(f"archive_sha256={sha256(archive_bytes)}")
    print(f"archive_bytes={len(archive_bytes)}")
    for name in sorted(entries):
        data = entries[name]
        print(f"entry={name} sha256={sha256(data)} bytes={len(data)}")
