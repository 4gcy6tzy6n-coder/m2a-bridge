#!/usr/bin/env python3
"""Self-state freshness dose-response: how old can the self-state sample be?"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

MODELS = (
    ("gate_goal", "gate goal", 1.0),
    ("graded_goal", "graded goal", 1.0),
)
LAGS = (0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.10, 0.20)
VISUAL_DELAYS = (0.10, 0.20)
REFERENCE = ("allnone", "gate filtered")  # lag not applicable
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
    delay: float,
    seed: int,
    ff_gain: float,
    lag: float,
) -> dict[str, object]:
    p = replace(params, ff_gain=ff_gain, ff_self_state_lag_s=lag)
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
        "ff_self_state_lag_s": lag,
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
        for model, _, ff_gain in MODELS:
            for lag in LAGS:
                for delay in VISUAL_DELAYS:
                    for seed in SEEDS:
                        rows.append(run_once(model, params, delay, seed, ff_gain, lag))
        for delay in VISUAL_DELAYS:
            for seed in SEEDS:
                rows.append(run_once(REFERENCE[0], params, delay, seed, 0.0, 0.0))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for model, label, _ in MODELS:
        key = f"{label}|ff=1"
        summary["grid"][key] = {}
        for lag in LAGS:
            lkey = f"{lag:g}"
            summary["grid"][key][lkey] = {}
            for delay in VISUAL_DELAYS:
                subset = [
                    row for row in rows
                    if row["model"] == model
                    and abs(float(row["ff_self_state_lag_s"]) - lag) < 1e-12
                    and abs(float(row["delay_s"]) - delay) < 1e-12
                ]
                summary["grid"][key][lkey][f"{delay:g}"] = {
                    "failure_rate": sum(int(r["failure"]) for r in subset) / len(subset),
                    "n": len(subset),
                }
    ref_key = "gate filtered"
    summary["grid"][ref_key] = {}
    for delay in VISUAL_DELAYS:
        subset = [
            row for row in rows
            if row["model"] == "allnone" and abs(float(row["delay_s"]) - delay) < 1e-12
        ]
        summary["grid"][ref_key][f"{delay:g}"] = {
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
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-SELFSTATE-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n = len(MODELS) * len(LAGS) * len(VISUAL_DELAYS) * len(SEEDS) * len(PARAMETER_SETS)
        n += len(VISUAL_DELAYS) * len(SEEDS) * len(PARAMETER_SETS)
        print(f"DRY RUN: {len(MODELS)} models x {len(LAGS)} lags x {len(VISUAL_DELAYS)} visual delays x 8 params + refs = {n} runs")
        return 0
    if args.selftest:
        for model, _, ff_gain in MODELS:
            row = run_once(model, replace(Params(dt_s=5e-4, t_end_s=1.0), t_end_s=1.0), 0.05, 0, ff_gain, 0.02)
            assert "failure" in row
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "selfstate_lag.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
