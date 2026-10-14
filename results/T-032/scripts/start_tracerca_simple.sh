#!/usr/bin/env bash
# T-032 TraceRCA EC2: khởi một đoạn của driver đơn giản, tách khỏi SSH. Môi trường y như start_script_stage_v3.sh.
# Dùng: start_tracerca_simple.sh <mã đoạn> <số ca tối đa; 0 = chạy hết>
set -euo pipefail
B=/home/ubuntu/rca/T-032
P=/home/ubuntu/rca/T-025/envs/main/bin/python
segment=${1:?segment}; max_cases=${2:?max-cases}
case "$segment" in *[!0-9]*|'') exit 2;; esac
case "$max_cases" in *[!0-9]*|'') exit 2;; esac
L="$B/runs/tracerca-cohort-simple-001-launch"
mkdir -p "$L" "$B/tmp" "$B/cache/mpl"
test ! -e "$L/$segment.out"
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 PYTHONHASHSEED=0
export PYTHONPATH="$B/scripts:$B/repo/src:/home/ubuntu/rca/T-025/src/RCAEval:/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/src/CIRCA"
export TMPDIR="$B/tmp" XDG_CACHE_HOME="$B/cache" MPLCONFIGDIR="$B/cache/mpl" MPLBACKEND=Agg
cd "$B"
nohup "$P" -B -X utf8 "$B/scripts/drive_tracerca_ec2_simple_v1.py" --segment "$segment" --max-cases "$max_cases" \
  > "$L/$segment.out" 2> "$L/$segment.err" < /dev/null &
pid=$!
printf '%s\n' "$pid" > "$L/$segment.pid"
printf 'driver_pid=%s\n' "$pid"
