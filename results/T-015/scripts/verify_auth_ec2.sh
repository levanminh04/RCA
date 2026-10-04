#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp" PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONHASHSEED=0
PY="$TASK_ROOT/env/bin/python"
SCRIPTS="$TASK_ROOT/results/T-015/scripts"
date -u
"$PY" -B "$SCRIPTS/independent_math.py" "$TASK_ROOT/runs/tt-local/auth/example.json" --output "$TASK_ROOT/runs/tt-independent-math/auth"
"$PY" -B "$SCRIPTS/independent_inputs.py" --input-parquet "$TASK_ROOT/data/re2tt_ts-auth-service_cpu_1/traces.parquet" --inject-file "$TASK_ROOT/data/re2tt_ts-auth-service_cpu_1/inject_time.txt" --snapshot "$TASK_ROOT/runs/tt-local/auth/example.json" --out "$TASK_ROOT/runs/tt-independent-inputs/auth"
"$PY" -B "$SCRIPTS/local_microrank_checks.py" --code-root "$TASK_ROOT" --input-parquet "$TASK_ROOT/data/re2tt_ts-auth-service_cpu_1/traces.parquet" --inject-file "$TASK_ROOT/data/re2tt_ts-auth-service_cpu_1/inject_time.txt" --out "$TASK_ROOT/runs/tt-local/auth" --case re2tt_ts-auth-service_cpu_1 --steps columns_reversed,rows_shuffled,seed1_repeat,half300,two_normal
date -u
