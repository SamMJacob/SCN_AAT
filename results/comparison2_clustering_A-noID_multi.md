# Comparison 2: clustering init for ANFIS (Setting A-noID, multi)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Imp (OvR) | F1 Imp (+stk) | rules (OvR / +stk) | train s (OvR / +stk) | macro-F1 5 ep (OvR) | macro-F1 5 ep (+stk) |
|---|---|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9463 ± 0.0122 | 0.9659 ± 0.0093 | 0.9788 ± 0.0170 | 0.9386 ± 0.0217 | 30.0 / 40.0 | 0.8 / 1.0 | 0.9475 ± 0.0110 | 0.9665 ± 0.0102 |
| ANFIS-KMeans | 0.9598 ± 0.0055 | 0.9871 ± 0.0031 | 0.9995 ± 0.0011 | 0.9939 ± 0.0058 | 30.0 / 40.0 | 1.4 / 1.8 | 0.9523 ± 0.0163 | 0.9867 ± 0.0026 |
| ANFIS-SC | 0.9832 ± 0.0019 | 0.9861 ± 0.0035 | 0.9990 ± 0.0014 | 0.9900 ± 0.0116 | 49.6 / 63.0 | 2.0 / 2.5 | 0.9833 ± 0.0019 | 0.9858 ± 0.0030 |
| ANFIS-FCM | 0.9525 ± 0.0059 | 0.9847 ± 0.0084 | 0.9985 ± 0.0034 | 0.9881 ± 0.0156 | 30.0 / 40.0 | 8.9 / 10.8 | 0.9589 ± 0.0152 | 0.9861 ± 0.0031 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: +0.0135 ± 0.0091 (KMeans wins 5/5 seeds, ties 0) → **KMeans better**
- Random → SC: +0.0370 ± 0.0126 (SC wins 5/5 seeds, ties 0) → **SC better**
- Random → FCM: +0.0062 ± 0.0097 (FCM wins 3/5 seeds, ties 0) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): -0.0073 ± 0.0034 (FCM wins 0/5 seeds, ties 0) → **FCM worse**

## 1 vs 5 epochs (5 = early stopping on a validation split, then refit)

- ANFIS-Random: 5 ep − 1 ep = +0.0012 ± 0.0015
- ANFIS-KMeans: 5 ep − 1 ep = -0.0075 ± 0.0208
- ANFIS-SC: 5 ep − 1 ep = +0.0001 ± 0.0003
- ANFIS-FCM: 5 ep − 1 ep = +0.0065 ± 0.0140

## ANFIS-KMeans rule count R ∈ {5, 10, 20} (validation split, 5 seeds; R = 10 stays fixed in the main tables)

| rules per member | val macro-F1 (OvR) | val macro-F1 (+stk) | train s (OvR) | train s (+stk) |
|---|---|---|---|---|
| R = 5 | 0.9350 ± 0.0381 | 0.9767 ± 0.0098 | 1.0 | 1.4 |
| R = 10 | 0.9609 ± 0.0033 | 0.9872 ± 0.0063 | 1.4 | 1.8 |
| R = 20 | 0.9609 ± 0.0100 | 0.9837 ± 0.0073 | 2.0 | 2.5 |

Figures: `figures/comparison2_A-noID_multi.png`, `figures/mf_overlay_A-noID_multi.png`
