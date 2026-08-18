"""Name: Repository tooling and Python package contract suite.

Description: Exercises importable repository validation, ordered test
docstrings, installable pc-core metadata, and exact host-template schemas.
Assumptions: Validation helpers are invoked as the tools package from the
repository root; wheel installation is covered by the CI integration smoke.
Expectations: Metadata and hook drift fail locally before packaging or host use.
"""

from __future__ import annotations

import unittest

from tools.validate_repository import (
    test_docstring_problem,
    validate_host_templates,
    validate_python_package,
)


class RepositoryToolingTests(unittest.TestCase):
    """Name: Validator import and contract checks.

    Description: Verifies the validator as an importable module and probes
    ordered docstring, package metadata, and nested hook-schema boundaries.
    Assumptions: Checked-in files are the canonical integration inputs.
    Expectations: Valid contracts produce no errors and reordered fields fail.
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


if __name__ == "__main__":
    unittest.main()
