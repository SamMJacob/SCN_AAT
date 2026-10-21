# Comparison 1: non-hybrid vs hybrid (Setting A-noID, binary)

Non-hybrid: MLP (pure neural), FCM-clf (pure fuzzy, no learning), LDA/LR/LinSVM/RBF-SVM/RF (classical). Hybrid: ANFIS-FCM, the paper's best model, unstacked and stacked (pre-specified, `ANFIS-FCM+stk` is the headline hybrid). The best of all 8 ANFIS rows is added when different, flagged as post-hoc (chosen on the test set).

| model | type | macro-F1 | F1 Attack | accuracy | train s |
|---|---|---|---|---|---|
| MLP | non-hybrid | 0.9606 ± 0.0170 | 0.9317 ± 0.0292 | 0.9817 ± 0.0083 | 1.54 |
| FCM-clf | non-hybrid | 0.9436 ± 0.0054 | 0.9026 ± 0.0092 | 0.9733 ± 0.0028 | 4.31 |
| LDA | non-hybrid | 0.7888 ± 0.0062 | 0.6572 ± 0.0090 | 0.8709 ± 0.0052 | 0.02 |
| LR | non-hybrid | 0.8942 ± 0.0216 | 0.8206 ± 0.0349 | 0.9454 ± 0.0135 | 0.05 |
| LinSVM | non-hybrid | 0.9424 ± 0.0059 | 0.9005 ± 0.0100 | 0.9728 ± 0.0031 | 0.07 |
| RBF-SVM | non-hybrid | 0.9445 ± 0.0080 | 0.9041 ± 0.0136 | 0.9739 ± 0.0041 | 0.82 |
| RF | non-hybrid | 0.9895 ± 0.0030 | 0.9817 ± 0.0052 | 0.9954 ± 0.0013 | 0.61 |
| ANFIS-FCM | hybrid | 0.9499 ± 0.0050 | 0.9133 ± 0.0086 | 0.9766 ± 0.0025 | 4.08 |
| ANFIS-FCM+stk | hybrid | 0.9794 ± 0.0031 | 0.9639 ± 0.0054 | 0.9909 ± 0.0014 | 5.65 |
| ANFIS-SC (best ANFIS, post-hoc) | hybrid | 0.9840 ± 0.0024 | 0.9720 ± 0.0042 | 0.9929 ± 0.0011 | 1.17 |

## Paired differences (macro-F1, per seed, same test sets)

- best non-hybrid vs paper hybrid (RF → ANFIS-FCM+stk): -0.0102 ± 0.0046 (hybrid wins 0/5 seeds, ties 0) → **hybrid worse**
- best non-hybrid vs best ANFIS (post-hoc) (RF → ANFIS-SC): -0.0056 ± 0.0029 (hybrid wins 0/5 seeds, ties 0) → **hybrid worse**
- pure neural (MLP) vs paper hybrid (MLP → ANFIS-FCM+stk): +0.0188 ± 0.0179 (hybrid wins 4/5 seeds, ties 0) → **hybrid better**
- pure fuzzy (FCM-clf) vs paper hybrid (FCM-clf → ANFIS-FCM+stk): +0.0357 ± 0.0071 (hybrid wins 5/5 seeds, ties 0) → **hybrid better**

## McNemar test (seed 0)

- RF vs ANFIS-FCM+stk: only RF correct = 28, only ANFIS-FCM+stk correct = 1, exact p = 1.12e-07
- RF vs ANFIS-SC: only RF correct = 10, only ANFIS-SC correct = 2, exact p = 0.0386

Figure: `figures/comparison1_A-noID_binary.png`
