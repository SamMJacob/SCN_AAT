# Comparison 1: non-hybrid vs hybrid (Setting A, binary)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Attack | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9972 ± 0.0015 | 0.9952 ± 0.0026 | 0.9988 ± 0.0006 | 0.99 |
| FCM-clf | non-hybrid | 0.9502 ± 0.0056 | 0.9139 ± 0.0095 | 0.9767 ± 0.0028 | 3.12 |
| LDA | non-hybrid | 0.8519 ± 0.0107 | 0.7526 ± 0.0166 | 0.9185 ± 0.0075 | 0.01 |
| LR | non-hybrid | 0.9962 ± 0.0013 | 0.9934 ± 0.0023 | 0.9983 ± 0.0006 | 0.04 |
| LinSVM | non-hybrid | 0.9962 ± 0.0024 | 0.9934 ± 0.0043 | 0.9983 ± 0.0011 | 0.03 |
| RBF-SVM | non-hybrid | 0.9972 ± 0.0011 | 0.9952 ± 0.0019 | 0.9988 ± 0.0005 | 0.14 |
| RF | non-hybrid | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.63 |
| ANFIS-FCM | hybrid | 0.9994 ± 0.0008 | 0.9990 ± 0.0014 | 0.9998 ± 0.0004 | 4.07 |
| ANFIS-FCM+stk | hybrid | 0.9998 ± 0.0005 | 0.9996 ± 0.0009 | 0.9999 ± 0.0002 | 5.10 |
| ANFIS-SC (best ANFIS, post-hoc) | hybrid | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.17 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (RF → ANFIS-FCM+stk): -0.0002 ± 0.0005 (hybrid wins 0/5 seeds, ties 4) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (RF → ANFIS-SC): +0.0000 ± 0.0000 (hybrid wins 0/5 seeds, ties 5) → **within noise**
- pure neural (MLP) vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0025 ± 0.0018 (hybrid wins 4/5 seeds, ties 1) → **hybrid better**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0496 ± 0.0058 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- RF vs ANFIS-FCM+stk: only RF correct = 0, only ANFIS-FCM+stk correct = 0, exact p = 1
- RF vs ANFIS-SC: only RF correct = 0, only ANFIS-SC correct = 0, exact p = 1

Figure: `figures/comparison1_A_binary.png`
