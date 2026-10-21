"""Run models under one identical protocol and append results to results/metrics_long.csv.

Example:
    python scripts/run_all.py --setting A A-noID --task binary multi --seeds 5
    python scripts/run_all.py --setting A-noID --task multi --models ANFIS-KMeans --epochs 5
"""
from __future__ import annotations

import os  # noqa: E402  (cap native thread pools before numpy/torch load; see src/__init__.py)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "8")

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.build_dataset import load_config, make_split, preprocess, val_split  # noqa: E402
from src.eval.metrics import compute_metrics  # noqa: E402
from src.models.anfis_classifiers import OvRANFIS, StackedANFIS  # noqa: E402
from src.models.baselines import baseline_grid, make_baseline  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
BASELINES = ["MLP", "FCM-clf", "LDA", "LR", "LinSVM", "RBF-SVM", "RF"]
ANFIS_INITS = {"ANFIS-Random": "random", "ANFIS-KMeans": "kmeans", "ANFIS-SC": "sc",
               "ANFIS-FCM": "fcm"}
ALL_MODELS = BASELINES + list(ANFIS_INITS)


def anfis_init_params(init: str, task: str, cfg: dict, n_rules: int | None = None) -> dict:
    a = cfg["anfis"]
    if init == "sc":
        p = dict(a["sc"]["binary" if task == "binary" else "multi"])
        p["max_points"] = a["sc"]["max_points"]
        return p
    if init == "fcm":
        p = dict(a["fcm"])
    elif init == "kmeans":
        p = {k: v for k, v in a["kmeans"].items() if k != "sweep"}
    else:
        p = {"n_clusters": a["n_rules"]}
    if n_rules is not None:
        p["n_clusters"] = n_rules
    return p


def anfis_params(cfg: dict, epochs: int) -> dict:
    a = cfg["anfis"]
    return dict(epochs=epochs, lr=a["lr"], batch_size=a["batch_size"], ridge=a["ridge"],
                sigma_min=a["sigma_min"])


def timed_predict(model, X):
    t = time.perf_counter()
    yp = model.predict(X)
    return yp, (time.perf_counter() - t) / len(X) * 1000.0


# ---------------------------------------------------------------------------
def run_baseline(name, split, seed, cfg, smote, log):
    grid = baseline_grid(name, cfg)
    best = grid[0]
    if len(grid) > 1:                        # tune on validation (20% of train, pre-SMOTE)
        Xa, Xv, ya, yv = val_split(split.X_train, split.y_train, seed, cfg)
        Xa, ya, (Xv,), _ = preprocess(Xa, ya, [Xv], seed, cfg, smote, log)
        scores = []
        for p in grid:
            m = make_baseline(name, seed, **p).fit(Xa, ya)
            scores.append(f1_score(yv, m.predict(Xv), average="macro"))
        best = grid[int(np.argmax(scores))]
        log(f"    tuned {name}: {best} (val macro-F1 {max(scores):.4f})")
    Xtr, ytr, (Xte,), _ = preprocess(split.X_train, split.y_train, [split.X_test], seed, cfg,
                                     smote, log)
    t = time.perf_counter()
    m = make_baseline(name, seed, **best).fit(Xtr, ytr)
    train_time = time.perf_counter() - t
    yp, inf = timed_predict(m, Xte)
    extra = {"n_rules": getattr(m, "n_rules", np.nan)}
    return [(name, yp, train_time, inf, extra, json.dumps(best, default=str))]


def run_anfis(name, split, seed, cfg, smote, epochs, stack_mode, n_rules, log):
    """One stacked fit yields two result rows: stage-1 OvR and the full stacked model."""
    init = ANFIS_INITS[name]
    ip = anfis_init_params(init, split.task, cfg, n_rules)
    ap = anfis_params(cfg, epochs)
    note = {"init_params": ip, "epochs": epochs}
    if epochs > 1:
        # choose per-member epoch count by early stopping on a validation split (pre-SMOTE),
        # then refit on the full training set with that count
        Xa, Xv, ya, yv = val_split(split.X_train, split.y_train, seed, cfg)
        Xa, ya, (Xv,), _ = preprocess(Xa, ya, [Xv], seed, cfg, smote, log)
        sel = OvRANFIS(init, ip, dict(ap, patience=2), seed=seed).fit(Xa, ya, Xv, yv)
        ap["epochs"] = [int(np.argmin(m.val_history)) + 1 for m in sel.models_]
        note["epochs_selected"] = ap["epochs"]
        log(f"    {name}: early-stopping epochs per member = {ap['epochs']}")
    Xtr, ytr, (Xte,), _ = preprocess(split.X_train, split.y_train, [split.X_test], seed, cfg,
                                     smote, log)
    t = time.perf_counter()
    m = StackedANFIS(init, ip, ap, stack_mode=stack_mode, oof_folds=cfg["anfis"]["oof_folds"],
                     seed=seed).fit(Xtr, ytr)
    total = time.perf_counter() - t
    t_stage1 = m.stage1_time          # the unstacked row is not charged for stage 2
    yp1, inf1 = timed_predict(m.stage1, Xte)
    yp2, inf2 = timed_predict(m, Xte)
    note["rules_per_member"] = m.stage1.rules_per_member
    note_s = json.dumps(note, default=str)
    m.params_dump = {f"m{i}_{k}": v for i, mm in enumerate(m.stage1.models_)
                     for k, v in (("c0", mm.init_state["centers"].numpy()),
                                  ("s0", np.exp(mm.init_state["log_sigma"].numpy())),
                                  ("c1", mm.centers.detach().cpu().numpy()),
                                  ("s1", mm.sigmas.detach().cpu().numpy()))}
    return [(name, yp1, t_stage1, inf1, {"n_rules": m.stage1.n_rules}, note_s),
            (name + "+stk", yp2, total, inf2, {"n_rules": m.n_rules}, note_s)], m


def flush(rows, out: Path) -> int:
    """Merge rows into the long CSV, replacing earlier rows for the same run keys."""
    new = pd.DataFrame(rows)
    if out.exists():
        old = pd.read_csv(out)
        keys = ["setting", "task", "model", "variant", "seed"]
        done = new[keys].drop_duplicates()
        old = old.merge(done, on=keys, how="left", indicator=True)
        old = old[old["_merge"] == "left_only"].drop(columns="_merge")
        new = pd.concat([old, new], ignore_index=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    new.to_csv(out, index=False)
    return len(new)


# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--setting", nargs="+", default=["A"])
    ap.add_argument("--task", nargs="+", default=["multi"], choices=["binary", "multi"])
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--seed-list", type=int, nargs="+")
    ap.add_argument("--models", nargs="+", default=ALL_MODELS)
    ap.add_argument("--epochs", type=int, default=None, help="ANFIS epochs (default from config)")
    ap.add_argument("--stack-mode", default=None, choices=["paper", "oof"])
    ap.add_argument("--n-rules", type=int, default=None, help="override R for Random/KMeans/FCM")
    ap.add_argument("--no-smote", action="store_true")
    ap.add_argument("--tag", default="", help="variant tag stored in the 'variant' column")
    ap.add_argument("--out", default=str(RES / "metrics_long.csv"))
    args = ap.parse_args(argv)

    cfg = load_config()
    seeds = args.seed_list or cfg["seeds"][: args.seeds]
    epochs = args.epochs or cfg["anfis"]["epochs"]
    stack_mode = args.stack_mode or cfg["anfis"]["stack_mode"]
    smote = not args.no_smote
    variant = args.tag or "main"
    (RES / "preds").mkdir(parents=True, exist_ok=True)
    (RES / "anfis_params").mkdir(parents=True, exist_ok=True)
    log = print

    for setting, task, seed in itertools.product(args.setting, args.task, seeds):
        rows = []
        split = make_split(setting, task, seed, cfg)
        log(f"== setting={setting} task={task} seed={seed} variant={variant} "
            f"(train {np.bincount(split.y_train).tolist()}, test {np.bincount(split.y_test).tolist()})")
        for name in args.models:
            t0 = time.perf_counter()
            if name in ANFIS_INITS:
                results, model = run_anfis(name, split, seed, cfg, smote, epochs, stack_mode,
                                           args.n_rules, log)
                if seed == cfg["seeds"][0]:
                    np.savez(RES / "anfis_params" / f"{setting}_{task}_{name}_{variant}.npz",
                             features=np.array(split.features), **model.params_dump)
            else:
                results = run_baseline(name, split, seed, cfg, smote, log)
            for mname, yp, ttrain, tinf, extra, note in results:
                met = compute_metrics(split.y_test, yp, split.class_names)
                met.update(train_time_s=ttrain, infer_ms_per_1k=tinf * 1000.0, **extra)
                for k, v in met.items():
                    rows.append(dict(setting=setting, task=task, model=mname, variant=variant,
                                     seed=seed, metric=k, value=v))
                rows.append(dict(setting=setting, task=task, model=mname, variant=variant,
                                 seed=seed, metric="params", value=note))
                np.savez_compressed(RES / "preds" / f"{setting}_{task}_{mname}_{variant}_s{seed}.npz",
                                    y_true=split.y_test, y_pred=yp)
                log(f"  {mname:<18} macroF1={met['macro_f1']:.4f} acc={met['accuracy']:.4f} "
                    f"F1_{split.class_names[0]}={met['f1_' + split.class_names[0]]:.4f} "
                    f"rules={extra.get('n_rules')} train={ttrain:.1f}s "
                    f"[{time.perf_counter() - t0:.0f}s]")
        n = flush(rows, Path(args.out))
        log(f"  -> {args.out} ({n} rows)", flush=True)


if __name__ == "__main__":
    main()
