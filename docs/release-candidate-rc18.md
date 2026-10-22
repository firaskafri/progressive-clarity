# rc.18 sequence and handoff boundary repair

rc.18 states that dates establish sequence, not a handoff window; any handoff
timing must be proposed, never called established. Context should explain a
distinct implication or evidence boundary, not restate order or invent mechanisms.
Complete safety gates remain intact.

Skill SHA-256:
`01507dc4e7ec514ac1cec7b7a87a27f6790880f411aa64d18d94501777ca938a`.

Original cases, specification, disclosed context-v1 expectations, immutable
marketplace pins, and all preceding failures remain unchanged.

## Targeted check

Azure `gpt-6-astra` generated 12 responses in four sessions: T04 three prescribed
runs and T10 once. Deterministic checks passed. A bounded same-model review
returned **12 PASS / 0 FAIL / 0 UNVERIFIED**. This is disclosed self-review,
not independent certification. No retries or in-round instruction changes occurred.

## Frozen full round

The fresh full round completed all 44 responses. Separate Sol review passed
44/44, but the preplanned Astra Full audit returned 11 PASS / 2 FAIL: T03 turn 1
repeated runbook sequence, and T04 run 3 duplicated handoff uncertainty. These
findings block release clearance; prior passes remain unchanged.

Ignored evidence: `evals/runs/azure-rc18-targeted/` and `azure-rc18-full/`.
Token usage is not captured; Azure billing is authoritative for actual charges.

All 172 tests, repository validation, compact-skill comparison, packaging
propagation assertions, Ruff, and whitespace checks passed. The tree is
uncommitted. Stable acceptance and publication remain blocked because the full
audit failed and release gates remain unsatisfied. No push, tag, publication,
vendor submission, or deployment occurred.
