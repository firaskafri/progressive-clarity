# Progressive Clarity 0.5.1-rc.10 — experimental prerelease

**Package `0.5.1-rc.10` is for opt-in experimentation, not a stable or verified
behavioral release. Stable 0.5.1 acceptance remains blocked.** The approved
0.5.0 marketplace pins are unchanged. This candidate is not vendor-approved.

## Changes

The candidate clarifies numeric uncertainty, per-turn presentation, explicit
correction, literal source labels, and response scope. These are instruction
changes, not proven improvements. Protocol 0.5 and wrapper schemas are unchanged.

## Historical failures and untested repairs — read before trying

These failures were observed in preceding candidates, not in a live rc.10 run.
rc.10's format-narration and additivity changes are mechanically validated only.
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
unverified. This release does not weaken or satisfy the stable acceptance rubric.

## Artifacts and use

When explicitly published, three host ZIPs, a Python wheel, and an sdist must
accompany `SHA256SUMS.txt`. No rc.10 release assets have been published yet.
Python filenames normalize `0.5.1-rc.10` to `0.5.1rc10`; they identify the same
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
the existing repository marketplaces still installs approved **0.5.0**, not rc.10.
Manual copies do not auto-update. Remove only the installed candidate directory
or generated rule to uninstall; preserve other skills and rules.

## Evidence and feedback

This rc.10 body has not been run against a live model. Earlier candidate failures
remain historical, not rc.10 outcomes. Current canonical skill SHA-256:
`0a05293fae8741d2885ae131b0055dadb268c7ba955f018e21c28193f1ea03e4`.
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
