# Comparison 1: non-hybrid vs hybrid (Setting B-ID, binary)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Attack | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9446 ± 0.0062 | 0.9044 ± 0.0106 | 0.9738 ± 0.0032 | 1.08 |
| FCM-clf | non-hybrid | 0.9067 ± 0.0037 | 0.8409 ± 0.0060 | 0.9531 ± 0.0021 | 3.10 |
| LDA | non-hybrid | 0.8387 ± 0.0071 | 0.7319 ± 0.0109 | 0.9093 ± 0.0051 | 0.01 |
| LR | non-hybrid | 0.9424 ± 0.0053 | 0.9006 ± 0.0091 | 0.9727 ± 0.0028 | 0.04 |
| LinSVM | non-hybrid | 0.9431 ± 0.0052 | 0.9018 ± 0.0089 | 0.9731 ± 0.0026 | 0.06 |
| RBF-SVM | non-hybrid | 0.9451 ± 0.0050 | 0.9052 ± 0.0085 | 0.9740 ± 0.0026 | 0.89 |
| RF | non-hybrid | 0.9410 ± 0.0061 | 0.8976 ± 0.0105 | 0.9728 ± 0.0028 | 0.61 |
| ANFIS-FCM | hybrid | 0.9456 ± 0.0055 | 0.9060 ± 0.0094 | 0.9743 ± 0.0028 | 3.97 |
| ANFIS-FCM+stk | hybrid | 0.9455 ± 0.0056 | 0.9059 ± 0.0096 | 0.9743 ± 0.0029 | 5.41 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (RBF-SVM → ANFIS-FCM+stk): +0.0004 ± 0.0008 (hybrid wins 2/5 seeds, ties 0) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (RBF-SVM → ANFIS-FCM): +0.0005 ± 0.0007 (hybrid wins 3/5 seeds, ties 0) → **within noise**
- pure neural (MLP) vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0009 ± 0.0009 (hybrid wins 4/5 seeds, ties 1) → **within noise**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0388 ± 0.0036 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- RBF-SVM vs ANFIS-FCM+stk: only RBF-SVM correct = 2, only ANFIS-FCM+stk correct = 2, exact p = 1
- RBF-SVM vs ANFIS-FCM: only RBF-SVM correct = 2, only ANFIS-FCM correct = 2, exact p = 1

Figure: `figures/comparison1_B-ID_binary.png`
