"""Pure presentation policy for trusted topic-oriented wrapper requests."""

from __future__ import annotations

from dataclasses import dataclass

from pc_core.model import (
    PROTOCOL_VERSION,
    STATE_SCHEMA_VERSION,
    ConversationState,
    SchemaError,
    TopicState,
    WrapperRequest,
)


_AUTO_FULL_TURNS = frozenset(
    {
        "decision_checkpoint",
        "summary_checkpoint",
        "material_resynthesis",
        "material_correction",
    }
)
_OVERVIEW_TURNS = _AUTO_FULL_TURNS | {"substantial"}


@dataclass(frozen=True)
class ResolvedTurn:
    """One immutable policy result reused across generation and repair."""

    topic_id: str
    topic_action: str
    topic: TopicState
    turn_before: int
    expected_response_kind: str
    reason: str
    marks_overview: bool

    def context_dict(self) -> dict[str, object]:
        """Return only target-topic context suitable for a model prompt."""
        return {
            "topic_id": self.topic_id,
            "topic_action": self.topic_action,
            "turn_before": self.turn_before,
            "turn_after": self.turn_before + 1,
            "topic": {
                "branch": self.topic.branch,
                "facts": {
                    fact_id: fact.to_dict()
                    for fact_id, fact in sorted(self.topic.facts.items())
                },
                "has_committed_overview": self.topic.has_committed_overview,
            },
            "expected_response_kind": self.expected_response_kind,
            "policy_reason": self.reason,
            "marks_overview_on_success": self.marks_overview,
        }


def _target_topic(request: WrapperRequest, state: ConversationState) -> TopicState:
    request.validate_invariants()
    if state.schema_version != STATE_SCHEMA_VERSION:
        raise SchemaError(
            f"conversation_state.schema_version: expected {STATE_SCHEMA_VERSION}"
        )
    if state.protocol_version != PROTOCOL_VERSION:
        raise SchemaError(
            f"conversation_state.protocol_version: expected {PROTOCOL_VERSION}"
        )
    known = request.topic_id in state.topics
    if request.topic_action == "start":
        if known:
            raise SchemaError(
                "wrapper_request.topic_action: start requires an unknown topic_id"
            )
        topic = TopicState()
    elif request.topic_action == "continue":
        if not known or state.active_topic_id != request.topic_id:
            raise SchemaError(
                "wrapper_request.topic_action: continue requires the active topic_id"
            )
        topic = state.topics[request.topic_id]
    else:
        if not known or state.active_topic_id == request.topic_id:
            raise SchemaError(
                "wrapper_request.topic_action: resume requires a known inactive "
                "topic_id"
            )
        topic = state.topics[request.topic_id]
    if request.required_facts is not None:
        for required in request.required_facts:
            stored = topic.facts.get(required.id)
            if stored is not None and stored.text != required.text:
                raise SchemaError(
                    "wrapper_request.required_facts: "
                    f"{required.id!r} conflicts with committed text"
                )
    return topic


def resolve_turn(
    request: WrapperRequest,
    state: ConversationState,
) -> ResolvedTurn:
    """Resolve one deterministic response shape from trusted classifications."""
    topic = _target_topic(request, state)

    if request.turn_kind == "clarification":
        expected_kind = "control"
        reason = "clarification"
    elif request.turn_kind == "quotation":
        expected_kind = "quotation"
        reason = "quotation"
    elif request.turn_kind == "non_fit":
        expected_kind = "non_fit"
        reason = "non_fit"
    elif request.presentation_request == "focused":
        expected_kind = "focused"
        reason = "explicit_focused"
    elif request.presentation_request == "full":
        expected_kind = "views"
        reason = "explicit_full"
    elif request.turn_kind in _AUTO_FULL_TURNS:
        expected_kind = "views"
        reason = request.turn_kind
    elif request.turn_kind == "substantial" and not topic.has_committed_overview:
        expected_kind = "views"
        reason = "first_substantial"
    else:
        expected_kind = "focused"
        reason = "ordinary_focused"

    marks_overview = (
        expected_kind == "views" and request.turn_kind in _OVERVIEW_TURNS
    )
    return ResolvedTurn(
        topic_id=request.topic_id,
        topic_action=request.topic_action,
        topic=topic,
        turn_before=state.turn,
        expected_response_kind=expected_kind,
        reason=reason,
        marks_overview=marks_overview,
    )
