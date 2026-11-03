#!/usr/bin/env python3
"""Ablation: does the feedforward benefit require current self-state?

The goal branch can use current proprioception (heading, omega) or the same
delayed values as the visual feedback path. If the benefit requires current
self-state, delaying it should remove the rescue.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

SPECS = (
    ("graded_goal", "graded goal", 1.0),
    ("gate_goal", "gate goal", 0.5),
    ("gate_goal", "gate goal", 1.0),
)
SELF_STATES = ("current", "delayed")
VISUAL_DELAYS = (0.10, 0.20)
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


def run_once(
    model: str,
    params: Params,
    visual_delay: float,
    seed: int,
    ff_gain: float,
    ff_self_state: str,
) -> dict[str, object]:
    p = replace(params, ff_gain=ff_gain, ff_self_state=ff_self_state)
    time, _, readouts = simulate(
        model, p, delay_s=visual_delay, grating_gain=p.k_opto, noise_sd=NOISE_SD, seed=seed
    )
    heading = readouts["heading"]
    omega = readouts["omega"]
    finite = np.isfinite(heading) & np.isfinite(omega)
    bad = (np.abs(heading) > HEADING_LIMIT) | (np.abs(omega) > OMEGA_LIMIT) | (~finite)
    failure = int(bad.any())
    return {
        "model": model,
        "visual_delay_s": visual_delay,
        "ff_self_state": ff_self_state,
        "seed": seed,
        "ff_gain": ff_gain,
        "window_s": WINDOW,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "failure": failure,
        "failure_time_s": float(time[np.argmax(bad)]) if failure else float("nan"),
        "max_abs_heading_rad": float(np.nanmax(np.abs(heading))) if finite.any() else float("inf"),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for model, _, ff_gain in SPECS:
            for ff_self_state in SELF_STATES:
                for visual_delay in VISUAL_DELAYS:
                    for seed in SEEDS:
                        rows.append(
                            run_once(model, params, visual_delay, seed, ff_gain, ff_self_state)
                        )
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model, label, ff_gain in SPECS:
        key = f"{label}|ff={ff_gain:g}"
        summary["grid"][key] = {}
        for ff_self_state in SELF_STATES:
            summary["grid"][key][ff_self_state] = {}
            for visual_delay in VISUAL_DELAYS:
                subset = [
                    row
                    for row in rows
                    if row["model"] == model
                    and abs(float(row["ff_gain"]) - ff_gain) < 1e-12
                    and row["ff_self_state"] == ff_self_state
                    and abs(float(row["visual_delay_s"]) - visual_delay) < 1e-12
                ]
                summary["grid"][key][ff_self_state][f"{visual_delay:g}"] = {
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-FF-STATE-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n = len(SPECS) * len(SELF_STATES) * len(VISUAL_DELAYS) * len(SEEDS) * len(PARAMETER_SETS)
        print(f"DRY RUN: {len(SPECS)} combos x {len(SELF_STATES)} self-states x {len(VISUAL_DELAYS)} visual delays x {len(SEEDS)} seed x 8 params = {n} runs")
        return 0
    if args.selftest:
        for model, _, ff_gain in SPECS:
            for ff_self_state in SELF_STATES:
                row = run_once(
                    model,
                    replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0),
                    0.1,
                    0,
                    ff_gain,
                    ff_self_state,
                )
                assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "ff_state.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
