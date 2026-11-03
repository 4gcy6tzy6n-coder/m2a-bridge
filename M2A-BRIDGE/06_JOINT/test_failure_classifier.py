#!/usr/bin/env python3
"""Tests for the canonical failure classifier."""

from __future__ import annotations

import numpy as np
import pytest

from failure_classifier import (
    DEFAULT_DWELL_S,
    HEADING_LIMIT_RAD,
    OMEGA_LIMIT_RAD_S,
    Classification,
    classify,
    longest_true_run_s,
)


def _traj(n: int, dt: float, heading: float = 0.0, omega: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    return np.full(n, heading), np.full(n, omega)


def test_longest_true_run_s_basic() -> None:
    dt = 1e-4
    mask = np.array([False, True, True, True, False, True, True])
    assert longest_true_run_s(mask, dt) == pytest.approx(3 * dt)
    assert longest_true_run_s(np.zeros(5, dtype=bool), dt) == 0.0
    assert longest_true_run_s(np.ones(4, dtype=bool), dt) == pytest.approx(4 * dt)


def test_clean_trajectory_is_not_failure() -> None:
    heading, omega = _traj(1000, 1e-4, heading=0.5, omega=10.0)
    result = classify(heading, omega, dt_s=1e-4)
    assert result.failure_instantaneous == 0
    assert result.failure_sustained == 0
    assert result.longest_omega_exceedance_s == 0.0
    assert result.longest_heading_exceedance_s == 0.0


def test_single_sample_spike_is_transient_only() -> None:
    dt = 1e-4
    heading, omega = _traj(1000, dt)
    omega = omega.copy()
    omega[500] = OMEGA_LIMIT_RAD_S + 1.0
    result = classify(heading, omega, dt_s=dt, dwell_s=DEFAULT_DWELL_S)
    assert result.failure_instantaneous == 1
    assert result.failure_sustained == 0
    assert result.longest_omega_exceedance_s == pytest.approx(dt)
    assert result.first_omega_crossing_s == pytest.approx(500 * dt)


def test_sustained_exceedance_is_failure_under_both_criteria() -> None:
    dt = 1e-4
    n = 1000
    omega = np.full(n, OMEGA_LIMIT_RAD_S + 1.0)
    heading = np.zeros(n)
    result = classify(heading, omega, dt_s=dt, dwell_s=0.005)
    assert result.failure_instantaneous == 1
    assert result.failure_sustained == 1
    assert result.longest_omega_exceedance_s == pytest.approx(n * dt)


def test_heading_channel_triggers_sustained_failure() -> None:
    dt = 1e-4
    heading = np.full(500, HEADING_LIMIT_RAD + 0.1)
    omega = np.zeros(500)
    result = classify(heading, omega, dt_s=dt, dwell_s=0.01)
    assert result.failure_instantaneous == 1
    assert result.failure_sustained == 1
    assert result.longest_heading_exceedance_s == pytest.approx(500 * dt)


def test_dwell_boundary_is_inclusive() -> None:
    dt = 1e-3
    n_burst = 10  # 10 ms burst at dt=1 ms
    omega = np.zeros(100)
    omega[20 : 20 + n_burst] = OMEGA_LIMIT_RAD_S + 1.0
    heading = np.zeros(100)
    result = classify(heading, omega, dt_s=dt, dwell_s=0.010)
    assert result.failure_sustained == 1


def test_nonfinite_is_failure_under_both_criteria() -> None:
    heading = np.array([0.0, 0.1, np.nan, np.inf])
    omega = np.array([0.0, 1.0, 1.0, 1.0])
    result = classify(heading, omega, dt_s=1e-4)
    assert result.failure_instantaneous == 1
    assert result.failure_sustained == 1
    assert result.longest_heading_exceedance_s == float("inf")


def test_instantaneous_matches_legacy_peak_formula() -> None:
    rng = np.random.default_rng(7)
    for _ in range(50):
        n = int(rng.integers(50, 500))
        heading = rng.normal(0.0, 4.0, n)
        omega = rng.normal(0.0, 120.0, n)
        if rng.random() < 0.3:
            heading[int(rng.integers(0, n))] = np.nan
        legacy = int(
            (not np.isfinite(heading).all())
            or np.nanmax(np.abs(heading)) > HEADING_LIMIT_RAD
            or np.nanmax(np.abs(omega)) > OMEGA_LIMIT_RAD_S
        )
        result = classify(heading, omega, dt_s=1e-4)
        assert result.failure_instantaneous == legacy


def test_classification_is_immutable() -> None:
    heading, omega = _traj(10, 1e-4)
    result = classify(heading, omega, dt_s=1e-4)
    with pytest.raises(Exception):
        result.failure_instantaneous = 1  # type: ignore[misc]
    assert isinstance(result, Classification)


def test_invalid_inputs_raise() -> None:
    heading, omega = _traj(10, 1e-4)
    with pytest.raises(ValueError):
        classify(heading, omega, dt_s=0.0)
    with pytest.raises(ValueError):
        classify(heading, omega, dt_s=1e-4, dwell_s=-1.0)
    with pytest.raises(ValueError):
        classify(np.ones(3), np.ones(4), dt_s=1e-4)
