# CAN-bus attack detection with ANFIS: reproduction and hybrid-vs-non-hybrid study

Soft Computing AAT. This repo reproduces and extends:

> O. A. Al Isawi, K. A. Al Jaafari, A. S. Al-Sumaiti, "Electric Vehicles CAN Bus Cyber Attacks Detection
> Using Adaptive Neuro Fuzzy Inference System," *IEEE Access* 13, 90862–90874, 2025.
> DOI 10.1109/ACCESS.2025.3550970 (PDF in `data/`).

The study answers two questions:

1. **Non-hybrid vs hybrid.** How do MLP (neural), an FCM classifier (fuzzy) and LDA/LR/SVM/RF compare
   with ANFIS (neuro-fuzzy), unstacked and with the paper's stacking ANFIS?
2. **Clustering init.** How does ANFIS behave with Random vs K-Means vs Subtractive Clustering vs
   Fuzzy C-Means initialisation, everything else fixed?

System architecture and implementation details for every method: `docs/ARCHITECTURE.md`.
All code in one notebook: `CAN_ANFIS_AAT.ipynb` (every source file as a cell, plus tests, a demo run and
the results; rebuild with `python scripts/make_notebook.py`).
The results are in `results/REPORT_NOTES.md`, with per-setting tables in `results/*.md` and figures in `results/figures/`.

## Setup

```bash
conda env create -f environment.yml      # Python 3.11, CUDA 12.4 torch (CPU also works)
conda activate can-anfis
```

## Data

Download the OTIDS **CAN-intrusion dataset** (HCRL, Korea University) manually from
https://ocslab.hksecurity.net/Dataset/CAN-intrusion-dataset (or IEEE DataPort, DOI 10.21227/sy7h-9057)
and place these files in `data/raw/`:

```
data/raw/DoS_attack_dataset.txt
data/raw/Fuzzy_attack_dataset.txt
data/raw/Impersonation_attack_dataset.txt
data/raw/Attack_free_dataset.txt
```

If the files are missing, the parser stops and prints these instructions. Parsed logs are cached in
`data/processed/*.parquet`.

## Settings

| Setting | Labels | Inputs | Purpose |
|---|---|---|---|
| `A` | by CAN ID (paper) | CAN ID, DLC, d0–d7 | reproduce the paper |
| `A-noID` | by CAN ID (paper) | DLC, d0–d7, log10 Δt same ID | main benchmark, without the label-leaking ID |
| `B` | Imp = 0x164 after t0+250 s | as A-noID | label-validity probe |
| `B-ID` | as B | + CAN ID | as B, with ID |

## Run

```bash
python -m pytest -q tests                                   # ~15 s
python -m src.data.parse_otids                              # parse + cache (~30 s)
python scripts/data_report.py                               # results/data_report.md
python scripts/run_all.py --setting A A-noID B B-ID --task binary multi --seeds 5   # main grid
# ablations
python scripts/run_all.py --setting A A-noID B --task binary multi --models ANFIS-Random ANFIS-KMeans ANFIS-SC ANFIS-FCM --epochs 5 --tag ep5
python scripts/run_all.py --setting A A-noID --task binary multi --models ANFIS-SC ANFIS-FCM --stack-mode oof --tag oof
python scripts/run_all.py --setting A-noID --task binary multi --no-smote --tag nosmote
python scripts/rule_sweep.py                                # KMeans R in {5,10,20}, validation only
python scripts/probe_B.py                                   # Setting B learnability probe
python -m src.eval.report                                   # tables, figures, REPORT_NOTES.md
python scripts/make_arch_figures.py                         # architecture diagrams
python scripts/make_report_docx.py                          # results/AAT_Report.docx
```

`run_all.py` options: `--setting`, `--task`, `--seeds N` or `--seed-list`, `--models`, `--epochs`,
`--stack-mode paper|oof`, `--n-rules`, `--no-smote`, `--tag`. Results are merged into
`results/metrics_long.csv` (one row per setting, task, model, variant, seed, metric). Predictions go to
`results/preds/` and seed-0 ANFIS membership functions to `results/anfis_params/`.

**Runtime** (20-core CPU + RTX 4060): about 1 min per (setting, task, seed) for all 15 model rows,
so about 40 min for the main grid and about 30 min for all ablations.

## Layout

```
configs/default.yaml           all hyperparameters, seeds, settings
src/data/                      parse_otids.py, features.py, build_dataset.py (sampling, scaling, SMOTE)
src/models/                    anfis.py (PyTorch ANFIS, hybrid LSE+Adam), subclust.py, inits.py,
                               anfis_classifiers.py (OvR + stacking), fcm_classifier.py, baselines.py
src/eval/                      metrics.py, stats.py (McNemar), plots.py, report.py, notes.py
scripts/                       run_all.py, data_report.py, probe_B.py, rule_sweep.py,
                               make_arch_figures.py, make_report_docx.py
docs/ARCHITECTURE.md           system architecture and implementation details
tests/                         parser, preprocessing, SC, ANFIS (sin·cos, XOR, LSE), inits
```

## Protocol (identical for every model)

- **Sample:** 20,000 rows per seed (1497 DoS / 979 Imp / 17524 Normal), stratified 80/20 split.
- **Preprocessing:** min-max scaling fit on train only, then SMOTE (k = 30, `not majority`) on train only.
- **Tuning:** on a validation split (20 % of train, carved before SMOTE), never on test. ANFIS
  uses the paper's hyperparameters.
- **Seeds:** 5 (each re-draws subsample, split and SMOTE). Results are reported as mean ± std, with
  macro-F1 as the primary metric.
