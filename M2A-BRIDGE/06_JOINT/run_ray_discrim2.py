#!/usr/bin/env python3
"""P3-RAY-DISCRIM-02 analysis (frozen PREREGISTRATION.md of the same round).

Residual-endpoint discrimination: the generic state->future-yaw autocorrelation
map g is learned ONLY from non-pulse (pseudo) epochs, then removed from pulse
epochs; the test asks whether pulse-epoch residuals still depend on pre-pulse
behavioral state. Primary decision rule includes the pseudo-pulse control
magnitude condition (DISCRIM-01 lesson). Unit = fly; dev sessions excluded.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from run_ray_discrim import (
    DATASET_DIR,
    DEV_DIR,
    LAMBDA_GRID,
    MIN_EPOCHS,
    SEED,
    TEST_CONTROLS_GLOB,
    TEST_INTERVENTION,
    interp,
    load_session,
    mean_at,
    pulse_onsets,
)

OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-RAY-DISCRIM-02/experiment/outputs")
N_PSEUDO = 300
PULSE_GAP_S = 3.0
SHIFT_S = 30.0


def pseudo_onsets(sess: dict, real_onsets: np.ndarray, n: int, rng) -> np.ndarray:
    T = sess["t_ephys"][-1]
    out = []
    guard = 0
    while len(out) < n and guard < n * 50:
        guard += 1
        t0 = float(rng.uniform(10.0, T - 5.0))
        if np.all(np.abs(t0 - real_onsets) > PULSE_GAP_S):
            out.append(t0)
    return np.sort(np.asarray(out))


def state_features(sess: dict, t0: float, shift: float = 0.0) -> np.ndarray:
    tb = sess["t_ball"]
    ts0, ts1 = t0 - 1.0 - shift, t0 - shift
    feats = []
    for sig in ("yaw", "fwd", "lat"):
        win = interp(tb, sess[sig], np.arange(ts0, ts1, 0.01))
        feats.extend([float(np.mean(win)), float(np.std(win))])
    return np.asarray(feats)


def yaw_post(sess: dict, t0: float) -> float:
    tb = sess["t_ball"]
    return float(np.mean(interp(tb, sess["yaw"], np.arange(t0, t0 + 1.0, 0.01))))


def vm_features(sess: dict, t0: float) -> np.ndarray:
    te = sess["t_ephys"]
    pre = mean_at(te, sess["ephys"], t0 - 0.5, t0)
    return np.asarray([pre])


def vm_post(sess: dict, t0: float) -> float:
    te = sess["t_ephys"]
    return mean_at(te, sess["ephys"], t0 + 0.05, t0 + 0.5)


def proto_features(onsets: np.ndarray, i: int) -> np.ndarray:
    t0 = onsets[i]
    gap = float(onsets[i] - onsets[i - 1]) if i > 0 else 0.0
    return np.asarray([float(i), gap, float(t0)])


def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xs = np.column_stack([np.ones(len(y)), (X - mu) / sd])
    W = np.linalg.solve(Xs.T @ Xs + lam * np.eye(Xs.shape[1]), Xs.T @ y)
    resid = y - Xs @ W
    return W, mu, sd, float(np.var(resid)) + 1e-9


def ll_gaussian(y, pred, var) -> float:
    return float(-0.5 * np.sum((y - pred) ** 2) / var - 0.5 * len(y) * np.log(2 * np.pi * var))


def fit_g(X: np.ndarray, y: np.ndarray, rng) -> callable:
    idx = rng.permutation(len(y))
    cut = int(0.8 * len(idx))
    best, best_lam = -np.inf, LAMBDA_GRID[0]
    for lam in LAMBDA_GRID:
        W, mu, sd, var = ridge_fit(X[idx[:cut]], y[idx[:cut]], lam)
        pred = np.column_stack([np.ones(len(idx[cut:])), (X[idx[cut:]] - mu) / sd]) @ W
        ll = ll_gaussian(y[idx[cut:]], pred, var)
        if ll > best:
            best, best_lam = ll, lam
    W, mu, sd, var = ridge_fit(X, y, best_lam)

    def g(Xnew):
        return np.column_stack([np.ones(len(Xnew)), (Xnew - mu) / sd]) @ W

    return g


def delta_ll_test(Xproto: np.ndarray, Xfull: np.ndarray, r: np.ndarray, rng) -> float:
    idx = rng.permutation(len(r))
    cut = int(0.8 * len(idx))
    best0 = (-np.inf, LAMBDA_GRID[0])
    best1 = (-np.inf, LAMBDA_GRID[0])
    for lam in LAMBDA_GRID:
        W0, m0, s0, v0 = ridge_fit(Xproto[idx[:cut]], r[idx[:cut]], lam)
        ll0 = ll_gaussian(r[idx[cut:]], np.column_stack([np.ones(len(idx[cut:])), (Xproto[idx[cut:]] - m0) / s0]) @ W0, v0)
        if ll0 > best0[0]:
            best0 = (ll0, lam)
        W1, m1, s1, v1 = ridge_fit(Xfull[idx[:cut]], r[idx[:cut]], lam)
        ll1 = ll_gaussian(r[idx[cut:]], np.column_stack([np.ones(len(idx[cut:])), (Xfull[idx[cut:]] - m1) / s1]) @ W1, v1)
        if ll1 > best1[0]:
            best1 = (ll1, lam)
    W0, m0, s0, v0 = ridge_fit(Xproto, r, best0[1])
    W1, m1, s1, v1 = ridge_fit(Xfull, r, best1[1])
    ll0 = ll_gaussian(r, np.column_stack([np.ones(len(r)), (Xproto - m0) / s0]) @ W0, v0)
    ll1 = ll_gaussian(r, np.column_stack([np.ones(len(r)), (Xfull - m1) / s1]) @ W1, v1)
    return ll1 - ll0


def exact_signflip_p(deltas: np.ndarray) -> float:
    n = len(deltas)
    obs = float(np.mean(deltas))
    ge = sum(
        1
        for bits in range(2**n)
        if float(np.mean(deltas * np.array([1.0 if (bits >> i) & 1 else -1.0 for i in range(n)]))) >= obs - 1e-15
    )
    return ge / (2**n)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    if args.dry_run:
        print("DRY RUN: residual-endpoint discrimination, two-stage g from pseudo epochs, 3 controls")
        return 0
    if args.selftest:
        y = np.arange(100.0)
        X = np.column_stack([np.ones(100), y])  # perfectly predictable
        g = fit_g(X, y + rng.normal(0, 1e-6, 100), rng)
        assert np.max(np.abs(g(X) - y)) < 0.01
        assert exact_signflip_p(np.array([1.0] * 6)) == 1 / 64
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    intervention = {}
    for f in TEST_INTERVENTION:
        intervention[f] = load_session(DATASET_DIR / f)
    control_files = sorted(p for p in DATASET_DIR.glob("*.mat") if TEST_CONTROLS_GLOB.match(p.name))[:5]
    controls = {f.name: load_session(f) for f in control_files}
    print(f"intervention={len(intervention)} controls={len(controls)}", flush=True)

    pseudo_iv = {}
    for f, s in intervention.items():
        pseudo_iv[f] = pseudo_onsets(s, pulse_onsets(s), N_PSEUDO, rng)
    pseudo_ctrl = {n: pseudo_onsets(s, pulse_onsets(s), N_PSEUDO, rng) for n, s in controls.items()}

    per_animal, per_animal_neural, gctrl_dl, shift_dl, cap_dl, ctrl_dl = [], [], [], [], [], []
    test_names = list(intervention)
    ctrl_names = list(controls)

    def pseudo_pairs(pool: dict, names: list[str], skip: str | None, feats, resp):
        X, y = [], []
        for nm in names:
            if nm == skip:
                continue
            for t0 in (pseudo_iv if pool is intervention else pseudo_ctrl)[nm]:
                X.append(feats(pool[nm], t0))
                y.append(resp(pool[nm], t0))
        return np.stack(X), np.asarray(y)

    for i, f in enumerate(test_names):
        sess = intervention[f]
        on = pulse_onsets(sess)
        # stage A: g from OTHER intervention animals' pseudo epochs
        Xg, yg = pseudo_pairs(intervention, test_names, f, state_features, yaw_post)
        g = fit_g(Xg, yg, rng)
        # stage B on this animal's pulse epochs
        states = np.stack([state_features(sess, t0) for t0 in on])
        ypost = np.array([yaw_post(sess, t0) for t0 in on])
        resid = ypost - g(states)
        Xproto = np.stack([proto_features(on, j) for j in range(len(on))])
        Xfull = np.column_stack([Xproto, states])
        d = delta_ll_test(Xproto, Xfull, resid, rng)
        per_animal.append({"animal": f[:34], "delta_ll": round(d, 3), "n_epochs": int(len(on))})
        # neural residual (same fold structure)
        Xgn, ygn = pseudo_pairs(
            intervention, test_names, f,
            lambda s, t0: np.concatenate([state_features(s, t0), vm_features(s, t0)]),
            vm_post,
        )
        gn = fit_g(Xgn, ygn, rng)
        vmpost = np.array([vm_post(sess, t0) for t0 in on])
        rn = vmpost - gn(np.column_stack([states, np.stack([vm_features(sess, t0) for t0 in on])]))
        dn = delta_ll_test(Xproto, Xfull, rn, rng)
        per_animal_neural.append({"animal": f[:34], "delta_ll": round(dn, 3)})
        # robustness g_ctrl: baseline map from control animals only
        Xgc, ygc = pseudo_pairs(controls, ctrl_names, None, state_features, yaw_post)
        gc = fit_g(Xgc, ygc, rng)
        gctrl_dl.append(delta_ll_test(Xproto, Xfull, ypost - gc(states), rng))
        # time-shift control
        states_sh = np.stack([state_features(sess, t0, shift=SHIFT_S) for t0 in on])
        shift_dl.append(delta_ll_test(Xproto, np.column_stack([Xproto, states_sh]), resid, rng))
        # capacity control: proto + 3 white-noise features
        noise = np.random.default_rng(SEED + 100 + i).standard_normal((len(on), 3))
        cap_dl.append(delta_ll_test(Xproto, np.column_stack([Xproto, noise]), resid, rng))
        print(f"  {f[:34]}: dLL={d:+.2f} neural={dn:+.2f} epochs={len(on)}", flush=True)

    # negative control 1: pseudo-pulse discrimination on CONTROL animals
    for j, nm in enumerate(ctrl_names):
        sess = controls[nm]
        Xg, yg = pseudo_pairs(controls, ctrl_names, nm, state_features, yaw_post)
        g = fit_g(Xg, yg, rng)
        test_on = pseudo_ctrl[nm]
        if len(test_on) < MIN_EPOCHS:
            continue
        states = np.stack([state_features(sess, t0) for t0 in test_on])
        resid = np.array([yaw_post(sess, t0) for t0 in test_on]) - g(states)
        Xproto = np.stack([proto_features(test_on, k) for k in range(len(test_on))])
        Xfull = np.column_stack([Xproto, states])
        ctrl_dl.append(delta_ll_test(Xproto, Xfull, resid, rng))
    print(f"pseudo-pulse control sessions: {len(ctrl_dl)}", flush=True)

    d_b = np.array([r["delta_ll"] for r in per_animal])
    p_b = exact_signflip_p(d_b)
    med_main = float(np.median(d_b))
    med_ctrl = float(np.median(ctrl_dl)) if ctrl_dl else float("nan")
    control_ok = bool(ctrl_dl) and abs(med_ctrl) < abs(med_main) / 3.0
    if p_b < 0.05 and control_ok:
        verdict = "PERTURBATION_SPECIFIC_STATE_DEPENDENCE"
    elif p_b < 0.05:
        verdict = "STATE_DEPENDENT_PERTURBATION_RESPONSE_WITH_FAILED_CONTROL"
    else:
        verdict = "NOT_DISCRIMINATED"
    summary = {
        "verdict": verdict,
        "p_exact_signflip": p_b,
        "median_delta_ll_behavior": med_main,
        "per_animal_behavior": per_animal,
        "median_delta_ll_neural": float(np.median([r["delta_ll"] for r in per_animal_neural])),
        "per_animal_neural": per_animal_neural,
        "controls": {
            "pseudo_pulse_median_delta_ll": med_ctrl,
            "pseudo_pulse_n_sessions": len(ctrl_dl),
            "control_magnitude_condition_met": control_ok,
            "g_ctrl_robustness_median": float(np.median(gctrl_dl)),
            "time_shift_median": float(np.median(shift_dl)),
            "capacity_median": float(np.median(cap_dl)),
        },
        "n_test_animals": len(per_animal),
        "guards": "dev excluded; g learned only from non-pulse epochs; all three controls implemented; prereg SHA-256 668e066a...483e",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
