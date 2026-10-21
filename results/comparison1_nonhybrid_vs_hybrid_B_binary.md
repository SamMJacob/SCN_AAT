# Comparison 1: non-hybrid vs hybrid (Setting B, binary)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Attack | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9041 ± 0.0526 | 0.8380 ± 0.0859 | 0.9496 ± 0.0317 | 0.71 |
| FCM-clf | non-hybrid | 0.9233 ± 0.0454 | 0.8696 ± 0.0740 | 0.9611 ± 0.0276 | 3.84 |
| LDA | non-hybrid | 0.7959 ± 0.0059 | 0.6674 ± 0.0086 | 0.8769 ± 0.0049 | 0.01 |
| LR | non-hybrid | 0.9448 ± 0.0043 | 0.9046 ± 0.0073 | 0.9740 ± 0.0022 | 0.05 |
| LinSVM | non-hybrid | 0.9445 ± 0.0057 | 0.9041 ± 0.0098 | 0.9738 ± 0.0029 | 0.03 |
| RBF-SVM | non-hybrid | 0.9449 ± 0.0044 | 0.9047 ± 0.0075 | 0.9741 ± 0.0023 | 1.07 |
| RF | non-hybrid | 0.9414 ± 0.0054 | 0.8984 ± 0.0093 | 0.9731 ± 0.0025 | 0.59 |
| ANFIS-FCM | hybrid | 0.9455 ± 0.0056 | 0.9059 ± 0.0095 | 0.9743 ± 0.0029 | 3.92 |
| ANFIS-FCM+stk | hybrid | 0.9455 ± 0.0056 | 0.9059 ± 0.0095 | 0.9743 ± 0.0029 | 5.31 |
| ANFIS-SC (best ANFIS, post-hoc) | hybrid | 0.9457 ± 0.0058 | 0.9061 ± 0.0099 | 0.9744 ± 0.0030 | 1.15 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (RBF-SVM → ANFIS-FCM+stk): +0.0007 ± 0.0021 (hybrid wins 3/5 seeds, ties 0) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (RBF-SVM → ANFIS-SC): +0.0008 ± 0.0018 (hybrid wins 4/5 seeds, ties 0) → **within noise**
- pure neural (MLP) vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0414 ± 0.0569 (hybrid wins 3/5 seeds, ties 1) → **within noise**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0222 ± 0.0463 (hybrid wins 4/5 seeds, ties 0) → **within noise**

## McNemar test (seed 0)

- RBF-SVM vs ANFIS-FCM+stk: only RBF-SVM correct = 1, only ANFIS-FCM+stk correct = 3, exact p = 0.625
- RBF-SVM vs ANFIS-SC: only RBF-SVM correct = 1, only ANFIS-SC correct = 4, exact p = 0.375

Figure: `figures/comparison1_B_binary.png`
