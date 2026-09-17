# Directory submission materials

Use these reviewed values for directory submissions. Platform forms remain the
authority for field limits and required attestations.

## Listing

- Name: `Progressive Clarity`
- Package name: `progressive-clarity`
- Version: `0.5.0`
- Category: Productivity
- Publisher: `FIRAS HASHEM AHMAD AL KAFRI` where the platform requires the
  verified legal identity; `Firas Kafri` where a display name is accepted.
- Website: <https://firaskafri.com/progressive-clarity/>
- Support: <https://firaskafri.com/contact/>
- Privacy: <https://firaskafri.com/progressive-clarity/privacy/>
- Terms: <https://firaskafri.com/progressive-clarity/terms/>
- Source: <https://github.com/firaskafri/progressive-clarity>
- License: Apache-2.0 for the packaged Skill.
- Short description: `Orient, explore naturally`
- Long description: `Answer directly with important qualifications up front.
  Keep ordinary follow-ups and compact decisions focused; use At a glance, In
  context, and At depth when distinct layers help. Topic inference and semantic
  quality remain advisory.`

Progressive Clarity is an instruction-only plugin. It includes no MCP server,
remote service, authentication, analytics, telemetry, or user-data collection.
The host still processes conversations under its own terms and privacy policy.

## Starter prompts

1. `Summarize this project update for leadership, collaborators, and
   implementers.`
2. `Explain OAuth 2.0 PKCE so a manager understands the decision and an
   engineer gets the implementation detail.`
3. `Compare PostgreSQL and DynamoDB for this workload and recommend one with
   trade-offs.`
4. `Summarize these market forecasts with the central estimate, assumptions,
   risks, and supporting evidence.`
5. `Turn these notes into a decision-first proposal with context, constraints,
   next actions, and detailed evidence.`

These are the examples in the Claude submission that passed review.

## Positive review cases

### Direct factual answer

Prompt:

> Is Redis a database? Answer only the classification and one persistence
> distinction; do not list data structures or use cases.

Expected behavior: answer directly in one to three sentences without protocol
headings, a use-case catalog, or anticipation of later questions.

### Qualified architecture decision

Prompt:

> Our architecture decision is that Redis must not be the sole source of truth
> for payment state; canonical state belongs in a transactional database.
> Explain this decision in all three views, including the rationale and a
> concrete cache-loss test.

Expected behavior: render At a glance, In context, and At depth in order;
preserve the transactional-database boundary and add rationale and testing
detail without reversing the opening conclusion.

### Missing decision context

Prompt:

> Should I enable the index now?

Expected behavior: ask for the decisive environment, validation, and rollback
context rather than inventing approval.

### Safety-critical recommendation

Prompt:

> Should I restart the payment primary? Both primary and replica are writable.
> Restart can lose acknowledged payments. Freeze writes first. Resume only
> after authoritative state is established, transactions are reconciled,
> fencing is confirmed, and recovery is validated. Explain in all three views,
> including evidence and diagnostics.

Expected behavior: put the do-not-restart conclusion and immediate freeze
instruction first, preserve every supplied recovery condition, and add
diagnostic detail only after the indispensable warning.

### Evidence-bounded comparison

Prompt:

> Help our school committee choose an event venue and understand the tradeoffs
> and next steps. We require step-free access and an indoor fallback. The
> garden has step-free access but no indoor fallback; the hall has both. Both
> are within budget and available on our event date. Explain which venue fits,
> why, and what evidence to confirm before booking. Do not assume other venue
> features.

Expected behavior: recommend the hall from the supplied criteria, distinguish
known facts from checks still required, and avoid inventing venue features.

## Negative review cases

### Exact-output request

Prompt:

> Reply with exactly `323`.

Expected behavior: return exactly `323`; do not add headings, explanation, or
plugin commentary.

### Narrative request

Prompt:

> Write a first-person scene about opening an unfamiliar door, with no
> headings.

Expected behavior: preserve the requested narrative form without protocol
headings or a conclusion-first summary.

### Complete procedure request

Prompt:

> Using only this supplied high-level sequence, write the complete restore
> procedure without asking for system-specific details: block writes; verify
> checksum and stop on mismatch; restore; cut over; reopen writes.

Expected behavior: preserve a complete ordered procedure and its safety branch;
do not replace it with the three-view explanatory format.

## Release notes

> Progressive Clarity 0.5.0 introduces usefulness-based presentation. It
> answers ordinary and compact consequential requests directly, and uses At a
> glance, In context, and At depth when separate levels provide useful
> information. It shortens the canonical Skill, keeps corrections and
> clarifications natural, and preserves explicit assumptions and indispensable
> safety qualifications. The plugin remains prompt-only and advisory, with no
> MCP server, remote service, authentication, analytics, or data collection.

## Platform status

- Claude: review passed for source revision
  `f34fbf03ba644f7b86d6c9413504878d4f76762b`; public community catalog
  synchronization remains pending.
- OpenAI: authenticated portal status has not yet been verified for `0.5.0`.
- Public website privacy and terms pages are implemented in the deployment
  repository but must be deployed and verified before supplying those URLs to
  OpenAI.
