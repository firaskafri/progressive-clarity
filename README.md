# Progressive Clarity

**Answer first. Add depth when it helps. Keep follow-ups natural.**

Progressive Clarity is a response protocol for AI assistants. It puts the answer
and its important qualifications up front, then adds useful rationale and detail
when a topic needs orientation or a decision checkpoint.

## The practical difference

Illustrative example: an index passed validation and rollback checks in staging;
production has not been approved.

> **User:** Can we enable the index?
>
> **Poorly qualified answer:** Yes, enable it. The checks passed, and rollback
> is available. … This applies only to staging; production is not approved.
>
> **Progressive Clarity:** Enable it in **staging only**. Validation and rollback
> checks passed; production has not been approved.

The scope belongs beside the recommendation, where someone stopping early will
see it. An important decision can still have a short answer.

For a more involved orientation, the assistant uses three additive views:

1. **At a glance** — answer, scope, consequence, and indispensable caveat.
2. **In context** — rationale, constraints, ownership, timing, or next action.
3. **At depth** — evidence, assumptions, alternatives, implementation, or sources.

Ordinary follow-ups return to a focused answer. Re-synthesize when decisions or
context change, using three views only when distinct layers help. See the
[conversation example](examples/topic-lifecycle.md).

## Try the skill

Copy `skills/progressive-clarity/` as a complete directory into your host's skill
location. For a Claude Code project, from this checkout:

```sh
mkdir -p "/path/to/project/.claude/skills"
cp -R skills/progressive-clarity "/path/to/project/.claude/skills/"
```

Invoke `/progressive-clarity`. For Cursor, packaged uploads, and the optional
Python wrapper, see [Installation](docs/installation.md).

## Principles

- **Use proportionate structure.** Simple facts, ordinary exploration, and compact
  consequential answers stay Focused. Explicit presentation requests take precedence.
- **Make depth additive.** Brief repetition may help comprehension or qualify an
  action; duplicated explanations and automatic recaps should be removed.
- **Ask useful questions.** Obtain decisive missing inputs, with a short rationale
  or supported bounded answer when helpful.
- **Expose assumptions.** Numeric advice may use a question, formula, or conditional
  example. It does not require fixed labels or an invented example number.
- **Repair errors naturally.** Identify the error and replacement, and explain any
  changed consequence. No mandatory sentence template.
- **Preserve the artifact.** Exact text, code/data formats, fiction, and complete
  procedures keep the shape their purpose requires.

For English Full answers, 40 words at a glance and 200 cumulatively through
context are provisional guidance. Tables, code, and warnings still consume
attention. These thresholds are design choices to evaluate, not proven optima.

## Status and guarantees

**Protocol v0.5 draft; coordinated package target 0.5.0.** This revision introduces
usefulness-based presentation, a shorter skill, expanded development cases, and
a matched comparison/reader-study workflow. See the [verification record](docs/verification.md)
for checks actually run. Live-host conformance and reader benefits remain unverified.

The skill is **Advisory**: prompt-only instructions cannot guarantee activation,
topic memory, or semantic quality. The optional non-streaming **`pc-core` wrapper**
checks structured output and state transitions and retains hard 40/200 caps.
It reports lexical repetition without rejecting it automatically. Mechanical
conformance does not establish accuracy or usefulness.

Use a fresh v0.5 wrapper state path. Request schema `4.0.0` adds `depth_useful`;
envelope and state schemas remain `3.0.0` with protocol `0.5`.

## Explore and evaluate

- [Specification and precedence table](SPEC.md)
- [Compact runtime skill](skills/progressive-clarity/SKILL.md)
- [Examples](examples/README.md) and [chat template](templates/chat.md)
- [Mechanical wrapper](docs/local-enforcement.md) and [limitations](docs/limitations.md)
- [Development evaluation](evals/README.md), [unseen holdouts](evals/holdouts.md),
  and [blinded reader study](evals/reader-study.md)
- [OpenAI](docs/openai-plugin.md) and [Claude](docs/claude-plugin.md) packages
- [License](LICENSE.md) and [provenance](PROVENANCE.md)

The comparison workflow tests ordinary responses, minimal principles, the archived
v0.4 long skill, and the revised skill with the same model and tasks. It records
protocol compliance separately from reader interpretation, retrieval time, and
preference.
