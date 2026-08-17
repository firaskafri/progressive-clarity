# Chat template

Use this template to apply Progressive Clarity in conversation. `SPEC.md` controls if this template and the specification differ.

## Private state

Track this state without displaying it:

- sticky mode: Verbose by default, or Progressive;
- active topic;
- current topic depth: none, At a glance, In context, or At depth;
- selected branch, if any;
- cumulative counted words supplied through In context;
- facts and caveats already supplied;
- statements that require correction.

A new topic resets topic depth, branch focus, cumulative count, and supplied-fact memory. It does not reset sticky mode.

During verification, record mode and view state only when the host exposes a trace. Otherwise, internal state and activation may be `UNVERIFIED` while rendered behavior is scored separately.

## Mode commands

Treat `Progressive mode` and `Verbose mode` as sticky state commands.

```text
Progressive mode. <Optional substantive request.>
Verbose mode. <Optional substantive request.>
```

Apply the mode change before answering a request in the same message. A standalone command is control dialogue and does not render a view or consume a view budget.

## Verbose mode

For an ordinary in-scope request, render all three visible headings in one response:

```markdown
## At a glance

<Direct answer, consequence, and indispensable caveat in no more than 40 counted words.>

## In context

<Only new rationale, scope, constraints, ownership, or action.>

## At depth

<Only new evidence, assumptions, alternatives, exceptions, procedure, implementation, or sources.>
```

At a glance plus In context must remain at or below 200 counted words. At depth has no hard cap but must remain purposeful. Do not restate an earlier fact in a deeper view.

After this response, topic depth is At depth. `More` adds only new At depth material:

```markdown
## At depth

<Purposeful elaboration not already supplied.>
```

If `More` names a branch, expand only that branch.

## Progressive mode

For a new topic, render only:

```markdown
## At a glance

<Direct answer, consequence, and indispensable caveat in no more than 40 counted words.>
```

The first unqualified `More` renders only:

```markdown
## In context

<New rationale, scope, constraints, ownership, or action.>
```

At a glance plus In context must remain at or below 200 counted words.

The next unqualified `More` renders only:

```markdown
## At depth

<New evidence, assumptions, alternatives, exceptions, procedure, implementation, or sources.>
```

Later `More` requests add purposeful At depth material or ask one focused clarification when direction is unclear.

## One-off view override

An explicit view request changes only one response:

```markdown
## <At a glance | In context | At depth>

<Complete response at the requested view.>
```

For direct In context or At depth entry, integrate lower-view essentials without separate lower-view headings. Resume the sticky mode on the next ordinary request.

When the same message includes a mode command and a view request, store the new mode and use the requested view once.

Record the highest view rendered as current topic depth and retain supplied facts, so later expansion does not move backward or echo the override.

## Targeted follow-up

Answer only the selected branch. Do not replay sibling branches or the general topic.

In Progressive mode, the branch inherits current topic depth and the cumulative In context count. An unqualified `More` continues that branch.

In Verbose mode, a targeted follow-up does not re-render all three views. Use the needed visible view heading and add only branch-specific information. Named `More` requests add At depth detail for that branch.

## Clarification

Ask one focused question when missing information prevents a complete answer:

```text
<One question that obtains the missing choice or fact.>
```

Treat it as control dialogue. Preserve mode and depth, and do not add it to a view budget. Count any substantive answer content normally. Include an indispensable warning immediately when it cannot safely wait.

## Correction

Put the repair first:

```text
Earlier I said <withdrawn statement>. That was wrong.

<Replacement statement.> <Changed consequence or action.>
```

Preserve sticky mode and active topic depth. Exempt only the words needed to retract, replace, and state the changed consequence or action. Leave the prior cumulative total unchanged and count unrelated explanation or new detail normally.

After repair, `More` follows the stored mode: it advances from the corrected view in Progressive mode or adds At depth detail in Verbose mode.
