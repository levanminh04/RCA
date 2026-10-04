# Artifact Requirements

This artifact has one primary review mode and two optional extended modes.

## 1. Lightweight Figure/Paper Validation

This mode is intended for artifact review of the paper package in this directory.

### Hardware

- 4 CPU cores recommended
- 8 GB RAM minimum, 16 GB recommended
- 15 GB free disk space minimum for the Docker-first path, 20 GB recommended

### Installation Time Target

- The artifact is packaged so that configuration and installation for the
  reduced reviewer path stay within the FSE guideline of under 30 minutes on a
  clean machine.
- This time budget refers to setup and installation, not to the full runtime of
  all experiments after setup completes.

### Software

- Linux or macOS recommended
- Python 3.10 or newer
- `pip` or another Python package installer
- Docker is recommended for the first reviewer run because the bundled image avoids local environment drift
- Outbound network access is required for the first Docker build or first local
  Python dependency installation, unless a previously built image/environment is
  already available

### Python Packages

The plotting scripts in this directory require:

- the exact pinned versions listed in `requirements.txt`

### Tested Configuration

- Ubuntu 24.04
- Docker 28.x
- Python 3.12
- Clean Docker-first reviewer execution through `bash scripts/run_review.sh`

## 2. Optional Existing-Data Replay

This mode is intended for rerunning dataset conversion, local RCA evaluation, and
paper-asset generation from an existing `rcabench_dataset` snapshot.

### Hardware

- 8 CPU cores minimum, 16+ recommended
- 16 GB RAM minimum, 32 GB recommended
- 100 GB free disk space minimum

### Software

- Linux recommended
- Python 3.10+
- `uv`
- `bash`
- optional `sudo` if your dataset directory requires elevated access
- the exact pinned versions listed in `requirements-experiment.txt`

### Storage Layout

- raw datapacks are expected at `/mnt/jfs/rcabench_dataset` by default
- `rcabench-platform/data/rcabench_dataset` should point to that location
- This path is optional for the reviewer-first reduced benchmark and required
  only for the extended existing-data replay

## 3. Optional Live Full-System Reproduction

This mode is intended for rebuilding the benchmark environment and rerunning dataset construction and RCA evaluation across the supporting repositories.

### Hardware

- 8 CPU cores minimum, 16+ recommended
- 32 GB RAM minimum for practical local work
- 100 GB free disk space minimum
- More resources are needed for cluster-scale dataset generation

### Software

- Docker
- Kubernetes or a compatible local cluster
- `kubectl`
- Helm
- `pytest`
- Go 1.23+
- Python 3.10+
- Java and Maven for Train-Ticket services
- `just` for some repository workflows
- `uv` is recommended where the repositories expect it

### Notes

- The paper reports large-scale dataset construction on a multi-node cluster. A laptop-class machine is sufficient for artifact inspection, conversion replay, and selected smoke tests, but not for reproducing the full 188.07-hour data-generation workload at reported scale.
- The reduced reviewer path runs entirely from this directory and is the intended first review path.
- The extended end-to-end workflow uses the bundled repositories under `vendor/fullstack/`, `vendor/rcabench-platform`, and `vendor/rca-algo-contrib`, but those repositories are supplementary to the default artifact evaluation path.
- The DOI-backed archive should remain the authoritative public release for the submitted version of this artifact.
- The artifact was vetted through the reduced Docker-first path on a clean
  environment before final packaging.
