# Install the Progressive Clarity skill

Progressive Clarity version 0.1 is a draft. Cursor and Claude Code document the
paths below. Wave 3 tested one project path in each host, but host behavior
remains unverified. These manual procedures do not claim compatibility or
support.

## Verification labels

Each destination and installation block distinguishes:

- **Documented host path:** the host's current official documentation lists
  the containing skills directory.
- **Manual command:** the local `mkdir` and `cp` procedure is documented here,
  not supplied by the host.
- **Test evidence:** only the exact project paths and dimensions marked
  `PASS` below were observed. Every other dimension remains `UNVERIFIED`.

Do not treat a documented path, successful copy, discovery trace, or explicit
load trace as behavioral compatibility evidence. See the
[verification record](verification.md) for hashes, environments, and blockers.

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
| Project | `/path/to/project/.agents/skills/progressive-clarity/` | Copy integrity PASS on Cursor 3.15.19; runtime discovery and behavior UNVERIFIED |
| Project | `/path/to/project/.cursor/skills/progressive-clarity/` | Documented only; UNVERIFIED |
| User | `~/.agents/skills/progressive-clarity/` | Documented only; UNVERIFIED |
| User | `~/.cursor/skills/progressive-clarity/` | Documented only; UNVERIFIED |

### Project installation through `.agents`

**Status: documented host path; manual commands; copy and byte equivalence
PASS; runtime discovery, invocation, and behavior UNVERIFIED.**

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
| Project | `/path/to/project/.claude/skills/progressive-clarity/` | Discovery and explicit load PASS on Claude Code 2.1.72; behavior UNVERIFIED |
| User/personal | `~/.claude/skills/progressive-clarity/` | Documented only; UNVERIFIED |

### Project installation

**Status: documented host path; manual commands; copy integrity, project
discovery, and explicit load PASS; rendered behavior and automatic activation
UNVERIFIED.**

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

## Invocation concepts

No host has completed behavioral invocation verification for Progressive
Clarity.

- **Explicit invocation:** Cursor documents selecting a discovered skill by
  typing `/` in Agent chat and searching for its name. Claude Code documents
  direct `/skill-name` invocation. The expected explicit selection or command
  for this package is `progressive-clarity` or `/progressive-clarity`,
  respectively. Cursor explicit invocation is `UNVERIFIED`. Claude Code
  project discovery and explicit load are `PASS`, but the API stopped before
  model inference, so the rendered response is `UNVERIFIED`.
- **Automatic invocation:** both hosts document that a skill can be loaded
  automatically when its name and description appear relevant to the current
  request. Intended activation and negative-trigger inactivity are
  `UNVERIFIED` in both hosts.
- **Protocol `auto`:** after the protocol is active, `auto` selects the
  shallowest response view that is complete and safe to stop. It does not
  activate or discover the skill. Automatic host invocation and protocol
  depth selection are separate decisions.

The full rerun must test explicit and automatic invocation separately and
capture a host trace when the host exposes one. A response that happens to
follow the protocol is not proof that the skill loaded.

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

This replacement/update procedure was not exercised in Wave 3 and remains
`UNVERIFIED`.

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
