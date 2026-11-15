#!/usr/bin/env bash
# T-063 thu3: chạy thử cường độ POOL-EVENT (KE-HOACH §4), KHÔNG phải ca RCA. Chạy trên exp-app ngay sau khi tải bắt đầu.
# Dùng: setsid -f nohup bash thu_pool.sh <file-ra.jsonl> > /dev/null 2>&1 < /dev/null
set -u; RA=${1:?ra}; I="python3 /home/ubuntu/inj3.py"
ev() { echo "{\"epoch\": $(date +%s.%N), \"ev\": \"$1\", \"out\": $(echo "$2" | tail -1)}" >> $RA; }
sleep 120; ev nen "$($I probe -)"
for o in POOL-EVENT-4 POOL-EVENT-5; do
  ev start-$o "$($I start $o --seconds 150)"; s=$(date +%s)
  sleep 45; ev probe45-$o "$($I probe $o)"
  sleep $((s + 140 - $(date +%s))); ev probe140-$o "$($I probe $o)"
  sleep $((s + 150 - $(date +%s))); ev stop-$o "$($I stop $o)"
  sleep 30; ev sau30-$o "$($I probe $o)"
  [ $o = POOL-EVENT-4 ] && sleep 60
done
ev verify "$($I verify)"
