# Progressive Clarity

**Progressive Clarity is an AI-first response protocol with two conversation modes. Verbose mode presents three additive views at once; Progressive mode reveals the same views across turns.**

## Two conversation modes

- **Verbose mode is the default.** An ordinary in-scope request renders **At a glance**, **In context**, and **At depth** in one response, in that order.
- **Progressive mode is explicit and sticky.** The command `Progressive mode` switches the conversation until `Verbose mode` changes it or the conversation ends. A new topic resets topic depth, not the selected mode.
- A one-off request for `At a glance`, `In context`, or `At depth` changes only that response. It does not change the sticky mode.

In Progressive mode, a new topic starts with At a glance. Each unqualified `More` advances to In context and then At depth, rendering only new information. In Verbose mode, `More` adds purposeful At depth detail without replaying all three views.

## Three additive views

- **At a glance** gives the direct answer, its decision-relevant consequence, and any indispensable caveat or warning. The target is no more than 40 counted English prose words.
- **In context** adds only the rationale, scope, constraints, ownership, and action needed to understand or act. Counted prose through this view is normally capped at 200 words: combined with At a glance in Verbose mode and accumulated across turns on the active topic in Progressive mode.
- **At depth** adds purposeful evidence, assumptions, alternatives, exceptions, procedures, implementation guidance, or sources. It has no hard word cap.

## Core invariants

Every rendered view must be:

- **Complete:** it answers the immediate request at the selected depth rather than teasing later content.
- **Accurate:** later detail may qualify the answer but must not silently make an earlier statement false.
- **Additive:** an expansion contributes new information instead of replaying earlier sentences or bullets.
- **Safe to stop:** the user can stop without forming a materially wrong belief or taking a materially wrong action.

## Compact interaction

> **User:** Progressive mode. Should we delay the mobile release? Crash-free sessions are 98.7%, the gate is 99.5%, the fix is ready, and review is tomorrow.
>
> **Assistant — At a glance:** Delay the release. Crash-free sessions are below the 99.5% gate, and the fix has not completed review. Reassess after tomorrow's review instead of waiving the reliability threshold.
>
> **User:** More.
>
> **Assistant — In context:** The known defect affects startup on older devices; the current rate represents about 13 failed sessions per 1,000. Mobile engineering completes review and targeted tests tomorrow, then the release owner compares the candidate with the existing gate.

The mode command applies before the request and remains active. The second answer advances the active topic by one view and supplies only new context. See the [full expansion example](examples/two-more.md) and [mode-persistence example](examples/mode-switching.md).

## Verification status

This repository is a **non-release-ready draft** of version 0.1. Official
Agent Skills structural validation and local CI-equivalent checks pass for the
final frozen inputs:

- `SPEC.md`: `ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d`;
- `skills/progressive-clarity/SKILL.md`:
  `5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`;
  and
- `evals/cases.json`:
  `4c27a740e2e02e54f97889618397a6417c82e089b9bb44919b92642e59289680`.

The bounded Cursor cycle is closed. Round one completed 21 fresh sessions and
39 scored responses against the pre-remediation skill: 6 cases passed and 5
failed. The one permitted remediation produced the final skill above; its
targeted round completed 9 fresh sessions and 20 responses: 0 cases passed and
all 5 failed again. All 59 response-budget checks passed. Neither round had a
safety-warning or procedural-safety failure.

The policy hard stop has therefore been reached. Cursor strict acceptance,
which requires every prescribed run to pass, is **unmet**. No additional
remediation is represented or implied. Claude Code behavior remains on hold for
insufficient API credit and **UNVERIFIED**.

These results establish neither behavioral compatibility nor support for
either host. See the exact [verification record](docs/verification.md).
Release and OpenAI portal upload or submission remain blocked by failed strict
acceptance. Publication is also blocked pending professional name and trademark
clearance. Licensing authority is no longer listed as a blocker following the
authorization recorded in [Provenance](PROVENANCE.md); neither that statement
nor Git metadata is independent legal proof.

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
- Blocked [OpenAI plugin packaging record](docs/openai-plugin.md)
- Host-neutral [evaluation guide](evals/README.md) and [case suite](evals/cases.json)
- Templates: [chat](templates/chat.md) and [document](templates/document.md)
- [Protocol examples](examples/README.md)
- [License mapping](LICENSE.md): [CC BY 4.0](LICENSES/CC-BY-4.0.txt) for protocol and documentation text, and [Apache-2.0](LICENSES/Apache-2.0.txt) for skill and tooling paths
- [Provenance](PROVENANCE.md)
- [Acknowledgements](ACKNOWLEDGEMENTS.md)
