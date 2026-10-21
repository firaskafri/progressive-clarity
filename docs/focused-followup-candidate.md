# Focused follow-ups — 0.5.1-rc.4

Unpublished candidate `0.5.1-rc.4` retains rc.3's numeric safeguards and clarifies
that presentation is selected for each turn. A request for three views applies
to that answer unless the user explicitly requests an ongoing format. Topic
continuity does not imply layout continuity. Narrow parameter/definition/input
follow-ups stay Focused, including when a formula or caveat is useful. A later
explicit three-view summary still receives Full presentation.

This record describes rc.4. The working tree now targets the separate
[silent-application candidate rc.5](preamble-candidate.md), not a published release.

This addresses the repeated T01 follow-up failure documented in the
[numeric candidate history](numeric-advice-candidate.md). Published `0.5.0`,
its tag, marketplace pins, and preceding candidate archives remain unchanged.
Protocol and wrapper schemas are unchanged; the candidate is not vendor-approved
or published.

Skill SHA-256:
`84c2e61ad9fb541d28c3a8b24fc0827aa44175307f4873652c835f5cbc954a14`.

## Frozen debugging round — 2026-10-21

Before inference, the plan froze original T01 prompts and rubric, all four turns
in one fresh isolated workspace/session, Cursor Agent `2026.10.19-6bbf2c4`,
requested `gpt-5.2`, read-only Ask mode, stream-JSON capture, 240 seconds per
response, and no retries or in-round revisions. The first turn uses the same
explicit skill-loading prefix as earlier rounds. Model labels and visible skill
reads are recorded rather than inferred from formatting.

This is known development material. Results do not replace preceding failures,
constitute full-suite acceptance, test generalization, or establish reader benefit.

## Observed outcome

All **4/4 responses** completed in one session, with zero retries. The completed
skill read matches the frozen candidate hash. Host init labels alternated
`GPT-5.2`, `GPT-5.2 Medium`, `GPT-5.2`, `GPT-5.2 Medium`; the requested model
remained `gpt-5.2`. Hidden settings are not certified by these labels.

- **Focused follow-up: PASS for turn 3.** The TTL answer contains a bounded
  relationship and relevant retry/replay dependency, with no protocol headings,
  general architecture recap, invented duration, or unsupported retention policy.
  It does not ask a question, but a supported relationship is permitted by the
  numeric guidance; the summary explicitly requests the unresolved inputs.
- **Explicit Full presentation: PASS for the named shape check in turns 2 and
  4.** Each required heading appears once and in order. Thus the focused-follow-up
  change does not suppress a later explicit three-view summary in this case.
- **Summary numeric/configuration dependency: PASS for turn 4.** TTL is explicitly
  not set until real retry/replay windows are known; no duration or indefinite
  retention fallback is selected. This checks unresolved-value handling, not
  exhaustive correctness of every architectural claim or formula.
- **First-turn directness: FAIL.** The host announces loading the skill before
  the Redis answer despite the no-loading-commentary instruction.

**Outcome: the named focused-follow-up and numeric-regression checks passed in
this one known development case; no overall T01 or full-suite pass is claimed.**
The loading preamble remains unresolved. Persistent-format requests, other kinds
of follow-ups, supplied-input arithmetic, and unseen cases were not exercised.
No additional revision or inference followed this frozen round.

## Local checks and evidence

- All 168 unit tests and repository validation pass.
- Packaging tests retain focused-follow-up instructions and numeric safeguards
  in all three host distributions. They do not certify model behavior.
- Candidate archives build deterministically; all existing archives are unchanged.
- Raw plan, prompts, traces, metadata, and visible output are retained under
  ignored `evals/runs/cursor-followup-0.5.1-rc.4-2026-10-21/`, not a public
  independent transcript archive.
