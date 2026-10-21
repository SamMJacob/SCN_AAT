# Summary: Setting A, binary

Test-set metrics, mean ± std over seeds (different subsample, split and SMOTE per seed). Sorted by macro-F1 (the primary metric). `+stk` = with the augmented stacking ANFIS.

Paper columns: Al Isawi et al. (2025), Tables 6/8 (by caption). The paper's 'Overall F1' is the unweighted mean of per-class F1, i.e. macro-F1. The paper's ANFIS rows are the full stacked architecture, so they are matched to our `+stk` rows. The paper's SVM kernel is not stated; it is matched to RBF-SVM.

| model | family | seeds | macro-F1 | accuracy | F1 Attack | F1 Normal | FPR (macro) | rules | train s | infer ms/1k | paper acc / F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ANFIS-SC | hybrid (ANFIS) | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | 7.6 | 1.17 | 0.52 | – |
| RF | classical ML | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | – | 0.63 | 21.04 | 0.9928 / 0.984 |
| ANFIS-SC+stk | hybrid (ANFIS) | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | 10.8 | 1.62 | 0.54 | 0.9958 / 0.991 |
| ANFIS-FCM+stk | hybrid (ANFIS) | 5 | 0.9998 ± 0.0005 | 0.9999 ± 0.0002 | 0.9996 ± 0.0009 | 0.9999 ± 0.0001 | 0.0001 | 30.0 | 5.10 | 0.68 | 0.9968 / 0.993 |
| ANFIS-KMeans+stk | hybrid (ANFIS) | 5 | 0.9995 ± 0.0007 | 0.9998 ± 0.0003 | 0.9992 ± 0.0013 | 0.9999 ± 0.0002 | 0.0001 | 30.0 | 1.00 | 0.48 | – |
| ANFIS-FCM | hybrid (ANFIS) | 5 | 0.9994 ± 0.0008 | 0.9998 ± 0.0004 | 0.9990 ± 0.0014 | 0.9999 ± 0.0002 | 0.0001 | 20.0 | 4.07 | 0.58 | – |
| ANFIS-KMeans | hybrid (ANFIS) | 5 | 0.9977 ± 0.0024 | 0.9990 ± 0.0010 | 0.9960 ± 0.0042 | 0.9994 ± 0.0006 | 0.0006 | 20.0 | 0.72 | 0.41 | – |
| MLP | non-hybrid soft computing | 5 | 0.9972 ± 0.0015 | 0.9988 ± 0.0006 | 0.9952 ± 0.0026 | 0.9993 ± 0.0004 | 0.0007 | – | 0.99 | 0.32 | – |
| RBF-SVM | classical ML | 5 | 0.9972 ± 0.0011 | 0.9988 ± 0.0005 | 0.9952 ± 0.0019 | 0.9993 ± 0.0003 | 0.0007 | – | 0.14 | 5.45 | 0.9750 / 0.951 |
| ANFIS-Random+stk | hybrid (ANFIS) | 5 | 0.9970 ± 0.0024 | 0.9987 ± 0.0011 | 0.9947 ± 0.0043 | 0.9993 ± 0.0006 | 0.0027 | 30.0 | 0.83 | 0.52 | – |
| LR | classical ML | 5 | 0.9962 ± 0.0013 | 0.9983 ± 0.0006 | 0.9934 ± 0.0023 | 0.9991 ± 0.0003 | 0.0009 | – | 0.04 | 0.10 | 0.9118 / 0.866 |
| LinSVM | classical ML | 5 | 0.9962 ± 0.0024 | 0.9983 ± 0.0011 | 0.9934 ± 0.0043 | 0.9991 ± 0.0006 | 0.0018 | – | 0.03 | 0.12 | – |
| ANFIS-Random | hybrid (ANFIS) | 5 | 0.9856 ± 0.0255 | 0.9933 ± 0.0122 | 0.9751 ± 0.0440 | 0.9961 ± 0.0071 | 0.0058 | 20.0 | 0.68 | 0.47 | – |
| FCM-clf | non-hybrid soft computing | 5 | 0.9502 ± 0.0056 | 0.9767 ± 0.0028 | 0.9139 ± 0.0095 | 0.9865 ± 0.0017 | 0.0133 | 20.0 | 3.12 | 2.30 | – |
| LDA | classical ML | 5 | 0.8519 ± 0.0107 | 0.9185 ± 0.0075 | 0.7526 ± 0.0166 | 0.9512 ± 0.0047 | 0.0465 | – | 0.01 | 0.21 | 0.8593 / 0.819 |
