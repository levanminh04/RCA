#!/bin/bash
set -u
B=/home/ubuntu/rca/T-033
cd "$B" || exit 1
run="$1"
script="$2"
shift 2
case "$script" in
  bocpd_factorial.py|nsigma_frozen.py) ;;
  *) exit 2 ;;
esac
if [ -e "runs/$run" ] || [ -e "runs/$run.out" ]; then
  printf '%s\n' "Refuse duplicate run $run" >&2
  exit 2
fi
export T033_HOME="$B" T033_PREFLIGHT=preflight-002
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export TMPDIR="$B/tmp" XDG_CACHE_HOME="$B/cache" MPLCONFIGDIR="$B/cache/mpl"
export PYTHONPATH=/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/repo/src
P=/home/ubuntu/rca/T-025/envs/main/bin/python
printf '%s\n' "$$" > "runs/$run.shell.pid"
"$P" -B -X utf8 "scripts/$script" --run "$run" "$@" > "runs/$run.out" 2> "runs/$run.err"
rc=$?
printf '%s\n' "$rc" > "runs/$run.exit"
exit "$rc"
