"""Name: Advisory discovery and evaluation input contracts.

Description: Checks standard skill metadata, fixture integrity, and temporal isolation.
Assumptions: Static labels describe expectations, never observed host activation.
Expectations: Prompt wording can evolve without tests requiring obsolete literal rules.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.azure_eval_harness import _available_source_facts, load_suite
from tools.package_common import load_canonical_skill_source


ROOT = Path(__file__).resolve().parents[1]


class TriggerRegressionTests(unittest.TestCase):
    """Name: Discovery metadata and oracle isolation.

    Description: Validates package eligibility fixtures and prevents future fact leakage.
    Assumptions: Host activation and semantic compliance require live evidence.
    Expectations: Fixtures stay well-formed and missing-input turns remain genuinely open.
    """

    def test_description_and_trigger_fixture_contract(self) -> None:
        """Name: Static skill-discovery fixture.

        Description: Loads standard skill metadata and unique eligibility examples.
        Assumptions: Examples distinguish conversational guidance from exact artifacts.
        Expectations: Metadata is valid and each fixture declares a recognized shape.
        """
        source = load_canonical_skill_source(ROOT / "skills" / "progressive-clarity", root=ROOT)
        self.assertEqual(source.frontmatter["name"], "progressive-clarity")
        fixture = json.loads((ROOT / "tests" / "trigger_regression.json").read_text())
        cases = fixture["cases"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertEqual(len({case["prompt"] for case in cases}), len(cases))
        for case in cases:
            self.assertIsInstance(case["eligible_for_skill"], bool)
            self.assertIn(case["expected_presentation_if_applied"], {
                "focused", "full", "non_fit", "adaptive", "control",
            })
        self.assertFalse(cases[-1]["eligible_for_skill"])

    def test_future_readiness_and_corrections_do_not_leak_to_judge(self) -> None:
        """Name: Temporal source-fact isolation.

        Description: Examines fact visibility before clarification and correction.
        Assumptions: A judge must not treat future inputs as already supplied.
        Expectations: Initial clarification sees no readiness; initial dates omit repairs.
        """
        cases = {case["id"]: case for case in load_suite()["cases"]}
        for case_id in ("T06", "T13"):
            case = cases[case_id]
            self.assertEqual(_available_source_facts(case, case["turns"][0]), [])
        case = cases["T04"]
        initial = {fact["id"] for fact in _available_source_facts(case, case["turns"][0])}
        self.assertEqual(initial, {"T04-F1", "T04-F4"})


if __name__ == "__main__":
    unittest.main()
