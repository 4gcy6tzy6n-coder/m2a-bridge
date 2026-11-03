#!/usr/bin/env python3
"""P3-F F2 identifiability analysis (D11-approved; governed by
COMPETING_MECHANISMS_PREREG.md + Amendment A1).

Question: under identical visual stimulus structure, does PAST motor history
add held-out predictive information for HS membrane potential beyond a
visual-history model? Models (capacity-matched, linear ridge on fixed bases):

  H0     : visual-history features only
  H0noise: H0 + equal-size white-noise feature branch (capacity control)
  H1     : H0 + strictly-causal past-motor-history features (lags >= 20 ms)

Bias guards (frozen): no same-timepoint behavior inputs; no cell/trial
selection by Vm sign; animal-level splits decided before any fitting; ridge
lambda selected inside training animals only. Independent unit = animal.
Claim limit: a positive result is "additional predictive information" only.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import h5py
import numpy as np
from scipy.signal import resample_poly

RAW = Path(
    "/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/fs2022_audit/raw"
)
OUT = Path("/Users/yyl/Desktop/workshop/nature/runs/P3-F-F2-01/experiment/outputs")

FS_TARGET = 500.0
VIS_KERNELS = 8  # raised-cosine bases on time-since-stim-onset, 0..1.5 s
VIS_SPAN_S = 1.5
MOTOR_LAG_MS = (20.0, 500.0)  # strictly causal window
MOTOR_KERNELS = 8
RIDGE_GRID = (1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0)
SEED = 20261028
MARKER_ON_V = 1.5  # marker 0/3 V -> threshold

ANIMAL_RE = re.compile(
    r"^(?P<fly>[Ff]ly\d+)_(?P<geno>[^_]+(?:x[^_]+)*)_age_\d+d_cell\d+_[Ll]ooming_wb_(?P<date>\d{4}_\d{2}_\d{2})"
)


def animal_key(fname: str) -> str | None:
    m = ANIMAL_RE.match(fname)
    if not m:
        return None
    return f"{m['fly']}_{m['geno']}_{m['date']}"


def raised_cosine_edges(n: int, span_s: float, fs: float) -> np.ndarray:
    centers = np.linspace(span_s / (2 * n), span_s - span_s / (2 * n), n)
    width = span_s / n
    return np.stack([centers, np.full(n, width)], axis=1)


def conv_basis(event_times_s: np.ndarray, t: np.ndarray, centers: np.ndarray, width: float) -> np.ndarray:
    """Causal raised-cosine events -> features (len(t) x n_basis)."""
    dt = t[1] - t[0]
    n = len(t)
    out = np.zeros((n, centers.shape[0]))
    lag_max = int(np.ceil((centers[-1] + width) / dt))
    for e in event_times_s:
        i0 = int(np.round(e / dt))
        if i0 < 0 or i0 >= n:
            continue
        L = min(lag_max, n - i0)
        lags = np.arange(L) * dt
        for b, c in enumerate(centers):
            v = 0.5 * (1 + np.cos(np.pi * np.clip((lags - c) / width, -1, 1)))
            out[i0 : i0 + L, b] += v
    return out


def load_session(path: Path) -> dict | None:
    try:
        with h5py.File(path, "r") as f:
            srate = float(f["experParams/srate"][0, 0])
            d = f["data"][:]
    except OSError:
        return None
    if d.shape[0] < 5:
        return None
    vm, wba_l, wba_r, marker = d[0], d[1], d[2], d[4]
    up = int(round(srate / FS_TARGET))
    if up < 2:
        return None
    vm = resample_poly(vm, 1, up)
    m = resample_poly(wba_r - wba_l, 1, up)
    mk = resample_poly(marker, 1, up)
    t = np.arange(len(vm)) / FS_TARGET
    on = (mk[:-1] < MARKER_ON_V) & (mk[1:] >= MARKER_ON_V)
    onset_times = t[1:][on]
    return {"vm": vm, "motor": m, "onsets": onset_times, "dur_s": float(t[-1]), "srate_raw": srate}


def features(sess: dict, noise_rng: np.random.Generator, with_motor: bool, with_noise: bool) -> np.ndarray:
    vm = sess["vm"]
    n = len(vm)
    t = np.arange(n) / FS_TARGET
    dt = 1.0 / FS_TARGET
    cols = [np.ones((n, 1))]
    centers = raised_cosine_edges(VIS_KERNELS, VIS_SPAN_S, FS_TARGET)[:, 0]
    width = VIS_SPAN_S / VIS_KERNELS
    cols.append(conv_basis(sess["onsets"], t, centers, width))
    if with_motor:
        lag_centers = np.linspace(MOTOR_LAG_MS[0] / 1000, MOTOR_LAG_MS[1] / 1000, MOTOR_KERNELS)
        lag_w = (MOTOR_LAG_MS[1] - MOTOR_LAG_MS[0]) / 1000 / MOTOR_KERNELS
        motor_f = np.zeros((n, MOTOR_KERNELS))
        m = sess["motor"]
        hi = int(round(MOTOR_LAG_MS[1] / 1000 / dt))
        lo_full = int(round(MOTOR_LAG_MS[0] / 1000 / dt))
        for b, c in enumerate(lag_centers):
            k_full = np.zeros(hi + 1)
            lags = np.arange(lo_full, hi + 1) * dt
            k_full[lo_full:] = 0.5 * (1 + np.cos(np.pi * np.clip((lags - c) / lag_w, -1, 1)))
            motor_f[:, b] = np.convolve(m, k_full, mode="full")[:n]
        cols.append(motor_f)
    if with_noise:
        cols.append(noise_rng.standard_normal((n, MOTOR_KERNELS)))
    return np.concatenate(cols, axis=1)


def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mu = X.mean(axis=0)
    sd = X.std(axis=0) + 1e-9
    Xs = np.column_stack([np.ones(len(y)), (X - mu) / sd])
    W = np.linalg.solve(Xs.T @ Xs + lam * np.eye(Xs.shape[1]), Xs.T @ y)
    return W, mu, sd


def r2_score(X: np.ndarray, y: np.ndarray, W: np.ndarray, mu: np.ndarray, sd: np.ndarray) -> float:
    Xs = np.column_stack([np.ones(len(y)), (X - mu) / sd])
    pred = Xs @ W
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / max(ss_tot, 1e-12)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="run on up to 2 animals")
    args = parser.parse_args()
    if args.dry_run:
        print("DRY RUN: H0 vs H0noise vs H1 on F&S looming sessions, LOMO by animal")
        return 0
    if args.selftest:
        rng = np.random.default_rng(0)
        n = 5000
        m = np.zeros(n)
        m[1000:1200] = 2.0
        vm = np.convolve(m, np.exp(-np.arange(50) / 10.0), "full")[:n] + rng.normal(0, 0.1, n)
        sess = {"vm": vm, "motor": m, "onsets": np.array([0.5, 2.0]), "dur_s": n / FS_TARGET, "srate_raw": FS_TARGET}
        X1 = features(sess, rng, with_motor=True, with_noise=False)
        X0 = features(sess, rng, with_motor=False, with_noise=False)
        assert X1.shape[1] == X0.shape[1] + MOTOR_KERNELS
        lags_ok = np.allclose(X1[:50, -MOTOR_KERNELS:], 0.0)  # causality: no motor before t=0 content
        tr, te = slice(None, None, 2), slice(1, None, 2)  # interleaved: shared stimulus structure
        W, mu, sd = ridge_fit(X1[tr], vm[tr], 1.0)
        r2_h1 = r2_score(X1[te], vm[te], W, mu, sd)
        W0, mu0, sd0 = ridge_fit(X0[tr], vm[tr], 1.0)
        r2_h0 = r2_score(X0[te], vm[te], W0, mu0, sd0)
        assert r2_h1 > r2_h0 and r2_h1 > 0.5, (r2_h1, r2_h0)
        assert lags_ok
        assert animal_key("Fly1_WTCS_age_3d_cell1_looming_wb_2019_11_06_15_13_46.mat") == "Fly1_WTCS_2019_11_06"
        print("SELFTEST PASS")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(RAW.glob("*.mat"))
    by_animal: dict[str, list[Path]] = {}
    skipped = []
    for p in files:
        k = animal_key(p.name)
        if k is None:
            skipped.append(p.name)
            continue
        by_animal.setdefault(k, []).append(p)
    animals = sorted(by_animal)
    if args.smoke:
        animals = animals[:2]
    print(f"animals={len(animals)} sessions={sum(len(v) for v in by_animal.values())} skipped={skipped}", flush=True)

    cache: dict[str, list[dict]] = {}
    for a in animals:
        sess_list = []
        for p in by_animal[a]:
            s = load_session(p)
            if s is not None and s["dur_s"] > 30 and len(s["onsets"]) >= 3:
                sess_list.append(s)
        if sess_list:
            cache[a] = sess_list
    usable = [a for a in animals if a in cache]
    print(f"usable animals: {len(usable)}", flush=True)
    if len(usable) < 2:
        if not args.smoke:
            print("NEED_AT_LEAST_2_ANIMALS (download in progress); use --smoke for plumbing check")
            return 2
        # plumbing smoke: session-level holdout within one animal (not evidence)
        a = usable[0]
        sess = cache[a]
        if len(sess) < 2:
            print(f"SMOKE_SKIP: only {len(sess)} usable session(s) for {a}; need >=2")
            return 2
        rng0 = np.random.default_rng(SEED)
        accX = {k: [] for k in ("H0", "H1")}
        accy = {k: [] for k in ("H0", "H1")}
        for s in sess[:-1]:
            accX["H0"].append(features(s, rng0, False, False))
            accX["H1"].append(features(s, rng0, True, False))
            accy["H0"].append(s["vm"])
            accy["H1"].append(s["vm"])
        out = {}
        for name in ("H0", "H1"):
            Xtr, ytr = np.concatenate(accX[name]), np.concatenate(accy[name])
            W, mu, sd = ridge_fit(Xtr, ytr, 1e-2)
            Xte = features(sess[-1], rng0, name == "H1", False)
            out[name] = r2_score(Xte, sess[-1]["vm"], W, mu, sd)
        print(f"SMOKE(plumbing only, 1 animal, session holdout): H0={out['H0']:.4f} H1={out['H1']:.4f} dR2={out['H1']-out['H0']:+.4f}")
        return 0

    rng = np.random.default_rng(SEED)
    per_animal = []
    for held in usable:
        train = [a for a in usable if a != held]
        sums = {k: (np.zeros((0, 0)), None) for k in ("H0", "H0noise", "H1")}
        acc = {k: [] for k in sums}
        y_acc = {k: [] for k in sums}
        for a in train:
            for sess in cache[a]:
                for name, wm, wn in (("H0", False, False), ("H0noise", False, True), ("H1", True, False)):
                    X = features(sess, rng, with_motor=wm, with_noise=wn)
                    acc[name].append(X)
                    y_acc[name].append(sess["vm"])
        rs = {}
        kernels = {}
        flags = {"H0": (False, False), "H0noise": (False, True), "H1": (True, False)}
        for name, (wm, wn) in flags.items():
            Xtr = np.concatenate(acc[name], axis=0)
            ytr = np.concatenate(y_acc[name], axis=0)
            # inner CV on training data for lambda (single pooled split)
            idx = rng.permutation(len(ytr))
            cut = int(0.9 * len(idx))
            best_lam, best_r2 = RIDGE_GRID[0], -np.inf
            for lam in RIDGE_GRID:
                W, mu, sd = ridge_fit(Xtr[idx[:cut]], ytr[idx[:cut]], lam)
                r2 = r2_score(Xtr[idx[cut:]], ytr[idx[cut:]], W, mu, sd)
                if r2 > best_r2:
                    best_r2, best_lam = r2, lam
            W, mu, sd = ridge_fit(Xtr, ytr, best_lam)
            Xte = np.concatenate([features(s, rng, with_motor=wm, with_noise=wn) for s in cache[held]], axis=0)
            yte = np.concatenate([s["vm"] for s in cache[held]], axis=0)
            rs[name] = r2_score(Xte, yte, W, mu, sd)
            if name == "H1":
                k = W[1:] / sd  # drop intercept; back to raw feature scale
                kernels["motor_kernel_mean"] = np.round(k[-MOTOR_KERNELS:], 5).tolist()
        per_animal.append(
            {"animal": held, "n_sessions": len(cache[held]), "r2_H0": rs["H0"], "r2_H0noise": rs["H0noise"], "r2_H1": rs["H1"], "delta_r2": rs["H1"] - rs["H0"], **kernels}
        )
        print(f"  held-out {held}: dR2={rs['H1']-rs['H0']:+.4f} (H0={rs['H0']:.4f})", flush=True)

    d = np.array([p["delta_r2"] for p in per_animal])
    n = len(d)
    obs = float(np.median(d))
    # exact sign-flip permutation (one-sided: H1 > H0)
    if n <= 20:
        ge = 0
        total = 2**n
        for bits in range(total):
            s = np.where([(bits >> i) & 1 for i in range(n)], 1.0, -1.0)
            if float(np.median(d * s)) >= obs - 1e-15:
                ge += 1
        p_one = ge / total
    else:
        flips = rng.choice([-1, 1], size=(20000, n))
        p_one = float(np.mean(np.median(flips * d, axis=1) >= obs))
    boots = [float(np.median(d[rng.integers(0, n, n)])) for _ in range(5000)]
    ci = [round(x, 5) for x in np.percentile(boots, [2.5, 97.5])]
    summary = {
        "n_animals": n,
        "median_delta_r2": obs,
        "bootstrap_ci95": ci,
        "signflip_p_one_sided": p_one,
        "n_delta_positive": int(np.sum(d > 0)),
        "verdict": "MOTOR_HISTORY_ADDS_PREDICTIVE_INFO" if (p_one < 0.05 and obs > 0) else "NOT_DISCRIMINATED",
        "claim_limit": "additional predictive information only; no efference-copy source claim (PREREG A1)",
        "per_animal": per_animal,
        "guards": "no same-timepoint behavior input (lags>=20ms); no Vm-sign selection; animal-level LOMO; lambda inner-CV on training only",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "per_animal"}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
