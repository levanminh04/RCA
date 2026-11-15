#!/usr/bin/env bash
# Chạy biến thể M1-FT lượt chọn 3 trên exp-obs (user rca, venv P7, mã nguồn /opt/rca-m1ft/goc-8 — TD-64-09).
# Dùng: bash chay_bien_the_obs_luot3.sh <thư mục ra> <file mã ca> <thư mục gói bổ sung> <mã biến thể>...
# Một lỗi ở một (bản, ca) chỉ ghi dòng lỗi rồi chạy tiếp (luật 21a). Chạy lại: (bản, ca) đã có summary.json thì bỏ qua (21b).
set -u
RA=$1; IDS=$(cat "$2"); BS=$3; shift 3
G=/opt/rca-m1ft/goc-8
ps -eo cmd | grep -q '[p]ython3 -B runner3' && { echo 'đợt thu còn chạy — dừng'; exit 2; }
for B in "$@"; do for I in $IDS; do
  [ -f "$RA/$B/$I/summary.json" ] && { echo "BO-QUA $B $I"; continue; }
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B $G/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "$G/results/T-064/bien-the/$B/cau-hinh.json" --ban "$B" --ra "$RA/$B" \
    --bo-sung "$BS/{id}/prometheus-bo-sung.json" 2>&1 | tail -1
done; done
echo XONG
