# rc.15 bounded composition repair

Under the user's authorization to continue Azure/Grok evaluation, rc.15 replaces
the depth paragraph: opening contains the decision/correction/complete safety
gate; In context supplies causal rationale or a new timing/handoff implication;
At depth supplies verification records/checks/outcomes. It prohibits repeating
the same schedule or gate as a list while preserving complete safety conditions.
Redundant wording was shortened to retain the compact-instruction test.

Skill SHA-256:
`6d02b5c5b7cfaf4dc41232a8117ebc3ee2158d2a8d3bcc7ef8fcf9e78d2b5a6e`.
Specification, original suite, disclosed context-v1 expectations, marketplace
pins, and previous artifacts/results are unchanged.

## Frozen targeted round
### Subsequent bounded completion review

Authorized continuation reviewed only the twelve previously unreviewed outputs,
preserving the three original PASS judgments. Each review ran in a separate
subprocess with a 60-second SDK timeout and 90-second process timeout, concurrency
two, zero automatic retries. No candidate responses were regenerated.

All twelve completion attempts returned valid judgments: seven PASS, five FAIL.
Combined with the original three results: **10 PASS / 5 FAIL / 0 UNVERIFIED
reviewed responses**. This separate-model review is not human certification.
Failures remain at T03 turn 3, T04 run 1 turn 3, T04 run 2 turn 3, and T05 runs
1 and 3. Findings cover repetitive context/closing gate lists and an unsupported
handoff/readiness assertion. Full reviewer quotations remain in local evidence.

The execution stall is resolved for this bounded continuation, but candidate
acceptance still fails. No full round, instruction edit, tag, push, or publication
followed. The original stalled attempt and incomplete summary remain historical,
not overwritten. Completed-review evidence is under the `bounded-review/`
subdirectory of the existing local round; actual Azure charges remain unknown.

T03 once, T04 three repetitions, T05 three repetitions: seven fresh sessions /
15 responses on `gpt-5.6-sol`, API `2024-10-21`, system-body injection,
180-second configured timeout, 5,000 completion-token limit, no retries or
in-round edits. All generation responses completed; raw semantics remain
UNVERIFIED because judging was disabled in the generation report.

Separate `gpt-6-astra` review reused the same criterion generator/parser for
existing outputs, with a frozen 15-judgment plan. Three judgments completed PASS:
T03 turn 1, T03 turn 2, T04 run 1 turn 1. The review worker subsequently made
no progress for over ten minutes, beyond the intended request timeout. It was
terminated to avoid uncontrolled resource use. Twelve reviews remain UNVERIFIED;
no retries were made and no favorable outcome is inferred for missing reviews.

**Stable acceptance remains blocked.** The targeted gate did not clear, so no
full round or release action followed. This is a review-execution blocker, not
a model-conformance pass. Fix bounded execution/usage observability before more
review calls rather than endlessly rerunning or weakening the rubric.

Local evidence: ignored `evals/runs/azure-rc15-composition/` contains the generation
plan/report, review plan, three completed judgments, and review summary recording
the incomplete state. Azure billing is authoritative for costs; generation/review
token metrics were not captured. Terminating the client cannot guarantee cancellation
of work already accepted by Azure.

Local repository validation, 172 tests, Ruff, and diff checks pass. Candidate
changes and evidence documentation are uncommitted; no push, tag, stable version,
vendor submission, deployment, or publication occurred.
