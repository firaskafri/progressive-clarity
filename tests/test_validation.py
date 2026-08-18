"""Name: Verbose-only structured envelope validation suite.

Description: Covers strict schemas, mandatory three-view order, per-response
budgets, warnings, state transitions, fact allocation/reuse, duplicates,
non-empty view prose, authoritative fact-catalog coverage, corrections,
quotations, clarifications, exact non-fit preservation, and canonical rendering.
Assumptions: Trusted requests and committed state are supplied separately from
model candidates; semantic truth is outside deterministic validation.
Expectations: Mechanically decidable violations fail closed, valid candidates
produce transactional state, and advisory claims remain UNVERIFIED.
"""

from __future__ import annotations

import hashlib
import unittest

from pc_core.model import (
    ENVELOPE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    ConversationState,
    Envelope,
    SchemaError,
    WrapperRequest,
)
from pc_core.render import render_markdown
from pc_core.validation import validate_envelope
from tests.helpers import (
    copied_verbose_dict,
    request_dict,
    valid_request,
    valid_verbose_envelope,
)


def _first_state() -> ConversationState:
    report = validate_envelope(
        valid_verbose_envelope(),
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
    exact non-fit bytes, safety-warning arithmetic, and 40/200 boundaries.
    Assumptions: The baseline fixture is a new ordinary in-scope response.
    Expectations: Structural or arithmetic drift prevents certification.
    """

    def test_valid_envelope_is_mechanically_certifiable(self) -> None:
        """Name: Valid v0.2 baseline.

        Description: Validates all three sections, facts, counts, and state.
        Assumptions: Request metadata identifies a new ordinary topic.
        Expectations: Mechanical checks pass and semantic checks stay
        UNVERIFIED.
        """
        report = validate_envelope(
            valid_verbose_envelope(),
            state=ConversationState.initial(),
            request=valid_request(),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertTrue(report.certifiable)
        self.assertEqual(report.next_state.turn, 1)
        self.assertEqual(len(report.next_state.facts), 4)
        self.assertTrue(
            all(value == "UNVERIFIED" for value in report.advisory_checks.values())
        )

    def test_removed_mode_field_is_rejected(self) -> None:
        """Name: Removed dual-mode field.

        Description: Adds the former top-level mode field to a v0.2 envelope.
        Assumptions: Mode selection no longer exists in the closed schema.
        Expectations: Strict parsing raises SchemaError.
        """
        data = copied_verbose_dict()
        data["mode"] = "progressive"
        with self.assertRaises(SchemaError):
            Envelope.from_dict(data)

    def test_removed_view_override_is_rejected(self) -> None:
        """Name: Removed one-view request field.

        Description: Adds the former view_override field to a v0.2 request.
        Assumptions: Every ordinary in-scope response now uses all three views.
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
                data = copied_verbose_dict()
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
                data = copied_verbose_dict()
                data["payload"]["sections"][section_index]["content"] = content
                with self.assertRaises(SchemaError):
                    Envelope.from_dict(data)
        punctuation_only = copied_verbose_dict()
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
                data = copied_verbose_dict()
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
        data = copied_verbose_dict()
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
        """Name: Indispensable-warning exception.

        Description: Places a 45-word warning before non-empty normal glance
        prose.
        Assumptions: pc-core can verify placement but not indispensability.
        Expectations: Mechanics pass while warning indispensability is
        UNVERIFIED.
        """
        data = copied_verbose_dict()
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
                    valid_verbose_envelope(),
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

    def test_renderer_emits_exact_headings_once(self) -> None:
        """Name: Canonical heading renderer.

        Description: Renders a validated envelope and extracts protocol headings.
        Assumptions: Candidate content cannot inject protocol headings.
        Expectations: Exactly three level-two headings appear in required order.
        """
        headings = [
            line
            for line in render_markdown(valid_verbose_envelope()).splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(
            headings,
            ["## At a glance", "## In context", "## At depth"],
        )

    def test_exact_non_fit_preserves_bytes_and_skips_view_only_checks(self) -> None:
        """Name: Exact-output non-fit preservation.

        Description: Validates a requested artifact containing a protocol-like
        heading, a repeated lexical unit, and no terminal newline.
        Assumptions: Exact output outranks view presentation and additivity
        checks and therefore receives no canonical newline.
        Expectations: Validation passes, view-only checks are not applicable,
        and rendering returns byte-for-byte content.
        """
        content = "## At a glance\nrepeat exactly.\nrepeat exactly."
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "non_fit",
            "topic_id": "atlas",
            "new_topic": True,
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
            request=valid_request(intent="non_fit"),
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
        self.assertEqual(render_markdown(envelope), content)


class StateFactAndExceptionTests(unittest.TestCase):
    """Name: State, facts, lexical checks, and exception handling.

    Description: Exercises cross-turn reuse, branches, exact lexical echoes,
    correction repair and false-withdrawal refusal, clarification control, and
    exact controlling text with separately validated summary prose.
    Assumptions: The baseline response supplies trusted committed prior state.
    Expectations: Only explicit, immutable, exception-scoped transitions pass.
    """

    def test_prior_context_reuse_preserves_fact_identity(self) -> None:
        """Name: Necessary cross-turn fact reuse.

        Description: Reuses one committed fact once and adds two new facts.
        Assumptions: Cross-turn context may be necessary but cross-view recap is
        still prohibited.
        Expectations: Matching ID, text, allocation, and prior_context pass.
        """
        state = _first_state()
        data = copied_verbose_dict()
        data["new_topic"] = False
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
            request=valid_request(new_topic=False),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(len(report.next_state.facts), 6)

    def test_targeted_followup_still_requires_all_views(self) -> None:
        """Name: Targeted full-view response.

        Description: Selects a branch while retaining the mandatory view set.
        Assumptions: Targeting changes subject focus, not presentation shape.
        Expectations: Three views pass and the branch commits transactionally.
        """
        state = _first_state()
        data = copied_verbose_dict()
        data["new_topic"] = False
        data["state"] = {
            "turn_before": 1,
            "turn_after": 2,
            "branch_before": None,
            "branch_after": "security",
            "prior_fact_count": 4,
            "next_fact_count": 8,
        }
        texts = (
            "Security review is the selected branch.",
            "Threat modeling starts Monday.",
            "Identity signs the exception.",
            "The review covers tenant isolation.",
        )
        for index, fact in enumerate(data["facts"], start=5):
            fact["id"] = f"ATLAS-F{index}"
            fact["text"] = texts[index - 5]
        for section in data["payload"]["sections"]:
            section["fact_ids"] = [
                f"ATLAS-F{5 + int(fact_id[-1]) - 1}"
                for fact_id in section["fact_ids"]
            ]
        data["payload"]["sections"][0]["content"] = texts[0]
        data["payload"]["sections"][1]["content"] = " ".join(texts[1:3])
        data["payload"]["sections"][2]["content"] = texts[3]
        report = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(new_topic=False, intent="targeted"),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(report.next_state.branch, "security")

    def test_exact_lexical_echo_between_views_fails(self) -> None:
        """Name: Exact cross-view lexical echo.

        Description: Repeats one normalized sentence in two different views.
        Assumptions: Exact sentence identity is mechanically decidable.
        Expectations: PC-M-DUPLICATE-001 rejects the response.
        """
        data = copied_verbose_dict()
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
            "new_topic": False,
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
                        "My adoption recommendation was wrong. Do not adopt "
                        "Atlas; pause procurement."
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
            request=valid_request(new_topic=False, intent="correction"),
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
            "new_topic": True,
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
                        "My earlier approval claim was wrong. Atlas is not "
                        "approved. Pause procurement."
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
            request=valid_request(intent="correction"),
        )
        self.assertFalse(report.mechanically_conformant)
        self.assertIn(
            "PC-M-CORRECTION-007",
            {item.code for item in report.diagnostics},
        )

    def test_clarification_control_preserves_state(self) -> None:
        """Name: Material ambiguity clarification.

        Description: Emits a control question without a fabricated view set.
        Assumptions: A material ambiguity prevents a safe substantive answer.
        Expectations: Topic ledger and branch remain while turn increments.
        """
        state = _first_state()
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "control",
            "topic_id": "atlas",
            "new_topic": False,
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
                "content": "Which cost baseline should I use?",
            },
        }
        report = validate_envelope(
            Envelope.from_dict(data),
            state=state,
            request=valid_request(
                prompt="Compare it to the baseline.",
                new_topic=False,
                intent="clarification",
            ),
        )
        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(report.next_state.facts, state.facts)

    def test_quotation_requires_exact_source_and_hash(self) -> None:
        """Name: Exact controlling quotation.

        Description: Checks trusted source bytes, SHA-256, and summary cap.
        Assumptions: Wrapper metadata carries the authoritative source.
        Expectations: Exact text passes; a one-character mutation fails.
        """
        controlling = "Supplier shall retain Customer Data for thirty days."
        request = valid_request(
            prompt="Quote and summarize the clause.",
            topic_id="retention",
            intent="quotation",
            controlling_text=controlling,
            summary_max_words=40,
        )
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "quotation",
            "topic_id": "retention",
            "new_topic": True,
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
            intent="quotation",
            controlling_text=controlling,
            summary_max_words=40,
        )
        data = {
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "response_kind": "quotation",
            "topic_id": "retention",
            "new_topic": True,
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
