"""Name: CLI and advisory-hook integration suite.

Description: Exercises validate/render process behavior, stdout withholding,
diagnostic redaction, Cursor response-to-stop handoff, Claude one-retry
decisions, and checked-in project template schemas.
Assumptions: Hook APIs cannot establish the trusted structured state available
to the non-streaming wrapper.
Expectations: CLI render is fail closed; hooks label themselves non-certifying
and request no more than one retry.
"""

from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from pc_core.cli import main
from pc_core.hooks import claude_stop, cursor_after_response, cursor_stop
from pc_core.validation import validate_rendered_markdown
from tests.helpers import request_dict, valid_verbose_dict


class ValidateRenderCliTests(unittest.TestCase):
    """Name: Validate and render command behavior.

    Description: Runs CLI handlers with temporary trusted request and candidate
    files for passing and failing scenarios, including invalid candidate prose
    that must not escape through diagnostics.
    Assumptions: Initial state is used when no state file is supplied.
    Expectations: Reports are machine-readable and invalid output is withheld.
    """

    def test_validate_prints_separated_mechanical_and_advisory_status(self) -> None:
        """Name: Validate report boundary.

        Description: Validates a complete ordinary v0.2 candidate.
        Assumptions: Request and envelope identify the same new topic.
        Expectations: Exit zero reports mechanical certification and semantic
        UNVERIFIED status separately.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            envelope_path = root / "envelope.json"
            request_path = root / "request.json"
            envelope_path.write_text(
                json.dumps(valid_verbose_dict()),
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
                json.dumps(valid_verbose_dict()),
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
        data = copy.deepcopy(valid_verbose_dict())
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
        data = copy.deepcopy(valid_verbose_dict())
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


class AdvisoryHookTests(unittest.TestCase):
    """Name: Cursor and Claude advisory hook behavior.

    Description: Verifies stateless visible-Markdown checks and each host's
    documented one-retry response shape plus the project-local runtime command.
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

    def test_cursor_hook_requests_only_one_retry(self) -> None:
        """Name: Cursor advisory retry bound.

        Description: Records an over-budget response, then evaluates stop input
        at loop counts zero and one.
        Assumptions: afterAgentResponse runs before stop with matching IDs.
        Expectations: The first stop auto-follows up and the second does not.
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
        self.assertIn("followup_message", first)
        self.assertIn("PC-M-BUDGET-005", first["followup_message"])
        self.assertEqual(second, {})

    def test_claude_hook_blocks_once_then_labels_failure(self) -> None:
        """Name: Claude Stop retry bound.

        Description: Applies the same over-budget output to initial and active
        Stop-hook calls.
        Assumptions: stop_hook_active marks continuation caused by the first
        block.
        Expectations: Initial output gets decision=block; second gets a visible
        non-certification message without another retry.
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
        self.assertEqual(first["decision"], "block")
        self.assertIn("PC-M-BUDGET-005", first["reason"])
        self.assertIn("systemMessage", second)
        self.assertNotIn("decision", second)

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
