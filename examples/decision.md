# Decision

- **Expected view:** In context, entered directly because the decision needs a trade-off and an owner action.
- **Required facts:** Retain daily retries for now; weekly retries delay recovery; costs must be compared with recovered revenue; the billing owner runs the analysis.
- **Budget:** The integrated In context response is at most 200 counted words.

## Prompt

Should we replace three daily billing retries with one weekly retry to reduce processor fees?

## Response

<!-- words:decision-context:start -->
Keep three daily retries for now. A weekly retry lengthens recovery from transient failures and may increase involuntary churn.

**Where it fits:** This decision concerns retry cadence only; payment-method reminders can be evaluated separately.

**Keep in view:** Daily attempts may raise processor fees and customer contacts. Compare those costs with recovered revenue before changing cadence.

**What follows:** The billing owner runs a four-week cohort analysis and proposes a threshold for any change.
<!-- words:decision-context:end -->
