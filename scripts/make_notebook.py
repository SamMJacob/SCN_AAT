"""Bundle the whole project into one Jupyter notebook: CAN_ANFIS_AAT.ipynb (repo root).

Every source file becomes a ``%%writefile`` cell, so the notebook alone recreates the package
byte-for-byte. Later cells run the tests, the data analysis, a one-seed demo experiment and the
report. The full experiment grid (~70 min) sits behind a RUN_FULL flag.

    python scripts/make_notebook.py            # build and execute
    python scripts/make_notebook.py --no-exec  # build only
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "CAN_ANFIS_AAT.ipynb"

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell


def src(path: str):
    text = (ROOT / path).read_text().rstrip("\n")
    return code(f"%%writefile {path}\n{text}\n")


SECTIONS = [
    ("## 2. Configuration\n\nAll hyperparameters, seeds, sample sizes and the four settings. The paper's "
     "values are the defaults.", ["configs/default.yaml"]),
    ("## 3. Data pipeline\n\n- `parse_otids.py`: regex parser for the OTIDS logs (remote frames → bytes −1), "
     "parquet cache.\n- `features.py`: per-frame temporal features (`dt_same_id`, `hamming_prev`) on the full "
     "chronological log, before any sampling.\n- `build_dataset.py`: label pools for settings A / A-noID / B / "
     "B-ID, the 20,000-frame sample per seed, the stratified 80/20 split, the validation split, and train-only "
     "min-max scaling + SMOTE.",
     ["src/__init__.py", "src/data/parse_otids.py", "src/data/features.py", "src/data/build_dataset.py"]),
    ("## 4. Models\n\n### 4.1 ANFIS (hybrid neuro-fuzzy)\n\nFirst-order Takagi–Sugeno ANFIS written from "
     "scratch in PyTorch. Gaussian membership functions, log-space firing strengths, and Jang's hybrid "
     "learning: ridge least squares for the consequents, one Adam pass on centres and widths per epoch.",
     ["src/models/anfis.py"]),
    ("### 4.2 Initial FIS: Random, K-Means, Subtractive Clustering, FCM\n\n`subclust.py` implements Chiu's "
     "subtractive clustering with MATLAB `subclust` semantics. `inits.py` turns each clustering method into "
     "initial centres and widths behind one interface.",
     ["src/models/subclust.py", "src/models/inits.py"]),
    ("### 4.3 Classifier wrappers: OvR ANFIS and the stacking ANFIS\n\nOne ANFIS per class (one-vs-rest); "
     "the stacked variant adds a second ANFIS that takes the stage-1 scores and regresses the class index "
     "(the paper's augmented ANFIS).", ["src/models/anfis_classifiers.py"]),
    ("### 4.4 Non-hybrid baselines\n\nPure fuzzy (FCM classifier: memberships + cluster class distributions, "
     "no learning), pure neural (MLP) and classical models (LDA, LR, linear/RBF SVM, Random Forest), with "
     "the small grids tuned on the validation split.",
     ["src/models/fcm_classifier.py", "src/models/baselines.py"]),
    ("## 5. Evaluation\n\nPer-run metrics (macro-F1 primary), the exact McNemar test, figure helpers, and "
     "the report generator that aggregates `results/metrics_long.csv` into summaries, paired comparisons, "
     "figures and `REPORT_NOTES.md`.",
     ["src/eval/metrics.py", "src/eval/stats.py", "src/eval/plots.py", "src/eval/report.py",
      "src/eval/notes.py"]),
    ("## 6. Experiment scripts\n\n- `run_all.py`: the experiment loop (settings × tasks × seeds × models), one "
     "identical protocol for every model.\n- `data_report.py`: what the OTIDS logs contain (0x164 before vs "
     "after the attack start, DoS injection).\n- `probe_B.py`: can the corrected Impersonation label be learned "
     "per frame?\n- `rule_sweep.py`: ANFIS-KMeans with R ∈ {5, 10, 20}, validation split only.",
     ["scripts/run_all.py", "scripts/data_report.py", "scripts/probe_B.py", "scripts/rule_sweep.py"]),
    ("## 7. Document builders\n\nArchitecture diagrams and the Word reports (`AAT_Report.docx`, "
     "`Architecture.docx`). They are not executed here.",
     ["scripts/make_arch_figures.py", "scripts/make_report_docx.py"]),
    ("## 8. Unit tests\n\nParser, train-only preprocessing, subtractive clustering on synthetic blobs, ANFIS "
     "on sin·cos and XOR, least squares vs numpy, and the initialisers.",
     ["tests/test_data.py", "tests/test_anfis.py"]),
]


SETUP = """import os, sys, platform, subprocess, zipfile
from pathlib import Path

# ---- options --------------------------------------------------------------------------------
DATA_DIR = '/content/drive/MyDrive/OTIDS'   # Colab: folder in Google Drive with the OTIDS .txt logs or zip
REPO_URL = 'https://github.com/SamMJacob/SCN_AAT.git'
RUN_FULL = False                            # True = re-run the full 5-seed grid and all ablations
# ---------------------------------------------------------------------------------------------

IN_COLAB = 'google.colab' in sys.modules
LOGS = ['DoS_attack_dataset.txt', 'Fuzzy_attack_dataset.txt', 'Impersonation_attack_dataset.txt',
        'Attack_free_dataset.txt']

def sh(*cmd):  # run a command and stream its output into the notebook
    p = subprocess.Popen([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        print(line, end='')
    if p.wait():
        raise RuntimeError(f'command failed ({p.returncode}): {cmd}')

# 1. packages missing from Colab
for mod, pkg in [('skfuzzy', 'scikit-fuzzy'), ('imblearn', 'imbalanced-learn'), ('yaml', 'pyyaml'),
                 ('pyarrow', 'pyarrow'), ('pytest', 'pytest')]:
    try:
        __import__(mod)
    except ImportError:
        sh(sys.executable, '-m', 'pip', 'install', '-q', pkg)

# 2. project folder: use the current one if it is the project, else clone the repository
if not (Path.cwd() / 'results' / 'metrics_long.csv').exists():
    target = Path('/content/SCN_AAT') if IN_COLAB else Path.cwd() / 'SCN_AAT'
    if not (target / 'results' / 'metrics_long.csv').exists():
        sh('git', 'clone', '-q', '--depth', '1', REPO_URL, target)
    os.chdir(target)
ROOT = Path.cwd()
for d in ['configs', 'src/data', 'src/models', 'src/eval', 'scripts', 'tests', 'results/figures',
          'data/raw', 'data/processed']:
    (ROOT / d).mkdir(parents=True, exist_ok=True)
for f in ['src/data/__init__.py', 'src/models/__init__.py', 'src/eval/__init__.py',
          'scripts/__init__.py', 'tests/__init__.py']:
    (ROOT / f).touch()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 3. OTIDS data -> data/raw (link the .txt logs, or extract them from the HCRL zip)
raw = ROOT / 'data' / 'raw'
if IN_COLAB and not all((raw / f).exists() for f in LOGS):
    from google.colab import drive
    drive.mount('/content/drive')
src_dir = Path(DATA_DIR)
for f in LOGS:
    if not (raw / f).exists() and (src_dir / f).exists():
        (raw / f).symlink_to(src_dir / f)
if not all((raw / f).exists() for f in LOGS):
    for z in list(src_dir.glob('*.zip')) + list(raw.glob('*.zip')):
        with zipfile.ZipFile(z) as zf:
            for name in zf.namelist():
                if Path(name).name in LOGS and not (raw / Path(name).name).exists():
                    with zf.open(name) as a, open(raw / Path(name).name, 'wb') as b:
                        b.write(a.read())
HAVE_DATA = all((raw / f).exists() for f in LOGS)

import torch, sklearn, numpy, pandas
print('project folder:', ROOT)
print('Python', platform.python_version(), '| torch', torch.__version__, '| sklearn', sklearn.__version__,
      '| CUDA:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'not available')
print('OTIDS data found:', HAVE_DATA, '' if HAVE_DATA else
      f'-> put the four logs (or the HCRL zip) in {DATA_DIR} and re-run this cell; data cells will be skipped')"""

def build() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["language_info"] = {"name": "python"}
    cells = [
        md("# EV CAN-bus attack detection with ANFIS\n\n"
           "**Soft Computing AAT (Hybrid Systems): Sam M Jacob**\n\n"
           "Reproduction and extension of O. A. Al Isawi, K. A. Al Jaafari, A. S. Al-Sumaiti, *Electric Vehicles "
           "CAN Bus Cyber Attacks Detection Using Adaptive Neuro Fuzzy Inference System*, IEEE Access 13 (2025).\n\n"
           "Research questions:\n"
           "1. **Non-hybrid vs hybrid:** MLP (neural), FCM classifier (fuzzy) and LDA/LR/SVM/RF vs ANFIS "
           "(neuro-fuzzy), unstacked and with the paper's stacking ANFIS.\n"
           "2. **Initialisation:** Random vs K-Means vs Subtractive Clustering vs Fuzzy C-Means for building the "
           "initial ANFIS.\n\n"
           "**How this notebook is organised.** Sections 2–8 contain *all* of the project's source code. Each "
           "cell writes one file (`%%writefile`), so running them recreates the package exactly as in the "
           "repository. Sections 9–13 then run it: unit tests, data analysis, a one-seed demo experiment, the "
           "results of the full 5-seed study, and the Setting B probe.\n\n"
           "**Running it (Colab or local).** Run all cells in order. The setup cell:\n"
           "1. installs `scikit-fuzzy` and `imbalanced-learn` if they are missing;\n"
           "2. if it is not already inside the project, clones the repository "
           "(github.com/SamMJacob/SCN_AAT) for the saved results of the full study;\n"
           "3. finds the OTIDS data. On Colab it mounts Google Drive and looks in `DATA_DIR` "
           "(default `MyDrive/OTIDS`) for the four `.txt` logs *or* the original HCRL zip.\n\n"
           "**Data.** The OTIDS CAN-intrusion dataset (HCRL, Korea University) must be downloaded manually "
           "(https://ocslab.hksecurity.net/Dataset/CAN-intrusion-dataset) and put in Google Drive (Colab) or "
           "`data/raw/` (local). Without it, the code, unit tests and saved results still run; the data-dependent "
           "cells are skipped with a message.\n\n"
           "**Runtime.** Setup, tests, data analysis and the demo take about 5 minutes on Colab (CPU is enough). "
           "The full grid (`RUN_FULL = True`) takes about 70 minutes on a 20-core CPU + GPU, and several hours on "
           "a Colab CPU runtime; use *Runtime → Change runtime type → GPU* for the ANFIS parts."),
        md("## 1. Setup"),
        code(SETUP),
    ]
    for text, files in SECTIONS:
        cells.append(md(text))
        cells.extend(src(f) for f in files)

    cells += [
        md("## 9. Run the unit tests"),
        code("sh(sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests')"),
        md("## 10. Data analysis\n\nParses the logs (cached after the first run) and checks whether the "
           "attacks are visible in the frames. Writes `results/data_report.md` and two figures."),
        code("from IPython.display import Image, Markdown, display\n"
             "if HAVE_DATA:\n"
             "    sh(sys.executable, 'scripts/data_report.py')\n"
             "else:\n"
             "    print('No OTIDS data: showing the saved data report.')\n"
             "display(Markdown((ROOT / 'results/data_report.md').read_text().split('### Per-ID rates')[0]))\n"
             "display(Image(str(ROOT / 'results/figures/data_impersonation_0x164.png'), width=900))"),
        md("## 11. Demo experiment (one seed)\n\nAll 15 model rows on the main benchmark (Setting A-noID, "
           "multiclass, seed 0) under the shared protocol. Results go to a separate file under the `demo` tag, so the "
           "saved 5-seed results are untouched; they should match the seed-0 rows of the full study exactly. "
           "Takes about 1 minute."),
        code("import pandas as pd\n"
             "demo_csv = ROOT / 'results/notebook_demo.csv'\n"
             "if HAVE_DATA:\n"
             "    demo_csv.unlink(missing_ok=True)\n"
             "    sh(sys.executable, 'scripts/run_all.py', '--setting', 'A-noID', '--task', 'multi', '--seed-list', '0',\n"
             "       '--tag', 'demo', '--out', demo_csv)\n"
             "else:\n"
             "    print('No OTIDS data: demo skipped.')"),
        code("if demo_csv.exists():\n"
             "    demo = pd.read_csv(demo_csv)\n"
             "    demo = demo[demo.metric != 'params'].astype({'value': float})\n"
             "    display(demo.pivot_table(index='model', columns='metric', values='value')\n"
             "            [['macro_f1', 'accuracy', 'f1_DoS', 'f1_Imp', 'f1_Normal', 'n_rules', 'train_time_s']]\n"
             "            .sort_values('macro_f1', ascending=False).round(4))"),
        md("## 12. Full study (5 seeds, all settings, ablations)\n\nThese are the exact commands behind every "
           "reported number. With `RUN_FULL = False` the saved `results/metrics_long.csv` is used instead."),
        code("FULL = [\n"
             "    '--setting A A-noID B B-ID --task binary multi --seeds 5',\n"
             "    '--setting A A-noID B --task binary multi --models ANFIS-Random ANFIS-KMeans ANFIS-SC ANFIS-FCM --epochs 5 --tag ep5',\n"
             "    '--setting A A-noID --task binary multi --models ANFIS-SC ANFIS-FCM ANFIS-KMeans --stack-mode oof --tag oof',\n"
             "    '--setting A-noID --task binary multi --no-smote --tag nosmote',\n"
             "    '--setting A-noID --task binary multi --models ANFIS-Random ANFIS-KMeans ANFIS-FCM --n-rules 20 --tag R20',\n"
             "]\n"
             "if RUN_FULL and HAVE_DATA:\n"
             "    for args in FULL:\n"
             "        sh(sys.executable, 'scripts/run_all.py', *args.split())\n"
             "    sh(sys.executable, 'scripts/rule_sweep.py')\n"
             "    sh(sys.executable, 'scripts/probe_B.py')\n"
             "else:\n"
             "    print('Using the saved results/metrics_long.csv (set RUN_FULL = True in the setup cell to re-run;'\n"
             "          ' needs the OTIDS data).')"),
        md("### 12.1 Generate tables, comparisons and figures"),
        code("if HAVE_DATA:\n"
             "    sh(sys.executable, '-m', 'src.eval.report')\n"
             "else:\n"
             "    print('No OTIDS data: using the saved tables and figures (the report step re-reads the logs '\n"
             "          'for one reference baseline).')"),
        md("### 12.2 Main benchmark (A-noID): all models, mean ± std over 5 seeds"),
        code("m = pd.read_csv(ROOT / 'results/metrics_long.csv')\n"
             "m = m[m.metric != 'params'].astype({'value': float})\n\n"
             "def summary(setting, task, metrics=('macro_f1', 'accuracy')):\n"
             "    s = m.query('setting == @setting and task == @task and variant == \"main\"')\n"
             "    g = s[s.metric.isin(metrics)].groupby(['model', 'metric']).value.agg(['mean', 'std']).unstack()\n"
             "    g.columns = [f'{a}_{b}' for b, a in g.columns]\n"
             "    return g.sort_values(g.columns[0], ascending=False).round(4)\n\n"
             "summary('A-noID', 'multi', ('macro_f1', 'f1_Imp', 'f1_DoS'))"),
        code("summary('A-noID', 'binary', ('macro_f1', 'f1_Attack'))"),
        md("### 12.3 Comparison 1: non-hybrid vs hybrid"),
        code("display(Markdown((ROOT / 'results/comparison1_nonhybrid_vs_hybrid_A-noID_multi.md').read_text()))\n"
             "display(Image(str(ROOT / 'results/figures/comparison1_A-noID_multi.png'), width=800))\n"
             "display(Image(str(ROOT / 'results/figures/confusion_A-noID_multi.png'), width=650))"),
        md("### 12.4 Comparison 2: clustering initialisation"),
        code("display(Markdown((ROOT / 'results/comparison2_clustering_A-noID_multi.md').read_text()))\n"
             "display(Image(str(ROOT / 'results/figures/comparison2_A-noID_multi.png'), width=1000))\n"
             "display(Image(str(ROOT / 'results/figures/mf_overlay_A-noID_multi.png'), width=1000))"),
        md("### 12.5 Reproduction check (Setting A) and the model ladder across settings"),
        code("display(Image(str(ROOT / 'results/figures/ladder_multi.png'), width=1000))\n"
             "summary('A', 'multi')"),
        md("## 13. Setting B: is the real Impersonation attack learnable?"),
        code("display(Markdown((ROOT / 'results/probe_B.md').read_text()))\n"
             "summary('B', 'multi', ('macro_f1', 'f1_Imp'))"),
        md("## 14. Conclusions\n\n"
           "- **Setting A reproduces the paper** (ANFIS-FCM+stk 99.99 % / 100 % accuracy), but the label is a "
           "function of the CAN ID input, so almost every non-linear model hits the ceiling.\n"
           "- **Q1 (A-noID):** Random Forest is the best model. The hybrid ANFIS clearly beats its pure-fuzzy "
           "ingredient (+0.036 / +0.101 macro-F1 over the FCM classifier) and is better than or equal to the MLP, "
           "with a small, interpretable rule base.\n"
           "- **Q2:** a clustering initialisation beats random placement at the paper's rule count, and SC is the "
           "most reliable because it sizes the rule base itself. Differences between clustering methods depend "
           "on the rule count and largely disappear after stacking; fuzzy (FCM) does not consistently beat "
           "hard (K-Means) clustering.\n"
           "- **Setting B:** genuine and impersonated 0x164 frames are indistinguishable per frame (probe AUC ≈ "
           "0.5 on payload), so the paper's Impersonation result measures ID recognition.\n\n"
           "Full discussion: `results/REPORT_NOTES.md` and `results/AAT_Report.docx`."),
    ]
    nb.cells = cells
    return nb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-exec", action="store_true")
    ap.add_argument("--kernel", default="can-anfis", help="kernel used to execute the notebook")
    ap.add_argument("--cwd", default=str(ROOT), help="folder to execute in (a fresh one tests the clone path)")
    ap.add_argument("--out", default=str(NB))
    args = ap.parse_args()
    nb = build()
    if not args.no_exec:
        from nbclient import NotebookClient
        NotebookClient(nb, timeout=1800, kernel_name=args.kernel,
                       resources={"metadata": {"path": args.cwd}}).execute()
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, args.out)
    print(f"wrote {args.out} ({len(nb.cells)} cells)")


if __name__ == "__main__":
    sys.exit(main())
