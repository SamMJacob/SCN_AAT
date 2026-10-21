# Summary: Setting A, multi

Test-set metrics, mean ± std over seeds (different subsample, split and SMOTE per seed). Sorted by macro-F1 (the primary metric). `+stk` = with the augmented stacking ANFIS.

Paper columns: Al Isawi et al. (2025), Tables 6/8 (by caption). The paper's 'Overall F1' is the unweighted mean of per-class F1, i.e. macro-F1. The paper's ANFIS rows are the full stacked architecture, so they are matched to our `+stk` rows. The paper's SVM kernel is not stated; it is matched to RBF-SVM.

| model | family | seeds | macro-F1 | accuracy | F1 DoS | F1 Imp | F1 Normal | FPR (macro) | rules | train s | infer ms/1k | paper acc / F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ANFIS-FCM+stk | hybrid (ANFIS) | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | 40.0 | 10.03 | 0.80 | 0.9968 / 0.989 |
| ANFIS-Random+stk | hybrid (ANFIS) | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | 40.0 | 0.99 | 0.67 | – |
| ANFIS-SC | hybrid (ANFIS) | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | 19.6 | 1.63 | 0.77 | – |
| RF | classical ML | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | – | 0.64 | 19.71 | – |
| ANFIS-SC+stk | hybrid (ANFIS) | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 | 23.4 | 2.07 | 0.85 | 0.9965 / 0.988 |
| ANFIS-FCM | hybrid (ANFIS) | 5 | 0.9993 ± 0.0016 | 0.9998 ± 0.0004 | 1.0000 ± 0.0000 | 0.9980 ± 0.0045 | 0.9999 ± 0.0003 | 0.0001 | 30.0 | 8.92 | 0.79 | – |
| ANFIS-KMeans+stk | hybrid (ANFIS) | 5 | 0.9986 ± 0.0032 | 0.9996 ± 0.0009 | 1.0000 ± 0.0000 | 0.9960 ± 0.0089 | 0.9998 ± 0.0005 | 0.0001 | 40.0 | 1.73 | 0.72 | – |
| MLP | non-hybrid soft computing | 5 | 0.9979 ± 0.0016 | 0.9992 ± 0.0005 | 0.9967 ± 0.0012 | 0.9975 ± 0.0036 | 0.9996 ± 0.0003 | 0.0003 | – | 1.73 | 0.50 | – |
| RBF-SVM | classical ML | 5 | 0.9971 ± 0.0011 | 0.9988 ± 0.0004 | 0.9920 ± 0.0030 | 1.0000 ± 0.0000 | 0.9993 ± 0.0003 | 0.0004 | – | 0.16 | 5.68 | – |
| ANFIS-KMeans | hybrid (ANFIS) | 5 | 0.9959 ± 0.0054 | 0.9989 ± 0.0016 | 1.0000 ± 0.0000 | 0.9885 ± 0.0154 | 0.9993 ± 0.0009 | 0.0010 | 30.0 | 1.35 | 0.58 | – |
| LR | classical ML | 5 | 0.9938 ± 0.0016 | 0.9981 ± 0.0005 | 0.9967 ± 0.0012 | 0.9859 ± 0.0038 | 0.9989 ± 0.0003 | 0.0007 | – | 0.18 | 0.14 | – |
| LinSVM | classical ML | 5 | 0.9896 ± 0.0036 | 0.9969 ± 0.0011 | 0.9957 ± 0.0032 | 0.9750 ± 0.0083 | 0.9982 ± 0.0006 | 0.0040 | – | 0.24 | 0.16 | – |
| ANFIS-Random | hybrid (ANFIS) | 5 | 0.9841 ± 0.0304 | 0.9946 ± 0.0104 | 0.9980 ± 0.0014 | 0.9574 ± 0.0853 | 0.9969 ± 0.0060 | 0.0019 | 30.0 | 0.79 | 0.62 | – |
| FCM-clf | non-hybrid soft computing | 5 | 0.9318 ± 0.0064 | 0.9768 ± 0.0027 | 0.9963 ± 0.0018 | 0.8125 ± 0.0165 | 0.9866 ± 0.0016 | 0.0081 | 12.0 | 2.90 | 1.34 | – |
| LDA | classical ML | 5 | 0.8231 ± 0.0092 | 0.9136 ± 0.0077 | 0.9807 ± 0.0066 | 0.5407 ± 0.0216 | 0.9481 ± 0.0049 | 0.0303 | – | 0.02 | 0.13 | – |
| CNN (paper only) | deep learning (not run) | – | – | – | – | – | – | – | – | – | – | 0.8263 / 0.497 |
| CNN-LSTM (paper only) | deep learning (not run) | – | – | – | – | – | – | – | – | – | – | 0.8645 / 0.459 |
| GRU (paper only) | deep learning (not run) | – | – | – | – | – | – | – | – | – | – | 0.9950 / 0.982 |
| LSTM (paper only) | deep learning (not run) | – | – | – | – | – | – | – | – | – | – | 0.9955 / 0.984 |
