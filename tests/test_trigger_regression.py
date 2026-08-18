"""Name: Advisory trigger-regression contract suite.

Description: Validates the front-loaded skill discovery description and a
small activation-only positive/negative prompt fixture.
Assumptions: Host skill selection remains advisory and separate from output
conformance; fixture labels are expectations rather than observed host results.
Expectations: Broad ordinary prompts activate, precise non-fit prompts remain
inactive, and removed presentation modes never reappear in discovery metadata.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.validate_repository import parse_frontmatter


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "trigger_regression.json"
SKILL_PATH = ROOT / "skills" / "progressive-clarity" / "SKILL.md"


class TriggerRegressionTests(unittest.TestCase):
    """Name: Advisory activation boundary.

    Description: Checks required discovery language and representative prompts
    on both sides of the ordinary-response/non-fit boundary.
    Assumptions: Prompt labels do not simulate ChatGPT or guarantee invocation.
    Expectations: Metadata and fixtures remain broad, explicit, and mode-free.
    """

    def test_description_and_trigger_fixture_contract(self) -> None:
        """Name: Front-loaded activation fixture.

        Description: Validates discovery priority, three-view ordering,
        exclusions, the evidence-derived gold prompt, and non-fit contrasts.
        Assumptions: Standard SKILL.md frontmatter and fixture schema 1.0.0 are
        the reviewed activation-only inputs.
        Expectations: Five positive and four negative unique cases pass without
        obsolete presentation-state terminology.
        """
        errors: list[str] = []
        fields = parse_frontmatter(SKILL_PATH.read_text(encoding="utf-8"), errors)
        self.assertEqual(errors, [])
        self.assertEqual(set(fields), {"name", "description", "license"})

        description = fields["description"]
        normalized_description = " ".join(
            re.sub(r"^(?:>-?|[|]-?)\s*", "", description).split()
        )
        self.assertLessEqual(len(description), 1024)
        self.assertTrue(
            normalized_description.startswith("Default response-formatting skill.")
        )
        self.assertIn(
            "MUST use for every ordinary user-facing",
            normalized_description,
        )
        self.assertIn(
            "even when the user does not name this skill",
            normalized_description,
        )
        self.assertLess(
            normalized_description.index("Output exactly three additive views"),
            normalized_description.index("Exclude only"),
        )
        self.assertNotRegex(
            normalized_description.lower(),
            r"\b(?:progressive mode|verbose mode|sticky mode)\b",
        )

        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(set(fixture), {"schema_version", "purpose", "cases"})
        self.assertEqual(fixture["schema_version"], "1.0.0")
        cases = fixture["cases"]
        self.assertEqual(
            [case["id"] for case in cases],
            [f"TR{number:02d}" for number in range(1, 10)],
        )
        self.assertTrue(
            all(
                set(case) == {"id", "prompt", "expected_activation", "rationale"}
                for case in cases
            )
        )
        prompts = [case["prompt"] for case in cases]
        self.assertEqual(len(prompts), len(set(prompts)))
        self.assertEqual(prompts[0], "gold prices and forecasts")
        self.assertEqual(
            [case["expected_activation"] for case in cases].count("activate"),
            5,
        )
        self.assertEqual(
            [case["expected_activation"] for case in cases].count(
                "remain_inactive"
            ),
            4,
        )


if __name__ == "__main__":
    unittest.main()
