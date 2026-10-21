# Setting B learnability probe

Task: classify each 0x164 frame of the impersonation log as after 250 s ('Impersonation', n = 27,673) or before 250 s (genuine, n = 29,799). 5-fold CV with 10 s time blocks as groups (stratified), AUC computed per fold and averaged. Control: identical probe on attack-free 0x164 frames with a fake boundary at 250 s (n = 61,018). AUC = 0.5 means no per-frame signal.

| data | features | model | ROC AUC (mean ± std over folds) |
|---|---|---|---|
| impersonation log (real boundary) | payload+DLC | LR | 0.501 ± 0.002 |
| impersonation log (real boundary) | payload+DLC | RF | 0.500 ± 0.002 |
| impersonation log (real boundary) | payload+DLC | ANFIS-FCM | 0.500 ± 0.002 |
| attack-free log (fake boundary, control) | payload+DLC | LR | 0.500 ± 0.001 |
| attack-free log (fake boundary, control) | payload+DLC | RF | 0.501 ± 0.002 |
| attack-free log (fake boundary, control) | payload+DLC | ANFIS-FCM | 0.501 ± 0.002 |
| impersonation log (real boundary) | timing (log_dt, hamming) | LR | 0.499 ± 0.004 |
| impersonation log (real boundary) | timing (log_dt, hamming) | RF | 0.591 ± 0.013 |
| impersonation log (real boundary) | timing (log_dt, hamming) | ANFIS-FCM | 0.496 ± 0.008 |
| attack-free log (fake boundary, control) | timing (log_dt, hamming) | LR | 0.500 ± 0.002 |
| attack-free log (fake boundary, control) | timing (log_dt, hamming) | RF | 0.504 ± 0.005 |
| attack-free log (fake boundary, control) | timing (log_dt, hamming) | ANFIS-FCM | 0.498 ± 0.006 |
| impersonation log (real boundary) | all | LR | 0.502 ± 0.003 |
| impersonation log (real boundary) | all | RF | 0.605 ± 0.013 |
| impersonation log (real boundary) | all | ANFIS-FCM | 0.499 ± 0.004 |
| attack-free log (fake boundary, control) | all | LR | 0.500 ± 0.002 |
| attack-free log (fake boundary, control) | all | RF | 0.505 ± 0.008 |
| attack-free log (fake boundary, control) | all | ANFIS-FCM | 0.503 ± 0.005 |
