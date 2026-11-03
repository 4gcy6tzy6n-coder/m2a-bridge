#!/usr/bin/env python3
"""Draw Fig. 2c: EC gain x delay failure heatmaps from the gain sweep."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-GAIN-01/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig2c_gain_delay_heatmap.png"
GAINS = ("0", "0.05", "0.25", "0.5", "0.75", "1")
DELAYS = ("0.02", "0.05", "0.1", "0.2")
PANELS = ("graded_sensory", "allnone", "allnone_motor")
LABELS = {
    "graded_sensory": "graded filtered",
    "allnone": "gate filtered",
    "allnone_motor": "gate unfiltered",
}


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), constrained_layout=True)
    image = None
    for ax, model in zip(axes, PANELS):
        grid = summary["grid"][model]
        matrix = np.array([[grid[g][d] for d in DELAYS] for g in GAINS])
        image = ax.imshow(matrix, aspect="auto", origin="lower", vmin=0, vmax=1, cmap="magma")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels(DELAYS)
        ax.set_yticks(range(len(GAINS)))
        ax.set_yticklabels(GAINS)
        ax.set_xlabel("delay (s)")
        ax.set_title(LABELS.get(model, model.replace("_", " ")))
    axes[0].set_ylabel("efference-copy gain")
    fig.colorbar(image, ax=axes, label="failure rate", shrink=0.9)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
