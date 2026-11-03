# Forensic consistency audit — Track C

- Date: 2026-10-27
- Scope: manuscript text, figure legends, and the simulation outputs under `runs/`.
- Status: editorial audit, not a fourth reviewer report.
- Isolation: reviewers did not see this audit.

## AUD-01 — confirmed internal error (corrected)

```yaml
audit_id: AUD-01
status: confirmed_internal_error
location: Abstract; Results "Efference-copy gain..."; README; cover letter; peer-review notes
claim_pointer: A current motor copy at high gain reduces 200 ms failure from 100% to 25-33% (3-4/12).
evidence_pointer: runs/P1-EC-GAIN-01/experiment/outputs/summary.json, graded_motor, 200 ms
check: Recomputed 200 ms failure counts for graded_motor at gains 0.5, 0.75, 1.0.
result: 5/12 (41.7%), 3/12 (25.0%), 4/12 (33.3%). The correct range is 25-42% (3-5/12), not 25-33% (3-4/12).
impact: The direction is unchanged, but the stated range was too narrow and excluded the gain-0.5 condition.
resolution_test: Replace 25-33% with 25-42% and 3-4/12 with 3-5/12 everywhere. Done in manuscript, README, cover letter, and peer-review notes.
reviewer_overlap: R1-m2, R2-m2, R3-m4
```

## Passed checks

| Check | Result |
| --- | --- |
| Gain-sweep run count | 5 models x 6 gains x 4 delays x 12 parameter sets = 1,440. Matches Methods. |
| Coarse-sweep run count | 4 models x 12 parameter sets x 16 delays = 768. Matches Methods. |
| Robustness run count | 5 models x 8 parameter sets x 19 delays x 2 seeds = 1,520. Matches Methods. |
| Fine-grid run count | 5 models x 3 parameter sets x 121 delays = 1,815. Matches Methods. |
| Adaptive run count | 12 parameter sets x 4 delays x 5 models = 240. Matches Methods. |
| Alpha-sweep run count | 4 alphas x 3 seeds x 4 delays x 12 parameter sets = 576. Matches Methods. |
| P1 medians | 0.04 / 0.03 / 0.02 / 0.25 s for addition / graded_sensory / graded_motor / allnone. Matches Results. |
| P1 140 ms counts | 12/12, 12/12, 4/12, 2/12. Matches Results. |
| P2 medians | 0.02 / 0.02 / 0.015 / 0.20 / 0.11 s. Matches Results. |
| P2 140 ms counts | 16/16, 16/16, 10/16, 3/16, 12/16. Matches Results. |
| P3 medians | 18 / 15 / 10 / 110 / 200 ms. Matches Results and Fig. 2b. |
| Gain sweep, source gain | At gain 0 or 0.05, addition and both graded variants fail 75% at 50 ms. Matches. |
| Gain sweep, delayed sensory | At gain >= 0.25, 100% failure at 50 ms versus 75% for addition. Matches. |
| Gating invariance | allnone 0% through 100 ms, 50% at 200 ms; allnone_motor 8% at 100 ms, 50% at 200 ms. Matches. |
| Adaptive MLP | learned gain 0.38, 0.75, 0.97, 1.06; failure 42%, 100%, 100%, 100%. Matches. |
| Alpha sweep | 1e-5 at 50 ms 75%; alpha >= 8e-5 at 50 ms 100%; all 100% by 100 ms. Matches. |
| Linear stability | 29, 31/43, 300, 29 ms for addition, graded_sensory (0.05/1.0), graded_motor (1.0), allnone open-gate. Matches Fig. 6. |
| Source protocol | 59.956 vs 59.956 (near-zero gate), 59.923 vs 59.770 (EC gain 0.5), 59.846 vs 50.846 (addition). Matches. |
| Percent bounds | All reported failure rates are within 0 and 1. |
| Figure calls | Fig. 1, 2, 2b, 2c, 2d, 2e, 3, 4, 5, 6 all resolve to existing files. |
| Reproducibility gate | Code snapshots exist for P1/P2/P3; clean venv passes 9 tests and selftests; six round gates pass. |

## Unresolved input needed

- The manuscript's author list, affiliations, CRediT, funding, and competing interests are owner-side and not assessable from the supplied material.
- The full source Figure 5 ODE-internal MLP and episode protocol are not reproduced; the manuscript declares this as future work.
- The raw animal data behind Canelo et al. 2024 are not part of the packet.

## Audit-driven notes for synthesis

- AUD-01 is a confirmed internal error but does not change the direction of the claim.
- No arithmetic or aggregation contradiction was found in the headline simulation counts or medians.
- The linear stability result is a scope limitation, not an error. It shows the main separation is large-signal/nonlinear.
