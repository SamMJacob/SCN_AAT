"""Per-frame features computed on the full chronological log (before any subsampling)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .parse_otids import BYTE_COLS

_POPCOUNT = np.array([bin(i).count("1") for i in range(256)], dtype=np.int16)


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``dt_same_id`` (s since previous frame with the same CAN ID) and
    ``hamming_prev`` (bit flips vs. the previous payload of the same ID).

    The first frame of each ID has no predecessor; its dt is filled with that
    ID's median dt (or 1 s if the ID occurs once) and its Hamming distance with 0.
    """
    df = df.sort_values("timestamp", kind="stable").reset_index(drop=True)
    g = df.groupby("can_id", sort=False)

    dt = g["timestamp"].diff()
    med = dt.groupby(df["can_id"]).transform("median")
    df["dt_same_id"] = dt.fillna(med).fillna(1.0).astype(np.float64)

    payload = df[BYTE_COLS].to_numpy().clip(min=0).astype(np.int16)  # missing bytes -> 0
    prev = g[BYTE_COLS].shift(1).to_numpy()
    has_prev = ~np.isnan(prev[:, 0])
    prev = np.nan_to_num(prev, nan=0).clip(min=0).astype(np.int16)
    ham = _POPCOUNT[np.bitwise_xor(payload, prev)].sum(axis=1)
    df["hamming_prev"] = np.where(has_prev, ham, 0).astype(np.int16)
    return df
