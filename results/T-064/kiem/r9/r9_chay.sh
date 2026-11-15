#!/usr/bin/env bash
# R9 (WHY-99; Minh duyệt 15/11 "Duyệt cả ba"): chạy lại slot ebd5ef38 với gói live-down mới /opt/rca-m1ft/out/r9-bo-sung; đầu ra /opt/rca-m1ft/out/r9. Chép từ l5_chay.sh, chỉ đổi O, đường gói và bỏ nhánh chờ gói. Lô 5 gốc (WHY-96) trên exp-obs: user rca, venv P7, mã /opt/rca-m1ft/goc-12 (= b0f79a4d…). Một luồng đọc một file việc,
# mỗi dòng "bản d tập ca" (tập: dev2 | dev3 | t062). Luật 21: một cặp lỗi chỉ ghi dòng lỗi rồi chạy tiếp; chạy lại bỏ qua
# cặp đã có summary.json; có ~/rca-dieu-phoi/STOP hoặc ~/l5/DUNG thì dừng ở ranh giới cặp; gói bổ sung quanh t' chưa có thì
# chờ tối đa 40 phút rồi ghi THIEU-GOI và chạy tiếp.
set -u
G=/opt/rca-m1ft/goc-12; O=/opt/rca-m1ft/out/r9; DEM=/opt/rca-m1ft/out/l5-dem; BDT=/opt/rca-m1ft/out/l5-bo-sung-dt
while read -r B D TAP I; do
  [ -z "$B" ] && continue
  [ -f "$O/$TAP/d$D/$B/$I/summary.json" ] && { echo "BO-QUA $B $D $I"; continue; }
  [ -e /home/ubuntu/rca-dieu-phoi/STOP ] && { echo "STOP $(date -u +%FT%TZ)"; break; }
  [ -e /home/ubuntu/l5/DUNG ] && { echo "DUNG $(date -u +%FT%TZ)"; break; }
  ps -eo cmd | grep -q '[p]ython3 -B runner' && { echo "RUNNER $(date -u +%FT%TZ) — dừng"; break; }
  THEM=(); BS=/opt/rca-m1ft/out/r9-bo-sung/d$D/{id}/prometheus-bo-sung.json
  [ -s "/opt/rca-m1ft/out/r9-bo-sung/d$D/$I/prometheus-bo-sung.json" ] || { echo "THIEU-GOI $B $D $I"; continue; }
  [ "$D" != 0 ] && THEM+=(--doi-t "$D" --dung-lai-dau-vao --dem-dau-vao "$DEM")
  [ "$D" = 0 ] && [ "$I" = ebd5ef38 ] && THEM+=(--dung-lai-dau-vao)
  C=$G/results/T-064/bien-the/$B/cau-hinh.json
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B $G/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "$C" --ban "$B" --ra "$O/$TAP/d$D/$B" --bo-sung "$BS" "${THEM[@]}" 2>&1 | tail -1 \
    | sed "s/^/$(date -u +%TZ) $B d=$D $TAP $I /"
done < "$1"
echo XONG
