# Forensic number-consistency audit — MANUSCRIPT_DRAFT_V2.md (new/rewritten content only)

- Manuscript: `08_MANUSCRIPT/SUBJOURNAL_PACKAGE/MANUSCRIPT_DRAFT_V2.md`
- Artifacts read: `runs/P2-OBSERVER-02`, `runs/W1-REVISION-01`, `runs/P4-AI-01`, `runs/W3-INJECT-01`, `runs/P3-RAY-DISCRIM-01`, `runs/P3-RAY-DISCRIM-02` (`experiment/outputs/summary.json`), claim map `08_MANUSCRIPT/TRACK_C_EC_DELAY/CLAIM_TO_EVIDENCE_MAP.csv`
- Methods: SHA-256 recomputed with `shasum -a 256` for the seven named preregistration files; injection p-values recomputed from `mean_dll_by_seed` using the artifact's own detection rule (exact one-sided paired sign-flip, 2^20 enumerations, beta vs beta=0, 20 seeds); figure files checked in `08_MANUSCRIPT/SUBJOURNAL_PACKAGE/figs/`.
- Verdicts: **pass** = claimed number matches artifact; **error** = contradicts artifact or missing required element; **not assessable** = claim not verifiable from the named artifact.

## Checks

| Check | Claimed | Artifact | Verdict | Fix |
| --- | --- | --- | --- | --- |
| R3/1.1 First-pass PD failure rate | 3 of 8 to 5 of 8 (38-62%) at every delay 50-200 ms (line 127; Fig. 15 legend; C40) | P2-OBSERVER-02 `pd_instant`: 3/8 (37.5%) @50 ms, 5/8 (62.5%) @100 ms, 4/8 (50%) @140 ms, 4/8 @200 ms; identical at noise 0 and 1e-13 | pass | — |
| R3/1.2 pd_gate zero failures | pd_gate failed in none of 8 parameter sets at any delay 50-200 ms (line 129; Fig. 15; C47) | W1: `pd_gate (instant PD + gate)` = 0/8 at 50/100/140/200 ms, both noise levels | pass | — |
| R3/1.3 PD gain sweep | robust to proportional-gain sweep one-half to five times base (line 129) | W1: `pd_instant removed + p_gain x0.5 / x2 / x5` all 0/8 at every delay, both noise levels | pass | — |
| R3/1.4 Delay-embedding observer | smith_dde fails 8 of 8 at every delay incl. 50 ms, exact and 10% mismatch (line 129; Fig. 15; C48) | W1: `smith_dde exact` and `smith_dde 10pct mismatch` both 8/8 at all 4 delays, both noise levels | pass | — |
| R3/1.5 Gate-disabled ablation | failure rises to 88-100% / 7-of-8 to 8-of-8 (line 131; C49) | W1: `gate_goal, gate disabled` = 7/8, 7/8, 8/8, 8/8 (87.5-100%) | pass | 87.5% rounds to 88%; acceptable |
| R3/1.6 Bar-drive trigger | triggering gate on |F_bar| alone preserves 0% at all delays (line 131; C49) | W1: `gate_goal, trigger on F_bar only` = 0/8 at every delay, both noise | pass | — |
| R3/1.7 Undelayed self-state | addition / graded / gate all 0% with current psi/omega; delayed-reference addition fails 100% (line 131; C50) | W1 `d_undelayed_selfstate`: three undelayed variants 0/8 everywhere; `addition (delayed reference)` 8/8 everywhere | pass | — |
| R3/1.8 Boundary multi-seed | gate-goal feedforward 0% through 500 ms across three seeds (line 133; C51); gate filtered at 75% | W1 `e_multiseed_boundary`: gate goal ff=1 0/8, seeds=3, at 250/300/400/500 ms; gate filtered 6/8 (75%) at all four | pass | — |
| R3/1.9 Fig. 15 legend Taylor attribution | "Taylor feedforward and naive forward-model observer fail from 50-100 ms (P2-OBSERVER-02)" | P2-OBSERVER-02 has no Taylor/predicted-state rows (models: addition, allnone, gate_goal instant-ref, pd_instant, smith, smith_pert). Predicted-state/Taylor data is in P1-EC-OBSERVER-01 (`gate goal, predicted state`: 0% @20 ms, 50% @50 ms, 100% @100 ms+, per C37) | error | Re-attribute Taylor to `runs/P1-EC-OBSERVER-01` in the Fig. 15 legend, or drop Taylor from that data line |
| AI/2.1 Critical delay C | C = 200/50/200 ms (T1/T2/T3); text "C and E1 crossed 50% failure between 50 and 200 ms" (line 164) | P4 `critical_delay_ms`: T1 200, T2 50, T3 200 | pass | — |
| AI/2.2 Critical delay E1 | E1 = 200/50/200 ms | T1 200, T2 50, T3 200 | pass | — |
| AI/2.3 Critical delay E2 | E2 = 300/150/300 ms; "critical delays of 150-300 ms" (line 164) | T1 300, T2 150, T3 300 | pass | — |
| AI/2.4 Critical delay E2m | E2m = 300/300/300 ms; "never worse than the exact-model version" (line 164) | T1 300, T2 300, T3 300; vs E2 (300/150/300): never worse ✓ | pass | — |
| AI/2.5 Family F stability | F null/null/null; "0% failure at every grid point" through 600 ms (line 164) | All 24 F rows (3 tasks × 8 delays 0-600 ms) failure_rate = 0; critical_delay F = null for all tasks | pass | — |
| AI/2.6 Critical delay Fplus | Fplus = 400/150/400 ms; text "critical delays of 150-400 ms" (line 164; C54) | T1 400, T2 150, T3 400 | pass | — |
| AI/2.7 Recovery times @150 ms | F ~0.36-0.47 s vs C 2.7/4.1 s at 150 ms | At 150 ms: F median recovery T1 0.455 s, T3 0.465 s (both inside 0.36-0.47); T2 1.365 s (only 2 survivors, outside range). C: T1 3.08 s, T3 3.30 s (both inside 2.7-4.1); T2 0 survivors (undefined) | pass | Numbers appear only in `reviews/RESPONSE_TO_REVIEWERS.md:115`, not in the manuscript (which defers to artifacts). Scope the range to T1/T3 (or note n_survivors) because the T2 F median (1.365 s) falls outside 0.36-0.47 |
| AI/2.8 Preregistration hash | "preregistration SHA-256 6e56c187" (line 162) | `shasum -a 256 runs/P4-AI-01/PREREGISTRATION.md` = `6e56c187098d…` | pass | — |
| AI/2.9 Design numbers | three tasks, 30 randomized plants, 8-point grid 0-600 ms, six controller families (line 162) | tasks T1-T3 (3); n_plants = 30; delays [0,50,100,150,200,300,400,600] (8); families C, E1, E2, E2m, F, Fplus (6) | pass | — |
| AI/2.10 "Non-effect of mismatch" wording | "an unexpected non-effect of mismatch" (line 164) | E2 = 300/150/300 vs E2m = 300/300/300: at T2 the mismatch variant CHANGED the critical delay 150 → 300 ms (beneficial); T1/T3 unchanged. There is an effect at T2 — it is a no-harm effect, not a non-effect | error | Reword: "identical at T1/T3 and higher at T2 (300 vs 150) — never worse" (matches claim-map C55 "does not consistently help") |
| AI/2.11 Claim citation | "(Fig. 23; C53-C55)" (line 164) | Claim map: C53 = injection-recovery (Fig. 22, W3-INJECT-01); only C54/C55 concern the transfer (Fig. 23). Line 157 already cites C53 correctly for injection | error | Change to "(Fig. 23; C54-C55)" |
| INJ/3.1 Threshold p-value | beta = 8, p = 0.020, same-seed paired sign-flip (line 157; C53) | Recomputed exact one-sided sign-flip from `results[8.0].mean_dll_by_seed` vs beta=0: p = 0.02005 | pass | — |
| INJ/3.2 Robust-recovery p-value | beta >= 16, p <= 4e-5 (line 157; C53) | Recomputed: beta 16 p = 4.48e-5 (47/2^20) — strictly greater than 4e-5; beta 32 and 64 p = 9.54e-7 | error | Change to "p <= 5e-5" (or state "p = 4.5e-5 at 16; 9.5e-7 at >=32") in manuscript AND claim-map C53 |
| INJ/3.3 Seed recovery fraction | 90-100% of 20 injection seeds at beta >= 16 | `frac_positive_mean`: beta 16 = 0.98, 32 = 0.98, 64 = 1.0 (i.e., 98-100%, over 5 sessions x 20 seeds) | pass | Actual envelope is 98-100%; "90-100%" is a true but loose bound — consider "98-100%" |
| INJ/3.4 Undetected small effects | beta <= 4 undetected at five sessions (line 157; C53) | Recomputed: beta 1 p = 0.814, beta 4 p = 0.442 (both > 0.05); W3 runs on 5 control sessions (matches R2 pseudo_pulse_n_sessions = 5) | pass | — |
| INJ/3.5 Variance share | beta <= 4 "below 1% of residual variance" (line 157; C53) | No residual-variance field in W3-INJECT-01/experiment/outputs/summary.json | not assessable | Cite the source for the 1% figure (code/config) or drop the clause |
| CM/4.1 Claim map C53 | beta=8 p=0.020; beta>=16 p<=4e-5; beta<=4 undetectable at five sessions; Fig22; W3-INJECT-01 | p(8) = 0.02005 ✓; p(16) = 4.48e-5 ✗ (>4e-5); p(1), p(4) = 0.81/0.44 ✓; artifact path ✓ | error | Same fix as INJ/3.2 in `CLAIM_TO_EVIDENCE_MAP.csv` row C53 |
| CM/4.2 Claim map C54 | F 0% at every delay 0-600 ms; C and E1 cross at 50-200 ms; stacking degrades fresh family to 150-400 ms; Fig23; P4-AI-01 | F max failure 0 ✓; C/E1 critical = 200/50/200 (range 50-200) ✓; Fplus = 400/150/400 (range 150-400) ✓ | pass | — |
| CM/4.3 Claim map C55 | E2 critical 150-300 ms; mismatch does not consistently help; zero-delay C/F identity verified; Fig23; P4-AI-01 | E2 = 300/150/300 (range 150-300) ✓; E2m vs E2: equal T1/T3, 300 vs 150 at T2 → helps only sometimes ✓; at delay 0 C and F both 0% failure in all three tasks ✓ | pass | — |
| SHA/5.1 P3-ROUND-2 prereg | prefix 9563d8c2 ("model graded-vs-gated selection") | `shasum -a 256 runs/P3-ROUND-2/PREREGISTRATION.md` = `9563d8c20947…` | pass | — |
| SHA/5.2 P3-VISORIENT-01 prereg | prefix 75cc2434 ("sealed Currier antenna-stabilized round") | `75cc24343970…` | pass | — |
| SHA/5.3 P3-RAY-DISCRIM-01 prereg | prefix 06813365 ("discrimination round one") | `068133659d72…` | pass | — |
| SHA/5.4 P3-RAY-DISCRIM-02 prereg | prefix 668e066a ("discrimination round two") | `668e066a8643…` (also embedded in R2 artifact guards: "668e066a...483e") | pass | — |
| SHA/5.5 COMPETING_MECHANISMS_PREREG | prefix b7e0e5d6 ("competing-mechanism framework and amendment A1") | `b7e0e5d6d7ee…` | pass | — |
| SHA/5.6 P3_F_LOCK | prefix 339dfbf3 ("F&S prediction protocol lock") | `339dfbf3bded…` | pass | — |
| SHA/5.7 P4-AI-01 prereg | prefix 6e56c187 | `6e56c187098d…` | pass | — |
| SHA/5.8 c4eb583f | "visual-integration exploration / exploratory turn-manifest (c4eb583f)" | File not among the seven named files and not located for recompute within this audit | not assessable | Provide the frozen file path so the prefix can be re-verified |
| SHA/5.9 6496b3f2 | "original freeze 6496b3f2 pre-amendment" | File not among the seven named files and not located for recompute within this audit | not assessable | Provide the pre-amendment file path for re-verification |
| R6/6.1 Control floor, round 1 | pseudo-pulse floor +20.1 (line 153; Fig. 22) | P3-RAY-DISCRIM-01 `negative_controls.pseudo_pulse_control.median_delta_ll` = 20.1496 | pass | — |
| R6/6.2 Control floor, round 2 | residual floor fell to +6.9 (line 155; Fig. 22) | P3-RAY-DISCRIM-02 `controls.pseudo_pulse_median_delta_ll` = 6.8842 | pass | — |
| R6/6.3 Main effect, round 1 | main +28.1 (line 153; Fig. 22) | `median_delta_ll_behavior` = 28.0866 | pass | — |
| R6/6.4 Main effect, round 2 | median +8.6, 6/6 animals positive (line 155; Fig. 22) | 8.5695; per-animal deltas all > 0 (6/6) | pass | — |
| R6/6.5 Net excess | net +1.7 (lines 155, 192) | 8.5695 − 6.8842 = 1.6853 | pass | — |
| R6/6.6 Supporting p-values/counts | R1: p = 0.031, 5 of 6 positive; R2: p = 1/64, 6 of 6 (lines 153, 155) | R1 p = 0.03125, 5/6 positive; R2 p = 0.015625 = 1/64, 6/6 positive | pass | — |
| FIG/7.1 Legends for Fig. 15, 19, 20, 21, 22 | Legends present in "Figure legends" section | Present: Figure 15 (line 381), 19 (383), 20 (385), 21 (387), 22 (389) | pass | — |
| FIG/7.2 Fig. 16 legend | Referenced at line 131 ("Fig. 16; C49, C50") | No "Figure 16" legend anywhere in the manuscript | error | Add a Figure 16 legend (ablation: gate-disabled / bar-trigger / undelayed self-state; data runs/W1-REVISION-01) |
| FIG/7.3 Fig. 23 legend | Referenced at lines 162 and 164 ("Fig. 23") | No "Figure 23" legend anywhere in the manuscript | error | Add a Figure 23 legend (AI transfer critical delays/recovery; data runs/P4-AI-01) |
| FIG/7.4 New figure files exist | fig15_classical.png, fig16_ablation.png, fig19_benchmark.png, fig20_modelselect.png, fig21_fs_forest.png, fig22_discrimination.png, fig23_transfer.png | All 7 present in `SUBJOURNAL_PACKAGE/figs/` (each with a matching .pdf) | pass | — |

## Counts

- Total checks: **47**
- pass: **37**
- error: **7** (R3/1.9 Taylor attribution; AI/2.10 "non-effect of mismatch" wording; AI/2.11 C53-C55 citation; INJ/3.2 p<=4e-5 bound; CM/4.1 C53 row inherits that bound; FIG/7.2 missing Fig. 16 legend; FIG/7.3 missing Fig. 23 legend)
- not assessable: **3** (INJ/3.5 "<1% of residual variance"; SHA/5.8 c4eb583f; SHA/5.9 6496b3f2)
