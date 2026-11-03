# m2a-bridge — delayed feedback control (code)

Core code for the study *"What delayed feedback control needs: fresh state, conditional
gating, and tests across artificial and biological systems"*. This repository contains
**code only**; the manuscript, figures, and experiment records are not part of this repo.

## Contents

| Path | What it is |
|---|---|
| `M2A-BRIDGE/06_JOINT/` | Steering-model implementation (`ec_model.py`), comparator/observer controllers, and all experiment runner scripts (delay sweeps, gate ablations, observer checks, AI-transfer benchmarks, injection-recovery) |
| `PROCESS/` | Round-gate runner (`round_gate.py`) and its protocol/templates — every experiment round passes debug gates before running |

## Requirements

Python 3.12+, `numpy`, `scipy`, `matplotlib`. Third-party raw datasets are **not**
bundled; obtain them from the original repositories (Tanaka et al. 2023 Dryad
`bcc2fqzjz`; Fischer & Schnell 2022 Edmond `doi:10.17617/3.92`; Rayshubskiy et al.
2025 Harvard Dataverse `doi:10.7910/DVN/0NCLP1`; Currier & Nagel 2018 Dryad
`m715hp3`) and qualify them field-by-field before use.

## Model tests

```bash
python3 M2A-BRIDGE/06_JOINT/ec_model.py --selftest
```
