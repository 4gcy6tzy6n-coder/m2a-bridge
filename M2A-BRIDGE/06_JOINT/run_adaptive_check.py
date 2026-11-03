#!/usr/bin/env python3
"""Compare adaptive graded EC with fixed gains and gating under delay."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from adaptive_model import simulate_adaptive
from ec_model import Params, simulate

DELAYS = (0.02, 0.05, 0.10, 0.20)
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain)
    for inertia in (6e-14, 1.2e-13, 2.4e-13)
    for drag in (1e-11, 2e-11)
    for gain in (2.5e-11, 5e-11)
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def classify(heading: np.ndarray, omega: np.ndarray) -> tuple[int, float, float]:
    finite = bool(np.isfinite(heading).all() and np.isfinite(omega).all())
    max_heading = float(np.nanmax(np.abs(heading))) if finite else float("inf")
    max_omega = float(np.nanmax(np.abs(omega))) if finite else float("inf")
    failure = int((not finite) or max_heading > HEADING_LIMIT or max_omega > OMEGA_LIMIT)
    return failure, max_heading, max_omega


def run_adaptive(params: Params, delay: float) -> dict[str, object]:
    result = simulate_adaptive(params, delay_s=delay, grating_gain=params.k_opto)
    failure, max_heading, max_omega = classify(result.heading, result.omega)
    return {
        "model": "graded_adaptive",
        "ec_gain": "learned",
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "delay_s": delay,
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "failure": failure,
        "mean_ro": float(np.nanmean(result.ro)),
        "final_ro": float(result.ro[-1]),
    }


def run_fixed(model: str, params: Params, delay: float, label: str | None = None) -> dict[str, object]:
    _, _, readouts = simulate(model, params, delay_s=delay, grating_gain=params.k_opto)
    failure, max_heading, max_omega = classify(readouts["heading"], readouts["omega"])
    return {
        "model": label or model,
        "ec_gain": params.ec_gain,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "delay_s": delay,
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "failure": failure,
        "mean_ro": float("nan"),
        "final_ro": float("nan"),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for delay in DELAYS:
            rows.append(run_adaptive(params, delay))
            rows.append(
                run_fixed(
                    "graded_sensory",
                    replace(params, ec_gain=0.05),
                    delay,
                    label="graded_fixed_0.05",
                )
            )
            rows.append(
                run_fixed(
                    "graded_sensory",
                    replace(params, ec_gain=1.0),
                    delay,
                    label="graded_fixed_1.0",
                )
            )
            rows.append(run_fixed("addition", params, delay))
            rows.append(run_fixed("allnone", params, delay))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "models": {}}
    for model in sorted({str(row["model"]) for row in rows}):
        summary["models"][model] = {}
        for delay in DELAYS:
            subset = [
                row
                for row in rows
                if row["model"] == model and abs(float(row["delay_s"]) - delay) < 1e-12
            ]
            ro_values = [
                float(row["mean_ro"]) for row in subset if np.isfinite(float(row["mean_ro"]))
            ]
            summary["models"][model][f"{delay:g}"] = {
                "failure_rate": sum(int(row["failure"]) for row in subset) / len(subset),
                "mean_ro": float(np.mean(ro_values)) if ro_values else None,
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-ADAPTIVE-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        row = run_adaptive(Params(dt_s=5e-4, t_end_s=0.8), 0.05)
        assert "failure" in row and np.isfinite(row["mean_ro"])
        print("SELFTEST PASS", row["mean_ro"])
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "adaptive_check.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
