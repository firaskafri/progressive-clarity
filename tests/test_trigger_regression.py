"""Name: Advisory v0.4 trigger and transcript-regression contract suite.

Description: Validates topic-oriented skill discovery, practical Full
composition, literal safety and repair gates, corrected host oracles, and a
static eligibility/presentation prompt fixture.
Assumptions: Host skill selection remains advisory and separate from output
conformance; fixture labels and transcript-derived checks are expectations
rather than observed current-host results.
Expectations: Factual and explained controlling-text prompts remain eligible
while focused/full presentation, purpose-specific shapes, and isolation
requirements stay explicit and mode-free.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.validate_repository import parse_frontmatter


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "trigger_regression.json"
EVAL_PATH = ROOT / "evals" / "cases.json"
SKILL_PATH = ROOT / "skills" / "progressive-clarity" / "SKILL.md"


def _evaluation_cases() -> dict[str, dict[str, object]]:
    """Return evaluation cases keyed by their stable IDs."""
    suite = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    return {case["id"]: case for case in suite["cases"]}


class TriggerRegressionTests(unittest.TestCase):
    """Name: Advisory activation and v0.4 semantic-regression boundary.

    Description: Checks topic cadence language, literal protocol templates,
    practical repetition scoring, and corrected T01/T03/T06/T07 host oracles.
    Assumptions: Prompt labels do not simulate ChatGPT or guarantee invocation.
    Expectations: Metadata, fixtures, and isolation rules remain explicit,
    advisory, and aligned with protocol 0.4.
    """

    def test_description_and_trigger_fixture_contract(self) -> None:
        """Name: Front-loaded activation fixture.

        Description: Validates focused/full discovery language, controlling-text
        eligibility, the gold prompt, narrow follow-up, checkpoint, and
        purpose-specific contrasts.
        Assumptions: Standard frontmatter and fixture schema 2.0.0 describe
        static eligibility rather than observed host activation.
        Expectations: Thirteen unique cases preserve the reviewed shape boundary.
        """
        errors: list[str] = []
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        fields = parse_frontmatter(skill_text, errors)
        self.assertEqual(errors, [])
        self.assertEqual(set(fields), {"name", "description", "license"})

        description = fields["description"]
        normalized_description = " ".join(
            re.sub(r"^(?:>-?|[|]-?)\s*", "", description).split()
        )
        normalized_skill_text = " ".join(skill_text.split())
        self.assertLessEqual(len(description), 1024)
        self.assertTrue(
            normalized_description.startswith(
                "Applies topic-oriented Progressive Clarity"
            )
        )
        self.assertIn("Focused format", normalized_description)
        self.assertIn("Full three-view format", normalized_description)
        self.assertIn("consequential orientation", normalized_description)
        self.assertIn("complete procedures", normalized_description)
        self.assertNotRegex(
            normalized_description.lower(),
            r"\b(?:progressive mode|verbose mode|sticky mode)\b",
        )
        required_guidance = (
            "For a simple fact, the maximum is three sentences",
            "Every deeper view must be dominated by new information",
            "Extract its complete propositions into a “do not restate” ledger",
            "Delete any concluding recap from At depth",
            "Governing input: <missing dependency>.",
            "Example assumption: <number and the assumption that justifies it>.",
            "do not replace it with a clarification question",
            "state only the supplied change",
            "A list embedded in one sentence is still a catalogue",
            "Keep it only when it adds new evidence",
            "Keep At a glance to the decision",
            "When At depth ends with a list",
            "Do not clarify when visible facts already determine a bounded answer",
            "Earlier I said <withdrawn statement>. That was wrong or incomplete.",
            "output only one clarification question",
            "Do not treat that answer as a new first orientation",
            "not a substitute for a requested narrative",
            "Do not insert qualifiers, dates, or scope",
            "For an open-ended fiction request",
            "Controlling text:",
            "Non-controlling plain-language summary:",
            "Only verbatim-only reproduction remains outside Skill activation",
        )
        for guidance in required_guidance:
            with self.subTest(guidance=guidance):
                self.assertIn(guidance, normalized_skill_text)

        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(set(fixture), {"schema_version", "purpose", "cases"})
        self.assertEqual(fixture["schema_version"], "2.0.0")
        cases = fixture["cases"]
        self.assertEqual(
            [case["id"] for case in cases],
            [f"TR{number:02d}" for number in range(1, 14)],
        )
        self.assertTrue(
            all(
                set(case)
                == {
                    "id",
                    "prompt",
                    "eligible_for_skill",
                    "expected_presentation_if_applied",
                    "rationale",
                }
                for case in cases
            )
        )
        prompts = [case["prompt"] for case in cases]
        self.assertEqual(len(prompts), len(set(prompts)))
        self.assertEqual(prompts[0], "gold prices and forecasts")
        self.assertEqual(
            [case["eligible_for_skill"] for case in cases].count(True),
            8,
        )
        self.assertEqual(
            [case["eligible_for_skill"] for case in cases].count(False),
            5,
        )
        self.assertEqual(
            [
                case["expected_presentation_if_applied"]
                for case in cases
            ].count("focused"),
            2,
        )
        self.assertTrue(cases[11]["eligible_for_skill"])
        self.assertFalse(cases[12]["eligible_for_skill"])
        self.assertIn("requested explanation", cases[11]["rationale"])
        self.assertIn("Verbatim-only", cases[12]["rationale"])

    def test_redis_transcript_regressions_remain_explicit(self) -> None:
        """Name: Redis transcript regressions.

        Description: Checks the lifecycle oracle for verbosity, repetition,
        and unsupported numeric defaults observed in live ChatGPT output.
        Assumptions: T01 remains the canonical Redis lifecycle regression.
        Expectations: T01 captures focused and numeric failures while the Full
        rubric captures complete-conclusion repetition.
        """
        suite = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
        lifecycle = _evaluation_cases()["T01"]
        prohibited = [
            behavior
            for turn in lifecycle["turns"]
            for behavior in turn["expected"]["prohibited_behavior"]
        ]

        self.assertTrue(any("three sentences" in item for item in prohibited))
        self.assertTrue(any("use-case catalogue" in item for item in prohibited))
        self.assertIn("complete earlier conclusion", suite["rubric"]["full"])
        self.assertTrue(any("numeric value or range" in item for item in prohibited))
        self.assertIs(
            lifecycle["turns"][2]["expected"]["numeric_template_required"],
            True,
        )

    def test_revised_oracles_supply_decision_inputs(self) -> None:
        """Name: Revised clarification and re-synthesis oracles.

        Description: Checks grounded T03 planning, dynamic T04 repairs, the T05
        warning contract, complete T06 clarification, purpose-specific T08/T09
        prompts, a grounded T10 decision, and authorized continuation policy.
        Assumptions: Missing recommendation inputs should trigger clarification,
        while supplied narratives, procedures, and decisions should be answered.
        Expectations: Every oracle supplies or requests the facts and artifact
        shape it later scores without leaking a future correction.
        """
        cases = _evaluation_cases()
        suite = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
        migration = cases["T03"]
        corrections = cases["T04"]
        warning = cases["T05"]
        clarification = cases["T06"]
        narrative = cases["T08"]
        procedure = cases["T09"]
        return_case = cases["T10"]

        self.assertEqual(
            migration["turns"][0]["prompt"],
            (
                "The migration is approved for Saturday. The runbook freezes "
                "writes, takes a verified backup, runs the migration, validates "
                "critical queries, and rolls back on checksum mismatch. Give the "
                "team a consequential Full orientation, explicitly including that "
                "the runbook runs the migration. Allocate each control to one view, "
                "do not rewrite a standalone procedure, and end At depth with a "
                "prospective recommendation about evidence that should be retained; "
                "do not claim any validation artifact is already retained."
            ),
        )
        self.assertEqual(
            migration["turns"][1]["prompt"],
            (
                "Update: the migration window, including the database freeze, "
                "moved from Saturday to Sunday."
            ),
        )
        self.assertEqual(
            migration["turns"][2]["prompt"],
            (
                "What changes in the rollout plan because of that? In Full format, "
                "At a glance states the Sunday shift and preserved runbook controls; "
                "In context updates only supplied schedule artifacts and does not "
                "infer staffing, roles, or handoffs; At depth states that external "
                "dependencies are unsupplied and gives a generic verification record "
                "without asserting that any dependency exists. End with the last new "
                "checklist item and do not append a recap."
            ),
        )
        self.assertEqual(
            corrections["turns"][0]["prompt"],
            (
                "The review is Tuesday, and production coverage is Tuesday. "
                "Confirm both dates."
            ),
        )
        self.assertEqual(
            [
                turn["expected"]["required_fact_ids"]
                for turn in corrections["turns"][1:]
            ],
            [
                ["T04-F1", "T04-F2"],
                ["T04-F2", "T04-F3", "T04-F4"],
            ],
        )
        self.assertTrue(
            all(
                turn["expected"]["correction_required"] is True
                for turn in corrections["turns"][1:]
            )
        )
        self.assertEqual(
            warning["turns"][0]["expected"]["warning_at_a_glance_requires"],
            [
                "prohibited action",
                "hazardous state",
                "concrete harm",
                "immediate containment",
                "condition for resuming",
            ],
        )
        self.assertEqual(
            warning["turns"][0]["expected"]["required_fact_ids"],
            ["T05-F1", "T05-F2", "T05-F3", "T05-F4"],
        )
        self.assertIn(
            "Resume only after authoritative state is established",
            warning["turns"][0]["prompt"],
        )
        self.assertEqual(
            clarification["turns"][1]["expected"]["presentation"],
            "focused",
        )
        self.assertEqual(
            clarification["turns"][1]["expected"]["required_fact_ids"],
            ["T06-F2", "T06-F3", "T06-F4", "T06-F5", "T06-F6"],
        )
        clarification_prohibitions = clarification["turns"][0]["expected"][
            "prohibited_behavior"
        ]
        self.assertTrue(
            any("omits environment" in item for item in clarification_prohibitions)
        )
        self.assertIn(
            "Claiming risk is low",
            clarification["turns"][1]["expected"]["prohibited_behavior"],
        )
        self.assertIn(
            "Given those inputs, answer my original question.",
            clarification["turns"][1]["prompt"],
        )
        self.assertEqual(
            narrative["turns"][0]["prompt"],
            (
                "Write a first-person scene about opening an unfamiliar door, "
                "with no headings."
            ),
        )
        self.assertIn(
            "without asking for system-specific details",
            procedure["turns"][0]["prompt"],
        )
        self.assertEqual(
            return_case["turns"][0]["prompt"],
            (
                "The Atlas decision is to require reconciliation before rollback "
                "because incomplete reconciliation can make rollback unsafe. "
                "Explain it in Full format: At a glance states only the decision "
                "and immediate risk; In context adds only new rationale; At depth "
                "lists only implementation questions not already named."
            ),
        )
        self.assertEqual(
            return_case["turns"][0]["expected"]["required_fact_ids"],
            ["T10-F1", "T10-F3"],
        )
        self.assertEqual(
            return_case["turns"][2]["expected"]["required_fact_ids"],
            ["T10-F3"],
        )
        self.assertIsNone(
            suite["run_policy"]["remediation"]["maximum_cycles"],
        )
        self.assertIn(
            "authorized controlled remediation cycles",
            suite["run_policy"]["remediation"]["continuation_authorization"],
        )

    def test_practical_repetition_and_literal_label_oracles(self) -> None:
        """Name: Practical repetition and controlling-label regressions.

        Description: Confirms Full scoring permits necessary anchors while
        rejecting complete restatements and recaps, and T07 rejects Summary:.
        Assumptions: Semantic host scoring remains advisory and explicit in the
        frozen rubric rather than inferred by lexical identifier counts.
        Expectations: The v0.4 rubric and T07 oracle contain every bounded rule.
        """
        suite = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
        full_rubric = suite["rubric"]["full"]
        controlling = _evaluation_cases()["T07"]["turns"][0]["expected"]

        self.assertIn("necessary short anchors", full_rubric)
        self.assertIn("complete earlier conclusion", full_rubric)
        self.assertIn("At-depth recap", full_rubric)
        self.assertEqual(
            controlling["summary_label_must_contain"],
            "Non-controlling plain-language summary:",
        )
        self.assertTrue(
            any(
                "Using Summary:" in item
                for item in controlling["prohibited_behavior"]
            )
        )


if __name__ == "__main__":
    unittest.main()
