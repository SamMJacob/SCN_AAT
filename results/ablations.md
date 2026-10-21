# Ablations

Each row compares a variant with the main protocol on the same seeds (paired difference in macro-F1, variant − main).

| setting | task | model | variant | seeds | main | variant value | Δ (variant − main) |
|---|---|---|---|---|---|---|---|
| A | binary | ANFIS-FCM | ep5 | 5 | 0.9994 ± 0.0008 | 0.9992 ± 0.0011 | -0.0002 ± 0.0005 |
| A | binary | ANFIS-FCM | oof | 5 | 0.9994 ± 0.0008 | 0.9994 ± 0.0008 | 0.0000 ± 0.0000 |
| A | binary | ANFIS-FCM+stk | ep5 | 5 | 0.9998 ± 0.0005 | 0.9998 ± 0.0005 | 0.0000 ± 0.0000 |
| A | binary | ANFIS-FCM+stk | oof | 5 | 0.9998 ± 0.0005 | 0.9979 ± 0.0038 | -0.0019 ± 0.0033 |
| A | binary | ANFIS-KMeans | ep5 | 5 | 0.9977 ± 0.0024 | 0.9969 ± 0.0059 | -0.0008 ± 0.0037 |
| A | binary | ANFIS-KMeans | oof | 5 | 0.9977 ± 0.0024 | 0.9977 ± 0.0024 | 0.0000 ± 0.0000 |
| A | binary | ANFIS-KMeans+stk | ep5 | 5 | 0.9995 ± 0.0007 | 1.0000 ± 0.0000 | 0.0005 ± 0.0007 |
| A | binary | ANFIS-KMeans+stk | oof | 5 | 0.9995 ± 0.0007 | 0.9981 ± 0.0029 | -0.0015 ± 0.0030 |
| A | binary | ANFIS-Random | ep5 | 5 | 0.9856 ± 0.0255 | 0.9979 ± 0.0021 | 0.0123 ± 0.0257 |
| A | binary | ANFIS-Random+stk | ep5 | 5 | 0.9970 ± 0.0024 | 0.9984 ± 0.0009 | 0.0014 ± 0.0017 |
| A | binary | ANFIS-SC | ep5 | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | binary | ANFIS-SC | oof | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | binary | ANFIS-SC+stk | ep5 | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | binary | ANFIS-SC+stk | oof | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-FCM | ep5 | 5 | 0.9993 ± 0.0016 | 0.9996 ± 0.0008 | 0.0004 ± 0.0008 |
| A | multi | ANFIS-FCM | oof | 5 | 0.9993 ± 0.0016 | 0.9993 ± 0.0016 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-FCM+stk | ep5 | 5 | 1.0000 ± 0.0000 | 0.9996 ± 0.0008 | -0.0004 ± 0.0008 |
| A | multi | ANFIS-FCM+stk | oof | 5 | 1.0000 ± 0.0000 | 0.9981 ± 0.0042 | -0.0019 ± 0.0042 |
| A | multi | ANFIS-KMeans | ep5 | 5 | 0.9959 ± 0.0054 | 0.9977 ± 0.0028 | 0.0017 ± 0.0049 |
| A | multi | ANFIS-KMeans | oof | 5 | 0.9959 ± 0.0054 | 0.9959 ± 0.0054 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-KMeans+stk | ep5 | 5 | 0.9986 ± 0.0032 | 1.0000 ± 0.0000 | 0.0014 ± 0.0032 |
| A | multi | ANFIS-KMeans+stk | oof | 5 | 0.9986 ± 0.0032 | 0.9848 ± 0.0293 | -0.0138 ± 0.0299 |
| A | multi | ANFIS-Random | ep5 | 5 | 0.9841 ± 0.0304 | 0.9986 ± 0.0005 | 0.0145 ± 0.0308 |
| A | multi | ANFIS-Random+stk | ep5 | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-SC | ep5 | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-SC | oof | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-SC+stk | ep5 | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A | multi | ANFIS-SC+stk | oof | 5 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0000 ± 0.0000 |
| A-noID | binary | ANFIS-FCM | R20 | 5 | 0.9499 ± 0.0050 | 0.9707 ± 0.0180 | 0.0208 ± 0.0183 |
| A-noID | binary | ANFIS-FCM | ep5 | 5 | 0.9499 ± 0.0050 | 0.9692 ± 0.0168 | 0.0193 ± 0.0179 |
| A-noID | binary | ANFIS-FCM | nosmote | 5 | 0.9499 ± 0.0050 | 0.9782 ± 0.0031 | 0.0283 ± 0.0047 |
| A-noID | binary | ANFIS-FCM | oof | 5 | 0.9499 ± 0.0050 | 0.9499 ± 0.0050 | 0.0000 ± 0.0000 |
| A-noID | binary | ANFIS-FCM+stk | R20 | 5 | 0.9794 ± 0.0031 | 0.9823 ± 0.0027 | 0.0030 ± 0.0047 |
| A-noID | binary | ANFIS-FCM+stk | ep5 | 5 | 0.9794 ± 0.0031 | 0.9813 ± 0.0017 | 0.0019 ± 0.0034 |
| A-noID | binary | ANFIS-FCM+stk | nosmote | 5 | 0.9794 ± 0.0031 | 0.9784 ± 0.0029 | -0.0010 ± 0.0034 |
| A-noID | binary | ANFIS-FCM+stk | oof | 5 | 0.9794 ± 0.0031 | 0.9557 ± 0.0124 | -0.0237 ± 0.0139 |
| A-noID | binary | ANFIS-KMeans | R20 | 5 | 0.9557 ± 0.0147 | 0.9610 ± 0.0319 | 0.0053 ± 0.0308 |
| A-noID | binary | ANFIS-KMeans | ep5 | 5 | 0.9557 ± 0.0147 | 0.9605 ± 0.0155 | 0.0048 ± 0.0030 |
| A-noID | binary | ANFIS-KMeans | nosmote | 5 | 0.9557 ± 0.0147 | 0.9550 ± 0.0142 | -0.0007 ± 0.0097 |
| A-noID | binary | ANFIS-KMeans | oof | 5 | 0.9557 ± 0.0147 | 0.9557 ± 0.0147 | 0.0000 ± 0.0000 |
| A-noID | binary | ANFIS-KMeans+stk | R20 | 5 | 0.9798 ± 0.0040 | 0.9769 ± 0.0182 | -0.0029 ± 0.0180 |
| A-noID | binary | ANFIS-KMeans+stk | ep5 | 5 | 0.9798 ± 0.0040 | 0.9856 ± 0.0034 | 0.0058 ± 0.0065 |
| A-noID | binary | ANFIS-KMeans+stk | nosmote | 5 | 0.9798 ± 0.0040 | 0.9742 ± 0.0074 | -0.0056 ± 0.0057 |
| A-noID | binary | ANFIS-KMeans+stk | oof | 5 | 0.9798 ± 0.0040 | 0.9630 ± 0.0123 | -0.0168 ± 0.0133 |
| A-noID | binary | ANFIS-Random | R20 | 5 | 0.9568 ± 0.0151 | 0.9770 ± 0.0045 | 0.0202 ± 0.0178 |
| A-noID | binary | ANFIS-Random | ep5 | 5 | 0.9568 ± 0.0151 | 0.9570 ± 0.0149 | 0.0002 ± 0.0003 |
| A-noID | binary | ANFIS-Random | nosmote | 5 | 0.9568 ± 0.0151 | 0.9759 ± 0.0031 | 0.0191 ± 0.0160 |
| A-noID | binary | ANFIS-Random+stk | R20 | 5 | 0.9713 ± 0.0158 | 0.9806 ± 0.0010 | 0.0093 ± 0.0165 |
| A-noID | binary | ANFIS-Random+stk | ep5 | 5 | 0.9713 ± 0.0158 | 0.9721 ± 0.0160 | 0.0008 ± 0.0015 |
| A-noID | binary | ANFIS-Random+stk | nosmote | 5 | 0.9713 ± 0.0158 | 0.9770 ± 0.0034 | 0.0057 ± 0.0184 |
| A-noID | binary | ANFIS-SC | ep5 | 5 | 0.9840 ± 0.0024 | 0.9836 ± 0.0021 | -0.0003 ± 0.0005 |
| A-noID | binary | ANFIS-SC | nosmote | 5 | 0.9840 ± 0.0024 | 0.9881 ± 0.0025 | 0.0042 ± 0.0026 |
| A-noID | binary | ANFIS-SC | oof | 5 | 0.9840 ± 0.0024 | 0.9840 ± 0.0024 | 0.0000 ± 0.0000 |
| A-noID | binary | ANFIS-SC+stk | ep5 | 5 | 0.9838 ± 0.0023 | 0.9837 ± 0.0022 | -0.0001 ± 0.0002 |
| A-noID | binary | ANFIS-SC+stk | nosmote | 5 | 0.9838 ± 0.0023 | 0.9885 ± 0.0022 | 0.0046 ± 0.0020 |
| A-noID | binary | ANFIS-SC+stk | oof | 5 | 0.9838 ± 0.0023 | 0.9836 ± 0.0021 | -0.0002 ± 0.0008 |
| A-noID | binary | FCM-clf | nosmote | 5 | 0.9436 ± 0.0054 | 0.7989 ± 0.0212 | -0.1447 ± 0.0228 |
| A-noID | binary | LDA | nosmote | 5 | 0.7888 ± 0.0062 | 0.8373 ± 0.0048 | 0.0485 ± 0.0084 |
| A-noID | binary | LR | nosmote | 5 | 0.8942 ± 0.0216 | 0.9198 ± 0.0029 | 0.0256 ± 0.0203 |
| A-noID | binary | LinSVM | nosmote | 5 | 0.9424 ± 0.0059 | 0.9321 ± 0.0036 | -0.0103 ± 0.0058 |
| A-noID | binary | MLP | nosmote | 5 | 0.9606 ± 0.0170 | 0.9340 ± 0.0522 | -0.0265 ± 0.0654 |
| A-noID | binary | RBF-SVM | nosmote | 5 | 0.9445 ± 0.0080 | 0.9739 ± 0.0050 | 0.0294 ± 0.0060 |
| A-noID | binary | RF | nosmote | 5 | 0.9895 ± 0.0030 | 0.9874 ± 0.0028 | -0.0022 ± 0.0032 |
| A-noID | multi | ANFIS-FCM | R20 | 5 | 0.9525 ± 0.0059 | 0.9824 ± 0.0019 | 0.0299 ± 0.0061 |
| A-noID | multi | ANFIS-FCM | ep5 | 5 | 0.9525 ± 0.0059 | 0.9589 ± 0.0152 | 0.0065 ± 0.0140 |
| A-noID | multi | ANFIS-FCM | nosmote | 5 | 0.9525 ± 0.0059 | 0.9821 ± 0.0031 | 0.0297 ± 0.0061 |
| A-noID | multi | ANFIS-FCM | oof | 5 | 0.9525 ± 0.0059 | 0.9525 ± 0.0059 | 0.0000 ± 0.0000 |
| A-noID | multi | ANFIS-FCM+stk | R20 | 5 | 0.9847 ± 0.0084 | 0.9846 ± 0.0037 | -0.0001 ± 0.0070 |
| A-noID | multi | ANFIS-FCM+stk | ep5 | 5 | 0.9847 ± 0.0084 | 0.9861 ± 0.0031 | 0.0013 ± 0.0054 |
| A-noID | multi | ANFIS-FCM+stk | nosmote | 5 | 0.9847 ± 0.0084 | 0.9672 ± 0.0125 | -0.0175 ± 0.0144 |
| A-noID | multi | ANFIS-FCM+stk | oof | 5 | 0.9847 ± 0.0084 | 0.9392 ± 0.0140 | -0.0455 ± 0.0097 |
| A-noID | multi | ANFIS-KMeans | R20 | 5 | 0.9598 ± 0.0055 | 0.9464 ± 0.0119 | -0.0134 ± 0.0092 |
| A-noID | multi | ANFIS-KMeans | ep5 | 5 | 0.9598 ± 0.0055 | 0.9523 ± 0.0163 | -0.0075 ± 0.0208 |
| A-noID | multi | ANFIS-KMeans | nosmote | 5 | 0.9598 ± 0.0055 | 0.9757 ± 0.0078 | 0.0159 ± 0.0121 |
| A-noID | multi | ANFIS-KMeans | oof | 5 | 0.9598 ± 0.0055 | 0.9598 ± 0.0055 | 0.0000 ± 0.0000 |
| A-noID | multi | ANFIS-KMeans+stk | R20 | 5 | 0.9871 ± 0.0031 | 0.9864 ± 0.0031 | -0.0007 ± 0.0021 |
| A-noID | multi | ANFIS-KMeans+stk | ep5 | 5 | 0.9871 ± 0.0031 | 0.9867 ± 0.0026 | -0.0004 ± 0.0018 |
| A-noID | multi | ANFIS-KMeans+stk | nosmote | 5 | 0.9871 ± 0.0031 | 0.9717 ± 0.0086 | -0.0154 ± 0.0099 |
| A-noID | multi | ANFIS-KMeans+stk | oof | 5 | 0.9871 ± 0.0031 | 0.9786 ± 0.0157 | -0.0084 ± 0.0171 |
| A-noID | multi | ANFIS-Random | R20 | 5 | 0.9463 ± 0.0122 | 0.9666 ± 0.0132 | 0.0203 ± 0.0104 |
| A-noID | multi | ANFIS-Random | ep5 | 5 | 0.9463 ± 0.0122 | 0.9475 ± 0.0110 | 0.0012 ± 0.0015 |
| A-noID | multi | ANFIS-Random | nosmote | 5 | 0.9463 ± 0.0122 | 0.9544 ± 0.0059 | 0.0081 ± 0.0129 |
| A-noID | multi | ANFIS-Random+stk | R20 | 5 | 0.9659 ± 0.0093 | 0.9748 ± 0.0029 | 0.0090 ± 0.0109 |
| A-noID | multi | ANFIS-Random+stk | ep5 | 5 | 0.9659 ± 0.0093 | 0.9665 ± 0.0102 | 0.0007 ± 0.0022 |
| A-noID | multi | ANFIS-Random+stk | nosmote | 5 | 0.9659 ± 0.0093 | 0.9460 ± 0.0097 | -0.0198 ± 0.0142 |
| A-noID | multi | ANFIS-SC | ep5 | 5 | 0.9832 ± 0.0019 | 0.9833 ± 0.0019 | 0.0001 ± 0.0003 |
| A-noID | multi | ANFIS-SC | nosmote | 5 | 0.9832 ± 0.0019 | 0.9866 ± 0.0025 | 0.0034 ± 0.0034 |
| A-noID | multi | ANFIS-SC | oof | 5 | 0.9832 ± 0.0019 | 0.9832 ± 0.0019 | 0.0000 ± 0.0000 |
| A-noID | multi | ANFIS-SC+stk | ep5 | 5 | 0.9861 ± 0.0035 | 0.9858 ± 0.0030 | -0.0003 ± 0.0014 |
| A-noID | multi | ANFIS-SC+stk | nosmote | 5 | 0.9861 ± 0.0035 | 0.9780 ± 0.0071 | -0.0082 ± 0.0073 |
| A-noID | multi | ANFIS-SC+stk | oof | 5 | 0.9861 ± 0.0035 | 0.9854 ± 0.0036 | -0.0007 ± 0.0010 |
| A-noID | multi | FCM-clf | nosmote | 5 | 0.8838 ± 0.0137 | 0.5844 ± 0.0182 | -0.2994 ± 0.0101 |
| A-noID | multi | LDA | nosmote | 5 | 0.6815 ± 0.0085 | 0.5789 ± 0.0076 | -0.1026 ± 0.0061 |
| A-noID | multi | LR | nosmote | 5 | 0.8621 ± 0.0223 | 0.8429 ± 0.0076 | -0.0192 ± 0.0152 |
| A-noID | multi | LinSVM | nosmote | 5 | 0.9214 ± 0.0056 | 0.8884 ± 0.0058 | -0.0330 ± 0.0092 |
| A-noID | multi | MLP | nosmote | 5 | 0.9824 ± 0.0016 | 0.9449 ± 0.0275 | -0.0375 ± 0.0272 |
| A-noID | multi | RBF-SVM | nosmote | 5 | 0.9441 ± 0.0189 | 0.9528 ± 0.0043 | 0.0088 ± 0.0179 |
| A-noID | multi | RF | nosmote | 5 | 0.9886 ± 0.0030 | 0.9867 ± 0.0029 | -0.0019 ± 0.0031 |
| B | binary | ANFIS-FCM | ep5 | 5 | 0.9455 ± 0.0056 | 0.9454 ± 0.0058 | -0.0001 ± 0.0003 |
| B | binary | ANFIS-FCM+stk | ep5 | 5 | 0.9455 ± 0.0056 | 0.9454 ± 0.0056 | -0.0001 ± 0.0002 |
| B | binary | ANFIS-KMeans | ep5 | 5 | 0.9432 ± 0.0072 | 0.9444 ± 0.0053 | 0.0012 ± 0.0029 |
| B | binary | ANFIS-KMeans+stk | ep5 | 5 | 0.9455 ± 0.0056 | 0.9456 ± 0.0057 | 0.0001 ± 0.0008 |
| B | binary | ANFIS-Random | ep5 | 5 | 0.9447 ± 0.0059 | 0.9451 ± 0.0058 | 0.0005 ± 0.0005 |
| B | binary | ANFIS-Random+stk | ep5 | 5 | 0.9453 ± 0.0051 | 0.9455 ± 0.0053 | 0.0001 ± 0.0006 |
| B | binary | ANFIS-SC | ep5 | 5 | 0.9457 ± 0.0058 | 0.9458 ± 0.0057 | 0.0001 ± 0.0003 |
| B | binary | ANFIS-SC+stk | ep5 | 5 | 0.9450 ± 0.0053 | 0.9453 ± 0.0056 | 0.0002 ± 0.0005 |
| B | multi | ANFIS-FCM | ep5 | 5 | 0.9259 ± 0.0068 | 0.9260 ± 0.0066 | 0.0001 ± 0.0007 |
| B | multi | ANFIS-FCM+stk | ep5 | 5 | 0.9257 ± 0.0072 | 0.9252 ± 0.0066 | -0.0006 ± 0.0014 |
| B | multi | ANFIS-KMeans | ep5 | 5 | 0.9259 ± 0.0071 | 0.9259 ± 0.0069 | 0.0000 ± 0.0004 |
| B | multi | ANFIS-KMeans+stk | ep5 | 5 | 0.9258 ± 0.0070 | 0.9259 ± 0.0068 | 0.0001 ± 0.0005 |
| B | multi | ANFIS-Random | ep5 | 5 | 0.9232 ± 0.0087 | 0.9232 ± 0.0086 | 0.0001 ± 0.0001 |
| B | multi | ANFIS-Random+stk | ep5 | 5 | 0.9239 ± 0.0075 | 0.9237 ± 0.0078 | -0.0002 ± 0.0005 |
| B | multi | ANFIS-SC | ep5 | 5 | 0.9263 ± 0.0065 | 0.9263 ± 0.0065 | 0.0000 ± 0.0000 |
| B | multi | ANFIS-SC+stk | ep5 | 5 | 0.9256 ± 0.0063 | 0.9251 ± 0.0060 | -0.0004 ± 0.0011 |

## Stacking on/off (main runs, Δ = +stk − OvR)

| setting | task | init | Δ macro-F1 |
|---|---|---|---|
| A | binary | Random | 0.0114 ± 0.0258 |
| A | binary | KMeans | 0.0018 ± 0.0025 |
| A | binary | SC | 0.0000 ± 0.0000 |
| A | binary | FCM | 0.0003 ± 0.0008 |
| A | multi | Random | 0.0159 ± 0.0304 |
| A | multi | KMeans | 0.0026 ± 0.0033 |
| A | multi | SC | 0.0000 ± 0.0000 |
| A | multi | FCM | 0.0007 ± 0.0016 |
| A-noID | binary | Random | 0.0145 ± 0.0148 |
| A-noID | binary | KMeans | 0.0241 ± 0.0139 |
| A-noID | binary | SC | -0.0001 ± 0.0002 |
| A-noID | binary | FCM | 0.0295 ± 0.0068 |
| A-noID | multi | Random | 0.0196 ± 0.0087 |
| A-noID | multi | KMeans | 0.0273 ± 0.0037 |
| A-noID | multi | SC | 0.0029 ± 0.0033 |
| A-noID | multi | FCM | 0.0323 ± 0.0048 |
| B | binary | Random | 0.0007 ± 0.0011 |
| B | binary | KMeans | 0.0024 ± 0.0018 |
| B | binary | SC | -0.0006 ± 0.0007 |
| B | binary | FCM | 0.0000 ± 0.0000 |
| B | multi | Random | 0.0008 ± 0.0018 |
| B | multi | KMeans | -0.0000 ± 0.0005 |
| B | multi | SC | -0.0007 ± 0.0006 |
| B | multi | FCM | -0.0001 ± 0.0006 |
| B-ID | binary | Random | 0.0000 ± 0.0000 |
| B-ID | binary | KMeans | 0.0101 ± 0.0220 |
| B-ID | binary | SC | -0.0001 ± 0.0012 |
| B-ID | binary | FCM | -0.0001 ± 0.0002 |
| B-ID | multi | Random | -0.0001 ± 0.0002 |
| B-ID | multi | KMeans | -0.0005 ± 0.0005 |
| B-ID | multi | SC | -0.0010 ± 0.0009 |
| B-ID | multi | FCM | 0.0001 ± 0.0010 |

## Effect of removing the CAN ID (A → A-noID, B-ID → B), macro-F1 means

| pair | task | model | with ID | without ID | Δ |
|---|---|---|---|---|---|
| A → A-noID | binary | MLP | 0.9972 | 0.9606 | -0.0367 |
| A → A-noID | binary | FCM-clf | 0.9502 | 0.9436 | -0.0066 |
| A → A-noID | binary | LDA | 0.8519 | 0.7888 | -0.0631 |
| A → A-noID | binary | LR | 0.9962 | 0.8942 | -0.1020 |
| A → A-noID | binary | LinSVM | 0.9962 | 0.9424 | -0.0539 |
| A → A-noID | binary | RBF-SVM | 0.9972 | 0.9445 | -0.0527 |
| A → A-noID | binary | RF | 1.0000 | 0.9895 | -0.0105 |
| A → A-noID | binary | ANFIS-Random | 0.9856 | 0.9568 | -0.0288 |
| A → A-noID | binary | ANFIS-Random+stk | 0.9970 | 0.9713 | -0.0257 |
| A → A-noID | binary | ANFIS-KMeans | 0.9977 | 0.9557 | -0.0420 |
| A → A-noID | binary | ANFIS-KMeans+stk | 0.9995 | 0.9798 | -0.0197 |
| A → A-noID | binary | ANFIS-SC | 1.0000 | 0.9840 | -0.0160 |
| A → A-noID | binary | ANFIS-SC+stk | 1.0000 | 0.9838 | -0.0162 |
| A → A-noID | binary | ANFIS-FCM | 0.9994 | 0.9499 | -0.0495 |
| A → A-noID | binary | ANFIS-FCM+stk | 0.9998 | 0.9794 | -0.0204 |
| B-ID → B | binary | MLP | 0.9446 | 0.9041 | -0.0405 |
| B-ID → B | binary | FCM-clf | 0.9067 | 0.9233 | +0.0166 |
| B-ID → B | binary | LDA | 0.8387 | 0.7959 | -0.0427 |
| B-ID → B | binary | LR | 0.9424 | 0.9448 | +0.0024 |
| B-ID → B | binary | LinSVM | 0.9431 | 0.9445 | +0.0014 |
| B-ID → B | binary | RBF-SVM | 0.9451 | 0.9449 | -0.0002 |
| B-ID → B | binary | RF | 0.9410 | 0.9414 | +0.0005 |
| B-ID → B | binary | ANFIS-Random | 0.9455 | 0.9447 | -0.0008 |
| B-ID → B | binary | ANFIS-Random+stk | 0.9455 | 0.9453 | -0.0001 |
| B-ID → B | binary | ANFIS-KMeans | 0.9345 | 0.9432 | +0.0087 |
| B-ID → B | binary | ANFIS-KMeans+stk | 0.9446 | 0.9455 | +0.0010 |
| B-ID → B | binary | ANFIS-SC | 0.9453 | 0.9457 | +0.0004 |
| B-ID → B | binary | ANFIS-SC+stk | 0.9452 | 0.9450 | -0.0001 |
| B-ID → B | binary | ANFIS-FCM | 0.9456 | 0.9455 | -0.0001 |
| B-ID → B | binary | ANFIS-FCM+stk | 0.9455 | 0.9455 | +0.0000 |
| A → A-noID | multi | MLP | 0.9979 | 0.9824 | -0.0155 |
| A → A-noID | multi | FCM-clf | 0.9318 | 0.8838 | -0.0480 |
| A → A-noID | multi | LDA | 0.8231 | 0.6815 | -0.1416 |
| A → A-noID | multi | LR | 0.9938 | 0.8621 | -0.1317 |
| A → A-noID | multi | LinSVM | 0.9896 | 0.9214 | -0.0682 |
| A → A-noID | multi | RBF-SVM | 0.9971 | 0.9441 | -0.0530 |
| A → A-noID | multi | RF | 1.0000 | 0.9886 | -0.0114 |
| A → A-noID | multi | ANFIS-Random | 0.9841 | 0.9463 | -0.0378 |
| A → A-noID | multi | ANFIS-Random+stk | 1.0000 | 0.9659 | -0.0341 |
| A → A-noID | multi | ANFIS-KMeans | 0.9959 | 0.9598 | -0.0361 |
| A → A-noID | multi | ANFIS-KMeans+stk | 0.9986 | 0.9871 | -0.0115 |
| A → A-noID | multi | ANFIS-SC | 1.0000 | 0.9832 | -0.0168 |
| A → A-noID | multi | ANFIS-SC+stk | 1.0000 | 0.9861 | -0.0139 |
| A → A-noID | multi | ANFIS-FCM | 0.9993 | 0.9525 | -0.0468 |
| A → A-noID | multi | ANFIS-FCM+stk | 1.0000 | 0.9847 | -0.0153 |
| B-ID → B | multi | MLP | 0.9260 | 0.9241 | -0.0019 |
| B-ID → B | multi | FCM-clf | 0.8823 | 0.8351 | -0.0472 |
| B-ID → B | multi | LDA | 0.7751 | 0.7148 | -0.0603 |
| B-ID → B | multi | LR | 0.9214 | 0.9010 | -0.0204 |
| B-ID → B | multi | LinSVM | 0.9220 | 0.9018 | -0.0202 |
| B-ID → B | multi | RBF-SVM | 0.9248 | 0.9111 | -0.0137 |
| B-ID → B | multi | RF | 0.9193 | 0.9190 | -0.0003 |
| B-ID → B | multi | ANFIS-Random | 0.9265 | 0.9232 | -0.0033 |
| B-ID → B | multi | ANFIS-Random+stk | 0.9264 | 0.9239 | -0.0025 |
| B-ID → B | multi | ANFIS-KMeans | 0.9263 | 0.9259 | -0.0004 |
| B-ID → B | multi | ANFIS-KMeans+stk | 0.9258 | 0.9258 | +0.0001 |
| B-ID → B | multi | ANFIS-SC | 0.9261 | 0.9263 | +0.0002 |
| B-ID → B | multi | ANFIS-SC+stk | 0.9251 | 0.9256 | +0.0004 |
| B-ID → B | multi | ANFIS-FCM | 0.9257 | 0.9259 | +0.0002 |
| B-ID → B | multi | ANFIS-FCM+stk | 0.9259 | 0.9257 | -0.0001 |
