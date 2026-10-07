#!/bin/bash
# T-025 trên EC2 thứ nhất (3.26.62.217), tmux phiên "t025b": chờ BOCPD (tmux "t025") xong, rồi dựng phần env RCA
# và chạy RCA tại t̂ của BOCPD (SPEC bước 3, "máy nào rảnh trước": máy này rảnh ngay khi BOCPD xong, có sẵn bản ghi).
# Không đọc nhãn. Xem tiến độ: cat ~/rca/T-025/trang-thai.txt. Dừng: tmux kill-session -t t025b.
set -u
B=~/rca/T-025
TT=$B/trang-thai.txt
echo "$(date -u +%FT%TZ) CHUOI MAY 1: cho BOCPD xong" >> $TT
while tmux has-session -t =t025 2>/dev/null; do sleep 60; done
echo "$(date -u +%FT%TZ) BOCPD da ket thuc; dung env RCA" >> $TT
bash $B/repo/results/T-025/scripts/dung_env_rca_ec2.sh > $B/runs/dung-env-rca.log 2>&1
rc=$?
echo "$(date -u +%FT%TZ) XONG dung env RCA exit=$rc" >> $TT
[ $rc -eq 0 ] || { echo "$(date -u +%FT%TZ) DUNG: dung env RCA loi" >> $TT; exit 1; }
cd $B/repo
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=$B/tmp MPLCONFIGDIR=$B/cache/mpl MPLBACKEND=Agg
export XDG_CACHE_HOME=$B/cache T025_DATA_ROOT=~/rca/T-031/repo
export PYTHONPATH=$B/src/RCAEval:$B/src/baro:$B/repo/src:$B/src/CIRCA
echo "$(date -u +%FT%TZ) BAT DAU rca-bocpd" >> $TT
$B/envs/main/bin/python -B -W ignore results/T-025/scripts/rca_b.py rca-bocpd-m1 tu=runs/bocpd-ec2-001 \
  > $B/runs/rca-bocpd.out 2> $B/runs/rca-bocpd.err
rc=$?
echo "$(date -u +%FT%TZ) XONG rca-bocpd exit=$rc" >> $TT
echo "$(date -u +%FT%TZ) XONG CHUOI MAY 1" >> $TT
