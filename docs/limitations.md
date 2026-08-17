# Version 0.1 scope and limitations

Progressive Clarity version 0.1 is a draft AI-first response protocol. It
defines intended response behavior and packages that guidance as one portable,
instruction-only Agent Skill. It does not establish host support, guaranteed
model behavior, or measured reader outcomes.

[`SPEC.md`](../SPEC.md) is normative for conversational responses. Templates,
examples, installation guidance, and the document-mode adaptation are
informative when they differ from the specification.

## What version 0.1 covers

Version 0.1 defines:

- the **At a glance**, **In context**, and **At depth** views;
- complete, accurate, additive, and safe-to-stop response invariants;
- explicit depth requests, automatic depth selection, incremental “more”
  requests, targeted expansion, topic reset, and explicit correction;
- optional clarity cues;
- observable evaluation criteria; and
- one standard Agent Skill containing instructions for that behavior.

It is a conversational response protocol, not a general document format.
Document mode is an informative adaptation. Procedures and tutorials retain
their necessary sequence, controlling legal text remains unchanged, and
narrative or voice-dependent writing retains its required structure.

## English-only word budgets

Version 0.1 defines budget conformance for English responses only:

- **At a glance** targets no more than 40 counted words.
- Counted prose for an active topic through **In context** normally has a
  cumulative hard cap of 200 words. Earlier At a glance prose and targeted
  branches at either shallow view contribute to that same total.
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
- If the host exposes no internal state trace, selected view, branch focus,
  and topic reset may be `UNVERIFIED`. Their rendered consequences remain
  observable pass/fail criteria.

Wave 3 used the same frozen skill and protocol revision for Cursor and Claude
Code. Official structural validation and local repository checks pass.
Cursor received a byte-identical project installation, but authentication
blocked runtime discovery and behavior. Claude Code discovered and explicitly
loaded its byte-identical project installation, but insufficient API credit
blocked inference. All rendered behavior, all Cursor invocation dimensions,
and automatic or negative activation in both hosts remain `UNVERIFIED`.
The exact environments, hashes, commands, and rerun requirements are in the
[verification record](verification.md).

## No host support or compatibility claim

The observed Cursor copy integrity and Claude Code discovery and explicit-load
evidence prove only those stated dimensions. They do not establish that either
host follows Progressive Clarity. Version 0.1 therefore claims no behavioral
compatibility or installation support for either host.

It also makes no compatibility claim for Codex, GitHub Copilot, Gemini CLI, or
any other agent, editor, CLI, marketplace, plugin system, or hosted service.
Following the Agent Skills directory format is a portability design choice,
not evidence that another host discovers, invokes, or follows this skill
correctly.

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
- a plugin, marketplace package, or compatibility adapter;
- a live web demo, submitted user text, analytics, or a custom domain;
- certification or universal conformance claims; or
- formal participant research.

Manual installations are copies and can drift from the canonical source.
Updates require replacing the installed skill directory with the complete
directory from a selected repository revision.
