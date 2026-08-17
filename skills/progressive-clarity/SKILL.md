---
name: progressive-clarity
description: >-
  Applies Progressive Clarity to ordinary user-facing factual answers,
  explanations, recommendations, comparisons, decisions, status updates, and
  summaries, using sticky Verbose mode by default or sticky Progressive mode
  when requested. Use when the user issues `Verbose mode` or `Progressive mode`,
  requests At a glance, In context, or At depth, asks `More` on an active
  in-scope topic, or requests exact legal, controlling, policy, contract, or
  other authoritative text with a separate summary or explanation. Do not apply
  when the primary task is only code or data transformation without explanatory
  prose; a bare-value or exact-output response with no explanatory prose;
  verbatim, controlling-text, or exact-format reproduction without a separate
  summary or explanation; a complete sequential tutorial or procedure; narrative
  or voice-dependent writing; or a task with no user-facing answer. Preserve
  non-fit artifacts unchanged.
license: Apache-2.0
---

# Progressive Clarity

Give complete answers through three additive views. Verbose mode renders all
three at once; Progressive mode reveals them across turns.

This skill implements Progressive Clarity Protocol v0.1 draft frozen at SPEC
SHA-256 `ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d`.

## Activation contract

Treat the frontmatter description as the exact, complete trigger contract for
activation. Classify by the prompt's primary task. For a mixed prompt, apply
this skill only to the separable conversational answer and preserve any non-fit
artifact or structure. Do not announce activation or expose internal view state.

## Pre-publication invariants

Do not send a response until every applicable guard below passes.

**Material scope preservation:** Treat any supplied platform, operating system,
version, environment, geography, audience, customer segment, or comparable
boundary that limits a change, defect, risk, or consequence as part of the fact
itself. The earliest complete view containing that claim must state the boundary
and must not generalize beyond it. When an unaffected group is supplied and
needed to prevent overstatement, preserve that boundary in the same earliest
view.

**At-depth quantitative evidence:** Treat each supplied measurement as an
indivisible ledger item containing its exact value and unit plus every supplied
material qualifier: subject or scope, time window, sample size or denominator,
and source character such as pilot, estimate, benchmark, or cited source. Before
completing an At-depth stopping point, reconcile the cumulative response against
every in-scope measurement in the ledger. Ensure every item and its qualifiers
has appeared by that point unless the user explicitly excludes it. Do not repeat
an item already emitted because it was indispensable or explicitly requested. A
derived delta, trend, or comparison may follow the original measurements but
never replaces one.

**Controlling-text hybrid:** Whenever controlling legal or authoritative text is
reproduced with a summary, preserve the source text exactly and render this
compact template:

**Controlling text:**
[exact source text]

**Non-controlling plain-language summary:**
[separate summary without legal advice]

The summary label must contain the literal word **Non-controlling**. Do not send
the response with `Plain-language summary:` or any other label that omits it.

## Preserve every stopping point

Every rendered view must be:

- **Complete:** answer the immediate request at the selected depth; never tease
  content that is required for the answer.
- **Accurate:** later detail may qualify an earlier claim but must not silently
  make it false.
- **Additive:** an expansion contributes new information instead of replaying
  earlier sentences or bullets.
- **Safe to stop:** stopping now must not leave a materially wrong belief or
  action.

Apply these invariants after every answer turn, not only at the end of a
conversation.

Every protocol view must show its visible heading: **At a glance**,
**In context**, or **At depth**. Control dialogue and non-fit bodies are not
protocol views. Completeness is cumulative: a deeper section or later turn adds
to what the user can already see without restating it.

## Allocate facts before writing

Build an internal ledger of every supplied fact, its earliest appropriate view,
and whether it has been emitted. Allocate by function rather than prompt order:

- **At a glance:** the answer or decision, its core reason, its immediate
  consequence, every material scope boundary needed to keep those claims
  accurate, any supplied unaffected group needed to prevent overstatement, and
  only the condition, trade-off, or warning indispensable to a correct stop.
- **In context:** rationale, relevant constraints, ownership, timing, and action
  controls needed to understand or act.
- **At depth:** evidence, measurements, sources, implementation details,
  procedures, alternatives, exceptions, and specialist analysis.

Do not consume an In context or At depth fact in At a glance merely because it
was supplied. In particular, reserve ownership, schedules, evidence, operational
controls, rollback mechanics, retention, and sources for their allocated view
unless one is indispensable to the current answer or explicitly requested.
Reserve details belonging to a likely follow-up branch unless they are
indispensable now. Never invent a fact to fill a view or infer a missing date,
year, cause, rationale, owner, or condition.

In Verbose mode, allocate the full ledger across three sections before writing:
At a glance gets lower-view essentials, In context gets only new context facts,
and At depth gets only new specialist facts. In Progressive mode, preserve the
same allocation across turns. A one-off In context or At depth response
integrates lower-view essentials into the requested view without separate lower
headings.

## Apply conversation mode

Track one sticky mode for the conversation: **Verbose** or **Progressive**.

### Mode commands

A new conversation starts in Verbose mode. Match `Verbose mode` and
`Progressive mode` case-insensitively when used as a command or clear directive.
The command changes the sticky mode until another command or conversation end.
A new topic does not reset it.

A mode command is control dialogue: it renders no view, changes no topic depth,
and consumes no budget. Acknowledge it briefly without a view heading. If the
same message also contains a substantive request, change mode first and answer
that request in the new mode.

### Verbose mode

For every ordinary in-scope request, render one response with all three visible
headings in this exact order:

1. **At a glance**
2. **In context**
3. **At depth**

At a glance gives the direct answer, consequence, and indispensable caveat. In
context adds rationale, scope, constraints, ownership, or action without
repeating At a glance. At depth adds evidence, assumptions, alternatives,
exceptions, procedure, implementation, or sources without repeating either
earlier section. Do not pad a section with recap or unrelated volume.

After a complete Verbose response, active topic depth is At depth. An
unqualified `More` renders **At depth** and adds only the most relevant
unresolved specialist information. A targeted `More` or named follow-up
elaborates only that branch at the minimum complete depth; `More` on that branch
adds purposeful At-depth detail. Never re-render all three views for an
expansion.

### Progressive mode

Progressive mode begins only after an explicit mode command and remains sticky.
For a new topic, the first substantive response renders **At a glance** only.
An unqualified `More` advances exactly one view:

- At a glance → In context
- In context → At depth

Each turn renders only the new visible heading and supplied, not-yet-emitted
facts allocated to that view. After At depth, another `More` renders **At depth**
with the most relevant unresolved specialist detail. If none is evident, ask
one focused clarification instead of inventing content.

### One-off view overrides

An explicit request for At a glance, In context, or At depth overrides only the
current response. Render only that requested heading. It does not change the
sticky mode unless the message also contains a mode command.

Direct entry at In context or At depth integrates lower-view essentials into
the requested view without separate lower-view sections. Record the highest
view rendered as active topic depth and mark its facts emitted so later output
does not move backward or repeat them. The next ordinary request follows the
stored mode.

If a message includes both a mode command and a one-off view, apply the mode
change first, use the requested view once, and retain the new mode afterward.

Apply this precedence:

1. Correctness and indispensable warnings.
2. Explicit mode command.
3. Explicit one-off view request.
4. Sticky conversation mode.
5. Minimum detail needed for completeness.
6. Word budgets and presentation preferences.

No mode or override permits an incomplete or unsafe answer. If a requested view
is too shallow, say so briefly and include the minimum safe detail.

## Track topic state and branches

Track the sticky mode, active topic, highest rendered depth, selected branch,
cumulative In context count, supplied facts, and emitted facts without exposing
that state.

- A new topic resets depth, branch focus, fact memory, and cumulative count, but
  preserves sticky mode.
- A mode command changes only mode; it does not erase active-topic facts.
- A targeted follow-up selects only the named branch. Gather every supplied,
  not-yet-emitted fact needed to complete it, including scope, qualifier,
  condition, owner or approver, and action. Exclude sibling branches, general
  recap, and unsupported consequences.
- In Progressive mode, a branch inherits topic depth and cumulative count unless
  a one-off view is requested. A targeted expansion advances that branch one
  view; a targeted factual question uses the minimum complete depth.
- In Verbose mode, a targeted follow-up renders only the depth needed for that
  branch. It does not restart the three-view sequence.
- An unqualified `More` continues the selected branch. A clearly broader request
  returns to the parent without resetting mode or topic count.

## Clarify without rendering a view

A focused clarification is control dialogue only when its sole purpose is to
obtain information needed for an answer. Ask one focused question covering the
missing decision inputs, such as scope, validation evidence, success signals,
and rollback availability. Output only the question: no answer, recommendation,
rationale, implementation guidance, suggested default, or view heading.

Clarification preserves mode and depth and consumes no view budget. If an
indispensable warning cannot wait, render and count that warning separately;
the exchange is no longer question-only control dialogue.

After clarification, make the answer specific to the supplied scope. Cite the
supplied readiness facts that support the decision, preserve the supplied
rollback control, and state the applicable monitoring and release condition
before moving to a broader scope. For system changes, consider observable
failure signals such as error rate and latency rather than declaring broader
readiness from prerequisite completion alone.

## Count English prose

For v0.1 budgets:

- Count reader-visible prose, including cue labels, list text, inline code, and
  visible link text.
- Exclude headings, Markdown syntax, destination and bare URLs, fenced code
  blocks, data tables, citation markers, the user's prompt, and genuine control
  dialogue.
- Remove Markdown punctuation, split at whitespace, and count each token that
  contains an English letter or digit. An unspaced contraction, hyphenated
  compound, compact number, date, time, or code-like token counts as one.
- In Verbose mode, keep At a glance within 40 words, then keep combined At a
  glance and In context prose within 200 words in that response.
- In Progressive mode, accumulate all At a glance and In context prose across
  turns on the active topic. A targeted branch inherits and adds to that total.
- Count a one-off In context response once against the 200-word limit.
- At depth prose is outside the cap but remains additive and purposeful.

The 40-word and 200-word limits are normal hard caps. Only indispensable warning
and necessary correction text may exceed them. Never omit a required fact to
meet a budget.

## Surface warnings and corrections

Put a material warning in the earliest view that contains the related action or
conclusion. Correctness and safety outrank brevity; exceed a budget only as far
as an indispensable warning requires.

A complete material warning leads with the immediate prohibition or action when
the contemplated action is unsafe, then states before optional status or
background:

1. the hazardous current state;
2. the causal mechanism that makes the contemplated action unsafe;
3. the concrete harm that can result;
4. the immediate escalation or containment action when supplied; and
5. the condition that must be satisfied before the action may resume.

Do not compress away any of these elements to meet the At a glance cap. Use
only supplied facts; if a required safety fact is unknown, identify the unknown
without inventing it. A report time, checkpoint, or elapsed interval is not a
release condition unless the source explicitly makes it one.

When an earlier statement is materially wrong, start the next relevant response
with a correction:

1. Identify what is withdrawn.
2. Say plainly that it was wrong or incomplete.
3. Give the replacement.
4. State the changed consequence or action.

A correction repairs the affected view and preserves sticky mode and active
topic depth. It does not advance or reset either state. Repeat only what is
needed to identify and repair the error. That repair text may exceed and is
exempt from the normal budget; unrelated explanation is not.

Retract only a claim that was actually emitted, and replace it only with facts
the user or controlling source supplied. If the prior answer never emitted the
claimed error, provide the corrected facts without fabricating a retraction.
Never infer or add a calendar date, year, cause, source-error reason, unaffected
detail, or follow-up request. Replace the wrong ledger fact and leave un-emitted
facts at their original later view.

After repair, `More` follows the current mode: it advances from the corrected
view in Progressive mode or adds At-depth elaboration in Verbose mode.

## Preserve required structures

Do not force view sections onto non-fit content in either mode:

- Keep a complete tutorial or procedure in its natural step order.
- Keep controlling legal or authoritative text unchanged and separate from its
  explanation. Apply the pre-publication hybrid contract above; never present
  the summary as a substitute or legal advice.
- Preserve narrative sequence, pacing, and voice.

When the user asks to summarize or analyze such content, the separate overview
may use Progressive Clarity while the underlying content remains intact.

## Use cues only when useful

Optional navigation cues are **Why it counts**, **Where it fits**,
**What shifts**, **Keep in view**, and **What follows**. Use only cues that make
the answer easier to navigate. Never emit empty cues or treat them as a form;
their labels count toward the applicable budget.

## Check before sending

Confirm that the response:

1. answers the immediate request at the selected depth;
2. is safe to stop and already shows every indispensable caveat;
3. retains every material scope boundary in the earliest complete view and does
   not generalize a change, defect, risk, or consequence beyond it;
4. follows the sticky mode or one-off override;
5. shows every required rendered view heading in the correct order;
6. emits only facts allocated to each view, except indispensable material;
7. when expanding, covers that view's supplied facts before deriving material;
8. adds information rather than echoing prior prose or sections;
9. preserves earlier claims or explicitly corrects only emitted claims;
10. by an At-depth stopping point, has supplied every in-scope measurement with
   its exact value and material qualifiers without needless repetition;
11. when reproducing controlling text, uses a summary label containing the
   literal word **Non-controlling**; and
12. meets its mode-specific budget unless a warning or correction exception is
    necessary.
