#!/usr/bin/env bash
# T-007, chạy lại bước 1 của chay_kiem_them.sh (soi giá trị trung gian MicroRank) sau lượt hỏng 10:41 UTC
# (lỗi import trong trung_gian_microrank.py, đã sửa). Lượt hỏng giữ lại với hậu tố -hong1 (luật cứng 10).
# Chạy: nohup bash ~/rca/scripts/chay_trung_gian_lai.sh > ~/rca/runs/trung-gian-lai.log 2>&1 &
set -uo pipefail
E=py312-pin
R=$HOME/rca
PY=$R/envs/$E/bin/python
export XDG_CACHE_HOME=$R/cache MPLCONFIGDIR=$R/cache/mpl TMPDIR=$R/tmp
W=$R/work/$E
RUNS=$R/runs/$E
ts() { date -u +%FT%TZ; }
[ -e $W/microrank-trung-gian-hong1 ] || mv $W/microrank-trung-gian $W/microrank-trung-gian-hong1
[ -e $RUNS/microrank-trung-gian-hong1.tar.gz ] || tar -czf $RUNS/microrank-trung-gian-hong1.tar.gz -C $W microrank-trung-gian-hong1
rm -f $RUNS/microrank-trung-gian.tar.gz   # bản nén cũ là của lượt hỏng; nội dung đã nằm trong -hong1

echo "=== $(ts) trung gian MicroRank (chạy lại)"
mkdir -p $W/microrank-trung-gian
$PY $R/scripts/trung_gian_microrank.py \
  --cases re2ob_currencyservice_loss_1,re2ob_productcatalogservice_loss_1,re2ob_recommendationservice_loss_1,re2ob_checkoutservice_cpu_1,re2ob_emailservice_delay_1,re2ob_currencyservice_mem_1 \
  --ket-qua-chinh $W/microrank/results --out $W/microrank-trung-gian/trung-gian.jsonl \
  > $W/microrank-trung-gian/chay.log 2>&1
rc=$?
echo "$(ts) mã thoát $rc"
grep "|" $W/microrank-trung-gian/chay.log
tar -czf $RUNS/microrank-trung-gian.tar.gz -C $W microrank-trung-gian && echo "$(ts) NEN microrank-trung-gian"
echo "$(ts) XONG_TRUNG_GIAN_LAI"
