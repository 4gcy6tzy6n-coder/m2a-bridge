# Submission checklist — Track C (revised)

> Status: revised after independent review. Scientific content is complete for a PLOS Computational Biology modeling paper. Owner-side author metadata and final DOI packaging remain.

## Science

- [x] Model equations ported and unit-tested (16 pytest tests).
- [x] Twenty-six gated rounds: P1 coarse, P2 noise/body, P3 1 ms fine, gain, adaptive, adaptive alpha, window, V-clip, gate threshold, adaptive gradient, command copy, feedforward, feedforward window, goal mismatch, goal delay, self-state ablation, multi-seed, adaptive ODE equivalence.
- [x] Gain sweep: source gain 0.05 inert; higher delayed-sensory gain harmful at 50 ms.
- [x] Window check: 2.5 s truncates late failures; long-delay gating advantage removed.
- [x] V-clip check: short-delay gating robust; 100 ms advantage not robust.
- [x] Gate-threshold check: short-delay gating robust from 0.01 to 0.5; 100 ms advantage not robust.
- [x] Adaptive check: signed gradient lowers the gain but does not rescue failure.
- [x] Command-copy check: a pre-plant-filter command copy matches the filtered plant state; only the current-visual oracle has lower long-delay failure.
- [x] Feedforward check: gate goal at ff_gain >= 0.5 is 0% failure through 200 ms at 6 s and 10 s windows; robust to goal mismatch; rescue requires current self-state (goal-delay and self-state ablations).
- [x] Multi-seed check: command-copy and feedforward conclusions hold across three seeds.
- [x] Adaptive ODE-equivalence check: 96/96 failure agreement between step-wise and ODE-internal weight updates.
- [x] Source check: zero-delay ranking not reproduced at a meaningful effect size; source result demoted to motivation.
- [x] Linear stability attempted but removed because delay-eigenvalue tracking was unreliable.
- [x] Claim-to-evidence map regenerated (33 rows; 7 pre-revision rows quarantined with status=retired_pre_revision; run-name to manuscript-name mapping in Methods).
- [ ] Exact reproduction of the source's adaptive solver semantics (step-wise and ODE-internal forms verified equivalent under forward Euler; declared limitation).

## Manuscript

- [x] Second independent review round complete (3 blind reports + forensic audit + synthesis); all consensus and audit findings addressed in the current manuscript.
- [x] Revised manuscript: `MANUSCRIPT_REVISED.md` (about 9,000 words including methods, 18 pages, 14 display items).
- [x] Revised PDF: `MANUSCRIPT_REVISED.pdf`.
- [x] References reconciled; the previously dangling citation now has an entry.
- [x] Cover letter rewritten for the revised title and claims.
- [x] Word and figure count checked.
- [ ] Author list, affiliations, ORCIDs, corresponding author. **Owner-side.**
- [ ] Author contributions (CRediT). **Owner-side.**
- [ ] Competing interests. **Owner-side.**
- [ ] Funding statement. **Owner-side.**
- [ ] Data/code availability statement with a persistent identifier (Zenodo DOI or repository URL). **Requires an archive account.**
- [ ] Acknowledgments. **Owner-side.**
- [ ] Suggested reviewers (optional). **Owner-side.**
- [ ] Preprint decision (bioRxiv recommended before submission). **Owner-side.**

## Figures

- [x] Fig 1 schematic: filtered and unfiltered labels; PNG + PDF.
- [x] Fig 2 gain × delay heatmap: PNG + PDF.
- [x] Fig 3 window check: PNG + PDF.
- [x] Fig 4 V-mode and gate-threshold stress: PNG + PDF.
- [x] Fig 5 adaptive updates: PNG + PDF.
- [x] Fig 6 command copy: PNG + PDF.
- [x] Fig 7 goal feedforward and mechanism controls: PNG + PDF.
- [x] Fig 8 mechanism schematic: PNG + PDF.
- [x] Fig 9 delay limits (fine grid + long delays): PNG + PDF.
- [x] Fig 10 noise robustness: PNG + PDF.
- [x] Fig 11 example trajectories and gate state: PNG + PDF.
- [x] Fig 12 failure-free curves: PNG + PDF.
- [x] Fig 13 body-parameter phase diagram: PNG + PDF.
- [x] Fig 14 self-state freshness, onset decoupling, damping control: PNG + PDF.
- [x] All figures at 220 dpi with PDF vector output.
- [x] Figure legends state n, units, and the failure definition.

## Reproducibility

- [x] Code snapshots for P1, P2, P3.
- [x] Code snapshots for gain, adaptive, window, V-clip, gate-threshold, command-copy, feedforward, window-check, goal-mismatch, goal-delay, self-state, multi-seed, adaptive-ODE, fine-delay, long-delay, noise, phase, trajectory, goal-onset, damping, and self-state-lag rounds.
- [x] `requirements-track-c.txt` covers the revised pipeline (including scipy).
- [x] `run_all.sh` uses relative paths and the P1 snapshot for the 768-row result; the P1 snapshot was verified to reproduce 768 rows.
- [x] Clean-environment tests pass (16 tests + selftests; rerun after adding scipy).
- [ ] Archive code and outputs with a DOI.

## Round-2 review findings (all addressed)

- [x] Gate-threshold claim scoped per variant; corner cell (gate unfiltered, threshold 0.5, clip) reported in text and Fig. 4 legend.
- [x] "continuous models 100% at 100 ms", "75% to 100%", "identically across three seeds", "same as the oracle", duty rounding, 0.15% vs 0.3%, prediction count — all corrected against artifacts.
- [x] Failure-criterion sensitivity reported (Methods); solver step-halving check cited.
- [x] Noise enumeration added (Methods); model-name mapping table added.
- [x] Forward-model / Smith-predictor positioning and von Holst, Westeinde, Lappalainen, Erginkaya, Wang-Chen, Dhiman citations added to body.
- [x] Superseded pre-revision figures archived to `archive_superseded_figures/`.
- [x] Availability statement notes pending DOI deposit (owner-side action remains).
- [x] Self-state proposition operationalized: freshness dose-response (20-30 ms threshold), goal-onset invariance (±200 ms), no-goal damping sufficiency (Fig. 14, claims C34-C36).

## Ethics and policy

- [x] No new animal or human data; no ethics approval needed.
- [x] Third-party code: only equations ported from Canelo et al. 2024; no source code redistributed.
- [x] Source repository has no license; only equations were ported and cited.
- [x] No text or figure copied from the source paper.
- [ ] AI-assistance disclosure if required by the journal. **Owner-side.**
