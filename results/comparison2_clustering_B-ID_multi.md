# Comparison 2: clustering init for ANFIS (Setting B-ID, multi)

Everything except the initial FIS is held fixed: same data, scaling, SMOTE, hybrid training (1 epoch unless noted), OvR and stacking configuration. Random and KMeans and FCM use R = 10 rules per member; SC sets its own rule count (paper radius/squash). Rules are summed over all OvR members (and the stacking ANFIS for `+stk`).

| init | macro-F1 (OvR) | macro-F1 (+stk) | F1 Imp (OvR) | F1 Imp (+stk) | rules (OvR / +stk) | train s (OvR / +stk) |
|---|---|---|---|---|---|---|
| ANFIS-Random | 0.9265 ± 0.0066 | 0.9264 ± 0.0068 | 0.7942 ± 0.0182 | 0.7938 ± 0.0187 | 30.0 / 40.0 | 0.8 / 1.0 |
| ANFIS-KMeans | 0.9263 ± 0.0067 | 0.9258 ± 0.0070 | 0.7937 ± 0.0183 | 0.7922 ± 0.0192 | 30.0 / 40.0 | 1.4 / 1.8 |
| ANFIS-SC | 0.9261 ± 0.0068 | 0.9251 ± 0.0064 | 0.7932 ± 0.0188 | 0.7904 ± 0.0176 | 42.0 / 51.0 | 2.0 / 2.5 |
| ANFIS-FCM | 0.9257 ± 0.0067 | 0.9259 ± 0.0068 | 0.7927 ± 0.0171 | 0.7927 ± 0.0183 | 30.0 / 40.0 | 8.9 / 11.2 |

## Paired differences vs the Random-init control (macro-F1, OvR)

- Random → KMeans: -0.0002 ± 0.0006 (KMeans wins 1/5 seeds, ties 2) → **within noise**
- Random → SC: -0.0004 ± 0.0004 (SC wins 0/5 seeds, ties 2) → **within noise**
- Random → FCM: -0.0008 ± 0.0006 (FCM wins 0/5 seeds, ties 1) → **within noise**
- KMeans → FCM (value of *fuzzy* vs hard clustering): -0.0006 ± 0.0011 (FCM wins 1/5 seeds, ties 1) → **within noise**

Figures: `figures/comparison2_B-ID_multi.png`, `figures/mf_overlay_B-ID_multi.png`
