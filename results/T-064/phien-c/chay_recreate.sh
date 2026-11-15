#!/usr/bin/env bash
# Phiên C — chạy 4 bản trên ca RECREATE-PAY ebd5ef38 (sổ `chay_them` 10:50:19Z), mã goc-11, đầu ra out/pc-recreate.
set -u
G=/opt/rca-m1ft/goc-11; O=/opt/rca-m1ft/out/pc-recreate; I=ebd5ef38; BS=/opt/rca-m1ft/bo-sung-dev3/{id}/prometheus-bo-sung.json
ps -eo cmd | grep -q '[p]ython3 -B runner3' && { echo 'runner3 chạy — dừng'; exit 2; }
for B in V058-KC-P7-dunglai-d0 V032-H5b V060-H8a V061-V032+H8a; do
  [ -f "$O/$B/$I/summary.json" ] && { echo "BO-QUA $B"; continue; }
  C=$G/results/T-064/bien-the/$B/cau-hinh.json; [ -f "$C" ] || C=/home/ubuntu/phien-c/cau-hinh-$B.json
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B $G/src/m1_ft/chay_ca.py \
    --id $I --cau-hinh "$C" --ban "$B" --ra "$O/$B" --bo-sung "$BS" --dung-lai-dau-vao 2>&1 | tail -1 | sed "s/^/$(date -u +%TZ) $B /"
done
echo XONG
