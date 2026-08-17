# Verification record

This record separates the completed bounded dual-mode cycle from earlier host
evidence. The cycle ended in failure at its required hard stop. Progressive
Clarity version 0.1 is therefore a **non-release-ready draft**.

## Result labels

- **PASS** means direct evidence establishes only the named check against the
  named frozen revision.
- **FAIL** means observable output violates a requirement of that frozen
  revision.
- **UNVERIFIED** means available evidence cannot establish the claim. It is
  neither a pass nor a failure.
- **HISTORICAL/SUPERSEDED** means the result belongs to the former protocol and
  must not be used as evidence for the dual-mode contract.

A file copy, structural validation, discovery trace, or explicit load does not
establish rendered behavior. Similar output without a host trace does not
establish activation.

## Current dual-mode target

The normative [`SPEC.md`](../SPEC.md) defines two sticky conversation modes:

- **Verbose mode is the default.** A new conversation starts in Verbose mode.
  An ordinary in-scope request renders **At a glance**, **In context**, and
  **At depth** in one response, in that order. Every deeper section is
  additive.
- **Progressive mode is explicit and sticky.** A new topic starts at
  **At a glance**. An unqualified `More` advances to **In context**, then
  **At depth**, rendering only the newly reached view. A topic change does not
  reset the mode.
- **Mode commands:** `Progressive mode` and `Verbose mode` change sticky mode
  when presented case-insensitively as a command or clear mode directive. If a
  command and substantive request share a message, the mode changes before the
  response is composed.
- **Per-response overrides:** a request for `At a glance`, `In context`, or
  `At depth` changes only that response. It does not change sticky mode. When a
  mode command and view override appear together, the mode changes first, the
  override applies once, and the new mode persists.

Every rendered view must show its view heading. A standalone mode command is
control dialogue and renders no view. In Verbose mode, `More` adds purposeful
At depth information without replaying all three views.

## Frozen dual-mode inputs

The synchronized host-execution baseline is frozen at:

- [`SPEC.md`](../SPEC.md): SHA-256
  `ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d`;
- [`skills/progressive-clarity/SKILL.md`](../skills/progressive-clarity/SKILL.md):
  SHA-256
  `5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`;
- [`evals/cases.json`](../evals/cases.json): SHA-256
  `4c27a740e2e02e54f97889618397a6417c82e089b9bb44919b92642e59289680`.

The repository validator and CI pin these bytes and validate the schema 2.0
fact references and declared run totals. Any change to a frozen input creates
a new revision and requires synchronized hashes before host execution. Do not
reuse a prior prompt, score, trace, or result merely because its case name still
exists.

## Host discovery paths

These are documented host paths, not current dual-mode verification results:

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

**Current status: strict acceptance unmet; hard stop reached.**

The active cycle used Cursor desktop `3.15.19`, Cursor Agent CLI
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
performed, is permitted within this cycle, or is implied by this record. The
final skill received only the prescribed targeted rerun, not a new full-suite
round, so this evidence cannot establish Cursor compatibility or support.

All former-protocol Cursor evidence remains **historical and superseded**. It
must not be aggregated with this cycle.

## Claude Code status

**Current status: behavior on hold and UNVERIFIED because of insufficient API
credit.**

Claude Code 2.1.72 previously:

- scanned `.claude/skills/progressive-clarity/` as a project skill;
- listed `progressive-clarity` as a skill and slash command; and
- parsed `/progressive-clarity` and attached the former skill text.

That observation used the former protocol and does not verify the dual-mode
package or the final frozen skill. The first API request stopped before
inference with `Credit balance is too low`. Input and output tokens were zero,
cost was `$0`, and no assistant response was scored. No Claude Code behavior
result is represented by this finalization.

## Strict acceptance rule and outcome

The active checks remain defined by the frozen suite and its
[`evals/README.md`](../evals/README.md): visible mode behavior, cumulative
facts, required caveats, additive views, budgets, corrections, controlling
text, non-fit structure, activation, and negative activation are scored
separately. Internal state may remain `UNVERIFIED` when the host exposes no
state trace, but observable consequences still pass or fail.

Strict acceptance required every prescribed run to pass. Round one failed five
cases, and the only permitted targeted remediation round failed all five
again. Cursor strict acceptance is therefore **unmet**.

## Security checks

The dual-mode package must remain instruction-only:

- only the canonical `SKILL.md` and Apache-2.0 `LICENSE` are installed;
- neither file is executable or a symlink;
- no script, hook, plugin runtime, service, or background process is installed;
- no tool is granted or pre-approved; and
- no network access, analytics, telemetry, or user-input collection is
  required.

This posture does not certify the host or model as secure. Host permissions,
tools, network access, and data handling remain host-controlled.

## OpenAI status

**Current status: publication is user-confirmed; listing, installation,
activation, and behavior remain independently UNVERIFIED.**

On 2026-08-17, the user reported publication of the ChatGPT plugin at
[`plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
An anonymous fetch independently confirmed that the URL returns a ChatGPT
Plugins route, but the response exposed only a login page. It did not expose
listing metadata or install controls.

The publication report supersedes the earlier statement that portal upload and
submission were blocked and that no upload occurred. It is a user report, not a
`PASS` under the result labels above. The anonymous route check independently
establishes only that the route exists; it does not establish authenticated
listing visibility, installability, successful installation, activation, or
rendered behavior. No authenticated install flow or ChatGPT evaluation run was
performed for this record.

The [OpenAI plugin packaging and publication record](openai-plugin.md) keeps
the full evidence boundary. Local deterministic packaging and user-reported
publication do not clear the failed Cursor gate or establish OpenAI
compatibility, support, or release readiness.

## Closed-cycle evidence boundary

- Round-one passes belong to the pre-remediation skill and do not constitute a
  full-suite result for the final skill.
- The final skill's targeted failures cannot be averaged with round-one
  passes.
- Historical former-protocol results cannot be combined with either active
  round.
- This record closes the bounded cycle; it does not authorize or imply another
  remediation round.
- No support, compatibility, or release claim follows from the structural
  checks or partial behavioral positives. Publication is recorded separately
  from the user report and anonymous route check described above.

## Licensing authorization

On 2026-08-17, Firas Kafri explicitly confirmed that he controls the source
draft and authorizes CC BY 4.0 for the protocol and documentation text and
Apache-2.0 for the skill and tooling paths. The
[provenance record](../PROVENANCE.md) documents this representation. Neither
the statement nor Git metadata independently proves copyright ownership or
licensing authority. Licensing authority is no longer tracked as a blocker.

## Remaining verification gaps and limitations

- Cursor strict acceptance failed, and the bounded remediation policy reached
  its hard stop.
- The final skill has no passing full-suite Cursor result.
- Claude Code behavior is on hold for insufficient API credit and remains
  `UNVERIFIED`.
- ChatGPT listing metadata, authenticated visibility, installability,
  activation, and rendered behavior remain independently `UNVERIFIED`.
- The upload, submission, review, approval, portal-validation, security-scan,
  and publication sequence is not independently documented.
- Professional name and trademark clearance remains unresolved.
