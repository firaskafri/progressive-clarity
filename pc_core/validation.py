"""Deterministic topic-oriented validation with explicit semantic boundaries."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from pc_core.model import (
    AT_A_GLANCE_MAX_NON_WARNING_WORDS,
    CORRECTION_FACT_FIELDS,
    CORRECTION_TURN_KINDS,
    ENVELOPE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    STATE_SCHEMA_VERSION,
    THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS,
    VIEW_HEADINGS,
    VIEWS,
    WRAPPER_REQUEST_SCHEMA_VERSION,
    ConversationState,
    Envelope,
    SchemaError,
    StoredFact,
    TopicState,
    WrapperRequest,
)
from pc_core.policy import ResolvedTurn, resolve_turn
from pc_core.word_count import (
    count_english_words,
    lexical_similarity,
    lexical_units,
    normalize_lexical_text,
    without_fenced_lines,
)


_FACT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$")
_PROTOCOL_HEADING = re.compile(
    r"(?im)^ {0,3}#{1,6}[ \t]+("
    + "|".join(re.escape(heading) for heading in VIEW_HEADINGS)
    + r")[ \t]*#*[ \t]*$"
)
_ATX_HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+\S")
_SETEXT_UNDERLINE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
_PROTOCOL_HEADING_NAMES = frozenset(
    heading.casefold() for heading in VIEW_HEADINGS
)
_CORRECTION_OPENING = re.compile(
    r"\AEarlier I said (?=\S).+?\. That was wrong or incomplete\.\s+"
    r"(?=\S).+?\. This changes (?=\S).+?(?:\.|\Z)",
    re.DOTALL,
)
_QUESTION_OPENING = re.compile(
    r"^(?:who|whom|whose|what|when|where|why|how|which|"
    r"is|are|am|was|were|do|does|did|can|could|will|would|"
    r"should|has|have|had|may|might|must)\b",
    re.IGNORECASE,
)
_CONTROL_CLAUSE_SEPARATOR = re.compile(r"[;:!]|--|[–—]")
_CONTROL_COORDINATED_CLAUSE = re.compile(
    r",\s+(?:and|or)\s+",
    re.IGNORECASE,
)
_COMPOUND_FACT_HINT = re.compile(r"(?:[.;]\s+|\b(?:and|but|while|whereas)\b)")
_MAX_NEAR_DUPLICATE_UNITS = 250
_NEAR_DUPLICATE_THRESHOLD = 0.86
_NEAR_DUPLICATE_MIN_TOKENS = 6

_ADVISORY_CHECKS = {
    "semantic_accuracy": "UNVERIFIED",
    "semantic_completeness": "UNVERIFIED",
    "safe_stopping_outcome": "UNVERIFIED",
    "hidden_reversal": "UNVERIFIED",
    "deeper_view_new_information_dominance": "UNVERIFIED",
    "complete_proposition_restatement": "UNVERIFIED",
    "short_anchor_necessity": "UNVERIFIED",
    "at_depth_concluding_recap": "UNVERIFIED",
    "fact_atomicity_and_allocation": "UNVERIFIED",
    "simple_fact_brevity": "UNVERIFIED",
    "numeric_assumption_labeling": "UNVERIFIED",
    "clarification_gate_semantics": "UNVERIFIED",
    "non_fit_intended_artifact_equality": "UNVERIFIED",
    "warning_indispensability": "UNVERIFIED",
    "correction_exception_scope": "UNVERIFIED",
    "topic_and_branch_intent": "UNVERIFIED",
    "presentation_policy_classification": "UNVERIFIED",
    "at_depth_relevance_and_purpose": "UNVERIFIED",
}
_CORRECTION_FIELD_SPECS = (
    ("withdrawn_fact_ids", "PC-M-CORRECTION-003", "withdrawn fact"),
    ("replacement_fact_ids", "PC-M-CORRECTION-004", "replacement fact"),
    ("changed_action_fact_ids", "PC-M-CORRECTION-005", "changed action"),
)


def _contains_protocol_heading(content: str) -> bool:
    """Detect reserved Markdown headings while ignoring fenced code."""
    lines = without_fenced_lines(content.splitlines())
    for index, line in enumerate(lines):
        if line is None:
            continue
        if _PROTOCOL_HEADING.fullmatch(line):
            return True
        if (
            line.strip().casefold() in _PROTOCOL_HEADING_NAMES
            and index + 1 < len(lines)
            and lines[index + 1] is not None
            and _SETEXT_UNDERLINE.fullmatch(lines[index + 1])
        ):
            return True
    return False


def _contains_markdown_heading(content: str) -> bool:
    """Detect any ATX or Setext heading while ignoring fenced code."""
    lines = without_fenced_lines(content.splitlines())
    for index, line in enumerate(lines):
        if line is None:
            continue
        if _ATX_HEADING.match(line):
            return True
        if (
            line.strip()
            and index + 1 < len(lines)
            and lines[index + 1] is not None
            and _SETEXT_UNDERLINE.fullmatch(lines[index + 1])
        ):
            return True
    return False


def _mask_fenced_markdown(markdown: str) -> str:
    """Replace fenced lines with spaces while preserving source offsets."""
    raw_lines = markdown.splitlines(keepends=True)
    visible_lines = without_fenced_lines(
        [line.rstrip("\r\n") for line in raw_lines]
    )
    return "".join(
        raw_line
        if visible_line is not None
        else "".join(
            character if character in "\r\n" else " "
            for character in raw_line
        )
        for raw_line, visible_line in zip(
            raw_lines,
            visible_lines,
            strict=True,
        )
    )


def _is_single_clarification_question(content: str) -> bool:
    """Check the conservative mechanical subset of one clarification question."""
    question_units = lexical_units(" ".join(content.split()))
    coordinated_clauses = tuple(
        content[match.end() :]
        for match in _CONTROL_COORDINATED_CLAUSE.finditer(content)
    )
    return (
        content.count("?") == 1
        and content.endswith("?")
        and len(question_units) == 1
        and _QUESTION_OPENING.match(content) is not None
        and _CONTROL_CLAUSE_SEPARATOR.search(content) is None
        and all(
            _QUESTION_OPENING.match(clause) is not None
            for clause in coordinated_clauses
        )
    )


@dataclass(frozen=True)
class Diagnostic:
    """One stable mechanical error or advisory warning."""

    code: str
    domain: str
    severity: str
    location: str
    message: str

    def to_dict(self) -> dict[str, str]:
        """Serialize the diagnostic."""
        return {
            "code": self.code,
            "domain": self.domain,
            "severity": self.severity,
            "location": self.location,
            "message": self.message,
        }


@dataclass(frozen=True)
class ValidationReport:
    """Mechanical result, semantic boundary, counts, and transactional state."""

    mechanically_conformant: bool
    certifiable: bool
    diagnostics: tuple[Diagnostic, ...]
    counts: Mapping[str, int]
    mechanical_checks: Mapping[str, str]
    advisory_checks: Mapping[str, str]
    next_state: ConversationState | None

    def __post_init__(self) -> None:
        """Snapshot result mappings so audit data cannot change after validation."""
        object.__setattr__(self, "counts", MappingProxyType(dict(self.counts)))
        object.__setattr__(
            self,
            "mechanical_checks",
            MappingProxyType(dict(self.mechanical_checks)),
        )
        object.__setattr__(
            self,
            "advisory_checks",
            MappingProxyType(dict(self.advisory_checks)),
        )

    def to_dict(self, *, include_next_state: bool = True) -> dict[str, object]:
        """Serialize a report without implying semantic conformance."""
        result: dict[str, object] = {
            "mechanically_conformant": self.mechanically_conformant,
            "certifiable": self.certifiable,
            "semantic_conformance": "UNVERIFIED",
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "counts": dict(self.counts),
            "mechanical_checks": dict(self.mechanical_checks),
            "advisory_checks": dict(self.advisory_checks),
        }
        if include_next_state:
            result["next_state"] = (
                None if self.next_state is None else self.next_state.to_dict()
            )
        return result


class _Collector:
    def __init__(self) -> None:
        self.items: list[Diagnostic] = []

    def mechanical(self, code: str, location: str, message: str) -> None:
        self.items.append(
            Diagnostic(code, "mechanical", "error", location, message)
        )

    def advisory(self, code: str, location: str, message: str) -> None:
        self.items.append(
            Diagnostic(code, "advisory", "warning", location, message)
        )

    @property
    def mechanically_conformant(self) -> bool:
        return not any(item.domain == "mechanical" for item in self.items)


def _content_records(
    envelope: Envelope,
) -> list[tuple[str, str, str | None]]:
    records: list[tuple[str, str, str | None]] = []
    if envelope.response_kind == "views":
        correction = envelope.payload["correction"]
        if correction is not None:
            records.append(
                ("payload.correction.content", correction["content"], "correction")
            )
        for index, section in enumerate(envelope.payload["sections"]):
            warning = section["warning"]
            if warning is not None:
                records.append(
                    (
                        f"payload.sections[{index}].warning.content",
                        warning["content"],
                        None,
                    )
                )
            records.append(
                (
                    f"payload.sections[{index}].content",
                    section["content"],
                    None,
                )
            )
    elif envelope.response_kind == "focused":
        warning = envelope.payload["warning"]
        if warning is not None:
            records.append(("payload.warning.content", warning["content"], None))
        correction = envelope.payload["correction"]
        if correction is not None:
            records.append(
                ("payload.correction.content", correction["content"], "correction")
            )
        records.append(("payload.content", envelope.payload["content"], None))
    elif envelope.response_kind == "quotation":
        records.extend(
            [
                (
                    "payload.controlling_text",
                    envelope.payload["controlling_text"],
                    "quotation",
                ),
                ("payload.summary", envelope.payload["summary"], None),
            ]
        )
    elif envelope.response_kind == "non_fit":
        records.append(("payload.content", envelope.payload["content"], None))
    return records


def _fact_references(envelope: Envelope) -> list[tuple[str, str, str | None, str]]:
    references: list[tuple[str, str, str | None, str]] = []
    if envelope.response_kind == "views":
        correction = envelope.payload["correction"]
        if correction is not None:
            for field in CORRECTION_FACT_FIELDS:
                references.extend(
                    (
                        fact_id,
                        f"payload.correction.{field}[{index}]",
                        "correction",
                        "correction",
                    )
                    for index, fact_id in enumerate(correction[field])
                )
        for section_index, section in enumerate(envelope.payload["sections"]):
            references.extend(
                (
                    fact_id,
                    f"payload.sections[{section_index}].fact_ids[{index}]",
                    None,
                    section["view"],
                )
                for index, fact_id in enumerate(section["fact_ids"])
            )
            warning = section["warning"]
            if warning is not None:
                references.extend(
                    (
                        fact_id,
                        (
                            f"payload.sections[{section_index}]."
                            f"warning.fact_ids[{index}]"
                        ),
                        None,
                        section["view"],
                    )
                    for index, fact_id in enumerate(warning["fact_ids"])
                )
    elif envelope.response_kind == "focused":
        references.extend(
            (
                fact_id,
                f"payload.fact_ids[{index}]",
                None,
                "focused",
            )
            for index, fact_id in enumerate(envelope.payload["fact_ids"])
        )
        warning = envelope.payload["warning"]
        if warning is not None:
            references.extend(
                (
                    fact_id,
                    f"payload.warning.fact_ids[{index}]",
                    None,
                    "focused",
                )
                for index, fact_id in enumerate(warning["fact_ids"])
            )
        correction = envelope.payload["correction"]
        if correction is not None:
            for field in CORRECTION_FACT_FIELDS:
                references.extend(
                    (
                        fact_id,
                        f"payload.correction.{field}[{index}]",
                        "correction",
                        "correction",
                    )
                    for index, fact_id in enumerate(correction[field])
                )
    elif envelope.response_kind == "quotation":
        for field in ("quotation_fact_ids", "summary_fact_ids"):
            references.extend(
                (
                    fact_id,
                    f"payload.{field}[{index}]",
                    "quotation",
                    "non_fit",
                )
                for index, fact_id in enumerate(envelope.payload[field])
            )
    elif envelope.response_kind == "non_fit":
        references.extend(
            (
                fact_id,
                f"payload.fact_ids[{index}]",
                None,
                "non_fit",
            )
            for index, fact_id in enumerate(envelope.payload["fact_ids"])
        )
    return references


def _fact_content_bindings(envelope: Envelope) -> dict[str, list[str]]:
    """Map declared fact references to the exact visible content they cover."""
    bindings: dict[str, list[str]] = {}

    def bind(fact_ids: tuple[str, ...], content: str) -> None:
        for fact_id in fact_ids:
            bindings.setdefault(fact_id, []).append(content)

    if envelope.response_kind == "views":
        correction = envelope.payload["correction"]
        if correction is not None:
            for field in CORRECTION_FACT_FIELDS:
                bind(correction[field], correction["content"])
        for section in envelope.payload["sections"]:
            bind(section["fact_ids"], section["content"])
            warning = section["warning"]
            if warning is not None:
                bind(warning["fact_ids"], warning["content"])
    elif envelope.response_kind == "focused":
        bind(envelope.payload["fact_ids"], envelope.payload["content"])
        warning = envelope.payload["warning"]
        if warning is not None:
            bind(warning["fact_ids"], warning["content"])
        correction = envelope.payload["correction"]
        if correction is not None:
            for field in CORRECTION_FACT_FIELDS:
                bind(correction[field], correction["content"])
    elif envelope.response_kind == "quotation":
        bind(
            envelope.payload["quotation_fact_ids"],
            envelope.payload["controlling_text"],
        )
        bind(envelope.payload["summary_fact_ids"], envelope.payload["summary"])
    elif envelope.response_kind == "non_fit":
        bind(envelope.payload["fact_ids"], envelope.payload["content"])
    return bindings


def _validate_versions(
    envelope: Envelope,
    state: ConversationState,
    request: WrapperRequest | None,
    collector: _Collector,
) -> None:
    if envelope.schema_version != ENVELOPE_SCHEMA_VERSION:
        collector.mechanical(
            "PC-M-SCHEMA-001",
            "schema_version",
            f"expected envelope schema {ENVELOPE_SCHEMA_VERSION}",
        )
    if envelope.protocol_version != PROTOCOL_VERSION:
        collector.mechanical(
            "PC-M-SCHEMA-002",
            "protocol_version",
            f"expected protocol {PROTOCOL_VERSION}",
        )
    if (
        state.schema_version != STATE_SCHEMA_VERSION
        or state.protocol_version != PROTOCOL_VERSION
    ):
        collector.mechanical(
            "PC-M-STATE-001",
            "conversation_state",
            "conversation state version does not match pc-core",
        )
    if (
        request is not None
        and request.schema_version != WRAPPER_REQUEST_SCHEMA_VERSION
    ):
        collector.mechanical(
            "PC-M-REQUEST-001",
            "wrapper_request.schema_version",
            f"expected request schema {WRAPPER_REQUEST_SCHEMA_VERSION}",
        )


def _validate_request_and_state(
    envelope: Envelope,
    state: ConversationState,
    request: WrapperRequest | None,
    resolved: ResolvedTurn | None,
    collector: _Collector,
) -> tuple[TopicState, dict[str, StoredFact]]:
    known = envelope.topic_id in state.topics
    if envelope.topic_action == "start":
        topic = TopicState()
        if known:
            collector.mechanical(
                "PC-M-TOPIC-001",
                "topic_action",
                "start requires an unknown topic_id",
            )
    elif envelope.topic_action == "continue":
        topic = state.topics[envelope.topic_id] if known else TopicState()
        if not known or state.active_topic_id != envelope.topic_id:
            collector.mechanical(
                "PC-M-TOPIC-002",
                "topic_action",
                "continue requires the active topic_id",
            )
    else:
        topic = state.topics[envelope.topic_id] if known else TopicState()
        if not known or state.active_topic_id == envelope.topic_id:
            collector.mechanical(
                "PC-M-TOPIC-003",
                "topic_action",
                "resume requires a known inactive topic_id",
            )

    if request is not None:
        if envelope.topic_action != request.topic_action:
            collector.mechanical(
                "PC-M-TOPIC-004",
                "topic_action",
                "envelope topic_action does not match wrapper request",
            )
        if envelope.topic_id != request.topic_id:
            collector.mechanical(
                "PC-M-TOPIC-005",
                "topic_id",
                "envelope topic_id does not match wrapper request",
            )
        if resolved is None:
            collector.mechanical(
                "PC-M-KIND-001",
                "response_kind",
                "trusted request requires a resolved presentation policy",
            )
        elif envelope.response_kind != resolved.expected_response_kind:
            collector.mechanical(
                "PC-M-KIND-002",
                "response_kind",
                (
                    f"resolved turn requires {resolved.expected_response_kind}; "
                    f"candidate declared {envelope.response_kind}"
                ),
            )
        if (
            request.turn_kind == "non_fit"
            and envelope.response_kind == "non_fit"
            and envelope.payload["non_fit_kind"] != request.non_fit_kind
        ):
            collector.mechanical(
                "PC-M-KIND-004",
                "payload.non_fit_kind",
                "candidate non_fit_kind does not match the trusted request",
            )
        if (
            envelope.response_kind == "control"
            and envelope.payload["control_kind"] != "clarification"
        ):
            collector.mechanical(
                "PC-M-KIND-003",
                "payload.control_kind",
                "the only control response is clarification",
            )
    if envelope.state.turn_before != state.turn:
        collector.mechanical(
            "PC-M-STATE-002",
            "state.turn_before",
            f"declared {envelope.state.turn_before}; computed {state.turn}",
        )
    if envelope.state.turn_after != state.turn + 1:
        collector.mechanical(
            "PC-M-STATE-003",
            "state.turn_after",
            f"declared {envelope.state.turn_after}; computed {state.turn + 1}",
        )
    if envelope.state.branch_before != topic.branch:
        collector.mechanical(
            "PC-M-STATE-004",
            "state.branch_before",
            "declared branch does not match committed branch state",
        )
    if envelope.state.prior_fact_count != len(topic.facts):
        collector.mechanical(
            "PC-M-STATE-005",
            "state.prior_fact_count",
            (
                f"declared {envelope.state.prior_fact_count}; "
                f"computed {len(topic.facts)}"
            ),
        )
    return topic, dict(topic.facts)


def _validate_presentation(envelope: Envelope, collector: _Collector) -> None:
    if envelope.response_kind == "control":
        content = envelope.payload["content"].strip()
        if not _is_single_clarification_question(content):
            collector.mechanical(
                "PC-M-CONTROL-001",
                "payload.content",
                "clarification control must contain exactly one question sentence",
            )
        if _contains_markdown_heading(content):
            collector.mechanical(
                "PC-M-CONTROL-002",
                "payload.content",
                "clarification control must not contain a heading",
            )
        return
    if envelope.response_kind == "focused":
        for location, content, _exception in _content_records(envelope):
            if _contains_protocol_heading(content):
                collector.mechanical(
                    "PC-M-HEADING-002",
                    location,
                    "focused content must not embed a reserved protocol heading",
                )
        return
    if envelope.response_kind != "views":
        return
    sequence = tuple(section["view"] for section in envelope.payload["sections"])
    if sequence != VIEWS:
        collector.mechanical(
            "PC-M-HEADING-001",
            "payload.sections",
            f"section sequence {list(sequence)} must be {list(VIEWS)}",
        )
    for index, section in enumerate(envelope.payload["sections"]):
        if count_english_words(section["content"]) == 0:
            collector.mechanical(
                "PC-M-CONTENT-001",
                f"payload.sections[{index}].content",
                "each required view must contain counted English prose",
            )
        if section["view"] != "at_a_glance" and section["warning"] is not None:
            collector.mechanical(
                "PC-M-WARNING-001",
                f"payload.sections[{index}].warning",
                "a structured Full warning must appear only in At a glance",
            )
    for location, content, _exception in _content_records(envelope):
        if _contains_protocol_heading(content):
            collector.mechanical(
                "PC-M-HEADING-002",
                location,
                "content must not embed a protocol heading; the renderer owns headings",
            )


def _validate_correction(
    envelope: Envelope,
    request: WrapperRequest | None,
    prior_facts: Mapping[str, StoredFact],
    collector: _Collector,
) -> None:
    if envelope.response_kind not in {"views", "focused"}:
        return
    correction = envelope.payload["correction"]
    expects = request is not None and request.turn_kind in CORRECTION_TURN_KINDS
    if expects and correction is None:
        collector.mechanical(
            "PC-M-CORRECTION-001",
            "payload.correction",
            "correction intent requires structured repair metadata",
        )
        return
    if correction is None:
        return
    if request is not None and request.turn_kind not in CORRECTION_TURN_KINDS:
        collector.mechanical(
            "PC-M-CORRECTION-002",
            "payload.correction",
            "structured correction is only valid for correction intent",
        )
    for field, code, label in _CORRECTION_FIELD_SPECS:
        if not correction[field]:
            collector.mechanical(
                code,
                f"payload.correction.{field}",
                (
                    "a correction requires at least one "
                    f"{label}"
                ),
            )
    for index, fact_id in enumerate(correction["withdrawn_fact_ids"]):
        if fact_id not in prior_facts:
            collector.mechanical(
                "PC-M-CORRECTION-007",
                f"payload.correction.withdrawn_fact_ids[{index}]",
                "a withdrawn fact must exist in the committed topic ledger",
            )
    correction_content = correction["content"]
    if _CORRECTION_OPENING.match(correction_content) is None:
        collector.mechanical(
            "PC-M-CORRECTION-006",
            "payload.correction.content",
            (
                "repair text must open exactly with withdrawal, the literal "
                "'That was wrong or incomplete.', replacement, and a literal "
                "'This changes' consequence or action"
            ),
        )


def _validate_quotation(
    envelope: Envelope,
    request: WrapperRequest | None,
    collector: _Collector,
) -> None:
    if envelope.response_kind != "quotation":
        return
    text = envelope.payload["controlling_text"]
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if envelope.payload["source_sha256"] != digest:
        collector.mechanical(
            "PC-M-QUOTE-001",
            "payload.source_sha256",
            "source_sha256 does not match controlling_text bytes",
        )
    if request is None or request.controlling_text is None:
        collector.advisory(
            "PC-A-QUOTE-001",
            "payload.controlling_text",
            "exactness against the user's source is unverified without trusted text",
        )
    elif text != request.controlling_text:
        collector.mechanical(
            "PC-M-QUOTE-002",
            "payload.controlling_text",
            "controlling text differs from the wrapper request",
        )
    expected_cap = None if request is None else request.summary_max_words
    declared_cap = envelope.payload["summary_max_words"]
    if request is not None and declared_cap != expected_cap:
        collector.mechanical(
            "PC-M-QUOTE-003",
            "payload.summary_max_words",
            f"declared summary cap {declared_cap}; expected {expected_cap}",
        )
    summary_words = count_english_words(envelope.payload["summary"])
    if declared_cap is not None and summary_words > declared_cap:
        collector.mechanical(
            "PC-M-BUDGET-004",
            "payload.summary",
            f"summary has {summary_words} counted words; cap is {declared_cap}",
        )


def _validate_facts(
    envelope: Envelope,
    prior_facts: dict[str, StoredFact],
    next_turn: int,
    resolved: ResolvedTurn | None,
    collector: _Collector,
) -> dict[str, StoredFact]:
    ids = [fact.id for fact in envelope.facts]
    if any(count > 1 for count in Counter(ids).values()):
        collector.mechanical(
            "PC-M-FACT-001",
            "facts",
            "fact IDs must be unique within the candidate",
        )
    declared = {fact.id: fact for fact in envelope.facts}
    for index, fact in enumerate(envelope.facts):
        location = f"facts[{index}]"
        if _FACT_ID.fullmatch(fact.id) is None:
            collector.mechanical(
                "PC-M-FACT-002",
                f"{location}.id",
                "fact id must contain 1-64 safe identifier characters",
            )
        if "\n" in fact.text or "\r" in fact.text:
            collector.mechanical(
                "PC-M-FACT-003",
                f"{location}.text",
                "atomic fact text must be one physical line",
            )
        if _COMPOUND_FACT_HINT.search(fact.text):
            collector.advisory(
                "PC-A-FACT-001",
                f"{location}.text",
                "fact text may contain more than one semantic proposition",
            )

    references = _fact_references(envelope)
    reference_counts = Counter(item[0] for item in references)
    contexts: dict[str, set[str | None]] = {}
    for fact_id, location, exception, placement in references:
        contexts.setdefault(fact_id, set()).add(exception)
        fact = declared.get(fact_id)
        if fact is None:
            collector.mechanical(
                "PC-M-FACT-004",
                location,
                "fact reference does not identify a declared fact",
            )
            continue
        if placement == "non_fit":
            if fact.allocation != "non_fit":
                collector.mechanical(
                    "PC-M-FACT-005",
                    location,
                    "referenced fact must use non_fit allocation here",
                )
        elif exception != "correction" and fact.allocation != placement:
            collector.mechanical(
                "PC-M-FACT-006",
                location,
                "referenced fact allocation does not match its placement",
            )

    normalized_owner: dict[str, str] = {}
    for fact_id, stored in prior_facts.items():
        normalized = normalize_lexical_text(stored.text)
        if normalized:
            normalized_owner[normalized] = fact_id
    for index, fact in enumerate(envelope.facts):
        location = f"facts[{index}]"
        count = reference_counts[fact.id]
        prior = prior_facts.get(fact.id)
        if count == 0:
            collector.mechanical(
                "PC-M-FACT-007",
                location,
                "declared fact is not referenced by rendered content",
            )
        if prior is not None:
            if fact.text != prior.text:
                collector.mechanical(
                    "PC-M-FACT-008",
                    location,
                    "a reused id must preserve committed text",
                )
            if fact.reuse_reason is None:
                collector.mechanical(
                    "PC-M-FACT-009",
                    f"{location}.reuse_reason",
                    "a prior fact requires an explicit reuse reason",
                )
        elif fact.reuse_reason in {"prior_context", "synthesis"}:
            collector.mechanical(
                "PC-M-FACT-010",
                f"{location}.reuse_reason",
                "cross-turn reuse reasons are valid only for a committed fact",
            )
        elif fact.reuse_reason in {"correction", "quotation"} and count < 2:
            collector.mechanical(
                "PC-M-FACT-011",
                f"{location}.reuse_reason",
                "a new exception fact must be referenced in both exception contexts",
            )
        if count > 1 and fact.reuse_reason not in {"correction", "quotation"}:
            collector.mechanical(
                "PC-M-FACT-012",
                location,
                f"fact is referenced {count} times without an allowed exception",
            )
        if fact.reuse_reason in {"correction", "quotation"}:
            if fact.reuse_reason not in contexts.get(fact.id, set()):
                collector.mechanical(
                    "PC-M-FACT-013",
                    f"{location}.reuse_reason",
                    "reuse reason lacks matching structured exception content",
                )
        if fact.reuse_reason == "synthesis" and (
            envelope.response_kind != "views"
            or resolved is None
            or not resolved.marks_overview
        ):
            collector.mechanical(
                "PC-M-FACT-015",
                f"{location}.reuse_reason",
                "synthesis reuse is valid only in a topic-wide Full overview",
            )
        normalized = normalize_lexical_text(fact.text)
        owner = normalized_owner.get(normalized)
        if owner is not None and owner != fact.id:
            collector.mechanical(
                "PC-M-FACT-014",
                f"{location}.text",
                "lexically identical text is already owned by another fact ID",
            )
        elif normalized:
            normalized_owner[normalized] = fact.id

    next_facts = dict(prior_facts)
    for fact in envelope.facts:
        if fact.id not in next_facts:
            next_facts[fact.id] = StoredFact(
                text=fact.text,
                first_turn=next_turn,
            )
    return next_facts


def _validate_required_facts(
    envelope: Envelope,
    request: WrapperRequest | None,
    collector: _Collector,
) -> None:
    """Require exact normalized coverage for a caller-authoritative catalog."""
    if request is None or request.required_facts is None:
        return
    declared = {fact.id: fact for fact in envelope.facts}
    bindings = _fact_content_bindings(envelope)
    normalized_bindings = {
        fact_id: tuple(
            f" {normalize_lexical_text(content)} "
            for content in contents
        )
        for fact_id, contents in bindings.items()
    }
    for index, required in enumerate(request.required_facts):
        location = f"wrapper_request.required_facts[{index}]"
        fact = declared.get(required.id)
        if fact is None:
            collector.mechanical(
                "PC-M-REQUIRED-001",
                location,
                "authoritative fact ID is not declared by the candidate",
            )
            continue
        if fact.text != required.text:
            collector.mechanical(
                "PC-M-REQUIRED-002",
                location,
                "candidate fact text differs from the authoritative catalog",
            )
            continue
        normalized_required = normalize_lexical_text(required.text)
        covered = any(
            f" {normalized_required} " in content
            for content in normalized_bindings.get(required.id, ())
        )
        if not normalized_required or not covered:
            collector.mechanical(
                "PC-M-REQUIRED-003",
                location,
                "authoritative fact text is not present in its referenced output",
            )


def _validate_duplicates(envelope: Envelope, collector: _Collector) -> None:
    if envelope.response_kind == "non_fit":
        return
    current: list[tuple[str, str | None, str]] = []
    seen: dict[str, tuple[str, str | None]] = {}
    for location, content, exception in _content_records(envelope):
        for unit in lexical_units(content):
            previous = seen.get(unit)
            if previous is not None:
                previous_location, previous_exception = previous
                allowed = (
                    exception == "quotation"
                    and previous_exception == "quotation"
                )
                if not allowed:
                    collector.mechanical(
                        "PC-M-DUPLICATE-001",
                        location,
                        f"exact lexical unit repeats content at {previous_location}",
                    )
            else:
                seen[unit] = (location, exception)
            current.append((unit, exception, location))

    if len(current) > _MAX_NEAR_DUPLICATE_UNITS:
        collector.advisory(
            "PC-A-DUPLICATE-002",
            "payload",
            "near-duplicate scan skipped above its deterministic size bound",
        )
        return
    for index, (unit, exception, location) in enumerate(current):
        if exception == "quotation":
            continue
        if len(unit.split()) < _NEAR_DUPLICATE_MIN_TOKENS:
            continue
        for candidate, _prior_exception, _prior_location in current[:index]:
            if (
                candidate != unit
                and len(candidate.split()) >= _NEAR_DUPLICATE_MIN_TOKENS
                and lexical_similarity(unit, candidate)
                >= _NEAR_DUPLICATE_THRESHOLD
            ):
                collector.advisory(
                    "PC-A-DUPLICATE-001",
                    location,
                    (
                        "high lexical overlap may restate a complete earlier "
                        "proposition; necessary short anchors remain allowed"
                    ),
                )
                break


def _validate_budgets(
    envelope: Envelope,
    collector: _Collector,
) -> dict[str, int]:
    counts = {
        "at_a_glance": 0,
        "in_context": 0,
        "at_depth": 0,
        "warning": 0,
        "correction_exempt": 0,
        "through_in_context": 0,
        "through_in_context_non_warning": 0,
    }
    if envelope.response_kind == "quotation":
        counts["quotation_summary"] = count_english_words(
            envelope.payload["summary"]
        )
        return counts
    if envelope.response_kind != "views":
        return counts
    correction = envelope.payload["correction"]
    if correction is not None:
        counts["correction_exempt"] = count_english_words(correction["content"])
    shallow_total = 0
    shallow_normal = 0
    for index, section in enumerate(envelope.payload["sections"]):
        view = section["view"]
        normal = count_english_words(section["content"])
        warning = section["warning"]
        warning_count = (
            0 if warning is None else count_english_words(warning["content"])
        )
        total = normal + warning_count
        counts[view] = total
        counts["warning"] += warning_count
        if view in {"at_a_glance", "in_context"}:
            shallow_total += total
            shallow_normal += normal
        if view == "at_a_glance" and normal > AT_A_GLANCE_MAX_NON_WARNING_WORDS:
            collector.mechanical(
                "PC-M-BUDGET-001",
                f"payload.sections[{index}].content",
                (
                    f"non-warning At a glance prose has {normal} words; cap is "
                    f"{AT_A_GLANCE_MAX_NON_WARNING_WORDS}"
                ),
            )
    counts["through_in_context"] = shallow_total
    counts["through_in_context_non_warning"] = shallow_normal
    if shallow_normal > THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS:
        collector.mechanical(
            "PC-M-BUDGET-003",
            "payload.sections",
            (
                "non-warning prose through In context has "
                f"{shallow_normal} words; cap is "
                f"{THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS}"
            ),
        )
    return counts


def _validate_branch_and_counts(
    envelope: Envelope,
    request: WrapperRequest | None,
    branch_before: str | None,
    next_fact_count: int,
    collector: _Collector,
) -> None:
    branch_after = envelope.state.branch_after
    if request is not None:
        if request.turn_kind == "narrow_followup" and branch_after is None:
            collector.mechanical(
                "PC-M-BRANCH-001",
                "state.branch_after",
                "narrow_followup requires a selected branch",
            )
        elif (
            request.turn_kind != "narrow_followup"
            and branch_after != branch_before
        ):
            collector.mechanical(
                "PC-M-BRANCH-002",
                "state.branch_after",
                f"{request.turn_kind} must preserve the selected branch",
            )
    if envelope.state.next_fact_count != next_fact_count:
        collector.mechanical(
            "PC-M-STATE-006",
            "state.next_fact_count",
            f"declared {envelope.state.next_fact_count}; computed {next_fact_count}",
        )


def validate_envelope(
    envelope: Envelope,
    *,
    state: ConversationState | None = None,
    request: WrapperRequest | None = None,
    resolved: ResolvedTurn | None = None,
) -> ValidationReport:
    """Validate every mechanically decidable v0.4 rule."""
    committed = state or ConversationState.initial()
    collector = _Collector()
    request_is_valid = True
    if request is not None:
        try:
            expected_resolution = resolve_turn(request, committed)
        except SchemaError as exc:
            collector.mechanical(
                "PC-M-POLICY-001",
                "wrapper_request",
                str(exc),
            )
            request_is_valid = False
            request = None
            resolved = None
        else:
            if resolved is not None and resolved != expected_resolution:
                collector.mechanical(
                    "PC-M-POLICY-002",
                    "resolved_turn",
                    "supplied policy resolution does not match request and state",
                )
            resolved = expected_resolution
    _validate_versions(envelope, committed, request, collector)
    topic, prior_facts = _validate_request_and_state(
        envelope, committed, request, resolved, collector
    )
    _validate_presentation(envelope, collector)
    _validate_correction(envelope, request, prior_facts, collector)
    _validate_quotation(envelope, request, collector)
    next_facts = _validate_facts(
        envelope, prior_facts, committed.turn + 1, resolved, collector
    )
    _validate_required_facts(envelope, request, collector)
    _validate_duplicates(envelope, collector)
    counts = _validate_budgets(envelope, collector)
    _validate_branch_and_counts(
        envelope, request, topic.branch, len(next_facts), collector
    )
    next_topic = TopicState(
        branch=envelope.state.branch_after,
        facts=next_facts,
        host_sessions=topic.host_sessions,
        has_committed_overview=(
            topic.has_committed_overview
            or (resolved is not None and resolved.marks_overview)
        ),
    )
    next_topics = dict(committed.topics)
    next_topics[envelope.topic_id] = next_topic
    next_state = ConversationState(
        active_topic_id=envelope.topic_id,
        turn=committed.turn + 1,
        topics=next_topics,
    )
    has_correction = (
        envelope.response_kind in {"views", "focused"}
        and envelope.payload["correction"] is not None
    )
    has_word_budget = envelope.response_kind == "views" or (
        envelope.response_kind == "quotation"
        and envelope.payload["summary_max_words"] is not None
    )
    mechanical_checks = {
        "schema_and_versions": "PASS",
        "topic_branch_and_state": "PASS",
        "three_view_heading_order": (
            "PASS" if envelope.response_kind == "views" else "NOT_APPLICABLE"
        ),
        "non_empty_view_content": (
            "PASS" if envelope.response_kind == "views" else "NOT_APPLICABLE"
        ),
        "clarification_question_shape": (
            "PASS" if envelope.response_kind == "control" else "NOT_APPLICABLE"
        ),
        "full_warning_placement": (
            "PASS" if envelope.response_kind == "views" else "NOT_APPLICABLE"
        ),
        "english_word_budgets": "PASS" if has_word_budget else "NOT_APPLICABLE",
        "fact_id_integrity_and_declared_reuse": "PASS",
        "authoritative_fact_coverage": (
            "PASS"
            if request is not None and request.required_facts is not None
            else "NOT_APPLICABLE"
        ),
        "exact_lexical_duplicate_detection": (
            "PASS"
            if envelope.response_kind in {"views", "focused", "quotation"}
            else "NOT_APPLICABLE"
        ),
        "correction_structure": "PASS" if has_correction else "NOT_APPLICABLE",
        "quotation_hash_and_expected_source": (
            "PASS"
            if envelope.response_kind == "quotation"
            and request is not None
            and request.controlling_text is not None
            else "NOT_APPLICABLE"
        ),
    }
    for diagnostic in collector.items:
        if diagnostic.domain != "mechanical":
            continue
        code = diagnostic.code
        if code.startswith(("PC-M-SCHEMA", "PC-M-REQUEST", "PC-M-POLICY")) or (
            code == "PC-M-STATE-001"
        ):
            mechanical_checks["schema_and_versions"] = "FAIL"
        elif code.startswith(("PC-M-TOPIC", "PC-M-BRANCH", "PC-M-STATE")):
            mechanical_checks["topic_branch_and_state"] = "FAIL"
        elif code.startswith(("PC-M-HEADING", "PC-M-KIND")):
            mechanical_checks["three_view_heading_order"] = "FAIL"
        elif code.startswith("PC-M-CONTROL"):
            mechanical_checks["clarification_question_shape"] = "FAIL"
        elif code.startswith("PC-M-WARNING"):
            mechanical_checks["full_warning_placement"] = "FAIL"
        elif code.startswith("PC-M-CONTENT"):
            mechanical_checks["non_empty_view_content"] = "FAIL"
        elif code.startswith("PC-M-BUDGET"):
            mechanical_checks["english_word_budgets"] = "FAIL"
        elif code.startswith("PC-M-FACT"):
            mechanical_checks["fact_id_integrity_and_declared_reuse"] = "FAIL"
        elif code.startswith("PC-M-REQUIRED"):
            mechanical_checks["authoritative_fact_coverage"] = "FAIL"
        elif code.startswith("PC-M-DUPLICATE"):
            mechanical_checks["exact_lexical_duplicate_detection"] = "FAIL"
        elif code.startswith("PC-M-CORRECTION"):
            mechanical_checks["correction_structure"] = "FAIL"
        elif code.startswith("PC-M-QUOTE"):
            mechanical_checks["quotation_hash_and_expected_source"] = "FAIL"
    conformant = collector.mechanically_conformant
    certifiable = (
        conformant
        and request_is_valid
        and request is not None
        and resolved is not None
    )
    return ValidationReport(
        mechanically_conformant=conformant,
        certifiable=certifiable,
        diagnostics=tuple(collector.items),
        counts=counts,
        mechanical_checks=mechanical_checks,
        advisory_checks=dict(_ADVISORY_CHECKS),
        next_state=next_state if certifiable else None,
    )


def validate_rendered_markdown(markdown: str) -> ValidationReport:
    """Validate visible checks available to advisory host hooks."""
    collector = _Collector()
    visible_markdown = _mask_fenced_markdown(markdown)
    matches = list(_PROTOCOL_HEADING.finditer(visible_markdown))
    headings = [match.group(1) for match in matches]
    counts: dict[str, int] = {}
    checks = {
        "three_view_heading_order": "UNVERIFIED",
        "non_empty_view_content": "UNVERIFIED",
        "english_word_budgets": "UNVERIFIED",
        "exact_lexical_duplicate_detection": "UNVERIFIED",
        "structured_state_and_fact_ids": "UNVERIFIED",
    }
    if not matches:
        collector.advisory(
            "PC-A-HOOK-001",
            "markdown",
            "no protocol headings; hook cannot distinguish an exception from omission",
        )
    elif headings != list(VIEW_HEADINGS):
        collector.advisory(
            "PC-A-HOOK-003",
            "markdown",
            "reserved headings do not prove that Full presentation was intended",
        )
    else:
        checks["three_view_heading_order"] = "PASS"
        sections: dict[str, str] = {}
        for index, match in enumerate(matches):
            end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(markdown)
            )
            sections[match.group(1)] = markdown[match.end() : end]
        for heading, content in sections.items():
            counts[heading] = count_english_words(content)
            if counts[heading] == 0:
                collector.mechanical(
                    "PC-M-CONTENT-002",
                    heading,
                    "each visible required view must contain counted English prose",
                )
        checks["non_empty_view_content"] = (
            "FAIL"
            if any(item.code.startswith("PC-M-CONTENT") for item in collector.items)
            else "PASS"
        )
        glance_heading, context_heading = VIEW_HEADINGS[:2]
        glance = counts.get(glance_heading, 0)
        context = counts.get(context_heading, 0)
        if (
            glance > AT_A_GLANCE_MAX_NON_WARNING_WORDS
            or glance + context > THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS
        ):
            collector.advisory(
                "PC-A-HOOK-004",
                "markdown",
                "visible text cannot separate budget-exempt warning or "
                "correction prose",
            )
        seen: set[str] = set()
        for heading in headings:
            for unit in lexical_units(sections.get(heading, "")):
                if unit in seen:
                    collector.advisory(
                        "PC-A-HOOK-005",
                        heading,
                        "visible text cannot identify structured duplicate exceptions",
                    )
                else:
                    seen.add(unit)
    collector.advisory(
        "PC-A-HOOK-002",
        "markdown",
        "displayed Markdown lacks the trusted request, state, and fact envelope",
    )
    return ValidationReport(
        mechanically_conformant=collector.mechanically_conformant,
        certifiable=False,
        diagnostics=tuple(collector.items),
        counts=counts,
        mechanical_checks=checks,
        advisory_checks=dict(_ADVISORY_CHECKS),
        next_state=None,
    )


def diagnostic_repair_text(report: ValidationReport) -> str:
    """Return stable feedback containing only mechanical failures."""
    return "\n".join(
        f"- {item.code} at {item.location}: {item.message}"
        for item in report.diagnostics
        if item.domain == "mechanical" and item.severity == "error"
    )
