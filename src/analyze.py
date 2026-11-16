# reads the responses and works out the four effects for each model + framing.
# CIs: bootstrap that resamples products (not single answers), because answers about the
# same product are correlated. writes results/summary.md, summary.csv and the plots.

import ast
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RNG = np.random.default_rng(2027)
B = 2000


def load():
    trials = pd.read_csv(ROOT / "data" / "trials.csv")
    trials["key"] = trials["key"].apply(ast.literal_eval)
    recs = []
    for p in sorted((ROOT / "data").glob("responses_*.jsonl")):
        with open(p, encoding="utf-8") as f:
            recs += [json.loads(l) for l in f]
    resp = pd.DataFrame(recs)
    resp = resp[resp["ok"]].drop_duplicates(["model_label", "framing", "trial_id"], keep="last")
    df = resp.merge(trials, on="trial_id")

    def role(r):
        # accept "B", "Option B", "option b." etc.
        m = re.match(r"^\s*(?:OPTION\s*)?([A-Z])\b", str(r["parsed"].get("choice", "")).upper())
        return r["key"].get(m.group(1)) if m else None

    def wtp(r):
        try:
            return float(str(r["parsed"].get("max_price")).replace(",", "").replace("₹", ""))
        except (TypeError, ValueError):
            return np.nan

    df["role"] = df.apply(role, axis=1)
    df["wtp"] = df.apply(wtp, axis=1)
    return df


def cluster_boot(df, stat):
    # resample products with replacement, recompute the stat each time
    if df.empty:
        return np.nan, np.nan, np.nan
    items = df["item"].unique()
    groups = {i: g for i, g in df.groupby("item")}
    vals = []
    for _ in range(B):
        pick = RNG.choice(items, len(items), replace=True)
        vals.append(stat(pd.concat([groups[i] for i in pick])))
    vals = np.array(vals)
    vals = vals[~np.isnan(vals)]
    lo, hi = np.percentile(vals, [2.5, 97.5])
    p = 2 * min((vals <= 0).mean(), (vals >= 0).mean())
    return lo, hi, min(1.0, max(p, 1 / B))  # draws exactly at 0 count in both tails, so cap at 1


def decoy(g):
    d = g[g.effect == "decoy"]
    d = d.assign(isA=(d.role == "A").astype(float), valid=d.role.isin(["A", "B"]))
    v = d[d.valid]

    def share(x, c):
        x = x[x.condition == c]
        return x.isA.mean() if len(x) else np.nan

    stat = lambda x: share(x, "decoy_A") - share(x, "decoy_B")
    lo, hi, p = cluster_boot(v, stat)
    tab = pd.crosstab(v[v.condition != "control"].condition, v[v.condition != "control"].isA)
    chi_p = stats.chi2_contingency(tab)[1] if tab.shape == (2, 2) else np.nan
    return dict(effect="decoy",
                measure="share choosing premium option A",
                control=share(v, "control"), cond_1=share(v, "decoy_A"), cond_2=share(v, "decoy_B"),
                diff=stat(v), ci_low=lo, ci_high=hi, p_boot=p, p_simple=chi_p,
                n=len(v), note=f"picked the dominated decoy {(d.role.str.endswith('decoy')).mean():.1%} of the time")


def anchoring(g):
    a = g[(g.effect == "anchoring") & (g.wtp > 0) & (g.wtp < 100 * g.anchor)].copy()
    a["logw"] = np.log(a.wtp)

    def stat(x):
        m = x.groupby(["item", "condition"]).logw.mean().unstack()
        return (m["high"] - m["low"]).mean()

    lo, hi, p = cluster_boot(a, stat)
    # Jacowitz & Kahneman anchoring index: (median high - median low) / (high anchor - low anchor)
    idx = []
    for item, x in a.groupby("item"):
        h, l = x[x.condition == "high"], x[x.condition == "low"]
        if len(h) and len(l):
            idx.append((h.wtp.median() - l.wtp.median()) / (h.anchor.iloc[0] - l.anchor.iloc[0]))
    t_p = stats.ttest_ind(a[a.condition == "high"].logw, a[a.condition == "low"].logw, equal_var=False).pvalue
    return dict(effect="anchoring", measure="log max price, high minus low anchor",
                control=np.nan, cond_1=a[a.condition == "high"].wtp.median(),
                cond_2=a[a.condition == "low"].wtp.median(),
                diff=stat(a), ci_low=lo, ci_high=hi, p_boot=p, p_simple=t_p, n=len(a),
                note=f"anchoring index {np.mean(idx):.2f} (0 = no effect, 1 = answer moves fully with the anchor); "
                     f"x{np.exp(stat(a)):.2f} higher stated price under the high anchor")


def pair(g, effect, label):
    s = g[(g.effect == effect) & g.role.isin(["cued", "plain"])]
    s = s.assign(isC=(s.role == "cued").astype(float))
    cue = s[s.condition == "cue"]
    stat = lambda x: x[x.condition == "cue"].isC.mean() - 0.5
    lo, hi, p = cluster_boot(s, stat)
    bp = stats.binomtest(int(cue.isC.sum()), len(cue), 0.5).pvalue if len(cue) else np.nan
    ctrl = s[s.condition == "control"].isC.mean() if "control" in set(s.condition) else np.nan
    return dict(effect=effect, measure=label, control=ctrl, cond_1=cue.isC.mean(), cond_2=0.5,
                diff=stat(s), ci_low=lo, ci_high=hi, p_boot=p, p_simple=bp, n=len(s), note="")


def plot(summary):
    RES.mkdir(exist_ok=True)
    for eff, d in summary.groupby("effect"):
        d = d.sort_values("group")
        fig, ax = plt.subplots(figsize=(6, 0.5 + 0.45 * len(d)))
        y = np.arange(len(d))
        ax.errorbar(d["diff"], y, xerr=[d["diff"] - d.ci_low, d.ci_high - d["diff"]],
                    fmt="o", color="#1f3864", capsize=3)
        ax.axvline(0, color="grey", lw=0.8)
        ax.set_yticks(y, d.group)
        ax.set_xlabel(d.measure.iloc[0] + "\n(difference vs. no-bias benchmark, 95% CI)")
        ax.set_title(eff.replace("_", " ").title())
        fig.tight_layout()
        fig.savefig(RES / f"fig_{eff}.png", dpi=200)
        plt.close(fig)


def main():
    df = load()
    rows = []
    for (m, fr), g in df.groupby(["model_label", "framing"]):
        for r in (decoy(g), anchoring(g),
                  pair(g, "scarcity", "share choosing the 'only 2 left' option (minus 50%)"),
                  pair(g, "social_proof", "share choosing many-reviews option (minus 50%)")):
            r.update(model=m, framing=fr, group=f"{m} / {fr}")
            rows.append(r)
    summary = pd.DataFrame(rows)
    RES.mkdir(exist_ok=True)
    summary.to_csv(RES / "summary.csv", index=False)
    plot(summary)

    mock = (summary.model == "mock").any()
    lines = ["# Project 1 results", ""]
    if mock:
        lines += ["> **WARNING: includes MOCK model output. Mock numbers are generated by rules "
                  "and must never be reported.**", ""]
    for eff, d in summary.groupby("effect", sort=False):
        lines += [f"## {eff.replace('_', ' ').title()}", f"Measure: {d.measure.iloc[0]}", "",
                  "| model / framing | effect | 95% CI | p (bootstrap) | n | note |",
                  "|---|---|---|---|---|---|"]
        for _, r in d.iterrows():
            lines.append(f"| {r.group} | {r['diff']:+.3f} | [{r.ci_low:+.3f}, {r.ci_high:+.3f}] | "
                         f"{r.p_boot:.3f} | {r.n} | {r.note} |")
        lines.append("")
    (RES / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
