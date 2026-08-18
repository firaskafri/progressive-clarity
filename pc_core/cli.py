"""Command-line entry points for validation, rendering, wrappers, and hooks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from pc_core.adapters import (
    HostInvocationError,
    claude_code_adapter,
    cursor_adapter,
)
from pc_core.hooks import claude_stop, cursor_after_response, cursor_stop
from pc_core.model import (
    ConversationState,
    Envelope,
    SchemaError,
    WrapperRequest,
)
from pc_core.render import render_markdown
from pc_core.state import FileStateStore, StateError
from pc_core.validation import validate_envelope
from pc_core.wrapper import CertifiedWrapper, WrapperFailure


def _read_json(path: str) -> object:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _state(path: str | None) -> ConversationState:
    if path is None:
        return ConversationState.initial()
    return FileStateStore(Path(path)).load()


def _request(path: str | None) -> WrapperRequest | None:
    if path is None:
        return None
    return WrapperRequest.from_dict(_read_json(path))


def _write_report(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _validate_command(args: argparse.Namespace) -> int:
    envelope = Envelope.from_dict(_read_json(args.envelope))
    report = validate_envelope(
        envelope,
        state=_state(args.state),
        request=_request(args.request),
    )
    print(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report.mechanically_conformant else 1


def _render_command(args: argparse.Namespace) -> int:
    envelope = Envelope.from_dict(_read_json(args.envelope))
    report = validate_envelope(
        envelope,
        state=_state(args.state),
        request=_request(args.request),
    )
    if not report.mechanically_conformant:
        print(
            json.dumps(
                report.to_dict(include_next_state=False),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    sys.stdout.write(render_markdown(envelope))
    return 0


def _wrap_command(args: argparse.Namespace) -> int:
    request = WrapperRequest.from_dict(_read_json(args.request))
    cwd = Path(args.cwd).resolve()
    if args.trust_workspace and args.host != "cursor":
        raise SchemaError("--trust-workspace is supported only for Cursor")
    if args.host == "cursor":
        host = cursor_adapter(
            cwd=cwd,
            executable=args.executable or "agent",
            timeout_seconds=args.timeout,
            trust_workspace=args.trust_workspace,
        )
    else:
        host = claude_code_adapter(
            cwd=cwd,
            executable=args.executable or "claude",
            timeout_seconds=args.timeout,
        )
    wrapper = CertifiedWrapper(host, FileStateStore(Path(args.state)))
    try:
        result = wrapper.run(request)
    except WrapperFailure as exc:
        failure = {
            "status": "WITHHELD",
            "attempts": exc.attempts,
            "message": str(exc),
            "reports": [
                report.to_dict(include_next_state=False) for report in exc.reports
            ],
        }
        print(
            json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True),
            file=sys.stderr,
        )
        return 1
    if args.report is not None:
        _write_report(
            Path(args.report),
            {
                "status": "MECHANICALLY_CERTIFIED",
                "semantic_conformance": "UNVERIFIED",
                "host": result.host,
                "attempts": result.attempts,
                "host_metadata": dict(result.host_metadata),
                "validation": result.report.to_dict(),
            },
        )
    sys.stdout.write(result.markdown)
    return 0


def _hook_command(args: argparse.Namespace) -> int:
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            raise ValueError("hook input must be an object")
        if args.adapter == "cursor-after-response":
            output = cursor_after_response(data, Path(args.state_dir))
        elif args.adapter == "cursor-stop":
            output = cursor_stop(data, Path(args.state_dir))
        else:
            output = claude_stop(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        if args.adapter == "claude-stop":
            output = {
                "systemMessage": (
                    "Progressive Clarity advisory hook failed and did not "
                    f"certify this output: {exc}"
                )
            }
        else:
            output = {}
    print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pc-core",
        description=(
            "Deterministic Progressive Clarity mechanics. Mechanical PASS does "
            "not claim semantic completeness, accuracy, or hidden-reversal safety."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate", help="validate a versioned response envelope"
    )
    validate.add_argument("envelope", help="JSON envelope path or - for stdin")
    validate.add_argument("--state", help="committed state JSON path")
    validate.add_argument("--request", help="trusted wrapper request JSON path")
    validate.set_defaults(handler=_validate_command)

    render = subparsers.add_parser(
        "render", help="validate then render canonical Markdown"
    )
    render.add_argument("envelope", help="JSON envelope path or - for stdin")
    render.add_argument("--state", help="committed state JSON path")
    render.add_argument("--request", help="trusted wrapper request JSON path")
    render.set_defaults(handler=_render_command)

    wrap = subparsers.add_parser(
        "wrap", help="run a non-streaming local host with fail-closed validation"
    )
    wrap.add_argument("--host", choices=("cursor", "claude-code"), required=True)
    wrap.add_argument("--request", required=True, help="trusted request JSON path")
    wrap.add_argument("--state", required=True, help="state JSON path")
    wrap.add_argument("--cwd", default=".", help="host working directory")
    wrap.add_argument("--executable", help="override the documented host executable")
    wrap.add_argument("--timeout", type=int, default=300, help="per-attempt seconds")
    wrap.add_argument("--report", help="optional certified audit-report path")
    wrap.add_argument(
        "--trust-workspace",
        action="store_true",
        help=(
            "explicitly authorize Cursor to trust --cwd; omit after an "
            "interactive trust bootstrap"
        ),
    )
    wrap.set_defaults(handler=_wrap_command)

    hook = subparsers.add_parser(
        "hook", help="run a project-local advisory host hook adapter"
    )
    hook.add_argument(
        "adapter",
        choices=("cursor-after-response", "cursor-stop", "claude-stop"),
    )
    hook.add_argument(
        "--state-dir",
        default=".pc-core/hook-state",
        help="Cursor hook handoff directory",
    )
    hook.set_defaults(handler=_hook_command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and return a stable process status."""
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (
        OSError,
        json.JSONDecodeError,
        SchemaError,
        StateError,
        HostInvocationError,
    ) as exc:
        print(f"pc-core: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
