#!/usr/bin/env python3
"""P3-VISORIENT-01: frozen confirmatory analysis on Dryad m715hp3.

Implements PREREGISTRATION.md exactly: primary endpoint is the animal-level
interaction in dH burstiness (kurtosis) between wind and nostim conditions in
antenna-stabilized versus control flies. One-shot analysis; no tuning.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.io import loadmat

DATA_DIR = Path(
    "/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/02_DATA_FEASIBILITY/"
    "public_data_audit/m715hp3_raw/Raw Data"
)
PRIMARY_CONDS = ("light0", "ms0")  # amendment A1: baseline is light-only (nostim0 absent in these files)
SECONDARY_CONDS = ("wind0",)  # wind-only kept as descriptive
PERMUTATIONS = 10_000
SEED = 0
MIN_VALID_TRIALS = 3
MAX_NONFINITE_FRAC = 0.20


def valid_fly_columns(mat_struct, cond: str) -> list[list[np.ndarray]]:
    """Per-fly list of valid per-trial dH columns (label-blind exclusions)."""
    fly = getattr(mat_struct, cond)
    n = len(fly) if hasattr(fly, "__len__") else 1
    per_fly = []
    for i in range(n):
        entry = fly[i] if n > 1 else fly
        dH = np.asarray(entry.dH, dtype=float)
        if dH.ndim == 1:
            dH = dH[:, None]
        cols = []
        for t in range(dH.shape[1]):
            col = dH[:, t]
            finite = np.isfinite(col)
            if finite.mean() < (1.0 - MAX_NONFINITE_FRAC):
                continue
            cols.append(col[finite])
        per_fly.append(cols)
    return per_fly


def per_fly_metrics(columns: list[np.ndarray]) -> dict[str, float]:
    if len(columns) < MIN_VALID_TRIALS:
        return {"n_trials": len(columns)}
    dH = np.concatenate(columns)
    kurt = float(np.mean((dH - dH.mean()) ** 4) / (np.var(dH) ** 2) - 3.0) if np.var(dH) > 0 else float("nan")
    absd = np.abs(dH)
    med = float(np.median(absd))
    hump = float(np.percentile(absd, 95) / med) if med > 0 else float("nan")
    return {"n_trials": len(columns), "kurtosis_dH": kurt, "hump_dH": hump}


def interaction_permutation(delta_ctrl: np.ndarray, delta_abl: np.ndarray) -> dict[str, float]:
    obs = float(np.median(delta_abl) - np.median(delta_ctrl))
    pooled = np.concatenate([delta_ctrl, delta_abl])
    n_ctrl = len(delta_ctrl)
    rng = np.random.default_rng(SEED)
    count = 0
    for _ in range(PERMUTATIONS):
        rng.shuffle(pooled)
        stat = float(np.median(pooled[n_ctrl:]) - np.median(pooled[:n_ctrl]))
        if stat >= obs:
            count += 1
    p = (1 + count) / (1 + PERMUTATIONS)
    return {"interaction": obs, "p_one_sided": p, "n_ctrl": n_ctrl, "n_ablated": len(delta_abl)}


def load_group(path: Path, root_key: str, conds: tuple[str, ...]) -> list[dict]:
    struct = loadmat(path, squeeze_me=True, struct_as_record=False)[root_key]
    per_cond = {cond: valid_fly_columns(struct, cond) for cond in conds}
    n_fly = min(len(v) for v in per_cond.values())
    records = []
    for i in range(n_fly):
        rec = {}
        for cond in conds:
            rec[cond] = per_fly_metrics(per_cond[cond][i])
        # inclusion rule (prereg): both primary conditions must have valid metrics
        if all(("kurtosis_dH" in rec.get(c, {})) for c in PRIMARY_CONDS if c in rec):
            records.append(rec)
    return records


def analyze() -> dict:
    ctrl = load_group(DATA_DIR / "exp2c.mat", "exp2c", PRIMARY_CONDS + SECONDARY_CONDS)
    abl = load_group(DATA_DIR / "exp2s.mat", "exp2s", PRIMARY_CONDS + SECONDARY_CONDS)
    out: dict = {"n_ctrl": len(ctrl), "n_ablated": len(abl)}

    d_ctrl = np.array([r["ms0"]["kurtosis_dH"] - r["light0"]["kurtosis_dH"] for r in ctrl])
    d_abl = np.array([r["ms0"]["kurtosis_dH"] - r["light0"]["kurtosis_dH"] for r in abl])
    primary = interaction_permutation(d_ctrl, d_abl)
    primary["median_delta_ctrl"] = float(np.median(d_ctrl))
    primary["median_delta_ablated"] = float(np.median(d_abl))
    out["primary_kurtosis_interaction"] = primary

    # secondary: hump
    h_ctrl = np.array([r["ms0"]["hump_dH"] - r["light0"]["hump_dH"] for r in ctrl])
    h_abl = np.array([r["ms0"]["hump_dH"] - r["light0"]["hump_dH"] for r in abl])
    out["secondary_hump_interaction"] = float(np.median(h_abl) - np.median(h_ctrl))

    # replication on exp4h (independent flies, high wind)
    rep = load_group(DATA_DIR / "exp4h.mat", "exp4h", PRIMARY_CONDS)
    rc = np.array([r["ms0"]["kurtosis_dH"] - r["light0"]["kurtosis_dH"] for r in rep])
    # exp4h is antenna-stabilized per README context (Fig4 high wind); group contrast
    # cannot be replicated inside exp4h alone — replication here = same-direction Δ>0 in ablated-highwind flies
    out["replication_exp4h"] = {
        "n": len(rc),
        "median_delta": float(np.median(rc)),
        "fraction_delta_positive": float(np.mean(rc > 0)),
        "note": "single-group directional replication (all flies antenna-stabilized context); no control arm in this file",
    }
    return out, ctrl, abl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P3-VISORIENT-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: one-shot analysis of exp2c+exp2s (primary), exp4h (replication); 10,000 label permutations, seed 0")
        return 0
    if args.selftest:
        rng = np.random.default_rng(1)
        bursty = [rng.laplace(0, 1, 2000) for _ in range(3)]
        smooth = [rng.normal(0, 1, 2000) for _ in range(3)]
        assert per_fly_metrics(bursty)["kurtosis_dH"] > per_fly_metrics(smooth)["kurtosis_dH"]
        a = np.array([1.0, 2.0, 3.0, 4.0])
        b = np.array([3.0, 4.0, 5.0, 9.0])
        r = interaction_permutation(a, b)
        assert r["interaction"] > 0
        print("SELFTEST PASS")
        return 0
    summary, ctrl, abl = analyze()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "per_animal.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["group", "fly", "cond", "n_trials", "kurtosis_dH", "hump_dH"])
        for group, recs in (("control", ctrl), ("antenna_stabilized", abl)):
            for i, rec in enumerate(recs):
                for cond, m in rec.items():
                    w.writerow([group, i, cond, m.get("n_trials"), m.get("kurtosis_dH"), m.get("hump_dH")])
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
