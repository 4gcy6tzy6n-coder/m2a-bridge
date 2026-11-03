#!/usr/bin/env python3
"""Adaptive graded efference-copy model, following the source's sim_effc.

The source's Figure 5 model learns the grating gain with a small online MLP.
Input is the bar torque F_bar; the hidden layer has 5 sigmoid units; the output
ro scales the efference-copy drive. Weights are updated from the squared error
between the actual heading and the ideal bar-only heading.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ec_model import Params, _stimulus, simulate

N_HIDDEN = 5
ALPHA = 8e-5


@dataclass(frozen=True)
class AdaptiveResult:
    time: np.ndarray
    heading: np.ndarray
    omega: np.ndarray
    f_bar: np.ndarray
    f_grating: np.ndarray
    omega_ec: np.ndarray
    ro: np.ndarray


def simulate_adaptive(
    params: Params = Params(),
    *,
    delay_s: float = 0.0,
    grating_gain: float | None = None,
    seed: int = 0,
    alpha: float = ALPHA,
    update_mode: str = "source",
) -> AdaptiveResult:
    """Run the adaptive graded model with an online 5-unit MLP."""
    if delay_s < 0:
        raise ValueError("delay_s must be non-negative")
    dt = params.dt_s
    n_steps = int(round(params.t_end_s / dt)) + 1
    gain = params.k_opto if grating_gain is None else float(grating_gain)

    # Ideal bar-only trajectory under the same delay.
    time_ideal, _, ideal = simulate("addition", params, delay_s=delay_s, grating_gain=0.0)
    y0 = np.interp(np.arange(n_steps) * dt, time_ideal, ideal["heading"])

    rng = np.random.default_rng(seed)
    wh = 0.1 * rng.random((N_HIDDEN, 1))
    wo = 0.025 * rng.random((1, N_HIDDEN))

    states = np.zeros((n_steps, 5), dtype=np.float64)
    ro_hist = np.zeros(n_steps)
    theta_bar_hist = np.zeros(n_steps)
    dtheta_bar_hist = np.zeros(n_steps)
    theta_grat_hist = np.zeros(n_steps)
    dtheta_grat_hist = np.zeros(n_steps)
    heading_hist = np.zeros(n_steps)
    omega_hist = np.zeros(n_steps)
    delay_steps = int(round(delay_s / dt))

    for index in range(n_steps):
        t = index * dt
        theta_bar, dtheta_bar, theta_grat, dtheta_grat = _stimulus(t, params)
        theta_bar_hist[index] = theta_bar
        dtheta_bar_hist[index] = dtheta_bar
        theta_grat_hist[index] = theta_grat
        dtheta_grat_hist[index] = dtheta_grat

        delayed = max(0, index - delay_steps)
        heading, omega, f_bar, f_grating, omega_ec = states[index]

        z = (wh * f_bar).ravel()
        rh = np.empty_like(z)
        pos = z >= 0
        rh[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
        exp_z = np.exp(z[~pos])
        rh[~pos] = exp_z / (1.0 + exp_z)
        ro = float(np.clip((wo @ rh).item(), 0.0, 2.0))
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
        dh = (rh * (1.0 - rh)) * (wo.T.ravel() * do)
        wo = wo + alpha * do * rh.reshape(1, -1)
        wh = wh + alpha * dh.reshape(-1, 1) * f_bar

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
        next_state = states[index] + np.array([omega, domega, f_bar_dot, f_grating_dot, domega_ec]) * dt
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


def main() -> None:
    result = simulate_adaptive(Params(t_end_s=1.0, dt_s=5e-4))
    print("finite:", bool(np.isfinite(result.heading).all()))
    print("peak heading deg:", float(np.rad2deg(np.nanmax(np.abs(result.heading)))))
    print("mean ro:", float(np.nanmean(result.ro)))


if __name__ == "__main__":
    main()
