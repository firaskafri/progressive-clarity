# Claude plugin and custom Skill distribution

## Current v0.4 distribution target

Progressive Clarity v0.4 has two Claude distribution forms. Both are
instruction-only and reuse the canonical
`skills/progressive-clarity/SKILL.md` body and `LICENSE`:

- a repository-root Claude plugin; and
- a minimal Claude.ai custom-Skill upload.

Both carry the Advisory topic-oriented profile. The model uses visible context
to infer topic continuity and return to an earlier topic. Ordinary and narrow
exploration is Focused; the first substantial orientation, decision or summary
checkpoint, material re-synthesis, and material correction use Full output.
Every deeper Full view must be dominated by new information; necessary short
anchors may recur, but complete earlier propositions and recaps may not.
Neither package contains `pc-core`, adapters, hooks, durable topic state, a
backend, an MCP server, executable code, network access, or analytics.

### Target package names

Both v0.4 Claude artifacts target version `0.4.3`:

```text
dist/progressive-clarity-claude-plugin-0.4.3.zip
dist/progressive-clarity-claude-ai-skill-0.4.3.zip
```

The plugin inventory is:

```text
.claude-plugin/plugin.json
skills/progressive-clarity/LICENSE
skills/progressive-clarity/SKILL.md
```

The custom-Skill inventory is:

```text
progressive-clarity/LICENSE
progressive-clarity/SKILL.md
```

The generated custom-Skill frontmatter must retain only the supported `name`,
`description`, and `license` fields, with a description that accurately
describes the v0.4 topic-oriented Focused/Full cadence. The generated body and
license must remain byte-equivalent to their canonical sources except for the
documented generated frontmatter replacement.

### Build and inspect

Run from the repository root with Python 3.11 or newer:

```sh
python3.11 -m tools.package_claude_plugin
python3.11 -m tools.package_claude_skill
python3.11 -m json.tool .claude-plugin/plugin.json >/dev/null
unzip -t dist/progressive-clarity-claude-plugin-0.4.3.zip
unzip -t dist/progressive-clarity-claude-ai-skill-0.4.3.zip
unzip -Z1 dist/progressive-clarity-claude-plugin-0.4.3.zip
unzip -Z1 dist/progressive-clarity-claude-ai-skill-0.4.3.zip
```

Run `claude plugin validate . --strict` only when the installed Claude Code
version supports that option. Preserve an unsupported-option or authentication
error as a tooling result; do not replace it with an inference claim.

Installed Claude Code 2.1.72 reported `✔ Validation passed` for
`claude plugin validate .`. Its help exposes no `--strict` option, so strict
installed-CLI validation remains unavailable with that version.

Two consecutive local builds from unchanged inputs produced matching bytes:

- Claude plugin: 25,789 bytes, SHA-256
  `dd71d71f8277188161429a61f5412d3a0e87b4f6b3a29847bb0bb7ce520bfed9`;
- Claude.ai custom Skill: 24,564 bytes, SHA-256
  `8f8f697778387a4845ee6d66726aa1cc5c90ce4e0dd63573f5a4923f6368b874`.

The generated custom-Skill description is 182 characters. Its packaged body
and canonical body both have SHA-256
`6cb3cd1621951eb13a8e0fcaec4945694c8e59db52507dd938c63767edcd5924`.

The exact Claude plugin inventory is:

- `.claude-plugin/plugin.json`: 584 bytes, SHA-256
  `44f3264f78708d0311495ee65f8f1df2f3fddb48641afb60730cb631fb8e0225`;
- `skills/progressive-clarity/LICENSE`: 11,358 bytes, SHA-256
  `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`;
  and
- `skills/progressive-clarity/SKILL.md`: 13,407 bytes, SHA-256
  `ac64b0d1e055c820275455626ebb054b7b41111aa7a53a2f03364dd33023f04d`.

The exact Claude.ai Skill inventory is:

- `progressive-clarity/LICENSE`: 11,358 bytes, SHA-256
  `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`;
  and
- `progressive-clarity/SKILL.md`: 12,922 bytes, SHA-256
  `8f588b73e5683a83f81f368f774bb90a085e9a070a2f9a89df5bd3c8da1b058e`.

Historical v0.2 hashes below identify only their old artifacts.

### Local use after a successful rebuild

Claude Code can load the source root or rebuilt plugin ZIP:

```sh
claude --plugin-dir /path/to/progressive-clarity
claude --plugin-dir /path/to/progressive-clarity/dist/progressive-clarity-claude-plugin-0.4.3.zip
```

The custom-Skill upload target is:

```text
dist/progressive-clarity-claude-ai-skill-0.4.3.zip
```

An archive that passes local validation is not automatically accepted by
Claude.ai, a custom-plugin uploader, an organization marketplace, or the public
community directory. Upload, review, approval, catalog synchronization, and
installation require separate authorization and evidence.

The project-local Claude Code Stop hook remains
**Advisory/block-and-retry**. It checks visible Full formatting when the
reserved headings are present. Heading-free output is nonblocking because it
may be a valid Focused or purpose-specific response. The hook cannot certify
topic inference, selected presentation, or output already displayed; use the
non-streaming wrapper for fail-closed local output.

### Current evidence boundary

No `0.4.3` live ChatGPT, Cursor, or Claude acceptance run exists. User-provided
v0.3.0–v0.3.2 ChatGPT observations are recorded separately in
[Verification](verification.md); they do not establish Claude behavior. Claude
skill selection, topic inference, topic resumption, presentation choice, and
rendered behavior are **UNVERIFIED**. No `0.4.3` Claude.ai upload,
custom-plugin upload, community-directory submission, approval, publication,
or installability is claimed.

## Historical/superseded v0.3.x evidence

The v0.3.x local packages and user-provided ChatGPT results are historical.
They showed generally successful cadence, budgets, topic return, warning
containment, and narrative/procedure exclusions, but recurring Full
restatement plus bounded proportionality, numeric-label, correction,
clarification, and controlling-label failures. Portal-byte identity and visible
Skill activation were not independently verified. No ChatGPT observation
establishes Claude behavior or transfers to v0.4.

## Historical v0.2 Claude packaging and evidence

Everything below this heading is retained as historical v0.2 documentation and
evidence. References to “current,” old artifact versions, hashes, upload paths,
dated local checks, and user-provided Claude transcripts describe the v0.2
record only. Their labels are preserved and do not establish v0.4 behavior.

Progressive Clarity has two Claude distribution forms. Both are
instruction-only and reuse the canonical
`skills/progressive-clarity/SKILL.md` body and `LICENSE`. Neither package
contains `pc-core`, adapters, hooks, a backend, an MCP server, executable code,
network access, analytics, or local state.

Packaging and local validation establish structure and byte integrity only.
They do not establish that Claude will select the skill, follow every
instruction, or render conforming answers. No live Claude behavior is claimed.

## Distribution forms

### Repository-root Claude plugin

The repository root is the plugin root:

```text
.claude-plugin/plugin.json
skills/progressive-clarity/LICENSE
skills/progressive-clarity/SKILL.md
```

The manifest points directly to `./skills/progressive-clarity/`. There is no
second maintained skill copy. Its metadata uses only fields documented by the
current [Claude plugin manifest
schema](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema).

The schema does not define a plugin logo or icon field, so the existing square
SVG assets are not referenced or copied into the Claude package. Do not add an
undocumented asset key. If an authenticated submission form separately asks
for an image, review that form's current requirements before selecting an
existing asset; that separate form path is not verified by this package.

The deterministic plugin archive contains exactly the three files shown above:

```text
dist/progressive-clarity-claude-plugin-0.2.1.zip
```

Claude Code can load either the repository root or this ZIP with
`--plugin-dir`. The ZIP is also suitable for the paid-plan custom-plugin upload
path, subject to the target account's controls.

### Claude.ai Free custom Skill

The deterministic upload archive is:

```text
dist/progressive-clarity-claude-ai-skill-0.2.2.zip
```

It contains exactly:

```text
progressive-clarity/LICENSE
progressive-clarity/SKILL.md
```

The folder name and generated frontmatter `name` are both
`progressive-clarity`. The packaged copy uses only the cross-product
frontmatter fields `name`, `description`, and `license`. Its generated
description is 187 characters:

> Default formatter. MUST use for every ordinary factual
> answer/explanation/recommendation/comparison/decision/status
> update/forecast/summary. Output At a glance, In context, then At depth.

The canonical frontmatter is not shortened or rewritten. The packager replaces
frontmatter only in the generated ZIP entry, then verifies that the body after
the closing frontmatter marker is byte-identical to the canonical body. The
packaged `LICENSE` is byte-identical to the canonical license.

## Build and offline validation

Run from the repository root with Python 3.11 or newer:

```sh
python -m tools.package_claude_plugin
python -m tools.package_claude_skill
```

Each packager:

- rejects symlinked inputs and unexpected canonical skill files;
- checks the folder/frontmatter name match;
- validates the supported manifest or skill-frontmatter fields;
- writes sorted entries with fixed timestamps, permissions, and compression;
- rereads the ZIP and checks its inventory, CRC integrity, metadata, and bytes;
- verifies canonical body and license equivalence where applicable; and
- prints the archive path, size, SHA-256, and per-entry hashes.

Build each artifact twice without changing source files. The SHA-256 reported
for each pair must match. Additional non-inference checks are:

```sh
python -m json.tool .claude-plugin/plugin.json >/dev/null
claude plugin validate . --strict
unzip -t dist/progressive-clarity-claude-plugin-0.2.1.zip
unzip -t dist/progressive-clarity-claude-ai-skill-0.2.2.zip
unzip -Z1 dist/progressive-clarity-claude-plugin-0.2.1.zip
unzip -Z1 dist/progressive-clarity-claude-ai-skill-0.2.2.zip
```

`claude plugin validate` is a local structural validator and does not require a
model request. `--strict` turns warnings, including unsupported manifest
fields, into failures. If the installed CLI requires authentication before it
will validate, preserve the exact CLI error as an unresolved tooling blocker;
do not replace it with a live inference test.

`dist/` is ignored. Generated ZIPs are release artifacts, not maintained source.

### Superseded v0.2.1 Claude.ai artifact

Before the v0.2.2 custom-Skill rebuild below, the retained local
`dist/progressive-clarity-claude-ai-skill-0.2.1.zip` was 16,712 bytes with
SHA-256
`77e7f9569790d424f229df67205b0b8b700b4a6e311fa22c9309e8f0457e8a62`.
That digest is a historical local-byte identity only; it does not establish an
upload or host result.

### Current local verification record

On 2026-08-18, without authentication or a model request:

- Claude Code `2.1.72` reported `✔ Validation passed` for
  `claude plugin validate .`;
- that installed release rejected `--strict` with
  `error: unknown option '--strict'`, so strict CLI validation remains
  unavailable until the local CLI is updated;
- the manifest passed the current SchemaStore
  `claude-code-plugin-manifest.json` with Python `jsonschema` 4.26.0;
- the generated Free Skill passed `agentskills validate` from `skills-ref`
  0.1.1;
- both archives passed `unzip -t` and exact inventory checks;
- two consecutive builds produced plugin SHA-256
  `4b44393e9e52bbe35874e5f62d8c7bf2fbca852b5a36f7877d4e6b9226f6b46c`
  and custom-Skill SHA-256
  `f4b8a5ca75cff3e8b18814841439d1866f16d34292116022be0481ab29424498`;
- canonical and packaged body SHA-256 values both equal
  `3e2eb0208cb9d01205a67acd5991cd93e449e84c4a744de6fb4e9222c7fca451`;
  and
- canonical and packaged license SHA-256 values both equal
  `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.

The public GitHub remote was anonymously reachable at commit
`aeaed474ca9d3b0198b956a9ec7028f9ca769513`, but the Claude packaging changes
were local and uncommitted. The public directory cannot review these new bytes
until an authorized commit and push occur.

### Latest user-provided Claude Free activation evidence

On 2026-08-18, the user provided a Claude Free transcript for an Orion factual
summary. The repository did not independently capture the conversation, inspect
host activation traces, or verify any Orion facts. The bounded results are:

- **Implicit activation: FAIL.** The initial factual summary did not load
  Progressive Clarity or produce the required three views.
- **Explicit follow-up body conformance: PASS.** After the user challenged the
  omission, the transcript showed Claude reading the skill and producing At a
  glance, In context, and At depth in order.
- **Budgets: PASS.** The follow-up met the visible 40/200 prose budgets.
- **Additivity: PASS.** The follow-up views added information without visible
  fact-only repetition.
- **Factual content: NOT VERIFIED.** These scores cover presentation behavior
  only.

This evidence supports one activation-recall change: front-load the generated
Claude.ai description with the default-formatter and mandatory-trigger language
already present in the canonical description. It does not change the canonical
skill body, protocol, local enforcement, or public plugin, and it does not prove
that Claude Free will invoke the skill automatically on a future prompt.

## Upload the custom Skill on Claude.ai Free

Anthropic currently documents custom Skills for Free, Pro, Max, Team, and
Enterprise accounts. Code execution and file creation must be enabled.

1. Build the custom-Skill ZIP and record its SHA-256.
2. In Claude.ai, open **Settings → Capabilities** and enable **Code execution
   and file creation**.
3. Open **Customize → Skills**.
4. Select **+ → + Create skill → Upload a skill**.
5. Choose
   `dist/progressive-clarity-claude-ai-skill-0.2.2.zip`.
6. Confirm that the displayed name and description match the generated
   metadata, then enable the skill.

Personal custom-Skill uploads are private to the account. Team and Enterprise
sharing has separate owner-controlled settings. A deterministic update should
be rebuilt from the canonical source and uploaded again; editing the uploaded
copy creates an account-side variant that this repository cannot reproduce.

The cited help page does not publish a numeric custom-Skill ZIP-size limit.
This package is intentionally minimal. The required limits validated here are
the 64-character lowercase-hyphenated name, matching root folder, required
`SKILL.md`, and Claude.ai's 200-character description cap.

Plugins are different: Anthropic currently limits Claude plugins in chat,
Desktop, and Cowork to paid Pro, Max, Team, and Enterprise plans. The Free
distribution path is the custom-Skill ZIP above, not the plugin ZIP.

### Optional Profile Preferences reinforcement

For Claude web, manually paste the following into Profile Preferences:

```text
Use Progressive Clarity as my default formatter. MUST use it for every ordinary user-facing factual answer, explanation, recommendation, comparison, decision, status update, forecast, or summary, even when I do not name the skill. Output exactly three additive views in this order: ## At a glance, ## In context, ## At depth. Keep At a glance to at most 40 counted English words and combined prose through In context to at most 200. Allocate each fact once; deeper views only add information. Preserve indispensable caveats, safety, and explicit corrections. Exclude bare values, exact-output replies, pure code/data transformations, complete sequential procedures, verbatim-only reproduction, narrative or voice-dependent writing, and tasks with no user-facing answer.
```

This preference is not included in either ZIP and cannot be configured by the
packager. Each user must add and maintain it manually. Profile Preferences are
the closest available always-on reinforcement for Claude web, but they are not
a formal activation or conformance guarantee and may be overridden by
higher-priority instructions or host behavior.

## Use the plugin with Claude Code or Claude

For local Claude Code development, no marketplace is required:

```sh
claude --plugin-dir /path/to/progressive-clarity
claude --plugin-dir /path/to/progressive-clarity/dist/progressive-clarity-claude-plugin-0.2.1.zip
```

Starting an interactive session can require account access and can use paid
inference after a prompt. It is not part of package validation.

A public GitHub repository containing `plugin.json` is not itself a Claude Code
marketplace. Before directory approval, distribute through `--plugin-dir` or
create a separate `.claude-plugin/marketplace.json` as documented in [Create
and distribute a plugin
marketplace](https://code.claude.com/docs/en/plugin-marketplaces). No
marketplace catalog is added here.

After community-directory publication, users install from the community
marketplace:

```text
/plugin marketplace add anthropics/claude-plugins-community
/plugin marketplace update claude-community
/plugin install progressive-clarity@claude-community
```

Run `/reload-plugins` only if the install result asks for it. Claude Code can
also refresh marketplaces and installed plugins automatically after startup.

On paid Claude plans, a user can add a custom plugin file from the
**Customize → Plugins** area. Team and Enterprise owners can distribute plugins
through organization marketplaces when Cowork and Skills are enabled.

## Public community directory submission

The detailed Claude Code documentation distinguishes two public marketplaces:

- `claude-community` accepts reviewed third-party submissions; and
- `claude-plugins-official` is curated separately by Anthropic.

There is no application process for the curated official marketplace.
Anthropic may choose plugins for it at its discretion. The submission forms
below target the community directory and do not promise an
**Anthropic Verified** badge.

Before submission:

1. Publish the intended plugin root in a public GitHub repository. Closed-source
   repositories are not accepted for the public directory.
2. Keep a root `README.md` with installation, intended use, limitations, and
   troubleshooting guidance.
3. Run `claude plugin validate . --strict` against the exact public checkout.
4. Review the [Anthropic Software Directory
   Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)
   and [Anthropic Software Directory
   Terms](https://support.claude.com/en/articles/13145338-anthropic-software-directory-terms).
5. Prepare at least three working example prompts, verified contact and support
   details, and accurate statements about data access. This plugin has no
   service account or remote endpoint; describe those fields as not applicable
   rather than inventing credentials.
6. Confirm ownership and licensing authority. A manifest author string and Git
   history do not prove those rights.

Official in-app forms:

- **Claude.ai:** <https://claude.ai/admin-settings/directory/submissions/plugins/new>
- **Console:** <https://platform.claude.com/plugins/submit>

The Claude.ai form requires a Team or Enterprise organization plus directory
management access; organization Owners have it by default. The Console form
requires Developer, Admin, or Owner access to a Console organization.
Individual authors who are not in a Claude.ai Team or Enterprise organization
can create a Console organization and use the Console form.

The review pipeline runs structural validation and automated safety screening.
Approval is discretionary. Approved community plugins are pinned to a commit in
the public
[`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community)
catalog. The catalog syncs from the review pipeline nightly, so approval and
installability can be separated by a delay.

Progressive Clarity asks to format a broad class of ordinary responses. The
Directory Policy requires instructional capabilities to be narrow, accurate,
and non-conflicting with other software. Structural validity does not resolve
whether Anthropic will accept that scope; compatibility review remains a
submission blocker that only Anthropic can clear.

Anthropic documents a Partner Skills directory but no open public submission
form for a standalone custom Skill. Free uploads remain private. Team and
Enterprise organizations can enable peer or organization sharing. For broad
public discovery, the documented open route is to bundle the canonical skill
in this plugin and submit the plugin to the community directory.

## Organization distribution limits

These limits apply to Team and Enterprise organization marketplaces, not to the
Free custom-Skill upload:

- manual plugin ZIPs must be valid archives under 50 MB;
- a manual marketplace can contain up to 100 plugins;
- a GitHub-synced marketplace can contain up to 500 plugins;
- plugin names are at most 64 characters and use lowercase hyphenated words;
- organization GitHub-synced marketplace repositories must be private or
  internal, unlike the public repository required for community submission;
- a sync can take up to 30 minutes; and
- an automatic organization sync is triggered by merging a pull request that
  includes a plugin version bump when the owner has enabled automatic syncing.

The same plugin ZIP name replaces an existing manual-marketplace plugin with
that manifest name. A GitHub sync replaces the marketplace contents with the
repository's current state.

## Update flow

The public plugin manifest declares an explicit semantic version, so bump it
only for a public plugin release. The Claude.ai Free artifact has an independent
`PACKAGE_VERSION` in `tools/package_claude_skill.py`; version `0.2.2` advances
only that generated ZIP. Rebuild the intended artifact, rerun validation, and
compare inventories and hashes before distribution.

After community publication, pushes to the public GitHub repository are picked
up by Anthropic's mirroring CI and screened again; the submission form does not
need to be repeated. Users receive the new plugin after the catalog pin and
version advance and their marketplace refreshes. Check the public catalog
before claiming that an update is installable.

The custom-Skill ZIP has no repository-driven update channel. Rebuild it from
the canonical source and have each account upload the replacement. Recheck the
generated description whenever Claude.ai changes its upload requirements.

## Verification boundaries

The following are independently checkable without paid inference:

- manifest JSON and supported fields;
- canonical skill path and folder/name match;
- generated frontmatter fields and 200-character description limit;
- exact ZIP inventory and integrity;
- deterministic archive metadata and SHA-256;
- canonical body and license byte equivalence;
- absence of packaged code, MCP configuration, network setup, and removed
  presentation terminology; and
- public repository reachability and documented submission prerequisites.

The following remain unverified until separately authorized and exercised:

- authenticated Claude.ai upload acceptance;
- custom plugin upload acceptance;
- community-directory review, safety screening, approval, and catalog sync;
- installation from the public catalog;
- automatic skill selection; and
- rendered response conformance or any other live Claude behavior.

Official references:

- [Create Claude
  plugins](https://code.claude.com/docs/en/plugins)
- [Claude plugin technical
  reference](https://code.claude.com/docs/en/plugins-reference)
- [Discover and install
  plugins](https://code.claude.com/docs/en/discover-plugins)
- [Submit a Claude
  plugin](https://claude.com/docs/plugins/submit)
- [Create custom
  Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Use Skills in
  Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Use plugins in
  Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Manage organization
  plugins](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization)
- [Agent Skills
  specification](https://agentskills.io/specification)
