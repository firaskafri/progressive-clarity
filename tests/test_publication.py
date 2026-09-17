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
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/firaskafri/progressive-clarity"
APPROVED_CLAUDE_REVISION = "f34fbf03ba644f7b86d6c9413504878d4f76762b"


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
                "ref": "v0.5.0",
                "sha": APPROVED_CLAUDE_REVISION,
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
                "ref": "v0.5.0",
                "sha": APPROVED_CLAUDE_REVISION,
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


if __name__ == "__main__":
    unittest.main()
