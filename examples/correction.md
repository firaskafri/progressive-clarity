# Narrow and material corrections

These fictional transcripts begin with an emitted error so each repair is
observable.

## Narrow correction

- **Expected presentation:** Focused, because the repair changes one local
  command consequence without re-synthesizing the topic.
- **Required repair facts:** Withdraw the claim that the command discards
  working-tree edits; say it was wrong; state that the command only unstages
  the path; remove the unnecessary copy-first action.
- **Budget:** The Full-format 40/200 budget does not apply.

### User

If I run `git restore --staged README.md`, what happens to my working-tree
edits?

### Assistant

It unstages `README.md` and discards its working-tree edits, so copy them first.

### User

That command does not discard working-tree edits.

### Assistant — correction

Earlier I said `git restore --staged README.md` discards the file's working-tree
edits. That was wrong or incomplete. It only unstages the path; your
working-tree edits remain. This changes the action: no copy is required first.

## Material correction

- **Expected presentation:** The initial date answer is a Focused simple fact.
  The schedule correction is Full because it changes the operative action; its
  repair is the first prose under At a glance.
- **Required repair facts:** Withdraw Tuesday as the production date; replace
  it with Thursday at 09:00 UTC; identify Tuesday as the dry run; move
  production coverage to Thursday.
- **Budget:** Necessary repair prose is exempt. Unaffected and new Full content
  follows the 40/200 allocation.

### User

When does production maintenance begin?

### Assistant

Production maintenance begins Tuesday at 09:00 UTC. Schedule coverage for that
window.

### User

The runbook says Thursday at 09:00 UTC. Tuesday is only the dry run. Backup
validation gates production cutover, and operations posts status every 30
minutes during production.

### Assistant — correction

#### At a glance

<!-- words:correction-repair:start -->
Earlier I said production maintenance begins Tuesday. That was wrong or
incomplete. Production begins Thursday at 09:00 UTC; Tuesday is only the dry
run. This changes production coverage to Thursday.
<!-- words:correction-repair:end -->

#### In context

<!-- words:correction-context:start -->
Use Tuesday for rehearsal support. Backup validation gates Thursday's cutover.
<!-- words:correction-context:end -->

#### At depth

<!-- words:correction-depth:start -->
The status cadence remains every 30 minutes during production maintenance.
Record dry-run findings separately so they cannot be mistaken for production
authorization.
<!-- words:correction-depth:end -->
