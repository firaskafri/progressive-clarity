# Progressive Clarity 0.5.1

**Package `0.5.1` is prepared, not yet published.** It uses the exact skill bytes
accepted as rc.21. Protocol 0.5 and wrapper schemas are unchanged.

## Changes and evidence

The skill clarifies complete safety qualifications, additive depth, natural
corrections, missing decision inputs, supplied-fact scope, and provider-specific
retry windows. The [rc.21 development round](release-candidate-rc21.md) generated
44 responses in 22 Azure `gpt-6-astra` sessions. All deterministic checks and
separate `gpt-5.6-sol` judgments passed; the preplanned 13-response Astra Full
audit also passed. That supplemental audit is same-model self-review.

The credential-free [acceptance record](../evals/release-acceptance-0.5.1.json)
retains every response and judgment. Its validator pins the record and source
hashes and checks complete coverage without further inference. Original T06
failures and all historical candidate findings remain unchanged.

## Boundaries

Acceptance covers a public development suite with Azure system-body injection.
It is not an unseen holdout, reader study, host activation test, universal model
compatibility claim, or vendor certification. Earlier T10, T15, and T18 failures
remain historical risks; prompt-only guidance cannot guarantee accuracy or safety.
Review complete responses against supplied facts and controlling requirements.

Approved repository marketplace pins remain on 0.5.0. This package is not newly
vendor-approved and does not update those catalogs, the website, or submissions.
The optional Python wrapper validates mechanics, not semantic correctness.

## Publication

No 0.5.1 release assets have been published yet. Publication requires successful
latest main-push CI for the exact tagged commit, immutable tag verification,
five artifacts plus SHA256SUMS, and refusal to overwrite an existing release.
Initial publication is explicitly non-latest. Verify remote inventory and
checksums before installation; local build checks are not remote verification.

Licensing remains Apache-2.0 for tooling/skills and CC BY 4.0 for protocol/docs.
No runtime service, authentication, analytics, or data collection is added.
