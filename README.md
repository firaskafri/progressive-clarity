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
context are current guidance. Tables, code, and warnings still consume
attention. These thresholds are design choices to evaluate, not proven optima.

## Status and guarantees

**Stable package 0.5.1 prepared (unpublished).**
See the [stable release notes](docs/release-0.5.1.md).
The [rc.21 development round](docs/release-candidate-rc21.md) cleared all 44
response judgments and the preplanned 13-response supplemental Full audit on
Azure `gpt-6-astra`. This clears the tested behavioral blocker, not publication,
other-model/host conformance, unseen holdouts, or vendor approval. The accepted candidate is committed; stable release preparation, exact-SHA CI,
and immutable remote release gates remain outstanding.
Earlier [rc.16](docs/release-candidate-rc16.md), [rc.17](docs/release-candidate-rc17.md),
[rc.18](docs/release-candidate-rc18.md), [rc.19](docs/release-candidate-rc19.md), and
[rc.20](docs/release-candidate-rc20.md) failures are preserved.
The [rc.15 composition repair](docs/release-candidate-rc15.md) completed 15
targeted responses. Bounded completion of its stalled review yielded ten PASS
and five FAIL response judgments; that historical candidate failed acceptance.
The [rc.14 complete Azure round](docs/release-candidate-rc14.md) completed all 44
responses after four passing targeted safety checks. T06's frozen expected
decision remains unmet; overall semantics are not independently adjudicated.
Stable release remains blocked; no release action has been performed.
The [rc.13 safety repair](docs/release-candidate-rc13.md) targets the failed
restart-condition and warning-coverage checks from the full Azure rc.12 round.
A [four-response rc.13 safety check](docs/azure-safety-rc13.md) still failed T05
run 1's restart condition; stable acceptance remains blocked.
The [rc.12 scope repair](docs/release-candidate-rc12.md) limits verification to
supplied criteria. Its [single T18 check](docs/sonnet-t18-rc12.md) passed, but no
full rc.12 acceptance round has run; stable acceptance remains blocked.
The [narrow rc.11 repair](docs/release-candidate-rc11.md) targets format promises
and automatic Full selection. The historical [rc.10 Sonnet round](docs/sonnet-targeted-rc10.md)
still failed format-promise and additivity checks; no full acceptance pass exists.
A [two-response rc.11 check](docs/sonnet-targeted-rc11.md) passed T15's boundary
and T18's Focused/shared-fact checks, but T18 still exceeded scope. Stable acceptance remains blocked.
Opt-in experimentation only: T10, T15, and T18 failed response-scope and
fact-preservation checks in preceding candidates. Stable 0.5.1 publication remains gated. Mechanical
validation is not behavioral certification. Read the
[experimental release notes](docs/experimental-prerelease.md) before trying it.

[rc.9 evidence](docs/release-candidate-rc9.md) and the
[instruction-delivery comparison](docs/instruction-delivery-comparison.md)
retain the failures. Repository marketplace pins and the GitHub release
resolve to published `0.5.1`. Official directory listings remain separate
submissions.

**Protocol v0.5; published package 0.5.1.** This revision introduces
usefulness-based presentation, a shorter skill, expanded development cases, and
a matched comparison/reader-study workflow.

- Versioned downloads are available in the
  [GitHub release](https://github.com/firaskafri/progressive-clarity/releases/tag/v0.5.1).
- OpenAI package 0.5.0 is published in the
  [Plugins Directory](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
- Direct Claude Code and Codex installs from the repository marketplaces are
  verified; see [Installation](docs/installation.md).
- Claude review passed for the approved source revision. Anthropic's official
  public catalog synchronization and installation from that catalog remain pending.

These are recorded release states, not a fresh availability check. Current v0.5
live-host conformance and reader benefits remain unverified. See the
[publication checklist](docs/publication-readiness.md),
[submission materials](docs/submission-materials.md), and
[verification record](docs/verification.md).

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
