#!/usr/bin/env python3
"""Compare the source-style squared-error update with signed-error gradients."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from adaptive_model import simulate_adaptive
from ec_model import Params

MODES = ("source", "gradient", "gradient_neg")
DELAYS = (0.02, 0.05, 0.10, 0.20)
ALPHA = 8e-5
NOISE_SD = 1e-13
WINDOW = 6.0
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain, t_end_s=WINDOW)
    for inertia in (6e-14, 1.2e-13, 2.4e-13)
    for drag in (1e-11, 2e-11)
    for gain in (2.5e-11, 5e-11)
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def run_once(params: Params, delay: float, mode: str) -> dict[str, object]:
    result = simulate_adaptive(
        params,
        delay_s=delay,
        grating_gain=params.k_opto,
        seed=0,
        alpha=ALPHA,
        update_mode=mode,
    )
    heading = result.heading
    omega = result.omega
    finite = np.isfinite(heading) & np.isfinite(omega)
    bad = (np.abs(heading) > HEADING_LIMIT) | (np.abs(omega) > OMEGA_LIMIT) | (~finite)
    failure = int(bad.any())
    return {
        "update_mode": mode,
        "delay_s": delay,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "window_s": WINDOW,
        "failure": failure,
        "failure_time_s": float(result.time[np.argmax(bad)]) if failure else float("nan"),
        "mean_ro": float(np.nanmean(result.ro)),
        "final_ro": float(result.ro[-1]),
        "max_abs_heading_rad": float(np.nanmax(np.abs(heading))) if finite.any() else float("inf"),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for delay in DELAYS:
            for mode in MODES:
                rows.append(run_once(params, delay, mode))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for mode in MODES:
        summary["grid"][mode] = {}
        for delay in DELAYS:
            subset = [
                row
                for row in rows
                if row["update_mode"] == mode and abs(float(row["delay_s"]) - delay) < 1e-12
            ]
            summary["grid"][mode][f"{delay:g}"] = {
                "failure_rate": sum(int(row["failure"]) for row in subset) / len(subset),
                "mean_ro": float(np.nanmean([float(row["mean_ro"]) for row in subset])),
                "final_ro": float(np.nanmean([float(row["final_ro"]) for row in subset])),
                "n": len(subset),
            }
    return summary


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-ADAPTIVE-03/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        for mode in MODES:
            row = run_once(replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0), 0.05, mode)
            assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "adaptive_gradient.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
