# Direct Azure GPT-5.6 Sol diagnostic — rc.12

The user requested preparation and execution through an existing custom Azure
deployment. Read-only Azure management discovery found one `gpt-5.6-sol`
deployment in Sweden Central, provisioning state `Succeeded`, model version
`2026-07-09`. No Azure deployment, quota, or account setting was changed.

The resource endpoint/key were resolved through the authenticated Azure CLI.
Credentials are stored only in ignored `evals/azure.local.json`, mode 0600;
they were not displayed or committed. An isolated temporary evaluation environment
uses Agno 2.9.0, OpenAI SDK 3.36.1, and SQLAlchemy with its asyncio extra.
No runtime dependency was added to the project package.

## Frozen bounded run

Original T10, T15, T18: three fresh sessions / five responses, unchanged rc.12,
condition `revised`, no judge calls, zero SDK/agent retries, 180-second timeout,
maximum 5,000 completion tokens per response. The existing Azure harness injects
the exact skill body as system instructions and preserves case history. API
version `2024-10-21` successfully served this bounded run; this does not establish
compatibility for other deployments. Skill SHA-256:
`be6a11809c702bfa810ba2dfc22e857f6c8ef25234b51032b22dc8c47e036eba`.

## Observed outcome

All five responses completed in three runs. The report is `COMPLETE` with
overall `UNVERIFIED`, correctly reflecting disabled semantic judging. No
mechanical failures were reported. Visible evaluator review found:

- **T10 named scope checks passed:** no database/product assumption; Beacon
  answered as discovery only; the risk follow-up remains Focused. Initial Full
  explanation uses generic dependency, sequencing, and verification requirements.
  Additivity of the overlapping gate language still needs independent review;
  no whole-case semantic certification is claimed.
- **T15 targeted PASS:** only requests agreement and decision criteria, without
  checklist, format promise, or sign/decline recommendation.
- **T18 targeted PASS:** Focused hall recommendation from supplied requirements;
  both venues' shared budget/date facts retained; written checks verify access,
  fallback, budget, and event-date availability only. No cancellation conditions,
  facilities catalogue, or approval process is added.

This is promising direct-API evidence, not stable acceptance. It does not verify
Cursor, Claude, ChatGPT package installation, or dynamic Skill activation. The
host/SDK/system-message path differs from Cursor, so improvements cannot be
attributed solely to model identity. Prompts are known development material.

Stop after this run: no retry, judge run, other deployment, full suite, instruction
revision, push, tag, or publication followed. A separately authorized full round
and independent semantic review remain required for a stable compatibility claim.

## Evidence and cost boundary

### Subsequent local semantic review — no new inference

T15's compact two-input request and T18's supplied-fact decision/verification
remain targeted passes under evaluator review. No overall acceptance claim follows.

T10 additivity remains **UNVERIFIED pending independent adjudication**:

- At a glance already states reconciliation before rollback and the unsafe
  incompletely understood/aligned state.
- In context adds an explicit verification step, but its three-step sequence
  and “rollback safety depends on the outcome of reconciliation” mostly restate
  the opening dependency. Whether verification supplies enough new decision
  content to make this view predominantly new is not settled by correct headings.
- At depth does add completion criteria, retained evidence, and a stop condition
  when reconciliation cannot be completed/verified. Repeated gate qualifications
  keep those proposed workflow actions safe and are not automatically redundant.

An independent reviewer should apply SPEC.md section 4 to these passages, rather
than mark all repetition a failure or treat a correct safety gate as an automatic
additivity pass. Do not launch a full paid round on the premise that all targeted
requirements have passed. No raw output or harness result was changed, and no
additional calls, skill changes, or release actions occurred during this review.

### User adjudication of the disputed additivity check

After reviewing the opening, middle-view sequence, and deeper verification
content, the user judged **T10 In-context additivity PASS**, stating that the
explicit verification step and sequence provide sufficient new decision guidance.
This is a user review distinct from the assistant's earlier unresolved judgment;
it is not a blinded study or independent certification of all response claims.

The disputed targeted additivity check is therefore adjudicated PASS for this
capture. T15 and T18 retain their named evaluator passes. The raw no-judge report
remains `UNVERIFIED` and is not rewritten. No full-suite result, cross-host
support, generalization, or stable release clearance follows from this decision.
A fresh full development round on unchanged rc.12 and `gpt-5.6-sol` is now the
next proposed gate and requires separate paid authorization.

The user subsequently authorized that [full round](azure-full-rc12.md). All 44
responses completed, but review found T05 run 2 restart-condition weakening and
T12 warning omissions. Stable acceptance remains blocked; targeted passes above
do not replace those complete-round findings.

Ignored `evals/runs/azure-gpt56-sol-rc12/` contains the pre-run plan and raw-response
report with instruction/suite identities. The current harness does not record
token metrics from generation outputs; actual usage/cost is therefore unknown
and must be checked in Azure billing. No inference-usage total is invented.
The endpoint host is report metadata; API credentials are excluded.
