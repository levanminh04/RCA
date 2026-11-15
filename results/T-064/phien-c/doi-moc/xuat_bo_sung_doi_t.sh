#!/usr/bin/env bash
# Phiên C (T-064, dời mốc): xuất lại gói metric bổ sung quanh t' = t + d cho 13 ca dev bản 2, d ∈ {−30, +30}.
# Chạy trên exp-obs, user ubuntu: bash xuat_bo_sung_doi_t.sh <file xuat_bo_sung.py của T-063> <file mã ca> <thư mục ra>
# Bộ xuất dùng nguyên bản results/T-063/dong-goi/xuat_bo_sung.py (chỉ đọc Prometheus localhost:9090, không nhãn).
# t lấy từ cases/<id>/request.json (đọc bằng user rca). Bước lưới 15 s; |d| = 30 là bội của 15 nên lưới trùng lưới gốc.
set -u
X=$1; IDS=$(cat "$2"); R=$3
for I in $IDS; do
  T=$(sudo -n -u rca cat /opt/flash-ticket-rca/cases/$I/request.json | python3 -c 'import json,sys;print(json.load(sys.stdin)["t"])')
  for D in -30 30; do
    F=$R/d$D/$I/prometheus-bo-sung.json
    [ -s "$F" ] && { echo "BO-QUA $I $D"; continue; }
    mkdir -p "$R/d$D/$I"
    python3 - --t $((T + D)) --ra "$F" < "$X" 2> "$R/d$D/$I/xuat.stderr"
    echo "$I d=$D t'=$((T + D)) rc=$? $(cat $R/d$D/$I/xuat.stderr)"
  done
done
echo XONG
