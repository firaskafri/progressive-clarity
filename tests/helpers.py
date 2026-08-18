"""Name: Deterministic v0.2 test fixture builders.

Description: Builds minimal valid requests and three-view envelopes without
hiding the protocol fields under test.
Assumptions: pc-core's exported versions are authoritative.
Expectations: Fixtures begin mechanically valid and callers mutate only the
field needed for an edge or corner case.
"""

from __future__ import annotations

import copy
import json
from typing import Any

from pc_core.model import (
    ENVELOPE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    WRAPPER_REQUEST_SCHEMA_VERSION,
    Envelope,
    WrapperRequest,
)


def request_dict(
    *,
    prompt: str = "Explain the Atlas adoption decision.",
    topic_id: str = "atlas",
    new_topic: bool = True,
    intent: str = "ordinary",
    controlling_text: str | None = None,
    summary_max_words: int | None = None,
    required_facts: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Return one complete trusted wrapper request document."""
    return {
        "schema_version": WRAPPER_REQUEST_SCHEMA_VERSION,
        "prompt": prompt,
        "topic_id": topic_id,
        "new_topic": new_topic,
        "intent": intent,
        "controlling_text": controlling_text,
        "summary_max_words": summary_max_words,
        "required_facts": required_facts,
    }


def valid_request(**overrides: Any) -> WrapperRequest:
    """Parse a valid request after applying named field overrides."""
    data = request_dict()
    data.update(overrides)
    return WrapperRequest.from_dict(data)


def valid_verbose_dict() -> dict[str, Any]:
    """Return a minimal valid new-topic verbose-only envelope."""
    return {
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
            "next_fact_count": 4,
        },
        "facts": [
            {
                "id": "ATLAS-F1",
                "text": "Atlas should be adopted.",
                "allocation": "at_a_glance",
                "reuse_reason": None,
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
                "allocation": "in_context",
                "reuse_reason": None,
            },
            {
                "id": "ATLAS-F4",
                "text": "The pilot processed 12 million events.",
                "allocation": "at_depth",
                "reuse_reason": None,
            },
        ],
        "payload": {
            "correction": None,
            "sections": [
                {
                    "view": "at_a_glance",
                    "content": "Adopt Atlas because it reduces annual cost.",
                    "fact_ids": ["ATLAS-F1"],
                    "warning": None,
                },
                {
                    "view": "in_context",
                    "content": (
                        "Migration takes two weekends. Security owns approval."
                    ),
                    "fact_ids": ["ATLAS-F2", "ATLAS-F3"],
                    "warning": None,
                },
                {
                    "view": "at_depth",
                    "content": (
                        "The pilot processed 12 million events with 99.97% "
                        "schema validity."
                    ),
                    "fact_ids": ["ATLAS-F4"],
                    "warning": None,
                },
            ],
        },
    }


def valid_verbose_envelope() -> Envelope:
    """Parse the minimal valid verbose-only envelope."""
    return Envelope.from_dict(valid_verbose_dict())


def copied_verbose_dict() -> dict[str, Any]:
    """Return a deep mutable copy for one-field failure scenarios."""
    return copy.deepcopy(valid_verbose_dict())


def envelope_json(data: dict[str, Any] | None = None) -> str:
    """Serialize a deterministic candidate as host output."""
    return json.dumps(data or valid_verbose_dict(), ensure_ascii=False)
