"""Prepare blinded, counterbalanced reader packets from matched condition reports."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Mapping, Sequence

from pc_core.json_io import parse_json, write_json_atomic
from tools.azure_eval_harness import CONDITIONS, RESULT_SCHEMA_VERSION, HarnessError


def prepare_packets(
    reports: Sequence[Mapping[str, object]], *, seed: int, readers: int = 4,
) -> tuple[dict[str, object], dict[str, object]]:
    """Blind run-one conversations, giving each reader one variant per case.

    The separate key records assignments and source identity. Characteristic
    output styles can still reveal a condition; label blinding cannot prevent that.
    """
    if readers < 4 or readers % 4:
        raise HarnessError("readers must be a positive multiple of four")
    if any(not isinstance(report.get("condition"), str) for report in reports):
        raise HarnessError("each report must identify its comparison condition")
    by_condition = {report.get("condition"): report for report in reports}
    if len(reports) != len(CONDITIONS) or set(by_condition) != set(CONDITIONS):
        raise HarnessError("supply exactly one report for each comparison condition")
    reference = by_condition[CONDITIONS[0]]
    case_selection = reference.get("selected_case_ids")
    if (
        not isinstance(case_selection, list) or not case_selection
        or any(not isinstance(case_id, str) or not case_id for case_id in case_selection)
        or len(case_selection) != len(set(case_selection))
    ):
        raise HarnessError("reader packets require a non-empty case selection")
    runs: dict[str, dict[str, list[dict[str, object]]]] = {}
    identities: dict[str, str] = {}
    for condition in CONDITIONS:
        report = by_condition[condition]
        if report.get("status") != "COMPLETE" or report.get("schema_version") != RESULT_SCHEMA_VERSION:
            raise HarnessError("reader packets require complete current-schema reports")
        for field in (
            "suite_sha256", "protocol_sha256", "model", "split", "selected_case_ids",
            "planned_case_run_keys",
        ):
            if field not in report or report[field] != reference.get(field):
                raise HarnessError(f"comparison reports differ or lack {field}")
        identities[condition] = hashlib.sha256(
            json.dumps(report, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        records = report.get("runs")
        if not isinstance(records, list):
            raise HarnessError("report runs must be an array")
        runs[condition] = {}
        for record in records:
            if not isinstance(record, dict) or record.get("run_number") != 1:
                continue
            case_id = record.get("case_id")
            turns = record.get("turns")
            if not isinstance(case_id, str) or case_id in runs[condition]:
                raise HarnessError("run-one case IDs must be unique strings")
            if not isinstance(turns, list) or not turns:
                raise HarnessError("run one must have complete conversation output")
            transcript = []
            for index, turn in enumerate(turns, 1):
                if (
                    not isinstance(turn, dict) or turn.get("turn") != index
                    or not isinstance(turn.get("prompt"), str)
                    or not isinstance(turn.get("raw_output"), str)
                    or not turn["raw_output"].strip()
                ):
                    raise HarnessError("conversation turns must be complete and sequential")
                transcript.append({
                    "turn": index, "user": turn["prompt"], "assistant": turn["raw_output"],
                })
            runs[condition][case_id] = transcript
        if set(runs[condition]) != set(reference["selected_case_ids"]):
            raise HarnessError("each selected case needs a completed run one")

    case_ids = sorted(runs[CONDITIONS[0]])
    for case_id in case_ids:
        prompts = [turn["user"] for turn in runs[CONDITIONS[0]][case_id]]
        for condition in CONDITIONS[1:]:
            if [turn["user"] for turn in runs[condition][case_id]] != prompts:
                raise HarnessError("conditions must contain identical user-turn sequences")

    rng = random.Random(seed)
    rng.shuffle(case_ids)
    conditions = list(CONDITIONS)
    rng.shuffle(conditions)
    packets = []
    assignments = []
    for reader in range(readers):
        tasks = []
        reader_id = f"R{reader + 1:03d}"
        for index, case_id in enumerate(case_ids):
            condition = conditions[(index + reader) % len(conditions)]
            sample_id = f"{reader_id}-S{index + 1:03d}"
            tasks.append({
                "sample_id": sample_id,
                "conversation": runs[condition][case_id],
                "observations": {
                    "action_interpretation": None,
                    "constraints_identified": None,
                    "retrieval_seconds": None,
                    "would_use_again_rating_1_to_5": None,
                    "notes": None,
                },
            })
            assignments.append({
                "sample_id": sample_id, "reader_id": reader_id,
                "case_id": case_id, "run_number": 1, "condition": condition,
            })
        rng.shuffle(tasks)
        packets.append({"reader_id": reader_id, "tasks": tasks})
    return (
        {"schema_version": "1.0.0", "packets": packets},
        {
            "schema_version": "1.0.0", "seed": seed,
            "design": "one variant per case per reader; balanced across blocks of four readers",
            "run_selection": "run one, fixed before inspecting quality",
            "source_report_sha256": identities,
            "assignments": assignments,
            "reader_outcomes": "UNVERIFIED",
        },
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Write reader-visible packets and a separate investigator-only key."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs=4, type=Path)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--readers", type=int, default=4)
    parser.add_argument("--packets", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        paths = [*args.reports, args.packets, args.key]
        if len({str(path.resolve()).casefold() for path in paths}) != len(paths):
            raise HarnessError("inputs, packets, and key must use distinct paths")
        if args.packets.exists() or args.key.exists():
            raise HarnessError("use fresh output paths for reader packets and key")
        reports = [parse_json(path.read_text(encoding="utf-8")) for path in args.reports]
        if any(not isinstance(report, dict) for report in reports):
            raise HarnessError("reports must be JSON objects")
        packets, key = prepare_packets(reports, seed=args.seed, readers=args.readers)
        write_json_atomic(args.key, key)
        write_json_atomic(args.packets, packets)
    except (OSError, ValueError, HarnessError) as exc:
        print(f"reader-study: {exc}", file=sys.stderr)
        return 2
    print(f"packets={args.packets}")
    print(f"investigator_key={args.key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
