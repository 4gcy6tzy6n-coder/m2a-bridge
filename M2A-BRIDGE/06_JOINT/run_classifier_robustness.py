#!/usr/bin/env python3
"""Classifier robustness pilot: instantaneous vs sustained failure criteria.

Re-runs conditions whose legacy label (peak |heading| > 2*pi or |omega|
> 100 rad/s at any single sample) is documented to flip under noise, seed
or dt perturbations near the critical delay zone, and classifies every
trajectory under both the legacy instantaneous criterion and the sustained
criterion from ``failure_classifier`` (dwell 10 ms). One simulation feeds
both verdicts, isolating criterion effects from trajectory effects.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate
from failure_classifier import DEFAULT_DWELL_S, classify

# (model, label, ff_gain, delay_s): documented flippers first, then controls.
SPECS = (
    ("allnone", "gate filtered", 0.0, 0.10),
    ("allnone", "gate filtered", 0.0, 0.14),
    ("gate_goal", "gate goal", 1.0, 0.20),
    ("graded_sensory", "graded filtered", 0.0, 0.02),
    ("addition", "addition", 0.0, 0.04),
)
NOISE_LEVELS = (0.0, 1e-12, 1e-11)
SEEDS = (0, 1, 2)
DT_LEVELS = (1e-4, 5e-5)
WINDOW = 6.0
BODY_SETS = ((6e-14, 2e-11), (6e-14, 1e-11), (1.2e-13, 1e-11), (2.4e-13, 1e-11))
GAINS = (2.5e-11, 5e-11)


def parameter_sets() -> list[Params]:
    return [
        replace(Params(), inertia=inertia, drag=drag, k_opto=gain, t_end_s=WINDOW)
        for inertia, drag in BODY_SETS
        for gain in GAINS
    ]


def run_once(
    model: str,
    label: str,
    ff_gain: float,
    delay: float,
    params: Params,
    noise_sd: float,
    seed: int,
    dt: float,
) -> dict[str, object]:
    p = replace(params, ff_gain=ff_gain, dt_s=dt)
    time, _, readouts = simulate(
        model, p, delay_s=delay, grating_gain=p.k_opto, noise_sd=noise_sd, seed=seed
    )
    verdict = classify(readouts["heading"], readouts["omega"], dt_s=dt)
    return {
        "model": model,
        "label": label,
        "ff_gain": ff_gain,
        "delay_s": delay,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "noise_sd": noise_sd,
        "seed": seed,
        "dt_s": dt,
        "window_s": WINDOW,
        "failure_instantaneous": verdict.failure_instantaneous,
        "failure_sustained": verdict.failure_sustained,
        "transient_only": int(
            verdict.failure_instantaneous == 1 and verdict.failure_sustained == 0
        ),
        "max_abs_heading_rad": verdict.max_abs_heading_rad,
        "max_abs_omega_rad_s": verdict.max_abs_omega_rad_s,
        "longest_heading_exceedance_s": verdict.longest_heading_exceedance_s,
        "longest_omega_exceedance_s": verdict.longest_omega_exceedance_s,
        "first_heading_crossing_s": verdict.first_heading_crossing_s,
        "first_omega_crossing_s": verdict.first_omega_crossing_s,
        "failure_time_s": (
            float(np.nanmin([verdict.first_heading_crossing_s, verdict.first_omega_crossing_s]))
            if verdict.failure_instantaneous
            else float("nan")
        ),
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in parameter_sets():
        for model, label, ff_gain, delay in SPECS:
            for noise_sd in NOISE_LEVELS:
                for seed in SEEDS:
                    for dt in DT_LEVELS:
                        rows.append(
                            run_once(model, label, ff_gain, delay, params, noise_sd, seed, dt)
                        )
    return rows


def _spread(rows: list[dict[str, object]], key_fn, flag: str) -> int:
    """Count key groups whose labels are not unanimous."""
    groups: dict[tuple[object, ...], set[int]] = {}
    for row in rows:
        key = key_fn(row)
        groups.setdefault(key, set()).add(int(row[flag]))
    return sum(1 for labels in groups.values() if len(labels) > 1)


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    per_condition: dict[str, object] = {}
    for _, label, ff_gain, delay in SPECS:
        key = f"{label}|ff={ff_gain:g}|d={delay:g}"
        subset = [
            r
            for r in rows
            if r["label"] == label
            and abs(float(r["ff_gain"]) - ff_gain) < 1e-12
            and abs(float(r["delay_s"]) - delay) < 1e-12
        ]
        n = len(subset)
        per_condition[key] = {
            "n": n,
            "failure_rate_instantaneous": sum(int(r["failure_instantaneous"]) for r in subset) / n,
            "failure_rate_sustained": sum(int(r["failure_sustained"]) for r in subset) / n,
            "transient_only_count": sum(int(r["transient_only"]) for r in subset),
        }

    across_seed = lambda r: (r["label"], r["ff_gain"], r["delay_s"], r["inertia"], r["drag"], r["k_opto"], r["noise_sd"], r["dt_s"])  # noqa: E731
    across_noise = lambda r: (r["label"], r["ff_gain"], r["delay_s"], r["inertia"], r["drag"], r["k_opto"], r["seed"], r["dt_s"])  # noqa: E731
    across_dt = lambda r: (r["label"], r["ff_gain"], r["delay_s"], r["inertia"], r["drag"], r["k_opto"], r["seed"], r["noise_sd"])  # noqa: E731

    return {
        "n_rows": len(rows),
        "dwell_s": DEFAULT_DWELL_S,
        "per_condition": per_condition,
        "criterion_disagreement": {
            "count": sum(int(r["transient_only"]) for r in rows),
            "note": "instantaneous=1 and sustained=0 on the identical trajectory",
        },
        "label_instability": {
            "across_seeds": {
                "instantaneous": _spread(rows, across_seed, "failure_instantaneous"),
                "sustained": _spread(rows, across_seed, "failure_sustained"),
            },
            "across_noise": {
                "instantaneous": _spread(rows, across_noise, "failure_instantaneous"),
                "sustained": _spread(rows, across_noise, "failure_sustained"),
            },
            "across_dt": {
                "instantaneous": _spread(rows, across_dt, "failure_instantaneous"),
                "sustained": _spread(rows, across_dt, "failure_sustained"),
            },
        },
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def planned_runs() -> int:
    return (
        len(SPECS)
        * len(NOISE_LEVELS)
        * len(SEEDS)
        * len(DT_LEVELS)
        * len(BODY_SETS)
        * len(GAINS)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir", type=Path, default=Path("runs/P1-EC-CLASSIFIER-01/experiment/outputs")
    )
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n = planned_runs()
        print(
            f"DRY RUN: {len(SPECS)} specs x {len(NOISE_LEVELS)} noise x {len(SEEDS)} seeds "
            f"x {len(DT_LEVELS)} dt x {len(BODY_SETS) * len(GAINS)} param sets = {n} runs"
        )
        return 0
    if args.selftest:
        for model, label, ff_gain, delay in SPECS:
            row = run_once(
                model,
                label,
                ff_gain,
                delay,
                replace(Params(dt_s=5e-4, t_end_s=1.0)),
                noise_sd=1e-12,
                seed=0,
                dt=5e-4,
            )
            assert "failure_instantaneous" in row and "failure_sustained" in row
            assert row["label"] == label
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "classifier_robustness.csv")
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
