"""Validate the immutable, credential-free stable development acceptance record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.azure_eval_harness import (
    deterministic_score,
    judge_criteria,
    load_suite,
    parse_judge_result,
    parse_view_sections,
)
from tools.package_common import split_skill


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = Path("evals/release-acceptance-0.5.1.json")
EVIDENCE_SHA256 = "77f4f5a4a4c3d30dfc87a14138b67173220af562687ba2492d7c61575553feb3"


def validate_acceptance(root: Path = ROOT) -> None:
    """Fail closed if accepted inputs, complete coverage, or judgments change."""
    raw = (root / EVIDENCE_PATH).read_bytes()
    if hashlib.sha256(raw).hexdigest() != EVIDENCE_SHA256:
        raise ValueError("release acceptance evidence differs from reviewed record")
    evidence = json.loads(raw)
    from tools.package_common import RELEASE_VERSION

    if evidence["release_version"] != RELEASE_VERSION:
        raise ValueError("acceptance record does not cover this release version")
    paths = {
        "skill_sha256": "skills/progressive-clarity/SKILL.md",
        "original_suite_sha256": "evals/cases.json",
        "protocol_sha256": "SPEC.md",
    }
    for field, path in paths.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != evidence[field]:
            raise ValueError(f"accepted input changed: {path}")
    _, body = split_skill((root / paths["skill_sha256"]).read_bytes())
    if hashlib.sha256(body).hexdigest() != evidence["skill_body_sha256"]:
        raise ValueError("accepted instruction body changed")
    suite = load_suite(root / evidence["suite_path"])
    suite_bytes = json.dumps(
        suite, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    if hashlib.sha256(suite_bytes).hexdigest() != evidence["suite_sha256"]:
        raise ValueError("accepted suite changed")
    cases = {case["id"]: case for case in suite["cases"]}
    expected = {
        (case["id"], run, turn["turn"])
        for case in cases.values()
        for run in range(1, case.get("runs_per_host", 1) + 1)
        for turn in case["turns"]
    }
    seen = set()
    audits = 0
    for record in evidence["records"]:
        key = (record["case_id"], record["run_number"], record["turn"])
        if key not in expected or key in seen:
            raise ValueError("invalid or duplicate acceptance response")
        seen.add(key)
        case = cases[key[0]]
        turn = next(turn for turn in case["turns"] if turn["turn"] == key[2])
        if record["prompt"] != turn["prompt"]:
            raise ValueError("acceptance prompt differs from frozen suite")
        score = deterministic_score(case=case, turn=turn, response=record["response"])
        if score != record["deterministic"] or score["result"] != "PASS":
            raise ValueError("acceptance deterministic check failed")
        criteria = [
            criterion["id"]
            for criterion in judge_criteria(case=case, turn=turn, response=record["response"])
        ]
        review = parse_judge_result(record["review"], expected_criteria=criteria)
        if review["overall"] != "PASS":
            raise ValueError("acceptance review did not pass")
        headings, _ = parse_view_sections(record["response"])
        if headings:
            audit = parse_judge_result(record["full_audit"], expected_criteria=criteria)
            if audit["overall"] != "PASS":
                raise ValueError("Full acceptance audit did not pass")
            audits += 1
    if seen != expected or len(seen) != 44 or audits != 13:
        raise ValueError("release acceptance coverage is incomplete")


def main() -> int:
    """Check acceptance without inference, authentication, or remote calls."""
    validate_acceptance()
    print("Stable development acceptance verified: 44 responses, 13 Full audits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
