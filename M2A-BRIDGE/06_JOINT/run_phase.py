#!/usr/bin/env python3
"""Body-parameter phase diagram: when does the feedforward rescue hold?

Sweeps body inertia and drag against visual delay for the gate variants,
mirroring the earlier phase-diagram round.
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
    ("allnone", "gate filtered", 0.0),
    ("gate_goal", "gate goal", 1.0),
)
INERTIAS = (3e-14, 6e-14, 1.2e-13, 2.4e-13)
DRAGS = (0.5e-11, 1e-11, 2e-11)
GRATING_GAINS = (2.5e-11, 5e-11)
DELAYS = (0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40)
SEEDS = (0,)
NOISE_SD = 1e-13
WINDOW = 6.0
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


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
    return {
        "model": model,
        "delay_s": delay,
        "seed": seed,
        "ff_gain": ff_gain,
        "inertia": params.inertia,
        "drag": params.drag,
        "body_tau_s": params.inertia / params.drag,
        "k_opto": params.k_opto,
        "window_s": WINDOW,
        "failure": failure,
        "failure_time_s": float(time[np.argmax(bad)]) if failure else float("nan"),
        "max_abs_heading_rad": float(np.nanmax(np.abs(heading))) if finite.any() else float("inf"),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for inertia in INERTIAS:
        for drag in DRAGS:
            for k_opto in GRATING_GAINS:
                params = replace(
                    Params(), inertia=inertia, drag=drag, k_opto=k_opto, t_end_s=WINDOW
                )
                for model, _, ff_gain in SPECS:
                    for delay in DELAYS:
                        for seed in SEEDS:
                            rows.append(run_once(model, params, delay, seed, ff_gain))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model, label, ff_gain in SPECS:
        key = f"{label}|ff={ff_gain:g}"
        summary["grid"][key] = {}
        for inertia in INERTIAS:
            ikey = f"{inertia:g}"
            summary["grid"][key][ikey] = {}
            for drag in DRAGS:
                dkey = f"{drag:g}"
                summary["grid"][key][ikey][dkey] = {}
                for delay in DELAYS:
                    subset = [
                        row
                        for row in rows
                        if row["model"] == model
                        and abs(float(row["ff_gain"]) - ff_gain) < 1e-12
                        and abs(float(row["inertia"]) - inertia) < 1e-30
                        and abs(float(row["drag"]) - drag) < 1e-30
                        and abs(float(row["delay_s"]) - delay) < 1e-12
                    ]
                    summary["grid"][key][ikey][dkey][f"{delay:g}"] = {
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-PHASE-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n = (
            len(INERTIAS)
            * len(DRAGS)
            * len(GRATING_GAINS)
            * len(SPECS)
            * len(DELAYS)
            * len(SEEDS)
        )
        print(f"DRY RUN: {len(INERTIAS)} inertias x {len(DRAGS)} drags x {len(GRATING_GAINS)} gains x {len(SPECS)} models x {len(DELAYS)} delays = {n} runs")
        return 0
    if args.selftest:
        params = replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0)
        for model, _, ff_gain in SPECS:
            row = run_once(model, params, 0.1, 0, ff_gain)
            assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "phase.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
