# Reviewer Output Landing Zone

Open this directory first after running `bash scripts/run_review.sh`.

This directory summarizes the bundled 10-case reviewer benchmark.
The files here are intended for fast artifact validation and should not be interpreted as exact numeric reproductions of the paper's full raw-data study.

Primary charts in this folder:
- `rq4_generation_proc_figure.pdf`
- `dataset_attributes_radar.pdf`
- `rq5_scalability_analysis.pdf`
- `rq5_failure_distribution.pdf`
- `overall_metrics.pdf`
- `rq5_perf_by_fault_type_figure.pdf`
- `rq5_perf_by_algo_figure.pdf`

Primary tables in this folder:
- `table5.sampled.md`
- `table5.sampled.csv`
- `reviewer_failure_categories.csv`

Supporting directories:
- `../reproduction_report/` contains the raw sampled experiment outputs
- `../paper_assets/` contains the sampled paper-assets bundle
