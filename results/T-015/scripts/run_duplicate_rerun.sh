#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1 XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp"
"$TASK_ROOT/env/bin/python" -B "$TASK_ROOT/results/T-015/scripts/run_cases.py" --data "$TASK_ROOT/data" --cases re2ob_recommendationservice_loss_1,re2ob_recommendationservice_loss_2 --snapshot re2ob_recommendationservice_loss_1,re2ob_recommendationservice_loss_2 --out "$TASK_ROOT/runs/ob-duplicate-rerun" --budget 180
for CASE in re2ob_recommendationservice_loss_1 re2ob_recommendationservice_loss_2; do
  "$TASK_ROOT/env/bin/python" -B "$TASK_ROOT/results/T-015/scripts/independent_math.py" "$TASK_ROOT/runs/ob-duplicate-rerun/$CASE.json" --output "$TASK_ROOT/runs/ob-duplicate-math/$CASE"
done
"$TASK_ROOT/env/bin/python" -B "$TASK_ROOT/results/T-015/scripts/inventory_ec2.py"
