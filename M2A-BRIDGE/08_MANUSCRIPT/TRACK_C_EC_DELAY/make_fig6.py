#!/usr/bin/env python3
"""Draw Fig. 6: linear stability (rightmost eigenvalue vs delay)."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
DATA = ROOT / "M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/linear_stability.json"
OUT = Path(__file__).resolve().parent / "fig6_linear_stability.png"
SERIES = (
    ("addition", 0.05, "addition", "#555555"),
    ("graded_sensory", 0.05, "graded sensory, gain 0.05", "#E69F00"),
    ("graded_sensory", 1.0, "graded sensory, gain 1.0", "#009E73"),
    ("graded_motor", 1.0, "graded motor, gain 1.0", "#CC79A7"),
    ("allnone", 0.05, "allnone (open gate)", "#D55E00"),
)


def main() -> None:
    rows = json.loads(DATA.read_text())
    lookup = {(row["model"], float(row["ec_gain"])): row for row in rows}
    fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
    for model, gain, label, color in SERIES:
        row = lookup.get((model, gain))
        if row is None:
            continue
        delays = [point["delay_s"] for point in row["curve"]]
        values = [point["max_real"] for point in row["curve"]]
        ax.plot(delays, values, label=label, color=color)
        critical = float(row["critical_delay_s"])
        if critical < 0.30:
            ax.axvline(critical, color=color, linestyle=":", alpha=0.6)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_ylim(-4.0, 4.0)
    ax.set_xlabel("feedback delay (s)")
    ax.set_ylabel("rightmost Re(lambda) (1/s)")
    ax.legend(frameon=False, fontsize=7)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
