# Protocol v0.2 and package v0.2.1 scope and limitations

Progressive Clarity protocol v0.2 and package v0.2.1 are a non-release-ready
draft with one ordinary response contract only: one response renders At a
glance, In context, and At depth together in that order. The prompt-only skill
is Advisory. The optional local wrapper gates only mechanically decidable
properties.

[`SPEC.md`](../SPEC.md) is normative. Templates, examples, installation
guidance, and document adaptation are informative when they differ.

## What v0.2 covers

- three additive views in every ordinary in-scope response;
- a 40-word non-warning At-a-glance cap;
- a 200-word per-response non-warning cap through In context;
- purposeful unrestricted At depth;
- no fact-only repetition across views;
- topic and targeted-branch focus;
- focused clarification control dialogue;
- explicit correction;
- safety, legal, exact-text, procedure, and narrative exceptions;
- Advisory prompt-only packaging; and
- an optional Enforced mechanical envelope, renderer, state store, and
  two-total-attempt wrapper.

There is no alternate presentation behavior, depth progression, view override,
or cross-turn shallow-word accumulation.

## Mechanical certification is narrow

For wrapper-buffered output, `pc-core` can guarantee schema/version checks,
trusted topic/branch/turn arithmetic, exact three-section order, deterministic
English counts, non-empty required-view prose, declared warning/correction
separation, fact-ID consistency,
exact trusted quotation bytes and hash, exact lexical-duplicate rejection for
Progressive Clarity view and explanatory prose while required verbatim artifact
bytes remain exempt, byte-preserving accepted non-fit payload rendering,
canonical view rendering, bounded attempts, cross-turn host-session resume, and
atomic local state commit. When a trusted request supplies a non-empty
authoritative fact catalog, it also guarantees exact normalized visible
coverage of those supplied IDs and texts.

It cannot guarantee:

- factual accuracy, completeness, or source quality;
- completeness or correctness of a caller-supplied authoritative fact catalog;
- semantic fact atomicity or correct allocation;
- actual human safe stopping;
- warning necessity, sufficiency, or safety outcome;
- paraphrased repetition or hidden semantic reversal;
- purposeful At-depth content;
- intended topic or branch beyond trusted metadata;
- host activation or general host behavior; or
- concurrent access to one state file; or
- an atomic transaction spanning state replacement and downstream stdout,
  transcript display, or host-side effects; or
- rollback of remote host-session history after a withheld turn.

Those properties remain Advisory or `UNVERIFIED`. A mechanical pass is not
semantic certification.

## English-only budgets

Version 0.2 makes no budget-conformance claim for non-English or mixed-language
responses. The exact ordered Markdown transformations and ASCII-letter/digit
token rule are normative in `SPEC.md`. Warning and correction exceptions do not
permit omission of required facts.

## No host support claim

One bounded live Cursor wrapper rerun records v0.2 mechanical behavior for
E02-E07. Of 17 responses, 10 were mechanically certified and 7 were withheld;
`E02`, `E06`, and `E07` passed, while `E03`, `E04`, and `E05` failed. The rerun
exercised the mechanical wrapper fixes against the pre-trigger-revision skill,
but it failed the full behavioral suite. Strict semantic and behavioral
acceptance remains unmet, and the result does not establish general Cursor
compatibility or current-v0.2.1 prompt-only conformance.

No current-revision prompt-only run establishes that Cursor, Claude Code,
ChatGPT, Codex, or another host follows v0.2. Standard Agent Skills packaging
is a portability choice, not compatibility evidence.

The generic host interface is designed for future local adapters. Codex support
is not claimed or tested.

## Historical evidence boundary

The preceding bounded Cursor cycle belongs to older dual-behavior inputs. Round
one completed 21 fresh sessions and 39 responses: 6 cases passed and 5 failed.
The single permitted targeted remediation round completed 9 sessions and 20
responses; all 5 rerun cases failed. All 59 budget checks passed, and neither
round had a safety-warning or procedural-safety failure. The mandatory hard
stop was reached. These observations neither establish safety nor verify v0.2.

Claude Code's older attempt stopped before inference with insufficient API
credit. Its hook and adapter are structurally tested, but current prompt-only
and live wrapper behavior remain `UNVERIFIED` because a live run requires paid
Anthropic API access.

On 2026-08-17, the user reported publication of an older ChatGPT plugin as
[`plugins_6a82efdddbb48191b2785354515e1be2`](https://chatgpt.com/plugins/plugins_6a82efdddbb48191b2785354515e1be2).
An anonymous fetch confirmed only that the login-gated route exists. The URL
is historical publication evidence and does not establish that the Advisory
v0.2.1 ZIP was uploaded; it has not been uploaded in this work.

The user also supplied a transcript they identified as a live interaction with
the published older build. It was not independently captured. Its historical
visible results were:

- default three-view rendering in order: `PASS`;
- older staged acknowledgment and transitions: `PASS`;
- safe stopping and caveats: `PASS`;
- At-a-glance budgets: `FAIL` — gold approximately 103 prose words; silver
  approximately 210, excluding tables and citations;
- prose through In context: `FAIL` — gold approximately 330+ words; silver
  approximately 600+;
- additivity and no fact-only repetition: `FAIL`; and
- switch-back acknowledgment: observed, while subsequent behavior remained
  `UNVERIFIED`.

A later user-provided transcript, captured before the v0.2.1 trigger-recall
patch, omitted the initial three-view response and then described removed
presentation modes. The repository did not independently capture either
session or identify the installed portal bytes.

That ChatGPT behavior is **historical, observed, and non-conformant**. It is not
current v0.2.1 evidence and does not verify financial facts, activation,
compatibility, or support.

## No empirical reader-outcome claim

Safe stopping is an evaluation proxy based on required facts and caveats. It
does not establish what a human understood, remembered, believed, or did.
There is no formal participant study or validated claim of improved
comprehension, decision quality, accessibility, safety, productivity, reading
time, or token use.

## Security and operational exclusions

The Advisory skill and ChatGPT ZIP are instruction-only and contain no runtime,
network dependency, analytics, or tool grant. This is not a host security
certification.

The separate local `pc-core` uses Python 3.11+ standard library code, starts no
service, configures no MCP server, and changes no user-global settings. It
requires one owner per conversation state path. Host subprocesses run without a
shell and under a per-attempt timeout, but host-managed tools, descendants, and
side effects remain governed by the selected host rather than rolled back by
`pc-core`. Cursor workspace trust is never added implicitly: a fresh workspace
requires either an interactive trust decision or the wrapper's explicit
`--trust-workspace` option for the reviewed path.

Protocol v0.2 and package v0.2.1 do not include an automated
installer/updater, hosted AI service, semantic oracle, formal participant
research, or independently verified ChatGPT listing/install/activation record.
Professional name and trademark clearance remains unresolved.
