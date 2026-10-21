# Comparison 2: clustering init for ANFIS (Setting B-ID, binary)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Attack (OvR) | F1 Attack (+stk) | rules (OvR / +stk) | train s (OvR / +stk) |
|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9455 ± 0.0053 | 0.9455 ± 0.0053 | 0.9058 ± 0.0089 | 0.9058 ± 0.0090 | 20.0 / 30.0 | 0.4 / 0.6 |
| ANFIS-KMeans | 0.9345 ± 0.0255 | 0.9446 ± 0.0059 | 0.8875 ± 0.0425 | 0.9043 ± 0.0100 | 20.0 / 30.0 | 0.7 / 1.0 |
| ANFIS-SC | 0.9453 ± 0.0055 | 0.9452 ± 0.0050 | 0.9054 ± 0.0094 | 0.9053 ± 0.0085 | 20.0 / 27.0 | 1.1 / 1.5 |
| ANFIS-FCM | 0.9456 ± 0.0055 | 0.9455 ± 0.0056 | 0.9060 ± 0.0094 | 0.9059 ± 0.0096 | 20.0 / 30.0 | 4.0 / 5.4 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: -0.0110 ± 0.0225 (KMeans wins 0/5 seeds, ties 0) → **within noise**
- Random → SC: -0.0002 ± 0.0010 (SC wins 2/5 seeds, ties 0) → **within noise**
- Random → FCM: +0.0001 ± 0.0005 (FCM wins 2/5 seeds, ties 2) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): +0.0111 ± 0.0227 (FCM wins 5/5 seeds, ties 0) → **within noise**

Figures: `figures/comparison2_B-ID_binary.png`, `figures/mf_overlay_B-ID_binary.png`
