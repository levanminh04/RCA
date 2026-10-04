# FSE 2026 Artifact Compliance Checklist

This file maps the repository contents to the requirements stated on the FSE
2026 artifact page.

Official artifact page:

- https://conf.researchr.org/track/fse-2026/fse-2026-artifacts

## Required Root Documents

- `README.md` and `README`
  Main artifact description, archival DOI, quick start, reproduction map, and
  output locations.
- `REQUIREMENTS.md` and `REQUIREMENTS`
  Hardware/software requirements, tested environment, storage expectations, and
  installation-time guidance.
- `STATUS.md` and `STATUS`
  Claimed badges and rationale.
- `LICENSE`
  Distribution-rights summary and bundled-license notes.
- `INSTALL.md` and `INSTALL`
  Installation, execution, and success-signal guidance.
- `main.pdf`
  Copy of the accepted paper.

## Non-Trivial Software Packaging Requirement

The FSE 2026 page requires a VirtualBox VM or Docker image for non-trivial
software artifacts. This repository satisfies that requirement with:

- `Dockerfile`
- `scripts/run_review.sh`

The preferred review path is Docker-first and falls back to local Python only if
Docker is unavailable.

## Installation-Time Requirement

The FSE 2026 page states that installation/configuration should take less than
30 minutes. This artifact addresses that requirement by:

- providing a single-command Docker-first entry point
- pinning Python dependencies
- bundling the reduced reviewer dataset needed for the first validation path
- separating the long-running extended reproduction path from the initial review
  path

## Reproduction And Validation Coverage

The reduced reviewer path:

- executes 12 RCA algorithms
- runs on 10 bundled datapacks
- regenerates `artifacts/reviewer_output/`
- regenerates `artifacts/reproduction_report/`
- regenerates `artifacts/paper_assets/`

Validation evidence currently present in this workspace:

- `artifacts/reproduction_report/table5.sampled.md` lists all 12 algorithms
- `artifacts/reproduction_report/output/data/rcabench/` contains
  `10 x 12 = 120` per-case `perf.parquet` files

## Archival Availability

- Version-specific DOI recorded in `README.md`:
  `10.5281/zenodo.19522409`

## Notes On Scope

- The reduced reviewer benchmark is the required first review path.
- The infrastructure-heavy full-data path remains documented but is not required
  for initial artifact validation.
