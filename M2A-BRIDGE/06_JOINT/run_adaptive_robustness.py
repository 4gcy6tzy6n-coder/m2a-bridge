#!/usr/bin/env python3
"""Learning-rate and seed robustness of the adaptive graded EC model."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from adaptive_model import simulate_adaptive
from ec_model import Params

ALPHAS = (1e-5, 8e-5, 5e-4, 1e-3)
SEEDS = (0, 1, 2)
DELAYS = (0.02, 0.05, 0.10, 0.20)
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain)
    for inertia in (6e-14, 1.2e-13, 2.4e-13)
    for drag in (1e-11, 2e-11)
    for gain in (2.5e-11, 5e-11)
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def run_once(params: Params, delay: float, alpha: float, seed: int) -> dict[str, object]:
    result = simulate_adaptive(
        params, delay_s=delay, grating_gain=params.k_opto, seed=seed, alpha=alpha
    )
    heading = result.heading
    omega = result.omega
    finite = bool(np.isfinite(heading).all() and np.isfinite(omega).all())
    max_heading = float(np.nanmax(np.abs(heading))) if finite else float("inf")
    max_omega = float(np.nanmax(np.abs(omega))) if finite else float("inf")
    failure = int((not finite) or max_heading > HEADING_LIMIT or max_omega > OMEGA_LIMIT)
    return {
        "alpha": alpha,
        "seed": seed,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "delay_s": delay,
        "failure": failure,
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "mean_ro": float(np.nanmean(result.ro)),
        "final_ro": float(result.ro[-1]),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for delay in DELAYS:
            for alpha in ALPHAS:
                for seed in SEEDS:
                    rows.append(run_once(params, delay, alpha, seed))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for alpha in ALPHAS:
        summary["grid"][f"{alpha:g}"] = {}
        for delay in DELAYS:
            subset = [
                row
                for row in rows
                if abs(float(row["alpha"]) - alpha) < 1e-15
                and abs(float(row["delay_s"]) - delay) < 1e-12
            ]
            summary["grid"][f"{alpha:g}"][f"{delay:g}"] = {
                "failure_rate": sum(int(row["failure"]) for row in subset) / len(subset),
                "mean_ro": float(np.nanmean([float(row["mean_ro"]) for row in subset])),
            }
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

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)
    for ax, key, title in zip(
        axes, ("failure_rate", "mean_ro"), ("failure rate", "mean learned gain")
    ):
        matrix = np.array(
            [
                [summary["grid"][f"{a:g}"][f"{d:g}"][key] for d in DELAYS]
                for a in ALPHAS
            ]
        )
        image = ax.imshow(matrix, aspect="auto", origin="lower", cmap="magma")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels([f"{d:g}" for d in DELAYS])
        ax.set_yticks(range(len(ALPHAS)))
        ax.set_yticklabels([f"{a:g}" for a in ALPHAS])
        ax.set_xlabel("delay (s)")
        ax.set_title(title)
        fig.colorbar(image, ax=ax, shrink=0.9)
    axes[0].set_ylabel("learning rate alpha")
    fig.savefig(out_dir / "adaptive_alpha_heatmap.png", dpi=220)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-ADAPTIVE-02/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        row = run_once(Params(dt_s=5e-4, t_end_s=0.8), 0.05, 8e-5, 0)
        assert "failure" in row and np.isfinite(row["mean_ro"])
        print("SELFTEST PASS", row["mean_ro"])
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "adaptive_alpha_sweep.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    make_figure(summary, args.output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
