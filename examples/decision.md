# Decision

- **Expected views:** All three views render once in order.
- **Required content:** Preserve the current cadence pending evidence; weekly
  retries can delay recovery; compare costs with recovered revenue; propose an
  analysis and a threshold rather than inventing an approved duration or owner.
- **Budget:** Provisional Advisory targets are 40 words at a glance and 200
  cumulatively through context.

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

**What follows:** Assign an analysis owner and choose a window covering the
billing cycle and recovery lag; define the evidence threshold before testing.
<!-- words:decision-context:end -->

### At depth

<!-- words:decision-depth:start -->
Segment results by decline reason, issuer, customer tenure, and day recovered. Measure net recovered revenue after processing and support costs, then test whether fewer attempts preserve recovery for soft declines. Require a rollback trigger before changing production cadence.
<!-- words:decision-depth:end -->
