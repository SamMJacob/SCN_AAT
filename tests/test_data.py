import numpy as np
import pytest

from src.data.build_dataset import load_config, preprocess
from src.data.parse_otids import parse_line


def test_parse_full_frame():
    ts, cid, remote, dlc, data = parse_line(
        "Timestamp:          0.000224        ID: 0329    000    DLC: 8    d7 a7 7f 8c 11 2f 00 10")
    assert (cid, remote, dlc) == (0x329, False, 8)
    assert data == [0xd7, 0xa7, 0x7f, 0x8c, 0x11, 0x2f, 0x00, 0x10]
    assert ts == pytest.approx(0.000224)


def test_parse_short_dlc_fills_minus_one():
    _, cid, _, dlc, data = parse_line(
        "Timestamp:          0.000878        ID: 0120    000    DLC: 4    00 00 00 00")
    assert (cid, dlc) == (0x120, 4)
    assert data == [0, 0, 0, 0, -1, -1, -1, -1]


def test_parse_remote_frame():
    _, cid, remote, dlc, data = parse_line(
        "Timestamp:          0.001684        ID: 0153    100    DLC: 0")
    assert (cid, remote, dlc) == (0x153, True, 0)
    assert data == [-1] * 8


def test_parse_trailing_ascii_and_absolute_ts():
    r = parse_line("Timestamp:        100.342207        ID: 04b1    000    DLC: 8    "
                   "75 32 6f 4a 61 69 37 79     'u2oJai7y'")
    assert r[4] == [0x75, 0x32, 0x6f, 0x4a, 0x61, 0x69, 0x37, 0x79]
    r = parse_line("Timestamp: 1481192898.075465        ID: 0587    000    DLC: 8    00 00 00 00 00 00 00 01")
    assert r[0] == pytest.approx(1481192898.075465) and r[1] == 0x587


def _toy(seed=0):
    rng = np.random.default_rng(seed)
    Xtr = rng.normal(size=(600, 3))
    ytr = np.r_[np.zeros(500), np.ones(60), np.full(40, 2)].astype(int)
    Xte = rng.normal(loc=0.5, size=(100, 3)) * 3
    yte = rng.integers(0, 3, size=100)
    return Xtr, ytr, Xte, yte


def test_smote_only_on_train():
    cfg = load_config()
    Xtr, ytr, Xte, yte = _toy()
    Xr, yr, (Xte_s,), _ = preprocess(Xtr, ytr, [Xte], 0, cfg)
    assert np.bincount(yr).tolist() == [500, 500, 500]
    assert Xte_s.shape == Xte.shape  # test untouched in size
    assert len(yte) == 100


def test_scaler_fit_on_train_only():
    cfg = load_config()
    Xtr, ytr, Xte, _ = _toy()
    _, _, (Xte_s,), scaler = preprocess(Xtr, ytr, [Xte], 0, cfg, smote=False)
    np.testing.assert_allclose(scaler.data_min_, Xtr.min(axis=0))
    np.testing.assert_allclose(scaler.data_max_, Xtr.max(axis=0))
    # test data has a wider range, so it must fall outside [0, 1] somewhere
    assert Xte_s.min() < 0 or Xte_s.max() > 1


def test_smote_reduces_k_for_tiny_class():
    cfg = load_config()
    Xtr, ytr, _, _ = _toy()
    ytr = ytr.copy()
    ytr[-40:-10] = 0   # class 2 now has 10 samples (< k = 30)
    msgs = []
    _, yr, _, _ = preprocess(Xtr, ytr, [], 0, cfg, log=msgs.append)
    assert len(set(np.bincount(yr))) == 1 and msgs
