"""Architecture diagrams for docs/ARCHITECTURE.md and the Word report.

Writes results/figures/arch_pipeline.png, arch_anfis.png, arch_stacking.png.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.eval.plots import AQUA, BLUE, GRID, ORANGE, SURFACE, TEXT, TEXT2  # noqa: E402

FIG = Path(__file__).resolve().parents[1] / "results" / "figures"
TINT = {BLUE: "#e3eefb", ORANGE: "#fde9e1", AQUA: "#dcf3ea", TEXT2: "#efeeeb"}


def box(ax, x, y, w, h, title, body="", color=TEXT2, fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=TINT[color], ec=color, lw=1.4))
    ty = y + h - 0.17 if body else y + h / 2
    ax.text(x + w / 2, ty, title, ha="center", va="center" if not body else "top",
            fontsize=fs, fontweight="bold", color=TEXT)
    if body:
        ax.text(x + w / 2, y + h - 0.42, body, ha="center", va="top", fontsize=fs - 1.3,
                color=TEXT2, linespacing=1.35)


def arrow(ax, p, q, color=TEXT2, style="-|>", rad=0.0, lw=1.2, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls,
                                 shrinkA=2, shrinkB=2))


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


# --------------------------------------------------------------------------- pipeline
def pipeline():
    fig, ax = canvas(13, 6.0)
    W, H = 2.25, 1.1
    xs = [0.3, 2.85, 5.4, 7.95, 10.5]
    y1, y2 = 4.35, 2.45
    row1 = [
        ("Raw OTIDS logs", "4 text files\nDoS · Fuzzy · Imp. ·\nAttack-free (4.6 M lines)"),
        ("Parser", "regex per line, remote\nframes → bytes = −1\nparquet cache"),
        ("Temporal features", "full chronological log:\ndt_same_id → log_dt\nhamming_prev"),
        ("Label pools", "settings A / A-noID\n(by ID) and B / B-ID\n(by attack time)"),
        ("Sample per seed", "20,000 frames\n1497 DoS / 979 Imp /\n17524 Normal"),
    ]
    for x, (t, b) in zip(xs, row1):
        box(ax, x, y1, W, H, t, b)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + W, y1 + H / 2), (b, y1 + H / 2))

    row2 = [
        ("Stratified split", "80 % train / 20 % test\n(stratified on 3-class\nlabel, seed-specific)", TEXT2),
        ("Validation split", "20 % of train, pre-SMOTE\nhyperparameter / epoch\nselection only", TEXT2),
        ("Preprocess (train only)", "MinMax fit on train\nSMOTE k = 30 on train\ntest only transformed", TEXT2),
        ("Fit model", "7 non-hybrid baselines\n4 ANFIS inits ×\n(OvR, +stacking)", BLUE),
        ("Evaluate on test", "40 metrics, preds .npz\n→ metrics_long.csv", TEXT2),
    ]
    for x, (t, b, c) in zip(xs[::-1], row2):
        box(ax, x, y2, W, H, t, b, c)
    arrow(ax, (xs[4] + W / 2, y1), (xs[4] + W / 2, y2 + H))
    for a, b in zip(xs[::-1], xs[::-1][1:]):
        arrow(ax, (a, y2 + H / 2), (b + W, y2 + H / 2))
    # the test set bypasses validation & SMOTE
    arrow(ax, (xs[4] + 0.5, y2), (xs[0] + W - 0.5, y2), rad=-0.12, ls=(0, (4, 3)))
    ax.text((xs[4] + xs[0] + W) / 2, 1.08, "test set: scaled with the train-fitted scaler, never "
            "resampled or used for tuning", ha="center", fontsize=8, color=TEXT2, style="italic")

    box(ax, xs[0], 0.15, 12.45, 0.62, "Reporting:  src.eval.report (summaries, paired comparisons, "
        "McNemar, figures, REPORT_NOTES.md)  →  make_report_docx.py (Word report)", color=TEXT2, fs=8.5)
    arrow(ax, (xs[0] + W / 2, y2), (xs[0] + W / 2, 0.77))
    ax.text(0.3, 5.7, "End-to-end pipeline (scripts/run_all.py), repeated for every setting × task × "
            "seed", fontsize=11, fontweight="bold", color=TEXT)
    fig.savefig(FIG / "arch_pipeline.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


# --------------------------------------------------------------------------- ANFIS network
def anfis():
    fig, ax = canvas(12, 6.4)
    L = [0.8, 2.9, 5.0, 7.0, 9.0, 11.0]
    ins = [4.6, 3.2, 1.8]
    mfs = [5.2, 4.6, 4.0, 3.2, 2.6, 2.0, 1.4, 0.8]
    rules = [4.4, 3.2, 2.0]
    r = 0.26

    def node(x, y, label, color=TEXT2, square=False):
        if square:
            ax.add_patch(FancyBboxPatch((x - r, y - r), 2 * r, 2 * r, boxstyle="round,pad=0.0,rounding_size=0.05",
                                        fc=TINT[color], ec=color, lw=1.3, zorder=3))
        else:
            ax.add_patch(Circle((x, y), r, fc=TINT[color], ec=color, lw=1.3, zorder=3))
        ax.text(x, y, label, ha="center", va="center", fontsize=8, color=TEXT, zorder=4)

    def line(p, q, color=GRID, lw=0.9):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, zorder=1)

    labels_in = ["x₁", "x₂", "x_d"]
    for y, lab in zip(ins, labels_in):
        node(L[0], y, lab)
    ax.text(L[0], 1.15, "⋮", ha="center", fontsize=12, color=TEXT2)
    # layer 1: Gaussian MFs; show 3 per input-ish (rule-specific MF per input)
    groups = [mfs[0:3], mfs[3:6], mfs[6:8]]
    for gi, (y_in, g) in enumerate(zip(ins, groups)):
        for k, y in enumerate(g):
            node(L[1], y, f"μ", ORANGE, square=True)
            line((L[0] + r, y_in), (L[1] - r, y))
    for k, y in enumerate(rules):
        node(L[2], y, "Π", BLUE)
        for g in groups:
            line((L[1] + r, g[min(k, len(g) - 1)]), (L[2] - r, y))
        node(L[3], y, "N", BLUE)
        for y2 in rules:
            line((L[2] + r, y2), (L[3] - r, y), lw=0.6)
        node(L[4], y, "f_r", AQUA, square=True)
        line((L[3] + r, y), (L[4] - r, y))
    node(L[5], rules[1], "Σ", TEXT2)
    for y in rules:
        line((L[4] + r, y), (L[5] - r, rules[1]))
    # inputs feed consequents
    for y in rules:
        ax.annotate("", (L[4], y - r), (L[4], 0.55), arrowprops=dict(arrowstyle="-", color=GRID, lw=0.8, ls=":"))
    ax.text(L[4], 0.35, "x (inputs)", ha="center", fontsize=7.5, color=TEXT2)
    ax.text(L[5] + 0.4, rules[1], "ŷ", fontsize=12, va="center", color=TEXT)

    heads = [("Input", "scaled features\nx ∈ [0,1]^d"),
             ("Layer 1 · fuzzify", "Gaussian MF per rule\nand input: μ_rj(x_j)\nparams c_rj, σ_rj"),
             ("Layer 2 · rule", "firing strength\nw_r = Π_j μ_rj(x_j)\n(log space)"),
             ("Layer 3 · normalise", "w̄_r = w_r / Σ w\n(softmax of log w)"),
             ("Layer 4 · consequent", "f_r = w̄_r (a_r·x + b_r)\nfirst-order Sugeno"),
             ("Layer 5 · output", "ŷ = Σ_r f_r")]
    for x, (t, b) in zip(L, heads):
        ax.text(x, 6.15, t, ha="center", fontsize=8.5, fontweight="bold", color=TEXT)
        ax.text(x, 5.92, b, ha="center", va="top", fontsize=7, color=TEXT2, linespacing=1.3)
    # learning annotations
    ax.add_patch(FancyBboxPatch((L[1] - 0.55, 0.05), 1.1, 0.42, boxstyle="round,pad=0.02",
                                fc=TINT[ORANGE], ec=ORANGE, lw=1))
    ax.text(L[1], 0.26, "premise: Adam (MSE)", ha="center", va="center", fontsize=7, color=TEXT)
    ax.add_patch(FancyBboxPatch((L[4] - 1.25, -0.0), 0.0, 0.0, fc="none", ec="none"))
    ax.text(L[4] + 0.55, 1.25, "consequent:\nridge least squares", ha="left", va="center", fontsize=7,
            color=TEXT, bbox=dict(boxstyle="round,pad=0.25", fc=TINT[AQUA], ec=AQUA, lw=1))
    fig.savefig(FIG / "arch_anfis.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


# --------------------------------------------------------------------------- OvR + stacking
def stacking():
    fig, ax = canvas(12, 5.0)
    box(ax, 0.2, 1.65, 1.7, 1.3, "Input x", "scaled frame\nfeatures (d = 10/11)")
    ys = [3.2, 1.95, 0.7]
    names = ["ANFIS: DoS vs rest", "ANFIS: Imp vs rest", "ANFIS: Normal vs rest"]
    for y, n in zip(ys, names):
        box(ax, 2.7, y, 2.5, 0.85, n, color=BLUE, fs=8)
        arrow(ax, (1.9, 2.3), (2.7, y + 0.42))
    ax.text(3.95, 4.2, "Stage 1 · OvR ANFIS (one per class; binary: Attack, Normal)", ha="center", fontsize=9,
            fontweight="bold", color=TEXT)
    box(ax, 6.0, 1.65, 1.7, 1.3, "Scores s", "s_c = clip(ŷ_c, 0, 1)\ns ∈ [0,1]^C")
    for y in ys:
        arrow(ax, (5.2, y + 0.42), (6.0, 2.3))
    # OvR decision
    box(ax, 8.5, 3.15, 3.2, 1.0, "OvR prediction", "multi: argmax_c s_c\nbinary: Attack if s_Attack ≥ 0.5",
        color=TEXT2, fs=8)
    arrow(ax, (7.7, 2.6), (8.5, 3.6))
    box(ax, 8.5, 0.45, 3.2, 1.55, "Stage 2 · stacking ANFIS (+stk)",
        "input = s only; target = class index\n(DoS 0 · Imp 1 · Normal 2)\nŷ → round, clip → class\nsame init method as stage 1",
        color=ORANGE, fs=8)
    arrow(ax, (7.7, 2.0), (8.5, 1.3))
    ax.text(0.2, 4.7, "Classifier wrappers (src/models/anfis_classifiers.py)", fontsize=10,
            fontweight="bold", color=TEXT)
    fig.savefig(FIG / "arch_stacking.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    pipeline()
    anfis()
    stacking()
    print("wrote arch_pipeline.png, arch_anfis.png, arch_stacking.png")
