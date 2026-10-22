# Authorized single T18 check — rc.12

The user authorized exactly one T18 response, a fresh isolated session, no
retries, then usage reporting and stop. Original development prompt unchanged;
Cursor Agent `2026.10.19-6bbf2c4`, requested `claude-sonnet-5-5-medium`, reported
`Claude Sonnet 5.5 300K Medium`, Ask mode, 240-second timeout. The always-applied
rule contains exact rc.12 body; skill SHA-256:
`be6a11809c702bfa810ba2dfc22e857f6c8ef25234b51032b22dc8c47e036eba`.

The response completed and its prompt/rule hashes were verified. **Targeted
T18 PASS** under visible-output review: recommends the hall from the two stated
requirements, preserves both venues' shared budget and date availability, stays
Focused, and limits evidence requests to supplied access, fallback, budget, and
availability. No cancellation/change terms, invented facilities, or approval
requirement are added. Conditional reporting back to the committee if supplied
facts change does not impose a new approval prerequisite. Brief same-answer
repetition is present but there is no failing repeated Full-view pattern.

This is one known development case, not independent adjudication, reliability,
full-suite acceptance, or absence of regressions. T15's earlier pass belongs to
rc.11, not rc.12. Stable acceptance remains blocked pending a fresh complete
round and review. No full round, further model call, instruction change, commit,
push, tag, or publication followed this authorized single-response check.

Reported tokens: input 4; output 459; cache-read 8,893; cache-write 21,125.
These are separate host counters, not a dollar bill; consult Cursor billing.
Raw plan, prompt, trace, visible response, metadata, and observations are retained
locally under ignored `evals/runs/cursor-sonnet-t18-rc12-2026-10-21/`.
