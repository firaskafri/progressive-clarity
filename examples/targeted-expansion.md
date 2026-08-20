# Named single-view follow-up

- **Expected presentation:** Focused at the requested At depth level, without
  forcing the other views or a reserved heading.
- **Required facts:** The fill race, prevention mechanism, required tests,
  freshness alert, and rollback trigger appear without general caching recap.
- **Budget:** The Full-format 40/200 budget does not apply.

## Prompt

For our staged search-cache rollout, give me only the At depth view of the
invalidation risk. Do not recap request coalescing or general rollout policy.

## Response

An in-flight fill can outlive a write and repopulate an obsolete value after
invalidation. Capture a monotonic content version with each fill request, then
compare it with the current version before storing; reject mismatches.

Test delete, update, partial-failure, and delayed-fill paths. Alert on result age
rather than hit rate alone, count rejected stale fills, and keep rollback tied
to the rollout's freshness-error threshold.
