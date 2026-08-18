"""Deterministic verbose-only validation with explicit semantic boundaries."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from typing import Mapping

from pc_core.model import (
    ENVELOPE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    STATE_SCHEMA_VERSION,
    VIEW_HEADINGS,
    VIEWS,
    WRAPPER_REQUEST_SCHEMA_VERSION,
    ConversationState,
    Envelope,
    StoredFact,
    WrapperRequest,
)
from pc_core.word_count import (
    count_english_words,
    lexical_similarity,
    lexical_units,
    normalize_lexical_text,
)


_FACT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$")
_PROTOCOL_HEADING = re.compile(
    r"(?im)^#{1,6}[ \t]+("
    + "|".join(re.escape(heading) for heading in VIEW_HEADINGS)
    + r")[ \t]*#*[ \t]*$"
)
_CORRECTION_WORD = re.compile(r"\b(?:wrong|incomplete)\b", re.IGNORECASE)
_COMPOUND_FACT_HINT = re.compile(r"(?:[.;]\s+|\b(?:and|but|while|whereas)\b)")
_MAX_NEAR_DUPLICATE_UNITS = 250
_NEAR_DUPLICATE_THRESHOLD = 0.86
_NEAR_DUPLICATE_MIN_TOKENS = 6

_ADVISORY_CHECKS = {
    "semantic_accuracy": "UNVERIFIED",
    "semantic_completeness": "UNVERIFIED",
    "safe_stopping_outcome": "UNVERIFIED",
    "hidden_reversal": "UNVERIFIED",
    "paraphrased_fact_repetition": "UNVERIFIED",
    "fact_atomicity_and_allocation": "UNVERIFIED",
    "warning_indispensability": "UNVERIFIED",
    "correction_exception_scope": "UNVERIFIED",
    "topic_and_branch_intent": "UNVERIFIED",
    "at_depth_relevance_and_purpose": "UNVERIFIED",
}


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


def _expected_kind(request: WrapperRequest) -> str:
    if request.intent == "clarification":
        return "control"
    if request.intent == "quotation":
        return "quotation"
    if request.intent == "non_fit":
        return "non_fit"
    return "views"


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
            for field in (
                "withdrawn_fact_ids",
                "replacement_fact_ids",
                "changed_action_fact_ids",
            ):
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
            for field in (
                "withdrawn_fact_ids",
                "replacement_fact_ids",
                "changed_action_fact_ids",
            ):
                bind(correction[field], correction["content"])
        for section in envelope.payload["sections"]:
            bind(section["fact_ids"], section["content"])
            warning = section["warning"]
            if warning is not None:
                bind(warning["fact_ids"], warning["content"])
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


def _base_state(
    state: ConversationState,
    envelope: Envelope,
) -> tuple[str | None, str | None, dict[str, StoredFact]]:
    if envelope.new_topic:
        return envelope.topic_id, None, {}
    return state.active_topic_id, state.branch, dict(state.facts)


def _validate_request_and_state(
    envelope: Envelope,
    state: ConversationState,
    request: WrapperRequest | None,
    collector: _Collector,
) -> tuple[str | None, str | None, dict[str, StoredFact]]:
    topic_id, branch, facts = _base_state(state, envelope)
    if envelope.new_topic and envelope.topic_id is None:
        collector.mechanical(
            "PC-M-TOPIC-001", "topic_id", "a new topic requires a topic_id"
        )
    if not envelope.new_topic and envelope.topic_id != state.active_topic_id:
        collector.mechanical(
            "PC-M-TOPIC-002",
            "topic_id",
            "continuing output must retain the active topic_id",
        )
    if request is not None:
        if envelope.new_topic != request.new_topic:
            collector.mechanical(
                "PC-M-TOPIC-003",
                "new_topic",
                "envelope new_topic does not match wrapper request",
            )
        if envelope.topic_id != request.topic_id:
            collector.mechanical(
                "PC-M-TOPIC-004",
                "topic_id",
                "envelope topic_id does not match wrapper request",
            )
        expected_kind = _expected_kind(request)
        if envelope.response_kind != expected_kind:
            collector.mechanical(
                "PC-M-KIND-001",
                "response_kind",
                f"intent {request.intent} requires {expected_kind}",
            )
        if (
            envelope.response_kind == "control"
            and envelope.payload["control_kind"] != "clarification"
        ):
            collector.mechanical(
                "PC-M-KIND-002",
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
    if envelope.state.branch_before != branch:
        collector.mechanical(
            "PC-M-STATE-004",
            "state.branch_before",
            "declared branch does not match committed branch state",
        )
    if envelope.state.prior_fact_count != len(facts):
        collector.mechanical(
            "PC-M-STATE-005",
            "state.prior_fact_count",
            f"declared {envelope.state.prior_fact_count}; computed {len(facts)}",
        )
    return topic_id, branch, facts


def _validate_presentation(envelope: Envelope, collector: _Collector) -> None:
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
    for location, content, _exception in _content_records(envelope):
        if _PROTOCOL_HEADING.search(content):
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
    if envelope.response_kind != "views":
        return
    correction = envelope.payload["correction"]
    expects = request is not None and request.intent == "correction"
    if expects and correction is None:
        collector.mechanical(
            "PC-M-CORRECTION-001",
            "payload.correction",
            "correction intent requires structured repair metadata",
        )
        return
    if correction is None:
        return
    if request is not None and request.intent != "correction":
        collector.mechanical(
            "PC-M-CORRECTION-002",
            "payload.correction",
            "structured correction is only valid for correction intent",
        )
    required_lists = (
        ("withdrawn_fact_ids", "withdrawn fact"),
        ("replacement_fact_ids", "replacement fact"),
        ("changed_action_fact_ids", "changed action"),
    )
    for index, (field, label) in enumerate(required_lists, start=3):
        if not correction[field]:
            collector.mechanical(
                f"PC-M-CORRECTION-00{index}",
                f"payload.correction.{field}",
                f"a correction requires at least one {label}",
            )
    for index, fact_id in enumerate(correction["withdrawn_fact_ids"]):
        if fact_id not in prior_facts:
            collector.mechanical(
                "PC-M-CORRECTION-007",
                f"payload.correction.withdrawn_fact_ids[{index}]",
                "a withdrawn fact must exist in the committed topic ledger",
            )
    if _CORRECTION_WORD.search(correction["content"]) is None:
        collector.mechanical(
            "PC-M-CORRECTION-006",
            "payload.correction.content",
            "repair text must say the withdrawn statement was wrong or incomplete",
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
    if expected_cap is not None and declared_cap != expected_cap:
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
            if fact.text != prior.text or fact.allocation != prior.allocation:
                collector.mechanical(
                    "PC-M-FACT-008",
                    location,
                    "a reused id must preserve committed text and allocation",
                )
            if fact.reuse_reason is None:
                collector.mechanical(
                    "PC-M-FACT-009",
                    f"{location}.reuse_reason",
                    "a prior fact requires an explicit reuse reason",
                )
        elif fact.reuse_reason == "prior_context":
            collector.mechanical(
                "PC-M-FACT-010",
                f"{location}.reuse_reason",
                "prior_context is valid only for a committed fact",
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
                allocation=fact.allocation,
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
            normalized_required in normalize_lexical_text(content)
            for content in bindings.get(required.id, ())
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
                    exception in {"correction", "quotation"}
                    and previous_exception == exception
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
        if exception in {"correction", "quotation"}:
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
                    "high lexical overlap may be a paraphrased repeat",
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
        if view == "at_a_glance" and normal > 40:
            collector.mechanical(
                "PC-M-BUDGET-001",
                f"payload.sections[{index}].content",
                f"non-warning At a glance prose has {normal} words; cap is 40",
            )
    counts["through_in_context"] = shallow_total
    counts["through_in_context_non_warning"] = shallow_normal
    if shallow_normal > 200:
        collector.mechanical(
            "PC-M-BUDGET-003",
            "payload.sections",
            (
                "non-warning prose through In context has "
                f"{shallow_normal} words; cap is 200"
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
        if request.intent == "targeted" and branch_after is None:
            collector.mechanical(
                "PC-M-BRANCH-001",
                "state.branch_after",
                "targeted intent requires a selected branch",
            )
        elif request.intent != "targeted" and branch_after != branch_before:
            collector.mechanical(
                "PC-M-BRANCH-002",
                "state.branch_after",
                f"{request.intent} must preserve the selected branch",
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
) -> ValidationReport:
    """Validate every mechanically decidable v0.2 rule."""
    committed = state or ConversationState.initial()
    collector = _Collector()
    _validate_versions(envelope, committed, request, collector)
    topic_id, branch_before, prior_facts = _validate_request_and_state(
        envelope, committed, request, collector
    )
    _validate_presentation(envelope, collector)
    _validate_correction(envelope, request, prior_facts, collector)
    _validate_quotation(envelope, request, collector)
    next_facts = _validate_facts(
        envelope, prior_facts, committed.turn + 1, collector
    )
    _validate_required_facts(envelope, request, collector)
    _validate_duplicates(envelope, collector)
    counts = _validate_budgets(envelope, collector)
    _validate_branch_and_counts(
        envelope, request, branch_before, len(next_facts), collector
    )
    next_state = ConversationState(
        active_topic_id=topic_id,
        branch=envelope.state.branch_after,
        turn=committed.turn + 1,
        facts=next_facts,
        host_sessions=committed.host_sessions,
    )
    has_correction = (
        envelope.response_kind == "views"
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
        "english_word_budgets": "PASS" if has_word_budget else "NOT_APPLICABLE",
        "fact_id_integrity_and_declared_reuse": "PASS",
        "authoritative_fact_coverage": (
            "PASS"
            if request is not None and request.required_facts is not None
            else "NOT_APPLICABLE"
        ),
        "exact_lexical_duplicate_detection": (
            "PASS"
            if envelope.response_kind in {"views", "quotation"}
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
        if code.startswith(("PC-M-SCHEMA", "PC-M-REQUEST")) or code == (
            "PC-M-STATE-001"
        ):
            mechanical_checks["schema_and_versions"] = "FAIL"
        elif code.startswith(("PC-M-TOPIC", "PC-M-BRANCH", "PC-M-STATE")):
            mechanical_checks["topic_branch_and_state"] = "FAIL"
        elif code.startswith(("PC-M-HEADING", "PC-M-KIND")):
            mechanical_checks["three_view_heading_order"] = "FAIL"
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
    return ValidationReport(
        mechanically_conformant=conformant,
        certifiable=conformant and request is not None,
        diagnostics=tuple(collector.items),
        counts=counts,
        mechanical_checks=mechanical_checks,
        advisory_checks=dict(_ADVISORY_CHECKS),
        next_state=next_state if conformant else None,
    )


def validate_rendered_markdown(markdown: str) -> ValidationReport:
    """Validate visible checks available to advisory host hooks."""
    collector = _Collector()
    matches = list(_PROTOCOL_HEADING.finditer(markdown))
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
    else:
        expected = ["At a glance", "In context", "At depth"]
        if headings != expected:
            collector.mechanical(
                "PC-M-HEADING-003",
                "markdown",
                f"visible heading sequence {headings} must be {expected}",
            )
            checks["three_view_heading_order"] = "FAIL"
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
        glance = counts.get("At a glance", 0)
        context = counts.get("In context", 0)
        if glance > 40:
            collector.mechanical(
                "PC-M-BUDGET-005",
                "At a glance",
                f"visible prose has {glance} counted words; cap is 40",
            )
        if glance + context > 200:
            collector.mechanical(
                "PC-M-BUDGET-006",
                "In context",
                (
                    "visible prose through In context has "
                    f"{glance + context} words; cap is 200"
                ),
            )
        checks["english_word_budgets"] = (
            "FAIL"
            if any(item.code.startswith("PC-M-BUDGET") for item in collector.items)
            else "PASS"
        )
        seen: dict[str, str] = {}
        for heading in headings:
            for unit in lexical_units(sections.get(heading, "")):
                if unit in seen:
                    collector.mechanical(
                        "PC-M-DUPLICATE-002",
                        heading,
                        f"exact lexical unit repeats {seen[unit]}: {unit!r}",
                    )
                else:
                    seen[unit] = heading
        checks["exact_lexical_duplicate_detection"] = (
            "FAIL"
            if any(item.code.startswith("PC-M-DUPLICATE") for item in collector.items)
            else "PASS"
        )
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
