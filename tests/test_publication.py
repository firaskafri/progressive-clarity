"""Name: Publication metadata contract suite.

Description: Validates the repository marketplace catalogs and the durable
publication-status record against the canonical plugin manifests.
Assumptions: Vendor review state remains distinct from public catalog presence,
and marketplace entries resolve only to the public canonical repository.
Expectations: Distribution metadata cannot silently drift from the reviewed
Progressive Clarity identity or claim catalog publication prematurely.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/firaskafri/progressive-clarity"
APPROVED_CLAUDE_REVISION = "f34fbf03ba644f7b86d6c9413504878d4f76762b"
PUBLISHED_RELEASE_REF = "v0.5.1"
PUBLISHED_RELEASE_REVISION = "3e6eb8f1b85e33c4c7386d55584f2666ade9836c"


def load_json(relative_path: str) -> dict[str, object]:
    """Load one repository JSON object."""

    value = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{relative_path} must contain a JSON object")
    return value


class PublicationMetadataTests(unittest.TestCase):
    """Name: Cross-platform marketplace and status checks.

    Description: Compares OpenAI and Claude marketplace entries with canonical
    package identity and verifies the approved-but-not-yet-listed distinction.
    Assumptions: Public source distribution uses GitHub without credentials.
    Expectations: Both catalogs expose one safe plugin and the tracker retains
    the exact reviewed Claude revision without claiming catalog synchronization.
    """

    def test_openai_marketplace_targets_the_public_repository(self) -> None:
        """Name: OpenAI repository marketplace.

        Description: Inspects the single OpenAI marketplace entry and policy.
        Assumptions: The marketplace follows the documented Git-backed source
        shape and the plugin requires no authentication of its own.
        Expectations: The canonical plugin is available from the public main
        branch with installation and use-time policy fields.
        """

        marketplace = load_json(".agents/plugins/marketplace.json")
        self.assertEqual(marketplace["name"], "progressive-clarity")
        self.assertEqual(
            marketplace["interface"],
            {"displayName": "Progressive Clarity"},
        )
        plugins = marketplace["plugins"]
        self.assertIsInstance(plugins, list)
        self.assertEqual(len(plugins), 1)
        plugin = plugins[0]
        self.assertEqual(plugin["name"], "progressive-clarity")
        self.assertEqual(
            plugin["source"],
            {
                "source": "url",
                "url": f"{REPOSITORY}.git",
                "ref": PUBLISHED_RELEASE_REF,
                "sha": PUBLISHED_RELEASE_REVISION,
            },
        )
        self.assertEqual(
            plugin["policy"],
            {
                "installation": "AVAILABLE",
                "authentication": "ON_USE",
            },
        )

    def test_claude_marketplace_defers_version_to_plugin_manifest(self) -> None:
        """Name: Claude repository marketplace.

        Description: Inspects the Claude marketplace owner and GitHub source.
        Assumptions: The plugin manifest is the only semantic-version authority.
        Expectations: The catalog targets the canonical repository and does not
        add a second version field that could mask future manifest updates.
        """

        marketplace = load_json(".claude-plugin/marketplace.json")
        self.assertEqual(marketplace["name"], "firas-kafri-plugins")
        plugins = marketplace["plugins"]
        self.assertIsInstance(plugins, list)
        self.assertEqual(len(plugins), 1)
        plugin = plugins[0]
        self.assertEqual(plugin["name"], "progressive-clarity")
        self.assertNotIn("version", plugin)
        self.assertEqual(
            plugin["source"],
            {
                "source": "github",
                "repo": "firaskafri/progressive-clarity",
                "ref": PUBLISHED_RELEASE_REF,
                "sha": PUBLISHED_RELEASE_REVISION,
            },
        )

    def test_tracker_separates_review_from_catalog_publication(self) -> None:
        """Name: Claude publication-state boundary.

        Description: Checks the tracked approval evidence and pending catalog
        synchronization language.
        Assumptions: Console review passed before the public mirror listed the
        plugin, and the approved source revision is immutable evidence.
        Expectations: The tracker records both facts without marking public
        catalog availability complete.
        """

        tracker = (ROOT / "docs" / "publication-readiness.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(APPROVED_CLAUDE_REVISION, tracker)
        self.assertIn(
            "- [x] Claude Console records the plugin as `passed_review`.",
            tracker,
        )
        self.assertIn(
            "- [ ] Confirm Progressive Clarity appears in Anthropic's public",
            tracker,
        )

    def test_release_tag_guard_rejects_unaccepted_and_mismatched_tags(self) -> None:
        """Name: Executable accepted release tag guard.

        Description: Executes the workflow's actual Python guard for candidate,
        stable, malformed, and mismatched tags without running publication.
        Assumptions: The workflow keeps its version check in one Python heredoc.
        Expectations: Only the canonical candidate with reviewed notes passes.
        """
        from tools.package_common import RELEASE_VERSION

        workflow = (ROOT / ".github/workflows/release.yml").read_text()
        source = workflow.split('<<\'PY\'\n', 1)[1].split('\n          PY', 1)[0]
        source = "\n".join(line.removeprefix("          ") for line in source.splitlines())
        for tag, valid in (
            (f"v{RELEASE_VERSION}", True),
            ("v0.5.1", RELEASE_VERSION == "0.5.1"),
            ("v0.5.0", False),
            ("v0.5.1-rc.0", False),
            ("v0.5.1-rc.999", False),
            ("v0.5.1-rc.9", False),
            ("v0.5.1-rc.9/unsafe", False),
        ):
            with self.subTest(tag=tag):
                result = subprocess.run(
                    [sys.executable, "-", tag], input=source, text=True,
                    capture_output=True, cwd=ROOT, check=False,
                )
                self.assertEqual(result.returncode == 0, valid, result.stderr)

    def test_release_workflow_preserves_experimental_and_immutable_boundaries(self) -> None:
        """Name: Prerelease publishing safeguards.

        Description: Checks explicit experimental labeling, artifact isolation,
        checksum verification, and refusal to overwrite published assets.
        Assumptions: Static checks supplement executable tag checks and CI builds.
        Expectations: Publication cannot mark this release latest without promotion,
        silently overwrite an existing release, or omit reviewed limitations.
        """
        workflow = (ROOT / ".github/workflows/release.yml").read_text()
        for safeguard in (
            '--prerelease', '--latest=false',
            '--notes-file docs/experimental-prerelease.md',
            'Existing release must not be overwritten',
            'dist must be empty', 'test "${#packages[@]}" -eq 5',
            'sha256sum --check SHA256SUMS.txt',
        ):
            self.assertIn(safeguard, workflow)
        self.assertNotIn('--clobber', workflow)
        self.assertNotIn('--generate-notes', workflow)
        self.assertIn('validate_acceptance()', workflow)
        self.assertIn('--notes-file docs/release-0.5.1.md', workflow)
        self.assertIn('release_options=(--notes-file docs/release-0.5.1.md)', workflow)
        notes = (ROOT / "docs/release-0.5.1.md").read_text()
        for boundary in ('T10', 'T15', 'T18', 'not yet published', 'vendor-approved'):
            self.assertIn(boundary, notes)

    def test_current_installation_documentation_matches_candidate_version(self) -> None:
        """Name: Current candidate documentation versions.

        Description: Checks current installation instructions and release notes
        against the canonical version, without rewriting historical evidence.
        Assumptions: Historical installation sections begin at the v0.4 heading.
        Expectations: Current commands and filenames name the current candidate,
        not stale rc.9 artifacts or already-published 0.5.0 build targets.
        """
        from tools.package_common import RELEASE_VERSION

        installation = (ROOT / "docs/installation.md").read_text().split(
            "## Historical v0.4 installation record", 1
        )[0]
        for host in ("openai-plugin", "claude-plugin", "claude-ai-skill"):
            self.assertIn(f"progressive-clarity-{host}-{RELEASE_VERSION}.zip", installation)
        self.assertNotIn("now builds unpublished candidate `0.5.1-rc.9`", installation)
        self.assertNotIn("The source targets package `0.5.0`", installation)
        notes = (ROOT / "docs/release-0.5.1.md").read_text()
        self.assertIn(f"`{RELEASE_VERSION}`", notes)
        self.assertIn(f"No {RELEASE_VERSION} release assets have been published yet.", notes)

    def test_stable_acceptance_record_fails_closed_on_changed_inputs(self) -> None:
        """Name: Immutable stable acceptance gate.

        Description: Validates the reviewed evidence and rejects modified source,
        missing evidence, and changed judgment records without inference.
        Assumptions: A temporary root contains only acceptance inputs.
        Expectations: Exact accepted inputs pass; altered or absent inputs fail.
        """
        import shutil
        import tempfile

        from tools.validate_release_acceptance import EVIDENCE_PATH, validate_acceptance

        validate_acceptance()
        paths = (
            EVIDENCE_PATH,
            Path("skills/progressive-clarity/SKILL.md"),
            Path("evals/release-acceptance-context-v1.json"),
            Path("evals/cases.json"),
            Path("SPEC.md"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in paths:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            validate_acceptance(root)
            for relative in paths:
                with self.subTest(path=relative):
                    target = root / relative
                    original = target.read_bytes()
                    target.write_bytes(original + b"\n")
                    if relative != Path("evals/release-acceptance-context-v1.json"):
                        with self.assertRaises(ValueError):
                            validate_acceptance(root)
                    else:
                        suite = json.loads(original)
                        suite["cases"][0]["title"] += " changed"
                        target.write_text(json.dumps(suite))
                        with self.assertRaises(ValueError):
                            validate_acceptance(root)
                    target.write_bytes(original)
            (root / EVIDENCE_PATH).unlink()
            with self.assertRaises(FileNotFoundError):
                validate_acceptance(root)

    def test_release_ci_guard_requires_latest_exact_commit_success(self) -> None:
        """Name: Exact-commit CI release gate.

        Description: Executes the workflow CI guard with successful, missing,
        failed, pending, stale-commit, and superseded-success reports.
        Assumptions: GitHub reports are untrusted until their commit and latest
        run state are checked; no network or publication is needed in this test.
        Expectations: Only a completed successful latest run on the exact SHA
        permits publication; all other states fail closed.
        """
        import tempfile

        workflow = (ROOT / ".github/workflows/release.yml").read_text()
        section = workflow.split(
            "- name: Require successful CI on the exact release commit", 1
        )[1]
        source = section.split("<<'PY'\n", 1)[1].split("\n          PY", 1)[0]
        source = "\n".join(line.removeprefix("          ") for line in source.splitlines())
        sha = "a" * 40
        good = {"headSha": sha, "status": "completed", "conclusion": "success", "databaseId": 1}
        reports = (
            ([good], True),
            ([], False),
            ([dict(good, headSha="b" * 40)], False),
            ([dict(good, conclusion="failure")], False),
            ([dict(good, status="in_progress", conclusion=None)], False),
            ([good, dict(good, databaseId=2, conclusion="failure")], False),
            ([dict(good, conclusion="failure"), dict(good, databaseId=2)], True),
        )
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "ci.json"
            for runs, expected in reports:
                with self.subTest(runs=runs):
                    report.write_text(json.dumps(runs))
                    result = subprocess.run(
                        [sys.executable, "-", sha, str(report)], input=source,
                        text=True, capture_output=True, check=False,
                    )
                    self.assertEqual(result.returncode == 0, expected, result.stderr)
        self.assertIn('--event push --branch main', workflow)
        self.assertIn('actions: read', workflow)


if __name__ == "__main__":
    unittest.main()
