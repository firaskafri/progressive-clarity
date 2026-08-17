# Install the Progressive Clarity skill

Progressive Clarity version 0.1 is a **non-release-ready draft**. Cursor and
Claude Code document the paths below, but the bounded Cursor dual-mode cycle
failed strict acceptance and reached its mandatory hard stop. Claude Code
behavior remains on hold and `UNVERIFIED`. These reference-only manual
procedures do not claim compatibility or support.

## Verification labels

Each destination and installation block distinguishes:

- **Documented host path:** the host's current official documentation lists
  the containing skills directory.
- **Manual command:** the local `mkdir` and `cp` procedure is documented here,
  not supplied by the host.
- **Current evidence:** the completed Cursor rounds contain case-specific
  passes and failures, but strict acceptance is unmet. Claude Code behavior is
  `UNVERIFIED`.
- **Historical evidence:** earlier Cursor results and the earlier Claude Code
  package load used the former protocol. They do not verify this contract.

Do not treat a documented path, successful copy, discovery trace, or explicit
load trace as behavioral compatibility evidence. See the
[verification record](verification.md) for status, environments, and blockers.

## Current bounded evidence

Cursor round one used the pre-remediation skill for 21 fresh sessions and 39
scored responses: 6 cases passed and 5 failed. The one permitted revision
produced the final skill; its targeted round used 9 fresh sessions and 20
responses: 0 cases passed and all 5 failed again. All 59 budget checks passed,
and neither round had a safety-warning or procedural-safety failure.

The policy hard stop has been reached. Cursor strict acceptance is unmet, the
final skill has no passing full-suite result, and this guide does not imply
another remediation round. Claude Code stopped before inference for
insufficient API credit; its behavior remains on hold and `UNVERIFIED`.

## Canonical source

The installable source is the complete directory at
`skills/progressive-clarity/`:

```text
skills/
└── progressive-clarity/       # Copy this directory as one unit
    ├── SKILL.md               # Required Agent Skills entry point
    └── LICENSE                # Apache License 2.0 text
```

The contents of that directory at the selected repository revision are
authoritative. Keep the directory name `progressive-clarity`, and do not copy
only selected files. Files elsewhere in the repository, including `docs/`,
`evals/`, `examples/`, and `templates/`, are not part of the installed skill.

The [verification record](verification.md#frozen-dual-mode-inputs) freezes the
canonical skill at SHA-256
`5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`.
The copy commands preserve the selected files; they do not convert an older
installation or establish a passing host result.

Run the commands below from the root of a Progressive Clarity checkout. For an
initial installation, the destination
`<skills-root>/progressive-clarity/` must not already exist. If it does, follow
[Update a manual installation](#update-a-manual-installation) first so that a
recursive copy does not retain stale files.

## Cursor

Cursor currently documents two project skills roots and two user skills roots.
Choose one root for a given scope; do not install duplicate copies under both
names.

| Scope | Destination | Verification status |
| --- | --- | --- |
| Project | `/path/to/project/.agents/skills/progressive-clarity/` | Documented path; bounded dual-mode cycle executed; strict acceptance failed; unsupported |
| Project | `/path/to/project/.cursor/skills/progressive-clarity/` | Documented only; UNVERIFIED |
| User | `~/.agents/skills/progressive-clarity/` | Documented only; UNVERIFIED |
| User | `~/.cursor/skills/progressive-clarity/` | Documented only; UNVERIFIED |

### Project installation through `.agents`

**Status: documented host path and manual commands. The isolated bounded
Cursor cycle used this project path, failed strict acceptance, and reached its
hard stop. This is not a supported installation.**

Replace `/path/to/project` with the target project's absolute path:

```bash
mkdir -p "/path/to/project/.agents/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.agents/skills/"
```

### Project installation through `.cursor`

**Status: documented host path; manual commands; not tested; UNVERIFIED.**

Replace `/path/to/project` with the target project's absolute path:

```bash
mkdir -p "/path/to/project/.cursor/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.cursor/skills/"
```

### User installation through `.agents`

**Status: documented host path; manual commands; not tested; UNVERIFIED.**

```bash
mkdir -p "$HOME/.agents/skills"
cp -R "skills/progressive-clarity" "$HOME/.agents/skills/"
```

### User installation through `.cursor`

**Status: documented host path; manual commands; not tested; UNVERIFIED.**

```bash
mkdir -p "$HOME/.cursor/skills"
cp -R "skills/progressive-clarity" "$HOME/.cursor/skills/"
```

## Claude Code

Claude Code calls user-level skills “personal” skills. Its current
documentation lists one project path and one personal path.

| Scope | Destination | Verification status |
| --- | --- | --- |
| Project | `/path/to/project/.claude/skills/progressive-clarity/` | Documented path; former-package evidence historical; dual-mode behavior on hold for credit; UNVERIFIED |
| User/personal | `~/.claude/skills/progressive-clarity/` | Documented only; UNVERIFIED |

### Project installation

**Status: documented host path. The earlier discovery and explicit-load
observation used the former protocol. Dual-mode behavior is on hold because
Claude Code reported insufficient API credit; current discovery, invocation,
and behavior remain UNVERIFIED.**

Replace `/path/to/project` with the target project's absolute path:

```bash
mkdir -p "/path/to/project/.claude/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.claude/skills/"
```

### User/personal installation

**Status: documented host path; manual commands; not tested; UNVERIFIED.**

```bash
mkdir -p "$HOME/.claude/skills"
cp -R "skills/progressive-clarity" "$HOME/.claude/skills/"
```

## Host invocation

Cursor completed the bounded dual-mode evidence cycle through the project
`.agents` path, but five cases failed both the initial and targeted rounds, so
strict acceptance and support remain unmet. Claude Code did not reach
inference, so its dual-mode behavior remains `UNVERIFIED`.

- **Explicit host invocation:** Cursor documents selecting a discovered skill
  by typing `/` in Agent chat and searching for its name. Claude Code documents
  direct `/skill-name` invocation. The expected selection or command is
  `progressive-clarity` or `/progressive-clarity`, respectively.
- **Automatic host invocation:** both hosts document loading a skill when its
  name and description are relevant to the request.

Explicit and automatic host invocation are separate from the protocol's
conversation modes. A response that resembles the protocol is not proof that
the skill loaded. A host trace, when available, is a separate evidence
dimension. The closed bounded cycle does not authorize another rerun.

## Conversation modes

After a synchronized dual-mode skill loads, the protocol uses one sticky
conversation mode:

- **Verbose mode is the default.** A new conversation starts in Verbose mode.
  Each ordinary in-scope response renders the visible headings **At a glance**,
  **In context**, and **At depth**, in that order. Each deeper section adds
  information without replaying an earlier section.
- **Progressive mode is explicit and sticky.** On a new topic, the first
  substantive response renders **At a glance** only. An unqualified `More`
  advances to **In context**, then **At depth**, rendering only the new view.
  A topic change resets topic depth but does not reset Progressive mode.
- **Mode-switch commands:** `Progressive mode` and `Verbose mode` change the
  sticky mode when presented case-insensitively as a command or clear mode
  directive. A standalone command renders no view. If the same message also
  asks a substantive question, the mode changes before that question is
  answered.
- **Per-response view overrides:** an explicit request for `At a glance`,
  `In context`, or `At depth` changes only that response. It does not change
  the sticky mode. If a message includes both a mode command and a view
  override, the mode changes first, the override applies once, and the new
  mode remains active afterward.

In Verbose mode, `More` adds purposeful At depth detail only; it does not
render all three views again. Direct one-off entry at In context or At depth
integrates lower-view essentials under the requested heading without adding
separate lower-view sections.

Cursor observations are limited to the named frozen cases and include both
passing and failing behavior; they do not establish general compatibility.
Claude Code mode switching, persistence, view overrides, headings, and
expansion behavior remain `UNVERIFIED`.

## Update a manual installation

There is no automated updater in version 0.1. To update a manual copy:

1. Obtain the intended newer repository revision and review its
   `skills/progressive-clarity/` directory.
2. Locate the one installed directory selected above.
3. Preserve any local changes outside every documented skills root, then
   remove the installed `progressive-clarity/` directory. A backup left inside
   a skills root could also be discovered.
4. Repeat the matching installation block to copy the complete canonical
   directory into the same root.
5. Start a new host session before checking discovery; do not infer
   compatibility from the copy alone.

This replacement/update procedure has not been exercised with the dual-mode
package and remains `UNVERIFIED`.

## Uninstall a manual installation

Delete only the installed `progressive-clarity/` directory from the one root
you selected:

- Cursor project: one of
  `/path/to/project/.agents/skills/progressive-clarity/` or
  `/path/to/project/.cursor/skills/progressive-clarity/`;
- Cursor user: one of `~/.agents/skills/progressive-clarity/` or
  `~/.cursor/skills/progressive-clarity/`;
- Claude Code project:
  `/path/to/project/.claude/skills/progressive-clarity/`;
- Claude Code user/personal:
  `~/.claude/skills/progressive-clarity/`.

Leave the containing skills root and unrelated skills in place. Start a new
host session before checking that the skill is no longer discoverable. These
removal steps remain `UNVERIFIED`.

## Security posture

The version 0.1 package is instruction-only:

- it contains no executable scripts;
- it grants or pre-approves no tools;
- it requires no network access; and
- it installs no service, hook, plugin, or background process.

The skill organizes an AI response. It does not add host capabilities, bypass
host permissions, or prevent the host from using capabilities independently
available to it. Review the selected source revision before copying it.

## GitHub CLI limitation

The current GitHub CLI manual documents skill management as a preview feature,
but the locally installed GitHub CLI is version `2.62.0`. On this machine,
`gh help skill` reports `Unknown help topic [skill]`.

No GitHub CLI skill installation, update, or removal command is recommended
here. Such instructions must remain absent until a compatible CLI is
provisioned and the exact workflow is reproduced. Current upstream
documentation does not establish local availability or host compatibility.

## OpenAI status

OpenAI packaging, access, testing, and publication status is maintained only in
the [OpenAI plugin packaging record](openai-plugin.md). This dual-mode
documentation update does not add an OpenAI compatibility or support claim.
Portal upload and submission are blocked because Cursor strict acceptance
failed; no upload occurred.

## Official sources

Sources checked on 17 August 2026:

- [Agent Skills specification](https://agentskills.io/specification) for the
  canonical skill directory and `SKILL.md` entry point;
- [Cursor Agent Skills](https://cursor.com/docs/skills) for project and user
  discovery paths and manual or automatic invocation concepts;
- [Claude Code skills](https://code.claude.com/docs/en/skills) for project and
  personal discovery paths and explicit or automatic invocation concepts; and
- [GitHub CLI `gh skill` manual](https://cli.github.com/manual/gh_skill) only
  to record that the upstream feature is preview and unavailable in the local
  `2.62.0` installation.

See the [verification record](verification.md) and
[Version 0.1 scope and limitations](limitations.md) before evaluating these
procedures.
