# Two consecutive expansions

- **Expected views:** At a glance → In context → At depth.
- **Required facts at first stop:** Delay the release; the reliability gate is missed; review is pending.
- **Required additions at second stop:** Affected users, failure rate, owner action, and reassessment condition.
- **Required additions at third stop:** Validation dimensions, rollout controls, and the hold condition.
- **Budgets:** At a glance is at most 40 counted words. At a glance plus the In context addition is at most 200 counted words. At depth has no hard cap but remains purposeful.

## Initial prompt

Should we delay the mobile release? Crash-free sessions are 98.7%, our gate is 99.5%, the fix is ready, and review is tomorrow.

## Assistant — At a glance

<!-- words:two-more-glance:start -->
Delay the release. Crash-free sessions are below the 99.5% gate, and the fix has not completed review. Reassess after tomorrow's review instead of waiving the reliability threshold.
<!-- words:two-more-glance:end -->

## User

More.

## Assistant — In context addition

<!-- words:two-more-context:start -->
**Where it fits:** The gate protects all users, while the known defect affects session startup on older devices.

**Keep in view:** The current 98.7% rate represents about 13 failed sessions per 1,000; release timing does not justify that regression.

**What follows:** Mobile engineering completes review and targeted device tests tomorrow. The release owner then compares the new crash-free rate with the existing gate.
<!-- words:two-more-context:end -->

## User

More.

## Assistant — At depth addition

<!-- words:two-more-depth:start -->
Validate the candidate against the same telemetry window and device mix used to define the gate. Segment startup crashes by OS version, model, and cold versus warm launch. Check confidence intervals, sample size, and whether retries mask user-visible failures.

If the candidate passes, retain a phased rollout with automated rollback. If it misses, document the residual failure mode and hold shipment until a new candidate is measured.
<!-- words:two-more-depth:end -->
