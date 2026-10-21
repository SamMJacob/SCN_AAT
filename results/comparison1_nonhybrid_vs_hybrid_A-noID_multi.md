# Comparison 1: non-hybrid vs hybrid (Setting A-noID, multi)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Imp | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9824 ± 0.0016 | 0.9969 ± 0.0033 | 0.9927 ± 0.0006 | 4.80 |
| FCM-clf | non-hybrid | 0.8838 ± 0.0137 | 0.7967 ± 0.0364 | 0.9643 ± 0.0040 | 6.60 |
| LDA | non-hybrid | 0.6815 ± 0.0085 | 0.3667 ± 0.0102 | 0.8278 ± 0.0055 | 0.03 |
| LR | non-hybrid | 0.8621 ± 0.0223 | 0.7577 ± 0.0547 | 0.9496 ± 0.0094 | 0.60 |
| LinSVM | non-hybrid | 0.9214 ± 0.0056 | 0.9315 ± 0.0056 | 0.9704 ± 0.0028 | 0.32 |
| RBF-SVM | non-hybrid | 0.9441 ± 0.0189 | 0.9144 ± 0.0117 | 0.9819 ± 0.0077 | 3.30 |
| RF | non-hybrid | 0.9886 ± 0.0030 | 1.0000 ± 0.0000 | 0.9952 ± 0.0013 | 0.76 |
| ANFIS-FCM | hybrid | 0.9525 ± 0.0059 | 0.9985 ± 0.0034 | 0.9779 ± 0.0033 | 8.85 |
| ANFIS-FCM+stk | hybrid | 0.9847 ± 0.0084 | 0.9881 ± 0.0156 | 0.9941 ± 0.0030 | 10.79 |
| ANFIS-KMeans+stk (best ANFIS, post-hoc) | hybrid | 0.9871 ± 0.0031 | 0.9939 ± 0.0058 | 0.9950 ± 0.0013 | 1.83 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (RF → ANFIS-FCM+stk): -0.0039 ± 0.0063 (hybrid wins 1/5 seeds, ties 0) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (RF → ANFIS-KMeans+stk): -0.0016 ± 0.0028 (hybrid wins 2/5 seeds, ties 0) → **within noise**
- pure neural (MLP) vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0023 ± 0.0078 (hybrid wins 4/5 seeds, ties 0) → **within noise**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.1009 ± 0.0179 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- RF vs ANFIS-FCM+stk: only RF correct = 0, only ANFIS-FCM+stk correct = 4, exact p = 0.125
- RF vs ANFIS-KMeans+stk: only RF correct = 0, only ANFIS-KMeans+stk correct = 4, exact p = 0.125

Figure: `figures/comparison1_A-noID_multi.png`
