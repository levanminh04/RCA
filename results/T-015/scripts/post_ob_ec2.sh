#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp" PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONHASHSEED=0
PY="$TASK_ROOT/env/bin/python"
S="$TASK_ROOT/results/T-015/scripts"
date -u
"$PY" -B "$S/capture_trace_vector.py" --snapshot "$TASK_ROOT/runs/tt-local/auth/example.json" --independent-dir "$TASK_ROOT/runs/tt-independent-math/auth" --official "$TASK_ROOT/src/microrank/official.py" --out "$TASK_ROOT/runs/tt-trace-vector-probe/auth"
"$PY" -B "$S/correct_root_audit.py" --input-parquet "$TASK_ROOT/data/re2tt_ts-auth-service_cpu_1/traces.parquet" --snapshot "$TASK_ROOT/runs/tt-local/auth/example.json" --out "$TASK_ROOT/runs/root-audit-correction/auth"
for CASE in re2tt_ts-route-service_mem_1 re2tt_ts-route-service_socket_1; do
  "$PY" -B "$S/correct_root_audit.py" --input-parquet "$TASK_ROOT/data/$CASE/traces.parquet" --snapshot "$TASK_ROOT/runs/tt-local/$CASE/example.json" --out "$TASK_ROOT/runs/root-audit-correction/$CASE"
done
bash "$S/launch.sh" ob-window300 "$TASK_ROOT/data" re2ob_checkoutservice_cpu_1,re2ob_recommendationservice_socket_3 300 180 0
"$PY" -B "$S/inventory_ec2.py"
date -u
