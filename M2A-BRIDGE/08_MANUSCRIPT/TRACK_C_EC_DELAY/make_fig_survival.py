#!/usr/bin/env python3
"""Failure-free survival curves at 140 ms from the three-seed run."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fig_style import COLORS, MARKERS, base_style, panel_label

ROOT = Path("/Users/yyl/Desktop/workshop/nature/runs/P1-EC-MULTISEED-01/experiment/outputs/multiseed.csv")
OUT = Path(__file__).resolve().parent / "fig_survival.png"

SERIES = (
    ("graded_sensory", 0.0, "graded filtered"),
    ("graded_goal", 1.0, "graded goal"),
    ("allnone", 0.0, "gate filtered"),
    ("gate_command", 0.0, "gate command"),
    ("gate_goal", 1.0, "gate goal"),
)
DELAY = 0.14
WINDOW = 6.0


def survival(rows: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray]:
    times, events = [], []
    for row in rows:
        failed = int(row["failure"])
        if failed:
            times.append(float(row["failure_time_s"]))
            events.append(1)
        else:
            times.append(WINDOW)
            events.append(0)
    order = np.argsort(times)
    times = np.asarray(times)[order]
    events = np.asarray(events)[order]
    n = len(times)
    n_censored = int(np.sum(events == 0))
    t_grid = np.linspace(0, WINDOW, 400)
    s = np.ones_like(t_grid)
    for i, t in enumerate(t_grid):
        fail_after = int(np.sum((times > t) & (events == 1)))
        s[i] = (fail_after + n_censored) / n
    return t_grid, s


def main() -> None:
    base_style()
    fig, ax = plt.subplots(figsize=(5.2, 3.8), constrained_layout=True)

    with ROOT.open() as fh:
        rows = list(csv.DictReader(fh))

    for model, ff, entity in SERIES:
        subset = [
            r for r in rows
            if r["model"] == model
            and abs(float(r["ff_gain"]) - ff) < 1e-12
            and abs(float(r["delay_s"]) - DELAY) < 1e-12
        ]
        t, s = survival(subset)
        ax.step(t, s, where="post", color=COLORS[entity], marker=MARKERS[entity],
                markevery=(0, 40), markersize=6, label=f"{entity} (n={len(subset)})")

    ax.set_xlabel("time (s)")
    ax.set_ylabel("failure-free fraction")
    ax.set_xlim(0, WINDOW)
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("failure-free runs at 140 ms delay (3 seeds × 8 parameter sets)")
    ax.legend(loc="lower left", fontsize=7.5)

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
