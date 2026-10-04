#!/usr/bin/env bash
# T-007, chạy thử đường ống trong lúc chờ X1 của T-006 (Minh duyệt 03/10/2026).
# MicroRank, TraceRCA trên 2 ca RE2-OB; BOCPD (script bọc E3) trên 1 ca fse-ob; mỗi thứ bằng py312 và py312-pin.
# Chỉ để bắt lỗi đường ống và xem hai bộ thư viện có cho cùng kết quả không. Không dùng làm số.
# Chạy: mkdir -p ~/rca/runs/thu && nohup bash ~/rca/scripts/thu_duong_ong.sh > ~/rca/runs/thu/thu.log 2>&1 &
set -uo pipefail
R=$HOME/rca
export XDG_CACHE_HOME=$R/cache MPLCONFIGDIR=$R/cache/mpl TMPDIR=$R/tmp
CASES=re2ob_checkoutservice_cpu_1,re2ob_checkoutservice_delay_1
FSE_CASE=cartservice_cpu/1
W=$R/work/thu
mkdir -p $W $R/runs/thu
ts() { date -u +%FT%TZ; }

for E in py312 py312-pin; do
  PY=$R/envs/$E/bin/python
  for M in microrank tracerca; do
    echo "=== $(ts) $E $M"
    $PY $R/scripts/chay_e2.py --method $M --out $W/$E/$M --cases $CASES
  done
  echo "=== $(ts) $E bocpd $FSE_CASE"
  D=$W/$E/bocpd
  mkdir -p $D/data/fse-ob/$(dirname $FSE_CASE)
  [ -d $D/data/fse-ob/$FSE_CASE ] || cp -r $R/data/fse/fse-ob/$FSE_CASE $D/data/fse-ob/$FSE_CASE
  ( cd $D && $PY $R/scripts/chay_e3_bocpd.py --log $D/tien-do.jsonl )
done

echo "=== $(ts) so hai bộ thư viện"
for M in microrank tracerca; do
  for f in $W/py312/$M/results/*.json; do
    b=$(basename $f)
    if cmp -s $f $W/py312-pin/$M/results/$b; then echo "$M $b GIONG"; else echo "$M $b KHAC"; fi
  done
done
python3 - <<PY
import json
a=[json.loads(l) for l in open("$W/py312/bocpd/tien-do.jsonl")]
b=[json.loads(l) for l in open("$W/py312-pin/bocpd/tien-do.jsonl")]
print("bocpd cps py312 == py312-pin:", [x.get("cps") for x in a] == [x.get("cps") for x in b])
PY
echo "$(ts) THU_XONG"
