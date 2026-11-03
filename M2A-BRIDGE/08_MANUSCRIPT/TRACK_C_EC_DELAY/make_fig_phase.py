#!/usr/bin/env python3
"""Body-parameter phase diagram: gate filtered versus gate goal."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fig_style import base_style, panel_label

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
OUT = Path(__file__).resolve().parent / "fig_phase.png"
GRID = json.loads((ROOT / "runs/P1-EC-PHASE-01/experiment/outputs/summary.json").read_text())["grid"]

INERTIAS = ("3e-14", "6e-14", "0.00012", "0.00024")
# summary keys use Python %g formatting of the floats
INERTIA_KEYS = tuple(sorted(GRID["gate filtered|ff=0"], key=float))
DRAG_KEYS = tuple(sorted(GRID["gate filtered|ff=0"][INERTIA_KEYS[0]], key=float))
DELAYS = ("0.02", "0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.4")


def matrix(label: str) -> np.ndarray:
    """Rows = inertia (slow body at bottom), columns = delay; mean over drags and gains."""
    grid = GRID[label]
    rows = []
    for inertia in reversed(INERTIA_KEYS):  # large inertia at top
        row = []
        for delay in DELAYS:
            vals = [
                grid[inertia][drag][delay]["failure_rate"]
                for drag in DRAG_KEYS
            ]
            row.append(float(np.mean(vals)))
        rows.append(row)
    return np.array(rows)


def main() -> None:
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6), constrained_layout=True)

    vmax = 1.0
    for ax, label, letter, title in (
        (axes[0], "gate filtered|ff=0", "a", "gate filtered"),
        (axes[1], "gate goal|ff=1", "b", "gate goal ff=1"),
    ):
        m = matrix(label)
        im = ax.imshow(m, cmap="Purples", vmin=0.0, vmax=vmax,
                       aspect="auto", origin="lower")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels([f"{int(float(d)*1000)}" for d in DELAYS])
        ax.set_yticks(range(len(INERTIA_KEYS)))
        ax.set_yticklabels([f"{float(k)*1e14:g}" for k in reversed(INERTIA_KEYS)])
        ax.set_xlabel("visual delay (ms)")
        ax.set_ylabel("inertia (×10⁻¹⁴ kg m²)")
        ax.grid(False)
        ax.set_title(f"{letter}  {title} (mean over drags and grating gains)")
        panel_label(ax, letter)
        # annotate cells
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                v = m[i, j]
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=7, color="#1A1A1A" if v < 0.55 else "#FFFFFF")
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cbar.set_label("failure rate", fontsize=8)
        cbar.ax.tick_params(labelsize=7)

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
