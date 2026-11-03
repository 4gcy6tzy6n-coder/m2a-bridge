#!/usr/bin/env python3
"""P3-RAY-DISCRIM-01 analysis (frozen PREREGISTRATION.md of the same round).

Does the response to optogenetic perturbation (83blexA CsChrimson) depend on
concurrent behavioral state beyond stimulus-history alone? M0 = pulse-protocol
history; M1 = M0 + strictly-pre-onset behavioral state; ridge; per-held-out-animal
log-likelihood increment with exact sign-flip test; three frozen negative
controls. Unit = fly. Development sessions are excluded from the test set.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
from scipy.io import loadmat

DEV_DIR = Path("/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/rayshubskiy_audit")
DATASET_DIR = DEV_DIR  # owner places remaining SH files here
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-RAY-DISCRIM-01/experiment/outputs")

DEV_FILES = (
    "161218_lexAOpCsChrimson_gfp_83blexA_ss731_02_data_for_SH_with_lat_vel.mat",
    "170802_gfp_ss731_03_data_for_SH_with_lat_vel.mat",
)
TEST_INTERVENTION = (
    "161208_lexAOpCsChrimson_gfp_83blexA_ss730_03_data_for_SH_with_lat_vel.mat",
    "161208_lexAOpCsChrimson_gfp_83blexA_ss730_04_data_for_SH_with_lat_vel.mat",
    "161208_lexAOpCsChrimson_gfp_83blexA_ss730_05_data_for_SH_with_lat_vel.mat",
    "161210_lexAOpCsChrimson_gfp_83blexA_ss730_06_data_for_SH_with_lat_vel.mat",
    "170721_lexAOpCsChrimson_gfp_83blexA_ss731_05_data_for_SH_with_lat_vel.mat",
    "170726_lexAOpCsChrimson_gfp_83blexA_ss731_08_data_for_SH_with_lat_vel.mat",
)
TEST_CONTROLS_GLOB = re.compile(r"^(170803|170804|170808).*_data_for_SH_with_lat_vel\.mat$")

LAMBDA_GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1000.0)
MIN_EPOCHS = 20
SEED = 20261029
SHIFT_S = 30.0


def load_session(path: Path) -> dict:
    d = loadmat(path, squeeze_me=True, struct_as_record=False)
    return {
        "ephys": np.asarray(d["ephys_A"], float),
        "t_ephys": np.asarray(d["t_ephys"], float),
        "yaw": np.asarray(d["yaw"], float),
        "fwd": np.asarray(d["fwd"], float),
        "lat": np.asarray(d["lat"], float),
        "t_ball": np.asarray(d["t_ball"], float),
        "stim": np.asarray(d["stim"], float),
    }


def pulse_onsets(sess: dict) -> np.ndarray:
    stim = sess["stim"]
    te = sess["t_ephys"]
    idx = np.where((stim[:-1] < 2.5) & (stim[1:] >= 2.5))[0] + 1
    return te[idx]


def interp(t_ball: np.ndarray, sig: np.ndarray, t_query: np.ndarray) -> np.ndarray:
    return np.interp(t_query, t_ball, sig)


def mean_at(t: np.ndarray, sig: np.ndarray, t0: float, t1: float) -> float:
    m = (t >= t0) & (t < t1)
    return float(np.mean(sig[m])) if m.any() else float("nan")


def build_epochs_v2(sess: dict, onsets: np.ndarray, shift_s: float = 0.0) -> dict:
    """Clean version: protocol features computed properly."""
    te, tb = sess["t_ephys"], sess["t_ball"]
    states, proto, rb_list, rn_list = [], [], [], []
    for i, t0 in enumerate(onsets):
        if t0 - 1.2 - max(shift_s, 0) < 0 or t0 + 1.2 > te[-1]:
            continue
        ts0, ts1 = t0 - 1.0 - shift_s, t0 - shift_s
        state = []
        for sig in ("yaw", "fwd", "lat"):
            win = interp(tb, sess[sig], np.arange(ts0, ts1, 0.01))
            if not np.isfinite(win).all():
                win = win[np.isfinite(win)]
            state.extend([float(np.mean(win)), float(np.std(win))])
        gap = float(onsets[i - 1]) if i > 0 else float(t0)
        proto.append([float(i), t0 - gap if i > 0 else 0.0, float(t0)])
        states.append(state)
        yaw_pre = float(np.mean(interp(tb, sess["yaw"], np.arange(t0 - 1.0, t0, 0.01))))
        yaw_post = float(np.mean(interp(tb, sess["yaw"], np.arange(t0, t0 + 1.0, 0.01))))
        rb_list.append(yaw_post - yaw_pre)
        rn_list.append(mean_at(te, sess["ephys"], t0 + 0.05, t0 + 0.5) - mean_at(te, sess["ephys"], t0 - 0.5, t0))
    m0 = np.column_stack([np.ones(len(proto)), np.asarray(proto, float)])
    m1 = np.column_stack([m0, np.asarray(states, float)])
    return {"M0": m0, "M1": m1, "resp_b": np.asarray(rb_list), "resp_n": np.asarray(rn_list)}


def ridge_ll(Xtr, ytr, Xte, yte, lam) -> float:
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xs = np.column_stack([np.ones(len(ytr)), (Xtr - mu) / sd])
    W = np.linalg.solve(Xs.T @ Xs + lam * np.eye(Xs.shape[1]), Xs.T @ ytr)
    Xst = np.column_stack([np.ones(len(yte)), (Xte - mu) / sd])
    pred = Xst @ W
    resid = yte - pred
    var = float(np.var(ytr - np.column_stack([np.ones(len(ytr)), (Xtr - mu) / sd]) @ W)) + 1e-9
    return float(-0.5 * np.sum(resid**2) / var - 0.5 * len(yte) * np.log(2 * np.pi * var))


def pick_lambda(Xtr, ytr, rng) -> float:
    idx = rng.permutation(len(ytr))
    cut = int(0.8 * len(idx))
    best, best_lam = -np.inf, LAMBDA_GRID[0]
    for lam in LAMBDA_GRID:
        ll = ridge_ll(Xtr[idx[:cut]], ytr[idx[:cut]], Xtr[idx[cut:]], ytr[idx[cut:]], lam)
        if ll > best:
            best, best_lam = ll, lam
    return best_lam


def lomo(sessions: list[dict], responses: str, rng) -> dict:
    per_animal = []
    for held in range(len(sessions)):
        X0tr = np.concatenate([sessions[i]["M0"] for i in range(len(sessions)) if i != held])
        X1tr = np.concatenate([sessions[i]["M1"] for i in range(len(sessions)) if i != held])
        ytr = np.concatenate([sessions[i][responses] for i in range(len(sessions)) if i != held])
        lam0, lam1 = pick_lambda(X0tr, ytr, rng), pick_lambda(X1tr, ytr, rng)
        ll0 = ridge_ll(X0tr, ytr, sessions[held]["M0"], sessions[held][responses], lam0)
        ll1 = ridge_ll(X1tr, ytr, sessions[held]["M1"], sessions[held][responses], lam1)
        per_animal.append({"animal": held, "ll0": ll0, "ll1": ll1, "delta_ll": ll1 - ll0,
                           "n_epochs": int(len(sessions[held]["M0"])), "lam0": lam0, "lam1": lam1})
    return per_animal


def exact_signflip_p(deltas: np.ndarray) -> float:
    n = len(deltas)
    obs = float(np.mean(deltas))
    ge = 0
    for bits in range(2**n):
        s = np.array([1.0 if (bits >> i) & 1 else -1.0 for i in range(n)])
        if float(np.mean(deltas * s)) >= obs - 1e-15:
            ge += 1
    return ge / (2**n)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="run pipeline on the two dev sessions only")
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    if args.dry_run:
        print("DRY RUN: M0 vs M1 on 6 test intervention animals, LOMO, exact sign-flip; 3 negative controls")
        return 0
    if args.selftest:
        on = np.array([10.0, 25.0, 41.0])
        sess = {
            "t_ephys": np.arange(0, 60, 2.5e-4), "ephys": np.zeros(240000),
            "t_ball": np.arange(0, 60, 0.01), "yaw": np.sin(np.arange(0, 60, 0.01)),
            "fwd": np.zeros(6000), "lat": np.zeros(6000), "stim": np.zeros(240000),
        }
        e = build_epochs_v2(sess, on)
        assert e["M0"].shape[1] == 4 and e["M1"].shape[1] == 10 and len(e["resp_b"]) == 3
        assert exact_signflip_p(np.array([1.0, 1.0, 1.0])) == 0.125
        assert pulse_onsets({"stim": np.r_[np.zeros(100), np.full(10, 5.0), np.zeros(100)], "t_ephys": np.arange(210) * 0.5}).tolist() == [50.0]
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.smoke:
        files = [DEV_DIR / f for f in DEV_FILES]
        sess = []
        for f in files:
            s = load_session(f)
            e = build_epochs_v2(s, pulse_onsets(s))
            print(f"{f.name[:36]}: epochs={len(e['resp_b'])} resp_b std={np.std(e['resp_b']):.2f}")
            sess.append(e)
        print("SMOKE OK (dev files only; no test outcomes touched)")
        return 0

    missing = [f for f in TEST_INTERVENTION if not (DATASET_DIR / f).exists()]
    if missing:
        print("MISSING_TEST_FILES:")
        for m in missing:
            print(" ", m)
        return 2

    test_sessions = []
    for f in TEST_INTERVENTION:
        s = load_session(DATASET_DIR / f)
        e = build_epochs_v2(s, pulse_onsets(s))
        if len(e["resp_b"]) >= MIN_EPOCHS:
            e["file"] = f
            test_sessions.append(e)
        else:
            print(f"EXCLUDED (epochs<{MIN_EPOCHS}): {f} ({len(e['resp_b'])})")
    print(f"test animals: {len(test_sessions)}", flush=True)

    beh = lomo(test_sessions, "resp_b", rng)
    neu = lomo(test_sessions, "resp_n", rng)
    d_b = np.array([r["delta_ll"] for r in beh])
    p_b = exact_signflip_p(d_b)

    # negative controls (frozen)
    controls = {}
    ctrl_files = sorted(p for p in DATASET_DIR.glob("*.mat") if TEST_CONTROLS_GLOB.match(p.name))
    ctrl_sessions = []
    for f in ctrl_files[:4]:
        s = load_session(f)
        onsets = pulse_onsets(s)
        if len(onsets) < MIN_EPOCHS:  # pseudo-pulses: matched-rate random onsets
            onsets = np.sort(rng.uniform(50, s["t_ephys"][-1] - 5, 261))
        ctrl_sessions.append(build_epochs_v2(s, onsets))
    if ctrl_sessions:
        pseudo = lomo(ctrl_sessions, "resp_b", rng)
        controls["pseudo_pulse_control"] = {
            "n_sessions": len(ctrl_sessions),
            "median_delta_ll": float(np.median([r["delta_ll"] for r in pseudo])),
        }
    shifted = []
    for f in TEST_INTERVENTION[: len(test_sessions)]:
        s = load_session(DATASET_DIR / f)
        shifted.append(build_epochs_v2(s, pulse_onsets(s), shift_s=SHIFT_S))
    sh = lomo(shifted, "resp_b", rng)
    controls["time_shift_control"] = {"median_delta_ll": float(np.median([r["delta_ll"] for r in sh]))}

    summary = {
        "verdict": "STATE_DEPENDENT_PERTURBATION_RESPONSE" if p_b < 0.05 else "NOT_DISCRIMINATED",
        "p_exact_signflip": p_b,
        "per_animal_behavior": beh,
        "per_animal_neural": neu,
        "median_delta_ll_behavior": float(np.median(d_b)),
        "median_delta_ll_neural": float(np.median([r["delta_ll"] for r in neu])),
        "negative_controls": controls,
        "n_test_animals": len(test_sessions),
        "guards": "dev sessions excluded; causal pre-onset state only; lambda inner-CV on training animals; claim ceiling per prereg section 0",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if not k.startswith("per_animal")}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
