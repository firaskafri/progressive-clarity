# Mode switching and persistence

- **Expected mode and views:** `Progressive mode` becomes sticky; a one-off At depth request does not change it; the next topic still starts At a glance. `Verbose mode` switches back and later `More` adds At depth only.
- **Required facts:** Mode commands apply before same-message requests; view overrides affect one response; topic changes do not reset mode; Verbose `More` does not replay earlier views.
- **Budgets:** Each At a glance response is at most 40 counted words. In the Verbose response, At a glance plus In context is at most 200.

## User

Progressive mode. Should we enable audit export for the internal pilot? Schema validation passed, rollback is available, and production exposure is out of scope.

## Assistant

### At a glance

<!-- words:mode-progressive-glance:start -->
Enable audit export for the internal pilot. Schema validation passed and rollback is available; production exposure remains out of scope.
<!-- words:mode-progressive-glance:end -->

## User

At depth only: explain how to validate recovery for this pilot.

## Assistant

### At depth

<!-- words:mode-override-depth:start -->
Generate a representative export, interrupt delivery after checkpoint creation, and restore from that checkpoint in an isolated consumer. Compare record identifiers and ordering with the source, then verify that resumption neither skips nor duplicates events.
<!-- words:mode-override-depth:end -->

## User

New topic: Should we move invoice generation to a queue? Job volume doubled, synchronous requests time out, the worker pool is ready, and Finance approval is pending.

## Assistant

### At a glance

<!-- words:mode-sticky-glance:start -->
Move invoice generation to the queue only after Finance approves. Current synchronous timeouts justify the change, and the worker pool is ready.
<!-- words:mode-sticky-glance:end -->

## User

Verbose mode. New topic: Should we activate nightly reconciliation? A 10,000-record dry run matched source totals. Operations owns Monday's rollout. Alert above 0.5% mismatch. One tax-region exception remains unresolved. Rollback disables the scheduler and retains reports for 30 days.

## Assistant

### At a glance

<!-- words:mode-verbose-glance:start -->
Do not activate nightly reconciliation yet. One tax-region exception remains unresolved; proceed only after its expected treatment is verified.
<!-- words:mode-verbose-glance:end -->

### In context

<!-- words:mode-verbose-context:start -->
Operations owns Monday's rollout. Alert when mismatch exceeds 0.5%; rollback disables the scheduler while preserving generated reports for 30 days.
<!-- words:mode-verbose-context:end -->

### At depth

<!-- words:mode-verbose-depth:start -->
The 10,000-record dry run matched source totals. Before approval, rerun the affected tax region and compare duplicate, late-arriving, and corrected invoices separately.
<!-- words:mode-verbose-depth:end -->

## User

More.

## Assistant

### At depth

<!-- words:mode-verbose-more-depth:start -->
Canary one business unit for the first scheduled run. Reconcile its output before widening scope, and retain the manual process until the first full cycle closes without an alert.
<!-- words:mode-verbose-more-depth:end -->
