"""Name: Topic-oriented structured envelope validation suite.

Description: Covers focused and full schemas, full-view order and budgets,
warnings, multi-topic state transitions, response-local fact placement,
permitted short anchors, exact sentence and list duplicates, semantic recap
boundaries, authoritative coverage, corrections, quotations, clarifications,
exact non-fit preservation, and canonical rendering.
Assumptions: Trusted requests and committed state are supplied separately from
model candidates; semantic truth is outside deterministic validation.
Expectations: Mechanically decidable violations fail closed, valid candidates
produce transactional state, and advisory claims remain UNVERIFIED.
"""

from __future__ import annotations

import hashlib
import unittest
from dataclasses import replace

from pc_core.model import (
    ENVELOPE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    ConversationState,
    DeclaredState,
    Envelope,
    Fact,
    SchemaError,
    TopicState,
    WrapperRequest,
)
from pc_core.policy import ResolvedTurn
from pc_core.render import render_markdown
from pc_core.validation import validate_envelope
from tests.helpers import (
    request_dict,
    valid_focused_dict,
    valid_focused_envelope,
    valid_full_dict,
    valid_request,
    valid_full_envelope,
)


def _first_state() -> ConversationState:
    report = validate_envelope(
        valid_full_envelope(),
        state=ConversationState.initial(),
        request=valid_request(),
    )
    if report.next_state is None:
        raise AssertionError("baseline fixture must validate")
    return report.next_state


class EnvelopeSchemaAndPresentationTests(unittest.TestCase):
    """Name: Schema, presentation, renderer, and budget checks.

    Description: Verifies closed fields, the only three-view sequence, exact
    canonical headings, non-empty prose, caller-authoritative fact coverage,
    direct-construction types, exact non-fit bytes, safety-warning arithmetic,
    and 40/200 boundaries.
    Assumptions: The baseline fixture is a new substantial in-scope response.
    Expectations: Structural or arithmetic drift prevents certification.
    """

    def test_valid_envelope_is_mechanically_certifiable(self) -> None:
        """Name: Valid v0.4 full baseline.

        Description: Validates all three sections, facts, counts, and state.
        Assumptions: Request metadata identifies a new substantial topic.
        Expectations: Mechanical checks pass and semantic checks stay
        UNVERIFIED.
        """
        report = validate_envelope(
            valid_full_envelope(),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertTrue(report.certifiable)
        self.assertEqual(report.next_state.turn, 1)
        self.assertEqual(len(report.next_state.topics["atlas"].facts), 4)
        self.assertTrue(
            report.next_state.topics["atlas"].has_committed_overview
        )
        self.assertTrue(
            all(value == "UNVERIFIED" for value in report.advisory_checks.values())
        )

    def test_envelope_payload_is_deeply_immutable(self) -> None:
        """Name: Immutable envelope payload.

        Description: Attempts to mutate top-level and nested parsed payload data.
        Assumptions: Validation and rendering must observe one stable candidate.
        Expectations: Both mapping writes fail after envelope construction.
        """
        envelope = valid_full_envelope()

        with self.assertRaises(TypeError):
            envelope.payload["correction"] = {}
        with self.assertRaises(TypeError):
            envelope.payload["sections"][0]["content"] = "Changed."

    def test_direct_envelope_components_reject_loose_types(self) -> None:
        """Name: Direct envelope component type safety.

        Description: Constructs a boolean transition counter and list-valued fact ID.
        Assumptions: Direct embedders must satisfy the same types as parsed JSON.
        Expectations: Both invalid values raise SchemaError before validation.
        """
        with self.assertRaisesRegex(SchemaError, "expected integer"):
            DeclaredState(
                turn_before=False,
                turn_after=1,
                branch_before=None,
                branch_after=None,
                prior_fact_count=0,
                next_fact_count=0,
            )
        with self.assertRaisesRegex(SchemaError, "expected string"):
            Fact(
                id=[],
                text="Invalid direct fact.",
                allocation="focused",
                reuse_reason=None,
            )

    def test_validation_report_mappings_are_immutable_snapshots(self) -> None:
        """Name: Immutable validation report.

        Description: Attempts to rewrite counts and check results after validation.
        Assumptions: Audit consumers may retain reports beyond the validation call.
        Expectations: Report mappings reject mutation and preserve certified data.
        """
        report = validate_envelope(
            valid_full_envelope(),
            state=ConversationState.initial(),
            request=valid_request(),
        )

        with self.assertRaises(TypeError):
            report.counts["at_a_glance"] = 999
        with self.assertRaises(TypeError):
            report.mechanical_checks["schema_and_versions"] = "FAIL"

    def test_focused_response_is_certified_without_view_budgets(self) -> None:
        """Name: Focused response certification.

        Description: Validates a simple answer with authoritative visible facts.
        Assumptions: Simple facts require no topic overview or three-view budget.
        Expectations: Focused rendering passes, remains heading-free, and leaves
        the overview marker unset.
        """
        request = valid_request(
            turn_kind="simple_fact",
            required_facts=[
                {"id": "ATLAS-F1", "text": "Atlas is a data platform."}
            ],
        )
        report = validate_envelope(
            valid_focused_envelope(),
            state=ConversationState.initial(),
            request=request,
        )

        self.assertTrue(report.certifiable)
        self.assertEqual(
            report.mechanical_checks["english_word_budgets"],
            "NOT_APPLICABLE",
        )
        self.assertFalse(
            report.next_state.topics["atlas"].has_committed_overview
        )
        self.assertEqual(
            render_markdown(valid_focused_envelope()),
            "Atlas is a data platform.\n",
        )

    def test_focused_warning_renders_before_answer(self) -> None:
        """Name: Focused warning precedence.

        Description: Adds an indispensable warning to a focused simple answer.
        Assumptions: Focused responses have no view budget requiring exemption.
        Expectations: The warning renders first and both facts bind once.
        """
        data = valid_focused_dict()
        data["state"]["next_fact_count"] = 2
        data["facts"] = [
            {
                "id": "ATLAS-F1",
                "text": "Do not restart during split-brain.",
                "allocation": "focused",
                "reuse_reason": None,
            },
            {
                "id": "ATLAS-F2",
                "text": "Escalate to the incident commander.",
                "allocation": "focused",
                "reuse_reason": None,
            },
        ]
        data["payload"] = {
            "content": "Escalate to the incident commander.",
            "fact_ids": ["ATLAS-F2"],
            "warning": {
                "content": "Do not restart during split-brain.",
                "fact_ids": ["ATLAS-F1"],
                "reason": "Restart could lose acknowledged writes.",
            },
            "correction": None,
        }
        envelope = Envelope.from_dict(data)
        report = validate_envelope(
            envelope,
            state=ConversationState.initial(),
            request=valid_request(turn_kind="simple_fact"),
        )

        self.assertTrue(report.certifiable)
        self.assertTrue(
            render_markdown(envelope).startswith(
                "Do not restart during split-brain.\n\n"
            )
        )

    def test_focused_heading_detection_ignores_fences_and_rejects_setext(self) -> None:
        """Name: Markdown-aware focused headings.

        Description: Compares a reserved heading inside code with a Setext heading.
        Assumptions: User-requested code may contain literal protocol syntax.
        Expectations: Fenced syntax passes while a rendered reserved heading fails.
        """
        fenced = valid_focused_dict()
        fenced["payload"]["content"] = "Example:\n\n```\n## At depth\n```"
        fenced_report = validate_envelope(
            Envelope.from_dict(fenced),
            state=ConversationState.initial(),
            request=valid_request(turn_kind="simple_fact"),
        )
        self.assertTrue(fenced_report.certifiable)

        setext = valid_focused_dict()
        setext["payload"]["content"] = "At depth\n--------"
        setext_report = validate_envelope(
            Envelope.from_dict(setext),
            state=ConversationState.initial(),
            request=valid_request(turn_kind="simple_fact"),
        )
        self.assertFalse(setext_report.mechanically_conformant)
        self.assertIn(
            "PC-M-HEADING-002",
            {item.code for item in setext_report.diagnostics},
        )

    def test_supplied_resolution_must_match_request_and_state(self) -> None:
        """Name: Forged policy resolution refusal.

        Description: Supplies a stale Full resolution for a simple focused turn.
        Assumptions: Validation independently derives policy from trusted inputs.
        Expectations: Policy mismatch prevents certification and state mutation.
        """
        request = valid_request(turn_kind="simple_fact")
        forged = ResolvedTurn(
            topic_id="atlas",
            topic_action="start",
            topic=TopicState(),
            turn_before=0,
            expected_response_kind="views",
            reason="forged",
            marks_overview=True,
        )
        report = validate_envelope(
            Envelope.from_dict(valid_focused_dict()),
            state=ConversationState.initial(),
            request=request,
            resolved=forged,
        )

        self.assertFalse(report.mechanically_conformant)
        self.assertIsNone(report.next_state)
        self.assertIn(
            "PC-M-POLICY-002",
            {item.code for item in report.diagnostics},
        )

    def test_invalid_direct_request_fails_without_downstream_type_errors(self) -> None:
        """Name: Invalid direct request short circuit.

        Description: Supplies an unhashable list as a direct turn classification.
        Assumptions: Policy validation owns request invariants before other checks.
        Expectations: Validation returns one policy failure without raising.
        """
        invalid_request = replace(valid_request(), turn_kind=[])
        report = validate_envelope(
            valid_full_envelope(),
            state=ConversationState.initial(),
            request=invalid_request,
        )

        self.assertFalse(report.mechanically_conformant)
        self.assertIsNone(report.next_state)
        self.assertIn(
            "PC-M-POLICY-001",
            {item.code for item in report.diagnostics},
        )

    def test_removed_mode_field_is_rejected(self) -> None:
        """Name: Removed dual-mode field.

        Description: Adds the removed top-level mode field to a current envelope.
        Assumptions: Mode selection no longer exists in the closed schema.
        Expectations: Strict parsing raises SchemaError.
        """
        data = valid_full_dict()
        data["mode"] = "progressive"
        with self.assertRaises(SchemaError):
            Envelope.from_dict(data)

    def test_removed_view_override_is_rejected(self) -> None:
        """Name: Removed one-view request field.

        Description: Adds the removed view_override field to a current request.
        Assumptions: Presentation uses the closed presentation_request field,
        not a per-view override.
        Expectations: Strict request parsing raises SchemaError.
        """
        data = request_dict()
        data["view_override"] = "at_depth"
        with self.assertRaises(SchemaError):
            WrapperRequest.from_dict(data)

    def test_single_or_reordered_view_fails(self) -> None:
        """Name: Mandatory three-view order.

        Description: Checks both a single section and swapped shallow sections.
        Assumptions: Every in-scope views response has all three ordered views.
        Expectations: Both candidates fail the heading-order check.
        """
        for mutate in ("single", "swapped"):
            with self.subTest(mutate=mutate):
                data = valid_full_dict()
                if mutate == "single":
                    data["payload"]["sections"] = data["payload"]["sections"][:1]
                else:
                    data["payload"]["sections"][0:2] = reversed(
                        data["payload"]["sections"][0:2]
                    )
                report = validate_envelope(
                    Envelope.from_dict(data),
                    state=ConversationState.initial(),
                    request=valid_request(),
                )
                self.assertFalse(report.mechanically_conformant)
                self.assertIn(
                    "PC-M-HEADING-001",
                    {item.code for item in report.diagnostics},
                )

    def test_each_required_view_rejects_empty_or_whitespace_content(self) -> None:
        """Name: Non-empty three-view prose.

        Description: Empties each required section independently using blank and
        whitespace-only values.
        Assumptions: A warning cannot substitute for the additive section prose.
        Expectations: Strict envelope parsing rejects every empty required view
        before certification.
        """
        for section_index, content in ((0, ""), (1, " \n\t"), (2, "")):
            with self.subTest(section_index=section_index):
                data = valid_full_dict()
                data["payload"]["sections"][section_index]["content"] = content
                with self.assertRaises(SchemaError):
                    Envelope.from_dict(data)
        punctuation_only = valid_full_dict()
        punctuation_only["payload"]["sections"][1]["content"] = "---"
        report = validate_envelope(
            Envelope.from_dict(punctuation_only),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-CONTENT-001",
            {item.code for item in report.diagnostics},
        )

    def test_glance_boundary_accepts_forty_and_rejects_forty_one(self) -> None:
        """Name: At-a-glance property boundary.

        Description: Generates exact token counts at and above the hard cap.
        Assumptions: Generated wordN tokens each count as one English word.
        Expectations: Forty passes and forty-one produces PC-M-BUDGET-001.
        """
        for size, conformant in ((40, True), (41, False)):
            with self.subTest(size=size):
                data = valid_full_dict()
                data["payload"]["sections"][0]["content"] = " ".join(
                    f"word{index}" for index in range(size)
                )
                report = validate_envelope(
                    Envelope.from_dict(data),
                    state=ConversationState.initial(),
                    request=valid_request(),
                )
                self.assertEqual(report.mechanically_conformant, conformant)

    def test_through_context_boundary_rejects_two_hundred_one(self) -> None:
        """Name: Cumulative shallow per-response cap.

        Description: Makes At a glance plus In context contain 201 words.
        Assumptions: At a glance remains independently within its 40-word cap.
        Expectations: PC-M-BUDGET-003 rejects the response.
        """
        data = valid_full_dict()
        data["payload"]["sections"][0]["content"] = " ".join(
            f"glance{index}" for index in range(40)
        )
        data["payload"]["sections"][1]["content"] = " ".join(
            f"context{index}" for index in range(161)
        )
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-BUDGET-003", {item.code for item in report.diagnostics}
        )

    def test_structured_warning_is_budget_exempt_but_advisory(self) -> None:
        """Name: Indispensable-warning exception and placement.

        Description: Places a 45-word warning before non-empty normal glance
        prose, then moves the same structured warning to At depth and reorders
        that section first.
        Assumptions: pc-core can verify placement but not indispensability.
        Expectations: At-a-glance placement passes with indispensability
        UNVERIFIED; deeper placement fails mechanically.
        """
        data = valid_full_dict()
        first = data["payload"]["sections"][0]
        first["content"] = "Proceed cautiously."
        first["fact_ids"] = []
        first["warning"] = {
            "content": " ".join(f"danger{index}" for index in range(45)),
            "fact_ids": ["ATLAS-F1"],
            "reason": "Immediate safety warning supplied by the source.",
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(
            report.advisory_checks["warning_indispensability"], "UNVERIFIED"
        )
        depth = data["payload"]["sections"][2]
        depth["warning"] = first["warning"]
        first["warning"] = None
        misplaced = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertFalse(misplaced.mechanically_conformant)
        self.assertIn(
            "PC-M-WARNING-001",
            {item.code for item in misplaced.diagnostics},
        )
        data["payload"]["sections"].insert(
            0,
            data["payload"]["sections"].pop(2),
        )
        reordered = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertEqual(
            reordered.mechanical_checks["full_warning_placement"],
            "FAIL",
        )

    def test_authoritative_catalog_requires_declared_exact_visible_text(self) -> None:
        """Name: Authoritative fact catalog coverage.

        Description: Checks a covered fact, an omitted ID, and a declared fact
        whose authoritative text does not occur in its referenced output.
        Assumptions: Catalog text is trusted caller input and exact normalized
        lexical presence is intentionally stricter than semantic paraphrase.
        Expectations: Only exact declared-and-visible coverage certifies, while
        semantic completeness beyond the supplied catalog remains UNVERIFIED.
        """
        scenarios = (
            (
                [{"id": "ATLAS-F2", "text": "Migration takes two weekends."}],
                True,
                None,
            ),
            (
                [{"id": "ATLAS-F9", "text": "Legal approved the migration."}],
                False,
                "PC-M-REQUIRED-001",
            ),
            (
                [{"id": "ATLAS-F1", "text": "Atlas should be adopted."}],
                False,
                "PC-M-REQUIRED-003",
            ),
        )
        for catalog, conformant, expected_code in scenarios:
            with self.subTest(expected_code=expected_code):
                report = validate_envelope(
                    valid_full_envelope(),
                    state=ConversationState.initial(),
                    request=valid_request(required_facts=catalog),
                )
                self.assertEqual(report.mechanically_conformant, conformant)
                self.assertEqual(
                    report.mechanical_checks["authoritative_fact_coverage"],
                    "PASS" if conformant else "FAIL",
                )
                if expected_code is not None:
                    self.assertIn(
                        expected_code,
                        {item.code for item in report.diagnostics},
                    )
                self.assertEqual(
                    report.advisory_checks["semantic_completeness"],
                    "UNVERIFIED",
                )

    def test_authoritative_catalog_rejects_partial_token_matches(self) -> None:
        """Name: Authoritative fact token boundary.

        Description: Places the required fact text only inside a longer word.
        Assumptions: Normalized exact coverage requires complete lexical tokens.
        Expectations: PC-M-REQUIRED-003 rejects the substring-only match.
        """
        data = valid_full_dict()
        data["facts"][0]["text"] = "cost"
        data["payload"]["sections"][0]["content"] = (
            "A costly migration is likely."
        )
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(
                required_facts=[{"id": "ATLAS-F1", "text": "cost"}],
            ),
        )
        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-REQUIRED-003",
            {item.code for item in report.diagnostics},
        )

    def test_renderer_emits_exact_headings_once(self) -> None:
        """Name: Canonical heading renderer.

        Description: Renders a validated envelope and extracts protocol headings.
        Assumptions: Candidate content cannot inject protocol headings.
        Expectations: Exactly three level-two headings appear in required order.
        """
        headings = [
            line
            for line in render_markdown(valid_full_envelope()).splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(
            headings,
            ["## At a glance", "## In context", "## At depth"],
        )

    def test_accepted_non_fit_payload_preserves_bytes_and_skips_view_checks(
        self,
    ) -> None:
        """Name: Accepted non-fit payload preservation.

        Description: Validates an accepted artifact containing a protocol-like
        heading, a repeated lexical unit, and no terminal newline.
        Assumptions: The wrapper lacks trusted intended-artifact bytes; accepted
        non-fit output still outranks view checks and receives no added newline.
        Expectations: Validation passes, view-only checks are not applicable,
        rendering preserves accepted bytes, and intended equality is UNVERIFIED.
        """
        content = "## At a glance\nrepeat exactly.\nrepeat exactly."
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "non_fit",
            "topic_id": "atlas",
            "topic_action": "start",
            "state": {
                "turn_before": 0,
                "turn_after": 1,
                "branch_before": None,
                "branch_after": None,
                "prior_fact_count": 0,
                "next_fact_count": 0,
            },
            "facts": [],
            "payload": {
                "non_fit_kind": "exact_output",
                "content": content,
                "fact_ids": [],
            },
        }
        envelope = Envelope.from_dict(data)
        report = validate_envelope(
            envelope,
            state=ConversationState.initial(),
            request=valid_request(
                turn_kind="non_fit",
                non_fit_kind="exact_output",
            ),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(
            report.mechanical_checks["three_view_heading_order"],
            "NOT_APPLICABLE",
        )
        self.assertEqual(
            report.mechanical_checks["exact_lexical_duplicate_detection"],
            "NOT_APPLICABLE",
        )
        self.assertEqual(
            report.advisory_checks["non_fit_intended_artifact_equality"],
            "UNVERIFIED",
        )
        self.assertEqual(render_markdown(envelope), content)

    def test_non_fit_kind_must_match_trusted_request(self) -> None:
        """Name: Trusted non-fit subtype.

        Description: Declares exact output for a trusted narrative request.
        Assumptions: Purpose-specific subtypes have different preservation rules.
        Expectations: The mismatched candidate fails before certification.
        """
        data = valid_focused_dict()
        data["response_kind"] = "non_fit"
        data["state"]["next_fact_count"] = 0
        data["facts"] = []
        data["payload"] = {
            "non_fit_kind": "exact_output",
            "content": "unchanged",
            "fact_ids": [],
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(
                turn_kind="non_fit",
                non_fit_kind="narrative",
            ),
        )

        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-KIND-004",
            {item.code for item in report.diagnostics},
        )


class StateFactAndExceptionTests(unittest.TestCase):
    """Name: State, practical repetition, facts, and exception handling.

    Description: Exercises cross-turn reuse, branches, permitted short anchors,
    exact sentence and list echoes, semantic recap boundaries, correction
    repair and false-withdrawal refusal, clarification control, and exact
    controlling text with literal labels and separately validated summary prose.
    Assumptions: The baseline response supplies trusted committed prior state.
    Expectations: New-information composition passes while complete lexical
    restatements fail and semantic-only judgments stay explicitly UNVERIFIED.
    """

    def test_prior_context_reuse_preserves_fact_identity(self) -> None:
        """Name: Necessary cross-turn fact reuse.

        Description: Reuses one committed fact once and adds two new facts.
        Assumptions: Cross-turn context may be necessary but cross-view recap is
        still prohibited.
        Expectations: Matching ID, text, current placement, and prior_context pass.
        """
        state = _first_state()
        data = valid_full_dict()
        data["topic_action"] = "continue"
        data["state"] = {
            "turn_before": 1,
            "turn_after": 2,
            "branch_before": None,
            "branch_after": None,
            "prior_fact_count": 4,
            "next_fact_count": 6,
        }
        data["facts"] = [
            {
                "id": "ATLAS-F1",
                "text": "Atlas should be adopted.",
                "allocation": "at_a_glance",
                "reuse_reason": "prior_context",
            },
            {
                "id": "ATLAS-F5",
                "text": "Finance owns migration funding.",
                "allocation": "in_context",
                "reuse_reason": None,
            },
            {
                "id": "ATLAS-F6",
                "text": "The funding gate closes Friday.",
                "allocation": "at_depth",
                "reuse_reason": None,
            },
        ]
        data["payload"]["sections"] = [
            {
                "view": "at_a_glance",
                "content": "Continue with the Atlas adoption.",
                "fact_ids": ["ATLAS-F1"],
                "warning": None,
            },
            {
                "view": "in_context",
                "content": "Finance owns migration funding.",
                "fact_ids": ["ATLAS-F5"],
                "warning": None,
            },
            {
                "view": "at_depth",
                "content": "The funding gate closes Friday.",
                "fact_ids": ["ATLAS-F6"],
                "warning": None,
            },
        ]
        report = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(
                topic_action="continue",
                turn_kind="decision_checkpoint",
            ),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(len(report.next_state.topics["atlas"].facts), 6)

    def test_targeted_followup_uses_focused_response(self) -> None:
        """Name: Focused targeted follow-up.

        Description: Selects a branch while answering only the requested detail.
        Assumptions: The topic already has a committed full overview.
        Expectations: Focused prose passes and the selected branch commits.
        """
        state = _first_state()
        data = valid_focused_dict()
        data["topic_action"] = "continue"
        data["state"] = {
            "turn_before": 1,
            "turn_after": 2,
            "branch_before": None,
            "branch_after": "security",
            "prior_fact_count": 4,
            "next_fact_count": 5,
        }
        data["facts"] = [
            {
                "id": "ATLAS-F5",
                "text": "Threat modeling starts Monday.",
                "allocation": "focused",
                "reuse_reason": None,
            }
        ]
        data["payload"] = {
            "content": "Threat modeling starts Monday.",
            "fact_ids": ["ATLAS-F5"],
            "warning": None,
            "correction": None,
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(
                topic_action="continue",
                turn_kind="narrow_followup",
            ),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(report.next_state.topics["atlas"].branch, "security")
        self.assertEqual(
            render_markdown(Envelope.from_dict(data)),
            "Threat modeling starts Monday.\n",
        )

    def test_narrow_correction_uses_focused_repair(self) -> None:
        """Name: Focused narrow correction.

        Description: Withdraws one prior claim ahead of a warning, accepts a
        correction-only body, then rejects loose, outdated, replacement-omitting,
        and duplicate repair prose.
        Assumptions: The correction changes a bounded fact but not topic action.
        Expectations: Only the exact withdrawal, retraction, replacement, and
        consequence opening validates first without exact sentence repetition.
        """
        state = _first_state()
        data = valid_focused_dict()
        data["topic_action"] = "continue"
        data["state"] = {
            "turn_before": 1,
            "turn_after": 2,
            "branch_before": None,
            "branch_after": None,
            "prior_fact_count": 4,
            "next_fact_count": 6,
        }
        data["facts"] = [
            {
                "id": "ATLAS-F1",
                "text": "Atlas should be adopted.",
                "allocation": "focused",
                "reuse_reason": "correction",
            },
            {
                "id": "ATLAS-F5",
                "text": "Atlas requires reevaluation.",
                "allocation": "focused",
                "reuse_reason": "correction",
            },
            {
                "id": "ATLAS-F6",
                "text": "Do not deploy Atlas during reevaluation.",
                "allocation": "focused",
                "reuse_reason": None,
            },
        ]
        data["payload"] = {
            "content": "Reevaluate Atlas before adoption.",
            "fact_ids": ["ATLAS-F5"],
            "warning": {
                "content": "Do not deploy Atlas during reevaluation.",
                "fact_ids": ["ATLAS-F6"],
                "reason": "Deployment would act on the withdrawn decision.",
            },
            "correction": {
                "content": (
                    "Earlier I said Atlas should be adopted. That was wrong or "
                    "incomplete. Atlas requires reevaluation. This changes the "
                    "action: reevaluate Atlas before adoption."
                ),
                "withdrawn_fact_ids": ["ATLAS-F1"],
                "replacement_fact_ids": ["ATLAS-F5"],
                "changed_action_fact_ids": ["ATLAS-F5"],
            },
        }
        envelope = Envelope.from_dict(data)
        report = validate_envelope(
            envelope,
            state=state,
            request=valid_request(
                topic_action="continue",
                turn_kind="narrow_correction",
            ),
        )

        self.assertTrue(report.certifiable)
        self.assertTrue(
            render_markdown(envelope).startswith(
                "Earlier I said Atlas should be adopted. That was wrong or"
            )
        )
        rendered = render_markdown(envelope)
        self.assertLess(
            rendered.index("Earlier I said"),
            rendered.index("Do not deploy Atlas"),
        )
        data["payload"]["content"] = ""
        data["payload"]["fact_ids"] = []
        correction_only = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(
                topic_action="continue",
                turn_kind="narrow_correction",
            ),
        )
        self.assertTrue(correction_only.certifiable)
        invalid_openings = (
            "Corrected: Atlas requires reevaluation.",
            (
                "Earlier I said Atlas should be adopted. That was outdated. "
                "Atlas requires reevaluation. This changes the action."
            ),
            (
                "Earlier I said Atlas should be adopted. That was wrong or "
                "incomplete. This changes the action."
            ),
        )
        for opening in invalid_openings:
            with self.subTest(opening=opening):
                data["payload"]["correction"]["content"] = opening
                loose_report = validate_envelope(
                    Envelope.from_dict(data),
                    state=state,
                    request=valid_request(
                        topic_action="continue",
                        turn_kind="narrow_correction",
                    ),
                )
                self.assertIn(
                    "PC-M-CORRECTION-006",
                    {item.code for item in loose_report.diagnostics},
                )
        data["payload"]["correction"]["content"] = (
            "Earlier I said Atlas should be adopted. That was wrong or "
            "incomplete. Atlas requires reevaluation. This changes the action: "
            "reevaluate Atlas before adoption. Atlas requires reevaluation."
        )
        duplicate_report = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(
                topic_action="continue",
                turn_kind="narrow_correction",
            ),
        )
        self.assertIn(
            "PC-M-DUPLICATE-001",
            {item.code for item in duplicate_report.diagnostics},
        )

    def test_focused_fact_can_move_into_later_full_view(self) -> None:
        """Name: Focused-to-full fact placement.

        Description: Reuses a focused fact in At a glance during orientation.
        Assumptions: Fact identity and text persist while placement is per response.
        Expectations: Synthesis reuse passes and the overview marker commits.
        """
        first = validate_envelope(
            Envelope.from_dict(valid_focused_dict()),
            state=ConversationState.initial(),
            request=valid_request(turn_kind="simple_fact"),
        )
        self.assertIsNotNone(first.next_state)

        data = valid_full_dict()
        data["topic_action"] = "continue"
        data["state"] = {
            "turn_before": 1,
            "turn_after": 2,
            "branch_before": None,
            "branch_after": None,
            "prior_fact_count": 1,
            "next_fact_count": 3,
        }
        data["facts"] = [
            {
                "id": "ATLAS-F1",
                "text": "Atlas is a data platform.",
                "allocation": "at_a_glance",
                "reuse_reason": "synthesis",
            },
            {
                "id": "ATLAS-F2",
                "text": "Migration takes two weekends.",
                "allocation": "in_context",
                "reuse_reason": None,
            },
            {
                "id": "ATLAS-F3",
                "text": "Security owns approval.",
                "allocation": "at_depth",
                "reuse_reason": None,
            },
        ]
        data["payload"]["sections"][0].update(
            {"content": "Atlas is a data platform.", "fact_ids": ["ATLAS-F1"]}
        )
        data["payload"]["sections"][1].update(
            {"content": "Migration takes two weekends.", "fact_ids": ["ATLAS-F2"]}
        )
        data["payload"]["sections"][2].update(
            {"content": "Security owns approval.", "fact_ids": ["ATLAS-F3"]}
        )
        report = validate_envelope(
            Envelope.from_dict(data),
            state=first.next_state,
            request=valid_request(
                topic_action="continue",
                turn_kind="substantial",
            ),
        )

        self.assertTrue(report.certifiable)
        self.assertTrue(
            report.next_state.topics["atlas"].has_committed_overview
        )

    def test_synthesis_reuse_is_rejected_in_focused_output(self) -> None:
        """Name: Synthesis reuse scope.

        Description: Marks a prior fact as synthesis inside ordinary focused prose.
        Assumptions: Synthesis is reserved for topic-wide Full orientation.
        Expectations: Focused reuse fails with the dedicated fact diagnostic.
        """
        first = validate_envelope(
            Envelope.from_dict(valid_focused_dict()),
            state=ConversationState.initial(),
            request=valid_request(turn_kind="simple_fact"),
        )
        data = valid_focused_dict()
        data["topic_action"] = "continue"
        data["state"] = {
            "turn_before": 1,
            "turn_after": 2,
            "branch_before": None,
            "branch_after": None,
            "prior_fact_count": 1,
            "next_fact_count": 1,
        }
        data["facts"][0]["reuse_reason"] = "synthesis"
        report = validate_envelope(
            Envelope.from_dict(data),
            state=first.next_state,
            request=valid_request(
                topic_action="continue",
                turn_kind="ordinary",
            ),
        )

        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-FACT-015",
            {item.code for item in report.diagnostics},
        )

    def test_exact_lexical_echo_between_views_fails(self) -> None:
        """Name: Exact cross-view lexical echo.

        Description: Repeats one complete normalized conclusion in two views.
        Assumptions: Exact sentence identity is mechanically decidable.
        Expectations: PC-M-DUPLICATE-001 rejects the response.
        """
        data = valid_full_dict()
        data["payload"]["sections"][1]["content"] = (
            data["payload"]["sections"][0]["content"]
        )
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-DUPLICATE-001", {item.code for item in report.diagnostics}
        )

    def test_short_anchor_may_recur_while_views_add_new_information(self) -> None:
        """Name: Permitted short cross-view anchor.

        Description: Reuses the Atlas identifier inside three otherwise distinct
        sentences that add ownership, timing, and evidence.
        Assumptions: An identifier is not itself a complete repeated proposition.
        Expectations: Exact duplicate checks pass and the response is certifiable.
        """
        data = valid_full_dict()
        data["payload"]["sections"][0]["content"] = (
            "Delay Atlas until approval."
        )
        data["payload"]["sections"][1]["content"] = (
            "For Atlas, Security owns approval and migration takes two weekends."
        )
        data["payload"]["sections"][2]["content"] = (
            "Atlas pilot evidence covers twelve million events."
        )

        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )

        self.assertTrue(report.certifiable)
        self.assertEqual(
            report.mechanical_checks["exact_lexical_duplicate_detection"],
            "PASS",
        )

    def test_exact_repeated_list_unit_between_views_fails(self) -> None:
        """Name: Exact repeated list-unit rejection.

        Description: Places one complete recovery instruction as a list item in
        both In context and At depth.
        Assumptions: Markdown list markers do not change normalized lexical units.
        Expectations: PC-M-DUPLICATE-001 rejects the repeated complete list item.
        """
        data = valid_full_dict()
        data["payload"]["sections"][1]["content"] = (
            "Security owns approval.\n- Freeze writes before cutover."
        )
        data["payload"]["sections"][2]["content"] = (
            "The pilot processed twelve million events.\n"
            "- Freeze writes before cutover."
        )

        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(),
        )

        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-DUPLICATE-001",
            {item.code for item in report.diagnostics},
        )

    def test_at_depth_concluding_recap_remains_advisory(self) -> None:
        """Name: At-depth concluding recap boundary.

        Description: Inspects the report contract for the semantic no-recap rule.
        Assumptions: Exact duplicate units are mechanical, but recognizing a
        paraphrased concluding recap requires an independent semantic oracle.
        Expectations: The dedicated advisory check remains explicitly UNVERIFIED.
        """
        report = validate_envelope(
            valid_full_envelope(),
            state=ConversationState.initial(),
            request=valid_request(),
        )

        self.assertEqual(
            report.advisory_checks["at_depth_concluding_recap"],
            "UNVERIFIED",
        )

    def test_correction_keeps_three_views_and_reuses_structured_facts(self) -> None:
        """Name: Structured correction exception.

        Description: Withdraws a committed fact, replaces it, changes action,
        and still renders three additive views.
        Assumptions: Correction prose says the earlier claim was wrong.
        Expectations: Exception-scoped reuse passes without changing branch.
        """
        state = _first_state()
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "views",
            "topic_id": "atlas",
            "topic_action": "continue",
            "state": {
                "turn_before": 1,
                "turn_after": 2,
                "branch_before": None,
                "branch_after": None,
                "prior_fact_count": 4,
                "next_fact_count": 7,
            },
            "facts": [
                {
                    "id": "ATLAS-F1",
                    "text": "Atlas should be adopted.",
                    "allocation": "at_a_glance",
                    "reuse_reason": "correction",
                },
                {
                    "id": "ATLAS-F5",
                    "text": "Atlas should not be adopted.",
                    "allocation": "at_a_glance",
                    "reuse_reason": "correction",
                },
                {
                    "id": "ATLAS-F6",
                    "text": "Pause procurement.",
                    "allocation": "in_context",
                    "reuse_reason": "correction",
                },
                {
                    "id": "ATLAS-F7",
                    "text": "The cost model omitted support charges.",
                    "allocation": "at_depth",
                    "reuse_reason": None,
                },
            ],
            "payload": {
                "correction": {
                    "content": (
                        "Earlier I said Atlas should be adopted. That was wrong "
                        "or incomplete. Atlas should not be adopted. This "
                        "changes the action: pause procurement."
                    ),
                    "withdrawn_fact_ids": ["ATLAS-F1"],
                    "replacement_fact_ids": ["ATLAS-F5"],
                    "changed_action_fact_ids": ["ATLAS-F6"],
                },
                "sections": [
                    {
                        "view": "at_a_glance",
                        "content": "Reject Atlas for now.",
                        "fact_ids": ["ATLAS-F5"],
                        "warning": None,
                    },
                    {
                        "view": "in_context",
                        "content": "Suspend the procurement workflow.",
                        "fact_ids": ["ATLAS-F6"],
                        "warning": None,
                    },
                    {
                        "view": "at_depth",
                        "content": "The cost model omitted support charges.",
                        "fact_ids": ["ATLAS-F7"],
                        "warning": None,
                    },
                ],
            },
        }
        envelope = Envelope.from_dict(data)
        report = validate_envelope(
            envelope,
            state=state,
            request=valid_request(
                topic_action="continue",
                turn_kind="material_correction",
            ),
        )
        self.assertTrue(report.mechanically_conformant)
        rendered = render_markdown(envelope)
        self.assertTrue(rendered.startswith("## At a glance"))
        self.assertEqual(rendered.count("## "), 3)

    def test_correction_cannot_withdraw_an_uncommitted_fact(self) -> None:
        """Name: Fabricated-withdrawal refusal.

        Description: Declares a new-topic correction whose withdrawn ID exists
        only in the candidate, not in committed conversation state.
        Assumptions: The trusted fact ledger is the mechanical record of claims
        emitted on the active topic.
        Expectations: PC-M-CORRECTION-007 rejects the invented retraction.
        """
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "views",
            "topic_id": "atlas",
            "topic_action": "start",
            "state": {
                "turn_before": 0,
                "turn_after": 1,
                "branch_before": None,
                "branch_after": None,
                "prior_fact_count": 0,
                "next_fact_count": 3,
            },
            "facts": [
                {
                    "id": "ATLAS-F1",
                    "text": "Atlas was approved.",
                    "allocation": "at_a_glance",
                    "reuse_reason": "correction",
                },
                {
                    "id": "ATLAS-F2",
                    "text": "Atlas is not approved.",
                    "allocation": "at_a_glance",
                    "reuse_reason": "correction",
                },
                {
                    "id": "ATLAS-F3",
                    "text": "Pause procurement.",
                    "allocation": "in_context",
                    "reuse_reason": "correction",
                },
            ],
            "payload": {
                "correction": {
                    "content": (
                        "Earlier I said Atlas was approved. That was wrong or "
                        "incomplete. Atlas is not approved. This changes the "
                        "action: pause procurement."
                    ),
                    "withdrawn_fact_ids": ["ATLAS-F1"],
                    "replacement_fact_ids": ["ATLAS-F2"],
                    "changed_action_fact_ids": ["ATLAS-F3"],
                },
                "sections": [
                    {
                        "view": "at_a_glance",
                        "content": "Reject Atlas.",
                        "fact_ids": ["ATLAS-F1", "ATLAS-F2"],
                        "warning": None,
                    },
                    {
                        "view": "in_context",
                        "content": "Suspend purchasing.",
                        "fact_ids": ["ATLAS-F3"],
                        "warning": None,
                    },
                    {
                        "view": "at_depth",
                        "content": "Approval records remain relevant.",
                        "fact_ids": [],
                        "warning": None,
                    },
                ],
            },
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=valid_request(turn_kind="material_correction"),
        )
        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-CORRECTION-007",
            {item.code for item in report.diagnostics},
        )

    def test_clarification_control_preserves_state(self) -> None:
        """Name: Material ambiguity clarification-only gate.

        Description: Emits one valid control question, then tries a recommendation
        before one question and a headed question without a fabricated view set.
        Assumptions: A material ambiguity prevents a safe substantive answer.
        Expectations: The single question preserves topic facts and branch while
        the turn advances; expanded controls fail the mechanical shape checks.
        """
        state = _first_state()
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "control",
            "topic_id": "atlas",
            "topic_action": "continue",
            "state": {
                "turn_before": 1,
                "turn_after": 2,
                "branch_before": None,
                "branch_after": None,
                "prior_fact_count": 4,
                "next_fact_count": 4,
            },
            "facts": [],
            "payload": {
                "control_kind": "clarification",
                "content": (
                    "Which environment is this, and have validation and rollback "
                    "readiness been confirmed?"
                ),
            },
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(
                prompt="Compare it to the baseline.",
                topic_action="continue",
                turn_kind="clarification",
            ),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(
            report.next_state.topics["atlas"].facts,
            state.topics["atlas"].facts,
        )
        invalid_controls = (
            (
                "Enable it in staging now. Which environment should I use?",
                "PC-M-CONTROL-001",
            ),
            (
                "Enable production now; which environment should I use?",
                "PC-M-CONTROL-001",
            ),
            (
                "Which environment should I use; enable production now?",
                "PC-M-CONTROL-001",
            ),
            (
                "Which environment should I use, and enable production now?",
                "PC-M-CONTROL-001",
            ),
            (
                "## Proposed plan\nIs rollback available?",
                "PC-M-CONTROL-002",
            ),
        )
        for content, expected_code in invalid_controls:
            with self.subTest(content=content):
                data["payload"]["content"] = content
                invalid = validate_envelope(
                    Envelope.from_dict(data),
                    state=state,
                    request=valid_request(
                        prompt="Compare it to the baseline.",
                        topic_action="continue",
                        turn_kind="clarification",
                    ),
                )
                self.assertFalse(invalid.mechanically_conformant)
                self.assertIn(
                    expected_code,
                    {item.code for item in invalid.diagnostics},
                )

    def test_quotation_requires_exact_source_and_hash(self) -> None:
        """Name: Exact controlling quotation and literal labels.

        Description: Checks trusted source bytes, SHA-256, exact summary-cap
        agreement, and the two required plain-text labels.
        Assumptions: Wrapper metadata carries the authoritative source.
        Expectations: Exact text and labels pass; invented caps and source
        mutations fail.
        """
        controlling = "Supplier shall retain Customer Data for thirty days."
        request = valid_request(
            prompt="Quote and summarize the clause.",
            topic_id="retention",
            turn_kind="quotation",
            controlling_text=controlling,
            summary_max_words=40,
        )
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "quotation",
            "topic_id": "retention",
            "topic_action": "start",
            "state": {
                "turn_before": 0,
                "turn_after": 1,
                "branch_before": None,
                "branch_after": None,
                "prior_fact_count": 0,
                "next_fact_count": 1,
            },
            "facts": [
                {
                    "id": "RETENTION-F1",
                    "text": "Customer Data is retained for thirty days.",
                    "allocation": "non_fit",
                    "reuse_reason": "quotation",
                }
            ],
            "payload": {
                "controlling_text": controlling,
                "source_sha256": hashlib.sha256(
                    controlling.encode("utf-8")
                ).hexdigest(),
                "quotation_fact_ids": ["RETENTION-F1"],
                "summary": "The default retention period is thirty days.",
                "summary_fact_ids": ["RETENTION-F1"],
                "summary_max_words": 40,
            },
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=request,
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(
            render_markdown(Envelope.from_dict(data)),
            (
                "Controlling text:\n"
                f"{controlling}\n\n"
                "Non-controlling plain-language summary:\n"
                "The default retention period is thirty days.\n"
            ),
        )
        invented_cap = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=replace(request, summary_max_words=None),
        )
        self.assertIn(
            "PC-M-QUOTE-003",
            {item.code for item in invented_cap.diagnostics},
        )
        data["payload"]["controlling_text"] += " "
        mutated = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=request,
        )
        self.assertFalse(mutated.mechanically_conformant)
        self.assertIn(
            "PC-M-QUOTE-002", {item.code for item in mutated.diagnostics}
        )

    def test_quotation_exempts_source_but_validates_separate_summary(self) -> None:
        """Name: Verbatim-source duplicate boundary.

        Description: Repeats one sentence inside trusted controlling text, then
        tests an exact source echo and a self-repeat in the separate summary.
        Assumptions: Required source bytes are exempt while non-controlling
        explanation remains subject to exact lexical duplicate checks.
        Expectations: Repeated source bytes pass; both summary variants produce
        PC-M-DUPLICATE-001.
        """
        controlling = "Supplier shall retain data. Supplier shall retain data."
        request = valid_request(
            prompt="Reproduce and summarize the clause.",
            topic_id="retention",
            turn_kind="quotation",
            controlling_text=controlling,
            summary_max_words=40,
        )
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "quotation",
            "topic_id": "retention",
            "topic_action": "start",
            "state": {
                "turn_before": 0,
                "turn_after": 1,
                "branch_before": None,
                "branch_after": None,
                "prior_fact_count": 0,
                "next_fact_count": 1,
            },
            "facts": [
                {
                    "id": "RETENTION-F1",
                    "text": "The clause repeats a retention instruction.",
                    "allocation": "non_fit",
                    "reuse_reason": "quotation",
                }
            ],
            "payload": {
                "controlling_text": controlling,
                "source_sha256": hashlib.sha256(
                    controlling.encode("utf-8")
                ).hexdigest(),
                "quotation_fact_ids": ["RETENTION-F1"],
                "summary": "The clause repeats a retention instruction.",
                "summary_fact_ids": ["RETENTION-F1"],
                "summary_max_words": 40,
            },
        }
        valid_report = validate_envelope(
            Envelope.from_dict(data),
            state=ConversationState.initial(),
            request=request,
        )
        self.assertTrue(valid_report.mechanically_conformant)
        self.assertEqual(
            valid_report.mechanical_checks[
                "exact_lexical_duplicate_detection"
            ],
            "PASS",
        )

        invalid_summaries = (
            "Supplier shall retain data.",
            "Plain explanation. Plain explanation.",
        )
        for summary in invalid_summaries:
            with self.subTest(summary=summary):
                data["payload"]["summary"] = summary
                report = validate_envelope(
                    Envelope.from_dict(data),
                    state=ConversationState.initial(),
                    request=request,
                )
                self.assertFalse(report.mechanically_conformant)
                self.assertIn(
                    "PC-M-DUPLICATE-001",
                    {item.code for item in report.diagnostics},
                )


if __name__ == "__main__":
    unittest.main()
