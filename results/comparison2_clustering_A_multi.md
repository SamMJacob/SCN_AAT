# Comparison 2: clustering init for ANFIS (Setting A, multi)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Imp (OvR) | F1 Imp (+stk) | rules (OvR / +stk) | train s (OvR / +stk) | macro-F1 5 ep (OvR) | macro-F1 5 ep (+stk) |
|---|---|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9841 ± 0.0304 | 1.0000 ± 0.0000 | 0.9574 ± 0.0853 | 1.0000 ± 0.0000 | 30.0 / 40.0 | 0.8 / 1.0 | 0.9986 ± 0.0005 | 1.0000 ± 0.0000 |
| ANFIS-KMeans | 0.9959 ± 0.0054 | 0.9986 ± 0.0032 | 0.9885 ± 0.0154 | 0.9960 ± 0.0089 | 30.0 / 40.0 | 1.4 / 1.7 | 0.9977 ± 0.0028 | 1.0000 ± 0.0000 |
| ANFIS-SC | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 19.6 / 23.4 | 1.6 / 2.1 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 |
| ANFIS-FCM | 0.9993 ± 0.0016 | 1.0000 ± 0.0000 | 0.9980 ± 0.0045 | 1.0000 ± 0.0000 | 30.0 / 40.0 | 8.9 / 10.0 | 0.9996 ± 0.0008 | 0.9996 ± 0.0008 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: +0.0118 ± 0.0330 (KMeans wins 3/5 seeds, ties 0) → **within noise**
- Random → SC: +0.0159 ± 0.0304 (SC wins 5/5 seeds, ties 0) → **within noise**
- Random → FCM: +0.0152 ± 0.0288 (FCM wins 5/5 seeds, ties 0) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): +0.0033 ± 0.0063 (FCM wins 3/5 seeds, ties 1) → **within noise**

## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)

- ANFIS-Random: 5 ep − 1 ep = +0.0145 ± 0.0308
- ANFIS-KMeans: 5 ep − 1 ep = +0.0017 ± 0.0049
- ANFIS-SC: 5 ep − 1 ep = +0.0000 ± 0.0000
- ANFIS-FCM: 5 ep − 1 ep = +0.0004 ± 0.0008

## ANFIS-KMeans rule count R ∈ {5, 10, 20} (validation split, 5 seeds; R = 10 stays fixed in the main tables)

| rules per member | val macro-F1 (OvR) | val macro-F1 (+stk) | train s (OvR) | train s (+stk) |
|---|---|---|---|---|
| R = 5 | 0.9763 ± 0.0218 | 0.9998 ± 0.0005 | 1.0 | 1.3 |
| R = 10 | 0.9958 ± 0.0063 | 0.9996 ± 0.0006 | 1.4 | 1.7 |
| R = 20 | 0.9997 ± 0.0004 | 1.0000 ± 0.0000 | 1.8 | 2.2 |

Figures: `figures/comparison2_A_multi.png`, `figures/mf_overlay_A_multi.png`
