"""Non-hybrid baselines (N1 MLP, N2 FCM classifier, N3 classical ML) and their small tuning grids."""
from __future__ import annotations

import warnings

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC

from .fcm_classifier import FCMClassifier

warnings.filterwarnings("ignore", category=ConvergenceWarning)


def make_baseline(name: str, seed: int, **p):
    if name == "LDA":
        return LinearDiscriminantAnalysis()
    if name == "LR":
        return LogisticRegression(C=p.get("C", 1.0), max_iter=2000, random_state=seed)
    if name == "LinSVM":
        return LinearSVC(C=p.get("C", 1.0), max_iter=5000, random_state=seed)
    if name == "RBF-SVM":
        return SVC(C=p.get("C", 1.0), kernel="rbf", gamma="scale", random_state=seed)
    if name == "RF":
        return RandomForestClassifier(n_estimators=p.get("n_estimators", 200),
                                      max_depth=p.get("max_depth"), n_jobs=8, random_state=seed)
    if name == "MLP":
        return MLPClassifier(hidden_layer_sizes=tuple(p.get("hidden", (64,))),
                             learning_rate_init=p.get("lr", 1e-3), max_iter=p.get("max_epochs", 50),
                             early_stopping=True, n_iter_no_change=5, random_state=seed)
    if name == "FCM-clf":
        return FCMClassifier(k=p.get("k", 10), m=p.get("m", 2.0), seed=seed)
    raise KeyError(name)


def baseline_grid(name: str, cfg: dict) -> list[dict]:
    b = cfg["baselines"]
    return {
        "LDA": [{}],
        "LR": [{"C": c} for c in b["lr"]["C"]],
        "LinSVM": [{"C": c} for c in b["lr"]["C"]],
        "RBF-SVM": [{"C": c} for c in b["svm_rbf"]["C"]],
        "RF": [{"n_estimators": b["rf"]["n_estimators"], "max_depth": d} for d in b["rf"]["max_depth"]],
        "MLP": [{"hidden": h, "lr": b["mlp"]["lr"], "max_epochs": b["mlp"]["max_epochs"]}
                for h in b["mlp"]["hidden"]],
        "FCM-clf": [{"k": k, "m": b["fcm_clf"]["m"]} for k in b["fcm_clf"]["k"]],
    }[name]
