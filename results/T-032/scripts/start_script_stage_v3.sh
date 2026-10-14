#!/usr/bin/env bash
# T-032 generic stage: detached supervisor, frozen environment, new run only.
set -euo pipefail
B=/home/ubuntu/rca/T-032
P=/home/ubuntu/rca/T-025/envs/main/bin/python
stage=${1:?stage}; local_bytes=${2:?local-reserve}; wall_s=${3:?wall-seconds}; script=${4:?script}
shift 4
case "$stage" in *[!a-zA-Z0-9_-]*|'') exit 2;; esac
case "$script" in *[!a-zA-Z0-9_.-]*|'') exit 2;; esac
test -f "$B/scripts/$script"
test ! -e "$B/runs/$stage-monitor"
test ! -e "$B/runs/$stage-launcher.out"
mkdir -p "$B/tmp" "$B/cache/mpl"
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 PYTHONHASHSEED=0
export PYTHONPATH="$B/scripts:$B/repo/src:/home/ubuntu/rca/T-025/src/RCAEval:/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/src/CIRCA"
export TMPDIR="$B/tmp" XDG_CACHE_HOME="$B/cache" MPLCONFIGDIR="$B/cache/mpl" MPLBACKEND=Agg
cd "$B"
nohup "$P" -B -X utf8 "$B/scripts/run_guarded_stage_v3.py" \
 --name "$stage-monitor" --local-bytes "$local_bytes" --max-wall-s "$wall_s" \
 -- "$P" -B -X utf8 "$B/scripts/$script" "$@" \
 > "$B/runs/$stage-launcher.out" 2> "$B/runs/$stage-launcher.err" < /dev/null &
pid=$!
printf '%s\n' "$pid" > "$B/runs/$stage-launcher.pid"
printf 'supervisor_pid=%s\n' "$pid"
