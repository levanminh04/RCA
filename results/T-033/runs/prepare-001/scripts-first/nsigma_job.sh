#!/bin/bash
# T-033: độc lập SSH/laptop; chỉ ghi dưới ~/rca/T-033.
set -u
B=/home/ubuntu/rca/T-033
cd "$B" || exit 1
run="$1"
mode="$2"
export T033_HOME="$B" T033_PREFLIGHT=preflight-002
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export TMPDIR="$B/tmp" XDG_CACHE_HOME="$B/cache" MPLCONFIGDIR="$B/cache/mpl"
export PYTHONPATH=/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/repo/src
P=/home/ubuntu/rca/T-025/envs/main/bin/python
printf '%s\n' "$$" > "$B/runs/$run.shell.pid"
if [ "$mode" = first ]; then
  "$P" -B -X utf8 scripts/nsigma_run.py --run "$run" --first > "runs/$run.out" 2> "runs/$run.err"
else
  "$P" -B -X utf8 scripts/nsigma_run.py --run "$run" > "runs/$run.out" 2> "runs/$run.err"
fi
rc=$?
printf '%s\n' "$rc" > "$B/runs/$run.exit"
exit "$rc"
