# Publication readiness

This checklist is the source of truth for publishing Progressive Clarity. It
separates repository evidence, vendor review, public catalog availability, and
live behavior so that one state is not mistaken for another.

## Current release

The working tree targets unpublished stable package `0.5.1` for acceptance
repair. It is not approved or published. The release identities and completed
publication checks below refer only to immutable published `0.5.0`; repository
marketplace catalogs remain pinned to that release. Candidate validation and
targeted debugging do not replace vendor review or a full development round.

The [rc.21 full round](release-candidate-rc21.md) cleared 44 separate-model
judgments and its 13-response supplemental Full audit. Behavioral development
acceptance is cleared for the disclosed Azure configuration only. Publication
remains gated: the stable preparation has no current exact-SHA CI, tag,
or remote artifact verification. The workflow now permits only accepted stable `v0.5.1` or RC tags; stable
publication checks the pinned acceptance record. No-overwrite protection,
non-latest initial publication, and exact-SHA CI requirements remain mandatory.
Prior failures and reviewer disagreement remain historical evidence.

Accepted rc.21 and complete public evidence are committed at
`f8f3a200bbcb5dcaf913a443787f13ef68ffa776`. Stable `0.5.1` preserves those skill
bytes and adds a pinned, offline acceptance validator. Local 173 tests, repository
validation, Ruff, official Claude manifest/catalog validation, five artifact
builds, archive integrity/body checks, and isolated wheel installation pass.
Local artifacts are under `/tmp/pc-stable-051-artifacts/`; they are not remote
release assets. Push, exact-SHA CI, immutable tagging, and remote verification
remain required. Approved marketplace pins are unchanged.

rc.14's [complete Azure round](release-candidate-rc14.md) completed but does not
establish acceptance: T06 misses the frozen expected decision and all semantic
results remain unverified in the no-judge report. Prior candidate gates below
are historical; no current candidate commit, CI pass, tag, or publication exists.

rc.13 is a [safety repair](release-candidate-rc13.md); its four-response targeted
round still failed T05 run 1. Stable acceptance remains blocked.
Historical rc.12 is a [scope repair](release-candidate-rc12.md), with one targeted T18 pass
and no full acceptance round.
Historical rc.11 is a [narrow repair](release-candidate-rc11.md). Its authorized two-response
check passed T15's targeted boundary but retained a T18 scope failure.
The rc.10 commit, failed behavior record, and preparation gates below
are historical. The workflow rejects rc.10 tags against current rc.11 metadata;
no current exact-commit CI or publication gate has passed.
The rc.7 full development round completed with 12 PASS and 10 FAIL case runs,
so stable release, website deployment, and vendor submissions are blocked.

rc.10 began as a [local-only repair](release-candidate-rc10.md). Its subsequently
authorized five-response Sonnet round still failed format promises and additivity.
The rc.9 preparation checklist below is historical. Its local bundle
must not be submitted as rc.10, and the current workflow's matching-version
guard rejects an rc.9 tag against rc.10 metadata. No new publication is authorized.

## Experimental rc.10 gates — not ready to publish

- [x] Current installation instructions and experimental notes name rc.10;
  earlier rc.9 artifacts and behavior records are explicitly historical.
- [x] Local repository validation, 172 tests, Ruff, and diff checks pass.
- [x] Release workflow requires the latest main-push CI run for the exact tagged
  SHA to be completed successfully; absent, pending, failed, or stale results block.
- [ ] Review and commit the intended changes; record the exact commit SHA.
- [ ] Push that commit only when authorized and verify CI success for that SHA,
  including package builds and official Claude validation. Local checks are not CI.
- [ ] Build/check rc.10 artifacts from that exact source revision; do not reuse
  the rc.9 bundle or release the current uncommitted working tree.
- [ ] Explicitly authorize creation of immutable `v0.5.1-rc.10` at the verified
  commit and publish it as a prerelease with `--latest=false` using reviewed notes.
- [ ] Verify remote source pin, prerelease/not-latest status, inventory, and checksums.

Stable 0.5.1 remains blocked pending behavioral acceptance. No commit, push,
tag, or publication was performed by this documentation cleanup.

## Historical experimental rc.9 preparation

The user explicitly authorized preparing a disclosed experimental prerelease,
not promoting rc.9 to stable or changing the acceptance rubric. Stable 0.5.1,
vendor submissions, and production website promotion remain blocked. An opt-in
GitHub prerelease was a separate distribution scope. The rc.9 bundle retains its
original notes; [current experimental notes](experimental-prerelease.md) now
describe rc.10 and must not be treated as the historical rc.9 notes.

- [x] Candidate notes disclose T10, T15, T18 and host/semantic limitations.
- [x] Workflow rejects stable/mismatched tags, marks releases prerelease and
  not latest, refuses existing releases, and checks isolated artifacts/checksums.
- [x] Repository checks, diff checks, 170 unit tests, and Ruff 0.12.9 pass locally.
- [x] Claude Code 2.1.274 validates plugin and marketplace manifests.
- [x] Wheel and sdist build and install in separate temporary environments;
  installed protocol/schema imports and console-script help pass.
- [x] Three host archives build twice identically from the current cleaned skill.
- [x] Clean local bundle: `dist/experimental-0.5.1-rc.9/`, with five packages,
  `SHA256SUMS.txt`, release notes, and preparation metadata. Existing root
  `dist/` archives are historical; do not publish them instead of this bundle.
- [ ] Review and commit the intended source changes; the bundle records an
  uncommitted working tree and is not committed-source provenance.
- [ ] Run CI on that exact commit, create immutable `v0.5.1-rc.9` there, and
  explicitly authorize push/publication. No tag, push, or publication was done.
- [ ] Run the experimental workflow and verify remote prerelease/not-latest
  status, notes, inventory, and attached checksums against the actual CI build.

The workflow can be dispatched only for an existing matching RC tag. Never use
an old stable tag, move an existing tag, overwrite release assets, or attach stale
local artifacts. CI-built Python artifacts may differ from local builds; compare
their own checksums and record their source revision rather than claiming byte
identity without checking. No PyPI publication or marketplace pin change is included.

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
- [x] Published website release `20260920T135005Z-49880-3a550689` is healthy,
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
the public directory is delayed. Progress is tracked in
[issue #1](https://github.com/firaskafri/progressive-clarity/issues/1).
Verify both public discovery surfaces:

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
