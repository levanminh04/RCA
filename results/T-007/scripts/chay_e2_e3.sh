#!/usr/bin/env bash
# T-007 E2 + E3 cho MỘT bộ thư viện (py312 hoặc py312-pin, theo X1 của T-006). Chạy tuần tự:
#   1. MicroRank, 90 ca RE2-OB            -> nén work/<env>/microrank
#   2. TraceRCA, 90 ca RE2-OB             -> nén work/<env>/tracerca
#   3. Chạy lại 6 ca mỗi phương pháp trong tiến trình mới (phép kiểm không cần nhãn), so từng byte
#   4. BOCPD (script bọc E3), 100 ca fse-ob -> nén work/<env>/bocpd
# Mỗi khối xong thì nén ngay vào ~/rca/runs/<env>/; dừng giữa chừng thì khối đã xong vẫn còn.
# Chạy: nohup bash ~/rca/scripts/chay_e2_e3.sh py312-pin > ~/rca/runs/chay-<env>.log 2>&1 &
# Sửa phiên 2 (03/10): bắt mã thoát bằng rc=$? ngay sau lệnh. Bản đã chạy ở phiên 1 in "$(ts) mã thoát $?",
# luôn ra 0 vì $(ts) đặt lại $?. Chỉ dòng log mã thoát sai; phép tính không đổi.
set -uo pipefail
E=$1
R=$HOME/rca
PY=$R/envs/$E/bin/python
export XDG_CACHE_HOME=$R/cache MPLCONFIGDIR=$R/cache/mpl TMPDIR=$R/tmp
W=$R/work/$E
RUNS=$R/runs/$E
mkdir -p $W $RUNS
ts() { date -u +%FT%TZ; }
nen() { tar -czf $RUNS/$1.tar.gz -C $W $1 && echo "$(ts) NEN $1 -> $RUNS/$1.tar.gz ($(du -h $RUNS/$1.tar.gz | cut -f1))"; }
# 6 ca chạy lại: mỗi service một ca, đủ 6 loại lỗi; chọn trước khi xem kết quả
LAI=re2ob_checkoutservice_cpu_1,re2ob_currencyservice_delay_2,re2ob_emailservice_disk_3,re2ob_productcatalogservice_loss_1,re2ob_recommendationservice_mem_2,re2ob_checkoutservice_socket_3

echo "$(ts) BAT_DAU $E | $(nproc) vCPU | $(free -m | awk '/Mem/{print $7}') MB RAM trống"
for M in microrank tracerca; do
  echo "=== $(ts) E2 $E $M"
  mkdir -p $W/$M
  $PY $R/scripts/chay_e2.py --method $M --out $W/$M > $W/$M/chay.log 2>&1; rc=$?
  echo "$(ts) mã thoát $rc | $(grep -c '"trang_thai": "ok"' $W/$M/tien-do.jsonl) ca ok | $(grep -c '"trang_thai": "LOI"' $W/$M/tien-do.jsonl) ca lỗi"
  nen $M
done

for M in microrank tracerca; do
  echo "=== $(ts) chạy lại $E $M (tiến trình mới)"
  mkdir -p $W/$M-lai
  $PY $R/scripts/chay_e2.py --method $M --out $W/$M-lai --cases $LAI > $W/$M-lai/chay.log 2>&1
  for f in $W/$M-lai/results/*.json; do
    b=$(basename $f)
    if cmp -s $f $W/$M/results/$b; then echo "$M $b GIONG"; else echo "$M $b KHAC"; fi
  done | tee $W/$M-lai/so-sanh.txt
  nen $M-lai
done

echo "=== $(ts) E3 $E bocpd"
mkdir -p $W/bocpd
[ -e $W/bocpd/data ] || ln -s $R/data/fse $W/bocpd/data   # reproduce_bocpd đọc ./data/fse-ob
( cd $W/bocpd && $PY $R/scripts/chay_e3_bocpd.py --log $W/bocpd/tien-do.jsonl > $W/bocpd/chay.log 2>&1 ); rc=$?
echo "$(ts) mã thoát $rc"
grep -A4 "Reproduce BOCPD" $W/bocpd/chay.log
nen bocpd
echo "$(ts) XONG_TAT_CA $E"
