"""Per-run metrics. Primary metric: macro-F1."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support


def compute_metrics(y_true, y_pred, class_names: list[str]) -> dict[str, float]:
    labels = list(range(len(class_names)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    p, r, f, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    out = {"accuracy": accuracy_score(y_true, y_pred), "macro_f1": float(np.mean(f)),
           "macro_precision": float(np.mean(p)), "macro_recall": float(np.mean(r))}
    n = cm.sum()
    rates = {"TPR": [], "TNR": [], "FPR": [], "FNR": []}
    for i, c in enumerate(class_names):
        tp = cm[i, i]
        fn = cm[i].sum() - tp
        fp = cm[:, i].sum() - tp
        tn = n - tp - fn - fp
        vals = {"TPR": tp / max(tp + fn, 1), "TNR": tn / max(tn + fp, 1),
                "FPR": fp / max(fp + tn, 1), "FNR": fn / max(fn + tp, 1)}
        out.update({f"precision_{c}": p[i], f"recall_{c}": r[i], f"f1_{c}": f[i]})
        for k, v in vals.items():
            out[f"{k}_{c}"] = float(v)
            rates[k].append(v)
    out.update({f"{k}_macro": float(np.mean(v)) for k, v in rates.items()})
    return {k: float(v) for k, v in out.items()}


def confusion(y_true, y_pred, n_classes: int) -> np.ndarray:
    return confusion_matrix(y_true, y_pred, labels=list(range(n_classes)))
