"""Project-local advisory hook adapters for Cursor and Claude Code."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import TextIO

from pc_core.validation import (
    ValidationReport,
    diagnostic_repair_text,
    validate_rendered_markdown,
)


_SAFE_ID = re.compile(r"[^A-Za-z0-9._-]+")


def _read_object(stdin: TextIO) -> dict[str, object]:
    value = json.load(stdin)
    if not isinstance(value, dict):
        raise ValueError("hook input must be a JSON object")
    return value


def _safe_id(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("hook conversation and generation ids must be strings")
    sanitized = _SAFE_ID.sub("_", value)
    if not sanitized:
        raise ValueError("hook id has no safe characters")
    return sanitized[:160]


def _cursor_report_path(data: dict[str, object], state_dir: Path) -> Path:
    conversation = _safe_id(data.get("conversation_id"))
    generation = _safe_id(data.get("generation_id"))
    return state_dir / f"cursor-{conversation}-{generation}.json"


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _load_report(path: Path) -> dict[str, object] | None:
    if not path.is_file() or path.is_symlink():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
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
    _atomic_json(
        _cursor_report_path(data, state_dir),
        report.to_dict(include_next_state=False),
    )
    return {}


def cursor_stop(data: dict[str, object], state_dir: Path) -> dict[str, object]:
    """Ask Cursor for one retry after an observed mechanical violation."""
    report_data = _load_report(_cursor_report_path(data, state_dir))
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
