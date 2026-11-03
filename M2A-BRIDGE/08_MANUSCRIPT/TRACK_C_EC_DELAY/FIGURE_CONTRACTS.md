# Figure contracts — Track C

| Figure | Content | Data source | Script | Status |
| --- | --- | --- | --- | --- |
| Fig 1 | Model schematic: visual scene → delay → bar/grating pathways → body → heading; graded EC and all-or-none boxes | none | `make_fig1.py` | draft |
| Fig 2 | Failure rate vs feedback delay for four models (P1 sweep) | `runs/P1-EC-DELAY-01/experiment/outputs/summary.json` | `make_fig2.py` | draft |
| Fig 2b | Critical delays at 1 ms resolution, five models, three parameter sets | `runs/P1-EC-DELAY-03/experiment/outputs/summary.json` | `make_fig2b.py` | draft |
| Fig 2c | EC gain × delay failure heatmap for graded_sensory, allnone, allnone_motor | `runs/P1-EC-GAIN-01/experiment/outputs/summary.json` | `make_fig2c.py` | draft |
| Fig 2d | Adaptive MLP vs fixed gains: failure rate and learned gain vs delay | `runs/P1-EC-ADAPTIVE-01/experiment/outputs/summary.json` | `make_fig2d.py` | draft |
| Fig 2e | Adaptive MLP across learning rates and seeds | `runs/P1-EC-ADAPTIVE-02/experiment/outputs/summary.json` | `make_fig2e.py` | draft |
| Fig 3 | Phase diagram: body time constant × delay, graded_sensory and allnone (P2 sweep) | `runs/P1-EC-DELAY-02/experiment/outputs/sweep_noise.csv` | `make_fig3.py` | draft |
| Fig 4 | Example heading trajectories at 140 ms, five variants, noise | P2 simulation | `make_fig4.py` | draft |
| Fig 5 | Failure rate vs delay, allnone vs allnone_motor | `runs/P1-EC-DELAY-02/experiment/outputs/summary.json` | `make_fig5.py` | archived |
| Fig 6 (old) | Linear stability: rightmost eigenvalue vs delay | `M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/linear_stability.json` | `make_fig6.py` | archived |
| Fig 5 (revised) | Adaptive updates: failure rate and learned gain | `runs/P1-EC-ADAPTIVE-03/experiment/outputs/summary.json` | `make_fig_adaptive_gradient.py` | final |
| Fig 6 (revised) | Command copy vs filtered plant state vs current-visual oracle; gate duty | `runs/P1-EC-COMMAND-01/experiment/outputs/summary.json` | `make_fig_command.py` | final |
| Fig 7 | Goal feedforward across ff gains; self-state ablation; goal-delay control | `runs/P1-EC-FEEDFORWARD-01`, `P1-EC-FF-STATE-01`, `P1-EC-GOAL-DELAY-01` summaries | `make_fig_feedforward.py` | final |

## Formatting

- PNG, 200–220 dpi for review; final submission should be vector (PDF/SVG) where possible.
- Axis labels in sentence case; no title inside panels except phase-diagram model names.
- Color: current default matplotlib palette; switch to a colorblind-safe palette before submission.
- Each legend states n, unit, and failure definition.
- No p values; the study is a parametric simulation, not a hypothesis test.

## Caption requirements

- Fig 2: state 12 parameter sets, 16 delays, failure definition, and that no biological data are used.
- Fig 3: state four body time constants, two grating gains, two seeds, noise SD, and failure definition.
- Fig 4: state the parameter set and seed; note that boundedness is not correctness.
- Fig 5: state that allnone and allnone_motor differ only in the gating signal.
