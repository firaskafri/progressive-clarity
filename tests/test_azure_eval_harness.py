"""Name: Agno Azure evaluation harness suite.

Description: Exercises configuration safety, case planning, deterministic
presentation scoring, turn-specific semantic judging, atomic checkpointing,
interruption preservation, and compatible resume without calling Azure OpenAI.
Assumptions: The current evaluation suite is frozen, mocked case executions are
representative of harness control flow, and live Agno imports occur only when a
configured execution begins.
Expectations: Dry runs remain dependency-free; checkpoints expose complete
identity and aggregate state; interrupted work resumes without duplicate calls;
and credentials never enter reports, errors, or captured model content.
"""

from __future__ import annotations

import copy
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

from pc_core.json_io import write_json_atomic as _write_json_atomic
from tools.azure_eval_harness import (
    AzureEvalConfig,
    HarnessError,
    _available_source_facts,
    _judge_prompt,
    deterministic_score,
    dry_run_summary,
    judge_criteria,
    load_local_config,
    load_resume_report,
    load_suite,
    main,
    parse_judge_result,
    parse_view_sections,
    run_suite,
    selected_cases,
)


def _test_config() -> AzureEvalConfig:
    """Return deterministic non-production configuration for harness tests."""
    return AzureEvalConfig(
        endpoint="https://checkpoint-resource.openai.azure.com",
        api_key="sentinel-test-api-key",
        deployment="gpt-test-deployment",
        api_version="2024-10-21",
    )


def _completed_record(
    case_id: str,
    run_number: int,
    *,
    raw_output: str = "synthetic output",
) -> dict[str, object]:
    """Return one minimal completed case-run record."""
    return {
        "case_id": case_id,
        "run_number": run_number,
        "session_id": f"{case_id}-run-{run_number}",
        "result": "PASS",
        "turns": [
            {
                "turn": 1,
                "raw_output": raw_output,
                "result": "PASS",
            }
        ],
    }


class AzureEvalHarnessTests(unittest.TestCase):
    """Name: Azure harness pure-contract tests.

    Description: Validates behavior available without network access or live
    Agno model construction, including durable reports and judge applicability.
    Assumptions: Tests read only the canonical suite, mock isolated case runs,
    and treat atomic JSON writes as the persistence boundary.
    Expectations: Planning, scoring, checkpoint status, resume compatibility,
    completed-run skipping, incomplete-run replay, and credential safety remain
    stable across successful and interrupted executions.
    """

    def test_complete_dry_run_matches_prescribed_totals(self) -> None:
        """Name: Complete suite planning.

        Description: Expands every case and required repetition.
        Assumptions: cases.json owns the canonical run counts.
        Expectations: Fourteen sessions and twenty-nine responses are planned.
        """
        suite = load_suite()
        summary = dry_run_summary(suite, selected_cases(suite, None))

        self.assertEqual(summary["sessions"], 14)
        self.assertEqual(summary["responses"], 29)
        self.assertEqual(
            summary["case_ids"],
            [f"T{index:02d}" for index in range(1, 11)],
        )

    def test_case_selection_preserves_order_and_rejects_unknown_ids(self) -> None:
        """Name: Selected case ordering.

        Description: Selects cases out of request order and requests one unknown.
        Assumptions: Canonical suite ordering makes reports comparable.
        Expectations: Known cases retain suite order and unknown IDs fail early.
        """
        suite = load_suite()

        chosen = selected_cases(suite, ["T03", "T01"])
        self.assertEqual([case["id"] for case in chosen], ["T01", "T03"])
        with self.assertRaisesRegex(HarnessError, "unknown case IDs"):
            selected_cases(suite, ["T99"])

    def test_configuration_requires_explicit_latest_deployment(self) -> None:
        """Name: Explicit Azure deployment.

        Description: Omits all Azure environment variables.
        Assumptions: Silent fallback could accidentally evaluate an older model.
        Expectations: Configuration fails and names the missing deployment input.
        """
        environment_names = (
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_EVAL_DEPLOYMENT",
            "AZURE_OPENAI_CHAT_DEPLOYMENT",
            "AZURE_OPENAI_DEPLOYMENT",
        )
        environment = {
            key: value
            for key, value in os.environ.items()
            if key not in environment_names
        }
        with mock.patch.dict(os.environ, environment, clear=True):
            with self.assertRaisesRegex(HarnessError, "deployment"):
                AzureEvalConfig.from_environment()

    def test_public_metadata_never_contains_api_key(self) -> None:
        """Name: Credential-safe result metadata.

        Description: Builds a valid configuration containing a sentinel secret.
        Assumptions: Reports need deployment identity but never credentials.
        Expectations: Public metadata omits both the key and complete endpoint.
        """
        config = AzureEvalConfig(
            endpoint="https://example-resource.openai.azure.com",
            api_key="sentinel-secret",
            deployment="latest-eval",
            api_version="2024-10-21",
        )

        metadata = config.public_metadata()
        self.assertNotIn("sentinel-secret", repr(metadata))
        self.assertNotIn("api_key", metadata)
        self.assertEqual(metadata["endpoint_host"], "example-resource.openai.azure.com")

    def test_ignored_local_config_supplies_required_values(self) -> None:
        """Name: Ignored local Azure configuration.

        Description: Loads four top-level values and constructs configuration.
        Assumptions: Real credentials live only in a Git-ignored JSON file.
        Expectations: Local values satisfy configuration without entering reports.
        """
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "azure.local.json"
            path.write_text(
                """{
  "endpoint": "https://example-resource.openai.azure.com",
  "api_key": "local-secret",
  "deployment": "latest-eval",
  "api_version": "2024-10-21"
}
""",
                encoding="utf-8",
            )
            local = load_local_config(path)
        with mock.patch.dict(os.environ, {}, clear=True):
            config = AzureEvalConfig.from_environment(local_config=local)

        self.assertEqual(config.deployment, "latest-eval")
        self.assertNotIn("local-secret", repr(config.public_metadata()))

    def test_checkpoint_exists_before_first_case_execution(self) -> None:
        """Name: Startup checkpoint creation.

        Description: Observes the report from inside the first mocked case run.
        Assumptions: The report path is the durable boundary available to resume.
        Expectations: A RUNNING report already contains suite identity, protocol
        hash, model identity, selected cases, and an empty aggregate.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T01"])
        config = _test_config()
        observed: list[dict[str, object]] = []
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"

            def execute_case(**kwargs: object) -> dict[str, object]:
                observed.append(load_resume_report(output))
                return _completed_record(
                    str(kwargs["case"]["id"]),  # type: ignore[index]
                    int(kwargs["run_number"]),
                )

            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=execute_case,
                ),
            ):
                report = run_suite(
                    suite=suite,
                    cases=cases,
                    config=config,
                    skill_body="skill",
                    judge_enabled=True,
                    output_path=output,
                )

        startup = observed[0]
        self.assertEqual(startup["status"], "RUNNING")
        self.assertEqual(startup["runs"], [])
        self.assertEqual(startup["selected_case_ids"], ["T01"])
        self.assertRegex(str(startup["suite_sha256"]), r"^[a-f0-9]{64}$")
        self.assertEqual(startup["protocol_sha256"], suite["protocol"]["sha256"])
        self.assertRegex(str(startup["skill_body_sha256"]), r"^[a-f0-9]{64}$")
        self.assertEqual(startup["model"]["deployment"], config.deployment)
        self.assertEqual(startup["model"]["api_version"], config.api_version)
        self.assertEqual(startup["aggregate"]["completed_runs"], 0)
        self.assertEqual(report["status"], "COMPLETE")

    def test_checkpoint_updates_after_every_completed_case_run(self) -> None:
        """Name: Per-run checkpoint updates.

        Description: Reads the durable checkpoint before each of three case runs.
        Assumptions: T04 prescribes three isolated runs in canonical order.
        Expectations: Each next run sees all prior completed runs persisted, and
        the final report contains all three completion keys.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T04"])
        observed_completed_counts: list[int] = []
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"

            def execute_case(**kwargs: object) -> dict[str, object]:
                checkpoint = load_resume_report(output)
                observed_completed_counts.append(
                    int(
                        checkpoint["aggregate"]["completed_runs"]  # type: ignore[index]
                    )
                )
                case = kwargs["case"]
                return _completed_record(
                    str(case["id"]),  # type: ignore[index]
                    int(kwargs["run_number"]),
                )

            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=execute_case,
                ),
            ):
                report = run_suite(
                    suite=suite,
                    cases=cases,
                    config=_test_config(),
                    skill_body="skill",
                    judge_enabled=True,
                    output_path=output,
                )

        self.assertEqual(observed_completed_counts, [0, 1, 2])
        self.assertEqual(
            report["completed_case_run_keys"],
            ["T04/run-1", "T04/run-2", "T04/run-3"],
        )
        self.assertEqual(report["aggregate"]["completed_runs"], 3)

    def test_keyboard_interrupt_preserves_completed_runs(self) -> None:
        """Name: Interrupted report preservation.

        Description: Interrupts T04 while its second prescribed run is active.
        Assumptions: A run is complete only after run_case returns a full record.
        Expectations: Run one remains durable, run two is absent, status becomes
        INTERRUPTED, and the aggregate cannot claim a complete PASS.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T04"])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=[
                        _completed_record("T04", 1),
                        KeyboardInterrupt(),
                    ],
                ),
            ):
                with self.assertRaises(KeyboardInterrupt):
                    run_suite(
                        suite=suite,
                        cases=cases,
                        config=_test_config(),
                        skill_body="skill",
                        judge_enabled=True,
                        output_path=output,
                    )
            checkpoint = load_resume_report(output)

        self.assertEqual(checkpoint["status"], "INTERRUPTED")
        self.assertEqual(checkpoint["completed_case_run_keys"], ["T04/run-1"])
        self.assertEqual(checkpoint["aggregate"]["completed_runs"], 1)
        self.assertEqual(checkpoint["aggregate"]["remaining_runs"], 2)
        self.assertEqual(checkpoint["overall"], "UNVERIFIED")

    def test_compatible_resume_reaches_complete_status(self) -> None:
        """Name: Compatible checkpoint resume.

        Description: Resumes a T01 report interrupted before its only case run.
        Assumptions: Suite, protocol, Skill body, deployment, API version, judge
        mode, and selected cases are unchanged between invocations.
        Expectations: The report transitions through INTERRUPTED and RUNNING to
        COMPLETE, increments resume_count, and records the replayed run once.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T01"])
        config = _test_config()
        snapshots: list[dict[str, object]] = []

        def capture_checkpoint(path: Path, value: object) -> None:
            snapshots.append(copy.deepcopy(value))  # type: ignore[arg-type]
            _write_json_atomic(path, value)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness.write_json_atomic",
                    side_effect=capture_checkpoint,
                ),
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
            ):
                with mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=KeyboardInterrupt(),
                ):
                    with self.assertRaises(KeyboardInterrupt):
                        run_suite(
                            suite=suite,
                            cases=cases,
                            config=config,
                            skill_body="skill",
                            judge_enabled=True,
                            output_path=output,
                        )
                interrupted = load_resume_report(output)
                with mock.patch(
                    "tools.azure_eval_harness.run_case",
                    return_value=_completed_record("T01", 1),
                ):
                    report = run_suite(
                        suite=suite,
                        cases=cases,
                        config=config,
                        skill_body="skill",
                        judge_enabled=True,
                        output_path=output,
                        resume_report=interrupted,
                    )

        self.assertEqual(
            [snapshot["status"] for snapshot in snapshots],
            ["RUNNING", "INTERRUPTED", "RUNNING", "RUNNING", "COMPLETE"],
        )
        self.assertEqual(report["status"], "COMPLETE")
        self.assertEqual(report["resume_count"], 1)
        self.assertEqual(report["completed_case_run_keys"], ["T01/run-1"])

    def test_incompatible_resume_reports_are_refused(self) -> None:
        """Name: Resume compatibility refusal.

        Description: Alters each identity dimension required for safe resumption.
        Assumptions: Completed response evidence is meaningful only under the
        exact suite, protocol, deployment, API, judge mode, and case selection.
        Expectations: Every incompatible variant fails before a checkpoint write
        or model/session construction.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T01"])
        config = _test_config()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    return_value=_completed_record("T01", 1),
                ),
            ):
                base = run_suite(
                    suite=suite,
                    cases=cases,
                    config=config,
                    skill_body="skill",
                    judge_enabled=True,
                    output_path=output,
                )

            variants: list[tuple[str, dict[str, object]]] = []
            variant = copy.deepcopy(base)
            variant["suite_id"] = "different-suite"
            variants.append(("suite ID", variant))
            variant = copy.deepcopy(base)
            variant["suite_sha256"] = "1" * 64
            variants.append(("suite hash", variant))
            variant = copy.deepcopy(base)
            variant["protocol_sha256"] = "0" * 64
            variants.append(("protocol hash", variant))
            variant = copy.deepcopy(base)
            variant["skill_body_sha256"] = "2" * 64
            variants.append(("Skill body hash", variant))
            variant = copy.deepcopy(base)
            variant["model"]["deployment"] = (  # type: ignore[index]
                "different-deployment"
            )
            variants.append(("deployment", variant))
            variant = copy.deepcopy(base)
            variant["model"]["api_version"] = (  # type: ignore[index]
                "different-version"
            )
            variants.append(("API version", variant))
            variant = copy.deepcopy(base)
            variant["judge"]["enabled"] = False  # type: ignore[index]
            variants.append(("judge mode", variant))
            variant = copy.deepcopy(base)
            variant["selected_case_ids"] = ["T02"]
            variants.append(("selected cases", variant))

            for label, incompatible in variants:
                with self.subTest(label=label):
                    with self.assertRaisesRegex(
                        HarnessError,
                        "incompatible resume report",
                    ):
                        run_suite(
                            suite=suite,
                            cases=cases,
                            config=config,
                            skill_body="skill",
                            judge_enabled=True,
                            output_path=output,
                            resume_report=incompatible,
                        )

    def test_resume_skips_every_completed_case_run(self) -> None:
        """Name: Completed-run skipping.

        Description: Resumes T04 after run one completed and run two interrupted.
        Assumptions: Completion keys are validated against canonical planned order.
        Expectations: The resumed invocation never calls run one again and runs
        only the remaining run numbers two and three.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T04"])
        config = _test_config()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=[
                        _completed_record("T04", 1),
                        KeyboardInterrupt(),
                    ],
                ),
            ):
                with self.assertRaises(KeyboardInterrupt):
                    run_suite(
                        suite=suite,
                        cases=cases,
                        config=config,
                        skill_body="skill",
                        judge_enabled=True,
                        output_path=output,
                    )
            interrupted = load_resume_report(output)
            called_runs: list[int] = []

            def execute_remaining(**kwargs: object) -> dict[str, object]:
                run_number = int(kwargs["run_number"])
                called_runs.append(run_number)
                return _completed_record("T04", run_number)

            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=execute_remaining,
                ),
            ):
                report = run_suite(
                    suite=suite,
                    cases=cases,
                    config=config,
                    skill_body="skill",
                    judge_enabled=True,
                    output_path=output,
                    resume_report=interrupted,
                )

        self.assertEqual(called_runs, [2, 3])
        self.assertEqual(report["aggregate"]["completed_runs"], 3)

    def test_resume_replays_the_interrupted_incomplete_run(self) -> None:
        """Name: Incomplete-run replay.

        Description: Interrupts the sole T01 run before it returns any record.
        Assumptions: In-progress turn fragments are never checkpointed as complete.
        Expectations: Resume executes T01 run one exactly once and produces one
        completed record rather than skipping the absent run.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T01"])
        config = _test_config()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=KeyboardInterrupt(),
                ),
            ):
                with self.assertRaises(KeyboardInterrupt):
                    run_suite(
                        suite=suite,
                        cases=cases,
                        config=config,
                        skill_body="skill",
                        judge_enabled=True,
                        output_path=output,
                    )
            interrupted = load_resume_report(output)
            called_runs: list[int] = []

            def replay_case(**kwargs: object) -> dict[str, object]:
                run_number = int(kwargs["run_number"])
                called_runs.append(run_number)
                return _completed_record("T01", run_number)

            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=replay_case,
                ),
            ):
                report = run_suite(
                    suite=suite,
                    cases=cases,
                    config=config,
                    skill_body="skill",
                    judge_enabled=True,
                    output_path=output,
                    resume_report=interrupted,
                )

        self.assertEqual(called_runs, [1])
        self.assertEqual(report["completed_case_run_keys"], ["T01/run-1"])

    def test_checkpoints_redact_credentials_from_outputs_and_errors(self) -> None:
        """Name: Whole-report credential absence.

        Description: Places sentinel credentials in one mocked raw output and one
        exception message while running all three T04 repetitions.
        Assumptions: Exact configured secrets must be removed even from unexpected
        model content or transport exceptions before atomic persistence.
        Expectations: Neither API key nor full endpoint appears in the report or
        returned object, while ordinary endpoint-host metadata remains available.
        """
        suite = load_suite()
        cases = selected_cases(suite, ["T04"])
        config = _test_config()
        leaked_text = f"{config.api_key} {config.endpoint}"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness._build_session_db",
                    return_value=object(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_case",
                    side_effect=[
                        _completed_record("T04", 1, raw_output=leaked_text),
                        RuntimeError(leaked_text),
                        _completed_record("T04", 3),
                    ],
                ),
            ):
                report = run_suite(
                    suite=suite,
                    cases=cases,
                    config=config,
                    skill_body="skill",
                    judge_enabled=True,
                    output_path=output,
                )
            persisted = output.read_text(encoding="utf-8")

        self.assertNotIn(config.api_key, persisted)
        self.assertNotIn(config.endpoint, persisted)
        self.assertNotIn(config.api_key, repr(report))
        self.assertNotIn(config.endpoint, repr(report))
        self.assertIn("[REDACTED]", persisted)
        self.assertEqual(
            report["model"]["endpoint_host"],
            "checkpoint-resource.openai.azure.com",
        )

    def test_main_returns_130_for_keyboard_interrupt(self) -> None:
        """Name: Interrupted command exit status.

        Description: Interrupts execution at the suite runner boundary.
        Assumptions: run_suite owns checkpoint preservation before re-raising.
        Expectations: The command reports interruption without exception details
        and exits with the conventional status code 130.
        """
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checkpoint.json"
            missing_config = Path(directory) / "missing-local-config.json"
            with (
                mock.patch(
                    "tools.azure_eval_harness.DEFAULT_LOCAL_CONFIG_PATH",
                    missing_config,
                ),
                mock.patch.object(
                    AzureEvalConfig,
                    "from_environment",
                    return_value=_test_config(),
                ),
                mock.patch(
                    "tools.azure_eval_harness.load_skill_body",
                    return_value="skill",
                ),
                mock.patch(
                    "tools.azure_eval_harness.run_suite",
                    side_effect=KeyboardInterrupt(),
                ),
                redirect_stderr(io.StringIO()) as stderr,
            ):
                exit_code = main(["--case", "T01", "--output", str(output)])

        self.assertEqual(exit_code, 130)
        self.assertIn("interrupted", stderr.getvalue())

    def test_deterministic_full_scoring_checks_headings_and_budgets(self) -> None:
        """Name: Full deterministic scoring.

        Description: Scores one valid Full response and one over-budget variant.
        Assumptions: T02 turn two requires exactly the canonical three headings.
        Expectations: Valid structure passes and a forty-one-word glance fails.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T02")
        turn = case["turns"][1]
        valid = """## At a glance
Hold the release until reliability passes.

## In context
The gate converts evidence into a release decision.

## At depth
Inspect the failed metric and rollback readiness.
"""
        valid_score = deterministic_score(case=case, turn=turn, response=valid)
        self.assertEqual(valid_score["result"], "PASS")

        words = " ".join(f"word{index}" for index in range(41))
        invalid = valid.replace("Hold the release until reliability passes.", words)
        invalid_score = deterministic_score(case=case, turn=turn, response=invalid)
        self.assertEqual(invalid_score["result"], "FAIL")
        self.assertEqual(
            invalid_score["checks"]["at_a_glance_budget"]["result"],
            "FAIL",
        )

    def test_deterministic_numeric_template_requires_both_ordered_labels(self) -> None:
        """Name: Numeric-template deterministic scoring.

        Description: Scores one exact missing-input template and one bare
        clarification question for T01's idempotency TTL turn.
        Assumptions: The expected prohibition explicitly invokes both literal
        numeric-template labels and their governing-input-first order.
        Expectations: Ordered labeled lines pass while an unlabeled question
        fails the deterministic numeric-template check.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T01")
        turn = case["turns"][2]
        valid = (
            "Governing input: the provider retry window.\n\n"
            "Example assumption: 14 days if retries end within 7 days."
        )
        invalid = "What is the provider retry window?"

        valid_score = deterministic_score(
            case=case,
            turn=turn,
            response=valid,
        )
        invalid_score = deterministic_score(
            case=case,
            turn=turn,
            response=invalid,
        )

        self.assertEqual(
            valid_score["checks"]["numeric_template_labels"]["result"],
            "PASS",
        )
        self.assertEqual(invalid_score["result"], "FAIL")
        self.assertEqual(
            invalid_score["checks"]["numeric_template_labels"]["result"],
            "FAIL",
        )

    def test_warning_budgets_remain_unverified_without_structured_accounting(
        self,
    ) -> None:
        """Name: Warning-budget exception boundary.

        Description: Scores a T05 Full warning whose At-a-glance prose exceeds
        the ordinary forty-word cap.
        Assumptions: The protocol exempts only necessary warning prose, while the
        raw Markdown scorer cannot separate warning and ordinary words.
        Expectations: Structure still passes, both affected budgets remain
        UNVERIFIED rather than FAIL, and semantic warning scoring decides the turn.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T05")
        turn = case["turns"][0]
        warning = " ".join(f"warning{index}" for index in range(42))
        response = f"""## At a glance
{warning}

## In context
Preserve evidence.

## At depth
Inspect divergent transactions.
"""

        score = deterministic_score(
            case=case,
            turn=turn,
            response=response,
        )

        self.assertEqual(score["result"], "PASS")
        self.assertEqual(
            score["checks"]["at_a_glance_budget"]["result"],
            "UNVERIFIED",
        )
        self.assertEqual(
            score["checks"]["through_in_context_budget"]["result"],
            "UNVERIFIED",
        )

    def test_full_correction_contract_is_scored_inside_at_a_glance(self) -> None:
        """Name: Full correction contract placement.

        Description: Places the T04 material-repair contract inside At a glance
        and compares the same contract deferred to In context.
        Assumptions: Full corrections begin with a heading, so response-byte
        prefix checks cannot represent the protocol's repair placement.
        Expectations: An At-a-glance repair passes while a deferred repair fails.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T04")
        turn = case["turns"][2]
        valid = """## At a glance
Earlier I said production coverage is Tuesday. That was wrong or incomplete.
Production coverage moves to Thursday. This changes the staffing plan.

## In context
Update the coverage calendar.

## At depth
Confirm Thursday staffing.
"""
        invalid = """## At a glance
Production coverage moves to Thursday.

## In context
Earlier I said production coverage is Tuesday. That was wrong or incomplete.
Production coverage moves to Thursday. This changes the staffing plan.

## At depth
Confirm Thursday staffing.
"""

        valid_score = deterministic_score(
            case=case,
            turn=turn,
            response=valid,
        )
        invalid_score = deterministic_score(
            case=case,
            turn=turn,
            response=invalid,
        )

        self.assertEqual(valid_score["checks"]["repair_contract"]["result"], "PASS")
        self.assertEqual(
            invalid_score["checks"]["repair_contract"]["result"],
            "FAIL",
        )

    def test_focused_scoring_ignores_fenced_protocol_headings(self) -> None:
        """Name: Focused fenced-heading boundary.

        Description: Places a reserved heading inside a code fence.
        Assumptions: Literal examples do not create rendered protocol sections.
        Expectations: No reserved headings are reported outside the fence.
        """
        headings, sections = parse_view_sections(
            "Example:\n\n```\n## At depth\nnot a view\n```\n"
        )

        self.assertEqual(headings, [])
        self.assertEqual(sections, {})

    def test_judge_contract_rejects_unstructured_results(self) -> None:
        """Name: Semantic judge result contract.

        Description: Parses one valid judge object, one incomplete result, and
        one result whose overall value contradicts its finding.
        Assumptions: Semantic judgment must remain machine-readable and auditable.
        Expectations: Exact consistent shape passes while missing or conflicting
        findings fail closed.
        """
        valid = {
            "overall": "PASS",
            "findings": [
                {
                    "criterion": "accuracy",
                    "result": "PASS",
                    "evidence": "No unsupported claims.",
                    "explanation": "The response remains within supplied facts.",
                }
            ],
            "notes": "",
        }
        self.assertEqual(parse_judge_result(valid), valid)
        with self.assertRaisesRegex(HarnessError, "overall, findings, and notes"):
            parse_judge_result({"overall": "PASS", "notes": ""})
        contradictory = copy.deepcopy(valid)
        contradictory["findings"][0]["result"] = "FAIL"
        with self.assertRaisesRegex(HarnessError, "conflicts with its findings"):
            parse_judge_result(contradictory)

    def test_judge_criteria_omit_warning_rules_from_corrections(self) -> None:
        """Name: Correction-only judge applicability.

        Description: Builds criteria for the narrow T04 correction turn.
        Assumptions: Correction expectations do not imply a material safety warning.
        Expectations: The literal repair criterion is present while warning
        completeness and placement are not requested from the semantic judge.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T04")
        criteria = judge_criteria(case=case, turn=case["turns"][1])
        criterion_ids = [criterion["id"] for criterion in criteria]
        correction = next(
            criterion
            for criterion in criteria
            if criterion["id"] == "correction_repair_contract"
        )

        self.assertIn("correction_repair_contract", criterion_ids)
        self.assertNotIn("warning_completeness_and_placement", criterion_ids)
        self.assertNotIn(
            "The correct information is",
            correction["requirement"],
        )
        self.assertNotIn("required_prefix", correction)

    def test_judge_prompt_includes_prior_conversation_for_corrections(self) -> None:
        """Name: Correction conversation evidence.

        Description: Builds the T04 narrow-correction judge prompt with the
        actual prior prompt and assistant response.
        Assumptions: A correction can withdraw a proposition from a combined
        earlier sentence, so static canonical prefixes are insufficient.
        Expectations: The judge receives the exact prior response separately
        from the current response and no static required prefix.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T04")
        history = [
            {
                "turn": 1,
                "prompt": case["turns"][0]["prompt"],
                "assistant_response": (
                    "Both the review and production coverage are scheduled "
                    "for Tuesday."
                ),
            }
        ]
        prompt = _judge_prompt(
            suite=suite,
            case=case,
            turn=case["turns"][1],
            response=(
                "Earlier I said the review is Tuesday. That was wrong or "
                "incomplete. The review is Wednesday. This changes the review day."
            ),
            conversation_history=history,
        )
        payload = json.loads(prompt.split("\n\n", 1)[1])
        correction = next(
            criterion
            for criterion in payload["criteria"]
            if criterion["id"] == "correction_repair_contract"
        )

        self.assertEqual(payload["conversation_history"], history)
        self.assertNotIn("required_prefix", correction)

    def test_judge_criteria_omit_correction_rules_from_warnings(self) -> None:
        """Name: Warning-only judge applicability.

        Description: Builds criteria for the material T05 warning turn.
        Assumptions: Warning expectations do not imply a prior emitted correction.
        Expectations: Warning completeness and placement are present while the
        literal correction repair contract is not requested.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T05")
        criteria = judge_criteria(case=case, turn=case["turns"][0])
        criterion_ids = [criterion["id"] for criterion in criteria]

        self.assertIn("warning_completeness_and_placement", criterion_ids)
        self.assertNotIn("correction_repair_contract", criterion_ids)

    def test_accuracy_criterion_does_not_treat_facts_as_closed_world(self) -> None:
        """Name: Open-world accuracy criterion.

        Description: Inspects the universal accuracy requirement for a simple fact.
        Assumptions: Case facts are required anchors but do not enumerate every
        generally valid domain explanation or recommendation the model may use.
        Expectations: The judge is told to permit non-contradictory domain detail
        while still rejecting fabricated case-specific state and measurements.
        """
        suite = load_suite()
        case = next(case for case in suite["cases"] if case["id"] == "T01")
        criteria = judge_criteria(case=case, turn=case["turns"][0])
        accuracy = next(
            criterion["requirement"]
            for criterion in criteria
            if criterion["id"] == "accuracy"
        )

        self.assertIn("not an exhaustive closed-world", accuracy)
        self.assertIn("fabricated case-specific", accuracy)

    def test_judge_criteria_follow_turn_presentation_and_contracts(self) -> None:
        """Name: Turn-specific semantic criterion set.

        Description: Samples focused, numeric, full, clarification, controlling,
        narrative, and procedure turns from the canonical suite.
        Assumptions: Presentation and explicit expected fields determine semantic
        applicability without inheriting criteria from unrelated protocol paths.
        Expectations: Every turn receives the three universal criteria plus only
        its focused, full, or purpose-specific additions.
        """
        suite = load_suite()
        cases = {case["id"]: case for case in suite["cases"]}

        def ids(case_id: str, turn_index: int) -> list[object]:
            case = cases[case_id]
            return [
                criterion["id"]
                for criterion in judge_criteria(
                    case=case,
                    turn=case["turns"][turn_index],
                )
            ]

        universal = ["accuracy", "required_facts", "prohibited_behaviors"]
        focused = ids("T01", 0)
        numeric = ids("T01", 2)
        full = ids("T01", 1)
        clarification = ids("T06", 0)
        controlling = ids("T07", 0)
        narrative = ids("T08", 0)
        procedure = ids("T09", 0)

        self.assertEqual(focused[:3], universal)
        self.assertIn("focused_proportionality", focused)
        self.assertIn("simple_fact_scope", focused)
        self.assertNotIn("numeric_template", focused)
        self.assertIn("numeric_template", numeric)
        self.assertIn("full_progressive_depth", full)
        self.assertIn("full_no_complete_repetition", full)
        self.assertIn("full_no_at_depth_recap", full)
        self.assertIn("clarification_gate", clarification)
        self.assertIn("controlling_text_contract", controlling)
        self.assertNotIn("purpose_specific_structure", controlling)
        self.assertIn("purpose_specific_structure", narrative)
        self.assertIn("purpose_specific_structure", procedure)

    def test_judge_receives_no_future_turn_source_facts(self) -> None:
        """Name: Turn-local semantic-judge facts.

        Description: Collects visible facts for T03's initial Saturday plan and
        T04's narrow Wednesday correction.
        Assumptions: Later correction facts are unavailable until their own
        prompts and must not retroactively contradict earlier responses.
        Expectations: Each fact set includes prior/current required IDs while
        excluding Sunday and Thursday facts introduced by future turns.
        """
        suite = load_suite()
        cases = {case["id"]: case for case in suite["cases"]}

        t03 = cases["T03"]
        t03_ids = {
            fact["id"]
            for fact in _available_source_facts(t03, t03["turns"][0])
        }
        t04 = cases["T04"]
        t04_ids = {
            fact["id"]
            for fact in _available_source_facts(t04, t04["turns"][1])
        }

        self.assertEqual(
            t03_ids,
            {f"T03-F{index}" for index in range(1, 7)},
        )
        self.assertNotIn("T03-F7", t03_ids)
        self.assertEqual(t04_ids, {"T04-F1", "T04-F2", "T04-F4"})
        self.assertNotIn("T04-F3", t04_ids)

    def test_judge_contract_rejects_unrequested_criteria(self) -> None:
        """Name: Semantic judge criterion boundary.

        Description: Parses a structured finding whose criterion was not requested.
        Assumptions: Prompt scoping alone cannot guarantee same-model compliance.
        Expectations: An extra warning criterion makes the judge result unavailable
        instead of allowing an irrelevant score into the case outcome.
        """
        result = {
            "overall": "PASS",
            "findings": [
                {
                    "criterion": "warning_completeness_and_placement",
                    "result": "PASS",
                    "evidence": "",
                    "explanation": "Irrelevant warning score.",
                }
            ],
            "notes": "",
        }

        with self.assertRaisesRegex(HarnessError, "requested criteria"):
            parse_judge_result(result, expected_criteria=["accuracy"])


if __name__ == "__main__":
    unittest.main()
