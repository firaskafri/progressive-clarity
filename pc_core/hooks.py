"""Project-local advisory hook adapters for Cursor and Claude Code."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pc_core.json_io import parse_json, write_json_atomic
from pc_core.validation import (
    ValidationReport,
    diagnostic_repair_text,
    validate_rendered_markdown,
)


_SAFE_ID = re.compile(r"[^A-Za-z0-9._-]+")
_SAFE_ID_PREFIX_LENGTH = 64
_SAFE_ID_DIGEST_LENGTH = 16


def _safe_id(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("hook conversation and generation ids must be strings")
    sanitized = _SAFE_ID.sub("_", value).strip("._-") or "id"
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return (
        f"{sanitized[:_SAFE_ID_PREFIX_LENGTH]}-"
        f"{digest[:_SAFE_ID_DIGEST_LENGTH]}"
    )


def _cursor_report_path(data: dict[str, object], state_dir: Path) -> Path:
    conversation = _safe_id(data.get("conversation_id"))
    generation = _safe_id(data.get("generation_id"))
    return state_dir / f"cursor-{conversation}-{generation}.json"


def _load_report(path: Path) -> dict[str, object] | None:
    if not path.is_file() or path.is_symlink():
        return None
    value = parse_json(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _hook_retry_message(report: ValidationReport) -> str:
    failures = diagnostic_repair_text(report)
    return (
        "Progressive Clarity advisory validation found mechanical violations. "
        "Return one complete corrected response; do not discuss this message.\n"
        f"{failures}"
    )


def cursor_after_response(
    data: dict[str, object],
    state_dir: Path,
) -> dict[str, object]:
    """Record advisory validation because Cursor cannot alter displayed output."""
    text = data.get("text")
    if not isinstance(text, str):
        raise ValueError("Cursor afterAgentResponse input is missing text")
    report = validate_rendered_markdown(text)
    write_json_atomic(
        _cursor_report_path(data, state_dir),
        report.to_dict(include_next_state=False),
    )
    return {}


def cursor_stop(data: dict[str, object], state_dir: Path) -> dict[str, object]:
    """Ask Cursor for one retry after an observed mechanical violation."""
    report_path = _cursor_report_path(data, state_dir)
    report_data = _load_report(report_path)
    report_path.unlink(missing_ok=True)
    loop_count = data.get("loop_count")
    if (
        report_data is None
        or report_data.get("mechanically_conformant") is not False
        or not isinstance(loop_count, int)
        or isinstance(loop_count, bool)
        or loop_count >= 1
    ):
        return {}
    diagnostics = report_data.get("diagnostics")
    failures: list[str] = []
    if isinstance(diagnostics, list):
        for item in diagnostics:
            if (
                isinstance(item, dict)
                and item.get("domain") == "mechanical"
                and item.get("severity") == "error"
            ):
                failures.append(
                    f"- {item.get('code')} at {item.get('location')}: "
                    f"{item.get('message')}"
                )
    return {
        "followup_message": (
            "Progressive Clarity advisory validation found mechanical "
            "violations. Return one complete corrected response; do not "
            "discuss this message.\n" + "\n".join(failures)
        )
    }


def claude_stop(data: dict[str, object]) -> dict[str, object]:
    """Block Claude stopping once, then label a second invalid displayed result."""
    text = data.get("last_assistant_message")
    if not isinstance(text, str):
        raise ValueError("Claude Stop input is missing last_assistant_message")
    report = validate_rendered_markdown(text)
    if report.mechanically_conformant:
        return {}
    if data.get("stop_hook_active") is not True:
        return {
            "decision": "block",
            "reason": _hook_retry_message(report),
        }
    return {
        "systemMessage": (
            "Progressive Clarity advisory validation still fails after the "
            "single retry. This displayed output is not mechanically certified; "
            "use the non-streaming pc-core wrapper for fail-closed output."
        )
    }
