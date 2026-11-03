#!/usr/bin/env python3
"""Draw Fig. 1: model schematic."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "fig1_model.png"


def box(ax, xy, width, height, text, color="#eef2f7"):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2,
        edgecolor="#333333",
        facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=9)
    return patch


def arrow(ax, start, end, style="-|>", color="#333333", linestyle="-"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=12,
            linewidth=1.1,
            color=color,
            linestyle=linestyle,
        )
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    box(ax, (0.2, 3.6), 1.8, 0.9, "visual scene\nbar + grating", "#e8f1fb")
    box(ax, (2.5, 3.6), 1.3, 0.9, "delay d", "#fdf1d7")
    box(ax, (4.3, 4.1), 1.7, 0.7, "bar pathway\nP(error), V(error)", "#e8f1fb")
    box(ax, (4.3, 3.1), 1.7, 0.7, "grating pathway\nk_opto", "#e8f1fb")
    box(ax, (6.7, 3.6), 1.5, 0.9, "body\nI, beta", "#e9f7ee")
    box(ax, (8.7, 3.6), 1.0, 0.9, "heading", "#e9f7ee")

    arrow(ax, (2.0, 4.05), (2.5, 4.05))
    arrow(ax, (3.8, 4.2), (4.3, 4.45))
    arrow(ax, (3.8, 3.9), (4.3, 3.45))
    arrow(ax, (6.0, 4.45), (6.7, 4.2))
    arrow(ax, (6.0, 3.45), (6.7, 3.9))
    arrow(ax, (8.2, 4.05), (8.7, 4.05))

    box(ax, (4.3, 2.0), 3.9, 0.7, "graded EC: filtered or unfiltered bar-pathway drive", "#f3e8fb")
    arrow(ax, (5.15, 4.1), (5.15, 2.7), style="-|>", linestyle="--", color="#7a3e9d")
    arrow(ax, (6.25, 2.35), (6.25, 3.1), style="-|>", linestyle="--", color="#7a3e9d")

    box(ax, (4.3, 0.8), 3.9, 0.7, "gating: set k_opto = 0 while |bar drive| > threshold", "#fde8e8")

    ax.text(
        0.2,
        0.35,
        "Five variants: addition  |  graded filtered  |  graded unfiltered  |  gate filtered  |  gate unfiltered",
        fontsize=9,
    )
    ax.text(0.2, 0.1, "Dashed paths are the two ways of removing self-generated optic flow.", fontsize=8, color="#555555")

    fig.tight_layout()
    fig.savefig(OUT, dpi=220, bbox_inches="tight")
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight")
    print(OUT)


if __name__ == "__main__":
    main()
