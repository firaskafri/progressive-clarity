# Local deterministic enforcement

## Current v0.4 implementation

The current `pc-core` source implements the Mechanical wrapper profile for
Progressive Clarity protocol `0.4`. The wrapper request, model envelope, and
persisted conversation-state schemas are all `3.0.0`. The locally built Python
distribution is `progressive-clarity-core` version `0.4.2`; artifact hashes are
recorded in [Verification](verification.md). This is a local release candidate,
not a published release or host-compatibility result.

The canonical skill and host packages use the separate Advisory conversational
profile. They are prompt-only: they use the visible-conversation topic
heuristic and Focused/Full cadence, but they do not call `pc-core`, maintain its
state, or inherit its mechanical guarantees.

### Certification boundary

```text
trusted wrapper request + committed v0.4 state
                     |
                     v
          resolve topic and presentation
                     |
                     v
            non-streaming host call
                     |
                     v
       schema 3.0.0 / protocol 0.4 envelope
                     |
                     v
             pc-core validation
          | pass                 | fail
          v                      v
 canonical rendering      one complete repair
          |                      |
 atomic state commit       second failure => withhold
```

Presentation policy resolves before the host runs and remains fixed for the
initial candidate and the single permitted repair. Invalid `start`, `continue`,
or `resume` transitions fail before host invocation. After a second invalid
candidate, the wrapper emits no candidate response and leaves committed state
unchanged.

### Trusted wrapper request

`WrapperRequest` schema `3.0.0` has exactly:

```json
{
  "schema_version": "3.0.0",
  "prompt": "Explain the Atlas adoption decision.",
  "topic_id": "atlas",
  "topic_action": "start",
  "turn_kind": "substantial",
  "presentation_request": "auto",
  "controlling_text": null,
  "summary_max_words": null,
  "non_fit_kind": null,
  "required_facts": null
}
```

`topic_action` is:

- `start` for an unknown topic;
- `continue` for the active topic; or
- `resume` for a known inactive topic.

`turn_kind` is `simple_fact`, `ordinary`, `narrow_followup`, `substantial`,
`decision_checkpoint`, `summary_checkpoint`, `material_resynthesis`,
`narrow_correction`, `material_correction`, `clarification`, `quotation`, or
`non_fit`. `presentation_request` is `auto`, `focused`, or `full`.

The caller supplies these classifications as trusted metadata. `pc-core`
checks their structural consistency but does not prove that the caller chose
the semantically correct topic or turn kind.

### Deterministic presentation policy

Purpose-specific shapes resolve first: clarification becomes `control`,
quotation becomes `quotation`, and a non-fit artifact becomes `non_fit`.
Otherwise, an explicit `focused` or `full` request controls the shape. Under
`auto`:

- the first `substantial` response for a topic without a committed overview is
  Full (`views`);
- `decision_checkpoint`, `summary_checkpoint`, `material_resynthesis`, and
  `material_correction` are Full;
- simple facts, ordinary or narrow follow-ups, later substantial turns, and
  narrow corrections are Focused.

A certified topic-wide overview sets `has_committed_overview` for that topic.
An explicit Full rendering of a simple or narrow turn does not mark the topic
as oriented.

The envelope response kinds are:

- `focused`: a direct natural answer without reserved protocol headings;
- `views`: Full output with At a glance, In context, and At depth;
- `control`: one clarification;
- `quotation`: exact controlling text plus a separate summary; and
- `non_fit`: a purpose-specific artifact such as exact output, a complete
  procedure, a transformation, or narrative writing.

### Topic-oriented state

`ConversationState` schema `3.0.0` stores a conversation turn counter, the
active topic ID, and a record for each known topic. Each topic record contains:

- the selected branch;
- the fact ledger;
- host session IDs keyed by host; and
- `has_committed_overview`.

`StoredFact` retains only exact text and the first committed turn. Presentation
placement is response-local: a proposition rendered in Focused output can
later be allocated to the appropriate Full view. State does not permanently
bind a fact to `focused`, `at_a_glance`, `in_context`, or `at_depth`.

Earlier protocol state is unsupported even when it uses schema `3.0.0`. Do not
point v0.4 commands at a v0.3 or v0.2 state file. Preserve old state needed as
evidence and use a fresh path for v0.4, such as
`conversation-state-v04.json`. A missing state file creates the empty v0.4
state; a present file must declare schema `3.0.0` and protocol `0.4`.

Treat state and audit reports as conversation-private because topic records
contain facts and host session identifiers. Use one owner per state path;
concurrent writers are unsupported.

### Validate, render, and wrap

Run from the repository root:

```sh
python3.11 -m pc_core validate candidate.json \
  --state conversation-state-v04.json \
  --request request.json
```

Validation without `--request` is structural inspection only. It cannot certify
the selected topic or presentation and does not produce committable next state.

Rendering requires the trusted request:

```sh
python3.11 -m pc_core render candidate.json \
  --state conversation-state-v04.json \
  --request request.json
```

A requestless render is refused: it exits without writing candidate Markdown
because the result is not certifiable.

Use the non-streaming wrappers when invalid output must be withheld:

```sh
python3.11 -m pc_core wrap \
  --host cursor \
  --request request.json \
  --state conversation-state-v04.json \
  --cwd /path/to/project \
  --report pc-report.json

python3.11 -m pc_core wrap \
  --host claude-code \
  --request request.json \
  --state conversation-state-v04.json \
  --cwd /path/to/project \
  --report pc-report.json
```

For a fresh Cursor workspace, review and accept workspace trust interactively
or explicitly add `--trust-workspace` for the reviewed `--cwd`. The wrapper
never adds Cursor's trust flag implicitly. An optional `--report` path must be
different from `--state` and `--request`; the CLI rejects a possible alias
before host invocation.

### Mechanical guarantees and exclusions

For output labeled `MECHANICALLY_CERTIFIED`, the wrapper checks:

- protocol and schema versions;
- the trusted topic action, selected response kind, target-topic transition,
  branch, turn, and fact-count arithmetic;
- Full view order, non-empty prose, canonical headings, and English 40/200
  budgets when `views` is selected, with structured warnings confined to At a
  glance;
- Focused content and exclusion of reserved protocol headings when `focused`
  is selected;
- exactly one heading-free question sentence when clarification `control` is
  selected;
- response-local fact allocation, stable cross-turn fact identity, declared
  reuse, and exact caller-authoritative fact coverage when supplied;
- correction structure and correction-before-warning rendering, trusted
  quotation bytes and SHA-256, and byte-preserving rendering of accepted
  non-fit payloads; equality to the intended artifact remains `UNVERIFIED`;
- exact normalized lexical duplicate checks, with required verbatim artifact
  bytes exempt; and
- withholding before output plus same-directory atomic state replacement after
  a pass.

These checks do not establish factual accuracy, semantic completeness, the
correctness of caller classifications, semantic fact atomicity or placement,
warning necessity or sufficiency, human safe stopping, whether a recurring
short anchor is necessary, whether a paraphrase restates a complete
proposition, whether At depth ends in a semantic recap, purposeful depth,
hidden-reversal safety, or host behavior outside the wrapper. Those properties
remain Advisory or `UNVERIFIED`.

### Advisory hooks

The project-local Cursor and Claude Code hook templates inspect already
generated Markdown. They remain **Advisory/block-and-retry**, not a
certification boundary. In v0.4, heading-free output is nonblocking because it
may be a valid Focused or purpose-specific response; absence of the three Full
headings is recorded as `UNVERIFIED`, not a mechanical failure. Fenced or
partial reserved headings are also nonblocking because they may belong to an
exact artifact. For an exact three-heading sequence, hooks can reject an empty
view. Budgets and lexical echoes remain `UNVERIFIED` because visible Markdown
cannot identify structured warning, correction, or quotation exceptions.
Cursor handoff reports are conversation-private and are deleted when consumed
by the matching stop event.

Hooks cannot determine whether Focused or Full was the correct policy, certify
topic state, replace output already displayed by Cursor, or provide the
wrapper's fail-closed guarantee.

### Current evidence boundary

No `0.4.2` live ChatGPT, Cursor, or Claude acceptance run exists. User-provided
v0.3.0–v0.3.2 ChatGPT observations do not inherit local wrapper certification
and are recorded as historical evidence in [Verification](verification.md).
Current Advisory activation, topic inference, topic resumption, presentation
selection, and rendered conformance are **UNVERIFIED**. Local mechanics do not
establish host compatibility.

## Historical/superseded v0.3.x enforcement boundary

The v0.3 request, envelope, and state shapes were also schema `3.0.0`, but their
protocol value was `0.3`. Protocol v0.4 rejects those states and candidates
rather than silently applying new semantics. Historical v0.3 package and host
results do not transfer to this wrapper.

## Historical v0.2 documentation and evidence

Everything below this heading is retained as historical v0.2 documentation and
evidence. References to “current,” package v0.2.1, schema 2.x, and dated host
results describe the v0.2 record only; they are not v0.4 instructions or
evidence.

`pc-core` package v0.2.1 is the Python 3.11+ standard-library enforcement path
for protocol v0.2 on local agents. For every ordinary in-scope `views`
response, it buffers model candidates and releases only one canonical response
containing At a glance, In context, and At depth in order after mechanically
decidable checks pass.

ChatGPT does not use this path. Its package remains prompt-only with no backend,
MCP server, hook, or local-state dependency. On 2026-08-18, the user reported
uploading and installing the Advisory v0.2.1 ChatGPT ZIP. The repository did
not independently capture those actions or identify the installed portal
bytes, and the report does not connect ChatGPT to `pc-core`.

## Certification boundary

```text
trusted request + committed state
             |
             v
non-streaming host invocation
             |
             v
schema 2.0.0 JSON envelope
             |
             v
pc-core mechanical validation
       | pass                 | fail
       v                      v
canonical Markdown      one complete repair
       |                      |
atomic state commit      second failure => withhold
```

There are at most two total generation attempts: the initial candidate and one
same-session repair. After a certified turn, the state document persists the
opaque host session ID so the next user turn resumes that same host
conversation. A second failure releases no candidate and leaves local state
unchanged.

## Mechanical guarantees

For output labeled `MECHANICALLY_CERTIFIED`, `pc-core` guarantees:

- exact envelope, request, state, and protocol versions;
- trusted topic identity, new-topic declaration, branch transition, turn
  increment, and fact-count arithmetic;
- exactly At a glance, In context, and At depth in order for a `views`
  response;
- non-empty counted English prose in each required view;
- canonical level-two headings owned by the renderer;
- the normative English counter, 40-word At-a-glance cap, and 200-word
  per-response shallow cap;
- explicit structural separation of warning and correction exemptions;
- correction fields, committed withdrawal IDs, and placement at the start of
  rendered At a glance;
- exact controlling-text equality when trusted text is supplied, its SHA-256,
  and the canonical non-controlling summary label;
- byte-preserving rendering of an accepted `non_fit` payload without an added
  heading or terminal newline; equality to the user's intended artifact remains
  unverified unless separately trusted;
- fact-ID uniqueness, references, immutable prior text/allocation, explicit
  cross-turn reuse, and allocation consistency;
- when the trusted request supplies a non-empty authoritative fact catalog,
  exact ID/text equality and exact normalized catalog text in the visible
  content referenced by each ID;
- exact normalized lexical-duplicate rejection in Progressive Clarity view and
  explanatory prose, including a separate quotation summary, while required
  verbatim artifact bytes remain exempt;
- output withholding until validation passes; and
- same-directory atomic replacement of conversation, fact, and host-session
  state after a pass.

Checks that do not apply to a response kind are reported `NOT_APPLICABLE`, not
`PASS`.

The guarantee covers declared structured data, not its semantic truth.

## Advisory and unverified properties

`pc-core` does not guarantee:

- factual accuracy, completeness, source quality, or model extraction quality;
- whether a caller-supplied authoritative fact catalog is itself correct or
  complete;
- semantic fact atomicity or best-view allocation;
- human safe stopping or warning sufficiency;
- warning indispensability;
- topic or branch intent not supplied as trusted metadata;
- paraphrased or conceptual repetition;
- hidden semantic reversals;
- purposeful At-depth content;
- legal effect or any safety outcome;
- host activation or host-wide compatibility; or
- concurrent writes to one state file.

Near lexical overlap is advisory. No result claims semantic completeness or
hidden-reversal safety.

## Trusted request

Request schema `2.1.0` has exactly:

```json
{
  "schema_version": "2.1.0",
  "prompt": "Explain the Atlas adoption decision.",
  "topic_id": "atlas",
  "new_topic": true,
  "intent": "ordinary",
  "controlling_text": null,
  "summary_max_words": null,
  "required_facts": null
}
```

`intent` is `ordinary`, `targeted`, `correction`, `clarification`, `quotation`,
or `non_fit`. A quotation carries exact trusted `controlling_text` and may
declare `summary_max_words`. The caller explicitly classifies topic continuity;
vocabulary alone is insufficient.

`required_facts` is either `null` or a non-empty caller-authoritative array of
objects with exactly `id` and `text`. When supplied, certification requires
each exact ID and text to be declared and its normalized text to occur in the
visible content referenced by that ID. This closes omission only relative to
the supplied catalog; `pc-core` does not infer missing catalog entries and does
not claim semantic completeness.

## Response envelope and state

The internal candidate has exactly:

```text
schema_version       protocol_version
response_kind        topic_id
new_topic            state
facts                payload
```

`response_kind` is `views`, `control`, `quotation`, or `non_fit`. State declares
turn, branch, and fact counts before and after the candidate. There is no
presentation depth or alternate-behavior state.

Each fact has a stable ID, single-line text, allocation, and optional
`prior_context`, `correction`, or `quotation` reuse reason. A new topic resets
the topic ledger. Unknown fields fail parsing.

Persisted state schema `2.1.0` also stores an opaque session ID per host. State
schema `2.0.0` files require an explicit migration or a new conversation state
path; they are not silently reinterpreted. Treat state and audit reports as
conversation-private because they contain host session identifiers.

## Validate and render

Run from the repository root:

```sh
python3.11 -m pc_core validate candidate.json \
  --state conversation-state.json \
  --request request.json
```

Exit codes are `0` for a mechanical pass, `1` for a mechanical failure, and `2`
for invalid input, state, configuration, or host execution. Reports separate
mechanical and advisory checks and label semantic conformance `UNVERIFIED`.

```sh
python3.11 -m pc_core render candidate.json \
  --state conversation-state.json \
  --request request.json
```

`render` writes no candidate Markdown on failure. Validation without a trusted
request is structural inspection and returns `certifiable: false`.

## Certified wrappers

Cursor:

```sh
python3.11 -m pc_core wrap \
  --host cursor \
  --request request.json \
  --state conversation-state.json \
  --cwd /path/to/project \
  --report pc-report.json
```

Claude Code:

```sh
python3.11 -m pc_core wrap \
  --host claude-code \
  --request request.json \
  --state conversation-state.json \
  --cwd /path/to/project \
  --report pc-report.json
```

The Cursor adapter uses non-streaming Agent CLI JSON in ask mode. The Claude
adapter uses non-streaming print-mode JSON. Repairs resume the same host
session, and certified successive user turns resume the persisted session.
Host authentication, model, permissions, tools, network access, cost, and
timeout remain host-controlled.

A fresh Cursor workspace is not trusted automatically. Review and accept it
interactively first, or explicitly authorize only the configured `--cwd`:

```sh
python3.11 -m pc_core wrap \
  --host cursor \
  --request request.json \
  --state conversation-state.json \
  --cwd /path/to/reviewed/project \
  --trust-workspace
```

Without `--trust-workspace`, the adapter never adds Cursor's `--trust` flag. A
fresh untrusted workspace therefore fails before inference unless the user has
completed Cursor's interactive trust bootstrap.

## Bounded live evidence

One authorized Cursor rerun exercised the session-resume, non-empty-view,
explicit-trust, authoritative-catalog, and fail-closed wrapper fixes against a
frozen pre-trigger-revision skill. Of 17 responses, 10 were mechanically
certified and 7 were withheld after two invalid candidates. `E02`, `E06`, and
`E07` passed; `E03`, `E04`, and `E05` failed. The full behavioral suite
therefore failed, strict semantic and behavioral acceptance remains unmet, and
the result is not a prompt-only acceptance run for the current v0.2.1 skill.

The preserved evidence is under
`/private/tmp/progressive-clarity-v02-cursor-live-5f9f7881/evidence/remediation-live-20260818`.
Live Claude Code wrapper behavior remains `UNVERIFIED`: its argv and result
parsing are structurally tested, but inference requires paid Anthropic API
access and no paid live run was completed.

The current ChatGPT evidence is separate from local enforcement. On
2026-08-18, a user-provided complex gold-forecast transcript triggered the
three-view structure but failed the 40/200 budgets and additivity, so it is
non-conformant. A later fresh fixed-facts smoke passed automatic trigger, exact
headings/order, a 26-word At a glance, approximately 50 cumulative shallow
words, supplied-fact coverage, additivity, and a negative exact-output control
whose response was exactly `323`. That smoke passes only those named checks.
Neither transcript was independently captured or reproduced. Neither
identifies the installed portal bytes or inherits this wrapper's mechanical
certification.

## Reusable host interface

`pc_core.adapters.HostAdapter` is the host-neutral boundary:

```python
class HostAdapter(Protocol):
    name: str

    def generate(
        self,
        prompt: str,
        *,
        session_id: str | None = None,
    ) -> HostCandidate:
        ...
```

Cursor and Claude Code are the only concrete adapters. The interface can host a
future Codex adapter after its official non-streaming result and resume
contracts are verified. This repository does not claim Codex support.

## Project-local advisory hooks

Reference templates are:

- `adapters/cursor/hooks.json`;
- `adapters/claude-code/settings.json`.

They are not installed and modify no user-global settings. Merge only the
selected template into project configuration after the project-local
`.pc-core/venv` install described in [Installation](installation.md). The
relative hook commands intentionally fail when that reviewed runtime is absent;
they do not fall back to a global `pc_core` import.

Cursor `afterAgentResponse` can inspect completed text but cannot replace or
suppress it. Cursor `stop` can submit one follow-up, not retract displayed
output. Claude Code `Stop` can block once with a reason but runs after response
generation; display replacement is not a reliable fail-closed transcript gate.

Both templates are therefore **Advisory/block-and-retry**. Use the wrappers
when invalid output must be withheld.

## Official capability sources

Checked on 18 August 2026:

- [Cursor Hooks](https://cursor.com/docs/hooks);
- [Cursor CLI output format](https://cursor.com/docs/cli/reference/output-format)
  and [parameters](https://cursor.com/docs/cli/reference/parameters);
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks);
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference);
  and
- [Claude Code headless mode](https://docs.anthropic.com/en/docs/claude-code/headless).
