#!/usr/bin/env python3
"""Sweep the graded efference-copy gain under feedback delay.

Question: does graded cancellation help, do nothing, or hurt as a function of
the EC gain and the feedback delay? Gating variants are included as controls.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import MODELS, Params, simulate

EC_GAINS = (0.0, 0.05, 0.25, 0.5, 0.75, 1.0)
DELAYS = (0.02, 0.05, 0.10, 0.20)
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain)
    for inertia in (6e-14, 1.2e-13, 2.4e-13)
    for drag in (1e-11, 2e-11)
    for gain in (2.5e-11, 5e-11)
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def run_once(model: str, params: Params, delay_s: float) -> dict[str, object]:
    _, _, readouts = simulate(model, params, delay_s=delay_s, grating_gain=params.k_opto)
    heading = readouts["heading"]
    omega = readouts["omega"]
    finite = bool(np.isfinite(heading).all() and np.isfinite(omega).all())
    max_heading = float(np.nanmax(np.abs(heading))) if finite else float("inf")
    max_omega = float(np.nanmax(np.abs(omega))) if finite else float("inf")
    failure = int((not finite) or max_heading > HEADING_LIMIT or max_omega > OMEGA_LIMIT)
    return {
        "model": model,
        "ec_gain": params.ec_gain,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "delay_s": float(delay_s),
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "failure": failure,
        "finite": int(finite),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for model in MODELS:
            for ec_gain in EC_GAINS:
                for delay in DELAYS:
                    rows.append(run_once(model, replace(params, ec_gain=ec_gain), delay))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model in MODELS:
        summary["grid"][model] = {}
        for ec_gain in EC_GAINS:
            key = f"{ec_gain:g}"
            summary["grid"][model][key] = {}
            for delay in DELAYS:
                subset = [
                    row
                    for row in rows
                    if row["model"] == model
                    and abs(float(row["ec_gain"]) - ec_gain) < 1e-12
                    and abs(float(row["delay_s"]) - delay) < 1e-12
                ]
                summary["grid"][model][key][f"{delay:g}"] = sum(
                    int(row["failure"]) for row in subset
                ) / len(subset)
    return summary


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_figure(summary: dict[str, object], out_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    panels = ("graded_sensory", "allnone", "allnone_motor")
    for ax, model in zip(axes, panels):
        grid = summary["grid"][model]
        matrix = np.array(
            [[grid[f"{g:g}"][f"{d:g}"] for d in DELAYS] for g in EC_GAINS]
        )
        image = ax.imshow(matrix, aspect="auto", origin="lower", vmin=0, vmax=1, cmap="magma")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels([f"{d:g}" for d in DELAYS])
        ax.set_yticks(range(len(EC_GAINS)))
        ax.set_yticklabels([f"{g:g}" for g in EC_GAINS])
        ax.set_xlabel("delay (s)")
        ax.set_title(model)
    axes[0].set_ylabel("EC gain")
    fig.colorbar(image, ax=axes, label="failure rate")
    fig.tight_layout()
    fig.savefig(out_dir / "gain_delay_heatmap.png", dpi=220)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-GAIN-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        rows = [run_once("graded_sensory", replace(Params(dt_s=5e-4), ec_gain=0.05), 0.05)]
        assert rows and "failure" in rows[0]
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "gain_sweep.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    make_figure(summary, args.output_dir)
    print(json.dumps(summary["grid"]["graded_sensory"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
