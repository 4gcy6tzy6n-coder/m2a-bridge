"""Shared style for Track C figures.

Palette validated with the dataviz six-checks validator (light mode,
2026-10-27): lightness band, chroma floor, CVD separation, and normal-vision
floor all pass. The three lighter hues carry a contrast WARN, so every series
keeps a visible legend and selective direct labels.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Entity -> hue, fixed across all figures (color follows the entity).
COLORS = {
    "addition": "#E69F00",
    "graded filtered": "#56B4E9",
    "graded command": "#0072B2",
    "graded goal": "#009E73",
    "gate filtered": "#D55E00",
    "gate command": "#CC79A7",
    "gate goal": "#7B5EA7",
    "oracle": "#A6761D",
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

INK = "#1A1A1A"
MUTED = "#5A5A5A"
GRID = "#E8E8E6"
SURFACE = "#FFFFFF"


def base_style() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.edgecolor": "#B8B8B6",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.7,
        "grid.linestyle": "-",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "lines.linewidth": 2.0,
        "lines.markersize": 7,
    })


def panel_label(ax, letter: str) -> None:
    ax.text(-0.12, 1.04, letter, transform=ax.transAxes,
            fontsize=12, fontweight="bold", color=INK, va="bottom", ha="right")
