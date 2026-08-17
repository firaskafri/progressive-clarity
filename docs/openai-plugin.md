# OpenAI plugin packaging and publication

Progressive Clarity uses the repository root as its copy-free OpenAI plugin
source. The required manifest is `.codex-plugin/plugin.json`, and its
`skills` field points to the existing root `skills/` directory. The repository
source does not duplicate or modify the canonical
`skills/progressive-clarity/` package.

Packaging alone does not establish ChatGPT Skills access, Codex compatibility,
OpenAI review, approval, publication, or support. The publication evidence
recorded below is separate from the local packaging result.

## Current gate

The local package was rebuilt against final skill SHA-256
`5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`.
Two consecutive builds produced the same archive SHA-256:
`439bf9ce41ca558c622d7d0b31e2a453fcc3a11fe3dbf73e284fd90d46113479`.

That packaging result does not clear the behavior gate. Cursor round one ended
with 6 cases passing and 5 failing; the one permitted targeted remediation
round ended with 0 passing and 5 failing. All response budgets passed, and
there were no safety-warning or procedural-safety failures, but strict
acceptance still requires every prescribed run to pass. The mandatory hard
stop has been reached.

Upload, submission, or publication does not clear that failed behavior gate.
This record does not authorize or imply another remediation round.

## Publication record

On 2026-08-17, the user reported that the ChatGPT plugin was published at
[`https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
The plugin ID is `plugins_6a82efdddbb48191b2785354515e1be2`. This report
supersedes earlier repository statements that upload, submission, or
publication had not occurred or remained blocked.

An anonymous fetch on 2026-08-17 independently reached that ChatGPT Plugins
route, but the response exposed only a login page with login and sign-up
controls. It did not expose the plugin's listing metadata or install controls.
The fetch therefore confirms that the route exists, not that the listing is
visible to an authenticated account or that the plugin can be installed.

No authenticated listing or install flow was independently exercised, and no
ChatGPT activation or rendered response was scored. Publication is
user-confirmed; listing visibility, installability, activation, and behavior
remain independently **UNVERIFIED**. The report also does not independently
document the upload, submission, review, approval, or publication sequence.

The publication report does not change the non-release-ready status, the failed
Cursor strict acceptance result, or the Claude Code hold. Professional name and
trademark clearance remains unresolved; publication is not evidence of
clearance.

## Package contents

Run the deterministic packager from the repository root:

```sh
source /Users/firaskafri/Work/code/lms-api/.venv/bin/activate
python3 tools/package_openai_plugin.py
```

It creates this ignored artifact:

```text
dist/progressive-clarity-openai-plugin-0.1.0.zip
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
SHA-256 digest and byte count for the archive and every entry. For the final
frozen source, the archive is 30,659 bytes and has
SHA-256
`439bf9ce41ca558c622d7d0b31e2a453fcc3a11fe3dbf73e284fd90d46113479`.

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
source /Users/firaskafri/Work/code/lms-api/.venv/bin/activate
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 tools/validate_repository.py
python3 tools/package_openai_plugin.py
unzip -t dist/progressive-clarity-openai-plugin-0.1.0.zip
unzip -Z1 dist/progressive-clarity-openai-plugin-0.1.0.zip
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
separate evidence dimensions, and this package has no passing result for them.

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

- failed Cursor strict acceptance and the completed bounded-cycle hard stop;
- Claude Code behavior, which remains on hold for insufficient API credit and
  **UNVERIFIED**;
- ChatGPT listing metadata, authenticated visibility, installability,
  activation, and rendered behavior, which remain independently
  **UNVERIFIED**;
- independently reviewable records of the upload, submission, review, approval,
  portal validation, security scans, and publication sequence;
- independent confirmation that the selected OpenAI Platform identity matched
  the manifest and that the submitter had **Apps Management: Write**;
- confirmation that no employer, client, collaborator, contract, or AI-tool
  term limits the selected licenses; or
- professional name and trademark clearance for “Progressive Clarity.”

Publication does not establish behavioral compatibility, installation support,
release readiness, or professional name clearance.
