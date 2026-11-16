# builds every trial from stimuli/products.yaml and saves them to data/trials.csv
# (order, letters and brands are all fixed here so the same run can be repeated with the same seed)

import argparse
import itertools
import random
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABC"


def inr(x):
    return f"₹{x:,}"


def fmt_value(v):
    return f"{v:g}"


def decoy_trials(stim, rng, reps):
    rows = []
    for item in stim["decoy"]:
        for cond in ["control", "decoy_A", "decoy_B"]:
            for rep in range(reps):
                opts = [("A", item["A"]), ("B", item["B"])]
                if cond == "decoy_A":
                    opts.append(("A_decoy", item["A_decoy"]))
                elif cond == "decoy_B":
                    opts.append(("B_decoy", item["B_decoy"]))
                rng.shuffle(opts)
                brands = rng.sample(stim["brands"], len(opts))
                lines, key = [], {}
                for (role, o), letter, brand in zip(opts, LETTERS, brands):
                    lines.append(f"Option {letter}: {brand} {item['category']} - "
                                 f"{item['attribute']} {fmt_value(o['value'])} {item['unit']}, "
                                 f"price {inr(o['price'])}")
                    key[letter] = role
                rows.append(dict(effect="decoy", item=item["category"], condition=cond, rep=rep,
                                 options="\n".join(lines), key=key))
    return rows


def anchoring_trials(stim, rng, reps):
    rows = []
    for item in stim["anchoring"]:
        for cond in ["low", "high"]:
            for rep in range(reps):
                rows.append(dict(effect="anchoring", item=item["item"], condition=cond, rep=rep,
                                 anchor=item[cond], options="", key={}))
    return rows


def pair_trials(stim, rng, reps, effect):
    # scarcity and social proof: two identical options, one gets the cue
    block = stim[effect]
    rows = []
    for item in block["items"]:
        conds = ["cue", "control"] if effect == "scarcity" else ["cue"]
        for cond in conds:
            for rep in range(reps):
                brands = rng.sample(stim["brands"], 2)
                order = [0, 1]
                rng.shuffle(order)
                lines, key = [], {}
                cued = rng.randint(0, 1)  # which brand gets the cue
                for letter, idx in zip("AB", order):
                    desc = f"{brands[idx]} {item['category']} - {item['spec']}, price {inr(item['price'])}"
                    role = "cued" if idx == cued else "plain"
                    if effect == "scarcity" and cond == "cue" and role == "cued":
                        desc += f" [{block['cue']}]"
                    if effect == "social_proof":
                        r = block["H"] if role == "cued" else block["L"]
                        desc += f", rated {r['stars']} stars ({r['ratings']:,} ratings)"
                    lines.append(f"Option {letter}: {desc}")
                    key[letter] = role
                rows.append(dict(effect=effect, item=item["category"], condition=cond, rep=rep,
                                 options="\n".join(lines), key=key))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=20, help="repetitions per item x condition")
    ap.add_argument("--seed", type=int, default=2027)
    args = ap.parse_args()

    stim = yaml.safe_load(open(ROOT / "stimuli" / "products.yaml", encoding="utf-8"))
    rng = random.Random(args.seed)
    rows = (decoy_trials(stim, rng, args.reps) + anchoring_trials(stim, rng, args.reps)
            + pair_trials(stim, rng, args.reps, "scarcity")
            + pair_trials(stim, rng, args.reps, "social_proof"))
    df = pd.DataFrame(rows)
    df.insert(0, "trial_id", range(len(df)))
    out = ROOT / "data" / "trials.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"wrote {len(df)} trials to {out}")
    print(df.groupby(["effect", "condition"]).size().to_string())


if __name__ == "__main__":
    main()
