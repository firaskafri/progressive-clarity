# Install Progressive Clarity

## Current v0.4 status

Progressive Clarity protocol `0.4` is a locally verified release candidate with
two separate profiles:

- the portable prompt-only skill is **Advisory** and uses topic inference plus
  Focused/Full cadence; and
- the optional Python 3.11+ non-streaming wrapper enforces mechanically
  decidable checks over trusted topic metadata and buffered output.

The v0.4 package target version is `0.4.2`. The intended package and artifact
names are:

- Python distribution: `progressive-clarity-core` version `0.4.2`;
- OpenAI package:
  `dist/progressive-clarity-openai-plugin-0.4.2.zip`;
- Claude plugin:
  `dist/progressive-clarity-claude-plugin-0.4.2.zip`; and
- Claude.ai custom Skill:
  `dist/progressive-clarity-claude-ai-skill-0.4.2.zip`.

Local v0.4 artifacts were built and verified; their exact SHA-256 values are
recorded in [Verification](verification.md). Do not substitute a v0.2 or v0.3.x
artifact or hash retained in the historical record. These instructions do not
claim registry publication, portal upload, review, approval, external
publication, or universal host compatibility.

## Install the prompt-only skill from source

The canonical installable directory remains:

```text
skills/
└── progressive-clarity/
    ├── SKILL.md
    └── LICENSE
```

Copy that directory as one unit. Do not copy `pc_core/`, `docs/`, `evals/`,
`examples/`, `templates/`, or hook configuration into the prompt-only skill.

### Cursor project scope

Choose one documented project root:

```sh
mkdir -p "/path/to/project/.agents/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.agents/skills/"
```

or:

```sh
mkdir -p "/path/to/project/.cursor/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.cursor/skills/"
```

### Claude Code project scope

```sh
mkdir -p "/path/to/project/.claude/skills"
cp -R "skills/progressive-clarity" "/path/to/project/.claude/skills/"
```

Successful copying or host discovery does not establish invocation or
conforming behavior. Explicit invocation is `progressive-clarity` in Cursor's
skill picker or `/progressive-clarity` in Claude Code. Automatic selection,
topic inference, and presentation selection remain host-controlled.

## Run `pc-core` from source

From this repository root:

```sh
python3.11 -m pc_core --help
```

Protocol, wrapper request, envelope, and state compatibility are strict:

- protocol version: `0.4`;
- wrapper request schema: `3.0.0`;
- envelope schema: `3.0.0`; and
- conversation-state schema: `3.0.0`.

Use a fresh v0.4 state path. Earlier protocol state, including v0.3 with schema
`3.0.0`, is unsupported and is not silently migrated. Preserve an old state
file if it is evidence; do not reuse it for v0.4.

Validate or render a prepared candidate:

```sh
python3.11 -m pc_core validate candidate.json \
  --state conversation-state-v04.json \
  --request request.json

python3.11 -m pc_core render candidate.json \
  --state conversation-state-v04.json \
  --request request.json
```

`render` requires the trusted request. Without `--request`, structural
validation cannot certify the resolved topic and presentation policy, so
rendering is refused and no candidate Markdown is written.

Invoke a non-streaming local host:

```sh
python3.11 -m pc_core wrap \
  --host cursor \
  --request request.json \
  --state conversation-state-v04.json \
  --cwd /path/to/project
```

Replace `cursor` with `claude-code` for Claude Code. Policy resolves before the
host call from `topic_action` (`start`, `continue`, or `resume`), `turn_kind`,
`presentation_request`, and the target topic's committed state. The wrapper
allows one initial candidate and one complete repair, commits state only after
a mechanical pass, and otherwise withholds candidate output. If `--report` is
used, it must name a different path from both `--state` and `--request`.

For a fresh Cursor workspace, first review and accept trust interactively.
Alternatively, add `--trust-workspace` as explicit authorization for the
configured `--cwd`. The wrapper never adds Cursor's trust flag by default.

See [Local deterministic enforcement](local-enforcement.md) for the complete
request, response-kind, state, and guarantee boundaries.

## Optional project hooks

To use a hook template, install the reviewed local checkout into the target
project's ignored Python 3.11 virtual environment:

```sh
python3.11 -m venv "/path/to/project/.pc-core/venv"
"/path/to/project/.pc-core/venv/bin/python" -m pip install \
  "/path/to/progressive-clarity"
"/path/to/project/.pc-core/venv/bin/pc-core" --help
```

Then merge only the selected template:

- `adapters/cursor/hooks.json` into `.cursor/hooks.json`; or
- `adapters/claude-code/settings.json` into `.claude/settings.json`.

Review the commands and preserve unrelated settings. The hooks inspect text
after generation and may request one retry for an empty view inside an exact
three-heading sequence. They remain **Advisory/block-and-retry**. Other
visible-only format, budget, and duplicate judgments are nonblocking, so hooks
cannot certify that the host selected the correct presentation. Use the wrapper
when invalid output must be withheld.

## Build target artifacts

After all v0.4 version and packaging inputs are synchronized locally, build:

```sh
python3.11 -m tools.package_openai_plugin
python3.11 -m tools.package_claude_plugin
python3.11 -m tools.package_claude_skill
```

Build each artifact twice without changing inputs and compare the reported
SHA-256 values. The current matching local hashes and inventories are recorded
in [Verification](verification.md); repeat these checks after any package input
changes.

## Current evidence boundary

No `0.4.2` live ChatGPT, Cursor, or Claude acceptance run exists. User-provided
v0.3.0–v0.3.2 ChatGPT observations are historical and recorded in
[Verification](verification.md). Current activation, topic inference,
presentation selection, and rendered conformance are **UNVERIFIED**. Package
construction and local tests do not establish host compatibility or support.

## Historical/superseded v0.3.x installation boundary

Package versions 0.3.0 through 0.3.2 and their hashes are historical. Do not
install them as v0.4 artifacts or point v0.4 commands at their state files.
Their user-provided ChatGPT results do not establish v0.4 behavior.

## Historical v0.2 installation and evidence

Everything below this heading is retained as historical v0.2 installation
guidance and evidence. References to “current,” v0.2 package names, old
artifacts, hashes, dated checks, and user-provided transcripts apply only to
that historical record.

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
access is still required. The current v0.2.1 prompt-only skill has no new
Cursor or Claude Code acceptance run and no independently executed full
ChatGPT acceptance run.

On 2026-08-18, the user reported uploading and installing the Advisory v0.2.1
ChatGPT ZIP. The repository did not independently capture those actions or
identify the installed portal bytes. In a user-provided complex gold-forecast
transcript from that date, the three-view structure triggered but the 40/200
budgets and additivity failed, making the response non-conformant. In a later
fresh fixed-facts smoke, automatic trigger, exact headings/order, a 26-word At
a glance, approximately 50 cumulative shallow words, supplied-fact coverage,
additivity, and a negative exact-output control returning exactly `323` passed.

The fixed-facts result is a bounded pass for those named checks, not universal
conformance or independent portal verification. The older user-reported
ChatGPT publication URL and earlier transcripts remain historical evidence in
[Verification](verification.md) and the [OpenAI record](openai-plugin.md).

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
