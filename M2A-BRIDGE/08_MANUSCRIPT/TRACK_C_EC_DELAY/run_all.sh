#!/usr/bin/env bash
set -euo pipefail

# Resolve the workspace root from this script's location.
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PY="$ROOT/M2A-BRIDGE/.venv/bin/python"
JOINT="$ROOT/M2A-BRIDGE/06_JOINT"

# Frozen P1, P2, P3 snapshots reproduce the archived row counts.
cd "$ROOT/runs/P1-EC-DELAY-01/code_snapshot"
"$PY" -m pytest -q test_ec_model.py
"$PY" run_delay_sweep.py --output-dir "$ROOT/runs/P1-EC-DELAY-01/experiment/outputs"

cd "$ROOT/runs/P1-EC-DELAY-02/code_snapshot"
"$PY" run_robustness.py --output-dir "$ROOT/runs/P1-EC-DELAY-02/experiment/outputs"

cd "$ROOT/runs/P1-EC-DELAY-03/code_snapshot"
"$PY" run_fine_grid.py --output-dir "$ROOT/runs/P1-EC-DELAY-03/experiment/outputs"

# Current-code rounds.
cd "$JOINT"
"$PY" run_gain_sweep.py --output-dir "$ROOT/runs/P1-EC-GAIN-01/experiment/outputs"
"$PY" run_gain_robustness.py --output-dir "$ROOT/runs/P1-EC-GAIN-02/experiment/outputs"
"$PY" run_adaptive_check.py --output-dir "$ROOT/runs/P1-EC-ADAPTIVE-01/experiment/outputs"
"$PY" run_adaptive_robustness.py --output-dir "$ROOT/runs/P1-EC-ADAPTIVE-02/experiment/outputs"
"$PY" run_adaptive_gradient.py --output-dir "$ROOT/runs/P1-EC-ADAPTIVE-03/experiment/outputs"
"$PY" run_window_check.py --output-dir "$ROOT/runs/P1-EC-WINDOW-01/experiment/outputs"
"$PY" run_vclip_check.py --output-dir "$ROOT/runs/P1-EC-VCLIP-01/experiment/outputs"
"$PY" run_gate_threshold.py --output-dir "$ROOT/runs/P1-EC-GATE-01/experiment/outputs"
"$PY" run_command_copy.py --output-dir "$ROOT/runs/P1-EC-COMMAND-01/experiment/outputs"
"$PY" run_feedforward.py --output-dir "$ROOT/runs/P1-EC-FEEDFORWARD-01/experiment/outputs"
"$PY" run_feedforward_window.py --output-dir "$ROOT/runs/P1-EC-FEEDFORWARD-02/experiment/outputs"
"$PY" run_goal_mismatch.py --output-dir "$ROOT/runs/P1-EC-GOAL-MISMATCH-01/experiment/outputs"
"$PY" run_goal_delay.py --output-dir "$ROOT/runs/P1-EC-GOAL-DELAY-01/experiment/outputs"
"$PY" run_ff_state.py --output-dir "$ROOT/runs/P1-EC-FF-STATE-01/experiment/outputs"
"$PY" run_multiseed.py --output-dir "$ROOT/runs/P1-EC-MULTISEED-01/experiment/outputs"
"$PY" run_adaptive_ode.py --output-dir "$ROOT/runs/P1-EC-ADAPTIVE-ODE-01/experiment/outputs"
"$PY" run_longdelay.py --output-dir "$ROOT/runs/P1-EC-LONGDELAY-01/experiment/outputs"
"$PY" run_fine_delay.py --output-dir "$ROOT/runs/P1-EC-FINEDELAY-01/experiment/outputs"
"$PY" run_noise.py --output-dir "$ROOT/runs/P1-EC-NOISE-01/experiment/outputs"
"$PY" run_phase.py --output-dir "$ROOT/runs/P1-EC-PHASE-01/experiment/outputs"
"$PY" run_trajectories.py --output-dir "$ROOT/runs/P1-EC-TRAJ-01/experiment/outputs"
"$PY" run_onset.py --output-dir "$ROOT/runs/P1-EC-ONSET-01/experiment/outputs"
"$PY" run_damping.py --output-dir "$ROOT/runs/P1-EC-DAMP-01/experiment/outputs"
"$PY" run_selfstate_lag.py --output-dir "$ROOT/runs/P1-EC-SELFSTATE-01/experiment/outputs"
"$PY" source_protocol_check.py

# Revised-paper analyses and figures.
cd "$ROOT/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY"
"$PY" analyze_thresholds.py
"$PY" solver_check.py
"$PY" make_fig1.py
"$PY" make_fig2c.py
"$PY" make_fig_window.py
"$PY" make_fig_stress.py
"$PY" make_fig_adaptive_gradient.py
"$PY" make_fig_command.py
"$PY" make_fig_feedforward.py
"$PY" make_fig_delay_limits.py
"$PY" make_fig_noise.py
"$PY" make_fig_phase.py
"$PY" make_fig_trajectories.py
"$PY" make_fig_survival.py
"$PY" make_fig_mechanism.py
"$PY" make_fig_selfstate.py

pandoc MANUSCRIPT_REVISED.md -f markdown-implicit_figures -o MANUSCRIPT_REVISED.pdf \
  --pdf-engine=xelatex --toc \
  -V geometry:margin=0.9in -V fontsize=10pt \
  -V mainfont="Times New Roman" -V monofont="Menlo"
