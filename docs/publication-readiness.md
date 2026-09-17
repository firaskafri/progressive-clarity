# Publication readiness

This checklist is the source of truth for publishing Progressive Clarity. It
separates repository evidence, vendor review, public catalog availability, and
live behavior so that one state is not mistaken for another.

## Current candidate

- Protocol: `0.5`
- Package: `0.5.0`
- Approved Claude source revision:
  `f34fbf03ba644f7b86d6c9413504878d4f76762b`
- OpenAI archive SHA-256:
  `c1acd2e17b1b6fd7d9e5c3ea480117770edf2ea921ad5c589d5d2930ee89cf44`
- Claude plugin archive SHA-256:
  `c66f85b81b2c90e71a4d32599fee50bb84064527889e7e6aa7a3e93eb112ecf9`
- Claude.ai Skill archive SHA-256:
  `bc2db57bdeda2e44e193bb53bb8bda20e929205cc9ab606adbd91346b540c377`

## Verified

- [x] Canonical source is public.
- [x] Repository validation and all 167 unit tests pass.
- [x] GitHub Actions passed for the candidate revision.
- [x] OpenAI, Claude plugin, and Claude.ai Skill archives build
  deterministically.
- [x] Claude Code 2.1.274 validates both the plugin manifest and repository
  marketplace without warnings.
- [x] Repository marketplace catalogs for Claude and OpenAI are pinned to the
  approved candidate revision.
- [x] Publication tracking, marketplace catalogs, validation coverage, and the
  release workflow are committed and pushed.
- [x] Immutable tag `v0.5.0` points to the approved candidate revision.
- [x] The GitHub release contains the three deterministic host archives, Python
  distributions, and checksums.
- [x] OpenAI package `0.5.0` is published in the Plugins Directory.
- [x] The website serves the candidate archives and manifests.
- [x] The public privacy and terms pages are deployed and pass exact-route
  smoke checks in website release `20260917T120102Z-13926-f8b646ae`.
- [x] Claude Console records the plugin as `passed_review`.
- [x] The approved Claude submission targets the exact candidate revision.
- [x] Claude approved the plugin for Claude Code and Cowork.

The authenticated Claude Console state above was checked on 2026-09-17. Do not
store Console account identifiers, credentials, or private contact information
in this repository.

## Remaining blockers

- [ ] Confirm Progressive Clarity appears in Anthropic's public
  `claude-plugins-community` catalog and record the catalog-pinned revision.
  Review has passed, but the public mirror has not synchronized yet.
- [ ] After the source tag exists, rebuild the website artifacts from that tag
  and change the website ledger from `unpublished` to `published` with the full
  source revision and release date.
- [ ] Deploy the published-provenance website artifact and verify every public
  archive against its recorded SHA-256.

Professional name and trademark clearance for “Progressive Clarity” remains a
documented legal-risk decision. It is not represented as completed by package
validation or vendor review.

## Evidence gaps that do not block packaging

- Current v0.5 live ChatGPT and Claude behavior has not been recorded against
  the exact candidate bytes.
- Public directory installability is unverified until each catalog entry is
  visible and can be installed.
- Prompt-only activation and semantic conformance remain probabilistic even
  after a vendor approves the package.

These gaps must remain explicit in release notes and support claims. They do
not invalidate the deterministic package or the completed Claude review.

## Release order

1. Do not modify the approved `0.5.0` package inputs.
2. Tag the approved candidate revision as `v0.5.0`.
3. Run the release workflow and verify its attached checksums.
4. Verify the Claude public catalog pin after synchronization.
5. Verify or complete the OpenAI `0.5.0` review.
6. Rebuild the website artifacts from `v0.5.0` with published provenance.
7. Deploy and verify the website.

If any package input must change, do not overwrite `0.5.0`; advance the package
version and repeat review.
