# Explicit view requests

These are independent one-off requests made while Verbose mode is sticky. Each response renders only the requested view; the stored mode remains Verbose for the next ordinary request.

- **Expected mode and views:** Verbose remains sticky while each explicit view request overrides one response.
- **Required facts:** Pooling is recommended; it reduces setup overhead and caps connections; an oversized pool can increase contention; implementation must use measured limits.
- **Budgets:** At a glance is at most 40 counted words. Direct In context is at most 200 counted words. At depth has no hard cap but remains purposeful.

## At a glance request

### Prompt

At a glance, should we add database connection pooling before traffic increases?

### Response

#### At a glance

<!-- words:explicit-glance:start -->
Yes—add connection pooling before traffic increases. It reduces setup overhead and protects the database from unbounded client connections; set a measured pool limit instead of accepting the library default.
<!-- words:explicit-glance:end -->

## In context request

### Prompt

Answer In context: should we add database connection pooling before traffic increases?

### Response

#### In context

<!-- words:explicit-context:start -->
Adopt connection pooling before traffic increases. It reduces setup overhead and caps concurrent database connections.

**Where it fits:** Add the pool in the application data-access layer; keep database server limits authoritative.

**Keep in view:** An oversized pool can increase contention rather than throughput. Size it from load-test results across all application instances.

**What follows:** Platform engineering measures peak concurrency, sets an initial per-instance cap, and validates timeout behavior in staging.
<!-- words:explicit-context:end -->

## At depth request

### Prompt

Answer At depth: should we add database connection pooling before traffic increases, and how should we implement it?

### Response

#### At depth

<!-- words:explicit-depth:start -->
Adopt connection pooling before traffic increases. The pool should bound aggregate concurrency across every application instance, not merely reduce connection setup time.

**Sizing assumptions**

Start from the database connection ceiling, subtract administrative and migration capacity, then divide the remaining allowance across the maximum instance count. Treat that result as an upper bound, not a performance target.

**Validation**

Load-test representative queries while varying pool size, acquisition timeout, and instance count. Measure query latency, wait time, rejected acquisitions, database CPU, and connection saturation. A larger pool is harmful when wait time moves from the application into database contention.

**Failure behavior**

Set a finite acquisition timeout, surface saturation separately from query failures, and prevent retries from multiplying demand. Confirm that rolling deployments cannot temporarily double the allowed connection total.

**Rollout**

Deploy the measured limit in staging, then enable it for a small production cohort. Increase exposure only while latency and saturation remain within the agreed thresholds. Retain a configuration rollback that does not require a new build.
<!-- words:explicit-depth:end -->
