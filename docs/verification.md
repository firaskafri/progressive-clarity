# Verification record

## Current v0.4 status

Progressive Clarity protocol `0.4` and coordinated package target `0.4.3` form
a **locally verified release candidate**.

**No v0.4 live ChatGPT, Cursor, or Claude acceptance run exists. Its host
behavior is UNVERIFIED.**

No current `0.4.3` result establishes prompt-only activation, topic inference,
return to an earlier topic, Focused/Full selection, rendered conformance, host
compatibility, or support. No `0.4.3` external upload, submission, review,
approval, publication, or catalog installation is claimed.

Package `0.4.0` is superseded and must not be distributed. Late source
hardening produced different local bytes after an earlier `0.4.0` download set
had already been generated, so the finalized bytes use package version `0.4.1`
to preserve versioned-artifact immutability.
The Azure initial round then justified a compatible guidance and evaluator
patch. Those changed bytes use package `0.4.2`; the `0.4.1` artifacts and
evidence remain immutable.
After the bounded 0.4.2 round remained below strict acceptance, the maintainer
explicitly authorized controlled continuation to a 0.4.3 candidate until every
prescribed Azure run passes.

### Result labels for v0.4

- **PASS** means direct evidence establishes only the named check against the
  named frozen v0.4 revision.
- **FAIL** means observable output violates a requirement of that frozen
  revision.
- **UNVERIFIED** means available evidence cannot establish the claim. It is
  neither a pass nor a failure.
- **HISTORICAL/SUPERSEDED** means the result belongs to an earlier contract and
  must not be used as v0.4 evidence.
- **MECHANICALLY_CERTIFIED** means the non-streaming local wrapper validated a
  trusted request, committed schema `3.0.0` state, resolved presentation,
  schema `3.0.0` envelope, and canonical rendering. It is not semantic `PASS`
  or host-wide acceptance.

A package build, file copy, manifest check, skill discovery trace, explicit
skill load, or structural test does not establish rendered host behavior.
Similar output without a host trace does not establish activation or topic
state.

## Implemented v0.4 surfaces

### Advisory conversational profile

The canonical skill is prompt-only. It applies the visible-conversation topic
heuristic and uses:

- Focused output for simple facts, ordinary and narrow follow-ups, later
  non-checkpoint exploration, and narrow corrections; and
- Full output for the first substantial topic overview, decision checkpoint,
  summary checkpoint, material re-synthesis, and material correction.

Purpose-specific structures and explicit presentation requests resolve before
automatic cadence. Focused output is heading-free by default and has no
protocol 40/200 budget. Full output uses At a glance, In context, and At depth
in order with the English 40/200 budgets. Every deeper view must be dominated
by new information; necessary short anchors may recur, while complete earlier
conclusions, sentences, lists, explanations, warnings, and recommendations may
not be restated. At depth cannot end in a recap.

This implementation does not make Advisory activation or behavior
deterministic.

### Local mechanical profile

The current local source declares:

- protocol version `0.4`;
- wrapper request schema `3.0.0`;
- response envelope schema `3.0.0`; and
- conversation-state schema `3.0.0`.

`WrapperRequest` carries `topic_action` (`start`, `continue`, or `resume`),
`turn_kind`, and `presentation_request`. Policy resolves the expected response
kind before host invocation. The envelope response kinds are `focused`,
`views`, `control`, `quotation`, and `non_fit`.

`ConversationState` stores the active topic plus per-topic branch, facts, host
sessions, and `has_committed_overview`. `StoredFact` stores exact text and first
turn; presentation placement is response-local. A fact previously used in
Focused prose may later be allocated to the appropriate Full view.

Requestless validation is non-certifying. Requestless rendering is refused and
writes no candidate Markdown. Earlier protocol state, including v0.3 state
with schema `3.0.0`, is unsupported; v0.4 requires a fresh state path.

Project hooks remain **Advisory/block-and-retry**. Heading-free output is
nonblocking because it can be valid Focused or purpose-specific output. Hooks
cannot certify presentation selection, trusted topic state, or already
displayed output.

## Local v0.4 artifact record

The target version for every current package is `0.4.3`:

- `progressive-clarity-core` version `0.4.3`;
- `dist/progressive-clarity-openai-plugin-0.4.3.zip`;
- `dist/progressive-clarity-claude-plugin-0.4.3.zip`; and
- `dist/progressive-clarity-claude-ai-skill-0.4.3.zip`.

The frozen v0.4 source-input hashes are:

- `SPEC.md`:
  `260c3facd8c5c95a1d4429863e24226621defe8274dd08afd4d4d044452e5122`;
- `skills/progressive-clarity/SKILL.md`:
  `ac64b0d1e055c820275455626ebb054b7b41111aa7a53a2f03364dd33023f04d`;
- `evals/cases.json`:
  `068ad1b881e674959d07b59e4f811f4e4e89beefa3f96f8b6a24d07ea7546844`.

Local Python artifacts are:

- sdist: 37,024 bytes, SHA-256
  `8068f09e2fe41e30a330397ad23fdcf304259949a8b868edd4eaacb7793f9fe2`;
- wheel: 44,036 bytes, SHA-256
  `b28696d5d54ca07ac8417e0b983b975175067e658e9c418000683b5089d5acfe`.

Two consecutive builds of each host ZIP produced matching bytes:

- OpenAI plugin: 27,402 bytes, SHA-256
  `26e3ca4cb687b893ef9adcf94acd8b9625a00e70e60f8853d28cfddb7bf19a54`;
- Claude plugin: 25,789 bytes, SHA-256
  `dd71d71f8277188161429a61f5412d3a0e87b4f6b3a29847bb0bb7ce520bfed9`;
- Claude.ai Skill: 24,564 bytes, SHA-256
  `8f8f697778387a4845ee6d66726aa1cc5c90ce4e0dd63573f5a4923f6368b874`.

The exact entry inventories, byte counts, and SHA-256 values are recorded in
the current [OpenAI](openai-plugin.md) and [Claude](claude-plugin.md) package
records from the packagers' verified output.

These are local build and integrity results, not a release, upload, review,
approval, publication, host-compatibility, or behavior result.

### Preserved package 0.4.2 identities

Package `0.4.2` remains immutable evidence for the first remediation round:

- sdist: 36,757 bytes, SHA-256
  `54a8799ce5749d0c7c9b63e3ef9b7dc4adacfb86b2d1a5a96b92b11262472cab`;
- wheel: 43,779 bytes, SHA-256
  `e386445b1cf0e3f4f34e1c3fefa94a915306badfcf0a4fc02d7d15394d5a90aa`;
- OpenAI plugin: 25,277 bytes, SHA-256
  `ba7e6c2e97ab3dc01ac81c9d2695ad5e504574de2b8bf50bbf7dc2c69d1251df`;
- Claude plugin: 23,664 bytes, SHA-256
  `a4d0bb9dca2c6e7d1986bd634c8f8b8b1f1b65359cb67dc33877e11c785efbba`;
  and
- Claude.ai Skill: 22,439 bytes, SHA-256
  `e051684925d205a8436c14979104ba95bacba1c1d39183ffde4b72843c3f2c9a`.

The maintainer reports that an OpenAI package identified as `0.4.2` is
published on OpenAI. The portal bytes and their equality with the local digest
above were not independently captured.

### Preserved package 0.4.1 identities

Package `0.4.1` remains immutable evidence for the Azure initial round:

- sdist: 36,434 bytes, SHA-256
  `a227a2b71f90daf5b58f33cb628822f7585d0491a84235d3be09ee84cf70a392`;
- wheel: 43,471 bytes, SHA-256
  `a0be32d02c5d1a874e06986f4638dcdf4473a436eb6e25de32aa798b1aa4c59a`;
- OpenAI plugin: 23,722 bytes, SHA-256
  `b2bf306a6591963ff3a06ee9e507162402c80b5fe9f8829a126204df3cd97323`;
- Claude plugin: 22,109 bytes, SHA-256
  `1340829081f7ed8a59cab8ed37e4fab509c89f48c104b5e7ce29fbbb07e4418d`;
  and
- Claude.ai Skill: 20,884 bytes, SHA-256
  `ca9a25433d8600d1bd0f55e8b8fa2b63c0b75ec82015e71659d386fb3ec94478`.

## Local v0.4 verification

On 2026-08-20, the current dirty worktree passed:

- `python3 -m tools.validate_repository`;
- 157 unit tests under Python 3.12, including 27 Azure-harness tests;
- `compileall` over `pc_core`, `tests`, and `tools`;
- Ruff 0.12.9 over the same Python paths;
- Python sdist/wheel build, isolated Python 3.11.15 installation, and installed
  Focused and Full `pc-core render` smoke tests;
- repeated deterministic OpenAI, Claude plugin, and Claude.ai Skill builds with
  matching hashes and successful ZIP integrity checks;
- `git diff --check`;
- the official `skills-ref` validator at pinned revision
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`;
- installed Claude Code 2.1.72 `claude plugin validate .` structural
  validation. That version does not expose the `--strict` option; and
- Agno Azure harness dry planning, checkpointed controlled remediation rounds,
  and a final complete 14-session/29-response passing round.

These checks cover local structure and mechanics. The source remains
uncommitted and remote CI was not run. No commit, push, upload, publication, or
public deployment was performed for v0.4.3. The Azure proxy ran only against
the explicitly configured local deployment; its reports contain no API key or
full endpoint and do not establish host activation or package behavior.

## Azure behavior-proxy evidence

Azure execution used Agno 2.6.7, deployment `gpt-5.6-sol`, and the configured
API version. It injected the canonical Skill as a system message. This is not
ChatGPT installation, activation, package, UI, or compatibility evidence. The
structured judge used the same deployment and is not independent.

The complete package-0.4.1 initial report is the ignored local file
`evals/runs/azure-v0.4.1-gpt-5.6-sol-initial.json`. It completed all 14
prescribed sessions and 29 responses: 2 runs passed and 12 failed. Eight turns
had deterministic failures; 19 turns had semantic-judge failures. Every failed
turn had this exact visible evidence:

- `T01` turn 1: “often used for caching, sessions, queues, and real-time data”
  was the prohibited adjacent catalogue; turn 2 repeated the database/Redis
  role split and ended “must not permit a payment to be charged twice”; turn 4
  repeated that role boundary in “Redis can cache durable idempotency results
  ... but a cache miss must fall through to the database uniqueness check.”
- `T02` turn 2 ended by repeating the authorized-exception rule: “use only the
  organization’s formal exception mechanism.”
- `T03` turn 1 reproduced the complete five-step list below At a glance; turn 3
  rendered no required views and instead asked, “Did the entire migration
  window move to Sunday, or only the write freeze while the migration remains
  scheduled for Saturday?”
- `T04` run 1 turn 2 ended “production coverage remains Tuesday” and was scored
  against future Thursday data plus a nonexistent correction phrase; turn 3
  withdrew “production coverage remains Tuesday,” not the required prior
  statement. Run 2 turn 1 invented “Tuesday, August 25, 2026”; turn 2 silently
  substituted “the review is Wednesday”; turn 3 placed the exact prefix below
  At a glance but the old deterministic check incorrectly tested response byte
  zero. Run 3 turn 2 again ended “production coverage remains Tuesday” and was
  scored against future data; turn 3 again withdrew “remains Tuesday.”
- `T05` run 1 omitted all three views and asked “have writes been frozen”; run
  3 included numbered item “Restart or promote only under the approved recovery
  plan.”
- `T06` turn 2 forced all three headings after the inputs were supplied and
  omitted the staging/production boundary.
- `T08` asked “What should the scene be about, and what tone or setting do you
  want?” instead of producing the requested narrative.
- `T09` asked for database, checksum, target, owner, and rollback details
  instead of rendering the supplied complete sequence.
- `T10` turn 1 asked “What Atlas decision was made—proceed, delay, or roll
  back?” instead of producing the required Full explanation.

The initial report exposed evaluator defects separately from model behavior:
the judge saw future-turn source facts; treated the supplied facts as an
exhaustive knowledge base; demanded the non-contract phrase `The correct
information is`; and sometimes treated materially new implementation anchors
as complete repetition. The deterministic repair-prefix check incorrectly
tested Full output before its At-a-glance heading. The warning oracle did not
clearly distinguish a permitted resume condition from operational restart
instructions, although the observed numbered restart item remained a model
failure. `T03`, `T09`, and `T10` contained avoidable ambiguity that encouraged
clarification; T08 was a direct model-adherence failure.

A later finding-by-finding read-only audit classified the 44 initial semantic
FAIL findings as 20 likely model failures, 13 oracle/scorer defects, and 11
same-deployment judge overreaches. That audit recommended evaluator-only
remediation because the existing Skill already stated the violated rules.

The one permitted remediation changed only what this evidence justified:
turn-local judge facts, open-world accuracy wording, exact applicable criteria,
At-a-glance repair-prefix scoring, deterministic numeric labels, clearer
non-fit and post-clarification guidance, exact correction withdrawal, and
grounded evaluation prompts. Because canonical Skill bytes changed, all
coordinated package channels moved to `0.4.2`; no `0.4.1` artifact was
overwritten.
The evaluator-only recommendation arrived after the single remediation input
was frozen. It does not establish that the 0.4.1 Skill was defective, authorize
rewinding immutable 0.4.2 bytes, or reopen the bounded cycle.

The ignored remediation report is
`evals/runs/azure-v0.4.2-gpt-5.6-sol-remediation.json`. It reran only the nine
initially failed case IDs, including all T04/T05 repetitions: 13 sessions and
28 responses. Four runs passed (`T04` run 3, `T05` run 3, `T08`, and `T09`);
nine failed. The cycle therefore stopped with strict acceptance unmet. The
remaining failures were observable: T01 still added a use-case catalogue,
ended one Full answer with a recap, and omitted the numeric template; T02 ended
with an exception-rule recap; T03 missed Full once, asserted unchanged or
normal state, and ended with a recap; two T04 runs failed exact narrow repair
or invented a date; two T05 runs missed Full or ended with a warning recap; T06
omitted passed validation and the production boundary; and T10 retained one
judge repetition conflict and omitted the reconciliation-before-rollback
anchor on return.

The remediation judge still produced a material inconsistency: for T10 turn 1,
`full_no_complete_repetition` passed the later reconciliation wording as a
necessary anchor while `prohibited_behaviors` failed the same wording as a
restatement. T10 turn 3 also illustrates oracle tension between requiring the
prior sequencing fact and prohibiting an unrequested complete recap. Those
claims remained unresolved. T04 additionally retained tension between a static
canonical repair prefix and the exact wording the model actually emitted in
the prior turn. On 2026-08-20 the maintainer explicitly overrode the earlier
hard stop and authorized controlled, reviewed cycles with no averaging until
all prescribed Azure runs pass.

Controlled continuation corrected remaining scorer exceptions, made correction
judging use actual conversation history, fingerprinted the exact Skill body in
checkpoints, and grounded case inputs and view allocation where the same-model
judge had produced inconsistent results. Every intermediate report remains
ignored and preserved locally; no failed run was averaged with a pass.

The decisive report is
`evals/runs/azure-v0.4.3-gpt-5.6-sol-final-v3.json`. It has status `COMPLETE`
and result `PASS`: all 14 prescribed sessions and all 29 generated responses
passed, including all three T04 and all three T05 repetitions. It used protocol
SHA-256
`260c3facd8c5c95a1d4429863e24226621defe8274dd08afd4d4d044452e5122`
and Skill-body SHA-256
`6cb3cd1621951eb13a8e0fcaec4945694c8e59db52507dd938c63767edcd5924`.

This is 100% acceptance under the frozen Azure harness and its explicitly
grounded prompts. It remains a same-deployment regression proxy, not an
independent semantic evaluation, stochastic reliability guarantee, ChatGPT
activation trace, or proof that OpenAI serves the local package bytes.

## Historical/superseded v0.3.x evidence

Everything in this section belongs to protocol v0.3 and packages 0.3.0 through
0.3.2. It is preserved as user-provided host evidence or local baseline
evidence and must not be aggregated into a v0.4 result. Portal-byte identity
and visible Skill activation were not independently verified.

### Preserved local v0.3.2 baseline

Before v0.4 editing, the intentional dirty worktree already targeted package
0.3.2 and retained the consolidated untracked `tools/package_common.py` plus
other untracked source dependencies. The baseline passed repository validation,
109 unit tests, compileall, Ruff 0.12.9, `git diff --check`, Python build and
isolated installation, and two byte-identical builds of every host ZIP.

The preserved v0.3.2 source hashes were:

- `SPEC.md`:
  `5bd4eb355cbbb45fdc055d3ecd3cf3e1dff12d4b534e4bb4ff0fb7fd0777a167`;
- `skills/progressive-clarity/SKILL.md`:
  `c62bb4bfe0044cf049dd2a491941243a2eda7e67d6f568ba36c306b5b620614b`;
- `evals/cases.json`:
  `fd259d1d0160a64427e3093c9e6559ce83a13264b4a7242b827a704f22f699cc`.

The v0.3.2 artifacts were:

- sdist: 32,306 bytes, SHA-256
  `b53528ec49408cc8cae1d874ef2e84de51741ad4daa3da42e74d3aefe5d8bf1e`;
- wheel: 39,376 bytes, SHA-256
  `0ccc113cc5f1ba3e969d83225e502670daae1142939a0249af33b9e9dbd9281d`;
- OpenAI plugin: 21,432 bytes, SHA-256
  `e0d2ed39a6ad06f64c99c163827f882614a7cb30e721414b16b46417d0526887`;
- Claude plugin: 19,865 bytes, SHA-256
  `6c18eb2f7e91bc07b0348bb99e21168a1249aa50c23bc219830f9809e54b681a`;
- Claude.ai Skill: 18,663 bytes, SHA-256
  `2ad59a7a69b4bf848fb6f5644544af8d862549434e501a54e1677165f53f5c4a`.

### Preserved local v0.3.0 and v0.3.1 host artifacts

The ignored `dist/` directory also retained these historical local artifacts
before v0.4 work began:

- OpenAI 0.3.0: 20,032 bytes, SHA-256
  `cec9f587c5f2a632e6a6c1057c4a3262f4629fdd18226ea61c60e51da6cdde85`;
- OpenAI 0.3.1: 20,627 bytes, SHA-256
  `a128a0e0ea57f8afa1d49a2fecd8c49f343dc54214d4687d1afec55b435b171d`;
- Claude plugin 0.3.0: 18,478 bytes, SHA-256
  `38933d23e657555381f7eb40918e1a715bd9a7f2efc82a414c64ffd1352b1090`;
- Claude plugin 0.3.1: 19,073 bytes, SHA-256
  `0049fbc8058b75c007036875826676b14b0654ef5192493a3ab6ed68d31c2319`;
- Claude.ai Skill 0.3.0: 17,263 bytes, SHA-256
  `68d38e0b8afe49a8e9ec3409a1248a9906b0957988a7a4c7b4dceeca2f484af5`;
  and
- Claude.ai Skill 0.3.1: 17,858 bytes, SHA-256
  `aa74c7ccdbc365568af02e6ff527c6bed58ec500ff320945954a11b8d31baab3`.

These local-byte identities do not establish portal identity, upload,
activation, or host behavior.

### User-provided v0.3.0 ChatGPT evidence

On 2026-08-19, the user reported publishing and installing package `0.3.0` in
ChatGPT. The repository did not independently observe the portal workflow,
identify installed bytes, or receive an activation trace.
The corresponding local OpenAI archive had SHA-256
`cec9f587c5f2a632e6a6c1057c4a3262f4629fdd18226ea61c60e51da6cdde85`,
but that does not establish portal-byte identity.

The user supplied two fresh Redis lifecycle transcripts:

- **Run one: FAIL.** The simple fact was Focused, but the first consequential
  payment decision failed to transition to Full. The TTL follow-up was Focused
  but supplied an overconfident numeric default without governing provider
  requirements.
- **Run two cadence and budgets: PASS.** The sequence was Focused → Full →
  Focused → Full. The payment decision counted 30 words in At a glance and 125
  through In context; the handoff counted 33 and 119.
- **Run two strict conformance: FAIL.** The simple fact remained
  disproportionate, and both Full answers repeated the headline
  database-authority conclusion below At a glance.

Visible output does not prove skill activation, so activation remains
`UNVERIFIED` without the host indicator. These bounded failures motivated
package `0.3.1`: simple facts now default to one to three sentences, Full
responses reserve the headline conclusion for At a glance, and numeric
recommendations without governing inputs must label assumptions or examples.

### User-provided v0.3.1 ChatGPT initial round

The user supplied the complete 14-session, 29-response initial round for
package `0.3.1`. No activation indicators were supplied, so activation remains
`UNVERIFIED`.

- **Passed cases:** T08 narrative and T09 procedure.
- **Failed cases:** T01–T07 and T10.
- **Consistent strengths:** every counted Full response met the 40/200 budgets;
  most cadence decisions and the A → B → A topic return worked.
- **Systemic failure:** Full responses repeated headline conclusions, warning
  steps, or decision propositions across deeper views.
- **Additional failures:** overlong simple facts, unsupported numeric defaults,
  implicit rather than explicit repairs, conditional answers instead of
  clarification, incomplete At-a-glance warnings, an unlabeled legal summary,
  and unsupported dependency assumptions.

### User-provided v0.3.2 ChatGPT results

The user supplied later ChatGPT observations identified as v0.3.2 behavior.
The repository did not observe the portal workflow, identify the installed
bytes, or independently verify the visible Skill activation indicator.

What generally worked:

- Focused → Full → Focused → Full cadence;
- explicit Focused and Full overrides;
- every observed Full 40/200 budget;
- topic switching and return;
- complete safety containment;
- narrative and sequential-procedure exclusions; and
- local Python/core and package verification.

Recurring failures were complete conclusions, dates, component roles,
warnings, and recovery steps restated across deeper views; overlong simple
facts; unlabeled numeric assumptions; correction openings that said only
“corrected,” “outdated,” or “superseded”; recommendations before clarification;
and `Summary:` instead of the literal non-controlling label. Strict scoring that
required every atomic fact to appear once was also too brittle for coherent
natural responses.

The bounded case status was:

- **T01: FAIL** — proportionality, numeric labeling, and Full repetition;
- **T02: latest run effectively PASS**;
- **T03: under-specified old oracle, plus Full repetition**;
- **T04: narrow repair improved; material repair and additivity remained weak**;
- **T05: warning improved; Full repetition remained**;
- **T06: isolation suspect; first-turn clarification failed**;
- **T07: FAIL** — literal non-controlling label missing;
- **T08: PASS**;
- **T09: PASS**; and
- **T10: topic return PASS; initial Full conclusion repeated**.

One T06 transcript mentioned staging, validation, and rollback before those
facts were supplied. Future ChatGPT runs therefore require Temporary Chat,
memory disabled, and one fresh chat per case run. T03 and T06 oracles are
corrected in v0.4. These observations are historical and do not establish
v0.4 activation, conformance, compatibility, or support.

## Current v0.4 verification still required

Before any release-readiness claim, the responsible maintainer must:

1. independently review the local Python and host artifacts;
2. run the v0.4 Advisory acceptance suite separately on ChatGPT, Cursor, and
   Claude with frozen inputs and preserved raw evidence; and
3. keep package integrity, host activation, rendered conformance, and semantic
   correctness as separate evidence dimensions.

Package `0.4.3` does not inherit any v0.3.x ChatGPT result or any result from
the historical v0.2 cycles below.

## Historical v0.2 verification record

Everything below this heading is retained as historical v0.2 and earlier
evidence. References to “current,” v0.2 package versions, old schema numbers,
hashes, dated checks, and user-provided transcripts describe those frozen
records only. Original PASS, FAIL, UNVERIFIED, and hard-stop labels are
preserved and must not be aggregated with v0.4.

This record separates the current revised artifacts and deterministic local
mechanics from the preceding bounded prompt-only host cycle and from
user-provided ChatGPT evidence. The preceding Cursor cycle ended in failure at
its required hard stop. The v0.2.1 prompt-only skill has no independently
executed full host acceptance run. The current ChatGPT evidence consists of
user-reported upload and installation plus two user-provided transcripts with
different bounded outcomes. Progressive Clarity protocol v0.2 and package
v0.2.1 remain a **non-release-ready draft**.

## Result labels

- **PASS** means direct evidence establishes only the named check against the
  named frozen revision.
- **FAIL** means observable output violates a requirement of that frozen
  revision.
- **UNVERIFIED** means available evidence cannot establish the claim. It is
  neither a pass nor a failure.
- **HISTORICAL/SUPERSEDED** means the result belongs to an older contract and
  must not be used as evidence for v0.2.
- **MECHANICALLY_CERTIFIED** means the non-streaming local wrapper validated a
  trusted request, committed state, schema `2.0.0` envelope, and canonical
  rendering. It is not a semantic `PASS`.

A file copy, structural validation, discovery trace, or explicit load does not
establish rendered behavior. Similar output without a host trace does not
establish activation.

## Current conformance surfaces

- **ChatGPT:** v0.2.1 is Advisory prompt-only. No backend or MCP is required.
  On 2026-08-18, the user reported uploading and installing the v0.2.1 ZIP.
  The portal bytes and authenticated portal actions were not independently
  captured.
- **Cursor and Claude Code skills:** Advisory prompt-only. No current-revision
  host acceptance run exists.
- **Project hook templates:** Advisory/block-and-retry. Current official hook
  contracts cannot provide the same reliable full-response fail-closed gate as
  the wrapper.
- **`pc-core` non-streaming wrapper:** Enforced mechanical when it emits output
  after a pass. Unit/property tests, an isolated installed-wheel smoke, and one
  bounded live Cursor remediation rerun exercise this path. Live Claude Code
  wrapper execution remains `UNVERIFIED` because paid Anthropic API access is
  required and no paid live run was completed.

Mechanical enforcement covers versions, topic/branch/turn arithmetic,
three-view heading order, English budgets, fact-ID integrity and declared reuse,
correction/quotation structure, exact lexical duplicates in Progressive Clarity
view and explanatory prose while required verbatim artifact bytes remain
exempt, canonical view rendering, byte-preserving accepted non-fit payloads,
and atomic state commit. Accuracy, completeness beyond a supplied authoritative
catalog, catalog correctness or completeness, warning indispensability, human
safe stopping, paraphrased repetition, purposeful detail, and hidden reversal
remain advisory `UNVERIFIED`.

## Current protocol v0.2 and package v0.2.1 target

The normative [`SPEC.md`](../SPEC.md) defines one ordinary in-scope behavior:
every response renders **At a glance**, **In context**, and **At depth** once
and in order. At a glance has a 40-word non-warning cap; non-warning prose
through In context has a 200-word per-response cap; At depth is unrestricted
but purposeful. Targeted follow-ups retain all three views. Clarification,
correction, controlling text, exact output, procedure, narrative, and safety
exceptions remain explicit.

There is no presentation depth, progression, alternate behavior, or cross-turn
shallow-word accumulation.

## Current revised inputs

The current synchronized v0.2.1 package inputs are:

- [`SPEC.md`](../SPEC.md): SHA-256
  `74d2df5d443e9bb8a9dd3612f96397e8050ce8c1b71ac0eea34cd209d19adfe8`;
- [`skills/progressive-clarity/SKILL.md`](../skills/progressive-clarity/SKILL.md):
  SHA-256
  `ab8d3ba8e9aa02530f97d21af15ff371ec0df02055b6e2f0cff665c36c59a749`;
- [`evals/cases.json`](../evals/cases.json): SHA-256
  `8788528b11667b99a8ba398efe1dd17da3b302c687e584e5c07ca94f84f17eb4`;
- rebuilt prompt-only OpenAI ZIP: SHA-256
  `d5e447abc41132a3e5d0580b5afc5231230317dead1adcee5767085159cbde23`;
  and
- local envelope, state, validator, renderer, adapters, and tests under
  `pc_core/`, `adapters/`, and `tests/`.

The v0.2 evaluation suite identifies prompt-only host behavior as Advisory.
No prompt-only Cursor or Claude Code acceptance run has been executed against
these current skill bytes. No independently executed full ChatGPT acceptance
run exists; the two current ChatGPT transcripts below are user-provided,
bounded observations after the reported upload and installation. Local tests
validate mechanics and wrapper state; the live evidence below covers the
separate Cursor wrapper boundary.

### Bounded live Cursor wrapper remediation

The initial live Cursor enforcement run was frozen to skill SHA-256
`5f9f7881588ce02f14a122fcd6fef1cc98d7e7a3e415afd61dc5f0a3d37fab01`,
SPEC SHA-256
`74d2df5d443e9bb8a9dd3612f96397e8050ce8c1b71ac0eea34cd209d19adfe8`,
and evaluation SHA-256
`8788528b11667b99a8ba398efe1dd17da3b302c687e584e5c07ca94f84f17eb4`.
The skill hash is a pre-trigger-revision evidence identifier, not a current
repository pin. Its files and scoring inputs were not changed. The initial run
failed E02-E07 and exposed four wrapper defects: per-turn host sessions,
certifiable empty views, implicit fresh-workspace trust assumptions, and a
model-defined completeness boundary.

One authorized remediation rerun then executed E02-E07 once with prescribed
repetitions against the same frozen skill while exercising the mechanical
wrapper fixes, then stopped. It preserved 162 evidence files under
`/private/tmp/progressive-clarity-v02-cursor-live-5f9f7881/evidence/remediation-live-20260818`.
Of 17 responses, 10 were mechanically certified and 7 were withheld after two
attempts with empty release files and unchanged local state. The architecture
targets passed: both eligible follow-up turns resumed their committed Cursor
session; all 15 sections in five certified view responses were non-empty; all
eight certified responses supplied an authoritative catalog passed exact
catalog coverage; and the adapter added no trust flag after the earlier
explicit isolated bootstrap.

The behavioral suite still failed overall: E02, E06, and E07 passed; E03,
E04, and E05 failed. E03 repeatedly returned Markdown instead of envelopes,
one E04 repetition was withheld, and E05's clarification did not directly ask
for the missing environment. This is the required hard stop; no further prompt
or live rerun is authorized in this remediation.

## Current local verification

On 2026-08-18, the CI-equivalent local checks produced:

- `PASS`: 64 standard-library unit/property tests under Python `3.11.15`,
  including the activation-only trigger fixture and synthetic
  invalid-then-valid wrapper repair smoke test;
- `PASS`: repository hashes, schema/references, whitespace, relative links,
  ordered test-docstring contracts, complete host-template shape, Python
  package metadata, skill package shape, and OpenAI source inventory;
- `PASS`: Ruff `0.12.9` over `pc_core`, `tests`, and `tools`;
- `PASS`: isolated Python 3.11 sdist/wheel build, wheel install, `pc_core`
  import outside the checkout, `pc-core` console-script smoke, and a
  project-local installed-hook command smoke;
- `PASS`: official `skills-ref` validation at pinned agentskills revision
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`;
- `PASS`: two byte-identical OpenAI package builds, ZIP integrity, normalized
  inventory, and source-byte equivalence; and
- `PASS`: local host adapter argv/result parsing without network inference.

The installed Cursor Agent CLI reported `2026.08.11-e8db854`; Claude Code
reported `2.1.72`. Their current official hook and non-streaming CLI contracts
were reviewed. Local passes establish deterministic mechanics and package
integrity; the separate bounded evidence above establishes only the recorded
Cursor wrapper observations.

## Retained older host-cycle inputs

The closed dual-behavior Cursor cycle remains frozen at its original inputs:

- [`SPEC.md`](../SPEC.md): SHA-256
  `ff72cb498d93f6a8d8e972798e664e64df5bbc1c99f6e0a47db819331c18e16d`;
- [`skills/progressive-clarity/SKILL.md`](../skills/progressive-clarity/SKILL.md):
  SHA-256
  `5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`;
- [`evals/cases.json`](../evals/cases.json): SHA-256
  `4c27a740e2e02e54f97889618397a6417c82e089b9bb44919b92642e59289680`.

These hashes are evidence identifiers, not current repository pins. The
current validator and CI pin the revised inputs above and evaluation schema
`4.0.0`. Do not reuse a prior prompt, score, trace, or result merely because its
case name still exists.

## Host discovery paths

These are documented host paths, not current v0.2 verification results:

- Cursor project: `.agents/skills/progressive-clarity/` or
  `.cursor/skills/progressive-clarity/`;
- Cursor user: `~/.agents/skills/progressive-clarity/` or
  `~/.cursor/skills/progressive-clarity/`;
- Claude Code project: `.claude/skills/progressive-clarity/`; and
- Claude Code user/personal: `~/.claude/skills/progressive-clarity/`.

The completed Cursor cycle used one isolated project copy and recorded its
exact path, host and model versions, frozen artifact hashes, invocation
method, and available host traces. The documented paths alone neither
authorize another run nor establish support.

## Cursor status

**Current status: revised prompt-only behavior UNVERIFIED; preceding strict
acceptance unmet; bounded live Cursor wrapper rerun completed and still failed
overall; hard stop reached.**

The retained preceding cycle used Cursor desktop `3.15.19`, Cursor Agent CLI
`2026.08.11-e8db854`, and model `GPT-5.6 Sol 272K Medium`. The bounded policy
required one complete initial round, allowed no more than one skill revision,
required every initially failed case to be rerun with all of its prescribed
repetitions, and required the cycle to stop after that targeted round
regardless of outcome. Every prescribed run had to pass; there was no majority
vote or intermittent-failure allowance.

### Round one

Round one used the frozen specification and cases above with pre-remediation
skill SHA-256
`168e2c301cd0a18f4f83161b70d61445ad926ba9d71f944d70c9c323972e0908`.
It completed 21 fresh sessions and 39 scored assistant responses with no
transient retries:

- cases: 6 `PASS`, 5 `FAIL`;
- facts: 200 `PASS`, 11 `FAIL`;
- budgets: 39 `PASS`, 0 `FAIL`;
- activation: 8 `PASS`, 1 `FAIL`, 2 `UNVERIFIED`; and
- internal state: 11 `UNVERIFIED`.

`M01`, `M03`, `M06`, `M08`, `M09`, and `M11` passed. The five failures were:

- `M02`: 62/66 facts; all three At-a-glance responses omitted the required
  Android 13 checkout-crash scope, and run 1 also omitted the 12 September
  date. Progressive advances and the switch to Verbose rendered correctly.
- `M04`: 8/12 facts; `$120,000 annually` and the two-weekend migration
  duration were absent at both required stopping points.
- `M05`: 20/21 facts; run 1 omitted the 14:30 report fact. All indispensable
  warning and payment-safety checks passed.
- `M07`: 5/7 facts; the clarification omitted environment or rollout scope,
  and staging monitoring was not connected to the pre-production decision
  gate.
- `M10`: procedural behavior, step order, and safety branches passed, but
  activation failed because Cursor read the skill despite `remain_inactive`.

### One permitted remediation round

The one permitted revision produced the final frozen skill SHA-256
`5051c55286533cecf65a7963bf7fab68471986e851dbd65a21bceda0683d7562`.
Only `M02`, `M04`, `M05`, `M07`, and `M10` were rerun, with their prescribed
repetitions. The targeted round completed 9 fresh sessions and 20 responses
with no transient retries:

- cases: 0 `PASS`, 5 `FAIL`;
- facts: 103 `PASS`, 10 `FAIL`;
- budgets: 20 `PASS`, 0 `FAIL`;
- activation: 4 `PASS`, 1 `FAIL`; and
- internal state: 5 `UNVERIFIED`.

The targeted outcomes were:

- `M02`: 63/66 facts; Android 13 scope was present, but all three At-a-glance
  responses omitted the required 12 September launch date.
- `M04`: 8/12 facts; the exact annual savings and two-weekend migration
  duration remained absent at both stopping points.
- `M05`: 20/21 facts; run 3 omitted the 14:30 report fact. All indispensable
  warning and payment-safety checks passed.
- `M07`: 5/7 facts; environment or rollout scope remained absent from the
  clarification, and monitoring remained unconnected to the pre-production
  decision gate.
- `M10`: procedural behavior, step order, and safety branches passed, but
  activation again failed because Cursor read the skill despite
  `remain_inactive`.

Across both rounds, all 59 budget checks passed. There were no safety-warning
or procedural-safety failures. Those bounded positives do not erase any case
failure and are not a safety certification.

The second round triggered the mandatory hard stop. No further remediation was
performed within that cycle or is implied by this record. That cycle's final
skill received only the prescribed targeted rerun, not a new full-suite round,
so this evidence cannot establish Cursor compatibility or support.

The current v0.2.1 trigger-recall skill is a new input, not another remediation
round, and has no prompt-only Cursor host result. The bounded live rerun used
the pre-trigger-revision skill while exercising the remediated wrapper. It
therefore establishes only the 10 certified and 7 withheld wrapper
observations above; it does not transfer a semantic or prompt-only acceptance
result to the current skill.

All former-protocol Cursor evidence remains **historical and superseded**. It
must not be aggregated with this cycle.

## Claude Code status

**Current status: revised prompt-only and live wrapper behavior UNVERIFIED; a
live run requires paid Anthropic API access and was not completed.**

Claude Code 2.1.72 previously:

- scanned `.claude/skills/progressive-clarity/` as a project skill;
- listed `progressive-clarity` as a skill and slash command; and
- parsed `/progressive-clarity` and attached the former skill text.

That observation used the former protocol and does not verify v0.2 or its
current skill. The first API request stopped before
inference with `Credit balance is too low`. Input and output tokens were zero,
cost was `$0`, and no assistant response was scored. No Claude Code behavior
result is represented by this finalization. Completing a live run requires
paid API credit; structural checks do not remove that paid-access requirement.

The current project Stop-hook template follows the documented
`last_assistant_message` and `decision: "block"` schema. The non-streaming
adapter follows documented `claude -p --output-format json` and `--resume`
behavior. These structures and synthetic parsing are locally tested, but no
live Claude inference was run and no compatibility claim follows.

## Strict acceptance rule and outcome

The preceding host cycle scored visible mode behavior, cumulative facts,
required caveats, additive views, budgets, corrections, controlling text,
non-fit structure, activation, and negative activation separately. Internal
state could remain `UNVERIFIED` when the host exposed no trace, while rendered
consequences still passed or failed.

Strict acceptance required every prescribed run to pass. Round one failed five
cases, and the only permitted targeted remediation round failed all five
again. Cursor strict acceptance is therefore **unmet**.

The v0.2 schema `4.0.0` suite defines a new future Advisory host run and has no
current result. `pc-core` mechanical tests do not
substitute for that run or satisfy its semantic criteria.

The bounded v0.2 Cursor wrapper rerun also failed `E03`, `E04`, and `E05`.
Its 10 mechanical certifications do not satisfy strict semantic or behavioral
acceptance, which remains unmet.

## Security checks

The Advisory Agent Skill and ChatGPT package remain instruction-only:

- only the canonical `SKILL.md` and Apache-2.0 `LICENSE` are installed;
- neither file is executable or a symlink;
- no script, hook, plugin runtime, service, or background process is installed;
- no tool is granted or pre-approved; and
- no network access, analytics, telemetry, or user-input collection is
  required.

This posture does not certify the host or model as secure. Host permissions,
tools, network access, and data handling remain host-controlled.

The optional local `pc-core` package is executable Python but uses only the
standard library, starts no service, configures no MCP server, collects no
analytics, and changes no user-global settings. The Cursor and Claude hook
files are templates only; the repository does not install them. The
non-streaming wrappers execute the selected host CLI under that host's existing
authentication and permissions.

## OpenAI status

**Current status: v0.2.1 is Advisory. On 2026-08-18, the user reported
uploading and installing it. Current user-provided ChatGPT evidence contains
one non-conformant complex transcript and one passing bounded smoke; portal-byte
identity, authenticated portal records, and universal conformance remain
independently UNVERIFIED.**

On 2026-08-17, the user reported publication of an older ChatGPT plugin at
[`plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
An anonymous fetch independently confirmed that the URL returns a ChatGPT
Plugins route, but the response exposed only a login page. It did not expose
listing metadata or install controls.

For that older package, the publication report supersedes the earlier
statement that portal upload and submission were blocked and that no upload
occurred. The URL is retained as historical publication evidence. Neither it
nor that older publication report establishes the separate current v0.2.1
upload or installation; those are recorded from the user's 2026-08-18 report.
The older report is not a `PASS` under the result labels above. The anonymous
route check independently establishes only that the route exists; it does not
establish authenticated listing visibility, installability, successful
installation, or activation.

### Historical user-provided live transcript

On 2026-08-17, the user also supplied a transcript they identified as a live
interaction with the published plugin. The repository did not independently
capture or reproduce that session. It is user-provided evidence. The
`PASS`/`FAIL` labels below score only the named visible checks in the supplied
transcript; they do not represent an independently run full-suite evaluation:

- **Default Verbose rendering:** `PASS`. All three views appeared in the
  required order.
- **Progressive acknowledgment and stickiness:** `PASS`. The transcript showed
  the acknowledgment and **At a glance → In context → At depth** transitions.
- **Safe stopping and caveats:** `PASS`.
- **At-a-glance budgets:** `FAIL`. Gold used approximately 103 prose words;
  silver used approximately 210 prose words excluding tables and citations.
- **Cumulative prose through In context:** `FAIL`. Gold used approximately
  330+ words; silver used approximately 600+ words.
- **Additivity and no fact-only repetition:** `FAIL`.
- **Switch back to Verbose:** the acknowledgment was observed, but actual
  subsequent Verbose behavior was not included and remains `UNVERIFIED`.

Because core budget and additivity requirements failed, the ChatGPT behavior
status is **observed but non-conformant**. Passing order, transition, and caveat
checks do not establish compatibility or support. No financial fact in the
gold or silver responses was independently verified, and this record makes no
claim about the factual accuracy or suitability of their financial content.

### Earlier user-provided pre-v0.2.1 trigger transcript

On 2026-08-18, the user supplied another transcript after reporting a new
plugin upload. The installed portal bytes were not independently identified,
and this transcript preceded the v0.2.1 trigger-recall patch. The initial `gold
prices and forecasts` answer did not render **At a glance**, **In context**, or
**At depth**. After the user challenged the omission, ChatGPT produced the
headings but described removed Progressive/Verbose modes and said it had failed
to activate the skill.

The repository did not independently capture the session, verify the installed
portal bytes, or receive a host activation trace. The visible initial response
therefore `FAILS` the v0.2 three-view output requirement; the exact activation
mechanism and loaded revision remain `UNVERIFIED`. The obsolete-mode explanation
is incompatible with the current skill body and indicates stale or non-loaded
behavior rather than a current v0.2 instruction.

### User-reported v0.2.1 upload and installation

On 2026-08-18, the user reported uploading package v0.2.1 and installing it in
ChatGPT. The repository did not independently observe either action, record an
authenticated listing, identify the portal artifact by digest, or receive
upload, submission, review, approval, portal-validation, security-scan, or
publication records. The evidence therefore establishes a **user-reported
upload and installation**, not independently verified portal-byte identity or
publication history.

### User-provided v0.2.1 complex gold-forecast transcript

On 2026-08-18, after the reported upload and installation, the user supplied a
complex gold-forecast transcript identified as v0.2.1 behavior. The repository
did not independently capture or reproduce the session. The named visible
checks score as follows:

- **Three-view structure:** `PASS`; the required structure triggered.
- **40-word At-a-glance budget:** `FAIL`.
- **200-word cumulative shallow budget:** `FAIL`.
- **Additivity:** `FAIL`.

Because both budgets and additivity failed, this transcript is **observed but
non-conformant**. Its financial statements were not independently verified,
and the behavioral score does not establish their accuracy or suitability.

### User-provided v0.2.1 fixed-facts smoke

Later on 2026-08-18, the user supplied a fresh fixed-facts smoke identified as
v0.2.1 behavior. The repository did not independently capture or reproduce the
session. The user-provided transcript supports these named visible checks:

- **Automatic trigger:** `PASS`.
- **Exact headings and order:** `PASS`; **At a glance**, **In context**, and
  **At depth** appeared once and in order.
- **At-a-glance budget:** `PASS`; the section contained 26 words.
- **Cumulative shallow budget:** `PASS`; prose through **In context** totaled
  approximately 50 words.
- **Supplied fixed-fact coverage:** `PASS`.
- **Additivity:** `PASS`.
- **Negative exact-output control:** `PASS`; the response was exactly `323`.

This is a bounded `PASS` for those checks in that smoke only. Fixed-fact
coverage does not establish completeness beyond the supplied facts, and the
negative control does not establish all non-fit behavior. The visible
automatic-trigger pass does not reveal the host's activation trace. The smoke
does not identify the installed portal bytes, erase the separate complex
transcript's failures, or establish universal v0.2.1 conformance.

Package v0.2.1 makes one bounded advisory change: it front-loads the skill
description with default, mandatory ordinary-response trigger language and the
three required views before exclusions. A separate local fixture records five
positive and four non-fit trigger prompts. The current user-provided evidence
shows both a visible automatic-trigger pass and a separate non-conformant
response. Activation therefore remains probabilistic rather than guaranteed.

The [OpenAI plugin packaging and publication record](openai-plugin.md) keeps
the full evidence boundary. Local deterministic packaging and user-reported
upload, installation, publication, or transcript evidence do not clear the
failed Cursor gate or establish general OpenAI compatibility, support, or
release readiness.

## Closed-cycle evidence boundary

- Round-one passes belong to the pre-remediation skill and do not constitute a
  full-suite result for that cycle's final skill.
- That cycle's final-skill targeted failures cannot be averaged with round-one
  passes.
- Historical former-protocol results cannot be combined with either active
  round.
- This record closes the bounded cycle; it does not authorize or imply another
  remediation round.
- No support, compatibility, or release claim follows from the structural
  checks or partial behavioral positives. Publication, the anonymous route
  check, and the user-provided transcript retain their separate evidence
  boundaries.
- The revised protocol, skill, evaluation metadata, and local core are new
  inputs. Their mechanical tests neither reopen the prior remediation cycle nor
  inherit a prior host result.

## Licensing authorization

On 2026-08-17, Firas Kafri explicitly confirmed that he controls the source
draft and authorizes CC BY 4.0 for the protocol and documentation text and
Apache-2.0 for the skill and tooling paths. The
[provenance record](../PROVENANCE.md) documents this representation. Neither
the statement nor Git metadata independently proves copyright ownership or
licensing authority. Licensing authority is no longer tracked as a blocker.

## Remaining verification gaps and limitations

- The preceding Cursor strict-acceptance cycle failed and reached its hard
  stop.
- The revised prompt-only skill has no Cursor or Claude Code host acceptance
  result and no independently executed full ChatGPT acceptance result.
- Live Cursor wrapper execution is evidenced only by the bounded E02-E07
  remediation rerun; it failed overall. Live Claude Code wrapper execution
  remains `UNVERIFIED` because it requires paid Anthropic API access.
- Local mechanical passes do not guarantee completeness, accuracy, warning
  necessity, semantic safe stopping, paraphrased repetition, purposeful depth,
  or hidden-reversal safety.
- The user-reported v0.2.1 upload and installation lack independently captured
  authenticated listing metadata, install records, and portal-byte identity.
- The older historical ChatGPT transcript remains non-conformant, and the
  earlier user-provided pre-v0.2.1 transcript missed the initial three-view
  trigger before producing a stale obsolete-mode explanation.
- The current user-provided complex gold-forecast transcript is
  non-conformant because the 40/200 budgets and additivity failed.
- The fresh fixed-facts smoke passes only its named automatic-trigger,
  headings/order, budget, supplied-fact-coverage, additivity, and exact `323`
  checks. It is not a full-suite or universal-conformance result.
- The bounded smoke's visible automatic-trigger check passed, but prompt-only
  activation remains probabilistic and no host activation trace was supplied.
- The upload, submission, review, approval, portal-validation, security-scan,
  and publication sequence is not independently documented.
- Professional name and trademark clearance remains unresolved.
