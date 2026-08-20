"""Canonical Markdown rendering from a validated structured envelope."""

from __future__ import annotations

from typing import Mapping

from pc_core.model import VIEW_HEADINGS, VIEWS, Envelope


_VIEW_HEADING_BY_NAME = dict(zip(VIEWS, VIEW_HEADINGS, strict=True))


def _terminal_newline(text: str) -> str:
    return text if text.endswith("\n") else f"{text}\n"


def _prelude_parts(
    correction: Mapping[str, object] | None,
    warning: Mapping[str, object] | None,
) -> list[str]:
    """Return correction and warning prose in canonical precedence order."""
    parts: list[str] = []
    if correction is not None:
        parts.append(str(correction["content"]).strip())
    if warning is not None:
        parts.append(str(warning["content"]).strip())
    return parts


def _render_views(envelope: Envelope) -> str:
    parts: list[str] = []
    correction = envelope.payload["correction"]
    for section in envelope.payload["sections"]:
        warning = section["warning"]
        section_correction = (
            correction if section["view"] == "at_a_glance" else None
        )
        body = _prelude_parts(section_correction, warning)
        if section["content"].strip():
            body.append(section["content"].strip())
        rendered = f"## {_VIEW_HEADING_BY_NAME[section['view']]}"
        if body:
            rendered += "\n\n" + "\n\n".join(body)
        parts.append(rendered)
    return _terminal_newline("\n\n".join(parts))


def _render_focused(envelope: Envelope) -> str:
    warning = envelope.payload["warning"]
    correction = envelope.payload["correction"]
    parts = _prelude_parts(correction, warning)
    parts.append(envelope.payload["content"].strip())
    return _terminal_newline("\n\n".join(part for part in parts if part))


def _render_quotation(envelope: Envelope) -> str:
    controlling_text = envelope.payload["controlling_text"]
    summary = envelope.payload["summary"].strip()
    rendered = (
        "Controlling text:\n"
        f"{controlling_text}\n\n"
        "Non-controlling plain-language summary:\n"
        f"{summary}"
    )
    return _terminal_newline(rendered)


def render_markdown(envelope: Envelope) -> str:
    """Render the only canonical visible representation for an envelope."""
    if envelope.response_kind == "views":
        return _render_views(envelope)
    if envelope.response_kind == "focused":
        return _render_focused(envelope)
    if envelope.response_kind == "quotation":
        return _render_quotation(envelope)
    if envelope.response_kind == "non_fit":
        return envelope.payload["content"]
    return _terminal_newline(envelope.payload["content"])
