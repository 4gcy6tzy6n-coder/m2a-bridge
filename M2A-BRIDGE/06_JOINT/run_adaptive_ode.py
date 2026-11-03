#!/usr/bin/env python3
"""Verify step-wise and ODE-internal adaptive updates agree."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

from adaptive_ode import compare
from ec_model import Params

DELAYS = (0.02, 0.05, 0.10, 0.20)
UPDATE_MODES = ("source", "gradient")
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain, t_end_s=6.0)
    for inertia in (6e-14, 1.2e-13, 2.4e-13)
    for drag in (1e-11, 2e-11)
    for gain in (2.5e-11, 5e-11)
)
SEED = 0
ALPHA = 8e-5


def run_once(params: Params, delay: float, update_mode: str) -> dict[str, object]:
    result = compare(
        params,
        delay_s=delay,
        seed=SEED,
        alpha=ALPHA,
        update_mode=update_mode,
    )
    return {
        "update_mode": update_mode,
        "delay_s": delay,
        "seed": SEED,
        "alpha": ALPHA,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "window_s": params.t_end_s,
        "failure_step": result.failure_step,
        "failure_ode": result.failure_ode,
        "failure_agree": int(result.failure_step == result.failure_ode),
        "abs_failure_time_diff": result.abs_failure_time_diff,
        "max_abs_heading_diff": result.max_abs_heading_diff,
        "max_abs_ro_diff": result.max_abs_ro_diff,
        "max_abs_heading_diff_prefix": result.max_abs_heading_diff_prefix,
        "max_abs_ro_diff_prefix": result.max_abs_ro_diff_prefix,
        "prefix_end_s": result.prefix_end_s,
    }


def run_grid() -> list[dict[str, object]]:
    rows = []
    for params in PARAMETER_SETS:
        for update_mode in UPDATE_MODES:
            for delay in DELAYS:
                rows.append(run_once(params, delay, update_mode))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "grid": {}}
    for update_mode in UPDATE_MODES:
        summary["grid"][update_mode] = {}
        for delay in DELAYS:
            subset = [
                row
                for row in rows
                if row["update_mode"] == update_mode
                and abs(float(row["delay_s"]) - delay) < 1e-12
            ]
            summary["grid"][update_mode][f"{delay:g}"] = {
                "n": len(subset),
                "failure_agree_rate": sum(int(r["failure_agree"]) for r in subset) / len(subset),
                "max_abs_failure_time_diff": max(float(r["abs_failure_time_diff"]) for r in subset),
                "max_abs_heading_diff_prefix": max(
                    float(r["max_abs_heading_diff_prefix"]) for r in subset
                ),
                "max_abs_ro_diff_prefix": max(float(r["max_abs_ro_diff_prefix"]) for r in subset),
                "min_prefix_end_s": min(float(r["prefix_end_s"]) for r in subset),
            }
    return summary


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-ADAPTIVE-ODE-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        n = len(PARAMETER_SETS) * len(UPDATE_MODES) * len(DELAYS)
        print(f"DRY RUN: {len(PARAMETER_SETS)} params x {len(UPDATE_MODES)} update modes x {len(DELAYS)} delays = {n} paired comparisons")
        return 0
    if args.selftest:
        row = run_once(replace(Params(dt_s=5e-4, t_end_s=1.5), t_end_s=1.5), 0.1, "source")
        assert "failure_agree" in row
        print("SELFTEST PASS")
        print(json.dumps(row, indent=2))
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "adaptive_ode.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
