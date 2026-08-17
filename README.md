# Progressive Clarity

**Progressive Clarity is an AI-first response protocol. It gives a complete answer at the shallowest useful view, then adds context and detail without repetition or hidden reversal.**

## Three views

- **At a glance** gives the direct answer, its decision-relevant consequence, and any indispensable caveat or warning. The target is no more than 40 counted English prose words.
- **In context** adds only the rationale, scope, constraints, ownership, and action needed to understand or act. Counted prose for the active topic through this view is normally capped at 200 words, including an earlier At a glance turn, with only the specification's warning and correction exceptions.
- **At depth** adds purposeful evidence, assumptions, alternatives, exceptions, procedures, implementation guidance, or sources. It has no hard word cap.

## Core invariants

Every rendered view must be:

- **Complete:** it answers the immediate request at the selected depth rather than teasing later content.
- **Accurate:** later detail may qualify the answer but must not silently make an earlier statement false.
- **Additive:** an expansion contributes new information instead of replaying earlier sentences or bullets.
- **Safe to stop:** the user can stop without forming a materially wrong belief or taking a materially wrong action.

## Compact interaction

> **User:** Should we delay the mobile release? Crash-free sessions are 98.7%, the gate is 99.5%, the fix is ready, and review is tomorrow.
>
> **Assistant — At a glance:** Delay the release. Crash-free sessions are below the 99.5% gate, and the fix has not completed review. Reassess after tomorrow's review instead of waiving the reliability threshold.
>
> **User:** More.
>
> **Assistant — In context addition:** The known defect affects startup on older devices; the current rate represents about 13 failed sessions per 1,000. Mobile engineering completes review and targeted tests tomorrow, then the release owner compares the candidate with the existing gate.

The second answer advances the active topic by one view and supplies only new context. See the [full expansion example](examples/two-more.md).

## Verification status

This repository is a pre-release draft of version 0.1. Official Agent Skills structural validation and the local CI-equivalent repository checks pass for the frozen skill and evaluation inputs.

Host evidence remains limited:

- Cursor 3.15.19 and Agent CLI `2026.01.23-916f423` received a byte-identical project copy of the skill. Runtime discovery, invocation, activation, and all behavior are **UNVERIFIED** because the Agent CLI was not authenticated.
- Claude Code 2.1.72 discovered the byte-identical project skill and explicitly loaded it, so those two dimensions pass. All rendered behavior and automatic or negative activation are **UNVERIFIED** because the API rejected the first request for insufficient credit before inference.

These results do not establish behavioral compatibility or support for either host. See the exact [verification record](docs/verification.md).

Publication remains gated on completed host behavior testing, confirmation of licensing authority, and name-risk review. “Progressive Clarity” has not received professional trademark clearance.

## Scope and limitations

- [`SPEC.md`](SPEC.md) is normative for conversational AI responses. The [document template](templates/document.md) is an informative adaptation, not a second protocol.
- Version 0.1 defines word-budget conformance for English responses only.
- Correctness, indispensable warnings, and higher-priority safety, policy, and legal requirements take precedence over brevity.
- Procedures, controlling legal text, and voice-dependent narratives retain the structure their purpose requires; Progressive Clarity may provide a separate overview where appropriate.
- The protocol defines intended, observable response behavior. Its empirical effectiveness and human reader outcomes have not been established.
- No host has been behaviorally verified as compatible, and no installation support is offered.

## Repository guide

- [Normative protocol](SPEC.md)
- [Canonical Agent Skill](skills/progressive-clarity/SKILL.md)
- Evidence-limited [installation guide](docs/installation.md), exact [verification record](docs/verification.md), and [version 0.1 limitations](docs/limitations.md)
- Host-neutral [evaluation guide](evals/README.md) and [case suite](evals/cases.json)
- Templates: [chat](templates/chat.md) and [document](templates/document.md)
- [Protocol examples](examples/README.md)
- [License mapping](LICENSE.md): [CC BY 4.0](LICENSES/CC-BY-4.0.txt) for protocol and documentation text, and [Apache-2.0](LICENSES/Apache-2.0.txt) for skill and tooling paths
- [Provenance](PROVENANCE.md)
- [Acknowledgements](ACKNOWLEDGEMENTS.md)
