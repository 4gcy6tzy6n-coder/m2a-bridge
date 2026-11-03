#!/usr/bin/env python3
"""P2-OBSERVER-02 (D13): do classical control methods explain Track C's advantage?

Comparators at discriminating delays, same parameter grid as the feedforward
sweeps (8 body-gain sets, 6 s window, noise {0, 1e-13}):
  addition      delayed filtered steering (baseline)
  allnone       gate filtered
  gate_goal ff=1  gated rescue with instantaneous self-state (reference)
  pd_instant    instantaneous classical PD, no gating
  smith         delayed-only forward-model observer, exact internal model
  smith_pert    same observer, 10% drag/inertia mismatch

Pre-stated readings (owner D13):
  - if a full dynamics observer (smith) rescues, Taylor insufficiency does NOT
    imply real instantaneous proprioception is required;
  - if pd_instant matches gate_goal, gating has no independent contribution
    given instantaneous state. Negative results are reported as-is.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

# (model, label, ff_gain, ff_mode, ff_self_state)
SPECS = (
    ("addition", "delayed filtered baseline", 0.0, "goal", "current"),
    ("allnone", "gate filtered", 0.0, "goal", "current"),
    ("gate_goal", "gate goal ff=1 (instant state ref)", 1.0, "goal", "current"),
    ("pd_instant", "instant classical PD (no gate)", 0.0, "goal", "current"),
    ("smith", "smith observer exact model", 0.0, "goal", "current"),
    ("smith_pert", "smith observer 10pct mismatch", 0.0, "goal", "current"),
)
DELAYS = (0.05, 0.10, 0.14, 0.20)
NOISE_LEVELS = (0.0, 1e-13)
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
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P2-OBSERVER-02/experiment/outputs")


def run_once(model, params, delay, noise, seed=0):
    p = replace(params, ff_gain=0.0)
    _, _, readouts = simulate(model, p, delay_s=delay, grating_gain=p.k_opto, noise_sd=noise, seed=seed)
    heading, omega = readouts["heading"], readouts["omega"]
    finite = np.isfinite(heading) & np.isfinite(omega)
    bad = (np.abs(heading) > HEADING_LIMIT) | (np.abs(omega) > OMEGA_LIMIT) | (~finite)
    return int(bad.any())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(f"DRY RUN: {len(SPECS)} specs x {len(DELAYS)} delays x {len(NOISE_LEVELS)} noise x {len(PARAMETER_SETS)} param sets")
        return 0
    if args.selftest:
        r = run_once("smith", Params(t_end_s=0.6, dt_s=5e-4), 0.05, 0.0)
        assert r in (0, 1)
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for model, label, ff_gain, ff_mode, state in SPECS:
        for noise in NOISE_LEVELS:
            for delay in DELAYS:
                fails = []
                for params in PARAMETER_SETS:
                    p = replace(params, ff_gain=ff_gain, ff_mode=ff_mode, ff_self_state=state)
                    _, _, readouts = simulate(
                        model, p, delay_s=delay, grating_gain=p.k_opto, noise_sd=noise, seed=0
                    )
                    heading, omega = readouts["heading"], readouts["omega"]
                    finite = np.isfinite(heading) & np.isfinite(omega)
                    bad = (np.abs(heading) > HEADING_LIMIT) | (np.abs(omega) > OMEGA_LIMIT) | (~finite)
                    fails.append(int(bad.any()))
                rate = float(np.mean(fails))
                rows.append(
                    {"model": model, "label": label, "noise_sd": noise, "delay_s": delay,
                     "n_param_sets": len(fails), "n_failed": int(np.sum(fails)), "failure_rate": rate}
                )
                print(f"{label:38s} noise={noise:.0e} delay={delay*1e3:5.0f} ms  fail={rate:.3f}", flush=True)
    with (args.output_dir / "sweep.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {"rows": rows, "window_s": WINDOW, "param_sets": len(PARAMETER_SETS), "seed": 0}
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("WROTE sweep.csv + summary.json", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
