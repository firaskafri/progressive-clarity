# Cursor v0.5 bounded smoke — 2026-10-21

## Scope and identity

This is a development smoke, not full-suite acceptance, an unseen holdout,
official-directory installation evidence, or a reader-outcome study.

- Host: Cursor Agent CLI `2026.10.19-6bbf2c4` on macOS.
- Requested model: `gpt-5.2`; host-reported model: `GPT-5.2 Medium`.
- Mode: read-only `ask`, with `stream-json` capture.
- Installation: complete canonical skill copied into `.agents/skills/` in an
  isolated temporary workspace. Only that workspace was explicitly trusted.
- Skill SHA-256:
  `38b1466a3036e639a98824c4b5e4ea71918fda7a5844c82d8c597a2c090cea4c`.
- Development-suite SHA-256:
  `b1afbd91172c1786dbffc42551d87b6db069b742c3ff5f270e1ef93b2bcdc19a`.
- Frozen scope: T01 once, T04 three times, T05 three times, T11 once, and an
  additional exact-output control S01 once: **9 sessions / 18 responses**.
- All turns of a case run resumed the same session. Each case run began fresh.
- Per-response timeout: 120 seconds; no retries, skill revisions, or remediation.

The first turn of each development case was prefixed with:

> Read .agents/skills/progressive-clarity/SKILL.md and apply Progressive Clarity
> to this conversation. Do not describe loading the skill; answer the request
> directly.

S01 had no prefix and asked only: ``Reply with exactly `323`.`` It tests exact
output in a fresh workspace session, not exact output after explicit skill load.

## Observations

All **18/18** responses completed successfully. The eight explicitly invoked
sessions each exposed a completed read of the exact canonical skill. No tool
calls other than those eight reads were captured. This verifies explicit file
loading, not automatic activation, hidden topic state, or other hosts.

The evaluator reviewed all visible assistant messages, including pre-tool
commentary, rather than only the final answer. Evaluator judgments below are
not independent human research or exhaustive semantic certification.

| Check | Observation |
| --- | --- |
| Explicit skill load | **PASS, 8/8 sessions**: completed skill reads are visible in the host trace. |
| Exact output S01 | **PASS, 1/1**: sole assistant text is `323`; no tool calls. |
| Requested Full structure | **PASS, 8/8 responses**: the three required top-level headings appear once and in order. This does not certify additivity or warning-first behavior. |
| T01 numeric follow-up | **FAIL, 1/1**: recommends “24 hours (minimum)” and “7 days” without the provider retry window; calls seven days a “common safe default.” |
| T01 handoff synthesis | **FAIL, 1/1**: carries those unsupported numbers into the summary and says to start with seven days if the replay window is unknown. |
| T04 narrow repair | **FAIL, 3/3**: supplies Wednesday with a generic “Correction” or “Corrected” label, but never explicitly identifies the earlier Tuesday review-date error. |
| T04 material repair | **FAIL, 3/3**: supplies Thursday but never explicitly identifies the earlier Tuesday production-coverage error. Run 2 does not label the change as a correction. |
| T05 warning content | **PASS for the named content check, 3/3**: At a glance prohibits restart, names dual writers and payment-loss risk, requires freezing writes, and retains authority, reconciliation, fencing, and validation before resumption. |
| T05 warning placement | **FAIL, 3/3**: visible planning/loading commentary precedes the indispensable warning. Safety qualifications belong first in the whole visible response. |
| First-turn directness | **FAIL, 8/8 explicitly invoked sessions**: commentary about loading/applying the protocol precedes the answer despite the no-loading-commentary instruction. |

T01 turn 1's final answer correctly classifies Redis and notes optional
persistence, but its preceding loading commentary prevents a directness pass.
T11's final answer says not to release while the gate is unmet; it does not
authorize release and conditions any exception on an existing policy process.
Its loading commentary still prevents a directness pass.

Full-response prose counts were recorded separately. Counts include warning
text; no warning-exemption classification was performed. In the non-warning
Full answers, At a glance exceeded the provisional 40-word target in T01
turns 2 and 4 and T04 run 1 turn 3; cumulative shallow prose exceeded 200 in
T01 turn 2 and T04 run 3 turn 3. These Advisory target deviations alone are not
conformance failures and do not measure reading time.

## Evidence and outcome

Local raw evidence is retained under the ignored directory
`evals/runs/cursor-smoke-2026-10-21/`: the pre-run plan, exact prompts, raw JSONL
traces, stderr, per-response metadata, extracted visible Markdown, and
`observations.json` with raw-trace hashes and word counts. These local files are
not bundled with the public repository; this summary is not an independently
reproducible public transcript archive.

**Outcome: current Cursor behavior observed, with named conformance failures.**
No whole-suite acceptance or general host-support claim is established. The
approved v0.5 package bytes were not changed. Stop after this frozen round and
review the failures before authorizing a separate revision or further inference.
