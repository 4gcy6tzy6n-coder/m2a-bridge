#!/usr/bin/env python3
"""True command-copy experiment.

Compares three signals used by the efference copy or gate:
- filtered plant-state F_bar (post-filter)
- command copy u_t (pre-plant-filter, based on the delayed visual estimate)
- current visual drive (oracle control, undelayed visual state)
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
    ("addition", "addition"),
    ("graded_sensory", "graded filtered"),
    ("graded_command", "graded command"),
    ("graded_motor", "graded unfiltered oracle"),
    ("allnone", "gate filtered"),
    ("gate_command", "gate command"),
    ("allnone_motor", "gate unfiltered oracle"),
)
EC_GAINS = (0.05, 1.0)
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
LABELS = dict(MODEL_SPECS)


def run_once(model: str, params: Params, delay: float, seed: int, ec_gain: float) -> dict[str, object]:
    p = replace(params, ec_gain=ec_gain)
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
        "label": LABELS[model],
        "ec_gain": ec_gain,
        "delay_s": delay,
        "seed": seed,
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
        for model, _ in MODEL_SPECS:
            for delay in DELAYS:
                for seed in SEEDS:
                    for ec_gain in EC_GAINS:
                        rows.append(run_once(model, params, delay, seed, ec_gain))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model, label in MODEL_SPECS:
        summary["grid"][label] = {}
        for gain in EC_GAINS:
            summary["grid"][label][f"{gain:g}"] = {}
            for delay in DELAYS:
                subset = [
                    row
                    for row in rows
                    if row["model"] == model
                    and abs(float(row["ec_gain"]) - gain) < 1e-12
                    and abs(float(row["delay_s"]) - delay) < 1e-12
                ]
                summary["grid"][label][f"{gain:g}"][f"{delay:g}"] = {
                    "failure_rate": sum(int(row["failure"]) for row in subset) / len(subset),
                    "mean_omega_ec": float(np.nanmean([float(row["mean_omega_ec"]) for row in subset])),
                    "gate_duty": float(np.nanmean([float(row["gate_duty"]) for row in subset])),
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-COMMAND-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        for model, _ in MODEL_SPECS:
            row = run_once(model, replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0), 0.05, 0, 0.05)
            assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "command_copy.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
