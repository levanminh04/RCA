#!/usr/bin/env bash
# Lô 5 (WHY-96) trên exp-obs: user rca, venv P7, mã /opt/rca-m1ft/goc-12 (= b0f79a4d…). Một luồng đọc một file việc,
# mỗi dòng "bản d tập ca" (tập: dev2 | dev3 | t062). Luật 21: một cặp lỗi chỉ ghi dòng lỗi rồi chạy tiếp; chạy lại bỏ qua
# cặp đã có summary.json; có ~/rca-dieu-phoi/STOP hoặc ~/l5/DUNG thì dừng ở ranh giới cặp; gói bổ sung quanh t' chưa có thì
# chờ tối đa 40 phút rồi ghi THIEU-GOI và chạy tiếp.
set -u
G=/opt/rca-m1ft/goc-12; O=/opt/rca-m1ft/out/l5; DEM=/opt/rca-m1ft/out/l5-dem; BDT=/opt/rca-m1ft/out/l5-bo-sung-dt
while read -r B D TAP I; do
  [ -z "$B" ] && continue
  [ -f "$O/$TAP/d$D/$B/$I/summary.json" ] && { echo "BO-QUA $B $D $I"; continue; }
  [ -e /home/ubuntu/rca-dieu-phoi/STOP ] && { echo "STOP $(date -u +%FT%TZ)"; break; }
  [ -e /home/ubuntu/l5/DUNG ] && { echo "DUNG $(date -u +%FT%TZ)"; break; }
  ps -eo cmd | grep -q '[p]ython3 -B runner' && { echo "RUNNER $(date -u +%FT%TZ) — dừng"; break; }
  THEM=()
  if [ "$TAP" = t062 ]; then
    BS=/opt/rca-m1ft/bo-sung/{id}/prometheus-bo-sung.json; [ "$D" != 0 ] && THEM+=(--bo-sung-t-goc)
  elif [ "$D" = 0 ]; then
    [ "$TAP" = dev2 ] && BS=/opt/rca-m1ft/bo-sung-dev2/{id}/prometheus-bo-sung.json || BS=/opt/rca-m1ft/bo-sung-dev3/{id}/prometheus-bo-sung.json
  else
    BS=$BDT/d$D/{id}/prometheus-bo-sung.json; F=$BDT/d$D/$I/prometheus-bo-sung.json; n=0
    while [ ! -s "$F" ] && [ $n -lt 240 ]; do sleep 10; n=$((n+1)); done
    [ -s "$F" ] || { echo "THIEU-GOI $B $D $I"; continue; }
  fi
  [ "$D" != 0 ] && THEM+=(--doi-t "$D" --dung-lai-dau-vao --dem-dau-vao "$DEM")
  [ "$D" = 0 ] && [ "$I" = ebd5ef38 ] && THEM+=(--dung-lai-dau-vao)
  C=$G/results/T-064/bien-the/$B/cau-hinh.json
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 /opt/flash-ticket-rca/venv/bin/python -B $G/src/m1_ft/chay_ca.py \
    --id "$I" --cau-hinh "$C" --ban "$B" --ra "$O/$TAP/d$D/$B" --bo-sung "$BS" "${THEM[@]}" 2>&1 | tail -1 \
    | sed "s/^/$(date -u +%TZ) $B d=$D $TAP $I /"
done < "$1"
echo XONG
