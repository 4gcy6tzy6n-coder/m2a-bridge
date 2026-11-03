# Reviewer 3 Report (Round 2)

Manuscript: Efference-copy gain, gating, and current self-state in a delayed fly steering model
Target: PLOS Computational Biology, Research Article
Packet reviewed: MANUSCRIPT_REVISED.md, CLAIM_TO_EVIDENCE_MAP.csv, spot-checks under /Users/yyl/Desktop/workshop/nature/runs/

---

## Overall assessment

This is a carefully bounded computational stress-test of a published fly-steering model under explicit transport delay, and the three headline results (gain dependence, short-delay gating, adaptation failure) plus the command-copy and feedforward results survive spot-checks against the underlying run summaries. The scope discipline is good, with explicit disclaimers about mechanism and about the model's failure to reproduce the source's zero-delay ranking. Two things hold it back from readiness. The claim-to-evidence map contradicts the revised manuscript on the very claims the revision retracts, and the paper never positions itself against the forward-model, Smith-predictor, and delay-compensation control literature that its central manipulation and its central conclusion naturally invite.

---

## Who would be interested in the results, and why

- Computational neuroscientists working on efference copy and internal models, because the paper shows that a canonical graded-cancellation architecture is inert at the gain the source model actually used and harmful at higher gain once delay is present.
- Experimentalists in Drosophila visuomotor control (the Canelo/Kim lineage), because the predictions name concrete manipulable variables (delay length, gate threshold, velocity-nonlinearity shape, proprioceptive access) for tethered-flight delay experiments.
- Control-oriented readers interested in biological implementations of delay tolerance, because the command-copy versus current-self-state dissociation is a clean empirical-style statement of a state-feedback versus command-feedback distinction inside a biological model.
- Model-comparison methodologists, because the window-artifact and V-clip corrections are a documented case where a qualitative ranking flipped under longer integration windows and an alternative nonlinearity.

---

## Major strengths

- Scope honesty. The title, abstract close, Discussion limits, Limitations list, and the standalone Scope note all state that no new biological data exist and that no claim is made about the fly's mechanism.
- Self-correction is transparent. The removed linear-stability analysis, the retracted 200 ms critical delay, and the window/V-clip artifacts are reported rather than buried (Introduction, "The long-delay gating claim was a window artifact", Discussion).
- Numerical claims are traceable. Spot-checks against run summaries confirmed the gain-sweep rates (runs/P1-EC-GAIN-01), window-check rates including the 140 ms 3/16 to 11/16 to 12/16 progression (runs/P1-EC-WINDOW-01), V-treatment rates at 100 ms (runs/P1-EC-VCLIP-01), gate-threshold rates (runs/P1-EC-GATE-01), adaptive gain ranges 0.51 to 1.05 versus 0.22 to 0.40 (runs/P1-EC-ADAPTIVE-03), command-copy identity with filtered variants (runs/P1-EC-COMMAND-01), feedforward rescue at ff_gain of 0.5 or more at both windows (runs/P1-EC-FEEDFORWARD-01, runs/P1-EC-FEEDFORWARD-02), and both mechanistic controls (runs/P1-EC-GOAL-DELAY-01, runs/P1-EC-FF-STATE-01).
- The two mechanistic controls on the feedforward branch (delay the goal, delay the self-state) are well designed and make the "current self-state, not command copy" reading much stronger than a single rescue result would be.
- The paper states its statistical philosophy explicitly (grid as design, not sample) rather than attaching unjustified p-values.

---

## Major Concerns

### R3-M1
- Severity: Major
- Blocking: No
- Axis: technical soundness
- Claim pointer: CLAIM_TO_EVIDENCE_MAP.csv rows C2 ("gating remains stable to a median critical delay of 0.20 s ... 19% failure at 140 ms") and C3 ("0.20 s vs 0.11 s; 19% vs 75% failure at 140 ms"), against MANUSCRIPT_REVISED.md Results, "The long-delay gating claim was a window artifact" ("The 140 ms comparison therefore does not support a gating advantage") and "We no longer report a 200 ms critical delay for gating."
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/CLAIM_TO_EVIDENCE_MAP.csv; /Users/yyl/Desktop/workshop/nature/runs/P1-EC-WINDOW-01/experiment/outputs/summary.json (gate filtered at 140 ms is 18.8% at the 2.5 s window but 68.8% at 6 s and 75% at 10 s)
- Concern: The claim map preserves claims the revised manuscript explicitly retracts, cites figure identifiers that do not exist in the revised figure set (Fig2b, Fig2d, Fig2e, Fig3 phase diagram, Fig5 gating signal), points to MANUSCRIPT_DRAFT.md in C7 rather than MANUSCRIPT_REVISED.md, and uses "current motor copy" language in C3 and C14 that the manuscript itself rejects ("The unfiltered variants are not copies of an issued motor command"). It also has no rows for two revised headline results, the window-artifact correction and the V-treatment stress test.
- Why it matters: The claim map is the audit trail a reviewer or editor uses to verify that each assertion rests on an artifact. Contradictions between map and text undermine confidence in every other number, and stale figure IDs make the packet look like two different papers stapled together.
- Resolution test: Regenerate the map from MANUSCRIPT_REVISED.md. Every row maps to a current section and figure, no row asserts a claim the text retracts, artifact naming matches the manuscript's variant vocabulary, and C7 cites MANUSCRIPT_REVISED.md. Re-run a row-by-row diff against the revised text before submission.

### R3-M2
- Severity: Major
- Blocking: No
- Axis: originality
- Claim pointer: Introduction, "Any visuomotor loop has a delay ... This omission matters because delayed negative feedback is a classic route to oscillation and loss of stability" and "what a delayed visual loop lacks is current self-state rather than a copy of the issued command" (Abstract); Discussion, "The relation to the broader connectome-to-behavior literature is indirect."
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md References list (13 items, none from the forward-model, Smith-predictor, or delay-compensation control canon; von Holst and Mittelstaedt is listed as reference 11 but never cited in the body text)
- Concern: The central manipulation, a transport delay in a negative feedback loop, and the central conclusion, that a delayed loop needs current state rather than a copy of the issued command, sit squarely in the classical literature on internal forward models, Smith predictors, and delay-tolerant control. The manuscript engages none of it. Novelty is framed only against Canelo et al. 2024 and, indirectly, the connectome-to-behavior literature.
- Why it matters: PLOS Computational Biology readership includes control-inclined computational neuroscientists who will immediately ask how this differs from known state-feedback versus command-feedback distinctions and from classic delay-compensation results. Without that positioning the originality claim reads thin, and the conclusion risks looking like a rediscovery of a known control principle inside a fly model.
- Resolution test: Add one Introduction paragraph and one Discussion paragraph that engage the forward-model and delay-compensation literature with real citations, and state in one sentence exactly what is new relative to that canon (for example, that the dissociation is demonstrated inside a published insect-steering architecture under stress tests rather than in an abstract control setting).

### R3-M3
- Severity: Major
- Blocking: No
- Axis: biological-claim boundaries (claim overreach)
- Claim pointer: Abstract, "show that what a delayed visual loop lacks is current self-state rather than a copy of the issued command"; Results, "A goal feedforward rescues delay", "What the delayed visual loop lacks is current self-state, not a copy of the issued command and not early knowledge of the target."
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md Discussion, which correctly qualifies the same statement as "The delayed visual loop in this architecture therefore lacks current self-state", and Limitations, "The goal feedforward is an upper bound, not a mechanism claim."
- Concern: The abstract and Results state the self-state conclusion as a general fact about delayed visual loops. Only the Discussion carries the architecture qualifier. The experiment establishes the claim for one stylized two-pathway model with an instructed goal that shares amplitude and onset with the stimulus, which the Limitations correctly call an upper bound.
- Why it matters: This is the sentence most likely to be quoted in a review or a blog post. Left unqualified it overclaims beyond the model, which is exactly the boundary the rest of the manuscript works hard to hold.
- Resolution test: Add "in this model" or "in this architecture" to the abstract sentence and to the Results sentence, or reword both to attribute the claim to the assay (for example, "in this assay, the delayed visual loop lacked access to current self-state").

### R3-M4
- Severity: Major
- Blocking: No
- Axis: readability
- Claim pointer: Discussion, "We then implemented the two manipulations that a command copy alone cannot provide."
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md Discussion section order (three results, relation to source, relation to connectome literature, model limits, discarded stability analysis, then the command-copy and feedforward recap)
- Concern: The command-copy and feedforward results are headline findings in the abstract, but the Discussion recounts them only after the limitations paragraph and the stability-analysis retraction, opening with "We then implemented", which reads like Results narration continuing late. A nonspecialist reaches the paper's most novel material after reading its caveats.
- Why it matters: For a broad computational-neuroscience readership the narrative order currently signals that the feedforward result is an afterthought, when it is the paper's most distinctive contribution.
- Resolution test: Move the command-copy and feedforward paragraph ahead of the limitations, rewrite it in discussion voice rather than results narration, and confirm that limitations and the stability-analysis note close the Discussion.

### R3-M5
- Severity: Major
- Blocking: No
- Axis: technical soundness (journal fit)
- Claim pointer: Methods, "Code and data availability", "All code is in `M2A-BRIDGE/06_JOINT/`. Outputs are in `runs/`."
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md Methods section
- Concern: The availability statement points at workspace-relative folders. PLOS Computational Biology expects a public repository with a persistent identifier in the availability statement.
- Why it matters: Without a resolvable repository the reproducibility promise of the paper cannot be checked by readers or editors, and the submission will not pass journal formatting requirements.
- Resolution test: Deposit code and the summary outputs cited in the claim map in a public repository with a DOI, update the statement to cite it, and retain the existing note that the source repository has no license and only equations were ported.

---

## Minor Comments

### R3-m1
- Axis: technical soundness
- Affected element: References 4, 5, 6, 7, 11, 12
- Issue: Erginkaya, Lappalainen, Wang-Chen, Westeinde, von Holst and Mittelstaedt, and Dhiman appear only in the reference list, never in the body text (verified by full-text search of MANUSCRIPT_REVISED.md).
- Required correction: Cite each in the relevant passage or remove it. The absence of an in-text citation for von Holst and Mittelstaedt is conspicuous in a paper about the reafference principle.

### R3-m2
- Axis: readability
- Affected element: Results, "Predictions"
- Issue: The text says "The model makes five predictions" but lists four numbered predictions, then describes two more in prose (the command-copy negative prediction and the feedforward positive one), for six total if counted naively.
- Required correction: Reconcile the count. Either number all predictions consistently or reword to "four numbered predictions plus two qualitative ones".

### R3-m3
- Axis: technical soundness
- Affected element: Discussion, "graded cancellation at a gain of 0.5 is 0.15% sensitive" against Results, "about 0.3% sensitive (59.923 versus 59.770 degrees)"
- Issue: The two sections report different percentages for the same comparison. The absolute difference of 0.153 degrees appears to have been labeled as a percent in the Discussion.
- Required correction: Compute one figure with one convention and use it in both sections.

### R3-m4
- Axis: readability
- Affected element: Abstract
- Issue: The abstract is roughly 380 words and dense with failure percentages, and it uses "V-term treatments" and "bar-torque scale" before either term is defined anywhere in the abstract. Broad readership readers will stall on both.
- Required correction: Trim to the three headline results plus the feedforward finding, define or replace the V-term wording with plain language such as "velocity nonlinearity shape", and check the length against the journal's abstract limit at submission.

### R3-m5
- Axis: readability
- Affected element: run artifact names (graded_motor, allnone_motor) and claim map C3/C14 wording against manuscript text
- Issue: The manuscript explicitly renames these signals as "unfiltered" and states they are not motor copies, but the underlying run directories and two claim-map rows still use motor-copy terminology. A reader auditing artifacts will not know which name maps to which variant.
- Required correction: Add one sentence in Methods or in the figure legends giving the artifact-name to manuscript-name mapping, and align the claim map wording with the manuscript's terminology.

### R3-m6
- Axis: originality
- Affected element: Introduction, second paragraph (LT52 grooming example)
- Issue: The Hartman et al. 2025 example concerns feedback about limb movement during grooming, and it is used as evidence that the computation relevant to steering is not purely visual. The link to steering is plausible but asserted in one sentence without the bridge being spelled out.
- Required correction: Add a half-sentence explaining why limb-movement feedback in grooming is informative about reafference generally, or soften the example to a general statement that non-visual feedback reaches visual circuits.

---

## Technical failings that need to be addressed before the case is established

1. Regenerate the claim-to-evidence map so it matches the revised manuscript (R3-M1). As it stands the packet's own evidence index asserts retracted claims.
2. Resolve the 0.15 percent versus 0.3 percent inconsistency between Discussion and Results (R3-m3), and reconcile the prediction count (R3-m2).
3. Remove or cite the six uncited references (R3-m1).
4. Qualify the abstract's self-state sentence so it does not generalize beyond the model (R3-M3).
5. Replace the local-path availability statement with a public repository (R3-M5).

The core quantitative case does not need new experiments. Every headline number I checked against runs/P1-EC-GAIN-01, P1-EC-WINDOW-01, P1-EC-VCLIP-01, P1-EC-GATE-01, P1-EC-ADAPTIVE-03, P1-EC-COMMAND-01, P1-EC-FEEDFORWARD-01/02, P1-EC-GOAL-DELAY-01, P1-EC-FF-STATE-01, and P1-EC-MULTISEED-01 matched the manuscript text.

---

## Assessment against the five axes

- Originality: Moderate. The gain-inertness finding at the source's own fixed gain, the systematic window and V-clip corrections, and the command-copy versus current-self-state dissociation are useful contributions. The score is capped by the complete absence of engagement with the forward-model and delay-compensation canon (R3-M2), which is the natural comparison class for both the manipulation and the conclusion.
- Scientific importance: Moderate. The paper produces testable, concretely parameterized predictions for delayed-feedback experiments and a documented caution about model rankings under delay, but it makes no new biological discovery and its most striking claim is bounded to a stylized assay with an instructed-goal upper bound.
- Interdisciplinary readership: Good potential, partially unrealized. The topic spans fly neuroethology, sensorimotor control, and control theory, which suits PLOS Computational Biology. The dense abstract, undefined jargon, buried feedforward discussion, and missing control-theory framing currently narrow the entry path (R3-M2, R3-M4, R3-m4).
- Technical soundness: Sound within the stated scope. Spot-checks confirmed the reported rates, denominators are mostly given, statistical philosophy is explicit, and limitations are candid. Deductions for the contradictory claim map, the internal numeric inconsistency, the uncited references, and the non-resolvable availability statement (R3-M1, R3-m1, R3-m3, R3-M5).
- Readability for nonspecialists: Mixed. Scope disclaimers and the plain-language structure of Results are strengths. The abstract's number density and jargon, the Discussion's ordering, the prediction-count slip, and the artifact-naming mismatch are the main obstacles (R3-M4, R3-m2, R3-m4, R3-m5).

---

## Recommendation posture

Major revision. The simulation results are internally consistent, spot-check cleanly against the run outputs, and are bounded with unusual care, so the central case is established in substance. What is missing is readiness for this journal and this readership: the claim map must be rebuilt so it no longer asserts retracted claims, the paper must position its novelty against the forward-model and delay-compensation literature, the abstract's generalizing sentence must be qualified, two headline results must be moved up in the Discussion, and the availability statement must point at a public repository. None of these require new experiments, and all are resolvable in one focused revision. I expect the revised paper would be of real interest to the insect visuomotor and computational sensorimotor communities, and I would look favorably on a resubmission that closes these items. This is a reviewer recommendation, not an editorial decision.
