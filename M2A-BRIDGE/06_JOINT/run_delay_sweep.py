#!/usr/bin/env python3
"""Delay sweep for the four efference-copy model variants.

The experiment asks whether the four models separate under an explicit
sensorimotor feedback delay: addition, graded_sensory, graded_motor, allnone.
A run is a failure if heading exceeds one full turn or |omega| exceeds
100 rad/s, or if the state becomes non-finite.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np

from ec_model import MODELS, Params, simulate

DELAYS = tuple(np.round(np.arange(0.0, 0.301, 0.02), 3))
PARAMETER_SETS = tuple(
    replace(Params(), inertia=inertia, drag=drag, k_opto=gain)
    for inertia in (6e-14, 1.2e-13, 2.4e-13)
    for drag in (1e-11, 2e-11)
    for gain in (2.5e-11, 5e-11)
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def run_once(model: str, params: Params, delay_s: float) -> dict[str, object]:
    time, _, readouts = simulate(
        model,
        params,
        delay_s=delay_s,
        grating_gain=params.k_opto,
    )
    heading = readouts["heading"]
    omega = readouts["omega"]
    finite = bool(np.isfinite(heading).all() and np.isfinite(omega).all())
    max_heading = float(np.nanmax(np.abs(heading))) if finite else float("inf")
    max_omega = float(np.nanmax(np.abs(omega))) if finite else float("inf")
    failure = int((not finite) or max_heading > HEADING_LIMIT or max_omega > OMEGA_LIMIT)
    divergence = max(max_heading / HEADING_LIMIT, max_omega / OMEGA_LIMIT)
    return {
        "model": model,
        "inertia": params.inertia,
        "drag": params.drag,
        "k_opto": params.k_opto,
        "tau_bar": params.tau_bar,
        "tau_opto": params.tau_opto,
        "delay_s": float(delay_s),
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "divergence": divergence,
        "failure": failure,
        "finite": int(finite),
    }


def run_grid(
    models: tuple[str, ...] = MODELS,
    delays: tuple[float, ...] = DELAYS,
    parameter_sets: tuple[Params, ...] = PARAMETER_SETS,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for params in parameter_sets:
        for model in models:
            for delay in delays:
                rows.append(run_once(model, params, delay))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "models": {}}
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        if not model_rows:
            continue
        by_delay: dict[float, list[dict[str, object]]] = {}
        for row in model_rows:
            by_delay.setdefault(float(row["delay_s"]), []).append(row)
        failure_curve = {
            str(delay): sum(int(row["failure"]) for row in group) / len(group)
            for delay, group in sorted(by_delay.items())
        }
        critical_delays: list[float] = []
        for params in PARAMETER_SETS:
            param_rows = [
                row
                for row in model_rows
                if row["inertia"] == params.inertia
                and row["drag"] == params.drag
                and row["k_opto"] == params.k_opto
            ]
            failures = [float(row["delay_s"]) for row in param_rows if int(row["failure"])]
            critical_delays.append(min(failures) if failures else float(max(DELAYS)))
        summary["models"][model] = {
            "failure_curve": failure_curve,
            "critical_delay_median_s": float(np.median(critical_delays)),
            "critical_delay_mean_s": float(np.mean(critical_delays)),
            "critical_delays_s": critical_delays,
            "failure_rate_at_150ms": failure_curve.get("0.14", failure_curve.get("0.15")),
        }
    return summary


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_figures(rows: list[dict[str, object]], summary: dict[str, object], out_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    for model in MODELS:
        curve = summary["models"][model]["failure_curve"]
        xs = [float(key) for key in curve]
        ys = [curve[key] for key in curve]
        ax.plot(xs, ys, marker="o", label=model)
    ax.set_xlabel("feedback delay (s)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out_dir / "failure_rate_vs_delay.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    data = [summary["models"][model]["critical_delays_s"] for model in MODELS]
    ax.boxplot(data, tick_labels=MODELS)
    ax.set_ylabel("first failing delay (s)")
    ax.set_title("critical delay by model")
    fig.tight_layout()
    fig.savefig(out_dir / "critical_delay.png", dpi=200)
    plt.close(fig)

    example = PARAMETER_SETS[0]
    fig, ax = plt.subplots(figsize=(7, 4))
    for model in MODELS:
        time, _, readouts = simulate(model, example, delay_s=0.16, grating_gain=example.k_opto)
        ax.plot(time, np.rad2deg(readouts["heading"]), label=model)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("heading (deg)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out_dir / "example_trajectories_160ms.png", dpi=200)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-DELAY-01/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        rows = run_grid(delays=(0.0, 0.1), parameter_sets=(Params(dt_s=5e-4),))
        assert rows
        assert all("failure" in row for row in rows)
        print("SELFTEST PASS", len(rows))
        return 0

    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "sweep.csv")
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_figures(rows, summary, args.output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
