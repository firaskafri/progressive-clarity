"""Name: OpenAI package determinism and isolation suite.

Description: Exercises exact archive inventory, prompt-only isolation,
normalized ZIP metadata, byte-for-byte reproducibility, and byte or metadata
tamper detection.
Assumptions: The tracked manifest, assets, skill, and license are canonical.
Expectations: Repeated builds are identical and never include local pc-core,
hooks, tests, state, or backend configuration.
"""

from __future__ import annotations

import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.package_openai_plugin import (
    ARCHIVE_TIMESTAMP,
    load_manifest,
    source_entries,
    verify_archive,
    zip_info,
)


def _write_archive(path: Path, entries: dict[str, bytes]) -> None:
    """Write one normalized test archive using production metadata."""
    with zipfile.ZipFile(path, mode="w") as archive:
        for name in sorted(entries):
            archive.writestr(zip_info(name), entries[name])


class OpenAiPackagingTests(unittest.TestCase):
    """Name: Prompt-only deterministic OpenAI archive.

    Description: Validates source isolation, reproducible bytes, normalized
    entries, and integrity verification over byte- and metadata-tampered
    archives.
    Assumptions: ZIP_STORED and fixed metadata are portable across Python 3.11+.
    Expectations: Only five reviewed prompt-package files are publishable.
    """

    def test_inventory_excludes_local_enforcement_runtime(self) -> None:
        """Name: Prompt-only package boundary.

        Description: Inspects every source entry selected by the packager.
        Assumptions: ChatGPT remains Option 1 and requires no backend or MCP.
        Expectations: The archive has five exact entries and no pc_core or hook
        path.
        """
        entries = source_entries(load_manifest())
        self.assertEqual(
            sorted(entries),
            [
                ".codex-plugin/plugin.json",
                "assets/progressive-clarity-composer.svg",
                "assets/progressive-clarity-logo.svg",
                "skills/progressive-clarity/LICENSE",
                "skills/progressive-clarity/SKILL.md",
            ],
        )
        self.assertFalse(any("pc_core" in name for name in entries))
        self.assertFalse(any("hook" in name.lower() for name in entries))

    def test_two_normalized_archives_are_byte_identical(self) -> None:
        """Name: Archive byte determinism.

        Description: Builds the same source entries twice in separate files.
        Assumptions: Fixed ordering, timestamps, permissions, and compression
        remove environment-dependent ZIP metadata.
        Expectations: Complete bytes and SHA-256 digests are equal.
        """
        entries = source_entries(load_manifest())
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            _write_archive(first, entries)
            _write_archive(second, entries)
            first_bytes = first.read_bytes()
            second_bytes = second.read_bytes()
        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(
            hashlib.sha256(first_bytes).hexdigest(),
            hashlib.sha256(second_bytes).hexdigest(),
        )

    def test_every_entry_uses_normalized_metadata(self) -> None:
        """Name: ZIP metadata normalization.

        Description: Opens a generated archive and checks timestamps,
        compression, Unix origin, and regular-file permissions.
        Assumptions: OpenAI consumes regular files and ignores no hidden
        platform metadata.
        Expectations: Every entry has the production-normalized metadata.
        """
        entries = source_entries(load_manifest())
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "package.zip"
            _write_archive(archive_path, entries)
            with zipfile.ZipFile(archive_path) as archive:
                infos = archive.infolist()
        for info in infos:
            self.assertEqual(info.date_time, ARCHIVE_TIMESTAMP)
            self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(info.create_system, 3)
            self.assertEqual(info.external_attr >> 16, 0o100644)

    def test_integrity_verifier_rejects_tampered_entry(self) -> None:
        """Name: Packaged-byte tamper detection.

        Description: Replaces the canonical skill bytes in an otherwise valid
        normalized archive.
        Assumptions: Entry path equality alone is insufficient for integrity.
        Expectations: Production verification raises ValueError.
        """
        entries = source_entries(load_manifest())
        tampered = dict(entries)
        tampered["skills/progressive-clarity/SKILL.md"] += b"\n"
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "tampered.zip"
            _write_archive(archive_path, tampered)
            with self.assertRaises(ValueError):
                verify_archive(archive_path, entries)

    def test_integrity_verifier_rejects_tampered_metadata(self) -> None:
        """Name: Packaged-metadata tamper detection.

        Description: Writes canonical entry names and bytes with default ZIP
        timestamps and permissions instead of production-normalized metadata.
        Assumptions: Matching source bytes alone do not establish deterministic
        archive identity.
        Expectations: Production verification raises ValueError.
        """
        entries = source_entries(load_manifest())
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "metadata-tampered.zip"
            with zipfile.ZipFile(archive_path, mode="w") as archive:
                for name in sorted(entries):
                    archive.writestr(name, entries[name])
            with self.assertRaises(ValueError):
                verify_archive(archive_path, entries)


if __name__ == "__main__":
    unittest.main()
