#!/usr/bin/env bash
# Phiên C — lô H8-adapter, H8-log trên exp-obs (user rca, venv P7, mã nguồn /opt/rca-m1ft/goc-11; WHY-81).
# Dùng: bash chay_h8.sh <file việc: dòng "bản tập ca [kc]"> [hạn ngừng phát, ISO UTC]
# tập dev2: gói bổ sung bo-sung-dev2; t062: bo-sung; "kc" ở cột 4 = chạy với --dung-lai-dau-vao (ca không có method-input).
# Luật 21: lỗi một cặp chỉ ghi dòng lỗi rồi chạy tiếp; chạy lại bỏ qua cặp đã có summary.json; qua hạn, có runner3 hoặc
# ~/phien-c/DUNG thì dừng phát ở ranh giới cặp.
set -u
G=/opt/rca-m1ft/goc-11; O=/opt/rca-m1ft/out/pc-h8
HAN=$(date -d "${2:-2099-01-01T00:00Z}" +%s)
while read -r B TAP I KC; do
  [ -z "$B" ] && continue
  [ -f "$O/$TAP/$B/$I/summary.json" ] && { echo "BO-QUA $B $I"; continue; }
  [ "$(date +%s)" -ge "$HAN" ] && { echo "HET-HAN $(date -u +%FT%TZ)"; break; }
  ps -eo cmd | grep -q '[p]ython3 -B runner3' && { echo "RUNNER3 $(date -u +%FT%TZ) — dừng"; break; }
  [ -e /home/ubuntu/phien-c/DUNG ] && { echo "DUNG $(date -u +%FT%TZ)"; break; }
  if [ "$TAP" = dev2 ]; then BS=/opt/rca-m1ft/bo-sung-dev2; else BS=/opt/rca-m1ft/bo-sung; fi
  X=(); [ "${KC:-}" = kc ] && X=(--dung-lai-dau-vao)
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B $G/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "$G/results/T-064/bien-the/$B/cau-hinh.json" --ban "$B" --ra "$O/$TAP/$B" \
    --bo-sung "$BS/{id}/prometheus-bo-sung.json" "${X[@]}" 2>&1 | tail -1 | sed "s/^/$(date -u +%TZ) $TAP /"
done < "$1"
echo XONG
