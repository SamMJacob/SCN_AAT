"""Initial-FIS generators for ANFIS. All share one interface:

    init_fn(X_train, y=None, seed=0, **params) -> (centers [R, d], sigmas [R, d])
"""
from __future__ import annotations

import warnings

import numpy as np
import skfuzzy
from sklearn.cluster import KMeans

from .subclust import subclust


def _global_std(X, floor):
    return np.maximum(X.std(axis=0), floor)


def init_random(X, y=None, seed: int = 0, n_clusters: int = 10, sigma_floor: float = 1e-2, **_):
    """Control: R centers sampled uniformly from training points, sigma = global std."""
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), size=n_clusters, replace=False)]
    return C.copy(), np.tile(_global_std(X, sigma_floor), (n_clusters, 1))


def init_kmeans(X, y=None, seed: int = 0, n_clusters: int = 10, n_init: int = 10,
                sigma_floor: float = 1e-2, **_):
    """Hard clustering: each K-Means cluster becomes one rule."""
    km = KMeans(n_clusters=n_clusters, n_init=n_init, random_state=seed).fit(X)
    gstd = _global_std(X, sigma_floor)
    S = np.empty_like(km.cluster_centers_)
    for r in range(n_clusters):
        pts = X[km.labels_ == r]
        S[r] = np.maximum(pts.std(axis=0), sigma_floor) if len(pts) >= 2 else gstd
    return km.cluster_centers_.copy(), S


def init_fcm(X, y=None, seed: int = 0, n_clusters: int = 10, m: float = 2.0, maxiter: int = 100,
             error: float = 1e-5, sigma_floor: float = 1e-2, **_):
    """Fuzzy C-Means (genfis3-style): sigma = sqrt of u^m-weighted variance per cluster."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        C, U, *_ = skfuzzy.cluster.cmeans(X.T, c=n_clusters, m=m, error=error, maxiter=maxiter,
                                          seed=seed)
    W = U ** m                                                       # [R, N]
    var = (W[:, :, None] * (X[None] - C[:, None]) ** 2).sum(1) / W.sum(1, keepdims=True)
    return C, np.maximum(np.sqrt(var), sigma_floor)


def init_sc(X, y=None, seed: int = 0, radius: float = 0.25, squash: float = 1.25,
            accept: float = 0.5, reject: float = 0.15, max_points: int = 5000,
            sigma_floor: float = 1e-2, **_):
    """Subtractive clustering (genfis2-style) on a stratified subsample (SC is O(N^2))."""
    rng = np.random.default_rng(seed)
    if len(X) > max_points:
        if y is not None:
            classes = np.unique(y)
            per = max_points // len(classes)
            idx = np.concatenate([rng.choice(np.flatnonzero(y == c),
                                             size=min(per, int((y == c).sum())), replace=False)
                                  for c in classes])
        else:
            idx = rng.choice(len(X), size=max_points, replace=False)
        Xs = X[idx]
    else:
        Xs = X
    # bounds of the full training set, so radii are relative to the same [0, 1] box
    C, s = subclust(Xs, radius, squash, accept, reject, bounds=(X.min(0), X.max(0)))
    return C, np.tile(np.maximum(s, sigma_floor), (len(C), 1))


INIT_FNS = {"random": init_random, "kmeans": init_kmeans, "sc": init_sc, "fcm": init_fcm}
