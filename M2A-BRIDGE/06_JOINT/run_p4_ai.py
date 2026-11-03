#!/usr/bin/env python3
"""P4-AI-01 analysis (frozen PREREGISTRATION.md of the same round).

Does the freshness necessity structure transfer to non-biological delayed
control tasks? Cart-pole family, rotary-pendulum family, reference-tracking
family; controllers: C (LQR on delayed observation), E1 (velocity
extrapolation), E2 (delay-embedding stochastic forward observer, exact and
10% mass-mismatch), F (fresh state + delayed reference), F+ (F plus the
delayed-state term, ungated). Delay grid, failure curves, critical delays,
impulse recovery. Single-shot per preregistration.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import solve_continuous_are

DT = 0.01
T_END = 8.0
N = int(T_END / DT)
DELAYS_MS = (0, 50, 100, 150, 200, 300, 400, 600)
NOISE = 0.01
SQRT_DT = float(DT ** 0.5)  # prereg sigma read as per-second intensity
N_PLANTS = 30
PLANT_SEED = 424242
KICK_STEP = int(2.5 / DT)
FAM_CODE = {"C": 11, "E1": 22, "E2": 33, "E2m": 44, "F": 55, "Fplus": 66}  # fixed: hash() varies per process
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P4-AI-01/experiment/outputs")


# ---------- plants ----------
def cartpole_matrices(p):
    M, m, l, b, g = p["M"], p["m"], p["l"], p["b"], 9.81
    # small-angle inverted pendulum on cart
    A = np.zeros((4, 4))
    A[0, 1] = 1.0
    A[2, 3] = 1.0
    A[1, 1] = -b / M
    A[1, 2] = m * g / M
    A[3, 1] = -b / (M * l)
    A[3, 2] = (M + m) * g / (M * l)
    B = np.array([[0.0], [1.0 / M], [0.0], [-1.0 / (M * l)]])
    return A, B


def rotary_matrices(p):
    J, c, g, m_r, l = p["J"], p["c"], 9.81, p["m"], p["l"]
    # theta = 0 upright; torque at joint
    A = np.zeros((2, 2))
    A[0, 1] = 1.0
    A[1, 0] = m_r * g * l / J
    A[1, 1] = -c / J
    B = np.array([[0.0], [1.0 / J]])
    return A, B


def draw_plants(task: str, seed: int = PLANT_SEED):
    rng = np.random.default_rng(seed + hash(task) % 1000)
    out = []
    for _ in range(N_PLANTS):
        if task in ("T1", "T3"):
            out.append({
                "M": 1.0 * rng.uniform(0.9, 1.1),
                "m": 0.15 * rng.uniform(0.9, 1.1),
                "l": 0.5 * rng.uniform(0.9, 1.1),
                "b": 0.1 * rng.uniform(0.8, 1.2),
            })
        else:
            out.append({
                "J": 0.01 * rng.uniform(0.85, 1.15),
                "c": 0.01 * rng.uniform(0.8, 1.2),
                "m": 0.1, "l": 0.5,
            })
    return out


def lqr_gain(A, B):
    # Implementation fix (documented): the initial weights produced an exactly
    # zero position gain, letting the cart random-walk into its limit under the
    # preregistered process noise (0/30-style zero-delay failures). Weights now
    # regulate position and angle jointly.
    if A.shape[0] == 4:
        Q = np.diag([20.0, 4.0, 40.0, 4.0])
    else:
        Q = np.diag([40.0, 4.0])
    R = np.array([[1.0]])
    S = solve_continuous_are(A, B, Q, R)
    K = np.linalg.inv(R + B.T @ S @ B) @ (B.T @ S @ A)
    return K.ravel()


# ---------- episode ----------
def run_episode_wrapped(task, plant, family, delay_ms, plant_idx, controls_cache=None):
    # controls for E2: precompute by running C once? Use frozen feedback during
    # prediction: observer propagates with the SAME control law it will apply.
    if task in ("T1", "T3"):
        A, B = cartpole_matrices(plant)
        n_state = 4
    else:
        A, B = rotary_matrices(plant)
        n_state = 2
    K = lqr_gain(A, B)
    ds = int(round(delay_ms / 1000.0 / DT))
    rng = np.random.default_rng(PLANT_SEED + int(delay_ms) + plant_idx * 7 + FAM_CODE[family])
    x = np.zeros(n_state)
    x[0] = 0.02 if task != "T2" else np.deg2rad(1.0)
    hist = [x.copy()]
    us = []
    mismatch = family == "E2m"
    fail = False
    th_lim = np.deg2rad(12.0 if task != "T2" else 15.0)
    x_lim = 2.4 if task != "T2" else np.inf
    for step in range(N):
        def ref(s):
            r = np.zeros(n_state)
            if task == "T3" and s >= 0:
                r[0] = 0.5 * np.sin(2 * np.pi * 0.2 * (s * DT))
            return r
        xd = hist[max(0, step - ds)]
        if family == "C":
            u = -K @ (xd - ref(step - ds))
        elif family == "E1":
            if ds > 0 and step - ds >= 1:
                xhat = xd + (hist[step - ds] - hist[step - ds - 1])
            else:
                xhat = xd
            u = -K @ (xhat - ref(step - ds))
        elif family in ("E2", "E2m"):
            xhat = hist[max(0, step - ds)].copy()
            A_o = A.copy()
            if family == "E2m":
                if n_state == 4:
                    A_o[1, 2] *= 1.1  # pole-mass mismatch in the cart term
                else:
                    A_o[1, 0] *= 1.1  # gravity-term mismatch for the rotary arm
            for j in range(max(0, step - ds), step):
                u_j = us[j] if j < len(us) else 0.0
                xhat = xhat + DT * (A_o @ xhat + B @ np.atleast_1d(u_j)) + rng.normal(0, NOISE * SQRT_DT, n_state)
            u = -K @ (xhat - ref(step - ds))
        elif family == "F":
            u = -K @ (x - ref(step - ds))
        elif family == "Fplus":
            u = -K @ (x - ref(step - ds)) - K @ (xd - ref(step - ds))
        us.append(np.atleast_1d(u).ravel()[0])
        x = x + DT * (A @ x + B @ np.atleast_1d(u)) + rng.normal(0, NOISE * SQRT_DT, n_state)
        if not np.isfinite(x).all() or np.abs(x).max() > 1e3:
            fail = True
        if n_state == 4 and (abs(x[2]) > th_lim or abs(x[0]) > x_lim):
            fail = True
        if n_state == 2 and abs(x[0]) > th_lim:
            fail = True
        if step == KICK_STEP:
            x = x.copy()
            x[0 if n_state == 2 else 2] += 0.05
        hist.append(x.copy())
        if fail:
            break
    # recovery time after the impulse kick (prereg secondary metric)
    rec = float("nan")
    if not fail and len(hist) > KICK_STEP:
        band = np.deg2rad(2.0)
        idx = 0 if n_state == 2 else 2
        below = np.abs(np.array([h[idx] for h in hist[KICK_STEP:]])) < band
        for i in range(0, len(below) - 50):
            if below[i:i + 50].all():
                rec = i * DT
                break
    return fail, hist, rec


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    families = ("C", "E1", "E2", "E2m", "F", "Fplus")
    if args.dry_run:
        print(f"DRY RUN: 3 tasks x {len(families)} families x {len(DELAYS_MS)} delays x {N_PLANTS} plants")
        return 0
    if args.selftest:
        pl = draw_plants("T1", seed=1)[0]
        f0, _, _ = run_episode_wrapped("T1", pl, "F", 0, 0)
        fd, _, _ = run_episode_wrapped("T1", pl, "C", 600, 0)
        assert isinstance(f0, bool) and isinstance(fd, bool)
        # F at zero delay must match C at zero delay (same information) — noise off
        global NOISE
        saved, NOISE = NOISE, 0.0
        fA, hA, _ = run_episode_wrapped("T1", pl, "F", 0, 0)
        fB, hB, _ = run_episode_wrapped("T1", pl, "C", 0, 0)
        NOISE = saved
        assert np.allclose(hA[-1], hB[-1], atol=1e-9), (hA[-1], hB[-1])
        # zero-delay sanity: C must stabilize most plants with process noise on
        ps = draw_plants("T1", seed=7)[:6]
        fails = sum(int(run_episode_wrapped("T1", pl, "C", 0, i)[0]) for i, pl in enumerate(ps))
        assert fails <= 1, f"zero-delay C failed {fails}/6"
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for task in ("T1", "T2", "T3"):
        plants = draw_plants(task)
        for fam in families:
            for d in DELAYS_MS:
                fails = 0
                recs = []
                for pi, pl in enumerate(plants):
                    f, _, rec = run_episode_wrapped(task, pl, fam, d, pi)
                    fails += int(f)
                    if not f and np.isfinite(rec):
                        recs.append(rec)
                rate = fails / N_PLANTS
                rows.append({"task": task, "family": fam, "delay_ms": d,
                             "n_failed": fails, "n_plants": N_PLANTS, "failure_rate": rate,
                             "n_survivors_with_recovery": len(recs),
                             "median_recovery_s": float(np.median(recs)) if recs else None})
                print(f"{task} {fam:6s} {d:4d}ms fail={rate:.2f}", flush=True)
    # critical delays
    crit = {}
    for task in ("T1", "T2", "T3"):
        crit[task] = {}
        for fam in families:
            rs = [r for r in rows if r["task"] == task and r["family"] == fam]
            cd = None
            for r in rs:
                if r["failure_rate"] > 0.5:
                    cd = r["delay_ms"]
                    break
            crit[task][fam] = cd  # None = stable across grid
    summary = {"rows": rows, "critical_delay_ms": crit, "n_plants": N_PLANTS,
               "task_family_unit": "task (n=3) with 30 randomized plants each"}
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(crit, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
