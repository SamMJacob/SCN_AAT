"""Parser for the OTIDS (HCRL CAN-intrusion) text logs.

Line format (verified on the raw files):
    Timestamp:   0.000224    ID: 0329    000    DLC: 8    d7 a7 7f 8c 11 2f 00 10
The field after the ID is a flag; ``100`` marks a remote frame (DLC 0, no bytes).
A couple of Fuzzy-log lines carry a trailing quoted ASCII column, which is ignored.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"

FILES = {
    "dos": "DoS_attack_dataset.txt",
    "fuzzy": "Fuzzy_attack_dataset.txt",
    "impersonation": "Impersonation_attack_dataset.txt",
    "attack_free": "Attack_free_dataset.txt",
}

BYTE_COLS = [f"d{i}" for i in range(8)]

LINE_RE = re.compile(
    r"Timestamp:\s*(?P<ts>\d+(?:\.\d+)?)\s+"
    r"ID:\s*(?P<id>[0-9a-fA-F]+)\s+"
    r"(?P<flag>[0-9a-fA-F]+)\s+"
    r"DLC:\s*(?P<dlc>\d+)"
    r"(?P<data>(?:\s+[0-9a-fA-F]{2})*)"
)

DOWNLOAD_HELP = """
OTIDS raw files not found in {raw}.

Download the 'CAN-intrusion-dataset (OTIDS)' manually from
  https://ocslab.hksecurity.net/Dataset/CAN-intrusion-dataset
  (or IEEE DataPort, DOI 10.21227/sy7h-9057)
and place these files in data/raw/:
  {files}
"""


def parse_line(line: str):
    """Parse one log line -> (timestamp, can_id, remote, dlc, [d0..d7]) or None."""
    m = LINE_RE.search(line)
    if m is None:
        return None
    dlc = int(m.group("dlc"))
    data = [int(b, 16) for b in m.group("data").split()][:8]
    remote = int(m.group("flag"), 16) != 0
    data = data[:dlc] if not remote else []
    data = data + [-1] * (8 - len(data))
    return float(m.group("ts")), int(m.group("id"), 16), remote, dlc, data


def parse_file(path: Path, source: str) -> pd.DataFrame:
    rows, bad = [], 0
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            r = parse_line(line)
            if r is None:
                bad += 1
                continue
            ts, cid, remote, dlc, data = r
            rows.append((ts, cid, remote, dlc, *data))
    df = pd.DataFrame(rows, columns=["timestamp", "can_id", "remote", "dlc", *BYTE_COLS])
    df["can_id"] = df["can_id"].astype(np.int32)
    df["dlc"] = df["dlc"].astype(np.int8)
    df[BYTE_COLS] = df[BYTE_COLS].astype(np.int16)
    df["t_rel"] = df["timestamp"] - df["timestamp"].iloc[0]
    df["source_file"] = source
    df.attrs["unparsed_lines"] = bad
    return df


def check_raw_files() -> None:
    missing = [f for f in FILES.values() if not (RAW_DIR / f).exists()]
    if missing:
        print(DOWNLOAD_HELP.format(raw=RAW_DIR, files="\n  ".join(FILES.values())))
        sys.exit(1)


def load(source: str, force: bool = False) -> pd.DataFrame:
    """Load one parsed log, using the parquet cache when present."""
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    cache = PROC_DIR / f"{source}.parquet"
    if cache.exists() and not force:
        return pd.read_parquet(cache)
    check_raw_files()
    df = parse_file(RAW_DIR / FILES[source], source)
    df.to_parquet(cache, index=False)
    return df


def main() -> None:
    check_raw_files()
    for source, fname in FILES.items():
        print(f"== {fname}: first lines")
        with open(RAW_DIR / fname) as fh:
            for _, line in zip(range(5), fh):
                print("   ", line.rstrip())
        df = load(source, force=True)
        print(f"   parsed {len(df):,} rows, unparsed lines: {df.attrs.get('unparsed_lines', 0)}")


if __name__ == "__main__":
    main()
