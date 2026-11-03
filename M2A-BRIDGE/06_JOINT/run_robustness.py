#!/usr/bin/env python3
"""Noise and body-time-constant robustness sweep for the EC delay pilot.

Adds allnone_motor (gate on the current motor-copy torque) and runs a focused
grid over body time constant tau_body = I / beta, grating gain, feedback delay
and noise seed.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import MODELS, Params, simulate

DELAYS = tuple(np.round(np.arange(0.0, 0.121, 0.01), 3)) + (0.14, 0.16, 0.18, 0.20, 0.25, 0.30)
GAINS = (2.5e-11, 5e-11)
BODY_SETS = (
    (6e-14, 2e-11),   # tau_body = 3 ms
    (6e-14, 1e-11),   # 6 ms
    (1.2e-13, 1e-11), # 12 ms
    (2.4e-13, 1e-11), # 24 ms
)
SEEDS = (0, 1)
NOISE_SD = 1e-13
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def parameter_sets() -> tuple[Params, ...]:
    return tuple(
        replace(Params(), inertia=inertia, drag=drag, k_opto=gain)
        for inertia, drag in BODY_SETS
        for gain in GAINS
    )


def run_once(model: str, params: Params, delay_s: float, seed: int) -> dict[str, object]:
    time, _, readouts = simulate(
        model,
        params,
        delay_s=delay_s,
        grating_gain=params.k_opto,
        noise_sd=NOISE_SD,
        seed=seed,
    )
    heading = readouts["heading"]
    omega = readouts["omega"]
    finite = bool(np.isfinite(heading).all() and np.isfinite(omega).all())
    max_heading = float(np.nanmax(np.abs(heading))) if finite else float("inf")
    max_omega = float(np.nanmax(np.abs(omega))) if finite else float("inf")
    failure = int((not finite) or max_heading > HEADING_LIMIT or max_omega > OMEGA_LIMIT)
    return {
        "model": model,
        "inertia": params.inertia,
        "drag": params.drag,
        "tau_body_s": params.inertia / params.drag,
        "k_opto": params.k_opto,
        "delay_s": float(delay_s),
        "seed": int(seed),
        "noise_sd": NOISE_SD,
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "divergence": max(max_heading / HEADING_LIMIT, max_omega / OMEGA_LIMIT),
        "failure": failure,
        "finite": int(finite),
    }


def run_grid() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for params in parameter_sets():
        for model in MODELS:
            for delay in DELAYS:
                for seed in SEEDS:
                    rows.append(run_once(model, params, delay, seed))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "noise_sd": NOISE_SD, "models": {}}
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        by_delay: dict[float, list[dict[str, object]]] = {}
        for row in model_rows:
            by_delay.setdefault(float(row["delay_s"]), []).append(row)
        curve = {
            str(delay): sum(int(row["failure"]) for row in group) / len(group)
            for delay, group in sorted(by_delay.items())
        }
        critical = []
        for params in parameter_sets():
            for seed in SEEDS:
                subset = [
                    row
                    for row in model_rows
                    if row["inertia"] == params.inertia
                    and row["drag"] == params.drag
                    and row["k_opto"] == params.k_opto
                    and row["seed"] == seed
                ]
                failures = [float(row["delay_s"]) for row in subset if int(row["failure"])]
                critical.append(min(failures) if failures else float(max(DELAYS)))
        summary["models"][model] = {
            "failure_curve": curve,
            "critical_delay_median_s": float(np.median(critical)),
            "critical_delay_mean_s": float(np.mean(critical)),
            "critical_delays_s": critical,
            "failure_rate_at_140ms": curve.get("0.14"),
        }
    return summary


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_figures(rows: list[dict[str, object]], summary: dict[str, object], out_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    for model in MODELS:
        curve = summary["models"][model]["failure_curve"]
        xs = [float(key) for key in curve]
        ys = [curve[key] for key in curve]
        ax.plot(xs, ys, marker="o", label=model)
    ax.set_xlabel("feedback delay (s)")
    ax.set_ylabel("failure rate (noise + body grid)")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "failure_rate_vs_delay_noise.png", dpi=200)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
    for ax, model in zip(axes, ("graded_sensory", "allnone")):
        taus = [params.inertia / params.drag * 1000 for params in parameter_sets()]
        taus_unique = sorted(set(round(tau, 3) for tau in taus))
        grid = np.full((len(taus_unique), len(DELAYS)), np.nan)
        for row in rows:
            if row["model"] != model:
                continue
            tau = round(float(row["tau_body_s"]) * 1000, 3)
            if tau not in taus_unique:
                continue
            i = taus_unique.index(tau)
            j = DELAYS.index(float(row["delay_s"]))
            if np.isnan(grid[i, j]):
                grid[i, j] = 0.0
            grid[i, j] += float(row["failure"])
        counts = np.zeros_like(grid)
        for row in rows:
            if row["model"] != model:
                continue
            tau = round(float(row["tau_body_s"]) * 1000, 3)
            if tau not in taus_unique:
                continue
            counts[taus_unique.index(tau), DELAYS.index(float(row["delay_s"]))] += 1
        grid = np.divide(grid, counts, out=np.zeros_like(grid), where=counts > 0)
        image = ax.imshow(grid, aspect="auto", origin="lower", vmin=0, vmax=1, cmap="magma")
        ax.set_xticks(range(len(DELAYS)))
        ax.set_xticklabels([f"{d:g}" for d in DELAYS], rotation=90, fontsize=6)
        ax.set_yticks(range(len(taus_unique)))
        ax.set_yticklabels([f"{t:g}" for t in taus_unique])
        ax.set_xlabel("delay (s)")
        ax.set_title(model)
    axes[0].set_ylabel("body time constant I/beta (ms)")
    fig.colorbar(image, ax=axes, label="failure rate")
    fig.savefig(out_dir / "phase_diagram.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    example = parameter_sets()[0]
    fig, ax = plt.subplots(figsize=(7, 4))
    for model in MODELS:
        time, _, readouts = simulate(
            model,
            example,
            delay_s=0.14,
            grating_gain=example.k_opto,
            noise_sd=NOISE_SD,
            seed=0,
        )
        ax.plot(time, np.rad2deg(readouts["heading"]), label=model)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("heading (deg)")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "example_trajectories_140ms_noise.png", dpi=200)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-DELAY-02/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        rows = [run_once("allnone_motor", Params(dt_s=5e-4), 0.1, 0) for _ in range(1)]
        assert rows and "failure" in rows[0]
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "sweep_noise.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    make_figures(rows, summary, args.output_dir)
    print(json.dumps({model: {
        "critical_delay_median_s": summary["models"][model]["critical_delay_median_s"],
        "failure_rate_at_140ms": summary["models"][model]["failure_rate_at_140ms"],
    } for model in MODELS}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
