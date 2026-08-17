# Document template

Document mode is an informative Verbose-style adaptation of Progressive Clarity for static artifacts. Conversational behavior in `SPEC.md` remains canonical.

Use the visible sections only when they help readers choose a stopping point. For tutorials, procedures, controlling legal text, and voice-dependent writing, use the hybrid guidance at the end.

Version 0.1 word-budget guidance applies to English prose only. Use the human counting rules in `SPEC.md`; no non-English budget claim is made.

```markdown
# <Conclusion written as a specific claim>

## At a glance

<!-- At a glance: no more than 40 counted prose words. -->

<Direct answer or central fact.> <Decision-relevant consequence.>
<Indispensable caveat or warning, when present.>

## In context

<!-- At a glance plus this section: no more than 200 counted prose words. -->
<!-- Keep only useful cues. -->
<!-- Add information; do not repeat At a glance facts. -->

- **Why it counts:** <Significance not already stated.>
- **Where it fits:** <Relevant scope or relationship.>
- **What shifts:** <Meaningful change from the prior state.>
- **Keep in view:** <Material limit, dependency, or caveat.>
- **What follows:** <Action, owner, or timing.>

## At depth

<!-- No hard word cap; remain purposeful and do not restate earlier prose. -->

### <Specific specialist concern>

<Evidence, assumptions, alternatives, exceptions, procedure, implementation,
or authoritative sources for this concern.>

### <Another specialist concern, if needed>

<Detail needed by this audience and not supplied above.>
```

## Hybrid use

### Tutorial or procedure

Place an optional concise orientation before the ordered steps, then preserve the complete natural sequence.

```markdown
# <Outcome the reader will reach>

<Optional complete orientation and indispensable warning.>

## Steps

1. <First action.>
2. <Second action.>
3. <Continue in required order.>
```

### Controlling legal text

Never edit the controlling text to fit this template. Put a clearly separate, non-controlling explanation before or after it.

```markdown
## Non-controlling informative summary

<Plain-language explanation. This does not replace the controlling text.>

## Controlling text

<Verbatim legal text.>
```

### Narrative or voice-dependent writing

Keep the narrative intact. If readers need orientation, add a separate summary rather than interrupting sequence, pacing, or voice with view labels.
