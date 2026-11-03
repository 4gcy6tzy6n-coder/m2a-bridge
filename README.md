# M2A-BRIDGE — What delayed feedback control needs

Research project behind the manuscript *"What delayed feedback control needs: fresh state,
conditional gating, and tests across artificial and biological systems"* (submitted to
Nature Machine Intelligence; see `M2A-BRIDGE/08_MANUSCRIPT/SUBJOURNAL_PACKAGE/`).

Private archive created 2026-11-03 from the working workspace.

## Contents

| Path | What it is |
|---|---|
| `M2A-BRIDGE/06_JOINT/` | Model, experiment, and analysis code (Python) |
| `M2A-BRIDGE/08_MANUSCRIPT/` | Manuscript source, Springer Nature LaTeX build (`latex_nmi/`), figures, submission package |
| `M2A-BRIDGE/09_P3_MECH_IDENT/` | Preregistration, dataset-qualification, and prior-art audits |
| `M2A-BRIDGE/02_DATA_FEASIBILITY/` | Field-level data eligibility reports (documents only) |
| `PROCESS/` | Round gate / debug protocol |
| `runs/` | Preregistered experiment rounds: manifests, preregistrations, gate results, summary outputs |
| `wiki/` | Project decision log and changelog |

## Data availability

Third-party raw datasets are **not** bundled (licensing): Tanaka et al. 2023 (Dryad
`bcc2fqzjz`), Fischer & Schnell 2022 (Edmond `doi:10.17617/3.92`), Rayshubskiy et al.
2025 (Harvard Dataverse `doi:10.7910/DVN/0NCLP1`), Currier & Nagel 2018 (Dryad
`m715hp3`). Fetch scripts and field-level qualification records live under
`M2A-BRIDGE/02_DATA_FEASIBILITY/`. All confirmatory analyses were preregistered;
frozen preregistration files and SHA-256 prefixes are under `runs/`.

## Build the manuscript

```bash
cd M2A-BRIDGE/08_MANUSCRIPT/SUBJOURNAL_PACKAGE/latex_nmi
pdflatex -interaction=nonstopmode manuscript.tex && bibtex manuscript \
  && pdflatex -interaction=nonstopmode manuscript.tex \
  && pdflatex -interaction=nonstopmode manuscript.tex
```
