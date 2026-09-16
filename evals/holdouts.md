# Unseen holdout workflow

The public `cases.json` suite is development material. Its paraphrases and
cross-domain cases exercise generalization but are not claimed to be unseen.

1. Freeze the protocol, skill, model settings, scoring rules, and planned run
   counts after development testing.
2. Have a reviewer who did not tune the instructions author fresh conversations
   under the ignored `evals/holdouts/` directory. Use the same suite structure,
   schema `6.0.0`, protocol version/hash, a unique suite ID, and `split: "holdout"`.
   The `--suite` option accepts that file without exposing it to the generator
   except as successive user prompts. Expectations and source-fact catalogs go
   to scoring only.
3. Include paraphrased requests without protocol vocabulary; compact consequential
   decisions; examples needing distinct depth; health, education, finance, and
   everyday planning domains; ambiguous topic returns in longer conversations;
   exact artifacts with explanations; and competing presentation requirements.
   Supply enough facts for each expected answer. Do not create a hidden-answer
   guessing test or require facts available only on later turns.
4. For legitimately variable presentation, use `presentation: "adaptive"` and
   `rendered_views: []`. Both a natural answer and a complete ordered three-view
   answer are eligible; semantic review must judge whether the chosen depth helps.
5. Commit the holdout digest and evaluation plan to an investigator's dated record
   before running. Keep prompts inaccessible to the instruction-tuning process.
   A `holdout` label or hash alone does not prove independence or lack of exposure.
6. Run every prescribed session once under the frozen plan and preserve raw
   outputs, including failures. Report development and holdout results separately.
   Debugging or changing instructions after inspecting failures consumes that
   holdout; move it into development and obtain a newly authored holdout.

```sh
python3.11 -m tools.azure_eval_harness \
  --suite evals/holdouts/round-1.json --condition revised --dry-run
python3.11 -m tools.azure_eval_harness \
  --suite evals/holdouts/round-1.json --condition revised \
  --output evals/runs/holdout-round-1.json
```

Holdout conformance and reader benefit remain **UNVERIFIED** until executed and
reviewed. Use the [reader-study plan](reader-study.md) for outcome claims.
