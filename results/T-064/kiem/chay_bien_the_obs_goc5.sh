#!/usr/bin/env bash
# Chạy các biến thể M1-FT trên exp-obs (user rca, venv P7). Dùng: bash chay_bien_the_obs.sh <thư mục ra> <mã biến thể>... (ca: 9 ca T-062)
set -u
RA=$1; shift
IDS="00eaea92 1ad3afeb 2e2a5541 6c1a9fd8 a5539fba a89954d1 bf17acbf e8661e0a f728fce2"
for B in "$@"; do for I in $IDS; do
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B /opt/rca-m1ft/goc-5/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "/opt/rca-m1ft/goc-5/results/T-064/bien-the/$B/cau-hinh.json" --ban "$B" --ra "$RA/$B" 2>&1 | tail -1
done; done
echo XONG
