#!/usr/bin/env bash
# Canh hai luồng lô chọn dev bản 2 trên exp-obs: A (xuôi, out/chon-dev2-1), B (ngược, out/chon-dev2-1b).
# Khi biến thể đang chạy của một luồng đã xong đủ ở luồng kia → dừng luồng đó (tiến trình chay_ca đang chạy tự kết thúc ca hiện tại).
# Không xóa gì. Bản chấm lấy, cho mỗi biến thể, thư mục có đủ N ca. Dùng: setsid -f nohup bash canh_hai_luong.sh 13 > canh.log 2>&1
N=$1; A=/opt/rca-m1ft/out/chon-dev2-1; B=/opt/rca-m1ft/out/chon-dev2-1b
du() { for d in "$1"/*/; do [ -d "$d" ] || continue; n=$(ls "$d" 2>/dev/null | while read i; do [ -f "$d$i/summary.json" ] && echo; done | wc -l); echo "$(basename "$d") $n"; done; }
song() { ps -eo cmd | grep -q "[c]hay_bien_the_obs_dev2.sh $1 "; }
while song "$A" || song "$B"; do
  dA=$(du "$A"); dB=$(du "$B")
  xongA=$(echo "$dA" | awk -v n=$N '$2==n{print $1}'); xongB=$(echo "$dB" | awk -v n=$N '$2==n{print $1}')
  dangA=$(echo "$dA" | awk -v n=$N '$2<n{print $1}'); dangB=$(echo "$dB" | awk -v n=$N '$2<n{print $1}')
  for v in $dangA; do if echo "$xongB $dangB" | tr ' ' '\n' | grep -qx "$v" && song "$A"; then
    echo "$(date -u +%FT%TZ) dừng A tại $v (B đã có/đang chạy)"; pkill -f "chay_bien_the_obs_dev2.sh $A " ; fi; done
  for v in $dangB; do if echo "$xongA" | tr ' ' '\n' | grep -qx "$v" && song "$B"; then
    echo "$(date -u +%FT%TZ) dừng B tại $v (A đã xong)"; pkill -f "chay_bien_the_obs_dev2.sh $B " ; fi; done
  sleep 60
done
echo "$(date -u +%FT%TZ) CANH-XONG"
