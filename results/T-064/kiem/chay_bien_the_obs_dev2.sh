#!/usr/bin/env bash
# Chạy biến thể M1-FT lượt chọn trên exp-obs (user rca, venv P7, mã nguồn /opt/rca-m1ft/goc-6 — TD-64-06b).
# Dùng: bash chay_bien_the_obs_dev2.sh <thư mục ra> <file mã ca (mỗi dòng một mã mờ)> <thư mục gói bổ sung> <mã biến thể>...
#   Gói bổ sung: <thư mục>/<mã>/prometheus-bo-sung.json (dev bản 2: chép từ ~/rca-dieu-phoi/ca/ sang chỗ rca đọc được).
# CHỈ chạy sau khi đợt thu chính xong (exp-obs 2 lõi, không tranh CPU với thu nhận telemetry — LOG T-064 13/11).
set -u
RA=$1; IDS=$(cat "$2"); BS=$3; shift 3
ps -eo cmd | grep -q '[p]ython3 -B runner3' && { echo 'đợt thu còn chạy — dừng'; exit 2; }
for B in "$@"; do for I in $IDS; do
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B /opt/rca-m1ft/goc-6/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "/opt/rca-m1ft/goc-6/results/T-064/bien-the/$B/cau-hinh.json" --ban "$B" --ra "$RA/$B" \
    --bo-sung "$BS/{id}/prometheus-bo-sung.json" 2>&1 | tail -1
done; done
echo XONG
