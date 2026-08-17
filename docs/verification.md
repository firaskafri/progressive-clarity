# Verification record

This record describes the checks completed on 17 August 2026 for the frozen
Progressive Clarity version 0.1 draft. It separates structural evidence from
host behavior. It is not a compatibility, support, or release-readiness claim.

## Result labels

- **PASS** means the named check produced direct evidence for only the stated
  claim.
- **UNVERIFIED** means the available evidence could not establish the claim.
  It is neither a pass nor a failure.
- A structural pass does not imply behavioral conformance. Discovery or load
  evidence does not imply that a model followed the skill.

No host behavioral case failed, because neither host reached a scorable model
response. No host behavioral case passed for the same reason.

## Frozen inputs

The canonical files matched these SHA-256 values before host testing and after
the Wave 4 documentation integration:

- [`SPEC.md`](../SPEC.md):
  `90ccf39dc5cf91e895fb3cf2f1f788cba80daea94e1f07435748083c55bb4096`
- [`skills/progressive-clarity/SKILL.md`](../skills/progressive-clarity/SKILL.md):
  `4167d7fa89d008453b223d2ff33a2182096abefaffeab4698a65a6ce23bdbaae`
- [`skills/progressive-clarity/LICENSE`](../skills/progressive-clarity/LICENSE):
  `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`
- [`evals/cases.json`](../evals/cases.json):
  `b5c2becc53e6e7e167878de3f4f84451fd0d446c38ac4d5e6df74eaeef42cbd4`

The repository had no commit or `HEAD` during testing, so the file hashes are
the available canonical revision identifiers. All repository files were
reviewed during Wave 4. No integration defect requiring a change to the
specification, skill, or evaluation behavior was found.

## Structural validation

### Official Agent Skills validator — PASS

Environment:

- operating system: Darwin 25.6.0, arm64;
- `uv`: 0.11.8;
- validator environment Python: 3.11.15;
- upstream repository: `agentskills/agentskills`;
- pinned revision:
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`.

The official demonstration `skills-ref` validator was installed from that
detached source revision with `uv sync`. The command:

```sh
skills-ref validate \
  "/Users/firaskafri/Work/progressive-clarity/skills/progressive-clarity"
```

returned:

```text
Valid skill: /Users/firaskafri/Work/progressive-clarity/skills/progressive-clarity
```

This passes Agent Skills structural validation only. It does not execute the
skill or establish host compatibility.

### Repository validation — PASS locally

Environment:

- operating system: Darwin 25.6.0, arm64;
- Python: 3.12.12;
- workflow runner declared in CI: `ubuntu-24.04`;
- workflow `uv` version: 0.11.8.

The local CI-equivalent repository commands passed:

```sh
python3 -m json.tool evals/cases.json >/dev/null
python3 tools/validate_repository.py
```

The repository validator returned:

```text
Repository validation passed.
```

Its checks cover frozen hashes, UTF-8 and whitespace rules, relative Markdown
destinations and anchors, the instruction-only skill package, standard
frontmatter, evaluation references and run policy, and terminology
allowlists. The skill contains only `SKILL.md` and `LICENSE`; neither is
executable, and no symlink, script, or tool is installed with it.

The GitHub Actions workflow reproduces these commands with read-only contents
permission, disabled persisted credentials, actions pinned by full commit
SHA, and the same pinned `skills-ref` revision. A hosted GitHub Actions run is
**UNVERIFIED** because the repository has no commit to push or check out.

## Host verification

The fixed suite contains 15 cases. Its policy requires 25 fresh sessions and
42 scorable assistant responses per host, with three runs each for `PC-01`,
`PC-03`, `PC-06`, `PC-10`, and `PC-11`. Multi-turn cases must keep their
turns in one session. See the [evaluation guide](../evals/README.md) and
[case data](../evals/cases.json).

### Cursor

Environment and attempted configuration:

- Cursor desktop/launcher: 3.15.19;
- Cursor commit: `de07bee81cefe43461ebf4f40c3d2d78d15052a0`;
- Cursor Agent CLI: `2026.01.23-916f423`;
- operating system: Darwin arm64;
- isolated project: `/private/tmp/progressive-clarity-cursor-wave3`;
- installation:
  `.agents/skills/progressive-clarity`;
- mode: `ask`;
- output format: JSON;
- model reported by `about`: `Auto`;
- authentication: not logged in;
- `CURSOR_API_KEY`: not set.

**PASS:**

- the complete skill directory was copied into the isolated project;
- installed paths, bytes, modes, and symlink state matched the canonical
  source;
- installed `SKILL.md` and `LICENSE` matched the frozen hashes above;
- the package remained instruction-only and non-executable.

**UNVERIFIED:**

- runtime discovery or load by Cursor;
- explicit invocation;
- automatic activation and negative-trigger inactivity;
- every fact, caveat, budget, expansion, correction, and non-fit behavior in
  `PC-01` through `PC-15`;
- Cursor behavioral compatibility and support.

The noninteractive probe stopped before session creation or model loading:

```text
Error: Authentication required. Please run 'cursor agent login' first, or set CURSOR_API_KEY environment variable.
```

The command exited `1`. Completed sessions were `0/25`; scorable responses
were `0/42`. The probe was not counted as a case run.

### Claude Code

Environment and attempted configuration:

- Claude Code: 2.1.72;
- binary: `/Users/firaskafri/.local/bin/claude`;
- selected model: `claude-sonnet-4-6`;
- model execution: not reached;
- operating system: Darwin arm64;
- isolated project:
  `/private/tmp/progressive-clarity-claude-wave3.wVZFUX`;
- installation:
  `.claude/skills/progressive-clarity`;
- settings source: `project`;
- permission mode: `dontAsk`;
- enabled tools: `Skill`;
- MCP servers and plugins: none;
- output style: `default`;
- fast mode: off.

**PASS:**

- the installed skill directory was byte-identical to the canonical source;
- the installed `SKILL.md` and `LICENSE` matched the frozen hashes above;
- Claude Code scanned the project skills directory and reported one project
  skill;
- `progressive-clarity` appeared in both the skill and slash-command lists;
- `/progressive-clarity` was parsed and the full skill text was attached for
  the attempted explicit `PC-02` invocation.

**UNVERIFIED:**

- the rendered behavior for the explicit `PC-02` invocation;
- automatic activation and negative-trigger inactivity;
- every fact, caveat, budget, expansion, correction, and non-fit behavior in
  `PC-01` through `PC-15`;
- Claude Code behavioral compatibility and support.

The first API request was rejected before inference with HTTP 400 and:

```text
Credit balance is too low
```

Input and output tokens were both zero, reported cost was `$0`, and the
synthetic error envelope was not scored as an assistant response. Completed
sessions were `0/25`; one blocked session was attempted; scorable responses
were `0/42`. Further attempts stopped after the definitive quota denial.

Local evidence hashes:

- raw JSON result:
  `07f1ad68bbb2cb65a3cc8f00e2ad4e22656b5f5a07ba5bce5378599d7ddc53ee`
- debug log:
  `cbeeddc410be87c4ff5577a7d6e714b01941b5e54bf5a6abc8be7c665f6a70b3`

These artifacts remain in the isolated temporary project and are not release
assets.

## Rerun structural checks

From the repository root:

```sh
source /Users/firaskafri/Work/code/lms-api/.venv/bin/activate
python3 -m json.tool evals/cases.json >/dev/null
python3 tools/validate_repository.py
```

To reproduce official validation from a fresh detached checkout:

```sh
SKILLS_REF_REVISION=69ef37e9424c0a7ea9dd2293b559e43ec8176379
SKILLS_REF_ROOT="$(mktemp -d)"
git clone --filter=blob:none --no-checkout \
  https://github.com/agentskills/agentskills.git \
  "$SKILLS_REF_ROOT"
git -C "$SKILLS_REF_ROOT" checkout --detach "$SKILLS_REF_REVISION"
test "$(git -C "$SKILLS_REF_ROOT" rev-parse HEAD)" = \
  "$SKILLS_REF_REVISION"
cd "$SKILLS_REF_ROOT/skills-ref"
uv sync
source .venv/bin/activate
skills-ref validate \
  "/Users/firaskafri/Work/progressive-clarity/skills/progressive-clarity"
```

## Rerun host behavior

Do not reuse the blocked runs as behavioral evidence. After the user restores
the required host access, copy the same frozen skill into new isolated
projects and rerun all cases from scratch.

For Cursor:

1. Authenticate the Agent CLI locally or provide it an authorized local
   credential; do not record the credential in evaluation artifacts.
2. Confirm `cursor agent status` and `cursor agent models`.
3. Create one fresh chat for every `(case, run)` pair, preserving a single
   chat across turns of each continuity case.
4. Use the host's explicit skill picker for `PC-02`; use the unchanged prompts
   for automatic and negative cases.
5. Capture raw JSON or IDE output, host traces, model/settings, counts, and
   every result field required by `evals/cases.json`.

A first-turn noninteractive command has this form:

```sh
NO_OPEN_BROWSER=1 cursor agent \
  --print \
  --mode ask \
  --output-format json \
  --workspace "$CURSOR_PROJECT" \
  "$PROMPT"
```

Use the current `cursor agent help create-chat` and
`cursor agent help resume` interfaces to preserve the suite's session rules.
If terminal explicit invocation is unsupported, run only `PC-02` through the
Cursor IDE skill picker and preserve its raw output separately.

For Claude Code, use a new UUID for each `(case, run)` pair. Begin `PC-02`
with `/progressive-clarity`; leave automatic-case prompts unchanged:

```sh
claude -p \
  --output-format json \
  --verbose \
  --session-id "$SESSION_ID" \
  --setting-sources project \
  --permission-mode dontAsk \
  --tools Skill \
  --no-chrome \
  --debug-file "$DEBUG_FILE" \
  "$FIRST_TURN"

claude -p \
  --output-format json \
  --verbose \
  --resume "$SESSION_ID" \
  --setting-sources project \
  --permission-mode dontAsk \
  --tools Skill \
  --no-chrome \
  --debug-file "$NEXT_DEBUG_FILE" \
  "$NEXT_TURN"
```

Score all 25 sessions and 42 responses per host using `PASS`, `FAIL`, or
`UNVERIFIED` exactly as defined by the suite.

## Release readiness

Version 0.1 is **not release-ready**. The structural checks above pass, but
the release acceptance criteria require behavioral and activation evidence
that does not yet exist.

User action is required to:

1. authenticate Cursor locally and complete the full Cursor suite;
2. restore sufficient Claude API credit and complete the full Claude suite;
3. confirm licensing authority and resolve the documented name-risk review;
4. authorize a first commit before a clean-checkout test, hosted CI run,
   reviewable release diff, tag, or release can exist.

Until those gates pass, the [installation guide](installation.md) remains
evidence-limited and the [limitations](limitations.md) remain controlling for
all compatibility and support claims.
