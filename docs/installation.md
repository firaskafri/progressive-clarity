# Install Progressive Clarity

Protocol v0.2 and package v0.2.1 are a non-release-ready draft. There is one
ordinary response behavior only: one response containing At a glance, In
context, and At depth in order. Two separate local surfaces implement or check
that contract:

- the portable prompt-only Agent Skill is **Advisory**;
- the optional Python 3.11+ non-streaming wrapper **Enforces mechanical checks**
  for output it buffers and releases.

Neither surface establishes semantic completeness, human outcomes, host-wide
compatibility, or support. Historical host evidence is recorded separately in
[Verification](verification.md).

## Prompt-only skill

The canonical installable directory is:

```text
skills/
└── progressive-clarity/
    ├── SKILL.md
    └── LICENSE
```

Copy the directory as one unit. Do not copy files from `pc_core/`, `docs/`,
`evals/`, `examples/`, or `templates/` into the skill.

### Cursor project scope

Choose one documented root:

```bash
mkdir -p "/path/to/project/.agents/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.agents/skills/"
```

or:

```bash
mkdir -p "/path/to/project/.cursor/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.cursor/skills/"
```

Cursor also documents equivalent user roots under `~/.agents/skills/` and
`~/.cursor/skills/`. User-global installation is not performed by this
repository.

### Claude Code project scope

```bash
mkdir -p "/path/to/project/.claude/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.claude/skills/"
```

Claude Code also documents `~/.claude/skills/` for personal skills. This
repository does not modify it.

Successful copying or discovery does not prove invocation or behavior.
Explicit invocation is `progressive-clarity` in Cursor's skill picker or
`/progressive-clarity` in Claude Code. Automatic selection remains host-owned.

## Deterministic local wrapper

From this repository root, the source tree is directly runnable:

```sh
python3.11 -m pc_core --help
```

Validate or render a prepared envelope:

```sh
python3.11 -m pc_core validate candidate.json \
  --state conversation-state.json \
  --request request.json

python3.11 -m pc_core render candidate.json \
  --state conversation-state.json \
  --request request.json
```

Invoke a non-streaming local host:

```sh
python3.11 -m pc_core wrap \
  --host cursor \
  --request request.json \
  --state conversation-state.json \
  --cwd /path/to/project
```

Replace `cursor` with `claude-code` for Claude Code. The wrapper allows at most
two total candidates and commits state only after a mechanical pass. See
[Local deterministic enforcement](local-enforcement.md) for request schema,
guarantees, and failure behavior.

For a fresh Cursor workspace, first review and accept trust interactively.
Alternatively, add `--trust-workspace` to the wrapper command as an explicit
authorization for the configured `--cwd`. The wrapper never adds Cursor's
`--trust` flag by default.

Both wrappers have synthetic structural and parsing coverage. A separate
bounded live Cursor remediation rerun produced 10 mechanically certified and 7
withheld responses: `E02`, `E06`, and `E07` passed; `E03`, `E04`, and `E05`
failed. That rerun exercised the mechanical wrapper fixes against the
pre-trigger-revision skill and did not satisfy strict semantic or behavioral
acceptance. Live Claude Code wrapper behavior remains `UNVERIFIED` because it
requires paid Anthropic API access.

## Optional project hooks

Reference templates live under `adapters/`. They do not modify user-global
settings. Before merging one into another project, install the reviewed local
checkout into that project's ignored Python 3.11 virtual environment:

```sh
python3.11 -m venv "/path/to/project/.pc-core/venv"
"/path/to/project/.pc-core/venv/bin/python" -m pip install \
  "/path/to/progressive-clarity"
"/path/to/project/.pc-core/venv/bin/pc-core" --help
```

Add `.pc-core/` to the target project's ignore rules. This is a project-local
source install, not a PyPI or global-install instruction. The checked-in hook
commands deliberately use `.pc-core/venv/bin/pc-core`; without that
prerequisite they fail rather than importing an unrelated global module.
The installed runtime has no third-party dependency; building the local wheel
uses the `hatchling` backend declared in `pyproject.toml`.

Then:

- merge `adapters/cursor/hooks.json` into `.cursor/hooks.json`;
- merge `adapters/claude-code/settings.json` into `.claude/settings.json`.

Review commands and preserve unrelated settings. These hooks inspect already
generated text and may request one retry. They are
**Advisory/block-and-retry**, not a certification boundary.

## Update or remove a manual skill copy

To update, review the new source revision, delete only the installed
`progressive-clarity/` directory, copy the complete canonical directory into
the same root, and begin a new host session. Do not leave backups inside a
skills root because hosts may discover them.

To uninstall, delete only that installed directory. Leave unrelated skills and
the containing root in place.

These manual update and removal procedures are documented but not current
behavioral compatibility evidence.

## Security posture

The prompt-only skill:

- contains no executable script;
- grants no tool;
- requires no network access; and
- starts no service, hook, or background process.

The separate `pc-core` package is executable local Python using only the
standard library. It starts no service, configures no MCP server, collects no
analytics, and changes no user-global settings. Host authentication,
permissions, tools, network access, and model cost remain host-controlled.

## Current evidence boundary

The older bounded Cursor prompt-only cycle failed strict acceptance and reached
its required hard stop. Claude Code stopped before inference for insufficient
API credit; its current adapter and hook are structurally tested, but paid live
access is still required. The current v0.2.1 prompt-only skill has no new host
acceptance run.

The Advisory v0.2.1 ChatGPT ZIP has not been uploaded. The older
user-reported ChatGPT publication URL and the user-provided non-conformant live
transcripts remain historical evidence in [Verification](verification.md) and
the [OpenAI record](openai-plugin.md). They do not verify v0.2.1.

## Official sources

Sources checked on 18 August 2026:

- [Agent Skills specification](https://agentskills.io/specification);
- [Cursor Agent Skills](https://cursor.com/docs/skills);
- [Cursor Hooks](https://cursor.com/docs/hooks);
- [Cursor CLI output format](https://cursor.com/docs/cli/reference/output-format);
- [Claude Code skills](https://code.claude.com/docs/en/skills);
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks);
  and
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference).
