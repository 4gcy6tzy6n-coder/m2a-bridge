#!/usr/bin/env python3
"""Draw adaptive update comparison with x-offsets so overlapping curves are visible."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-ADAPTIVE-03/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig_adaptive_gradient.png"
DELAYS = ("0.02", "0.05", "0.1", "0.2")
SERIES = (
    ("source", "source-style squared error", "#555555", "o", -0.18),
    ("gradient", "signed gradient", "#0072B2", "s", 0.0),
    ("gradient_neg", "signed gradient, opposite sign", "#E69F00", "^", 0.18),
)


def main() -> None:
    d = json.loads(SUMMARY.read_text())
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)
    base = np.arange(len(DELAYS))
    for mode, label, color, marker, offset in SERIES:
        axes[0].plot(
            base + offset,
            [d["grid"][mode][delay]["failure_rate"] for delay in DELAYS],
            marker=marker,
            linestyle="none",
            markersize=7,
            label=label,
            color=color,
        )
        axes[1].plot(
            base + offset,
            [d["grid"][mode][delay]["mean_ro"] for delay in DELAYS],
            marker=marker,
            label=label,
            color=color,
        )
    for ax, ylabel in zip(axes, ("failure rate", "mean learned gain")):
        ax.set_xticks(base)
        ax.set_xticklabels(DELAYS)
        ax.set_xlabel("delay (s)")
        ax.set_ylabel(ylabel)
    axes[0].set_ylim(-0.05, 1.05)
    axes[0].legend(frameon=False, fontsize=7)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
