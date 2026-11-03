#!/usr/bin/env python3
"""W1 review-response model suite (SYNTHESIS.md revision plan).

(a) R1-M1: gated-classical hybrids — pd_instant, pd_gate, pd_instant with the
    grating pathway removed, and a PD gain sweep on the removed-grating variant.
(b) R1-M2/R3-M2: smith_dde — observer whose internal loop embeds the
    transport delay (exact and 10% mismatch).
(c) R1-M3: gate ablations within gate_goal (disable_gate; gate on |F_bar| only).
(d) R1-M4: undelayed self-state in the delayed pathways (addition/graded/gate).
(e) R3 TF#5: multi-seed boundary cells (long-delay gate_goal; phase subset).
Standard grid: 8 body-gain parameter sets, 6 s window, delays 50-200 ms,
noise {0, 1e-13} unless noted.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

DELAYS = (0.05, 0.10, 0.14, 0.20)
NOISE = (0.0, 1e-13)
WINDOW = 6.0
BODY_SETS = ((6e-14, 2e-11), (6e-14, 1e-11), (1.2e-13, 1e-11), (2.4e-13, 1e-11))
GAINS = (2.5e-11, 5e-11)
PARAMETER_SETS = tuple(
    replace(Params(), inertia=i, drag=d, k_opto=g, t_end_s=WINDOW)
    for i, d in BODY_SETS for g in GAINS
)
HEADING_LIMIT, OMEGA_LIMIT = 2.0 * np.pi, 100.0
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/W1-REVISION-01/experiment/outputs")


def run_cell(model, params_over, delay, noise, seed=0):
    p = replace(params_over, **{}) if params_over else Params()
    _, _, r = simulate(model, p, delay_s=delay, grating_gain=p.k_opto, noise_sd=noise, seed=seed)
    h, w = r["heading"], r["omega"]
    finite = np.isfinite(h) & np.isfinite(w)
    bad = (np.abs(h) > HEADING_LIMIT) | (np.abs(w) > OMEGA_LIMIT) | (~finite)
    return int(bad.any())


def sweep(exp, specs, delays=DELAYS, noises=NOISE, seeds=(0,), rows=None):
    rows = [] if rows is None else rows
    for label, model, ov in specs:
        for noise in noises:
            for delay in delays:
                fails = []
                for base in PARAMETER_SETS:
                    per_seed = [run_cell(model, ov(base) if callable(ov) else replace(base, **ov), delay, noise, s) for s in seeds]
                    fails.append(int(np.any(per_seed)))
                rows.append({"experiment": exp, "label": label, "noise_sd": noise,
                             "delay_s": delay, "seeds": len(seeds),
                             "n_failed": int(np.sum(fails)), "n_sets": len(fails),
                             "failure_rate": float(np.mean(fails))})
                print(f"{exp} {label:44s} noise={noise:.0e} d={delay*1e3:3.0f}ms fail={np.mean(fails):.3f}", flush=True)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: W1 suite (a-e)")
        return 0
    if args.selftest:
        r = run_cell("smith_dde", Params(t_end_s=0.6, dt_s=5e-4), 0.05, 0.0)
        assert r in (0, 1)
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    # (a) gated-classical hybrids
    sweep("a_gated_classical", [
        ("pd_instant (ungated grating)", "pd_instant", {}),
        ("pd_gate (instant PD + gate)", "pd_gate", {}),
    ], rows=rows)
    # grating-removed variants (grating_gain=0 set explicitly)
    for label, pmul in (("pd_instant, grating removed", 1.0),
                        ("pd_gate, grating removed", 1.0),
                        ("pd_instant removed + p_gain x0.5", 0.5),
                        ("pd_instant removed + p_gain x2", 2.0),
                        ("pd_instant removed + p_gain x5", 5.0)):
        model = "pd_gate" if label.startswith("pd_gate") else "pd_instant"
        for noise in NOISE:
            for delay in DELAYS:
                fails = []
                for base in PARAMETER_SETS:
                    p = replace(base, p_gain=base.p_gain * pmul)
                    _, _, r = simulate(model, p, delay_s=delay, grating_gain=0.0, noise_sd=noise, seed=0)
                    h, w = r["heading"], r["omega"]
                    finite = np.isfinite(h) & np.isfinite(w)
                    bad = (np.abs(h) > HEADING_LIMIT) | (np.abs(w) > OMEGA_LIMIT) | (~finite)
                    fails.append(int(bad.any()))
                rows.append({"experiment": "a_gated_classical", "label": label, "noise_sd": noise,
                             "delay_s": delay, "seeds": 1, "n_failed": int(np.sum(fails)),
                             "n_sets": len(fails), "failure_rate": float(np.mean(fails))})
                print(f"a {label:44s} noise={noise:.0e} d={delay*1e3:3.0f}ms fail={np.mean(fails):.3f}", flush=True)
    # (b) delay-aware observer
    sweep("b_delay_observer", [
        ("smith_dde exact", "smith_dde", {}),
        ("smith_dde 10pct mismatch", "smith_dde", {"smith_drag_scale": 1.1, "smith_inertia_scale": 1.1}),
        ("gate goal ff=1 (reference)", "gate_goal", {"ff_gain": 1.0, "ff_mode": "goal", "ff_self_state": "current"}),
    ], rows=rows)
    # (c) gate ablations within gate_goal
    sweep("c_gate_ablation", [
        ("gate_goal reference (augmented)", "gate_goal", {"ff_gain": 1.0, "ff_mode": "goal", "ff_self_state": "current"}),
        ("gate_goal, gate disabled", "gate_goal", {"ff_gain": 1.0, "ff_mode": "goal", "ff_self_state": "current", "disable_gate": True}),
        ("gate_goal, trigger on F_bar only", "gate_goal", {"ff_gain": 1.0, "ff_mode": "goal", "ff_self_state": "current", "gate_trigger": "bar"}),
    ], rows=rows)
    # (d) undelayed self-state in delayed pathways
    sweep("d_undelayed_selfstate", [
        ("addition, psi/omega undelayed", "addition", {"undelayed_selfstate": True}),
        ("graded filtered, undelayed", "graded_sensory", {"undelayed_selfstate": True}),
        ("gate filtered, undelayed", "allnone", {"undelayed_selfstate": True}),
        ("addition (delayed reference)", "addition", {}),
    ], rows=rows)
    # (e) multi-seed boundary cells
    sweep("e_multiseed_boundary", [
        ("gate goal ff=1 long delay", "gate_goal", {"ff_gain": 1.0, "ff_mode": "goal", "ff_self_state": "current"}),
        ("gate filtered long delay", "allnone", {}),
    ], delays=(0.25, 0.30, 0.40, 0.50), noises=(1e-13,), seeds=(0, 1, 2), rows=rows)
    sweep("e_multiseed_phase", [
        ("gate filtered @0.14/0.20", "allnone", {}),
        ("gate goal ff=1 @0.14/0.20", "gate_goal", {"ff_gain": 1.0, "ff_mode": "goal", "ff_self_state": "current"}),
    ], delays=(0.14, 0.20), noises=(1e-13,), seeds=(0, 1, 2), rows=rows)

    with (args.output_dir / "sweep.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (args.output_dir / "summary.json").write_text(json.dumps({"rows": rows}, indent=2) + "\n")
    print(f"WROTE {len(rows)} cells", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
