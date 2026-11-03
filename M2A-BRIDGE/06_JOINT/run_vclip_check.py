#!/usr/bin/env python3
"""Sensitivity of the main failure ordering to the bar-velocity V-term treatment."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

V_MODES = ("clip", "smooth", "unclipped")
MODELS = ("addition", "graded_sensory", "graded_motor", "allnone", "allnone_motor")
DELAYS = (0.02, 0.05, 0.10, 0.14, 0.20)
SEEDS = (0, 1)
NOISE_SD = 1e-13
WINDOW = 6.0
BODY_SETS = ((6e-14, 2e-11), (6e-14, 1e-11), (1.2e-13, 1e-11), (2.4e-13, 1e-11))
GAINS = (2.5e-11, 5e-11)
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain, t_end_s=WINDOW)
    for inertia, drag in BODY_SETS
    for gain in GAINS
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def run_once(model: str, params: Params, delay: float, seed: int, mode: str) -> dict[str, object]:
    p = replace(params, v_mode=mode)
    time, _, readouts = simulate(
        model, p, delay_s=delay, grating_gain=p.k_opto, noise_sd=NOISE_SD, seed=seed
    )
    heading = readouts["heading"]
    omega = readouts["omega"]
    finite = np.isfinite(heading) & np.isfinite(omega)
    bad = (np.abs(heading) > HEADING_LIMIT) | (np.abs(omega) > OMEGA_LIMIT) | (~finite)
    failure = int(bad.any())
    return {
        "model": model,
        "v_mode": mode,
        "delay_s": delay,
        "seed": seed,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "window_s": WINDOW,
        "failure": failure,
        "failure_time_s": float(time[np.argmax(bad)]) if failure else float("nan"),
        "max_abs_heading_rad": float(np.nanmax(np.abs(heading))) if finite.any() else float("inf"),
        "max_abs_omega_rad_s": float(np.nanmax(np.abs(omega))) if finite.any() else float("inf"),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for model in MODELS:
            for delay in DELAYS:
                for seed in SEEDS:
                    for mode in V_MODES:
                        rows.append(run_once(model, params, delay, seed, mode))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model in MODELS:
        summary["grid"][model] = {}
        for delay in DELAYS:
            summary["grid"][model][f"{delay:g}"] = {}
            for mode in V_MODES:
                subset = [
                    row
                    for row in rows
                    if row["model"] == model
                    and abs(float(row["delay_s"]) - delay) < 1e-12
                    and row["v_mode"] == mode
                ]
                summary["grid"][model][f"{delay:g}"][mode] = {
                    "failure_rate": sum(int(row["failure"]) for row in subset) / len(subset),
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-VCLIP-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        for mode in V_MODES:
            row = run_once("allnone", replace(Params(dt_s=5e-4, t_end_s=1.0), v_mode=mode), 0.14, 0, mode)
            assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "vclip_check.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
