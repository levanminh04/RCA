#!/usr/bin/env bash
# T-063 thu3: theo dõi nhẹ lượt chính (chỉ đọc file nhỏ trên exp-obs). Dừng sớm khi có sự kiện bất thường hoặc xong.
# Dùng: bash theo_doi.sh <số lần> <giây giữa hai lần>
N=${1:-9}; G=${2:-63}
KO="D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key"; KH="UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts"
for i in $(seq 1 $N); do
  r=$(ssh -i "$KO" -o BatchMode=yes -o ConnectTimeout=15 -o "$KH" ubuntu@213.35.116.128 'S=~/rca-dieu-phoi/thu3/tiem-loi/so-thu3.jsonl; B=$(grep -cE "\"event\": \"(cycle-error|dirty|run-abort-dirty|cycle-abort|fault-start-failed|m1-skipped|cycle-stopped)\"" $S); E=$(grep -c "\"event\": \"thu3-end\"" $S); L=$(grep -c "M1 LỖI" ~/rca-dieu-phoi/thu3/chay/nhat-ky-3.jsonl); X=$(grep -c "M1 xong" ~/rca-dieu-phoi/thu3/chay/nhat-ky-3.jsonl); P=$(ps -eo cmd | grep -c "^python3 -B runner4.py thu"); C=$(grep -c "\"event\": \"cycle-end\"" $S); echo "bat_thuong=$B xong=$E m1_loi=$L m1_xong=$X runner=$P cycle_end=$C"' < /dev/null 2>&1)
  echo "$(date -u +%T) $r"
  case "$r" in *"bat_thuong=0 "*"runner=1"*) ;; *) break;; esac
  case "$r" in *" xong=1 "*) break;; esac
  sleep $G
done
