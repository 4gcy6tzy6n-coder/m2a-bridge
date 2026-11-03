#!/usr/bin/env python3
"""Delay limits: fine grid at 6 s (0-250 ms) and long-delay check at 10 s."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fig_style import COLORS, MARKERS, base_style, panel_label

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
OUT = Path(__file__).resolve().parent / "fig_delay_limits.png"

FINE = json.loads((ROOT / "runs/P1-EC-FINEDELAY-01/experiment/outputs/summary.json").read_text())["grid"]
LONG = json.loads((ROOT / "runs/P1-EC-LONGDELAY-01/experiment/outputs/summary.json").read_text())["grid"]

FINE_SERIES = (
    ("graded filtered|ff=0", "graded filtered"),
    ("graded goal|ff=1", "graded goal"),
    ("gate filtered|ff=0", "gate filtered"),
    ("gate goal|ff=1", "gate goal"),
)
LONG_SERIES = (
    ("addition|ff=0", "addition"),
    ("graded filtered|ff=0", "graded filtered"),
    ("graded goal|ff=1", "graded goal"),
    ("gate filtered|ff=0", "gate filtered"),
    ("gate goal|ff=0.5", "gate goal"),   # dashed = partial dose
    ("gate goal|ff=1", "gate goal"),
)


def main() -> None:
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8), constrained_layout=True)

    ax = axes[0]
    for key, entity in FINE_SERIES:
        delays = sorted(float(k) for k in FINE[key])
        rates = [FINE[key][f"{d:g}"]["failure_rate"] for d in delays]
        ax.plot([d * 1000 for d in delays], rates, marker=MARKERS[entity],
                color=COLORS[entity], markersize=4.5, linestyle="-",
                label=entity)
    ax.set_xlabel("visual delay (ms)")
    ax.set_ylabel("failure rate")
    ax.set_xlim(0, 255)
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("a  fine grid, 6 s window (n = 8 per cell)")
    panel_label(ax, "a")
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98))

    ax = axes[1]
    for key, entity in LONG_SERIES:
        delays = sorted(float(k) for k in LONG[key])
        rates = [LONG[key][f"{d:g}"]["failure_rate"] for d in delays]
        partial = key.endswith("ff=0.5")
        ax.plot([d * 1000 for d in delays], rates, marker=MARKERS[entity],
                color=COLORS[entity], markersize=6,
                linestyle=(0, (4, 2)) if partial else "-",
                label="gate goal ff=0.5" if partial else entity)
    ax.set_xlabel("visual delay (ms)")
    ax.set_ylabel("failure rate")
    ax.set_xlim(190, 510)
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("b  long delays, 10 s window (n = 8 per cell)")
    panel_label(ax, "b")
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98))

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
