# rc.9 second-model diagnostic — 2026-10-21

Unchanged rc.9, skill SHA-256
`a1604c1b188d80afa6afe9b2f7e72270cd8fa121db0578d88a835907219f1ce5`.
Original T10, T15, T18 prompts and rubric; each case once per model, six fresh
sessions and ten responses. Both conditions use the same always-applied rule
body in isolated workspaces, with no invocation prefix. Cursor Agent
`2026.10.19-6bbf2c4`, Ask mode, 240 seconds per response, concurrency three,
no retries or in-round revisions. Requested models:
`gpt-5.2` and `claude-sonnet-5-5-medium`.

## Observations

The subsequent [scoring review](sonnet-scoring-review.md) separates candidate
silent-application failure from T15's passing frozen-case checks. T18's written
verification requests are not invented facilities, but repetitive In-context
content fails additivity under conservative evaluator review. Named improvements
below are not whole-case passes or a basis for immediate stable clearance.

All ten responses completed. This one-run comparison measures observable
differences, not model reliability, independent adjudication, or causality.
Host-reported model labels are retained per response; hidden settings are unknown.

| Check | GPT-5.2 | Claude Sonnet 5.5 Medium |
| --- | --- | --- |
| T10 evidence-bound topic/follow-up | FAIL: adds unsupported technical mechanisms and metrics; narrow follow-up uses Full. | Named scope check PASS: does not identify Atlas as a product, answers Beacon from supplied status, and keeps risk follow-up Focused without invented technical facts. |
| T15 two-input clarification | FAIL: lengthy clause/context checklist. | Named checklist check PASS: requests agreement and decision criteria only; no clause/risk catalogue. However, narrates skipping the format, so silent application fails. |
| T18 supplied comparison facts | FAIL: supplied shared facts are incompletely retained; introduces contract/payment detail and weather consequences. | Named fact-preservation check PASS: explicitly retains access, fallback, budget, and event-date availability; no invented venue advantage. Additional written booking/access confirmation detail still requires scope/proportionality review. |

Sonnet's T18 verification requests do not assert the existence of unsupplied
facilities. The request itself asks for evidence before booking, so verifying
access, budget, availability, and fallback is relevant. Whether its route and
booking terms are proportionate under the strict scope contract remains
UNVERIFIED, not automatically a pass or fabricated fact.

**Decision: model selection is a promising diagnostic direction, not a stable
release clearance.** Sonnet avoided the three recurring core patterns in this
capture, but silent application and full T18 scope are not cleanly established.
No full-suite acceptance or compatibility with Claude Code/Claude.ai is claimed;
Sonnet was accessed through Cursor. Previous failures remain documented.

Stop after the comparison. No instruction edits, further inference, tags, vendor
submissions, deployment, or publication followed. A separately frozen full
development round on the selected Sonnet configuration is the next justified
evaluation, with explicit review of commentary and bounded evidence requests.
Stable publication requires passing the agreed contract, not selecting only the
successful checks from this comparison. Fresh independent cases remain necessary
before broader generalization claims.

Local evidence: ignored `evals/runs/cursor-model-comparison-rc9-2026-10-21/`
contains the pre-run plan, original prompts, raw traces, metadata, visible
responses, and per-response observations/hashes. This is not a public independent
transcript archive. Source bytes, prerelease artifacts, marketplace pins, and
release safeguards remain unchanged.
