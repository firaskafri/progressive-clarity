# rc.17 numeric scope repair and reviewer disagreement

rc.17 explicitly retains the provider retry/redelivery window in payment
idempotency questions and summaries. Redundant prose was shortened without
changing the compact-skill limit, specification, rubric, or original cases.

Skill SHA-256:
`98e49e14c00aae6f2e91472e88fb2aeb2af7782eacf7245933f47b655e5c604d`.

## Fresh full round

Azure `gpt-6-astra` generated all 44 responses in 22 context-v1 sessions.
Deterministic checks passed for all 44 responses. Separate `gpt-5.6-sol` review
returned **44 PASS / 0 FAIL / 0 UNVERIFIED**. The raw no-judge report remains
UNVERIFIED; this is a separate-model judgment, not human or live-host certification.

A finite supplemental `gpt-6-astra` audit reviewed only the 13 Full responses,
using the same criteria and existing outputs. It returned **11 PASS / 2 FAIL**:

- T04 run 1 turn 3: “The corrected schedule places the handoff between
  Wednesday’s review and Thursday’s production coverage.” Dates establish order,
  not handoff timing; the following proposal label does not qualify this assertion.
- T10 turn 1: context repeatedly restates reconciliation before rollback instead
  of adding predominantly new depth. The useful other-requirements caveat does
  not make the entire view predominantly new.

Both findings were accepted as genuine boundary failures. The initial 44 PASS
judgments remain unchanged. The supplemental audit is same-model self-review,
not independent certification, and its disagreement blocks release clearance.

All reviews used 60-second SDK / 90-second process bounds, concurrency two,
zero automatic retries. All completed; no timeout or answer regeneration occurred.
Ignored captures: `evals/runs/azure-rc17-astra-full/`, with `bounded-review/` and
`full-audit/` retained separately. Actual charges require Azure billing.

All 172 tests, repository validation, Ruff, and whitespace checks passed.
Five local artifacts were built under `/tmp/pc-rc17-artifacts/`; archive bodies
match the canonical skill, and local checksums were generated. These uncommitted
artifacts are not release assets and must not be reused for later versions.
No commit, push, tag, publication, vendor submission, or deployment occurred.
