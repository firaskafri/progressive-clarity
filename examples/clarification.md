# Index-enablement clarification gate

- **Expected presentation:** One clarification question only, then a Focused
  staging decision after the missing inputs arrive.
- **Required facts:** The assistant obtains environment, validation, and
  rollback readiness before recommending activation; pure clarification
  preserves topic state and consumes no budget.
- **Budget:** Control dialogue and the Focused answer have no Full-format budget.

## User

Should I enable the new index now?

## Assistant — control dialogue

Which environment is this, and have validation and rollback readiness been confirmed?

## User

The environment is staging. Validation passed, and rollback is available.

## Assistant

Enable the index in staging. Validation passed and rollback is available; this
is staging authorization only, not production approval.
