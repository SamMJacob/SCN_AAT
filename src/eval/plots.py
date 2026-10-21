"""Static report figures (matplotlib, light mode).

Palette: first three categorical slots of the validated reference palette (they pass
all-pairs CVD checks). Identity is never colour-only: every bar carries an x label
and a direct value label.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TEXT, TEXT2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
FAMILY_COLOR = {"classical ML": AQUA, "non-hybrid soft computing": ORANGE, "hybrid (ANFIS)": BLUE}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
    "text.color": TEXT, "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID,
    "grid.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 11, "axes.titleweight": "bold", "font.size": 9,
})


def family(model: str) -> str:
    if model.startswith("ANFIS"):
        return "hybrid (ANFIS)"
    if model in ("MLP", "FCM-clf"):
        return "non-hybrid soft computing"
    return "classical ML"


def _cap_ticks(ax, top=1.0):
    """Hide y ticks above 1.0 on score axes (headroom exists only for labels)."""
    ax.set_yticks([t for t in ax.get_yticks() if ax.get_ylim()[0] <= t <= top + 1e-9])


def _ylim_for(lo_vals):
    lo = float(np.nanmin(lo_vals))
    return (max(0.0, np.floor((lo - 0.02) * 20) / 20), 1.02)


def bar_with_err(ax, labels, means, stds, colors, ylabel, fmt="{:.3f}", ylim=None):
    x = np.arange(len(labels))
    ax.bar(x, means, width=0.62, color=colors, yerr=stds, capsize=2.5,
           error_kw=dict(ecolor=TEXT2, lw=0.8), edgecolor=SURFACE, linewidth=2)
    tops = np.asarray(means, float) + np.nan_to_num(np.asarray(stds, float))
    for xi, m, top in zip(x, means, tops):
        ax.annotate(fmt.format(m), (xi, top), ha="center", va="bottom", fontsize=7.5, color=TEXT,
                    xytext=(0, 3), textcoords="offset points")
    ax.set_xticks(x, labels, rotation=35, ha="right")
    ax.set_ylabel(ylabel)
    if ylim:
        ax.set_ylim(*ylim)
        _cap_ticks(ax)


def comparison1_chart(df, path, title):
    """df: index=model, columns mean/std of macro_f1 (ordered)."""
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    colors = [FAMILY_COLOR[family(m)] for m in df.index]
    bar_with_err(ax, df.index, df["mean"], df["std"], colors, "macro-F1 (test, mean ± std, 5 seeds)",
                 ylim=_ylim_for(df["mean"] - df["std"].fillna(0)))
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in FAMILY_COLOR.values()]
    ax.legend(handles, FAMILY_COLOR.keys(), frameon=False, fontsize=8, ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, -0.5))
    ax.set_title(title, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def comparison2_chart(tab, path, title, primary_label):
    """tab: rows=init names; columns: f1, f1_std, f1_stk, f1_stk_std, cls, cls_std, cls_stk,
    cls_stk_std, rules, rules_stk, time, time_stk, (optional) f1_ep5, f1_ep5_std."""
    inits = list(tab.index)
    x = np.arange(len(inits))
    w = 0.38
    panels = [("macro-F1", "f1", "{:.3f}"), (primary_label, "cls", "{:.3f}"),
              ("rule count", "rules", "{:.0f}"), ("train time (s)", "time", "{:.1f}")]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.4))
    for ax, (lab, key, fmt) in zip(axes, panels):
        for off, suffix, color, name in [(-w / 2, "", BLUE, "OvR (unstacked)"),
                                         (w / 2, "_stk", ORANGE, "OvR + stacking ANFIS")]:
            vals = tab[key + suffix].to_numpy(float)
            err = tab.get(key + suffix + "_std")
            ax.bar(x + off, vals, w, color=color, label=name, edgecolor=SURFACE, linewidth=2,
                   yerr=None if err is None else err.to_numpy(float), capsize=2,
                   error_kw=dict(ecolor=TEXT2, lw=0.8))
            tops = vals + (0 if err is None else np.nan_to_num(err.to_numpy(float)))
            for xi, v, top in zip(x + off, vals, tops):
                ax.annotate(fmt.format(v), (xi, top), ha="center", va="bottom", fontsize=6.5,
                            rotation=90 if key in ("f1", "cls") else 0,
                            xytext=(0, 2), textcoords="offset points")
        ax.set_xticks(x, inits)
        ax.set_title(lab, loc="left", fontsize=10)
        if key in ("f1", "cls"):
            lo = np.nanmin(np.r_[tab[key].to_numpy(float), tab[key + "_stk"].to_numpy(float)])
            ax.set_ylim(_ylim_for([lo - 0.01])[0], 1.03)
            _cap_ticks(ax)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=8, ncol=2, loc="lower center")
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def ladder_chart(data, path, title):
    """data: dict setting -> DataFrame(index=model in ladder order, mean, std)."""
    n = len(data)
    fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 3.6), sharey=False)
    axes = np.atleast_1d(axes)
    for ax, (setting, df) in zip(axes, data.items()):
        colors = [FAMILY_COLOR[family(m)] for m in df.index]
        bar_with_err(ax, df.index, df["mean"], df["std"], colors,
                     "macro-F1" if ax is axes[0] else "",
                     ylim=_ylim_for(df["mean"] - df["std"].fillna(0)))
        ax.set_title(f"Setting {setting}", loc="left", fontsize=10)
    present = {family(m) for df in data.values() for m in df.index}
    fams = [f for f in FAMILY_COLOR if f in present]
    handles = [plt.Rectangle((0, 0), 1, 1, color=FAMILY_COLOR[f]) for f in fams]
    fig.legend(handles, fams, frameon=False, fontsize=8, ncol=3, loc="lower center")
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def time_chart(df, path, title):
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    colors = [FAMILY_COLOR[family(m)] for m in df.index]
    bar_with_err(ax, df.index, df["mean"], df["std"], colors, "train time (s, log scale)",
                 fmt="{:.2g}")
    ax.set_yscale("log")
    ax.set_title(title, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def confusion_pair(cms, names, class_names, path, title):
    fig, axes = plt.subplots(1, len(cms), figsize=(3.6 * len(cms), 3.4))
    for ax, cm, name in zip(np.atleast_1d(axes), cms, names):
        norm = cm / np.maximum(cm.sum(1, keepdims=True), 1)
        ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, f"{cm[i, j]}", ha="center", va="center", fontsize=9,
                        color="white" if norm[i, j] > 0.6 else TEXT)
        ax.set_xticks(range(len(class_names)), class_names)
        ax.set_yticks(range(len(class_names)), class_names)
        ax.set_xlabel("predicted")
        ax.set_ylabel("true")
        ax.grid(False)
        ax.set_title(name, loc="left", fontsize=10)
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _gauss(x, c, s):
    return np.exp(-0.5 * ((x - c) / s) ** 2)


def mf_overlay(params_by_init, feature_idx, feature_name, member, path, title):
    """One panel per init: the member's MFs on one input, before (dashed) vs after training."""
    xs = np.linspace(-0.05, 1.05, 400)
    n = len(params_by_init)
    fig, axes = plt.subplots(1, n, figsize=(3.4 * n, 3.0), sharey=True)
    for ax, (init, p) in zip(np.atleast_1d(axes), params_by_init.items()):
        c0, s0 = p[f"m{member}_c0"][:, feature_idx], p[f"m{member}_s0"][:, feature_idx]
        c1, s1 = p[f"m{member}_c1"][:, feature_idx], p[f"m{member}_s1"][:, feature_idx]
        for r in range(len(c0)):
            ax.plot(xs, _gauss(xs, c0[r], s0[r]), color=TEXT2, lw=1, ls="--", alpha=0.6,
                    label="initial" if r == 0 else None)
            ax.plot(xs, _gauss(xs, c1[r], s1[r]), color=BLUE, lw=2,
                    label="after training" if r == 0 else None)
        ax.set_title(f"{init}  (R = {len(c0)})", loc="left", fontsize=10)
        ax.set_xlabel(f"{feature_name} (scaled)")
        ax.grid(False)
    np.atleast_1d(axes)[0].set_ylabel("membership")
    np.atleast_1d(axes)[0].legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
