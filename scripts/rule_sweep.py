"""ANFIS-KMeans rule-count sweep R in {5, 10, 20}, scored on the validation split only
(20% of training, carved before SMOTE). Writes results/rule_sweep.csv.
"""
from __future__ import annotations

import os  # noqa: E402  (cap native thread pools before numpy/torch load; see src/__init__.py)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "8")

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_all import anfis_init_params, anfis_params  # noqa: E402
from src.data.build_dataset import load_config, make_split, preprocess, val_split  # noqa: E402
from src.models.anfis_classifiers import StackedANFIS  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--setting", nargs="+", default=["A", "A-noID"])
    ap.add_argument("--task", nargs="+", default=["binary", "multi"])
    ap.add_argument("--seeds", type=int, default=5)
    args = ap.parse_args()
    cfg = load_config()
    rows = []
    for setting in args.setting:
        for task in args.task:
            for seed in cfg["seeds"][: args.seeds]:
                sp = make_split(setting, task, seed, cfg)
                Xa, Xv, ya, yv = val_split(sp.X_train, sp.y_train, seed, cfg)
                Xa, ya, (Xv,), _ = preprocess(Xa, ya, [Xv], seed, cfg)
                for R in cfg["anfis"]["kmeans"]["sweep"]:
                    t = time.perf_counter()
                    m = StackedANFIS("kmeans", anfis_init_params("kmeans", task, cfg, R),
                                     anfis_params(cfg, 1), seed=seed).fit(Xa, ya)
                    tt = time.perf_counter() - t
                    for name, yp, tm in (("OvR", m.stage1.predict(Xv), m.stage1_time),
                                         ("+stk", m.predict(Xv), tt)):
                        rows.append(dict(setting=setting, task=task, seed=seed, R=R, model=name,
                                         val_macro_f1=f1_score(yv, yp, average="macro"),
                                         train_time_s=tm))
                    print(rows[-2], rows[-1]["val_macro_f1"])
    pd.DataFrame(rows).to_csv(RES / "rule_sweep.csv", index=False)


if __name__ == "__main__":
    main()
