# Clarification control dialogue

- **Expected views:** No view renders until missing facts arrive; then all three views render.
- **Required facts:** The assistant identifies environment and readiness before recommending activation; pure clarification preserves topic state and consumes no budget.
- **Budget:** Control dialogue does not count. At a glance is at most 40 words; At a glance plus In context is at most 200.

## User

Tell me whether to enable the new index now.

## Assistant — control dialogue

Is this staging or production, and have the backfill, query comparison, and rollback path been verified?

## User

Staging. The backfill is complete, query comparison passed, and the rollback switch is available.

## Assistant

### At a glance

<!-- words:clarification-glance:start -->
Enable the index in staging. Readiness checks passed and rollback is available; do not treat this as production approval.
<!-- words:clarification-glance:end -->

### In context

<!-- words:clarification-context:start -->
**Where it fits:** Staging limits exposure to internal validation.

**What follows:** Assign an activation owner and observation window before switching traffic.
<!-- words:clarification-context:end -->

### At depth

<!-- words:clarification-depth:start -->
Capture baseline query latency and plans before activation. Define rollback thresholds for errors and latency, then compare representative traffic after the switch. Preserve the previous index until the observation window closes.
<!-- words:clarification-depth:end -->
