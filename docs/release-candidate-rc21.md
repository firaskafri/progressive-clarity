# rc.21 bounded composition repair

For a failed release gate, explain evidence validity against the corrected candidate rather than restating the block.
Redundant prose was shortened to preserve the compact-skill limit.

Skill SHA-256:
`3d329872cbad63d985506786603d318637aedf7d8eee78de5e78d85d73c0f5dc`.

## Frozen results

- Targeted T02: two responses, both deterministic and bounded Astra judgments PASS.
- Fresh context-v1 full round: 22 sessions / 44 responses, all deterministic PASS.
- Separate Azure `gpt-5.6-sol` review: **44 PASS / 0 FAIL / 0 UNVERIFIED**.
- Preplanned Azure `gpt-6-astra` supplemental Full audit: **13 PASS / 0 FAIL /
  0 UNVERIFIED**. This is disclosed same-model self-review, not independent certification.

The behavioral development gate is cleared for Azure `gpt-6-astra` with system-body
injection and the disclosed context-v1 suite. It does not establish unseen
holdout performance, reader benefit, plugin activation, other-model compatibility,
or vendor approval. Original T06 failures remain historical and unchanged.

Full generation report SHA-256:
`9ea69fbdffc2469dcdba61915bfb1b5e32a42c0d59deeb3d8938c40ee9cccbf8`.
Injected skill body SHA-256:
`7b9cea52c52d98a61eac0d8e32f8922d795e119b065a53e7ce70372b29960623`.
Suite SHA-256:
`0570c94c791d6c12d802c53a8b0dc7a8c211f90af8da515259f4b2a89c632dba`.
Ignored captures: `evals/runs/azure-rc21-targeted/` and `azure-rc21-full/`.
Both completed review tracks have separate hash inventories and summaries;
no original output or judgment was replaced. No review timeout occurred.

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

## Release boundary

Five local artifacts build successfully under `/tmp/pc-rc21-artifacts/`; all
three ZIP bodies match the canonical skill and archive integrity checks pass.
Local SHA256SUMS are retained there. These are uncommitted validation builds,
not published assets or exact-SHA CI evidence.

Stable publication remains unavailable through the unchanged RC-only workflow.
Before release: review and commit intended changes, obtain authorized push,
verify latest main-push CI on that exact SHA, deliberately review stable version
and workflow changes, create an immutable authorized tag, and verify remote
artifact inventory and checksums. No local pass bypasses those gates.
