#!/usr/bin/env python3
"""Draw a critical-delay dot plot from the 1 ms fine grid."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-DELAY-03/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig2b_critical_delays.png"

MODELS = ("addition", "graded_sensory", "graded_motor", "allnone_motor", "allnone")
COLORS = ("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00")


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    rng = np.random.default_rng(0)
    for index, (model, color) in enumerate(zip(MODELS, COLORS)):
        values = np.array(summary["models"][model]["critical_delays_s"], dtype=float) * 1000
        jitter = rng.uniform(-0.08, 0.08, size=len(values))
        ax.scatter(np.full_like(values, index) + jitter, values, color=color, s=28, alpha=0.85, zorder=3)
        median = np.median(values)
        ax.hlines(median, index - 0.25, index + 0.25, color=color, linewidth=2, zorder=2)
        ax.text(index, median + 6, f"{median:.0f}", ha="center", va="bottom", fontsize=8, color=color)
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels(MODELS, rotation=15)
    ax.set_ylabel("first failing delay (ms)")
    ax.set_ylim(0, 230)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
