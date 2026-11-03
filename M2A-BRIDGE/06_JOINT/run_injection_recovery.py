#!/usr/bin/env python3
"""W3: injection-recovery validation of the pseudo-pulse/residual pipeline
(SYNTHESIS plan; R3 technical failure #6 / R3-M5).

Ground truth is created by injection: on CONTROL (unstimulated) sessions,
a known state-dependent effect beta is added to the yaw response around
pseudo-pulses, and the frozen two-stage residual discrimination pipeline must
recover it. Sensitivity: beta in {0, 0.5, 1, 2, 4} x 20 injection seeds.
If the pipeline recovers injected effects at stated beta with adequate power
and keeps type-I at beta=0, the method's sensitivity is established within
the tested range.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from run_ray_discrim import (
    MIN_EPOCHS, SEED, TEST_CONTROLS_GLOB, DATASET_DIR,
    build_epochs_v2, load_session, pulse_onsets,
)
from run_ray_discrim2 import (
    N_PSEUDO, delta_ll_test, fit_g,
    pseudo_onsets, proto_features, state_features, exact_signflip_p, yaw_post,
)

OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/W3-INJECT-01/experiment/outputs")
BETAS = (0.0, 1.0, 4.0, 8.0, 16.0, 32.0, 64.0)  # extended to locate detection threshold (pilot design fix, attempts logged)
INJ_SEEDS = 20
SHIFT_S = 30.0


def pseudo_pairs(controls: dict, names: list[str], skip: str):
    X, y = [], []
    for nm in names:
        if nm == skip:
            continue
        for t0 in controls["_pseudo"][nm]:
            X.append(state_features(controls[nm], t0))
            y.append(yaw_post(controls[nm], t0))
    return np.stack(X), np.asarray(y)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    rng = np.random.default_rng(SEED + 77)
    if args.dry_run:
        print(f"DRY RUN: injection-recovery, betas={BETAS}, {INJ_SEEDS} seeds, control sessions")
        return 0
    if args.selftest:
        r = np.random.default_rng(0).normal(0, 1, 100)
        assert exact_signflip_p(np.ones(6)) == 1 / 64
        assert len(r) == 100
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    ctrl_files = sorted(p for p in DATASET_DIR.glob("*.mat") if TEST_CONTROLS_GLOB.match(p.name))[:5]
    controls, pseudo = {}, {}
    for f in ctrl_files:
        s = load_session(f)
        on = pulse_onsets(s)
        controls[f.name] = s
        pseudo[f.name] = pseudo_onsets(s, on, N_PSEUDO, rng)
    controls["_pseudo"] = pseudo
    names = [n for n in controls if n != "_pseudo"]
    print(f"control sessions: {len(names)}", flush=True)

    # stage A once per held-out session: g from other controls' pseudo epochs
    def g_for(skip, grng):
        Xg, yg = pseudo_pairs(controls, names, skip)
        return fit_g(Xg, yg, grng)

    results = {}
    per_seed_matrix = {str(b): [] for b in BETAS}
    for beta in BETAS:
        recoveries, type1 = [], []
        for inj in range(INJ_SEEDS):
            per_sess = []
            irng = np.random.default_rng(SEED + 1000 + inj)
            for si, nm in enumerate(names):
                sess_rng = np.random.default_rng(SEED + 5000 + inj * 100 + si)
                g = g_for(nm, sess_rng)
                test_on = pseudo[nm]
                if len(test_on) < MIN_EPOCHS:
                    continue
                states = np.stack([state_features(controls[nm], t0) for t0 in test_on])
                resid = np.array([yaw_post(controls[nm], t0) for t0 in test_on]) - g(states)
                # injection: beta * (standardized pre-state score) on every epoch
                score = states[:, 0] / (np.std(states[:, 0]) + 1e-9)  # yaw-state z
                resid = resid + beta * score * irng.choice([-1.0, 1.0]) * 1.0
                Xproto = np.stack([proto_features(test_on, k) for k in range(len(test_on))])
                Xfull = np.column_stack([Xproto, states])
                per_sess.append(delta_ll_test(Xproto, Xfull, resid, sess_rng))
            if per_sess:
                d = np.asarray(per_sess)
                recoveries.append(float(np.mean(d > 0)))
                per_seed_matrix[str(beta)].append(float(np.mean(d)))
        results[str(beta)] = {
            "frac_positive_mean": float(np.mean(recoveries)),
            "mean_dll_by_seed": per_seed_matrix[str(beta)],
            "n_seeds": INJ_SEEDS,
        }
        print(f"beta={beta}: frac>0={np.mean(recoveries):.2f} mean_dLL={np.mean(per_seed_matrix[str(beta)]):.3f}", flush=True)
    # paired detection: same-seed dLL(beta) vs dLL(0)
    base = np.asarray(per_seed_matrix["0.0"])
    for b in BETAS:
        if b == 0.0:
            continue
        cur = np.asarray(per_seed_matrix[str(b)])
        n = len(cur)
        diffs = cur - base
        obs = float(np.mean(diffs))
        ge = 0
        for bits in range(2 ** n):
            s = np.array([1.0 if (bits >> i) & 1 else -1.0 for i in range(n)])
            if float(np.mean(diffs * s)) >= obs - 1e-15:
                ge += 1
        results[str(b)]["paired_vs_beta0"] = {
            "median_diff": float(np.median(diffs)),
            "frac_seeds_positive": float(np.mean(diffs > 0)),
            "signflip_p": ge / (2 ** n),
            "detected": bool(ge / (2 ** n) < 0.05),
        }

    summary = {
        "pipeline": "two-stage residual discrimination (P3-RAY-DISCRIM-02 frozen code paths)",
        "injection": "beta * z(pre-yaw-state) * random sign added to pseudo-epoch responses on control sessions",
        "results": results,
        "interpretation_rule": "detection = same-seed paired rise of mean dLL over beta=0 with exact sign-flip p<0.05 (the dLL>0 floor metric was found uninformative at design time and is reported for reference only)",
        "seeds": INJ_SEEDS,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
