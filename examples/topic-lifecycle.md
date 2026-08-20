# Topic lifecycle

This fictional transcript demonstrates the primary Advisory cadence on one
continuing release-decision topic:

1. a simple fact uses Focused format;
2. the first consequential, orientation-capable answer uses Full format;
3. a narrow follow-up returns to Focused format; and
4. an accumulated team summary uses Full format.

The 40/200 English budget applies only to the two Full responses.

## Turn 1 — simple fact

### User

Our mobile release gate is 99.5% crash-free sessions. Is 98.7% below it?

### Assistant

Yes. 98.7% is 0.8 percentage points below the 99.5% gate.

## Turn 2 — first consequential orientation

### User

The missed sessions come from startup crashes on older devices. A fix is ready,
but review is tomorrow. Should we release tonight?

### Assistant

#### At a glance

<!-- words:lifecycle-orientation-glance:start -->
Delay tonight's release. The current result misses the reliability gate, and
the fix has not passed review; reassess after tomorrow's review.
<!-- words:lifecycle-orientation-glance:end -->

#### In context

<!-- words:lifecycle-orientation-context:start -->
Limit validation to the affected older-device startup cohort and assign one
release owner to record the go/no-go decision.
<!-- words:lifecycle-orientation-context:end -->

#### At depth

<!-- words:lifecycle-orientation-depth:start -->
Segment results by operating-system version and device age, verify cold-start
and restored-session paths, and retain a rollback trigger tied to post-release
crash-free sessions.
<!-- words:lifecycle-orientation-depth:end -->

## Turn 3 — narrow follow-up

### User

What should the reviewer check first?

### Assistant

Reproduce the startup crash on the affected older-device cohort, then confirm
the candidate prevents it on the same cold-start path before broad regression
testing.

## Turn 4 — accumulated summary

### User

Summarize the decision for the release team.

### Assistant

#### At a glance

<!-- words:lifecycle-summary-glance:start -->
Do not release tonight. Crash-free sessions are 98.7%, below the 99.5% gate;
reconsider after tomorrow's fix review.
<!-- words:lifecycle-summary-glance:end -->

#### In context

<!-- words:lifecycle-summary-context:start -->
The failure is concentrated in startup on older devices. The reviewer first
reproduces that path, then tests the candidate on the same cohort.
<!-- words:lifecycle-summary-context:end -->

#### At depth

<!-- words:lifecycle-summary-depth:start -->
The release owner records cohort results and the go/no-go outcome. Any approved
rollout retains a rollback trigger tied to post-release crash-free sessions; a
failed candidate gets a revised date rather than a gate waiver.
<!-- words:lifecycle-summary-depth:end -->
