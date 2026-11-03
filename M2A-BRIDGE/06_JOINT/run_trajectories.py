#!/usr/bin/env python3
"""Save example trajectories for the mechanism figure."""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

SPECS = (
    ("addition", "addition", 0.0),
    ("graded_sensory", "graded filtered", 0.0),
    ("allnone", "gate filtered", 0.0),
    ("gate_goal", "gate goal", 1.0),
)
DELAY = 0.20
SEED = 0
NOISE_SD = 1e-13
WINDOW = 10.0
PARAMS = replace(Params(), inertia=6e-14, drag=2e-11, k_opto=2.5e-11, t_end_s=WINDOW)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-TRAJ-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(f"DRY RUN: {len(SPECS)} trajectories x delay {DELAY} s x window {WINDOW} s")
        return 0
    if args.selftest:
        for model, _, ff_gain in SPECS:
            time, _, readouts = simulate(
                model,
                replace(PARAMS, ff_gain=ff_gain, dt_s=5e-4, t_end_s=1.0),
                delay_s=DELAY,
                grating_gain=PARAMS.k_opto,
                noise_sd=NOISE_SD,
                seed=SEED,
            )
            assert time.size > 0 and "heading" in readouts
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"delay_s": DELAY, "seed": SEED, "noise_sd": NOISE_SD, "window_s": WINDOW, "runs": []}
    for model, label, ff_gain in SPECS:
        time, _, readouts = simulate(
            model,
            replace(PARAMS, ff_gain=ff_gain),
            delay_s=DELAY,
            grating_gain=PARAMS.k_opto,
            noise_sd=NOISE_SD,
            seed=SEED,
        )
        payload = {
            "time": time,
            "heading": readouts["heading"],
            "omega": readouts["omega"],
            "theta_bar": readouts["theta_bar"],
            "f_grating": readouts["f_grating"],
        }
        if "gate_closed" in readouts:
            payload["gate_closed"] = readouts["gate_closed"]
        if "omega_ec" in readouts:
            payload["omega_ec"] = readouts["omega_ec"]
        np.savez_compressed(args.output_dir / f"{label.replace(' ', '_')}.npz", **payload)
        manifest["runs"].append(
            {
                "model": model,
                "label": label,
                "ff_gain": ff_gain,
                "file": f"{label.replace(' ', '_')}.npz",
                "final_heading_rad": float(readouts["heading"][-1]),
            }
        )
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
