#!/usr/bin/env python3
"""Draw Fig. 3: phase diagram from the P2 noise/body sweep."""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SWEEP = ROOT / "runs/P1-EC-DELAY-02/experiment/outputs/sweep_noise.csv"
OUT = Path(__file__).resolve().parent / "fig3_phase_diagram.png"
MODELS = ("graded_sensory", "allnone")


def main() -> None:
    with SWEEP.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    taus = sorted({round(float(row["tau_body_s"]) * 1000, 3) for row in rows})
    delays = sorted({float(row["delay_s"]) for row in rows})

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), constrained_layout=True)
    image = None
    for ax, model in zip(axes, MODELS):
        counts: dict[tuple[float, float], list[int]] = defaultdict(list)
        for row in rows:
            if row["model"] != model:
                continue
            tau = round(float(row["tau_body_s"]) * 1000, 3)
            counts[(tau, float(row["delay_s"]))].append(int(row["failure"]))
        matrix = np.array(
            [
                [np.mean(counts[(tau, delay)]) if counts[(tau, delay)] else np.nan for delay in delays]
                for tau in taus
            ]
        )
        image = ax.imshow(matrix, aspect="auto", origin="lower", vmin=0, vmax=1, cmap="magma")
        ax.set_xticks(range(len(delays)))
        ax.set_xticklabels([f"{d:g}" for d in delays], rotation=90, fontsize=6)
        ax.set_yticks(range(len(taus)))
        ax.set_yticklabels([f"{t:g}" for t in taus])
        ax.set_xlabel("delay (s)")
        ax.set_title(model.replace("_", " "))
    axes[0].set_ylabel("body time constant I/beta (ms)")
    fig.colorbar(image, ax=axes, label="failure rate", shrink=0.9)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
