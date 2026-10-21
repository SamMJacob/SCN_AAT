"""ANFIS classifier wrappers following the paper's architecture.

OvRANFIS:     one ANFIS per class, MSE regression to the one-hot column; outputs are
              clipped to [0, 1] and used as class scores.
StackedANFIS: stage 1 = OvRANFIS; stage 2 = an augmented ANFIS that takes the stage-1
              score vector and regresses the integer class index (DoS=0, Imp=1, Normal=2;
              binary Attack=0, Normal=1), rounded and clipped. This is our reading of the
              paper's description ("output the class predictions").
              stack_mode="paper": stage 2 is trained on in-sample stage-1 outputs.
              stack_mode="oof":   stage 2 is trained on K-fold out-of-fold stage-1 outputs.

Initial FIS: like MATLAB genfis2/genfis3, clustering runs on the joint input-output
space [X, target] and the output coordinate is then dropped (cluster_space="xy").
"""
from __future__ import annotations

import time

import numpy as np
from sklearn.model_selection import StratifiedKFold

from .anfis import fit_anfis, predict
from .inits import INIT_FNS


class OvRANFIS:
    def __init__(self, init: str, init_params: dict | None = None, anfis_params: dict | None = None,
                 cluster_space: str = "xy", seed: int = 0):
        self.init, self.init_params = init, dict(init_params or {})
        self.anfis_params = dict(anfis_params or {})
        self.cluster_space, self.seed = cluster_space, seed

    def _init(self, X, t, y):
        fn = INIT_FNS[self.init]
        if self.cluster_space == "xy" and self.init != "random":
            Z = np.column_stack([X, t])
            C, S = fn(Z, y=y, seed=self.seed, **self.init_params)
            return C[:, :-1], S[:, :-1]
        return fn(X, y=y, seed=self.seed, **self.init_params)

    def fit(self, X, y, X_val=None, y_val=None):
        self.classes_ = np.unique(y)
        self.models_ = []
        epochs = self.anfis_params.get("epochs", 1)
        for i, c in enumerate(self.classes_):
            t = (y == c).astype(float)
            C, S = self._init(X, t, y)
            tv = None if X_val is None else (y_val == c).astype(float)
            params = dict(self.anfis_params,
                          epochs=epochs[i] if isinstance(epochs, (list, tuple)) else epochs)
            self.models_.append(fit_anfis(C, S, X, t, X_val=X_val, y_val=tv, seed=self.seed,
                                          **params))
        return self

    @property
    def n_rules(self) -> int:
        return int(sum(m.R for m in self.models_))

    @property
    def rules_per_member(self) -> list[int]:
        return [m.R for m in self.models_]

    def predict_scores(self, X):
        return np.column_stack([np.clip(predict(m, X), 0, 1) for m in self.models_])

    def predict(self, X):
        S = self.predict_scores(X)
        if len(self.classes_) == 2:          # binary: threshold 0.5 on P(Attack) (class 0)
            return np.where(S[:, 0] >= 0.5, self.classes_[0], self.classes_[1])
        return self.classes_[np.argmax(S, axis=1)]


class StackedANFIS:
    def __init__(self, init: str, init_params: dict | None = None, anfis_params: dict | None = None,
                 stack_init_params: dict | None = None, stack_mode: str = "paper",
                 oof_folds: int = 5, cluster_space: str = "xy", seed: int = 0):
        self.kw = dict(init=init, init_params=init_params, anfis_params=anfis_params,
                       cluster_space=cluster_space, seed=seed)
        self.stack_init_params = stack_init_params if stack_init_params is not None else init_params
        self.stack_mode, self.oof_folds, self.seed = stack_mode, oof_folds, seed

    def fit(self, X, y, X_val=None, y_val=None):
        t0 = time.perf_counter()
        self.stage1 = OvRANFIS(**self.kw).fit(X, y, X_val, y_val)
        self.stage1_time = time.perf_counter() - t0
        self.classes_ = self.stage1.classes_
        if self.stack_mode == "paper":
            S = self.stage1.predict_scores(X)
        elif self.stack_mode == "oof":
            S = np.zeros((len(X), len(self.classes_)))
            skf = StratifiedKFold(self.oof_folds, shuffle=True, random_state=self.seed)
            for tr, te in skf.split(X, y):
                S[te] = OvRANFIS(**self.kw).fit(X[tr], y[tr]).predict_scores(X[te])
        else:
            raise ValueError(self.stack_mode)
        kw2 = dict(self.kw, init_params=self.stack_init_params)
        self.stage2 = OvRANFIS(**kw2)
        t = np.searchsorted(self.classes_, y).astype(float)      # integer class index target
        C, S0 = self.stage2._init(S, t, y)
        self.stage2.classes_ = self.classes_
        p2 = dict(self.kw["anfis_params"] or {})
        if isinstance(p2.get("epochs"), (list, tuple)):     # per-member epochs -> use the max
            p2["epochs"] = max(p2["epochs"])
        self.stage2.models_ = [fit_anfis(C, S0, S, t, seed=self.seed, **p2)]
        return self

    @property
    def n_rules(self) -> int:
        return self.stage1.n_rules + self.stage2.n_rules

    def predict(self, X):
        S = self.stage1.predict_scores(X)
        out = predict(self.stage2.models_[0], S)
        idx = np.clip(np.rint(out), 0, len(self.classes_) - 1).astype(int)
        return self.classes_[idx]
