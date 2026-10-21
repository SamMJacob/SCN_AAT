## 9. Discussion (hand-written after reading the numbers above)

All numbers below are copied from the tables above, `results/ablations.md`, `results/probe_B.md` and
`results/rule_sweep.csv`. "A-noID" is the main benchmark.

### Setting A reproduces the paper, and shows why its headline is uninformative
- Our ANFIS-SC/FCM+stk reach 100.0 % / 99.99 % accuracy, against the paper's 99.6–99.7 %. RF, MLP, RBF-SVM and
  LR also reach ≥ 0.99 macro-F1. The CAN ID determines the label, so any model that can isolate
  ID 0 and ID 356 hits the ceiling.
- Why linear baselines vary: with the CAN ID as its only input, LR gets macro-F1 0.718 and LDA 0.671
  (Setting A binary, seed 0). ID 0x164 = 356 sits mid-range, so one linear cut cannot isolate it. With
  all 10 inputs, LR gets 0.934 at C = 1 and 0.995 at C = 10, the value validation tuning picks. The
  paper's LR (0.866) is consistent with an untuned, strongly regularised model. LDA stays weak
  (0.85) in both studies.

### Comparison 1: non-hybrid vs hybrid (A-noID)
- **Best overall is a non-hybrid model: Random Forest** (macro-F1 0.990 binary / 0.989 multi). The
  pre-specified hybrid (ANFIS-FCM+stk) is significantly worse in binary (Δ = −0.010, worse on 5/5 seeds;
  McNemar p ≈ 1e-7 on seed 0). It is within noise of RF in multiclass (Δ = −0.004 ± 0.006). Even the best
  ANFIS chosen post hoc on the test set (ANFIS-SC 0.984 binary; ANFIS-KMeans+stk 0.987 multi) does
  not beat RF.
- **Against its own non-hybrid ingredients, the hybrid wins clearly.**
  - **vs pure fuzzy (FCM classifier):** +0.036 binary and +0.101 multiclass, on 5/5 seeds. Adding
    neural learning (LSE consequents + gradient-tuned MFs) on top of FCM clusters is the single
    largest improvement in the study.
  - **vs pure neural (MLP):** +0.019 in binary (4/5 seeds, MLP is unstable across seeds: std 0.017).
    Within noise in multiclass (MLP 0.982 vs 0.985).
- **Impersonation F1** (multiclass, A-noID): RF 1.000, MLP 0.997, unstacked ANFIS-KMeans/SC/FCM
  0.998–0.9995, FCM classifier 0.80, LR 0.76. The stacking stage slightly *lowers* Imp F1
  (0.988–0.994 for KMeans/SC/FCM; 0.939 for Random). Rounding a regressed class index puts Imp (index 1) between DoS and Normal, so
  stage-2 errors spill into it.
- Where the errors are (seed 0 confusion matrices, multiclass): nearly all are Normal frames
  predicted as DoS (RF 19, ANFIS-FCM+stk 17 of 3505). These are normal frames with an all-zero
  payload (159k such frames exist in the attack-free log), which look like DoS once the ID is gone.
  Only timing separates them. Impersonation is recognised perfectly by both models.
- Cost and size: ANFIS trains in 1–11 s with 20–63 rules, against RF's 200 trees in under 1 s. ANFIS's advantage
  is a compact, inspectable rule base (see the MF figures), not accuracy.

**Answer to Q1:** hybridisation helps relative to its components: a large gain over the pure fuzzy
model and a modest, setting-dependent gain over a pure MLP. It does not beat a strong classical
ensemble (RF) on this data. In Setting A everything is at the ceiling, and in Setting B there is
nothing learnable to compare (below).

### Comparison 2: clustering init (A-noID)
- **At the paper's R = 10:** SC is best unstacked (0.984 / 0.983). It beats Random on 5/5 seeds in both
  tasks (+0.027 / +0.037) and has the lowest variance. KMeans beats Random in multiclass (+0.014, 5/5).
  FCM is within noise of Random and *below* KMeans in multiclass (−0.007, 0/5).
- **Confound: rule count.** SC sizes itself (43–50 rules in total vs 20–30). With R = 20 per member
  (`R20` rows in `ablations.md`):
  - FCM rises to 0.971 / 0.982, closing most of the gap to SC in multiclass.
  - Random rises to 0.977 / 0.967.
  - KMeans does not improve (0.961 / 0.946).
  - So the fuzzy-vs-hard verdict (FCM vs KMeans) flips with R. **The init ranking is fragile and
    largely a capacity effect.** On the validation split, KMeans R = 5 is clearly worse and unstable
    (0.935 ± 0.038), while R = 10 ≈ R = 20 (0.961).
- **Stacking evens out the inits.** With the augmented ANFIS, KMeans/SC/FCM all land at 0.985–0.987
  (multi) and 0.979–0.984 (binary). Random+stk lags (0.966 multi).
- **Epochs.** 5 epochs (with early stopping, then refit) change macro-F1 by less than the seed noise
  for every init. This supports the paper's statement that extra epochs only add time. Early stopping picks
  1 epoch most often for SC (10 of 25 member fits in A-noID), consistent with a clustering init
  converging fastest. The other inits keep lowering validation MSE without any test-F1 gain.
- **Train time.** FCM initialisation (skfuzzy, 28–42k points) makes ANFIS-FCM 4–6× slower than KMeans/SC
  (8.9 s vs 1.4 / 2.0 s, multiclass).

**Answer to Q2:** a clustering init beats random placement at the paper's rule count. SC is the most
reliable choice because it also chooses a sensible rule count. Differences between the clustering
methods are small, depend on R, and mostly disappear once the stacking ANFIS is added. We do not find
consistent evidence that *fuzzy* clustering (FCM) beats *hard* clustering (KMeans) as an ANFIS initialiser.

### Setting B: the corrected labels are (almost) not learnable
- Every model (classical, MLP, all ANFIS) reaches Imp F1 ≈ 0.79. That equals the reference rule
  "Imp iff CAN ID = 0x164" (0.794 ± 0.018) on the same test sets. The models learn to recognise
  0x164-*type* messages (payload signature) and cannot separate the attacker's 0x164 frames from the
  genuine ECU's.
- The probe confirms it:
  - **Payload:** AUC 0.50 for every model, on the real and the control boundary.
  - **Timing:** a non-linear model (RF) finds a faint fingerprint, AUC 0.59–0.61 vs 0.50 on the
    attack-free control. LR and 1-epoch ANFIS-FCM do not (0.50).
- **Implication for the paper:** its Impersonation results measure "is this frame ID 0x164?". They
  say nothing about detecting an impersonating node. Per-frame detection on OTIDS Impersonation needs
  temporal/sequence features at least. Even then, the available signal is weak.

### Ablations worth citing
- **Paper vs OOF stacking:** OOF is *worse* for KMeans/FCM (FCM+stk −0.024 binary, −0.046 multi) and
  equal for SC. The feared leak of in-sample stacking does not show up. A 10-rule stage-1 ANFIS
  barely overfits, so its training outputs resemble its test outputs, while OOF stage 2 is trained
  on noisier scores than it sees at test time.
- **SMOTE:** removing it breaks the pure fuzzy classifier (−0.14 binary, −0.30 multi), because the
  cluster class-distributions get swamped by Normal. It barely affects RF (−0.002). Unstacked ANFIS
  actually improves without SMOTE (+0.03 for FCM). Stacked ANFIS is about unchanged in binary
  (−0.006 to +0.006) and loses 0.008–0.020 in multiclass.
- **Removing the CAN ID (A → A-noID)** costs RF 0.010. It costs ANFIS 0.016–0.050 unstacked
  (SC least) and 0.012–0.034 stacked, and linear models up to 0.14 (LDA, multiclass). See the last table in `ablations.md`.
