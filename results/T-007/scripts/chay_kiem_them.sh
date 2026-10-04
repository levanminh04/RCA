#!/usr/bin/env bash
# T-007, phép kiểm không cần nhãn chạy thêm sau lượt chính, bằng bộ X1 đã chốt (py312-pin). Không đổi tham số nào.
#   1. Giá trị trung gian MicroRank (QT5) trên 6 ca: 3 ca LOSS lệch khỏi thứ hạng chung + 3 ca thường.
#   2. Độ nhạy theo thứ tự span: xáo thứ tự dòng (seed 1), chạy lại 90 ca TraceRCA và MicroRank; so từng byte
#      với lượt chính và chấm lại. Kiểm một nguyên nhân khả thi của các ô lệch mốc: bộ đọc khác cho thứ tự khác.
# Chạy: nohup bash ~/rca/scripts/chay_kiem_them.sh > ~/rca/runs/kiem-them.log 2>&1 &
set -uo pipefail
# Sửa phiên 2 (03/10), sau khi lượt trên EC2 đã chạy: bắt mã thoát bằng rc=$? (bản đã chạy in "$(ts) mã thoát $?", luôn ra 0).
# Bước 1 của lượt đã chạy hỏng vì lỗi import trong trung_gian_microrank.py; chạy lại bằng chay_trung_gian_lai.sh.
E=py312-pin
R=$HOME/rca
PY=$R/envs/$E/bin/python
export XDG_CACHE_HOME=$R/cache MPLCONFIGDIR=$R/cache/mpl TMPDIR=$R/tmp
W=$R/work/$E
RUNS=$R/runs/$E
ts() { date -u +%FT%TZ; }
nen() { tar -czf $RUNS/$1.tar.gz -C $W $1 && echo "$(ts) NEN $1 -> $RUNS/$1.tar.gz ($(du -h $RUNS/$1.tar.gz | cut -f1))"; }

echo "=== $(ts) 1. trung gian MicroRank"
mkdir -p $W/microrank-trung-gian
$PY $R/scripts/trung_gian_microrank.py \
  --cases re2ob_currencyservice_loss_1,re2ob_productcatalogservice_loss_1,re2ob_recommendationservice_loss_1,re2ob_checkoutservice_cpu_1,re2ob_emailservice_delay_1,re2ob_currencyservice_mem_1 \
  --ket-qua-chinh $W/microrank/results --out $W/microrank-trung-gian/trung-gian.jsonl \
  > $W/microrank-trung-gian/chay.log 2>&1; rc=$?
echo "$(ts) mã thoát $rc"; grep "|" $W/microrank-trung-gian/chay.log
nen microrank-trung-gian

for M in tracerca microrank; do
  echo "=== $(ts) 2. xáo thứ tự span, $M"
  mkdir -p $W/$M-tron
  $PY $R/scripts/chay_e2.py --method $M --out $W/$M-tron --tron 1 > $W/$M-tron/chay.log 2>&1; rc=$?
  echo "$(ts) mã thoát $rc"
  for f in $W/$M/results/*.json; do
    b=$(basename $f)
    if cmp -s $f $W/$M-tron/results/$b; then echo "GIONG $b"; else echo "KHAC $b"; fi
  done > $W/$M-tron/so-sanh.txt
  echo "$M: giống $(grep -c ^GIONG $W/$M-tron/so-sanh.txt), khác $(grep -c ^KHAC $W/$M-tron/so-sanh.txt)"
  $PY $R/scripts/cham.py $W/$M-tron/results --json $W/$M-tron/cham.json > $W/$M-tron/cham.txt 2>&1
  nen $M-tron
done
echo "$(ts) XONG_KIEM_THEM"
