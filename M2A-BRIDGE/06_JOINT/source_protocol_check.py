#!/usr/bin/env python3
"""Check the source paper's constant-grating background protocol.

The source's Figure 5 uses scaled parameters (I=6e-4, beta=1e-1, P=1.0,
V=1e-2), a bar step of pi/3, a constant grating angle (zero velocity), and a
grating gain that switches from 0.05 to 0.7. We ask whether the peak heading is
invariant to the grating gain in each of our variants, across efference-copy
gains and gate thresholds.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ec_model import Params, simulate

OUT = Path(__file__).resolve().parent.parent / "08_MANUSCRIPT/TRACK_C_EC_DELAY/source_protocol_check.json"
BASE = Params(
    inertia=6e-4,
    drag=1e-1,
    tau_bar=0.05,
    tau_opto=0.04,
    k_opto=0.05,
    gate_threshold=0.15,
    bar_amplitude_deg=60.0,
    grating_amplitude_deg=0.0,
    bar_onset_s=0.5,
    grating_onset_s=0.75,
    stimulus_slope=30.0,
    t_end_s=2.2,
    dt_s=2e-5,
    p_gain=1.0,
    v_gain=1e-2,
    ec_gain=1.0,
)


def run(model: str, gain: float, params: Params) -> dict[str, object]:
    _, _, readouts = simulate(model, params, delay_s=0.0, grating_gain=gain)
    heading = readouts["heading"]
    return {
        "model": model,
        "grating_gain": gain,
        "ec_gain": params.ec_gain,
        "gate_threshold": params.gate_threshold,
        "max_abs_heading_deg": float(np.rad2deg(np.nanmax(np.abs(heading)))),
        "heading_final_deg": float(np.rad2deg(heading[-1])),
        "finite": bool(np.isfinite(heading).all()),
    }


def main() -> None:
    rows = []
    # Fixed-gain graded variants: vary the efference-copy gain.
    for ec_gain in (0.5, 1.0, 1.5):
        for model in ("graded_sensory", "graded_motor"):
            for gain in (0.05, 0.7):
                rows.append(run(model, gain, replace(BASE, ec_gain=ec_gain)))
    # All-or-none variants: vary the gate threshold.
    for threshold in (0.15, 0.015, 1.5e-12):
        for model in ("allnone", "allnone_motor"):
            for gain in (0.05, 0.7):
                rows.append(run(model, gain, replace(BASE, gate_threshold=threshold)))
    # Addition baseline.
    for gain in (0.05, 0.7):
        rows.append(run("addition", gain, BASE))

    OUT.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(
            f"{row['model']:16} ec_gain={row['ec_gain']:.1f} "
            f"gate={row['gate_threshold']:.2e} gain={row['grating_gain']:.2f} "
            f"peak={row['max_abs_heading_deg']:.3f} deg"
        )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
