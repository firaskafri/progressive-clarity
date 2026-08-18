"""Canonical Markdown rendering from a validated structured envelope."""

from __future__ import annotations

from pc_core.model import VIEW_HEADINGS, VIEWS, Envelope


_VIEW_HEADING_BY_NAME = dict(zip(VIEWS, VIEW_HEADINGS, strict=True))


def _terminal_newline(text: str) -> str:
    return text if text.endswith("\n") else f"{text}\n"


def _render_views(envelope: Envelope) -> str:
    parts: list[str] = []
    correction = envelope.payload["correction"]
    for section in envelope.payload["sections"]:
        body: list[str] = []
        if section["view"] == "at_a_glance" and correction is not None:
            body.append(correction["content"].strip())
        warning = section["warning"]
        if warning is not None:
            body.append(warning["content"].strip())
        if section["content"].strip():
            body.append(section["content"].strip())
        rendered = f"## {_VIEW_HEADING_BY_NAME[section['view']]}"
        if body:
            rendered += "\n\n" + "\n\n".join(body)
        parts.append(rendered)
    return _terminal_newline("\n\n".join(parts))


def _render_quotation(envelope: Envelope) -> str:
    controlling_text = envelope.payload["controlling_text"]
    summary = envelope.payload["summary"].strip()
    rendered = (
        "**Controlling text:**\n"
        f"{controlling_text}\n\n"
        "**Non-controlling plain-language summary:**\n"
        f"{summary}"
    )
    return _terminal_newline(rendered)


def render_markdown(envelope: Envelope) -> str:
    """Render the only canonical visible representation for an envelope."""
    if envelope.response_kind == "views":
        return _render_views(envelope)
    if envelope.response_kind == "quotation":
        return _render_quotation(envelope)
    if envelope.response_kind == "non_fit":
        return envelope.payload["content"]
    return _terminal_newline(envelope.payload["content"])
