#!/usr/bin/env python3
"""P3-A baseline reproduction (benchmark only; no new biological claims).

Reproduce the Tanaka/Clark published dataset-level results at fly level for
three branches (T4/T5, LPTC, Mi4) as a pipeline-validation benchmark:
(1) reconstruct population mean traces from per-fly data and compare against
the authors' precomputed respMatPlot (per-epoch correlation);
(2) report the published qualitative directions (T4/T5 and LPTC not suppressed
by outside stationary checkers; Mi4 stationary-vs-flicker difference).
Independent unit is the fly throughout; ROIs are averaged within fly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.io import loadmat

from explore_fig4 import unwrap, fly_epoch_matrix, per_fly_matrices, integrate_epoch_matrix

AUDIT = Path("/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit")
FIG4_T4T5 = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-CE-FIG4-EXPLORE-01/staging/fig4_01_T4T5.mat")
LPTC = AUDIT / "fig4_02_LPTC.mat"
MI4 = AUDIT / "fig7_mi4.mat"
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-A-BASELINE-01/experiment/outputs")

LPTC_TYPES = ("HS", "CH", "H2", "Hx", "FD1")  # fig4_02_LPTC.m order
INTEG = (0.0, 3.0)


def load_var(path: Path, name: str):
    return unwrap(loadmat(path, variable_names=[name], squeeze_me=True, struct_as_record=False)[name])


def epoch_corr(ours: np.ndarray, ref: np.ndarray) -> dict:
    """ours/ref: time x epochs population mean traces."""
    rs, maxdiffs = [], []
    for e in range(min(ours.shape[1], ref.shape[1])):
        a, b = ours[:, e], ref[:, e]
        if np.std(a) > 1e-12 and np.std(b) > 1e-12:
            rs.append(float(np.corrcoef(a, b)[0, 1]))
        else:
            rs.append(float("nan"))
        maxdiffs.append(float(np.max(np.abs(a - b))))
    return {
        "n_epochs_compared": len(rs),
        "pearson_r_per_epoch": [round(r, 4) for r in rs],
        "min_r": round(float(np.nanmin(rs)), 4) if rs else None,
        "max_absdiff_per_epoch": [round(d, 5) for d in maxdiffs],
        "max_absdiff_overall": round(float(np.max(maxdiffs)), 5) if maxdiffs else None,
    }


def integrate_profile(group, time_len: int) -> np.ndarray:
    timeX = np.asarray(group.timeX, dtype=float) / 1000.0
    m = (timeX > INTEG[0]) & (timeX < INTEG[1])
    return m


def fly_mean_traces_T4T5(data) -> tuple[np.ndarray, dict]:
    names = ("T4a", "T5a", "T4b", "T5b")
    out = {}
    for tt, base in (("T4", 0), ("T5", 1)):
        merged: dict[int, list[np.ndarray]] = {}
        for sub, flip in ((base, False), (base + 2, True)):
            for fly_id, mat in per_fly_matrices(data[sub], flip).items():
                merged.setdefault(fly_id, []).append(mat)
        traces = [np.concatenate(mats, axis=2).mean(axis=2) for mats in merged.values()]
        out[tt] = np.stack(traces, axis=2)  # time x 8 x n_fly
    return None, out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: three-branch baseline reproduction (T4/T5, LPTC, Mi4)")
        return 0
    if args.selftest:
        ref = np.random.default_rng(0).normal(size=(38, 8))
        r = epoch_corr(ref + 0.01 * np.random.default_rng(1).normal(size=ref.shape), ref)
        assert r["min_r"] > 0.99 and r["max_absdiff_overall"] < 0.2
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    result: dict = {"note": "P3-A benchmark reproduction; no new biological claims; unit = fly"}

    # ---- T4/T5
    print("== T4/T5 ==", flush=True)
    data = load_var(FIG4_T4T5, "data")
    _, by_type = fly_mean_traces_T4T5(data)
    t4t5 = {}
    for tt, base in (("T4", 0), ("T5", 1)):
        pop = by_type[tt].mean(axis=2)  # time x 8
        ref = np.asarray(data[base].respMatPlot, dtype=float)
        t4t5[tt] = {"n_fly": int(by_type[tt].shape[2]), "vs_respMatPlot": epoch_corr(pop, ref)}
        np.savez_compressed(args.output_dir / f"t4t5_{tt}_flytraces.npz", fly_traces=by_type[tt])
    result["T4T5"] = t4t5
    print(json.dumps(t4t5, indent=2), flush=True)

    # ---- LPTC
    print("== LPTC ==", flush=True)
    data = load_var(LPTC, "data")
    lptc = {}
    for ci, g in enumerate(np.atleast_1d(data)):
        celltype = LPTC_TYPES[ci]
        timeX = np.asarray(g.timeX, dtype=float) / 1000.0
        is_integ = integrate_profile(g, len(timeX))
        flies = np.atleast_1d(g.fliesUsed)
        ind = np.atleast_1d(g.indFly)
        fly_integ, fly_traces = [], []
        for idx in range(len(ind)):
            mat = fly_epoch_matrix(ind[idx])  # 55 x 12 x R
            fly_traces.append(mat.mean(axis=2))
            fly_integ.append(mat.mean(axis=2)[is_integ].mean(axis=0))
        fly_integ = np.asarray(fly_integ)
        pop = np.stack(fly_traces, axis=2).mean(axis=2)
        ref = np.asarray(g.respMatPlot, dtype=float)
        figleg = [str(x).strip() for x in np.atleast_1d(g.figLeg).ravel()]
        entry = {
            "n_fly": int(len(ind)),
            "fly_ids": [int(x) for x in flies],
            "epochs": figleg,
            "vs_respMatPlot": epoch_corr(pop[:, -len(figleg):] if pop.shape[1] != len(figleg) else pop, ref),
            "mean_integ_per_epoch": np.round(fly_integ.mean(axis=0), 4).tolist(),
            "sem_integ_per_epoch": np.round(fly_integ.std(axis=0) / np.sqrt(len(ind)), 4).tolist(),
        }
        lptc[celltype] = entry
        np.savez_compressed(args.output_dir / f"lptc_{celltype}_flyinteg.npz", fly_integ=fly_integ, fly_ids=flies)
        print(celltype, "n_fly=", entry["n_fly"], "min_r=", entry["vs_respMatPlot"]["min_r"], flush=True)
    result["LPTC"] = lptc

    # ---- Mi4
    print("== Mi4 ==", flush=True)
    d = load_var(MI4, "data")
    timeX = np.asarray(d.timeX, dtype=float) / 1000.0
    is_integ = (timeX > INTEG[0]) & (timeX < INTEG[1])
    ind = np.atleast_1d(d.indFly)
    figleg = [str(x).strip() for x in np.atleast_1d(d.figLeg).ravel()]
    fly_integ, fly_traces = [], []
    for idx in range(len(ind)):
        snip = unwrap(unwrap(ind[idx].p8_combinedOpposites).snipMat)
        if snip.ndim == 1:
            snip = snip[:, None]
        cols = []
        for e in range(snip.shape[0]):
            traces = [np.asarray(unwrap(snip[e, r]), dtype=float) for r in range(snip.shape[1])]
            cols.append(np.mean(np.stack(traces, axis=1), axis=1))
        mat = np.stack(cols, axis=1)  # time x 2
        fly_traces.append(mat)
        fly_integ.append(mat[is_integ].mean(axis=0))
    fly_integ = np.asarray(fly_integ)
    pop = np.stack(fly_traces, axis=2).mean(axis=2)
    ref = np.asarray(d.respMatPlot, dtype=float)
    result["Mi4"] = {
        "n_fly": int(len(ind)),
        "epochs": figleg,
        "vs_respMatPlot": epoch_corr(pop, ref),
        "mean_integ_S_F": np.round(fly_integ.mean(axis=0), 4).tolist(),
        "sem_integ_S_F": np.round(fly_integ.std(axis=0) / np.sqrt(len(ind)), 4).tolist(),
        "per_fly_S_minus_F": np.round(fly_integ[:, 0] - fly_integ[:, 1], 4).tolist(),
    }
    np.savez_compressed(args.output_dir / "mi4_flyinteg.npz", fly_integ=fly_integ)
    print(json.dumps(result["Mi4"], indent=2), flush=True)

    (args.output_dir / "baseline_reproduction.json").write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE baseline_reproduction.json", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
