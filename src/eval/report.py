"""Turn results/metrics_long.csv into summary / comparison tables, figures and REPORT_NOTES.md.

    python -m src.eval.report
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import plots
from .metrics import confusion
from .stats import mcnemar

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results"
FIG = RES / "figures"

NONHYBRID = ["MLP", "FCM-clf", "LDA", "LR", "LinSVM", "RBF-SVM", "RF"]
INITS = ["Random", "KMeans", "SC", "FCM"]
ANFIS = [f"ANFIS-{i}{s}" for i in INITS for s in ("", "+stk")]
LADDER = ["MLP", "FCM-clf", "ANFIS-Random", "ANFIS-KMeans", "ANFIS-SC", "ANFIS-FCM",
          "ANFIS-SC+stk", "ANFIS-FCM+stk"]
PAPER_HYBRID = "ANFIS-FCM+stk"       # pre-specified: the paper's best model / architecture
SETTINGS = ["A", "A-noID", "B", "B-ID"]
TASKS = ["binary", "multi"]
KEY_CLASS = {"binary": "Attack", "multi": "Imp"}
CLASSES = {"binary": ["Attack", "Normal"], "multi": ["DoS", "Imp", "Normal"]}

# Paper (Al Isawi et al. 2025), Tables 6 and 8 (by caption): accuracy, overall (macro) F1
PAPER = {
    "binary": {"LDA": (0.8593, 0.819), "LR": (0.9118, 0.866), "RBF-SVM": (0.9750, 0.951),
               "RF": (0.9928, 0.984), "ANFIS-SC+stk": (0.9958, 0.991),
               "ANFIS-FCM+stk": (0.9968, 0.993)},
    "multi": {"ANFIS-SC+stk": (0.9965, 0.988), "ANFIS-FCM+stk": (0.9968, 0.989),
              "CNN (paper only)": (0.8263, 0.497), "CNN-LSTM (paper only)": (0.8645, 0.459),
              "GRU (paper only)": (0.9950, 0.982), "LSTM (paper only)": (0.9955, 0.984)},
}
PAPER_IMP_F1 = {"ANFIS-SC+stk": 0.968, "ANFIS-FCM+stk": 0.968}


# ---------------------------------------------------------------------------
def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(RES / "metrics_long.csv")
    params = df[df.metric == "params"]
    num = df[df.metric != "params"].copy()
    num["value"] = num["value"].astype(float)
    wide = num.pivot_table(index=["setting", "task", "model", "variant", "seed"],
                           columns="metric", values="value").reset_index()
    return wide, params


def agg(wide, setting, task, variant="main", models=None):
    d = wide[(wide.setting == setting) & (wide.task == task) & (wide.variant == variant)]
    if models is not None:
        d = d[d.model.isin(models)]
    g = d.drop(columns=["setting", "task", "variant", "seed"]).groupby("model")
    return g.mean(), g.std(), g.size()


def pm(m, s, fmt="{:.4f}"):
    if pd.isna(m):
        return "–"
    return fmt.format(m) + ("" if pd.isna(s) else " ± " + fmt.format(s))


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join([df.index.name or "model"] + cols) + " |", "|" + "---|" * (len(cols) + 1)]
    for i, r in df.iterrows():
        out.append("| " + " | ".join([str(i)] + [str(v) for v in r]) + " |")
    return "\n".join(out)


def paired_diff(wide, setting, task, a, b, metric="macro_f1", variant="main"):
    """Per-seed difference b - a on the same splits."""
    d = wide[(wide.setting == setting) & (wide.task == task) & (wide.variant == variant)]
    pa = d[d.model == a].set_index("seed")[metric]
    pb = d[d.model == b].set_index("seed")[metric]
    diff = (pb - pa).dropna()
    return diff


def verdict(diff: pd.Series, who: str = "hybrid") -> str:
    if len(diff) == 0:
        return "n/a"
    m, s = diff.mean(), diff.std(ddof=1) if len(diff) > 1 else np.nan
    wins = int((diff > 0).sum())
    ties = int((diff == 0).sum())
    # within noise: |mean| <= std across seeds, or below ~one minority-class test error (0.0025)
    if np.isnan(s) or abs(m) <= (s if s > 0 else 0) or abs(m) < 0.0025:
        tag = "within noise"
    else:
        tag = f"{who} better" if m > 0 else f"{who} worse"
    return f"{m:+.4f} ± {s:.4f} ({who} wins {wins}/{len(diff)} seeds, ties {ties}) → **{tag}**"


def load_preds(setting, task, model, seed=0, variant="main"):
    f = RES / "preds" / f"{setting}_{task}_{model}_{variant}_s{seed}.npz"
    if not f.exists():
        return None
    z = np.load(f)
    return z["y_true"], z["y_pred"]


# ---------------------------------------------------------------------------
def summary(wide, setting, task):
    mean, std, n = agg(wide, setting, task)
    if mean.empty:
        return None
    cls = CLASSES[task]
    order = mean.sort_values("macro_f1", ascending=False).index
    rows = {}
    for m in order:
        r = {"family": plots.family(m), "seeds": int(n[m]),
             "macro-F1": pm(mean.at[m, "macro_f1"], std.at[m, "macro_f1"]),
             "accuracy": pm(mean.at[m, "accuracy"], std.at[m, "accuracy"])}
        for c in cls:
            r[f"F1 {c}"] = pm(mean.at[m, f"f1_{c}"], std.at[m, f"f1_{c}"])
        r["FPR (macro)"] = pm(mean.at[m, "FPR_macro"], None)
        r["rules"] = "–" if pd.isna(mean.at[m, "n_rules"]) else f"{mean.at[m, 'n_rules']:.1f}"
        r["train s"] = f"{mean.at[m, 'train_time_s']:.2f}"
        r["infer ms/1k"] = f"{mean.at[m, 'infer_ms_per_1k']:.2f}"
        if setting == "A" and m in PAPER[task]:
            r["paper acc / F1"] = "{:.4f} / {:.3f}".format(*PAPER[task][m])
        elif setting == "A":
            r["paper acc / F1"] = "–"
        rows[m] = r
    t = pd.DataFrame(rows).T
    t.index.name = "model"
    if setting == "A":
        extra = {k: v for k, v in PAPER[task].items() if "paper only" in k}
        for k, (a, f) in extra.items():
            t.loc[k] = {c: "–" for c in t.columns} | {"family": "deep learning (not run)",
                                                     "paper acc / F1": f"{a:.4f} / {f:.3f}"}
    txt = [f"# Summary: Setting {setting}, {task}", "",
           "Test-set metrics, mean ± std over seeds (different subsample, split and SMOTE per seed). "
           "Sorted by macro-F1 (the primary metric). `+stk` = with the augmented stacking ANFIS.", ""]
    if setting == "A":
        txt += ["Paper columns: Al Isawi et al. (2025), Tables 6/8 (by caption). The paper's 'Overall F1' "
                "is the unweighted mean of per-class F1, i.e. macro-F1. The paper's ANFIS rows are the "
                "full stacked architecture, so they are matched to our `+stk` rows. The paper's SVM kernel "
                "is not stated; it is matched to RBF-SVM.", ""]
    txt.append(md(t))
    (RES / f"summary_{setting}_{task}.md").write_text("\n".join(txt) + "\n")
    return mean, std


def comparison1(wide, setting, task):
    mean, std, _ = agg(wide, setting, task)
    if mean.empty or PAPER_HYBRID not in mean.index:
        return None
    k = KEY_CLASS[task]
    nh = [m for m in NONHYBRID if m in mean.index]
    an = [m for m in ANFIS if m in mean.index]
    best_nh = mean.loc[nh, "macro_f1"].idxmax()
    best_h = mean.loc[an, "macro_f1"].idxmax()
    show = nh + [m for m in ["ANFIS-FCM", PAPER_HYBRID] if m in mean.index]
    if best_h not in show:
        show.append(best_h)
    rows = {}
    for m in show:
        label = m + (" (best ANFIS, post-hoc)" if m == best_h and m not in ("ANFIS-FCM", PAPER_HYBRID) else "")
        rows[label] = {"type": "hybrid" if m.startswith("ANFIS") else "non-hybrid",
                       "macro-F1": pm(mean.at[m, "macro_f1"], std.at[m, "macro_f1"]),
                       f"F1 {k}": pm(mean.at[m, f"f1_{k}"], std.at[m, f"f1_{k}"]),
                       "accuracy": pm(mean.at[m, "accuracy"], std.at[m, "accuracy"]),
                       "train s": f"{mean.at[m, 'train_time_s']:.2f}"}
    t = pd.DataFrame(rows).T
    t.index.name = "model"

    lines = [f"# Comparison 1: non-hybrid vs hybrid (Setting {setting}, {task})", "",
             "Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF "
             "(classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked "
             f"(pre-specified, `{PAPER_HYBRID}` is the headline hybrid). The best of all 8 ANFIS rows is "
             "added when different, flagged as post-hoc (chosen on the test set).", "",
             md(t), "",
             "## Paired differences (macro-F1, per seed, same test sets)", ""]
    pairs = [(best_nh, PAPER_HYBRID, "best non-hybrid vs paper hybrid"),
             (best_nh, best_h, "best non-hybrid vs best ANFIS (post-hoc)"),
             ("MLP", PAPER_HYBRID, "pure neural (MLP) vs paper hybrid"),
             ("FCM-clf", PAPER_HYBRID, "pure fuzzy (FCM-clf) vs paper hybrid")]
    seen = set()
    for a, b, lab in pairs:
        if (a, b) in seen:
            continue
        seen.add((a, b))
        if a in mean.index and b in mean.index:
            lines.append(f"- {lab} ({a} → {b}): {verdict(paired_diff(wide, setting, task, a, b))}")
    lines.append("")
    lines += ["## McNemar test (seed 0)", ""]
    mc = {}
    for b in dict.fromkeys([PAPER_HYBRID, best_h]):
        pa, pb = load_preds(setting, task, best_nh), load_preds(setting, task, b)
        if pa is not None and pb is not None:
            r = mcnemar(pa[0], pa[1], pb[1])
            mc[b] = r
            lines.append(f"- {best_nh} vs {b}: only {best_nh} correct = {r['a_only_correct']}, "
                         f"only {b} correct = {r['b_only_correct']}, exact p = {r['p_value']:.3g}")
    lines += ["", f"Figure: `figures/comparison1_{setting}_{task}.png`"]
    (RES / f"comparison1_nonhybrid_vs_hybrid_{setting}_{task}.md").write_text("\n".join(lines) + "\n")

    chart = pd.DataFrame({"mean": mean.loc[show, "macro_f1"], "std": std.loc[show, "macro_f1"]})
    plots.comparison1_chart(chart, FIG / f"comparison1_{setting}_{task}.png",
                            f"Non-hybrid vs hybrid: Setting {setting}, {task}")
    return dict(best_nh=best_nh, best_h=best_h, mean=mean, std=std, mcnemar=mc)


def comparison2(wide, params, setting, task):
    mean, std, _ = agg(wide, setting, task)
    names = [f"ANFIS-{i}" for i in INITS]
    if not all(n in mean.index for n in names):
        return None
    k = KEY_CLASS[task]
    m5, s5, _ = agg(wide, setting, task, variant="ep5")
    tab = pd.DataFrame(index=INITS)
    for i in INITS:
        n = f"ANFIS-{i}"
        for suf, mm in (("", n), ("_stk", n + "+stk")):
            tab.at[i, "f1" + suf] = mean.at[mm, "macro_f1"]
            tab.at[i, "f1" + suf + "_std"] = std.at[mm, "macro_f1"]
            tab.at[i, "cls" + suf] = mean.at[mm, f"f1_{k}"]
            tab.at[i, "cls" + suf + "_std"] = std.at[mm, f"f1_{k}"]
            tab.at[i, "rules" + suf] = mean.at[mm, "n_rules"]
            tab.at[i, "time" + suf] = mean.at[mm, "train_time_s"]
            tab.at[i, "time" + suf + "_std"] = std.at[mm, "train_time_s"]
            if mm in m5.index:
                tab.at[i, "f1_ep5" + suf] = m5.at[mm, "macro_f1"]
                tab.at[i, "f1_ep5" + suf + "_std"] = s5.at[mm, "macro_f1"]

    rows = {}
    for i in INITS:
        r = {"macro-F1 (OvR)": pm(tab.at[i, "f1"], tab.at[i, "f1_std"]),
             "macro-F1 (+stk)": pm(tab.at[i, "f1_stk"], tab.at[i, "f1_stk_std"]),
             f"F1 {k} (OvR)": pm(tab.at[i, "cls"], tab.at[i, "cls_std"]),
             f"F1 {k} (+stk)": pm(tab.at[i, "cls_stk"], tab.at[i, "cls_stk_std"]),
             "rules (OvR / +stk)": f"{tab.at[i, 'rules']:.1f} / {tab.at[i, 'rules_stk']:.1f}",
             "train s (OvR / +stk)": f"{tab.at[i, 'time']:.1f} / {tab.at[i, 'time_stk']:.1f}"}
        if "f1_ep5" in tab.columns:
            r["macro-F1 5 ep (OvR)"] = pm(tab.at[i, "f1_ep5"], tab.at[i, "f1_ep5_std"])
            r["macro-F1 5 ep (+stk)"] = pm(tab.at[i, "f1_ep5_stk"], tab.at[i, "f1_ep5_stk_std"])
        rows[f"ANFIS-{i}"] = r
    t = pd.DataFrame(rows).T
    t.index.name = "init"

    lines = [f"# Comparison 2: clustering init for ANFIS (Setting {setting}, {task})", "",
             "Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid "
             "training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use "
             "R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed "
             "over all OvR members (and the stacking ANFIS for `+stk`).", "",
             md(t), "",
             "## Paired differences vs the Random-init control (macro-F1, OvR)", ""]
    for i in INITS[1:]:
        lines.append(f"- Random → {i}: "
                     f"{verdict(paired_diff(wide, setting, task, 'ANFIS-Random', f'ANFIS-{i}'), i)}")
    lines.append(f"- KMeans → FCM (value of *fuzzy* vs hard clustering): "
                 f"{verdict(paired_diff(wide, setting, task, 'ANFIS-KMeans', 'ANFIS-FCM'), 'FCM')}")
    if "f1_ep5" in tab.columns:
        lines += ["", "## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)", ""]
        for i in INITS:
            d1 = wide[(wide.setting == setting) & (wide.task == task) & (wide.model == f"ANFIS-{i}")]
            m1 = d1[d1.variant == "main"].set_index("seed")["macro_f1"]
            m5_ = d1[d1.variant == "ep5"].set_index("seed")["macro_f1"]
            dd = (m5_ - m1).dropna()
            if len(dd):
                lines.append(f"- ANFIS-{i}: 5 ep − 1 ep = {dd.mean():+.4f} ± {dd.std():.4f}")
    sweep = rule_sweep(wide, setting, task)
    if sweep is not None:
        lines += ["", "## ANFIS-KMeans rule count R ∈ {5, 10, 20} (validation split, 5 seeds; "
                  "R = 10 stays fixed in the main tables)", "", sweep]
    lines += ["", f"Figures: `figures/comparison2_{setting}_{task}.png`, "
              f"`figures/mf_overlay_{setting}_{task}.png`"]
    (RES / f"comparison2_clustering_{setting}_{task}.md").write_text("\n".join(lines) + "\n")
    plots.comparison2_chart(tab, FIG / f"comparison2_{setting}_{task}.png",
                            f"Effect of the clustering init on ANFIS: Setting {setting}, {task}",
                            f"F1 {k}")
    mf_figure(setting, task)
    return tab


def rule_sweep(wide, setting, task):
    f = RES / "rule_sweep.csv"
    if not f.exists():
        return None
    d = pd.read_csv(f)
    d = d[(d.setting == setting) & (d.task == task)]
    if d.empty:
        return None
    g = d.groupby(["R", "model"]).agg(f1=("val_macro_f1", "mean"), f1s=("val_macro_f1", "std"),
                                      t=("train_time_s", "mean"))
    rows = {}
    for R in sorted(d.R.unique()):
        rows[f"R = {R}"] = {"val macro-F1 (OvR)": pm(g.at[(R, "OvR"), "f1"], g.at[(R, "OvR"), "f1s"]),
                            "val macro-F1 (+stk)": pm(g.at[(R, "+stk"), "f1"], g.at[(R, "+stk"), "f1s"]),
                            "train s (OvR)": f"{g.at[(R, 'OvR'), 't']:.1f}",
                            "train s (+stk)": f"{g.at[(R, '+stk'), 't']:.1f}"}
    t = pd.DataFrame(rows).T
    t.index.name = "rules per member"
    return md(t)


MF_FEATURE = {"A": "can_id", "A-noID": "log_dt", "B": "log_dt", "B-ID": "log_dt"}


def mf_figure(setting, task):
    p = {}
    for i in INITS:
        f = RES / "anfis_params" / f"{setting}_{task}_ANFIS-{i}_main.npz"
        if f.exists():
            p[i] = dict(np.load(f))
    if len(p) < len(INITS):
        return
    feats = list(next(iter(p.values()))["features"])
    feat = MF_FEATURE[setting] if MF_FEATURE[setting] in feats else feats[0]
    member = 1 if task == "multi" else 0
    who = CLASSES[task][member]
    plots.mf_overlay(p, feats.index(feat), feat, member, FIG / f"mf_overlay_{setting}_{task}.png",
                     f"MFs of input '{feat}' in the {who} OvR member, seed 0 (Setting {setting}, {task})")


def extra_figures(wide, setting, task, c1):
    mean, std, _ = agg(wide, setting, task)
    if mean.empty:
        return
    t = pd.DataFrame({"mean": mean["train_time_s"], "std": std["train_time_s"]})
    order = [m for m in NONHYBRID + ANFIS if m in t.index]
    plots.time_chart(t.loc[order], FIG / f"train_time_{setting}_{task}.png",
                     f"Training time: Setting {setting}, {task}")
    if c1:
        cms, names = [], []
        for m in (c1["best_nh"], PAPER_HYBRID):
            pr = load_preds(setting, task, m)
            if pr is not None:
                cms.append(confusion(pr[0], pr[1], len(CLASSES[task])))
                names.append(m)
        if cms:
            plots.confusion_pair(cms, names, CLASSES[task], FIG / f"confusion_{setting}_{task}.png",
                                 f"Test confusion matrices, seed 0 (Setting {setting}, {task})")


def ladder_figures(wide):
    for task in TASKS:
        data = {}
        for s in SETTINGS:
            mean, std, _ = agg(wide, s, task, models=LADDER)
            if len(mean):
                order = [m for m in LADDER if m in mean.index]
                data[s] = pd.DataFrame({"mean": mean.loc[order, "macro_f1"],
                                        "std": std.loc[order, "macro_f1"]})
        if data:
            plots.ladder_chart(data, FIG / f"ladder_{task}.png",
                               f"Hybridisation ladder, macro-F1 ({task})")


def ablations(wide):
    """Collect every non-main variant against its main counterpart."""
    lines = ["# Ablations", "",
             "Each row compares a variant with the main protocol on the same seeds "
             "(paired difference in macro-F1, variant − main).", ""]
    rows = []
    for (s, t, m, v), d in wide[wide.variant != "main"].groupby(["setting", "task", "model", "variant"]):
        base = wide[(wide.setting == s) & (wide.task == t) & (wide.model == m) & (wide.variant == "main")]
        x = d.set_index("seed")["macro_f1"]
        b = base.set_index("seed")["macro_f1"]
        dd = (x - b).dropna()
        rows.append({"setting": s, "task": t, "model": m, "variant": v, "seeds": len(dd),
                     "main": pm(b.loc[dd.index].mean(), b.loc[dd.index].std()),
                     "variant value": pm(x.loc[dd.index].mean(), x.loc[dd.index].std()),
                     "Δ (variant − main)": pm(dd.mean(), dd.std()) if len(dd) else "–"})
    if rows:
        t = pd.DataFrame(rows).set_index("setting")
        lines.append(md(t))
    # stacking on/off and A vs A-noID from the main runs
    lines += ["", "## Stacking on/off (main runs, Δ = +stk − OvR)", ""]
    srows = []
    for s in SETTINGS:
        for t in TASKS:
            for i in INITS:
                dd = paired_diff(wide, s, t, f"ANFIS-{i}", f"ANFIS-{i}+stk")
                if len(dd):
                    srows.append({"setting": s, "task": t, "init": i, "Δ macro-F1": pm(dd.mean(), dd.std())})
    if srows:
        lines.append(md(pd.DataFrame(srows).set_index("setting")))
    lines += ["", "## Effect of removing the CAN ID (A → A-noID, B-ID → B), macro-F1 means", ""]
    crows = []
    for t in TASKS:
        for with_id, no_id in (("A", "A-noID"), ("B-ID", "B")):
            m1, _, _ = agg(wide, with_id, t)
            m2, _, _ = agg(wide, no_id, t)
            for m in [x for x in NONHYBRID + ANFIS if x in m1.index and x in m2.index]:
                crows.append({"pair": f"{with_id} → {no_id}", "task": t, "model": m,
                              "with ID": f"{m1.at[m, 'macro_f1']:.4f}",
                              "without ID": f"{m2.at[m, 'macro_f1']:.4f}",
                              "Δ": f"{m2.at[m, 'macro_f1'] - m1.at[m, 'macro_f1']:+.4f}"})
    if crows:
        lines.append(md(pd.DataFrame(crows).set_index("pair")))
    (RES / "ablations.md").write_text("\n".join(lines) + "\n")


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    wide, params = load()
    out = {}
    for s in SETTINGS:
        for t in TASKS:
            if wide[(wide.setting == s) & (wide.task == t)].empty:
                continue
            summary(wide, s, t)
            c1 = comparison1(wide, s, t)
            c2 = comparison2(wide, params, s, t)
            extra_figures(wide, s, t, c1)
            out[(s, t)] = (c1, c2)
    ladder_figures(wide)
    ablations(wide)
    from .notes import write_notes
    write_notes(wide, out)
    print("report written to", RES)


if __name__ == "__main__":
    main()
