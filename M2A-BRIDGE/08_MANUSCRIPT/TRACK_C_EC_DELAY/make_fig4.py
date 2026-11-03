#!/usr/bin/env python3
"""Draw Fig. 4: example trajectories at 140 ms with noise."""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/06_JOINT")
from ec_model import Params, simulate  # noqa: E402

OUT = Path(__file__).resolve().parent / "fig4_example_trajectories.png"
SERIES = (
    ("addition", "addition", "#555555"),
    ("graded_sensory", "graded sensory", "#E69F00"),
    ("graded_motor", "graded motor", "#009E73"),
    ("allnone", "allnone gating", "#D55E00"),
    ("allnone_motor", "allnone motor-copy gating", "#CC79A7"),
)


def main() -> None:
    params = Params()
    fig, ax = plt.subplots(figsize=(6.2, 3.6), constrained_layout=True)
    for model, label, color in SERIES:
        time, _, readouts = simulate(
            model,
            params,
            delay_s=0.14,
            grating_gain=params.k_opto,
            noise_sd=1e-13,
            seed=0,
        )
        ax.plot(time, np.rad2deg(readouts["heading"]), label=label, color=color)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("heading (deg)")
    ax.legend(frameon=False, fontsize=7)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
