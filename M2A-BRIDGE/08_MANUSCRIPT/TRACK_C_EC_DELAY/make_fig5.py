#!/usr/bin/env python3
"""Draw Fig. 5: allnone versus allnone_motor failure curves from P2 summary."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SUMMARY = ROOT / "runs/P1-EC-DELAY-02/experiment/outputs/summary.json"
OUT = Path(__file__).resolve().parent / "fig5_gating_signal.png"


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    for model, color in (("allnone", "#c0392b"), ("allnone_motor", "#7d3c98")):
        curve = summary["models"][model]["failure_curve"]
        xs = [float(key) for key in curve]
        ys = [curve[key] for key in curve]
        ax.plot(xs, ys, marker="o", label=model, color=color)
    ax.set_xlabel("feedback delay (s)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
