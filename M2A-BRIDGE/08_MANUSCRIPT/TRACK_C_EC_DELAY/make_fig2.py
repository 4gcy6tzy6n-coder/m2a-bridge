#!/usr/bin/env python3
"""Draw Fig. 2: failure rate vs delay from the P1 coarse sweep."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-DELAY-01/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig2_failure_rate_vs_delay.png"
SERIES = (
    ("addition", "addition", "#555555"),
    ("graded_sensory", "graded sensory", "#E69F00"),
    ("graded_motor", "graded motor", "#009E73"),
    ("allnone", "allnone gating", "#D55E00"),
)


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    fig, ax = plt.subplots(figsize=(5.6, 3.6), constrained_layout=True)
    for model, label, color in SERIES:
        curve = summary["models"][model]["failure_curve"]
        xs = [float(k) for k in curve]
        ys = [curve[k] for k in curve]
        ax.plot(xs, ys, marker="o", markersize=3, label=label, color=color)
    ax.set_xlabel("feedback delay (s)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
