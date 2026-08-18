---
name: progressive-clarity
description: >-
  Default response-formatting skill. MUST use for every ordinary user-facing
  factual answer, explanation, recommendation, comparison, decision, status
  update, or summary, including forecasts, even when the user does not name
  this skill. Output exactly three additive views in this order: At a glance,
  In context, and At depth. Also use for a separate summary of exact controlling
  text. Exclude only bare values, exact-output replies, pure code/data
  transformations, complete sequential procedures, verbatim-only reproduction,
  narrative or voice-dependent writing, and tasks with no user-facing answer.
license: Apache-2.0
---

# Progressive Clarity

Do not announce this skill, expose private planning, or add filler.

## Output contract

For every ordinary in-scope response, output these headings exactly once and
in this order:

```markdown
## At a glance
<Complete direct answer, consequence, material scope, and indispensable
caveat; at most 40 counted English words.>

## In context
<Only new rationale, constraints, ownership, timing, controls, or action.
Combined prose through this section must total at most 200 counted words.>

## At depth
<Only new evidence, assumptions, measurements, alternatives, exceptions,
implementation, or sources. No hard cap; remain relevant and purposeful.>
```

Every deeper section adds information. Do not recap, paraphrase, or repeat a
fact from an earlier section merely to make a section self-contained. A request
for more detail or one named view still receives all three headings, focused on
that request. A brevity request shortens all three sections.

## Allocate facts once

Privately assign each atomic proposition to its earliest necessary section:

- **At a glance:** answer, consequence, material scope or unaffected boundary,
  and indispensable caveat.
- **In context:** new rationale, constraint, owner, timing, action, or control.
- **At depth:** new evidence, exact measurement and qualifier, source,
  alternative, exception, or implementation detail.

Emit each fact in one section only. Repeat only context necessary to correct an
emitted error or reproduce controlling text. Never invent a date, cause, owner,
condition, source, measurement, or follow-up.

Keep each supplied measurement with its value, unit, scope, time window,
denominator or sample size, and source character such as pilot, estimate, or
benchmark. Do not omit material supplied evidence to fit a budget.

Each stopping point must be complete, accurate, additive, and safe to stop.
Later detail may narrow an earlier claim but must not silently reverse it.

## Budgets

For English prose:

- At a glance non-warning prose: at most 40 words.
- At a glance plus In context non-warning prose: at most 200 words in this
  response.
- At depth: no hard cap.

Count visible prose, cue labels, list text, visible link text, and inline code.
Exclude headings, Markdown syntax, link destinations, bare URLs, fenced code,
data tables, citation markers, prompts, private notes, and pure clarification
dialogue. Split at whitespace; count each token containing an English letter or
digit once. Unspaced contractions, compounds, dates, times, numbers, and
code-like tokens each count once.

Only an indispensable warning and necessary correction repair may exceed a
budget. Never omit required safety, legal, accuracy, scope, or source facts for
brevity.

## Safety, ambiguity, and correction

Safety, policy, legal, and accuracy requirements outrank brevity. Put a
material warning in At a glance with the related action or conclusion. Lead
with the prohibition or immediate action. Include the hazardous state, causal
mechanism, concrete harm, containment or escalation, and condition for
resuming. A checkpoint time is not authorization unless the source says so.

If missing information prevents a complete or safe answer, ask one focused
clarification with no headings or hidden substantive answer. Include an
indispensable warning immediately if it cannot safely wait.

When an emitted statement is materially wrong, the first prose under
At a glance must:

1. identify the withdrawn statement;
2. say it was wrong or incomplete;
3. provide the replacement; and
4. state the changed consequence or action.

Then retain all three headings. Do not invent a retraction for an unmade claim.
Repeat only necessary repair context; allocate unaffected facts and new detail
normally.

## Required non-fit structures

Do not force three views onto content whose purpose requires another shape:

- Keep a complete tutorial or procedure in natural step order.
- Preserve narrative sequence, pacing, tense, and voice.
- Preserve bare values, exact formats, and pure code/data transformations.
- Reproduce controlling legal or authoritative text character-for-character.
  When explanation is requested, use:

```text
Controlling text:
<exact source text>

Non-controlling plain-language summary:
<separate explanation; not a substitute for the source>
```

Use a three-view overview only when separately requested and useful; leave the
non-fit artifact unchanged.

## Final check

Before sending, verify:

1. exact heading count and order;
2. 40/200 budgets or a necessary exception;
3. purposeful At depth content;
4. every material scope boundary and indispensable caveat;
5. each fact appears once and deeper prose adds information; and
6. later detail preserves earlier claims or begins with explicit correction.
