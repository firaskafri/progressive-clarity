"""Name: Distribution package determinism and isolation suite.

Description: Exercises cross-channel versions, exact archive inventory,
prompt-only isolation, validated manifest-byte identity, shared canonical Skill
loading, normalized ZIP metadata, byte reproducibility, and tamper detection
including ambiguous manifests and entry names.
Assumptions: The tracked manifest, assets, skill, and license are canonical.
Expectations: Repeated builds are identical and never include local pc-core,
hooks, tests, state, or backend configuration.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

from tools import (
    package_claude_plugin,
    package_claude_skill,
    package_openai_plugin,
)
from tools.package_common import (
    ARCHIVE_TIMESTAMP,
    REGULAR_FILE_MODE,
    RELEASE_VERSION,
    ZIP_CREATE_SYSTEM,
    load_canonical_skill_source,
    validate_entry_name,
    verify_archive,
    write_archive,
)
from tools.package_openai_plugin import (
    build_archive,
    load_manifest,
    source_entries,
    validate_svg_asset,
)
def _openai_entries() -> dict[str, bytes]:
    """Load the validated OpenAI manifest bytes and source inventory."""
    manifest, manifest_bytes = load_manifest()
    return source_entries(manifest, manifest_bytes)


class CrossDistributionMetadataTests(unittest.TestCase):
    """Name: Coordinated distribution metadata.

    Description: Checks OpenAI, Claude plugin, and Claude.ai Skill release
    identity and controlling-text discovery while preserving each packager's
    distinct archive shape.
    Assumptions: Protocol v0.4 changes every coordinated prompt distribution.
    Expectations: All channels use version 0.4.3 and canonical skill content.
    """

    def test_all_distribution_versions_and_skill_bodies_match(self) -> None:
        """Name: v0.4 distribution synchronization.

        Description: Loads all manifests, checks Claude.ai controlling-text
        discovery, and generates its Skill.
        Assumptions: Claude.ai regenerates only frontmatter, not canonical body.
        Expectations: Versions and discovery metadata match, and generated body
        equals canonical body.
        """
        openai, _openai_manifest_bytes = package_openai_plugin.load_manifest()
        claude, _manifest_bytes = package_claude_plugin.load_manifest()
        canonical = load_canonical_skill_source(
            package_claude_skill.SKILL_DIR,
            root=package_claude_skill.ROOT,
        )
        generated = package_claude_skill.generate_packaged_skill(canonical.body)
        _generated_frontmatter, generated_body = (
            package_claude_skill.split_skill(generated)
        )

        self.assertEqual(openai["version"], RELEASE_VERSION)
        self.assertEqual(claude["version"], RELEASE_VERSION)
        self.assertEqual(package_claude_skill.PACKAGE_VERSION, RELEASE_VERSION)
        self.assertIn(
            "controlling text",
            package_claude_skill.PACKAGED_DESCRIPTION,
        )
        self.assertEqual(generated_body, canonical.body)

    def test_claude_ai_generation_rejects_empty_canonical_body(self) -> None:
        """Name: Empty Claude.ai canonical body refusal.

        Description: Calls the public frontmatter generator with empty bytes.
        Assumptions: Production loading rejects empty bodies before generation.
        Expectations: Direct callers receive the same fail-closed behavior.
        """
        with self.assertRaisesRegex(ValueError, "non-empty bytes"):
            package_claude_skill.generate_packaged_skill(b"")


class CanonicalSkillSourceTests(unittest.TestCase):
    """Name: Shared canonical Skill source validation.

    Description: Exercises byte identity between packaged and repository
    licensing inputs.
    Assumptions: Apache metadata must identify the exact reviewed license text.
    Expectations: Divergent canonical license bytes are rejected before packaging.
    """

    def test_canonical_license_must_match_repository_license(self) -> None:
        """Name: Canonical license byte identity.

        Description: Loads a valid Skill body beside divergent license files.
        Assumptions: Directory shape and frontmatter remain otherwise canonical.
        Expectations: Shared source loading rejects the mismatched license bytes.
        """
        canonical_skill = (
            package_claude_skill.SKILL_DIR / "SKILL.md"
        ).read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "skills" / "progressive-clarity"
            license_dir = root / "LICENSES"
            skill_dir.mkdir(parents=True)
            license_dir.mkdir()
            (skill_dir / "SKILL.md").write_bytes(canonical_skill)
            (skill_dir / "LICENSE").write_bytes(b"packaged license\n")
            (license_dir / "Apache-2.0.txt").write_bytes(
                b"reviewed license\n"
            )

            with self.assertRaisesRegex(ValueError, "LICENSE bytes differ"):
                load_canonical_skill_source(skill_dir, root=root)


class OpenAiPackagingTests(unittest.TestCase):
    """Name: Prompt-only deterministic OpenAI archive.

    Description: Validates source isolation, reproducible bytes, normalized
    entries, strict manifests, safe names, and tamper detection.
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
        entries = _openai_entries()
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

    def test_manifest_rejects_another_valid_package_name(self) -> None:
        """Name: Fixed package identity.

        Description: Replaces the canonical name with another syntactically
        valid name.
        Assumptions: Package paths and review history are specific to
        Progressive Clarity.
        Expectations: Manifest loading rejects the alternate identity.
        """
        manifest, _manifest_bytes = load_manifest()
        manifest["name"] = "another-valid-name"
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "plugin.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(
                package_openai_plugin,
                "MANIFEST_PATH",
                manifest_path,
            ):
                with self.assertRaisesRegex(ValueError, "canonical package identity"):
                    package_openai_plugin.load_manifest()

    def test_manifest_rejects_duplicate_json_members(self) -> None:
        """Name: Unambiguous package manifest JSON.

        Description: Repeats the canonical name member with the same value.
        Assumptions: Plugin metadata requires unique JSON object member names.
        Expectations: Manifest loading rejects the ambiguous source bytes.
        """
        manifest_text = package_openai_plugin.MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
        duplicate = manifest_text.replace(
            '"name": "progressive-clarity",',
            (
                '"name": "progressive-clarity",\n'
                '  "name": "progressive-clarity",'
            ),
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "plugin.json"
            manifest_path.write_text(duplicate, encoding="utf-8")
            with mock.patch.object(
                package_openai_plugin,
                "MANIFEST_PATH",
                manifest_path,
            ):
                with self.assertRaisesRegex(ValueError, "duplicate members"):
                    package_openai_plugin.load_manifest()

    def test_source_entries_use_the_validated_manifest_bytes(self) -> None:
        """Name: Validated OpenAI manifest byte identity.

        Description: Replaces the manifest path after loading validated bytes,
        then pairs those bytes with mutated parsed data.
        Assumptions: Packaging must use the exact bytes paired with parsed data.
        Expectations: Original bytes are retained and mismatched data is rejected.
        """
        manifest, manifest_bytes = load_manifest()
        with tempfile.TemporaryDirectory() as directory:
            replacement = Path(directory) / "plugin.json"
            replacement.write_text('{"changed": true}\n', encoding="utf-8")
            with mock.patch.object(
                package_openai_plugin,
                "MANIFEST_PATH",
                replacement,
            ):
                entries = source_entries(manifest, manifest_bytes)

        self.assertEqual(
            entries[".codex-plugin/plugin.json"],
            manifest_bytes,
        )
        changed = dict(manifest)
        changed["version"] = "9.9.9"
        with self.assertRaisesRegex(ValueError, "do not match"):
            source_entries(changed, manifest_bytes)

    def test_symlinked_skill_root_is_rejected(self) -> None:
        """Name: Skill-root confinement.

        Description: Replaces the canonical skill directory with a symlink.
        Assumptions: Published source directories must remain inside the repository.
        Expectations: Source selection rejects the symlink before reading entries.
        """
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            target = temporary_root / "target"
            target.mkdir()
            symlink = temporary_root / "skill"
            symlink.symlink_to(target, target_is_directory=True)
            with mock.patch.object(package_openai_plugin, "SKILL_DIR", symlink):
                with self.assertRaisesRegex(
                    ValueError,
                    "canonical skill directory",
                ):
                    _openai_entries()

    def test_svg_assets_reject_active_content(self) -> None:
        """Name: Active SVG content refusal.

        Description: Supplies script and external-reference SVG constructs.
        Assumptions: Published branding assets require only static drawing elements.
        Expectations: Both active constructs are rejected before archive creation.
        """
        active_sources = (
            b'<svg width="64" height="64" viewBox="0 0 64 64"><script/></svg>',
            (
                b'<svg width="64" height="64" viewBox="0 0 64 64">'
                b'<rect width="64" height="64" fill="url(https://example.com/x)"/>'
                b"</svg>"
            ),
        )
        for source in active_sources:
            with self.subTest(source=source):
                with self.assertRaisesRegex(ValueError, "active SVG"):
                    validate_svg_asset(source, Path("asset.svg"))

    def test_two_normalized_archives_are_byte_identical(self) -> None:
        """Name: Archive byte determinism.

        Description: Builds the same source entries twice in separate files.
        Assumptions: Fixed ordering, timestamps, permissions, and compression
        remove environment-dependent ZIP metadata.
        Expectations: Complete bytes and SHA-256 digests are equal.
        """
        entries = _openai_entries()
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            write_archive(first, entries)
            write_archive(second, entries)
            first_bytes = first.read_bytes()
            second_bytes = second.read_bytes()
        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(
            hashlib.sha256(first_bytes).hexdigest(),
            hashlib.sha256(second_bytes).hexdigest(),
        )

    def test_concurrent_builds_publish_one_valid_archive(self) -> None:
        """Name: Concurrent archive publication.

        Description: Builds the same package concurrently into one directory.
        Assumptions: Each build uses a private same-directory temporary file.
        Expectations: Both calls succeed and the final archive remains valid.
        """
        entries = _openai_entries()
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            with ThreadPoolExecutor(max_workers=2) as executor:
                paths = list(
                    executor.map(lambda _: build_archive(output_dir)[0], range(2))
                )
            archive_path = paths[0]
            self.assertTrue(all(path == archive_path for path in paths))
            verify_archive(archive_path, entries)

    def test_failed_verification_preserves_existing_archive(self) -> None:
        """Name: Pre-publication verification failure.

        Description: Forces temporary archive verification to fail.
        Assumptions: A prior published archive may already exist.
        Expectations: Failure propagates and prior bytes remain unchanged.
        """
        manifest, _manifest_bytes = load_manifest()
        archive_name = f"{manifest['name']}-openai-plugin-{manifest['version']}.zip"
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            archive_path = output_dir / archive_name
            archive_path.write_bytes(b"previous")
            with mock.patch(
                "tools.package_common.verify_archive",
                side_effect=ValueError("forced verification failure"),
            ):
                with self.assertRaisesRegex(ValueError, "forced verification failure"):
                    build_archive(output_dir)
            self.assertEqual(archive_path.read_bytes(), b"previous")

    def test_every_entry_uses_normalized_metadata(self) -> None:
        """Name: ZIP metadata normalization.

        Description: Opens a generated archive and checks timestamps,
        compression, Unix origin, and regular-file permissions.
        Assumptions: OpenAI consumes regular files and ignores no hidden
        platform metadata.
        Expectations: The archive and every entry have normalized permissions
        and metadata.
        """
        entries = _openai_entries()
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "package.zip"
            write_archive(archive_path, entries)
            archive_mode = archive_path.stat().st_mode & 0o777
            with zipfile.ZipFile(archive_path) as archive:
                infos = archive.infolist()
        self.assertEqual(archive_mode, REGULAR_FILE_MODE & 0o777)
        for info in infos:
            self.assertEqual(info.date_time, ARCHIVE_TIMESTAMP)
            self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(info.create_system, ZIP_CREATE_SYSTEM)
            self.assertEqual(info.external_attr >> 16, REGULAR_FILE_MODE)

    def test_archive_entry_names_reject_ambiguous_paths(self) -> None:
        """Name: Cross-platform archive path safety.

        Description: Checks empty segments, dot segments, directory names,
        Windows drives, backslashes, and null bytes.
        Assumptions: Every package entry is one portable relative file path.
        Expectations: Each ambiguous or extraction-sensitive name is rejected.
        """
        unsafe_names = (
            "folder//file.txt",
            "folder/./file.txt",
            "folder/",
            "C:/escape.txt",
            "..\\escape.txt",
            "null\x00name.txt",
        )
        for name in unsafe_names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    validate_entry_name(name)

    def test_integrity_verifier_rejects_tampered_entry(self) -> None:
        """Name: Packaged-byte tamper detection.

        Description: Replaces the canonical skill bytes in an otherwise valid
        normalized archive.
        Assumptions: Entry path equality alone is insufficient for integrity.
        Expectations: Production verification raises ValueError.
        """
        entries = _openai_entries()
        tampered = dict(entries)
        tampered["skills/progressive-clarity/SKILL.md"] += b"\n"
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "tampered.zip"
            write_archive(archive_path, tampered)
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
        entries = _openai_entries()
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "metadata-tampered.zip"
            with zipfile.ZipFile(archive_path, mode="w") as archive:
                for name in sorted(entries):
                    archive.writestr(name, entries[name])
            with self.assertRaises(ValueError):
                verify_archive(archive_path, entries)


if __name__ == "__main__":
    unittest.main()
