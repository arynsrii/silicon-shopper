# Methods - do LLM shopping agents show human choice biases?

Aryan Srivastava, IIT Delhi

## Question
When LLMs pick products, either buying for a user or role-playing a shopper, do they show the
decoy effect, anchoring, scarcity and social proof the way people do?

## Model
One open-weight model, `qwen/qwen3.8-27b` (label `qwen3.8-27b`), called through the Groq API
(free tier) on 2026-11-16.

Settings for every call: temperature 1.0, max 400 output tokens, provider defaults otherwise.

## Design
Trials come from `data/trials.csv` (made from `stimuli/products.yaml` with
`python src/build_trials.py --reps 20`, seed 2027). Every model answers **reps 0-5** of every
item x condition, i.e. 6 reps, 480 trials, in both framings = **960 calls**
(`python src/run_experiment.py --max-rep 6`). Brands are fictional. Option order, letters and
which brand gets which option are randomised per trial and saved.

| effect | items | conditions | what I measure |
|---|---|---|---|
| decoy | 10 | {A,B}, {A,B,A-decoy}, {A,B,B-decoy} | share picking A (premium) out of A/B picks |
| anchoring | 10 | low vs high anchor ("would you pay ₹X?") | stated max price (log) |
| scarcity | 10 | identical pair, one says "Only 2 left in stock"; plus no-cue control | share picking the one with the cue |
| social proof | 10 | 4.3★ (18,240 ratings) vs 4.6★ (37 ratings) | share picking the many-ratings one |

That gives 60 answers per condition per framing (10 items x 6 reps).

Two framings: `assistant` (AI buying for a customer) and `shopper` (AI playing an Indian shopper).

## Hypotheses
- H1 decoy: more A with the A-decoy than with the B-decoy
- H2 anchoring: higher max price after the high anchor
- H3 scarcity: cued option picked more than 50% of the time
- H4 social proof: many-ratings option picked more than 50% of the time
- exploratory: differences between framings, anchoring index (Jacowitz & Kahneman 1995)

## Analysis
One test per hypothesis per framing. 95% CIs from a cluster bootstrap over products
(2,000 draws). Also reporting chi-square (H1), Welch t-test on log price (H2) and binomial tests
(H3, H4). Bonferroni across the 4 hypotheses, so p < .0125 counts as significant; raw p-values
shown too.

## Exclusions
- replies that aren't valid JSON or don't name an option get re-run once; whatever's still broken is dropped and counted
- a choice written as "Option B" counts as "B"
- anchoring answers ≤ 0 or ≥ 100x the anchor are dropped
- picks of the dominated decoy are left out of H1 but I report how often it happened

All four effects get reported, including nulls.

## How it was run
All on 2026-11-16:
1. Setup checks on a few other models (Gemini, gpt-oss) were cut short by free-tier daily limits,
   so only qwen3.8-27b is analysed and included.
2. The 6-rep design was set after a one-rep format check.
3. Qwen3.8-27b (via the Groq API) finished all 960 calls. Broken replies were re-run once (44 calls).
