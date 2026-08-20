"""Versioned topic-oriented domain models and strict parsers for pc-core."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


ENVELOPE_SCHEMA_VERSION = "3.0.0"
STATE_SCHEMA_VERSION = "3.0.0"
WRAPPER_REQUEST_SCHEMA_VERSION = "3.0.0"
PROTOCOL_VERSION = "0.4"
AT_A_GLANCE_MAX_NON_WARNING_WORDS = 40
THROUGH_IN_CONTEXT_MAX_NON_WARNING_WORDS = 200
FACT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$")

VIEWS = ("at_a_glance", "in_context", "at_depth")
VIEW_HEADINGS = ("At a glance", "In context", "At depth")
VIEW_SET = frozenset(VIEWS)
RESPONSE_KINDS = frozenset(
    {"views", "focused", "control", "quotation", "non_fit"}
)
TOPIC_ACTIONS = frozenset({"start", "continue", "resume"})
CORRECTION_TURN_KINDS = frozenset(
    {"narrow_correction", "material_correction"}
)
TURN_KINDS = frozenset(
    {
        "simple_fact",
        "ordinary",
        "narrow_followup",
        "substantial",
        "decision_checkpoint",
        "summary_checkpoint",
        "material_resynthesis",
        *CORRECTION_TURN_KINDS,
        "clarification",
        "quotation",
        "non_fit",
    }
)
PRESENTATION_REQUESTS = frozenset({"auto", "focused", "full"})
ALLOCATIONS = frozenset({*VIEWS, "focused", "non_fit"})
REUSE_REASONS = frozenset(
    {"prior_context", "synthesis", "correction", "quotation"}
)
CORRECTION_FACT_FIELDS = (
    "withdrawn_fact_ids",
    "replacement_fact_ids",
    "changed_action_fact_ids",
)
NON_FIT_KINDS = frozenset(
    {"procedure", "narrative", "exact_output", "transformation", "other"}
)


class SchemaError(ValueError):
    """Report a structured-data shape error with a stable field path."""


def _freeze_value(value: object) -> object:
    """Recursively snapshot JSON-like values behind immutable containers."""
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _freeze_value(item) for key, item in value.items()}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_value(item) for item in value)
    return value


def _object(value: object, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SchemaError(f"{path}: expected object")
    if not all(isinstance(key, str) for key in value):
        raise SchemaError(f"{path}: object keys must be strings")
    return value


def _exact_keys(value: Mapping[str, object], expected: set[str], path: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        raise SchemaError(f"{path}: missing fields {missing}")
    if unexpected:
        raise SchemaError(f"{path}: unexpected fields are not allowed")


def _string(value: object, path: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise SchemaError(f"{path}: expected string")
    if not allow_empty and not value.strip():
        raise SchemaError(f"{path}: must not be empty")
    return value


def _optional_string(value: object, path: str) -> str | None:
    if value is None:
        return None
    return _string(value, path)


def _boolean(value: object, path: str) -> bool:
    if not isinstance(value, bool):
        raise SchemaError(f"{path}: expected boolean")
    return value


def _integer(value: object, path: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise SchemaError(f"{path}: expected integer")
    if value < minimum:
        raise SchemaError(f"{path}: expected integer >= {minimum}")
    return value


def _enum(value: object, choices: frozenset[str], path: str) -> str:
    parsed = _string(value, path)
    if parsed not in choices:
        raise SchemaError(f"{path}: expected one of {sorted(choices)}")
    return parsed


def _string_list(value: object, path: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise SchemaError(f"{path}: expected array")
    parsed = tuple(
        _string(item, f"{path}[{index}]") for index, item in enumerate(value)
    )
    if len(parsed) != len(set(parsed)):
        raise SchemaError(f"{path}: duplicate values are not allowed")
    return parsed


@dataclass(frozen=True)
class Fact:
    """One declared atomic fact and its allocation or cross-turn reuse metadata."""

    id: str
    text: str
    allocation: str
    reuse_reason: str | None

    def __post_init__(self) -> None:
        """Validate directly constructed fact values."""
        _string(self.id, "fact.id")
        if FACT_ID_PATTERN.fullmatch(self.id) is None:
            raise SchemaError(
                "fact.id: expected 1-64 safe identifier characters"
            )
        _string(self.text, "fact.text")
        _enum(self.allocation, ALLOCATIONS, "fact.allocation")
        if self.reuse_reason is not None:
            _enum(self.reuse_reason, REUSE_REASONS, "fact.reuse_reason")

    @classmethod
    def from_dict(cls, value: object, path: str) -> Fact:
        """Parse one strict fact object."""
        data = _object(value, path)
        _exact_keys(data, {"id", "text", "allocation", "reuse_reason"}, path)
        reuse_reason = data["reuse_reason"]
        if reuse_reason is not None:
            reuse_reason = _enum(reuse_reason, REUSE_REASONS, f"{path}.reuse_reason")
        return cls(
            id=_string(data["id"], f"{path}.id"),
            text=_string(data["text"], f"{path}.text"),
            allocation=_enum(data["allocation"], ALLOCATIONS, f"{path}.allocation"),
            reuse_reason=reuse_reason,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the fact deterministically."""
        return {
            "id": self.id,
            "text": self.text,
            "allocation": self.allocation,
            "reuse_reason": self.reuse_reason,
        }


@dataclass(frozen=True)
class StoredFact:
    """A fact committed in the active topic state."""

    text: str
    first_turn: int

    def __post_init__(self) -> None:
        """Validate directly constructed stored facts."""
        _string(self.text, "stored_fact.text")
        _integer(self.first_turn, "stored_fact.first_turn", minimum=1)

    @classmethod
    def from_dict(cls, value: object, path: str) -> StoredFact:
        """Parse one committed fact."""
        data = _object(value, path)
        _exact_keys(data, {"text", "first_turn"}, path)
        return cls(
            text=_string(data["text"], f"{path}.text"),
            first_turn=_integer(data["first_turn"], f"{path}.first_turn", minimum=1),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize one committed fact."""
        return {
            "text": self.text,
            "first_turn": self.first_turn,
        }


@dataclass(frozen=True)
class RequiredFact:
    """One caller-authoritative fact requiring exact normalized output coverage."""

    id: str
    text: str

    def __post_init__(self) -> None:
        """Validate directly constructed authoritative facts."""
        _string(self.id, "required_fact.id")
        if FACT_ID_PATTERN.fullmatch(self.id) is None:
            raise SchemaError(
                "required_fact.id: expected 1-64 safe identifier characters"
            )
        _string(self.text, "required_fact.text")
        if "\n" in self.text or "\r" in self.text:
            raise SchemaError("required_fact.text: must be one physical line")
        if re.search(r"[A-Za-z0-9]", self.text) is None:
            raise SchemaError(
                "required_fact.text: must contain a lexical token"
            )

    @classmethod
    def from_dict(cls, value: object, path: str) -> RequiredFact:
        """Parse one strict authoritative fact."""
        data = _object(value, path)
        _exact_keys(data, {"id", "text"}, path)
        return cls(
            id=_string(data["id"], f"{path}.id"),
            text=_string(data["text"], f"{path}.text"),
        )

    def to_dict(self) -> dict[str, str]:
        """Serialize one authoritative fact."""
        return {"id": self.id, "text": self.text}


@dataclass(frozen=True)
class DeclaredState:
    """Candidate-declared state transition for deterministic validation."""

    turn_before: int
    turn_after: int
    branch_before: str | None
    branch_after: str | None
    prior_fact_count: int
    next_fact_count: int

    def __post_init__(self) -> None:
        """Validate directly constructed transition values."""
        _integer(self.turn_before, "state.turn_before")
        _integer(self.turn_after, "state.turn_after")
        _optional_string(self.branch_before, "state.branch_before")
        _optional_string(self.branch_after, "state.branch_after")
        _integer(self.prior_fact_count, "state.prior_fact_count")
        _integer(self.next_fact_count, "state.next_fact_count")

    @classmethod
    def from_dict(cls, value: object, path: str = "state") -> DeclaredState:
        """Parse the explicit state transition in an envelope."""
        data = _object(value, path)
        _exact_keys(
            data,
            {
                "turn_before",
                "turn_after",
                "branch_before",
                "branch_after",
                "prior_fact_count",
                "next_fact_count",
            },
            path,
        )
        return cls(
            turn_before=_integer(data["turn_before"], f"{path}.turn_before"),
            turn_after=_integer(data["turn_after"], f"{path}.turn_after"),
            branch_before=_optional_string(
                data["branch_before"], f"{path}.branch_before"
            ),
            branch_after=_optional_string(data["branch_after"], f"{path}.branch_after"),
            prior_fact_count=_integer(
                data["prior_fact_count"], f"{path}.prior_fact_count"
            ),
            next_fact_count=_integer(
                data["next_fact_count"], f"{path}.next_fact_count"
            ),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the declared transition."""
        return {
            "turn_before": self.turn_before,
            "turn_after": self.turn_after,
            "branch_before": self.branch_before,
            "branch_after": self.branch_after,
            "prior_fact_count": self.prior_fact_count,
            "next_fact_count": self.next_fact_count,
        }


def _parse_warning(value: object, path: str) -> dict[str, object] | None:
    if value is None:
        return None
    data = _object(value, path)
    _exact_keys(data, {"content", "fact_ids", "reason"}, path)
    return {
        "content": _string(data["content"], f"{path}.content"),
        "fact_ids": _string_list(data["fact_ids"], f"{path}.fact_ids"),
        "reason": _string(data["reason"], f"{path}.reason"),
    }


def _parse_section(value: object, path: str) -> dict[str, object]:
    data = _object(value, path)
    _exact_keys(data, {"view", "content", "fact_ids", "warning"}, path)
    return {
        "view": _enum(data["view"], VIEW_SET, f"{path}.view"),
        "content": _string(data["content"], f"{path}.content"),
        "fact_ids": _string_list(data["fact_ids"], f"{path}.fact_ids"),
        "warning": _parse_warning(data["warning"], f"{path}.warning"),
    }


def _parse_correction(value: object, path: str) -> dict[str, object] | None:
    if value is None:
        return None
    data = _object(value, path)
    _exact_keys(data, {"content", *CORRECTION_FACT_FIELDS}, path)
    return {
        "content": _string(data["content"], f"{path}.content"),
        **{
            field: _string_list(data[field], f"{path}.{field}")
            for field in CORRECTION_FACT_FIELDS
        },
    }


def _serialize_correction(
    correction: Mapping[str, object] | None,
) -> dict[str, object] | None:
    """Serialize correction fact references as JSON arrays."""
    if correction is None:
        return None
    return {
        **correction,
        **{
            field: list(correction[field])
            for field in CORRECTION_FACT_FIELDS
        },
    }


def _parse_payload(kind: str, value: object, path: str) -> dict[str, object]:
    data = _object(value, path)
    if kind == "views":
        _exact_keys(data, {"correction", "sections"}, path)
        sections = data["sections"]
        if not isinstance(sections, list):
            raise SchemaError(f"{path}.sections: expected array")
        return {
            "correction": _parse_correction(data["correction"], f"{path}.correction"),
            "sections": tuple(
                _parse_section(section, f"{path}.sections[{index}]")
                for index, section in enumerate(sections)
            ),
        }
    if kind == "focused":
        _exact_keys(data, {"content", "fact_ids", "warning", "correction"}, path)
        correction = _parse_correction(
            data["correction"],
            f"{path}.correction",
        )
        return {
            "content": _string(
                data["content"],
                f"{path}.content",
                allow_empty=correction is not None,
            ),
            "fact_ids": _string_list(data["fact_ids"], f"{path}.fact_ids"),
            "warning": _parse_warning(data["warning"], f"{path}.warning"),
            "correction": correction,
        }
    if kind == "control":
        _exact_keys(data, {"control_kind", "content"}, path)
        control_kind = _string(data["control_kind"], f"{path}.control_kind")
        if control_kind != "clarification":
            raise SchemaError(f"{path}.control_kind: expected 'clarification'")
        return {
            "control_kind": control_kind,
            "content": _string(data["content"], f"{path}.content"),
        }
    if kind == "quotation":
        _exact_keys(
            data,
            {
                "controlling_text",
                "source_sha256",
                "quotation_fact_ids",
                "summary",
                "summary_fact_ids",
                "summary_max_words",
            },
            path,
        )
        summary_max_words = data["summary_max_words"]
        if summary_max_words is not None:
            summary_max_words = _integer(
                summary_max_words, f"{path}.summary_max_words", minimum=1
            )
        return {
            "controlling_text": _string(
                data["controlling_text"],
                f"{path}.controlling_text",
                allow_empty=True,
            ),
            "source_sha256": _string(data["source_sha256"], f"{path}.source_sha256"),
            "quotation_fact_ids": _string_list(
                data["quotation_fact_ids"], f"{path}.quotation_fact_ids"
            ),
            "summary": _string(data["summary"], f"{path}.summary"),
            "summary_fact_ids": _string_list(
                data["summary_fact_ids"], f"{path}.summary_fact_ids"
            ),
            "summary_max_words": summary_max_words,
        }
    _exact_keys(data, {"non_fit_kind", "content", "fact_ids"}, path)
    return {
        "non_fit_kind": _enum(
            data["non_fit_kind"], NON_FIT_KINDS, f"{path}.non_fit_kind"
        ),
        "content": _string(data["content"], f"{path}.content", allow_empty=True),
        "fact_ids": _string_list(data["fact_ids"], f"{path}.fact_ids"),
    }


@dataclass(frozen=True)
class Envelope:
    """A complete model candidate before deterministic validation and rendering."""

    schema_version: str
    protocol_version: str
    response_kind: str
    topic_id: str
    topic_action: str
    state: DeclaredState
    facts: tuple[Fact, ...]
    payload: Mapping[str, object]

    def __post_init__(self) -> None:
        """Validate direct values and snapshot one parsed payload."""
        if self.schema_version != ENVELOPE_SCHEMA_VERSION:
            raise SchemaError(
                "envelope.schema_version: unsupported candidate version; "
                f"expected {ENVELOPE_SCHEMA_VERSION}"
            )
        if self.protocol_version != PROTOCOL_VERSION:
            raise SchemaError(
                "envelope.protocol_version: unsupported candidate version; "
                f"expected {PROTOCOL_VERSION}"
            )
        kind = _enum(self.response_kind, RESPONSE_KINDS, "response_kind")
        _string(self.topic_id, "topic_id")
        _enum(self.topic_action, TOPIC_ACTIONS, "topic_action")
        if not isinstance(self.state, DeclaredState):
            raise SchemaError("state: expected DeclaredState")
        if not isinstance(self.facts, tuple):
            raise SchemaError("facts: expected tuple")
        if any(not isinstance(fact, Fact) for fact in self.facts):
            raise SchemaError("facts: every item must be Fact")
        if not isinstance(self.payload, Mapping):
            raise SchemaError("payload: expected object")
        parsed_payload = _parse_payload(kind, dict(self.payload), "payload")
        frozen_payload = _freeze_value(parsed_payload)
        if not isinstance(frozen_payload, Mapping):
            raise SchemaError("payload: expected object")
        object.__setattr__(self, "payload", frozen_payload)

    @classmethod
    def from_dict(cls, value: object) -> Envelope:
        """Parse an envelope and reject every unknown or missing field."""
        data = _object(value, "envelope")
        if data.get("schema_version") != ENVELOPE_SCHEMA_VERSION:
            raise SchemaError(
                "envelope.schema_version: unsupported candidate version; "
                f"expected {ENVELOPE_SCHEMA_VERSION}"
            )
        if data.get("protocol_version") != PROTOCOL_VERSION:
            raise SchemaError(
                "envelope.protocol_version: unsupported candidate version; "
                f"expected {PROTOCOL_VERSION}"
            )
        _exact_keys(
            data,
            {
                "schema_version",
                "protocol_version",
                "response_kind",
                "topic_id",
                "topic_action",
                "state",
                "facts",
                "payload",
            },
            "envelope",
        )
        kind = _enum(data["response_kind"], RESPONSE_KINDS, "response_kind")
        facts = data["facts"]
        if not isinstance(facts, list):
            raise SchemaError("facts: expected array")
        return cls(
            schema_version=_string(data["schema_version"], "schema_version"),
            protocol_version=_string(data["protocol_version"], "protocol_version"),
            response_kind=kind,
            topic_id=_string(data["topic_id"], "topic_id"),
            topic_action=_enum(
                data["topic_action"], TOPIC_ACTIONS, "topic_action"
            ),
            state=DeclaredState.from_dict(data["state"]),
            facts=tuple(
                Fact.from_dict(fact, f"facts[{index}]")
                for index, fact in enumerate(facts)
            ),
            payload=_object(data["payload"], "payload"),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the envelope in canonical field order."""
        payload: dict[str, object] = dict(self.payload)
        if self.response_kind == "views":
            payload["sections"] = [
                {
                    **section,
                    "fact_ids": list(section["fact_ids"]),
                    "warning": (
                        None
                        if section["warning"] is None
                        else {
                            **section["warning"],
                            "fact_ids": list(section["warning"]["fact_ids"]),
                        }
                    ),
                }
                for section in payload["sections"]
            ]
            payload["correction"] = _serialize_correction(payload["correction"])
        elif self.response_kind == "focused":
            payload["fact_ids"] = list(payload["fact_ids"])
            warning = payload["warning"]
            if warning is not None:
                payload["warning"] = {
                    **warning,
                    "fact_ids": list(warning["fact_ids"]),
                }
            payload["correction"] = _serialize_correction(payload["correction"])
        elif self.response_kind == "quotation":
            payload["quotation_fact_ids"] = list(payload["quotation_fact_ids"])
            payload["summary_fact_ids"] = list(payload["summary_fact_ids"])
        elif self.response_kind == "non_fit":
            payload["fact_ids"] = list(payload["fact_ids"])
        return {
            "schema_version": self.schema_version,
            "protocol_version": self.protocol_version,
            "response_kind": self.response_kind,
            "topic_id": self.topic_id,
            "topic_action": self.topic_action,
            "state": self.state.to_dict(),
            "facts": [fact.to_dict() for fact in self.facts],
            "payload": payload,
        }


@dataclass(frozen=True)
class TopicState:
    """Committed branch, fact, overview, and host-session state for one topic."""

    branch: str | None = None
    facts: Mapping[str, StoredFact] = field(default_factory=dict)
    host_sessions: Mapping[str, str] = field(default_factory=dict)
    has_committed_overview: bool = False

    def __post_init__(self) -> None:
        """Validate and snapshot topic mappings behind read-only views."""
        _optional_string(self.branch, "topic.branch")
        if not isinstance(self.facts, Mapping):
            raise SchemaError("topic.facts: expected mapping")
        for fact_id, stored in self.facts.items():
            _string(fact_id, "topic.facts key")
            if FACT_ID_PATTERN.fullmatch(fact_id) is None:
                raise SchemaError(
                    "topic.facts key: expected 1-64 safe identifier characters"
                )
            if not isinstance(stored, StoredFact):
                raise SchemaError("topic.facts values must be StoredFact")
        if not isinstance(self.host_sessions, Mapping):
            raise SchemaError("topic.host_sessions: expected mapping")
        for host, session_id in self.host_sessions.items():
            _string(host, "topic.host_sessions key")
            _string(session_id, f"topic.host_sessions.{host}")
        _boolean(self.has_committed_overview, "topic.has_committed_overview")
        object.__setattr__(self, "facts", MappingProxyType(dict(self.facts)))
        object.__setattr__(
            self,
            "host_sessions",
            MappingProxyType(dict(self.host_sessions)),
        )

    @classmethod
    def from_dict(cls, value: object, path: str) -> TopicState:
        """Parse one strict persisted topic document."""
        data = _object(value, path)
        _exact_keys(
            data,
            {"branch", "facts", "host_sessions", "has_committed_overview"},
            path,
        )
        facts_data = _object(data["facts"], f"{path}.facts")
        sessions_data = _object(data["host_sessions"], f"{path}.host_sessions")
        return cls(
            branch=_optional_string(data["branch"], f"{path}.branch"),
            facts={
                fact_id: StoredFact.from_dict(stored, f"{path}.facts.{fact_id}")
                for fact_id, stored in facts_data.items()
            },
            host_sessions={
                host: _string(session_id, f"{path}.host_sessions.{host}")
                for host, session_id in sessions_data.items()
            },
            has_committed_overview=_boolean(
                data["has_committed_overview"],
                f"{path}.has_committed_overview",
            ),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize one topic deterministically."""
        return {
            "branch": self.branch,
            "facts": {
                fact_id: stored.to_dict()
                for fact_id, stored in sorted(self.facts.items())
            },
            "host_sessions": dict(sorted(self.host_sessions.items())),
            "has_committed_overview": self.has_committed_overview,
        }


@dataclass(frozen=True)
class ConversationState:
    """Committed multi-topic state used for deterministic validation."""

    schema_version: str = STATE_SCHEMA_VERSION
    protocol_version: str = PROTOCOL_VERSION
    active_topic_id: str | None = None
    turn: int = 0
    topics: Mapping[str, TopicState] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and snapshot mutable topic inputs."""
        _string(self.schema_version, "conversation_state.schema_version")
        _string(self.protocol_version, "conversation_state.protocol_version")
        _optional_string(
            self.active_topic_id,
            "conversation_state.active_topic_id",
        )
        _integer(self.turn, "conversation_state.turn")
        if not isinstance(self.topics, Mapping):
            raise SchemaError("conversation_state.topics: expected mapping")
        for topic_id, topic in self.topics.items():
            _string(topic_id, "conversation_state.topics key")
            if not isinstance(topic, TopicState):
                raise SchemaError(
                    "conversation_state.topics values must be TopicState"
                )
            for stored in topic.facts.values():
                if stored.first_turn > self.turn:
                    raise SchemaError(
                        "stored fact first_turn must not exceed conversation turn"
                    )
        object.__setattr__(self, "topics", MappingProxyType(dict(self.topics)))
        if self.active_topic_id is not None and self.active_topic_id not in self.topics:
            raise SchemaError(
                "conversation_state.active_topic_id: must identify a stored topic"
            )

    @classmethod
    def initial(cls) -> ConversationState:
        """Return the required new-conversation state."""
        return cls()

    @classmethod
    def from_dict(cls, value: object) -> ConversationState:
        """Parse a strict persisted state document."""
        data = _object(value, "conversation_state")
        if data.get("schema_version") != STATE_SCHEMA_VERSION:
            raise SchemaError(
                "conversation_state.schema_version: unsupported version "
                f"{data.get('schema_version')!r}; expected {STATE_SCHEMA_VERSION}"
            )
        if data.get("protocol_version") != PROTOCOL_VERSION:
            raise SchemaError(
                "conversation_state.protocol_version: unsupported version "
                f"{data.get('protocol_version')!r}; expected {PROTOCOL_VERSION}"
            )
        _exact_keys(
            data,
            {
                "schema_version",
                "protocol_version",
                "active_topic_id",
                "turn",
                "topics",
            },
            "conversation_state",
        )
        topics_data = _object(data["topics"], "conversation_state.topics")
        return cls(
            schema_version=_string(
                data["schema_version"], "conversation_state.schema_version"
            ),
            protocol_version=_string(
                data["protocol_version"], "conversation_state.protocol_version"
            ),
            active_topic_id=_optional_string(
                data["active_topic_id"], "conversation_state.active_topic_id"
            ),
            turn=_integer(data["turn"], "conversation_state.turn"),
            topics={
                topic_id: TopicState.from_dict(
                    topic, f"conversation_state.topics.{topic_id}"
                )
                for topic_id, topic in topics_data.items()
            },
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize state for atomic persistence."""
        return {
            "schema_version": self.schema_version,
            "protocol_version": self.protocol_version,
            "active_topic_id": self.active_topic_id,
            "turn": self.turn,
            "topics": {
                topic_id: topic.to_dict()
                for topic_id, topic in sorted(self.topics.items())
            },
        }


@dataclass(frozen=True)
class WrapperRequest:
    """Trusted caller metadata used to select and certify one response shape."""

    schema_version: str
    prompt: str
    topic_id: str
    topic_action: str
    turn_kind: str
    presentation_request: str
    controlling_text: str | None
    summary_max_words: int | None
    non_fit_kind: str | None
    required_facts: tuple[RequiredFact, ...] | None

    def validate_invariants(self) -> None:
        """Validate invariants for parsed and directly constructed requests."""
        if self.schema_version != WRAPPER_REQUEST_SCHEMA_VERSION:
            raise SchemaError(
                "wrapper_request.schema_version: unsupported version "
                f"{self.schema_version!r}; expected {WRAPPER_REQUEST_SCHEMA_VERSION}"
            )
        for field_name, value in (
            ("prompt", self.prompt),
            ("topic_id", self.topic_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SchemaError(
                    f"wrapper_request.{field_name}: must not be empty"
                )
        if (
            not isinstance(self.topic_action, str)
            or self.topic_action not in TOPIC_ACTIONS
        ):
            raise SchemaError(
                "wrapper_request.topic_action: expected one of "
                f"{sorted(TOPIC_ACTIONS)}"
            )
        if not isinstance(self.turn_kind, str) or self.turn_kind not in TURN_KINDS:
            raise SchemaError(
                f"wrapper_request.turn_kind: expected one of {sorted(TURN_KINDS)}"
            )
        if (
            not isinstance(self.presentation_request, str)
            or self.presentation_request not in PRESENTATION_REQUESTS
        ):
            raise SchemaError(
                "wrapper_request.presentation_request: expected one of "
                f"{sorted(PRESENTATION_REQUESTS)}"
            )
        if self.controlling_text is not None and (
            not isinstance(self.controlling_text, str)
            or not self.controlling_text.strip()
        ):
            raise SchemaError(
                "wrapper_request.controlling_text: must be a non-empty string"
            )
        if self.summary_max_words is not None and (
            not isinstance(self.summary_max_words, int)
            or isinstance(self.summary_max_words, bool)
            or self.summary_max_words < 1
        ):
            raise SchemaError(
                "wrapper_request.summary_max_words: expected integer >= 1"
            )
        if self.non_fit_kind is not None and (
            not isinstance(self.non_fit_kind, str)
            or self.non_fit_kind not in NON_FIT_KINDS
        ):
            raise SchemaError(
                "wrapper_request.non_fit_kind: expected one of "
                f"{sorted(NON_FIT_KINDS)}"
            )
        if self.turn_kind == "quotation" and self.controlling_text is None:
            raise SchemaError(
                "wrapper_request.controlling_text: quotation requires trusted text"
            )
        if self.turn_kind != "quotation" and (
            self.controlling_text is not None
            or self.summary_max_words is not None
        ):
            raise SchemaError(
                "wrapper_request: controlling_text and summary_max_words are "
                "valid only for quotation"
            )
        if self.turn_kind == "non_fit" and self.non_fit_kind is None:
            raise SchemaError(
                "wrapper_request.non_fit_kind: non_fit requires a kind"
            )
        if self.turn_kind != "non_fit" and self.non_fit_kind is not None:
            raise SchemaError(
                "wrapper_request.non_fit_kind: valid only for non_fit"
            )
        if self.required_facts is None:
            return
        if self.turn_kind == "clarification":
            raise SchemaError(
                "wrapper_request.required_facts: clarification cannot render facts"
            )
        if not isinstance(self.required_facts, tuple):
            raise SchemaError(
                "wrapper_request.required_facts: expected tuple or null"
            )
        if not self.required_facts:
            raise SchemaError(
                "wrapper_request.required_facts: authoritative catalog "
                "must not be empty"
            )
        required_ids: list[str] = []
        for index, fact in enumerate(self.required_facts):
            if not isinstance(fact, RequiredFact):
                raise SchemaError(
                    f"wrapper_request.required_facts[{index}]: "
                    "expected RequiredFact"
                )
            if not isinstance(fact.id, str) or not fact.id.strip():
                raise SchemaError(
                    f"wrapper_request.required_facts[{index}].id: "
                    "must not be empty"
                )
            if not isinstance(fact.text, str) or not fact.text.strip():
                raise SchemaError(
                    f"wrapper_request.required_facts[{index}].text: "
                    "must not be empty"
                )
            required_ids.append(fact.id)
        if len(required_ids) != len(set(required_ids)):
            raise SchemaError(
                "wrapper_request.required_facts: duplicate IDs are not allowed"
            )

    @classmethod
    def from_dict(cls, value: object) -> WrapperRequest:
        """Parse a strict wrapper request."""
        data = _object(value, "wrapper_request")
        if data.get("schema_version") != WRAPPER_REQUEST_SCHEMA_VERSION:
            raise SchemaError(
                "wrapper_request.schema_version: unsupported version "
                f"{data.get('schema_version')!r}; "
                f"expected {WRAPPER_REQUEST_SCHEMA_VERSION}"
            )
        _exact_keys(
            data,
            {
                "schema_version",
                "prompt",
                "topic_id",
                "topic_action",
                "turn_kind",
                "presentation_request",
                "controlling_text",
                "summary_max_words",
                "non_fit_kind",
                "required_facts",
            },
            "wrapper_request",
        )
        summary_max_words = data["summary_max_words"]
        if summary_max_words is not None:
            summary_max_words = _integer(
                summary_max_words,
                "wrapper_request.summary_max_words",
                minimum=1,
            )
        turn_kind = _enum(
            data["turn_kind"], TURN_KINDS, "wrapper_request.turn_kind"
        )
        controlling_text = _optional_string(
            data["controlling_text"], "wrapper_request.controlling_text"
        )
        non_fit_kind = data["non_fit_kind"]
        if non_fit_kind is not None:
            non_fit_kind = _enum(
                non_fit_kind, NON_FIT_KINDS, "wrapper_request.non_fit_kind"
            )
        required_facts_data = data["required_facts"]
        required_facts: tuple[RequiredFact, ...] | None
        if required_facts_data is None:
            required_facts = None
        elif not isinstance(required_facts_data, list):
            raise SchemaError("wrapper_request.required_facts: expected array or null")
        elif not required_facts_data:
            raise SchemaError(
                "wrapper_request.required_facts: authoritative catalog "
                "must not be empty"
            )
        else:
            required_facts = tuple(
                RequiredFact.from_dict(
                    item,
                    f"wrapper_request.required_facts[{index}]",
                )
                for index, item in enumerate(required_facts_data)
            )
        request = cls(
            schema_version=_string(
                data["schema_version"], "wrapper_request.schema_version"
            ),
            prompt=_string(data["prompt"], "wrapper_request.prompt"),
            topic_id=_string(data["topic_id"], "wrapper_request.topic_id"),
            topic_action=_enum(
                data["topic_action"], TOPIC_ACTIONS, "wrapper_request.topic_action"
            ),
            turn_kind=turn_kind,
            presentation_request=_enum(
                data["presentation_request"],
                PRESENTATION_REQUESTS,
                "wrapper_request.presentation_request",
            ),
            controlling_text=controlling_text,
            summary_max_words=summary_max_words,
            non_fit_kind=non_fit_kind,
            required_facts=required_facts,
        )
        request.validate_invariants()
        return request

    def to_dict(self) -> dict[str, object]:
        """Serialize request metadata for prompts and diagnostics."""
        return {
            "schema_version": self.schema_version,
            "prompt": self.prompt,
            "topic_id": self.topic_id,
            "topic_action": self.topic_action,
            "turn_kind": self.turn_kind,
            "presentation_request": self.presentation_request,
            "controlling_text": self.controlling_text,
            "summary_max_words": self.summary_max_words,
            "non_fit_kind": self.non_fit_kind,
            "required_facts": (
                None
                if self.required_facts is None
                else [fact.to_dict() for fact in self.required_facts]
            ),
        }
