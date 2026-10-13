#!/bin/bash
# T-029: chỉ ghi dưới B, env/source/dữ liệu các task trước chỉ đọc.
set -euo pipefail
B="$HOME/rca/T-029"
S="$HOME/rca/T-025"
cd "$B"
export T029_HOME="$B" PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export TMPDIR="$B/tmp" XDG_CACHE_HOME="$B/cache" MPLCONFIGDIR="$B/cache/mpl" MPLBACKEND=Agg
export PYTHONPATH="$S/src/RCAEval:$S/src/baro:$S/repo/src:$S/src/CIRCA"
trap 'rc=$?; printf "%s SHELL_KET_THUC exit=%s\n" "$(date -u +%FT%TZ)" "$rc" >> "$B/trang-thai.txt"' EXIT
"$S/envs/main/bin/python" -B -W ignore "$B/scripts/ec2_chain.py" > "$B/runs/chuoi.out" 2> "$B/runs/chuoi.err"
