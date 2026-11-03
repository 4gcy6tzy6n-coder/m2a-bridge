import numpy as np
import pytest

from ec_model import FEEDFORWARD_MODELS, MODELS, Params, metrics, simulate


@pytest.mark.parametrize("model", MODELS)
def test_models_are_finite_at_zero_delay(model):
    params = Params(t_end_s=1.0, dt_s=5e-4)
    time, states, readouts = simulate(model, params)
    assert time.shape == states.shape[:1]
    assert np.isfinite(states).all()
    assert abs(readouts["heading"][-1]) > 0.01


def test_allnone_reduces_grating_torque_relative_to_addition():
    params = Params(t_end_s=1.0, dt_s=5e-4)
    _, _, addition = simulate("addition", params, grating_gain=params.k_opto)
    _, _, gated = simulate("allnone", params, grating_gain=params.k_opto)
    addition_rms = np.sqrt(np.mean(addition["f_grating"] ** 2))
    gated_rms = np.sqrt(np.mean(gated["f_grating"] ** 2))
    assert gated_rms < addition_rms


def test_graded_models_have_ec_state():
    params = Params(t_end_s=0.5, dt_s=5e-4)
    for model in ("graded_sensory", "graded_motor", "graded_command", "graded_goal"):
        _, states, readouts = simulate(model, params)
        assert states.shape[1] == 5
        assert "omega_ec" in readouts
        assert np.isfinite(readouts["omega_ec"]).all()


@pytest.mark.parametrize("model", FEEDFORWARD_MODELS)
def test_feedforward_models_are_finite(model):
    params = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0)
    _, states, _ = simulate(model, params)
    assert np.isfinite(states).all()


def test_feedforward_zero_gain_matches_graded_sensory():
    params = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=0.0)
    _, sensory, sensory_readouts = simulate("graded_sensory", params)
    _, goal, goal_readouts = simulate("graded_goal", params)
    assert np.allclose(sensory, goal)
    assert np.allclose(sensory_readouts["omega_ec"], goal_readouts["omega_ec"])


def test_feedforward_gain_changes_trajectory():
    params = Params(t_end_s=1.0, dt_s=5e-4)
    _, _, baseline = simulate("graded_goal", params, delay_s=0.1)
    _, _, driven = simulate(
        "graded_goal", Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0), delay_s=0.1
    )
    assert not np.allclose(baseline["heading"], driven["heading"])


def test_goal_delay_changes_feedforward_trajectory():
    params = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0)
    _, _, immediate = simulate("graded_goal", params, delay_s=0.1)
    _, _, delayed = simulate(
        "graded_goal",
        Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, goal_delay_s=0.1),
        delay_s=0.1,
    )
    assert not np.allclose(immediate["heading"], delayed["heading"])


def test_ff_self_state_changes_feedforward_trajectory():
    params = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0)
    _, _, current = simulate("graded_goal", params, delay_s=0.1)
    _, _, delayed = simulate(
        "graded_goal",
        Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_self_state="delayed"),
        delay_s=0.1,
    )
    assert not np.allclose(current["heading"], delayed["heading"])


def test_unknown_ff_self_state_raises():
    with pytest.raises(ValueError):
        simulate(
            "graded_goal",
            Params(t_end_s=0.2, dt_s=1e-3, ff_gain=1.0, ff_self_state="nope"),
        )


def test_damping_mode_finite_and_zero_gain_matches_allnone():
    params = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_mode="damping", ff_damp_gain=1e-11)
    _, states, _ = simulate("gate_goal", params)
    assert np.isfinite(states).all()
    p0 = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=0.0, ff_mode="damping")
    _, gated, _ = simulate("gate_goal", p0)
    _, base, _ = simulate("allnone", p0)
    assert np.allclose(gated, base)


def test_damping_changes_trajectory():
    base = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0)
    _, _, goal_run = simulate("gate_goal", base, delay_s=0.1)
    _, _, damp_run = simulate(
        "gate_goal",
        Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_mode="damping"),
        delay_s=0.1,
    )
    assert not np.allclose(goal_run["heading"], damp_run["heading"])


def test_self_state_lag_changes_trajectory():
    _, _, fresh = simulate(
        "graded_goal",
        Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_self_state_lag_s=0.0),
        delay_s=0.2,
    )
    _, _, aged = simulate(
        "graded_goal",
        Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_self_state_lag_s=0.1),
        delay_s=0.2,
    )
    assert not np.allclose(fresh["heading"], aged["heading"])


def test_unknown_ff_mode_raises():
    with pytest.raises(ValueError):
        simulate(
            "gate_goal",
            Params(t_end_s=0.2, dt_s=1e-3, ff_gain=1.0, ff_mode="nope"),
        )


def test_predicted_self_state_runs_and_differs():
    params = Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_self_state="predicted")
    _, states, _ = simulate("gate_goal", params, delay_s=0.1)
    assert np.isfinite(states).all()
    _, _, delayed = simulate(
        "gate_goal",
        Params(t_end_s=1.0, dt_s=5e-4, ff_gain=1.0, ff_self_state="delayed"),
        delay_s=0.1,
    )
    _, _, predicted = simulate("gate_goal", params, delay_s=0.1)
    assert not np.allclose(delayed["heading"], predicted["heading"])


def test_predicted_zero_delay_matches_delayed():
    # at zero delay the Taylor correction vanishes, so predicted == delayed
    _, _, pred = simulate("gate_goal", Params(t_end_s=0.8, dt_s=5e-4, ff_gain=1.0, ff_self_state="predicted"), delay_s=0.0)
    _, _, dly = simulate("gate_goal", Params(t_end_s=0.8, dt_s=5e-4, ff_gain=1.0, ff_self_state="delayed"), delay_s=0.0)
    assert np.allclose(pred["heading"], dly["heading"], equal_nan=True)


def test_metrics_schema_and_failure_flag():
    params = Params(t_end_s=0.8, dt_s=5e-4)
    result = metrics(
        "addition",
        params,
        delay_s=0.0,
        grating_gain=params.k_opto,
        noise_sd=0.0,
        seed=0,
    )
    payload = result.__dict__
    assert payload["model"] == "addition"
    assert np.isfinite(payload["final_error_deg"])
    assert payload["numerical_failure"] in (0, 1)


def test_delay_changes_trajectory():
    params = Params(t_end_s=1.0, dt_s=5e-4)
    _, _, fast = simulate("addition", params, delay_s=0.0)
    _, _, delayed = simulate("addition", params, delay_s=0.1)
    assert not np.allclose(fast["heading"], delayed["heading"])


def test_smith_zero_delay_equals_addition():
    # with delay 0 the innovation snaps the estimator to the true state every
    # step, so the smith observer must reproduce the plain addition model
    params = Params(t_end_s=0.8, dt_s=5e-4)
    _, _, add = simulate("addition", params, delay_s=0.0, noise_sd=0.0)
    _, _, sm = simulate("smith", params, delay_s=0.0, noise_sd=0.0)
    assert np.allclose(add["heading"], sm["heading"], equal_nan=True)
    assert np.allclose(add["f_grating"], sm["f_grating"], equal_nan=True)


def test_pd_instant_zero_delay_equals_addition():
    # instantaneous classical PD with zero delay equals the delayed model
    params = Params(t_end_s=0.8, dt_s=5e-4)
    _, _, add = simulate("addition", params, delay_s=0.0, noise_sd=0.0)
    _, _, pd = simulate("pd_instant", params, delay_s=0.0, noise_sd=0.0)
    assert np.allclose(add["heading"], pd["heading"], equal_nan=True)


def test_smith_finite_under_delay_and_noise():
    params = Params(t_end_s=1.2, dt_s=5e-4)
    for model in ("smith", "smith_pert", "pd_instant"):
        _, states, readouts = simulate(model, params, delay_s=0.1, noise_sd=1e-13, seed=0)
        assert np.isfinite(readouts["heading"]).all()
        assert states.shape[1] == 4


def test_pd_gate_zero_delay_matches_pd_instant_when_never_closing():
    # with a huge gate threshold the gate never closes: pd_gate == pd_instant
    params = Params(t_end_s=0.8, dt_s=5e-4, gate_threshold=1e9)
    _, _, a = simulate("pd_instant", params, delay_s=0.0, noise_sd=0.0)
    _, _, b = simulate("pd_gate", params, delay_s=0.0, noise_sd=0.0)
    assert np.allclose(a["heading"], b["heading"], equal_nan=True)


def test_smith_dde_zero_delay_equals_addition():
    params = Params(t_end_s=0.8, dt_s=5e-4)
    _, _, add = simulate("addition", params, delay_s=0.0, noise_sd=0.0)
    _, _, sm = simulate("smith_dde", params, delay_s=0.0, noise_sd=0.0)
    assert np.allclose(add["heading"], sm["heading"], equal_nan=True)


def test_undelayed_selfstate_zero_delay_equals_addition():
    params = Params(t_end_s=0.8, dt_s=5e-4, undelayed_selfstate=True)
    _, _, add = simulate("addition", Params(t_end_s=0.8, dt_s=5e-4), delay_s=0.0, noise_sd=0.0)
    _, _, us = simulate("addition", params, delay_s=0.0, noise_sd=0.0)
    assert np.allclose(add["heading"], us["heading"], equal_nan=True)


def test_disable_gate_and_gate_trigger_bar_run_finite():
    p1 = Params(t_end_s=1.2, dt_s=5e-4, ff_gain=1.0, disable_gate=True)
    _, s1, _ = simulate("gate_goal", p1, delay_s=0.1, noise_sd=1e-13, seed=0)
    assert np.isfinite(s1).all()
    p2 = Params(t_end_s=1.2, dt_s=5e-4, ff_gain=1.0, gate_trigger="bar")
    _, s2, r2 = simulate("gate_goal", p2, delay_s=0.1, noise_sd=1e-13, seed=0)
    assert np.isfinite(s2).all() and "gate_closed" in r2


def test_smith_dde_finite_under_delay():
    params = Params(t_end_s=1.2, dt_s=5e-4)
    _, states, _ = simulate("smith_dde", params, delay_s=0.1, noise_sd=1e-13, seed=0)
    assert np.isfinite(states).all() and states.shape[1] == 4
