"""Build the 20k-row datasets for each setting and the train/test preprocessing.

Labels (multiclass): 0 = DoS, 1 = Impersonation, 2 = Normal.
Binary: 0 = Attack (DoS + Imp), 1 = Normal (paper's one-hot order).

Pools
-----
A / A-noID (paper labels, by CAN ID):
    DoS    = 0x000 frames of the DoS log
    Imp    = 0x164 frames of the impersonation log (any time)
    Normal = attack-free log frames with ID not in {0x000, 0x164}
B / B-ID (corrected labels):
    DoS    = 0x000 frames of the DoS log
    Imp    = 0x164 frames of the impersonation log with t_rel >= 250 s
    Normal = impersonation-log frames with t_rel < 250 s (all IDs, incl. genuine 0x164)
             plus non-0x164 frames with t_rel >= 250 s
    Normal is drawn from the same session as Imp, so a classifier cannot separate
    Imp from genuine 0x164 by recording-session differences.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from .features import add_temporal_features
from .parse_otids import load

ROOT = Path(__file__).resolve().parents[2]
CLASS_NAMES = {"multi": ["DoS", "Imp", "Normal"], "binary": ["Attack", "Normal"]}
DOS_ID, IMP_ID = 0x000, 0x164


def load_config(path: Path | str | None = None) -> dict:
    with open(path or ROOT / "configs" / "default.yaml") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=None)
def _log(source: str) -> pd.DataFrame:
    df = add_temporal_features(load(source))
    df["log_dt"] = np.log10(df["dt_same_id"].clip(lower=1e-6))
    return df


@lru_cache(maxsize=None)
def build_pool(labels: str, t_attack: float = 250.0) -> pd.DataFrame:
    """All candidate frames with a ``label`` column (0/1/2)."""
    dos, imp = _log("dos"), _log("impersonation")
    p_dos = dos[dos.can_id == DOS_ID]
    if labels == "id":
        af = _log("attack_free")
        p_imp = imp[imp.can_id == IMP_ID]
        p_norm = af[~af.can_id.isin([DOS_ID, IMP_ID])]
    elif labels == "corrected":
        is164, late = imp.can_id == IMP_ID, imp.t_rel >= t_attack
        p_imp = imp[is164 & late]
        p_norm = imp[~(is164 & late)]
    else:
        raise ValueError(labels)
    parts = [p_dos.assign(label=0), p_imp.assign(label=1), p_norm.assign(label=2)]
    return pd.concat(parts, ignore_index=True)


def sample_dataset(setting: str, seed: int, cfg: dict) -> pd.DataFrame:
    """Draw exactly the paper's class totals from the setting's pool."""
    s = cfg["settings"][setting]
    pool = build_pool(s["labels"], cfg["sample"]["t_attack"])
    rng = np.random.default_rng(seed)
    totals = cfg["sample"]["totals"]
    out = []
    for lab, n in zip([0, 1, 2], [totals["dos"], totals["imp"], totals["normal"]]):
        idx = np.flatnonzero(pool.label.to_numpy() == lab)
        out.append(pool.iloc[rng.choice(idx, size=n, replace=False)])
    return pd.concat(out, ignore_index=True)


def to_task(y_multi: np.ndarray, task: str) -> np.ndarray:
    return (y_multi == 2).astype(int) if task == "binary" else y_multi.astype(int)


@dataclass
class Split:
    setting: str
    task: str
    seed: int
    features: list
    X_train: np.ndarray       # raw (unscaled), before SMOTE
    y_train: np.ndarray
    X_test: np.ndarray
    y_test: np.ndarray
    class_names: list = field(default_factory=list)


def make_split(setting: str, task: str, seed: int, cfg: dict) -> Split:
    df = sample_dataset(setting, seed, cfg)
    feats = cfg["settings"][setting]["features"]
    X = df[feats].to_numpy(dtype=np.float64)
    y = to_task(df["label"].to_numpy(), task)
    # stratify on the multiclass label so both tasks share the same rows per seed
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=cfg["sample"]["test_frac"], random_state=seed,
        stratify=df["label"].to_numpy())
    return Split(setting, task, seed, feats, Xtr, ytr, Xte, yte, CLASS_NAMES[task])


def val_split(X, y, seed: int, cfg: dict):
    """Validation split carved from (raw) training data, for tuning only."""
    return train_test_split(X, y, test_size=cfg["sample"]["val_frac"],
                            random_state=seed + 1000, stratify=y)


def preprocess(X_train, y_train, X_eval_list, seed: int, cfg: dict, smote: bool | None = None,
               log=print):
    """Fit min-max on training only, transform eval sets, then SMOTE training only.

    Returns (X_train_res, y_train_res, [X_eval_scaled...], scaler).
    """
    scaler = MinMaxScaler().fit(X_train)
    Xtr = scaler.transform(X_train)
    Xev = [scaler.transform(X) for X in X_eval_list]
    use_smote = cfg["smote"]["enabled"] if smote is None else smote
    ytr = np.asarray(y_train)
    if use_smote:
        counts = np.bincount(ytr)
        minority = counts[counts > 0].min()
        k = cfg["smote"]["k_neighbors"]
        if minority <= k:
            k = max(1, minority - 1)
            log(f"[smote] smallest class has {minority} samples; k_neighbors reduced to {k}")
        sm = SMOTE(k_neighbors=k, sampling_strategy=cfg["smote"]["sampling_strategy"],
                   random_state=seed)
        Xtr, ytr = sm.fit_resample(Xtr, ytr)
    return Xtr, ytr, Xev, scaler
