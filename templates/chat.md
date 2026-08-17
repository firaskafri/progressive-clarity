# Chat template

Use this template to apply Progressive Clarity in conversation. `SPEC.md` controls if this template and the specification differ.

## Private state

Track this state without displaying it:

- active topic;
- current view: none, At a glance, In context, or At depth;
- selected branch, if any;
- cumulative counted words supplied through In context;
- facts and caveats already supplied;
- statements that require correction.

Reset the state when the user starts a new topic.

This state need not be displayed. During verification, record it only when the host exposes a trace; otherwise, internal state and activation may be `UNVERIFIED` while rendered behavior is scored separately.

## Initial or direct response

Choose the view explicitly requested by the user. Otherwise, choose the shallowest complete view.

### At a glance

```text
<Direct answer.> <Decision-relevant consequence.> <Indispensable caveat or warning, when present.>
```

Keep counted prose at or below 40 words unless completeness or safety requires more. Do not tease later content.

### In context

Write one integrated response of at most 200 counted words. Include the direct answer and only the context needed to understand or act.

Use any helpful cues; omit the rest:

```text
<Direct answer and consequence.>

**Where it fits:** <Relevant scope or relationship.>
**What shifts:** <Meaningful change, if any.>
**Keep in view:** <Material limit, dependency, or caveat.>
**What follows:** <Action, owner, or timing.>
```

### At depth

Start with the answer and indispensable caveat, then organize the requested specialist detail:

```text
<Direct answer and consequence.>

<Evidence, assumptions, alternatives, exceptions, procedure, implementation, or sources needed for this request.>
```

Use descriptive headings when the response covers several specialist concerns. Do not render separate lower-view sections before the detailed answer.

At depth has no hard word cap, but every section must support the user's request.

## Clarification

Ask one focused question when missing information prevents view selection or a complete answer:

```text
<One question that obtains the missing choice or fact.>
```

Treat this as control dialogue, not a rendered view. Do not advance depth or add it to the word budget. If the question includes substantive answer content, count that content normally. Include an indispensable warning immediately when it cannot safely wait.

## Expansion turn

When the user says “more,” advance one view and supply only new information.

### At a glance → In context

```text
<New rationale, scope, constraint, ownership, or action that completes In context.>
```

The cumulative counted prose for the active topic must remain at or below 200 words unless an allowed exception applies.

### In context → At depth

```text
<New evidence, assumptions, alternatives, exceptions, procedure, implementation, or sources.>
```

Do not repeat the direct answer as an opening summary.

## Targeted follow-up

Answer only the selected branch:

```text
**<Optional cue>:** <The shallowest complete answer for the named branch.>
```

Keep the parent topic's view unchanged. Continue the branch if the next request is an unqualified “more.”

The branch inherits the active topic's cumulative count. Add branch prose at At a glance or In context to the same 200-word total. Once the branch enters At depth, remove the hard cap for its purposeful detail.

## Correction

Put the repair first:

```text
Earlier I said <withdrawn statement>. That was wrong.

<Replacement statement.> <Changed consequence or action.>
```

Use “incomplete” instead of “wrong” only when the earlier statement remains true but omitted information that materially changes its meaning. Repeat only enough to identify and repair the error.

Preserve the active view. Exempt only the words needed to retract, replace, and state the changed consequence or action; leave the prior cumulative total unchanged. Count any unrelated explanation or new detail normally. A later unqualified “more” advances from the corrected view.
