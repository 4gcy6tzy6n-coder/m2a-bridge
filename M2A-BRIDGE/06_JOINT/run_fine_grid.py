#!/usr/bin/env python3
"""1 ms fine grid around the critical delays for three representative parameter sets."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import MODELS, Params, simulate

DELAYS = tuple(np.round(np.arange(0.0, 0.1005, 0.001), 3)) + tuple(
    np.round(np.arange(0.11, 0.301, 0.01), 3)
)
PARAMETER_SETS = (
    Params(),                              # source parameters
    replace(Params(), k_opto=5e-11),       # high grating gain
    replace(Params(), inertia=1.2e-13, drag=1e-11),  # slow body (12 ms)
)
HEADING_LIMIT = 2.0 * np.pi
OMEGA_LIMIT = 100.0


def run_once(model: str, params: Params, delay_s: float) -> dict[str, object]:
    time, _, readouts = simulate(model, params, delay_s=delay_s, grating_gain=params.k_opto)
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
        "k_opto": params.k_opto,
        "delay_s": float(delay_s),
        "max_abs_heading_rad": max_heading,
        "max_abs_omega_rad_s": max_omega,
        "failure": failure,
        "finite": int(finite),
    }


def run_grid() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for params in PARAMETER_SETS:
        for model in MODELS:
            for delay in DELAYS:
                rows.append(run_once(model, params, delay))
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {"n_rows": len(rows), "models": {}}
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
        for params in PARAMETER_SETS:
            subset = [
                row
                for row in model_rows
                if row["inertia"] == params.inertia
                and row["drag"] == params.drag
                and row["k_opto"] == params.k_opto
            ]
            failures = [float(row["delay_s"]) for row in subset if int(row["failure"])]
            critical.append(min(failures) if failures else float(max(DELAYS)))
        summary["models"][model] = {
            "failure_curve": curve,
            "critical_delays_s": critical,
            "critical_delay_median_s": float(np.median(critical)),
            "failure_rate_at_140ms": curve.get("0.14"),
        }
    return summary


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_figure(summary: dict[str, object], out_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.5, 4))
    for model in MODELS:
        curve = summary["models"][model]["failure_curve"]
        xs = [float(key) for key in curve]
        ys = [curve[key] for key in curve]
        ax.plot(xs, ys, label=model)
    ax.set_xlabel("feedback delay (s)")
    ax.set_ylabel("failure rate (3 parameter sets)")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "failure_rate_fine.png", dpi=220)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runs/P1-EC-DELAY-03/experiment/outputs"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        rows = [run_once("allnone", Params(dt_s=5e-4), 0.1)]
        assert rows and "failure" in rows[0]
        print("SELFTEST PASS")
        return 0
    rows = run_grid()
    summary = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.output_dir / "sweep_fine.csv")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    make_figure(summary, args.output_dir)
    print(json.dumps({model: {
        "critical_delays_s": summary["models"][model]["critical_delays_s"],
        "failure_rate_at_140ms": summary["models"][model]["failure_rate_at_140ms"],
    } for model in MODELS}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
