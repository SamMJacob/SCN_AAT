# Comparison 2: clustering init for ANFIS (Setting B, multi)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Imp (OvR) | F1 Imp (+stk) | rules (OvR / +stk) | train s (OvR / +stk) | macro-F1 5 ep (OvR) | macro-F1 5 ep (+stk) |
|---|---|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9232 ± 0.0087 | 0.9239 ± 0.0075 | 0.7877 ± 0.0232 | 0.7876 ± 0.0205 | 30.0 / 40.0 | 0.8 / 1.0 | 0.9232 ± 0.0086 | 0.9237 ± 0.0078 |
| ANFIS-KMeans | 0.9259 ± 0.0071 | 0.9258 ± 0.0070 | 0.7932 ± 0.0188 | 0.7924 ± 0.0192 | 30.0 / 40.0 | 1.3 / 1.7 | 0.9259 ± 0.0069 | 0.9259 ± 0.0068 |
| ANFIS-SC | 0.9263 ± 0.0065 | 0.9256 ± 0.0063 | 0.7937 ± 0.0180 | 0.7922 ± 0.0171 | 53.2 / 66.8 | 2.0 / 2.5 | 0.9263 ± 0.0065 | 0.9251 ± 0.0060 |
| ANFIS-FCM | 0.9259 ± 0.0068 | 0.9257 ± 0.0072 | 0.7932 ± 0.0185 | 0.7924 ± 0.0196 | 30.0 / 40.0 | 8.7 / 11.0 | 0.9260 ± 0.0066 | 0.9252 ± 0.0066 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: +0.0027 ± 0.0040 (KMeans wins 4/5 seeds, ties 0) → **within noise**
- Random → SC: +0.0031 ± 0.0041 (SC wins 4/5 seeds, ties 1) → **within noise**
- Random → FCM: +0.0027 ± 0.0036 (FCM wins 4/5 seeds, ties 1) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): -0.0000 ± 0.0007 (FCM wins 1/5 seeds, ties 2) → **within noise**

## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)

- ANFIS-Random: 5 ep − 1 ep = +0.0001 ± 0.0001
- ANFIS-KMeans: 5 ep − 1 ep = +0.0000 ± 0.0004
- ANFIS-SC: 5 ep − 1 ep = +0.0000 ± 0.0000
- ANFIS-FCM: 5 ep − 1 ep = +0.0001 ± 0.0007

Figures: `figures/comparison2_B_multi.png`, `figures/mf_overlay_B_multi.png`
