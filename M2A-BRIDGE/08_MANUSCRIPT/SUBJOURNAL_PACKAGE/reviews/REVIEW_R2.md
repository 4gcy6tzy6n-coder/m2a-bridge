# Reviewer 2 (lens: empirical/statistical rigor)

## Overall assessment

This manuscript couples a computational necessity-structure claim (fresh self-state in a fast path, with gating of the delayed visual pathway, stabilizes a delayed steering model) to an empirical layer spanning four public neural-behavioral datasets, in which every confirmatory outcome is reported regardless of direction. Judged strictly on empirical and statistical rigor, the empirical layer is unusually honest: preregistrations with frozen hashes are listed, negative controls are allowed to overrule significant primary endpoints (C45), an inconclusive model selection is reported as inconclusive under a preregistered resolution rule (C43), and the one borderline-positive result (C44, p=0.0503, CI crossing zero) carries an explicit claim ceiling ("additional predictive information only"). The claim-to-evidence map (C1–C46) is itself a model of transparency, retaining retired claims (`retired_pre_revision`) and caveats per row.

That said, three items must be resolved before the empirical layer can be said to match its evidence exactly: (1) the abstract's "four public neural-behavioral datasets" versus the three datasets enumerated in Methods, with a "sealed antenna-stabilized round" mentioned only in the preregistration list; (2) the governance of the C44 interpretation — the claim map's "owner stage-gate pass D12" and the manuscript's "by prior agreement" are not assessable from the packet and must be documented; and (3) the C46 statistic reported for the residual excess (p=1/64 for positivity) is not the statistic that addresses pulse-specificity, given a control floor of +6.88. None of these is individually blocking for the paper's central (computational) case, which stands on the model layer; all are required for the empirical layer's claims to be exactly coextensive with its evidence.

## Who would be interested and why

- Computational neuroscientists and control theorists working on sensorimotor delay, efference copy, and observer architectures: the matched-budget classical and observer comparators (C37, C39, C40) and their explicit limits are directly reusable.
- Experimentalists designing state-dependent perturbation experiments (optogenetics and beyond): the pseudo-pulse control and residual pipeline (C45/C46) offer a concrete, quantified confound and a reusable control suite.
- Researchers using the Tanaka/Clark counter-evidence dataset and the HS and walking-steering datasets: the fly-level reproduction (C42) and the documented resolution limits at n=6–19 constrain future analyses.
- Methodologists interested in preregistered negative and inconclusive results: the retained retired claims and the enforced specificity threshold make this a usable case study.

## Major strengths

1. Preregistration discipline with an audit trail. Methods ("Statistics and preregistration") list seven preregistrations with SHA-256 prefixes, including a documented amendment ("competing-mechanism framework and amendment A1 (b7e0e5d6, original freeze 6496b3f2 pre-amendment)"). Exploratory analyses are labeled as such (Discussion, Limitations).
2. Negative controls that decide interpretation, not just decorate it. In round 1 of the intervention analysis (C45), the primary endpoint "passed its statistical threshold (5 of 6 animals positive; exact sign-flip p=0.031)" but was correctly defeated by the pseudo-pulse control (+20.1 in unstimulated controls versus +28.1 main effect). In round 2 (C46), a positive consistency result (6/6 animals, p=1/64) was reported as NOT established because it failed a preregistered three-fold specificity threshold. This is exactly the right ordering of evidence over desire.
3. The inconclusive result is reported as inconclusive. C43: "INCONCLUSIVE_BY_RESOLUTION at n=19: ... p=0.534, minimum detectable |delta|=0.454", with the exploration-phase gap "recorded as a fitting artifact". The manuscript explicitly refuses to read this as equivalence — "the available sample cannot discriminate the shape families — and not as evidence for either side". No p>0.05 equivalence fallacy anywhere in the empirical layer.
4. Interpretation ceiling on C44 is enforced in the abstract ("reported as additional predictive information only"), Results ("nothing more... not a mechanism discovery"), Fig. 7 legend ("Claim ceiling: additional predictive information only"), and Discussion ("Correlational predictive information, however carefully controlled, is not circuit causality, and we do not present it as such"). Prediction-information-is-not-causation is, in wording, consistently held.
5. Animal-level statistics throughout. Methods: "independent unit = animal throughout; ROIs, time windows, and trials were never counted as independent samples". Exact sign-flip / label-shuffle permutation tests at the animal level; n=6 limitation disclosed with "all intervention animals available were used".
6. Self-correction on the model layer is documented rather than buried: the 140 ms "window artifact" (C23), the criterion-dependent gating boundary (C33), the non-reproduction of the source's zero-delay ranking (C12), and retired claims C1–C3, C9, C15–C17 are all visible in the claim map with `retired_pre_revision` status.
7. Resolution honesty: the minimum detectable effect for C43, the control floor for C46, the negative held-out baselines for C44 ("held-out variance-explained baselines were strongly negative"), and the ensemble (not single-run) status of boundary-region failure rates (C38) are all disclosed.

## Major Concerns

### R2-M1
- Severity: Major
- Blocking: No
- Axis: Sample-size / scope honesty
- Claim pointer: Abstract — "tested the empirical boundaries of these claims across four public neural-behavioral datasets"; Introduction — the three-layer plan enumerates three datasets ("a visual counter-evidence dataset... simultaneous HS-cell intracellular recordings... and a walking-steering dataset")
- Evidence pointer: Manuscript Methods, "Public datasets and qualification" — enumerates exactly three datasets, (i) Counter-evidence (Dryad bcc2fqzjz), (ii) Flight HS (Edmond doi:10.17617/3.92), (iii) Walking steering (Harvard Dataverse doi:10.7910/DVN/0NCLP1). Methods, "Statistics and preregistration" — "the sealed antenna-stabilized round (75cc2434)" is listed with no corresponding Results section or dataset description. Claim map C42–C46 cover only datasets (i)–(iii).
- Concern: The abstract and framing claim four datasets; the manuscript describes three. The only candidate for a fourth is the "sealed antenna-stabilized round", which appears once, in the preregistration list, with no data, no results, and no qualification statement. Either the count is wrong, or a dataset (and its status) is missing from the record.
- Why it matters: Dataset count is a scope claim a reviewer and reader verify first; an unaccounted fourth dataset — especially one labeled "sealed" — invites the reading that a dataset was acquired but its (presumably null or unanalyzed) result is being silently omitted, which would undercut the paper's otherwise exemplary report-everything ethos.
- Resolution test: Either change the abstract/intro to "three public datasets" and remove the fourth-dataset framing, or add the sealed round's dataset to Methods with its qualification, its preregistration hash, and an explicit statement of what was (not) analyzed and why (e.g., sealed prospective round, no outcome yet). Not assessable from the packet which is correct; the text must make it assessable.

### R2-M2
- Severity: Major
- Blocking: No
- Axis: Preregistration discipline / interpretation governance (C44)
- Claim pointer: C44 — "9/12 animals positive; median dR2=+0.056; exact sign-flip p=0.0503; CI95 crosses zero; owner stage-gate pass D12 with numbers on record". Abstract — "past motor history carried a small, consistent incremental predictive signal for neural activity (9/12 animals; p=0.0503, confidence interval crossing zero)". Results, Empirical layer II — "We record these numbers unchanged and interpret them, by prior agreement, as evidence that observable motor history carries additional predictive information".
- Evidence pointer: Manuscript Results, Empirical layer II; claim map row C44; Methods preregistration list ("F&S prediction protocol lock (339dfbf3)") — the packet does not show whether the interpretive rule is inside that lock.
- Concern: The entire positive framing of C44 rests on a decision rule ("by prior agreement", claim map: "owner stage-gate pass D12") whose criteria and freeze time relative to data access are not assessable from these two files. By conventional standards this is a null-convergent result: p=0.0503, CI crossing zero, 9/12 animals (a plain one-sided sign test on 9/12 gives p≈0.073). The manuscript's claim ceiling is correct, but two residual issues remain: (a) a reader cannot verify that "pass" applied a pre-specified rule rather than a borderline-result judgment call; (b) the abstract's word "consistent" characterizes 9/12 with a CI crossing zero — the counts immediately following are honest, but the adjective leans.
- Why it matters: This is the paper's most quotable empirical number. If the stage-gate rule was fixed after seeing p=0.0503, the "additional predictive information" frame is post-hoc; if fixed before, it is exemplary. The difference is invisible in the packet, and the claim map's internal-governance phrasing ("owner stage-gate pass") will read to an editor as an internal memo reference, not evidence.
- Resolution test: Quote the D12 rule verbatim in the Methods or supplement, with its freeze timestamp relative to first analysis of P3-F-F2-01, and state whether the C44 test was one-sided (preregistered direction) or two-sided. In the claim map, replace "owner stage-gate pass D12 with numbers on record" with the rule's substance. In the abstract, prefer "9/12 animals" over "consistent".

### R2-M3
- Severity: Major
- Blocking: No
- Axis: Negative controls / the statistic matching the claim (C46)
- Claim pointer: C46 — "a consistent positive excess remains (6/6 animals, median +8.57, p=1/64), below the preregistered 3x specificity threshold; perturbation-specific state dependence NOT established". Results, Empirical layer II round 2 — "The real-pulse residuals still carried a small, remarkably consistent excess — positive in all six animals, median +8.6, p=1/64, the smallest attainable value". Discussion — "The residual excess above the pseudo-pulse floor (+2 to +5 log-likelihood units per animal in our data) is the effect size against which intervention datasets must now be powered."
- Evidence pointer: Manuscript Results, Empirical layer II (round 2); Fig. 8 legend; claim map row C46 (artifact: runs/P3-RAY-DISCRIM-02).
- Concern: The reported p=1/64 tests that real-pulse residuals are positive — but the control arm establishes that residuals are generically positive (control floor +6.88). The claim-relevant comparison is real versus control residual gain per animal; no animal-level paired test or interval for that difference is reported (the difference of medians is +8.6 − 6.88 ≈ +1.7, i.e., ~1.25×, far under the 3× threshold). The narrative weight falls on the consistency statistic, which the floor largely explains, and the Discussion then promotes this sub-threshold excess to the effect size "against which intervention datasets must now be powered". Powering a future study on an effect that did not clear its own preregistered threshold — and on a raw rather than net effect — is statistically unsound. Separately, the Discussion's "+2 to +5 log-likelihood units per animal" is not reconcilable from the packet with the reported medians (implying a median excess near +1.7); see R2-m1.
- Why it matters: The paper's conclusion ("not established") is correct and commendable; the danger is downstream reuse. As written, the "candidate signal" and its magnitude can be cited as if a pulse-specific effect had been measured, when what was measured is (a) generic-positive residuals and (b) a net excess that failed the specificity rule.
- Resolution test: Add an animal-level paired comparison of real versus pseudo-pulse residual gains (or an explicit statement that no such test was powered/designed), report the net excess with an interval, and re-anchor the Discussion's power recommendation on the net excess with uncertainty — or drop the "must now be powered" formulation. Explicitly state that p=1/64 tests positivity above zero, not specificity above the floor.

## Minor Comments

### R2-m1
- Axis: Internal numeric consistency
- Affected element: Discussion, "Predictions" paragraph — "(+2 to +5 log-likelihood units per animal in our data)"
- Evidence pointer: Results, Empirical layer II round 2 — median +8.6 (real) versus floor +6.88 (control)
- Issue: The stated per-animal excess range cannot be reconciled with the reported medians from the packet; the median-of-medians excess is ≈ +1.7, not +2 to +5.
- Required correction: State whether "+2 to +5" is the range of per-animal (real − control) differences, give the per-animal values or their range explicitly, or correct the number to match the reported medians.

### R2-m2
- Axis: Presentation / claim-to-figure traceability
- Affected element: Figure legends block and the "Figure N (new)" block
- Evidence pointer: Manuscript — model legends "Fig. 3", "Fig. 5", "Fig. 6", "Fig. 7", "Fig. 8" collide with empirical legends "Figure 3 (new)", "Figure 5 (new)", "Figure 6 (new)", "Figure 7 (new)", "Figure 8 (new)"; Results citations ("Fig. 5; C42", "Fig. 6; C43", "Fig. 7; C44", "Fig. 8; C45/C46") are ambiguous as written.
- Issue: Two distinct figure numbering schemes overlap; claim-to-figure pointers cannot be resolved unambiguously from the text.
- Required correction: Renumber to a single scheme (e.g., model Figs. 1–14, empirical Figs. 15–19, or panel-suffixed) and update all in-text and claim-map figure pointers.

### R2-m3
- Axis: Reference completeness
- Affected element: Reference 21 — "[Counter-evidence dataset paper — Clark laboratory, *Curr Biol* (2023); exact author list and DOI to be inserted at submission — data: Dryad bcc2fqzjz]"
- Evidence pointer: Manuscript reference list; claim map C42, C43 (dataset: Tanaka and Clark)
- Issue: The anchor citation for empirical Layer I is a placeholder; the dataset is also referred to in prose as "Tanaka and Clark" without a numbered citation.
- Required correction: Insert the full citation before submission and cite it at first mention in Results.

### R2-m4
- Axis: Sample-size / resolution honesty (C43)
- Affected element: Results, Empirical layer I — "a minimum detectable effect of 0.454, at n=19 flies"
- Evidence pointer: Claim map C43 (status: current; caveat: "resolution-limited; no directional claim"); Fig. 6 legend
- Issue: The packet does not show how the MDE was computed (bootstrap power curve? parametric-bootstrap quantile?) nor whether n=19 was all available flies or a subset. The MDE (~0.454) is roughly five times the observed effect (−0.091), meaning the design had essentially no chance of resolution at this n — this should be stated as such.
- Required correction: Define the MDE computation in Methods/supplement; state whether n=19 exhausted the dataset; add one sentence noting that the inconclusive outcome was near-certain at this sample size given the MDE.

### R2-m5
- Axis: Interpretation ceiling (absence-based localization)
- Affected element: Abstract — "localized stationary-pattern suppression away from elementary motion detectors and measured LPTC"; Results, Empirical layer I — "localizing behavioral counter-evidence suppression downstream of the measured stages"
- Evidence pointer: Claim map C42 — "LPTC shows no consistent stationary suppression across five cell types, matching the published claim"; strength "strong", caveat "pipeline validation on same-source data"
- Issue: Localization by absence requires bounds on what suppression magnitudes can be excluded at the measured stages; only "no consistent suppression" is reported. As a reproduction of the source paper's claim this is acceptable, but the manuscript's active-voice verbs ("localized", "localizing") claim more than the null supports.
- Required correction: Attribute the localization explicitly to the source paper ("consistent with the source's localization"), and, if the packet allows, report an exclusion bound (e.g., the largest per-fly suppression consistent with the data) rather than only absence of consistency.

### R2-m6
- Axis: Interpretation ceiling (prediction wording)
- Affected element: Discussion, "Predictions" paragraph — "the effect should replicate at a similar or larger magnitude"
- Evidence pointer: C44 (p=0.0503, CI95 crosses zero)
- Issue: A directional replication prediction of "similar or larger" magnitude is over-anchored for an effect whose CI crosses zero; a genuine replication could well be smaller.
- Required correction: Reword to a directional-positive, magnitude-open prediction (e.g., "should replicate as a positive increment, with magnitude to be re-estimated").

### R2-m7
- Axis: Claim-map hygiene
- Affected element: Claim map C37 (status field empty); C7 and C8 (artifact pointer: "MANUSCRIPT_REVISED.md")
- Evidence pointer: /Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/CLAIM_TO_EVIDENCE_MAP.csv
- Issue: C37's status is missing, and C7/C8 point to a manuscript filename that is not the current draft (MANUSCRIPT_DRAFT_V2.md), so those interpretive-boundary claims cannot be located in the submitted text.
- Required correction: Fill C37's status; repoint C7/C8 to the current draft's Discussion/Limitations sections.

### R2-m8
- Axis: Sample-size honesty (model layer, 0% cells)
- Affected element: Results — "gate goal at ff_gain = 1.0 stays at 0% failure at every delay" (long-delay, C27); phase diagram (C30); several supporting sweeps
- Evidence pointer: Claim map C27, C28, C29, C30, C32, C34, C35, C36 — each caveated "1 seed, 8 parameter sets" (multi-seed confirmation at gain 1.0 exists only for the C21 combinations); Fig. 9/13/14 legends ("n = 8 per cell")
- Issue: 0-of-8 (or 0-of-24) cells are reported as "0% failure" with no uncertainty statement; by the rule of three, 0/24 still permits ~12.5% failure rate over the sampled ensemble. Several boundary claims (500 ms ceiling, phase-diagram extent) rest on single-seed grids, and this limitation appears in the claim map but not always in the manuscript prose.
- Required correction: Add rule-of-three (or exact binomial) upper bounds for 0% cells in the supplement, and mark single-seed sweeps as single-seed in the Results text where the boundary claims are made.

## Technical failings that need to be addressed before the case is established

The central computational case does not depend on the empirical layer and is not blocked by anything in this review. For the empirical layer to be established exactly as claimed, the following are required:

1. Reconcile "four public datasets" with the three enumerated in Methods, and state the status of the "sealed antenna-stabilized round" (R2-M1).
2. Disclose the C44 stage-gate rule (D12) verbatim with its freeze timing relative to data access, and state the preregistered sidedness of the C44 test (R2-M2).
3. Report or explicitly decline an animal-level real-versus-control residual comparison for C46, and re-anchor the Discussion's effect-size/power statement on the net (floor-subtracted) excess with uncertainty (R2-M3, R2-m1).
4. Resolve the "+2 to +5" versus ≈+1.7 excess inconsistency (R2-m1).
5. Complete reference 21 and unify figure numbering so claim-to-figure pointers are unambiguous (R2-m2, R2-m3).

## Assessment against Nature Machine Intelligence criteria

- Significance: The methodological contribution (the pseudo-pulse control and residual pipeline, C45/C46, presented as "one methodological result with a candidate signal attached") is of real interest to the growing audience running state-dependent perturbation analyses, and the model's freshness threshold (20–30 ms, C36) is a concrete, falsifiable target. The empirical layer carries appropriate weight precisely because it claims to map boundaries rather than mechanisms.
- Rigor: Strong overall — preregistration with hashes, animal-level statistics, controls that overrule primary endpoints, and enforced claim ceilings. The three Major concerns are governance/disclosure and statistic-matching issues, not fabricated or p-hacked results; notably, no p>0.05 equivalence claim appears anywhere, and the one "significant" consistency statistic (p=1/64) is correctly subordinated to a failed specificity threshold in the conclusion.
- Originality: The combination of a necessity-structure model with preregistered, control-decided empirical boundary tests on existing public data is unusual and, in my view, publishable in principle; the novelty of the empirical layer is the control methodology, not a discovered mechanism — the manuscript says so itself.
- Clarity / transparency: The claim-to-evidence map is a strong asset; figure numbering and the fourth-dataset ambiguity are the clarity deficits.
- Scope of claims: "Prediction information is not causation" is enforced in the abstract, Results, figure legends, and Discussion. The remaining over-weights are the abstract's "consistent" (R2-M2), the localization verbs (R2-m5), and the Discussion's power-target statement (R2-M3) — all fixable by wording.

## Recommendation posture

Major revision. I have no Blocking Yes concerns: the central computational case is established within its stated model scope, and the empirical layer's conclusions (inconclusive at n=19; predictive-information-only at p=0.0503; perturbation-specific state dependence not established at n=6) are, as worded, matched to their evidence. What prevents acceptance as-is is the unresolved dataset-count discrepancy (R2-M1), the undisclosed governance behind the C44 framing (R2-M2), and the floor-versus-excess statistic behind the C46 effect-size claim (R2-M3). If these three are resolved as specified — and the minor items cleaned — I would support publication at Nature Machine Intelligence as a methodologically exemplary boundary-map study, provided the title/abstract continue to avoid implying biological mechanism. Reviewer confidence is high on the textual and statistical points above; items marked not assessable from the packet (D12 freeze timing, MDE computation, per-animal residual values, sidedness of the C44 test, existence/status of a fourth dataset) must be settled from the preregistration supplement and run artifacts before final judgment.
