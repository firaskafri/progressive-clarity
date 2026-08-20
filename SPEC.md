# Progressive Clarity Protocol

Version 0.4 release candidate

Progressive Clarity is a topic-oriented response protocol. It uses a focused,
natural answer for ordinary exploration and three additive views when a topic
needs orientation, re-synthesis, or a meaningful checkpoint.

## 1. Scope and profiles

This specification is normative for conversational factual answers,
explanations, recommendations, comparisons, decisions, status updates, and
summaries. It governs view composition, stopping quality, correction,
exceptions, and response-budget accounting.

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
state requirements. Version 0.4 defines word-budget conformance for English
Full-format responses only.

The protocol has two profiles:

- **Advisory conversational profile:** The model infers topic continuity and
  presentation from the visible conversation. The canonical skill and ChatGPT
  package are prompt-only. Activation, topic inference, return to an earlier
  topic, and presentation selection are best-effort rather than deterministic.
- **Mechanical wrapper profile:** A trusted caller supplies topic action, turn
  classification, and presentation request. The wrapper verifies the selected
  shape and state transition. It does not infer natural-language intent or
  prove that the caller classified the turn correctly.

Document adaptation is informative. It does not create another conversational
behavior.

## 2. Universal response requirements

Every governed response, whether Focused or Full, MUST:

- answer the immediate request directly when the requested artifact permits;
- be complete for that request rather than a teaser for later detail;
- remain accurate, including material scope and uncertainty;
- place an indispensable caveat with the claim or action it qualifies;
- put safety, policy, and legal requirements ahead of brevity; and
- explicitly repair a materially wrong emitted statement.

When a numeric recommendation lacks governing inputs, the response MUST use
this visible structure:

```text
Governing input: <missing dependency>.

Example assumption: <number and the assumption that justifies it>.
```

`Example assumption:` is the required combined Example/Assumption label. The
response MUST NOT use “good default,” “I’d use,” or a numeric value or range
outside this structure. When the governing inputs are supplied, a direct
numeric recommendation is allowed.
When the user requests a numeric recommendation and the governing input is
missing, this two-label template MUST be the answer and MUST NOT be replaced by
a clarification question. Any example number MUST appear only after
`Example assumption:`.

Later detail MAY narrow an earlier claim but MUST NOT silently reverse its
operative meaning. A Focused response as a whole MUST be safe to act on or stop
after. In a Full response, each cumulative stopping point MUST be complete,
accurate, and safe to stop.

Directness, accuracy, caveat placement, safety, and repair are semantic
requirements. A deterministic validator can inspect declared structure and
exact lexical echoes, but it cannot prove those properties.

## 3. Topic and presentation selection

### 3.1 Advisory topic heuristic

A topic continues while the objective, decision, or prior context needed to
answer remains the same.

In the Advisory conversational profile:

- Continue the current topic when the objective, decision, or required context
  is unchanged.
- Start a new topic only when the objective changes and prior context is no
  longer needed.
- Treat acknowledgements and formatting instructions as part of the current
  topic; they do not create topics.
- Treat return to an earlier topic as best-effort. Prompt-only hosts, including
  ChatGPT, do not provide protocol-controlled durable topic state.
- When uncertain, continue the current topic and prefer Focused format.

### 3.2 Mechanical topic input

In the Mechanical wrapper profile, the trusted caller MUST identify a topic
and classify the action as start, continue, or resume. The wrapper MUST reject
an invalid state transition before generation. It MUST NOT claim that the
supplied topic boundary is semantically correct.

### 3.3 Presentation precedence

Resolve presentation in this order:

1. **Purpose-specific shape:** A clarification, quotation, exact output,
   transformation, narrative, or complete procedure MUST preserve the shape
   required by its purpose.
2. **Explicit presentation:** A request for all three views MUST use Full
   format. A request for a brief answer or no headings MUST use Focused format.
   A request for one named view MUST receive a Focused answer at that requested
   depth; it MUST NOT force the other views.
3. **Meaningful checkpoint:** A decision checkpoint, accumulated-context
   summary, material re-synthesis, or material correction MUST use Full format.
4. **First consequential orientation:** The first consequential answer on a
   topic that can orient the reader MUST use Full format, including a bounded
   recommendation.
5. **Ordinary exploration:** A simple fact, acknowledgement, narrow follow-up,
   later ordinary turn, or narrow correction MUST use Focused format.

An orientation-capable answer has enough context to frame the objective,
consequence, material constraints, or next action. A simple fact does not
become Full merely because it is the first turn.

A material re-synthesis revises topic-level implications or a recommendation
using new or accumulated context. An accumulated-context summary integrates
the topic rather than restating one narrow branch.

A pure information update receives a Focused acknowledgement. If the same turn
asks for changed implications, a revised recommendation, or synthesis against
prior context, it is material re-synthesis and MUST use Full format.
A pure update MUST state only the supplied change. It MUST NOT claim that
another step, dependency, condition, or rollback rule remains unchanged unless
the user also supplied that fact.

After a clarification supplies the requested inputs, the pending request
continues the same topic. The answer MUST NOT be classified as a new first
orientation merely because the clarification withheld a recommendation. It
SHOULD use Focused format unless another meaningful-checkpoint rule
independently requires Full.

Explaining or orienting the reader to a consequential supplied plan uses Full
format. Procedure shape takes precedence only when the user asks to write or
execute the procedure itself, not merely because the plan contains ordered
steps.

### 3.4 Focused format

A Focused response MUST lead with the answer and use only the structure needed
for the immediate request. Reserved Progressive Clarity headings are not
required and SHOULD be omitted. Ordinary headings, lists, code blocks, or
other task-appropriate structure MAY be used when they improve the answer.

A request for one named view receives that depth of answer without the other
views. Do not add a reserved view heading unless the user explicitly requires
that exact heading.

Focused format has no 40/200 word budget and no mandatory section count.
Length MUST remain proportionate to the request. Safety and correction follow
sections 7 and 8.

For a simple fact, a Focused response MUST use at most three sentences unless
an indispensable safety or accuracy caveat requires more. Sentence one MUST
answer. The response MAY add one indispensable distinction, then MUST stop. It
MUST NOT add an adjacent use-case catalogue or anticipate the next question.
Before sending a simple fact, the response MUST remove any unrequested “used
for,” “such as,” “including,” or similar catalogue. Embedding a list in one
sentence does not make it proportionate.

### 3.5 Full format

A Full response MUST render these headings exactly once and in this order:

1. **At a glance**
2. **In context**
3. **At depth**

The canonical Markdown renderer uses level-two headings. Other renderers MAY
adapt heading level to their artifact while preserving text and order.
Headings do not count toward a prose budget.

#### At a glance

At a glance gives the direct answer, its decision-relevant consequence,
material scope, and every caveat indispensable to a correct stopping point.

Its non-warning English prose MUST contain no more than 40 counted words.
An indispensable warning MAY exceed the cap only as far as section 8 requires.

#### In context

In context adds only what the reader needs to understand or act: new rationale,
scope, constraints, ownership, timing, controls, or next action.

Combined non-warning prose in At a glance and In context MUST contain no more
than 200 counted words in that response. This is a per-response limit, not
conversation state.

#### At depth

At depth adds purposeful specialist detail: evidence, assumptions,
measurements, alternatives, exceptions, implementation guidance, procedures,
or sources.

At depth has no hard word limit. It MUST remain relevant, organized, and
additive. Length alone does not satisfy this view.

## 4. Full-format composition and repetition

Every deeper view MUST be dominated by new information. A brief anchoring
reference MAY recur only when it is needed to understand new content. Names,
dates, identifiers, and short anaphoric cues such as “this decision” or “that
constraint” MAY recur.

A deeper view MUST NOT repeat or paraphrase a complete conclusion, sentence,
list, explanation, warning, or recommendation. The headline recommendation
belongs in At a glance. In context explains new rationale, scope, constraints,
ownership, timing, or action. At depth adds new evidence, exceptions,
alternatives, implementation, or sources. At depth MUST NOT end with a recap,
summary, “key rule,” or restated operative recommendation.

An anchoring reference MUST NOT reassert the earlier operative proposition
before adding detail. It SHOULD use the shortest cue that makes the new content
understandable. A component name or role boundary MAY recur when the sentence's
operative content is materially new implementation, evidence, exception, or
action. Repeating the complete rule and then elaborating does not become an
anchor.

The composer MUST use this private workflow:

1. Draft At a glance.
2. Extract its complete propositions into a “do not restate” ledger.
3. Draft In context using only new rationale, constraints, or actions plus
   minimal anchors.
4. Add its complete propositions to the ledger.
5. Draft At depth using only new evidence, exceptions, or implementation.
6. Delete any sentence that restates a ledger proposition.
7. Delete any concluding recap from At depth.
8. Inspect the final At-depth sentence or list item. Retain it only when it adds
   new evidence, exception, implementation, or source; otherwise delete it.

Compact positive example: At a glance says “Delay Atlas until security
approval.” In context may say “For Atlas, Security owns the approval gate and
needs the threat model by Friday.” The recurring name anchors new ownership and
timing.

Compact negative example: At a glance says “Delay Atlas until security
approval.” In context says “Atlas must wait for security approval,” or At depth
ends “Key rule: delay Atlas.” Both restate the operative conclusion.

Necessary correction reuse follows section 7. Exact-artifact exceptions and
any separately requested Full overview or explanation follow section 9.

In either format, a supplied measurement SHOULD retain its value, unit, scope,
time window, denominator or sample size, and source character such as pilot,
estimate, or benchmark. Material supplied evidence MUST NOT be silently
omitted to satisfy a budget or preference for brevity; clarify or use the
warning/non-fit rules when necessary.

## 5. Full-format English word-count algorithm

Human scoring and `pc-core` use the following ordered deterministic algorithm
for Full-format budgets.

### 5.1 Included and excluded Markdown

Normalize CRLF and bare CR to LF, then:

1. Exclude fenced code blocks opened by at least three backticks or tildes
   after no more than three leading spaces and closed by at least the opening
   marker length of the same character.
2. Exclude an ATX heading line. Exclude a Setext heading line together with its
   immediately following `===` or `---` underline.
3. Exclude a GitHub-style data table when a pipe-containing header is followed
   by a pipe-containing delimiter row whose two or more cells each match
   `:?-{3,}:?`. Exclude the header, delimiter, and contiguous following
   non-empty pipe-containing rows.
4. Remove an inline or reference Markdown image, including alt text and
   destination or reference label. Replace an inline or reference link with its
   visible text. Remove a reference destination definition, autolink, or bare
   URL.
5. Remove a footnote-reference marker but retain explanatory footnote prose
   after its definition marker. Remove a footnote backlink.
6. Remove these citation-marker forms: a bracket containing only numeric
   references and comma/dash ranges; a textual bracket label ending in a
   separate one-to-four-digit reference number, such as `[Ops Memo 7]`; and a
   parenthetical author-date marker containing a comma followed by a year from
   1900 through 2099, such as `(Smith, 2025)`.
7. Remove HTML comments and tags. Remove leading blockquote, unordered-list,
   ordered-list, and task-checkbox markers. Delete these Markdown punctuation
   characters without inserting whitespace: backslash, backtick, `*`, `_`,
   `{`, `}`, `[`, `]`, `(`, `)`, `#`, `+`, `.`, `!`, `>`, `|`, `~`, and `-`.

The remaining reader-visible assistant prose is included, including cue labels,
list text, visible link text, inline-code content after backtick removal, and
explanatory footnote prose. The user prompt, non-rendered state, and genuine
clarification control dialogue are excluded.

### 5.2 Token count and budgets

Split included prose at Unicode whitespace. Count each resulting token that
contains at least one ASCII letter `A-Z` or `a-z`, or digit `0-9`, as one word.
Do not split a token at attached punctuation.

An unspaced contraction or hyphenated compound therefore counts once. Compact
dates, times, numbers, currency amounts, inequalities, and code-like tokens
also count once. A standalone symbol without an ASCII letter or digit does not
count.

Budget accounting is:

- At a glance non-warning prose: at most 40 words.
- At a glance plus In context non-warning prose in the current response: at
  most 200 words.
- At depth prose: outside the hard cap.
- An indispensable warning: separately counted and exempt only as necessary.
- Necessary correction repair text: separately counted and exempt only as
  necessary.

## 6. Branch focus and clarification

The Advisory conversational profile uses visible conversation context to
retain the active topic, selected branch, and statements requiring correction.
This memory is best-effort. The Mechanical wrapper profile uses the
caller-selected topic state described in section 10. Neither profile treats
Focused or Full presentation as a depth state that the user must progress
through.

A targeted follow-up selects only the named branch and excludes sibling
branches and general recap. It uses Focused format unless an earlier
presentation rule requires Full format.

Before making a recommendation, privately check whether required environment,
validation, rollback, ownership, or governing constraints are missing. If
missing information prevents a complete or safe answer, the response MUST
contain only one clarification question. It MUST have no heading, conditional
recommendation, generic plan, rationale, or implementation detail. It MAY
incorporate an indispensable warning clause within that question only when the
warning cannot safely wait.

This clarification gate applies when missing input blocks a recommendation. It
MUST NOT replace a requested narrative or a complete high-level procedure whose
content and order the user has already supplied.

For example, `Should I enable the new index now?` lacks the environment,
validation result, and rollback readiness. A conforming response asks one
question for those inputs and gives no recommendation. After the user supplies
staging, passed validation, and available rollback, a Focused recommendation
MAY follow while preserving the staging/production boundary.
For that example, a complete Focused answer states that validation passed,
rollback is available, enablement is limited to staging, and staging
authorization is not production approval.

## 7. Corrections

A correction is a repair, not ordinary elaboration. When an emitted statement
is wrong or materially incomplete, the next relevant response MUST begin with:

```text
Earlier I said <withdrawn statement>. That was wrong or incomplete.
<replacement statement>. This changes <consequence or action>.
```

The withdrawn statement MUST preserve the operative wording of the visible
earlier response or faithfully isolate the affected proposition from a combined
sentence. It MUST NOT insert a qualifier, date, or scope that was not part of
the earlier response.

Under automatic presentation, a narrow correction uses Focused format and puts
the complete repair first; a material correction uses Full format and puts the
complete repair as the first prose under At a glance. Explicit presentation
requests retain the precedence defined in section 3.3. A correction is material
when it changes the operative decision, action, risk, scope, or topic-level
understanding; otherwise it is narrow.

If the same response requires a warning, the literal correction opening remains
first and the warning follows it immediately.

“Corrected,” “outdated,” “superseded,” or an implicit substitution without the
literal opening above does not satisfy the correction requirement.

In a Full correction, only context necessary to identify, retract, replace, and
state the changed action is exempt from the normal budget. Unaffected facts and
new explanation follow normal Full-format allocation and budgets.

The assistant MUST NOT invent a retraction for a claim it did not emit.

## 8. Safety and legal precedence

Safety, policy, legal, and accuracy requirements outrank brevity. A material
warning MUST appear with the related action or conclusion. In Focused format,
put it in the earliest actionable prose. In Full format, put it in the earliest
relevant view and never defer an At a glance warning to In context or At depth.

In Full format, At a glance MUST contain the prohibited action, hazardous
state, concrete harm, immediate containment, and condition for resuming. A
warning element MUST NOT be deferred to In context or At depth. Include a
causal mechanism when needed to make the harm understandable. A checkpoint
time is not authorization unless the source says it is.

In context and At depth MUST NOT repeat the complete warning or containment
sequence. They MAY add new diagnostics, evidence, or implementation.
A condition for resuming MAY name the prohibited operation, but it MUST NOT
become operational or numbered restart instructions.
When the user supplies a hazardous state, concrete harm, and immediate
containment for a consequential action, the response MUST use Full format and
place the complete warning in At a glance. It MUST NOT replace that answer with
a clarification.

Warning placement and Full-format arithmetic can be mechanically inspected.
Whether a warning is indispensable, sufficient, accurate, or safe remains
semantic and `UNVERIFIED`.

## 9. Non-fit structures

Do not force the three views onto output whose function depends on another
shape:

- **Tutorials and procedures:** preserve complete natural step order. Do not
  withhold required later steps.
- **Narrative or voice-dependent writing:** preserve sequence, pacing, tense,
  and voice.
- **Exact output and transformations:** preserve the requested value, format,
  code, data, or verbatim reproduction without added headings.
- **Controlling legal or authoritative text:** preserve source bytes exactly.
  When an explanation or summary is requested, use exactly:

```text
Controlling text:
<exact source>

Non-controlling plain-language summary:
<summary>
```

For an open-ended fiction request, the response MAY choose ordinary creative
details and MUST produce the requested narrative; the prohibition on invented
factual claims does not ban requested fiction. When the user supplies a
complete high-level procedure, the response MUST render every supplied step in
order and MUST NOT demand system-specific commands, owners, or values that are
unnecessary to preserve that procedure.

Controlling text with a requested explanation is eligible for the Advisory
Skill. Only verbatim-only reproduction remains outside Skill activation.

Exact controlling text, quotations, code, data, and other user-required
verbatim artifacts MAY retain repeated source bytes when exactness requires
them. The artifact itself is outside Progressive Clarity cross-view
no-repetition checks. If a separate summary, overview, or explanation uses Full
format, it remains subject to new-information dominance and
no-complete-restatement rules.

An optional, separate overview MAY use Full format when the user separately
requests all three views and it does not damage the required artifact.

## 10. Mechanical wrapper profile and guarantee boundary

The canonical `SKILL.md` and ChatGPT package use the Advisory conversational
profile. They are prompt-only surfaces with no backend, MCP server, protocol
hook, deterministic output gate, or protocol-controlled durable topic store.

The local non-streaming `pc-core` wrapper implements the Mechanical wrapper
profile only when it:

1. receives a trusted wrapper request and committed state separately from model
   output;
2. resolves caller-supplied topic action, turn classification, and presentation
   request before generation;
3. buffers a complete schema `3.0.0` envelope using protocol `0.4`;
4. validates versions, selected response kind, target-topic state, Full-format
   section order and budgets when applicable, Focused content when selected,
   clarification question-only shape, fact-ID integrity and reuse declarations,
   correction structure, quotation bytes and hash when trusted source is
   supplied, and exact lexical duplicates while exempting required verbatim
   artifact bytes;
5. renders only from the validated envelope; and
6. atomically commits the complete next state only after validation succeeds.

The wrapper withholds an invalid candidate. It permits at most two total
generation attempts: one initial candidate and one complete repair using the
same resolved presentation. If the second candidate fails, it emits no
candidate response and leaves committed state unchanged.

Post-response host hooks are **Advisory/block-and-retry**. They MAY inspect
visible headings and reject an empty view inside an exact three-heading
sequence. Heading-free, fenced, or partial reserved headings are nonblocking.
Visible budget and lexical-echo observations remain `UNVERIFIED` because hooks
cannot identify structured exceptions. Hooks cannot certify presentation
selection, topic state, trusted request classification, or output already
displayed.

### 10.1 Request, topic state, and envelope

Version 0.4 wrapper request, envelope, and state schemas are `3.0.0`.

The trusted request supplies:

- `topic_action`: start, continue, or resume;
- `topic_id`;
- `turn_kind`;
- `presentation_request`: auto, focused, or full; and
- any controlling text, summary limit, non-fit kind, or authoritative required
  facts used by the selected shape.

Start requires an unknown topic. Continue requires the active topic. Resume
requires a known inactive topic. Each known topic retains its branch, fact
ledger, host sessions, and whether a topic-wide overview has been committed.
Starting creates fresh topic state; resuming restores the selected topic state.
A failed or withheld response MUST NOT create, activate, or mutate a topic.

A certified topic-wide substantial answer, decision or summary checkpoint,
material re-synthesis, or material correction marks the overview committed.
Explicit Full formatting of a simple or narrow turn does not.

The envelope declares the selected response kind and target-topic transition.
Response kinds include Focused content, Full views, clarification control,
quotation, and non-fit output. Fact allocation is response-local: a fact used
in Focused prose MAY later appear in the appropriate Full view. A stored fact
retains its stable ID, exact text, and first turn rather than permanently
retaining a presentation allocation.

`prior_context` marks necessary cross-turn reference; `synthesis` marks reuse
while building a later Full overview. `correction` and `quotation` mark only
their structured exceptions. Exact normalized lexical repetition is
mechanically inspectable. Required exact controlling text, quotations, code,
data, and other verbatim artifacts are exempt from that check and MAY preserve
repeated source bytes.

Cross-view new-information dominance applies only to Full format. Exact
sentence and list-unit duplication remains mechanically rejected. Whether a
recurring short anchor is necessary, a paraphrase restates a complete
proposition, or At depth ends in a semantic recap remains advisory because
lexical similarity does not prove those properties. Fact declarations cannot
prove that every material proposition was extracted, split appropriately, or
placed well.

### 10.2 Guarantee boundary

Mechanical `PASS` guarantees only implemented checks over the trusted request,
committed state, resolved presentation, structured envelope, and canonical
renderer buffered by that wrapper. It does not guarantee:

- semantic accuracy or completeness;
- human safe-stopping outcomes;
- warning indispensability or sufficiency;
- correctness of the caller's topic, turn, or presentation classification;
- semantic appropriateness of Focused versus Full format;
- equality between an accepted non-fit payload and the user's intended
  artifact without trusted expected bytes;
- necessity of recurring anchors and semantic complete-proposition
  restatement;
- absence of a concluding At-depth recap;
- purposeful At depth content;
- hidden-reversal absence;
- Advisory host activation, topic inference, or topic resumption;
- host-wide behavior outside the wrapper; or
- compatibility with an untested host.

Those properties remain advisory and `UNVERIFIED` without an independent
oracle.

## 11. Conformance check

Before sending a governed response, verify:

1. the topic continues unless the objective changed and prior context is
   unnecessary;
2. purpose-specific output shape and explicit presentation requests were
   resolved before automatic Full triggers;
3. a Focused response answers directly without forced protocol headings;
4. a Full response has exactly three ordered views, satisfies the 40/200
   English budgets, makes every deeper view predominantly new, permits only
   necessary short anchors, does not restate a complete earlier proposition,
   and ends At depth without a recap;
5. every material scope boundary and indispensable caveat appears early enough;
6. a correction begins with explicit withdrawal, replacement, and changed
   consequence or action;
7. later detail preserves earlier claims or uses explicit correction; and
8. a required non-fit structure remains intact.
