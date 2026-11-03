# Reporting Summary（Nature 系 Reporting Summary 骨架——多数条目可直接勾选）

## Sample size
- Model sweeps: fixed design grids (8 parameter sets × delays), not random
  samples; explicitly stated in Methods ("the parameter grid is a design, not a
  random sample").
- Artificial-task transfer: 30 randomized plants per task family (preregistered).
- Empirical datasets: all available animals analyzed per dataset
  (T4 13 / T5 15 / LPTC 10–12 per type / F&S 12 / walking intervention 6;
  sample-size limitations disclosed in Limitations).

## Data exclusions
- Animal-level exclusion rules preregistered per confirmatory round
  (e.g., >20% non-finite predictions); applied counts reported
  (0 exclusions in executed confirmatory rounds; sealed round unchanged).

## Replication
- Key model results replicated across: 3 seeds (multi-seed rounds), 8 body-gain
  parameter sets, two noise levels, and two independent artificial task families
  beyond the original plant. Empirical findings: exact tests, single-shot
  preregistered; replication attempts and their failures reported in full.

## Randomization
- Plant randomization seeds preregistered (P4-AI-01, seed 424242).
- Permutation/bootstrap seeds preregistered per round (listed in Methods table).

## Blinding
- Not applicable to experiments (no intervention-assignment in model rounds).
- For public-data analyses: all confirmatory analyses preregistered with frozen
  files before outcome access; animal labels never used for outcome-dependent
  selection (guards listed per round).

## Quantification and statistics
- Animal-level exact sign-flip / label-shuffle permutation tests (one-sided
  where direction preregistered); bootstrap CIs; multiple-testing correction
  (Holm) where applicable; rule-of-three bounds for 0/N cells; minimum
  detectable effects as null-distribution quantiles (defined in Methods).
  No p>0.05 equivalence claims anywhere.

## Software
- Python 3.12, NumPy/SciPy/Matplotlib; all code archived with deposit [DOI].
- Simulation: Euler integration, dt disclosed; step-halving checks reported.
