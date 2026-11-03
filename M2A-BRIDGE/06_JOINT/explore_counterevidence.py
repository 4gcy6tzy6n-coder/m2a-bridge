#!/usr/bin/env python3
"""EXPLORATORY round P3-CE-EXPLORE-01.

Reimplement the original MATLAB preprocess for Tanaka et al. counterevidence
fig3 sweeps, extract per-fly turn matrices (contrast and velocity sweeps), and
compute candidate graded-vs-gated discriminative statistics. Everything here is
exploratory; the confirmatory design is frozen in a later round.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.io import loadmat

MAT = Path(
    "/Users/yyl/Desktop/workshop/nature/runs/P3-CE-EXPLORE-01/staging/fig3_sweeps.mat"
)
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-CE-EXPLORE-01/experiment/outputs")


def unwrap(obj):
    # Only 0-d object arrays wrap a value; arr[()] on ndim>=1 returns the array
    # itself, which would loop forever.
    while isinstance(obj, np.ndarray) and obj.dtype == object and obj.ndim == 0:
        obj = obj[()]
    return obj
    return obj


def load_sweeps(*names: str) -> dict[str, object]:
    """Single loadmat pass: the 745 MB v5 mat is compressed, so each extra
    variable_names call would re-decompress the whole stream sequentially."""
    mats = loadmat(MAT, variable_names=list(names), squeeze_me=True, struct_as_record=False)
    return {name: unwrap(mats[name]) for name in names}


def turnmat_from_analysis(data, stim_dur: float = 3.0) -> np.ndarray:
    """Python port of the MATLAB preprocess(): per-fly mean angular velocity."""
    timeX = np.asarray(data.timeX, dtype=float) / 1000.0
    is_stim = (timeX > 0) & (timeX < stim_dur)
    ind_fly = unwrap(data.indFly)
    n_fly = len(ind_fly)
    per_fly: list[list[float]] = []
    skipped_cells = 0
    squeezed_reps1 = 0
    for ff in range(n_fly):
        fly = unwrap(ind_fly[ff])
        snip = unwrap(unwrap(fly.p8_averagedRois).snipMat)
        if snip.ndim == 1:
            snip = snip[:, None]  # ROIs==1 squeezed to (epochs,)
        ep_vals = []
        for e in range(snip.shape[0]):
            rois = np.atleast_1d(snip[e])
            ang = []
            for r in range(len(rois)):
                arr = np.asarray(unwrap(rois[r]), dtype=float)
                if arr.ndim == 3:  # time x reps x (angular, forward)
                    ang.append(arr[:, :, 0])
                elif arr.ndim == 2 and arr.shape[1] == 2:
                    ang.append(arr[:, 0][:, None])  # reps==1 squeezed by loadmat
                    squeezed_reps1 += 1
                else:
                    skipped_cells += 1
            if not ang:
                ep_vals.append(np.nan)
                continue
            stacked = np.concatenate(ang, axis=1)  # time x (reps*rois)
            ep_vals.append(float(np.nanmean(stacked[is_stim, :])))
        per_fly.append(ep_vals)
        if (ff + 1) % 10 == 0:
            print(f"  fly {ff + 1}/{n_fly}", flush=True)
    n_ep = max(len(r) for r in per_fly)
    out = np.full((n_fly, n_ep), np.nan)
    for ff, row in enumerate(per_fly):
        out[ff, : len(row)] = row
    print(
        f"turnmat done: {n_fly} flies x {n_ep} epochs; "
        f"skipped {skipped_cells} cells, {squeezed_reps1} reps==1 cells unwrapped",
        flush=True,
    )
    return out


def bimodality_coefficient(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 5 or np.var(x) == 0:
        return float("nan")
    m3 = np.mean((x - x.mean()) ** 3)
    m4 = np.mean((x - x.mean()) ** 4)
    skew2 = (m3 / np.var(x) ** 1.5) ** 2
    kurt = m4 / np.var(x) ** 2
    return float((skew2 + 1.0) / kurt)


def hill(c: np.ndarray, vmax: float, k: float, n: float = 1.0) -> np.ndarray:
    return vmax * np.power(c, n) / (np.power(k, n) + np.power(c, n) + 1e-12)


def lfo_cv_rmse(suppression: np.ndarray, contrasts: np.ndarray, n_fold: int = 5, gated: bool = False) -> float:
    """Leave-one-fly-out style K-fold CV RMSE of Hill(n=1) [graded] or Hill(n free) [gated]."""
    n_fly = suppression.shape[0]
    rng = np.random.default_rng(0)
    idx = rng.permutation(n_fly)
    folds = np.array_split(idx, n_fold)
    errs = []
    for test in folds:
        train = np.setdiff1d(idx, test)
        y_train = suppression[train].mean(axis=0)
        grid_n = (1.0, 2.0, 4.0, 8.0) if gated else (1.0,)
        best = (np.inf, None)
        for n in grid_n:
            def loss(params):
                vmax, k = params
                pred = hill(contrasts, vmax, k, n)
                return float(np.sum((pred - y_train) ** 2))
            # coarse grid search then refine
            for vmax in np.linspace(0.1, 120.0, 24):
                for k in np.linspace(0.02, 1.0, 12):
                    l = loss((vmax, k))
                    if l < best[0]:
                        best = (l, (vmax, k, n))
        pred_test = hill(contrasts, *best[1])
        errs.append(np.sqrt(np.mean((pred_test - suppression[test].mean(axis=0)) ** 2)))
    return float(np.mean(errs))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: load fig3 contrast+velocity sweeps, per-fly turnmat, candidate stats")
        return 0
    if args.selftest:
        obj1d = np.empty(2, dtype=object)
        obj1d[0] = {"a": 1}
        obj1d[1] = {"b": 2}
        assert unwrap(obj1d) is obj1d  # regression: 1-d object arrays must not loop
        # regression: squeeze Me leaves reps==1 cells as time x 2 (must use col 0)
        from types import SimpleNamespace

        rng = np.random.default_rng(0)
        cell3d = rng.normal(size=(40, 3, 2))
        cell2d = rng.normal(size=(40, 2))
        snip = np.empty((2, 2), dtype=object)
        snip[0, 0], snip[0, 1], snip[1, 0], snip[1, 1] = cell3d, cell2d, cell2d, cell3d
        fly = SimpleNamespace(p8_averagedRois=SimpleNamespace(snipMat=snip))
        ind = np.empty(1, dtype=object)
        ind[0] = fly
        fake = SimpleNamespace(timeX=np.arange(-50, 350, 10.0), indFly=ind)
        tm = turnmat_from_analysis(fake)
        assert tm.shape == (1, 2) and np.isfinite(tm).all(), tm
        x = np.concatenate([np.random.normal(0, 1, 500), np.random.normal(8, 0.5, 500)])
        assert bimodality_coefficient(x) > bimodality_coefficient(np.random.normal(0, 1, 1000))
        sup = np.abs(np.random.normal(30, 10, (20, 6)))
        cs = np.array([0, 0.1, 0.25, 0.5, 0.75, 1.0])
        assert lfo_cv_rmse(sup, cs, n_fold=4) > 0
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # ---- contrast + velocity sweeps (single decompression pass)
    print("loading fig3_sweeps.mat (single pass, both variables)...", flush=True)
    sweeps = load_sweeps("data_contrast", "data_velocity")
    print("mat loaded; extracting contrast turnmat...", flush=True)
    data_c = sweeps["data_contrast"]
    tm_c = turnmat_from_analysis(data_c)
    # staged checkpoint: keep the contrast half even if velocity extraction dies
    np.savez_compressed(args.output_dir / "turnmat_contrast_stage.npz", contrast_turnmat=tm_c)
    # folded epochs (per original script): 1=interleave, 2=0-contrast,
    # 3..12 = 5 contrasts x {stationary(odd), flicker(even)} in MATLAB 1-based
    contrasts = np.array([0.0, 0.1, 0.25, 0.5, 0.75, 1.0])
    stat_cols = [1] + list(range(2, 12, 2))   # 0-based: ep2,3,5,7,9,11
    flick_cols = [1] + list(range(3, 12, 2))  # ep2,4,6,8,10,12
    stat = tm_c[:, stat_cols]
    # suppression per fly per contrast: uniform(=0-contrast islands) minus stationary
    uniform0 = tm_c[:, 1][:, None]
    sup_contrast = uniform0 - stat  # n_fly x 6 (c=0 gives 0 by construction)
    bc_contrast = [bimodality_coefficient(sup_contrast[:, j]) for j in range(1, 6)]
    cv_graded = lfo_cv_rmse(sup_contrast[:, 1:], contrasts[1:], gated=False)
    cv_gated = lfo_cv_rmse(sup_contrast[:, 1:], contrasts[1:], gated=True)

    # ---- velocity sweep
    print("extracting velocity turnmat...", flush=True)
    data_v = sweeps["data_velocity"]
    tm_v = turnmat_from_analysis(data_v)
    vels = 10 * 2.0 ** np.arange(6)
    grey = tm_v[:, 0::3]
    statv = tm_v[:, 1::3]
    sup_vel = grey - statv  # n_fly x 6
    bc_vel = [bimodality_coefficient(sup_vel[:, j]) for j in range(6)]

    np.savez_compressed(
        args.output_dir / "turnmat_fig3.npz",
        contrast_turnmat=tm_c,
        velocity_turnmat=tm_v,
        contrasts=contrasts,
        velocities=vels,
    )
    summary = {
        "n_fly_contrast": int(tm_c.shape[0]),
        "n_epoch_contrast": int(tm_c.shape[1]),
        "n_fly_velocity": int(tm_v.shape[0]),
        "n_epoch_velocity": int(tm_v.shape[1]),
        "contrast_mean_turn_stat": np.nanmean(stat, axis=0).round(3).tolist(),
        "contrast_mean_turn_flicker": np.nanmean(tm_c[:, flick_cols], axis=0).round(3).tolist(),
        "contrast_mean_suppression": np.nanmean(sup_contrast, axis=0).round(3).tolist(),
        "contrast_bimodality_by_level": [round(float(b), 3) for b in bc_contrast],
        "lfo_cv_rmse_graded_hill1": round(cv_graded, 3),
        "lfo_cv_rmse_gated_hillN": round(cv_gated, 3),
        "velocity_mean_suppression": np.nanmean(sup_vel, axis=0).round(3).tolist(),
        "velocity_bimodality_by_level": [round(float(b), 3) for b in bc_vel],
        "note": "EXPLORATORY: numbers here are for designing a frozen confirmatory test, not for claims",
    }
    (args.output_dir / "exploration.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
