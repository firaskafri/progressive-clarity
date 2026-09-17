# Publication readiness

This checklist is the source of truth for publishing Progressive Clarity. It
separates repository evidence, vendor review, public catalog availability, and
live behavior so that one state is not mistaken for another.

## Current release

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
- [x] An isolated Claude Code install from
  `firaskafri/progressive-clarity` resolves
  `progressive-clarity@firas-kafri-plugins` as version `0.5.0`.
- [x] An isolated Codex 0.154.0 install from the repository marketplace
  resolves `progressive-clarity@progressive-clarity` as version `0.5.0` pinned
  to tag `v0.5.0` and the approved source revision.
- [x] Publication tracking, marketplace catalogs, validation coverage, and the
  release workflow are committed and pushed.
- [x] Immutable tag `v0.5.0` points to the approved candidate revision.
- [x] The GitHub release contains the three deterministic host archives, Python
  distributions, and checksums.
- [x] OpenAI package `0.5.0` is publicly visible in the
  [Plugins Directory](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2)
  with the reviewed listing copy, prompts, website, privacy, and terms links.
- [x] The website release ledger records tag `v0.5.0`, the approved full source
  revision, and release date `2026-09-17`.
- [x] Published website release `20260917T130223Z-9953-91e4ddf4` is healthy,
  drift-free, and serves metadata identical to the committed ledger.
- [x] The public privacy and terms pages are deployed and pass exact-route
  smoke checks.
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

Professional name and trademark clearance for “Progressive Clarity” remains a
documented legal-risk decision. It is not represented as completed by package
validation or vendor review.

## Anthropic catalog synchronization

The Claude Console submission is complete; do not resubmit it merely because
the public directory is delayed. Verify both public discovery surfaces:

```sh
gh api repos/anthropics/claude-plugins-community/contents/.claude-plugin/marketplace.json \
  --jq .content \
  | base64 --decode \
  | jq '.plugins[] | select(
      .name == "progressive-clarity"
      or (.source.repo? == "firaskafri/progressive-clarity")
    )'
```

Also check <https://claude.com/plugins/progressive-clarity>. Once either source
lists the plugin, record its public URL and pinned source revision here, then
verify installation from the official marketplace.

If the entry remains absent for seven days after the latest `passed_review`
update, contact Anthropic support with the plugin name, public repository,
review date, and submission identifier. Keep the submission identifier and
account details private rather than posting them in a public issue.

The self-hosted marketplace remains an available distribution path during the
sync delay:

```sh
claude plugin marketplace add firaskafri/progressive-clarity
claude plugin install progressive-clarity@firas-kafri-plugins
```

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
