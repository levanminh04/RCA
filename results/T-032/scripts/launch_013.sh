#!/usr/bin/env bash
# T-032 phiên 13 (thiet-ke-phep-doi-013.md): chạy nền một script chỉ-đọc. Dùng: launch_013.sh <tên lượt> <script> [tham số thêm...]
set -u
B=/home/ubuntu/rca/T-032
RUN=$1; SCRIPT=$2; shift 2
L=$B/runs/$RUN-launch
mkdir -p "$L"
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 PYTHONHASHSEED=0 PYTHONPATH="$B/scripts:$B/repo/src:/home/ubuntu/rca/T-025/src/RCAEval"
cd "$B"
sha256sum scripts/$SCRIPT scripts/thiet-ke-phep-doi-013.md > "$L/pins.txt"
echo "nice -n 10 /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 scripts/$SCRIPT runs/$RUN $*" > "$L/command.txt"
date -u +%FT%TZ > "$L/start.txt"
nohup bash -c "nice -n 10 /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 scripts/$SCRIPT runs/$RUN $* > $L/out.txt 2> $L/err.txt; echo \"exit=\$? \$(date -u +%FT%TZ)\" > $L/done.txt" > /dev/null 2>&1 &
echo $! > "$L/pid.txt"
echo started $RUN pid $(cat $L/pid.txt)
