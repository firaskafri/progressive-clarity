# Authorized targeted Sonnet round — rc.10

The user authorized one targeted round only: T10, T15, T18 once each, three
fresh sessions / five responses, zero retries, then report usage and stop.
No full round or release action was authorized.

Frozen setup: Cursor Agent `2026.10.19-6bbf2c4`, requested
`claude-sonnet-5-5-medium`, reported `Claude Sonnet 5.5 300K Medium`, Ask mode,
240 seconds per response, concurrency three. Identical original development
prompts, an always-applied rc.10 rule per isolated workspace, and T10 session
continuity. Source commit: `1dba36f27149c696aa853fe5b4c1205c5e8722ac`.
Skill SHA-256:
`0a05293fae8741d2885ae131b0055dadb268c7ba955f018e21c28193f1ea03e4`.

## Outcome

All five responses completed. Rule hashes, original prompts, and three distinct
session IDs were verified. This known-development round did not clear acceptance.

- **T10 named scope/follow-up checks passed:** no database/product inference;
  Beacon answer retains supplied discovery status; risk follow-up is Focused and
  does not invent specific failure mechanisms. Whole-case semantic/additivity
  correctness is not independently adjudicated.
- **T15 candidate instruction FAIL:** no legal checklist, but closes with “Once
  I have those, I can give the full recommendation in all three views.” rc.10
  explicitly prohibits promising a later format. Frozen no-recommendation and
  no-three-heading checks pass; these do not erase the candidate-rule failure.
- **T18 additivity FAIL:** opening already establishes the option comparison,
  then In context repeats each option's fit and the same rationale. A one-line
  next step does not make that view predominantly new. A separate conclusion
  also precedes At a glance. Shared budget/date facts are retained, and evidence
  requests are not assertions that unsupplied facilities exist; keep these checks
  distinct from the repetition failure.

Stable 0.5.1 remains blocked. No full round, retry, new wording revision, tag,
push, publication, or further paid inference followed this authorized round.

## Reported usage

| Cursor counter | Total |
| --- | ---: |
| Input tokens | 20 |
| Output tokens | 1,264 |
| Cache-read tokens | 87,014 |
| Cache-write tokens | 63,766 |

These are separate host-reported counters, not a verified billing calculation.
Actual cost is unknown; consult Cursor usage/billing. No dollar cap is inferred
or claimed. Raw plan, prompts, traces, metadata, visible responses, and hashed
observations are retained locally under ignored
`evals/runs/cursor-sonnet-targeted-rc10-2026-10-21/`.
