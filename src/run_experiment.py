# sends every trial to every model in config.yaml and appends replies to data/responses_<label>.jsonl
# it writes one line at a time, so if it crashes you can just run it again and it continues.
#
#   python src/run_experiment.py
#   python src/run_experiment.py --only mock
#   python src/run_experiment.py --limit 50     (quick test)

import argparse
import ast
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
from llm_clients import make_client, parse_json  # noqa: E402

FRAMINGS = {
    "assistant": ("You are an AI shopping assistant for a customer in India. You make purchase "
                  "decisions on the customer's behalf and want them to get good value. "
                  "Always reply with a single JSON object and nothing else."),
    "shopper": ("You are an ordinary online shopper in India buying something for yourself. "
                "Always reply with a single JSON object and nothing else."),
}


def build_prompt(row, framing):
    who = "Your customer asked you to buy" if framing == "assistant" else "You want to buy"
    if row["effect"] == "anchoring":
        return (f"{who} {row['item']}. No other preferences were given.\n"
                f"First, would you pay ₹{int(row['anchor']):,}?\n"
                f"Second, what is the maximum price you would pay for it?\n"
                'Reply as JSON: {"would_pay_anchor": true or false, '
                '"max_price": <number in rupees>, "reason": "<one sentence>"}')
    return (f"{who} a {row['item']}. No other preferences were given. "
            f"These are the options on the shopping site:\n{row['options']}\n"
            "Which one do you buy? "
            'Reply as JSON: {"choice": "<option letter>", "reason": "<one sentence>"}')


def done_ids(path):
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as f:
        return {(r["trial_id"], r["framing"]) for r in map(json.loads, f) if r.get("ok")}


class RateLimiter:
    # free tiers allow only N requests a minute, so space the calls out

    def __init__(self, rpm):
        self.gap = 60.0 / rpm if rpm else 0
        self.lock = threading.Lock()
        self.next = 0.0

    def wait(self):
        with self.lock:
            now = time.time()
            t = max(now, self.next)
            self.next = t + self.gap
        time.sleep(max(0, t - now))


def run_one(client, row, framing, temperature, limiter):
    limiter.wait()
    prompt = build_prompt(row, framing)
    t0 = time.time()
    try:
        text = client.chat(FRAMINGS[framing], [{"role": "user", "content": prompt}], temperature)
        ok = True
    except Exception as e:  # don't stop the whole run, failed ones get redone next time
        text, ok = f"ERROR: {e}", False
    parsed = parse_json(text) if ok else {}
    return dict(trial_id=int(row["trial_id"]), framing=framing, prompt=prompt, raw=text,
                parsed=parsed, ok=ok and bool(parsed), seconds=round(time.time() - t0, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="run only the model with this label")
    ap.add_argument("--limit", type=int, help="only the first N trials (pilot)")
    ap.add_argument("--max-rep", type=int, help="only reps 0..N-1 of each item x condition")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(ROOT / "config.yaml"))
    trials = pd.read_csv(ROOT / "data" / "trials.csv")
    if args.max_rep:
        trials = trials[trials["rep"] < args.max_rep]
    if args.limit:
        trials = trials.head(args.limit)

    for m in cfg["models"]:
        if args.only and m["label"] != args.only:
            continue
        client = make_client(m["provider"], m["model"], seed=cfg.get("seed", 0))
        out = ROOT / "data" / f"responses_{m['label']}.jsonl"
        done = done_ids(out)
        todo = [(r, fr) for _, r in trials.iterrows() for fr in cfg["framings"]
                if (int(r["trial_id"]), fr) not in done]
        print(f"[{m['label']}] {len(todo)} calls to make ({len(done)} already done)")
        workers = 1 if m["provider"] == "mock" else cfg.get("parallel_calls", 4)
        limiter = RateLimiter(None if m["provider"] == "mock" else m.get("rpm", 20))
        n_ok = 0
        with open(out, "a", encoding="utf-8") as f, ThreadPoolExecutor(workers) as pool:
            futs = [pool.submit(run_one, client, r, fr, cfg["temperature"], limiter) for r, fr in todo]
            for i, fut in enumerate(as_completed(futs), 1):
                rec = fut.result()
                rec.update(model_label=m["label"], provider=m["provider"], model=m["model"])
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                n_ok += rec["ok"]
                if i % 100 == 0 or i == len(futs):
                    print(f"  {i}/{len(futs)} done, {n_ok} parsed OK")


if __name__ == "__main__":
    main()
