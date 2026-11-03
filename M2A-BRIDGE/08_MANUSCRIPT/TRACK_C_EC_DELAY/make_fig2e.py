#!/usr/bin/env python3
"""Draw Fig. 2e (supplementary): adaptive MLP across learning rates."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-ADAPTIVE-02/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig2e_adaptive_alpha.png"
ALPHAS = ("1e-05", "8e-05", "0.0005", "0.001")
DELAYS = ("0.02", "0.05", "0.1", "0.2")


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)
    for ax, key, title in zip(
        axes, ("failure_rate", "mean_ro"), ("failure rate", "mean learned gain")
    ):
        matrix = np.array(
            [[summary["grid"][a][d][key] for d in DELAYS] for a in ALPHAS]
        )
        image = ax.imshow(matrix, aspect="auto", origin="lower", cmap="magma")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels(DELAYS)
        ax.set_yticks(range(len(ALPHAS)))
        ax.set_yticklabels(ALPHAS)
        ax.set_xlabel("delay (s)")
        ax.set_title(title)
        fig.colorbar(image, ax=ax, shrink=0.9)
    axes[0].set_ylabel("learning rate alpha")
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
