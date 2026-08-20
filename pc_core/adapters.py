"""Non-streaming local host adapters behind a reusable subprocess interface."""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Protocol, Sequence

from pc_core.json_io import JsonContractError, parse_json


class HostInvocationError(RuntimeError):
    """Report a local host process or response-contract failure."""


@dataclass(frozen=True)
class HostCandidate:
    """One completed host candidate and the session needed for bounded repair."""

    text: str
    session_id: str
    metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        """Validate session identity and snapshot host metadata."""
        if not isinstance(self.session_id, str) or not self.session_id:
            raise ValueError("host candidate session_id must be non-empty text")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


class HostAdapter(Protocol):
    """Interface future local hosts can implement without changing pc-core."""

    name: str

    def generate(self, prompt: str, *, session_id: str | None = None) -> HostCandidate:
        """Generate one non-streaming candidate, optionally resuming a session."""


@dataclass(frozen=True)
class JsonCliSpec:
    """Declarative contract for a completed-result JSON CLI."""

    name: str
    executable: str
    initial_arguments: tuple[str, ...]
    resume_arguments: tuple[str, ...]
    prompt_argument: str | None = None
    result_field: str = "result"
    session_field: str = "session_id"


class JsonCliHostAdapter:
    """Run a JSON CLI without a shell and parse its completed result."""

    def __init__(
        self,
        spec: JsonCliSpec,
        *,
        cwd: Path,
        timeout_seconds: int = 300,
    ) -> None:
        self.spec = spec
        self.name = spec.name
        self.cwd = cwd
        self.timeout_seconds = timeout_seconds

    def _command(self, session_id: str | None) -> list[str]:
        command = [self.spec.executable, *self.spec.initial_arguments]
        if session_id is not None:
            command.extend(self.spec.resume_arguments)
            command.append(session_id)
        if self.spec.prompt_argument is not None:
            command.append(self.spec.prompt_argument)
        return command

    def generate(self, prompt: str, *, session_id: str | None = None) -> HostCandidate:
        """Run one completed generation and reject malformed host output."""
        command = self._command(session_id)
        try:
            completed = subprocess.run(
                command,
                input=prompt,
                text=True,
                encoding="utf-8",
                capture_output=True,
                cwd=self.cwd,
                timeout=self.timeout_seconds,
                check=False,
            )
        except UnicodeError as exc:
            raise HostInvocationError(
                f"{self.name} returned process output that is not valid UTF-8"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise HostInvocationError(
                f"{self.name} timed out after {self.timeout_seconds} seconds"
            ) from exc
        except OSError as exc:
            raise HostInvocationError(
                f"{self.name} invocation failed before completion: {exc}"
            ) from exc
        if completed.returncode != 0:
            stderr_bytes = completed.stderr.encode("utf-8")
            stderr_digest = hashlib.sha256(stderr_bytes).hexdigest()
            raise HostInvocationError(
                f"{self.name} exited {completed.returncode}: "
                f"stderr_bytes={len(stderr_bytes)} stderr_sha256={stderr_digest}"
            )
        try:
            payload = parse_json(completed.stdout)
        except JsonContractError as exc:
            raise HostInvocationError(
                f"{self.name} did not return one JSON result object: {exc}"
            ) from exc
        if not isinstance(payload, dict):
            raise HostInvocationError(f"{self.name} result must be a JSON object")
        result = payload.get(self.spec.result_field)
        returned_session = payload.get(self.spec.session_field)
        if not isinstance(result, str):
            raise HostInvocationError(
                f"{self.name} result field {self.spec.result_field!r} is not text"
            )
        if not isinstance(returned_session, str) or not returned_session:
            raise HostInvocationError(
                f"{self.name} session field {self.spec.session_field!r} is missing"
            )
        if session_id is not None and returned_session != session_id:
            raise HostInvocationError(
                f"{self.name} returned a different resumed session identifier"
            )
        metadata = {
            key: value
            for key, value in payload.items()
            if key not in {self.spec.result_field, self.spec.session_field}
        }
        return HostCandidate(
            text=result,
            session_id=returned_session,
            metadata=metadata,
        )


def cursor_adapter(
    *,
    cwd: Path,
    executable: str = "agent",
    timeout_seconds: int = 300,
    trust_workspace: bool = False,
) -> JsonCliHostAdapter:
    """Create a Cursor adapter with optional explicit workspace trust opt-in."""
    trust_arguments = ("--trust",) if trust_workspace else ()
    return JsonCliHostAdapter(
        JsonCliSpec(
            name="cursor",
            executable=executable,
            initial_arguments=(
                "-p",
                *trust_arguments,
                "--output-format",
                "json",
                "--mode",
                "ask",
                "--workspace",
                str(cwd),
            ),
            resume_arguments=("--resume",),
            prompt_argument=(
                "Process the complete Progressive Clarity request supplied "
                "on stdin."
            ),
        ),
        cwd=cwd,
        timeout_seconds=timeout_seconds,
    )


def claude_code_adapter(
    *,
    cwd: Path,
    executable: str = "claude",
    timeout_seconds: int = 300,
) -> JsonCliHostAdapter:
    """Create the tested-against-docs Claude Code print-mode adapter."""
    return JsonCliHostAdapter(
        JsonCliSpec(
            name="claude-code",
            executable=executable,
            initial_arguments=("-p", "--output-format", "json"),
            resume_arguments=("--resume",),
            prompt_argument=(
                "Process the complete Progressive Clarity request supplied "
                "on stdin."
            ),
        ),
        cwd=cwd,
        timeout_seconds=timeout_seconds,
    )


def command_preview(
    adapter: JsonCliHostAdapter,
    session_id: str | None = None,
) -> Sequence[str]:
    """Expose an argv preview for documentation and non-executing tests."""
    return tuple(adapter._command(session_id))
