# rc.16 composition boundary repair

The authorized continuation narrowed Full guidance: end after the last useful
check, keep complete safety gates beside later permissions, and distinguish
proposed arrangements from supplied requirements. Specification, original cases,
context-v1 expectations, marketplace pins, and historical evidence are unchanged.

Skill SHA-256:
`0d41b5c9ce725f58c74e09a3959e71bffb04c36fbecf45ae7f3f21c3aba111e6`.

## Frozen rounds and results

| Generator | Scope | Separate reviewer | Response judgments |
| --- | --- | --- | --- |
| Azure `gpt-5.6-sol` | T03 once, T04/T05 three times; 7 sessions / 15 responses | `gpt-6-astra` | 11 PASS / 4 FAIL |
| Azure `gpt-6-astra` | Same targeted scope, unchanged candidate | `gpt-5.6-sol` | 15 PASS |
| Azure `gpt-6-astra` | Fresh full context-v1, 22 sessions / 44 responses | `gpt-5.6-sol` | 43 PASS / 1 FAIL |

All deterministic checks passed. The Sol generation retains composition failures
at T03 turn 3, T04 runs 1/3 turn 3, and T05 run 1. The Astra full round retains
T01 turn 4's provider-specific retry-window omission. Model comparison did not
replace prior scores, establish universal compatibility, or authorize release.

Each review used a subprocess with SDK timeout 60 seconds, hard process timeout
90 seconds, concurrency two, and no automatic retries. No review timeouts occurred.
Raw no-judge reports remain UNVERIFIED; separate review summaries record judgments
and hashes without mutating them. Ignored captures are under
`evals/runs/azure-rc16-composition/`, `azure-rc16-astra-composition/`, and
`azure-rc16-astra-full/`. Azure billing remains authoritative for charges; token
usage was not retained. Local tests and validation passed; no commit, push, tag,
publication, vendor submission, or deployment occurred.
