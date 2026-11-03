#!/usr/bin/env python3
"""Source-style adaptive MLP with weights integrated as ODE states.

The discrete update in ``adaptive_model.py`` adds ``alpha * u`` to each weight
every step. Integrating the weights as states with rate ``alpha / dt`` under
forward Euler reproduces that update exactly, so the step-wise and ODE forms
should agree to floating-point tolerance. This module exists to verify that
equivalence numerically rather than assume it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from adaptive_model import ALPHA, N_HIDDEN, AdaptiveResult
from ec_model import Params, _stimulus, simulate

N_STATE = 5 + N_HIDDEN + N_HIDDEN


@dataclass(frozen=True)
class OdeCompare:
    time: np.ndarray
    step: AdaptiveResult
    ode: AdaptiveResult
    max_abs_heading_diff: float
    max_abs_ro_diff: float
    max_abs_heading_diff_prefix: float
    max_abs_ro_diff_prefix: float
    prefix_end_s: float
    abs_failure_time_diff: float
    failure_step: int
    failure_ode: int


def simulate_adaptive_ode(
    params: Params = Params(),
    *,
    delay_s: float = 0.0,
    grating_gain: float | None = None,
    seed: int = 0,
    alpha: float = ALPHA,
    update_mode: str = "source",
) -> AdaptiveResult:
    """Run the adaptive graded model with the weights as ODE states."""
    if delay_s < 0:
        raise ValueError("delay_s must be non-negative")
    if params.dt_s <= 0:
        raise ValueError("dt_s must be positive")
    dt = params.dt_s
    n_steps = int(round(params.t_end_s / dt)) + 1
    gain = params.k_opto if grating_gain is None else float(grating_gain)

    time_ideal, _, ideal = simulate("addition", params, delay_s=delay_s, grating_gain=0.0)
    y0 = np.interp(np.arange(n_steps) * dt, time_ideal, ideal["heading"])

    rng = np.random.default_rng(seed)
    states = np.zeros((n_steps, N_STATE), dtype=np.float64)
    states[0, 5 : 5 + N_HIDDEN] = 0.1 * rng.random(N_HIDDEN)
    states[0, 5 + N_HIDDEN :] = 0.025 * rng.random(N_HIDDEN)
    ro_hist = np.zeros(n_steps)
    theta_bar_hist = np.zeros(n_steps)
    dtheta_bar_hist = np.zeros(n_steps)
    theta_grat_hist = np.zeros(n_steps)
    dtheta_grat_hist = np.zeros(n_steps)
    heading_hist = np.zeros(n_steps)
    omega_hist = np.zeros(n_steps)
    delay_steps = int(round(delay_s / dt))
    alpha_rate = alpha / dt

    for index in range(n_steps):
        t = index * dt
        theta_bar, dtheta_bar, theta_grat, dtheta_grat = _stimulus(t, params)
        theta_bar_hist[index] = theta_bar
        dtheta_bar_hist[index] = dtheta_bar
        theta_grat_hist[index] = theta_grat
        dtheta_grat_hist[index] = dtheta_grat

        delayed = max(0, index - delay_steps)
        heading, omega, f_bar, f_grating, omega_ec = states[index, :5]
        wh = states[index, 5 : 5 + N_HIDDEN]
        wo = states[index, 5 + N_HIDDEN :]

        z = wh * f_bar
        rh = np.empty_like(z)
        pos = z >= 0
        rh[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
        exp_z = np.exp(z[~pos])
        rh[~pos] = exp_z / (1.0 + exp_z)
        ro = float(np.clip(np.dot(wo, rh), 0.0, 2.0))
        ro_hist[index] = ro

        error = y0[index] - heading
        if update_mode == "source":
            do = error * error
        elif update_mode == "gradient":
            do = error
        elif update_mode == "gradient_neg":
            do = -error
        else:
            raise ValueError(f"unknown update_mode: {update_mode}")
        dh = (rh * (1.0 - rh)) * (wo * do)
        dwo = alpha_rate * do * rh
        dwh = alpha_rate * dh * f_bar

        error_bar = np.arctan2(
            np.sin(theta_bar_hist[delayed] - heading_hist[delayed]),
            np.cos(theta_bar_hist[delayed] - heading_hist[delayed]),
        )
        p_term = params.p_gain * np.sin(error_bar)
        v_term = params.v_gain * max(0.0, 20.0 - 2.0 * error_bar * error_bar)
        f_bar_dot = (
            -f_bar
            + p_term
            + (dtheta_bar_hist[delayed] - omega_hist[delayed]) * v_term
        ) / params.tau_bar
        grating_drive = dtheta_grat_hist[delayed] + omega_ec - omega_hist[delayed]
        f_grating_dot = (-f_grating + grating_drive * gain) / params.tau_opto
        domega = (-params.drag * omega + f_bar + f_grating) / params.inertia
        domega_ec = (-params.drag * omega_ec + f_bar * ro) / params.inertia

        if index == n_steps - 1:
            break
        deriv = np.concatenate(
            (
                np.array([omega, domega, f_bar_dot, f_grating_dot, domega_ec]),
                dwh,
                dwo,
            )
        )
        next_state = states[index] + deriv * dt
        if not np.isfinite(next_state).all():
            states[index + 1 :] = np.nan
            break
        states[index + 1] = next_state
        heading_hist[index + 1] = states[index + 1, 0]
        omega_hist[index + 1] = states[index + 1, 1]

    time = np.arange(n_steps) * dt
    return AdaptiveResult(
        time=time,
        heading=states[:, 0],
        omega=states[:, 1],
        f_bar=states[:, 2],
        f_grating=states[:, 3],
        omega_ec=states[:, 4],
        ro=ro_hist,
    )


def _failure(result: AdaptiveResult) -> int:
    bad = (
        (np.abs(result.heading) > 2.0 * np.pi)
        | (np.abs(result.omega) > 100.0)
        | (~np.isfinite(result.heading))
        | (~np.isfinite(result.omega))
    )
    return int(bad.any())


def compare(
    params: Params = Params(),
    *,
    delay_s: float = 0.0,
    seed: int = 0,
    alpha: float = ALPHA,
    update_mode: str = "source",
) -> OdeCompare:
    """Run both forms and measure their disagreement."""
    from adaptive_model import simulate_adaptive

    step = simulate_adaptive(
        params, delay_s=delay_s, seed=seed, alpha=alpha, update_mode=update_mode
    )
    ode = simulate_adaptive_ode(
        params, delay_s=delay_s, seed=seed, alpha=alpha, update_mode=update_mode
    )
    heading_diff = np.abs(step.heading - ode.heading)
    ro_diff = np.abs(step.ro - ode.ro)
    # Post-divergence differences are chaotic amplification of floating-point
    # noise, so also report the prefix before either trajectory leaves the
    # bounded region (|heading| < 2 pi and finite for both).
    bounded = (
        np.isfinite(step.heading)
        & np.isfinite(ode.heading)
        & (np.abs(step.heading) < 2.0 * np.pi)
        & (np.abs(ode.heading) < 2.0 * np.pi)
    )
    if bounded.any():
        prefix_heading = heading_diff[bounded]
        prefix_ro = ro_diff[bounded]
        prefix_end = float(step.time[bounded][-1])
        max_prefix_heading = float(np.nanmax(prefix_heading))
        max_prefix_ro = float(np.nanmax(prefix_ro))
    else:
        prefix_end = 0.0
        max_prefix_heading = float("nan")
        max_prefix_ro = float("nan")
    failure_step = _failure(step)
    failure_ode = _failure(ode)
    if failure_step and failure_ode:
        step_bad = np.where(
            (np.abs(step.heading) > 2.0 * np.pi)
            | (np.abs(step.omega) > 100.0)
            | (~np.isfinite(step.heading))
        )[0]
        ode_bad = np.where(
            (np.abs(ode.heading) > 2.0 * np.pi)
            | (np.abs(ode.omega) > 100.0)
            | (~np.isfinite(ode.heading))
        )[0]
        abs_failure_time_diff = float(
            abs(step.time[step_bad[0]] - ode.time[ode_bad[0]])
        )
    elif failure_step == failure_ode:
        abs_failure_time_diff = 0.0
    else:
        abs_failure_time_diff = float("inf")
    return OdeCompare(
        time=step.time,
        step=step,
        ode=ode,
        max_abs_heading_diff=float(np.nanmax(heading_diff)) if heading_diff.size else float("nan"),
        max_abs_ro_diff=float(np.nanmax(ro_diff)) if ro_diff.size else float("nan"),
        max_abs_heading_diff_prefix=max_prefix_heading,
        max_abs_ro_diff_prefix=max_prefix_ro,
        prefix_end_s=prefix_end,
        abs_failure_time_diff=abs_failure_time_diff,
        failure_step=failure_step,
        failure_ode=failure_ode,
    )


def main() -> None:
    result = compare(Params(t_end_s=1.5, dt_s=5e-4), delay_s=0.1)
    print("max heading diff:", result.max_abs_heading_diff)
    print("max ro diff:", result.max_abs_ro_diff)
    print("failure step/ode:", result.failure_step, result.failure_ode)


if __name__ == "__main__":
    main()
