# Authorized two-response Sonnet check — rc.11

The user authorized only T15 and T18 once each, two fresh sessions, no retries,
then usage reporting and stop. No full round, further revision, or publication
is included. Cursor Agent `2026.10.19-6bbf2c4`, requested
`claude-sonnet-5-5-medium`, reported `Claude Sonnet 5.5 300K Medium`, Ask mode,
240 seconds per response, concurrency two. Exact rc.11 body in one always-applied
rule per isolated workspace; original prompts unchanged, no invocation prefix.

Skill SHA-256:
`f5a1a6b20ba55137af051950485246848358ea8bb9c8e7b94f3c919eb9131b45`.

Both responses completed. Original prompts, rule hashes, and distinct sessions
were verified. Conservative visible-output review:

- **T15 targeted PASS:** “Please provide the agreement and your decision
  criteria; I need both to assess whether to sign.” No checklist, heading,
  premature recommendation, narration, or later-format promise.
- **T18 Focused/fact-preservation checks PASS:** no protocol headings, hall
  recommendation grounded in the supplied criteria, and both options' budget
  and date availability explicitly retained. It does not exhibit the previously
  failing Full-view repetition pattern.
- **T18 broader scope FAIL:** adds cancellation/change terms and a committee
  approval step beyond supplied facts and their verification. These are proposed
  checks/actions, not assertions that such contract conditions exist; nonetheless
  they exceed the candidate's bounded response-scope requirement. Repetition and
  proportionality elsewhere are not independently certified by the named passes.

Stable acceptance remains blocked. This is a known-development targeted capture,
not full-suite acceptance, an unseen case, or independent adjudication. No full
round or additional paid call followed. No instruction change was made after
these results.

Reported counters: input 8; output 513; cache-read 17,786; cache-write 42,144.
These separate host counters are not a verified dollar charge; consult Cursor
billing. Local evidence and trace hashes are retained under ignored
`evals/runs/cursor-sonnet-targeted-rc11-2026-10-21/`.
