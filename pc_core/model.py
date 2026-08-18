"""Versioned verbose-only domain models and strict parsers for pc-core."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


ENVELOPE_SCHEMA_VERSION = "2.0.0"
STATE_SCHEMA_VERSION = "2.1.0"
WRAPPER_REQUEST_SCHEMA_VERSION = "2.1.0"
PROTOCOL_VERSION = "0.2"

VIEWS = ("at_a_glance", "in_context", "at_depth")
VIEW_HEADINGS = ("At a glance", "In context", "At depth")
VIEW_SET = frozenset(VIEWS)
RESPONSE_KINDS = frozenset({"views", "control", "quotation", "non_fit"})
INTENTS = frozenset(
    {
        "ordinary",
        "targeted",
        "correction",
        "clarification",
        "quotation",
        "non_fit",
    }
)
ALLOCATIONS = frozenset({*VIEWS, "non_fit"})
REUSE_REASONS = frozenset({"prior_context", "correction", "quotation"})
NON_FIT_KINDS = frozenset(
    {"procedure", "narrative", "exact_output", "transformation", "other"}
)


class SchemaError(ValueError):
    """Report a structured-data shape error with a stable field path."""


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
    allocation: str
    first_turn: int

    @classmethod
    def from_dict(cls, value: object, path: str) -> StoredFact:
        """Parse one committed fact."""
        data = _object(value, path)
        _exact_keys(data, {"text", "allocation", "first_turn"}, path)
        return cls(
            text=_string(data["text"], f"{path}.text"),
            allocation=_enum(data["allocation"], ALLOCATIONS, f"{path}.allocation"),
            first_turn=_integer(data["first_turn"], f"{path}.first_turn", minimum=1),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize one committed fact."""
        return {
            "text": self.text,
            "allocation": self.allocation,
            "first_turn": self.first_turn,
        }


@dataclass(frozen=True)
class RequiredFact:
    """One caller-authoritative fact requiring exact normalized output coverage."""

    id: str
    text: str

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
    _exact_keys(
        data,
        {
            "content",
            "withdrawn_fact_ids",
            "replacement_fact_ids",
            "changed_action_fact_ids",
        },
        path,
    )
    return {
        "content": _string(data["content"], f"{path}.content"),
        "withdrawn_fact_ids": _string_list(
            data["withdrawn_fact_ids"], f"{path}.withdrawn_fact_ids"
        ),
        "replacement_fact_ids": _string_list(
            data["replacement_fact_ids"], f"{path}.replacement_fact_ids"
        ),
        "changed_action_fact_ids": _string_list(
            data["changed_action_fact_ids"], f"{path}.changed_action_fact_ids"
        ),
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
    topic_id: str | None
    new_topic: bool
    state: DeclaredState
    facts: tuple[Fact, ...]
    payload: Mapping[str, object]

    @classmethod
    def from_dict(cls, value: object) -> Envelope:
        """Parse an envelope and reject every unknown or missing field."""
        data = _object(value, "envelope")
        _exact_keys(
            data,
            {
                "schema_version",
                "protocol_version",
                "response_kind",
                "topic_id",
                "new_topic",
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
            topic_id=_optional_string(data["topic_id"], "topic_id"),
            new_topic=_boolean(data["new_topic"], "new_topic"),
            state=DeclaredState.from_dict(data["state"]),
            facts=tuple(
                Fact.from_dict(fact, f"facts[{index}]")
                for index, fact in enumerate(facts)
            ),
            payload=_parse_payload(kind, data["payload"], "payload"),
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
            correction = payload["correction"]
            if correction is not None:
                payload["correction"] = {
                    **correction,
                    "withdrawn_fact_ids": list(correction["withdrawn_fact_ids"]),
                    "replacement_fact_ids": list(correction["replacement_fact_ids"]),
                    "changed_action_fact_ids": list(
                        correction["changed_action_fact_ids"]
                    ),
                }
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
            "new_topic": self.new_topic,
            "state": self.state.to_dict(),
            "facts": [fact.to_dict() for fact in self.facts],
            "payload": payload,
        }


@dataclass(frozen=True)
class ConversationState:
    """Committed state used for topic, branch, turn, and fact-ID validation."""

    schema_version: str = STATE_SCHEMA_VERSION
    protocol_version: str = PROTOCOL_VERSION
    active_topic_id: str | None = None
    branch: str | None = None
    turn: int = 0
    facts: Mapping[str, StoredFact] = field(default_factory=dict)
    host_sessions: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def initial(cls) -> ConversationState:
        """Return the required new-conversation state."""
        return cls()

    @classmethod
    def from_dict(cls, value: object) -> ConversationState:
        """Parse a strict persisted state document."""
        data = _object(value, "conversation_state")
        _exact_keys(
            data,
            {
                "schema_version",
                "protocol_version",
                "active_topic_id",
                "branch",
                "turn",
                "facts",
                "host_sessions",
            },
            "conversation_state",
        )
        facts_data = _object(data["facts"], "conversation_state.facts")
        facts = {
            fact_id: StoredFact.from_dict(
                stored, f"conversation_state.facts.{fact_id}"
            )
            for fact_id, stored in facts_data.items()
        }
        sessions_data = _object(
            data["host_sessions"], "conversation_state.host_sessions"
        )
        host_sessions = {
            host: _string(
                session_id,
                f"conversation_state.host_sessions.{host}",
            )
            for host, session_id in sessions_data.items()
        }
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
            branch=_optional_string(data["branch"], "conversation_state.branch"),
            turn=_integer(data["turn"], "conversation_state.turn"),
            facts=facts,
            host_sessions=host_sessions,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize state for atomic persistence."""
        return {
            "schema_version": self.schema_version,
            "protocol_version": self.protocol_version,
            "active_topic_id": self.active_topic_id,
            "branch": self.branch,
            "turn": self.turn,
            "facts": {
                fact_id: stored.to_dict()
                for fact_id, stored in sorted(self.facts.items())
            },
            "host_sessions": dict(sorted(self.host_sessions.items())),
        }

@dataclass(frozen=True)
class WrapperRequest:
    """Trusted host metadata used to validate topic, intent, and exceptions."""

    schema_version: str
    prompt: str
    topic_id: str
    new_topic: bool
    intent: str
    controlling_text: str | None
    summary_max_words: int | None
    required_facts: tuple[RequiredFact, ...] | None

    @classmethod
    def from_dict(cls, value: object) -> WrapperRequest:
        """Parse a strict wrapper request."""
        data = _object(value, "wrapper_request")
        _exact_keys(
            data,
            {
                "schema_version",
                "prompt",
                "topic_id",
                "new_topic",
                "intent",
                "controlling_text",
                "summary_max_words",
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
        intent = _enum(data["intent"], INTENTS, "wrapper_request.intent")
        controlling_text = _optional_string(
            data["controlling_text"], "wrapper_request.controlling_text"
        )
        if intent == "quotation" and controlling_text is None:
            raise SchemaError(
                "wrapper_request.controlling_text: quotation intent requires "
                "trusted source text"
            )
        if intent != "quotation" and (
            controlling_text is not None or summary_max_words is not None
        ):
            raise SchemaError(
                "wrapper_request: controlling_text and summary_max_words are "
                "valid only for quotation intent"
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
            required_ids = [fact.id for fact in required_facts]
            if len(required_ids) != len(set(required_ids)):
                raise SchemaError(
                    "wrapper_request.required_facts: duplicate IDs are not allowed"
                )
        return cls(
            schema_version=_string(
                data["schema_version"], "wrapper_request.schema_version"
            ),
            prompt=_string(data["prompt"], "wrapper_request.prompt"),
            topic_id=_string(data["topic_id"], "wrapper_request.topic_id"),
            new_topic=_boolean(data["new_topic"], "wrapper_request.new_topic"),
            intent=intent,
            controlling_text=controlling_text,
            summary_max_words=summary_max_words,
            required_facts=required_facts,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize request metadata for prompts and diagnostics."""
        return {
            "schema_version": self.schema_version,
            "prompt": self.prompt,
            "topic_id": self.topic_id,
            "new_topic": self.new_topic,
            "intent": self.intent,
            "controlling_text": self.controlling_text,
            "summary_max_words": self.summary_max_words,
            "required_facts": (
                None
                if self.required_facts is None
                else [fact.to_dict() for fact in self.required_facts]
            ),
        }
