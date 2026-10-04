#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp" PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONHASHSEED=0
PY="$TASK_ROOT/env/bin/python"
for CASE in re2tt_ts-route-service_mem_1 re2tt_ts-route-service_socket_1; do
  "$PY" -B "$TASK_ROOT/results/T-015/scripts/local_microrank_checks.py" --code-root "$TASK_ROOT" --input-parquet "$TASK_ROOT/data/$CASE/traces.parquet" --inject-file "$TASK_ROOT/data/$CASE/inject_time.txt" --out "$TASK_ROOT/runs/tt-local/$CASE" --case "$CASE" --steps primary
done
