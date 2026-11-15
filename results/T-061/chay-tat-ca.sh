#!/usr/bin/env bash
# T-061: chạy lại toàn bộ đường sử dụng: chuyển đổi → băm mẫu → chỉ mục danh sách → phát lại (kiểm đủ đợt) → khung Grafana.
# Chạy trong results/T-061. Mọi lệnh Python dùng -B (không ghi bytecode). Sau đó: py -3 -B kiem.py
set -euo pipefail
G=../T-058/dem-2026-11-10
for c in c12e47ab f4a8c021; do
  py -3 -B -I chuyen-doi.py --vao $G/rca-ban-dau/outputs/$c/method-output-1.json \
    --request $G/rca-ban-dau/cases/$c/request.json --manifest $G/artifacts-sha256.json \
    --goc-manifest $G --adapter $G/src/m1/adapter_flashticket.py --ma-ca $c --ra mau/$c.json
done
py -3 -B -I bam-mau.py
py -3 -B -I chi-muc.py
py -3 -B -I phat-lai.py --dot $G/m1-launch-record.json --thu-muc-mau mau --manifest-mau mau/manifest-mau.json \
  --ke-hoach $G/m1-execution-plan-v2.json --so $G/ledger-received.jsonl --manifest $G/artifacts-sha256.json \
  --goc-manifest $G
py -3 -B -I khung-grafana.py
