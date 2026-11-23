# Silicon Shopper 2.0 — Experimental Protocol (Draft)

**Status: DRAFT / NOT PREREGISTERED / NOT RUN.** This document describes proposed research. It must be finalized *before* any confirmatory data collection. The original v1 data are exploratory motivation.

**Working title:** When AI Shops for Us: Scarcity, Delivery Risk and Delegated Consumer Choice

## Motivation

In v1, the single tested model (Qwen3.8-27B, Groq) selected an otherwise equal product labeled “Only 2 left in stock” in 3.3% of the assistant-framing trials versus 13.3% under role-play. The original treatment changes only one listing and the setup does not establish a psychological mechanism. We therefore propose to test possible interpretations, **not to announce an identified mechanism**.

## Primary research question

Does presenting truthful low-inventory information change an AI buying assistant's hypothetical selection, and is that treatment effect moderated by (a) fulfillment certainty, and (b) the purchaser's explicitly delegated goal?

## Proposed design

Randomize fictional brand assignments, options' alphabetical labels, display positions, and condition assignments. Keep base product price, specifications, warranties, availability and delivery windows constant within matched sets.

- **Factor S — Scarcity:** no stock warning versus “Only 2 left in stock”.
- **Factor G — Guarantee:** same explicit delivery guarantee shown consistently for both options versus no explicit delivery guarantee. A two-level factorial requires precise wording so that guarantee is not contradicted by low stock.
- **Factor O — Objective:** “prioritize a reliable, on-time delivery” versus “no deadline; prioritize total value”. Use a separate balanced goal condition. The exact goal wording must be piloted for comparable specificity.
- **Exploratory popularity factor:** no social-demand claim versus “Popular this week”. Only add if it does not expand total sample beyond budget.

Study the two-way interactions S×G and S×O. Full S×G×O = eight cells before optional popularity factor. Randomly assign focal listing status independent of letter or brand.

### Primary outcome

Binary selection of the focal product, in a two-product hypothetical choice. **Estimate treatment-vs-control differences** with uncertainty; do not assume the neutral focal choice probability is exactly 50% when residual position/name effects exist. The no-scarcity condition directly supplies a baseline.

### Secondary outcomes

- Report invalid outputs / refusals / non-choices.
- Record budget/delivery goal adherence where clearly operationalized.
- Optionally collect perceived delivery-risk ratings in a separate *post-choice* task; the model's free-text explanation does not establish true causal reasoning.
- Compare between independent model families and between text-only versus tool-mediated shopping in a separate extension.

### Sampling and inference

- Unit of treatment assignment: *individual experimental trial*, with counterbalanced templates; trials are nested within product categories/models.
- Independent generalization units: products and categories, **not** repeated stochastic completions. Do not equate a large API-call count with a large number of independent products.
- Fix target minimum effect and precision using a simulation-based power study before confirmatory deployment. No arbitrary sample size will be represented as scientifically sufficient.
- Primary regression: selected_focal ~ scarcity * guarantee + scarcity * objective + product fixed effects + position covariate (define regression family and interaction contrasts before run). Cluster by product; with few clusters, report bootstrap sensitivity and avoid overstated precision.
- Report overall effect, treatment interactions, per-model heterogeneity, model-identifiable sample sizes, confidence intervals, and exact exclusions.
- Decide multiplicity adjustment and hypothesis family in advance. Keep confirmatory vs exploratory tests clearly separate.
- Re-run analysis at category level and with leave-one-category-out sensitivity checks.

## Controls and error handling

- Same factual base descriptions and equivalent text lengths.
- Randomize or balance option order and fictional brand.
- Validate choice schema; do not count a JSON object with an invalid option as a successful choice.
- Store attempts, retries, raw text, time, model/provider/version, settings and random seeds.
- Use explicit model outputs only; mock outputs are excluded from research results.
- Ensure reproducible analysis from a frozen, versioned dataset.

## Study B — deconfounded replications (secondary)

**Decoy:** report unconditional premium selection probability in each randomized condition; give dominated-decoy selection separately (no cherry-picking by excluding dominated selections from the main effect).

**Anchoring:** validate the original cluster bootstrap over products; report median, log-scale or median-normalized differences with sensible exclusions, as appropriate to the preregistered question.

**Review count and star rating:** independently manipulate count and stars in a factorial design. V1 compared 4.3 stars / 18,240 ratings with 4.6 stars / 37 ratings, which does not identify a pure review-count effect.

**Human benchmark:** if feasible, obtain a consenting sample and use matched experimental descriptions; give the human-AI comparison its own sampling and power plan.

## What this design does NOT establish

- The inner cognitive process of an LLM.
- Actual human purchase behavior from hypothetical responses.
- How a fully autonomous browser agent buys without testing one.
- An effect generalized to all LLMs from a small convenience sample of models.

## Main literature
- MIT ABxLab / ICLR 2026, https://abxlab.media.mit.edu/
- Columbia Business School ACES study, https://business.columbia.edu/insights/digital-future-initiative/ai-shopping-agents
- Wharton report “Agentic Shopping is Complicated and Contingent”, https://gail.wharton.upenn.edu/research-and-insights/technical-report-agentic-shopping/

## Before collection

[ ] Record exact primary hypotheses, prompts and stimuli; [ ] run reproducibility audit; [ ] determine model availability/cost; [ ] prespecify effects and power/precision; [ ] decide exclusions and missingness reporting; [ ] freeze a preregistration-like dated protocol commit.
