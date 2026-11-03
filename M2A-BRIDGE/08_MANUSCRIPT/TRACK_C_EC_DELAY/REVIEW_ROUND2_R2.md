# Review Round 2, Reviewer 2

Manuscript: Efference-copy gain, gating, and current self-state in a delayed fly steering model
Target: PLOS Computational Biology, Research Article
Scope of this review: B0 computational study, no new biological data. Working lens: experimental design and robustness.
Verification budget: manuscript and claim-to-evidence map read once; six summary.json files spot-checked (listed under Evidence below). All other numbers are marked not assessable.

---

## Overall assessment

This is a carefully self-correcting computational stress test of efference-copy architectures under explicit transport delay, and the revised text is substantially more honest than the earlier version it replaces. The window-dependence analysis and the feedforward self-state ablation verified cleanly against the checked summaries, and the manuscript scopes its claims to the assay rather than to the fly. The main outstanding problems are scope statements that the checked evidence does not fully support (an "identically across three seeds" claim and an abstract-level gate-threshold robustness claim that covers only one of the two models present in its evidence file), an unreported failure-criterion sensitivity that the project's own claim map records, and a claim-to-evidence map that is stale relative to the revised text. I would support revision toward publication after these are resolved, and I do not consider new biological experiments a condition of publication.

## Who would be interested in the results, and why

Researchers in Drosophila visuomotor processing and efference copy will care because the paper converts a qualitative model-family debate (graded subtraction versus all-or-none gating) into concrete, experimentally manipulable variables, namely copy gain, feedback delay, gate threshold, and the shape of the velocity nonlinearity, and because it offers testable predictions about imposed visual delay with intact versus delayed proprioceptive pathways. Computational neuroscientists and control theorists working on delayed negative feedback will find the central lesson useful, namely that a graded cancellation loop can become destabilizing as gain rises, that gating buys time rather than asymptotic stability, and that a command copy adds no information absent from the delayed sensory estimate. Robustness and methodology readers will value the explicit demonstration that an earlier long-delay claim was a finite-window and V-term artifact, since it is a worked example of how window and nonlinearity choices manufacture stability results. Roboticists building reafference-based stabilization under latency are a natural secondary audience.

## Major strengths

1. Self-correction is exemplary. The manuscript removes two earlier claims (robust gating through 100 to 200 ms, and a linear-stability explanation) and documents why each failed. The window-artifact quantification verified exactly (see R2-m territory below and the verified numbers).
2. The control logic around the command-copy and feedforward questions is well designed. Pre-plant command copy, current-visual oracle, goal-delay, and self-state ablation form a coherent ladder that locates the rescue in current self-state rather than in a motor copy or early target knowledge. The self-state ablation numbers verified exactly against the checked summary.
3. Stress testing is unusually broad for a model paper. Gate threshold, V-term form, simulation window, seeds, parameter sets, goal amplitude and time-constant mismatch, and an ODE-internal re-implementation of the adaptive update are all reported, with run counts given per sweep in Methods.
4. Interpretive discipline is strong. The scope note, Limitations, and Abstract all state that the model does not reproduce the source's zero-delay ranking and makes no claim about the fly's mechanism. The goal feedforward is explicitly labeled an upper bound.
5. Within the checked files, most reported rates match the evidence exactly, including several nontrivial ones (the 3 of 16 to 11 of 16 to 12 of 16 window progression at 140 ms, and the full gate-threshold grid for the reported model).

## Major Concerns

### R2-M1
- Severity: High
- Blocking: No
- Axis: Technical soundness
- Claim pointer: Results, "A true command copy does not rescue delay", final sentence. "All of these rates are reproduced identically across three seeds (24 parameter-seed combinations per cell)." Also claim map rows C18 and C21.
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/runs/P1-EC-MULTISEED-01/experiment/outputs/summary.json (verified)
- Concern: The word "identically" does not hold for gate filtered. In the checked multi-seed summary, gate filtered at ff=0 fails 0%, 0%, and 12.5% at 100 ms across seeds 0, 1, and 2 (pooled 4.2%, 1 of 24), and 75%, 62.5%, and 62.5% at 140 ms (pooled 66.7%, 16 of 24). Gate command stays at 0% at 100 ms and 75% at 140 ms in every seed. So gate command and gate filtered are identical in seed 0 only, and pooled rates diverge at 100 and 140 ms. The graded-command versus graded-filtered identity and the gate-goal 0% claims do verify exactly in every seed, and the oracle and graded-goal rates match the text.
- Why it matters: This is a robustness claim in the Results, and the checked evidence shows seed-level variability of 1 to 2 runs out of 16 to 24 in exactly the cells being called identical. Overstated replication language is the kind of thing that erodes trust in the cells that do replicate.
- Resolution test: Rewrite the sentence to report pooled and per-seed rates (for example, gate filtered 4.2% pooled at 100 ms and 66.7% at 140 ms versus gate command 0% and 75%), state that the command-versus-filtered equality is qualitative at long delays and exact for the graded family, and keep "identical" only where the file supports it.

### R2-M2
- Severity: High
- Blocking: Yes
- Axis: Technical soundness
- Claim pointer: Abstract ("gating prevents failure (0%) across gate thresholds from 0.01 to 0.5 of the bar-torque scale"), Results "The 100 ms advantage depends on the V-term treatment and gate threshold" ("At 20 and 50 ms, gating remained at 0% across every threshold"), and the Methods statement that the gate-threshold check crossed two gating models.
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/runs/P1-EC-GATE-01/experiment/outputs/summary.json (verified)
- Concern: Every gate-threshold number quoted in the manuscript matches the allnone rows of the checked summary exactly (0% at 20 and 50 ms for all thresholds; at 100 ms, 0% for thresholds below 0.5 and 37.5% at 0.5 under clip, 75% at every threshold under smooth; 75% everywhere at 140 ms). However, the same file contains a second model, allnone_motor, which is never discussed in this section, and its numbers contradict the blanket wording. For that model, failure is 25% at 50 ms with threshold 0.5 under clip, and 62.5% at 100 ms with threshold 0.5 under clip rather than 37.5%. The manuscript Methods say two gating models were crossed, but the mapping between run names (allnone, allnone_motor) and manuscript variants (gate filtered, gate unfiltered, gate command) is not documented anywhere in the review packet, so it is also unclear which manuscript variant the unreported rows correspond to.
- Why it matters: The abstract-level robustness claim is one of the paper's three headline results. As written it is supported for one of the two models in the evidence file, and the failure mode is a corner (highest threshold, clip, short delay) that a careful reader can find. Either the claim must be scoped to the specific variant, or both variants must be reported, or the name mapping must show that the second model is not one of the variants covered by the sentence.
- Resolution test: Name the two models in the sweep, map run names to manuscript variant names once in Methods, report both models' gate-threshold results (in text, figure, or supplement), and scope the abstract and Results sentences to exactly what the combined grid shows.

### R2-M3
- Severity: Medium-High
- Blocking: No
- Axis: Technical soundness
- Claim pointer: Results gating sections and Abstract (short-delay advantage "survives ... across clip, smooth, and unclipped V treatments" and across thresholds), plus Limitations "The failure criterion is a modeling choice."
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/CLAIM_TO_EVIDENCE_MAP.csv row C10, which states that the ordering is robust but "the gating advantage ... [is] criterion-dependent" with roughly a 60 ms boundary under an alternative absolute-angular-velocity threshold of 50 rad/s, citing threshold_sensitivity.json. That JSON file was not read in this review (not assessable here).
- Concern: The manuscript quantifies its dependence on two analysis choices (simulation window and V-term form) with full transparency, but it does not report any quantified dependence on the failure criterion itself, even though the project's own claim map records that the gating advantage shrinks to about 60 ms under an alternative criterion. The Limitations line asserts the criterion is a modeling choice without showing the sensitivity that the claim map says exists.
- Why it matters: The failure criterion defines every rate in the paper. A reader cannot judge robustness of the 100 ms boundary discussion, which the manuscript already treats as fragile, without knowing how much the criterion moves it. The window and V analyses set a standard the criterion analysis should meet.
- Resolution test: Add a short criterion-sensitivity paragraph or figure citing the existing threshold-sensitivity artifact, quantifying how the 20 to 50 ms, 100 ms, and 140 ms conclusions change under at least one alternative threshold (for example the angular-velocity threshold named in the claim map), or remove all robustness phrasing that could be read as covering the criterion choice.

### R2-M4
- Severity: Medium
- Blocking: No
- Axis: Technical soundness
- Claim pointer: Abstract first result ("At gains of 0.25 or more, delayed-sensory cancellation is harmful at 50 ms, failing in 100% of parameter sets versus 75% for no efference copy") and Results "Efference-copy gain".
- Evidence pointer: Manuscript Methods "Sweeps" text (gain sweep, 12 parameter sets, 1,440 runs, no seeds listed) and claim map row C14 caveat ("no noise in this sweep"). The gain-sweep summary itself was not on the spot-check list and is not assessable here. For contrast, addition at 50 ms was verified at 100% failure in both checked runs that contain it (window check, n=16; feedforward check, n=8).
- Concern: The paper's first headline result rests on a single configuration, namely 12 parameter sets, one run per cell, no noise, no seed replication, with a margin of 12 of 12 versus 9 of 12. Elsewhere in the checked evidence, failure rates for unchanged conditions move by 1 to 2 runs between seeds or runs, and the addition baseline at 50 ms is 75% in the gain-sweep text but 100% in both summaries checked here. The other two headline results were stress-tested across seeds or windows; this one was not.
- Why it matters: "Robust variable" is the paper's framing for gain, but only parameter-set and delay robustness were demonstrated for it. A 3-run margin with a shifting baseline is thin support for abstract-level language.
- Resolution test: Either run the gain grid at three seeds with the noise used elsewhere and report the pooled rates, or soften the abstract and Results to state the sweep configuration (single noiseless run per cell, 12 sets) alongside the claim.

### R2-M5
- Severity: Medium
- Blocking: No
- Axis: Originality and interpretation (also design)
- Claim pointer: Results "A goal feedforward rescues delay, and it requires current self-state" and the Discussion's "the delayed visual loop ... lacks current self-state", plus Abstract third result.
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/runs/P1-EC-FEEDFORWARD-01/experiment/outputs/summary.json and /Users/yyl/Desktop/workshop/nature/runs/P1-EC-FF-STATE-01/experiment/outputs/summary.json (both verified for the rates they contain). The goal-delay grid (P1-EC-GOAL-DELAY-01) and goal-mismatch grid were not spot-checked (not assessable).
- Concern: The rescue branch is privileged in three compounding ways that are disclosed but not fully controlled. The instructed goal shares amplitude and onset with the bar stimulus, so the branch is told what the delayed visual loop is trying to recover. The branch uses current heading and angular velocity without delay, an assumption with no biological justification offered. And the same augmented signal (F_bar plus feedforward torque) drives both the corrective torque and the gate trigger, while the branch also modifies the bar pathway itself, so "rescue by the feedforward" is partly "rescue by a second current-state feedback loop that redefines the gate input". The self-state ablation cleanly establishes that current self-state is necessary for the rescue, and that is the manuscript's stated conclusion. What is not established is whether the goal signal contributes anything beyond generic current-state feedback, and how the result would look with goal onset decoupled from stimulus onset, which Limitations lists as untested.
- Why it matters: The mechanistic sentence readers will quote is about current self-state, and that holds. The framing "goal feedforward rescues" invites the stronger reading that goal-related pathways are special, which the current control set cannot separate from any current-state feedback pathway.
- Resolution test: Add one control that injects a current-state-driven torque of matched magnitude without an instructed goal (or with the goal replaced by a fixed setpoint unrelated to the stimulus), and one control that decouples goal onset from stimulus onset. Then state which ingredient the rescue requires. If those controls are out of scope, narrow the wording so the claim is strictly the necessity of current self-state, which the existing ablation supports.

### R2-M6
- Severity: Medium
- Blocking: No
- Axis: Technical soundness and readability (documentation)
- Claim pointer: The packet's claim-to-evidence map as a whole, specifically rows C1, C2, C3, and C9.
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/CLAIM_TO_EVIDENCE_MAP.csv (read in full)
- Concern: The map is stale relative to the revised manuscript. Rows C2 and C3 assert that gating "remains stable to a median critical delay of 0.20 s" and that gating on the delayed sensory estimate beats gating on a motor copy (0.20 s versus 0.11 s), and row C9 reports median first-failure times. The revised manuscript explicitly retracts the 200 ms critical-delay claim ("We no longer report a 200 ms critical delay for gating") and reattributes the earlier motor-copy result to a current-visual oracle effect. Row C17 is marked as removed, but C2, C3, and C9 are not. The map also uses model names (graded_sensory, graded_motor, allnone, allnone_motor) that never appear in the manuscript.
- Why it matters: The map is the artifact a reader or editor uses to trace claims to evidence. If it still carries retracted claims under "strong_within_model" strength labels, the packet contradicts itself, and the naming mismatch makes the six-figure evidence trail harder to audit than it should be.
- Resolution test: Regenerate the map against the revised manuscript only, delete or clearly quarantine rows corresponding to retracted claims, add rows for the revised claims that currently lack pointers (for example the window-artifact result and the criterion and V-treatment stress tests), and include a one-line mapping between manuscript variant names and run model names.

## Minor Comments

### R2-m1
- Axis: Technical soundness
- Affected element: Results, "Gating prevents failure at short delays", sentence "The continuous models failed in 100% of runs at 100 ms."
- Issue: In the checked window summary, graded unfiltered (graded_motor in the run file) fails 62.5%, 75%, and 75% at 100 ms across the three windows, while addition and graded filtered are at 100%. The sentence is true only for a subset of the continuous models.
- Required correction: Name the models covered (addition and graded filtered) or report the graded-unfiltered rate alongside them.

### R2-m2
- Axis: Technical soundness
- Affected element: Results feedforward section, gate duty values at ff_gain 1.0.
- Issue: The text gives the duty sequence as 0.31/0.58/0.62/0.65/0.67. The checked summary gives 0.313/0.582/0.624/0.645/0.669, so the fourth value rounds to 0.64, not 0.65.
- Required correction: Correct the value or state the rounding convention.

### R2-m3
- Axis: Technical soundness
- Affected element: Results feedforward section, "At ff_gain = 1.0 ... the same as the current-visual oracle."
- Issue: Graded goal at ff 1.0 is 75%, 62.5%, 75%, 75%, 75% (verified), while the oracle as reported in the command section and verified in the multi-seed summary is 75%, 62.5%, 75%, 75%, 62.5%. They differ at 200 ms, and the comparison crosses two different runs.
- Required correction: Say "matches the oracle at four of five delays" or give both sequences.

### R2-m4
- Axis: Technical soundness
- Affected element: Two statements about gate filtered at 100 ms with a 10 s window. The window section says 18.8% (3 of 16, verified); the feedforward section says it "rises from 0% to 12.5%".
- Issue: Two different rates are presented for what reads as the same condition. The most likely explanation is different runs and sample sizes (3 of 16 versus presumably 1 of 8 in the feedforward 10 s check), but the text does not say so. The feedforward 10 s file (P1-EC-FEEDFORWARD-02) was not spot-checked, so its rate is not assessable here.
- Required correction: Attribute each rate to its run and n, or report one canonical number.

### R2-m5
- Axis: Readability
- Affected element: Predictions section, opening sentence "The model makes five predictions", followed by four numbered items.
- Issue: The fifth (and a sixth, since the closing paragraph contains both a negative command-copy prediction and a positive feedforward prediction) appears only in prose.
- Required correction: Renumber so the count matches, or fold the prose predictions into the list.

### R2-m6
- Axis: Technical soundness
- Affected element: Methods "Sweeps" inventory and the Results' 200 ms ceiling on feedforward claims.
- Issue: A run at delays of 200 to 500 ms exists (P1-EC-LONGDELAY-01, verified) and is not listed in the Methods sweep inventory. Its contents are consistent with the manuscript's decision to stop claims at 200 ms. Gate goal at ff 1.0 shows 0% failure at every delay through 500 ms, while gate goal at ff 0.5 degrades beyond 200 ms (12.5% at 250 and 300 ms, 62.5% at 400 ms, 50% at 500 ms).
- Required correction: Either add a sentence reporting this run (it strengthens the ff 1.0 result and locates the ff 0.5 boundary) or list it in Methods with a reason for exclusion from the claims.

### R2-m7
- Axis: Readability
- Affected element: Whole manuscript and the claim map.
- Issue: Manuscript variant names (gate filtered, gate unfiltered, graded filtered, graded unfiltered, gate command) do not match run and claim-map names (allnone, allnone_motor, graded_sensory, graded_motor, graded unfiltered oracle). No mapping table is given.
- Required correction: One mapping table in Methods or supplement.

### R2-m8
- Axis: Technical soundness
- Affected element: Methods "Sweeps" and the gate-threshold results.
- Issue: The gate-threshold sweep used dt = 2e-4 s while the main sweeps used dt = 1e-4 s, and results from the two are contrasted in the same abstract sentence. The claim map (row C11) records an existing step-halving check (solver_check.json) that the manuscript never cites.
- Required correction: Cite the solver check in Methods and state its outcome for the specific contrasts used, or rerun the threshold sweep at the main step.

### R2-m9
- Axis: Technical soundness
- Affected element: Statistics section and all 0% claims.
- Issue: No form of uncertainty is reported for cells with 0 failures out of 8 or 16 runs. The statement that the parameter grid is a design rather than a sample justifies skipping inferential tests over parameter sets, but seed replication is a sampling process, and the multi-seed file shows exactly where seeds disagree.
- Required correction: Report per-seed rates for headline cells, as the multi-seed summary already allows, without requiring formal hypothesis tests.

## Technical failings that need to be addressed before the case is established

1. The abstract-level gate-threshold robustness claim must be reconciled with the second model present in its own evidence file, and the model-name mapping must be documented (R2-M2). Until then the headline robustness sentence is not established by the checked evidence.
2. The "identically across three seeds" sentence must be corrected to match the multi-seed summary, because it is a checkable factual statement about replication (R2-M1).
3. Failure-criterion sensitivity must be surfaced in the manuscript, since the project's own claim map records it and every reported rate is defined by the criterion (R2-M3).
4. The claim-to-evidence map must be regenerated against the revised text so that retracted claims are not carried as current strong evidence (R2-M6).
5. The gain result, as the first abstract result, needs either seed-level replication or configuration-scoped wording (R2-M4).

None of these requires new biological data, new animal experiments, or a change to the model. All are analysis, reporting, and documentation fixes within the existing artifacts.

## Assessment against the five axes

- Originality: Moderate. Extending a published fly-steering model with a transport delay and stress-testing model families is incremental, but the control ladder (command copy, oracle, goal delay, self-state ablation) and the artifact-correction narrative give it a distinct contribution. The conclusion that a command copy adds no information while current self-state does is a crisp, reusable idea within this literature.
- Scientific importance: Moderate within computational sensorimotor biology, limited outside it. The paper produces no new biology and validates against no new data, and it does not reproduce its source model's behavioral ranking, which it states plainly. Its value lies in converting a qualitative model debate into manipulable variables and in honest negative results that can steer experimental design.
- Interdisciplinary readership: Good potential. The predictions section is written so that experimentalists (Drosophila, and potentially roboticists) can act on it, and the delay-as-first-class-variable framing travels well. Density of inline percentages, the stale claim map, and the missing name mapping currently impede readers outside the immediate project.
- Technical soundness: Mostly sound within the stated assay, with exemplary self-correction on window and stability claims, and verified agreement between text and evidence for the window, feedforward, self-state, and multi-seed graded-family numbers. The concerns in R2-M1 through R2-M4 concern scope and unreported sensitivity rather than fabricated or unverifiable core results, but they must be fixed. Items I could not verify (adaptive and ODE-equivalence runs, gain and V-mode sweeps, goal-delay and goal-mismatch grids, 10 s feedforward check, solver and threshold-sensitivity JSONs) are marked not assessable and should not be read as endorsed.
- Readability for nonspecialists: Fair to good. Figure legends, the scope note, and the plain-language framing of the corrections are strengths. The Results reads as a stream of percentages in places, the prediction count is off, and the variant naming is inconsistent across the packet. A compact summary table of failure rates per variant and delay would carry much of the numeric load.

## Recommendation posture

I am positively disposed toward this manuscript for PLOS Computational Biology after a focused revision. The design story is coherent, the self-corrections strengthen rather than weaken the paper, and the two results I could verify most directly, the window artifact and the self-state ablation, hold up exactly against their summaries. The revision must fix the two overstated robustness sentences, surface the failure-criterion sensitivity that the project already quantified, reconcile the claim map with the retracted claims, and either replicate or scope the gain result; these are reporting and documentation tasks, not new experiments. I would view the goal-feedforward controls as desirable strengthening rather than a condition of acceptance, since the manuscript already labels the construction an upper bound. I encourage the authors to submit after these revisions, while noting that any publication decision rests with the editors and that I have assessed only the materials in this packet.
