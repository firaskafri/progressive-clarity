# Correction

This fictional transcript intentionally begins with a wrong statement so the required repair is observable.

- **Expected mode and views:** Progressive mode renders At a glance, correction preserves mode and depth, then `More` advances to In context.
- **Required facts in the repair:** Withdraw Tuesday as the production date; replace it with Thursday at 09:00 UTC; identify Tuesday as the dry run; move production coverage to Thursday.
- **Required additions after repair:** Backup validation owner, cutover approval owner, and status cadence.
- **Budget:** The initial At a glance response is at most 40 words. Only necessary repair text is exempt and leaves the prior cumulative count unchanged. The later In context addition resumes that count and keeps the total at most 200 words.

## User

Progressive mode. When does production maintenance begin? The database owner validates backups before the production window, the incident commander approves cutover, and operations publishes status every 30 minutes.

## Assistant

### At a glance

<!-- words:correction-glance:start -->
Production maintenance begins Tuesday at 09:00 UTC. Schedule coverage for that window.
<!-- words:correction-glance:end -->

## User

The runbook says Thursday. Tuesday is only the dry run.

## Assistant — correction

<!-- words:correction-repair:start -->
Earlier I said production maintenance begins Tuesday. That was wrong.

Production maintenance begins Thursday at 09:00 UTC; Tuesday is only the dry run. Schedule production coverage for Thursday and use Tuesday for rehearsal support.
<!-- words:correction-repair:end -->

## User

More.

## Assistant

### In context

<!-- words:correction-context:start -->
**What follows:** The database owner validates backups before Thursday's window. The incident commander approves cutover, and operations publishes status updates every 30 minutes.
<!-- words:correction-context:end -->
