# Correction

This fictional transcript intentionally begins with a wrong date so the repair
is observable.

- **Expected views:** Both substantive responses contain all three views. The
  repair is the first prose under At a glance.
- **Required repair facts:** Withdraw Tuesday as the production date; replace
  it with Thursday at 09:00 UTC; identify Tuesday as the dry run; move
  production coverage to Thursday.
- **Budget:** Necessary repair prose is exempt. Unaffected and new content
  follows ordinary 40/200 allocation.

## User

When does production maintenance begin?

## Assistant

### At a glance

Production maintenance begins Tuesday at 09:00 UTC. Schedule coverage for that
window.

### In context

The database owner validates backups before cutover.

### At depth

Operations publishes status every 30 minutes during the window.

## User

The runbook says Thursday. Tuesday is only the dry run.

## Assistant — correction

### At a glance

<!-- words:correction-repair:start -->
Earlier I said production maintenance begins Tuesday. That was wrong.
Production begins Thursday at 09:00 UTC; Tuesday is only the dry run. Move
production coverage to Thursday.
<!-- words:correction-repair:end -->

### In context

<!-- words:correction-context:start -->
Use Tuesday for rehearsal support. The incident commander approves Thursday's
cutover after backup validation.
<!-- words:correction-context:end -->

### At depth

<!-- words:correction-depth:start -->
The status cadence remains every 30 minutes during production maintenance.
Record dry-run findings separately so they cannot be mistaken for production
authorization.
<!-- words:correction-depth:end -->
