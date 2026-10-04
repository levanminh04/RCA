#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
mkdir -p "$TASK_ROOT/cache" "$TASK_ROOT/tmp" "$TASK_ROOT/runs/$1"
export XDG_CACHE_HOME="$TASK_ROOT/cache" PIP_CACHE_DIR="$TASK_ROOT/cache" UV_CACHE_DIR="$TASK_ROOT/cache" MPLCONFIGDIR="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED="${6:-0}" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
uptime
free -m
ps -eo pid,etimes,%cpu,%mem,rss,args --sort=-%cpu | head -15
"${T015_PYTHON:-$TASK_ROOT/env/bin/python}" -B "$TASK_ROOT/results/T-015/scripts/run_cases.py" --data "$2" --cases "$3" --out "$TASK_ROOT/runs/$1" --half "$4" --snapshot "${7:-}" --budget "$5"
