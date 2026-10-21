"""Significance testing."""
from __future__ import annotations

import numpy as np
from scipy.stats import binomtest


def mcnemar(y_true, pred_a, pred_b) -> dict:
    """Exact (binomial) McNemar test on paired predictions over the same test set."""
    a_ok = np.asarray(pred_a) == np.asarray(y_true)
    b_ok = np.asarray(pred_b) == np.asarray(y_true)
    n01 = int(np.sum(a_ok & ~b_ok))      # A right, B wrong
    n10 = int(np.sum(~a_ok & b_ok))      # A wrong, B right
    n = n01 + n10
    p = 1.0 if n == 0 else binomtest(n01, n, 0.5).pvalue
    return {"a_only_correct": n01, "b_only_correct": n10, "p_value": float(p)}
