"""Atomic persistence for deterministic Progressive Clarity conversation state."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Protocol

from pc_core.model import (
    PROTOCOL_VERSION,
    STATE_SCHEMA_VERSION,
    ConversationState,
    SchemaError,
)


class StateError(RuntimeError):
    """Report state loading or commit failures."""


class StateStoreProtocol(Protocol):
    """Minimal transactional state-store interface used by the wrapper."""

    def load(self) -> ConversationState:
        """Load committed state without changing it."""

    def commit(self, state: ConversationState) -> None:
        """Atomically replace committed state."""


class FileStateStore:
    """Persist one conversation state document with same-directory replacement."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> ConversationState:
        """Load state, returning the required initial state when absent."""
        if self.path.is_symlink():
            raise StateError(f"state path must not be a symlink: {self.path}")
        if not self.path.exists():
            return ConversationState.initial()
        if not self.path.is_file():
            raise StateError(f"state path must be a regular file: {self.path}")
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            state = ConversationState.from_dict(data)
        except (OSError, json.JSONDecodeError, SchemaError) as exc:
            raise StateError(f"cannot load state {self.path}: {exc}") from exc
        if state.schema_version != STATE_SCHEMA_VERSION:
            raise StateError(
                f"unsupported state schema {state.schema_version}; "
                f"expected {STATE_SCHEMA_VERSION}"
            )
        if state.protocol_version != PROTOCOL_VERSION:
            raise StateError(
                f"state protocol {state.protocol_version}; expected {PROTOCOL_VERSION}"
            )
        return state

    def commit(self, state: ConversationState) -> None:
        """Write, sync, and atomically replace the state file."""
        if self.path.is_symlink():
            raise StateError(f"refusing to replace symlink state path: {self.path}")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            payload = (
                json.dumps(
                    state.to_dict(),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                dir=self.path.parent,
                text=True,
            )
            temporary = Path(temporary_name)
            try:
                os.fchmod(descriptor, 0o600)
                with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                    handle.write(payload)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, self.path)
                directory_descriptor = os.open(self.path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_descriptor)
                finally:
                    os.close(directory_descriptor)
            finally:
                temporary.unlink(missing_ok=True)
        except OSError as exc:
            raise StateError(f"cannot commit state {self.path}: {exc}") from exc


class MemoryStateStore:
    """In-memory transactional store for embedders and deterministic tests."""

    def __init__(self, state: ConversationState | None = None) -> None:
        self.state = state or ConversationState.initial()
        self.commit_count = 0

    def load(self) -> ConversationState:
        """Return the currently committed immutable state."""
        return self.state

    def commit(self, state: ConversationState) -> None:
        """Commit state and record the transaction count."""
        self.state = state
        self.commit_count += 1
