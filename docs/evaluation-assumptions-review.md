# Evaluation assumptions and Cursor host review — 2026-10-21

This review adds no inference, candidate revision, or acceptance claim. It
compares frozen specification/case expectations with rc.6 raw captures. Earlier
outputs and assessments remain historical; the caveats below qualify their
interpretation rather than silently replacing failures with passes.

A subsequent [minimal diagnostic round](prerequisite-diagnostics.md) used a
separate three-case fixture with unchanged rc.6. Its named decision checks passed;
headless question handling and interaction quality remain limited. The review
below and original frozen suite/results are preserved.

## T06: ambiguous object and an overdetermined expected answer

The first prompt is only “Should I enable the index now?” The second supplies
staging, passed validation, and available rollback, without identifying the index
or declaring those the exhaustive prerequisites. The rubric nevertheless expects
enablement in staging and a staging-not-production approval distinction.

The frozen specification requires the smallest decisive missing inputs, not a
fixed environment/validation/rollback checklist for every meaning of “index.”
Database, IDE, and remote-data indexing can have different decisive requirements.
Asking which index is meant is therefore legitimate; withholding a definitive
yes after turn 2 is not, by itself, evidence of unnecessary clarification.

Problems still observed: the response offers IDE/workspace-based advice while
the object is unknown, and conditional “enable anytime” advice uses insufficient
privacy/permission evidence. Those should be judged separately from the test's
presumed staging enablement. No safe general recommendation is established.

The rc.6 first-turn raw trace also contains `askQuestionToolCall`, asking index
type, environment, and sensitivity. Its result is rejected with:

> Questions skipped by the user, continue with the information you already have

The noninteractive runner did not provide an answer or explicitly skip questions.
This is a captured host/tool behavior, not evidence that the human evaluator chose
to skip them. The host event may affect subsequent generation; causality is not
established. Prior visible-Markdown summaries omitted this interaction detail.
Do not equate headless tool rejection with a completed human clarification exchange.

For a future revised development case, identify the action class (for example,
a specified database index change) while leaving readiness unknown. In the
second turn, explicitly declare the readiness inputs sufficient for the bounded
decision. Keep a separate genuinely ambiguous-object case where identifying the
object is a valid clarification. Neither revised case would be an unseen holdout.

## T02: frozen-suite expectations versus candidate-specific restrictions

T02 supplies a candidate below a reliability gate and requests presentation,
remediation, and reconsideration evidence. Its prohibited behavior is protocol
headings in the one-sentence turn and invented reliability measurements in Full.
It does not say the gate is mandatory, exceptions forbidden, or what waiver
authority exists. The frozen specification prioritizes policy and accuracy but
does not explicitly forbid mentioning a conditional policy change.

rc.6 adds a stricter rule: discuss exception routes only with supplied authority.
Its response fails that candidate-specific restriction by introducing an approval
route. That is not automatically a frozen-T02 failure. Conditional “if an approved
waiver exists” is different from asserting that leadership has authority to grant
one; these passages need separate semantic judgment. The detailed invented
accountable-owner path remains an unsupported-policy concern.

Earlier T02 FAIL labels therefore combine candidate-specific and frozen-suite
criteria. They must not be presented as clean frozen-rubric scores. Frozen-suite
policy semantics remain UNVERIFIED pending independent adjudication, not PASS.
T11 supplies an explicit mandatory prohibition and is a stronger existing test
of known-blocker behavior; rc.6 passed its bounded contract.

## T15: separate the contract from clarification quality

rc.6 withheld signing/declining and avoided three-view headings despite the Full
request. Those observable contract checks passed. Its long input request is a
separate proportionality/smallest-input concern, not evidence that it authorized
signing or invented actual agreement clauses. Overall clarification quality stays
UNVERIFIED without an independently applied semantic standard.

## Host and scope conclusions

Cursor's coding orientation is visible in workspace searches and interpretations
of project names/indexes, but the traces do not prove an immutable host bias or
identify its hidden system prompt. Empty synthetic workspaces and headless question
handling are part of the tested integration. Results do not transfer automatically
to interactive Cursor, ChatGPT, Claude, or a generic model API.

The canonical skill grew from 5,611 bytes in published 0.5.0 to 11,084 bytes in
rc.6. Added text is not evidence of better behavior. Stop instruction expansion
until rubric/host ambiguities are addressed.

Recommended next sequence:

1. Keep rc.6 unchanged and unpublished. Keep frozen cases/hashes intact.
2. Independently review policy and clarification judgments; report candidate-rule
   violations separately from frozen-suite scores. Do not claim current totals
   are independently adjudicated conformance rates.
3. Define a separate revised development suite with an explicit action class,
   sufficient bounded prerequisites, and specified policy authority. Preserve the
   old suite and results; do not relabel revised cases as unseen.
4. Decide whether to test interactive question handling or a documented headless
   clarification path. Retain skipped/rejected tool outcomes explicitly.
5. Only then authorize a frozen diagnostic run or candidate change. A full new
   round and genuinely independent cases remain prerequisites for broad claims.

No code, frozen suite, skill bytes, published artifact, or marketplace pin changed
during this review. This is an audit of evidence interpretation, not a fix.
