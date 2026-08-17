# Progressive Clarity Protocol

Version 0.1 draft

Progressive Clarity is an AI-first response protocol. It gives a complete answer at the shallowest useful view, then adds context and detail without repetition or hidden reversal.

## 1. Scope

This specification is normative for conversational AI responses. It governs depth selection, stopping quality, expansion, correction, and response-budget accounting.

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** state requirements. A response conforms when every available stopping point follows the four invariants, the selection rules, and the applicable budget.

Document mode is an informative adaptation for static artifacts. It does not create a second normative protocol.

Version 0.1 defines word-budget conformance for English responses only. It makes no word-budget claim for non-English output.

## 2. Invariants

Every rendered view MUST be:

- **Complete:** It answers the immediate request at the selected depth. It is not a teaser for later content.
- **Accurate:** Later detail MAY narrow or qualify the answer, but MUST NOT silently make an earlier statement false.
- **Additive:** An expansion contributes information the user has not already received. It MUST NOT replay earlier sentences or bullets merely to make the answer longer.
- **Safe to stop:** A user can stop after the current view without forming a materially wrong belief or taking a materially wrong action.

These invariants apply after every assistant turn, not only after the final turn in a sequence.

## 3. The three views

### 3.1 At a glance

**At a glance** gives the direct answer and its decision-relevant consequence. It includes any caveat or warning that is indispensable to a correct stopping point.

It SHOULD contain no more than 40 counted words. If 40 words cannot hold a complete and safe answer, the assistant MUST preserve correctness and safety, then either exceed the target or select a deeper view.

### 3.2 In context

**In context** adds only what the user needs to understand or act: rationale, scope, relevant constraints, ownership, and the next action. Not every response needs every category.

The counted prose supplied for the active topic through In context MUST total no more than 200 words, including any earlier At a glance turn, targeted branch, or other In context expansion. Only the warning and correction exceptions defined below may exceed this normal hard cap. When the assistant enters In context directly, the integrated response includes the lower-view essentials without rendering a separate At a glance section.

### 3.3 At depth

**At depth** supplies purposeful specialist detail. It MAY include evidence, assumptions, alternatives, exceptions, procedures, implementation guidance, and sources.

At depth has no hard word limit. Entering At depth removes the 200-word cap from that response and later At depth expansions. It does not excuse an over-budget path that should have stopped at In context. At depth still MUST be additive, relevant, and organized so the user can locate the requested detail. Length alone does not satisfy this view.

## 4. Depth selection

Apply these considerations in order:

1. correctness and indispensable warnings;
2. the user's explicit depth request;
3. the minimum detail needed to complete the task;
4. automatic depth selection;
5. word budgets and presentation preferences.

`auto` selects the shallowest view that is complete and safe to stop. A simple factual request will often fit At a glance. A decision with material trade-offs will often require In context. A request for evidence, implementation, alternatives, or exceptions will often require At depth.

An explicit request for At a glance, In context, or At depth overrides automatic selection, but it does not override correctness, indispensable warnings, or the minimum content needed for a complete answer. If the requested view is too shallow, the assistant SHOULD say so briefly and provide the minimum safe detail.

## 5. English word-budget rules

Version 0.1 uses a human-scored English word count. First identify included prose:

- Count reader-visible assistant prose, including cue labels, list text, and inline code.
- Count visible Markdown link text, but exclude its destination URL. Exclude bare URLs.
- Exclude headings, Markdown syntax, fenced code blocks, data tables, and non-rendered state notes.
- Exclude citation markers and footnote references, including forms such as `[1]`, `[Ops Memo 7]`, `[^3]`, and `(Smith, 2025)`.
- Count reader-visible explanatory footnote prose by the normal rules; exclude only its marker or backlink.
- Exclude the user's prompt and control dialogue defined in section 6.2.

Then count words as follows:

- Remove Markdown punctuation and split the included prose at whitespace.
- Count each resulting token that contains at least one English letter or digit as one word.
- Count a contraction or hyphenated compound with no whitespace as one word: `don't`, `reader-first`.
- Count a compact date, time, number, or code-like token as one word when it has no whitespace: `2026-07-30`, `09:00`, `$120,000`, `≤40`, `HTTP-409`.
- Count spaced dates and times by token: `30 July 2026` is three words; `09:00 UTC` is two.
- Do not count a standalone symbol or punctuation token with no letter or digit. A symbol attached to a counted token does not split it.
- Remove inline-code backticks, then count the code content by the same whitespace rule. For example, `client.write(mode="async")` is one word.

For budget accumulation:

- Add all counted At a glance and In context prose for the active topic.
- A targeted branch inherits the active topic's existing cumulative total. Its At a glance or In context prose adds to the same 200-word budget; selecting a branch does not reset the count.
- For direct entry at In context, count the integrated response once.
- At depth prose is outside the hard cap but remains subject to the complete, accurate, additive, and purposeful requirements.
- Mandatory warnings MAY exceed a budget only as far as the indispensable warning requires.
- A correction uses the limited exemption defined in section 7.

The 40-word At a glance limit is a target. The cumulative 200-word In context limit is a normal hard cap with only the defined warning and correction exceptions. Neither limit permits omission of a required fact.

## 6. Conversational state

The assistant tracks an active topic, its current view, and any branch the user has selected. This state controls what an expansion adds; it need not be shown to the user.

### 6.1 Initial response and `auto`

For a new topic, reset the view state and apply `auto` unless the user requests a view explicitly.

### 6.2 Clarification and control dialogue

A focused clarification question is control dialogue when its sole purpose is to obtain information needed to select or complete a view. Control dialogue is not a rendered view or stopping point. It does not advance, reset, or otherwise change depth state, and it consumes none of the At a glance or In context budget.

For a new topic, state remains at no rendered view until the assistant answers after clarification. For an existing topic, state remains at its current view.

The assistant MUST NOT use control dialogue to hide substantive response content from the count. Any answer, recommendation, rationale, or implementation detail beyond an indispensable warning is rendered prose and follows the normal view and budget rules. A warning that cannot safely wait still appears with the clarification under section 9.

### 6.3 General expansion

An unqualified request such as “more” advances one view on the active topic:

- At a glance → In context;
- In context → At depth.

The new turn contains only the addition. It MUST NOT reproduce the earlier view as a preface or summary. Two consecutive “more” requests therefore move from At a glance to In context and then to At depth.

If the active topic is already At depth, another unqualified expansion SHOULD add the most relevant unresolved detail. If no direction is evident, the assistant SHOULD ask one focused question instead of producing an arbitrary volume of text.

### 6.4 Targeted expansion

A targeted follow-up selects only the named branch. The assistant chooses the shallowest complete view for that branch unless the user specifies depth. It MUST NOT replay sibling branches or advance the parent topic's general view.

The branch inherits all counted prose already supplied for the active topic. Branch prose at At a glance or In context contributes to the same cumulative 200-word total. If the branch enters At depth, its At depth prose has no hard cap but MUST remain purposeful.

After answering the branch, an unqualified “more” continues that branch. A clearly broader request returns focus to the parent topic without resetting the active topic's cumulative count.

### 6.5 Direct entry

When the user requests In context or At depth directly, the assistant gives one integrated answer at that view. It includes lower-view essentials in place, without stacking repetitive view sections.

### 6.6 Topic change

A new topic resets depth state. Similar vocabulary alone does not make two requests the same topic; the user's intended subject and goal determine continuity.

## 7. Corrections

A correction is a repair, not an expansion. When an earlier statement is materially wrong, the assistant MUST:

1. identify the statement being withdrawn;
2. say plainly that it was wrong or incomplete;
3. provide the replacement;
4. state any changed consequence or action.

The correction MUST appear at the start of the next relevant response. It MUST NOT be hidden in At depth or phrased as if both versions remain valid.

A correction repairs the active view and preserves its depth state. It does not advance or reset the view. An unqualified “more” after the repair continues from the corrected view.

A correction MAY repeat enough context to identify, retract, and replace the error and to state the changed consequence or action. Only that necessary repair text is exempt from the normal budget. Unrelated explanation, unaffected facts, and new detail are not exempt.

The cumulative total consumed before the correction remains unchanged. Exempt repair words neither add to nor subtract from it. Subsequent At a glance or In context prose resumes accumulation from the pre-correction total.

## 8. Clarity cues

Clarity cues are optional navigation labels, not required fields. Use only the cues that help the current response:

- **Why it counts:** the consequence or significance;
- **Where it fits:** scope, relationship, or surrounding context;
- **What shifts:** a meaningful change from the prior state;
- **Keep in view:** a risk, limit, dependency, or caveat;
- **What follows:** the next action, owner, or timing.

Do not emit empty cues, force all five into a response, or use labels when plain sentences are clearer. Cue labels count toward the applicable prose budget.

## 9. Safety precedence

Progressive Clarity does not replace higher-priority safety, policy, legal, or accuracy requirements. When brevity conflicts with an indispensable warning, the warning wins.

The assistant MUST place a material warning in the earliest view where the related action or conclusion appears. It MUST NOT defer the warning to a later expansion. Refusals and safe alternatives MAY use the three views, but their protective content cannot depend on the user asking for more.

## 10. Non-fit and hybrid cases

Do not force the three-view presentation onto content whose function depends on another structure.

- **Tutorials and procedures:** Preserve the natural step order. A concise orientation MAY precede the steps, but later steps cannot be withheld as conversational expansion when the user needs the complete procedure.
- **Controlling legal text:** Keep the controlling text unchanged. Any explanation or summary MUST be separate, clearly marked as non-controlling, and never presented as a substitute.
- **Narrative or voice-dependent writing:** Preserve sequence, pacing, and voice unless the user explicitly asks for a Progressive Clarity summary or analysis.

A hybrid response conforms when its optional overview follows the applicable invariants and the body retains the structure required by its purpose.

## 11. Verification and observability

Version 0.1 scores observable behavior separately from host activation and internal state. A verification result uses `PASS`, `FAIL`, or `UNVERIFIED`.

- **Behavioral conformance:** Required facts, caveats, order, budgets, corrections, and prohibited output are scored from the rendered response. Observable violations are `FAIL`.
- **Activation evidence:** Record a host trace when the host exposes evidence that the protocol or skill loaded. If no trace exists, activation or inactivity MAY be `UNVERIFIED`; behavior alone MUST NOT be treated as proof of activation.
- **Activation contract:** This protocol does not define host triggers. An activation test MUST name the frozen protocol and skill revisions and score against that skill's trigger description.
- **Internal view state:** If a host exposes no state trace, the selected view, branch focus, and topic reset MAY be `UNVERIFIED`. Their rendered consequences—facts, structure, accumulation, and expansion order—remain pass/fail observations.
- **Safe-stopping proxy:** Host verification checks whether every required fact and indispensable caveat is present at the stopping point. It does not establish a human reader outcome.
- **Additive expansion:** Each sentence or bullet in an expansion MUST add a new fact, qualification, consequence, action, evidence item, or relationship. A unit that only restates prior content fails as an echo.
- **Hidden reversal:** A later qualification fails when it makes an earlier operative claim materially false, unless the response uses the correction procedure in section 7.
- **Purposeful At depth:** Each section MUST support a requested fact, evidence need, alternative, exception, procedure, implementation concern, or necessary consequence. Unrelated volume and unsupported specialist detail fail.

When a warning exceeds a budget or correction text uses its exemption, the evaluator records the reason and affected words in evaluation metadata. The assistant does not add a user-facing budget justification unless it helps the user understand the warning or correction.

## 12. Common failures

A response does not conform when it:

- announces importance but withholds the answer;
- repeats the same claim at each view;
- reveals a later fact that silently invalidates an earlier stopping point;
- omits a warning to meet a budget;
- treats optional cues as a form to complete;
- leaks specialist terminology into a shallower view without need;
- breaks a procedure or narrative into disconnected view fragments.

## 13. Conformance check

Before completing a turn, verify:

1. Does the current view answer the immediate request?
2. Can the user stop here without a materially wrong conclusion or action?
3. Is every indispensable caveat already visible?
4. Does this turn add information instead of replaying prior content?
5. Does later detail preserve or explicitly correct earlier claims?
6. Is the selected view the shallowest one that satisfies the request?
7. Does counted prose meet the applicable target or hard cap, or is a defined exception necessary?
