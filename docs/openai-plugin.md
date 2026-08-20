# OpenAI plugin packaging and publication

## Current v0.4 package target

The repository root remains the copy-free OpenAI plugin source.
`.codex-plugin/plugin.json` points to the root `skills/` directory, which
contains the canonical `skills/progressive-clarity/` package; packaging does
not maintain a second skill body.

Package version `0.4.2` carries the Advisory topic-oriented profile:

- the model infers topic continuity from visible conversation;
- simple facts and ordinary or narrow exploration use Focused output;
- Full output is automatic for the first substantial topic overview,
  decision or summary checkpoints, material re-synthesis, and material
  correction; every deeper view must be dominated by new information while
  permitting necessary short anchors; and
- purpose-specific shapes and explicit presentation requests take precedence.

The ZIP is instruction-only. It does not contain `pc-core`, a backend, MCP
server, hook configuration, durable topic state, executable code, or a runtime
dependency. It does not inherit local-wrapper mechanical certification.

### Target artifact and inventory

The target archive name is:

```text
dist/progressive-clarity-openai-plugin-0.4.2.zip
```

Its intended inventory remains:

```text
.codex-plugin/plugin.json
assets/progressive-clarity-composer.svg
assets/progressive-clarity-logo.svg
skills/progressive-clarity/LICENSE
skills/progressive-clarity/SKILL.md
```

Build it from the repository root:

```sh
python3.11 -m tools.package_openai_plugin
python3.11 -m json.tool .codex-plugin/plugin.json >/dev/null
python3.11 -m tools.validate_repository
unzip -t dist/progressive-clarity-openai-plugin-0.4.2.zip
unzip -Z1 dist/progressive-clarity-openai-plugin-0.4.2.zip
```

Two consecutive local builds from unchanged inputs produced the same
25,277-byte archive with SHA-256
`ba7e6c2e97ab3dc01ac81c9d2695ad5e504574de2b8bf50bbf7dc2c69d1251df`.
The canonical packaged skill SHA-256 is
`2379f0cf3e8b9ccbfd0a7553b0843097f3fddc764cbc758160b80127377b6c21`.
The exact current inventory is:

- `.codex-plugin/plugin.json`: 857 bytes, SHA-256
  `89ad8c61af198736be5d33ff82fcb012399631ee9fb1ae8d6e8cd3ab9dc87366`;
- `assets/progressive-clarity-composer.svg`: 513 bytes, SHA-256
  `bf37be72d058568f451efb22cace2703c684a2aaa6b8a1ae21309a4a9911add9`;
- `assets/progressive-clarity-logo.svg`: 529 bytes, SHA-256
  `e0b487bcf7852dc2fb4074f90f86e1fb468b04a02bb54f7f6e963bd258275a92`;
- `skills/progressive-clarity/LICENSE`: 11,358 bytes, SHA-256
  `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`;
  and
- `skills/progressive-clarity/SKILL.md`: 11,282 bytes, SHA-256
  `2379f0cf3e8b9ccbfd0a7553b0843097f3fddc764cbc758160b80127377b6c21`.

These checks establish local byte determinism and inventory integrity only.

### Current v0.4 publication and behavior status

No `0.4.2` upload, publication, or live ChatGPT run was performed. Activation,
topic inference, topic resumption, Focused/Full selection, and rendered
conformance remain **UNVERIFIED**. Local archive validation establishes source
and byte integrity only.

### Historical/superseded v0.3.x ChatGPT evidence

On 2026-08-19, the user reported publishing and installing package `0.3.0` in
ChatGPT. The repository did not independently observe the portal workflow or
match installed bytes to the local archive.

The user supplied two Redis lifecycle transcripts. The first missed the
automatic Full transition. The second selected the correct Focused → Full →
Focused → Full cadence and passed both shallow budgets, but failed strict
Focused proportionality and Full cross-view additivity. Those observations
belong to package `0.3.0`; they motivated the bounded `0.3.1` guidance patch.

The user then supplied the complete `0.3.1` ChatGPT initial round. T08
narrative and T09 procedure passed; T01–T07 and T10 failed. Full budgets and
most cadence checks passed, but cross-view repetition was systemic. Additional
failures covered Focused proportionality, unsupported numeric defaults,
correction wording, clarification selection, warning completeness, and the
literal non-controlling label. Those results motivated the targeted `0.3.2`
remediation and do not establish activation without a host indicator.

The user later supplied observations identified as v0.3.2. Cadence, explicit
overrides, Full budgets, topic return, safety containment, and non-fit
narrative/procedure behavior generally worked. Complete conclusions and warning
or recovery sequences still repeated in deeper views; simple facts, numeric
labels, correction openings, clarification, and the literal controlling-text
summary label retained failures. T02's latest run, T08, and T09 were bounded
passes; T10 topic return passed but its initial Full conclusion repeated. T03
used an under-specified oracle, and T06 isolation was suspect because facts
appeared before the user supplied them.

All v0.3.x evidence is user-provided. Portal-byte identity and visible Skill
activation were not independently verified, and no v0.3.x result transfers to
v0.4.

## Historical v0.2 packaging, publication, and evidence

Everything below this heading is retained as historical v0.2 documentation and
evidence. References to “current,” old package versions, hashes, artifact
sizes, portal steps, release notes, and user-provided transcripts describe the
v0.2 record only. Their original result labels are preserved and do not transfer
to v0.4.

Progressive Clarity uses the repository root as its copy-free OpenAI plugin
source. The required manifest is `.codex-plugin/plugin.json`, and its
`skills` field points to the existing root `skills/` directory. The repository
source does not duplicate or modify the canonical
`skills/progressive-clarity/` package.

Packaging alone does not establish ChatGPT Skills access, Codex compatibility,
OpenAI review, approval, publication, or support. The publication evidence
recorded below is separate from the local packaging result.

ChatGPT remains the Option 1 **Advisory prompt-only** surface. The archive does
not contain `pc-core`, a backend, an MCP server, hook configuration, local
state, or any runtime dependency. Deterministic local enforcement is available
only outside this ZIP for explicitly invoked local-agent wrappers. Its only
ordinary response contract is one response containing At a glance, In context,
and At depth in order.

## Current gate

The v0.2.1 package was rebuilt against prompt-only skill SHA-256
`ab8d3ba8e9aa02530f97d21af15ff371ec0df02055b6e2f0cff665c36c59a749`.
Two consecutive builds produced the same archive SHA-256:
`d5e447abc41132a3e5d0580b5afc5231230317dead1adcee5767085159cbde23`.

The v0.2.1 ZIP remains Advisory. On 2026-08-18, the user reported uploading and
installing it in ChatGPT. The repository did not independently capture those
actions or identify the portal artifact by digest. The packaging result does
not clear a behavior gate. The current ChatGPT evidence is user-provided and is
not an independently reproduced full acceptance run.

The bounded Cursor wrapper remediation rerun completed against the frozen
pre-trigger-revision skill: 10 of 17 responses were mechanically certified and
7 were withheld; `E02`, `E06`, and `E07` passed, while `E03`, `E04`, and `E05`
failed. It exercised mechanical wrapper fixes but is not a result for this
v0.2.1 ZIP. Strict semantic and behavioral acceptance remains unmet. Upload,
submission, or publication would not clear that failed behavior gate.

## Historical publication record

On 2026-08-17, the user reported that an older ChatGPT plugin was published at
[`https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
The plugin ID is `plugins_6a82efdddbb48191b2785354515e1be2`. This report
supersedes earlier repository statements that upload, submission, or
publication had not occurred or remained blocked.

An anonymous fetch on 2026-08-17 independently reached that ChatGPT Plugins
route, but the response exposed only a login page with login and sign-up
controls. It did not expose the plugin's listing metadata or install controls.
The fetch therefore confirms that the route exists, not that the listing is
visible to an authenticated account or that the plugin can be installed.

No authenticated listing or install flow was independently exercised. The
older publication is user-confirmed; listing visibility, installability, and
activation remain independently **UNVERIFIED**. The URL is retained as
historical publication evidence and does not establish the separate
user-reported v0.2.1 upload or installation. The older report also does not
independently document the upload, submission, review, approval, or publication
sequence.

### Historical user-provided live behavior transcript

On 2026-08-17, the user supplied a transcript they identified as a live
interaction with the published older dual-behavior plugin. It is user-provided
historical evidence and was not independently captured or reproduced. Its
visible protocol results are:

- **Default Verbose rendering:** `PASS`; all three views appeared in order.
- **Progressive acknowledgment and sticky transitions:** `PASS`; the transcript
  showed **At a glance → In context → At depth**.
- **Safe stopping and caveats:** `PASS`.
- **At-a-glance budgets:** `FAIL`; gold ≈103 prose words and silver ≈210 prose
  words excluding tables and citations.
- **Cumulative prose through In context:** `FAIL`; gold ≈330+ words and silver
  ≈600+ words.
- **Additivity and no fact-only repetition:** `FAIL`.
- **Switch back to Verbose:** acknowledgment observed; actual subsequent
  Verbose behavior `UNVERIFIED`.

The transcript changes ChatGPT behavior status from unverified to **observed
but non-conformant**. It does not independently establish activation,
compatibility, or support. No financial fact in the gold or silver responses
was independently verified; the behavioral scores do not establish factual
accuracy or suitability.

This evidence applies to the user-identified older published plugin session,
not to v0.2, the later trigger transcript, or the v0.2.1 ZIP.

### Earlier user-provided pre-v0.2.1 trigger transcript

On 2026-08-18, the user supplied a second transcript after reporting a new
plugin upload. The repository did not independently verify which portal bytes
were installed or capture the conversation, and the transcript preceded the
v0.2.1 trigger-recall patch. In the supplied transcript:

- the first `gold prices and forecasts` response omitted all three required
  headings, so visible v0.2 output conformance `FAILED`;
- after the user challenged the omission, ChatGPT rendered the three headings
  but described removed Progressive/Verbose presentation modes; and
- the response itself said it had failed to activate the skill, but no
  independent host activation trace exists.

This is evidence of missed implicit trigger recall plus stale or non-loaded
behavior, not evidence that the v0.2 body requested those modes. The bounded
v0.2.1 change front-loads the discovery description and adds local
activation-only regression prompts. It can improve recall but cannot guarantee
implicit ChatGPT invocation. The output body and local enforcement semantics
are unchanged.

### User-reported v0.2.1 upload and installation

On 2026-08-18, the user reported uploading package v0.2.1 and installing it in
ChatGPT. This is a user-provided portal-state report. The repository did not
independently observe the upload or install, inspect an authenticated listing,
match the installed portal bytes to the local ZIP, or obtain upload,
submission, review, approval, portal-validation, security-scan, or publication
records.

### User-provided v0.2.1 complex gold-forecast transcript

On 2026-08-18, after the reported upload and installation, the user supplied a
complex gold-forecast transcript identified as v0.2.1 behavior. The required
three-view structure triggered, but the 40-word At-a-glance budget, 200-word
cumulative shallow budget, and additivity requirement failed. The transcript
is therefore **observed but non-conformant**.

The repository did not independently capture or reproduce the session. No
financial fact in the response was independently verified, and the behavioral
result does not establish financial accuracy or suitability.

### User-provided v0.2.1 fixed-facts smoke

Later on 2026-08-18, the user supplied a fresh fixed-facts smoke identified as
v0.2.1 behavior. Its named visible checks all passed:

- automatic trigger;
- exactly **At a glance**, **In context**, and **At depth**, once and in order;
- 26 words in **At a glance**;
- approximately 50 cumulative shallow words through **In context**;
- coverage of the supplied fixed facts;
- additivity; and
- the negative exact-output control, whose response was exactly `323`.

This is a bounded pass for those checks only. The repository did not
independently capture or reproduce the session or receive a host activation
trace. Fixed-fact coverage does not establish completeness beyond the supplied
facts, and the negative control does not establish all non-fit behavior. The
smoke neither identifies the installed portal bytes nor cancels the separate
complex transcript's failures. It does not establish universal v0.2.1
conformance.

Together, the two current transcripts show that implicit activation and
rendered conformance remain probabilistic: one fresh bounded smoke passed while
one complex response failed core budgets and additivity.

The historical publication report, transcript evidence, and bounded Cursor
wrapper rerun do not change the non-release-ready status or failed strict
acceptance result. The Claude Code adapter is structurally tested, but live
behavior remains `UNVERIFIED` because it requires paid Anthropic API access.
Professional name and trademark clearance remains unresolved; publication is
not evidence of clearance.

## Package contents

Run the deterministic packager from the repository root:

```sh
python3.11 -m tools.package_openai_plugin
```

It creates this ignored artifact:

```text
dist/progressive-clarity-openai-plugin-0.2.1.zip
```

The ZIP contains exactly:

```text
.codex-plugin/plugin.json
assets/progressive-clarity-composer.svg
assets/progressive-clarity-logo.svg
skills/progressive-clarity/LICENSE
skills/progressive-clarity/SKILL.md
```

The packager fixes ZIP timestamps, permissions, ordering, and compression
settings. It rejects unexpected files in the canonical skill directory,
validates the documented manifest, publisher-name, asset-path, SVG, and square
image constraints, rereads the completed ZIP, and fails if any packaged file
differs byte-for-byte from its repository source. Its output reports the
SHA-256 digest and byte count for the archive and every entry. For the revised
prompt-only source, the archive is 19,413 bytes and has
SHA-256
`d5e447abc41132a3e5d0580b5afc5231230317dead1adcee5767085159cbde23`.

The two original visual assets use a restrained three-level nested-view motif
with flat midnight and mint colors. They contain no text, gradients, external
references, scripts, or third-party marks:

- `progressive-clarity-composer.svg`: 64×64, SHA-256
  `bf37be72d058568f451efb22cace2703c684a2aaa6b8a1ae21309a4a9911add9`;
- `progressive-clarity-logo.svg`: 256×256, SHA-256
  `e0b487bcf7852dc2fb4074f90f86e1fb468b04a02bb54f7f6e963bd258275a92`.

`dist/` was already ignored before this packaging work. Do not commit the ZIP.

## Local validation and inspection

Run:

```sh
python3.11 -m json.tool .codex-plugin/plugin.json >/dev/null
python3.11 -m tools.validate_repository
python3.11 -m tools.package_openai_plugin
unzip -t dist/progressive-clarity-openai-plugin-0.2.1.zip
unzip -Z1 dist/progressive-clarity-openai-plugin-0.2.1.zip
```

Run the packager twice without changing source inputs and compare the reported
archive SHA-256 values. They must match.

OpenAI documents the minimal manifest shape and package path rules in
[Package your plugin](https://developers.openai.com/plugins/build/plugins).
The public submission checks are documented separately in the
[submission error reference](https://developers.openai.com/plugins/deploy/submission-errors).
No supported offline OpenAI plugin-schema validator was available locally
during this implementation. The packager checks the documented source
invariants, including the 48–4,096-pixel square SVG range and 5 MiB asset limit,
but the OpenAI submission portal remains authoritative for current upload and
final-directory validation. This repository does not contain independently
reviewable portal-validation or security-scan output for the reported
publication.

Do not treat a valid ZIP, a local install, or the user-reported portal upload
and installation as behavioral compatibility evidence. Activation and rendered
behavior are separate evidence dimensions. The historical older-build
transcript remains non-conformant. For current v0.2.1, the user-provided
fixed-facts smoke passed its visible automatic-trigger check while the complex
gold-forecast transcript failed core conformance checks; the host activation
mechanism and installed bytes remain independently unverified.

## Portal update checklist and evidence boundary

The user reported completing a v0.2.1 upload and installation on 2026-08-18,
but the repository did not observe the portal workflow and does not claim that
the steps below were followed. Keep this checklist for a future replacement or
re-upload. It is operational guidance, not a reconstruction of the reported
portal actions.

1. Rebuild the archive from the intended final checkout and confirm its
   SHA-256 and five-entry inventory against this document.
2. Sign in to the [OpenAI Platform](https://platform.openai.com/), select the
   organization that owns `plugins_6a82efdddbb48191b2785354515e1be2`, and
   confirm **Apps Management: Write**.
3. Confirm that the selected verified developer identity is exactly
   `FIRAS HASHEM AHMAD AL KAFRI`.
4. Open the existing plugin and create a new draft version. Do not create a
   separate plugin: updates must retain package name `progressive-clarity`.
5. Keep the submission type **Skills only** and upload
   `dist/progressive-clarity-openai-plugin-0.2.1.zip`.
6. Confirm the parsed manifest reports version `0.2.1`, the same package name,
   the identity above, and the two packaged SVG paths. Review and explicitly
   accept any portal-reported manifest normalization only if it preserves the
   intended fields.
7. Set or confirm the listing copy from the uploaded manifest:
   - display name: `Progressive Clarity`;
   - short description: `Three views, one response`;
   - long description: `Prompt-only guidance that asks models to render At a
     glance, In context, and At depth in order, preserve stopping-point caveats,
     and avoid fact repetition while leaving semantic conformance advisory.`
8. Remove any starter prompt or test case that asks for a mode switch, sticky
   mode, staged view advancement, or Progressive behavior. Supply five positive
   and three negative reviewer-reproducible cases for the single v0.2 contract.
9. Review category, website, support, privacy, terms, availability, and policy
   attestations against the actual publisher and prompt-only data handling. Do
   not inherit an older value without checking it.
10. Use the release notes below, run the portal package and security checks,
    and inspect every warning. Save the draft without submission until the
    current live-host evidence and listing materials are approved.
11. After separate authorization, select **Submit for Review**. Submission
    starts review; it does not publish. If OpenAI approves the new version,
    obtain separate authorization before publishing the replacement.

Exact release notes:

> Updates the Progressive Clarity v0.2 advisory plugin from package version
> 0.2.0 to 0.2.1. Front-loads the skill description as the default formatter
> for ordinary user-facing factual answers, including forecasts, and states the
> required three-view output before precise exclusions. The response contract,
> skill body, and skills-only runtime boundary are unchanged. This improves
> implicit trigger recall but does not guarantee ChatGPT or Codex invocation.

For any future v0.2.1 replacement, uninstall or remove the previously installed
copy, install the replacement, and start a fresh chat before running `gold
prices and forecasts` without naming the skill. An existing conversation may
retain stale instructions or state and is not a valid clean trigger check.

## Check ChatGPT Skills access

Do not assume that the account or workspace has Skills enabled.

1. Sign in to the intended ChatGPT account and select the intended workspace.
2. Look for **Skills** in the ChatGPT sidebar or profile menu.
3. If **Skills** is present, open it and check whether **Create** and
   **Upload from your computer** are available.
4. For a managed workspace, ask an administrator to check the workspace's
   Skills permissions, including whether the intended role may create, upload,
   install, share, or publish skills.
5. If the controls are absent, stop. Record the account plan, workspace, and
   missing control without uploading the ZIP or inferring eligibility.

OpenAI states that Personal Skills are generally available to ChatGPT
Business, Enterprise, Healthcare, and Edu users, are subject to workspace
controls, and may need separate installation across surfaces. Availability
must still be checked on the target account. See
[Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

## Check OpenAI Platform submission access

ChatGPT Skills access and public plugin submission access are separate.

1. Sign in to the [OpenAI Platform](https://platform.openai.com/).
2. Select the organization intended to own the plugin.
3. Open **Settings → Organization → People → Roles**.
4. Open the submitter's role and verify that **Apps Management** is set to
   **Write**. Organization owners already have this permission.
5. Open **Settings → Organization → General** and verify the individual or
   business identity that would appear as the publisher.
6. Open the [plugin submission portal](https://platform.openai.com/plugins).
   Record whether **Create plugin** is available without treating that control
   as evidence for the reported publication's submission history.

Do not copy account identifiers, access tokens, API keys, or authentication
files into this repository or into verification records.

## Submission prerequisites

For the public ChatGPT/Codex path, OpenAI currently requires:

- a **Skills only** submission containing a supported plugin manifest and at
  least one real `skills/<skill-name>/SKILL.md`;
- a verified individual or business publisher identity;
- **Apps Management: Write** for the submitter;
- final listing metadata, category, logo, and realistic starter prompts;
- five positive and three negative reviewer-reproducible test cases;
- release notes, geographic availability, and policy attestations;
- successful package, policy, safety, and security scans; and
- local testing with the same final file tree submitted for review.

Submission starts review; it does not publish the plugin. After approval, the
publisher separately chooses whether to publish it. See
[Submit plugins](https://developers.openai.com/plugins/deploy/submission) and
[Connect and test your plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt).

The repository manifest now contains the package identity and root skills path,
plus the required public interface fields: display name, short and long
descriptions, developer name, composer icon, and logo. Both `author.name` and
`interface.developerName` are exactly
`FIRAS HASHEM AHMAD AL KAFRI`, the user-provided verified identity. The
submission portal must still confirm that the selected verified Platform
identity matches those fields. OpenAI may normalize a mismatch to the selected
verified identity only after portal confirmation.

## Security and identity boundaries

The packaged skill is instruction-only. Apart from the manifest and two static
SVG branding assets, the ZIP contains no scripts, MCP server configuration, app
mapping, hooks, network dependency, executable bit, analytics, telemetry, or
`agents/openai.yaml`.

The local `pc_core/`, `adapters/`, and `tests/` trees are deliberately outside
the archive inventory. ChatGPT does not require or call them.

OpenAI scans uploaded skills, but that scan does not replace source review.
Treat every submitted instruction and file as security-sensitive. Review the
final ZIP inventory before any future upload and rerun the byte-equivalence
checks after every source change.

The manifest records the user-provided verified identity exactly as
`FIRAS HASHEM AHMAD AL KAFRI`. Git history and a manifest string are not proof
of copyright ownership or licensing authority. The selected OpenAI Platform
identity must be the person or business actually authorized to publish.

## Remaining verification and release limitations

The reported actions and transcript evidence do not resolve:

- the revised prompt-only skill's unrun Cursor and Claude behavior or the
  absence of an independently executed full ChatGPT acceptance run;
- failed preceding Cursor strict acceptance and that cycle's hard stop;
- Claude Code behavior, which requires paid Anthropic API access and remains
  **UNVERIFIED** despite structural adapter tests;
- authenticated ChatGPT listing metadata, the installed portal bytes, and
  independent records of the user-reported v0.2.1 upload and installation;
- the current complex gold-forecast transcript's failed 40/200 budgets and
  additivity;
- universal conformance beyond the fresh fixed-facts smoke's named
  automatic-trigger, exact-heading/order, budget, supplied-fact-coverage,
  additivity, and exact `323` passes;
- the host activation mechanism, which remains independently **UNVERIFIED**
  even though the fixed-facts smoke visibly triggered automatically;
- the earlier user-provided pre-v0.2.1 transcript's missed initial three-view
  output and obsolete-mode explanation;
- historical older-build ChatGPT rendered behavior, which is observed but
  non-conformant in the user-provided transcript, with actual post-switch-back
  Verbose behavior still **UNVERIFIED** and no evidentiary effect on v0.2;
- independently reviewable records of the upload, submission, review, approval,
  portal validation, security scans, and publication sequence;
- independent confirmation that the selected OpenAI Platform identity matched
  the manifest and that the submitter had **Apps Management: Write**;
- confirmation that no employer, client, collaborator, contract, or AI-tool
  term limits the selected licenses; or
- professional name and trademark clearance for “Progressive Clarity.”

Publication does not establish behavioral compatibility, installation support,
release readiness, or professional name clearance.

The deterministic package build establishes only local byte integrity. It does
not establish semantic completeness, hidden-reversal safety, or behavior of
the published portal artifact.
