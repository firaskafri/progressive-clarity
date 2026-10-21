# Acceptance repair candidate — 0.5.1-rc.7

Unpublished candidate `0.5.1-rc.7` retains the numeric, follow-up,
silent-application, and prerequisite guidance from rc.6. It adds narrow repairs
for failures and proportionality concerns already documented in the development
suite:

- a mandatory failed gate ends at meeting the gate unless the user supplies an
  authorized exception route;
- pure updates state only the changed fact;
- supplied conversational entity facts are not reinterpreted through workspace
  searches;
- reserved Full headings remain literal;
- corrections name both the earlier value and its replacement;
- blocked agreement decisions request the agreement and decision criteria
  without a speculative legal checklist; and
- evidence-bounded comparisons retain all supplied facts without inventing
  additional tradeoffs.

These are development changes, not proof of generalization. Earlier rc.5 and
rc.6 results remain historical and must not be relabeled as rc.7 evidence.

## Fresh complete round — 2026-10-21

The frozen development suite completed all 44 responses in 22 fresh sessions
with Cursor Agent, requested model `gpt-5.2`, Ask mode, the exact rc.7 body in
an always-applied project rule, concurrency three, no retries, and no in-round
revision. All commands completed.

Strict visible-output review produced **12 PASS / 10 FAIL / 0 UNVERIFIED** case
runs. Presentation shape matched 43/44 responses; T03 turn 2 incorrectly used
Full headings for a pure update. Failures were:

- T02: unsupplied gate-revision and override routes;
- T03: full plan rewrite and unsupported “unchanged” claims;
- T04 runs 2 and 3: the material correction did not identify the earlier
  Tuesday production-coverage value;
- T07: controlling text used `Summary` instead of the required literal
  non-controlling label;
- T09: added operational specifics despite the supplied-sequence-only request;
- T10: reinterpreted conversational entities as technical products and added
  unsupported status facts;
- T15: expanded a two-input clarification into a speculative legal checklist;
- T16: inferred unsupported Beacon approval facts and over-answered an ambiguous
  reference; and
- T18: omitted the supplied shared budget and date-availability facts.

T01, T04 run 1, all three T05 runs, T06, T08, T11–T14, and T17 passed their
bounded case contracts. These passes do not override the failures.

**Outcome: release acceptance failed.** The repository permits one remediation
cycle after review. Do not publish, tag, submit, deploy, or relabel rc.7 as
stable `0.5.1`. Further work requires a new reviewed development plan rather
than another immediate prompt-tuning cycle.

The user subsequently requested remediation. A separate reviewed
[rc.8 development plan](release-candidate-rc8.md) preserves this round and freezes
bounded debugging before any new complete acceptance round. rc.7 is not relabeled.
