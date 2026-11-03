#!/usr/bin/env python3
"""Mechanism schematic: what a delayed visual loop lacks.

Three panels: (a) a command copy does not rescue, (b) a goal feedforward with
current self-state rescues, (c) delaying that self-state removes the rescue.
Static publication figure; palette validated for CVD separation.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "fig_mechanism.png"

# Validated categorical hues (dataviz validator, 2026-10-27).
C_DELAY = "#D55E00"      # delay / failure
C_COMMAND = "#CC79A7"    # command copy
C_FEEDFWD = "#009E73"    # goal feedforward, rescue
C_CTRL = "#56B4E9"       # controller
C_PLANT = "#A6761D"      # plant
INK = "#1A1A1A"
MUTED = "#5A5A5A"
SURFACE = "#FFFFFF"
BOX_FACE = "#F7F7F5"


def box(ax, x, y, w, h, label, edge, face=BOX_FACE, lw=1.6, fontsize=9, dashed=False):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=face, edgecolor=edge, linewidth=lw,
        linestyle=(0, (4, 2)) if dashed else "-",
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fontsize, color=INK, linespacing=1.3)


def arrow(ax, x0, y0, x1, y1, color, style="-", lw=1.8, shrink=5):
    arr = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="-|>", mutation_scale=13,
        color=color, linewidth=lw, linestyle=style,
        shrinkA=shrink, shrinkB=shrink,
    )
    ax.add_patch(arr)


def badge(ax, x, y, ok, text, sub):
    mark = "✓" if ok else "✗"
    color = C_FEEDFWD if ok else C_DELAY
    ax.text(x, y, f"{mark} {text}", ha="center", va="center",
            fontsize=11, color=color, fontweight="bold")
    ax.text(x, y - 0.5, sub, ha="center", va="center", fontsize=8.5, color=MUTED)


def panel(ax, letter, mode: str) -> None:
    """mode: command | feedforward | delayed_self"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.text(0.1, 6.05, letter, fontsize=13, fontweight="bold", color=INK, va="top")

    # Core loop: delayed visual state -> controller -> torque filter -> plant -> back
    box(ax, 0.4, 3.0, 2.5, 1.0, "delayed visual\nstate  (t − d)", C_DELAY)
    box(ax, 3.7, 3.0, 2.0, 1.0, "controller", C_CTRL, face="#EAF6FB")
    box(ax, 6.5, 3.0, 1.9, 1.0, "bar torque\nfilter", C_PLANT)
    box(ax, 3.5, 0.7, 2.4, 1.1, "plant\n(body)", C_PLANT, face="#FBF3E7")

    arrow(ax, 2.9, 3.5, 3.7, 3.5, INK)
    arrow(ax, 5.7, 3.5, 6.5, 3.5, INK)
    arrow(ax, 7.45, 3.0, 7.45, 1.6, INK)
    arrow(ax, 7.45, 1.25, 5.9, 1.25, INK)
    # plant -> delayed visual, dashed orange (visual feedback with delay)
    arrow(ax, 3.5, 1.25, 1.65, 1.25, C_DELAY, style=(0, (4, 2)))
    arrow(ax, 1.65, 1.25, 1.65, 3.0, C_DELAY, style=(0, (4, 2)))
    ax.text(2.35, 2.15, "visual feedback\nwith delay d", fontsize=8,
            color=C_DELAY, ha="center", va="center", linespacing=1.3)

    if mode == "command":
        # command copy node above the loop, fed from the issued command
        box(ax, 4.9, 4.6, 2.4, 0.9, "command copy\n→ EC / gate",
            C_COMMAND, face="#F9EEF4", dashed=True, fontsize=8.5)
        arrow(ax, 6.1, 4.6, 6.1, 3.55, C_COMMAND, style=(0, (3, 2)))
        ax.text(4.35, 4.2, "copy of issued command", fontsize=8,
                color=C_COMMAND, ha="center", va="center")
        badge(ax, 8.9, 5.35, False, "no rescue", "same as feedback")
    elif mode == "feedforward":
        box(ax, 0.4, 4.7, 3.4, 0.9, "goal + current\nself-state (ψ, ω)",
            C_FEEDFWD, face="#E9F7F3")
        arrow(ax, 3.8, 5.15, 6.9, 5.15, C_FEEDFWD, lw=2.2)
        arrow(ax, 6.9, 5.15, 6.9, 4.0, C_FEEDFWD, lw=2.2)
        ax.text(5.3, 5.42, "feedforward torque", fontsize=8.5,
                color=C_FEEDFWD, ha="center")
        badge(ax, 8.9, 5.15, True, "rescue", "0% failure ≤ 200 ms")
    else:  # delayed_self
        box(ax, 0.4, 4.7, 3.4, 0.9, "goal + delayed\nself-state (t − d)",
            C_DELAY, face="#FBEEE6", dashed=True)
        arrow(ax, 3.8, 5.15, 6.9, 5.15, C_DELAY, lw=2.2, style=(0, (4, 2)))
        arrow(ax, 6.9, 5.15, 6.9, 4.0, C_DELAY, lw=2.2, style=(0, (4, 2)))
        ax.text(5.3, 5.42, "feedforward torque", fontsize=8.5,
                color=C_DELAY, ha="center")
        badge(ax, 8.9, 5.15, False, "rescue lost", "75–100% failure")


def main() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.0), constrained_layout=True)
    panel(axes[0], "a", "command")
    panel(axes[1], "b", "feedforward")
    panel(axes[2], "c", "delayed_self")
    fig.savefig(OUT, dpi=220, facecolor=SURFACE)
    fig.savefig(OUT.with_suffix(".pdf"), facecolor=SURFACE)
    print(OUT)


if __name__ == "__main__":
    main()
