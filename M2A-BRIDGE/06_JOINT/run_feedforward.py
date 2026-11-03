#!/usr/bin/env python3
"""Goal-based feedforward experiment.

Compares the delayed feedback controller with a goal feedforward branch. The
goal trajectory is instructed (amplitude, onset, time constant), and the
feedforward torque uses current proprioception, not delayed vision. The
efference copy or gate uses the filtered bar torque plus the feedforward term.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

MODEL_SPECS = (
    ("addition", "addition", False),
    ("graded_sensory", "graded filtered", False),
    ("graded_command", "graded command", False),
    ("graded_goal", "graded goal", True),
    ("allnone", "gate filtered", False),
    ("gate_command", "gate command", False),
    ("gate_goal", "gate goal", True),
)
FF_GAINS = (0.0, 0.25, 0.5, 0.75, 1.0)
DELAYS = (0.02, 0.05, 0.10, 0.14, 0.20)
SEEDS = (0,)
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


def gains_for(is_goal: bool) -> tuple[float, ...]:
    return FF_GAINS if is_goal else (0.0,)


def run_once(
    model: str,
    params: Params,
    delay: float,
    seed: int,
    ff_gain: float,
) -> dict[str, object]:
    p = replace(params, ff_gain=ff_gain)
    time, _, readouts = simulate(
        model, p, delay_s=delay, grating_gain=p.k_opto, noise_sd=NOISE_SD, seed=seed
    )
    heading = readouts["heading"]
    omega = readouts["omega"]
    finite = np.isfinite(heading) & np.isfinite(omega)
    bad = (np.abs(heading) > HEADING_LIMIT) | (np.abs(omega) > OMEGA_LIMIT) | (~finite)
    failure = int(bad.any())
    row = {
        "model": model,
        "delay_s": delay,
        "seed": seed,
        "ff_gain": ff_gain,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "window_s": WINDOW,
        "failure": failure,
        "failure_time_s": float(time[np.argmax(bad)]) if failure else float("nan"),
        "max_abs_heading_rad": float(np.nanmax(np.abs(heading))) if finite.any() else float("inf"),
        "mean_omega_ec": float(np.nanmean(readouts["omega_ec"])) if "omega_ec" in readouts else float("nan"),
        "gate_duty": float(np.nanmean(readouts["gate_closed"])) if "gate_closed" in readouts else float("nan"),
    }
    return row


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for model, _, is_goal in MODEL_SPECS:
            for ff_gain in gains_for(is_goal):
                for delay in DELAYS:
                    for seed in SEEDS:
                        rows.append(run_once(model, params, delay, seed, ff_gain))
    return rows


def _nanmean(values: list[float]) -> float:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    return float(finite.mean()) if finite.size else float("nan")


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model, label, is_goal in MODEL_SPECS:
        summary["grid"][label] = {}
        for ff_gain in gains_for(is_goal):
            key = f"{ff_gain:g}"
            summary["grid"][label][key] = {}
            for delay in DELAYS:
                subset = [
                    row
                    for row in rows
                    if row["model"] == model
                    and abs(float(row["ff_gain"]) - ff_gain) < 1e-12
                    and abs(float(row["delay_s"]) - delay) < 1e-12
                ]
                summary["grid"][label][key][f"{delay:g}"] = {
                    "failure_rate": sum(int(row["failure"]) for row in subset) / len(subset),
                    "mean_omega_ec": _nanmean([float(row["mean_omega_ec"]) for row in subset]),
                    "gate_duty": _nanmean([float(row["gate_duty"]) for row in subset]),
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-FEEDFORWARD-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n_models = sum(len(gains_for(is_goal)) for _, _, is_goal in MODEL_SPECS)
        print(
            f"DRY RUN: {n_models} model-gain combos x {len(DELAYS)} delays x "
            f"{len(SEEDS)} seeds x {len(PARAMETER_SETS)} parameter sets = "
            f"{n_models * len(DELAYS) * len(SEEDS) * len(PARAMETER_SETS)} runs"
        )
        return 0
    if args.selftest:
        for model, _, is_goal in MODEL_SPECS:
            for ff_gain in gains_for(is_goal):
                row = run_once(
                    model,
                    replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0),
                    0.05,
                    0,
                    ff_gain,
                )
                assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "feedforward.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
