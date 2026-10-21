# Optional Cursor startup-rule integration

## Why use a project rule?

Cursor's [CLI documentation](https://cursor.com/docs/cli/using) supports
`.cursor/rules` and root `AGENTS.md`/`CLAUDE.md` as project instructions. Its
[rules documentation](https://cursor.com/docs/context/rules) says applied rule
contents are included at the start of model context and `alwaysApply: true`
includes an `.mdc` rule in every chat. A referenced file is not inlined: content
needed at startup must be placed in the rule body, not merely referenced.

This is different from dynamically reading a Skill. The
[rc.5 explicit-skill round](preamble-candidate.md) emitted loading commentary
before reading the skill in 4/4 sessions, including all three warning cases.
The startup-rule experiment below avoided that loading step. Neither path is
a semantic or safety certification.

The reviewed CLI help exposes no dedicated system-prompt or commentary-off
flag. This does not establish that no other documented integration can do so.
`--output-format text` is a rendering option, not proof that commentary was
never generated; output filtering was not used to obtain the results below.

## Optional project-local setup

This is an always-applied **rule integration**, not a plugin install or skill
activation test. It applies to every chat in the chosen project. Review existing
project/team rules for conflicts, and do not install duplicate instruction copies
without reviewing their interactions. No user-global setting is needed.

From the selected Progressive Clarity checkout, generate a new rule in a target
project you control. The following refuses to overwrite an existing rule and
copies the canonical body rather than a pointer to the Skill:

```sh
python3.11 - /absolute/path/to/target-project <<'PY'
from pathlib import Path
import sys
from tools.package_common import load_canonical_skill_source

source = Path.cwd().resolve()
target = Path(sys.argv[1]).expanduser()
if not target.is_absolute() or not target.is_dir():
    raise SystemExit("target must be an existing absolute project directory")
canonical = load_canonical_skill_source(
    source / "skills" / "progressive-clarity", root=source
)
rule = target / ".cursor" / "rules" / "progressive-clarity.mdc"
rule.parent.mkdir(parents=True, exist_ok=True)
with rule.open("xb") as output:
    output.write(b"---\nalwaysApply: true\n---\n" + canonical.body)
print(rule)
PY
```

Use a checkout of the desired revision. This command copies that checkout's
body, not a fixed rc.5 artifact. The historical rc.5 results below do not establish
behavior for the current rc.10 candidate or published 0.5.0 body.
Record the source revision and body hash. This copy does not update automatically.
Start a fresh Cursor session. To remove it, delete only the generated
`progressive-clarity.mdc`, leaving other rules intact. No global install was
performed for this investigation.

## Frozen rc.5 integration experiment — 2026-10-21

Before inference: one T01 direct-answer first turn and all three T05 warning
repetitions, four fresh sessions, concurrency two, 240 seconds per response,
zero retries. Cursor Agent `2026.10.19-6bbf2c4`, requested `gpt-5.2`, Ask mode,
stream-JSON output; all host init labels reported `GPT-5.2 Medium`.

The isolated workspace contained only one always-applied rule with the exact
unchanged rc.5 skill body. No Skill directory was installed, no explicit
skill-loading prefix was sent, and no evaluator-written warning was prepended.
The original development prompts were unchanged. Rule and prompt changes mean
this is a separate integration experiment, not a controlled causal attribution
of the earlier preamble to one specific host mechanism.

Canonical skill SHA-256:
`cb6e95151e4501641319f786fefbcc7e53f650ff5f6f9503f639a554429efcdd`.

All **4/4 responses completed**, with four distinct sessions, one visible
assistant message per session, and no captured tool calls.

- **Direct-answer opening: PASS, 1/1.** Redis classification and optional
  persistence appear directly, without a loading/planning preamble.
- **Warning-first opening: PASS, 3/3.** The response starts with At a glance
  and the do-not-restart warning, dual-writer hazard, payment-loss risk, and
  containment. No process commentary precedes the warning.
- These are named opening/placement checks, not exhaustive diagnostic safety,
  full-suite semantic conformance, numeric regression, or reader-benefit claims.
- Startup rule injection is documented but not exposed as a trusted activation
  trace in these captures. No automatic Skill activation is claimed.

Raw plan, prompts, traces, visible messages, metadata, and observations with
trace hashes are retained locally under ignored
`evals/runs/cursor-startup-rule-rc5-2026-10-21/`. The rule's body was verified
byte-identical to rc.5. The setup command was checked in temporary projects;
it is not an automated updater or a public independent transcript archive.

**Outcome: bounded passing opening checks for the optional startup-rule path.**
The subsequent [full development round](cursor-full-development.md) captured all
44 responses but failed acceptance, including clarification, repair, labeling,
topic handling, and presentation failures. The opening experiment alone must
not be used as a general rule-profile conformance claim.
The explicit-skill failures remain. rc.5 package bytes, published artifacts,
marketplace pins, and user-global configuration were not changed by this experiment.
