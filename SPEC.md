# Progressive Clarity Protocol

Version 0.5 draft

Progressive Clarity is a topic-oriented response protocol: orient when useful,
explore naturally, and re-synthesize when decisions or context materially change.
Structure serves comprehension; consequential answers may be short.

## 1. Scope and profiles

This specification governs conversational factual answers, explanations,
recommendations, comparisons, decisions, status updates, and summaries.
**MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.
Document adaptation is informative. Word-budget claims apply to English only.

- **Advisory conversational profile:** the model infers topic continuity and
  useful presentation from visible context. The canonical skill and packaged
  skills are prompt-only. Their activation and conformance are probabilistic.
- **Mechanical wrapper profile:** a trusted caller supplies topic action, turn
  classification, whether distinct depth is useful, and presentation preference.
  The wrapper verifies the selected structure and state transition. It does not
  establish the semantic correctness of those classifications.

Version 0.5 revises the v0.4 behavior contract. Earlier results are historical;
they do not establish current conformance or reader benefit. Package target:
`0.5.0`. Wrapper requests use schema `4.0.0`; envelope and state shapes remain
`3.0.0`, with protocol `0.5`. Earlier protocol state is rejected.

## 2. Universal response requirements

Every governed response MUST:

- answer the immediate request directly and completely for its purpose;
- preserve accuracy, material scope, uncertainty, and supplied evidence qualifiers;
- distinguish established facts from assumptions and prospective advice;
- place indispensable caveats beside the claims or actions they qualify;
- put safety, policy, legal requirements, and accuracy ahead of brevity; and
- explicitly repair an emitted error rather than silently reversing it.

At each cumulative stopping point, the reader MUST receive a non-misleading
answer within its stated scope. A decision summary need not contain a complete
implementation procedure, but MUST NOT imply permission to execute while hiding
prerequisites later. Requested procedures MUST be complete and ordered.
Whether a human understood or acted safely remains an empirical outcome, not a
property certified by formatting or fact declarations.

Supplied measurements SHOULD retain value, unit, scope, time window, denominator
or sample size, and source character such as pilot, estimate, or benchmark.
Material evidence MUST NOT be silently discarded to meet a length preference.

## 3. Topic and presentation selection

### 3.1 Topic continuity

Continue while the objective or prior context needed to answer remains relevant.
Recognize explicit topic switches; acknowledgements and formatting instructions
normally stay in the current topic. A targeted follow-up selects its branch
without an unrequested general recap. Return to earlier topics when visible
context supports it. When uncertain, prefer a Focused answer.

Prompt-only continuity is best-effort. The wrapper receives `start` for an
unknown topic, `continue` for the active topic, and `resume` for a known inactive
topic. Invalid transitions MUST fail before generation.

### 3.2 Authoritative presentation decision table

Apply the rows in priority order. Requirements for warnings, corrections, and
assumptions govern content within the selected shape; they do not introduce a
competing Full-format trigger.

| Priority | Situation | Required behavior |
| --- | --- | --- |
| 1 | Safety, accuracy, policy, or legal requirement conflicts with brevity | Include indispensable content immediately; exceed a length preference only as needed. |
| 2 | Exact artifact, quotation, transformation, narrative, or complete procedure | Preserve its functional shape and exact bytes where required. A requested explanation is separate. |
| 3 | Missing input blocks the requested recommendation | Ask for the smallest decisive input set, optionally with brief rationale or supported bounded advice. Do not authorize the blocked action. |
| 4 | Explicit all-three, brief/no-headings, or named-view request | Use Full, Focused, or Focused at the named depth respectively. |
| 5 | First consequential orientation or meaningful checkpoint with useful distinct layers | Use Full. |
| 6 | Compact consequential answer, simple fact, acknowledgement, ordinary follow-up, or uncertain depth benefit | Use Focused. |

The following combinations resolve using the same table:

| Combination | Resolution |
| --- | --- |
| No headings + material warning | Focused; put the complete indispensable warning first. |
| Missing numeric input + no defensible example | Ask for the input or give a supported formula; do not manufacture a number. |
| Exact artifact + explanation | Preserve the artifact; separate the explanation without injecting headings into the artifact. |
| Correction + procedure | Identify and repair the affected step, then preserve the complete requested sequence. |
| Full request + insufficient factual basis | Clarify the decisive input; do not invent three sections. |
| Full request + short but answerable topic | Honor all three views with proportionate grounded detail; do not pad. |
| Hazard + missing implementation details | Give the known containment or warning immediately; ask only for details needed for the remaining answer. |

An answer benefits from distinct layers when the decision, its rationale or
constraints, and specialist evidence or implementation each provide useful
content that would be harder to navigate as one compact answer. Importance or a
yes/no decision alone is insufficient. Full SHOULD NOT be used merely to fill
three slots. A checkpoint may be a decision, accumulated-context summary,
material re-synthesis, or correction; it still requires the usefulness judgment.

A pure update SHOULD receive a brief acknowledgement without inventing changes
to other conditions. Requested implications warrant synthesis at an appropriate
length. A clarification reply continues the pending request and does not create
a new first orientation. Explaining a plan follows this table; writing or
executing its procedure preserves the procedure's natural order.

### 3.3 Focused format

Lead with the answer and use only structure helpful for the immediate request.
Reserved view headings SHOULD be omitted unless explicitly requested. Ordinary
headings, lists, code, and tables MAY be used. There is no protocol word cap.
Simple facts SHOULD normally take one to three sentences, without unrequested
adjacent use-case catalogues. Longer content must earn its place.

### 3.4 Full format

Render exactly these headings, once and in order. The canonical renderer uses
level-two Markdown headings:

1. **At a glance:** the answer, decision-relevant consequence, material scope,
   and indispensable caveat.
2. **In context:** useful rationale, constraints, ownership, timing, or next action.
3. **At depth:** purposeful evidence, assumptions, alternatives, exceptions,
   implementation, measurements, or sources.

For English, 40 non-warning words at a glance and 200 cumulatively through
context are **provisional Advisory targets** and **Mechanical hard caps**.
Warnings and necessary correction repair are separately counted and exempt only
as needed. At depth has no hard cap. Length alone never establishes useful depth.

## 4. Additive composition and useful repetition

Every deeper Full view MUST be predominantly new information. Brief repetition
MAY connect reasoning, materially improve comprehension, or keep an action
properly qualified, including restating a complete proposition when necessary.
Names, dates, identifiers, and short anchors may recur naturally.

Duplicated explanations, repeated lists, and automatic closing recaps SHOULD
be removed. A recap is justified only by a concrete reader need or explicit
request, not by a habit of ending every answer with a summary. A semantic review
of repetition MUST identify the repeated passage and explain why it adds no
useful connection or qualification; lexical identity alone is insufficient.

For example, after “Keep writes frozen during recovery,” a deeper section may
say “With writes still frozen, compare the transaction logs” to qualify an action.
Repeating the whole recovery explanation under every heading adds no value.

Composition SHOULD start with the answer, then add needed rationale and depth,
then remove filler and unhelpful duplication. No particular private drafting
workflow or proposition ledger is required.

## 5. English word accounting and visible reading cost

### 5.1 Deterministic budget counter

The Mechanical profile retains the v0.4 algorithm for reproducible counts.
Normalize CRLF and bare CR to LF, then:

1. Exclude fenced code blocks opened by at least three backticks or tildes after
   no more than three leading spaces and closed by at least the opening marker
   length of the same character.
2. Exclude ATX headings. Exclude a Setext heading and its immediately following
   `===` or `---` underline.
3. Exclude a GitHub-style data table when a pipe-containing header is followed by
   a pipe-containing delimiter row whose two or more cells each match
   `:?-{3,}:?`. Exclude contiguous following non-empty pipe-containing rows.
4. Remove Markdown images including alt text and destination/reference label.
   Replace links with visible text. Remove reference destination definitions,
   autolinks, and bare URLs.
5. Remove footnote-reference markers and backlinks; retain explanatory footnote
   prose after its definition marker.
6. Remove citation markers consisting of bracketed numeric references/ranges,
   textual bracket labels ending in a separate one-to-four-digit reference
   number, or parenthetical author-date markers with a comma followed by a year
   from 1900 through 2099.
7. Remove HTML comments/tags and leading blockquote, list, or task markers.
   Delete these Markdown punctuation characters without inserting whitespace:
   backslash, backtick, `*`, `_`, `{`, `}`, `[`, `]`, `(`, `)`, `#`, `+`, `.`,
   `!`, `>`, `|`, `~`, and `-`.

Split remaining prose at Unicode whitespace. Count each token containing an
ASCII letter or digit as one word. Attached punctuation does not split tokens;
unspaced contractions, hyphenated compounds, dates, times, and code-like tokens
count once. Standalone symbols do not count. Visible labels, link text,
inline-code content, list text, and explanatory footnotes are included.

### 5.2 Reading cost is separate

The counter excludes material that still costs attention: tables, code, headings,
and exempt warnings. Authors MUST NOT move prose into excluded structures to
evade budgets. Review the whole rendered answer for visible bulk, density,
navigation, and whether qualifications can be found before acting.

Implementations SHOULD report supplemental rendered character and non-empty-line
counts, including excluded blocks, beside prose budgets. These are diagnostics,
not validated measures of reading time. Reader studies SHOULD measure actual
retrieval time and comprehension separately and test the 40/200 thresholds.

## 6. Clarification and numeric recommendations

Ask only for missing inputs that materially change the answer or determine
whether the action is supportable. Obtain the smallest decisive set, using one
or more natural questions or a compact input request. A brief rationale and a
supported bounded answer MAY accompany it. Do not authorize an action contingent
on unresolved prerequisites. Known containment MUST NOT wait for an answer.

Do not replace requested fiction, a complete supplied procedure, or a bounded
answer determined by visible facts with unnecessary clarification. Preserve the
boundary between confirmed readiness and unknown readiness.

Numeric advice MUST expose governing assumptions and avoid unsupported precision.
Depending on the missing input and task, the response MAY:

- ask for the decisive input;
- provide a supported relationship or formula; or
- provide a clearly conditional example with assumptions beside its numbers.

No literal labels, example number, or universal default are required. An example
MUST NOT be presented as a recommendation for the user's actual environment.
When inputs suffice, a direct recommendation is allowed.

## 7. Corrections

An emitted error MUST be repaired promptly and explicitly. The repair MUST
identify the earlier error faithfully and give its replacement. It MUST explain
the changed consequence or action when there is one. Natural wording is allowed;
do not fabricate a retraction or a consequence to satisfy a template.

Put the repair first in conversational prose, or first under At a glance when
Full is selected. Include any urgent warning beside it. For a requested corrected
procedure, identify the affected step and preserve the requested step order.
An exact artifact remains byte-preserved; a separately requested correction or
explanation MUST NOT be silently inserted into controlling source text.

The wrapper requires structured withdrawn and replacement fact references;
changed-action references may be empty when no action changes. Withdrawn IDs
must exist in committed topic state. Presence of references and repair placement
is mechanical; faithfulness, explicitness, and consequence sufficiency are semantic.

## 8. Safety and legal precedence

An indispensable warning MUST accompany the related claim or action early enough
to prevent a misleading stopping point. Preserve the known hazard, concrete
harm, immediate containment, and conditions for proceeding when material to the
case. Do not invent a hazard or universal restart checklist.

Warnings do not force Full. In a Focused answer put them in the earliest
actionable prose; in Full put indispensable decision-level warnings at a glance.
Deeper detail may repeat a short qualification needed to keep an action safe,
but SHOULD NOT repeat the entire warning sequence. A checkpoint time alone
does not authorize action. Warning sufficiency remains `UNVERIFIED` mechanically.

## 9. Purpose-specific structures

- Preserve complete natural order for tutorials and procedures.
- Preserve sequence, pacing, tense, and voice for narrative writing.
- Preserve requested exact values, code, data, formats, and transformations.
- Preserve controlling legal or authoritative source bytes. When reproduced
  with an explanation, use `Controlling text:` and
  `Non-controlling plain-language summary:` to separate source and explanation.
- Verbatim-only reproduction contains only the exact source.

Requested fiction may invent creative details. A supplied complete high-level
procedure does not require unnecessary system-specific commands, owners, or
values. An optional Full overview requires a separate request and must not
damage the artifact. Required repeated source bytes are always preserved.

## 10. Mechanical wrapper and guarantee boundary

The non-streaming wrapper MUST resolve trusted metadata before generation,
buffer the complete envelope, validate it, render canonical Markdown, and commit
state only after success. It permits one initial candidate and one complete
repair under the same resolved policy. Two failures withhold candidate output
and leave state unchanged.

### 10.1 Request, state, and fact semantics

Request schema `4.0.0` adds required Boolean `depth_useful` to the existing
prompt, topic, turn, presentation, controlling-text, non-fit, and required-fact
fields. Callers set it true only when distinct layers help. Under `auto`, first
substantial orientation and checkpoint turns use Full only when it is true.
Explicit presentation and purpose-specific shapes retain their precedence.

Each topic retains its branch, stable facts, host sessions, and
`has_committed_overview`. A successful first substantial answer or meaningful
checkpoint marks orientation, including a compact Focused answer. Explicit Full
formatting of a simple or narrow turn does not. Failed turns never mutate state.

Fact `allocation` identifies primary response-local placement. A Full fact may
also be referenced in other views; its primary placement must be referenced.
Repeated references do not create new facts. Existing IDs retain exact text;
cross-turn references declare `prior_context`, `synthesis`, `correction`, or
`quotation` as appropriate. `synthesis` is valid for a topic-wide overview in
either format. Exact lexical echoes are nonblocking observations: usefulness
cannot be decided by a lexical matcher.

Clarification `control` contains natural clarification text without reserved
view headings and no fact ledger entries. If bounded advice needs committed
facts, the caller selects a Focused ordinary answer that can include an input
request. A control turn's relevance and completeness remain semantic.

### 10.2 What a mechanical pass establishes

Only implemented checks over the trusted request, committed state, selected
kind, envelope, and renderer: version/shape consistency; topic/branch/count
transitions; Full section order, content, and hard budgets; structured warning
placement; correction reference structure; fact identity and declared reuse;
trusted quotation equality/hash; and supplied authoritative fact coverage.

It does not establish accuracy, completeness, warning sufficiency, useful depth,
helpful repetition, correct caller classification, clarification quality, repair
meaning, human safe stopping, or equality to an intended non-fit artifact without
trusted expected bytes. These remain `UNVERIFIED`. Post-response hooks remain
Advisory/block-and-retry and cannot certify displayed output or topic state.

## 11. Evaluation and conformance

Review directness, qualifications, appropriate shape, additive usefulness,
assumptions, clarification relevance, faithful repair, and artifact preservation.
Score Advisory length targets separately from mechanical hard-cap conformance.

Development regressions, unseen holdouts, and reader outcomes are separate
evidence tracks. Freeze prompts, model settings, rubric, and run plan before
evaluation. Preserve failures and report denominators; failed-case reruns are
debugging evidence rather than a new full-suite acceptance result. Once used to
tune instructions, a holdout becomes development material and must be replaced.

Compare ordinary responses, minimal core-principles instructions, the archived
v0.4 long skill, and the revised skill on matched tasks. Blind condition labels
and counterbalance presentation for reader assessment. Measure correct action
interpretation, constraint recognition, retrieval time, and preference separately
from protocol compliance. See [the evaluation guide](evals/README.md) and
[reader study plan](evals/reader-study.md). No reader-benefit claim is established
until observations support it.
