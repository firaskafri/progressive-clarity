# Document template

Document adaptation is an informative use of Progressive Clarity's Full format
for static artifacts. Conversational behavior in `SPEC.md` remains canonical.

Use the visible sections only when they help readers choose a stopping point. For tutorials, procedures, controlling legal text, and voice-dependent writing, use the hybrid guidance at the end.

Version 0.5 Advisory targets apply to English prose only. The 40/200 thresholds
are provisional; inspect visible bulk including tables, code, and headings.

Draft the answer, needed rationale, and purposeful depth. Keep deeper sections
predominantly new. Brief repetition may aid comprehension or qualify an action;
remove duplicated explanations and automatic concluding recaps.

```markdown
# <Conclusion written as a specific claim>

## At a glance

<!-- At a glance: aim for 40 non-warning prose words. -->

<Direct answer or central fact.> <Decision-relevant consequence.>
<Indispensable caveat or warning, when present.>

## In context

<!-- Through this section: aim for 200 non-warning prose words. -->
<!-- Keep only useful cues. -->
<!-- New information must dominate; repetition must earn its place. -->

- **Why it counts:** <Significance not already stated.>
- **Where it fits:** <Relevant scope or relationship.>
- **What shifts:** <Meaningful change from the prior state.>
- **Keep in view:** <Material limit, dependency, or caveat.>
- **What follows:** <Action, owner, or timing.>

## At depth

<!-- No hard word cap; avoid duplicated explanations and automatic recaps. -->

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

Never edit the controlling text to fit this template. When an explanation is
requested, use the two literal labels below. Verbatim-only reproduction keeps
only the exact source.

```markdown
Controlling text:

<Verbatim legal text.>

Non-controlling plain-language summary:

<Plain-language explanation. This does not replace the controlling text.>
```

### Narrative or voice-dependent writing

Keep the narrative intact. If readers need orientation, add a separate summary rather than interrupting sequence, pacing, or voice with view labels.
