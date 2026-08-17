# Progressive Clarity v0.1 evaluations

This directory contains the host-neutral behavioral suite for Cursor and Claude Code. It is pinned to `SPEC.md` SHA-256 `90ccf39dc5cf91e895fb3cf2f1f788cba80daea94e1f07435748083c55bb4096`.

## Contents

- `cases.json` — protocol pin, run policy, counting rules, rubric, source facts, prompts, and pass criteria.
- `README.md` — execution and scoring guidance.

## Run policy

Run all 15 cases against the same skill revision in both hosts. Start every case run in a fresh session; keep all turns of a multi-turn case in that session.

Most cases run once per host. Run `PC-01`, `PC-03`, `PC-06`, `PC-10`, and `PC-11` three total times per host, with the baseline execution counted as run 1. This produces 25 sessions and 42 scored assistant responses per host.

Record the host, host version, model identifier, date/time, settings, skill revision, protocol checksum, installation path, invocation method, traces, prompts, unmodified raw outputs, word counts, fact checks, exceptions, and results listed in `run_policy.capture_fields`.

## Scoring

Use `PASS`, `FAIL`, or `UNVERIFIED`.

- Score required facts, caveats, order, budgets, corrections, and prohibited behavior from rendered output.
- Any omitted indispensable warning, contradiction, hidden reversal, or unsafe instruction is an immediate behavioral `FAIL`.
- Every required run must behaviorally pass. One behavioral failure fails the case for that host.
- Activation or inactivity is `UNVERIFIED` when the host exposes no load trace. Behavioral similarity is not activation evidence.
- Selected view, branch focus, and topic reset may be `UNVERIFIED` without a state trace. Their observable consequences remain pass/fail.
- Treat clarification as uncounted control dialogue only when it contains no substantive answer, recommendation, rationale, or implementation detail beyond an indispensable warning.
- A targeted branch inherits the active topic count, excludes sibling branches, and does not advance the parent view.
- A correction starts the response, withdraws the material error, replaces it, and updates changed consequences or actions. Exempt only the necessary repair words; resume accumulation from the pre-correction total.
- For every expansion sentence or bullet, identify the new fact, qualification, consequence, action, evidence item, or relationship. A unit with none is an echo and fails.
- Record warning and correction exception reasons and affected words in evaluation metadata, not user-facing output.

Word counting follows `cases.json.word_count`: remove excluded material, split included prose at whitespace, and count each token containing an English letter or digit. Inline code counts; fenced code and data tables do not.

## Result boundaries

The suite measures observable protocol behavior, host activation evidence when available, and safe-stopping completeness through predetermined fact and caveat checks. It does not establish comprehension, task success, safety outcomes, reader preference, or any other human outcome.

## Validation

From the repository root:

```sh
source /Users/firaskafri/Work/code/lms-api/.venv/bin/activate
python -m json.tool evals/cases.json >/dev/null
```

Internal validation must additionally confirm unique case and fact IDs, valid fact references, sequential turn numbers, declared repeat cases, and agreement between each case's `runs_per_host` and the suite run policy.
