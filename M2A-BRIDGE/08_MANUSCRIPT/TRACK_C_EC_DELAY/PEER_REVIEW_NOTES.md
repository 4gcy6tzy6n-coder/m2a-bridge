# Internal adversarial review — Track C

> **Superseded:** This was the pre-review self-assessment. The independent three-reviewer synthesis is in `CROSS_REVIEW_SYNTHESIS.md`; the current paper is `MANUSCRIPT_REVISED.md`. Kept as a historical record.

- Date: 2026-10-27
- Reviewer: session (adversarial, not the author)
- Manuscript: `MANUSCRIPT_DRAFT.md`
- Recommendation: **minor-to-major revision**; the gain sweep and source-protocol check resolved the three structural concerns, and the remaining items are figure production, adaptive-MLP scope, and owner-side metadata.

---

## Summary of the submission

The manuscript extends the Canelo et al. (2024) flight-steering model with an explicit transport delay on the visual feedback and compares five efference-copy variants: addition, graded sensory, graded motor, allnone, and allnone_motor. It reports that graded sensory cancellation fails at 9-15 ms, while gating lasts to 140-200 ms under a large-excursion criterion, and that the gating advantage shrinks to ~56-58 ms under a strict oscillation criterion. It makes four predictions for delayed-feedback experiments.

## Major concerns

### M1. The model does not reproduce the source's zero-delay background result

The source paper's behavioral argument is that all-or-none gating explains the invariance of object-evoked turns across sparse and dense backgrounds, while graded cancellation does not. The manuscript's zero-delay check with a single bar and a single grating step finds the opposite ordering: graded cancellation is more invariant to grating gain (ratio 0.9998) than all-or-none (0.9830). The manuscript now discloses this, which is good, but a reviewer will ask whether the implementation is faithful. The source's Figure 5 uses a different protocol (constant grating angle, `k_opto` changing from 0.05 to 0.7, scaled parameters `I=6e-4`, `beta=1e-1`, `P=10e-1`, `V=1e-2`, and an auto-tuned MLP for the graded model). The current comparison is therefore not a replication of the source's background experiment.

**Required action (choose one):**
- Port the source's Figure 5 protocol (constant grating, piecewise gain, scaled parameters) and show whether the ranking is recovered; or
- Reframe the paper explicitly as a new minimal model inspired by the source's equations, not as a replication, and remove any implication that it reproduces the source's behavioral result. The manuscript already leans toward the second option; make it explicit in the title/abstract if the first is not done.

### M2. The graded model is not the adaptive graded model of the source

The source's graded model includes an online MLP that learns the grating gain (`sim_effc`). The manuscript's `graded_sensory` and `graded_motor` use a fixed gain (implicitly 1) and differ only in whether `omega_ec` is driven by delayed or current bar torque. This is a legitimate comparison of two fixed graded architectures, but it is not a fair test of "graded efference copy" as implemented in the source. An adaptive graded model might learn to compensate for delay or for the grating gain, which could change the result.

**Required action:** either implement an adaptive graded variant (the source's MLP or a simpler online gain) and report its delay curve, or state clearly that the paper compares fixed-gain graded variants and that adaptive graded EC is future work. The current Limitations mention the absence of learning, but the Results and Abstract should not generalize to "graded efference copy" without qualification.

### M3. The headline depends on the failure criterion

Under the prespecified large-excursion criterion, allnone lasts 200 ms and allnone_motor 110 ms. Under a strict oscillation criterion (`|omega|>50`), both last ~56-58 ms. The ordering graded < gating is robust, but the magnitude of the gating advantage and the allnone-vs-allnone_motor difference are not. The manuscript discloses this in a dedicated Results subsection, which is good. But the title ("more than binary gating") and the abstract's emphasis on 200 ms may still overstate the robustness. A reviewer will ask for a criterion-independent statement.

**Required action:** make the criterion-dependence part of the headline claim, not a caveat. For example: "Graded sensory cancellation fails first under every criterion; binary gating buys time, but how much depends on what counts as failure." Consider reporting a range (56-200 ms) in the abstract rather than a single number.

## Moderate concerns

### m1. Linear stability analysis (addressed)

A linear stability analysis is now included (`linear_stability.py`, Fig. 6). It gives critical delays of 29-43 ms for continuous models, 300 ms for graded_motor at gain 1.0, and 29 ms for allnone on the open-gate branch. Importantly, it does not capture the gating or motor-copy benefits, which are large-signal/nonlinear effects. This is disclosed in the Results and Discussion, and it strengthens the paper by scoping the main result correctly.

### m2. The "motor copy" is a proxy

`f_bar_motor` is the bar torque computed from the current visual state, not an actual motor command. Calling it a "current motor copy" is a modeling shorthand. Either rename it ("current-state torque") or justify the proxy more carefully.

### m3. The failure criterion and the V-term clip are modeling choices

The manuscript discloses the V-term clip and the failure criterion. A reviewer may ask for sensitivity to the clip. We have not run that. Add a short sensitivity analysis or state it as a limitation.

### m4. The stimulus is a single bar and a single grating step

The source's behavioral experiments use sparse/dense backgrounds and naturalistic scenes. The manuscript's stimulus is simpler. This bounds the generality of the result. The Discussion acknowledges it; keep it explicit.

### m5. Only three parameter sets in the fine grid

The 1 ms grid uses three parameter sets; the coarse/noise grids use more. The fine-grid medians are representative, not exhaustive. Report the number and the selection rule.

### m6. No new biological data

The paper is a B0 computational study. This is acceptable for PLOS Computational Biology, but the cover letter and abstract must not imply experimental validation. They currently do not.

## Minor concerns

- Figures are PNG; final submission should be vector or 300+ dpi.
- Default matplotlib palette is not colorblind-safe.
- Reference formatting should be checked against the journal style; the Canelo 2024 entry is a reviewed preprint, not a final journal article.
- Author list, affiliations, contributions, funding, competing interests, and code license are placeholders.
- The source repository has no license; only equations were ported. State this in the Methods.
- The code snapshots and `run_all.sh` are in place; a clean-environment check passed (9 tests + selftests).

## Post-review addendum (2026-10-27, after the gain sweep)

M2 is now substantially addressed by the gain sweep (`P1-EC-GAIN-01`) and the adaptive MLP check (`P1-EC-ADAPTIVE-01`). At the source's fixed gain 0.05, graded cancellation is inert and indistinguishable from no efference copy. At gains of 0.25 or more, delayed sensory cancellation becomes harmful at 50 ms (100% versus 75% failure). A current motor copy at high gain is worse at short delays but better at long delays (200 ms failure 25-42% versus 100%). Gating is gain-invariant. The adaptive MLP learns a higher gain as delay increases (0.38 to 1.06) and also fails at 50 ms (100% versus 75% for no EC). The learning-rate sweep (`P1-EC-ADAPTIVE-02`, alpha 1e-5 to 1e-3, three seeds) confirms that every rate reaches 100% failure by 100 ms; no rate rescues stability. This turns the "unfair fixed-gain comparison" concern into a main finding. The only remaining M2 caveat is that the MLP update is step-wise rather than ODE-internal.

M1 is partially addressed by the source-protocol check: the source's background ranking is recoverable with a near-zero gate threshold and a sub-unity EC gain, but not as a generic property. M3 is addressed by making criterion-dependence a Results subsection; the title/abstract now center gain and source rather than a single 200 ms number.

The recommendation shifts from "major revision" to **"science structurally complete; remaining items are owner-side author metadata, a preprint/journal decision, and the optional ODE-internal MLP reproduction."** The linear stability analysis is now included and correctly scopes the main result as a large-signal/nonlinear effect; it does not explain the gating or motor-copy benefits, which is disclosed.

## What is strong

- The delay manipulation is genuinely new relative to the source's main simulations.
- The separation between graded sensory and gating is large and robust in ordering across criteria.
- The zero-delay negative result is disclosed rather than hidden.
- The threshold and solver sensitivity checks are honest.
- The claim-to-evidence map and experiment logs make the provenance clear.

## Verdict

**Major revision, then submit to PLOS Computational Biology.** The paper is not ready for Nature or Nature Communications; it is a solid specialist modeling paper if M1-M3 are addressed. The fastest path is to reframe as a new minimal model (M1), implement or explicitly defer adaptive graded EC (M2), and make the criterion-dependence the headline (M3). A faithful reproduction of the source's Figure 5 would be the strongest revision but is not strictly necessary if the paper stops claiming replication.
