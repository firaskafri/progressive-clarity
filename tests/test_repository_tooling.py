"""Name: Repository tooling and Python package contract suite.

Description: Exercises importable repository validation, ordered test
docstrings, malformed container reporting, coordinated v0.4.3 metadata, frozen
protocol/evaluation identities, and exact host-template schemas.
Assumptions: Validation helpers are invoked as the tools package from the
repository root; wheel installation is covered by the CI integration smoke.
Expectations: Metadata and hook drift fail locally before packaging or host use.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import validate_repository
from tools.validate_repository import (
    test_docstring_problem,
    validate_distributions,
    validate_evaluation_suite,
    validate_host_templates,
    validate_python_package,
    validate_relative_links,
)


class RepositoryToolingTests(unittest.TestCase):
    """Name: Validator import and contract checks.

    Description: Verifies the validator as an importable module and probes
    ordered docstrings, malformed container types, package and word-count
    metadata, and nested hook-schema boundaries.
    Assumptions: Checked-in files are the canonical integration inputs.
    Expectations: Valid contracts produce no errors and metadata drift fails.
    """

    def test_docstring_contract_requires_exact_field_order(self) -> None:
        """Name: Ordered four-field docstring contract.

        Description: Compares one valid docstring with the same fields in the
        wrong order.
        Assumptions: Each field label must appear exactly once at line start.
        Expectations: The ordered form passes and the reordered form reports
        an ordering problem.
        """
        ordered = """Name: Case.

Description: Scenario.
Assumptions: Inputs.
Expectations: Result.
"""
        reordered = """Name: Case.

Assumptions: Inputs.
Description: Scenario.
Expectations: Result.
"""
        self.assertIsNone(test_docstring_problem(ordered))
        self.assertIn("order", test_docstring_problem(reordered))

    def test_python_package_metadata_matches_local_runtime_contract(self) -> None:
        """Name: Installable pc-core metadata.

        Description: Runs repository validation over pyproject package name,
        version, Python floor, dependency list, console script, and wheel scope.
        Assumptions: pc-core has no runtime dependency outside Python 3.11.
        Expectations: The checked-in local-install metadata produces no errors.
        """
        errors: list[str] = []
        validate_python_package(errors)
        self.assertEqual(errors, [])

    def test_distribution_versions_match_v04_release_candidate(self) -> None:
        """Name: Cross-surface v0.4.3 release-candidate versions.

        Description: Validates OpenAI, Claude plugin, and Claude.ai Skill versions.
        Assumptions: Protocol 0.4 changes every coordinated prompt package.
        Expectations: All package channels report coordinated version 0.4.3.
        """
        errors: list[str] = []
        validate_distributions(errors)
        self.assertEqual(errors, [])

    def test_evaluation_word_count_metadata_matches_core(self) -> None:
        """Name: Exact evaluation word-count metadata.

        Description: Mutates the algorithm identifier and At-a-glance budget in
        otherwise complete evaluation suites.
        Assumptions: Evaluation metadata must remain synchronized with pc-core.
        Expectations: Each drift produces its dedicated repository error.
        """
        source = json.loads(
            (
                validate_repository.ROOT
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        mutations = (
            (
                lambda suite: suite["word_count"].update(
                    {"method": f"{suite['word_count']['method']}-drift"}
                ),
                "word_count method",
            ),
            (
                lambda suite: suite["word_count"]["full_budgets"].update(
                    {"at_a_glance_max_non_warning_words": 41}
                ),
                "full_budgets",
            ),
        )
        for mutate, expected in mutations:
            with self.subTest(expected=expected):
                suite = json.loads(json.dumps(source))
                mutate(suite)
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    (root / "evals").mkdir()
                    (root / "evals" / "cases.json").write_text(
                        json.dumps(suite),
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    with mock.patch.object(validate_repository, "ROOT", root):
                        validate_evaluation_suite(errors)
                self.assertTrue(
                    any(expected in error for error in errors),
                    errors,
                )

    def test_wrong_container_types_are_reported_without_crashing(self) -> None:
        """Name: Validator container-type resilience.

        Description: Supplies a list-root evaluation suite and scalar Hatch data.
        Assumptions: Repository drift can remain syntactically valid JSON or TOML.
        Expectations: Both validators append actionable errors and return.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evals").mkdir()
            (root / "evals" / "cases.json").write_text(
                "[]\n",
                encoding="utf-8",
            )
            evaluation_errors: list[str] = []
            with mock.patch.object(validate_repository, "ROOT", root):
                validate_evaluation_suite(evaluation_errors)

            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                '[project]\nname = "progressive-clarity-core"\n'
                '[tool]\nhatch = "invalid"\n',
                encoding="utf-8",
            )
            package_errors: list[str] = []
            with mock.patch.object(
                validate_repository,
                "PYPROJECT_PATH",
                pyproject,
            ):
                validate_python_package(package_errors)

        self.assertTrue(
            any(
                "must be a JSON object" in error
                for error in evaluation_errors
            )
        )
        self.assertIn(
            "pyproject.toml: wheel must contain only pc_core",
            package_errors,
        )

    def test_host_templates_match_nested_official_shapes(self) -> None:
        """Name: Complete host-template schemas.

        Description: Validates Cursor event entries, retry limit, project-local
        runtime commands, and Claude's nested command-hook structure.
        Assumptions: Current official schemas match the frozen template fields.
        Expectations: Both checked-in templates produce no validation errors.
        """
        errors: list[str] = []
        validate_host_templates(errors)
        self.assertEqual(errors, [])

    def test_host_template_parse_failures_are_reported_independently(self) -> None:
        """Name: Independent host-template parse failures.

        Description: Supplies malformed Cursor and Claude JSON simultaneously.
        Assumptions: Repository validation promises to report every independent
        integration failure in one run.
        Expectations: Both template paths produce distinct actionable errors.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cursor_path = root / "adapters" / "cursor" / "hooks.json"
            claude_path = (
                root / "adapters" / "claude-code" / "settings.json"
            )
            cursor_path.parent.mkdir(parents=True)
            claude_path.parent.mkdir(parents=True)
            cursor_path.write_text("{", encoding="utf-8")
            claude_path.write_text("{", encoding="utf-8")
            errors: list[str] = []
            with mock.patch.object(validate_repository, "ROOT", root):
                validate_host_templates(errors)

        self.assertTrue(
            any("adapters/cursor/hooks.json" in error for error in errors)
        )
        self.assertTrue(
            any("adapters/claude-code/settings.json" in error for error in errors)
        )

    def test_invalid_markdown_encoding_does_not_abort_validation(self) -> None:
        """Name: Invalid Markdown encoding aggregation.

        Description: Supplies one non-UTF-8 Markdown source to link validation.
        Assumptions: Bad repository text is an actionable validation error, not
        a reason to skip unrelated checks.
        Expectations: The validator appends an error and returns normally.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "broken.md").write_bytes(b"\xff")
            errors: list[str] = []
            with mock.patch.object(validate_repository, "ROOT", root):
                validate_relative_links(errors)

        self.assertTrue(
            any("cannot inspect Markdown links" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
