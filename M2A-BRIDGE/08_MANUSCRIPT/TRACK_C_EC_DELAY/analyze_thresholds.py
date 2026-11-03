#!/usr/bin/env python3
"""Reclassify P3 failures under alternative thresholds.

No new simulation: reads sweep_fine.csv and recomputes the first failing delay
for heading limits of pi, 2*pi, 4*pi and omega limits of 50, 100, 200 rad/s.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
SWEEP = ROOT / "runs/P1-EC-DELAY-03/experiment/outputs/sweep_fine.csv"
OUT = Path(__file__).resolve().parent / "threshold_sensitivity.json"

MODELS = ("addition", "graded_sensory", "graded_motor", "allnone_motor", "allnone")
HEADING_LIMITS = {"pi": np.pi, "2pi": 2 * np.pi, "4pi": 4 * np.pi}
OMEGA_LIMITS = {"50": 50.0, "100": 100.0, "200": 200.0}
PARAM_KEYS = ("inertia", "drag", "k_opto")


def main() -> None:
    with SWEEP.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("inertia", "drag", "k_opto", "delay_s", "max_abs_heading_rad", "max_abs_omega_rad_s"):
            row[key] = float(row[key])

    result: dict[str, object] = {}
    for heading_name, heading_limit in HEADING_LIMITS.items():
        for omega_name, omega_limit in OMEGA_LIMITS.items():
            key = f"heading>{heading_name}_omega>{omega_name}"
            result[key] = {}
            for model in MODELS:
                critical = []
                for params in {(row["inertia"], row["drag"], row["k_opto"]) for row in rows}:
                    subset = [
                        row
                        for row in rows
                        if row["model"] == model
                        and (row["inertia"], row["drag"], row["k_opto"]) == params
                    ]
                    failures = [
                        row["delay_s"]
                        for row in subset
                        if row["max_abs_heading_rad"] > heading_limit
                        or row["max_abs_omega_rad_s"] > omega_limit
                    ]
                    critical.append(min(failures) if failures else max(row["delay_s"] for row in subset))
                result[key][model] = {
                    "critical_delays_s": sorted(critical),
                    "median_s": float(np.median(critical)),
                }

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{'threshold':32} " + " ".join(f"{model:>16}" for model in MODELS))
    for key, models in result.items():
        print(f"{key:32} " + " ".join(f"{models[model]['median_s']:>16.3f}" for model in MODELS))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
