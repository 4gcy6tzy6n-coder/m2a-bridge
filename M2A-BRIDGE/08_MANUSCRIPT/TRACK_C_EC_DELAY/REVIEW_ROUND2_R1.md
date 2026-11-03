# Review Round 2 — Reviewer 1

Manuscript: `M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md`
Journal target: PLOS Computational Biology, Research Article.
Scope of this review: internal consistency and evidence grounding for a B0 computational study with no new biological data.

## Overall assessment

This is a careful and largely well-executed computational stress-test study whose central results (gain dependence, short-delay gating, adaptation failure, command-copy null, goal-feedforward rescue via current self-state) I was able to verify against the run summaries it cites. However, several quantitative statements in the Abstract and Results are contradicted by the very runs they cite, and the claim-to-evidence map shipped with the packet still documents the pre-revision manuscript, including two claims (C2, C3) that the revised paper explicitly retracts. The arithmetic of run counts, percentages over n=8 and n=12 grids, figure legends, and Methods constants is otherwise sound, and the corrections culture of the paper is a genuine strength. I recommend major revision, driven by factual corrections rather than by any flaw in the core argument.

## Who would be interested in the results, and why

Computational neuroscientists and control theorists working on sensorimotor delay, efference copy, and gating will find the main result directly relevant, namely that efference-copy gain and short-delay gating are the robust variables while long-delay advantages dissolve under longer windows and a smooth velocity nonlinearity. Drosophila vision and flight-steering researchers will care about the testable predictions about imposed visual delay and proprioceptive pathways, and about the explicit boundary that no claim is made about the fly's mechanism. Researchers interested in simulation methodology will value the paper's demonstration that a finite window and a saturation clip can manufacture a stability advantage, plus the transparent reporting of retracted claims.

## Major strengths

- Nearly every quantitative claim I checked reconciles exactly with the cited `summary.json` artifacts. This includes the gain sweep (1,440 rows; 100% vs 75% at 50 ms; 42% to 50% at 20 ms), the window check (0/16, 18.8%, 68.8%, 75% sequences), the V-treatment numbers at 100 ms (0/75/0 and 6.2/75/6.2), the adaptive gain ranges (0.51 to 1.05, 0.22 to 0.40, 0.11 to 0.38), the command-copy rates and duty cycles, the feedforward grid (0% for ff at or above 0.5 everywhere; partial gate at ff=0.25 of 0/0/25/25/37.5), the goal-mismatch and goal-delay controls, and the self-state ablation.
- All Methods run counts reconcile with the artifact row counts (1,440 / 1,200 / 1,200 / 1,024 / 144 / 560 / 600 / 400 / 648 / 256 / 96 / 960 / 96 pairs), and the failure criterion in code (|heading| > 2 pi, |omega| > 100, non-finite) matches the Methods text in every runner script checked.
- The paper reports its own corrections prominently rather than burying them, and the window-artifact and V-clip corrections are themselves among its most valuable contributions.
- Scope discipline is excellent. The Limitations and Scope note repeatedly deny any mechanistic claim about the fly, disclose the stylized reimplementation and the failure of the zero-delay replication, and mark the goal feedforward as an upper bound.
- The zero-delay ranking ratios (0.9148, 0.9830, 0.9996, 0.9998) and the source-protocol numbers (59.956 vs 59.956, 59.890 vs 57.422, 59.923 vs 59.770, 59.846 vs 50.846) trace exactly to `runs/P1-EC-DELAY-01/experiment/outputs/sweep.csv` and `source_protocol_check.json`.
- Controls are well designed: multi-seed re-runs, ODE-internal weight updates, goal-delay and self-state ablations, and a stated negative result for adaptation.

## Major Concerns

### R1-M1 — The gate-threshold robustness claim is contradicted by the cited run
- Severity: High
- Blocking: No
- Axis: technical soundness
- Claim pointer: Abstract, "gating prevents failure (0%) across gate thresholds from 0.01 to 0.5 of the bar-torque scale"; Results, "At 20 and 50 ms, gating remained at 0% across every threshold and both the clip and smooth V treatments"; Discussion, "The advantage survives gate thresholds from 0.01 to 0.5"
- Evidence pointer: `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-GATE-01/experiment/outputs/summary.json`
- Concern: In the cited sweep, `allnone_motor` (gate unfiltered) at threshold ratio 0.5, delay 0.05 s, clip V has failure rate 0.25 (4 of 16 runs). Every other short-delay cell is 0. The blanket statement "gating ... 0% across every threshold" is therefore false for one of the two gating variants, and Figure 4 (middle and right panels, drawn only from `grid["allnone"]` per `make_fig_stress.py`) does not display the failing cell, so the reader cannot see it.
- Why it matters: This is a headline stress-test claim in the Abstract. An overclaim here weakens trust in the paper's central narrowing message, which is otherwise that the authors are unusually careful about what their grids do and do not show.
- Resolution test: Restate the claim per variant (gate filtered 0% at all four thresholds; gate unfiltered 0% except 25% at threshold 0.5, 50 ms, clip), or re-run that single condition at the main step size dt = 1e-4 (the threshold sweep used dt = 2e-4, disclosed in Methods) and report the result either way. Update Abstract, Results, Discussion, and the Figure 4 legend to match.

### R1-M2 — The claim-to-evidence map documents the old draft and contradicts the revised manuscript
- Severity: High
- Blocking: No
- Axis: technical soundness
- Claim pointer: packet artifact `CLAIM_TO_EVIDENCE_MAP.csv`, rows C2 and C3, quote, "All-or-none gating remains stable to a median critical delay of 0.20 s ... (19% failure at 140 ms)" and "gating on the delayed sensory estimate is more stable than gating on the current motor copy (0.20 s vs 0.11 s; 19% vs 75% failure at 140 ms) ... Fig5"
- Evidence pointer: `/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/CLAIM_TO_EVIDENCE_MAP.csv` (rows exist and correctly describe `runs/P1-EC-DELAY-02`, but that is the claim the revised paper retracts); `/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md` ("We no longer report a 200 ms critical delay for gating")
- Concern: The map is stale relative to the revised manuscript in several ways. C2 and C3 assert the exact median-critical-delay claims that the revised Results section retracts as finite-window artifacts, and C3's figure pointer "Fig5" now denotes the adaptive figure. C7 and C8 point to `MANUSCRIPT_DRAFT.md` rather than the revised file. C9, C15, C16 cite Figure 2b, 2d, 2e, which no longer exist in the revised figure set. C10, C11, C16 make claims absent from the revised text. Conversely, major revised claims have no rows at all: the window-artifact correction, the V-term stress results, the gate-threshold stress results, the three-rule adaptive comparison (the revised numbers 0.51 to 1.05 and 0.22 to 0.40 come from `runs/P1-EC-ADAPTIVE-03`, which no row cites; C15 cites `P1-EC-ADAPTIVE-01` numbers 0.38 to 1.06 that appear nowhere in the revised text), and the goal-mismatch grid.
- Why it matters: The map is the audit trail tying claims to artifacts. If it survives into submission in this state, any editor or reviewer who opens it will find it contradicting the manuscript's central corrections.
- Resolution test: Regenerate the map from the revised manuscript, one row per quantitative claim, retire or relabel C1, C2, C3, C9, C15, C16, add rows for the window, V, threshold, adaptive-three-rule, and goal-mismatch results, and repoint C7, C8 to `MANUSCRIPT_REVISED.md`.

### R1-M3 — "The continuous models failed in 100% of runs at 100 ms" is false for graded unfiltered
- Severity: High
- Blocking: No
- Axis: technical soundness
- Claim pointer: Results, section "Gating prevents failure at short delays", "The continuous models failed in 100% of runs at 100 ms."
- Evidence pointer: `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-WINDOW-01/experiment/outputs/summary.json` (graded_motor at 0.1 s is 0.625, 0.75, 0.75 across the 2.5, 6, 10 s windows); corroborated by `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-VCLIP-01/experiment/outputs/summary.json` (0.75 at 100 ms under all three V treatments) and `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-GAIN-01/experiment/outputs/summary.json` (0.5 at unity gain, 2.5 s window)
- Concern: Graded unfiltered is a continuous model by the manuscript's own taxonomy and it never reaches 100% at 100 ms in any of these runs (50% to 75%). Addition and graded filtered do reach 100%. As written, the sentence is contradicted by the same dataset the paragraph cites.
- Why it matters: The sentence supports the paragraph's contrast between gates and continuous models at 100 ms. The contrast survives with an accurate predicate, but the current wording is simply wrong.
- Resolution test: Replace with "Addition and graded filtered failed in 100% of runs at 100 ms; graded unfiltered failed in 62.5% to 75%", and verify the new sentence against `WINDOW-01`.

### R1-M4 — The failure-rate range at 140 and 200 ms under all V treatments is wrong
- Severity: Medium
- Blocking: No
- Axis: technical soundness
- Claim pointer: Results, section "The 100 ms advantage depends on the V-term treatment and gate threshold", "At 140 and 200 ms, all variants failed in 75% to 100% under all three treatments."
- Evidence pointer: `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-VCLIP-01/experiment/outputs/summary.json` (graded_motor at 0.2 s is 0.625 under all three treatments; allnone at 0.14 s is 0.6875 under clip and unclipped)
- Concern: Two cells fall below the stated floor. Graded unfiltered fails at 62.5% at 200 ms, and gate filtered fails at 68.75% at 140 ms under clip and unclipped. The paper itself reports the latter as 68.8% in the window section, so the two sections disagree.
- Why it matters: An inflated floor makes the long-delay regime look more uniformly catastrophic than it is, which is the opposite of the paper's own message that these rates are configuration-dependent.
- Resolution test: Restate the range as 62.5% to 100%, or scope the sentence to the specific variants it intends (for example addition and graded filtered only), and cross-check against the 68.8% figure reported two paragraphs earlier.

### R1-M5 — "All of these rates are reproduced identically across three seeds" overclaims
- Severity: High
- Blocking: No
- Axis: technical soundness
- Claim pointer: Results, section "A true command copy does not rescue delay", "All of these rates are reproduced identically across three seeds (24 parameter-seed combinations per cell)."
- Evidence pointer: `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-MULTISEED-01/experiment/outputs/summary.json`
- Concern: Graded command does equal graded filtered identically in every seed (0.875, 1.0, 1.0, 1.0, 1.0), the oracle repeats identically, and gate goal is 0% everywhere, so the claim map's narrower C21 wording holds. However gate filtered and gate command are not identical across seeds. Gate filtered at 100 ms is 0%, 0%, 12.5% by seed (pooled 4.2%) while gate command is 0% in all three seeds; gate filtered at 140 ms is 75%, 62.5%, 62.5% (pooled 66.7%) while gate command is 75% in all three. The sentence as written is false for the gate pair, and the claim map itself (C21) is more careful than the manuscript.
- Why it matters: The command-copy null conclusion survives (gate command never rescues, and is if anything slightly worse at 140 ms), but a validation sentence that is contradicted by its own cited artifact is exactly the kind of thing this paper's credibility rests on avoiding.
- Resolution test: Restrict the sentence to what C21 asserts (graded command equals graded filtered identically; gate goal at ff at or above 0.5 is 0% in every seed), and report the gate filtered versus gate command seed-wise rates explicitly, noting that the difference is 1 to 2 of 16 runs and does not favor the command copy.

### R1-M6 — The ODE-equivalence trajectory claim is not supported by its own summary
- Severity: Medium
- Blocking: No
- Axis: technical soundness
- Claim pointer: Results, section "Adaptive updates do not rescue delay", "trajectories agree to floating-point precision until chaotic amplification in runs that diverge anyway"
- Evidence pointer: `/Users/yyl/Desktop/workshop/nature/runs/P1-EC-ADAPTIVE-ODE-01/experiment/outputs/summary.json`
- Concern: Failure classification and failure time agree in 96 of 96 pairs with max failure-time difference 0.0, which fully supports the main validation claim. The trajectory clause does not match the summary, which reports max prefix heading differences of 0.205 rad (source rule, 20 ms) and 4.12 rad (gradient rule, 20 ms), and a max prefix omega difference of 0.017 rad/s for the gradient rule at 20 ms. Those are not floating-point-precision agreements under any ordinary reading, and the summary gives no field showing where precision agreement ends and amplification begins.
- Why it matters: The failure-agreement result is the load-bearing check and it is solid. The trajectory sentence adds a stronger, unsupported flourish that a careful reader can falsify from the cited file.
- Resolution test: Either delete the trajectory clause, or qualify it with the actual numbers (for example, prefix heading agreement better than 1e-12 rad until within some stated time of divergence, with the observed exceptions listed), or recompute and report the divergence onset time per pair.

## Minor Comments

### R1-m1 — Discussion and Results disagree on graded sensitivity
- Axis: readability / internal consistency
- Affected element: Discussion, "graded cancellation at a gain of 0.5 is 0.15% sensitive" versus Results, "about 0.3% sensitive (59.923 versus 59.770 degrees)"
- Issue: The data in `source_protocol_check.json` give (59.923 - 59.770) / 59.923 = 0.255%, which rounds to 0.3% as in Results. The Discussion figure 0.15% appears to be the absolute difference in degrees mislabeled as a percent.
- Required correction: Change the Discussion to 0.3% (or state 0.15 degrees and convert consistently).

### R1-m2 — Prediction count does not match the list
- Axis: readability
- Affected element: Results, section "Predictions", "The model makes five predictions"
- Issue: Four numbered predictions follow, then a paragraph offering a command-copy negative prediction and a feedforward positive prediction, yielding either four or six depending on how one counts.
- Required correction: State the correct count or number all predictions explicitly.

### R1-m3 — Figure 3 is cited for rates it does not show
- Axis: readability
- Affected element: Results, "Addition failed in 75% and 100% ... graded unfiltered in 75% and 62.5% (Fig. 3)"
- Issue: `make_fig_window.py` plots only `allnone` and `allnone_motor`. The continuous-model rates are real in `WINDOW-01` but are not in Figure 3.
- Required correction: Move the citation so it attaches only to the gate rates, or add the continuous curves to the figure.

### R1-m4 — "The same as the current-visual oracle" fails at 200 ms
- Axis: technical soundness
- Affected element: Results, section "A goal feedforward rescues delay", graded goal at ff=1.0 "75%, 62.5%, 75%, 75%, and 75% ... the same as the current-visual oracle"
- Issue: The oracle rates in `P1-EC-COMMAND-01` are 75%, 62.5%, 75%, 75%, 62.5%. They match through 140 ms but differ at 200 ms (goal 75% versus oracle 62.5%, 1 of 8 parameter sets). Claim C19's wording ("0.625-0.75") is the safer formulation.
- Required correction: Replace "the same as" with "in the same range as" or state the 200 ms difference explicitly.

### R1-m5 — Uncited references
- Axis: readability
- Affected element: References 4, 5, 6, 7, 11, 12 (Erginkaya, Lappalainen, Wang-Chen, Westeinde, von Holst, Dhiman)
- Issue: None of these appear in the body text of the revised manuscript as far as I can find by search.
- Required correction: Cite them in the Introduction or Discussion where they belong (for example von Holst and Mittelstaedt for the reafference principle, Lappalainen and Erginkaya alongside the connectome paragraph), or remove them.

### R1-m6 — Noise provenance and unit terminology
- Axis: internal consistency
- Affected element: Abstract, "75% for no efference copy" and "62.5% to 100% of parameter sets"; Results gain section (addition 75% at 50 ms) versus Results gating section (addition 100% at 50 ms)
- Issue: The gain sweep is noiseless with 12 parameter sets; the window, V, and threshold sweeps add noise with 8 parameter sets and 2 seeds, so addition at 50 ms is legitimately 75% in one run and 100% in another. The Stimuli section says noise is added "in the robustness sweeps" but never enumerates which those are, and the Abstract calls stress-test cells "parameter sets" when they are parameter-seed runs.
- Required correction: Enumerate the noisy sweeps explicitly in Methods, and use "runs" or "parameter-seed combinations" where the unit is not a bare parameter set.

### R1-m7 — Manuscript labels versus code and artifact labels
- Axis: readability
- Affected element: Results, section "A minimal steering model and five variants", the filtered/unfiltered naming disclaimer
- Issue: The runs and code use `graded_motor`, `allnone_motor`, "graded unfiltered oracle", and "gate unfiltered oracle". The manuscript insists these are not motor signals, which is correct for the implementation (I verified that `allnone_motor` computes the bar torque from the current visual state in `ec_model.py`), but the artifacts a reader must trace say "motor" everywhere. No mapping table is provided.
- Required correction: Add a one-line label mapping (manuscript name, code name, run-summary name) in Methods or a supplementary note.

### R1-m8 — The window-extension sentence mixes two runs
- Axis: internal consistency
- Affected element: Results, gain section, "At gains of 0.5 or more, its 200 ms failure was 25% to 42%. At unity gain, extending the window to 6 s raised the 200 ms failure to 62.5%."
- Issue: The 25% to 42% figures come from `P1-EC-GAIN-01` (2.5 s, noiseless, 12 parameter sets, unity gain 200 ms = 33.3%). The 62.5% comes from `P1-EC-WINDOW-01` (noise, 8 parameter sets, 2.5 s = 50%, 6 s = 62.5%). The window extension is real within `WINDOW-01`, but the juxtaposition implies it applies to the gain-sweep numbers.
- Required correction: Name the run each number comes from, or phrase as "in a separate window check with noise, the same delay rose from 50% at 2.5 s to 62.5% at 6 s".

### R1-m9 — Stale figure files in the submission directory
- Axis: readability
- Affected element: `fig2_failure_rate_vs_delay.png`, `fig2b_critical_delays.png`, `fig2d_adaptive.png`, `fig2e_adaptive_alpha.png`, `fig3_phase_diagram.png`, `fig4_example_trajectories.png`, `fig5_gating_signal.png`, `fig6_linear_stability.png`, `fig_mechanism.png`
- Issue: These belong to the pre-revision figure numbering and are not referenced by `MANUSCRIPT_REVISED.md`. Two of them (the old Fig. 5 gating-signal figure and the linear-stability figure) depict claims the paper now retracts.
- Required correction: Remove them from the submission package or move them to an archive subfolder.

### R1-m10 — Figure 4 legend does not name the variant in the threshold panels
- Axis: readability
- Affected element: Figure 4 legend, "Middle and right, failure rate across gate thresholds"
- Issue: The script titles say "gate filtered", but the legend does not, which contributes to the variant-attribution problem in R1-M1.
- Required correction: State "gate filtered" in the legend for all three panels, or add the gate-unfiltered curve.

### R1-m11 — Ephemeral evidence pointer
- Axis: technical soundness
- Claim pointer: claim map C6 artifact field, `/tmp/flightsim/Figure S3/FIGURE_S3_delayed_vs_nondelayed.m`
- Evidence pointer: `/tmp/flightsim/Figure S3/FIGURE_S3_delayed_vs_nondelayed.m` (exists now)
- Issue: A `/tmp` path will not survive machine or session boundaries, and the Introduction's claim about the source's supplementary delay comparison depends on it.
- Required correction: Copy the audited source file (or the relevant excerpt with a checksum) into a durable, license-compliant location in the packet, or cite the commit and file path in the public repository instead.

### R1-m12 — Sweep descriptions under-specify dimensions
- Axis: readability
- Affected element: Methods, Sweeps, "a goal-delay control over four goal delays and two visual delays (256 runs)", "the discriminating conditions at gain 1.0", "a 10 s window check (400 runs)"
- Issue: 256 runs requires four model-gain conditions in addition to the stated dimensions; the multi-seed run includes gate goal at ff=0.5, not only gain 1.0; the 400 rows of `P1-EC-FEEDFORWARD-02` span both the 6 s and 10 s windows (200 each), so "10 s window check (400 runs)" overcounts the 10 s portion if read as new simulations.
- Required correction: List the model-gain conditions for each check and state that the feedforward window check re-ran both windows.

## Technical failings that need to be addressed before the case is established

1. Correct the three false quantitative statements in the main text (R1-M1 threshold robustness, R1-M3 the 100% at 100 ms sentence, R1-M4 the 75% to 100% range) so that every rate in the Abstract, Results, and Discussion matches its cited artifact.
2. Fix the multi-seed validation sentence (R1-M5) so it asserts only what `P1-EC-MULTISEED-01` shows.
3. Regenerate the claim-to-evidence map against the revised manuscript (R1-M2). In its current state the packet's own audit file contradicts the paper's central corrections.
4. Qualify or remove the trajectory-precision clause of the ODE check (R1-M6).

None of these, once corrected, threatens the direction of the results. The gain, gating-at-short-delay, adaptation-null, command-copy-null, and feedforward-mechanism conclusions all survived my spot-checks against the run summaries.

## Assessment against the five axes

- Originality: Strong within its niche. Treating transport delay as a first-class variable in this model family, the window and clip artifact demonstrations, and the goal-feedforward versus efference-copy dissociation are new relative to the source paper. The reimplementation is deliberately stylized and the paper says so.
- Scientific importance: Moderate. There is no new biological data, but the paper yields experimentally separable predictions (short-delay gating, V-shape dependence at 100 ms, intolerance to jointly delayed proprioception) and a methodological caution that transfers to any finite-window stability claim in closed-loop simulation.
- Interdisciplinary readership: Well suited to PLOS Computational Biology. The prose is largely accessible to nonspecialists, the scope note is explicit, and the control-theoretic content (delayed feedback, gating) is introduced rather than assumed. The density of percentage sequences in Results is the main barrier for casual readers.
- Technical soundness: Mostly sound. Run counts, constants, failure criteria, figure data sources, and the great majority of quoted rates check out. The blemishes are several over-precise generalizations contradicted by cited cells, the stale claim map, and one unsupported numerical-validation flourish. Statistical reporting is appropriate for a design grid and the absence of inferential tests is justified in the text.
- Readability: Good overall with clear sectioning, honest corrections, and informative figure legends. Weak points are the unmapped manuscript-versus-code model names (R1-m7), noise provenance (R1-m6), a few figure-pointer slips (R1-m3, R1-m10), and leftover superseded figures in the directory (R1-m9).

## Recommendation posture

Major revision. The central computational case is real and, with the exception of the items above, well supported by the artifacts I could inspect, and the paper's transparency about its own corrections is exemplary. However, the Abstract and Results contain at least three quantitative statements that the cited runs contradict, the multi-seed validation sentence overreaches, and the claim-to-evidence map shipped in the packet still asserts the very long-delay gating results the revised manuscript retracts. These are corrections of text and documentation rather than new experiments, and I would expect the revised paper to be publishable in PLOS Computational Biology once every quantitative claim reconciles with its evidence pointer. I do not treat any single concern here as blocking the establishment of the central case, but the collection must be resolved before the case can be certified as internally consistent.
