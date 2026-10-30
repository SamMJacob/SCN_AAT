"""Spoken walkthrough for presenting the project: results/Talk_Script.docx (+ Desktop copy).

    python scripts/make_talk_script.py
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_report_docx import GREY, NAVY, RES, Report, save_both  # noqa: E402

OUT = RES / "Talk_Script.docx"

# (heading, minutes, what to show, [spoken paragraphs])
PARTS = [
    ("1. Opening", "0:30", "Title page of AAT_Report.docx",
     ["My project reproduces and extends an IEEE Access 2025 paper by Al Isawi and colleagues, which uses "
      "ANFIS, an adaptive neuro-fuzzy inference system, to detect cyber-attacks on the CAN bus of electric "
      "vehicles. I will cover four things: what I took from the paper, what problems I identified in it and "
      "how I improved on them, the other methods I tested, and my results."]),

    ("Part A · What I took from the paper", "", "", []),
    ("2. The dataset: OTIDS", "2:00", "Report Table 1 (the four logs), then a few raw lines of a log file",
     ["The paper uses OTIDS, a public in-vehicle intrusion dataset from the Hacking and Countermeasure Research "
      "Lab at Korea University. It accompanies Lee, Jeong and Kim's 2017 paper on detecting intrusions using "
      "remote frames. The traffic was recorded from a real car, a KIA Soul, through its OBD-II port.",
      "Every line of the logs is one CAN frame: a timestamp, the CAN ID, a flag saying whether it is a normal data "
      "frame or a remote frame, the data length (DLC), and up to eight data bytes. The CAN ID is the 11-bit "
      "identifier at the start of every CAN message. It names the message type, for example wheel speed, not "
      "the sender, and it also sets priority: the lower the ID, the higher the priority. A remote frame is a "
      "request asking an ECU to send its data. CAN has no authentication, so any node can send any ID.",
      "There are four recordings. The attack-free log is normal driving: 2.37 million frames over about 17 "
      "minutes, from 45 different IDs. The DoS log, 657,000 frames, has an attacker flooding the bus with ID "
      "0x000, the highest possible priority, so legitimate frames are delayed. About half of that log, 336,000 "
      "frames, is injected 0x000 traffic: all-zero payloads, sent in bursts about half a millisecond apart, mixed "
      "with the car's normal traffic. The fuzzy log injects random IDs and payloads; neither the paper nor I "
      "used it. In the impersonation log, about a million frames, the ECU that sends ID 0x164 is taken offline "
      "and an attacker sends 0x164 in its place. According to the dataset documentation, the attack starts 250 "
      "seconds into the recording.",
      "The two attacks behave very differently. For DoS, the ID is a reliable marker: no real ECU uses 0x000, so "
      "labelling every 0x000 frame as an attack is the standard approach, and it is correct. For "
      "impersonation, the attacker uses a legitimate ID with legitimate-looking payloads. The dataset's own "
      "authors detect it from timing, how an ECU's responses to remote frames are delayed and spaced, not from "
      "the ID or payload. I confirmed this in the data: 0x164 traffic before and after the attack starts has the "
      "same rate, the same payload patterns and almost the same timing. And ID 0x164 is ordinary traffic: it "
      "makes up 5.3 % of the attack-free drive.",
      "The paper samples 20,000 frames: 1,497 DoS, 979 impersonation and 17,524 normal. It does not say which "
      "files these came from, and those proportions do not match any log's natural mix, so I documented my "
      "choice. DoS frames come from the DoS log, impersonation frames from the impersonation log, and normal "
      "frames from the attack-free log, excluding IDs 0x000 and 0x164 so that the paper's labelling rule stays "
      "consistent. I also computed a timing feature on the full chronological logs before sampling: the time "
      "since the previous frame with the same ID."]),

    ("3. The paper's method, which I kept", "1:30", "Report Section 3 and the Architecture.docx ANFIS diagram",
     ["From the paper I kept the whole core method so that the reproduction is faithful.",
      "The data setup: the same 20,000-frame sample size with the paper's exact class "
      "sizes (1,497 DoS, 979 impersonation, 17,524 normal), the same 80/20 split, and the same ten input "
      "features: CAN ID, data length and the eight payload bytes.",
      "The preprocessing: min-max scaling and SMOTE oversampling with k = 30.",
      "The model: a first-order Sugeno ANFIS with Gaussian membership functions, trained with Jang's hybrid "
      "learning, where least squares solves the consequents and gradient descent tunes the membership "
      "functions. I kept the paper's two initialisations, subtractive clustering with its radius and squash "
      "values and fuzzy c-means with 10 clusters, one training epoch, and the paper's architecture: one "
      "ANFIS per class followed by a second 'augmented' stacking ANFIS.",
      "The tasks and baselines: binary and multiclass detection, the same metrics, and the paper's classical "
      "baselines (LDA, logistic regression, SVM and Random Forest).",
      "I re-implemented all of this from scratch in Python and PyTorch, because the paper used MATLAB and "
      "no code accompanies the paper."]),

    ("Part B · What I identified and how I improved it", "", "", []),
    ("4. Problems I identified in the paper", "1:30", "The paper, Section III-B (p. 90867), then leakage_demo.ipynb",
     ["Before running models I checked whether the labels match something visible in the data. That "
      "check found the main problems.",
      "The paper says on page 90867 that the CAN ID is one of the ten inputs, and in the same paragraph that "
      "the classes are labelled from the CAN ID: 0x000 is DoS, 0x164 is impersonation, everything else is normal.",
      "For DoS that is fine. No real ECU uses 0x000, so the labels are correct. The ID simply makes DoS "
      "detection trivial, so a high DoS score does not show that ANFIS is needed.",
      "For impersonation it is a real fault. 0x164 is a legitimate ID, so the rule also labels the genuine ECU's "
      "frames as attacks, including 5.3 % of a normal, attack-free drive. And because the ID is also an input, "
      "the impersonation class reduces to 'is the ID 0x164?'. That is label leakage. The dataset's own "
      "documentation says impersonation cannot be separated by ID, and in the data the attacker's frames are "
      "statistically identical to the genuine ones: the same rate (119 Hz), the same payload patterns "
      "(chi-squared p = 0.999) and the same bus load.",
      "Second, the evaluation protocol. The paper describes no validation split, so it is unclear whether "
      "hyperparameters were tuned on the test data. It reports a single train/test split with no variance "
      "or significance tests, and its weak linear baselines look under-tuned. It also only "
      "compares the two clustering initialisations with each other, with no random or hard-clustering "
      "control."]),
    ("5. My improvements", "1:30", "Report Table 2 (settings) and Section 3.2 (protocol)",
     ["I addressed each problem.",
      "For label leakage I created a new main benchmark, A-noID. It keeps the paper's labels but removes the "
      "CAN ID and adds a timing feature, the log of the time since the previous frame with the same ID. "
      "Models then have to recognise attacks from payload and timing, which is a real pattern-recognition "
      "task. I still run the paper's original setting, A, to show the reproduction.",
      "For the invisible attack I added Setting B, which labels only frames sent after the attack starts as "
      "impersonation, and B-ID, the same with the CAN ID. I also ran a learnability probe with a control on "
      "attack-free data, to measure whether the real attack can be detected at all.",
      "For the protocol: tuning happens only on a validation split, never the test set. Every experiment is "
      "repeated over five seeds and reported as mean ± standard deviation. Models are compared on paired "
      "seeds, with an exact McNemar test. Scaling and SMOTE are fitted on the training data only. The "
      "headline hybrid was fixed in advance, so I could not pick the best-looking one afterwards.",
      "Finally, I added methods that let me answer two clean questions about hybrid systems, which I "
      "describe next."]),

    ("Part C · The other methods I tested", "", "", []),
    ("6. Methods beyond the paper", "1:15", "Architecture.docx, baselines and initialisation tables",
     ["Question 1 is whether the hybrid beats non-hybrid methods. Besides the paper's classical baselines I "
      "added the two ingredients of ANFIS on their own. One is a pure neural network, an MLP. The other is a "
      "pure fuzzy classifier built from fuzzy c-means memberships, with no learning at all. Comparing ANFIS "
      "with these two shows what the neural learning adds and what the fuzzy rules add. All baselines are "
      "tuned on validation.",
      "Question 2 is how much the initialisation matters. Besides the paper's subtractive clustering and fuzzy "
      "c-means, I added random initialisation as a control and K-Means as hard clustering. K-Means versus "
      "fuzzy c-means isolates the value of fuzzy memberships. Every initialisation is tested with and "
      "without the stacking ANFIS.",
      "I also ran ablations on the paper's design choices: in-sample versus out-of-fold stacking, 1 versus "
      "5 epochs, with and without SMOTE, and 10 versus 20 rules. In total that is 15 model variants, four "
      "settings, two tasks and five seeds, plus the ablations."]),

    ("Part D · Results", "", "", []),
    ("7. Reproduction (Setting A)", "0:45", "Report Table 4 and the ladder figure",
     ["The reproduction worked. My stacked ANFIS-FCM reaches 99.99 % accuracy in binary and 100 % in "
      "multiclass, against the paper's 99.68 %.",
      "But this confirms the leakage: 11 of 15 models score at least 0.99 macro-F1. Logistic regression tuned "
      "on validation reaches 0.996, where the paper reports 0.87. So the paper's headline shows the task is "
      "easy when the ID is available, not that ANFIS is needed."]),
    ("8. Question 1: hybrid vs non-hybrid (A-noID)", "1:30", "Report Tables 5–8 and the comparison-1 figure",
     ["On the fair benchmark, the best model is the Random Forest, with macro-F1 0.990 binary and 0.989 "
      "multiclass. The pre-chosen hybrid, stacked ANFIS-FCM, scores 0.979 and 0.985. That is significantly "
      "worse in binary (McNemar p around 10 to the minus 7) and statistically tied in multiclass.",
      "Against its own ingredients, the hybrid wins clearly. It beats the pure fuzzy classifier by 0.036 and "
      "0.101 macro-F1, on all five seeds, which is the largest single improvement in the study. It beats the "
      "MLP by 0.019 in binary and ties it in multiclass, with a much smaller and readable rule base.",
      "The remaining errors are almost all normal frames with an all-zero payload mistaken for DoS. Without "
      "the ID, only timing separates them.",
      "Answer to question 1: hybridisation clearly helps compared with pure fuzzy and pure neural models, but "
      "it does not beat a strong ensemble like Random Forest."]),
    ("9. Question 2: initialisation", "1:15", "Report Tables 9–10 and the comparison-2 / membership-function figures",
     ["At the paper's 10 rules per model, subtractive clustering is the best initialisation (0.984 / 0.983) "
      "and beats random initialisation on all five seeds.",
      "But subtractive clustering chooses more rules itself (43 to 50 in total, against 20 to 30). With 20 "
      "rules each, fuzzy c-means rises to 0.971 / 0.982 and random to 0.977 / 0.967, and the ranking between "
      "fuzzy c-means and K-Means flips. With the stacking ANFIS, all clustering methods end up level. Five "
      "epochs gave no gain, as the paper said, and fuzzy c-means initialisation is four to six times slower.",
      "Answer to question 2: clustering beats random initialisation, and subtractive clustering is the safest "
      "choice because it sizes the rule base itself. But fuzzy clustering does not consistently beat hard "
      "clustering."]),
    ("10. Setting B: real impersonation", "0:45", "Report Table 11 (learnability probe)",
     ["With honest labels, every model reaches impersonation F1 of about 0.79, which is exactly what the "
      "trivial rule 'flag every 0x164 frame' gets (0.794). The probe gives AUC 0.50, chance level, on payload. "
      "On timing, a Random Forest finds only a faint signal (about 0.6). So the paper's impersonation result "
      "measures ID recognition, not attack detection."]),
    ("11. Ablations", "0:30", "Report Table 12",
     ["Out-of-fold stacking was worse than the paper's in-sample stacking. SMOTE is essential for the pure "
      "fuzzy classifier (which drops by 0.14 to 0.30 without it) but hardly matters for Random Forest. "
      "Removing the CAN ID costs Random Forest only 0.01, but costs linear models up to 0.14."]),

    ("Wrap-up", "", "", []),
    ("12. What I am submitting", "0:45", "GitHub repo and the notebook",
     ["Everything is on GitHub. The Jupyter notebook contains all of the code, one file per cell, plus 13 "
      "unit tests, a one-seed demo and all the results. It runs on Colab, and the demo reproduces the saved "
      "results exactly. There is also the written report and an architecture document describing every "
      "method in detail."]),
    ("13. Limitations", "0:30", "Report Section 6",
     ["Five seeds give limited statistical power, so 'within noise' is a practical threshold rather than a "
      "formal test. I did not re-run the paper's deep-learning baselines. Training times come from one "
      "machine. And where the paper's description was ambiguous, such as how the stacking ANFIS outputs a "
      "class, I state my interpretation."]),
    ("14. Close", "0:20", "–",
     ["In short: I kept the paper's method and reproduced its result, but identified that the result comes "
      "from label leakage through the CAN ID. On a fair benchmark, ANFIS clearly improves on pure fuzzy and "
      "pure neural models but not on Random Forest; clustering initialisation matters less than rule count; "
      "and the impersonation attack in this dataset cannot be detected per frame. Happy to go into any part "
      "in more detail."]),
]

QA = [
    ("Why is Random Forest better than ANFIS?",
     "The remaining errors need sharp, non-linear cuts on a few byte values and on timing. Trees make those "
     "cuts directly, while ANFIS with 10 smooth Gaussian rules per class approximates them. ANFIS's "
     "advantage is a small, readable rule base, not raw accuracy."),
    ("Isn't removing the CAN ID changing the paper's task?",
     "I kept the paper's labels exactly. Setting A reproduces the paper unchanged. A-noID only removes the "
     "feature that is the label, which is the minimum change that turns the task into real pattern "
     "recognition. Both are reported."),
    ("What exactly is hybrid learning in ANFIS?",
     "Each epoch has two steps. With the membership functions fixed, the output is linear in the consequent "
     "parameters, so they are solved exactly by least squares. Then, with the consequents fixed, gradient "
     "descent (Adam) updates the centres and widths of the membership functions."),
    ("Why does stacking sometimes lower impersonation F1?",
     "The stacking ANFIS regresses the class index (DoS 0, Imp 1, Normal 2) and rounds it. Imp is in the "
     "middle, so a DoS or Normal frame whose prediction drifts by about half a class lands on Imp."),
    ("Isn't subtractive clustering only better because it has more rules?",
     "Partly, yes, and I tested that directly: with 20 rules the other methods close most of the gap. That "
     "is why I conclude SC is the most reliable choice, not that it is intrinsically better."),
    ("How do you know you didn't tune on the test set?",
     "All tuning uses a validation split carved from the training data before SMOTE, and ANFIS uses the "
     "paper's hyperparameters unchanged. The headline hybrid was fixed in advance. The 'best ANFIS' column "
     "is chosen on test and is labelled as post hoc and optimistic."),
    ("Why apply SMOTE only to the training data?",
     "Synthetic samples in the test set would make the evaluation unrealistic and leak information. The "
     "test set stays exactly as sampled; a unit test checks this."),
    ("What does 'within noise' mean?",
     "Two models are compared on the same five seeds. If the mean paired difference is no larger than its "
     "standard deviation, or smaller than 0.0025 (about one impersonation test error), I call it within "
     "noise. For one seed I also run an exact McNemar test."),
    ("Why didn't you re-run the CNN/LSTM baselines?",
     "They were out of scope for a hybrid-systems comparison and the time budget. Their numbers from the "
     "paper are quoted, and this is listed as a limitation."),
    ("Is the paper wrong about DoS too?",
     "No. Labelling 0x000 as DoS is correct, because no real ECU uses that ID, and DoS stays learnable without "
     "the ID (DoS F1 about 0.97 on A-noID). The problem is only that the ID makes DoS trivial. The real fault is "
     "impersonation, where a legitimate ID is used as the label."),
    ("Why didn't you use the fuzzy attack log?",
     "The paper does not use it, so it is outside the reproduction. Fuzzy attacks inject random IDs that can "
     "overlap real ones, so the same ID-based labelling would not work for it either."),
    ("Does OTIDS's own detection method help here?",
     "It supports my finding. The OTIDS authors detect impersonation from remote-frame response timing, not "
     "from IDs or payloads. The paper uses no timing at all. My simpler timing feature found only a faint "
     "signal; a remote-frame response analysis would be the natural next step."),
    ("Can I run it myself?",
     "Yes. Open the notebook in Colab and put the OTIDS zip in a Google Drive folder called OTIDS. The basic "
     "run takes about 5 minutes; the full study is one flag and takes several hours on a Colab CPU."),
    ("What tools did you use to build this?",
     "[Answer honestly, in line with your course's policy on AI assistance. For example: Python, PyTorch, "
     "scikit-learn and scikit-fuzzy, plus any coding assistants you used and what you used them for.]"),
]


def build():
    R = Report()
    d = R.doc
    t = R.p("Project Walkthrough: Talk Script", align=WD_ALIGN_PARAGRAPH.CENTER)
    t.runs[0].font.size, t.runs[0].bold, t.runs[0].font.color.rgb = Pt(20), True, NAVY
    s = R.p("EV CAN-bus attack detection with ANFIS: Soft Computing AAT (Hybrid Systems)",
            align=WD_ALIGN_PARAGRAPH.CENTER)
    s.runs[0].font.color.rgb = GREY
    R.p(f"Sam M Jacob · {date.today().strftime('%d %B %Y')}", align=WD_ALIGN_PARAGRAPH.CENTER)
    R.callout("How to use this.",
              "About 15 minutes if read in full, in four parts: (A) what I took from the paper, (B) what I "
              "identified and improved, (C) the other methods I tested, (D) the results. Grey lines say what "
              "to have on screen. If short on time, cut sections 11 and 13 first. A paper-vs-project table, "
              "likely questions and key numbers are at the end.")

    for head, mins, show, paras in PARTS:
        if not mins:                       # part divider
            R.h(head, 1)
            continue
        R.h(f"{head}  ({mins})", 2)
        cue = R.p(f"Show: {show}", italic=True)
        cue.runs[0].font.color.rgb = GREY
        cue.runs[0].font.size = Pt(9.5)
        for text in paras:
            R.p(text)

    R.page_break()
    R.h("At a glance: the paper vs this project", 1)
    R.table([
        ["Aspect", "Paper (kept)", "This project (identified / improved / added)"],
        ["Data", "OTIDS; 20k frames, 1497/979/17524; 80/20 split", "Same; found DoS genuine, impersonation "
         "invisible in the frames"],
        ["Labels", "By CAN ID", "Kept (A, A-noID); added honest attack-time labels (B, B-ID)"],
        ["Inputs", "CAN ID, DLC, 8 payload bytes", "Kept (A); A-noID removes the label-leaking ID and adds "
         "log inter-arrival time"],
        ["Preprocessing", "Min-max, SMOTE k = 30", "Same, fitted on training data only"],
        ["ANFIS", "Sugeno, Gaussian MFs, hybrid learning, 1 epoch", "Same, from scratch in PyTorch"],
        ["Initialisation", "Subtractive clustering, FCM", "Added Random (control) and K-Means (hard "
         "clustering); 10 vs 20 rules"],
        ["Architecture", "OvR ANFIS + stacking ANFIS", "Same; reported with and without stacking; "
         "out-of-fold stacking ablation"],
        ["Baselines", "LDA, LR, SVM, RF (binary); CNN/LSTM/GRU (multi)", "Classical ones tuned on validation; "
         "added MLP (pure neural) and FCM classifier (pure fuzzy); DL quoted only"],
        ["Tuning", "No validation split described", "Validation split only; test set never used for choices"],
        ["Statistics", "Single run", "5 seeds, mean ± std, paired comparisons, McNemar"],
        ["Headline", "≈ 99.7 % accuracy", "Reproduced (99.99 % / 100 %), shown to come from the CAN ID"],
    ], None, col_widths=[2.8, 5.6, 8.1], font=8.5, bold_first_col=True)

    R.h("Likely questions and answers", 1)
    for q, a in QA:
        qp = R.p(f"Q: {q}")
        qp.runs[0].bold = True
        qp.paragraph_format.space_after = Pt(2)
        qp.paragraph_format.keep_with_next = True
        R.p(f"A: {a}")

    R.h("Key numbers at a glance", 1)
    R.table([
        ["Result", "Number"],
        ["Setting A, ANFIS-FCM+stk accuracy (paper 99.68 %)", "99.99 % binary / 100 % multi"],
        ["Setting A, models with macro-F1 ≥ 0.99 (multi)", "11 of 15"],
        ["A-noID best model: Random Forest (macro-F1)", "0.990 binary / 0.989 multi"],
        ["A-noID ANFIS-FCM+stk (macro-F1)", "0.979 binary / 0.985 multi"],
        ["Hybrid gain over pure fuzzy FCM classifier", "+0.036 binary / +0.101 multi (5/5 seeds)"],
        ["Hybrid vs MLP", "+0.019 binary / tied multi"],
        ["Best init at R = 10: subtractive clustering", "0.984 / 0.983, beats Random 5/5 seeds"],
        ["Setting B impersonation F1 (rule 'ID = 0x164': 0.794)", "≈ 0.79 for every model"],
        ["Probe AUC, attacker vs genuine 0x164 (payload / timing)", "0.50 / ≈ 0.6 (control 0.50)"],
    ], None, col_widths=[10, 6.5], font=9)
    save_both(R, OUT)


if __name__ == "__main__":
    build()
