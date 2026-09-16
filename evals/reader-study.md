# Reader-benefit comparison plan

Status: **study design only; no participant outcomes have been collected**.
Protocol compliance, model-judge assessments, and human reader outcomes are
separate results. Do not use any one as a substitute for the others.

## Freeze the design before generation

Record the suite and instruction hashes, model/deployment and generation
settings, date, sampling plan, condition order, participant population, tasks,
scoring key, exclusions, and analysis plan. Hold the model and settings constant
across conditions. Randomize condition execution order to reduce time/deployment
effects. Include ordinary conversations and consequential tasks across domains.

The four conditions are:

| Condition | Instructions | Question it helps answer |
| --- | --- | --- |
| baseline | Generic helpful-assistant prompt | Does the method improve ordinary output? |
| minimal | Short core-principles prompt | How much benefit comes from the core idea? |
| legacy | Archived v0.4 long skill | What changes when rigid rules are removed? |
| revised | Current compact v0.5 skill | Does the revised implementation help readers? |

The legacy skill is preserved byte-for-byte in `baselines/v0.4-skill.md`.
It is an experimental condition, not current normative guidance. The baseline
is this API harness's ordinary response, not a claim about any product's hidden
system prompt. Current conformance scores for legacy/baseline arms are diagnostic;
they cannot establish which condition benefits readers.

## Tasks and outcomes

Before generating answers, have a domain reviewer write an answer key for each
task from its supplied facts. Specify the correct action, indispensable
conditions, acceptable uncertainty, and a retrieval question. Do not derive the
key from model outputs. Use tasks with multiple useful stopping points as well
as straightforward answers, tables, and code-heavy outputs.

Collect separately:

- **Action interpretation:** whether the reader identifies the appropriate action
  or recognizes that a decision is unresolved, scored against the frozen key.
- **Constraint recognition:** each indispensable condition identified or missed;
  retain per-condition results and denominators.
- **Retrieval time:** elapsed time from revealing the answer and task to the
  reader's submitted response; record timeouts and wrong answers separately.
- **Preference:** willingness to use the response again on a fixed 1–5 scale.
  For direct pairwise preference, use a separate phase after primary answers
  are locked, anonymize variants, and counterbalance their left/right order.
- **Secondary diagnostics:** prose-target adherence, whole Markdown characters
  and non-empty lines, unnecessary clarification, repetition usefulness, and
  factual errors. Source-text bulk includes Markdown syntax and is not reading time.

For stopping-point tests, assign different readers to the opening, opening plus
context, or whole answer. Do not expose later sections before collecting the
earlier stopping-point response. Evaluate Focused answers as complete answers.

## Prepare blinded packets

Run the same suite in each condition using `--no-judge` for reader-study capture;
semantic judges are unnecessary for generating reader packets. Reports must be
complete and match model settings, suite, selected cases, and run plan.

```sh
python3.11 -m tools.prepare_reader_study \
  evals/runs/baseline.json evals/runs/minimal.json \
  evals/runs/legacy.json evals/runs/revised.json \
  --seed 20260916 --readers 4 \
  --packets evals/studies/pilot-packets.json \
  --key evals/studies/pilot-investigator-key.json
```

The seed and four-reader block here illustrate reproducible counterbalancing,
not an adequate sample-size recommendation. Plan sample size from the primary
effect of interest and task/reader variability before the study.

Packets contain raw conversations and blank observation fields, with condition,
model, score, and source-report metadata removed. Give each reader only their
packet and the appropriate frozen task questions. Keep the investigator key
separate until scoring is locked. Output style may reveal a condition despite
label blinding; record that limitation.

Each reader sees one variant per case. Across a block of four readers every
case appears once in each condition, with task order shuffled. Run one is selected
in advance to avoid repeated exposure to the same case and post-hoc selection of
better outputs. Additional generation replicates require separately assigned
reader cohorts and a preregistered replication plan.

## Analysis and next revision

Report all runs and participants, exclusions, missing responses, accuracy,
constraint misses, time distributions, and preference by condition. Account for
task and reader variation rather than treating every turn as independent.
Report uncertainty intervals and adverse tradeoffs; a faster wrong answer is
not an improvement. Have blinded reviewers adjudicate ambiguous scoring.

Compare the full method against both baseline and minimal instructions. Remove
or revise constraints only when the observations justify the change. Test
alternative opening-length targets in a separately frozen experiment that keeps
the model and remaining instructions constant. No existing 40/200 conformance
result establishes those thresholds as optimal.
