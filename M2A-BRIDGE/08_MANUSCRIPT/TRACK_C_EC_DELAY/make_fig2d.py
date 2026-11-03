#!/usr/bin/env python3
"""Draw Fig. 2d: adaptive MLP vs fixed gains under delay."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-ADAPTIVE-01/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig2d_adaptive.png"
DELAYS = ("0.02", "0.05", "0.1", "0.2")
SERIES = (
    ("graded_adaptive", "adaptive MLP", "#0072B2"),
    ("graded_fixed_0.05", "fixed graded, gain 0.05", "#E69F00"),
    ("graded_fixed_1.0", "fixed graded, gain 1.0", "#009E73"),
    ("addition", "no EC", "#555555"),
    ("allnone", "delayed sensory gating", "#D55E00"),
)


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)

    ax = axes[0]
    for model, label, color in SERIES:
        ys = [summary["models"][model][d]["failure_rate"] for d in DELAYS]
        ax.plot(range(len(DELAYS)), ys, marker="o", label=label, color=color)
    ax.set_xticks(range(len(DELAYS)))
    ax.set_xticklabels(DELAYS)
    ax.set_xlabel("delay (s)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False, fontsize=7)

    ax = axes[1]
    ro = [summary["models"]["graded_adaptive"][d]["mean_ro"] for d in DELAYS]
    ax.plot(range(len(DELAYS)), ro, marker="o", color="#0072B2")
    ax.set_xticks(range(len(DELAYS)))
    ax.set_xticklabels(DELAYS)
    ax.set_xlabel("delay (s)")
    ax.set_ylabel("learned EC gain (mean ro)")
    ax.set_ylim(0, 1.3)

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
