import numpy as np
import torch

from src.models.anfis import ANFIS, fit_anfis, predict
from src.models.inits import init_fcm, init_kmeans, init_random, init_sc
from src.models.subclust import subclust


def test_subclust_three_blobs():
    rng = np.random.default_rng(0)
    means = np.array([[0.2, 0.2], [0.8, 0.3], [0.5, 0.85]])
    X = np.vstack([m + 0.03 * rng.standard_normal((150, 2)) for m in means])
    C, s = subclust(X, radius=0.5, squash=1.25)
    assert len(C) == 3
    for m in means:
        assert np.min(np.linalg.norm(C - m, axis=1)) < 0.05
    assert s.shape == (2,)


def test_anfis_regression_sin_cos():
    rng = np.random.default_rng(0)
    X = rng.uniform(0, 1, size=(3000, 2))
    y = np.sin(X[:, 0]) * np.cos(X[:, 1])
    C, S = init_kmeans(X, n_clusters=10, seed=0)
    m = fit_anfis(C, S, X, y, epochs=5, seed=0)
    Xt = rng.uniform(0, 1, size=(1000, 2))
    rmse = np.sqrt(np.mean((predict(m, Xt) - np.sin(Xt[:, 0]) * np.cos(Xt[:, 1])) ** 2))
    assert rmse < 0.05


def test_anfis_xor_classifier():
    rng = np.random.default_rng(1)
    corners = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    labels = np.array([0, 1, 1, 0])
    idx = rng.integers(0, 4, size=2000)
    X = corners[idx] + 0.1 * rng.standard_normal((2000, 2))
    y = labels[idx].astype(float)
    C, S = init_kmeans(X, n_clusters=4, seed=0)
    m = fit_anfis(C, S, X, y, epochs=3, seed=0)
    acc = np.mean((predict(m, X) > 0.5) == (y > 0.5))
    assert acc > 0.97


def test_lse_matches_numpy_lstsq():
    rng = np.random.default_rng(2)
    X = rng.uniform(0, 1, size=(500, 3))
    y = X @ np.array([1.0, -2.0, 0.5]) + np.sin(5 * X[:, 0])
    C, S = init_random(X, n_clusters=4, seed=0)
    m = ANFIS(C, S).double()
    xt, yt = torch.tensor(X), torch.tensor(y)
    m.theta = m.theta.double()
    m.lse_step(xt, yt, ridge=0.0)
    phi = m.design(xt).detach().numpy()
    ref = np.linalg.lstsq(phi, y, rcond=None)[0]
    np.testing.assert_allclose(phi @ m.theta.numpy(), phi @ ref, atol=1e-5)


def test_kmeans_init_range_and_floor():
    rng = np.random.default_rng(3)
    X = rng.uniform(0, 1, size=(400, 4))
    X[:, 3] = 0.5                       # constant column -> sigma must hit the floor
    C, S = init_kmeans(X, n_clusters=10, seed=0, sigma_floor=1e-2)
    assert C.shape == (10, 4) and S.shape == (10, 4)
    assert np.all(C >= X.min(0) - 1e-9) and np.all(C <= X.max(0) + 1e-9)
    assert np.all(S >= 1e-2)


def test_fcm_and_sc_init_shapes():
    rng = np.random.default_rng(4)
    X = rng.uniform(0, 1, size=(600, 3))
    C, S = init_fcm(X, n_clusters=5, seed=0)
    assert C.shape == S.shape == (5, 3) and np.all(S >= 1e-2)
    C, S = init_sc(X, y=rng.integers(0, 2, 600), radius=0.5, max_points=300)
    assert C.shape == S.shape and len(C) >= 1
