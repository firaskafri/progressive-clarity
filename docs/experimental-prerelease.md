# Progressive Clarity 0.5.1-rc.21 — experimental prerelease

**Package `0.5.1-rc.21` is for opt-in experimentation, not a stable or verified
behavioral release. Stable 0.5.1 publication remains gated.** The approved
0.5.0 marketplace pins are unchanged. This candidate is not vendor-approved.

## Changes

Current [rc.21 evidence](release-candidate-rc21.md) records 44 separate-model
passes and 13 supplemental Full-audit passes in a fresh Azure context-v1 round.
This clears the tested development behavioral gate, not stable publication,
live-host conformance, unseen generalization, or universal model compatibility.
Prior failures and reviewer disagreements remain historical evidence.

The candidate clarifies numeric uncertainty, per-turn presentation, explicit
correction, literal source labels, and response scope. These are instruction
changes, not proven improvements. Protocol 0.5 and wrapper schemas are unchanged.

## Historical failures and untested repairs — read before trying

These failures were observed in preceding candidates, not in a live rc.10 run.
rc.11's clarification and automatic-Full selection changes are locally validated only.
The following limitations remain release risks, not verified fixes.

- **T10:** may infer database/migration context, add unsupported implications to
  supplied project status, and recap instead of answering a narrow follow-up.
- **T15:** may expand a request for agreement text and decision criteria into an
  unsolicited legal/context checklist.
- **T18:** may omit shared budget/date facts and add unsupplied facilities,
  booking, timing, pricing, or contract considerations.
- Prompt-only instructions cannot guarantee activation, accuracy, scope, or
  warning placement. Cursor's explicit Skill-load path has emitted commentary
  before safety warnings. A project-rule path produced bounded opening passes,
  but failed broader development checks. Direct instruction delivery did not
  resolve the remaining failures.

Do not rely on this candidate as a safety, legal, financial, or operational
approval mechanism. Review the entire response against the original facts and
controlling requirements. Formatting and mechanical validation do not prove
semantic correctness. Reader benefits and other hosts' current behavior are
unverified. This candidate does not weaken the acceptance rubric or bypass release gates.

## Artifacts and use

When explicitly published, three host ZIPs, a Python wheel, and an sdist must
accompany `SHA256SUMS.txt`. No 0.5.1-rc.21 release assets have been published yet.
Python filenames normalize `0.5.1-rc.21` to `0.5.1rc21`; they identify the same
prerelease. Download only the artifact for the intended profile and verify its
checksum before installation. Use a temporary/test project and begin a fresh
host session; do not replace production policy or unrelated configuration.

For a manual prompt-only install, extract the complete
`skills/progressive-clarity/` directory from a plugin ZIP to the host's supported
project skill folder, or upload the Claude.ai custom-Skill ZIP through the host's
supported UI. The optional Python wrapper is a separate executable local profile
requiring Python 3.11+, and checks mechanics, not semantic quality.

See [installation](installation.md), [limitations](limitations.md), and the
optional [Cursor project-rule profile](cursor-startup-rule.md). Installing from
the existing repository marketplaces still installs approved **0.5.0**, not rc.18.
Manual copies do not auto-update. Remove only the installed candidate directory
or generated rule to uninstall; preserve other skills and rules.

## Evidence and feedback

The [two-response rc.11 check](sonnet-targeted-rc11.md) passed the T15 boundary
and T18 Focused/fact checks, but T18 still exceeded scope. No full acceptance
pass exists. The rc.10 failed round remains historical.
rc.12's [single T18 check](sonnet-t18-rc12.md) passed; no full acceptance round
has passed. The rc.11 capture is historical.
The [rc.12 full Azure round](azure-full-rc12.md) failed T05 run 2 and T12 safety
checks. The [rc.13 safety round](azure-safety-rc13.md) still failed T05 run 1's
restart condition; no full acceptance pass is established.
Current canonical skill SHA-256:
`3d329872cbad63d985506786603d318637aedf7d8eee78de5e78d85d73c0f5dc`.
Repository tests, archive validation, and checksums establish mechanical
integrity only. Local capture files are not a public independently adjudicated
study. See [rc.9 results](release-candidate-rc9.md) and
[delivery comparison](instruction-delivery-comparison.md).

Report issues at <https://github.com/firaskafri/progressive-clarity/issues> with
candidate version, host/model, prompt, expected behavior, and a redacted response.
Do not post private agreements, credentials, personal data, or sensitive logs.
The prompt-only packages contain no runtime, remote service, authentication,
analytics, or data collection. The host processes conversations under its own
terms. Licensing remains Apache-2.0 for tooling/skills and CC BY 4.0 for protocol
and documentation; see [licensing](../LICENSE.md).
