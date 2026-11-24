# Research extension: When does scarcity repel AI purchasing agents?

**Status:** Proposed follow-up study; not yet run.  
**Researcher:** Aryan Srivastava, B.S. Chemistry, IIT Delhi  
**Previous study:** [Silicon Shopper](../README.md) (November 2026)

## Motivation
The first Silicon Shopper study found that a single LLM selected products marked “Only 2 left” less often than unmarked alternatives. In the original shopping-assistant framing, the marked product was chosen around 3% of the time, versus 53% under a no-label comparison. Those findings are exploratory, model-specific, and must not be generalized to humans or other models.

Recent related work: Kumar et al. (2026), *Agentic Shopping is Complicated and Contingent*, Wharton Generative AI Labs, https://gail.wharton.upenn.edu/research-and-insights/technical-report-agentic-shopping/ ; Tomaino, Mazar, Carmon & Wertenbroch (2025), *Scope Testing with AI-Generated Stimuli (STAGS)*, Consumer Psychology Review. The proposed novelty here is an explicit mechanism test for *inventory scarcity as perceived fulfillment risk*, not a generic demonstration of agentic-shopping context sensitivity.

## Research question
Does an AI shopping agent treat scarce inventory as a positive popularity cue, a negative stock-out/fulfillment-risk cue, or both depending on the shopping objective and fulfillment information?

## Proposed hypotheses (to preregister before collecting new outcomes)
- **H1: Scarcity penalty.** An inventory-scarcity label decreases the probability of selecting an otherwise identical product relative to no label in the shopping-agent condition.
- **H2: Fulfillment-risk moderation.** The scarcity penalty becomes smaller when a verified-delivery assurance is included.
- **H3: Popularity-cue moderation.** A scarcity label explicitly attributed to high demand attenuates or reverses the negative effect relative to unexplained scarcity.
- **H4: Goal dependence.** The scarcity penalty is stronger for time-critical fulfillment tasks than for exploratory purchases.

All hypotheses are testable; none is claimed as established.

## Experimental design
Use an independently randomized, balanced factorial design across product categories, models, and prompt-order variations. The primary factors should be: scarcity label (absent/present), delivery assurance (absent/present), purchase goal (urgent/nonurgent), and label explanation (none/high demand) where meaningful. Randomly rotate product display order and fictional-brand assignments. Lock prompts, datasets, provider versions, and analysis code before the full run.

The unit of randomization is the *prompt trial*; outcomes are clustered across product templates and replicated model calls. Avoid prompt leakage across conditions and record provider versions, decoding settings, timestamps, response text, parsing decisions, and missing/failed attempts.

## Outcomes and analysis
**Primary outcome:** Probability of choosing the focal product.  
**Secondary outcomes:** Stated expected delivery reliability, preference strength, perceived demand, willingness-to-pay where elicited, and refusal/invalid-response rate. Explanations are qualitative data, not proof of an internal causal mechanism.

Estimate factorial interaction effects via a prespecified generalized linear model and report absolute risk differences; use product-cluster bootstrapping (and additional model-level sensitivity analyses when model count allows). Correct or clearly flag multiple secondary tests. Include power/simulation planning before collection, descriptive missingness reporting, and sensitivity to wording and order.

## Robustness and ethical practice
Replicate across multiple independently sourced model families; audit parser disagreement and rerun only according to prespecified rules. Do **not** fabricate or substitute mock-provider responses for live results. Distinguish simulated shopper persona from actual human decisions. Any human-participant comparison requires suitable ethics/IRB review or institutional exemption, informed consent, and documented recruitment/compensation rules.

## What a research assistant could contribute
- Implement clean stimulus-generation and experimental-control pipelines in Python.
- Audit model responses, parse choices, and build reproducible regression/bootstrap analyses.
- Run literature searches and structured replications of specific experimental effects.
- Collaborate with faculty on a preregistration, power simulations, and research-ready presentation.

## Milestones
1. Freeze research questions, design, estimands, inclusion/exclusion rules, and analysis plan.
2. Run power simulations and a small parser/reproducibility pilot.
3. Execute and audit the multi-model experiment.
4. Write a short report with reproducible code and limitations.
5. Seek an institutional partner before conducting any human-subject experiment.

**This document describes proposed work, not completed results or an accepted publication.**
