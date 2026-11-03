#!/usr/bin/env python3
"""Noise robustness of the failure rates."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fig_style import COLORS, MARKERS, base_style, panel_label

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
OUT = Path(__file__).resolve().parent / "fig_noise.png"
GRID = json.loads((ROOT / "runs/P1-EC-NOISE-01/experiment/outputs/summary.json").read_text())["grid"]

SERIES = (
    ("graded filtered|ff=0", "graded filtered"),
    ("graded goal|ff=1", "graded goal"),
    ("gate filtered|ff=0", "gate filtered"),
    ("gate goal|ff=0.5", "gate goal"),
    ("gate goal|ff=1", "gate goal"),
)
NOISE_TICKS = ("0", "1e-13", "1e-12", "1e-11")


def main() -> None:
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.7), constrained_layout=True)

    for ax, delay, letter, title in (
        (axes[0], "0.1", "a", "100 ms delay"),
        (axes[1], "0.2", "b", "200 ms delay"),
    ):
        for key, entity in SERIES:
            rates = [GRID[key][n][delay]["failure_rate"] for n in NOISE_TICKS]
            partial = key.endswith("ff=0.5")
            if entity == "gate goal":
                label = "gate goal ff=0.5" if partial else "gate goal ff=1"
            else:
                label = entity
            ax.plot(
                range(len(NOISE_TICKS)), rates,
                marker=MARKERS[entity], color=COLORS[entity],
                linestyle=(0, (4, 2)) if partial else "-",
                label=label,
            )
        ax.set_xticks(range(len(NOISE_TICKS)))
        ax.set_xticklabels(NOISE_TICKS)
        ax.set_xlabel("torque noise SD (N m)")
        ax.set_ylabel("failure rate")
        ax.set_ylim(-0.05, 1.08)
        ax.set_title(f"{letter}  {title} (n = 8 per cell)")
        panel_label(ax, letter)

    # single shared legend below
    handles, labels = axes[0].get_legend_handles_labels()
    dedup = dict(zip(labels, handles))
    fig.legend(dedup.values(), dedup.keys(), loc="lower center",
               ncol=5, bbox_to_anchor=(0.5, -0.02))
    fig.savefig(OUT, dpi=220, bbox_inches="tight")
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight")
    print(OUT)


if __name__ == "__main__":
    main()
