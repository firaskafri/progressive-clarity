# Targeted follow-up

- **Expected views:** All three views focus only on the invalidation branch.
- **Required facts:** The fill race, prevention mechanism, required tests,
  freshness alert, and rollback trigger appear without general caching recap.
- **Budget:** At a glance is at most 40 words; prose through In context is at
  most 200 words.

## Prompt

For our staged search-cache rollout, expand only the invalidation risk. Do not
recap request coalescing or general rollout policy.

## Response

### At a glance

<!-- words:targeted-glance:start -->
Prevent stale overwrites by versioning cache entries or rejecting fills older
than the latest invalidation. Keep rollback available until freshness checks
pass.
<!-- words:targeted-glance:end -->

### In context

<!-- words:targeted-context:start -->
Writes can race with in-flight fills, allowing an obsolete value to arrive
after deletion or update. Test delete, update, partial failure, and delayed-fill
paths. Alert on result age rather than hit rate alone.
<!-- words:targeted-context:end -->

### At depth

<!-- words:targeted-depth:start -->
Record a monotonic content version with each invalidation and fill request.
Before storing, compare the fill's captured version with the current version.
Reject mismatches, count them, and trigger rollback when freshness errors exceed
the rollout threshold.
<!-- words:targeted-depth:end -->
