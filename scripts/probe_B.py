"""Setting B learnability probe: can any model tell 0x164 frames after t0+250 s (labelled
Impersonation) from 0x164 frames before 250 s (genuine), per frame?

Time-blocked CV: frames are grouped in 10 s blocks and whole blocks go to one fold, so
neighbouring (correlated) frames never sit on both sides of a split. Folds are stratified
(StratifiedGroupKFold) and AUC is computed within each fold, then averaged. Pooling
out-of-fold scores across folds whose class mix differs gives spurious below-chance AUCs
(a no-signal model just echoes its training prior, which anti-correlates with the test fold).
Control: the same probe on the attack-free log, with a fake boundary at 250 s
(first 500 s only), which measures what drift over time alone produces.
"""
from __future__ import annotations

import os  # noqa: E402  (cap native thread pools before numpy/torch load; see src/__init__.py)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "8")

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import MinMaxScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.build_dataset import _log  # noqa: E402
from src.models.anfis import fit_anfis, predict  # noqa: E402
from src.models.inits import init_fcm  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
BYTES = [f"d{i}" for i in range(8)]
GROUPS = {"payload+DLC": ["dlc"] + BYTES,
          "timing (log_dt, hamming)": ["log_dt", "hamming_prev"],
          "all": ["dlc"] + BYTES + ["log_dt", "hamming_prev"]}


def anfis_fcm(Xtr, ytr, Xte, seed):
    Z = np.column_stack([Xtr, ytr])
    C, S = init_fcm(Z, seed=seed, n_clusters=10)
    m = fit_anfis(C[:, :-1], S[:, :-1], Xtr, ytr.astype(float), epochs=1, seed=seed)
    return np.clip(predict(m, Xte), 0, 1)


MODELS = {
    "LR": lambda a, b, c, s: LogisticRegression(max_iter=2000).fit(a, b).predict_proba(c)[:, 1],
    "RF": lambda a, b, c, s: RandomForestClassifier(300, min_samples_leaf=5, n_jobs=8,
                                                    random_state=s).fit(a, b).predict_proba(c)[:, 1],
    "ANFIS-FCM": anfis_fcm,
}


def probe(df, label, feats, seed=0):
    X = df[feats].to_numpy(float)
    y = label.astype(int)
    groups = (df.t_rel // 10).astype(int).to_numpy()
    res = {}
    folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=seed).split(X, y, groups))
    for name, fn in MODELS.items():
        aucs = []
        for tr, te in folds:
            sc = MinMaxScaler().fit(X[tr])
            s_te = fn(sc.transform(X[tr]), y[tr], sc.transform(X[te]), seed)
            aucs.append(roc_auc_score(y[te], s_te) if len(np.unique(y[te])) == 2 else np.nan)
        res[name] = (np.nanmean(aucs), np.nanstd(aucs))
    return res


def main():
    imp = _log("impersonation")
    s = imp[(imp.can_id == 0x164)].reset_index(drop=True)
    lab = (s.t_rel >= 250).to_numpy()
    af = _log("attack_free")
    c = af[(af.can_id == 0x164) & (af.t_rel < 500)].reset_index(drop=True)
    lab_c = (c.t_rel >= 250).to_numpy()

    rows = []
    for gname, feats in GROUPS.items():
        for data, y, which in ((s, lab, "impersonation log (real boundary)"),
                               (c, lab_c, "attack-free log (fake boundary, control)")):
            for model, (auc, sd) in probe(data, y, feats).items():
                rows.append({"data": which, "features": gname, "model": model,
                             "ROC AUC": round(auc, 4), "AUC std (folds)": round(sd, 4)})
                print(rows[-1])
    t = pd.DataFrame(rows)
    t.to_csv(RES / "probe_B.csv", index=False)
    lines = ["# Setting B learnability probe", "",
             f"Task: classify each 0x164 frame of the impersonation log as after 250 s ('Impersonation', "
             f"n = {lab.sum():,}) or before 250 s (genuine, n = {(~lab).sum():,}). 5-fold CV with "
             "10 s time blocks as groups (stratified), AUC computed per fold and averaged. Control: identical probe on attack-free 0x164 frames with a fake "
             f"boundary at 250 s (n = {len(c):,}). AUC = 0.5 means no per-frame signal.", "",
             "| data | features | model | ROC AUC (mean ± std over folds) |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['data']} | {r['features']} | {r['model']} | "
                     f"{r['ROC AUC']:.3f} ± {r['AUC std (folds)']:.3f} |")
    (RES / "probe_B.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
