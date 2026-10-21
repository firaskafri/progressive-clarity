# Cursor startup-rule full development round — 2026-10-21

**Outcome: completed execution, not acceptance.** The unchanged rc.5 startup-rule
profile produced all 44 prescribed responses across 22 distinct sessions, with
no execution errors, timeouts, retries, or in-round instruction revisions.
Visible failures prevent a whole-suite conformance claim.

## Frozen setup

- Cursor Agent `2026.10.19-6bbf2c4`, requested model `gpt-5.2`, read-only Ask mode,
  stream-JSON capture, 240 seconds per response, concurrency three.
- Original development suite: 18 cases, 22 sessions, 44 responses. T04 and T05
  each ran three times. Turns within each run resumed one session; runs began fresh.
- Every run used a separate temporary workspace containing one `.mdc` rule with
  `alwaysApply: true` and the exact rc.5 body. No Skill directory or explicit
  skill-read prefix was used. Only those temporary workspaces were trusted.
- Canonical skill SHA-256:
  `cb6e95151e4501641319f786fefbcc7e53f650ff5f6f9503f639a554429efcdd`.
- Suite SHA-256:
  `b1afbd91172c1786dbffc42551d87b6db069b742c3ff5f270e1ef93b2bcdc19a`.
- Protocol SHA-256:
  `a7f15f4d7ebd5c451a465923cc4ba44b8eb48e046ac34d42ef119c6ae03be236`.

Session continuity, all workspace rule hashes, and raw-trace hashes were checked.
Host model labels are retained per response; a stable requested model does not
certify hidden settings. Rule injection is documented, not exposed as a trusted
activation trace. No hidden topic state or dynamic Skill activation is claimed.

## Review boundaries and results

A later [assumptions audit](evaluation-assumptions-review.md) identified ambiguity
in T06's expected enablement and T02's waiver scoring. The totals below are
historical conservative evaluator labels, not independently adjudicated frozen-
rubric conformance rates. No raw output was changed or silently rescored.

All visible assistant messages were retained, including tool commentary. Heading
checks alone yielded **38 PASS / 5 FAIL / 1 UNVERIFIED** across 44 responses:
T03 turn 2, T05 run 3, T10 turns 2 and 3, and T15 failed exact shape checks;
adaptive T18 requires semantic review rather than fixed-heading classification.
These are heading checks, not full presentation or semantic passes.

Conservative evaluator review yielded **4 PASS / 12 FAIL / 6 UNVERIFIED case
runs** (22 total). PASS is limited to the supplied case requirements; no exhaustive
independently adjudicated fact-by-fact score or participant study was completed.
UNVERIFIED is not a pass. The review notes below retain observable violations
without certifying all unmentioned claims or detailed operational commands.

| Case | Runs | Judgment | Evidence |
| --- | --- | --- | --- |
| T01 | 1 | UNVERIFIED | Focused TTL follow-up gives a relationship and asks for provider/retry inputs; broader Full-answer additivity and semantic correctness are not fully adjudicated. |
| T02 | 1 | FAIL | Offers a leadership risk-waiver shipping route without supplied authority to bypass the reliability gate. |
| T03 | 1 | FAIL | Turn 2 rewrites an ordinary date update in Full and says gates stay identical before the user confirms controls in turn 3. |
| T04 | 3 | FAIL, 3/3 | Replacements omit explicit identification of earlier Tuesday errors; run 3 also adds unsupplied calendar dates. |
| T05 | 3 | FAIL, 1/3; UNVERIFIED, 2/3 | Warning-first openings appear in all three. Run 3 changes the exact heading to `At depth (evidence + diagnostics)`. Exhaustive safety of diagnostic/recovery instructions remains unverified in the other runs. |
| T06 | 1 | FAIL | Authorizes repository indexing without asking environment, validation, or rollback. Later answer omits explicit staging-not-production approval boundary. |
| T07 | 1 | FAIL | Reproduces source, but uses `Summary` instead of the required non-controlling summary label. |
| T08 | 1 | PASS | First-person narrative, no protocol headings or conclusion-first summary. |
| T09 | 1 | PASS | Complete ordered restore sequence and checksum-stop branch, with no blocking clarification. |
| T10 | 1 | FAIL | Full structure appears in focused topic switch/return; asks which Beacon despite supplied discovery status. |
| T11 | 1 | UNVERIFIED | Refuses release, but conditional exception discussion needs further policy/semantic review. |
| T12 | 1 | UNVERIFIED | Immediate no-touch/isolation warning; added breaker advice needs independent safety review. |
| T13 | 1 | PASS | Missing-input formula, then supplied 48h + 12h = 60h; whole-day rounding is explicitly conditional. |
| T14 | 1 | PASS | Identifies affected order and supplies complete build → validate → publish repair. |
| T15 | 1 | FAIL | Full legal triage replaces the expected focused/control request for decisive missing agreement inputs. |
| T16 | 1 | FAIL | Searches empty workspace and announces process; rejects supplied Beacon discovery status as insufficient. |
| T17 | 1 | UNVERIFIED | Freeze qualification retained; lengthy repetition and optional freeze relaxation need independent semantic review. |
| T18 | 1 | FAIL | Correct hall choice, but supplied budget/date facts are not retained and unsupplied aesthetic/weather tradeoffs are introduced. |

The T05 breakdown is conservative: only run 3 has the named exact-heading failure;
the other two runs are unverified for exhaustive semantic safety.

Prose and whole-output counts are retained separately, including warning text
without warning-exemption adjudication. Advisory 40/200 targets do not alone
fail conformance and are not reading-time measures. Long answers, repeated
explanations, and unsolicited context remain review concerns even with valid headings.

## What this establishes

The small startup-rule opening experiment did not generalize to all development
tasks. T16 generated process commentary and workspace searches despite supplied
facts; T06 inferred a coding-tool index rather than asking for the missing context.
The host's coding orientation and rule behavior must not be mistaken for a fully
verified general conversational assistant.

No candidate input, published archive, marketplace pin, or global setting changed
during this round. No remediation or rerun was performed afterward. Review before
any new candidate; after a revision, freeze a new full development round. Do not
tune on a holdout while calling it unseen.

Local evidence: ignored `evals/runs/cursor-startup-full-rc5-2026-10-21/` contains
the pre-run plan, exact prompts, raw JSONL, stderr, metadata, visible Markdown,
hash/count observations, and conservative assessments. It is not an independent
public transcript archive. Unit tests and package checks remain distinct from
live semantic conformance and reader outcomes.
