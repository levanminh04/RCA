#!/usr/bin/env bash
# T-062 A2: thay 7 service bằng image T-062 (compose-t062, env-t062). Hoàn tác: rollback-t062.sh
set -Euo pipefail
SHA8=${1:?sha8 (8 ký tự)}
[ ${#SHA8} = 8 ] || { echo 'sha8 phải 8 ký tự'; exit 1; }
A=/opt/flash-ticket-app; R=/home/ubuntu/t062
APP_PRIVATE_IP=$(python3 "$(dirname "$(readlink -f "$0")")/../../campaigns/lib/inventory.py" get application.private_ip)
mkdir -p $R
# lưu image đang chạy để hoàn tác
[ -f $R/truoc-trien-khai.json ] || docker ps --format '{{json .}}' | python3 -c '
import sys,json; d={}
for l in sys.stdin:
  j=json.loads(l); d[j["Names"]]=j["Image"]
json.dump(d,open("'$R'/truoc-trien-khai.json","w"),indent=1)'
sudo install -d -o 10001 -g 10001 -m 0750 $A/rca-faults $A/rca-faults/booking-service $A/rca-faults/event-service
for s in booking-service event-service; do
  sudo install -d -o 10001 -g 10001 -m 0750 $A/rca-faults/$s/control
  sudo install -d -o 10001 -g 10001 -m 0770 $A/rca-faults/$s/audit
done
port() { grep -E "^(SERVER_PORT|DISCOVERY_SERVER_PORT|API_GATEWAY_PORT|[A-Z]+_SERVICE_PORT)=" $A/env-t062/$1.env | head -1 | cut -d= -f2; }
for s in discovery-server user-service event-service ticket-service booking-service payment-service api-gateway; do
  img=ft-local/$s:arm64-t062-$SHA8
  echo "$(date -u +%FT%TZ) $s up $img"
  ( cd $A/compose-t062 && IMAGE=$img docker compose -p flash-ticket-$s -f $s.yml up -d --force-recreate ) 2>&1 | tail -2
  p=$(port $s); ok=no
  for i in $(seq 1 60); do
    for h in 127.0.0.1 $APP_PRIVATE_IP; do
      c=$(curl -s -o /dev/null -w '%{http_code}' -m 3 http://$h:$p/actuator/health || true)
      # 200 = health mở; 401 = service đã lên, actuator yêu cầu xác thực (gateway, event)
      case $c in 200|401) started=$(docker inspect flash-ticket-$s-$s-1 --format '{{.State.StartedAt}}'); [ "$(date -d "$started" +%s)" -lt "$(date +%s)" ] && ok=yes;; esac
    done
    [ $ok = yes ] && break; sleep 5
  done
  st=$(docker inspect flash-ticket-$s-$s-1 --format '{{.State.Status}} restarts={{.RestartCount}} image={{.Config.Image}}')
  case "$st" in *"image=$img"*) ;; *) ok=no;; esac
  echo "$(date -u +%FT%TZ) $s port=$p health=$ok $st"
  if [ $ok != yes ]; then docker logs --tail 30 flash-ticket-$s-$s-1 2>&1 | cut -c1-300; echo "DUNG: $s không healthy"; exit 2; fi
done
date -u +%FT%TZ > $R/deploy.done
