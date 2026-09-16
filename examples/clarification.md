# Index-enablement clarification gate

- **Expected presentation:** A compact clarification with rationale, then a Focused
  staging decision after the missing inputs arrive.
- **Required facts:** The assistant obtains environment, validation, and
  rollback readiness before recommending activation; pure clarification
  preserves topic state and consumes no budget.
- **Budget:** Control dialogue and the Focused answer have no Full-format budget.

## User

Should I enable the new index now?

## Assistant — control dialogue

Is this staging or production, and have validation and rollback readiness been
confirmed? Those inputs determine whether enablement is supportable.

## User

The environment is staging. Validation passed, and rollback is available.

## Assistant

Those inputs support enabling the index in staging: validation passed and
rollback is available. They do not establish production readiness.
