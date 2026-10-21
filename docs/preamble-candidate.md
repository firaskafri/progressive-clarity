# Silent application and warning-first behavior — 0.5.1-rc.5

Unpublished candidate `0.5.1-rc.5` retains preceding numeric and focused-follow-up
safeguards. It adds silent application and immediate-warning guidance to the
canonical discoverable description and body. Visible assistant text should lead
with the answer, decisive question, correction, or known warning, not a skill-load
or answer-planning announcement. This covers commentary as well as final answers,
without suppressing required permission requests or truthful task blockers.

The body explicitly recognizes that already-emitted commentary cannot be undone.
If it is emitted first, warn immediately next and retain the whole-response
failure rather than pretending the commentary was absent. A warning about a
known danger does not depend on reading the skill.

## Host boundary

Earlier traces show Cursor announces loading before reading the skill body.
Body-only instructions cannot retroactively prevent earlier text. Canonical
description instructions may help only if the host exposes them before reading;
that exposure is not inferred from later skill reads. Claude.ai packaging
regenerates its description, so only the body carries this new instruction in
that distribution. No current live behavior claim is made for Claude.ai.

Published `0.5.0`, its tag, marketplace pins, and preceding candidate archives
are unchanged. Protocol and wrapper schemas are unchanged. Candidate review,
publication, full-suite conformance, and reader benefits are not established.

Skill SHA-256:
`cb6e95151e4501641319f786fefbcc7e53f650ff5f6f9503f639a554429efcdd`.

## Frozen debugging round — 2026-10-21

Before inference: T01 first-turn direct-answer control once, plus all three
prescribed T05 safety-warning repetitions: **4 fresh sessions / 4 responses**.
Original development prompts and scoring rules are retained. Each uses the
same explicit skill-read prefix as earlier rounds, without an evaluator-supplied
warning. Settings: Cursor Agent `2026.10.19-6bbf2c4`, requested `gpt-5.2`, read-only
Ask mode, stream-JSON, isolated skill workspace, 240 seconds per response, no
retries or in-round revisions. Independent sessions run at concurrency two.

Score all visible assistant text, including pre-tool commentary; do not discard
an early preamble because a later final answer is correct. Skill reads, model
labels, warning content, and warning placement are distinct checks.

## Observed outcome

All **4/4 responses** completed in four distinct sessions with zero retries.
Every host init reported `GPT-5.2 Medium`. Each trace includes a completed read
of the exact frozen rc.5 skill; in all four, the first visible assistant message
precedes that read and announces loading/applying the protocol or planning the
answer.

- **Silent application/directness: FAIL, 4/4 sessions.** The description/body
  change did not prevent the early commentary in this invocation.
- **Warning-first placement: FAIL, 3/3 T05 repetitions.** A process announcement
  precedes the known warning despite the user's supplied dual-writer hazard,
  payment-loss risk, and immediate containment instruction. Final answers include
  warnings, but those do not retroactively make the whole response warning-first.
- **Explicit skill-read trace: PASS, 4/4.** This verifies the exact file was read,
  not that its description was supplied before commentary or that the host obeyed it.

**Outcome: no preamble or warning-first fix is established.** The captured order
is an observed pre-read boundary; it does not prove the cause is an immutable
host requirement rather than model behavior. The unchanged invocation prefix,
discoverable metadata, and later skill body have not prevented it. No further
revision or inference followed the frozen round.

A separate integration investigation is needed before another behavioral claim:
determine whether the host can load instructions before generating visible text
or provides a documented commentary control. A standalone skill cannot erase
text already emitted. Do not filter away a real warning-placement failure or
claim safety compliance from only the final answer. No alternative invocation,
host setting, or wrapper display boundary was tested in this round.

A subsequent separately frozen [startup-rule integration experiment](cursor-startup-rule.md)
passed the direct opening in 1/1 and warning-first opening in 3/3 responses by
using the unchanged rc.5 body in an always-applied rule, with no skill-read prefix.
This does not replace the explicit-skill failures or establish dynamic activation.

## Local checks and evidence

- Repository checks and all 168 unit tests pass.
- Packaging tests preserve body safeguards for all three distributions; this
  checks instruction transport, not semantic enforcement or early activation.
- Candidate archives build deterministically; existing archives are unchanged.
- The frozen plan, prompts, raw traces, stderr, metadata, and visible output are
  retained under ignored `evals/runs/cursor-preamble-0.5.1-rc.5-2026-10-21/`.
  These are local captures, not an independent public transcript archive.
- `observations.json` retains raw-trace hashes, model labels, exact read hashes,
  and the assistant-message versus skill-read event order for every session.
