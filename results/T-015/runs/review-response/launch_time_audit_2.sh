#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp" PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONHASHSEED=0
OUT="$TASK_ROOT/runs/review-response/input-time-audit"
mkdir -p "$TASK_ROOT/runs/review-response"
[ ! -e "$OUT" ]
(uptime; free -m; ps -eo pid,pcpu,pmem,rss,args --sort=-rss | head -n 15) > "$TASK_ROOT/runs/review-response/preflight-2.txt"
nohup "$TASK_ROOT/env/bin/python" -B "$TASK_ROOT/bin/check_input_times_review.py" --root "$TASK_ROOT" --expected "$TASK_ROOT/runs/review-response/expected-inputs.json" --output "$OUT" > "$TASK_ROOT/runs/review-response/time-audit-console-2.log" 2>&1 < /dev/null &
echo $! > "$TASK_ROOT/runs/review-response/time-audit-2.pid"
cat "$TASK_ROOT/runs/review-response/time-audit-2.pid"
