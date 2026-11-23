# Silicon Shopper v1 — Initial Code Review

**Review date:** 2026-11-24  
**Scope:** Static source-code review of README, methods, stimuli, analysis, experiment runner and summary on GitHub. **Not a fresh numerical rerun.** The items below are audit targets; fix and verify them before publishing a revised v1 result.

## Verified repository observations

- 10 items each for decoy, anchoring, scarcity and rating/review-choice tasks.
- 6 repetitions per item-condition and two role prompts, reported as 960 model calls in the methods document. The saved trial-generation configuration creates 20 candidate repetitions; only repetitions 0–5 are run.
- Results contain cluster-bootstrap CIs, effect sizes and p-values; only one main model is included.
- Scarcity ‘n = 120’ in results summary combines both cue and no-cue *conditions* for a framing; the cue selection percentage itself is measured on 60 cue-condition trials. This should be described more clearly to prevent denominator confusion.

## Important audit/fix tasks

1. **Anchoring bootstrap cluster multiplicities.** In src/analyze.py, cluster_boot() concatenates resampled product groups. The anchoring statistic then groups by product and condition, potentially collapsing duplicate bootstrap draws into the same single product mean. This can distort cluster-bootstrap CIs. Refactor to bootstrap unique resampled cluster identifiers or compute the effect from the explicit vector of product-level effects with multiplicities preserved. Verify with tests.
2. **Incomplete/invalid responses.** In run_experiment.py, ok=True is set if a parseable nonempty JSON object exists; invalid choice letters and malformed numerical fields are only excluded later. Document *attempted, parsed, valid and analyzed* counts and reasons by condition.
3. **Decoy estimand.** The current primary decoy share is conditional on choosing a non-decoy option. This is defensible if declared, but headline effects should also report unconditional A selection (including valid dominated-decoy selections) as a robustness check.
4. **Social-proof interpretation.** The v1 task pits 4.3 stars with 18,240 ratings against 4.6 stars with 37 ratings; do not call it the independent effect of ratings volume. Randomize the two signals separately in v2.
5. **Potential dependence.** Repeated trials of the same product and model are not independent products or participant observations. Simple binomial and Welch p-values are descriptive only; rely on a suitable hierarchical/clustered primary method.
6. **Prompt-role distinction.** An assistant-framed single LLM answer is not a fully tool-using browser agent. Use the phrase ‘LLM in shopping-assistant framing’ for v1.
7. **Parsing fragility.** Greedy JSON extraction via regex in shared/llm_clients.py can misparse model outputs containing multiple brace blocks. Strengthen parsing and add negative tests.
8. **Reproducibility.** Pin dependencies and capture exact model/date/run settings; check raw data completeness and compare regenerated summary to committed summary.
9. **Statistics labels.** ‘p (bootstrap) = 0.001’ is only a finite-sample resampling tail statistic under the existing implementation; verify method and appropriate null calibration before treating it as confirmatory evidence.
10. **No human comparison claims.** A human study is mentioned as next steps but no completed human comparison appears in the reviewed files.

## Definition of done for v1 audit

- Clean install -> reproducible results and figures.
- Documented denominators and exclusion flows.
- Cluster/bootstrap tests pass, including duplicate-resampled clusters.
- Clear original-vs-corrected table.
- No invented human data or generalized claims beyond the tested model.
