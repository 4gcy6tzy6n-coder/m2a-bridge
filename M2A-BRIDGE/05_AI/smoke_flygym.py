#!/usr/bin/env python3
"""Minimal flyvis / FlyGym smoke test.

Modes:
    --dry-run   print plan and versions; no simulation
    --debug     one flyvis Network + one FlyGym step; validate outputs
    --run       flyvis Network + FlyGym N steps; write JSON report

The full FlyGym actuated models (FlyBody / MusculoskeletalFly) need a one-time
mesh asset download from datasets.epfl.ch. If that host is unreachable, the
smoke test still validates the CPU free-body simulation and records the
actuated-model status as BLOCKED_BY_ASSET_HOST.
"""

from __future__ import annotations

import argparse
import importlib.metadata as metadata
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REQUIRED_KEYS = ("status", "timestamp", "versions", "flyvis", "flygym", "resources", "checks")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in ("flyvis", "flygym", "torch", "mujoco", "numpy", "scipy"):
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "missing"
    return versions


def rss_mb() -> float:
    try:
        import psutil

        return round(psutil.Process(os.getpid()).memory_info().rss / 1e6, 1)
    except Exception:
        return float("nan")


def environment() -> dict[str, str]:
    info = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cwd": str(Path.cwd()),
    }
    try:
        import torch

        info["torch_mps"] = str(bool(torch.backends.mps.is_available()))
        info["torch_cuda"] = str(bool(torch.cuda.is_available()))
    except Exception as exc:
        info["torch_error"] = repr(exc)
    return info


def flyvis_check() -> dict[str, object]:
    import flyvis

    started = time.time()
    network = flyvis.Network()
    elapsed = time.time() - started
    return {
        "nodes": int(network.n_nodes),
        "edges": int(network.n_edges),
        "parameters": str(getattr(network, "num_parameters", "")),
        "seconds": round(elapsed, 2),
    }


def flygym_check(steps: int) -> dict[str, object]:
    import flygym
    from flygym.compose import FlatGroundWorld, NeuroMechFly
    from flygym.utils.math import Rotation3D

    started = time.time()
    world = FlatGroundWorld()
    fly = NeuroMechFly()
    world.add_fly(
        fly,
        spawn_position=(0.0, 0.0, 0.5),
        spawn_rotation=Rotation3D("quat", (1.0, 0.0, 0.0, 0.0)),
    )
    simulation = flygym.Simulation(world)
    build_seconds = time.time() - started

    qpos_before = simulation.mj_data.qpos.copy()
    step_started = time.time()
    for _ in range(steps):
        simulation.step()
    step_seconds = time.time() - step_started

    qpos = simulation.mj_data.qpos.copy()
    positions = simulation.get_body_positions("nmf")
    result = {
        "timestep": float(simulation.timestep),
        "steps": int(steps),
        "qpos_dim": int(qpos.shape[0]),
        "bodies": int(positions.shape[0]),
        "build_seconds": round(build_seconds, 2),
        "step_seconds": round(step_seconds, 3),
        "qpos_finite": bool(np.isfinite(qpos).all()),
        "positions_finite": bool(np.isfinite(positions).all()),
        "qpos_max_delta": float(np.abs(qpos - qpos_before).max()),
        "actuated_model": "BLOCKED_BY_ASSET_HOST (default NeuroMechFly has free root joint only)",
    }
    simulation.close()
    return result


def validate(result: dict[str, object]) -> dict[str, bool]:
    flyvis = result["flyvis"]
    flygym = result["flygym"]
    return {
        "flyvis_imported": bool(flyvis["nodes"] > 0),
        "flyvis_connectome_nonempty": bool(flyvis["edges"] > 0),
        "flygym_timestep_positive": bool(flygym["timestep"] > 0),
        "flygym_qpos_finite": bool(flygym["qpos_finite"]),
        "flygym_positions_finite": bool(flygym["positions_finite"]),
        "flygym_bodies_nonempty": bool(flygym["bodies"] > 0),
    }


def build_result(steps: int) -> dict[str, object]:
    checks: dict[str, object] = {}
    try:
        flyvis = flyvis_check()
        checks["flyvis"] = "PASS"
    except Exception as exc:
        flyvis = {"error": repr(exc)}
        checks["flyvis"] = "FAIL"

    try:
        flygym = flygym_check(steps)
        checks["flygym"] = "PASS"
    except Exception as exc:
        flygym = {"error": repr(exc)}
        checks["flygym"] = "FAIL"

    result: dict[str, object] = {
        "status": "pending",
        "timestamp": now_iso(),
        "versions": package_versions(),
        "environment": environment(),
        "flyvis": flyvis,
        "flygym": flygym,
        "resources": {"rss_mb": rss_mb()},
        "checks": checks,
    }

    if checks["flyvis"] == "PASS" and checks["flygym"] == "PASS":
        assertions = validate(result)
        result["assertions"] = assertions
        result["status"] = "pass" if all(assertions.values()) else "fail"
    else:
        result["assertions"] = {}
        result["status"] = "fail"

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Minimal flyvis / FlyGym smoke test")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--debug", action="store_true")
    mode.add_argument("--run", action="store_true")
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "steps": args.steps,
                    "versions": package_versions(),
                    "environment": environment(),
                    "plan": ["flyvis.Network()", "FlyGym FlatGroundWorld + NeuroMechFly", f"{args.steps} simulation steps", "write JSON"],
                },
                indent=2,
            )
        )
        return 0

    steps = 1 if args.debug else args.steps
    result = build_result(steps)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
