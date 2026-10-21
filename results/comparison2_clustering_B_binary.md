# Comparison 2: clustering init for ANFIS (Setting B, binary)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Attack (OvR) | F1 Attack (+stk) | rules (OvR / +stk) | train s (OvR / +stk) | macro-F1 5 ep (OvR) | macro-F1 5 ep (+stk) |
|---|---|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9447 ± 0.0059 | 0.9453 ± 0.0051 | 0.9044 ± 0.0100 | 0.9056 ± 0.0086 | 20.0 / 30.0 | 0.4 / 0.6 | 0.9451 ± 0.0058 | 0.9455 ± 0.0053 |
| ANFIS-KMeans | 0.9432 ± 0.0072 | 0.9455 ± 0.0056 | 0.9019 ± 0.0122 | 0.9060 ± 0.0095 | 20.0 / 30.0 | 0.7 / 1.0 | 0.9444 ± 0.0053 | 0.9456 ± 0.0057 |
| ANFIS-SC | 0.9457 ± 0.0058 | 0.9450 ± 0.0053 | 0.9061 ± 0.0099 | 0.9051 ± 0.0090 | 39.6 / 46.6 | 1.2 / 1.5 | 0.9458 ± 0.0057 | 0.9453 ± 0.0056 |
| ANFIS-FCM | 0.9455 ± 0.0056 | 0.9455 ± 0.0056 | 0.9059 ± 0.0095 | 0.9059 ± 0.0095 | 20.0 / 30.0 | 3.9 / 5.3 | 0.9454 ± 0.0058 | 0.9454 ± 0.0056 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: -0.0015 ± 0.0016 (KMeans wins 1/5 seeds, ties 0) → **within noise**
- Random → SC: +0.0010 ± 0.0006 (SC wins 5/5 seeds, ties 0) → **within noise**
- Random → FCM: +0.0008 ± 0.0006 (FCM wins 4/5 seeds, ties 0) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): +0.0023 ± 0.0021 (FCM wins 4/5 seeds, ties 1) → **within noise**

## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)

- ANFIS-Random: 5 ep − 1 ep = +0.0005 ± 0.0005
- ANFIS-KMeans: 5 ep − 1 ep = +0.0012 ± 0.0029
- ANFIS-SC: 5 ep − 1 ep = +0.0001 ± 0.0003
- ANFIS-FCM: 5 ep − 1 ep = -0.0001 ± 0.0003

Figures: `figures/comparison2_B_binary.png`, `figures/mf_overlay_B_binary.png`
