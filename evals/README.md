# Progressive Clarity v0.1 two-mode acceptance

This directory contains the bounded, host-neutral acceptance suite for Cursor and Claude Code. It is pinned to `SPEC.md` SHA-256 `ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d`.

## Active suite

`cases.json` defines the only active acceptance cases:

- `M01`: Verbose default with all three additive views.
- `M02`: sticky Progressive mode, two `More` advances, and a switch to Verbose.
- `M03`: one-response view override and return to the sticky mode.
- `M04`: targeted branch expansion.
- `M05`: indispensable safety warning.
- `M06`: explicit correction and continued expansion.
- `M07`: clarification control dialogue.
- `M08`: controlling legal text hybrid.
- `M09`: narrative non-fit.
- `M10`: sequential procedure non-fit.
- `M11`: negative activation and exact-format response.

Former `PC-01` through `PC-15` results may remain in `docs` as historical evidence. They are not active cases, do not contribute to this suite's counts, and cannot establish acceptance.

## Run policy

Run every case once per host in a fresh session. Keep all turns of one case run in that session. Run `M02`, `M05`, `M06`, `M08`, and `M11` three total times per host, with the baseline execution counted as run 1.

The initial evidence round is exactly:

- 21 sessions and 39 scored assistant responses per host.
- 42 sessions and 78 scored assistant responses across both hosts.

Record every field listed in `run_policy.capture_fields`, including unmodified prompts and raw outputs. Every prescribed run must behaviorally pass. There is no majority vote, average score, or allowance for intermittent failure.

Any omitted indispensable warning, contradiction, hidden reversal, unsafe instruction, false or incomplete correction, controlling-text mutation, missing non-controlling label, or broken procedural safety condition is an immediate failure.

## Bounded remediation and hard stop

Permit one remediation cycle at most:

1. Complete the full initial evidence round.
2. Review failures and approve no more than one revision.
3. Rerun only failed cases, repeating all prescribed runs for each failed case.
4. Stop after that targeted rerun regardless of outcome.

Do not automatically rewrite, optimize, or begin another cycle. If the oracle is ambiguous, stop remediation until the ambiguity is resolved. Do not weaken a warning, correction, exact-text requirement, user constraint, or procedural safety condition to gain a pass.

## Scoring

Use `PASS`, `FAIL`, or `UNVERIFIED`.

### Observable behavior

Score rendered behavior directly:

- visible view headings and their order;
- required facts and caveats at each stopping point;
- word budgets and cumulative counts;
- mode-switch and one-off-override consequences;
- additive expansion and targeted-branch isolation;
- correction placement and content;
- exact controlling text and required non-fit structure;
- prohibited output.

In Verbose mode, an ordinary in-scope response must show `At a glance`, `In context`, and `At depth` in that order. At a glance is at most 40 counted words. At a glance plus In context is at most 200 counted words. At depth has no hard cap but must remain purposeful.

In Progressive mode, a new topic starts with `At a glance`. Each unqualified `More` advances exactly one view and returns only additive content. A switch to Verbose applies before a substantive request in the same message.

### Cumulative facts without arbitrary timing

Score each `required_fact_ids` list cumulatively at its stopping point. A fact emitted in an earlier view or response satisfies a later requirement and must not be repeated solely to satisfy the oracle.

The suite does not prescribe arbitrary first appearances. Early emission fails only when it independently violates an explicit reservation, requested view, budget, safety requirement, or additivity rule. Timing is mandatory for:

- indispensable warnings, which appear before the related action or conclusion;
- facts the prompt explicitly reserves for a follow-up;
- corrections, which begin the next relevant response;
- explicit mode and one-off view controls.

For every deeper-view sentence or bullet, identify the new fact, qualification, relationship, consequence, action, evidence item, alternative, or exception. A unit with none is an echo and fails.

### Budgets

Count English prose according to `cases.json.word_count`.

- Count reader-visible prose, cue labels, list text, inline code, and visible link text.
- Exclude headings, Markdown syntax, destination and bare URLs, fenced code, data tables, state notes, citation markers, prompts, and genuine control dialogue.
- Remove Markdown punctuation, split at whitespace, and count each token containing an English letter or digit.
- Count an unspaced contraction, hyphenated compound, compact date, time, number, or code-like token as one word.

In Verbose mode, count At a glance separately against 40 words, then At a glance plus In context against 200 words. In Progressive mode, accumulate all At a glance and In context prose on the active topic across responses. A targeted branch inherits that total. A genuine new topic resets the topic count but preserves sticky mode.

Only indispensable warning words and necessary correction repair words receive their defined exemptions. Record the reason and affected words in evaluation metadata.

### Activation and state

Behavior alone is not proof that the skill loaded or stayed inactive.

- Activation or inactivity is `PASS` only with an exposed host trace matching the case expectation.
- Activation or inactivity is `UNVERIFIED` when the host exposes no such trace.
- Sticky mode, selected view, depth, branch focus, and topic reset are `UNVERIFIED` without an internal-state trace.
- Their rendered consequences remain observable and must be scored `PASS` or `FAIL`.

An `UNVERIFIED` activation or state dimension does not fail otherwise conforming behavior and cannot erase an observable failure.

### Special cases

A focused clarification is uncounted control dialogue only when its sole purpose is gathering missing decision inputs. It must contain no recommendation, rationale, implementation detail, or view heading beyond an indispensable warning.

A targeted branch inherits the active topic count and excludes sibling branches and general recap.

A correction starts the response, identifies and withdraws the emitted error, says it was wrong or incomplete, replaces it, and states the changed consequence or action. Only necessary repair words are exempt; unrelated prose counts normally.

Controlling legal text remains character-exact and separate from a summary labeled with the literal word `Non-controlling`. Narrative voice and sequence, and complete procedural step order and safety branches, take precedence over three-view presentation.

## Result boundary

The suite measures observable protocol behavior, host activation evidence when available, internal-state evidence when available, and safe-stopping completeness through predetermined fact and caveat checks. It does not establish comprehension, task success, reader preference, safety outcomes, or any other human outcome.

## Validation

From the repository root:

```sh
source /Users/firaskafri/Work/code/lms-api/.venv/bin/activate
python -m json.tool evals/cases.json >/dev/null
```

Internal validation must also confirm:

- `schema_version` is `2.0.0`;
- case IDs are exactly `M01` through `M11` and unique;
- all fact IDs are unique and every fact reference resolves within its case,
  including nested stopping points and required step order;
- turn numbers begin at 1 and are sequential;
- repeat case declarations agree with each case's `runs_per_host`;
- the initial totals are 21 sessions and 39 scored responses per host;
- the protocol checksum matches `SPEC.md`; and
- the cases checksum matches the frozen repository-validator input.
