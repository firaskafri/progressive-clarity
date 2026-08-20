"""Name: Topic-oriented presentation policy tests.

Description: Verifies deterministic response-shape selection and target-topic
resolution for new, continued, and resumed protocol-v0.4 conversations,
including shared invariants for parsed and directly constructed requests and
rejection of old-protocol state with the unchanged schema shape.
Assumptions: Trusted callers classify turn purpose; pc-core verifies the
classification contract without claiming semantic correctness.
Expectations: Every supported policy branch produces one stable response kind,
reason, and overview effect while invalid topic actions fail before generation.
"""

from __future__ import annotations

import unittest
from dataclasses import replace

from pc_core.model import (
    ConversationState,
    RequiredFact,
    SchemaError,
    StoredFact,
    TopicState,
)
from pc_core.policy import resolve_turn
from tests.helpers import valid_request


class PresentationPolicyTests(unittest.TestCase):
    """Name: Resolved turn policy scenarios.

    Description: Exercises automatic, explicit, and purpose-specific shape
    selection plus direct-request invariant failures against unsynthesized and
    oriented topics.
    Assumptions: Topic IDs and turn kinds are trusted caller metadata.
    Expectations: Policy precedence remains deterministic at every boundary.
    """

    def test_simple_fact_starts_focused_without_marking_overview(self) -> None:
        """Name: Simple first fact.

        Description: Resolves a simple fact on an unknown topic.
        Assumptions: The request starts a valid topic with automatic presentation.
        Expectations: The turn is focused and does not mark topic orientation.
        """
        resolved = resolve_turn(
            valid_request(turn_kind="simple_fact"),
            ConversationState.initial(),
        )

        self.assertEqual(resolved.expected_response_kind, "focused")
        self.assertEqual(resolved.reason, "ordinary_focused")
        self.assertFalse(resolved.marks_overview)

    def test_first_substantial_answer_uses_full_views(self) -> None:
        """Name: First consequential orientation.

        Description: Resolves a substantial first answer for a new topic.
        Assumptions: The answer can populate all three views with grounded detail.
        Expectations: Full views are required and successful output marks overview.
        """
        resolved = resolve_turn(valid_request(), ConversationState.initial())

        self.assertEqual(resolved.expected_response_kind, "views")
        self.assertEqual(resolved.reason, "first_substantial")
        self.assertTrue(resolved.marks_overview)

    def test_later_substantial_answer_is_focused_after_overview(self) -> None:
        """Name: Later ordinary exploration.

        Description: Resolves another substantial turn after topic orientation.
        Assumptions: No checkpoint, re-synthesis, or explicit full request exists.
        Expectations: The response stays focused and does not refresh overview.
        """
        state = ConversationState(
            active_topic_id="atlas",
            topics={
                "atlas": TopicState(has_committed_overview=True),
            },
        )
        resolved = resolve_turn(
            valid_request(topic_action="continue"),
            state,
        )

        self.assertEqual(resolved.expected_response_kind, "focused")
        self.assertFalse(resolved.marks_overview)

    def test_checkpoints_and_material_changes_use_full_views(self) -> None:
        """Name: Automatic full checkpoints.

        Description: Checks decisions, summaries, re-synthesis, and material repair.
        Assumptions: Each classification represents a meaningful topic checkpoint.
        Expectations: Every classification requires views and marks overview.
        """
        for turn_kind in (
            "decision_checkpoint",
            "summary_checkpoint",
            "material_resynthesis",
            "material_correction",
        ):
            with self.subTest(turn_kind=turn_kind):
                resolved = resolve_turn(
                    valid_request(turn_kind=turn_kind),
                    ConversationState.initial(),
                )
                self.assertEqual(resolved.expected_response_kind, "views")
                self.assertTrue(resolved.marks_overview)

    def test_explicit_presentation_overrides_automatic_cadence(self) -> None:
        """Name: Explicit presentation request.

        Description: Applies focused and full requests to checkpoints, simple
        facts, and opposite correction cadences.
        Assumptions: Purpose-specific artifact shapes are not involved.
        Expectations: Explicit focused/full instructions control visible shape.
        """
        focused = resolve_turn(
            valid_request(
                turn_kind="decision_checkpoint",
                presentation_request="focused",
            ),
            ConversationState.initial(),
        )
        full = resolve_turn(
            valid_request(
                turn_kind="simple_fact",
                presentation_request="full",
            ),
            ConversationState.initial(),
        )
        focused_material_correction = resolve_turn(
            valid_request(
                turn_kind="material_correction",
                presentation_request="focused",
            ),
            ConversationState.initial(),
        )
        full_narrow_correction = resolve_turn(
            valid_request(
                turn_kind="narrow_correction",
                presentation_request="full",
            ),
            ConversationState.initial(),
        )

        self.assertEqual(focused.expected_response_kind, "focused")
        self.assertFalse(focused.marks_overview)
        self.assertEqual(full.expected_response_kind, "views")
        self.assertFalse(full.marks_overview)
        self.assertEqual(
            focused_material_correction.expected_response_kind,
            "focused",
        )
        self.assertEqual(full_narrow_correction.expected_response_kind, "views")
        self.assertFalse(full_narrow_correction.marks_overview)

    def test_purpose_specific_shapes_outrank_presentation(self) -> None:
        """Name: Purpose-specific shape precedence.

        Description: Requests full presentation for clarification and non-fit turns.
        Assumptions: Their functional output shape must remain intact.
        Expectations: Control and non-fit kinds override the presentation request.
        """
        clarification = resolve_turn(
            valid_request(
                turn_kind="clarification",
                presentation_request="full",
            ),
            ConversationState.initial(),
        )
        non_fit = resolve_turn(
            valid_request(
                turn_kind="non_fit",
                presentation_request="full",
                non_fit_kind="exact_output",
            ),
            ConversationState.initial(),
        )

        self.assertEqual(clarification.expected_response_kind, "control")
        self.assertEqual(non_fit.expected_response_kind, "non_fit")

    def test_resume_restores_known_inactive_topic(self) -> None:
        """Name: Known topic resumption.

        Description: Selects an oriented inactive topic after another topic.
        Assumptions: Both topic records are committed and immutable.
        Expectations: The resumed topic controls policy and retains its overview.
        """
        atlas = TopicState(has_committed_overview=True)
        state = ConversationState(
            active_topic_id="beacon",
            topics={"atlas": atlas, "beacon": TopicState()},
        )
        resolved = resolve_turn(
            valid_request(topic_action="resume"),
            state,
        )

        self.assertIs(resolved.topic, atlas)
        self.assertEqual(resolved.expected_response_kind, "focused")

    def test_invalid_topic_action_fails_before_generation(self) -> None:
        """Name: Invalid topic transition.

        Description: Attempts to resume a topic that has not been committed.
        Assumptions: State contains no matching inactive topic.
        Expectations: Policy raises a schema error before a host can run.
        """
        with self.assertRaisesRegex(SchemaError, "known inactive"):
            resolve_turn(
                valid_request(topic_action="resume"),
                ConversationState.initial(),
            )

    def test_direct_objects_still_enforce_policy_contracts(self) -> None:
        """Name: Direct policy input validation.

        Description: Bypasses JSON parsing with an invalid action and v0.3
        protocol state.
        Assumptions: Embedders may construct exported dataclasses directly.
        Expectations: Resolution rejects unknown actions and old protocol versions.
        """
        invalid_request = replace(valid_request(), topic_action="invalid")
        with self.assertRaisesRegex(SchemaError, "topic_action"):
            resolve_turn(invalid_request, ConversationState.initial())

        incompatible_state = ConversationState(protocol_version="0.3")
        with self.assertRaisesRegex(SchemaError, "protocol_version"):
            resolve_turn(valid_request(), incompatible_state)

    def test_direct_request_invariants_match_parsed_requests(self) -> None:
        """Name: Shared direct-request invariants.

        Description: Constructs invalid quotation, non-fit, summary-cap,
        clarification-catalog, lexical-fact, and ledger-conflict combinations.
        Assumptions: Direct embedders and parsed requests share one invariant owner.
        Expectations: Policy rejects every invalid combination with SchemaError.
        """
        for controlling_text in (None, "", "   "):
            with self.subTest(controlling_text=controlling_text):
                source_less_quotation = replace(
                    valid_request(),
                    turn_kind="quotation",
                    controlling_text=controlling_text,
                )
                with self.assertRaisesRegex(
                    SchemaError,
                    "requires trusted text|non-empty string",
                ):
                    resolve_turn(
                        source_less_quotation,
                        ConversationState.initial(),
                    )

        invalid_requests = (
            (
                replace(
                    valid_request(),
                    turn_kind="quotation",
                    controlling_text="Source",
                    summary_max_words=0,
                ),
                "summary_max_words",
            ),
            (
                replace(
                    valid_request(),
                    turn_kind="non_fit",
                    non_fit_kind=None,
                ),
                "non_fit_kind",
            ),
            (
                replace(valid_request(), required_facts=()),
                "must not be empty",
            ),
            (
                replace(
                    valid_request(turn_kind="clarification"),
                    required_facts=(
                        RequiredFact(id="ATLAS-F9", text="Fact."),
                    ),
                ),
                "clarification cannot render facts",
            ),
        )
        for request, message in invalid_requests:
            with self.subTest(message=message):
                with self.assertRaisesRegex(SchemaError, message):
                    resolve_turn(request, ConversationState.initial())

        with self.assertRaisesRegex(SchemaError, "one physical line"):
            RequiredFact(id="ATLAS-F9", text="Line one.\nLine two.")

        state = ConversationState(
            active_topic_id="atlas",
            turn=1,
            topics={
                "atlas": TopicState(
                    facts={
                        "ATLAS-F1": StoredFact(
                            text="Committed text.",
                            first_turn=1,
                        )
                    }
                )
            },
        )
        conflicting = valid_request(
            topic_action="continue",
            required_facts=[
                {"id": "ATLAS-F1", "text": "Different text."}
            ],
        )
        with self.assertRaisesRegex(SchemaError, "conflicts with committed"):
            resolve_turn(conflicting, state)


if __name__ == "__main__":
    unittest.main()
