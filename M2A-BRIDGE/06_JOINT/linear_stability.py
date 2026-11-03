#!/usr/bin/env python3
"""Linear stability analysis of the delayed steering model.

Linearize around the target (heading = bar angle, omega = 0, torques = 0):
    x_dot = A x(t) + B x(t - d)
Solve det(lambda I - A - B exp(-lambda d)) = 0 for the rightmost eigenvalue.
The all-or-none gate is non-smooth; the open-gate branch is analyzed here.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np
from scipy.optimize import root

from ec_model import Params

MODELS = ("addition", "graded_sensory", "graded_motor", "allnone", "allnone_motor")
GRID = tuple(
    complex(re, im)
    for re in (-4.0, -2.0, -1.0, -0.5, 0.0, 0.5)
    for im in (-30.0, -20.0, -10.0, -5.0, 0.0, 5.0, 10.0, 20.0, 30.0)
)


def matrices(model: str, params: Params) -> tuple[np.ndarray, np.ndarray]:
    graded = model in ("graded_sensory", "graded_motor")
    n = 5 if graded else 4
    a = np.zeros((n, n))
    b = np.zeros((n, n))

    # heading, omega
    a[0, 1] = 1.0
    a[1, 1] = -params.drag / params.inertia
    a[1, 2] = 1.0 / params.inertia
    a[1, 3] = 1.0 / params.inertia

    # bar torque
    a[2, 2] = -1.0 / params.tau_bar
    b[2, 0] = -params.p_gain / params.tau_bar
    b[2, 1] = -params.v_gain * 20.0 / params.tau_bar

    # grating torque: delayed self-motion; current EC term for graded models
    a[3, 3] = -1.0 / params.tau_opto
    b[3, 1] = -params.k_opto / params.tau_opto
    if graded:
        a[3, 4] = params.k_opto * params.ec_gain / params.tau_opto
        a[4, 4] = -params.drag / params.inertia
        if model == "graded_sensory":
            a[4, 2] = 1.0 / params.inertia
        else:
            a[4, 0] = -params.p_gain / params.inertia
            a[4, 1] = -params.v_gain * 20.0 / params.inertia
    return a, b


def char_det(lam: complex, a: np.ndarray, b: np.ndarray, delay: float) -> complex:
    n = a.shape[0]
    return np.linalg.det(lam * np.eye(n) - a - b * np.exp(-lam * delay))


def scaled_residual(lam: complex, a: np.ndarray, b: np.ndarray, delay: float) -> float:
    n = a.shape[0]
    scale = np.linalg.norm(a, 2) + np.linalg.norm(b, 2) + 1.0
    return float(abs(char_det(lam, a, b, delay)) / (scale**n))


def find_roots(
    a: np.ndarray,
    b: np.ndarray,
    delay: float,
    guesses: tuple[complex, ...],
    tol: float = 1e-6,
) -> list[complex]:
    roots: list[complex] = []
    for guess in guesses:
        sol = root(
            lambda z: [
                char_det(complex(z[0], z[1]), a, b, delay).real,
                char_det(complex(z[0], z[1]), a, b, delay).imag,
            ],
            [guess.real, guess.imag],
            method="hybr",
        )
        if not sol.success:
            continue
        lam = complex(sol.x[0], sol.x[1])
        if abs(lam.imag) > 60.0 or lam.real > 20.0:
            continue
        if scaled_residual(lam, a, b, delay) < tol:
            if not any(abs(lam - other) < 1e-4 for other in roots):
                roots.append(lam)
    return sorted(roots, key=lambda z: z.real, reverse=True)


def critical_delay(
    model: str,
    params: Params,
    *,
    max_delay: float = 0.30,
    step: float = 0.001,
) -> dict[str, object]:
    a, b = matrices(model, params)
    base_roots = tuple(np.linalg.eigvals(a + b))
    previous = base_roots
    curve = []
    critical = None
    for delay in np.round(np.arange(0.0, max_delay + step, step), 6):
        guesses = tuple(previous) + base_roots + GRID
        roots = find_roots(a, b, float(delay), guesses)
        if not roots:
            roots = list(previous)
        rightmost = max(roots, key=lambda z: z.real)
        curve.append({"delay_s": float(delay), "max_real": float(rightmost.real), "max_imag": float(rightmost.imag)})
        previous = tuple(roots)
        if critical is None and rightmost.real > 0:
            critical = float(delay)
            break
    return {
        "model": model,
        "ec_gain": params.ec_gain,
        "critical_delay_s": critical if critical is not None else float(max_delay),
        "curve": curve,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        params = Params(t_end_s=1.0, dt_s=5e-4)
        for model in MODELS:
            result = critical_delay(model, params, max_delay=0.05, step=0.005)
            assert "critical_delay_s" in result
        print("SELFTEST PASS")
        return 0

    source = Params()
    rows = []
    for ec_gain in (0.05, 1.0):
        params = replace(source, ec_gain=ec_gain)
        for model in MODELS:
            rows.append(critical_delay(model, params))
    output = Path(__file__).resolve().parent.parent / "08_MANUSCRIPT/TRACK_C_EC_DELAY/linear_stability.json"
    output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"{row['model']:16} ec_gain={row['ec_gain']:.2f} critical={row['critical_delay_s']:.3f} s")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
