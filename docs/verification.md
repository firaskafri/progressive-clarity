# Verification record

This record separates the current revised artifacts and deterministic local
mechanics from the preceding bounded prompt-only host cycle and from
user-provided ChatGPT evidence. The preceding Cursor cycle ended in failure at
its required hard stop. The v0.2.1 prompt-only skill has no new host acceptance
run. Progressive Clarity protocol v0.2 and package v0.2.1 remain a
**non-release-ready draft**.

## Result labels

- **PASS** means direct evidence establishes only the named check against the
  named frozen revision.
- **FAIL** means observable output violates a requirement of that frozen
  revision.
- **UNVERIFIED** means available evidence cannot establish the claim. It is
  neither a pass nor a failure.
- **HISTORICAL/SUPERSEDED** means the result belongs to an older contract and
  must not be used as evidence for v0.2.
- **MECHANICALLY_CERTIFIED** means the non-streaming local wrapper validated a
  trusted request, committed state, schema `2.0.0` envelope, and canonical
  rendering. It is not a semantic `PASS`.

A file copy, structural validation, discovery trace, or explicit load does not
establish rendered behavior. Similar output without a host trace does not
establish activation.

## Current conformance surfaces

- **ChatGPT:** v0.2.1 is Advisory prompt-only. No backend or MCP is required.
  The v0.2.1 ZIP has not been uploaded.
- **Cursor and Claude Code skills:** Advisory prompt-only. No current-revision
  host acceptance run exists.
- **Project hook templates:** Advisory/block-and-retry. Current official hook
  contracts cannot provide the same reliable full-response fail-closed gate as
  the wrapper.
- **`pc-core` non-streaming wrapper:** Enforced mechanical when it emits output
  after a pass. Unit/property tests, an isolated installed-wheel smoke, and one
  bounded live Cursor remediation rerun exercise this path. Live Claude Code
  wrapper execution remains `UNVERIFIED` because paid Anthropic API access is
  required and no paid live run was completed.

Mechanical enforcement covers versions, topic/branch/turn arithmetic,
three-view heading order, English budgets, fact-ID integrity and declared reuse,
correction/quotation structure, exact lexical duplicates in Progressive Clarity
view and explanatory prose while required verbatim artifact bytes remain
exempt, canonical view rendering, byte-preserving accepted non-fit payloads,
and atomic state commit. Accuracy, completeness beyond a supplied authoritative
catalog, catalog correctness or completeness, warning indispensability, human
safe stopping, paraphrased repetition, purposeful detail, and hidden reversal
remain advisory `UNVERIFIED`.

## Current protocol v0.2 and package v0.2.1 target

The normative [`SPEC.md`](../SPEC.md) defines one ordinary in-scope behavior:
every response renders **At a glance**, **In context**, and **At depth** once
and in order. At a glance has a 40-word non-warning cap; non-warning prose
through In context has a 200-word per-response cap; At depth is unrestricted
but purposeful. Targeted follow-ups retain all three views. Clarification,
correction, controlling text, exact output, procedure, narrative, and safety
exceptions remain explicit.

There is no presentation depth, progression, alternate behavior, or cross-turn
shallow-word accumulation.

## Current revised inputs

The current synchronized v0.2.1 package inputs are:

- [`SPEC.md`](../SPEC.md): SHA-256
  `74d2df5d443e9bb8a9dd3612f96397e8050ce8c1b71ac0eea34cd209d19adfe8`;
- [`skills/progressive-clarity/SKILL.md`](../skills/progressive-clarity/SKILL.md):
  SHA-256
  `ab8d3ba8e9aa02530f97d21af15ff371ec0df02055b6e2f0cff665c36c59a749`;
- [`evals/cases.json`](../evals/cases.json): SHA-256
  `8788528b11667b99a8ba398efe1dd17da3b302c687e584e5c07ca94f84f17eb4`;
- rebuilt prompt-only OpenAI ZIP: SHA-256
  `d5e447abc41132a3e5d0580b5afc5231230317dead1adcee5767085159cbde23`;
  and
- local envelope, state, validator, renderer, adapters, and tests under
  `pc_core/`, `adapters/`, and `tests/`.

The v0.2 evaluation suite identifies prompt-only host behavior as Advisory.
No prompt-only Cursor, Claude Code, or ChatGPT acceptance run has been executed
against these current skill bytes. Local tests validate mechanics and wrapper
state; the live evidence below covers the separate Cursor wrapper boundary.

### Bounded live Cursor wrapper remediation

The initial live Cursor enforcement run was frozen to skill SHA-256
`5f9f7881588ce02f14a122fcd6fef1cc98d7e7a3e415afd61dc5f0a3d37fab01`,
SPEC SHA-256
`74d2df5d443e9bb8a9dd3612f96397e8050ce8c1b71ac0eea34cd209d19adfe8`,
and evaluation SHA-256
`8788528b11667b99a8ba398efe1dd17da3b302c687e584e5c07ca94f84f17eb4`.
The skill hash is a pre-trigger-revision evidence identifier, not a current
repository pin. Its files and scoring inputs were not changed. The initial run
failed E02-E07 and exposed four wrapper defects: per-turn host sessions,
certifiable empty views, implicit fresh-workspace trust assumptions, and a
model-defined completeness boundary.

One authorized remediation rerun then executed E02-E07 once with prescribed
repetitions against the same frozen skill while exercising the mechanical
wrapper fixes, then stopped. It preserved 162 evidence files under
`/private/tmp/progressive-clarity-v02-cursor-live-5f9f7881/evidence/remediation-live-20260818`.
Of 17 responses, 10 were mechanically certified and 7 were withheld after two
attempts with empty release files and unchanged local state. The architecture
targets passed: both eligible follow-up turns resumed their committed Cursor
session; all 15 sections in five certified view responses were non-empty; all
eight certified responses supplied an authoritative catalog passed exact
catalog coverage; and the adapter added no trust flag after the earlier
explicit isolated bootstrap.

The behavioral suite still failed overall: E02, E06, and E07 passed; E03,
E04, and E05 failed. E03 repeatedly returned Markdown instead of envelopes,
one E04 repetition was withheld, and E05's clarification did not directly ask
for the missing environment. This is the required hard stop; no further prompt
or live rerun is authorized in this remediation.

## Current local verification

On 2026-08-18, the CI-equivalent local checks produced:

- `PASS`: 64 standard-library unit/property tests under Python `3.11.15`,
  including the activation-only trigger fixture and synthetic
  invalid-then-valid wrapper repair smoke test;
- `PASS`: repository hashes, schema/references, whitespace, relative links,
  ordered test-docstring contracts, complete host-template shape, Python
  package metadata, skill package shape, and OpenAI source inventory;
- `PASS`: Ruff `0.12.9` over `pc_core`, `tests`, and `tools`;
- `PASS`: isolated Python 3.11 sdist/wheel build, wheel install, `pc_core`
  import outside the checkout, `pc-core` console-script smoke, and a
  project-local installed-hook command smoke;
- `PASS`: official `skills-ref` validation at pinned agentskills revision
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`;
- `PASS`: two byte-identical OpenAI package builds, ZIP integrity, normalized
  inventory, and source-byte equivalence; and
- `PASS`: local host adapter argv/result parsing without network inference.

The installed Cursor Agent CLI reported `2026.08.11-e8db854`; Claude Code
reported `2.1.72`. Their current official hook and non-streaming CLI contracts
were reviewed. Local passes establish deterministic mechanics and package
integrity; the separate bounded evidence above establishes only the recorded
Cursor wrapper observations.

## Retained older host-cycle inputs

The closed dual-behavior Cursor cycle remains frozen at its original inputs:

- [`SPEC.md`](../SPEC.md): SHA-256
  `ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d`;
- [`skills/progressive-clarity/SKILL.md`](../skills/progressive-clarity/SKILL.md):
  SHA-256
  `5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`;
- [`evals/cases.json`](../evals/cases.json): SHA-256
  `4c27a740e2e02e54f97889618397a6417c82e089b9bb44919b92642e59289680`.

These hashes are evidence identifiers, not current repository pins. The
current validator and CI pin the revised inputs above and evaluation schema
`4.0.0`. Do not reuse a prior prompt, score, trace, or result merely because its
case name still exists.

## Host discovery paths

These are documented host paths, not current v0.2 verification results:

- Cursor project: `.agents/skills/progressive-clarity/` or
  `.cursor/skills/progressive-clarity/`;
- Cursor user: `~/.agents/skills/progressive-clarity/` or
  `~/.cursor/skills/progressive-clarity/`;
- Claude Code project: `.claude/skills/progressive-clarity/`; and
- Claude Code user/personal: `~/.claude/skills/progressive-clarity/`.

The completed Cursor cycle used one isolated project copy and recorded its
exact path, host and model versions, frozen artifact hashes, invocation
method, and available host traces. The documented paths alone neither
authorize another run nor establish support.

## Cursor status

**Current status: revised prompt-only behavior UNVERIFIED; preceding strict
acceptance unmet; bounded live Cursor wrapper rerun completed and still failed
overall; hard stop reached.**

The retained preceding cycle used Cursor desktop `3.15.19`, Cursor Agent CLI
`2026.08.11-e8db854`, and model `GPT-5.6 Sol 272K Medium`. The bounded policy
required one complete initial round, allowed no more than one skill revision,
required every initially failed case to be rerun with all of its prescribed
repetitions, and required the cycle to stop after that targeted round
regardless of outcome. Every prescribed run had to pass; there was no majority
vote or intermittent-failure allowance.

### Round one

Round one used the frozen specification and cases above with pre-remediation
skill SHA-256
`168e2c301cd0a18f4f83161b70d61445ad926ba9d71f944d70c9c323972e0908`.
It completed 21 fresh sessions and 39 scored assistant responses with no
transient retries:

- cases: 6 `PASS`, 5 `FAIL`;
- facts: 200 `PASS`, 11 `FAIL`;
- budgets: 39 `PASS`, 0 `FAIL`;
- activation: 8 `PASS`, 1 `FAIL`, 2 `UNVERIFIED`; and
- internal state: 11 `UNVERIFIED`.

`M01`, `M03`, `M06`, `M08`, `M09`, and `M11` passed. The five failures were:

- `M02`: 62/66 facts; all three At-a-glance responses omitted the required
  Android 13 checkout-crash scope, and run 1 also omitted the 12 September
  date. Progressive advances and the switch to Verbose rendered correctly.
- `M04`: 8/12 facts; `$120,000 annually` and the two-weekend migration
  duration were absent at both required stopping points.
- `M05`: 20/21 facts; run 1 omitted the 14:30 report fact. All indispensable
  warning and payment-safety checks passed.
- `M07`: 5/7 facts; the clarification omitted environment or rollout scope,
  and staging monitoring was not connected to the pre-production decision
  gate.
- `M10`: procedural behavior, step order, and safety branches passed, but
  activation failed because Cursor read the skill despite `remain_inactive`.

### One permitted remediation round

The one permitted revision produced the final frozen skill SHA-256
`5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`.
Only `M02`, `M04`, `M05`, `M07`, and `M10` were rerun, with their prescribed
repetitions. The targeted round completed 9 fresh sessions and 20 responses
with no transient retries:

- cases: 0 `PASS`, 5 `FAIL`;
- facts: 103 `PASS`, 10 `FAIL`;
- budgets: 20 `PASS`, 0 `FAIL`;
- activation: 4 `PASS`, 1 `FAIL`; and
- internal state: 5 `UNVERIFIED`.

The targeted outcomes were:

- `M02`: 63/66 facts; Android 13 scope was present, but all three At-a-glance
  responses omitted the required 12 September launch date.
- `M04`: 8/12 facts; the exact annual savings and two-weekend migration
  duration remained absent at both stopping points.
- `M05`: 20/21 facts; run 3 omitted the 14:30 report fact. All indispensable
  warning and payment-safety checks passed.
- `M07`: 5/7 facts; environment or rollout scope remained absent from the
  clarification, and monitoring remained unconnected to the pre-production
  decision gate.
- `M10`: procedural behavior, step order, and safety branches passed, but
  activation again failed because Cursor read the skill despite
  `remain_inactive`.

Across both rounds, all 59 budget checks passed. There were no safety-warning
or procedural-safety failures. Those bounded positives do not erase any case
failure and are not a safety certification.

The second round triggered the mandatory hard stop. No further remediation was
performed within that cycle or is implied by this record. That cycle's final
skill received only the prescribed targeted rerun, not a new full-suite round,
so this evidence cannot establish Cursor compatibility or support.

The current v0.2.1 trigger-recall skill is a new input, not another remediation
round, and has no prompt-only Cursor host result. The bounded live rerun used
the pre-trigger-revision skill while exercising the remediated wrapper. It
therefore establishes only the 10 certified and 7 withheld wrapper
observations above; it does not transfer a semantic or prompt-only acceptance
result to the current skill.

All former-protocol Cursor evidence remains **historical and superseded**. It
must not be aggregated with this cycle.

## Claude Code status

**Current status: revised prompt-only and live wrapper behavior UNVERIFIED; a
live run requires paid Anthropic API access and was not completed.**

Claude Code 2.1.72 previously:

- scanned `.claude/skills/progressive-clarity/` as a project skill;
- listed `progressive-clarity` as a skill and slash command; and
- parsed `/progressive-clarity` and attached the former skill text.

That observation used the former protocol and does not verify v0.2 or its
current skill. The first API request stopped before
inference with `Credit balance is too low`. Input and output tokens were zero,
cost was `$0`, and no assistant response was scored. No Claude Code behavior
result is represented by this finalization. Completing a live run requires
paid API credit; structural checks do not remove that paid-access requirement.

The current project Stop-hook template follows the documented
`last_assistant_message` and `decision: "block"` schema. The non-streaming
adapter follows documented `claude -p --output-format json` and `--resume`
behavior. These structures and synthetic parsing are locally tested, but no
live Claude inference was run and no compatibility claim follows.

## Strict acceptance rule and outcome

The preceding host cycle scored visible mode behavior, cumulative facts,
required caveats, additive views, budgets, corrections, controlling text,
non-fit structure, activation, and negative activation separately. Internal
state could remain `UNVERIFIED` when the host exposed no trace, while rendered
consequences still passed or failed.

Strict acceptance required every prescribed run to pass. Round one failed five
cases, and the only permitted targeted remediation round failed all five
again. Cursor strict acceptance is therefore **unmet**.

The v0.2 schema `4.0.0` suite defines a new future Advisory host run and has no
current result. `pc-core` mechanical tests do not
substitute for that run or satisfy its semantic criteria.

The bounded v0.2 Cursor wrapper rerun also failed `E03`, `E04`, and `E05`.
Its 10 mechanical certifications do not satisfy strict semantic or behavioral
acceptance, which remains unmet.

## Security checks

The Advisory Agent Skill and ChatGPT package remain instruction-only:

- only the canonical `SKILL.md` and Apache-2.0 `LICENSE` are installed;
- neither file is executable or a symlink;
- no script, hook, plugin runtime, service, or background process is installed;
- no tool is granted or pre-approved; and
- no network access, analytics, telemetry, or user-input collection is
  required.

This posture does not certify the host or model as secure. Host permissions,
tools, network access, and data handling remain host-controlled.

The optional local `pc-core` package is executable Python but uses only the
standard library, starts no service, configures no MCP server, collects no
analytics, and changes no user-global settings. The Cursor and Claude hook
files are templates only; the repository does not install them. The
non-streaming wrappers execute the selected host CLI under that host's existing
authentication and permissions.

## OpenAI status

**Current status: v0.2.1 is Advisory and has not been uploaded; an older
publication is user-confirmed historical evidence; user-provided ChatGPT
transcripts are non-conformant; listing, installation, and activation remain
independently UNVERIFIED.**

On 2026-08-17, the user reported publication of an older ChatGPT plugin at
[`plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
An anonymous fetch independently confirmed that the URL returns a ChatGPT
Plugins route, but the response exposed only a login page. It did not expose
listing metadata or install controls.

For that older package, the publication report supersedes the earlier
statement that portal upload and submission were blocked and that no upload
occurred. The URL is retained as historical publication evidence. Neither it
nor the report establishes that the current v0.2.1 ZIP was uploaded. The report
is not a `PASS` under the result labels above. The anonymous route check
independently establishes only that the route exists; it does not establish
authenticated listing visibility, installability, successful installation, or
activation.

### Historical user-provided live transcript

On 2026-08-17, the user also supplied a transcript they identified as a live
interaction with the published plugin. The repository did not independently
capture or reproduce that session. It is user-provided evidence. The
`PASS`/`FAIL` labels below score only the named visible checks in the supplied
transcript; they do not represent an independently run full-suite evaluation:

- **Default Verbose rendering:** `PASS`. All three views appeared in the
  required order.
- **Progressive acknowledgment and stickiness:** `PASS`. The transcript showed
  the acknowledgment and **At a glance → In context → At depth** transitions.
- **Safe stopping and caveats:** `PASS`.
- **At-a-glance budgets:** `FAIL`. Gold used approximately 103 prose words;
  silver used approximately 210 prose words excluding tables and citations.
- **Cumulative prose through In context:** `FAIL`. Gold used approximately
  330+ words; silver used approximately 600+ words.
- **Additivity and no fact-only repetition:** `FAIL`.
- **Switch back to Verbose:** the acknowledgment was observed, but actual
  subsequent Verbose behavior was not included and remains `UNVERIFIED`.

Because core budget and additivity requirements failed, the ChatGPT behavior
status is **observed but non-conformant**. Passing order, transition, and caveat
checks do not establish compatibility or support. No financial fact in the
gold or silver responses was independently verified, and this record makes no
claim about the factual accuracy or suitability of their financial content.

### Latest user-provided pre-v0.2.1 trigger transcript

On 2026-08-18, the user supplied another transcript after reporting a new
plugin upload. The installed portal bytes were not independently identified,
and this transcript preceded the v0.2.1 trigger-recall patch. The initial `gold
prices and forecasts` answer did not render **At a glance**, **In context**, or
**At depth**. After the user challenged the omission, ChatGPT produced the
headings but described removed Progressive/Verbose modes and said it had failed
to activate the skill.

The repository did not independently capture the session, verify the installed
portal bytes, or receive a host activation trace. The visible initial response
therefore `FAILS` the v0.2 three-view output requirement; the exact activation
mechanism and loaded revision remain `UNVERIFIED`. The obsolete-mode explanation
is incompatible with the current skill body and indicates stale or non-loaded
behavior rather than a current v0.2 instruction.

Package v0.2.1 makes one bounded advisory change: it front-loads the skill
description with default, mandatory ordinary-response trigger language and the
three required views before exclusions. A separate local fixture records five
positive and four non-fit trigger prompts. This can improve model recall but
cannot guarantee implicit invocation. The v0.2.1 ZIP has not been uploaded or
live-tested in ChatGPT.

The [OpenAI plugin packaging and publication record](openai-plugin.md) keeps
the full evidence boundary. Local deterministic packaging and user-reported
publication or transcript evidence do not clear the failed Cursor gate or
establish OpenAI compatibility, support, or release readiness.

## Closed-cycle evidence boundary

- Round-one passes belong to the pre-remediation skill and do not constitute a
  full-suite result for that cycle's final skill.
- That cycle's final-skill targeted failures cannot be averaged with round-one
  passes.
- Historical former-protocol results cannot be combined with either active
  round.
- This record closes the bounded cycle; it does not authorize or imply another
  remediation round.
- No support, compatibility, or release claim follows from the structural
  checks or partial behavioral positives. Publication, the anonymous route
  check, and the user-provided transcript retain their separate evidence
  boundaries.
- The revised protocol, skill, evaluation metadata, and local core are new
  inputs. Their mechanical tests neither reopen the prior remediation cycle nor
  inherit a prior host result.

## Licensing authorization

On 2026-08-17, Firas Kafri explicitly confirmed that he controls the source
draft and authorizes CC BY 4.0 for the protocol and documentation text and
Apache-2.0 for the skill and tooling paths. The
[provenance record](../PROVENANCE.md) documents this representation. Neither
the statement nor Git metadata independently proves copyright ownership or
licensing authority. Licensing authority is no longer tracked as a blocker.

## Remaining verification gaps and limitations

- The preceding Cursor strict-acceptance cycle failed and reached its hard
  stop.
- The revised prompt-only skill has no Cursor or Claude Code host acceptance
  result.
- Live Cursor wrapper execution is evidenced only by the bounded E02-E07
  remediation rerun; it failed overall. Live Claude Code wrapper execution
  remains `UNVERIFIED` because it requires paid Anthropic API access.
- Local mechanical passes do not guarantee completeness, accuracy, warning
  necessity, semantic safe stopping, paraphrased repetition, purposeful depth,
  or hidden-reversal safety.
- ChatGPT listing metadata, authenticated visibility, installability,
  and activation remain independently `UNVERIFIED`.
- The historical ChatGPT transcript remains non-conformant, and the latest
  user-provided pre-v0.2.1 transcript missed the initial three-view trigger
  before producing a stale obsolete-mode explanation.
- Package v0.2.1 has not been uploaded, installed, or retested in a fresh
  ChatGPT conversation; improved description recall is not an invocation
  guarantee.
- The upload, submission, review, approval, portal-validation, security-scan,
  and publication sequence is not independently documented.
- Professional name and trademark clearance remains unresolved.
