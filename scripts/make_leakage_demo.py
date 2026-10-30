"""Short live demonstration of the label-leakage issue: leakage_demo.ipynb (repo root).

    python scripts/make_leakage_demo.py
"""
from __future__ import annotations

from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "leakage_demo.ipynb"
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

CELLS = [
    md("# Label leakage in Al Isawi et al. (2025): a live demonstration\n\n"
       "Run from the project root (needs the OTIDS logs in `data/raw/`). About one minute."),
    code("import sys, numpy as np, pandas as pd\n"
         "from pathlib import Path\n"
         "sys.path.insert(0, str(Path.cwd()))\n"
         "from sklearn.tree import DecisionTreeClassifier, export_text\n"
         "from sklearn.linear_model import LogisticRegression\n"
         "from sklearn.preprocessing import MinMaxScaler\n"
         "from sklearn.metrics import accuracy_score, f1_score\n"
         "from scipy.stats import chi2_contingency\n"
         "from src.data.build_dataset import load_config, sample_dataset, make_split, _log\n"
         "cfg = load_config()\n"
         "NAMES = {0: 'DoS', 1: 'Impersonation', 2: 'Normal'}"),

    md("## 1. What the paper says (Section III-B, p. 90867)\n\n"
       "> *\"The total number of inputs for all techniques is 10, which are the **CAN ID**, DLC, and the eight "
       "data field values.\"*\n\n"
       "> *\"The class labeling is done **based on the CAN ID** where an ID of '0×164' … corresponds to an "
       "'Impersonation' attack class, an ID of '0×000' corresponds to a 'DOS' attack class, and the rest "
       "corresponds to the 'Normal' or benign class.\"*\n\n"
       "So the label is a fixed function of one of the inputs: **label = f(CAN ID)**.\n\n"
       "**For DoS this labelling is correct:** no real ECU uses 0x000, so every 0x000 frame really is injected "
       "(the ID just makes DoS trivial to detect). **For Impersonation it is not:** 0x164 is a legitimate ID, so "
       "the rule also labels the genuine ECU's frames as attacks. Sections 6–7 show this."),

    md("## 2. In the data: the CAN ID determines the label completely\n\n"
       "A 20,000-frame sample built exactly as the paper describes (seed 0). Each CAN ID group maps to exactly "
       "one class: there are no off-diagonal entries."),
    code("df = sample_dataset('A', seed=0, cfg=cfg)\n"
         "id_group = np.select([df.can_id == 0x000, df.can_id == 0x164], ['ID 0x000', 'ID 0x164'], 'any other ID')\n"
         "pd.crosstab(pd.Series(id_group, name='CAN ID'), df.label.map(NAMES).rename('label'))"),

    md("## 3. A one-line rule on the CAN ID alone is perfect\n\n"
       "No learning and no payload: just `if ID == 0x000 → DoS; elif ID == 0x164 → Imp; else Normal`, applied to "
       "the paper-style test set."),
    code("sp = make_split('A', 'multi', seed=0, cfg=cfg)\n"
         "ids = sp.X_test[:, sp.features.index('can_id')]\n"
         "rule = np.where(ids == 0x000, 0, np.where(ids == 0x164, 1, 2))\n"
         "print(f'rule on CAN ID only: accuracy = {accuracy_score(sp.y_test, rule):.4f}, '\n"
         "      f'macro-F1 = {f1_score(sp.y_test, rule, average=\"macro\"):.4f}  (paper ANFIS: 99.68 % accuracy)')"),

    md("## 4. Any model that can isolate an ID value learns this rule\n\n"
       "A depth-3 decision tree trained on the **CAN ID alone** recovers the labelling rule as its splits. A linear "
       "model on the same single input cannot isolate the middle value 356 (0x164) with one threshold, which "
       "explains the paper's weak LDA/LR baselines."),
    code("Xtr_id = sp.X_train[:, [sp.features.index('can_id')]]\n"
         "Xte_id = sp.X_test[:, [sp.features.index('can_id')]]\n"
         "tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr_id, sp.y_train)\n"
         "print(f'decision tree, CAN ID only: macro-F1 = {f1_score(sp.y_test, tree.predict(Xte_id), average=\"macro\"):.4f}')\n"
         "print(export_text(tree, feature_names=['can_id'], class_names=list(NAMES.values())))\n"
         "sc = MinMaxScaler().fit(Xtr_id)\n"
         "lr = LogisticRegression(max_iter=2000).fit(sc.transform(Xtr_id), sp.y_train)\n"
         "print(f'logistic regression, CAN ID only: macro-F1 = '\n"
         "      f'{f1_score(sp.y_test, lr.predict(sc.transform(Xte_id)), average=\"macro\"):.4f}  (one linear cut cannot isolate ID 356)')"),

    md("## 5. Consequence: almost every model hits the ceiling, and removing the ID shows real differences\n\n"
       "Macro-F1, multiclass, mean over 5 seeds, from the full study (`results/metrics_long.csv`). Setting A uses "
       "the paper's inputs; A-noID removes the CAN ID (and adds inter-arrival time)."),
    code("m = pd.read_csv('results/metrics_long.csv')\n"
         "m = m[(m.metric == 'macro_f1') & (m.variant == 'main') & (m.task == 'multi') & m.setting.isin(['A', 'A-noID'])]\n"
         "t = m.astype({'value': float}).groupby(['model', 'setting']).value.mean().unstack().round(4)\n"
         "t['drop without ID'] = (t['A-noID'] - t['A']).round(4)\n"
         "print('models with macro-F1 >= 0.99 in Setting A:', int((t['A'] >= 0.99).sum()), 'of', len(t))\n"
         "t.sort_values('A', ascending=False)"),

    md("## 6. The rule labels normal driving as an attack\n\n"
       "ID 0x164 is a **legitimate ECU message**: a car under no attack sends it all the time. Applying the paper's "
       "rule to the attack-free log flags all of those frames as 'Impersonation'."),
    code("af = _log('attack_free')\n"
         "n164 = int((af.can_id == 0x164).sum())\n"
         "print(f'attack-free log: {len(af):,} frames, {n164:,} with ID 0x164 = {n164 / len(af):.1%} of a clean drive '\n"
         "      'that the paper\\'s rule would call an attack')"),

    md("## 7. In the impersonation log, attacker and genuine 0x164 frames look the same\n\n"
       "HCRL documents that the attack starts at 250 s. If impersonation were visible in the frames, 0x164 traffic "
       "after 250 s should differ from before. It does not."),
    code("imp = _log('impersonation')\n"
         "s = imp[imp.can_id == 0x164]\n"
         "pre, post = s[s.t_rel < 250], s[s.t_rel >= 250]\n"
         "rate = lambda x, dur: len(x) / dur\n"
         "print(f'0x164 rate: before {rate(pre, 250):.1f} Hz, after {rate(post, imp.t_rel.max() - 250):.1f} Hz')\n"
         "print(f'mean gap:  before {pre.dt_same_id.mean()*1e3:.2f} ms, after {post.dt_same_id.mean()*1e3:.2f} ms')\n"
         "pay = lambda x: x[[f'd{i}' for i in range(8)]].astype(str).agg(' '.join, axis=1)\n"
         "ct = pd.crosstab(pay(s), s.t_rel >= 250)\n"
         "ct = ct[(ct.sum(axis=1) >= 20)]\n"
         "chi2, p, dof, _ = chi2_contingency(ct)\n"
         "print(f'payload patterns before vs after: chi2 = {chi2:.1f}, dof = {dof}, p = {p:.3f}  (p near 1 = same distribution)')\n"
         "from IPython.display import Image\n"
         "Image('results/figures/data_impersonation_0x164.png', width=900)"),

    md("## Conclusion\n\n"
       "1. **In the paper:** the CAN ID is an input *and* the label is defined from the CAN ID (Section III-B).\n"
       "2. **In the data:** the ID alone predicts the label perfectly; a 3-split tree recovers the rule; most "
       "models reach ≥ 0.99, so the ≈ 99.7 % headline does not show that ANFIS is needed.\n"
       "3. **DoS: labels correct, detection trivial.** No real ECU uses 0x000.\n"
       "4. **Impersonation: label leakage.** Genuine 0x164 traffic is labelled as an attack (5.3 % of a normal "
       "drive), and attacker frames are statistically identical to genuine ones, as the dataset's own "
       "documentation says (impersonation cannot be separated by ID). The paper's Impersonation result "
       "measures ID recognition, not attack detection.\n\n"
       "This is why the project's main benchmark (A-noID) removes the CAN ID, and Setting B relabels "
       "impersonation by attack time."),
]


def main():
    nb = nbf.v4.new_notebook()
    nb.cells = CELLS
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    NotebookClient(nb, timeout=900, kernel_name="can-anfis",
                   resources={"metadata": {"path": str(ROOT)}}).execute()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, NB)
    print(f"wrote {NB}")


if __name__ == "__main__":
    main()
