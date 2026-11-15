#!/usr/bin/env bash
# Phiên C — lô kiểm độ nhạy mốc trên exp-obs (user rca, venv P7, mã nguồn /opt/rca-m1ft/goc-10; WHY-81).
# Dùng: bash chay_doi_moc.sh <file việc: dòng "bản d tập ca"> [hạn ngừng phát, ISO UTC]
# Luật 21: một (bản, d, ca) lỗi chỉ ghi dòng lỗi rồi chạy tiếp; chạy lại bỏ qua cặp đã có summary.json; qua hạn hoặc
# thấy runner3 (đợt thu của phiên B) thì dừng phát cặp mới ở ranh giới cặp.
set -u
G=/opt/rca-m1ft/goc-10; O=/opt/rca-m1ft/out/pc-doi-moc; DEM=/opt/rca-m1ft/out/pc-doi-moc-dem
HAN=$(date -d "${2:-2099-01-01T00:00Z}" +%s)
while read -r B D TAP I; do
  [ -z "$B" ] && continue
  [ -f "$O/$TAP/$B/$I/summary.json" ] && { echo "BO-QUA $B $I"; continue; }
  [ "$(date +%s)" -ge "$HAN" ] && { echo "HET-HAN $(date -u +%FT%TZ)"; break; }
  ps -eo cmd | grep -q '[p]ython3 -B runner3' && { echo "RUNNER3 $(date -u +%FT%TZ) — dừng"; break; }
  [ -e /home/ubuntu/phien-c/DUNG ] && { echo "DUNG $(date -u +%FT%TZ)"; break; }
  if [ "$TAP" = dev2 ]; then BS=(--bo-sung "/opt/rca-m1ft/out/pc-bo-sung-dt/d$D/{id}/prometheus-bo-sung.json")
  else BS=(--bo-sung "/opt/rca-m1ft/bo-sung/{id}/prometheus-bo-sung.json" --bo-sung-t-goc); fi
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B $G/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "$G/results/T-064/bien-the/$B/cau-hinh.json" --ban "$B" --ra "$O/$TAP/$B" \
    --doi-t "$D" --dung-lai-dau-vao --dem-dau-vao "$DEM" "${BS[@]}" 2>&1 | tail -1 | sed "s/^/$(date -u +%TZ) $TAP d=$D /"
done < "$1"
echo XONG
