# Progressive Clarity Protocol

Version 0.1 draft

Progressive Clarity is an AI-first response protocol with two conversation modes. Verbose mode renders all three additive views at once. Progressive mode reveals those views across turns.

## 1. Scope

This specification is normative for conversational AI responses. It governs conversation mode, view composition, stopping quality, expansion, correction, and response-budget accounting.

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

View completeness is cumulative. In Verbose mode, the In context stopping point includes At a glance above it, and the At depth stopping point includes both earlier sections. In Progressive mode, the stopping point includes earlier turns on the active topic. Each deeper section remains additive and does not restate those earlier facts.

## 3. The three views

Every rendered view MUST show its heading: **At a glance**, **In context**, or **At depth**. Markdown heading level MAY vary with the surrounding artifact. Headings do not count toward a word budget.

### 3.1 At a glance

**At a glance** gives the direct answer and its decision-relevant consequence. It includes any caveat or warning that is indispensable to a correct stopping point.

It MUST contain no more than 40 counted words. Only an indispensable warning MAY exceed this cap, and only as far as section 9 requires.

### 3.2 In context

**In context** adds only what the user needs to understand or act: rationale, scope, relevant constraints, ownership, and the next action. Not every response needs every category.

The counted prose supplied through In context MUST total no more than 200 words. In Verbose mode, this is the combined At a glance and In context prose in one response. In Progressive mode, it includes earlier At a glance turns, targeted branches, and other In context expansions on the active topic. Only the warning and correction exceptions defined below may exceed this normal hard cap.

### 3.3 At depth

**At depth** supplies purposeful specialist detail. It MAY include evidence, assumptions, alternatives, exceptions, procedures, implementation guidance, and sources.

At depth has no hard word limit. Entering At depth removes the 200-word cap from that response and later At depth expansions. It does not excuse an over-budget path that should have stopped at In context. At depth still MUST be additive, relevant, and organized so the user can locate the requested detail. Length alone does not satisfy this view.

## 4. Conversation modes and view selection

The assistant tracks one sticky conversation mode: **Verbose** or **Progressive**.

### 4.1 Mode state and commands

A new conversation starts in Verbose mode. Starting a new topic inside that conversation does not reset the mode.

The commands `Progressive mode` and `Verbose mode` change the sticky mode. Match them case-insensitively when the user presents the phrase as a command or clear mode directive. A mode command is control dialogue: it does not render a view, advance topic depth, or consume a view budget.

When a message contains both a mode command and a substantive request, change the mode first and use the new mode for that request. The selected mode remains active until another mode command changes it or the conversation ends.

### 4.2 Verbose mode

Verbose mode is the default. For each ordinary in-scope request, the assistant MUST render one response with these visible headings in this order:

1. **At a glance**
2. **In context**
3. **At depth**

At a glance contains the direct answer, consequence, and indispensable caveat. In context adds rationale, scope, constraints, ownership, or action without repeating At a glance facts. At depth adds evidence, assumptions, alternatives, exceptions, procedure, implementation, or sources without repeating facts from either earlier view.

After a complete Verbose response, topic depth is At depth. An unqualified `More` adds purposeful At depth information only. A named `More` request expands only that branch. The assistant MUST NOT replay At a glance, In context, or previously supplied At depth material.

### 4.3 Progressive mode

Progressive mode is explicit and sticky. On a new topic, the first substantive response renders **At a glance** only.

An unqualified `More` advances one view on the active topic:

- At a glance → In context;
- In context → At depth.

Each expansion renders only the new visible view and adds information not already supplied. At depth has no hard cap but remains purposeful. After At depth, another unqualified `More` adds the most relevant unresolved At depth information or asks one focused clarification when no direction is evident.

### 4.4 One-off view overrides

An explicit request for At a glance, In context, or At depth overrides presentation for that response only. It MUST NOT change the sticky conversation mode unless the request also includes a mode command.

A one-off response renders only the requested view heading. Direct entry at In context or At depth integrates the lower-view essentials into that view without rendering separate lower-view sections.

If a message includes both a mode command and one-off view request, apply the mode change first, use the requested view for that response, and retain the new mode afterward.

### 4.5 Selection precedence

Apply these considerations in order:

1. correctness and indispensable warnings;
2. an explicit mode command;
3. an explicit one-off view request;
4. the sticky conversation mode;
5. the minimum detail needed to complete the task;
6. word budgets and presentation preferences.

No mode or one-off override permits an incomplete or unsafe answer. If a requested view is too shallow, the assistant SHOULD say so briefly and provide the minimum safe detail.

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

- In Verbose mode, count At a glance separately against 40 words, then combine its prose with In context prose for the 200-word limit.
- In Progressive mode, add all counted At a glance and In context prose across turns on the active topic.
- A targeted branch in Progressive mode inherits the active topic's existing cumulative total. Its At a glance or In context prose adds to the same 200-word budget; selecting a branch does not reset the count.
- For a one-off In context response, count the integrated response once against the 200-word limit.
- At depth prose is outside the hard cap but remains subject to the complete, accurate, additive, and purposeful requirements.
- Mandatory warnings MAY exceed a budget only as far as the indispensable warning requires.
- A correction uses the limited exemption defined in section 7.

The 40-word At a glance limit and cumulative 200-word In context limit are normal hard caps with only the defined warning and correction exceptions. Neither limit permits omission of a required fact.

## 6. Conversational state

The assistant tracks the sticky mode, active topic, current topic depth, cumulative In context count, facts already supplied, and any selected branch. This state controls composition and expansion; it need not be shown to the user.

### 6.1 Conversation and topic boundaries

A new conversation initializes Verbose mode. A new topic resets topic depth, branch focus, supplied-fact memory, and cumulative count, but preserves the sticky mode.

### 6.2 Clarification and control dialogue

A focused clarification question is control dialogue when its sole purpose is to obtain information needed to select or complete a view. Control dialogue is not a rendered view or stopping point. It does not advance, reset, or otherwise change depth state, and it consumes none of the At a glance or In context budget.

For a new topic, depth remains at no rendered view until the assistant answers after clarification. For an existing topic, mode and depth remain unchanged.

The assistant MUST NOT use control dialogue to hide substantive response content from the count. Any answer, recommendation, rationale, or implementation detail beyond an indispensable warning is rendered prose and follows the normal view and budget rules. A warning that cannot safely wait still appears with the clarification under section 9.

### 6.3 Targeted expansion

A targeted follow-up selects only the named branch and MUST NOT replay sibling branches or the general topic.

In Progressive mode, the branch inherits the active topic's current depth and cumulative count unless the user requests a view explicitly. A request to expand that branch advances it one view; a targeted factual question uses the minimum complete depth. Branch prose through In context contributes to the same 200-word total. An unqualified `More` continues the selected branch.

In Verbose mode, a targeted follow-up adds only the depth needed for that branch; it does not re-render all three views. `More` on a named branch adds purposeful At depth detail to that branch without replaying prior views.

A clearly broader request returns focus to the parent topic. Returning focus does not reset the sticky mode or active topic's cumulative count.

### 6.4 Mode and override continuity

A mode command changes only the sticky mode. It does not erase facts already supplied for the active topic.

A one-off view override changes only the current response's composition, not sticky mode. It records the highest view rendered as the active topic depth so later expansion never moves backward, and it updates supplied-fact memory so later output does not repeat it. The next ordinary request still follows the stored mode.

Similar vocabulary alone does not make two requests the same topic; the user's intended subject and goal determine continuity.

## 7. Corrections

A correction is a repair, not an expansion. When an earlier statement is materially wrong, the assistant MUST:

1. identify the statement being withdrawn;
2. say plainly that it was wrong or incomplete;
3. provide the replacement;
4. state any changed consequence or action.

The correction MUST appear at the start of the next relevant response. It MUST NOT be hidden in At depth or phrased as if both versions remain valid.

A correction repairs the affected view and preserves the sticky mode and active topic depth. It does not advance or reset either state. After repair, an unqualified `More` follows the current mode: it advances from the corrected view in Progressive mode or elaborates At depth in Verbose mode.

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

Do not force the three-view presentation onto content whose function depends on another structure. These exceptions apply in both conversation modes.

- **Tutorials and procedures:** Preserve the natural step order. A concise orientation MAY precede the steps, but later steps cannot be withheld as conversational expansion when the user needs the complete procedure.
- **Controlling legal text:** Keep the controlling text unchanged. Any explanation or summary MUST be separate, clearly marked as non-controlling, and never presented as a substitute.
- **Narrative or voice-dependent writing:** Preserve sequence, pacing, and voice unless the user explicitly asks for a Progressive Clarity summary or analysis.

A hybrid response conforms when its optional overview follows the applicable invariants and the body retains the structure required by its purpose.

## 11. Verification and observability

Version 0.1 scores observable behavior separately from host activation and internal state. A verification result uses `PASS`, `FAIL`, or `UNVERIFIED`.

- **Behavioral conformance:** Required facts, caveats, visible view headings, order, budgets, mode transitions, corrections, and prohibited output are scored from rendered responses. Observable violations are `FAIL`.
- **Activation evidence:** Record a host trace when the host exposes evidence that the protocol or skill loaded. If no trace exists, activation or inactivity MAY be `UNVERIFIED`; behavior alone MUST NOT be treated as proof of activation.
- **Activation contract:** This protocol does not define host triggers. An activation test MUST name the frozen protocol and skill revisions and score against that skill's trigger description.
- **Internal mode and view state:** If a host exposes no state trace, sticky mode, selected view, branch focus, and topic reset MAY be `UNVERIFIED`. Their rendered consequences—headings, facts, structure, accumulation, and expansion order—remain pass/fail observations.
- **Safe-stopping proxy:** Host verification checks whether every required fact and indispensable caveat is present at the stopping point. It does not establish a human reader outcome.
- **Additive composition:** Each sentence or bullet in a deeper Verbose view or later expansion MUST add a new fact, qualification, consequence, action, evidence item, or relationship. A unit that only restates prior content fails as an echo.
- **Hidden reversal:** A later qualification fails when it makes an earlier operative claim materially false, unless the response uses the correction procedure in section 7.
- **Purposeful At depth:** Each section MUST support a requested fact, evidence need, alternative, exception, procedure, implementation concern, or necessary consequence. Unrelated volume and unsupported specialist detail fail.

When a warning exceeds a budget or correction text uses its exemption, the evaluator records the reason and affected words in evaluation metadata. The assistant does not add a user-facing budget justification unless it helps the user understand the warning or correction.

## 12. Common failures

A response does not conform when it:

- announces importance but withholds the answer;
- repeats the same claim at each view;
- omits a rendered view heading;
- treats a one-off view request as a sticky mode change;
- resets the sticky mode when only the topic changes;
- replays all three views after `More` in Verbose mode;
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
6. Does presentation follow the sticky mode or explicit one-off override?
7. Is every rendered view heading visible?
8. Does counted prose meet the applicable target or hard cap, or is a defined exception necessary?
