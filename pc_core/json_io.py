"""Strict JSON parsing for untrusted host, CLI, hook, and state inputs."""

from __future__ import annotations

import json
import math
import os
import tempfile
from pathlib import Path


class JsonContractError(ValueError):
    """Report malformed or ambiguous JSON without echoing input content."""


MAX_JSON_DEPTH = 100


def _object_from_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    parsed: dict[str, object] = {}
    for key, value in pairs:
        if key in parsed:
            raise JsonContractError(
                "JSON objects must not contain duplicate member names"
            )
        parsed[key] = value
    return parsed


def _reject_nonstandard_constant(_value: str) -> object:
    raise JsonContractError(
        "JSON must not contain non-standard numeric constants"
    )


def _validate_json_value(value: object, *, depth: int = 0) -> None:
    if depth > MAX_JSON_DEPTH:
        raise JsonContractError(
            f"JSON nesting must not exceed {MAX_JSON_DEPTH} levels"
        )
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise JsonContractError("JSON numbers must be finite")
        return
    if isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise JsonContractError(
                "JSON strings must contain valid Unicode scalar values"
            ) from exc
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item, depth=depth + 1)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise JsonContractError("JSON object keys must be strings")
            _validate_json_value(key, depth=depth + 1)
            _validate_json_value(item, depth=depth + 1)
        return
    raise JsonContractError(
        f"value of type {type(value).__name__} is not JSON-compatible"
    )


def parse_json(text: str) -> object:
    """Parse standards-compliant JSON and reject duplicate object members."""
    if not isinstance(text, str):
        raise JsonContractError("JSON input must be UTF-8 text")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_from_pairs,
            parse_constant=_reject_nonstandard_constant,
        )
    except JsonContractError:
        raise
    except json.JSONDecodeError as exc:
        raise JsonContractError(
            f"invalid JSON at line {exc.lineno} column {exc.colno}"
        ) from exc
    except (RecursionError, ValueError) as exc:
        raise JsonContractError("JSON input exceeds parser limits") from exc
    _validate_json_value(value)
    return value


def write_json_atomic(path: Path, value: object) -> None:
    """Write one private JSON document with same-directory atomic replacement."""
    _validate_json_value(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            os.fchmod(handle.fileno(), 0o600)
            json.dump(
                value,
                handle,
                ensure_ascii=False,
                sort_keys=True,
                allow_nan=False,
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
