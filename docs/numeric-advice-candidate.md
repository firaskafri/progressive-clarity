# Numeric-advice hardening — candidate history

## Candidate, not a release

The numeric hardening history below ends at unpublished package `0.5.1-rc.3`,
protocol `0.5`. The working tree now targets the separate
[focused-follow-up candidate `0.5.1-rc.4`](focused-followup-candidate.md), which
retains these numeric safeguards.
Published `0.5.0` archives, its tag, and repository marketplace pins are unchanged.
Wrapper schemas and mechanical behavior are unchanged. The candidate has no
vendor approval, publication, or full-suite acceptance result.

The specification already prohibits unsupported numeric recommendations. The
preceding `0.5.1-rc.1` candidate strengthened the skill to reject numbers presented
as “common”, “minimum”, or “safe default” values when decisive inputs are missing.
Hypothetical examples must stay conditional, unresolved dependencies must stay
unresolved in summaries, and an earlier unsupported recommendation must be
retracted rather than promoted into guidance.

Historical rc.1 skill SHA-256:
`a7789c42ae7e274125477ebf54062ed6b9d1ef0af9ca5f868529bb2709cc89c8`.

## rc.1 targeted Cursor debugging — 2026-10-21

Frozen before inference: T01, one fresh session, all four original turns, no
retries, 120 seconds per response. The original development prompts and rubric
were unchanged. This is a failed-case debugging rerun, not a replacement for the
[earlier v0.5 smoke](cursor-v05-smoke.md), a full development round, or a holdout.

Settings match the earlier smoke: Cursor Agent `2026.10.19-6bbf2c4`, requested
`gpt-5.2`, reported `GPT-5.2 Medium`, read-only Ask mode, stream-JSON capture,
and the same explicit skill-loading prefix on the first turn. A fresh temporary
workspace contains only the copied candidate skill; trust was explicit for that
workspace. The host trace confirms a completed read of the candidate skill.

All **4/4 responses** completed successfully. Evaluator review of the visible
outputs found:

- **Numeric follow-up: FAIL.** Turn 3 recommends “typically 30–90 days”, calls
  90 days a “common safe default”, and recommends indefinite or at least one-year
  DB retention without the decisive provider/operational inputs. It asks for the
  PSP only after supplying recommendations. It also uses Full rather than the
  required Focused presentation.
- **Summary propagation: FAIL.** Turn 4 correctly says TTL is unresolved at the
  opening, but later preserves “a likely range 30–90 days.” It does not retract
  the earlier unsupported recommendation. The opening qualification does not
  justify the range deeper in the response.
- **Loading preamble remains.** Turn 1 announces skill loading before answering.
  This candidate targeted numeric advice, not the separate directness failure.

**rc.1 outcome: the instruction change is implemented, but the observed numeric
failure is not fixed.** No second revision or further inference was performed
after this round. Review is required before another candidate or a full round.
Text-preservation tests establish packaging integrity, not semantic enforcement.

## rc.2 decision rule and contrasting examples

After reviewing rc.1's failures, the user authorized a separate candidate and
one further bounded test. rc.2 replaces broad prohibitions with three branches:
missing decisive inputs, sufficient inputs, and a clearly hypothetical example.
It disallows appending a typical range or fallback after asking a question.
Contrasting examples cover an unresolved retry window and a supplied versus
hypothetical buffer-capacity calculation. The summary/retraction safeguards remain.

rc.2 skill SHA-256:
`f7750662ec3b5aabbda9bb2cb3e8a4a3de766d6dd36ce914114195525048faea`.

The rc.2 debugging plan freezes the same T01 prompts and settings as rc.1:
one fresh session, four turns, 120 seconds per response, no retries or revisions
within the round. This case is known development material, not an unseen test
of generalization.

All **4/4 responses** completed successfully. The captured completed skill read
matches the frozen rc.2 hash. Review of the whole visible output found:

- **Unsupported numeric durations absent, 2/2 relevant turns.** The TTL
  follow-up and summary do not recommend a concrete duration or numeric range.
  Both name the provider/client/job replay-window dependencies. This is a
  bounded observation, not proof of reliable generalization.
- **Decision fallback still unsupported.** Turn 3 says to use DB records with
  “no TTL” or “a very long TTL” if the window cannot be bounded; turn 4's first
  summary preserves “no TTL or long retention.” Missing inputs do not justify
  selecting an indefinite or vague-long retention policy. The candidate's
  missing-input branch therefore remains unmet.
- **Focused follow-up: FAIL.** Turn 3 uses all three protocol headings instead
  of the required Focused answer.
- **Summary structure: FAIL.** Turn 4 emits an incomplete three-view answer,
  then starts a second three-view answer. Each required heading appears twice
  across the whole visible output. The runner invoked this turn only once;
  both passages are retained as host output, not treated as a clean retry.
- The skill-loading preamble remains in turn 1. No supplied-input calculation
  or hypothetical-example behavior was tested in this four-turn scope.

**rc.2 outcome: bounded improvement in numeric specificity, still no T01
conformance pass.** No further revision or inference followed this round. A
broader development round and fresh independent cases are required before any
general numeric-advice reliability claim.

## rc.3 nonnumeric configuration dependencies

After review of rc.2, the user authorized one separate candidate and bounded
rerun. rc.3 states that unresolved expiry requirements do not justify disabling
expiry, retaining indefinitely, choosing vague-long retention, or changing policy
without evidence. A contrasting example separates durable duplicate protection
from an undecided retention policy; summaries preserve that distinction too.

rc.3 skill SHA-256:
`6859ef2a1d4f0db776493d6520b87703de8f6b0e3b375d84f393415c1a353815`.

The pre-run plan retains the same T01 prompts, explicit invocation, Cursor
version/model, four turns in one fresh session, and 120-second response timeout.
No retries or in-round revisions are allowed. This remains known development
material, not generalization or acceptance evidence.

**Execution outcome: TIMEOUT; behavior UNVERIFIED.** The first Redis
classification turn timed out after 120 seconds without a terminal result
event. The partial trace confirms a completed read matching the frozen rc.3
skill hash and displays a loading preamble, but no completed answer. Host init
reported `GPT-5.2` (not the earlier runs' `GPT-5.2 Medium`); the requested CLI
model remained `gpt-5.2`. Hidden model settings cannot be assumed identical.

Denominators: **0/4 planned responses completed; 1 attempt timed out; 3 dependent
turns unattempted; 0 retries**. The runner stopped rather than resume an
incomplete case or silently retry. Numeric/configuration outcomes are therefore
neither a pass nor an observed semantic failure for rc.3. The earlier rc.1/rc.2
failures remain unchanged. No further revision or inference followed this run.

## Local validation and evidence

### rc.3 separately authorized fresh round — 2026-10-21

Following the timeout, the user authorized one fresh execution of unchanged
rc.3. The plan was frozen before inference: identical T01 prompts and skill
hash, one new workspace/session, requested `gpt-5.2`, 240 seconds per response,
and no automatic retries. The earlier timeout evidence was not overwritten.

All **4/4 planned responses completed**, in one session, with zero retries.
The completed skill read matches the frozen rc.3 hash. Host init labels were
`GPT-5.2` for turns 1–2 and `GPT-5.2 Medium` for turns 3–4; this is reported
rather than treated as proof of identical hidden settings.

- **Missing-input numeric/configuration check: PASS for turn 3.** It supplies
  a relationship based on client, job, webhook, and operational replay horizons,
  asks for retry/replay inputs, and chooses no duration, numeric range, disabled
  expiry, indefinite-retention policy, or vague-long retention fallback.
- **Summary dependency check: PASS for turn 4.** It explicitly states that a
  numeric TTL is not set until the replay horizons are known, and does not
  introduce an unsupported retention fallback. Its three headings each appear
  once, unlike the rc.2 capture.
- **Focused follow-up: FAIL for turn 3.** All three protocol headings remain,
  with an unnecessary broader architecture discussion instead of a focused
  request for decisive inputs and a bounded relationship.
- **First-turn directness: FAIL.** A loading preamble still precedes the Redis
  classification answer.

**Outcome: the two named numeric/configuration checks passed in this fresh
round; T01 still fails overall.** This single known development case does not
establish cross-host reliability, general semantic correctness, or full-suite
acceptance. No supplied-input calculation or hypothetical-example control was
tested. The earlier failures and timeout remain part of the record.

No additional instruction revision or inference followed this round. A full
development round and fresh independent cases remain necessary before a broader
candidate conformance claim.

### Validation and retained captures

- Repository validation and all **168 unit tests: PASS**.
- Added packaging test checks that all three host distributions retain the
  numeric safeguards and use a version other than published `0.5.0`.
- Two builds of each candidate host archive: matching hashes. Existing `0.5.0`
  and rc.1 distributions remain byte-identical.
- Changed Python files parse successfully; Ruff is unavailable locally.
- Raw plan, prompts, traces, metadata, and visible outputs are retained locally
  under ignored `evals/runs/cursor-numeric-0.5.1-rc.1-2026-10-21/`.
  They are not a public transcript archive or independent reader research.
- The separate rc.2 plan and captures are retained under ignored
  `evals/runs/cursor-numeric-0.5.1-rc.2-2026-10-21/`; earlier evidence is unchanged.
- rc.3's frozen plan, partial raw trace, timeout metadata, and extracted
  commentary are retained under ignored
  `evals/runs/cursor-numeric-0.5.1-rc.3-2026-10-21/`. Two candidate builds match;
  all existing release and preceding candidate archives remain byte-identical.
- The separate fresh rc.3 round is retained under ignored
  `evals/runs/cursor-numeric-0.5.1-rc.3-round2-2026-10-21/`, including prompts,
  raw traces, visible output, metadata, and `observations.json` with trace hashes.
