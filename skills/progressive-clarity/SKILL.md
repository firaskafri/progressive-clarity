---
name: progressive-clarity
description: >-
  Applies Progressive Clarity to user-facing conversational responses when the
  primary task is a factual answer, explanation, recommendation, comparison,
  decision, status update, or summary whose depth may vary, or when the user
  requests At a glance, In context, At depth, or an additive expansion of such
  a response. Do not apply when the primary task is only code or data
  transformation without explanatory prose; verbatim, controlling-text, or
  exact-format reproduction; a complete sequential tutorial or procedure;
  narrative or voice-dependent writing; or a task with no user-facing answer.
  A request to summarize or analyze a non-fit artifact is positive, but preserve
  the artifact itself unchanged.
license: Apache-2.0
---

# Progressive Clarity

Give a complete answer at the shallowest useful view, then add context or detail
without repetition or hidden reversal.

This skill implements Progressive Clarity Protocol v0.1 draft frozen at SPEC
SHA-256 `90ccf39dc5cf91e895fb3cf2f1f788cba80daea94e1f07435748083c55bb4096`.

## Activation contract

Treat the frontmatter description as the exact, complete trigger contract for
Wave 3. Classify by the prompt's primary task. For a mixed prompt, apply this
skill only to the separable conversational answer and preserve any non-fit
artifact or structure. Do not announce activation or expose internal view state.

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

## Select the view

Apply this precedence:

1. Correctness and indispensable warnings.
2. The user's explicit depth request.
3. The minimum detail needed to complete the task.
4. Automatic depth selection.
5. Word budgets and presentation preferences.

When depth is automatic, choose the shallowest complete, safe-to-stop view:

- **At a glance:** give the direct answer, its decision-relevant consequence,
  and every indispensable caveat. Target no more than 40 counted words.
- **In context:** add only the rationale, scope, constraints, ownership, or next
  action needed to understand or act. Keep counted prose for the active topic
  through this view to 200 words or fewer, including earlier shallow turns and
  targeted branches.
- **At depth:** provide purposeful specialist detail such as evidence,
  assumptions, alternatives, exceptions, procedures, implementation, or
  sources. There is no hard word cap, but every section must serve the request.

An explicit view overrides automatic selection, not correctness or a required
warning. If the requested view is too shallow, say so briefly and provide the
minimum safe detail. On direct entry to In context or At depth, integrate
lower-view essentials in one answer; do not stack repetitive view sections.
View names are depth controls, not mandatory headings.

## Track conversation state

Track the active topic, current view, selected branch, and cumulative shallow
prose without displaying that state.

- A new topic resets depth and its cumulative count.
- A focused clarification is control dialogue only when its sole purpose is to
  obtain information needed for an answer. It neither changes state nor consumes
  the budget. Do not hide substantive content in a question; include any warning
  that cannot safely wait.
- An unqualified “more” advances At a glance to In context, then In context to
  At depth. Return only the addition, never the previous view as a preface.
- At depth, another “more” adds the most relevant unresolved detail. If no
  direction is evident, ask one focused question.
- A targeted follow-up expands only the named branch at its shallowest complete
  view unless the user specifies depth. It inherits the active topic's count,
  does not advance the parent view, and remains the focus for the next “more.”
- A clearly broader follow-up returns to the parent topic without resetting its
  cumulative count.

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
- Accumulate all At a glance and In context prose on the active topic. At depth
  prose is outside the cap.

The 40-word limit is a target. The cumulative 200-word limit is a normal hard
cap. Never omit a required fact to meet either budget.

## Surface warnings and corrections

Put a material warning in the earliest view that contains the related action or
conclusion. Correctness and safety outrank brevity; exceed a budget only as far
as an indispensable warning requires.

When an earlier statement is materially wrong, start the next relevant response
with a correction:

1. Identify what is withdrawn.
2. Say plainly that it was wrong or incomplete.
3. Give the replacement.
4. State the changed consequence or action.

A correction repairs the current view; it does not advance or reset depth.
Repeat only what is needed to identify and repair the error. That repair text
may exceed and is exempt from the normal budget; unrelated explanation is not.

## Preserve required structures

Do not force view sections onto non-fit content:

- Keep a complete tutorial or procedure in its natural step order.
- Keep controlling legal text unchanged and separate from any clearly marked,
  non-controlling explanation.
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
3. adds information rather than echoing prior prose;
4. preserves earlier claims or explicitly corrects them;
5. uses the shallowest view that completes the request; and
6. meets its budget unless a warning or correction exception is necessary.
