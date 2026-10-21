# rc.9 instruction-delivery comparison — 2026-10-21

## Frozen diagnostic scope

Unchanged whitespace-cleaned rc.9, skill SHA-256
`a1604c1b188d80afa6afe9b2f7e72270cd8fa121db0578d88a835907219f1ce5`.
T10, T15, and T18 once per condition: six fresh sessions, ten responses.
Original prompts and rubric unchanged. Cursor Agent `2026.10.19-6bbf2c4`,
requested `gpt-5.2`, Ask mode, 240 seconds per response, concurrency three,
no retries or in-round revisions. T10 preserves its session across turns.

- **Startup rule:** exact body in an always-applied project rule.
- **Direct message:** same body prepended to the first user message, followed
  by the original request; no rule or Skill installed. Later turns resume without
  repeating instructions.

Instruction priority and placement both change. This is a diagnostic comparison,
not proof of a rule-injection defect, a hidden-system-prompt test, or controlled
causal attribution. One run per condition is insufficient for reliability claims.

## Observed result

All ten responses completed. Neither condition resolved the three case groups.

| Case | Startup rule | Direct message |
| --- | --- | --- |
| T10 | Continues unsupported expansion/status interpretation. | Initial explanation is more generic, but Beacon turn announces workspace searching despite supplied status; risk follow-up still expands into unsupplied mechanisms. |
| T15 | Long context/risk checklist remains. | Clause/context checklist remains despite directly supplied two-input boundary. |
| T18 | Says budget/availability do not differentiate options, but does not explicitly preserve both supplied successes; adds weather/facility/booking details. | Explicitly preserves both options' budget and availability; still introduces unsupplied facility-route checks. Partial improvement, not a scope-contract pass. |

Facility checks are framed as verification requests, not established facilities.
Their presence is assessed against the requested bounded scope; it must not be
misreported as an assertion that facilities exist. Similarly, generic technical
possibilities and situation-specific claims must be distinguished in semantic
review. These distinctions do not eliminate the checklist and scope failures.

**Conclusion: directly presenting the instructions is not a sufficient fix.**
Observed differences suggest delivery can affect outputs, but do not identify
the root cause. T15's failure in both conditions particularly argues against
treating startup rule loading as the sole explanation.

Stop after this comparison. No instruction change, further inference, full
acceptance round, or release action followed. rc.9 remains unpublished and
acceptance blocked. Do not launch another immediate wording cycle or build a
semantic validator based on these few cases. Any model/host comparison would
need a separate bounded plan and accurate cost/evidence boundaries.

Local evidence: ignored `evals/runs/cursor-delivery-comparison-rc9-2026-10-21/`
contains the pre-run plan, exact delivered prompts, traces, metadata, visible
responses, and observations. This is not an independent public transcript archive.
Repository validation, diff checks, and 168 unit tests remain separate from
behavioral acceptance. No skill bytes, package artifacts, or marketplace pins
were changed by this experiment.
