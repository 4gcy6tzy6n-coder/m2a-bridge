"""Unified visual system for the redrawn manuscript figures (v2).

One design language across every panel:
  * entity -> colour is fixed globally (Okabe-Ito based, CVD-safe);
  * typography scale is set once and reused by all panels;
  * axes carry only a left and bottom spine, hairline grey;
  * heatmaps use a calm white -> deep-blue sequential ramp with
    a hairline cell grid, never a saturated rainbow.

Every figure in this series is laid out 3 columns x 2 rows = 6 panels.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------- palette
# Colour follows the entity, never the plotting order.
COLORS = {
    "addition": "#E69F00",
    "graded filtered": "#56B4E9",
    "graded command": "#0072B2",
    "graded goal": "#009E73",
    "gate filtered": "#D55E00",
    "gate command": "#CC79A7",
    "gate goal": "#7B5EA7",
    "oracle": "#A6761D",
    # comparator / empirical entities
    "delayed": "#E69F00",
    "smith": "#2F6DB5",
    "pd_instant": "#009E73",
    "pd_gate": "#CC79A7",
    "smith_dde": "#8C6D31",
    "Mi4": "#009E73",
    "T4/T5": "#0072B2",
    "LPTC": "#7B5EA7",
    "main": "#7B5EA7",
    "pseudo": "#D55E00",
    "shift": "#56B4E9",
    "capacity": "#A6761D",
}

MARKERS = {
    "addition": "o",
    "graded filtered": "s",
    "graded command": "^",
    "graded goal": "D",
    "gate filtered": "s",
    "gate command": "^",
    "gate goal": "o",
    "oracle": "v",
}

INK = "#111418"
MUTED = "#5F6873"
FAINT = "#9AA3AD"
GRID_C = "#E7EAEE"
SPINE = "#B6BDC5"
PANEL_BG = "#FFFFFF"

# calm sequential ramp for heatmaps
SEQ = LinearSegmentedColormap.from_list(
    "paper_blue",
    ["#FBFCFE", "#E4EEF7", "#BBD4EA", "#87B0D2", "#4F84B3", "#2A5885", "#153B5C"],
)

# ---------------------------------------------------------------- sizes
FIGSIZE = (13.2, 7.5)      # one big figure = 3 cols x 2 rows
DPI = 300


def base_style() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9.5,
        "axes.titlesize": 10.0,
        "axes.labelsize": 9.5,
        "axes.edgecolor": SPINE,
        "axes.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID_C,
        "grid.linewidth": 0.7,
        "grid.linestyle": "-",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
        "xtick.major.size": 3.2,
        "ytick.major.size": 3.2,
        "xtick.major.width": 0.9,
        "ytick.major.width": 0.9,
        "legend.frameon": False,
        "legend.fontsize": 7.6,
        "legend.handlelength": 1.6,
        "legend.labelspacing": 0.32,
        "legend.borderaxespad": 0.3,
        "figure.facecolor": PANEL_BG,
        "axes.facecolor": PANEL_BG,
        "savefig.facecolor": PANEL_BG,
        "lines.linewidth": 1.7,
        "lines.markersize": 4.6,
        "lines.solid_capstyle": "round",
    })


def title(ax, letter: str, text: str) -> None:
    """Panel title: bold letter, then a quiet descriptive phrase."""
    ax.set_title("", pad=16)
    ax.text(0.0, 1.035, letter, transform=ax.transAxes,
            fontsize=11.5, fontweight="bold", color=INK, va="bottom", ha="left")
    ax.text(0.055, 1.035, text, transform=ax.transAxes,
            fontsize=9.6, color=INK, va="bottom", ha="left")


def style_axis(ax, grid_x: bool = False) -> None:
    ax.grid(axis="y", visible=True)
    ax.grid(axis="x", visible=grid_x)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(SPINE)
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(length=3.0, color=SPINE)


def rate_axis(ax, ylim=(-0.04, 1.08)) -> None:
    ax.set_ylim(*ylim)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])
    style_axis(ax)


def heat(ax, matrix, xlab, ylab, xticklabels, yticklabels, cbar_label="failure rate",
         annotate=True, fmt="{:.2f}", title_ax=None):
    """Sequential heatmap with hairline cell separators."""
    import numpy as np

    m = np.asarray(matrix, dtype=float)
    im = ax.imshow(m, cmap=SEQ, vmin=0.0, vmax=1.0, aspect="auto", origin="lower")
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels)
    ax.set_yticks(range(len(yticklabels)))
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.grid(False)
    # hairline separators between cells
    for i in range(1, m.shape[0]):
        ax.axhline(i - 0.5, color="white", lw=1.1)
    for j in range(1, m.shape[1]):
        ax.axvline(j - 0.5, color="white", lw=1.1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    if annotate:
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                v = m[i, j]
                ax.text(j, i, fmt.format(v), ha="center", va="center",
                        fontsize=7.4, color="white" if v > 0.62 else "#2A3540")
    return im


def save(fig, outdir, stem: str) -> None:
    from pathlib import Path

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / f"{stem}.png", dpi=DPI, facecolor=PANEL_BG)
    fig.savefig(outdir / f"{stem}.pdf", facecolor=PANEL_BG)
    plt.close(fig)
    print(f"wrote {stem}.png/.pdf")


def legend(ax, loc="upper left", ncol=1, fontsize=7.0, anchor=None, title=None):
    """Legend on a soft white card so it never fights the data underneath."""
    kw = dict(loc=loc, ncol=ncol, fontsize=fontsize, frameon=True,
              facecolor="white", edgecolor="#DDE1E6", framealpha=0.94,
              borderpad=0.55, handletextpad=0.65, borderaxespad=0.45)
    if anchor is not None:
        kw["bbox_to_anchor"] = anchor
    if title is not None:
        kw["title"] = title
    lg = ax.legend(**kw)
    lg.get_frame().set_linewidth(0.6)
    lg.get_frame().set_boxstyle("round,pad=0.35,rounding_size=0.28")
    return lg
