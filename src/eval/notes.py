"""Auto-generate results/REPORT_NOTES.md from the computed results.

Every number in the notes comes from results/*.csv. Static text covers only the protocol,
deviations and caveats. Interpretation that needs judgement lives in
results/commentary.md (hand-written after reading the numbers) and is appended verbatim.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from .report import (ANFIS, CLASSES, INITS, KEY_CLASS, NONHYBRID, PAPER, PAPER_HYBRID,
                     PAPER_IMP_F1, RES, SETTINGS, TASKS, agg, md, paired_diff, pm, verdict)

SETTING_DESC = {
    "A": "paper-faithful: labels by CAN ID, 10 features incl. CAN ID",
    "A-noID": "paper labels, CAN ID removed, + log inter-arrival time (main benchmark)",
    "B": "corrected labels (Imp = 0x164 after t0+250 s), no CAN ID (learnability probe)",
    "B-ID": "corrected labels, with CAN ID",
}


def _section_data() -> list[str]:
    f = RES / "data_report.md"
    out = ["## 1. Data-labelling findings", ""]
    if not f.exists():
        return out + ["(run `scripts/data_report.py`)", ""]
    txt = f.read_text()
    m = re.search(r"## 3\. Impersonation log.*?\n\n(.*?)\n## 4", txt, re.S)
    concl = re.search(r"## 5\. Conclusions for the experimental design\n\n(.*?)\n\nFigures", txt, re.S)
    out += ["Full details: `results/data_report.md`. Key evidence (impersonation log, 0x164 frames):", ""]
    if m:
        out += [ln for ln in m.group(1).splitlines() if ln.startswith("- ")] + [""]
    if concl:
        out += [concl.group(1), ""]
    return out


def _section_repro(wide) -> list[str]:
    out = ["## 2. Did Setting A reproduce the paper?", ""]
    rows = []
    for task in TASKS:
        mean, std, _ = agg(wide, "A", task)
        for m, (pa, pf) in PAPER[task].items():
            if m not in mean.index:
                continue
            rows.append({"task": task, "model": m, "paper acc": f"{pa:.4f}", "ours acc": pm(mean.at[m, "accuracy"], std.at[m, "accuracy"]),
                         "paper macro-F1": f"{pf:.3f}", "ours macro-F1": pm(mean.at[m, "macro_f1"], std.at[m, "macro_f1"])})
        if task == "multi":
            for m, f in PAPER_IMP_F1.items():
                if m in mean.index:
                    rows.append({"task": task, "model": m + " (Imp F1)", "paper acc": "–", "ours acc": "–",
                                 "paper macro-F1": f"{f:.3f}", "ours macro-F1": pm(mean.at[m, "f1_Imp"], std.at[m, "f1_Imp"])})
    if not rows:
        return out + ["(no Setting A results)", ""]
    t = pd.DataFrame(rows).set_index("task")
    out += [md(t), ""]
    mean_b, _, _ = agg(wide, "A", "binary")
    mean_m, _, _ = agg(wide, "A", "multi")
    ceiling = [m for m in mean_m.index if mean_m.at[m, "macro_f1"] >= 0.99]
    out += [f"- Setting A, multiclass: {len(ceiling)} of {len(mean_m)} models reach macro-F1 ≥ 0.99 "
            f"({', '.join(sorted(ceiling))}).",
            f"- The paper's ANFIS-SC/FCM results (≈ 99.6–99.7 % accuracy) are reproduced and slightly "
            f"exceeded: ours {PAPER_HYBRID} binary accuracy = {mean_b.at[PAPER_HYBRID, 'accuracy']:.4f}, "
            f"multiclass = {mean_m.at[PAPER_HYBRID, 'accuracy']:.4f}.",
            f"- The paper's weak linear baselines are also reproduced in kind: LDA binary macro-F1 = "
            f"{mean_b.at['LDA', 'macro_f1']:.3f} (paper 0.819). The CAN ID 0x164 = 356 lies in the middle "
            "of the ID range, so no single linear cut on the ID isolates it, while a rule- or tree-based "
            "model can carve out the ID value. Our LR/linear SVM score higher than the paper's "
            "(see `results/commentary.md` for the check of why).",
            "- Conclusion: the ~99.6 % headline is a property of the setting, not evidence that the hybrid "
            "model is needed. The labels are a function of the CAN ID, which is also an input. For DoS the "
            "ID-based label is correct (no real ECU uses 0x000) and the ID simply makes it trivial. For "
            "Impersonation, a legitimate ID, the label also covers genuine ECU frames, so the class measures "
            "ID recognition (label leakage).", ""]
    return out


def _section_c1(wide, results) -> list[str]:
    out = ["## 3. Comparison 1: non-hybrid vs hybrid", "",
           f"Headline hybrid = `{PAPER_HYBRID}` (pre-specified as the paper's best architecture). Positive "
           "Δ = hybrid better. 'Within noise' = |mean paired Δ| ≤ its std across the 5 seeds, or |Δ| < 0.0025 (about one Imp-class test error, ≈196 Imp test frames).", ""]
    rows = []
    for s in SETTINGS:
        for t in TASKS:
            c1 = results.get((s, t), (None, None))[0]
            if not c1:
                continue
            mean, std = c1["mean"], c1["std"]
            bnh, bh = c1["best_nh"], c1["best_h"]
            k = KEY_CLASS[t]
            mc = c1["mcnemar"].get(PAPER_HYBRID)
            rows.append({"setting": s, "task": t,
                         "best non-hybrid": f"{bnh} {mean.at[bnh, 'macro_f1']:.4f}",
                         "MLP": f"{mean.at['MLP', 'macro_f1']:.4f}",
                         "FCM-clf": f"{mean.at['FCM-clf', 'macro_f1']:.4f}",
                         PAPER_HYBRID: f"{mean.at[PAPER_HYBRID, 'macro_f1']:.4f}",
                         "best ANFIS (post-hoc)": f"{bh} {mean.at[bh, 'macro_f1']:.4f}",
                         "key-class F1: best NH / hybrid": f"{k}: {mean.at[bnh, f'f1_{k}']:.3f} / {mean.at[PAPER_HYBRID, f'f1_{k}']:.3f}",
                         "McNemar p (seed 0)": "–" if mc is None else f"{mc['p_value']:.3g}"})
    if rows:
        out += [md(pd.DataFrame(rows).set_index("setting")), ""]
    out += ["Paired verdicts (macro-F1):", ""]
    for s in SETTINGS:
        for t in TASKS:
            c1 = results.get((s, t), (None, None))[0]
            if not c1:
                continue
            bnh = c1["best_nh"]
            parts = [f"{a} → {PAPER_HYBRID}: {verdict(paired_diff(wide, s, t, a, PAPER_HYBRID))}"
                     for a in dict.fromkeys([bnh, "MLP", "FCM-clf"])]
            out.append(f"- **{s} / {t}**: " + "; ".join(parts))
    out += ["", "Per-setting tables: `results/comparison1_nonhybrid_vs_hybrid_<setting>_<task>.md`; "
            "figures: `results/figures/comparison1_*.png`, `results/figures/ladder_*.png`.", ""]
    return out


def _section_c2(wide, results) -> list[str]:
    out = ["## 4. Comparison 2: effect of the clustering init on ANFIS", "",
           "Random (control) vs K-Means (hard clustering) vs SC vs FCM (fuzzy clustering). Only the "
           "initial FIS changes. K-Means vs FCM isolates the value of *fuzzy* (partial) memberships over "
           "hard assignment at the same rule count.", ""]
    rows = []
    for s in SETTINGS:
        for t in TASKS:
            tab = results.get((s, t), (None, None))[1]
            if tab is None:
                continue
            r = {"setting": s, "task": t}
            for i in INITS:
                r[f"{i} OvR / +stk"] = f"{tab.at[i, 'f1']:.4f} / {tab.at[i, 'f1_stk']:.4f}"
            r["rules OvR (R/K/SC/F)"] = " / ".join(f"{tab.at[i, 'rules']:.0f}" for i in INITS)
            r["train s OvR (R/K/SC/F)"] = " / ".join(f"{tab.at[i, 'time']:.1f}" for i in INITS)
            rows.append(r)
    if rows:
        out += ["Macro-F1 means (OvR / stacked):", "", md(pd.DataFrame(rows).set_index("setting")), ""]
    out += ["Paired verdicts vs the Random control (OvR macro-F1):", ""]
    for s in SETTINGS:
        for t in TASKS:
            if results.get((s, t), (None, None))[1] is None:
                continue
            parts = [f"{i}: {verdict(paired_diff(wide, s, t, 'ANFIS-Random', f'ANFIS-{i}'), i)}"
                     for i in INITS[1:]]
            out.append(f"- **{s} / {t}**: " + "; ".join(parts))
    ep5 = wide[wide.variant == "ep5"]
    if len(ep5):
        out += ["", "1 vs 5 epochs (OvR macro-F1, mean over seeds):", ""]
        for (s, t), d in ep5.groupby(["setting", "task"]):
            parts = []
            for i in INITS:
                a = wide[(wide.setting == s) & (wide.task == t) & (wide.model == f"ANFIS-{i}")]
                m1 = a[a.variant == "main"].macro_f1.mean()
                m5 = a[a.variant == "ep5"].macro_f1.mean()
                if not np.isnan(m5):
                    parts.append(f"{i} {m1:.4f} → {m5:.4f}")
            out.append(f"- **{s} / {t}**: " + "; ".join(parts))
    out += ["", "Per-setting tables: `results/comparison2_clustering_<setting>_<task>.md`; figures: "
            "`results/figures/comparison2_*.png`, `results/figures/mf_overlay_*.png`.", ""]
    return out


wide_cache: dict = {}


def id_rule_baseline():
    """Imp F1 of the rule 'Imp iff CAN ID = 0x164' on each seed's Setting B test set.
    B-ID draws exactly the same rows as B (same pool, seed and split) and keeps can_id."""
    from sklearn.metrics import f1_score
    from ..data.build_dataset import load_config, make_split
    cfg = load_config()
    vals = []
    for seed in cfg["seeds"]:
        sp = make_split("B-ID", "multi", seed, cfg)
        cid = sp.X_test[:, sp.features.index("can_id")]
        pred = sp.y_test.copy()
        pred[cid == 0x164] = 1
        pred[(cid != 0x164) & (pred == 1)] = 2
        vals.append(f1_score(sp.y_test, pred, labels=[1], average=None)[0])
    return pd.Series(vals)


def _section_probe() -> list[str]:
    f = RES / "probe_B.md"
    out = ["## 5. Setting B: is the corrected Impersonation label learnable?", ""]
    if not f.exists():
        return out + ["(run `scripts/probe_B.py`)", ""]
    body = f.read_text().split("\n", 2)[2]
    out += [body.strip(), ""]
    p = pd.read_csv(RES / "probe_B.csv")
    real = p[p.data.str.startswith("impersonation")]
    ctrl = p[p.data.str.startswith("attack-free")]
    rule = id_rule_baseline()
    if rule is not None:
        mean_b, std_b, _ = agg(wide_cache["wide"], "B", "multi")
        best = mean_b["f1_Imp"].idxmax()
        out += [f"- **Reference rule 'Imp iff CAN ID = 0x164'** on the same Setting B test sets: Imp F1 = "
                f"{rule.mean():.4f} ± {rule.std():.4f}. The best trained model reaches Imp F1 = "
                f"{mean_b.at[best, 'f1_Imp']:.4f} ± {std_b.at[best, 'f1_Imp']:.4f} ({best}), i.e. the models "
                "learn to recognise 0x164-type messages, not the attack."]
    out += [f"- Best AUC on the real boundary: {real['ROC AUC'].max():.3f} "
            f"({real.loc[real['ROC AUC'].idxmax(), 'model']}, {real.loc[real['ROC AUC'].idxmax(), 'features']}); "
            f"best AUC on the fake boundary (control): {ctrl['ROC AUC'].max():.3f}.", ""]
    return out


def write_notes(wide, results):
    wide_cache["wide"] = wide
    out = ["# REPORT_NOTES (auto-generated by `python -m src.eval.report`)", "",
           "Reproduction and extension of Al Isawi et al., *Electric Vehicles CAN Bus Cyber Attacks "
           "Detection Using ANFIS*, IEEE Access 13 (2025). All numbers are test-set means ± std over 5 seeds "
           "(each seed draws a new 20,000-row subsample, stratified 80/20 split and SMOTE), unless stated.", "",
           "Settings:", ""]
    out += [f"- **{k}**: {v}" for k, v in SETTING_DESC.items()] + [""]
    out += _section_data()
    out += _section_repro(wide)
    out += _section_c1(wide, results)
    out += _section_c2(wide, results)
    out += _section_probe()
    out += ["## 6. Ablations", "", "See `results/ablations.md` (stacking on/off, paper vs OOF stacking, "
            "SMOTE on/off, 1 vs 5 epochs, with vs without CAN ID).", ""]
    out += [DEVIATIONS, CAVEATS]
    c = RES / "commentary.md"
    if c.exists():
        out += [c.read_text()]
    (RES / "REPORT_NOTES.md").write_text("\n".join(out) + "\n")


DEVIATIONS = """## 7. Deviations from the paper and the original brief

- **Settings revised after inspecting the data.** The brief's Setting B (post-250 s 0x164 = Imp) is
  kept, but as a learnability probe: Section 1 shows the label has almost no per-frame signal. The
  main extension benchmark is **A-noID** (paper labels, CAN ID removed, + log inter-arrival time).
- **Sampling.** The paper does not say which files its 20,000 rows came from, and its class ratios
  (7.5 % DoS, 4.9 % Imp) match no log's natural ratio. We draw DoS = 0x000 frames from the DoS log,
  Imp = 0x164 frames from the impersonation log, Normal = other-ID frames from the attack-free log
  (Setting A). Split is stratified 80/20 (train 1198/783/14019 vs the paper's 1180/784/14036, which
  was a random split).
- **Setting B Normal** is drawn from the impersonation log itself (all frames before 250 s plus
  non-0x164 frames after), so Imp and genuine 0x164 come from the same recording session.
- **DoS log has no attack-free window.** 0x000 injection runs from t = 0, unlike HCRL's 250 s
  description for Fuzzy/Impersonation, so no time-based relabelling is applied to DoS.
- **Inter-arrival feature** is log10(dt_same_id) (heavy-tailed; min-max would squash it).
- **ANFIS** is implemented from scratch in PyTorch (the paper used MATLAB). The hybrid rule is
  LSE (ridge 1e-6) + one Adam pass on premise parameters per epoch. The consequents are re-solved once
  after the final premise update. Initial FIS clustering runs on the joint input-output space
  [X, target], as genfis2/genfis3 do.
- **SC squash factor.** The paper's 0.20/0.25 (radius 0.20/0.25) is used: it gives a sensible 5–25
  rules per member. MATLAB's default 1.25 collapses to 2 rules per member and loses accuracy.
  SC runs on a stratified subsample of ≤ 5,000 training points (O(N²)).
- **Stacking target.** The augmented ANFIS regresses the integer class index and is rounded and
  clipped (our reading of the paper's ambiguous description). Default `stack_mode = paper`
  (in-sample stage-1 outputs); `oof` (5-fold out-of-fold) is reported as an ablation.
- **Tuning.** Baseline hyperparameters are chosen on a validation split (20 % of training, carved
  before SMOTE). ANFIS uses the paper's values unchanged. The paper describes no validation split (it tunes "while training" and reports test results), so test-set leakage cannot be ruled out; we never touch the test set.
- **Baselines.** The paper's deep-learning multiclass baselines (CNN, CNN-LSTM, GRU, LSTM) were
  not re-run; their reported numbers are quoted in the Setting A summary.
- **Paper table numbering**: in-text references are off by one versus the captions. We cite captions.
"""

CAVEATS = """## 8. Caveats

- Setting A is at the ceiling for most models, so differences there are within noise by construction.
- 'Best ANFIS (post-hoc)' is selected on the test set and is optimistic. The headline comparison uses
  the pre-specified `ANFIS-FCM+stk`.
- Training times are wall-clock on one machine (20-core CPU, 8-thread cap; ANFIS on an RTX 4060 GPU).
  They are indicative only and not comparable to the paper's MATLAB timings.
- OOF stacking folds are taken over the SMOTE-resampled training set, so synthetic neighbours can
  straddle folds. This is a mild leak, the same for all inits.
- With only 979 Imp frames per 20k sample (≈196 in test), one Imp error moves Imp F1 by ≈ 0.003.
- The 0x164 timing shift in the impersonation log (Section 1) is small. We cannot tell whether it
  comes from the attack or from changing drive conditions.
"""
