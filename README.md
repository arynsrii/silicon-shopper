# do AI shopping agents fall for the same tricks as people?

I've been reading about decoy pricing and anchoring for a while, and with AI agents starting to
shop for people I wanted to see if the models fall for the same stuff we do. So I ran a set of
small choice experiments on an LLM and checked four classic effects:

- **decoy effect** - add a clearly worse, pricier option next to the premium one. does the premium one get picked more?
- **anchoring** - ask "would you pay ₹5,500?" vs "would you pay ₹700?" first. does the max price it names move?
- **scarcity** - two identical products, one says "Only 2 left in stock". does that one get picked more than half the time?
- **social proof** - 4.3★ with 18,240 ratings vs 4.6★ with 37 ratings, same product and price. which one?

40 products, prices roughly what you'd see on Amazon.in / Flipkart. Brands are made up on purpose:
with real ones (boAt, Prestige etc.) the model could just go with the brand it knows and I couldn't
tell whether the decoy or the stock warning did anything. Each trial was asked twice, once as a
shopping assistant buying for a customer and once role-playing a normal shopper.

## what I found

Model: **Qwen3.8-27B** (open-weight, via Groq), temperature 1.0, 6 reps of each item x condition,
**960 calls** in total, run on 16 Nov 2026. CIs are 95% cluster-bootstrap over products.

| effect | assistant | shopper |
|---|---|---|
| **decoy**: premium picked with A-decoy vs B-decoy | 66% vs 37% (+29 pp, CI +18 to +39) | 60% vs 30% (+30 pp, CI +11 to +48) |
| **anchoring**: max price, high vs low anchor | 2.1x higher (anchoring index 0.33) | 2.2x higher (index 0.35) |
| **scarcity**: picked the "only 2 left" one | **3%** (53% with no label) | **13%** (53% with no label) |
| **social proof**: picked 18,240-ratings option | 98% | 98% |

The decoy, anchoring and review-count results look a lot like what's been found with people.
Scarcity went the **other way**: the model mostly avoided the "only 2 left" product, and its reasons
were things like *"avoids the low stock risk"*. So it read the label as a delivery risk, not as a
sign the product is popular. Plots are in `results/`, full numbers in `results/summary.md`.

## caveats (please read)

- **one model.** Runs on other models (Gemini, gpt-oss) were cut short by free-tier daily limits, so
  they were only used to test the setup and aren't included.

## running it yourself

```
pip install -r requirements.txt
export GROQ_API_KEY=...                       # free key from console.groq.com
python src/build_trials.py --reps 20          # writes data/trials.csv (seed 2027)
python src/run_experiment.py --max-rep 6      # models are set in config.yaml
python src/analyze.py                         # tables + plots go into results/
```

If it stops halfway (rate limit, wifi) just run it again, it skips whatever's already done.
The `mock` provider in `shared/llm_clients.py` is fake, only for testing the code offline.

## what's where

- `stimuli/products.yaml` - all products, prices and conditions
- `src/build_trials.py` - shuffles options/brands and writes every trial to a csv so runs are reproducible
- `src/run_experiment.py` - sends the prompts, saves every raw reply to `data/responses_<model>.jsonl`
- `src/analyze.py` - effect sizes + bootstrap CIs (resampling products, since answers about the same product aren't independent)
- `shared/llm_clients.py` - small wrappers for the Gemini / Groq / OpenAI / Anthropic APIs
- `data/` - every raw model reply from the main run
- `methods.md` - hypotheses, analysis plan and exactly how the runs went

## next

The same questions are going to real people in a survey, so I can compare human and AI answers directly.

Aryan Srivastava, IIT Delhi
