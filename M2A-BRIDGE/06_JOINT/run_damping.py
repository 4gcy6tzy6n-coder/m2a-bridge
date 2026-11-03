#!/usr/bin/env python3
"""No-goal control: pure current-state damping versus goal tracking."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

# (model, label, ff_mode, ff_damp_gain or None for goal reference)
SPECS = (
    ("gate_goal", "gate damping 0.5e-11", "damping", 0.5e-11),
    ("gate_goal", "gate damping 1e-11", "damping", 1e-11),
    ("gate_goal", "gate damping 2e-11", "damping", 2e-11),
    ("graded_goal", "graded damping 0.5e-11", "damping", 0.5e-11),
    ("graded_goal", "graded damping 1e-11", "damping", 1e-11),
    ("graded_goal", "graded damping 2e-11", "damping", 2e-11),
    ("gate_goal", "gate goal ff=1", "goal", None),
    ("allnone", "gate filtered", "goal", None),
)
DELAYS = (0.05, 0.10, 0.20)
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


def run_once(model: str, params: Params, delay: float, seed: int, ff_mode: str, damp: float | None) -> dict[str, object]:
    ff_gain = 0.0 if damp is None and model == "allnone" else 1.0
    p = replace(
        params,
        ff_gain=ff_gain,
        ff_mode=ff_mode,
        ff_damp_gain=1e-11 if damp is None else damp,
    )
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
        "delay_s": delay,
        "seed": seed,
        "ff_mode": ff_mode,
        "ff_damp_gain": 1e-11 if damp is None else damp,
        "window_s": WINDOW,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "failure": failure,
        "failure_time_s": float(time[np.argmax(bad)]) if failure else float("nan"),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for model, _, ff_mode, damp in SPECS:
            for delay in DELAYS:
                for seed in SEEDS:
                    rows.append(run_once(model, params, delay, seed, ff_mode, damp))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model, label, ff_mode, damp in SPECS:
        summary["grid"][label] = {}
        for delay in DELAYS:
            subset = [
                row for row in rows
                if row["model"] == model
                and row["ff_mode"] == ff_mode
                and abs(float(row["ff_damp_gain"]) - (1e-11 if damp is None else damp)) < 1e-30
                and abs(float(row["delay_s"]) - delay) < 1e-12
            ]
            summary["grid"][label][f"{delay:g}"] = {
                "failure_rate": sum(int(r["failure"]) for r in subset) / len(subset),
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-DAMP-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n = len(SPECS) * len(DELAYS) * len(SEEDS) * len(PARAMETER_SETS)
        print(f"DRY RUN: {len(SPECS)} combos x {len(DELAYS)} delays x 8 params = {n} runs")
        return 0
    if args.selftest:
        for model, _, ff_mode, damp in SPECS:
            row = run_once(model, replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0), 0.05, 0, ff_mode, damp)
            assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "damping.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
