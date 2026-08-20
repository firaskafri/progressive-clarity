"""Fail-closed, two-attempt orchestration for non-streaming local hosts."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping

from pc_core.adapters import HostAdapter
from pc_core.json_io import JsonContractError, parse_json
from pc_core.model import Envelope, SchemaError, WrapperRequest
from pc_core.policy import resolve_turn
from pc_core.prompts import build_generation_prompt, build_repair_prompt
from pc_core.render import render_markdown
from pc_core.state import StateStoreProtocol
from pc_core.validation import (
    Diagnostic,
    ValidationReport,
    diagnostic_repair_text,
    validate_envelope,
)


MAX_ATTEMPTS = 2


class WrapperFailure(RuntimeError):
    """Report failure without exposing an uncertified model candidate."""

    def __init__(
        self,
        message: str,
        *,
        attempts: int,
        reports: tuple[ValidationReport, ...],
    ) -> None:
        super().__init__(message)
        self.attempts = attempts
        self.reports = reports


@dataclass(frozen=True)
class CertifiedResult:
    """A mechanically certified rendering and its committed audit metadata."""

    markdown: str
    envelope: Envelope
    report: ValidationReport
    attempts: int
    host: str
    host_metadata: Mapping[str, object]


def _schema_failure(exc: Exception) -> ValidationReport:
    diagnostic = Diagnostic(
        code="PC-M-ENVELOPE-001",
        domain="mechanical",
        severity="error",
        location="host_result",
        message=f"candidate is not a valid versioned envelope: {exc}",
    )
    return ValidationReport(
        mechanically_conformant=False,
        certifiable=False,
        diagnostics=(diagnostic,),
        counts={},
        mechanical_checks={"envelope_parse": "FAIL"},
        advisory_checks={
            "semantic_accuracy": "UNVERIFIED",
            "semantic_completeness": "UNVERIFIED",
        },
        next_state=None,
    )


class CertifiedWrapper:
    """Withhold candidates until pc-core validates and commits their state."""

    def __init__(self, host: HostAdapter, state_store: StateStoreProtocol) -> None:
        self.host = host
        self.state_store = state_store

    def run(self, request: WrapperRequest) -> CertifiedResult:
        """Generate at most twice, fail closed, and commit only a valid result."""
        state = self.state_store.load()
        resolved = resolve_turn(request, state)
        prompt = build_generation_prompt(request, resolved)
        session_id = resolved.topic.host_sessions.get(self.host.name)
        reports: list[ValidationReport] = []
        latest_metadata: Mapping[str, object] = {}

        for attempt in range(1, MAX_ATTEMPTS + 1):
            candidate = self.host.generate(
                prompt,
                session_id=session_id,
            )
            session_id = candidate.session_id
            latest_metadata = candidate.metadata
            try:
                raw_envelope = parse_json(candidate.text)
                envelope = Envelope.from_dict(raw_envelope)
            except (JsonContractError, SchemaError) as exc:
                report = _schema_failure(exc)
            else:
                report = validate_envelope(
                    envelope,
                    state=state,
                    request=request,
                    resolved=resolved,
                )
                if (
                    report.mechanically_conformant
                    and report.certifiable
                    and report.next_state is not None
                ):
                    markdown = render_markdown(envelope)
                    next_topic = report.next_state.topics[request.topic_id]
                    committed_topic = replace(
                        next_topic,
                        host_sessions={
                            **next_topic.host_sessions,
                            self.host.name: session_id,
                        },
                    )
                    committed_state = replace(
                        report.next_state,
                        topics={
                            **report.next_state.topics,
                            request.topic_id: committed_topic,
                        },
                    )
                    committed_report = replace(
                        report,
                        next_state=committed_state,
                    )
                    self.state_store.commit(committed_state)
                    return CertifiedResult(
                        markdown=markdown,
                        envelope=envelope,
                        report=committed_report,
                        attempts=attempt,
                        host=self.host.name,
                        host_metadata=latest_metadata,
                    )
            reports.append(report)
            if attempt < MAX_ATTEMPTS:
                prompt = build_repair_prompt(
                    request,
                    resolved,
                    diagnostic_repair_text(report),
                )

        raise WrapperFailure(
            (
                f"pc-core withheld output after {MAX_ATTEMPTS} mechanically invalid "
                "candidates; semantic conformance was not evaluated"
            ),
            attempts=MAX_ATTEMPTS,
            reports=tuple(reports),
        )
