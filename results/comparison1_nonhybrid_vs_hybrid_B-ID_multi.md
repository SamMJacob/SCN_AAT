# Comparison 1: non-hybrid vs hybrid (Setting B-ID, multi)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Imp | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9260 ± 0.0062 | 0.7929 ± 0.0172 | 0.9744 ± 0.0027 | 1.75 |
| FCM-clf | non-hybrid | 0.8823 ± 0.0030 | 0.6755 ± 0.0080 | 0.9529 ± 0.0017 | 6.75 |
| LDA | non-hybrid | 0.7751 ± 0.0034 | 0.4500 ± 0.0082 | 0.8911 ± 0.0041 | 0.02 |
| LR | non-hybrid | 0.9214 ± 0.0062 | 0.7802 ± 0.0168 | 0.9723 ± 0.0027 | 0.24 |
| LinSVM | non-hybrid | 0.9220 ± 0.0068 | 0.7827 ± 0.0186 | 0.9729 ± 0.0028 | 0.33 |
| RBF-SVM | non-hybrid | 0.9248 ± 0.0063 | 0.7939 ± 0.0180 | 0.9738 ± 0.0027 | 0.97 |
| RF | non-hybrid | 0.9193 ± 0.0072 | 0.7733 ± 0.0201 | 0.9733 ± 0.0024 | 0.79 |
| ANFIS-FCM | hybrid | 0.9257 ± 0.0067 | 0.7927 ± 0.0171 | 0.9742 ± 0.0029 | 8.90 |
| ANFIS-FCM+stk | hybrid | 0.9259 ± 0.0068 | 0.7927 ± 0.0183 | 0.9744 ± 0.0028 | 11.21 |
| ANFIS-Random (best ANFIS, post-hoc) | hybrid | 0.9265 ± 0.0066 | 0.7942 ± 0.0182 | 0.9746 ± 0.0028 | 0.82 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (MLP → ANFIS-FCM+stk): -0.0001 ± 0.0010 (hybrid wins 2/5 seeds, ties 2) → **within noise**
- best non-hybrid vs best ANFIS (post-hoc) (MLP → ANFIS-Random): +0.0005 ± 0.0005 (hybrid wins 3/5 seeds, ties 2) → **within noise**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0435 ± 0.0049 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- MLP vs ANFIS-FCM+stk: only MLP correct = 0, only ANFIS-FCM+stk correct = 1, exact p = 1
- MLP vs ANFIS-Random: only MLP correct = 0, only ANFIS-Random correct = 1, exact p = 1

Figure: `figures/comparison1_B-ID_multi.png`
