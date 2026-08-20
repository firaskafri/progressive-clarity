# Scope and limitations

## Current v0.4 scope and limitations

Progressive Clarity protocol `0.4` is a locally verified release candidate. It
is topic-oriented: ordinary exploration uses Focused answers, while Full
responses with At a glance, In context, and At depth provide orientation and
meaningful checkpoints.

[`SPEC.md`](../SPEC.md) is normative. Templates, examples, installation
guidance, and document adaptation are informative when they differ.

### Advisory prompt-only profile

The canonical skill and ChatGPT, Cursor, and Claude packages are prompt-only.
They use a visible-conversation heuristic:

- continue while the objective, decision, or required prior context remains
  the same;
- start a new topic only when the objective changes and old context is no
  longer needed;
- treat acknowledgements and formatting instructions as part of the current
  topic;
- resume an earlier topic only when visible context supports that inference;
  and
- when uncertain, continue the current topic and prefer Focused output.

This heuristic is not durable state. Activation, topic boundaries, branch
selection, topic resumption, and Focused/Full selection remain probabilistic
and host-controlled.

Automatic Full presentation applies to:

- the first substantial, orientation-capable overview on a topic;
- a decision checkpoint;
- an accumulated-context summary checkpoint;
- material re-synthesis; and
- material correction.

Simple facts, ordinary turns, narrow follow-ups, later non-checkpoint
exploration, and narrow corrections are Focused. Purpose-specific structures
and explicit presentation requests take precedence. Focused output has no
mandatory protocol headings or 40/200 budget; Full output retains the three
ordered headings and English 40/200 budgets.

### Mechanical wrapper profile

The local `pc-core` source implements protocol `0.4` with wrapper request,
envelope, and state schemas `3.0.0`. A trusted caller supplies
`topic_action`, `turn_kind`, and `presentation_request`; deterministic policy
resolves before the host is invoked.

The wrapper can mechanically check the resolved response kind
(`focused`, `views`, `control`, `quotation`, or `non_fit`), target-topic state,
Full structure and budgets when applicable, Focused reserved-heading
exclusion, one-sentence clarification question shape, At-a-glance structured
warning placement, response-local fact placement, fact identity and declared
reuse, correction structure and rendering precedence, trusted quotation bytes,
exact lexical duplicates, and atomic state commit. It can withhold invalid
buffered output after one complete repair attempt.

It cannot guarantee:

- factual accuracy, completeness, or source quality;
- correctness of caller-supplied topic, turn, or presentation classification;
- correctness or completeness of an authoritative fact catalog;
- semantic fact atomicity or appropriate response-local placement;
- activation or topic inference on an Advisory host;
- semantic appropriateness of Focused versus Full presentation;
- human safe stopping or warning necessity and sufficiency;
- whether a short anchor is necessary, whether a paraphrase restates a complete
  proposition, or whether At depth ends with a semantic recap;
- hidden semantic reversal;
- purposeful At-depth content;
- host behavior outside the non-streaming wrapper;
- concurrent access to one state path;
- rollback of remote host history or host-side effects after withholding; or
- an atomic transaction spanning local state replacement and downstream
  display or stdout.

A mechanical pass is not semantic certification.

### State compatibility

`ConversationState` is topic-oriented and stores each topic's branch, facts,
host sessions, and `has_committed_overview`. `StoredFact` retains exact text
and first turn; placement is response-local rather than durable fact state.

Earlier protocol state, including v0.3 state with schema `3.0.0`, is unsupported
by v0.4. Preserve old state needed for evidence, then start v0.4 with a fresh
state path. There is no silent migration or reinterpretation.

### Hook limitation

Cursor and Claude Code hooks remain **Advisory/block-and-retry**. They inspect
visible Markdown after generation and cannot certify trusted request
classification or topic state. A heading-free response is nonblocking because
it can be valid Focused or purpose-specific output. The hooks therefore cannot
detect every omitted Full response and cannot provide the wrapper's
fail-closed guarantee.

### Language and outcome limits

Version 0.4 makes a deterministic budget claim only for English Full
responses. Focused responses have no protocol hard cap. No claim is made for
non-English or mixed-language budget conformance.

There is no formal participant study or validated claim of improved
comprehension, decision quality, accessibility, safety, productivity, reading
time, or token use.

### Current evidence and release boundary

No `0.4.3` live ChatGPT, Cursor, or Claude acceptance run exists. User-provided
v0.3.0–v0.3.2 ChatGPT evidence is historical and recorded in
[Verification](verification.md). Portal-byte identity and visible Skill
activation were not independently verified. Current v0.4 host activation,
topic inference, topic resumption, presentation selection, and rendered
conformance are **UNVERIFIED**.

Local package version `0.4.3` artifacts, byte counts, and hashes are recorded in
[Verification](verification.md). They establish only local build integrity and
determinism. Do not reuse v0.2 or v0.3.x hashes as v0.4 identifiers. No upload,
review, approval, external publication, universal compatibility, or support
claim is made.

## Historical/superseded v0.3.x boundary

The v0.3.x packages and user-provided ChatGPT observations are retained in the
[verification record](verification.md). They exposed systemic Full repetition,
simple-fact proportionality, numeric-labeling, correction, clarification, and
controlling-label failures. T08 and T09 passed their bounded cases; other
partial positives do not transfer to v0.4. Portal bytes and Skill activation
were not independently verified.

## Historical v0.2 documentation and evidence

Everything below this heading is retained as historical v0.2 documentation and
evidence. References to “current,” v0.2 package versions, dated checks, and
user-provided host observations describe the historical record only. Their
labels and results are not transferred to v0.4.

Progressive Clarity protocol v0.2 and package v0.2.1 are a non-release-ready
draft with one ordinary response contract only: one response renders At a
glance, In context, and At depth together in that order. The prompt-only skill
is Advisory. The optional local wrapper gates only mechanically decidable
properties.

[`SPEC.md`](../SPEC.md) is normative. Templates, examples, installation
guidance, and document adaptation are informative when they differ.

## What v0.2 covers

- three additive views in every ordinary in-scope response;
- a 40-word non-warning At-a-glance cap;
- a 200-word per-response non-warning cap through In context;
- purposeful unrestricted At depth;
- no fact-only repetition across views;
- topic and targeted-branch focus;
- focused clarification control dialogue;
- explicit correction;
- safety, legal, exact-text, procedure, and narrative exceptions;
- Advisory prompt-only packaging; and
- an optional Enforced mechanical envelope, renderer, state store, and
  two-total-attempt wrapper.

There is no alternate presentation behavior, depth progression, view override,
or cross-turn shallow-word accumulation.

## Mechanical certification is narrow

For wrapper-buffered output, `pc-core` can guarantee schema/version checks,
trusted topic/branch/turn arithmetic, exact three-section order, deterministic
English counts, non-empty required-view prose, declared warning/correction
separation, fact-ID consistency,
exact trusted quotation bytes and hash, exact lexical-duplicate rejection for
Progressive Clarity view and explanatory prose while required verbatim artifact
bytes remain exempt, byte-preserving accepted non-fit payload rendering,
canonical view rendering, bounded attempts, cross-turn host-session resume, and
atomic local state commit. When a trusted request supplies a non-empty
authoritative fact catalog, it also guarantees exact normalized visible
coverage of those supplied IDs and texts.

It cannot guarantee:

- factual accuracy, completeness, or source quality;
- completeness or correctness of a caller-supplied authoritative fact catalog;
- semantic fact atomicity or correct allocation;
- actual human safe stopping;
- warning necessity, sufficiency, or safety outcome;
- paraphrased repetition or hidden semantic reversal;
- purposeful At-depth content;
- intended topic or branch beyond trusted metadata;
- host activation or general host behavior; or
- concurrent access to one state file; or
- an atomic transaction spanning state replacement and downstream stdout,
  transcript display, or host-side effects; or
- rollback of remote host-session history after a withheld turn.

Those properties remain Advisory or `UNVERIFIED`. A mechanical pass is not
semantic certification.

## English-only budgets

Version 0.2 makes no budget-conformance claim for non-English or mixed-language
responses. The exact ordered Markdown transformations and ASCII-letter/digit
token rule are normative in `SPEC.md`. Warning and correction exceptions do not
permit omission of required facts.

## No host support claim

One bounded live Cursor wrapper rerun records v0.2 mechanical behavior for
E02-E07. Of 17 responses, 10 were mechanically certified and 7 were withheld;
`E02`, `E06`, and `E07` passed, while `E03`, `E04`, and `E05` failed. The rerun
exercised the mechanical wrapper fixes against the pre-trigger-revision skill,
but it failed the full behavioral suite. Strict semantic and behavioral
acceptance remains unmet, and the result does not establish general Cursor
compatibility or current-v0.2.1 prompt-only conformance.

No independently executed full current-revision prompt-only run establishes
that Cursor, Claude Code, ChatGPT, Codex, or another host generally follows
v0.2. The current user-provided ChatGPT observations below are bounded, mixed
evidence rather than universal acceptance. Standard Agent Skills packaging is
a portability choice, not compatibility evidence.

The generic host interface is designed for future local adapters. Codex support
is not claimed or tested.

## Historical evidence boundary

The preceding bounded Cursor cycle belongs to older dual-behavior inputs. Round
one completed 21 fresh sessions and 39 responses: 6 cases passed and 5 failed.
The single permitted targeted remediation round completed 9 sessions and 20
responses; all 5 rerun cases failed. All 59 budget checks passed, and neither
round had a safety-warning or procedural-safety failure. The mandatory hard
stop was reached. These observations neither establish safety nor verify v0.2.

Claude Code's older attempt stopped before inference with insufficient API
credit. Its hook and adapter are structurally tested, but current prompt-only
and live wrapper behavior remain `UNVERIFIED` because a live run requires paid
Anthropic API access.

On 2026-08-17, the user reported publication of an older ChatGPT plugin as
[`plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
An anonymous fetch confirmed only that the login-gated route exists. The URL
is historical publication evidence and does not establish the separate
user-reported Advisory v0.2.1 upload or installation.

The user also supplied a transcript they identified as a live interaction with
the published older build. It was not independently captured. Its historical
visible results were:

- default three-view rendering in order: `PASS`;
- older staged acknowledgment and transitions: `PASS`;
- safe stopping and caveats: `PASS`;
- At-a-glance budgets: `FAIL` — gold approximately 103 prose words; silver
  approximately 210, excluding tables and citations;
- prose through In context: `FAIL` — gold approximately 330+ words; silver
  approximately 600+;
- additivity and no fact-only repetition: `FAIL`; and
- switch-back acknowledgment: observed, while subsequent behavior remained
  `UNVERIFIED`.

A later user-provided transcript, captured before the v0.2.1 trigger-recall
patch, omitted the initial three-view response and then described removed
presentation modes. The repository did not independently capture either
session or identify the installed portal bytes.

Those earlier ChatGPT records are **historical, observed, and
non-conformant**. They are not current v0.2.1 evidence and do not verify
financial facts, activation, compatibility, or support.

## Current ChatGPT evidence boundary

On 2026-08-18, the user reported uploading and installing the Advisory v0.2.1
ZIP in ChatGPT. The repository did not independently observe those actions,
inspect an authenticated listing, identify the portal artifact by digest, or
receive upload, submission, review, approval, portal-validation, security-scan,
or publication records.

The user then supplied two separate v0.2.1 transcripts from 2026-08-18:

- In a complex gold-forecast response, the three-view structure triggered, but
  the 40-word At-a-glance budget, 200-word cumulative shallow budget, and
  additivity failed. This transcript is **observed but non-conformant**.
- In a later fresh fixed-facts smoke, automatic trigger, the exact three
  headings and order, a 26-word At a glance, approximately 50 cumulative
  shallow words, supplied-fact coverage, additivity, and a negative exact-output
  control returning exactly `323` all passed.

The fixed-facts smoke is a bounded pass for those named checks only. The
repository did not independently capture or reproduce either current session.
The smoke's fact coverage does not establish completeness beyond its supplied
facts; its exact-output control does not establish every non-fit case; and its
visible automatic trigger does not expose the host activation mechanism. The
mixed results do not establish installed-byte identity, universal v0.2.1
conformance, compatibility, support, or release readiness.

## No empirical reader-outcome claim

Safe stopping is an evaluation proxy based on required facts and caveats. It
does not establish what a human understood, remembered, believed, or did.
There is no formal participant study or validated claim of improved
comprehension, decision quality, accessibility, safety, productivity, reading
time, or token use.

## Security and operational exclusions

The Advisory skill and ChatGPT ZIP are instruction-only and contain no runtime,
network dependency, analytics, or tool grant. This is not a host security
certification.

The separate local `pc-core` uses Python 3.11+ standard library code, starts no
service, configures no MCP server, and changes no user-global settings. It
requires one owner per conversation state path. Host subprocesses run without a
shell and under a per-attempt timeout, but host-managed tools, descendants, and
side effects remain governed by the selected host rather than rolled back by
`pc-core`. Cursor workspace trust is never added implicitly: a fresh workspace
requires either an interactive trust decision or the wrapper's explicit
`--trust-workspace` option for the reviewed path.

Protocol v0.2 and package v0.2.1 do not include an automated
installer/updater, hosted AI service, semantic oracle, formal participant
research, or independently verified ChatGPT listing/install/activation record.
Professional name and trademark clearance remains unresolved.
