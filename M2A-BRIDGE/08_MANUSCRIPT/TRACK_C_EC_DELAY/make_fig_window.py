#!/usr/bin/env python3
"""Draw the window-sensitivity figure."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-WINDOW-01/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig_window_check.png"
DELAYS = ("0.02", "0.05", "0.1", "0.14", "0.2")


def main() -> None:
    d = json.loads(SUMMARY.read_text())
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)
    for ax, model, color in (
        (axes[0], "allnone", "#D55E00"),
        (axes[1], "allnone_motor", "#CC79A7"),
    ):
        for window, style in (("2.5", "-"), ("6", "--"), ("10", ":")):
            ys = [d["grid"][model][delay][window]["failure_rate"] for delay in DELAYS]
            ax.plot(range(len(DELAYS)), ys, marker="o", linestyle=style, color=color, label=f"{window} s")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels(DELAYS)
        ax.set_xlabel("delay (s)")
        ax.set_ylabel("failure rate")
        ax.set_ylim(-0.05, 1.05)
        ax.set_title("gate filtered" if model == "allnone" else "gate unfiltered")
        ax.legend(frameon=False, fontsize=7)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
