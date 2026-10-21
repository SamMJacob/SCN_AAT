# Comparison 1: non-hybrid vs hybrid (Setting A, multi)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Imp | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9979 ± 0.0016 | 0.9975 ± 0.0036 | 0.9992 ± 0.0005 | 1.73 |
| FCM-clf | non-hybrid | 0.9318 ± 0.0064 | 0.8125 ± 0.0165 | 0.9768 ± 0.0027 | 2.90 |
| LDA | non-hybrid | 0.8231 ± 0.0092 | 0.5407 ± 0.0216 | 0.9136 ± 0.0077 | 0.02 |
| LR | non-hybrid | 0.9938 ± 0.0016 | 0.9859 ± 0.0038 | 0.9981 ± 0.0005 | 0.18 |
| LinSVM | non-hybrid | 0.9896 ± 0.0036 | 0.9750 ± 0.0083 | 0.9969 ± 0.0011 | 0.24 |
| RBF-SVM | non-hybrid | 0.9971 ± 0.0011 | 1.0000 ± 0.0000 | 0.9988 ± 0.0004 | 0.16 |
| RF | non-hybrid | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.64 |
| ANFIS-FCM | hybrid | 0.9993 ± 0.0016 | 0.9980 ± 0.0045 | 0.9998 ± 0.0004 | 8.92 |
| ANFIS-FCM+stk | hybrid | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 10.03 |
| ANFIS-Random+stk (best ANFIS, post-hoc) | hybrid | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.99 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (RF → ANFIS-FCM+stk): +0.0000 ± 0.0000 (hybrid wins 0/5 seeds, ties 5) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (RF → ANFIS-Random+stk): +0.0000 ± 0.0000 (hybrid wins 0/5 seeds, ties 5) → **within noise**
- pure neural (MLP) vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0021 ± 0.0016 (hybrid wins 5/5 seeds, ties 0) → **within noise**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0682 ± 0.0064 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- RF vs ANFIS-FCM+stk: only RF correct = 0, only ANFIS-FCM+stk correct = 0, exact p = 1
- RF vs ANFIS-Random+stk: only RF correct = 0, only ANFIS-Random+stk correct = 0, exact p = 1

Figure: `figures/comparison1_A_multi.png`
