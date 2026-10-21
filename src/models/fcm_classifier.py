"""N2: non-hybrid fuzzy classifier built only from FCM memberships (no gradient learning).

1. FCM on the training data (k clusters).
2. Each cluster gets a class distribution: membership-weighted class frequencies.
3. Prediction: membership-weighted vote over clusters.
"""
from __future__ import annotations

import warnings

import numpy as np
import skfuzzy


class FCMClassifier:
    def __init__(self, k: int = 10, m: float = 2.0, maxiter: int = 100, error: float = 1e-5,
                 seed: int = 0):
        self.k, self.m, self.maxiter, self.error, self.seed = k, m, maxiter, error, seed

    def fit(self, X, y):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.centers_, U, *_ = skfuzzy.cluster.cmeans(
                X.T, c=self.k, m=self.m, error=self.error, maxiter=self.maxiter, seed=self.seed)
        self.classes_ = np.unique(y)
        onehot = (y[:, None] == self.classes_[None]).astype(float)       # [N, C]
        dist = U @ onehot                                                 # [k, C]
        self.cluster_dist_ = dist / np.maximum(dist.sum(1, keepdims=True), 1e-12)
        self.n_rules = self.k
        return self

    def predict_scores(self, X):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            U, *_ = skfuzzy.cluster.cmeans_predict(
                X.T, self.centers_, self.m, error=self.error, maxiter=self.maxiter, seed=self.seed)
        return U.T @ self.cluster_dist_                                   # [N, C]

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_scores(X), axis=1)]
