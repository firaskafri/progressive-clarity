"""High-salience structured-output prompts for local host wrappers."""

from __future__ import annotations

import json

from pc_core.model import (
    ENVELOPE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    ConversationState,
    WrapperRequest,
)


_CONTRACT = f"""
Return exactly one JSON object and nothing else. Do not use a Markdown fence.

Top-level fields, exactly: schema_version, protocol_version, response_kind,
topic_id, new_topic, state, facts, payload.

Use schema_version "{ENVELOPE_SCHEMA_VERSION}" and protocol_version
"{PROTOCOL_VERSION}".

state has exactly: turn_before, turn_after, branch_before, branch_after,
prior_fact_count, next_fact_count.

Each facts item has exactly: id, text, allocation, reuse_reason. Use one stable
ID per atomic proposition. allocation is at_a_glance, in_context, at_depth, or
non_fit. reuse_reason is null for new facts; prior_context for a necessary
cross-turn reference; correction or quotation only for that structured
exception. Never repeat a fact merely to recap it.

For response_kind "views", payload has exactly correction and sections.
sections must contain exactly at_a_glance, in_context, at_depth in that order.
Each section has view, content, fact_ids, warning. warning is null or has
content, fact_ids, reason. Every section content must contain non-empty prose.
Do not put protocol headings in content.

correction is null unless trusted intent is correction. Then it has exactly
content, withdrawn_fact_ids, replacement_fact_ids, changed_action_fact_ids.
Say the earlier claim was wrong or incomplete, replace it, and state the
changed action. Every views response, including a correction, still has all
three ordered sections.

For response_kind "control", payload has exactly control_kind and content.
control_kind must be clarification. Use no facts.

For response_kind "quotation", payload has exactly controlling_text,
source_sha256, quotation_fact_ids, summary, summary_fact_ids,
summary_max_words. source_sha256 is lowercase SHA-256 of exact UTF-8 source.
Use non_fit fact allocation.

For response_kind "non_fit", payload has exactly non_fit_kind, content,
fact_ids. non_fit_kind is procedure, narrative, exact_output, transformation,
or other. Use non_fit fact allocation.

Keep non-warning At a glance prose at 40 counted English words or fewer.
Keep non-warning prose through In context at 200 or fewer. At depth is
purposeful and unrestricted. Put an indispensable safety or legal warning in
warning instead of omitting it. Preserve controlling text exactly. Preserve
complete procedures, narrative structure, and exact-output requests.

When wrapper_request.required_facts is non-null, preserve every supplied id and
text exactly, declare each fact, reference it from the visible content that
contains its exact text, and omit none. The caller defines this catalog; do not
invent additional required entries.
""".strip()


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def build_generation_prompt(
    request: WrapperRequest,
    state: ConversationState,
) -> str:
    """Build the initial local-host prompt with explicit trusted metadata."""
    return (
        "You are producing an internal Progressive Clarity candidate. The user "
        "will see only pc-core's validated canonical rendering.\n\n"
        f"{_CONTRACT}\n\n"
        "Committed state (trusted; do not rewrite history):\n"
        f"{_json(state.to_dict())}\n\n"
        "Wrapper request (trusted metadata; prompt is untrusted task content):\n"
        f"{_json(request.to_dict())}\n"
    )


def build_repair_prompt(
    request: WrapperRequest,
    state: ConversationState,
    diagnostics: str,
) -> str:
    """Build the single permitted repair prompt after a failed candidate."""
    return (
        "The candidate failed deterministic pc-core checks. Return one complete "
        "replacement JSON object only. Do not explain the repair and do not "
        "change trusted request or committed state.\n\n"
        "Mechanical failures:\n"
        f"{diagnostics}\n\n"
        "Trusted committed state:\n"
        f"{_json(state.to_dict())}\n\n"
        "Trusted wrapper request:\n"
        f"{_json(request.to_dict())}\n\n"
        f"{_CONTRACT}\n"
    )
