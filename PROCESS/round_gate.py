#!/usr/bin/env python3
"""Round gate: block experiments until debug evidence is complete.

Usage:
    python3 PROCESS/round_gate.py --init runs/R001
    python3 PROCESS/round_gate.py --round runs/R001
    python3 PROCESS/round_gate.py --selftest

Exit codes:
    0  gate passed
    1  usage or internal error
    2  gate blocked
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TEMPLATES = Path(__file__).resolve().parent / "templates"
ALLOWED_TYPES = {"dev", "pilot", "confirmatory"}
MIN_DEBUG_CHECKS = 4
REQUIRED_HEADINGS = (
    "## 1. 本轮范围",
    "## 2. 已运行的检查",
    "## 3. 发现的问题",
    "## 4. 修复",
    "## 5. 残余风险",
    "## 6. 门禁结论",
)


class GateError(Exception):
    """Raised when the round cannot be initialized or checked."""


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    if not path.exists():
        raise GateError(f"missing file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GateError(f"invalid JSON in {path}: {exc}") from exc


def resolve(base: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (base / path)


def hash_paths(base: Path, paths: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for raw in paths:
        path = resolve(base, raw)
        if not path.exists():
            raise GateError(f"code path does not exist: {raw}")
        if path.is_file():
            hashes[str(path)] = sha256_file(path)
            continue
        for child in sorted(path.rglob("*")):
            if child.is_file() and "__pycache__" not in child.parts and child.suffix != ".pyc":
                hashes[str(child)] = sha256_file(child)
    if not hashes:
        raise GateError("no files hashed from code_paths")
    return hashes


def validate_manifest(manifest: Any, round_dir: Path) -> list[str]:
    if not isinstance(manifest, dict):
        return ["round_manifest.json must contain a JSON object"]

    reasons: list[str] = []
    required = {
        "round_id": str,
        "type": str,
        "objective": str,
        "owner": str,
        "created_at": str,
        "code_paths": list,
        "debug_commands": list,
        "experiment_command": str,
        "budget": dict,
        "preregistration": (str, type(None)),
        "expected_outputs": list,
    }
    for key, expected in required.items():
        if key not in manifest:
            reasons.append(f"manifest missing key: {key}")
        elif not isinstance(manifest[key], expected):
            reasons.append(f"manifest key {key} has wrong type")

    if manifest.get("type") not in ALLOWED_TYPES:
        reasons.append(f"manifest type must be one of {sorted(ALLOWED_TYPES)}")
    for key in ("round_id", "objective", "owner", "experiment_command"):
        value = manifest.get(key)
        if isinstance(value, str) and not value.strip():
            reasons.append(f"manifest key {key} must not be empty")
    for key in ("code_paths", "debug_commands", "expected_outputs"):
        value = manifest.get(key)
        if isinstance(value, list) and not any(isinstance(item, str) and item.strip() for item in value):
            reasons.append(f"manifest key {key} must contain at least one non-empty string")

    budget = manifest.get("budget")
    if isinstance(budget, dict):
        for key in ("max_minutes", "max_gpu_hours"):
            value = budget.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                reasons.append(f"budget.{key} must be a number")
            elif key == "max_minutes" and value <= 0:
                reasons.append("budget.max_minutes must be > 0")
            elif key == "max_gpu_hours" and value < 0:
                reasons.append("budget.max_gpu_hours must be >= 0")

    if manifest.get("type") == "confirmatory":
        preregistration = manifest.get("preregistration")
        if not isinstance(preregistration, str) or not preregistration.strip():
            reasons.append("confirmatory round requires a preregistration path")
        elif not resolve(round_dir, preregistration).exists():
            reasons.append(f"preregistration file does not exist: {preregistration}")

    return reasons


def validate_debug(round_dir: Path) -> tuple[list[str], dict[str, str]]:
    reasons: list[str] = []
    evidence: dict[str, str] = {}
    result_path = round_dir / "debug" / "debug_result.json"
    report_path = round_dir / "debug" / "debug_report.md"

    if not result_path.exists():
        reasons.append("missing debug/debug_result.json")
    else:
        evidence["debug_result_sha256"] = sha256_file(result_path)
        try:
            debug_result = load_json(result_path)
        except GateError as exc:
            reasons.append(str(exc))
            debug_result = None
        if isinstance(debug_result, dict):
            if debug_result.get("status") != "pass":
                reasons.append("debug_result.status must be 'pass'")
            checks = debug_result.get("checks")
            if not isinstance(checks, list) or len(checks) < MIN_DEBUG_CHECKS:
                reasons.append(f"debug_result.checks must contain at least {MIN_DEBUG_CHECKS} entries")
            else:
                bad = [
                    str(check.get("name", f"check[{index}]"))
                    for index, check in enumerate(checks)
                    if not isinstance(check, dict) or check.get("status") != "pass"
                ]
                if bad:
                    reasons.append("debug checks not passing: " + ", ".join(bad))
        elif debug_result is not None:
            reasons.append("debug_result.json must contain a JSON object")

    if not report_path.exists():
        reasons.append("missing debug/debug_report.md")
    else:
        evidence["debug_report_sha256"] = sha256_file(report_path)
        text = report_path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
        if missing:
            reasons.append("debug_report.md missing sections: " + ", ".join(missing))

    return reasons, evidence


def write_gate_result(round_dir: Path, result: dict[str, Any]) -> None:
    path = round_dir / "GATE_RESULT.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_round(round_dir: Path) -> dict[str, Any]:
    round_dir = round_dir.resolve()
    if not round_dir.is_dir():
        raise GateError(f"round directory does not exist: {round_dir}")

    result: dict[str, Any] = {
        "round_id": round_dir.name,
        "type": None,
        "status": "blocked",
        "checked_at": now_iso(),
        "blocking_reasons": [],
        "evidence": {},
    }

    try:
        manifest = load_json(round_dir / "round_manifest.json")
    except GateError as exc:
        result["blocking_reasons"].append(str(exc))
        write_gate_result(round_dir, result)
        return result

    if isinstance(manifest, dict):
        result["round_id"] = manifest.get("round_id", round_dir.name)
        result["type"] = manifest.get("type")

    reasons = validate_manifest(manifest, round_dir)
    if not reasons:
        try:
            result["code_hashes"] = hash_paths(round_dir, manifest["code_paths"])
        except GateError as exc:
            reasons.append(str(exc))

    debug_reasons, debug_evidence = validate_debug(round_dir)
    reasons.extend(debug_reasons)
    result["evidence"].update(debug_evidence)
    result["blocking_reasons"] = reasons
    if not reasons:
        result["status"] = "pass"

    write_gate_result(round_dir, result)
    return result


def init_round(round_dir: Path, force: bool = False) -> None:
    round_dir = round_dir.resolve()
    manifest_path = round_dir / "round_manifest.json"
    if manifest_path.exists() and not force:
        raise GateError(f"round already initialized: {manifest_path} (use --force to overwrite)")

    (round_dir / "debug" / "logs").mkdir(parents=True, exist_ok=True)
    (round_dir / "experiment" / "outputs").mkdir(parents=True, exist_ok=True)

    manifest = load_json(TEMPLATES / "round_manifest.json")
    if not isinstance(manifest, dict):
        raise GateError("round_manifest template is not a JSON object")
    manifest["round_id"] = round_dir.name
    manifest["created_at"] = now_iso()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for source, destination in (
        (TEMPLATES / "debug_report.md", round_dir / "debug" / "debug_report.md"),
        (TEMPLATES / "experiment_log.md", round_dir / "experiment_log.md"),
    ):
        shutil.copyfile(source, destination)
        destination.write_text(
            destination.read_text(encoding="utf-8").replace("<ROUND_ID>", round_dir.name),
            encoding="utf-8",
        )

    print(f"initialized round: {round_dir}")
    print("next: fill round_manifest.json, run debug checks, then rerun with --round")


def print_report(result: dict[str, Any]) -> None:
    print(f"round: {result['round_id']}  type: {result['type']}  status: {result['status']}")
    if result["status"] == "pass":
        print(f"code files hashed: {len(result.get('code_hashes', {}))}")
        print(f"gate result: {result.get('gate_result_path', 'GATE_RESULT.json')}")
        return
    print("blocked by:")
    for reason in result["blocking_reasons"]:
        print(f"  - {reason}")
    print("fix the items above, then rerun; do not start the experiment.")


def selftest() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        round_dir = Path(temporary) / "runs" / "R-TEST"
        init_round(round_dir)
        (round_dir / "code.py").write_text("print('ok')\n", encoding="utf-8")

        manifest_path = round_dir / "round_manifest.json"
        manifest = load_json(manifest_path)
        manifest.update(
            {
                "code_paths": ["code.py"],
                "debug_commands": ["python3 -m compileall code.py"],
                "experiment_command": "python3 code.py",
                "expected_outputs": ["outputs/metrics.json"],
                "budget": {"max_minutes": 1, "max_gpu_hours": 0},
            }
        )
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        debug_result = {
            "status": "pass",
            "timestamp": now_iso(),
            "checks": [
                {"name": "D1 syntax", "status": "pass", "evidence": "compileall OK"},
                {"name": "D2 tests", "status": "pass", "evidence": "selftest OK"},
                {"name": "D3 contract", "status": "pass", "evidence": "schema OK"},
                {"name": "D4 smoke", "status": "pass", "evidence": "1 sample OK"},
            ],
            "residual_risks": [],
        }
        debug_path = round_dir / "debug" / "debug_result.json"
        debug_path.write_text(json.dumps(debug_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        passed = check_round(round_dir)
        if passed["status"] != "pass":
            raise GateError(f"selftest expected pass, got: {passed['blocking_reasons']}")

        debug_result["status"] = "fail"
        debug_path.write_text(json.dumps(debug_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        blocked = check_round(round_dir)
        if blocked["status"] != "blocked":
            raise GateError("selftest expected blocked after debug status changed to fail")

        print("SELFTEST PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Round gate for the M2A-BRIDGE workspace")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", metavar="ROUND_DIR", help="create a round directory from templates")
    group.add_argument("--round", metavar="ROUND_DIR", help="check a round before running its experiment")
    group.add_argument("--selftest", action="store_true", help="run the built-in gate selftest")
    parser.add_argument("--force", action="store_true", help="overwrite an existing manifest with --init")
    args = parser.parse_args(argv)

    try:
        if args.selftest:
            selftest()
            return 0
        if args.init:
            init_round(Path(args.init), force=args.force)
            return 0
        result = check_round(Path(args.round))
        print_report(result)
        return 0 if result["status"] == "pass" else 2
    except GateError as exc:
        print(f"GATE ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
