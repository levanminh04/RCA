#!/usr/bin/env bash
# T-063 thu3: thử toxic bandwidth 1 KB/s trên booking-amqp dưới tải ×3 (KE-HOACH §5), KHÔNG phải ca RCA.
# Chạy trên exp-app ngay sau khi tải ×3 bắt đầu. Dùng: setsid -f nohup bash thu_h4.sh <tiền tố ra> > /dev/null 2>&1 < /dev/null
set -u; P=${1:?prefix}; I="python3 /home/ubuntu/inj3.py"; O=CONSUMER-BOOK-SLOW-X3; B=flash-ticket-booking-service-booking-service-1
ev() { echo "{\"epoch\": $(date +%s.%N), \"ev\": \"$1\", \"out\": $(echo "$2" | tail -1)}" >> $P.jsonl; }
python3 /home/ubuntu/t063/thu3/do_h4.py $P-do.jsonl 560 10 &
sleep 120; ev nen "$($I probe -)"; t0=$(date -u +%FT%TZ)
ev start "$($I start $O --seconds 150)"; s=$(date +%s)
sleep 60; ev probe60 "$($I probe $O)"
sleep $((s + 140 - $(date +%s))); ev probe140 "$($I probe $O)"
sleep $((s + 150 - $(date +%s))); ev stop "$($I stop $O)"
sleep 30; ev sau30 "$($I probe $O)"
sleep 60; ev sau90 "$($I probe $O)"
ev verify "$($I verify)"
docker logs --since "$t0" $B 2>&1 | grep -iE "heartbeat|AmqpConnect|Restarting|ShutdownSignal|connection.*(clos|lost|reset)|ListenerExecutionFailed" | cut -c1-400 > $P-booking-log.txt
wait
