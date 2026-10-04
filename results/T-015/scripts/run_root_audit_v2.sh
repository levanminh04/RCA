#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp"
"$TASK_ROOT/env/bin/python" -B "$TASK_ROOT/results/T-015/scripts/stream_root_audit_ob.py" --data "$TASK_ROOT/data" --fixed-dir "$TASK_ROOT/runs/ob-pilot-ec2-2" --fixed-dir "$TASK_ROOT/runs/ob-block-1" --fixed-dir "$TASK_ROOT/runs/ob-block-2" --fixed-dir "$TASK_ROOT/runs/ob-block-3" --out "$TASK_ROOT/runs/ob-root-audit-correction-v2"
"$TASK_ROOT/env/bin/python" -B "$TASK_ROOT/results/T-015/scripts/inventory_ec2.py"
