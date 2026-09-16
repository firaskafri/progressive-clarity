# Progressive Clarity v0.5 evaluation

Three evidence tracks answer different questions:

1. **Development conformance:** does output follow the revised protocol?
2. **Unseen holdouts:** does behavior generalize beyond cases used for tuning?
3. **Reader outcomes:** do people interpret actions and constraints correctly,
   retrieve information efficiently, and prefer the answers?

Current v0.5 live-host, holdout, and reader-outcome results are **UNVERIFIED**.
Local `tests/` cover mechanical contracts and harness behavior without inference.
Historical host observations remain in [Verification](../docs/verification.md).

## Development suite

`cases.json` contains 18 cases, 22 sessions, and 44 scored responses per host.
T04 corrections and T05 warnings each have three prescribed runs. Preserve one
session for all turns of a case and start a fresh session for every case run.

| Cases | Coverage |
| --- | --- |
| T01–T03 | Orientation, exploration, explicit presentation, updates and synthesis |
| T04–T06 | Natural repairs, warning placement, useful clarification |
| T07–T10 | Controlling text, fiction, procedures, topic return |
| T11–T13 | Compact decisions, no-heading warnings, missing numeric inputs |
| T14–T15 | Corrected procedures and Full requests blocked by missing information |
| T16–T17 | Longer ambiguous topic conversation and useful repeated qualification |
| T18 | Natural cross-domain orientation with usefulness-based presentation |

Prompts avoid prescribing a sentence-by-sentence answer. Explicit Full requests
test requested presentation; compact and ambiguous cases test natural behavior.
The suite is public development material, not an unseen holdout.

## Scoring

Use `PASS`, `FAIL`, or `UNVERIFIED` for observable conformance. Evaluate accuracy,
required facts, caveat placement, appropriate shape, useful depth, assumptions,
clarification, and faithful correction. Natural correction wording and brief
helpful repetition are valid. A repetition failure must identify both passages
and explain the missing reader benefit. An input request may include rationale
or supported bounded advice, but may not authorize an unsupported action.

The 40/200 English limits are provisional Advisory targets. Harness budget
observations include `binding: false`: an exceeded target is recorded separately
and does not alone fail conformance. The Mechanical wrapper retains hard caps.
Whole-output character and non-empty-line diagnostics include code, tables,
headings, warnings, and Markdown syntax. They do not estimate reading time.

Repair meaning and numeric-assumption support require semantic review. Literal
labels do not establish them. Model judging is a regression proxy, not human
reader research. Record activation only when a host exposes a relevant trace;
similar formatting does not prove Skill activation.

## Frozen rounds and holdouts

Freeze instructions, suite, rubric, settings, and planned repetitions before a
round. Complete the round and retain every outcome and denominator. Failed-case
reruns are debugging evidence; after revision, a fresh full development run is
needed for a whole-suite claim. Inspecting and tuning to a holdout consumes it.

See [unseen holdout authoring](holdouts.md) and the
[blinded reader-study plan](reader-study.md). For manual ChatGPT evaluation, use
Temporary Chat with memory disabled, record model/settings/date and visible
activation indicators, and keep raw transcripts separate from annotations.

## Azure API regression and comparison harness

`tools.azure_eval_harness` uses Agno to run a named Azure OpenAI deployment. It
injects the selected instruction condition and preserves case history. This
does not verify a ChatGPT package installation, product system prompt, or host
activation. The optional same-deployment judge is non-independent.

Install Agno 2.6.x or newer in the evaluation environment and configure:

```sh
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com"
export AZURE_OPENAI_API_KEY="<secret>"
export AZURE_OPENAI_EVAL_DEPLOYMENT="<deployment-name>"
export AZURE_OPENAI_API_VERSION="2024-10-21"
```

Alternatively use the ignored `evals/azure.local.json`, matching
`azure.local.example.json`, or pass `--config` with another local configuration.
The harness has no deployment default. Credentials are not recorded in reports.

```sh
python3.11 -m tools.azure_eval_harness --dry-run
python3.11 -m tools.azure_eval_harness --case T11 --case T12 --dry-run
python3.11 -m tools.azure_eval_harness --condition revised \
  --output evals/runs/revised.json
```

For matched comparisons, run the same suite and settings with each of
`--condition baseline`, `minimal`, `legacy`, and `revised`, using separate output
paths. `baseline` uses a generic helpful-assistant prompt, `minimal` uses the
short principles prompt, `legacy` uses the preserved v0.4 skill, and `revised`
uses the compact current skill. `--no-judge` captures raw output and mechanical
observations without a second model call; semantic status remains `UNVERIFIED`.
Exit status 1 means `FAIL` or `UNVERIFIED`, so a completed `--no-judge` capture
normally returns 1 while still preserving its report for reader-study preparation.

Use `--suite path/to/suite.json` for an independently authored holdout or reader
study. A report records suite/protocol/instruction hashes, condition, split,
model settings, run plan, and raw responses. Startup and per-run checkpoints are
atomic; interrupted reports can resume:

```sh
python3.11 -m tools.azure_eval_harness --resume evals/runs/revised.json
```

For an external suite, pass the same `--suite` on resume. Condition defaults to
the saved one. Changed instructions, suite, model settings, or condition reject
resume. Completed runs are skipped. Incomplete interrupted runs replay in a fresh
session. A completed run with an error remains recorded, rather than being
silently replaced by a better attempt.

## Local validation

```sh
python3.11 -m tools.validate_repository
python3.11 -m unittest discover -s tests
```

Repository checks cover frozen inputs, suite identity, reference integrity, run
totals, package synchronization, and the Advisory/Mechanical guarantee boundary.
