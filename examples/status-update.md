# Status update

- **Expected views:** All three views render with no fact replay.
- **Required facts:** The migration is 80% complete; two clients are blocked; 4 September is conditional; Priya owns the token-refresh fix; staging validation and client testing precede the launch decision.
- **Budget:** At a glance is at most 40 counted words; At a glance plus In context is at most 200.

## Prompt

Give me a status update: the API migration is 80% complete. Two clients are blocked by a token-refresh regression. Priya owns the fix, which is in staging. Client testing completes Tuesday, the launch decision is Wednesday, and 4 September holds only if both clients pass.

## Response

### At a glance

<!-- words:status-glance:start -->
The API migration is 80% complete, but two clients remain blocked. The 4 September target holds only if both clear testing.
<!-- words:status-glance:end -->

### In context

<!-- words:status-context:start -->
**What shifts:** A token-refresh regression caused the block; Priya's fix is now in staging.

**What follows:** Client validation finishes Tuesday, followed by the launch decision Wednesday.
<!-- words:status-context:end -->

### At depth

<!-- words:status-depth:start -->
The decision review should compare authentication success, refresh latency, and regression results for both affected clients. If either client fails, publish a revised date with the unresolved failure owner rather than treating partial clearance as launch approval.
<!-- words:status-depth:end -->
