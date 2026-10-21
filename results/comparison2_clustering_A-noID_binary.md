# Comparison 2: clustering init for ANFIS (Setting A-noID, binary)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Attack (OvR) | F1 Attack (+stk) | rules (OvR / +stk) | train s (OvR / +stk) | macro-F1 5 ep (OvR) | macro-F1 5 ep (+stk) |
|---|---|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9568 ± 0.0151 | 0.9713 ± 0.0158 | 0.9252 ± 0.0258 | 0.9501 ± 0.0273 | 20.0 / 30.0 | 0.4 / 0.6 | 0.9570 ± 0.0149 | 0.9721 ± 0.0160 |
| ANFIS-KMeans | 0.9557 ± 0.0147 | 0.9798 ± 0.0040 | 0.9233 ± 0.0254 | 0.9648 ± 0.0070 | 20.0 / 30.0 | 0.7 / 1.0 | 0.9605 ± 0.0155 | 0.9856 ± 0.0034 |
| ANFIS-SC | 0.9840 ± 0.0024 | 0.9838 ± 0.0023 | 0.9720 ± 0.0042 | 0.9718 ± 0.0040 | 43.2 / 50.0 | 1.2 / 1.6 | 0.9836 ± 0.0021 | 0.9837 ± 0.0022 |
| ANFIS-FCM | 0.9499 ± 0.0050 | 0.9794 ± 0.0031 | 0.9133 ± 0.0086 | 0.9639 ± 0.0054 | 20.0 / 30.0 | 4.1 / 5.6 | 0.9692 ± 0.0168 | 0.9813 ± 0.0017 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: -0.0011 ± 0.0100 (KMeans wins 2/5 seeds, ties 0) → **within noise**
- Random → SC: +0.0272 ± 0.0141 (SC wins 5/5 seeds, ties 0) → **SC better**
- Random → FCM: -0.0069 ± 0.0123 (FCM wins 2/5 seeds, ties 0) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): -0.0058 ± 0.0152 (FCM wins 3/5 seeds, ties 0) → **within noise**

## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)

- ANFIS-Random: 5 ep − 1 ep = +0.0002 ± 0.0003
- ANFIS-KMeans: 5 ep − 1 ep = +0.0048 ± 0.0030
- ANFIS-SC: 5 ep − 1 ep = -0.0003 ± 0.0005
- ANFIS-FCM: 5 ep − 1 ep = +0.0193 ± 0.0179

## ANFIS-KMeans rule count R ∈ {5, 10, 20} (validation split, 5 seeds; R = 10 stays fixed in the main tables)

| rules per member | val macro-F1 (OvR) | val macro-F1 (+stk) | train s (OvR) | train s (+stk) |
|---|---|---|---|---|
| R = 5 | 0.9473 ± 0.0088 | 0.9493 ± 0.0069 | 0.5 | 0.8 |
| R = 10 | 0.9501 ± 0.0059 | 0.9781 ± 0.0092 | 0.6 | 0.9 |
| R = 20 | 0.9662 ± 0.0180 | 0.9766 ± 0.0161 | 0.9 | 1.3 |

Figures: `figures/comparison2_A-noID_binary.png`, `figures/mf_overlay_A-noID_binary.png`
