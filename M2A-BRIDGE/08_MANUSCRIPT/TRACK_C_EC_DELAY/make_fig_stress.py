#!/usr/bin/env python3
"""Draw V-mode and gate-threshold stress panels as three heatmaps."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
VCLIP = ROOT / "runs/P1-EC-VCLIP-01/experiment/outputs/summary.json"
GATE = ROOT / "runs/P1-EC-GATE-01/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig_stress.png"


def main() -> None:
    v = json.loads(VCLIP.read_text())["grid"]["allnone"]
    g = json.loads(GATE.read_text())["grid"]["allnone"]
    delays_v = ("0.02", "0.05", "0.1", "0.14", "0.2")
    modes = ("clip", "smooth", "unclipped")
    matrix_v = np.array([[v[d][m]["failure_rate"] for d in delays_v] for m in modes])

    ratios = ("0.01", "0.05", "0.15", "0.5")
    delays_g = ("0.02", "0.05", "0.1", "0.14")
    matrix_clip = np.array([[g[r][d]["clip"]["failure_rate"] for d in delays_g] for r in ratios])
    matrix_smooth = np.array([[g[r][d]["smooth"]["failure_rate"] for d in delays_g] for r in ratios])

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), constrained_layout=True)
    panels = (
        (axes[0], matrix_v, delays_v, modes, "V-term treatment", "gate filtered, V-mode"),
        (axes[1], matrix_clip, delays_g, ratios, "threshold ratio", "gate filtered, gate, clip"),
        (axes[2], matrix_smooth, delays_g, ratios, "threshold ratio", "gate filtered, gate, smooth"),
    )
    image = None
    for ax, matrix, xlabels, ylabels, ylabel, title in panels:
        image = ax.imshow(matrix, aspect="auto", origin="lower", vmin=0, vmax=1, cmap="magma")
        ax.set_xticks(range(len(xlabels)))
        ax.set_xticklabels(xlabels, fontsize=7)
        ax.set_yticks(range(len(ylabels)))
        ax.set_yticklabels(ylabels, fontsize=7)
        ax.set_xlabel("delay (s)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
    fig.colorbar(image, ax=axes, label="failure rate", shrink=0.9)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
