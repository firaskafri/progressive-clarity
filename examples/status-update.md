# Information update and re-synthesis

The same facts receive different presentations depending on whether the user
only supplies information or asks for revised implications.

## Pure information update

- **Expected presentation:** Focused acknowledgement, with no unsolicited
  re-synthesis.
- **Required facts:** Acknowledge the completion level, blocked clients,
  staging owner, Tuesday testing, and conditional date without changing them.
- **Budget:** The Full-format 40/200 budget does not apply.

### User

Update only: the API migration is 80% complete. Two clients are blocked by a
token-refresh regression. Priya's fix is in staging, client testing completes
Tuesday, and 4 September holds only if both clients pass.

### Assistant

Noted. The migration is 80% complete, with two clients blocked pending Tuesday
tests of Priya's staging fix; 4 September remains conditional on both passing.

## Update requesting implications

- **Expected presentation:** Full, because the user requests material
  re-synthesis against the launch decision.
- **Required facts:** The migration is 80% complete; two clients are blocked;
  4 September is conditional; Priya owns the staging token-refresh fix; client
  testing precedes the launch decision.
- **Budget:** The Full-format 40/200 English budget applies.

### User

The API migration is 80% complete. Two clients are blocked by a token-refresh
regression. Priya owns the fix, which is in staging. Client testing completes
Tuesday, the launch decision is Wednesday, and 4 September holds only if both
clients pass. What does this mean for launch?

### Assistant

#### At a glance

<!-- words:status-glance:start -->
The API migration is 80% complete, but two clients remain blocked. The 4 September target holds only if both clear testing.
<!-- words:status-glance:end -->

#### In context

<!-- words:status-context:start -->
**What shifts:** A token-refresh regression caused the block; Priya's fix is now in staging.

**What follows:** Client validation finishes Tuesday, followed by the launch decision Wednesday.
<!-- words:status-context:end -->

#### At depth

<!-- words:status-depth:start -->
The decision review should compare authentication success, refresh latency, and regression results for both affected clients. If either client fails, publish a revised date with the unresolved failure owner rather than treating partial clearance as launch approval.
<!-- words:status-depth:end -->
