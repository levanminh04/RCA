#!/usr/bin/env bash
# Lô 5 (WHY-96): xuất lại gói metric bổ sung quanh t' = t + d. Chạy trên exp-obs, user ubuntu.
# Dùng: bash l5_xuat_bo_sung.sh <xuat_bo_sung.py T-063> <file "mã_ca d1 d2 ..." mỗi dòng> <thư mục ra>
# Bộ xuất nguyên bản results/T-063/dong-goi/xuat_bo_sung.py (chỉ đọc Prometheus localhost:9090, không nhãn); t lấy
# từ cases/<id>/request.json. |d| là bội của 15 nên lưới trùng lưới gốc. Đã có file khác rỗng thì bỏ qua.
set -u
X=$1; R=$3
while read -r I DS; do
  [ -z "$I" ] && continue
  T=$(sudo -n -u rca cat /opt/flash-ticket-rca/cases/$I/request.json | python3 -c 'import json,sys;print(json.load(sys.stdin)["t"])')
  for D in $DS; do
    F=$R/d$D/$I/prometheus-bo-sung.json
    [ -s "$F" ] && { echo "BO-QUA $I $D"; continue; }
    mkdir -p "$R/d$D/$I"
    python3 - --t $((T + D)) --ra "$F.tmp" < "$X" 2> "$R/d$D/$I/xuat.stderr"; rc=$?
    [ $rc -eq 0 ] && mv "$F.tmp" "$F"
    echo "$(date -u +%TZ) $I d=$D t'=$((T + D)) rc=$rc $(tail -1 $R/d$D/$I/xuat.stderr)"
  done
done < "$2"
echo XONG
