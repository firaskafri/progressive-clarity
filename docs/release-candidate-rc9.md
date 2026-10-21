# Response-scope consolidation — 0.5.1-rc.9

This reviewed experiment follows repeated rc.8 failures, without changing the
frozen cases or replacing earlier failures. Candidate rc.9 is unpublished.
Its response-scope rule replaces overlapping entity, blocked-agreement, and
comparison instructions: use established facts, preserve shared decision facts,
separate implications from unknowns, and stop after the current request.
Corrections and literal-label guidance are consolidated without removing their
contracts. The canonical skill shrank from 12,901 to 12,442 bytes.

## Frozen plan — 2026-10-21

T10, T15, and T18 once each: three fresh sessions, five original development
responses, with T10 session continuity. Cursor Agent `2026.10.19-6bbf2c4`,
requested `gpt-5.2`, Ask mode, always-applied project rule containing the exact
rc.9 body, 240 seconds per response, concurrency three. No retries or in-round
revisions. These are known development checks, not an unseen holdout.

Tested skill SHA-256 (retained in the frozen plan and captures):
`b2963e3d91ed1726c01507e72d8a702af7e16b265982cedf65a61d59cfe004af`.

Stopping condition: capture and review every planned response, retain every
failure, and stop after this round without another wording revision. Only a
targeted pass justifies proposing a separate fresh complete development round;
no targeted result authorizes publication, submission, tagging, or deployment.

## Observed outcome

All five planned responses completed in three sessions with no retries or
execution errors. The shorter scope rule did not establish a behavioral fix:

- **T10 FAIL:** treats reconciliation as a database-migration scenario, asks
  whether Atlas is a technical product, expands Beacon's supplied discovery
  status, and uses a Full schema/data/ledger recap for the narrow risk follow-up.
- **T15 FAIL:** withholds a recommendation but still requests risk tolerance,
  jurisdiction/deadlines, and a detailed clause list instead of two decisive inputs.
- **T18 FAIL:** chooses the hall but omits that both venues are within budget and
  available. Adds weather/fallback sourcing, accessibility facility detail, and
  booking/contract considerations beyond the supplied evidence.

**Stop condition reached: 0/3 targeted case groups passed.** No subsequent behavioral
revision, inference, or full acceptance round was performed. Mechanical integrity
does not establish semantic compliance. rc.9 remains unpublished and release
acceptance blocked. This experiment does not justify more immediate prompt tuning
or relaxed scoring; a separate host/model or instruction-delivery investigation
would need its own reviewed scope.

## Local checks

A separately authorized [second-model comparison](model-comparison-rc9.md)
found substantially more bounded outputs with Sonnet through Cursor, but silent
application and full comparison scope remain unresolved. It is not stable
acceptance; no full round or release action followed that diagnostic.

The user later authorized a separate **experimental prerelease preparation**,
not stable acceptance. [Historical preparation status](publication-readiness.md#historical-experimental-rc9-preparation)
records validated artifacts and prerelease-only publishing safeguards. No tag,
push, vendor submission, website deployment, or publication was performed.

A subsequent separately authorized [instruction-delivery comparison](instruction-delivery-comparison.md)
tested unchanged whitespace-cleaned rc.9 as a startup rule and directly in the
first user message. Neither condition resolved the remaining scope failures;
direct delivery is not a sufficient fix. Earlier captures remain historical.

After the failed round, one extra newline at the skill EOF was removed to fix
`git diff --check`. No instruction text changed. The current whitespace-cleaned
skill SHA-256 is
`a1604c1b188d80afa6afe9b2f7e72270cd8fa121db0578d88a835907219f1ce5`.
The frozen behavioral evidence still identifies the pre-cleanup hash above;
neither hash is a behavioral acceptance pass. Previously built rc.9 archives
were not overwritten, and no new inference was run for the whitespace cleanup.

Repository validation and all 168 tests pass, including the compact-instruction
and cross-host instruction-preservation checks. All three candidate archives
build deterministically. Earlier archives, marketplace pins, and frozen cases
are unchanged. No new infrastructure or dependency is introduced.

Local evidence is retained under ignored
`evals/runs/cursor-response-scope-rc9-2026-10-21/`, including the pre-run plan,
prompts, traces, metadata, and visible responses. These are not an independent
public transcript archive or evidence of dynamic Skill activation.
