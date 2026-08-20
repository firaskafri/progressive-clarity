# Progressive Clarity v0.4 Advisory host acceptance

`cases.json` scores visible topic-oriented behavior in ChatGPT, Cursor, and
Claude Code. This surface is **Advisory**: no current v0.4 host run exists, so
its status is `UNVERIFIED`. Historical v0.2 and v0.3.x results remain separate
in `docs/verification.md`.

## Active cases

- `T01`: focused fact, full orientation, focused exploration, full handoff.
- `T02`: explicit focused and full presentation.
- `T03`: information update followed by material re-synthesis.
- `T04`: narrow and material corrections.
- `T05`: indispensable safety warning.
- `T06`: clarification before orientation.
- `T07`: exact controlling text.
- `T08`: narrative non-fit.
- `T09`: sequential procedure non-fit.
- `T10`: best-effort return to an earlier topic.

## Evidence boundary

The suite scores only observable output: focused/full cadence, directness,
caveats, continuity, repetition, filler, and purpose-specific shapes. It does
not infer trusted topic IDs, policy reasons, committed state, or host activation
without an exposed trace.

`tests/` separately exercises protocol `0.4`, schemas `3.0.0`, caller-driven
policy, per-topic state, focused/full rendering, deterministic English counts,
fact reuse, corrections, quotations, atomic state, and the two-attempt wrapper.
A local mechanical pass does not pass this advisory suite.

## Run policy

Run each case in a fresh session and preserve one session for all turns in that
case. Run `T04` and `T05` three times per host. The initial round contains 14
sessions and 29 scored responses per host.

### ChatGPT isolation

- Use Temporary Chat.
- Disable ChatGPT memory.
- Use one fresh chat for each case run.
- Preserve one chat only for the turns within that case run.
- Record model, settings, and date.
- Record the visible Skill activation indicator exactly as shown.
- Preserve raw transcripts unchanged. Put counts, annotations, and scores in a
  separate record.

These controls prevent facts from another case or prior chat from entering the
oracle. In particular, T06 must not inherit staging, validation, or rollback
facts before the user supplies them.

Every prescribed run must pass. The maintainer explicitly authorized controlled
continuation on 2026-08-20 after the first bounded remediation remained below
100%. Complete and review each round before revising, rerun only failed cases
with every prescribed repetition, never average outcomes, and stop when every
run passes or the maintainer pauses the cycle.

## Scoring

Use `PASS`, `FAIL`, or `UNVERIFIED`.

A focused response must answer directly without a forced three-view sequence,
general recap, or manufactured depth. A simple fact uses at most three
sentences unless an indispensable safety or accuracy caveat requires more;
sentence one answers, an optional indispensable distinction may follow, and
then it stops without a use-case catalogue or anticipated next question.

A full response must render At a glance, In context, and At depth exactly once
and in order and keep non-warning English prose within the 40/200 limits. Every
deeper view must be dominated by new information. Names, dates, identifiers,
and necessary short anchors may recur, but a complete conclusion, sentence,
list, explanation, warning, or recommendation may not be repeated or
paraphrased. At depth must not end with a recap, summary, “key rule,” or
restated operative recommendation.

Score Full composition against this private workflow:

1. Draft At a glance.
2. Extract its complete propositions into a “do not restate” ledger.
3. Draft In context using only new rationale, constraints, or actions plus
   minimal anchors.
4. Add its complete propositions to the ledger.
5. Draft At depth using only new evidence, exceptions, or implementation.
6. Delete any sentence that restates a ledger proposition.
7. Delete any concluding recap from At depth.

Positive: “For Atlas, Security owns the gate” may anchor new ownership after an
At-a-glance Atlas recommendation. Negative: repeating “Atlas must wait for
security approval” or ending “Key rule: delay Atlas” fails.

When governing inputs are missing, require:

```text
Governing input: <missing dependency>.

Example assumption: <number and the assumption that justifies it>.
```

`Example assumption:` is the required combined Example/Assumption label. A
“good default,” “I’d use,” or numeric value or range outside this structure
fails.
Supplied governing inputs permit a direct number.

Clarification asks one focused question without a conditional recommendation,
rationale, or implementation detail. Corrections use the literal explicit
repair pattern; under automatic presentation, material corrections use Full
format while narrow corrections remain Focused. A material warning places
prohibition, hazardous state,
concrete harm, containment, and resume condition in At a glance. Controlling
text explanations preserve the source under `Controlling text:` and use the
literal `Non-controlling plain-language summary:` label. Exact output, narrative
voice, and complete procedure order retain their required shape.

Activation requires the visible host indicator or another exposed host trace.
Similar output is not activation evidence, and a trace does not prove
behavioral conformance.

## Automated Azure behavior proxy

`tools.azure_eval_harness` runs the behavior suite through an explicitly named
Azure OpenAI deployment using Agno. It injects the canonical Skill as the system
message, creates a new Agno agent for each prescribed case run, preserves turns
inside that run, captures raw output, applies deterministic presentation and
budget checks, and optionally requests a structured semantic judgment. The
judge receives only criteria applicable to the current turn: universal
accuracy/fact/prohibition checks plus presentation- and contract-specific
criteria. Unrelated correction and warning criteria are omitted.

This is a regression proxy, not ChatGPT acceptance evidence. It cannot verify
ChatGPT package installation, automatic Skill selection, the visible Skill
indicator, memory isolation, product system instructions, or UI behavior.
The same-deployment semantic judge is not independent and remains subject to
human review.

Use Agno 2.6.x or newer from the configured evaluation environment. Export
credentials without putting them on the command line:

```sh
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com"
export AZURE_OPENAI_API_KEY="<secret>"
export AZURE_OPENAI_EVAL_DEPLOYMENT="<latest-deployment-name>"
export AZURE_OPENAI_API_VERSION="2024-10-21"
```

Alternatively, copy `evals/azure.local.example.json` to
`evals/azure.local.json` and fill its four top-level values. The local file is
ignored by Git and loaded automatically; use `--config <path>` to select
another ignored JSON file. Never place real credentials in the committed
example or Python source.

The harness has no deployment default. `--deployment` or one of
`AZURE_OPENAI_EVAL_DEPLOYMENT`, `AZURE_OPENAI_CHAT_DEPLOYMENT`, or
`AZURE_OPENAI_DEPLOYMENT` is required so an older deployment cannot be selected
silently.

Plan calls without credentials:

```sh
python3 -m tools.azure_eval_harness --dry-run
python3 -m tools.azure_eval_harness --dry-run --case T01 --case T06
```

Run one case or the complete prescribed suite:

```sh
python3 -m tools.azure_eval_harness --case T01 --output evals/runs/t01.json
python3 -m tools.azure_eval_harness --output evals/runs/complete.json
```

Use `--no-judge` to capture generations and deterministic checks without the
second model call. The harness creates the report with status `RUNNING`, writes
an atomic checkpoint after every completed case run, marks a caught keyboard
interrupt as `INTERRUPTED`, and marks successful suite execution as `COMPLETE`.
Each checkpoint records suite/protocol identity, the exact Skill-body hash,
deployment, API version, judge mode, selected cases, completed case/run keys,
and current aggregate state.

Resume an interrupted or otherwise incomplete checkpoint in place:

```sh
python3 -m tools.azure_eval_harness \
  --resume evals/runs/complete.json
```

Resume validates suite ID, suite hash, protocol hash, Skill-body hash,
deployment, API version, judge mode, selected cases, and planned runs before
making a model call. Completed runs are skipped; an interrupted run without a
completed record is replayed in a fresh Agno session. Reports are written under
ignored `evals/runs/` by default and never contain the API key or full endpoint.
The same-deployment judge remains non-independent even when its criteria are
correctly scoped.

## Validation

From the repository root:

```sh
python3.11 -m json.tool evals/cases.json >/dev/null
python3.11 -m tools.validate_repository
```

Repository validation checks suite identity, case and fact references,
sequential turns, repetitions, totals, protocol hash, frozen inputs, and the
Advisory/Enforced boundary.
