"""Name: Blinded reader-study preparation.

Description: Tests matched report validation and counterbalanced packet assignment.
Assumptions: Reports capture the same tasks and model under four instruction arms.
Expectations: Readers see one variant per case without labels or judge metadata.
"""

from __future__ import annotations

import copy
import json
import unittest
from collections import Counter

from tools.azure_eval_harness import CONDITIONS, RESULT_SCHEMA_VERSION, HarnessError
from tools.prepare_reader_study import prepare_packets


def _reports() -> list[dict[str, object]]:
    return [
        {
            "schema_version": RESULT_SCHEMA_VERSION, "status": "COMPLETE",
            "condition": condition, "suite_sha256": "suite", "protocol_sha256": "protocol",
            "model": {"deployment": "same-model"}, "split": "reader_study",
            "selected_case_ids": ["A", "B"],
            "planned_case_run_keys": ["A/run-1", "B/run-1"],
            "judge": {"private_score": "not-for-readers"},
            "runs": [{
                "case_id": case_id, "run_number": 1,
                "turns": [{"turn": 1, "prompt": f"Task {case_id}", "raw_output": "An answer."}],
            } for case_id in ("A", "B")],
        }
        for condition in CONDITIONS
    ]


class ReaderStudyTests(unittest.TestCase):
    """Name: Balanced, matched, blinded packet construction.

    Description: Checks assignment, reproducibility, leakage, and mismatched inputs.
    Assumptions: Style itself may reveal an arm; metadata must not reveal it.
    Expectations: Every case receives all arms across four readers without repeats.
    """

    def test_balancing_and_blinding_preserve_raw_conversations(self) -> None:
        """Name: Blinded counterbalancing.

        Description: Builds four reader packets twice with the same frozen seed.
        Assumptions: A reader must not see the same case in multiple conditions.
        Expectations: Assignments balance, bytes reproduce, and score labels vanish.
        """
        packets, key = prepare_packets(_reports(), seed=7)
        self.assertEqual((packets, key), prepare_packets(_reports(), seed=7))
        self.assertNotIn("condition", json.dumps(packets))
        self.assertNotIn("private_score", json.dumps(packets))
        self.assertNotIn("same-model", json.dumps(packets))
        for case in ("A", "B"):
            counts = Counter(
                item["condition"] for item in key["assignments"] if item["case_id"] == case
            )
            self.assertEqual(counts, Counter(CONDITIONS))
        for packet in packets["packets"]:
            self.assertEqual(len(packet["tasks"]), 2)
            self.assertEqual(
                {task["conversation"][0]["user"] for task in packet["tasks"]},
                {"Task A", "Task B"},
            )
            self.assertTrue(all(
                task["conversation"][0]["assistant"] == "An answer."
                for task in packet["tasks"]
            ))

    def test_mismatched_or_incomplete_reports_are_rejected(self) -> None:
        """Name: Matched comparison boundary.

        Description: Changes settings, prompts, completeness, and condition identity.
        Assumptions: Unmatched generations cannot support controlled comparisons.
        Expectations: Every mismatch fails before producing reader packets.
        """
        for change in ("model", "prompt", "empty", "condition", "status"):
            reports = copy.deepcopy(_reports())
            if change == "model":
                reports[0]["model"] = {"deployment": "other-model"}
            elif change == "prompt":
                reports[0]["runs"][0]["turns"][0]["prompt"] = "Different task"
            elif change == "empty":
                reports[0]["runs"][0]["turns"] = []
            elif change == "condition":
                reports[0]["condition"] = "revised"
            else:
                reports[0]["status"] = "INTERRUPTED"
            with self.subTest(change=change), self.assertRaises(HarnessError):
                prepare_packets(reports, seed=7)
        with self.assertRaises(HarnessError):
            prepare_packets(_reports(), seed=7, readers=3)


if __name__ == "__main__":
    unittest.main()
