# Document template

Document adaptation is an informative use of Progressive Clarity's Full format
for static artifacts. Conversational behavior in `SPEC.md` remains canonical.

Use the visible sections only when they help readers choose a stopping point. For tutorials, procedures, controlling legal text, and voice-dependent writing, use the hybrid guidance at the end.

Version 0.4 Full-format word-budget guidance applies to English prose only. Use
the counting rules in `SPEC.md`; no non-English budget claim is made.

Privately draft At a glance, place its complete propositions in a “do not
restate” ledger, draft In context with new rationale/constraints/actions plus
minimal anchors, add those propositions to the ledger, and draft At depth with
new evidence/exceptions/implementation. Delete every sentence that restates
the ledger and every concluding At-depth recap.

```markdown
# <Conclusion written as a specific claim>

## At a glance

<!-- At a glance: no more than 40 counted non-warning prose words. -->

<Direct answer or central fact.> <Decision-relevant consequence.>
<Indispensable caveat or warning, when present.>

## In context

<!-- Through this section: no more than 200 counted non-warning prose words. -->
<!-- Keep only useful cues. -->
<!-- New information must dominate; use only necessary brief anchors. -->

- **Why it counts:** <Significance not already stated.>
- **Where it fits:** <Relevant scope or relationship.>
- **What shifts:** <Meaningful change from the prior state.>
- **Keep in view:** <Material limit, dependency, or caveat.>
- **What follows:** <Action, owner, or timing.>

## At depth

<!-- No hard word cap; do not restate earlier complete propositions or recap. -->

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
