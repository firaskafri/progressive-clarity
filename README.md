# Progressive Clarity

**Progressive Clarity is an AI-first response protocol that renders three
additive views in every ordinary in-scope response.**

## One response contract

1. **At a glance** gives the direct answer, consequence, material scope, and
   indispensable caveat in at most 40 counted English prose words.
2. **In context** adds rationale, constraints, ownership, timing, controls, or
   action. Non-warning prose through this section totals at most 200 words.
3. **At depth** adds purposeful evidence, assumptions, measurements,
   alternatives, exceptions, implementation, or sources without a hard cap.

Each fact belongs in one view. Deeper sections add information instead of
recapping earlier facts. Safety, legal, and accuracy requirements outrank
brevity. Corrections explicitly retract and replace errors. Clarifications,
complete procedures, controlling text, exact outputs, transformations, and
narratives retain the structure required by their purpose.

See the [normative v0.2 specification](SPEC.md).

## Advisory and Enforced surfaces

- **ChatGPT is Advisory.** Its deterministic ZIP contains only the prompt-only
  skill, license, manifest, and static assets. It has no backend or MCP server.
- **Ordinary Cursor and Claude Code skill use is Advisory.** Prompt adherence
  is not a deterministic gate.
- **Project hook templates are Advisory/block-and-retry.** They inspect output
  after generation and cannot reliably retract every displayed candidate.
- **The non-streaming `pc-core` wrapper Enforces mechanical checks.** It
  validates a versioned envelope, mandatory three-view order, 40/200 budgets,
  non-empty view prose, fact IDs and declared reuse, optional authoritative
  fact-catalog coverage, correction/quotation structure, exact lexical echoes
  in Progressive Clarity explanation, verbatim-artifact exemptions, explicit
  topic/branch/turn state, and cross-turn host-session resume. It emits only
  canonical Markdown after a pass and permits at most two total candidates.

Mechanical certification applies only to output buffered and released by that
wrapper. It does not establish accuracy, completeness, warning necessity,
human safe stopping, semantic repetition, purposeful depth, hidden-reversal
absence, caller-catalog correctness or completeness, or host-wide
compatibility. Those remain advisory `UNVERIFIED`.

See [Local deterministic enforcement](docs/local-enforcement.md).

## Example

> **User:** Should we delay the mobile release? Crash-free sessions are 98.7%,
> the gate is 99.5%, the fix is ready, and review is tomorrow.
>
> **At a glance:** Delay the release. Crash-free sessions remain below the
> 99.5% gate; reassess after tomorrow's fix review instead of waiving the
> reliability threshold.
>
> **In context:** The release owner should compare the reviewed candidate with
> the existing gate before scheduling rollout.
>
> **At depth:** Test the affected startup path on older devices and preserve a
> rollback trigger tied to the same crash-free-session metric.

## Verification status

Protocol v0.2 and package v0.2.1 remain a **non-release-ready draft**. The
v0.2.1 ChatGPT ZIP is Advisory and has not been uploaded. Local verification
covers deterministic mechanics, package integrity, links, lint, and structural
skill validation.

One bounded live Cursor wrapper remediation rerun produced 17 responses: 10
were mechanically certified and 7 were withheld. `E02`, `E06`, and `E07`
passed; `E03`, `E04`, and `E05` failed. The rerun verified the targeted
session-resume, non-empty-view, explicit-trust, catalog-coverage, and
fail-closed mechanics, but strict semantic and behavioral acceptance remains
unmet. It used the pre-trigger-revision skill, so it is not a prompt-only
acceptance result for the current v0.2.1 bytes.

No current prompt-only Cursor, Claude Code, or ChatGPT acceptance run exists.
The Claude Code adapter and hook are structurally tested, but live Claude Code
wrapper behavior remains `UNVERIFIED` because it requires paid Anthropic API
access and no paid live run was completed.

The preceding bounded Cursor cycle belongs to older dual-behavior inputs. It
ended at its required hard stop: round one passed 6 of 11 cases; its one
targeted remediation round failed all 5 rerun cases. Across both rounds, all 59
budget checks passed and no safety-warning or procedural-safety branch failed.
These results do not verify v0.2.

On 2026-08-17, the user reported publication of an older ChatGPT plugin as
[`plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
An anonymous fetch confirmed only a login-gated ChatGPT Plugins route. This URL
is retained as historical publication evidence; it is not evidence that the
v0.2.1 ZIP was uploaded.

The user also supplied a live transcript from the older published build. It is
historical, user-provided evidence: heading order, staged transitions, and
caveats passed; 40/200 budgets and no-fact-repetition failed; post-switch-back
behavior remained `UNVERIFIED`. A later user-provided pre-v0.2.1 transcript
missed the initial three-view response and then described removed modes. Both
records are non-conformant historical evidence, not current v0.2.1 conformance
or activation evidence.

See the exact [verification record](docs/verification.md) and
[OpenAI publication record](docs/openai-plugin.md).

## Repository guide

- [Normative protocol](SPEC.md)
- [Canonical prompt-only skill](skills/progressive-clarity/SKILL.md)
- [Local enforcement architecture](docs/local-enforcement.md)
- [Installation](docs/installation.md) and [limitations](docs/limitations.md)
- [Verification record](docs/verification.md)
- [OpenAI package record](docs/openai-plugin.md)
- [Advisory host evaluation suite](evals/README.md)
- [Chat](templates/chat.md) and [document](templates/document.md) templates
- [Examples](examples/README.md)
- [License mapping](LICENSE.md) and [provenance](PROVENANCE.md)
