#!/bin/bash
# T-031 bước 4 trên EC2: TORAI nguồn B rồi A, 30 ca × 3 seed, tuần tự. Chạy trong tmux phiên "t031"
# để vẫn chạy khi laptop tắt. Xem tiến độ: tail -f ~/rca/T-031/trang-thai.txt
# hoặc ~/rca/T-031/repo/results/T-031/runs/torai-*/tien-do.txt
set -u
B=~/rca/T-031
cd $B/repo
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=$B/tmp
export PYTHONPATH=$B/src/RCAEval:$B/repo/src
P=$B/envs/main/bin/python
echo "$(date -u +%FT%TZ) BAT DAU" > $B/trang-thai.txt
for src in B A; do
  echo "$(date -u +%FT%TZ) torai_$src bat dau" >> $B/trang-thai.txt
  $P -B -W ignore results/T-031/scripts/chay_ec2.py torai-$src-ec2 torai_$src > $B/runs/torai-$src.out 2> $B/runs/torai-$src.err
  echo "$(date -u +%FT%TZ) torai_$src xong, exit=$?" >> $B/trang-thai.txt
done
echo "$(date -u +%FT%TZ) XONG CA HAI" >> $B/trang-thai.txt
