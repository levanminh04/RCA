#!/usr/bin/env bash
# Phiên C: chờ lô dời mốc (luot-A/B.log) in XONG rồi phát hai luồng lô H8; hạn ngừng phát cặp mới truyền vào $1.
set -u
cd ~/phien-c
until grep -q '^XONG' luot-A.log && grep -q '^XONG' luot-B.log; do
  [ -e DUNG ] && { echo "DUNG $(date -u +%FT%TZ)"; exit 1; }
  sleep 20
done
echo "phat $(date -u +%FT%TZ)"
setsid -f nohup bash chay_h8.sh viec-h8-A.txt "$1" > h8-A.log 2>&1 < /dev/null
sleep 2
setsid -f nohup bash chay_h8.sh viec-h8-B.txt "$1" > h8-B.log 2>&1 < /dev/null
