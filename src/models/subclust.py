"""Chiu's subtractive clustering, following MATLAB ``subclust`` semantics.

Data are normalised to the unit hypercube using the data bounds. Potentials use
alpha = 4 / r_a^2 and revisions use beta = 4 / r_b^2 with r_b = squash * r_a.
Cluster sigmas are r_a * (max - min) / sqrt(8) per dimension, as MATLAB returns.
"""
from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


def subclust(X: np.ndarray, radius: float, squash: float = 1.25, accept: float = 0.5,
             reject: float = 0.15, bounds: tuple | None = None, max_centers: int | None = None):
    """Return (centers [R, d], sigmas [d]) in the original data space."""
    X = np.asarray(X, dtype=np.float64)
    n, d = X.shape
    lo, hi = (X.min(axis=0), X.max(axis=0)) if bounds is None else map(np.asarray, bounds)
    span = np.where(hi - lo > 0, hi - lo, 1.0)
    Z = (X - lo) / span

    ra = np.full(d, radius, dtype=np.float64)
    rb = squash * ra
    Za = Z / ra                                     # alpha = 4 / ra^2 per dimension
    pot = np.exp(-4.0 * cdist(Za, Za, "sqeuclidean")).sum(axis=1)

    ref = pot.max()
    centers: list[np.ndarray] = []
    while True:
        k = int(np.argmax(pot))
        pk = pot[k]
        if pk <= reject * ref:
            break
        if pk <= accept * ref:                      # grey zone: accept only if far enough
            dmin = np.sqrt(np.min(np.sum(((Z[k] - np.array(centers)) / ra) ** 2, axis=1)))
            if dmin + pk / ref < 1.0:
                pot[k] = 0.0                        # reject this point, try the next highest
                if pot.max() <= 0:
                    break
                continue
        centers.append(Z[k].copy())
        # potential revision around the new center
        dz = np.sum(((Z - Z[k]) / rb) ** 2, axis=1)
        pot = pot - pk * np.exp(-4.0 * dz)
        pot[pot < 0] = 0.0
        if max_centers is not None and len(centers) >= max_centers:
            break
        if pot.max() <= 0:
            break

    C = np.array(centers) * span + lo
    sigmas = ra * span / np.sqrt(8.0)
    return C, sigmas
