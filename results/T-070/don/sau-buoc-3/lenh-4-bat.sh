set -euo pipefail
date -u +%FT%TZ
echo "== 1 ha tang"
cd /opt/flashticket/infra/deploy
sudo -n docker compose -p flash-ticket-infra --env-file ../.env -f docker-compose.postgresql.yml -f docker-compose.redis.yml -f docker-compose.rabbitmq.yml -f mongodb/compose.yaml -f docker-compose.rca-log.yml up -d --wait --wait-timeout 300 2>&1 | tail -6
echo "== 2 toxiproxy"
sudo -n docker run -d --name rca-toxiproxy --network host --restart unless-stopped --memory 128m --label t062=topology \
  -v /srv/flashticket-rca/faults/toxiproxy/proxies.json:/config/proxies.json:ro \
  ghcr.io/shopify/toxiproxy:2.12.0 -host=127.0.0.1 -port=8474 -config=/config/proxies.json
sleep 3; curl -s -m 5 http://127.0.0.1:8474/proxies | python3 -c "import json,sys;d=json.load(sys.stdin);print('proxies',sorted((k,v['listen'],v['enabled']) for k,v in d.items()))"
echo "== 3 keycloak"
cd /opt/flashticket/compose
sudo -n env IMAGE=ft-local/keycloak:arm64-776d9c9e docker compose -p flash-ticket-keycloak -f keycloak.yml up -d 2>&1 | tail -3
for i in $(seq 1 60); do c=$(curl -s -o /dev/null -w '%{http_code}' -m 3 http://10.0.0.158:8080/realms/master || true); [ "$c" = 200 ] && break; sleep 5; done; echo "keycloak http=$c sau $((i*5))s"
echo "== 4 bay service"
sudo -n env APP_PRIVATE_IP=10.0.0.158 bash /opt/flashticket-rca/test-environment/scripts/deploy.sh trien-khai /opt/flashticket/compose arm64-t067-36a3725d /srv/flashticket-rca/faults/deploy-don-2026-11.tsv 2>&1 | tail -16
echo "== 5 agent"
cd /opt/flashticket-rca/observability/collector
sudo -n docker compose -f agent-compose.yaml --env-file ../../inventory/oracle-exp.env up -d 2>&1 | tail -2
echo "== 6 VNPay gia, duong ham"
cd /opt/flashticket-rca/load/controller/support
{ echo "RECOVER=True"; cat kiem-mock.py; } | python3 -
{ echo "ACTION='start'"; cat tunnel-remote.py; } | python3 -
sleep 5; ps -eo pid,args | grep -E "mock-runner|tunnel-supervisor|ssh .*-R" | grep -v grep | cut -c1-160
echo "== trang thai"
sudo -n docker ps --format '{{.Names}} {{.Status}}'
sudo -n docker volume ls --format '{{.Name}}'
date -u +%FT%TZ
