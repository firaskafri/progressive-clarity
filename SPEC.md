# Progressive Clarity Protocol

Version 0.2 draft

Progressive Clarity is an AI-first response protocol with one presentation
contract: every ordinary in-scope response renders all three additive views in
one response.

## 1. Scope

This specification is normative for conversational factual answers,
explanations, recommendations, comparisons, decisions, status updates, and
summaries. It governs view composition, stopping quality, correction,
exceptions, and response-budget accounting.

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
state requirements. Version 0.2 defines word-budget conformance for English
responses only.

Document adaptation is informative. It does not create another conversational
behavior.

## 2. Invariants

Each response and each cumulative stopping point MUST be:

- **Complete:** It answers the immediate request, not a teaser.
- **Accurate:** Later detail MAY narrow a claim but MUST NOT silently make an
  earlier operative claim false.
- **Additive:** Each deeper view contributes information not already supplied.
- **Safe to stop:** The reader can stop after At a glance or In context without
  forming a materially wrong belief or taking a materially wrong action.

The invariants are semantic requirements. A deterministic validator can check
declared structure and exact lexical echoes, but it cannot prove truth,
completeness, safe reader outcomes, semantic repetition, or hidden reversal.

## 3. The only in-scope presentation

Every ordinary in-scope response MUST render these headings exactly once and
in this order:

1. **At a glance**
2. **In context**
3. **At depth**

The canonical Markdown renderer uses level-two headings. Other renderers MAY
adapt heading level to their artifact while preserving text and order.
Headings do not count toward a prose budget.

### 3.1 At a glance

At a glance gives the direct answer, its decision-relevant consequence,
material scope, and every caveat indispensable to a correct stopping point.

Its non-warning English prose MUST contain no more than 40 counted words.
An indispensable warning MAY exceed the cap only as far as section 8 requires.

### 3.2 In context

In context adds only what the reader needs to understand or act: new rationale,
scope, constraints, ownership, timing, controls, or next action.

Combined non-warning prose in At a glance and In context MUST contain no more
than 200 counted words in that response. This is a per-response limit, not
conversation state.

### 3.3 At depth

At depth adds purposeful specialist detail: evidence, assumptions,
measurements, alternatives, exceptions, implementation guidance, procedures,
or sources.

At depth has no hard word limit. It MUST remain relevant, organized, and
additive. Length alone does not satisfy this view.

### 3.4 Requests for more, less, or one named view

There is no depth progression or alternate presentation state. A substantive
follow-up receives the same three ordered views, focused on the follow-up.

A preference for brevity SHOULD make all three sections shorter without
removing them. A request whose required output is an exact value, exact format,
pure transformation, complete procedure, controlling text, or narrative uses
the applicable non-fit structure in section 9.

## 4. Fact allocation and repetition

Before composing, assign each atomic proposition to its earliest necessary
view:

- At a glance: answer, consequence, material boundary, or indispensable caveat.
- In context: new rationale, constraint, owner, timing, action, or control.
- At depth: new evidence, measurement, source, alternative, exception, or
  implementation detail.

An atomic fact MUST appear in only one view. A deeper view MUST NOT recap,
paraphrase, or repeat an earlier fact merely to make the section self-contained.
Necessary correction reuse follows section 7. This cross-view rule applies to
Progressive Clarity explanation, not to an artifact whose function requires
exact reproduction. Exact controlling text, quotations, code, data, or another
user-required verbatim artifact MAY preserve and repeat source bytes as
required and is outside cross-view no-repetition checks. Any separate summary,
overview, or explanation remains subject to ordinary additive and
no-duplicate rules.

A supplied measurement SHOULD retain its value, unit, scope, time window,
denominator or sample size, and source character such as pilot, estimate, or
benchmark. Material supplied evidence MUST NOT be silently omitted to satisfy a
budget; clarify or use the warning/non-fit rules when necessary.

## 5. English word-count algorithm

Human scoring and `pc-core` use the following ordered deterministic algorithm.

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
6. Remove these citation-marker forms: `[^label]`; a bracket containing only
   numeric references and comma/dash ranges; a textual bracket label ending in
   a separate one-to-four-digit reference number, such as `[Ops Memo 7]`; and a
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

## 6. Topic, branch, and clarification state

The assistant tracks the active topic, selected branch, turn number, and
emitted fact ledger. It does not track presentation depth or a cumulative
cross-turn shallow-word count.

A new topic resets branch focus and the topic fact ledger. A targeted follow-up
selects only the named branch and excludes sibling branches and general recap,
but still renders all three views for that branch.

When missing information prevents a complete or safe substantive response, ask
one focused clarification. A pure clarification is control dialogue: it has no
view headings and consumes no view budget. It MUST NOT contain a hidden
recommendation, rationale, or implementation detail. An indispensable warning
that cannot safely wait appears with the question.

## 7. Corrections

A correction is a repair. When an emitted statement is materially wrong, the
next relevant response MUST:

1. identify the withdrawn statement;
2. say plainly that it was wrong or incomplete;
3. provide the replacement; and
4. state the changed consequence or action.

The repair text MUST be the first prose under At a glance. The response still
renders At a glance, In context, and At depth in order. Only context necessary
to identify, retract, replace, and state the changed action is exempt from the
normal budget. Unaffected facts and new explanation follow ordinary allocation
and budgets.

The assistant MUST NOT invent a retraction for a claim it did not emit.

## 8. Safety and legal precedence

Safety, policy, legal, and accuracy requirements outrank brevity. A material
warning MUST appear in the earliest view containing the related action or
conclusion. It MUST NOT be deferred to In context or At depth.

When a warning cannot fit normally, put it in explicit warning content and
include only what is indispensable: prohibition or immediate action, hazardous
state, causal mechanism, concrete harm, containment or escalation, and
condition for resuming. A checkpoint time is not authorization unless the
source says it is.

Warning placement and arithmetic are mechanically checkable. Whether a warning
is indispensable, sufficient, accurate, or safe remains semantic and
`UNVERIFIED`.

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
  Put any explanation in a separate, clearly marked non-controlling summary.

Exact controlling text, quotations, code, data, and other user-required
verbatim artifacts MAY retain repeated source bytes when exactness requires
them. The artifact itself is outside Progressive Clarity cross-view
no-repetition checks. Any separate Progressive Clarity summary, overview, or
explanation MUST remain additive and MUST NOT duplicate the artifact or repeat
its own facts merely to recap them.

An optional overview MAY use all three views only when the user requests it and
it does not damage the required artifact.

## 10. Deterministic local conformance

The canonical `SKILL.md` and ChatGPT package are **Advisory** prompt-only
surfaces. They have no backend, MCP server, hook, or deterministic output gate.

The local `pc-core` non-streaming wrapper is an **Enforced mechanical** surface
only when it:

1. receives a trusted wrapper request and committed state separately from model
   output;
2. buffers a complete schema `2.0.0` envelope using protocol `0.2`;
3. validates versions, intent/kind, topic/branch/turn state, three-section
   order, word budgets, fact-ID integrity and reuse declarations, correction
   structure, quotation bytes and hash when trusted source is supplied, and
   exact lexical duplicates in Progressive Clarity explanation while exempting
   required verbatim artifact bytes;
4. renders only from the validated envelope; and
5. atomically commits state only after validation succeeds.

The wrapper withholds an invalid candidate. It permits at most two total
generation attempts: one initial candidate and one complete repair. If the
second candidate fails, it emits no candidate response and leaves committed
state unchanged.

Post-response host hooks are **Advisory/block-and-retry**. They can inspect
visible headings, budgets, and exact lexical echoes, but cannot certify trusted
request/state/fact-envelope conformance or retract output already displayed.

### 10.1 Envelope and fact ledger

Envelope schema `2.0.0` contains `protocol_version`, `response_kind`,
`topic_id`, `new_topic`, explicit turn/branch/fact-count state, atomic facts,
and a kind-specific payload. There is no presentation-state field.

Each fact has one stable ID, single-line text declaration, allocation, and
optional cross-turn reuse reason. A prior ID retains exact text and allocation.
`prior_context` marks necessary cross-turn reference. `correction` and
`quotation` mark only their structured exceptions. A new topic resets the
active fact ledger.

Exact normalized lexical repetition in Progressive Clarity view or explanatory
prose is mechanical. Required exact controlling text, quotations, code, data,
and other verbatim artifacts are exempt from that check and MAY preserve
repeated source bytes. A separate summary, overview, or explanation is not
exempt: it remains mechanically subject to exact-duplicate checks and
semantically subject to additivity. Near-duplicate overlap is advisory because
lexical similarity does not prove semantic repetition. Fact declarations
cannot prove that every material fact was extracted, split atomically, or
allocated to the semantically right view.

### 10.2 Guarantee boundary

Mechanical `PASS` guarantees only implemented checks over the trusted request,
committed state, structured envelope, and canonical renderer buffered by that
wrapper. It does not guarantee:

- semantic accuracy or completeness;
- human safe-stopping outcomes;
- warning indispensability or sufficiency;
- topic or branch intent;
- paraphrased fact repetition;
- purposeful At depth content;
- hidden-reversal absence;
- host-wide behavior outside the wrapper; or
- compatibility with an untested host.

Those properties remain advisory and `UNVERIFIED` without an independent
oracle.

## 11. Conformance check

Before sending an ordinary in-scope response, verify:

1. all three headings appear exactly once and in order;
2. At a glance directly answers and stays within 40 non-warning words;
3. shallow non-warning prose totals at most 200 words;
4. At depth is purposeful rather than filler;
5. every material scope boundary and indispensable caveat appears early enough;
6. each fact is allocated once and deeper prose adds new information;
7. later detail preserves earlier claims or uses explicit correction; and
8. a required non-fit structure has not been damaged by the three-view form.
