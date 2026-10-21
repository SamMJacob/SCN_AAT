# Comparison 2: clustering init for ANFIS (Setting A, binary)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Attack (OvR) | F1 Attack (+stk) | rules (OvR / +stk) | train s (OvR / +stk) | macro-F1 5 ep (OvR) | macro-F1 5 ep (+stk) |
|---|---|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9856 ± 0.0255 | 0.9970 ± 0.0024 | 0.9751 ± 0.0440 | 0.9947 ± 0.0043 | 20.0 / 30.0 | 0.7 / 0.8 | 0.9979 ± 0.0021 | 0.9984 ± 0.0009 |
| ANFIS-KMeans | 0.9977 ± 0.0024 | 0.9995 ± 0.0007 | 0.9960 ± 0.0042 | 0.9992 ± 0.0013 | 20.0 / 30.0 | 0.7 / 1.0 | 0.9969 ± 0.0059 | 1.0000 ± 0.0000 |
| ANFIS-SC | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 7.6 / 10.8 | 1.2 / 1.6 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 |
| ANFIS-FCM | 0.9994 ± 0.0008 | 0.9998 ± 0.0005 | 0.9990 ± 0.0014 | 0.9996 ± 0.0009 | 20.0 / 30.0 | 4.1 / 5.1 | 0.9992 ± 0.0011 | 0.9998 ± 0.0005 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: +0.0121 ± 0.0257 (KMeans wins 4/5 seeds, ties 0) → **within noise**
- Random → SC: +0.0144 ± 0.0255 (SC wins 5/5 seeds, ties 0) → **within noise**
- Random → FCM: +0.0138 ± 0.0249 (FCM wins 4/5 seeds, ties 1) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): +0.0017 ± 0.0020 (FCM wins 4/5 seeds, ties 1) → **within noise**

## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)

- ANFIS-Random: 5 ep − 1 ep = +0.0123 ± 0.0257
- ANFIS-KMeans: 5 ep − 1 ep = -0.0008 ± 0.0037
- ANFIS-SC: 5 ep − 1 ep = +0.0000 ± 0.0000
- ANFIS-FCM: 5 ep − 1 ep = -0.0002 ± 0.0005

## ANFIS-KMeans rule count R ∈ {5, 10, 20} (validation split, 5 seeds; R = 10 stays fixed in the main tables)

| rules per member | val macro-F1 (OvR) | val macro-F1 (+stk) | train s (OvR) | train s (+stk) |
|---|---|---|---|---|
| R = 5 | 0.9812 ± 0.0247 | 0.9957 ± 0.0035 | 0.9 | 1.1 |
| R = 10 | 0.9979 ± 0.0033 | 0.9996 ± 0.0006 | 0.6 | 0.9 |
| R = 20 | 0.9858 ± 0.0247 | 0.9997 ± 0.0004 | 0.8 | 1.1 |

Figures: `figures/comparison2_A_binary.png`, `figures/mf_overlay_A_binary.png`
