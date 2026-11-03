#!/usr/bin/env python3
"""P3-ROUND-2 confirmatory analysis (single-shot; frozen preregistration).

Graded-vs-gated model selection on the FROZEN fig3 contrast-sweep turnmat
(P3-CE-EXPLORE-01 product). Implements PREREGISTRATION.md sections 2-5 exactly:
nested leave-one-fly-out CV (gated family n in {2,4,8} selected inside each
outer training fold), parametric-bootstrap null B=2000 seed 20261028, and the
bimodality secondary endpoints. Never reads the raw .mat.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

NPZ_PATH = Path(
    "/Users/yyl/Desktop/workshop/nature/runs/P3-CE-EXPLORE-01/experiment/outputs/turnmat_fig3.npz"
)
NPZ_SHA256 = "f04f22b400e2cd9bd3a961696d4812401efe2f0348429e0dd30f8ddce4cb93ce"
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-ROUND-2/experiment/outputs")

CONTRASTS = np.array([0.1, 0.25, 0.5, 0.75, 1.0])
UNIFORM_COL = 1
STAT_COLS = (2, 4, 6, 8, 10)
USED_COLS = (1, 2, 4, 6, 8, 10)
GATED_N_FAMILY = (2.0, 4.0, 8.0)
B_BOOT = 2000
SEED = 20261028
SEED_BC = 20261029
BC_REFERENCE = 0.555  # Sarle bimodality reference line (prereg section 5)
EXCL_MAX_NONFINITE_FRAC = 0.2


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hill(c: np.ndarray, vmax: float, k: float, n: float) -> np.ndarray:
    return vmax * np.power(c, n) / (np.power(k, n) + np.power(c, n))


def fit_hill(mean_curve: np.ndarray, n: float) -> tuple[float, float]:
    vmax0 = float(min(np.max(mean_curve) * 1.2, 499.0))
    def residual(params):
        vmax, k = params
        return hill(CONTRASTS, vmax, k, n) - mean_curve
    result = least_squares(residual, x0=[vmax0, 0.3], bounds=([0.0, 1e-3], [500.0, 10.0]), max_nfev=200)
    vmax, k = result.x
    return float(vmax), float(k)


def fly_rmse(pred: np.ndarray, fly_sup: np.ndarray) -> float:
    return float(np.sqrt(np.mean((pred - fly_sup) ** 2)))


def inner_select_n(train_sup: np.ndarray) -> float:
    """4-fold LFO on training flies; returns n with min mean fly-level RMSE (ties -> smaller n)."""
    rng = np.random.default_rng(SEED)
    idx = rng.permutation(train_sup.shape[0])
    folds = np.array_split(idx, 4)
    scores = []
    for n in GATED_N_FAMILY:
        total, count = 0.0, 0
        for test in folds:
            test = test[test >= 0]
            if test.size == 0:
                continue
            inner_train = np.setdiff1d(np.arange(train_sup.shape[0]), test)
            params = fit_hill(train_sup[inner_train].mean(axis=0), n)
            pred = hill(CONTRASTS, *params, n)
            for t in test:
                total += fly_rmse(pred, train_sup[t])
                count += 1
        scores.append(total / max(count, 1))
    return GATED_N_FAMILY[int(np.argmin(scores))]


def nested_delta(sup: np.ndarray) -> tuple[float, list[dict]]:
    """Outer LFO; returns (delta, per-fly records). Same seed for inner folds on every call."""
    n_fly = sup.shape[0]
    records = []
    for i in range(n_fly):
        train = np.delete(sup, i, axis=0)
        graded_params = fit_hill(train.mean(axis=0), 1.0)
        graded_pred = hill(CONTRASTS, *graded_params, 1.0)
        n_hat = inner_select_n(train)
        gated_params = fit_hill(train.mean(axis=0), n_hat)
        gated_pred = hill(CONTRASTS, *gated_params, n_hat)
        records.append(
            {
                "fly": i,
                "graded_rmse": fly_rmse(graded_pred, sup[i]),
                "gated_rmse": fly_rmse(gated_pred, sup[i]),
                "gated_n_selected": float(n_hat),
            }
        )
    delta = float(np.mean([r["gated_rmse"] for r in records]) - np.mean([r["graded_rmse"] for r in records]))
    return delta, records


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


def bc_with_bootstrap(sup_j: np.ndarray, rng: np.random.default_rng, b: int) -> dict:
    bc_obs = bimodality_coefficient(sup_j)
    n = sup_j.shape[0]
    draws = np.empty(b)
    for i in range(b):
        sample = sup_j[rng.integers(0, n, n)]
        draws[i] = bimodality_coefficient(sample)
    lo, hi = np.nanpercentile(draws, [2.5, 97.5])
    p_above = float((1 + np.sum(draws <= BC_REFERENCE)) / (b + 1))  # P(BC* <= ref): evidence CI-lower > ref
    return {"bc_obs": bc_obs, "ci_low": float(lo), "ci_high": float(hi), "p_le_ref": p_above}


def holm_adjust(pvals: list[float]) -> list[float]:
    order = np.argsort(pvals)
    adjusted = [0.0] * len(pvals)
    running = 0.0
    m = len(pvals)
    for rank, oi in enumerate(order):
        val = min(1.0, (m - rank) * pvals[oi])
        running = max(running, val)
        adjusted[oi] = running
    return adjusted


def build_sup(turnmat: np.ndarray) -> tuple[np.ndarray, list[int]]:
    used = turnmat[:, list(USED_COLS)]
    keep = [f for f in range(turnmat.shape[0]) if np.isfinite(used[f]).mean() > EXCL_MAX_NONFINITE_FRAC]
    uniform0 = turnmat[keep, UNIFORM_COL][:, None]
    stat = turnmat[np.ix_(keep, STAT_COLS)]
    return uniform0 - stat, keep


def run_analysis(sup: np.ndarray, b_boot: int) -> dict:
    delta_obs, records = nested_delta(sup)
    theta_hat = fit_hill(sup.mean(axis=0), 1.0)
    null_curve = hill(CONTRASTS, *theta_hat, 1.0)
    residuals = sup - null_curve[None, :]
    rng = np.random.default_rng(SEED)
    n = sup.shape[0]
    delta_star = np.empty(b_boot)
    for b in range(b_boot):
        idx = rng.integers(0, n, n)
        sup_star = null_curve[None, :] + residuals[idx]
        delta_star[b], _ = nested_delta(sup_star)
        if (b + 1) % 200 == 0:
            print(f"  bootstrap {b + 1}/{b_boot}", flush=True)
    p_one_sided = float((1 + np.sum(delta_star <= delta_obs)) / (b_boot + 1))
    delta_crit = float(abs(np.quantile(delta_star, 0.05)))
    bc_rng = np.random.default_rng(SEED_BC)
    secondary = {
        "contrast_0.75": bc_with_bootstrap(sup[:, 3], bc_rng, 2000),
        "contrast_1.0": bc_with_bootstrap(sup[:, 4], bc_rng, 2000),
    }
    pvals = [secondary[k]["p_le_ref"] for k in ("contrast_0.75", "contrast_1.0")]
    for key, adj in zip(("contrast_0.75", "contrast_1.0"), holm_adjust(pvals)):
        secondary[key]["p_holm"] = adj
    return {
        "delta_obs": delta_obs,
        "p_one_sided": p_one_sided,
        "decision": "prefers_gated" if p_one_sided < 0.05 else "did_not_distinguish",
        "delta_crit_abs": delta_crit,
        "inconclusive_by_resolution": bool(abs(delta_obs) < delta_crit),
        "delta_star_5pct": float(np.quantile(delta_star, 0.05)),
        "delta_star_median": float(np.median(delta_star)),
        "bimodality_secondary": secondary,
        "per_fly": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: verify npz hash, build sup (19x5), nested LFO delta,")
        print(f"parametric bootstrap B={B_BOOT} seed={SEED}, bimodality secondary")
        return 0
    if args.selftest:
        rng = np.random.default_rng(7)
        c_grid = CONTRASTS
        graded = np.stack([60.0 * c_grid / (0.3 + c_grid) + rng.normal(0, 1.0, 5) for _ in range(12)])
        d_graded, _ = nested_delta(graded)
        gated = np.stack([
            np.where(c_grid < 0.4, rng.normal(0, 0.5, 5), 25.0 * c_grid / (0.2 + c_grid) + rng.normal(0, 1.0, 5))
            for _ in range(12)
        ])
        d_gated, _ = nested_delta(gated)
        # graded truth: gated family cannot represent n=1, so Delta should not favor gated
        assert d_graded > -0.5, d_graded
        # thresholded truth: Delta should clearly favor the gated family
        assert d_gated < -1.0, d_gated
        assert holm_adjust([0.01, 0.04]) == [0.02, 0.04]
        fake_tm = np.arange(3 * 12, dtype=float).reshape(3, 12)
        sup_demo, keep_demo = build_sup(fake_tm)
        assert keep_demo == [0, 1, 2] and sup_demo.shape == (3, 5)
        assert np.allclose(sup_demo[0], fake_tm[0, 1] - fake_tm[0, list(STAT_COLS)])
        bc_bi = bimodality_coefficient(np.concatenate([rng.normal(0, 1, 400), rng.normal(6, 0.4, 400)]))
        bc_uni = bimodality_coefficient(rng.normal(0, 1, 800))
        assert bc_bi > bc_uni
        try:
            import tempfile
            bad = Path(tempfile.mkstemp(suffix=".npz")[1])
            bad.write_bytes(b"not-an-npz")
            assert sha256_file(bad) != NPZ_SHA256
        finally:
            bad.unlink(missing_ok=True)
        print("SELFTEST PASS")
        return 0

    actual_hash = sha256_file(NPZ_PATH)
    if actual_hash != NPZ_SHA256:
        raise SystemExit(f"FATAL: npz hash mismatch: {actual_hash}")
    print(f"npz hash OK: {actual_hash}", flush=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    turnmat = np.load(NPZ_PATH)["contrast_turnmat"]
    sup, keep = build_sup(turnmat)
    excluded = sorted(set(range(turnmat.shape[0])) - set(keep))
    print(f"sup matrix: {sup.shape[0]} flies x {sup.shape[1]} contrasts; excluded: {excluded}", flush=True)

    result = run_analysis(sup, B_BOOT)
    result.update(
        {
            "n_fly": int(sup.shape[0]),
            "excluded_flies": excluded,
            "b_boot": B_BOOT,
            "seed": SEED,
            "seed_bc": SEED_BC,
            "npz_sha256": actual_hash,
            "preregistration": "runs/P3-ROUND-2/PREREGISTRATION.md",
            "note": "confirmatory single-shot per frozen preregistration; interpretation boundaries in prereg section 7",
        }
    )
    (args.output_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    with (args.output_dir / "per_fly.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["fly", "graded_rmse", "gated_rmse", "gated_n_selected"])
        for r in result["per_fly"]:
            writer.writerow([r["fly"], r["graded_rmse"], r["gated_rmse"], r["gated_n_selected"]])
    print(json.dumps({k: v for k, v in result.items() if k != "per_fly"}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
