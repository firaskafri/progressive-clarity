# Sonnet scoring review — no new inference

This review uses the recorded rc.9 Sonnet outputs and unchanged SPEC.md and
development cases. It does not change instructions, scoring requirements, or
earlier traces. It is an evaluator review, not independent adjudication.

## T15: separate frozen case checks from candidate requirements

The frozen case prohibits invented agreement terms, signing/declining without
inputs, and manufactured three sections. The Sonnet response does none of those.
It requests agreement and decision criteria, without a speculative clause list.
Those named frozen-case checks pass.

The response also says “I'm skipping the three-view format until you supply
them. I'll use it once I have them.” This is explicit format narration and
violates the candidate's silent-application instruction. It is not a permission
request or a task blocker that requires explaining the format. Preserve this
as **candidate silent-application FAIL**, not a frozen-case heading failure.
The agreement description alternative does not establish that a final legal
recommendation could be grounded without the controlling text; that later
decision was not tested.

## T18: verification is not fabrication

The prompt explicitly asks what evidence to confirm before booking. Sonnet
retains all four source-fact groups, recommends the hall from the fallback
requirement, and states that other venue details are unknown.

Requests for written access-route, fallback, event-date, and budget confirmation
are tied to the supplied criteria. “Check that the written agreement states the
items above” requests documentary evidence; it does not assert new contract terms.
The access-route request names no unsupplied ramp, lift, restroom, capacity, fee,
or staffing feature. These passages therefore are **not invented-facility facts**.
Do not score them as fabrication merely because they add verification detail.

If verification instead introduces new venue attributes as established facts,
or turns the task into unrelated facilities/payment/cancellation requirements,
that remains a failure. Supplied budget/date facts must be explicitly retained,
not replaced with uncertainty about whether they hold.

Separate concern: the opening already states the two requirements, both venue
fits, and shared budget/date facts. The In-context table repeats all of those,
and its two bullets repeat the same fallback rationale. No new criterion or
constraint is introduced there. The side-by-side table offers navigation, but
the second view is not predominantly new information as SPEC.md section 4
requires. **Additivity FAIL** is the conservative evaluator judgment for this
capture; correct facts and relevant later evidence do not remove that violation.

## Decision before another paid round

The comparison supports named Sonnet improvements, not stable readiness.
T15 silent application and T18 additivity still fail candidate/spec requirements.
Do not launch a full round on the premise that the targeted round fully passed.
Keep stable acceptance blocked and the experimental distribution scope separate.

Any further inference requires a new bounded plan and an explicit spending cap.
A dollar cap cannot be enforced from these CLI token traces alone; inspect
Cursor billing/usage controls first. No model calls, package rebuilds, release
actions, or instruction edits occurred during this review.
