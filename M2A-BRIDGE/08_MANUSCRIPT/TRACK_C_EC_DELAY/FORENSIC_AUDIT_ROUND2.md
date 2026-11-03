# Forensic consistency audit — Round 2 (editorial pass, post-freeze)

- 日期：2026-10-27
- 依据：`nature-reviewer` 的 `forensic-consistency-audit.md`
- 隔离规则：本审计在三份报告冻结后独立执行；未回喂任何审稿人；未改动冻结报告。
- 状态枚举：confirmed_internal_error / aggregation_ambiguity / provenance_gap / suspected_duplication / unresolved_input_needed / not_assessable / passed。

## 审计记录

```yaml
- audit_id: AUD-01
  status: confirmed_internal_error
  location: Abstract; Results "The 100 ms advantage depends on the V-term treatment and gate threshold"; Discussion; Fig. 4 legend
  claim_pointer: "gating prevents failure (0%) across gate thresholds from 0.01 to 0.5" / "gating remained at 0% across every threshold"
  evidence_pointer: runs/P1-EC-GATE-01/experiment/outputs/summary.json
  check: Recomputed all cells for both models in the sweep (allnone, allnone_motor), thresholds 0.01-0.5, delays 20-140 ms, clip/smooth.
  result: allnone_motor at threshold 0.5, 50 ms, clip = 0.25 (4/16); at 100 ms, clip = 0.625 (vs allnone 0.375). The blanket 0% claim is false for the second model; make_fig_stress.py plots only allnone.
  impact: Headline abstract claim over-generalized; Fig. 4 hides the failing cell.
  resolution_test: Scope the claim per variant, report both models, add name mapping, update Fig. 4 or its legend.
  reviewer_overlap: R1-M1, R2-M2

- audit_id: AUD-02
  status: confirmed_internal_error
  location: Results "Gating prevents failure at short delays"
  claim_pointer: "The continuous models failed in 100% of runs at 100 ms."
  evidence_pointer: runs/P1-EC-WINDOW-01/experiment/outputs/summary.json
  check: graded_motor at 100 ms across windows 2.5/6/10 s = 0.625/0.75/0.75; addition = 1.0 in all.
  result: Sentence false for graded_motor (a continuous model by the paper's own taxonomy).
  impact: Direct contradiction inside the paragraph that cites this file.
  resolution_test: "Addition and graded filtered failed in 100%...; graded unfiltered failed 62.5-75%."
  reviewer_overlap: R1-M3, R2-m1

- audit_id: AUD-03
  status: confirmed_internal_error
  location: Results "The 100 ms advantage depends on the V-term treatment and gate threshold"
  claim_pointer: "At 140 and 200 ms, all variants failed in 75% to 100% under all three treatments."
  evidence_pointer: runs/P1-EC-VCLIP-01/experiment/outputs/summary.json
  check: graded_motor at 200 ms = 0.625 under clip, smooth, unclipped; allnone at 140 ms = 0.6875 clip/unclipped.
  result: Stated floor 75% is wrong; actual floor 62.5%. Also disagrees with the window section's own 68.8% for allnone at 140 ms.
  impact: Inflates the long-delay regime; two sections disagree.
  resolution_test: Restate as 62.5% to 100% or scope to named variants; cross-check with the 68.8% figure.
  reviewer_overlap: R1-M4

- audit_id: AUD-04
  status: confirmed_internal_error
  location: Results "A true command copy does not rescue delay", final sentence
  claim_pointer: "All of these rates are reproduced identically across three seeds (24 parameter-seed combinations per cell)."
  evidence_pointer: runs/P1-EC-MULTISEED-01/experiment/outputs/summary.json
  check: Per-seed rates for every model in the run.
  result: Graded command == graded filtered in all seeds (true); gate goal zeros (true). But gate filtered at 100 ms = 0/0/0.125 by seed (pooled 0.042) and at 140 ms = 0.75/0.625/0.625 (pooled 0.667); gate command = 0 and 0.75 in all seeds. "Identically" false for the gate pair.
  impact: Replication claim contradicted by its own artifact (1-2 of 16-24 runs differ).
  resolution_test: Restrict "identical" to the graded family and gate-goal zeros; report gate pair per-seed rates explicitly.
  reviewer_overlap: R1-M5, R2-M1

- audit_id: AUD-05
  status: confirmed_internal_error
  location: Results feedforward section, gate duty sequence at ff=1.0
  claim_pointer: "0.31, 0.58, 0.62, 0.65, 0.67"
  evidence_pointer: runs/P1-EC-FEEDFORWARD-01/experiment/outputs/summary.json
  check: duties = 0.3132, 0.5818, 0.6241, 0.6448, 0.6690.
  result: Fourth value rounds to 0.64, not 0.65.
  impact: Minor numerical slip in a verified paragraph.
  resolution_test: Correct to 0.64 (or state rounding convention).
  reviewer_overlap: R2-m2

- audit_id: AUD-06
  status: aggregation_ambiguity
  location: Two statements about gate filtered at 100 ms, 10 s window
  claim_pointer: window section "18.8%" (3/16) vs feedforward section "rises from 0% to 12.5%" (1/8)
  evidence_pointer: runs/P1-EC-WINDOW-01; runs/P1-EC-FEEDFORWARD-02 summaries
  check: WINDOW-01 allnone@100ms@10s = 0.1875 (n=16); FEEDFORWARD-02 gate filtered@100ms@10s = 0.125 (n=8).
  result: Both values valid for their own run; the text does not attribute them.
  impact: Reader sees two rates for "the same" condition.
  resolution_test: Attribute each rate to its run and n, or pick one canonical number.
  reviewer_overlap: R2-m4

- audit_id: AUD-07
  status: confirmed_internal_error
  location: Results adaptive section, ODE-equivalence sentence
  claim_pointer: "trajectories agree to floating-point precision until chaotic amplification in runs that diverge anyway"
  evidence_pointer: runs/P1-EC-ADAPTIVE-ODE-01/experiment/outputs/summary.json
  check: max prefix heading differences: source 20 ms = 0.205 rad; gradient 20 ms = 4.12 rad; gradient 100 ms = 2.3e-3 rad. Failure agreement = 96/96, failure-time diff = 0.
  result: Prefix differences of 0.2-4.1 rad are not floating-point precision under any ordinary reading. The load-bearing claim (failure classification and timing) holds.
  impact: Unsupported flourish beside a solid result.
  resolution_test: Delete or qualify the trajectory clause with the actual numbers.
  reviewer_overlap: R1-M6

- audit_id: AUD-08
  status: aggregation_ambiguity
  location: Abstract first result vs other runs
  claim_pointer: "75% for no efference copy" at 50 ms (gain sweep) vs 100% (window/feedforward runs)
  evidence_pointer: runs/P1-EC-GAIN-01 (noiseless, n=12, 75% = 9/12); WINDOW-01 (noise, n=16, 100%); FEEDFORWARD-01 (noise, n=8, 100%)
  check: Recomputed both.
  result: Each number correct within its own configuration; the paper does not enumerate which sweeps include noise.
  impact: First headline rests on a single noiseless configuration; baseline shifts across runs.
  resolution_test: Enumerate noisy sweeps in Methods; scope the gain claim to its configuration or add seed replication.
  reviewer_overlap: R2-M4, R1-m6

- audit_id: AUD-09
  status: confirmed_internal_error
  location: Discussion vs Results, source-protocol sensitivity
  claim_pointer: Discussion "0.15% sensitive" vs Results "about 0.3% sensitive (59.923 versus 59.770 degrees)"
  evidence_pointer: runs/../source_protocol_check.json (via manuscript); (59.923-59.770)/59.923 = 0.255%
  check: Recomputed the percentage.
  result: Results (0.3%) is correct; Discussion (0.15%) mislabels the absolute difference in degrees as a percent.
  impact: Same quantity at two values in two sections.
  resolution_test: Use 0.3% (or 0.15 degrees) consistently.
  reviewer_overlap: R1-m1, R3-m3

- audit_id: AUD-10
  status: confirmed_internal_error
  location: Results "Predictions"
  claim_pointer: "The model makes five predictions" followed by four numbered items plus two prose predictions
  evidence_pointer: MANUSCRIPT_REVISED.md lines ~119-135
  check: Counted numbered items and prose predictions.
  result: Count does not match (4 numbered, 6 if prose included).
  impact: Readability slip in a reader-facing section.
  resolution_test: Renumber all predictions or restate the count.
  reviewer_overlap: R1-m2, R2-m5, R3-m2

- audit_id: AUD-11
  status: confirmed_internal_error
  location: Results feedforward section
  claim_pointer: graded goal ff=1.0 "the same as the current-visual oracle"
  evidence_pointer: oracle (COMMAND-01) = 0.75/0.625/0.75/0.75/0.625; goal (FEEDFORWARD-01) = 0.75/0.625/0.75/0.75/0.75
  check: Compared cell by cell.
  result: Identical at four of five delays; differ at 200 ms (0.75 vs 0.625, 1/8 runs).
  impact: "The same as" is false at one delay and crosses two runs.
  resolution_test: "Matches the oracle at four of five delays" or give both sequences.
  reviewer_overlap: R1-m4, R2-m3

- audit_id: AUD-12
  status: provenance_gap
  location: CLAIM_TO_EVIDENCE_MAP.csv as a whole
  claim_pointer: rows C2, C3 assert retracted 200 ms critical-delay and motor-copy claims; C7/C8 point to MANUSCRIPT_DRAFT.md; C9/C15/C16 cite removed figures; window/V/threshold/adaptive-03/goal-mismatch claims have no rows
  evidence_pointer: CLAIM_TO_EVIDENCE_MAP.csv vs MANUSCRIPT_REVISED.md
  check: Row-by-row comparison against the revised text.
  result: The packet's own audit trail contradicts the manuscript's central corrections.
  impact: Any editor or reviewer opening the map finds retracted claims labeled strong.
  resolution_test: Regenerate the map from the revised manuscript; quarantine retired rows; add the missing rows; add the run-name to manuscript-name mapping.
  reviewer_overlap: R1-M2, R2-M6, R3-M1

- audit_id: AUD-13
  status: provenance_gap
  location: Methods; directory contents; claim map C6
  claim_pointer: Methods sweep inventory lacks P1-EC-FINEDELAY-01, LONGDELAY-01, NOISE-01, PHASE-01, TRAJ-01 (new rounds) and under-specifies goal-delay/multi-seed/window-check dimensions; C6 evidence path is /tmp/flightsim/...; six references (4,5,6,7,11,12) appear only in the reference list; eight superseded figure files remain in the submission directory
  evidence_pointer: MANUSCRIPT_REVISED.md; ls of TRACK_C_EC_DELAY; claim map C6
  check: Listed runs, grepped body text for the six names, listed figure files.
  result: All confirmed; new-round omission is expected because integration is pending, the rest are packet-hygiene gaps.
  impact: Audit trail incomplete; ephemeral evidence path; uncited references; stale figures (two depict retracted claims).
  resolution_test: Extend the Methods inventory during integration; durable path for C6; cite or drop the six references; archive stale figures.
  reviewer_overlap: R1-m5, R1-m9, R1-m11, R1-m12, R2-m6, R3-m1

- audit_id: AUD-14
  status: passed
  check: Run counts vs row counts for every Methods sweep (1,440 / 1,200 / 1,200 / 1,024 / 144 / 560 / 600 / 400 / 648 / 256 / 96 / 960 / 96 pairs); gain-sweep headline cells (addition 50 ms = 9/12 = 75%; graded_sensory gain>=0.25 = 12/12; gain 0.05 inert); window 3/16-11/16-12/16 progression; V 100 ms cells (0/75/0 and 6.2/75/6.2); adaptive gain ranges; command-copy identity; feedforward rates and ff=0 identity; self-state ablation; long-delay consistency with the 200 ms claim ceiling; source-protocol numbers; dt=2e-4 disclosure; failure-criterion definition vs code.
  result: All reconcile.
  impact: none
  resolution_test: none needed
  reviewer_overlap: multiple (strengths sections)

- audit_id: AUD-15
  status: passed (reproducibility gate)
  check: 16 unit tests pass; every round carries determinism evidence (array_equal); P1 snapshot previously verified to reproduce 768 rows; clean-environment test pass recorded in checklist.
  result: Existing artifacts reproduce existing headline numbers within recorded tolerances; full re-run not repeated this round.
  impact: none
  resolution_test: none needed
  reviewer_overlap: none
```

## 汇总

| 状态 | 数量 | IDs |
| --- | --- | --- |
| confirmed_internal_error | 9 | AUD-01, 02, 03, 04, 05, 07, 09, 10, 11 |
| aggregation_ambiguity | 2 | AUD-06, AUD-08 |
| provenance_gap | 2 | AUD-12, AUD-13 |
| passed | 2 | AUD-14, AUD-15 |

所有 confirmed 项都可由已提供的工件用算术证明；无一项动摇方向性结论（gain、短延迟 gating、adaptation 负结果、command-copy 负结果、feedforward+self-state 机制），但 AUD-01/02/04 直接命中摘要级句子，必须在修稿中解决。
