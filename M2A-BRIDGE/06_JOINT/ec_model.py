#!/usr/bin/env python3
"""Minimal efference-copy steering model.

Ported from the MATLAB simulator accompanying Canelo et al. (2024), eLife 93487
(https://github.com/nisl-hyu/flightsim). Three models:

- addition: bar and grating torques are summed; no efference copy.
- graded:   an internal ``omega_ec`` predicts the bar-driven angular velocity and
            subtracts it from the grating drive.
- allnone:  the grating gain is set to zero while ``|F_bar|`` exceeds a threshold.

The extension here is an explicit visual feedback delay on the delayed visual
state (bar angle, grating angle, heading, angular velocity). Canelo et al. tested
a delay block only in Fig. S3 and omitted it from the main simulations.

Units follow the source: torque in N m, inertia in kg m^2, angles in radians.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

MODELS = (
    "addition",
    "graded_sensory",
    "graded_motor",
    "allnone",
    "allnone_motor",
    # P2-OBSERVER-02 classical-control comparators (D13):
    "pd_instant",   # instantaneous-state classical PD, no gating
    "smith",        # delayed-only forward-model observer (exact internal model)
    "smith_pert",   # same observer with 10% drag/inertia mismatch
    # W1 review-response suite:
    "pd_gate",      # instantaneous classical PD WITH allnone-style grating gate
    "smith_dde",    # observer whose internal feedback loop embeds the delay
)
COMMAND_MODELS = ("graded_command", "gate_command")
FEEDFORWARD_MODELS = ("graded_goal", "gate_goal")
OBSERVER_MODELS = ("pd_instant", "smith", "smith_pert", "smith_dde")


@dataclass(frozen=True)
class Params:
    inertia: float = 6e-14
    drag: float = 1e-11
    tau_bar: float = 0.05
    tau_opto: float = 0.04
    k_opto: float = 25e-12
    gate_threshold: float = 1.5e-11
    bar_amplitude_deg: float = 60.0
    grating_amplitude_deg: float = 30.0
    bar_onset_s: float = 0.5
    grating_onset_s: float = 0.75
    stimulus_slope: float = 30.0
    t_end_s: float = 2.5
    dt_s: float = 1e-4
    p_gain: float = 10e-11
    v_gain: float = 1e-12
    ec_gain: float = 1.0
    v_mode: str = "clip"
    goal_amplitude_deg: float = 60.0
    goal_onset_s: float = 0.5
    goal_tau_s: float = 0.1
    goal_delay_s: float = 0.0
    ff_self_state: str = "current"
    ff_self_state_lag_s: float = 0.0
    ff_mode: str = "goal"
    ff_damp_gain: float = 1e-11
    ff_gain: float = 0.0
    smith_drag_scale: float = 1.1
    smith_inertia_scale: float = 1.1
    # W1 review-response ablations:
    disable_gate: bool = False          # gate_goal variant: grating pathway never gated
    gate_trigger: str = "augmented"     # "augmented" | "bar" (gate_goal trigger signal)
    undelayed_selfstate: bool = False   # bar/grating feedback uses current psi/omega


@dataclass(frozen=True)
class Metrics:
    model: str
    delay_s: float
    k_opto: float
    noise_sd: float
    seed: int
    final_error_deg: float
    peak_heading_deg: float
    overshoot_deg: float
    settling_time_s: float
    grating_torque_rms: float
    max_abs_grating_torque: float
    heading_final_deg: float
    numerical_failure: int


def _sigmoid(t: float, onset: float, slope: float) -> float:
    return 1.0 / (1.0 + np.exp(-(t - onset) * slope))


def _stimulus(t: float, params: Params) -> tuple[float, float, float, float]:
    bar_amp = np.deg2rad(params.bar_amplitude_deg)
    grating_amp = np.deg2rad(params.grating_amplitude_deg)
    s_bar = _sigmoid(t, params.bar_onset_s, params.stimulus_slope)
    s_grat = _sigmoid(t, params.grating_onset_s, params.stimulus_slope)
    bar = bar_amp * s_bar
    dbar = bar_amp * params.stimulus_slope * s_bar * (1.0 - s_bar)
    grating = -grating_amp * s_grat
    dgrating = -grating_amp * params.stimulus_slope * s_grat * (1.0 - s_grat)
    return bar, dbar, grating, dgrating


def _goal(t: float, params: Params) -> tuple[float, float]:
    """Instructed goal heading and velocity, independent of visual feedback."""
    if t <= params.goal_onset_s:
        return 0.0, 0.0
    amplitude = np.deg2rad(params.goal_amplitude_deg)
    elapsed = (t - params.goal_onset_s) / params.goal_tau_s
    return amplitude * (1.0 - np.exp(-elapsed)), amplitude * np.exp(-elapsed) / params.goal_tau_s


def _bar_torque(
    theta_bar: float,
    dtheta_bar: float,
    heading: float,
    omega: float,
    p_gain: float,
    v_gain: float,
    v_mode: str = "clip",
) -> float:
    error = np.arctan2(np.sin(theta_bar - heading), np.cos(theta_bar - heading))
    p_term = p_gain * np.sin(error)
    # The source's V term is negative for |error| > sqrt(10) rad. Outside the
    # small-error regime the model is not identified, so clip to a non-negative
    # gain and record the numerical boundary explicitly.
    if v_mode == "clip":
        v_term = v_gain * max(0.0, 20.0 - 2.0 * error * error)
    elif v_mode == "smooth":
        v_term = v_gain * 20.0 / (1.0 + (error / 3.16227766) ** 4)
    elif v_mode == "unclipped":
        v_term = v_gain * (20.0 - 2.0 * error * error)
    else:
        raise ValueError(f"unknown v_mode: {v_mode}")
    return p_term + (dtheta_bar - omega) * v_term


def _ff_torque(
    goal: tuple[float, float],
    ff_state: tuple[float, float],
    params: Params,
) -> float:
    """Feedforward torque from the resolved self-state sample.

    mode "goal" tracks the instructed goal trajectory; mode "damping" applies
    pure derivative feedback with no target information, as a no-goal control.
    """
    if params.ff_mode == "goal":
        theta_goal, dtheta_goal = goal
        ff_heading, ff_omega = ff_state
        return _bar_torque(
            theta_goal,
            dtheta_goal,
            ff_heading,
            ff_omega,
            params.p_gain,
            params.v_gain,
            params.v_mode,
        )
    if params.ff_mode == "damping":
        _, ff_omega = ff_state
        return -params.ff_damp_gain * ff_omega
    raise ValueError(f"unknown ff_mode: {params.ff_mode}")


def _derivatives(
    state: np.ndarray,
    model: str,
    delayed: tuple[float, float, float, float, float, float],
    current: tuple[float, float, float, float, float, float],
    goal: tuple[float, float],
    ff_state: tuple[float, float],
    params: Params,
    grating_gain: float,
) -> np.ndarray:
    heading, omega, f_bar, f_grating = state[:4]
    theta_bar, dtheta_bar, theta_grat, dtheta_grat, heading_d, omega_d = delayed
    theta_bar_c, dtheta_bar_c, _, _, heading_c, omega_c = current
    if params.undelayed_selfstate:
        heading_d, omega_d = heading_c, omega_c

    if model in ("pd_instant", "pd_gate"):
        # Classical PD stabilization with instantaneous true state (no gating,
        # no delay in the steering feedback). The grating pathway keeps the
        # delayed sensory estimate — it is the plant's optomotor channel.
        # pd_gate adds allnone-style grating gating on |f_bar| (W1, R1-M1).
        f_bar_feedback = _bar_torque(
            theta_bar_c,
            dtheta_bar_c,
            heading_c,
            omega_c,
            params.p_gain,
            params.v_gain,
            params.v_mode,
        )
        gain_pd = grating_gain
        if model == "pd_gate" and abs(f_bar) > params.gate_threshold:
            gain_pd = 0.0
        f_grating_dot = (-f_grating + (dtheta_grat - omega_d) * gain_pd) / params.tau_opto
        domega = (-params.drag * omega + f_bar + f_grating) / params.inertia
        return np.array([omega, domega, (-f_bar + f_bar_feedback) / params.tau_bar, f_grating_dot])

    f_bar_feedback = _bar_torque(
        theta_bar,
        dtheta_bar,
        heading_d,
        omega_d,
        params.p_gain,
        params.v_gain,
        params.v_mode,
    )
    f_goal = 0.0
    if model in FEEDFORWARD_MODELS:
        f_goal = _ff_torque(goal, ff_state, params)
    f_bar_dot = (-f_bar + f_bar_feedback + params.ff_gain * f_goal) / params.tau_bar
    f_bar_motor = _bar_torque(
        theta_bar_c,
        dtheta_bar_c,
        heading_c,
        omega_c,
        params.p_gain,
        params.v_gain,
        params.v_mode,
    )
    # A copy of the command issued at the current time. The command is based on
    # the delayed visual estimate, but the copy is available before the plant
    # filter has acted on it.
    f_bar_command = _bar_torque(
        theta_bar,
        dtheta_bar,
        heading_d,
        omega_d,
        params.p_gain,
        params.v_gain,
        params.v_mode,
    )

    grating_drive = dtheta_grat - omega_d
    gain = grating_gain
    if model in ("graded_sensory", "graded_motor", "graded_command", "graded_goal"):
        omega_ec = state[4]
        grating_drive = dtheta_grat + params.ec_gain * omega_ec - omega_d
    elif model == "allnone" and abs(f_bar) > params.gate_threshold:
        gain = 0.0
    elif model == "allnone_motor" and abs(f_bar_motor) > params.gate_threshold:
        gain = 0.0
    elif model == "gate_command" and abs(f_bar_command) > params.gate_threshold:
        gain = 0.0
    elif model == "gate_goal" and not params.disable_gate:
        trigger = abs(f_bar) if params.gate_trigger == "bar" else abs(f_bar + params.ff_gain * f_goal)
        if trigger > params.gate_threshold:
            gain = 0.0
    f_grating_dot = (-f_grating + grating_drive * gain) / params.tau_opto

    domega = (-params.drag * omega + f_bar + f_grating) / params.inertia
    if model in ("graded_sensory", "graded_motor", "graded_command", "graded_goal"):
        if model == "graded_sensory":
            ec_drive = f_bar
        elif model == "graded_motor":
            ec_drive = f_bar_motor
        elif model == "graded_command":
            ec_drive = f_bar_command
        else:
            ec_drive = f_bar + params.ff_gain * f_goal
        domega_ec = (-params.drag * state[4] + ec_drive) / params.inertia
        return np.array([omega, domega, f_bar_dot, f_grating_dot, domega_ec])
    return np.array([omega, domega, f_bar_dot, f_grating_dot])


def simulate(
    model: str,
    params: Params = Params(),
    *,
    delay_s: float = 0.0,
    grating_gain: float | None = None,
    noise_sd: float = 0.0,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    """Euler-Maruyama simulation. Returns time, state history, and readouts."""
    if model not in MODELS and model not in COMMAND_MODELS and model not in FEEDFORWARD_MODELS:
        raise ValueError(f"unknown model: {model}")
    if delay_s < 0:
        raise ValueError("delay_s must be non-negative")
    if params.ff_mode not in ("goal", "damping"):
        raise ValueError(f"unknown ff_mode: {params.ff_mode}")
    if params.ff_self_state_lag_s < 0:
        raise ValueError("ff_self_state_lag_s must be non-negative")

    dt = params.dt_s
    n_steps = int(round(params.t_end_s / dt)) + 1
    state_size = 5 if model in ("graded_sensory", "graded_motor", "graded_command", "graded_goal") else 4
    states = np.zeros((n_steps, state_size), dtype=np.float64)

    delay_steps = int(round(delay_s / dt))
    theta_bar_hist = np.zeros(n_steps)
    dtheta_bar_hist = np.zeros(n_steps)
    theta_grat_hist = np.zeros(n_steps)
    dtheta_grat_hist = np.zeros(n_steps)
    heading_hist = np.zeros(n_steps)
    omega_hist = np.zeros(n_steps)
    gate_hist = np.zeros(n_steps)

    rng = np.random.default_rng(seed)
    gain = params.k_opto if grating_gain is None else float(grating_gain)

    # P2-OBSERVER-02: forward-model observer state (smith/smith_pert).
    # The estimator integrates the internal model every step and, every
    # delay_steps, applies the delayed innovation on (heading, omega):
    # est += obs(t-d) - est_history(t-d). Exact params + no process noise =>
    # innovation is identically zero and the estimate equals the true state;
    # noise and/or parameter mismatch make it a genuine delayed-only observer.
    est = np.zeros(4)  # heading, omega, f_bar, f_grating of the internal model
    est_h_hist = np.zeros(n_steps)
    est_w_hist = np.zeros(n_steps)
    # W1: smith_dde keeps its OWN delayed feedback loop (delay embedded in the
    # internal model) and corrects via the d-old prediction error each interval.
    sh = np.zeros(4)
    sh_h_hist = np.zeros(n_steps)
    sh_w_hist = np.zeros(n_steps)

    for index in range(n_steps):
        t = index * dt
        theta_bar, dtheta_bar, theta_grat, dtheta_grat = _stimulus(t, params)
        goal = _goal(t - params.goal_delay_s, params)
        theta_bar_hist[index] = theta_bar
        dtheta_bar_hist[index] = dtheta_bar
        theta_grat_hist[index] = theta_grat
        dtheta_grat_hist[index] = dtheta_grat

        delayed_index = max(0, index - delay_steps)
        delayed = (
            theta_bar_hist[delayed_index],
            dtheta_bar_hist[delayed_index],
            theta_grat_hist[delayed_index],
            dtheta_grat_hist[delayed_index],
            heading_hist[delayed_index],
            omega_hist[delayed_index],
        )
        current = (
            theta_bar,
            dtheta_bar,
            theta_grat,
            dtheta_grat,
            states[index, 0],
            states[index, 1],
        )

        if model in ("smith", "smith_pert"):
            delay_steps_obs = max(1, delay_steps)
            if index % delay_steps_obs == 0:
                est[0] += heading_hist[delayed_index] - est_h_hist[delayed_index]
                est[1] += omega_hist[delayed_index] - est_w_hist[delayed_index]
            delayed = delayed[:4] + (est[0], est[1])
        if model == "smith_dde":
            delay_steps_obs = max(1, delay_steps)
            if index % delay_steps_obs == 0:
                sh[0] += heading_hist[delayed_index] - sh_h_hist[delayed_index]
                sh[1] += omega_hist[delayed_index] - sh_w_hist[delayed_index]
            delayed = delayed[:4] + (sh[0], sh[1])

        # Resolve the self-state sample used by the feedforward branch:
        # "current" ages the sample by ff_self_state_lag_s; "delayed" uses the
        # same lag as the visual path; "predicted" is a second-order Taylor
        # predictor that reconstructs current state from the delayed
        # observation alone (delayed states plus delayed angular acceleration).
        if model in FEEDFORWARD_MODELS:
            if params.ff_self_state == "current":
                lag_steps = int(round(params.ff_self_state_lag_s / dt))
                ff_index = max(0, index - lag_steps)
                ff_state = (heading_hist[ff_index], omega_hist[ff_index])
            elif params.ff_self_state == "delayed":
                ff_state = (heading_hist[delayed_index], omega_hist[delayed_index])
            elif params.ff_self_state == "predicted":
                d = delay_steps * dt
                h_d = heading_hist[delayed_index]
                w_d = omega_hist[delayed_index]
                alpha_d = (
                    states[delayed_index, 2] + states[delayed_index, 3]
                    - params.drag * w_d
                ) / params.inertia
                ff_state = (h_d + w_d * d + 0.5 * alpha_d * d * d, w_d + alpha_d * d)
            else:
                raise ValueError(f"unknown ff_self_state: {params.ff_self_state}")
        else:
            ff_state = (0.0, 0.0)

        if model in ("allnone", "allnone_motor", "gate_command", "gate_goal"):
            if model == "allnone":
                gate_closed = abs(states[index, 2]) > params.gate_threshold
            elif model == "allnone_motor":
                motor_drive = _bar_torque(
                    theta_bar,
                    dtheta_bar,
                    states[index, 0],
                    states[index, 1],
                    params.p_gain,
                    params.v_gain,
                    params.v_mode,
                )
                gate_closed = abs(motor_drive) > params.gate_threshold
            elif model == "gate_command":
                command_drive = _bar_torque(
                    theta_bar_hist[delayed_index],
                    dtheta_bar_hist[delayed_index],
                    heading_hist[delayed_index],
                    omega_hist[delayed_index],
                    params.p_gain,
                    params.v_gain,
                    params.v_mode,
                )
                gate_closed = abs(command_drive) > params.gate_threshold
            else:
                goal_drive = _ff_torque(goal, ff_state, params)
                if params.disable_gate:
                    gate_closed = False
                elif params.gate_trigger == "bar":
                    gate_closed = abs(states[index, 2]) > params.gate_threshold
                else:
                    gate_closed = (
                        abs(states[index, 2] + params.ff_gain * goal_drive) > params.gate_threshold
                    )
            gate_hist[index] = float(gate_closed)
        elif model == "pd_gate":
            gate_hist[index] = float(abs(states[index, 2]) > params.gate_threshold)

        deriv = _derivatives(states[index], model, delayed, current, goal, ff_state, params, gain)
        if noise_sd > 0:
            deriv[1] += rng.normal(0.0, noise_sd) / params.inertia
        if index == n_steps - 1:
            break
        next_state = states[index] + deriv * dt
        if not np.isfinite(next_state).all():
            states[index + 1 :] = np.nan
            break
        states[index + 1] = next_state
        heading_hist[index + 1] = states[index + 1, 0]
        omega_hist[index + 1] = states[index + 1, 1]
        if model in ("smith", "smith_pert"):
            drag_e = params.drag * (params.smith_drag_scale if model == "smith_pert" else 1.0)
            iner_e = params.inertia * (params.smith_inertia_scale if model == "smith_pert" else 1.0)
            f_bar_e = (
                -est[2]
                + _bar_torque(theta_bar, dtheta_bar, est[0], est[1], params.p_gain, params.v_gain, params.v_mode)
            ) / params.tau_bar
            f_grat_e = (-est[3] + (dtheta_grat - est[1]) * gain) / params.tau_opto
            d_h = est[1]
            d_w = (-drag_e * est[0] + est[2] + est[3]) / iner_e
            est = est + dt * np.array([d_h, d_w, f_bar_e, f_grat_e])
            est_h_hist[index + 1] = est[0]
            est_w_hist[index + 1] = est[1]
        if model == "smith_dde":
            drag_e = params.drag * params.smith_drag_scale
            iner_e = params.inertia * params.smith_inertia_scale
            j = delayed_index
            f_bar_sh = (
                -sh[2]
                + _bar_torque(
                    theta_bar_hist[j], dtheta_bar_hist[j], sh_h_hist[j], sh_w_hist[j],
                    params.p_gain, params.v_gain, params.v_mode,
                )
            ) / params.tau_bar
            f_grat_sh = (-sh[3] + (dtheta_grat_hist[j] - sh_w_hist[j]) * gain) / params.tau_opto
            d_h = sh[1]
            d_w = (-drag_e * sh[0] + sh[2] + sh[3]) / iner_e
            sh = sh + dt * np.array([d_h, d_w, f_bar_sh, f_grat_sh])
            sh_h_hist[index + 1] = sh[0]
            sh_w_hist[index + 1] = sh[1]

    time = np.arange(n_steps) * dt
    readouts = {
        "theta_bar": theta_bar_hist,
        "theta_grating": theta_grat_hist,
        "heading": states[:, 0],
        "omega": states[:, 1],
        "f_bar": states[:, 2],
        "f_grating": states[:, 3],
    }
    if model in ("graded_sensory", "graded_motor", "graded_command", "graded_goal"):
        readouts["omega_ec"] = states[:, 4]
    if model in ("allnone", "allnone_motor", "gate_command", "gate_goal"):
        readouts["gate_closed"] = gate_hist
    return time, states, readouts


def metrics(
    model: str,
    params: Params,
    *,
    delay_s: float,
    grating_gain: float,
    noise_sd: float,
    seed: int,
) -> Metrics:
    time, _, readouts = simulate(
        model,
        params,
        delay_s=delay_s,
        grating_gain=grating_gain,
        noise_sd=noise_sd,
        seed=seed,
    )
    bar_final = float(readouts["theta_bar"][-1])
    heading = readouts["heading"]
    failure = int(not np.isfinite(heading).all())
    error = np.abs(readouts["theta_bar"] - heading)
    threshold = 0.05 * abs(bar_final) if abs(bar_final) > 0 else np.inf
    settled = error < threshold
    settling_time = float("nan")
    for index in range(len(time)):
        if settled[index:].all():
            settling_time = float(time[index])
            break

    return Metrics(
        model=model,
        delay_s=float(delay_s),
        k_opto=float(grating_gain),
        noise_sd=float(noise_sd),
        seed=int(seed),
        final_error_deg=float(np.rad2deg(abs(bar_final - heading[-1]))),
        peak_heading_deg=float(np.rad2deg(np.max(np.abs(heading)))),
        overshoot_deg=float(np.rad2deg(max(0.0, np.max(heading) - bar_final))),
        settling_time_s=settling_time,
        grating_torque_rms=float(np.sqrt(np.mean(readouts["f_grating"] ** 2))),
        max_abs_grating_torque=float(np.max(np.abs(readouts["f_grating"]))),
        heading_final_deg=float(np.rad2deg(heading[-1])),
        numerical_failure=failure,
    )


def run_sweep(
    params: Params = Params(),
    *,
    delays: tuple[float, ...] = (0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3),
    gains: tuple[float, ...] = (0.0, 25e-12, 50e-12),
    seeds: tuple[int, ...] = (0,),
    noise_sd: float = 0.0,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model in MODELS:
        for delay in delays:
            for gain in gains:
                for seed in seeds:
                    row = metrics(
                        model,
                        params,
                        delay_s=delay,
                        grating_gain=gain,
                        noise_sd=noise_sd,
                        seed=seed,
                    )
                    rows.append(asdict(row))
    return rows


def _selftest() -> None:
    params = Params(t_end_s=1.2, dt_s=2e-4)
    for model in MODELS:
        time, states, readouts = simulate(model, params)
        assert time.shape == states.shape[:1]
        assert np.isfinite(states).all(), model
        assert abs(readouts["heading"][-1]) > 0.01, model
    for model in FEEDFORWARD_MODELS:
        time, states, readouts = simulate(
            model, Params(t_end_s=1.2, dt_s=2e-4, ff_gain=1.0)
        )
        assert np.isfinite(states).all(), model

    base = metrics("addition", params, delay_s=0.0, grating_gain=25e-12, noise_sd=0.0, seed=0)
    gated = metrics("allnone", params, delay_s=0.0, grating_gain=25e-12, noise_sd=0.0, seed=0)
    assert np.isfinite(base.final_error_deg)
    assert np.isfinite(gated.final_error_deg)
    print("SELFTEST PASS")
    print(json.dumps(asdict(base), indent=2))
    print(json.dumps(asdict(gated), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal efference-copy steering model")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if args.selftest:
        _selftest()
        return 0
    if args.sweep:
        rows = run_sweep()
        text = json.dumps(rows, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {len(rows)} rows")
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
