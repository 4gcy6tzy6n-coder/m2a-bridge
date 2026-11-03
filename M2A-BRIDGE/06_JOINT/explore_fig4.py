#!/usr/bin/env python3
"""EXPLORATORY round P3-CE-FIG4-EXPLORE-01.

Stage A (--inspect): dump the real structure of fig4_01_T4T5.mat (shapes of
data{1..4}, fliesUsed, indFly snipMat cells) so the port of fig4_01_T4T5.m is
written against observed dims, not guesses. Stage B (default run): port the
preprocess and compute candidate suppression-distribution statistics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.io import loadmat

MAT = Path(
    "/Users/yyl/Desktop/workshop/nature/runs/P3-CE-FIG4-EXPLORE-01/staging/fig4_01_T4T5.mat"
)
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-CE-FIG4-EXPLORE-01/experiment/outputs")


def unwrap(obj):
    while isinstance(obj, np.ndarray) and obj.dtype == object and obj.ndim == 0:
        obj = obj[()]
    return obj


def describe(obj, depth: int = 0, max_depth: int = 4) -> dict:
    obj = unwrap(obj)
    if isinstance(obj, np.ndarray):
        info = {"type": "ndarray", "shape": list(obj.shape), "dtype": str(obj.dtype)}
        if obj.dtype == object and depth < max_depth:
            flat = obj.ravel()
            info["elem0"] = describe(flat[0], depth + 1, max_depth)
            info["n_elem"] = int(flat.size)
        return info
    if hasattr(obj, "_fieldnames"):
        return {
            "type": "mat_struct",
            "fields": {f: describe(getattr(obj, f), depth + 1, max_depth) for f in obj._fieldnames},
        }
    if hasattr(obj, "__dict__") and vars(obj):
        return {
            "type": type(obj).__name__,
            "fields": {k: describe(v, depth + 1, max_depth) for k, v in vars(obj).items()},
        }
    return {"type": type(obj).__name__, "repr": repr(obj)[:120]}


def load_data():
    return unwrap(loadmat(MAT, variable_names=["data"], squeeze_me=True, struct_as_record=False)["data"])


# Observed structure (structure_dump.json): 4 groups T4a/T5a/T4b/T5b;
# p8_combinedOpposites.snipMat is an (8 epochs x R ROIs) object grid (R==1
# squeezes to (8,)); each cell is a 1-D 38-sample dF/F trace (trials already
# averaged, opposite directions already combined).
EPOCH_FLIP_B = (0, 1, 3, 2, 5, 4, 7, 6)  # MATLAB [1,2,4,3,6,5,8,7], 0-based
DIR_SETS = ((1, 3, 5), (2, 4, 6))  # {uniform, stationary, flicker} per direction
INTEG_T_RANGE = (0.0, 3.0)


def fly_epoch_matrix(ind_fly_entry) -> np.ndarray:
    """38 x 8 x R trace matrix for one fly from its snipMat grid."""
    snip = unwrap(unwrap(ind_fly_entry.p8_combinedOpposites).snipMat)
    if snip.ndim == 1:
        snip = snip[:, None]  # R==1 squeezed to (8,)
    traces = []
    for r in range(snip.shape[1]):
        cols = []
        for e in range(snip.shape[0]):
            trace = np.asarray(unwrap(snip[e, r]), dtype=float)
            cols.append(trace)
        traces.append(np.stack(cols, axis=1))  # 38 x 8
    return np.stack(traces, axis=2)  # 38 x 8 x R


def per_fly_matrices(group, flip_b: bool) -> dict[int, np.ndarray]:
    """fly_id -> 38 x 8 x R trace matrix (flip applied to b-group epochs)."""
    flies_used = [int(x) for x in np.atleast_1d(group.fliesUsed)]
    by_fly: dict[int, list[np.ndarray]] = {}
    for idx, fly_id in enumerate(flies_used):
        mat = fly_epoch_matrix(group.indFly[idx])  # 38 x 8 x R
        if flip_b:
            mat = mat[:, EPOCH_FLIP_B, :]
        by_fly.setdefault(fly_id, []).append(mat)
    return {fid: np.concatenate(mats, axis=2) for fid, mats in by_fly.items()}


def integrate_epoch_matrix(group, mat: np.ndarray) -> np.ndarray:
    """38 x 8 -> 8-vector mean dF/F over the integration window."""
    timeX = np.asarray(group.timeX, dtype=float) / 1000.0
    is_integ = (timeX > INTEG_T_RANGE[0]) & (timeX < INTEG_T_RANGE[1])
    return mat.mean(axis=2)[is_integ].mean(axis=0)


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


def type_suppression(integ: dict[int, np.ndarray]) -> tuple[np.ndarray, list[int]]:
    """Per fly: PD-chosen set (larger uniform response) suppression values.

    Returns (n_fly x 3 array of {uniform, stationary, flicker} for the PD set,
    fly ids). PD-set choice is label-blind and exploratory only.
    """
    rows, ids = [], sorted(integ)
    for fly_id in ids:
        v = integ[fly_id]
        means = [float(np.mean(v[list(s)])) for s in DIR_SETS]
        s = DIR_SETS[int(np.argmax(means))]
        rows.append([float(v[s[0]]), float(v[s[1]]), float(v[s[2]])])
    return np.asarray(rows), ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: load fig4_01_T4T5.mat 'data' cell, dump structure, port preprocess")
        return 0
    if args.selftest:
        obj1d = np.empty(2, dtype=object)
        obj1d[0] = {"a": 1}
        obj1d[1] = {"b": 2}
        assert unwrap(obj1d) is obj1d
        fake = SimpleNamespace(x=np.array([[1.0, 2.0]]))
        d = describe(fake)
        assert d["fields"]["x"]["shape"] == [1, 2]
        # snipMat grid contract: 2 ROIs x 8 epochs of 38-traces -> 38x8x2
        snip = np.empty((8, 2), dtype=object)
        for e in range(8):
            for r in range(2):
                snip[e, r] = np.arange(38.0) + 100 * e + r
        entry = SimpleNamespace(p8_combinedOpposites=SimpleNamespace(snipMat=snip))
        mat = fly_epoch_matrix(entry)
        assert mat.shape == (38, 8, 2) and mat[0, 3, 1] == 300.0 + 1.0
        snip1 = snip[:, 0]
        mat1 = fly_epoch_matrix(SimpleNamespace(p8_combinedOpposites=SimpleNamespace(snipMat=snip1)))
        assert mat1.shape == (38, 8, 1)
        assert list(np.array(EPOCH_FLIP_B)[list(EPOCH_FLIP_B)]) == list(range(8))
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    print("loading data cell (1.1 GB mat, single variable)...", flush=True)
    data = load_data()
    if args.inspect:
        print(f"data: {type(data).__name__}, len={len(data)}", flush=True)
        dump = {"n_groups": len(data), "groups": [describe(data[i], max_depth=5) for i in range(len(data))]}
        (args.output_dir / "structure_dump.json").write_text(json.dumps(dump, indent=2) + "\n")
        print("structure dump written", flush=True)
        return 0

    # Stage B: per-fly integrated responses (groups: T4a, T5a, T4b, T5b)
    names = ("T4a", "T5a", "T4b", "T5b")
    integ_by_type: dict[str, dict[int, np.ndarray]] = {}
    for tt, base in (("T4", 0), ("T5", 1)):
        merged: dict[int, list[np.ndarray]] = {}
        for sub, flip in ((base, False), (base + 2, True)):
            print(f"extracting group {names[sub]}...", flush=True)
            for fly_id, mat in per_fly_matrices(data[sub], flip).items():
                merged.setdefault(fly_id, []).append(mat)
        integ_by_type[tt] = {
            fid: integrate_epoch_matrix(data[base], np.concatenate(mats, axis=2))
            for fid, mats in merged.items()
        }
        print(f"{tt}: {len(integ_by_type[tt])} unique flies", flush=True)

    summary: dict = {"n_fly": {t: len(v) for t, v in integ_by_type.items()}, "suppression": {}}
    npz_payload = {}
    for tt, integ in integ_by_type.items():
        supp, ids = type_suppression(integ)
        npz_payload[f"integ_{tt}"] = np.asarray([integ[i] for i in sorted(integ)])
        npz_payload[f"fly_ids_{tt}"] = np.asarray(sorted(integ))
        npz_payload[f"supp_pd_{tt}"] = supp
        sup_stat = supp[:, 0] - supp[:, 1]
        sup_flick = supp[:, 0] - supp[:, 2]
        summary["suppression"][tt] = {
            "mean_uniform_stationary": round(float(np.mean(sup_stat)), 4),
            "mean_uniform_flicker": round(float(np.mean(sup_flick)), 4),
            "bimodality_uniform_stationary": round(bimodality_coefficient(sup_stat), 3),
            "bimodality_uniform_flicker": round(bimodality_coefficient(sup_flick), 3),
            "per_fly_uniform_stationary": np.round(sup_stat, 4).tolist(),
            "per_fly_uniform_flicker": np.round(sup_flick, 4).tolist(),
        }
    np.savez_compressed(args.output_dir / "neural_integ.npz", **npz_payload)
    summary["note"] = "EXPLORATORY: for designing a frozen confirmatory neural round; no claims"
    (args.output_dir / "neural_explore.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
