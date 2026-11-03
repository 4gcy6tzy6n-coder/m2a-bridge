#!/usr/bin/env python3
"""Draw the true command-copy comparison."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-COMMAND-01/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig_command_copy.png"
DELAYS = ("0.02", "0.05", "0.1", "0.14", "0.2")
GRADED = (
    ("graded filtered", "#E69F00", "s", -0.12),
    ("graded command", "#0072B2", "o", 0.0),
    ("graded unfiltered oracle", "#009E73", "^", 0.12),
)
GATE = (
    ("gate filtered", "#D55E00", "s", -0.12),
    ("gate command", "#CC79A7", "o", 0.0),
    ("gate unfiltered oracle", "#555555", "^", 0.12),
)


def main() -> None:
    d = json.loads(SUMMARY.read_text())["grid"]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)

    base = [i for i in range(len(DELAYS))]
    for label, color, marker, offset in GRADED:
        axes[0].plot(
            [x + offset for x in base],
            [d[label]["1"][delay]["failure_rate"] for delay in DELAYS],
            marker=marker,
            linestyle="none",
            markersize=7,
            label=label,
            color=color,
        )
    axes[0].set_xticks(range(len(DELAYS)))
    axes[0].set_xticklabels(DELAYS)
    axes[0].set_xlabel("delay (s)")
    axes[0].set_ylabel("failure rate")
    axes[0].set_ylim(-0.05, 1.05)
    axes[0].set_title("graded EC, gain 1.0")
    axes[0].legend(frameon=False, fontsize=7)

    for label, color, marker, offset in GATE:
        axes[1].plot(
            [x + offset for x in base],
            [d[label]["1"][delay]["gate_duty"] for delay in DELAYS],
            marker=marker,
            label=label,
            color=color,
        )
    axes[1].set_xticks(range(len(DELAYS)))
    axes[1].set_xticklabels(DELAYS)
    axes[1].set_xlabel("delay (s)")
    axes[1].set_ylabel("gate duty cycle")
    axes[1].set_ylim(0, 1)
    axes[1].set_title("gating")
    axes[1].legend(frameon=False, fontsize=7)

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
