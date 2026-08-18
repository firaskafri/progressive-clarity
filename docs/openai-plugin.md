# OpenAI plugin packaging and publication

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

The v0.2.1 ZIP remains Advisory and has not been uploaded. That packaging
result does not clear a behavior gate. The latest ChatGPT evidence is
user-provided and not an independently reproduced acceptance run.

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
historical publication evidence and does not establish that v0.2.1 was
uploaded. The report also does not independently document the upload,
submission, review, approval, or publication sequence.

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

### Latest user-provided pre-v0.2.1 trigger transcript

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
are unchanged. The current v0.2.1 ZIP has not been uploaded or live-tested in
ChatGPT.

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

Do not treat a valid ZIP, a successful local install, or a portal upload as
behavioral compatibility evidence. Activation and rendered behavior are
separate evidence dimensions. The historical older-build user-provided
transcript records non-conformant rendered behavior. It is not current v0.2
evidence, and activation remains independently unverified.

## Manual v0.2.1 portal update

These steps are prepared for the authorized publisher. They were not performed
by this repository work and must not be treated as a portal-state record.

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

After an approved replacement is published, uninstall or remove the old
installed plugin version, install v0.2.1, and start a fresh chat before running
`gold prices and forecasts` without naming the skill. An existing conversation
may retain stale instructions or state and is not a valid clean trigger check.

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

The reported publication does not resolve:

- the Advisory v0.2.1 ZIP, which has not been uploaded, or the revised
  prompt-only skill's unrun ChatGPT, Cursor, and Claude behavior;
- failed preceding Cursor strict acceptance and that cycle's hard stop;
- Claude Code behavior, which requires paid Anthropic API access and remains
  **UNVERIFIED** despite structural adapter tests;
- ChatGPT listing metadata, authenticated visibility, installability,
  and activation, which remain independently **UNVERIFIED**;
- the latest user-provided pre-v0.2.1 transcript's missed initial three-view
  output and obsolete-mode explanation, which v0.2.1 has not retested;
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
