# OpenAI plugin packaging

Progressive Clarity uses the repository root as its copy-free OpenAI plugin
source. The required manifest is `.codex-plugin/plugin.json`, and its
`skills` field points to the existing root `skills/` directory. The repository
source does not duplicate or modify the canonical
`skills/progressive-clarity/` package.

This is packaging work only. It does not establish ChatGPT Skills access,
Codex compatibility, OpenAI review, approval, publication, or support.

## Current gate

The local package was rebuilt against final skill SHA-256
`5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`.
Two consecutive builds produced the same archive SHA-256:
`76312e768fa23590eb920b13b9a49278e8fc4e6b1218e84ad46436d9532374c5`.

That packaging result does not clear the behavior gate. Cursor round one ended
with 6 cases passing and 5 failing; the one permitted targeted remediation
round ended with 0 passing and 5 failing. All response budgets passed, and
there were no safety-warning or procedural-safety failures, but strict
acceptance still requires every prescribed run to pass. The mandatory hard
stop has been reached.

**OpenAI portal upload and submission are blocked because Cursor strict
acceptance failed.** No portal upload, submission, publication, or release was
performed. This record does not authorize or imply another remediation round.

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
skills/progressive-clarity/LICENSE
skills/progressive-clarity/SKILL.md
```

The packager fixes ZIP timestamps, permissions, ordering, and compression
settings. It rejects unexpected files in the canonical skill directory,
validates the documented minimal manifest fields, rereads the completed ZIP,
and fails if any packaged file differs byte-for-byte from its repository source.
Its output reports the SHA-256 digest and byte count for the archive and every
entry. For the final frozen source, the archive is 28,725 bytes and has
SHA-256
`76312e768fa23590eb920b13b9a49278e8fc4e6b1218e84ad46436d9532374c5`.

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
invariants, but the OpenAI submission portal remains authoritative for current
upload and final-directory validation. Portal validation was not attempted
because the strict-acceptance blocker applies before upload.

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
   Confirm that **Create plugin** is available, but do not create a draft until
   the publication blockers below are resolved.

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

The repository manifest intentionally contains only the official minimal fields:
plugin name, semantic version, description, and the root skills path. It does
not claim a verified publisher identity or finished public listing. If the
portal requires public interface metadata or image assets in the uploaded
archive, add them only after the publisher identity, branding, and artifact
scope are explicitly approved.

## Security and identity boundaries

The packaged skill is instruction-only. The ZIP contains no scripts, MCP
server configuration, app mapping, hooks, network dependency, executable bit,
analytics, telemetry, or `agents/openai.yaml`.

OpenAI scans uploaded skills, but that scan does not replace source review.
Treat every submitted instruction and file as security-sensitive. Review the
final ZIP inventory before upload and rerun the byte-equivalence checks after
every source change.

The repository records Firas Kafri as the source author and includes an author
statement, but Git history is not proof of copyright ownership or licensing
authority. The verified OpenAI publisher identity must match the person or
business actually authorized to publish. Do not add publisher claims merely
to satisfy a form.

## Explicit blockers

Do not submit or publish while any of these remain unresolved:

- failed Cursor strict acceptance and the completed bounded-cycle hard stop;
- confirmation that no employer, client, collaborator, contract, or AI-tool
  term limits the selected licenses;
- professional trademark clearance for “Progressive Clarity”;
- verified ChatGPT Skills availability and upload permission on the target
  account or workspace;
- verified OpenAI Platform publisher identity and **Apps Management: Write**;
- completed ChatGPT and Codex activation and behavioral testing against the
  frozen suite;
- approved public listing copy, publisher name, logo, category, starter
  prompts, availability, and policy attestations;
- selected five positive and three negative submission cases with
  reviewer-reproducible expected behavior;
- successful OpenAI portal validation and security scans; and
- explicit user approval to submit and, after any approval, separate explicit
  user approval to publish.
