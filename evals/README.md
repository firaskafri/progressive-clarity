# Progressive Clarity v0.2 Advisory host acceptance

`cases.json` scores rendered prompt-only behavior in Cursor and Claude Code.
This surface is **Advisory**. No current v0.2 host run exists; suite status is
`UNVERIFIED`.

Historical results for older behavior remain in `docs/verification.md` and must
not be combined with this suite.

## Active cases

- `E01`: ordinary three-view decision and qualified evidence.
- `E02`: targeted follow-up that still renders all three views.
- `E03`: explicit correction with three-view continuity.
- `E04`: indispensable safety warning.
- `E05`: clarification control dialogue, then a complete response.
- `E06`: exact controlling text and non-controlling summary.
- `E07`: narrative non-fit.
- `E08`: sequential procedure non-fit.

## Separate local mechanical surface

`tests/` exercises schema `2.0.0`, protocol `0.2`, mandatory section order,
deterministic English counts, fact-ID allocation/reuse, correction/quotation
structure, lexical duplicate signals, canonical rendering, atomic state, and
the two-total-attempt wrapper.

A `pc-core` pass does not pass this semantic suite. It cannot establish
accuracy, completeness, warning indispensability, human safe stopping,
paraphrased repetition, purposeful depth, or hidden-reversal safety.

## Run policy

Run each case in a fresh session and preserve one session for all turns in that
case. Run `E03`, `E04`, and `E06` three total times per host. This is 14
sessions and 19 scored responses per host.

Every prescribed run must pass. There is no majority vote or intermittent
failure allowance. Permit at most one reviewed remediation cycle:

1. complete the full initial round;
2. review failures;
3. revise once;
4. rerun only failed cases with every prescribed repetition; and
5. stop regardless of outcome.

Do not weaken safety, correction, exact-text, user constraints, or procedure
conditions to obtain a pass.

## Scoring

Use `PASS`, `FAIL`, or `UNVERIFIED`.

For an ordinary in-scope response, require:

- At a glance, In context, and At depth exactly once and in order;
- at most 40 non-warning words in At a glance;
- at most 200 non-warning words through In context in that response;
- purposeful At depth;
- every required material boundary and caveat at the applicable stopping point;
  and
- no fact-only repetition across views.

Targeted follow-ups use the same three headings but exclude sibling branches
and general recap. Pure clarification has no headings or hidden substantive
answer. Correction repair is first under At a glance and still retains all
three views. Controlling text, narrative voice, exact output, and complete
procedure order take precedence over the three-view form.

Activation requires an exposed host trace. Similar output is not activation
evidence, and a trace does not prove behavioral conformance.

## Word count

Human scoring must use the exact ordered algorithm in `SPEC.md` and
`cases.json.word_count`, matching `pc-core`.

Count reader-visible prose, labels, list text, inline code content, and visible
link text. Exclude headings, Markdown syntax, destination and bare URLs, fenced
code, data tables, state notes, citation markers, prompts, and pure
clarification dialogue.

Only indispensable warning words and necessary correction repair words receive
their defined exemptions. Record each exception and affected word span.

## Validation

From the repository root:

```sh
python3.11 -m json.tool evals/cases.json >/dev/null
python3.11 -m tools.validate_repository
```

Repository validation checks schema/suite identity, case/fact references,
sequential turns, repetitions, totals, protocol hash, frozen input hashes, and
the explicit Advisory/Enforced boundary.
