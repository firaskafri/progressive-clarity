# rc.14 disclosed context-suite review

The user authorized continued work using the supplied Azure deployments or
Grok 4.7. No repeated approval was requested for this diagnostic sequence.

The original rc.14 suite failed its T06 expected decision. That result is retained.
A separate `evals/release-acceptance-context-v1.json` identifies the database index
and declares the authorization prerequisites exhaustive. Only T06's title and
two prompts changed; every original expected result and rubric is unchanged.
This is a disclosed context correction, not a retroactive pass or unseen holdout.

On unchanged rc.14 and `gpt-5.6-sol`, all 44 responses in 22 fresh runs completed.
The separate D03 ambiguity control asks which index is meant and also completed,
showing that the contextualized enablement case does not remove ambiguity handling.
No SDK retries or in-round instruction changes were made.

## Separate model review

Existing outputs were reviewed using the supplied `gpt-6-astra` deployment and
the harness's original criterion-generation and validated judge-result contracts.
No generation answers were rerun or replaced. Review scope: 44 calls, no retries;
one failed criterion makes that reviewed response FAIL. This different-model
review is a regression proxy, not independent human or safety certification.

Review completed: **37 PASS / 7 FAIL / 0 UNVERIFIED responses**.
Failures: T03 turns 1 and 3; T04 material-correction turns in all three runs;
T05 runs 1 and 3. Findings principally concern repetitive Full composition and
insufficient new information in deeper views. T06's clarified-context answers,
T10, T12, T15, T17, and T18 passed the listed reviewer criteria in this capture.

The original no-judge reports remain UNVERIFIED; reviewer findings are separate
files, not silently substituted outcomes. The full reviewer evidence, including
quoted failure passages, is retained locally. No stable acceptance pass exists:
correct facts and safety gates do not automatically satisfy additive composition.

## Work and publication boundary

This continuation made 45 generation responses (44-suite plus one ambiguity
control) and 44 reviewer responses. Costs/tokens are not captured by the current
harness and must be checked in Azure billing. Do not treat open-ended approval
as justification for unbounded retry/tuning expenditure.

No additional skill revision, stable-version relabeling, tag, push, deployment,
or publication occurred. Release remains blocked by seven reviewed failures.
Any next composition repair must address those quoted passages, preserve the
original safety contracts, and use a finite frozen plan rather than repeat runs
until a model returns a favorable judgment.

Local evidence: ignored `evals/runs/azure-rc14-context-v1-full/` (generation plan,
report, review plan, 44 criterion reports) and
`evals/runs/azure-rc14-ambiguity-control.json`. Original suite and rc.14 bytes are
unchanged. The new suite is committed only when separately reviewed with the
source changes; current work is not published-source provenance.
