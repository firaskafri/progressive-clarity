# Clarification control dialogue

- **Expected views:** No rendered view during clarification, then At a glance after the missing facts arrive.
- **Required facts:** The assistant must identify the environment and readiness evidence before recommending activation; clarification must not advance depth or consume budget.
- **Budget:** The clarification question is control dialogue and does not count. The later At a glance response is at most 40 counted words.

## User

Tell me whether to enable the new index now.

## Assistant — control dialogue

Is this staging or production, and have the backfill, query comparison, and rollback path been verified?

## User

Staging. The backfill is complete, query comparison passed, and the rollback switch is available.

## Assistant — At a glance

<!-- words:clarification-glance:start -->
Enable the index in staging. The backfill and query comparison are complete, and rollback is available; monitor error rate and latency before any production decision.
<!-- words:clarification-glance:end -->
