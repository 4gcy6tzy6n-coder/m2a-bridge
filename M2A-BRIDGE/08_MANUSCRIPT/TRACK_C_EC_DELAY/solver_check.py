#!/usr/bin/env python3
"""Compare Euler dt=1e-4 against dt=5e-5 for representative conditions."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/06_JOINT")
from ec_model import Params, simulate  # noqa: E402

OUT = Path(__file__).resolve().parent / "solver_check.json"
CASES = (
    ("addition", 0.02),
    ("graded_sensory", 0.02),
    ("graded_motor", 0.02),
    ("allnone", 0.12),
    ("allnone_motor", 0.12),
)


def main() -> None:
    rows = []
    for model, delay in CASES:
        results = {}
        for dt in (1e-4, 5e-5):
            params = Params(dt_s=dt, t_end_s=1.5)
            _, _, readouts = simulate(model, params, delay_s=delay, grating_gain=params.k_opto)
            results[str(dt)] = {
                "max_abs_heading_rad": float(np.nanmax(np.abs(readouts["heading"]))),
                "max_abs_omega_rad_s": float(np.nanmax(np.abs(readouts["omega"]))),
            }
        coarse = results["0.0001"]
        fine = results["5e-05"]
        rows.append(
            {
                "model": model,
                "delay_s": delay,
                "coarse": coarse,
                "fine": fine,
                "heading_rel_diff": abs(coarse["max_abs_heading_rad"] - fine["max_abs_heading_rad"])
                / max(fine["max_abs_heading_rad"], 1e-12),
                "omega_rel_diff": abs(coarse["max_abs_omega_rad_s"] - fine["max_abs_omega_rad_s"])
                / max(fine["max_abs_omega_rad_s"], 1e-12),
            }
        )
    OUT.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(
            f"{row['model']:16} delay={row['delay_s']:.2f} "
            f"heading_rel_diff={row['heading_rel_diff']:.3e} omega_rel_diff={row['omega_rel_diff']:.3e}"
        )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
