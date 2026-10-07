#!/bin/bash
# T-025 bước 1: BOCPD chế độ (b), 30 ca dev, tuần tự theo mã mờ, trên EC2 trong tmux phiên "t025"
# (chạy tiếp khi laptop tắt). Giới hạn 21.600 s mỗi ca (SPEC). Không đọc nhãn.
# Xem tiến độ:  cat ~/rca/T-025/trang-thai.txt
#               tail -f ~/rca/T-025/repo/results/T-025/runs/bocpd-ec2-001/tien-do.txt
# Dừng:         tmux kill-session -t t025   (ca đang chạy và ca chưa chạy ghi TIMEOUT theo SPEC)
set -u
B=~/rca/T-025
cd $B/repo
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=$B/tmp MPLCONFIGDIR=$B/cache/mpl MPLBACKEND=Agg
export XDG_CACHE_HOME=$B/cache T025_DATA_ROOT=~/rca/T-031/repo
export PYTHONPATH=$B/src/baro:$B/repo/src
P=$B/envs/main/bin/python
echo "$(date -u +%FT%TZ) BAT DAU bocpd 30 ca" >> $B/trang-thai.txt
$P -B -W ignore results/T-025/scripts/chay_b.py bocpd-ec2 bocpd trang_thai=$B/trang-thai.txt \
  > $B/runs/bocpd-ec2.out 2> $B/runs/bocpd-ec2.err
rc=$?
echo "$(date -u +%FT%TZ) XONG bocpd, exit=$rc" >> $B/trang-thai.txt
