# Cross-review synthesis — Track C

- Date: 2026-10-27
- Input: three mutually blind reviewer reports (R1 technical, R2 originality, R3 significance/reproducibility), plus the forensic audit.
- Status: major revision. The current manuscript is not submission-ready.

## Consensus blocking concerns

| Issue | Reviewers | Evidence | What must change |
| --- | --- | --- | --- |
| "Motor copy" is an undelayed visual signal, confounded with filter lag | R1-M3, R2-M1, R3-M2 | `ec_model.py` `f_bar_motor` from current visual state; `f_bar` is the filtered applied torque | Drop or relabel the "source" claim. Use "filtered vs unfiltered bar-pathway signal" or implement a true motor command and matching filter. |
| 2.5 s window truncates late failures | R1-M1, R2-M2 | `P1-EC-WINDOW-01`: allnone at 140 ms 3/16 (2.5 s), 11/16 (6 s), 12/16 (10 s); allnone_motor 12/16 at all windows | Replace absolute gating robustness claims with window-aware statements. Report failure times and window sensitivity. |
| V-term clip is active in the failure regime | R1-M4 | `P1-EC-VCLIP-01`: at 100 ms, allnone 0% (clip), 75% (smooth), 0% (unclipped); allnone_motor 6.2%, 75%, 6.2% | Do not claim a 100 ms gating advantage. Restrict gating claims to delays where the ordering survives all V modes. |
| Adaptive MLP update is monotone, not gradient descent | R1-M2, R2-M3, R3-M1 | `adaptive_model.py` `do = error*error`, all updates positive; `ro` hits the 2.0 clip | Implement a proper signed-error gradient or reproduce the source update exactly; rerun. Otherwise remove the adaptive headline. |
| Absolute gating robustness is overstated | R1-M1, R2-M5, R3-M5 | `threshold_sensitivity.json`; `P1-EC-WINDOW-01`; `P1-EC-VCLIP-01` | State that gating buys time at short delays, not asymptotic stability. Qualify 100 ms and 200 ms claims by window, criterion, and V mode. |
| Linear stability analysis is unreliable | R1-M5, R2-M8, R3-M3 | `linear_stability.json`: graded_motor 300 ms is censoring, not a crossing; root jumps; opposite ordering at gain 1.0 | Remove Fig. 6 and the linear section, or replace with a validated delay-eigenvalue solver. |
| Source-protocol check is degenerate | R1-M6, R2-M4, R3-M4 | Near-zero gate threshold makes allnone the no-grating model; at the main threshold allnone is not invariant; constant grating, not sparse/dense | Stop claiming the source ranking is "recovered." State it is not reproduced at a meaningful effect size; treat the source result as motivation, not validation. |
| Reproducibility package does not reproduce the manuscript | R3-M9 | P1 snapshot has 4 models, current runner has 5; gain/adaptive runs lack snapshots; requirements lack scipy; PDF stale; hardcoded paths | Freeze per-round code, fix requirements and relative paths, rebuild PDF, archive with DOI. |

## Consensus major concerns (non-blocking but required)

- Gate threshold is unswept in the main regime (R1-M1, R2-M5, R3-M5). Run a threshold sweep and report the range where the short-delay ordering holds.
- Gating has no EC gain parameter, so "gain-invariant" is definitional (R1-m7, R2-m7, R3-M6). State this explicitly or sweep a gate parameter.
- The failure curves are nonmonotonic in delay; explain or use a survival metric (R1-M1, R3-m6).
- The V-term clip, filter asymmetry, and `tau_bar` need sensitivity checks (R1-M3, R1-M4, R2-m10, R3-M11).
- Prior art on forward models, Smith predictors, delay-tolerant control, and Drosophila efference-copy physiology is missing (R2-M6, R3-m12).
- Predictions are qualitative; make them operational (R3-M8).
- Figures do not show the five variants, gate state, or graded_motor's long-delay benefit (R1-M7, R2-m1, R3-M7).
- References are inconsistent; one in-text citation has no entry; several entries are uncited (R1-m15, R2-m6, R3-m1).
- Discussion and Limitations contradict the adaptive section (R1-m14, R2-m4, R3-M10).
- The delay applies to heading and omega, not only visual variables (R1-m6). State and justify or control.
- Linearization is around a moving target and omits `dtheta_bar` forcing (R1-m13).
- The failure criterion uses "and" in text but "or" in code (R1-m1, R2-m3).
- Coarse medians are interpolated between grid points and censored (R1-m11, R1-m2).

## Forensic audit

- AUD-01 confirmed internal error: "25-33% (3-4/12)" should be "25-42% (3-5/12)". Corrected in the manuscript and supporting files. Reviewer overlap: R1-m2, R2-m2, R3-m4.
- All simulation counts and headline medians otherwise reconcile with the archived summaries.
- The PDF was stale at the time of review (25-33%); rebuild after revisions.

## What survives the review

1. **Gain sweep.** At the source's fixed gain 0.05, fixed-gain graded cancellation is inert. At gains of 0.25 or more, delayed sensory cancellation is harmful at 50 ms. This result is robust across the coarse parameter grid and is the strongest contribution.
2. **Short-delay gating.** At delays of 20-50 ms, gating is 0% failure across 2.5/6/10 s windows and clip/smooth/unclipped V. Continuous models fail 62.5-100%. This is the defensible gating claim.
3. **Long-delay gating claim does not survive.** At 100 ms, the gating advantage is V-mode-dependent; at 140 ms and beyond, it disappears or shrinks to a few runs.
4. **The adaptive and linear-stability headlines do not survive in their current form.** They must be fixed or removed.

## What must be removed or reframed

- The title's "gain and source" should become "gain and gating" or "gain, delay, and gating." The "source" half is confounded.
- The "gating is most robust through 100 ms" claim must become "gating prevents failure at delays up to about 50 ms; at 100 ms the advantage depends on the V-term treatment; at 140 ms and beyond it is not established."
- The "200 ms critical delay" is a 2.5 s window artifact. Remove it.
- The adaptive MLP section must be downgraded to a step-wise approximation caveat or replaced by a proper-gradient experiment.
- Fig. 6 and the linear section should be removed unless a validated delay-eigenvalue solver is added.
- The source-protocol "recoverable" sentence must be replaced by "not reproduced at a meaningful effect size; motivation only."

## Revision plan (experiments first, then prose)

1. **Gate-threshold sweep** in the main regime, at 6 s, clip and smooth V, delays 20-140 ms. Determine the threshold range where the short-delay gating ordering holds.
2. **Proper-gradient adaptive check** with signed error; compare to the source-style monotone update. If the gain can decrease and the failure ordering changes, rewrite the adaptive section.
3. **Motor-signal control** with a filtered current copy and a delayed unfiltered copy; if the "source" distinction collapses, drop it.
4. **Robust linear stability** or removal. Default plan: remove Fig. 6 and the linear section, state that the nonlinear analysis is primary.
5. **Reproducibility fixes**: per-round snapshots, scipy in requirements, relative paths, PDF rebuild, reference reconciliation.
6. **Manuscript rewrite** around the surviving claims: gain sweep + short-delay gating + window/V-mode limitations.

## Post-review experiments completed (2026-10-27)

| Experiment | Result | Consequence |
| --- | --- | --- |
| Window check (`P1-EC-WINDOW-01`) | allnone at 140 ms: 3/16 at 2.5 s, 11/16 at 6 s, 12/16 at 10 s; allnone_motor 12/16 at all windows | Long-delay gating claim removed. |
| V-clip check (`P1-EC-VCLIP-01`) | At 20/50 ms, failure rates identical across clip/smooth/unclipped and gating 0%. At 100 ms, allnone 0% clip, 75% smooth, 0% unclipped | Short-delay gating retained; 100 ms advantage removed. |
| Gate-threshold check (`P1-EC-GATE-01`) | At 20/50 ms, gating 0% across thresholds 0.01-0.5 and clip/smooth. At 100 ms, clip 0% below 0.5, smooth 75%; at 140 ms 75% | Short-delay gating retained; threshold range stated. |
| Adaptive gradient (`P1-EC-ADAPTIVE-03`) | Source-style mean gain 0.51 to 1.05; signed gradient 0.22 to 0.40; failure 50% at 20 ms and 100% at 50/100/200 ms in all modes | Adaptive claim rewritten; signed gradient does not rescue. |
| Command copy (`P1-EC-COMMAND-01`) | Graded command matches graded filtered (87.5% at 20 ms, 100% at 50-200 ms); gate command matches gate filtered (0% at 20-100 ms, 75% at 140-200 ms); only the current-visual oracle has lower long-delay failure | The apparent motor-copy benefit was an oracle effect; source question closes for this architecture. |
| Source check | Zero-delay ranking not reproduced; main-threshold gate ~4% sensitive; graded at gain 0.5 ~0.3% sensitive; addition 15% | Source result demoted to motivation; "source" claim removed. |
| Linear stability | Root tracking unreliable; 300 ms was censoring, not a crossing | Fig. 6 and the linear section removed. |

## Revised manuscript

- `MANUSCRIPT_REVISED.md` and `MANUSCRIPT_REVISED.pdf` (11 pages, 6 figures).
- Title: "Efference-copy gain and short-delay gating in a delayed fly steering model."
- Retained claims: gain sweep, short-delay gating, window/V-mode/threshold limitations, signed-gradient adaptive negative result, command-copy negative result.
- Removed claims: source/motor-copy distinction, gating robust through 100/200 ms, linear stability.
- Remaining experiments: a goal-based feedforward command; full ODE-internal MLP.

## Recommendation

Major revision is complete in the revised draft. The paper is now a narrower, defensible PLOS Computational Biology modeling paper. It is not a Nature-level contribution. The true command-copy experiment is complete and negative, so the next scientific step is a goal-based feedforward command, not more analysis of the current variants.
