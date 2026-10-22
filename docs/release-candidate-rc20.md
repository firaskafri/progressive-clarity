# rc.20 bounded composition repair

For a lone safety prerequisite, distinguish necessary from sufficient instead of repeating order.
Redundant prose was shortened to preserve the compact-skill limit.

Skill SHA-256:
`8d3aba65754227dde0fed42eaf8fa9d32ae521bfa7be85d0def36dd8828cf00d`.

## Frozen results

- `azure-rc20-targeted`: COMPLETE, 5 sessions, 15 responses; deterministic {'PASS': 15}.
  - `bounded-review`: {'PASS': 15}; no timeout or retry.
- `azure-rc20-full`: COMPLETE, 22 sessions, 44 responses; deterministic {'PASS': 44}.
  - `bounded-review`: {'PASS': 44}; no timeout or retry.
  - `full-audit`: {'PASS': 12, 'FAIL': 1}; no timeout or retry.
    - T02-r1-t2.review.json: full_progressive_depth, full_repetition_usefulness

The targeted or supplemental review retains a failure; no acceptance clearance follows.
Original cases, specification, context-v1 expectations, marketplace pins, and
historical failures remain unchanged. Raw no-judge reports remain UNVERIFIED;
review results are separate model judgments, not human certification. Astra
review of its own outputs is disclosed self-review, not independent evidence.

All review processes use SDK timeout 60 seconds, process timeout 90 seconds,
concurrency two, no retries or regeneration. Ignored captures remain under the
listed run directories. Token usage is not retained; actual charges require Azure
billing. All 172 tests and repository validation passed; compactness and package
propagation assertions remain enforced. The source is uncommitted; no push, tag,
publication, vendor submission, or deployment occurred.
