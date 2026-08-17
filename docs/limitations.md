# Version 0.1 scope and limitations

Progressive Clarity version 0.1 is a non-release-ready draft AI-first response
protocol with two conversation modes. Verbose mode presents all three additive
views in one response. Progressive mode reveals them across turns. The
portable Agent Skill is instruction-only; it does not establish host support,
guaranteed model behavior, or measured reader outcomes.

[`SPEC.md`](../SPEC.md) is normative for conversational responses. Templates,
examples, installation guidance, and the document-mode adaptation are
informative when they differ from the specification.

## What version 0.1 covers

Version 0.1 defines:

- the **At a glance**, **In context**, and **At depth** views;
- default Verbose mode and explicit, sticky Progressive mode;
- the `Progressive mode` and `Verbose mode` state commands;
- one-response view overrides that do not change sticky mode;
- complete, accurate, additive, and safe-to-stop response invariants;
- incremental `More` requests, targeted expansion, topic reset, and explicit
  correction;
- optional clarity cues;
- observable evaluation criteria; and
- one standard Agent Skill packaging target for that behavior.

It is a conversational response protocol, not a general document format.
Document mode is an informative adaptation. Procedures and tutorials retain
their necessary sequence, controlling legal text remains unchanged, and
narrative or voice-dependent writing retains its required structure.

## Dual-mode contract

A new conversation starts in **Verbose mode**. For each ordinary in-scope
request, one response renders the visible headings **At a glance**,
**In context**, and **At depth**, in that order. The sections are cumulative
but additive: each deeper section contributes new information instead of
restating an earlier section.

`Progressive mode` switches to **Progressive mode** and remains active until
`Verbose mode` changes it or the conversation ends. Treat either phrase
case-insensitively when it is a command or clear mode directive. A new topic
resets topic depth, branch focus, and the cumulative topic count, but it does
not reset the sticky mode. In Progressive mode, a new topic starts at
At a glance; each unqualified `More` advances to In context and then At depth.

An explicit request for `At a glance`, `In context`, or `At depth` is a
one-response presentation override. It does not change the sticky mode. When a
message contains both a mode command and a view override, the mode change
applies first, the requested view applies to that response, and the new mode
remains active afterward.

Every rendered view has a visible view heading. A standalone mode command is
control dialogue: it renders no view and consumes no view budget. Correctness,
indispensable warnings, and the minimum safe answer take precedence over every
mode or override.

## English-only word budgets

Version 0.1 defines budget conformance for English responses only:

- **At a glance** has a 40-word cap. Only an indispensable warning may exceed
  it, and only as far as the warning requires.
- Counted prose for an active topic through **In context** normally has a
  cumulative hard cap of 200 words. In Verbose mode, combine At a glance and
  In context prose in the response. In Progressive mode, accumulate those
  views across turns on the active topic. Targeted shallow branches contribute
  to the same total.
- **At depth** has no hard word cap, but every section must remain relevant,
  additive, and purposeful.
- An indispensable warning may exceed a budget only as far as the warning
  requires. Necessary correction text has the limited exemption defined in
  the specification.
- A budget never permits omission of a required fact or warning.

The count is human-scored. Reader-visible prose counts, including cue labels,
list text, visible link text, and inline code. Headings, Markdown syntax,
destination or bare URLs, fenced code blocks, data tables, citation markers,
non-rendered state notes, user prompts, and pure control dialogue do not count.
After removing Markdown punctuation, each whitespace-separated token
containing an English letter or digit counts as one word.

Version 0.1 makes no word-budget claim for non-English or mixed-language
responses. A response in another language may still use the qualitative
invariants, but it cannot claim v0.1 budget conformance.

## Verification semantics

Version 0.1 separates rendered behavior from host activation and hidden state.
Verification records `PASS`, `FAIL`, or `UNVERIFIED`:

- Observable response requirements, such as required facts, caveats, order,
  budgets, corrections, and prohibited repetition, can pass or fail from the
  rendered output.
- A **host trace** is host-exposed evidence that the named skill or protocol
  loaded. If the host exposes no such evidence, activation or inactivity may
  be `UNVERIFIED`.
- `UNVERIFIED` means that the available evidence cannot establish the claim.
  It is neither a pass nor a failure, and it must not be reported as support.
- Behavior that resembles Progressive Clarity is not proof of activation.
  Conversely, a host trace does not prove that the rendered response conforms.
- If the host exposes no internal state trace, sticky mode, selected view,
  branch focus, and topic reset may be `UNVERIFIED`. Their rendered
  consequences remain observable pass/fail criteria.

The bounded dual-mode Cursor cycle completed but failed strict acceptance.
Round one used the pre-remediation skill and completed 21 fresh sessions and
39 scored responses: 6 cases passed and 5 failed. The one permitted revision
produced the final frozen skill. Its targeted round reran the five failed cases
in 9 fresh sessions and 20 responses: 0 passed and 5 failed. The mandatory hard
stop was then reached.

All 59 budget checks across both rounds passed. The indispensable-warning
checks in `M05` and procedural order and safety branches in `M10` passed in
both rounds; there were no safety-warning or procedural-safety failures. These
results neither erase the five case failures nor establish safety. The final
skill received only the prescribed targeted rerun, not a new full-suite round.
No additional remediation is represented or implied.

Claude Code's earlier discovery mechanism used the former protocol. Current
behavior is on hold because Claude Code reported insufficient API credit before
inference and remains `UNVERIFIED`. The exact inputs, counts, failures, and
evidence boundaries are in the [verification record](verification.md).

## No host support or compatibility claim

Current Cursor evidence contains case-specific activation and behavior passes,
but the repeated five-case failure and hard stop prevent a compatibility or
support claim. No current evidence establishes that Claude Code discovers,
invokes, or follows the dual-mode contract. Version 0.1 therefore claims no
behavioral compatibility or installation support for either host.

It also makes no compatibility claim for Codex, GitHub Copilot, Gemini CLI, or
any other agent, editor, CLI, marketplace, plugin system, or hosted service.
Following the Agent Skills directory format is a portability design choice,
not evidence that another host discovers, invokes, or follows this skill
correctly.

OpenAI packaging and access status remains separate. See
[OpenAI plugin packaging](openai-plugin.md); this document makes no additional
OpenAI compatibility, approval, publication, or support claim. Portal upload
and submission are blocked because Cursor strict acceptance failed, and no
upload occurred.

The locally installed GitHub CLI is version `2.62.0` and does not expose the
upstream preview skill commands. GitHub CLI installation and update workflows
therefore remain untested and are not recommended in version 0.1.

## No empirical reader-outcome claim

The safe-stopping check is an evaluation proxy: it checks whether the rendered
response contains the facts and indispensable caveats defined by a case. It
does not establish what a human reader understood, remembered, believed, or
did.

Version 0.1 has no formal human-subject study or validated field evidence. It
does not claim proven gains in comprehension, decision quality, accessibility,
task completion, safety, productivity, reading time, or token use. Model
evaluation results, when available, demonstrate only performance on the
specified cases and host versions.

## Instruction-only security posture

The version 0.1 skill:

- contains no executable scripts;
- grants or pre-approves no tools;
- requires no network access;
- starts no service or background process; and
- includes no analytics, telemetry, or user-input collection.

This narrow package reduces installed capability, but it is not a security
certification or sandbox. The host still controls its model, tools, permissions,
network access, and data handling. The protocol does not override
higher-priority safety, policy, legal, or accuracy requirements, and it cannot
guarantee that a model will follow its instructions.

## Operational exclusions

Version 0.1 does not include:

- executable helpers, hosted AI services, or runtime dependencies;
- always-on rules or vendor-specific skill frontmatter;
- an automated installer, updater, or uninstaller;
- an uploaded, submitted, approved, or published plugin, marketplace listing,
  or compatibility adapter;
- a live web demo, submitted user text, analytics, or a custom domain;
- certification or universal conformance claims; or
- formal participant research.

Manual installations are copies and can drift from the canonical source.
Updates require replacing the installed skill directory with the complete
directory from a selected repository revision.
