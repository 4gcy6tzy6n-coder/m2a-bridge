#!/usr/bin/env python3
"""Self-state proposition package: freshness dose-response, onset decoupling, no-goal damping."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fig_style import COLORS, MARKERS, base_style, panel_label

ROOT = Path("/Users/yyl/Desktop/workshop/nature/runs")
OUT = Path(__file__).resolve().parent / "fig_selfstate.png"

LAG = json.loads((ROOT / "P1-EC-SELFSTATE-01/experiment/outputs/summary.json").read_text())["grid"]
ONSET = json.loads((ROOT / "P1-EC-ONSET-01/experiment/outputs/summary.json").read_text())["grid"]
DAMP = json.loads((ROOT / "P1-EC-DAMP-01/experiment/outputs/summary.json").read_text())["grid"]

LAGS = ("0", "0.01", "0.02", "0.03", "0.04", "0.05", "0.1", "0.2")
ONSETS = ("0.3", "0.4", "0.5", "0.6", "0.8")
DAMP_LABELS = ("gate damping 0.5e-11", "gate damping 1e-11", "gate damping 2e-11",
               "graded damping 0.5e-11", "graded damping 1e-11", "graded damping 2e-11",
               "gate goal ff=1", "gate filtered")


def main() -> None:
    base_style()
    fig, axes = plt.subplots(1, 3, figsize=(12.4, 3.8), constrained_layout=True)

    # (a) freshness dose-response
    ax = axes[0]
    for key, color, marker in (("gate goal|ff=1", COLORS["gate goal"], "o"),
                               ("graded goal|ff=1", COLORS["graded goal"], "D")):
        for delay, style in (("0.1", "-"), ("0.2", (0, (4, 2)))):
            rates = [LAG[key][lag][delay]["failure_rate"] for lag in LAGS]
            ax.plot([float(l) * 1000 for l in LAGS], rates, marker=marker, color=color,
                    linestyle=style, markersize=6,
                    label=f"{key.split('|')[0]}, visual {float(delay)*1000:.0f} ms")
    for delay, style in (("0.1", "-"), ("0.2", (0, (4, 2)))):
        v = LAG["gate filtered"][delay]["failure_rate"]
        ax.axhline(v, color=COLORS["gate filtered"], linestyle=style, linewidth=1.4,
                   label=f"gate filtered, visual {float(delay)*1000:.0f} ms" if delay == "0.1" else None)
    ax.set_xlabel("self-state sample age (ms)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("a  self-state freshness (n = 8 per cell)")
    panel_label(ax, "a")
    ax.legend(loc="upper left", fontsize=6.8, frameon=False)

    # (b) goal onset decoupling
    ax = axes[1]
    for key, color, marker in (("gate goal|ff=0.5", COLORS["gate goal"], "o"),
                               ("gate goal|ff=1", COLORS["gate goal"], "s"),
                               ("graded goal|ff=1", COLORS["graded goal"], "D")):
        rates = [ONSET[key][o]["0.2"]["failure_rate"] for o in ONSETS]
        ax.plot([float(o) for o in ONSETS], rates, marker=marker, color=color,
                linestyle="-", markersize=6,
                label=key.replace("|ff=", " ff="))
    ax.axvline(0.5, color="#B8B8B6", linewidth=1.0)
    ax.text(0.5, 1.02, "bar onset", fontsize=7, color="#5A5A5A", ha="center")
    ax.set_xlabel("goal onset (s)")
    ax.set_ylabel("failure rate at 200 ms")
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("b  goal onset decoupling (n = 8 per cell)")
    panel_label(ax, "b")
    ax.legend(loc="center left", fontsize=7, frameon=False)

    # (c) damping vs goal
    ax = axes[2]
    x = range(len(DAMP_LABELS))
    rates = [DAMP[label]["0.2"]["failure_rate"] for label in DAMP_LABELS]
    colors = [COLORS["gate goal"] if "gate" in label else COLORS["graded goal"] for label in DAMP_LABELS]
    colors[-1] = COLORS["gate filtered"]
    markers = [MARKERS["gate goal"] if "gate" in label else MARKERS["graded goal"] for label in DAMP_LABELS]
    for i, (r, c) in enumerate(zip(rates, colors)):
        ax.plot([i], [r], marker=markers[i], color=c, markersize=8, linestyle="none")
    ax.plot(list(x), rates, color="#B8B8B6", linewidth=1.0, zorder=0)
    ax.set_xticks(list(x))
    ax.set_xticklabels(["0.5", "1", "2", "0.5", "1", "2", "goal\nff=1", "filtered"],
                       fontsize=7.5)
    ax.set_xlabel("feedforward gain (×10⁻¹¹)")
    ax.set_ylabel("failure rate at 200 ms")
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("c  damping without a goal (n = 8 per cell)")
    panel_label(ax, "c")
    ax.text(0.5, 1.02, "purple: gate   green: graded", fontsize=7, color="#5A5A5A", ha="left")

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
