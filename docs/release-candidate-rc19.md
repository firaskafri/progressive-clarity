# rc.19 bounded composition repair

Put executable steps in one view and delete duplicated context information.
Redundant prose was shortened to preserve the compact-skill limit.

Skill SHA-256:
`cd219ac6da494498203fc6442530b639e50a53a3eacc5a34127d59123f2b63e7`.

## Frozen results

- `azure-rc19-targeted`: COMPLETE, 5 sessions, 15 responses; deterministic {'PASS': 15}.
  - `bounded-review`: {'PASS': 14, 'FAIL': 1}; no timeout or retry.
    - T10-r1-t1.review.json: full_progressive_depth, full_repetition_usefulness

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
