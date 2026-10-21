# Comparison 1: non-hybrid vs hybrid (Setting B, multi)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Imp | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9241 ± 0.0058 | 0.7886 ± 0.0168 | 0.9739 ± 0.0027 | 4.71 |
| FCM-clf | non-hybrid | 0.8351 ± 0.0599 | 0.6006 ± 0.1476 | 0.9319 ± 0.0384 | 5.40 |
| LDA | non-hybrid | 0.7148 ± 0.0053 | 0.3415 ± 0.0084 | 0.8314 ± 0.0064 | 0.02 |
| LR | non-hybrid | 0.9010 ± 0.0054 | 0.7582 ± 0.0122 | 0.9692 ± 0.0023 | 0.34 |
| LinSVM | non-hybrid | 0.9018 ± 0.0054 | 0.7536 ± 0.0150 | 0.9687 ± 0.0017 | 0.27 |
| RBF-SVM | non-hybrid | 0.9111 ± 0.0058 | 0.7716 ± 0.0141 | 0.9716 ± 0.0025 | 2.67 |
| RF | non-hybrid | 0.9190 ± 0.0070 | 0.7726 ± 0.0198 | 0.9732 ± 0.0025 | 0.78 |
| ANFIS-FCM | hybrid | 0.9259 ± 0.0068 | 0.7932 ± 0.0185 | 0.9744 ± 0.0029 | 8.68 |
| ANFIS-FCM+stk | hybrid | 0.9257 ± 0.0072 | 0.7924 ± 0.0196 | 0.9744 ± 0.0030 | 11.05 |
| ANFIS-SC (best ANFIS, post-hoc) | hybrid | 0.9263 ± 0.0065 | 0.7937 ± 0.0180 | 0.9745 ± 0.0028 | 2.03 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0016 ± 0.0016 (hybrid wins 4/5 seeds, ties 1) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (MLP → ANFIS-SC): +0.0022 ± 0.0011 (hybrid wins 5/5 seeds, ties 0) → **within noise**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0906 ± 0.0571 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- MLP vs ANFIS-FCM+stk: only MLP correct = 0, only ANFIS-FCM+stk correct = 2, exact p = 0.5
- MLP vs ANFIS-SC: only MLP correct = 0, only ANFIS-SC correct = 2, exact p = 0.5

Figure: `figures/comparison1_B_multi.png`
