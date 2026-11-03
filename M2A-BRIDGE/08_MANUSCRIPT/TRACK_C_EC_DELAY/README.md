# Track C — EC delay computational manuscript

> Status: draft, 2026-10-27. Not submitted. B0 computational study; no new biological data.
> Target: PLOS Computational Biology (realistic); eLife / Nature Communications only if the model is strengthened with connectome-constrained vision or biological data.

## Files

| File | Content |
| --- | --- |
| `MANUSCRIPT_REVISED.md` | Revised manuscript: abstract, introduction, results, discussion, methods, limitations, references, figure legends |
| `MANUSCRIPT_REVISED.pdf` | Built PDF (18 pages, fourteen figures) |
| `FIGURE_CONTRACTS.md` | Figure sources, formatting, caption requirements |
| `fig1_model.png` | Model schematic |
| `fig2c_gain_delay_heatmap.png` | Gain × delay failure heatmap |
| `fig_window_check.png` | Window dependence |
| `fig_stress.png` | V-term and gate-threshold stress |
| `fig_adaptive_gradient.png` | Adaptive updates |
| `fig_command_copy.png` | Command copy vs filtered plant state vs oracle |
| `fig_feedforward.png` | Goal feedforward, self-state ablation, goal-delay control |
| `fig_mechanism.png` | Mechanism schematic (command copy / feedforward / delayed self-state) |
| `fig_delay_limits.png` | Fine grid 0-250 ms and long delays 200-500 ms |
| `fig_noise.png` | Noise robustness 0 to 1e-11 |
| `fig_phase.png` | Body-parameter phase diagram |
| `fig_trajectories.png` | Example trajectories and gate state at 200 ms |
| `fig_survival.png` | Failure-free curves at 140 ms |
| `fig_selfstate.png` | Freshness dose-response, onset decoupling, damping control |
| `REVIEW_ROUND2_*.md` / `FORENSIC_AUDIT_ROUND2.md` / `REVIEW_ROUND2_SYNTHESIS.md` | Second review round: three blind reports, audit, synthesis |
| `CLAIM_TO_EVIDENCE_MAP.csv` | 36 rows (7 retired pre-revision), status column |
| `make_fig*.py` | Figure scripts |

## Reproduce

```bash
cd M2A-BRIDGE/06_JOINT
../.venv/bin/python -m pytest -q test_ec_model.py
../.venv/bin/python run_delay_sweep.py --output-dir ../../runs/P1-EC-DELAY-01/experiment/outputs
../.venv/bin/python run_robustness.py --output-dir ../../runs/P1-EC-DELAY-02/experiment/outputs
../.venv/bin/python run_fine_grid.py --output-dir ../../runs/P1-EC-DELAY-03/experiment/outputs
```

## Core claim

The revised manuscript reports three results that survive window, V-mode, gate-threshold, and adaptive-update stress tests. First, gain: at the source model's fixed gain 0.05, fixed-gain graded cancellation is inert, indistinguishable from no efference copy; at gains of 0.25 or more, delayed-sensory cancellation is harmful at 50 ms (100% vs 75% failure). Second, gating: at delays of 20 to 50 ms, gating prevents failure across gate thresholds from 0.01 to 0.5 and across clip, smooth, and unclipped V treatments, while continuous models fail in 62.5% to 100% of parameter sets. The advantage is not asymptotic; at 100 ms it depends on the V treatment, and at 140 ms or longer it is not established. Third, adaptation: neither the source-style squared-error update nor a signed-gradient update rescues failure at 50 ms, and an ODE-internal reimplementation of the weight update agrees with the step-wise form in 96/96 failure classifications. Fourth, source: a pre-plant-filter command copy does not rescue delay, matching the filtered plant state; only the current-visual oracle has lower long-delay failure, so the earlier benefit was an oracle effect. Fifth, a goal feedforward branch that uses current proprioception does rescue: gate goal at ff_gain >= 0.5 fails in no parameter set through 200 ms at 6 and 10 s windows, robust to goal mismatch, and the rescue disappears when that branch's self-state estimate is delayed.

## What this paper is not

- Not a claim that the fly uses all-or-none gating.
- Not a connectome-constrained model.
- Not a Nature flagship submission.
- Not a substitute for the M2A-BRIDGE biological experiment.

## Next steps before submission

1. The revised manuscript is `MANUSCRIPT_REVISED.md`, with an 18-page PDF at `MANUSCRIPT_REVISED.pdf`.
2. The command-copy and feedforward experiments are complete, including window, goal-mismatch, goal-delay, self-state, multi-seed, and ODE-equivalence controls.
3. The remaining scientific step is an experimental test of the proposition that stabilization under visual delay depends on pathways carrying current self-state or a goal, not on an efference copy alone. The source's exact adaptive solver semantics remain unreproduced but were shown equivalent under forward Euler.
4. Author/affiliation/competing-interest statements and the preprint decision are owner-side.
5. The source's zero-delay ranking is not reproduced; the manuscript states this explicitly.
