# Local safety-content repair — 0.5.1-rc.13

rc.13 follows the [rc.12 full Azure round](azure-full-rc12.md), which completed
44 responses but failed two safety checks. Stable acceptance remains blocked.
No paid inference or publication is part of this local repair.

The user later authorized a [four-response Azure safety check](azure-safety-rc13.md).
T12 and T05 runs 2/3 passed their targeted checks, but T05 run 1 still weakened
the restart condition. Stable remains blocked; no full round or retry followed.

Changes:
- Preserve the prohibited action, supplied hazardous state, concrete harm,
  containment, and resume conditions together beside the decision. Containment
  alone cannot replace the hazard/harm content.
- Keep every supplied prerequisite attached to later action conditions. Freezing
  writes and preserving evidence cannot authorize restart when authority,
  reconciliation, fencing, and validated recovery are also required.

Overlapping prose was shortened to retain the compact-instruction test. Original
SPEC.md, development cases, prior outputs, marketplace pins, and existing archives
are unchanged. Package/manifests target unpublished `0.5.1-rc.13`; skill SHA-256:
`051cd1d8cb35756c8df407a1773ad379ab28e2d291cb408dea6c81bd8a178b58`.

Local repository and diff checks, 172 tests, and Ruff pass. Packaging assertions
verify both safety instructions reach every distribution, not that a model obeys
them. No behavioral pass is claimed; rc.13 is local and uncommitted.

Next test, only after separate authorization: T05 all three repetitions and T12
once, four fresh sessions / four responses on the same direct Azure deployment,
no retries or judge calls, report outcomes and stop. Any failed requirement stops
progression to a new full round. Targeted passes alone do not clear stable release.
