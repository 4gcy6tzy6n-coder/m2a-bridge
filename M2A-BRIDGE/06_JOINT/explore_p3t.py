#!/usr/bin/env python3
"""P3-T exploratory model discrimination (D10/D11 scope; visual evidence
integration ONLY — never self-state delay).

Data: Tanaka fig1_05_onset (two brief-wait experiments: gap/motion =
666/333 ms, n=27; and 500/500 ms, n=17). Per-fly angular-velocity traces for
uniform / stationary / flicker foregrounds (p8, trials averaged).

Three pre-stated model families (frozen in this script before any run):
  A late_step  : suppression expressed only after motion onset as an
                 exponential approach with time constant tau (gap-invariant
                 after aligning to motion onset)
  B fg_ramp    : evidence accumulates from FOREGROUND onset, so the response
                 at motion onset depends on gap length (1-exp(-gap/tau))
  C fg_kernel  : flexible raised-cosine temporal kernel from foreground
                 onset (5 taps, 0-1.5 s) — capacity-heavy reference

Pre-stated discriminant (reported regardless of model ranking): the
uniform-minus-stationary difference sampled at motion onset +100 ms, measured
per experiment, and each model's prediction of that between-experiment
contrast. Exploratory only; unit = fly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.io import loadmat
from scipy.optimize import least_squares

MAT = Path("/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/fig1_05_onset.mat")
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-T-EXPLORE-01/experiment/outputs")

EXPERIMENTS = (
    {"name": "gap666", "idx": 0, "gap_ms": 666.0, "motion_ms": 333.0},
    {"name": "gap500", "idx": 1, "gap_ms": 500.0, "motion_ms": 500.0},
)
EPOCHS = ("uniform", "stationary", "flicker")
SAMPLE_MS = 100.0  # discriminant sampling offset after motion onset


def unwrap0(obj):
    while isinstance(obj, np.ndarray) and obj.dtype == object and obj.ndim == 0:
        obj = obj[()]
    return obj


def load_group(idx: int) -> dict:
    d = loadmat(MAT, variable_names=["data"], squeeze_me=True, struct_as_record=False)["data"]
    g = np.atleast_1d(d)[idx]
    time_s = np.asarray(g.timeX, float) / 1000.0
    ind = np.atleast_1d(g.indFly)
    traces = []
    for f in ind:
        snip = unwrap0(unwrap0(f.p8_averagedRois).snipMat)
        snip = np.atleast_1d(snip)
        cols = []
        for e in range(len(snip)):
            cell = np.asarray(unwrap0(snip[e]), dtype=float)
            cols.append(cell[:, 0])  # angular velocity
        traces.append(np.stack(cols, axis=1))  # time x 3
    return {"t": time_s, "traces": np.stack(traces, axis=2), "n_fly": len(ind)}


def exp_kernel(t: np.ndarray, tau: float) -> np.ndarray:
    return 1.0 - np.exp(-np.maximum(t, 0.0) / max(tau, 1e-3))


def model_response(name: str, t: np.ndarray, gap_s: float, motion_s: float, amps: np.ndarray, tau: float, taps: np.ndarray | None) -> np.ndarray:
    """Per-epoch response traces (len(t) x 3) given fitted parameters."""
    t_mot = gap_s
    out = np.zeros((len(t), len(amps)))
    for e, a in enumerate(amps):
        if name == "A_late_step":
            out[:, e] = a * exp_kernel(t - t_mot, tau) * (t >= t_mot)
        elif name == "B_fg_ramp":
            ev = exp_kernel(t, tau)  # from foreground onset (t=0)
            out[:, e] = a * ev * (t >= t_mot)
        elif name == "C_fg_kernel":
            if taps is not None:
                centers = np.linspace(0.15, 1.5, len(taps))
                width = 1.5 / len(taps)
                for w, c in zip(taps, centers):
                    basis = 0.5 * (1 + np.cos(np.pi * np.clip((t - c) / width, -1, 1)))
                    out[:, e] += a * w * basis
    return out


def fit_model(name: str, t: np.ndarray, y_mean: np.ndarray, gap_s: float, motion_s: float) -> dict:
    n_taps = 5 if name == "C_fg_kernel" else 0

    def resid(p):
        amps = p[:3]
        tau = p[3] if n_taps == 0 else 1.0
        taps = p[4:] if n_taps else None
        pred = model_response(name, t, gap_s, motion_s, amps, tau, taps)
        return (pred - y_mean).ravel()

    p0 = [float(np.nanmean(y_mean[:, e])) for e in range(3)] + ([0.5] if n_taps == 0 else [1.0] * n_taps)
    lo = [-50.0] * 3 + ([0.02] if n_taps == 0 else [-3.0] * n_taps)
    hi = [50.0] * 3 + ([3.0] if n_taps == 0 else [3.0] * n_taps)
    r = least_squares(resid, p0, bounds=(lo, hi), max_nfev=400)
    return {"p": r.x.tolist(), "n_taps": n_taps}


def predict(name: str, fit: dict, t: np.ndarray, gap_s: float, motion_s: float) -> np.ndarray:
    p = np.asarray(fit["p"])
    amps, tau, taps = p[:3], (p[3] if fit["n_taps"] == 0 else 1.0), (p[4:] if fit["n_taps"] else None)
    return model_response(name, t, gap_s, motion_s, amps, tau, taps)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    models = ("A_late_step", "B_fg_ramp", "C_fg_kernel")
    if args.dry_run:
        print("DRY RUN: A/B/C visual-integration models on fig1_05, LOMO within experiment")
        return 0
    if args.selftest:
        t = np.arange(-0.483, 4.0, 1 / 60)
        gap = 0.5
        y = model_response("B_fg_ramp", t, gap, 0.5, np.array([10.0, 4.0, 6.0]), 0.8, None)
        fit = fit_model("B_fg_ramp", t, y, gap, 0.5)
        pred = predict("B_fg_ramp", fit, t, gap, 0.5)
        assert np.sqrt(np.mean((pred - y) ** 2)) < 0.5
        # discriminant sanity: B predicts larger pre-asymptote start for bigger gap
        r666 = model_response("B_fg_ramp", np.array([0.666]), 0.666, 0.333, np.array([1.0, 1.0, 1.0]), 0.8, None)
        r500 = model_response("B_fg_ramp", np.array([0.500]), 0.500, 0.500, np.array([1.0, 1.0, 1.0]), 0.8, None)
        assert r666[0, 0] > r500[0, 0]
        ra = model_response("A_late_step", np.array([0.666]), 0.666, 0.333, np.array([1.0] * 3), 0.8, None)
        rb = model_response("A_late_step", np.array([0.500]), 0.500, 0.500, np.array([1.0] * 3), 0.8, None)
        assert np.isclose(ra[0, 0], rb[0, 0])  # A is gap-invariant at motion onset
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    result: dict = {"note": "EXPLORATORY P3-T: visual evidence integration only; unit = fly; no self-state claims"}
    for exp in EXPERIMENTS:
        g = load_group(exp["idx"])
        t, traces = g["t"], g["traces"]  # time x 3 x fly
        t_mot = exp["gap_ms"] / 1000.0
        post = (t >= t_mot + 0.1)
        per_model = {}
        for name in models:
            lomo_r2 = []
            for held in range(g["n_fly"]):
                train = np.delete(traces, held, axis=2).mean(axis=2)
                fit = fit_model(name, t, train, t_mot, exp["motion_ms"] / 1000.0)
                pred = predict(name, fit, t, t_mot, exp["motion_ms"] / 1000.0)
                y = traces[:, :, held]
                ss_res = float(np.nansum((pred - y) ** 2))
                ss_tot = float(np.nansum((y - np.nanmean(y)) ** 2))
                lomo_r2.append(1.0 - ss_res / max(ss_tot, 1e-12))
            per_model[name] = {
                "lomo_r2_median": round(float(np.median(lomo_r2)), 4),
                "lomo_r2_mean": round(float(np.mean(lomo_r2)), 4),
            }
        # pre-stated discriminant: uniform-stationary difference at motion+100 ms
        i100 = int(np.argmin(np.abs(t - (t_mot + 0.1))))
        diff = traces[:, 0, :] - traces[:, 1, :]  # time x fly
        meas = diff[i100, :]
        disc = {
            "measured_diff_at_mot100_median": round(float(np.median(meas)), 3),
            "measured_diff_at_mot100_iqr": [round(float(x), 3) for x in np.percentile(meas, [25, 75])],
            "n_fly": g["n_fly"],
        }
        np.savez_compressed(args.output_dir / f"traces_{exp['name']}.npz", t=t, traces=traces)
        result[exp["name"]] = {"models": per_model, "discriminant": disc}
        print(exp["name"], json.dumps(result[exp["name"]], indent=2), flush=True)

    # between-experiment discriminant summary (data vs A (invariant) prediction)
    d666 = result["gap666"]["discriminant"]["measured_diff_at_mot100_median"]
    d500 = result["gap500"]["discriminant"]["measured_diff_at_mot100_median"]
    result["between_experiment"] = {
        "measured_contrast_666_minus_500": round(d666 - d500, 3),
        "model_A_prediction": "≈0 (gap-invariant at motion onset)",
        "model_B_prediction": "positive if evidence ramps during the gap (sign/magnitude depends on fitted tau)",
        "batch_confound": "experiments are different animal batches with different motion durations (T1 map) — between-experiment contrast is confounded, reported descriptively only",
    }
    (args.output_dir / "p3t_explore.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["between_experiment"], indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
