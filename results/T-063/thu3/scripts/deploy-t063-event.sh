#!/usr/bin/env bash
# T-063 thu3: tạo lại RIÊNG event-service với image mới (compose-t062, env-t062 giữ nguyên). Dùng: bash deploy-t063-event.sh <image>
# Hoàn tác: bash deploy-t063-event.sh ft-local/event-service:arm64-t062-6b21ed55
set -Euo pipefail
IMG=${1:?image}
A=/opt/flash-ticket-app; R=/home/ubuntu/t063/thu3; C=flash-ticket-event-service-event-service-1
docker image inspect "$IMG" > /dev/null || { echo "DUNG: không có image $IMG"; exit 1; }
echo "$(date -u +%FT%TZ) TRUOC container=$(docker inspect $C --format '{{.Id}} {{.Image}} {{.Config.Image}} {{.State.StartedAt}}')"
sha256sum $A/compose-t062/event-service.yml $A/compose-t062/_common.yml
sudo sha256sum $A/env-t062/event-service.env | cut -c1-64  # chỉ băm, không đọc nội dung
( cd $A/compose-t062 && IMAGE=$IMG docker compose -p flash-ticket-event-service -f event-service.yml up -d --force-recreate ) 2>&1 | tail -3
# cổng lấy từ socket đang nghe của tiến trình container (không đọc file env)
ok=no; port=; c=
for i in $(seq 1 60); do
  pid=$(docker inspect $C --format '{{.State.Pid}}')
  port=$(sudo ss -ltnpH 2>/dev/null | grep "pid=$pid," | awk '{print $4}' | sed 's/.*://' | sort -n | head -1)
  if [ -n "$port" ]; then
    c=$(curl -s -o /dev/null -w '%{http_code}' -m 3 http://127.0.0.1:$port/actuator/health || true)
    case $c in 200|401) ok=yes;; esac
  fi
  [ $ok = yes ] && break; sleep 5
done
echo "$(date -u +%FT%TZ) SAU port=$port health_http=$c ok=$ok container=$(docker inspect $C --format '{{.Id}} {{.Image}} {{.Config.Image}} {{.State.Status}} restarts={{.RestartCount}}')"
[ $ok = yes ] || { docker logs --tail 40 $C 2>&1 | cut -c1-300; echo "DUNG: event-service không lên"; exit 2; }
