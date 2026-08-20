"""Name: CLI and advisory-hook integration suite.

Description: Exercises validate/render process behavior, stdout withholding,
diagnostic redaction, Cursor response-to-stop handoff, Claude one-retry
decisions, protocol-v0.4 envelopes, audit/request/state path isolation, and
checked-in project template schemas.
Assumptions: Hook APIs cannot establish the trusted structured state available
to the non-streaming wrapper.
Expectations: CLI render is fail closed; hooks label themselves non-certifying
and request no more than one retry.
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from pc_core.cli import main
from pc_core.hooks import claude_stop, cursor_after_response, cursor_stop
from pc_core.validation import validate_rendered_markdown
from tests.helpers import request_dict, valid_focused_dict, valid_full_dict


class ValidateRenderCliTests(unittest.TestCase):
    """Name: Validate and render command behavior.

    Description: Runs CLI handlers with temporary trusted request and candidate
    files for passing and failing scenarios, including invalid candidate prose
    that must not escape through diagnostics and report paths that must not
    replace committed state.
    Assumptions: Initial state is used when no state file is supplied.
    Expectations: Reports are machine-readable and invalid output is withheld.
    """

    def test_validate_prints_separated_mechanical_and_advisory_status(self) -> None:
        """Name: Validate report boundary.

        Description: Validates a complete substantial v0.4 candidate.
        Assumptions: Request and envelope identify the same new topic.
        Expectations: Exit zero reports mechanical certification and semantic
        UNVERIFIED status separately.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            envelope_path = root / "envelope.json"
            request_path = root / "request.json"
            envelope_path.write_text(
                json.dumps(valid_full_dict()),
                encoding="utf-8",
            )
            request_path.write_text(
                json.dumps(request_dict()),
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                status = main(
                    [
                        "validate",
                        str(envelope_path),
                        "--request",
                        str(request_path),
                    ]
                )
        report = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertTrue(report["mechanically_conformant"])
        self.assertEqual(report["semantic_conformance"], "UNVERIFIED")

    def test_render_outputs_only_canonical_markdown_after_pass(self) -> None:
        """Name: Render success output.

        Description: Runs the validating renderer on a valid candidate.
        Assumptions: Diagnostics are unnecessary on successful stdout.
        Expectations: Output starts with the canonical At-a-glance heading.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            envelope_path = root / "envelope.json"
            request_path = root / "request.json"
            envelope_path.write_text(
                json.dumps(valid_full_dict()),
                encoding="utf-8",
            )
            request_path.write_text(
                json.dumps(request_dict()),
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                status = main(
                    [
                        "render",
                        str(envelope_path),
                        "--request",
                        str(request_path),
                    ]
                )
        self.assertEqual(status, 0)
        self.assertTrue(output.getvalue().startswith("## At a glance\n"))

    def test_render_withholds_invalid_candidate(self) -> None:
        """Name: Render failure withholding.

        Description: Reverses a valid candidate's mandatory section sequence.
        Assumptions: Stderr may expose diagnostics but never candidate prose.
        Expectations: Exit one leaves stdout empty and emits a failure report.
        """
        data = valid_full_dict()
        data["payload"]["sections"].reverse()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            envelope_path = root / "envelope.json"
            request_path = root / "request.json"
            envelope_path.write_text(json.dumps(data), encoding="utf-8")
            request_path.write_text(
                json.dumps(request_dict()),
                encoding="utf-8",
            )
            output = io.StringIO()
            errors = io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                status = main(
                    [
                        "render",
                        str(envelope_path),
                        "--request",
                        str(request_path),
                    ]
                )
        self.assertEqual(status, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertIn('"mechanically_conformant": false', errors.getvalue())

    def test_render_diagnostics_do_not_echo_invalid_candidate_prose(self) -> None:
        """Name: Invalid-prose diagnostic redaction.

        Description: Repeats a private lexical unit across two views to trigger
        deterministic duplicate rejection.
        Assumptions: Failure diagnostics may identify the code and locations
        but are not a channel for uncertified response prose.
        Expectations: Stdout is empty and stderr omits the repeated phrase.
        """
        secret = "private candidate phrase."
        data = valid_full_dict()
        data["payload"]["sections"][0]["content"] = secret
        data["payload"]["sections"][1]["content"] = secret
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            envelope_path = root / "envelope.json"
            request_path = root / "request.json"
            envelope_path.write_text(json.dumps(data), encoding="utf-8")
            request_path.write_text(
                json.dumps(request_dict()),
                encoding="utf-8",
            )
            output = io.StringIO()
            errors = io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                status = main(
                    [
                        "render",
                        str(envelope_path),
                        "--request",
                        str(request_path),
                    ]
                )
        self.assertEqual(status, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertNotIn(secret.rstrip("."), errors.getvalue())

    def test_requestless_render_refuses_structural_only_candidate(self) -> None:
        """Name: Requestless render refusal.

        Description: Invokes render without trusted topic or policy metadata.
        Assumptions: Structural validity cannot certify focused/full selection.
        Expectations: Exit one withholds stdout and reports certifiable false.
        """
        with tempfile.TemporaryDirectory() as directory:
            envelope_path = Path(directory) / "envelope.json"
            envelope_path.write_text(
                json.dumps(valid_full_dict()),
                encoding="utf-8",
            )
            output = io.StringIO()
            errors = io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                status = main(["render", str(envelope_path)])

        self.assertEqual(status, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertIn('"certifiable": false', errors.getvalue())

    def test_optional_report_failure_preserves_committed_output(self) -> None:
        """Name: Optional report delivery failure.

        Description: Fails audit-report persistence after wrapper certification.
        Assumptions: The wrapper has already committed state before returning.
        Expectations: Canonical output still succeeds and stderr reports the loss.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_path = root / "request.json"
            request_path.write_text(
                json.dumps(request_dict()),
                encoding="utf-8",
            )
            report = mock.Mock()
            report.to_dict.return_value = {}
            result = SimpleNamespace(
                markdown="certified output\n",
                host="cursor",
                attempts=1,
                host_metadata={},
                report=report,
            )
            wrapper = mock.Mock()
            wrapper.run.return_value = result
            output = io.StringIO()
            errors = io.StringIO()
            with (
                mock.patch("pc_core.cli.CertifiedWrapper", return_value=wrapper),
                mock.patch(
                    "pc_core.cli.write_json_atomic",
                    side_effect=OSError("report unavailable"),
                ),
                redirect_stdout(output),
                redirect_stderr(errors),
            ):
                status = main(
                    [
                        "wrap",
                        "--host",
                        "cursor",
                        "--request",
                        str(request_path),
                        "--state",
                        str(root / "state.json"),
                        "--cwd",
                        str(root),
                        "--report",
                        str(root / "report.json"),
                    ]
                )

        self.assertEqual(status, 0)
        self.assertEqual(output.getvalue(), "certified output\n")
        self.assertIn("report write failed", errors.getvalue())

    def test_wrap_rejects_report_aliases_for_inputs_and_state(self) -> None:
        """Name: Audit input and state path isolation.

        Description: Supplies state, case-variant state, and request aliases for
        audit output.
        Assumptions: Reports must not replace trusted inputs or committed state,
        and case-insensitive volumes may alias differently cased names.
        Expectations: The CLI rejects every alias before host or wrapper
        invocation and preserves the request bytes.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_path = root / "request.json"
            request_path.write_text(
                json.dumps(request_dict()),
                encoding="utf-8",
            )
            request_bytes = request_path.read_bytes()
            shared_path = root / "state-and-report.json"
            report_paths = (
                shared_path,
                root / "STATE-AND-REPORT.JSON",
                request_path,
            )
            for report_path in report_paths:
                with self.subTest(report_path=report_path):
                    errors = io.StringIO()
                    with (
                        mock.patch("pc_core.cli.CertifiedWrapper") as wrapper,
                        redirect_stderr(errors),
                    ):
                        status = main(
                            [
                                "wrap",
                                "--host",
                                "cursor",
                                "--request",
                                str(request_path),
                                "--state",
                                str(shared_path),
                                "--cwd",
                                str(root),
                                "--report",
                                str(report_path),
                            ]
                        )

                    self.assertEqual(status, 2)
                    wrapper.assert_not_called()
                    self.assertFalse(shared_path.exists())
                    if report_path != request_path:
                        self.assertFalse(report_path.exists())
                    self.assertEqual(request_path.read_bytes(), request_bytes)
                    self.assertIn("different path", errors.getvalue())


class AdvisoryHookTests(unittest.TestCase):
    """Name: Cursor and Claude advisory hook behavior.

    Description: Verifies stateless visible-Markdown checks and each host's
    metadata-limited nonblocking boundaries, collision-safe Cursor handoff, one
    retry for visible empty views, and local runtime command.
    Assumptions: Invalid assistant output may already be displayed by the host,
    and hook commands run from the configured project root.
    Expectations: Hooks never claim certification and never exceed two total
    displayed attempts.
    """

    def test_rendered_markdown_check_never_certifies_structured_state(self) -> None:
        """Name: Hook certification boundary.

        Description: Validates visibly well-formed three-view Markdown.
        Assumptions: No trusted envelope or fact ledger accompanies display text.
        Expectations: Visible mechanics pass but certifiable remains false.
        """
        markdown = """## At a glance
Adopt Atlas.

## In context
Security owns approval.

## At depth
The pilot covered twelve million events.
"""
        report = validate_rendered_markdown(markdown)
        self.assertTrue(report.mechanically_conformant)
        self.assertFalse(report.certifiable)

    def test_focused_output_is_nonblocking_but_unverified(self) -> None:
        """Name: Focused advisory hook boundary.

        Description: Sends a heading-free focused response through visible checks.
        Assumptions: Hooks cannot know whether focused presentation was selected.
        Expectations: Output is nonblocking and remains mechanically uncertified.
        """
        text = valid_focused_dict()["payload"]["content"]
        report = validate_rendered_markdown(text)

        self.assertTrue(report.mechanically_conformant)
        self.assertFalse(report.certifiable)
        self.assertEqual(
            report.mechanical_checks["three_view_heading_order"],
            "UNVERIFIED",
        )
        self.assertEqual(
            claude_stop(
                {
                    "last_assistant_message": text,
                    "stop_hook_active": False,
                }
            ),
            {},
        )

    def test_fenced_protocol_heading_is_nonblocking(self) -> None:
        """Name: Fenced protocol-heading boundary.

        Description: Places a reserved heading inside a fenced code example.
        Assumptions: Fenced source text is not visible response structure.
        Expectations: Hook validation remains nonblocking and uncertified.
        """
        text = "Example:\n\n```\n## At a glance\n```\n"
        report = validate_rendered_markdown(text)

        self.assertTrue(report.mechanically_conformant)
        self.assertEqual(
            report.mechanical_checks["three_view_heading_order"],
            "UNVERIFIED",
        )

    def test_cursor_hook_does_not_retry_unverifiable_budget(self) -> None:
        """Name: Cursor advisory budget boundary.

        Description: Records a visibly over-budget response, then evaluates stop
        at loop counts zero and one.
        Assumptions: Visible Markdown cannot separate exempt warning or repair text.
        Expectations: Neither stop call requests a potentially destructive retry.
        """
        markdown = "## At a glance\n\n" + " ".join(
            f"word{index}" for index in range(41)
        )
        base = {
            "conversation_id": "conversation-1",
            "generation_id": "generation-1",
            "text": markdown,
        }
        with tempfile.TemporaryDirectory() as directory:
            state_dir = Path(directory)
            self.assertEqual(cursor_after_response(base, state_dir), {})
            first = cursor_stop(
                {**base, "status": "completed", "loop_count": 0},
                state_dir,
            )
            second = cursor_stop(
                {**base, "status": "completed", "loop_count": 1},
                state_dir,
            )
        self.assertEqual(first, {})
        self.assertEqual(second, {})

    def test_cursor_hook_ids_with_same_sanitized_text_do_not_collide(self) -> None:
        """Name: Collision-safe Cursor hook handoff.

        Description: Records valid and invalid reports under IDs that sanitize
        to the same readable text.
        Assumptions: Host identifiers may contain different punctuation.
        Expectations: Each stop event reads and removes only its matching report.
        """
        invalid_markdown = """## At a glance
One.

## In context

## At depth
Three.
"""
        valid_markdown = """## At a glance
One.

## In context
Two.

## At depth
Three.
"""
        invalid = {
            "conversation_id": "conversation/a",
            "generation_id": "generation-1",
            "text": invalid_markdown,
        }
        valid = {
            "conversation_id": "conversation?a",
            "generation_id": "generation-1",
            "text": valid_markdown,
        }
        with tempfile.TemporaryDirectory() as directory:
            state_dir = Path(directory)
            cursor_after_response(invalid, state_dir)
            cursor_after_response(valid, state_dir)
            invalid_stop = cursor_stop(
                {**invalid, "loop_count": 0},
                state_dir,
            )
            valid_stop = cursor_stop(
                {**valid, "loop_count": 0},
                state_dir,
            )
            report_count = len(list(state_dir.iterdir()))
        self.assertIn("followup_message", invalid_stop)
        self.assertEqual(valid_stop, {})
        self.assertEqual(report_count, 0)

    def test_claude_hook_does_not_block_unverifiable_budget(self) -> None:
        """Name: Claude advisory budget boundary.

        Description: Applies the same visibly over-budget output to initial and
        active
        Stop-hook calls.
        Assumptions: Stop hooks lack structured warning and correction metadata.
        Expectations: Neither call blocks or mutates potentially valid output.
        """
        markdown = "## At a glance\n\n" + " ".join(
            f"word{index}" for index in range(41)
        )
        first = claude_stop(
            {
                "last_assistant_message": markdown,
                "stop_hook_active": False,
            }
        )
        second = claude_stop(
            {
                "last_assistant_message": markdown,
                "stop_hook_active": True,
            }
        )
        self.assertEqual(first, {})
        self.assertEqual(second, {})

    def test_checked_in_templates_use_project_scoped_official_shapes(self) -> None:
        """Name: Host hook template schemas.

        Description: Parses the Cursor version-one hook map and Claude project
        settings Stop hook.
        Assumptions: Templates are copied or merged project-locally by users.
        Expectations: No user-global path or unsupported event is configured.
        """
        root = Path(__file__).resolve().parents[1]
        cursor = json.loads(
            (root / "adapters" / "cursor" / "hooks.json").read_text(
                encoding="utf-8"
            )
        )
        claude = json.loads(
            (root / "adapters" / "claude-code" / "settings.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(cursor["version"], 1)
        self.assertEqual(
            set(cursor["hooks"]),
            {"afterAgentResponse", "stop"},
        )
        self.assertEqual(set(claude["hooks"]), {"Stop"})
        self.assertEqual(
            claude["hooks"]["Stop"][0]["hooks"][0]["type"],
            "command",
        )
        self.assertTrue(
            cursor["hooks"]["afterAgentResponse"][0]["command"].startswith(
                ".pc-core/venv/bin/pc-core "
            )
        )
        self.assertEqual(cursor["hooks"]["stop"][0]["loop_limit"], 1)
        self.assertTrue(
            claude["hooks"]["Stop"][0]["hooks"][0]["command"].startswith(
                ".pc-core/venv/bin/pc-core "
            )
        )


if __name__ == "__main__":
    unittest.main()
