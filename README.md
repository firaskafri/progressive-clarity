# Progressive Clarity

**Orient with three views, explore naturally, and re-synthesize when the
decision or topic materially changes.**

Progressive Clarity v0.4 is a topic-oriented response protocol. It keeps simple
facts and ordinary follow-ups conversational, while preserving a structured
three-view format for consequential orientation and meaningful checkpoints.

## The conversational cadence

Use **Focused** format by default for:

- simple facts and acknowledgements;
- narrow follow-ups and later ordinary turns;
- narrow corrections; and
- explicit requests for brevity or no headings.

Focused responses lead with the answer and use only the structure the request
needs. A simple fact uses at most three sentences unless an indispensable
safety or accuracy caveat requires more: answer, add one indispensable
distinction, then stop. Focused responses have no protocol word cap and do not
require reserved headings.

Use **Full** format by default for:

- the first consequential, orientation-capable answer on a topic;
- decision checkpoints;
- accumulated-context summaries;
- material re-synthesis; and
- material corrections.

Full responses render exactly:

1. **At a glance** — direct answer, consequence, material scope, and
   indispensable caveat; non-warning prose is at most 40 counted English words.
2. **In context** — new rationale, constraints, ownership, timing, controls, or
   action; combined non-warning prose through this view is at most 200 words.
3. **At depth** — new evidence, assumptions, measurements, alternatives,
   exceptions, implementation, or sources without a hard cap.

Every deeper Full view is dominated by new information. A necessary short
anchor—such as a name, date, identifier, “this decision,” or “that
constraint”—may recur, but a complete conclusion, sentence, list, explanation,
warning, or recommendation may not be repeated or paraphrased. At depth does
not end with a recap.

## What it feels like

> **User:** Is Redis a database?
>
> **Assistant:** Yes. Redis is an in-memory data store with optional
> persistence.
>
> **User:** Should we use it as the sole source of truth for payment state?
>
> **Assistant — At a glance:** No. Keep canonical payment state in
> transactional storage with explicitly tested durability and recovery; use
> Redis only where its persistence and consistency trade-offs are acceptable.
>
> **Assistant — In context:** Transactions make related state changes atomic.
> Durability depends on the database and its configuration; auditable payment
> history requires explicit transition records or audit logging.
>
> **Assistant — At depth:** If Redis is used for acceleration or coordination,
> design cache loss as recoverable, bound lock lifetimes, and test persistence,
> replay, failover, stale reads, and delayed webhooks.
>
> **User:** What TTL should the idempotency keys use?
>
> **Assistant:** Cover the provider’s maximum retry and webhook-delivery window,
> plus a documented safety margin.

Technical basis: [PostgreSQL transactions][postgres-transactions] describe
atomicity and configured durability; [Redis persistence][redis-persistence]
documents Redis durability options and their trade-offs.

[postgres-transactions]: https://www.postgresql.org/docs/current/tutorial-transactions.html
[redis-persistence]: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/

The rhythm is: **orient → explore naturally → re-synthesize at decisions,
summaries, or material change**.

## Topic behavior

On prompt-only hosts, the model uses visible conversation context:

- continue when the objective, decision, or required context is unchanged;
- start a new topic only when the objective changes and prior context is no
  longer needed;
- keep acknowledgements and formatting instructions inside the current topic;
- return to an earlier topic when visible context supports it; and
- prefer Focused format when uncertain.

Prompt-only topic inference and return are best-effort. They are not durable
state guarantees.

## Purpose-specific output still wins

Do not force either conversational format onto content that requires another
shape:

- clarification asks one focused question;
- verbatim-only reproduction remains exact;
- controlling text with a requested explanation remains exact and uses literal
  `Controlling text:` and `Non-controlling plain-language summary:` labels;
- exact values, JSON, code, and transformations preserve the requested format;
- open-ended fiction produces the requested narrative while preserving voice
  and pacing; and
- complete supplied procedures preserve every step in natural order without
  demanding unnecessary system-specific detail.

Clarification is not a substitute for these requested artifacts. After a
clarification supplies recommendation inputs, the pending answer remains a
continuation and defaults to Focused unless another checkpoint rule requires
Full.

Safety, policy, legal requirements, accuracy, and explicit correction outrank
brevity in every governed response.

When a numeric recommendation lacks governing inputs, the response uses:

```text
Governing input: <missing dependency>.

Example assumption: <number and the assumption that justifies it>.
```

`Example assumption:` is the required combined Example/Assumption label. No
“good default,” “I’d use,” or numeric value or range is allowed outside this
structure.

See the [normative v0.4 specification](SPEC.md).

## Advisory and mechanical profiles

- **ChatGPT and packaged skills are Advisory.** Their ZIPs contain instructions,
  metadata, licenses, and static assets only. They have no `pc-core`, backend,
  MCP server, hook, or protocol-controlled durable topic state.
- **Ordinary Cursor and Claude Code skill use is Advisory.** Activation, topic
  inference, presentation selection, and semantic conformance remain
  probabilistic.
- **Project hook templates are Advisory/block-and-retry.** They can inspect
  an exact three-heading sequence and reject an empty view. Other visible-only
  format, budget, and duplicate judgments remain nonblocking because the hooks
  lack trusted response-kind and exception metadata.
- **The non-streaming `pc-core` wrapper enforces mechanical checks.** A trusted
  caller supplies `start`, `continue`, or `resume`, the turn classification, and
  any presentation override. The wrapper resolves presentation before
  generation, validates a versioned structured envelope, renders canonical
  Markdown, and commits per-topic state only after success.

`pc-core` stores each known topic’s branch, facts, host sessions, and whether a
topic-wide overview has been committed. Returning to a known topic restores
that mechanical state. It does not prove that the caller classified the topic
or turn correctly.

Mechanical certification does not establish semantic accuracy, completeness,
warning sufficiency, useful depth, human safe-stopping outcomes, or prompt-only
host compatibility. Without trusted expected bytes, it also does not establish
that an accepted non-fit payload equals the user's intended artifact. Those
properties remain `UNVERIFIED`.

See [Local deterministic enforcement](docs/local-enforcement.md).

## Installation

The current release-candidate package target is `0.4.3`:

- Python: `progressive-clarity-core`;
- OpenAI: `dist/progressive-clarity-openai-plugin-0.4.3.zip`;
- Claude plugin: `dist/progressive-clarity-claude-plugin-0.4.3.zip`;
- Claude.ai custom Skill:
  `dist/progressive-clarity-claude-ai-skill-0.4.3.zip`.

Use a fresh v0.4 `pc-core` state path. Earlier protocol state is intentionally
rejected rather than silently reinterpreted, even though schema `3.0.0` remains
unchanged.

See [Installation](docs/installation.md) for source, package, hook, and wrapper
instructions.

## Verification status

Protocol v0.4 and package 0.4.3 form a **locally verified release candidate**,
not a published release or universal host-compatibility claim.

Local verification covers repository contracts, the complete unit suite, compile and
lint checks, Python build/install smoke, focused and Full CLI rendering,
deterministic host-package builds, ZIP integrity, and the pinned official
Agent Skills validator. Exact artifact hashes and evidence are recorded in the
[verification record](docs/verification.md).

The optional Agno Azure harness in `tools.azure_eval_harness` automates the
behavior suite against an explicitly named deployment. It is a regression
proxy, not evidence of ChatGPT package installation or automatic activation;
see the [evaluation guide](evals/README.md).

### Historical/superseded v0.3.x ChatGPT evidence

User-provided v0.3.0–v0.3.2 testing generally passed Focused → Full → Focused →
Full cadence, explicit presentation overrides, 40/200 budgets, topic return,
safety containment, and narrative/procedure exclusions. Recurring failures
were repeated complete conclusions and warning/recovery sequences in deeper
views, overlong simple facts, unlabeled numeric assumptions, weak correction
openings, recommendations before clarification, and `Summary:` instead of the
literal non-controlling label.

The latest case record treated T02, T08, and T09 as passes; T10 topic return
passed but its initial Full answer repeated its conclusion. T01, T03, T04, T05,
T06, and T07 retained bounded failures or oracle/isolation concerns. T03 and
T06 are corrected in the v0.4 suite. All of this evidence is user-provided:
portal-byte identity and visible Skill activation were not independently
verified.

All v0.2 package hashes, uploads, transcripts, and bounded host results are
retained as historical evidence. Neither v0.2 nor v0.3.x results establish v0.4
behavior.

## Repository guide

- [Normative protocol](SPEC.md)
- [Canonical prompt-only skill](skills/progressive-clarity/SKILL.md)
- [Local enforcement architecture](docs/local-enforcement.md)
- [Installation](docs/installation.md) and [limitations](docs/limitations.md)
- [Verification record](docs/verification.md)
- [OpenAI](docs/openai-plugin.md) and
  [Claude](docs/claude-plugin.md) package records
- [Advisory host evaluation suite](evals/README.md)
- [Chat](templates/chat.md) and [document](templates/document.md) templates
- [Examples](examples/README.md)
- [License mapping](LICENSE.md) and [provenance](PROVENANCE.md)
