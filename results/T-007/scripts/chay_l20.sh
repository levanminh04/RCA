#!/usr/bin/env bash
# T-007 phiên 2: biến thể chẩn đoán cửa sổ ±600 s (--length 20) cho MicroRank, TraceRCA, 90 ca, bộ py312-pin
# (Minh duyệt 03/10, phiên 2). Lượt chính (±300 s, --length 10) không đổi.
# Chạy: nohup bash ~/rca/scripts/chay_l20.sh > ~/rca/runs/chay-l20.log 2>&1 &
set -uo pipefail
E=py312-pin
R=$HOME/rca
PY=$R/envs/$E/bin/python
export XDG_CACHE_HOME=$R/cache MPLCONFIGDIR=$R/cache/mpl TMPDIR=$R/tmp
W=$R/work/$E
RUNS=$R/runs/$E
ts() { date -u +%FT%TZ; }
nen() { tar -czf $RUNS/$1.tar.gz -C $W $1 && echo "$(ts) NEN $1 -> $RUNS/$1.tar.gz ($(du -h $RUNS/$1.tar.gz | cut -f1))"; }

echo "=== $(ts) kiểm hồi quy: chay_e2.py bản mới, mặc định (--length 10), TraceRCA 6 ca, so từng byte với lượt chính"
LAI=re2ob_checkoutservice_cpu_1,re2ob_currencyservice_delay_2,re2ob_emailservice_disk_3,re2ob_productcatalogservice_loss_1,re2ob_recommendationservice_mem_2,re2ob_checkoutservice_socket_3
mkdir -p $W/tracerca-hoi-quy
$PY $R/scripts/chay_e2.py --method tracerca --cases $LAI --out $W/tracerca-hoi-quy > $W/tracerca-hoi-quy/chay.log 2>&1; rc=$?
for f in $W/tracerca-hoi-quy/results/*.json; do
  b=$(basename $f); if cmp -s $f $W/tracerca/results/$b; then echo "GIONG $b"; else echo "KHAC $b"; fi
done | tee $W/tracerca-hoi-quy/so-sanh.txt
echo "$(ts) mã thoát $rc"
nen tracerca-hoi-quy

for M in tracerca microrank; do
  echo "=== $(ts) $M --length 20"
  mkdir -p $W/$M-L20
  $PY $R/scripts/chay_e2.py --method $M --length 20 --out $W/$M-L20 > $W/$M-L20/chay.log 2>&1; rc=$?
  echo "$(ts) mã thoát $rc | ok $(grep -c '"trang_thai": "ok"' $W/$M-L20/tien-do.jsonl) | lỗi $(grep -c '"trang_thai": "LOI"' $W/$M-L20/tien-do.jsonl)"
  $PY $R/scripts/cham.py $W/$M-L20/results --json $W/$M-L20/cham.json > $W/$M-L20/cham.txt 2>&1
  nen $M-L20
done
echo "$(ts) XONG_L20"
