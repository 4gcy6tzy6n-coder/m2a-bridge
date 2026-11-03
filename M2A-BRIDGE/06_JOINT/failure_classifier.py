#!/usr/bin/env python3
"""Canonical failure classification for the EC steering model.

Historical problem (see wiki/90_changelog, P1-EC-NOISE-01 / solver_check):
26 runner scripts each carried a copy of a peak-threshold classifier — any
single sample with |heading| > 2*pi rad or |omega| > 100 rad/s labels the
whole run a failure. Near the critical delay zone, single-sample flickers
and float-noise amplified by chaos flip labels across noise levels, seeds
and dt (gate filtered @100 ms: 0% -> 12.5% at noise 1e-12; dt halving moves
fast-failing variants by 2-16%).

This module centralizes the criterion and records the sufficient statistics
(longest continuous exceedance duration per channel) so that:

- ``failure_instantaneous`` reproduces the legacy label bit-for-bit;
- ``failure_sustained`` requires the threshold to be exceeded continuously
  for at least ``dwell_s`` (genuine instabilities cross 2*pi and stay;
  noise flickers recover within a sample or two);
- any other dwell can be applied post-hoc from the recorded durations
  without re-simulating.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

HEADING_LIMIT_RAD = 2.0 * np.pi
OMEGA_LIMIT_RAD_S = 100.0
DEFAULT_DWELL_S = 0.010


@dataclass(frozen=True)
class Classification:
    failure_instantaneous: int
    failure_sustained: int
    max_abs_heading_rad: float
    max_abs_omega_rad_s: float
    longest_heading_exceedance_s: float
    longest_omega_exceedance_s: float
    first_heading_crossing_s: float
    first_omega_crossing_s: float


def longest_true_run_s(mask: np.ndarray, dt_s: float) -> float:
    """Duration of the longest consecutive True run in ``mask``."""
    if mask.size == 0:
        return 0.0
    padded = np.concatenate(([False], mask, [False]))
    edges = np.diff(padded.astype(np.int8))
    starts = np.flatnonzero(edges == 1)
    ends = np.flatnonzero(edges == -1)
    if starts.size == 0:
        return 0.0
    return float((ends - starts).max() * dt_s)


def _first_crossing_s(mask: np.ndarray, dt_s: float) -> float:
    indices = np.flatnonzero(mask)
    return float(indices[0] * dt_s) if indices.size else float("nan")


def classify(
    heading: np.ndarray,
    omega: np.ndarray,
    *,
    dt_s: float,
    dwell_s: float = DEFAULT_DWELL_S,
) -> Classification:
    """Classify one trajectory under both the instantaneous and sustained criteria."""
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    if dwell_s < 0:
        raise ValueError("dwell_s must be non-negative")
    if heading.shape != omega.shape:
        raise ValueError("heading and omega must have the same shape")

    finite = np.isfinite(heading) & np.isfinite(omega)
    all_finite = bool(finite.all())
    heading_mask = np.abs(np.where(finite, heading, np.inf)) > HEADING_LIMIT_RAD
    omega_mask = np.abs(np.where(finite, omega, np.inf)) > OMEGA_LIMIT_RAD_S

    if all_finite:
        longest_heading = longest_true_run_s(heading_mask, dt_s)
        longest_omega = longest_true_run_s(omega_mask, dt_s)
        max_heading = float(np.max(np.abs(heading)))
        max_omega = float(np.max(np.abs(omega)))
    else:
        # Non-finite anywhere: treat as diverged from the first bad sample on.
        longest_heading = float("inf")
        longest_omega = float("inf")
        max_heading = float("inf")
        max_omega = float("inf")

    failure_instantaneous = int(
        (not all_finite) or bool(heading_mask.any()) or bool(omega_mask.any())
    )
    failure_sustained = int(
        (not all_finite)
        or longest_heading >= dwell_s
        or longest_omega >= dwell_s
    )

    return Classification(
        failure_instantaneous=failure_instantaneous,
        failure_sustained=failure_sustained,
        max_abs_heading_rad=max_heading,
        max_abs_omega_rad_s=max_omega,
        longest_heading_exceedance_s=longest_heading,
        longest_omega_exceedance_s=longest_omega,
        first_heading_crossing_s=_first_crossing_s(heading_mask, dt_s),
        first_omega_crossing_s=_first_crossing_s(omega_mask, dt_s),
    )
