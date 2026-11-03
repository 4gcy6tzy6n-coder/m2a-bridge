#!/usr/bin/env python3
"""Example trajectories and gate state at 200 ms delay."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fig_style import COLORS, base_style, panel_label

ROOT = Path("/Users/yyl/Desktop/workshop/nature/runs/P1-EC-TRAJ-01/experiment/outputs")
OUT = Path(__file__).resolve().parent / "fig_trajectories.png"

TRACES = (
    ("addition", "addition"),
    ("graded_filtered", "graded filtered"),
    ("gate_filtered", "gate filtered"),
    ("gate_goal", "gate goal"),
)


def main() -> None:
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.7), constrained_layout=True)

    ax = axes[0]
    for fname, entity in TRACES:
        d = np.load(ROOT / f"{fname}.npz")
        t, h = d["time"], d["heading"]
        ax.plot(t, h, color=COLORS[entity], label=entity, alpha=0.9)
    theta_bar = np.load(ROOT / "gate_goal.npz")["theta_bar"]
    ax.plot(t, theta_bar, color="#1A1A1A", linewidth=1.2, linestyle=(0, (3, 2)),
            label="bar target", zorder=1)
    ax.axhline(2 * np.pi, color="#B8B8B6", linewidth=0.8)
    ax.axhline(-2 * np.pi, color="#B8B8B6", linewidth=0.8)
    ax.set_ylim(-7.5, 7.5)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("heading (rad)")
    ax.set_title("a  heading, 200 ms delay, 10 s window")
    panel_label(ax, "a")
    ax.text(0.03, 0.05, "addition and graded filtered\nleave ±2π (off scale)",
            transform=ax.transAxes, fontsize=8, color="#5A5A5A", va="bottom")
    ax.legend(loc="upper left", fontsize=7.5, ncol=2)

    ax = axes[1]
    for fname, entity in (("gate_filtered", "gate filtered"), ("gate_goal", "gate goal")):
        d = np.load(ROOT / f"{fname}.npz")
        t, g = d["time"], d["gate_closed"]
        duty = float(np.mean(g))
        ax.plot(t, g, color=COLORS[entity], label=f"{entity} (duty {duty:.2f})",
                linewidth=1.4, alpha=0.9)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("gate closed")
    ax.set_title("b  grating gate state, 200 ms delay")
    panel_label(ax, "b")
    ax.legend(loc="upper left", fontsize=7.5)

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
