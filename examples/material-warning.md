# Material warning

- **Expected view:** At a glance, with the warning before any destructive action.
- **Required facts:** Early key deletion can make data unreadable; the old key must remain restricted and available through re-encryption and recovery verification.
- **Budget:** At a glance is at most 40 counted words. Safety would take precedence if the warning required more.

## Prompt

Can I delete the old encryption key immediately after rotating to a new key?

## Response

<!-- words:warning-glance:start -->
No. Deleting the old key before re-encryption and verification can make existing data permanently unreadable. Keep it available, restrict its use, re-encrypt every dependent record, verify recovery, and only then schedule destruction under your key-management policy.
<!-- words:warning-glance:end -->
