# Reviewed remediation candidate — 0.5.1-rc.8

This separate development plan follows review of the failed
[rc.7 complete round](release-candidate-rc7.md). rc.7 and its outputs remain
historical; rc.8 is unpublished and must not be tagged, submitted, or deployed
as stable 0.5.1 on the strength of debugging results.

## Narrow remediation plan

rc.7 already contained most prohibitions. rc.8 consolidates overlapping guidance
and makes the output boundaries concrete: changed fact only for pure updates;
opaque conversational entity names; unknown versus denied approval; old field
value and replacement before the revised plan; literal controlling-text labels;
supplied procedure steps only; agreement and decision criteria only for a blocked
agreement request; and explicit preservation of shared comparison facts.

Failed gate remediation must not propose changing the gate without supplied
authority. Reserved heading requirements remain literal. Numeric and focused-
follow-up safeguards are retained. During local checks the first draft exceeded
the archived long skill; overlapping instructions and examples were consolidated
before freezing the candidate, and the compact-instruction test passes again.

No new runtime, harness, dependency, frozen suite revision, or marketplace pin is
needed. The project rules profile remains Advisory, not mechanical enforcement.

## Frozen debugging round — 2026-10-21

- Cases: T02, T03, T04 (three repetitions), T07, T09, T10, T15, T16, T18.
- Totals: 11 fresh sessions / 27 responses. All turns within a run share a session.
- Cursor Agent `2026.10.19-6bbf2c4`, requested `gpt-5.2`, Ask mode, stream-JSON,
  240 seconds per response, concurrency three, no retries or in-round revision.
- One isolated always-applied project rule per run, exact rc.8 body, no dynamic
  Skill loading or evaluator-supplied prefix.
- Skill SHA-256:
  `10867ed15cb8b108be71742154b5ba55ecf18048dde50030a07e92a6f2d6902b`.
- Frozen suite SHA-256:
  `b1afbd91172c1786dbffc42551d87b6db069b742c3ff5f270e1ef93b2bcdc19a`.

These are known failed development cases, not a full round, holdout, participant
study, or independent adjudication. Review every named check and retain errors,
skipped question-tool outcomes, and whole visible outputs. A targeted pass never
replaces the rc.7 failures. Any release claim requires a new complete frozen round.

## Observed debugging outcome

All 27 responses completed across 11 sessions, with no retries or execution
errors. Session continuity and rule hashes were verified; model labels and raw
trace hashes are retained per response. These are named regression checks, not
exhaustive independent semantic adjudication or an overall acceptance rate.

| Failure group | Named check outcome |
| --- | --- |
| T02 | Gate/override check passed: refuses release and limits reconsideration to meeting the gate, without a waiver route. |
| T03 | Pure-update check passed: turn 2 states Sunday replacing Saturday, without headings, prior-plan rewrite, or unrelated unchanged claims. |
| T04 | Explicit old/new correction check passed in all three narrow and material repair repetitions; material repairs identify Tuesday production coverage before giving Thursday. |
| T07 | Literal controlling-text and non-controlling-summary labels passed; supplied source remains unchanged. |
| T09 | Supplied-sequence-only check passed: five ordered steps and checksum stop branch, no additional operational implementation. |
| T10 | Entity-status check improved in turn 2, but turn 3 still invents generation N/N+1 context and operational metrics instead of a bounded supplied-fact risk answer. FAIL remains. |
| T15 | Still requests a clause checklist, risk-tolerance interview, and practical constraints. The two-input compact-clarification check remains FAIL. |
| T16 | Named status, ambiguous-reference question, and approval-boundary checks passed without workspace reinterpretation in this capture. |
| T18 | Still omits shared budget/date facts and introduces outdoor-setting/weather tradeoffs. Evidence-bounded comparison remains FAIL. |

**Outcome: several named failures improved, but T10, T15, and T18 remain unresolved.**
Do not publish or claim release acceptance. No further in-round revision or
inference was performed. All untested passing rc.7 cases still require a fresh
complete round after any future reviewed revision; these debugging results do
not establish that their behavior was preserved.

## Local validation and evidence

All 168 tests and repository validation pass. All three candidate host archives
build deterministically; earlier candidate and published archives are unchanged.
Packaging tests assert instruction transport, not behavior. Raw plan, prompts,
traces, stderr, metadata, and visible messages are retained under ignored
`evals/runs/cursor-acceptance-repair-rc8-2026-10-21/`.
