# Decision

- **Expected mode and views:** Default Verbose mode renders all three views once.
- **Required facts:** Retain daily retries; weekly retries delay recovery; costs must be compared with recovered revenue; the billing owner runs a four-week analysis; any change requires a defined threshold.
- **Budget:** At a glance is at most 40 counted words; At a glance plus In context is at most 200.

## Prompt

Should we replace three daily billing retries with one weekly retry to reduce processor fees?

## Response

### At a glance

<!-- words:decision-glance:start -->
Keep three daily retries for now. A weekly attempt delays recovery from transient payment failures and may increase involuntary churn.
<!-- words:decision-glance:end -->

### In context

<!-- words:decision-context:start -->
**Where it fits:** This decision concerns retry cadence only; payment-method reminders can be evaluated separately.

**Keep in view:** Daily attempts may raise processor fees and customer contacts. Compare those costs with recovered revenue before changing cadence.

**What follows:** The billing owner runs a four-week cohort analysis and proposes a threshold for any change.
<!-- words:decision-context:end -->

### At depth

<!-- words:decision-depth:start -->
Segment results by decline reason, issuer, customer tenure, and day recovered. Measure net recovered revenue after processing and support costs, then test whether fewer attempts preserve recovery for soft declines. Require a rollback trigger before changing production cadence.
<!-- words:decision-depth:end -->
