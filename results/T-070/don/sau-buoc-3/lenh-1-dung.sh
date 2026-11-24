set -euo pipefail
date -u +%FT%TZ
echo "== 1 VNPay gia va duong ham"
SUP=$(cat /opt/flash-ticket-app/l1-vnpay/tunnel/supervisor.pid); MOCK=$(cat /opt/flash-ticket-app/l1-vnpay/pid); SSHP=$(cat /opt/flash-ticket-app/l1-vnpay/tunnel/ssh.pid)
echo "sup=$SUP mock=$MOCK ssh=$SSHP"
grep -q tunnel-supervisor /proc/$SUP/cmdline && kill $SUP
sleep 2
if [ -e /proc/$SSHP ] && grep -q "ssh" /proc/$SSHP/cmdline; then kill $SSHP; fi
grep -q mock-runner /proc/$MOCK/cmdline && kill $MOCK
sleep 3
ps -eo pid,args | grep -E "mock-runner|tunnel-supervisor|ssh .*-R" | grep -v grep || echo "da dung het"
(ss -tln | grep -q ':19090 ') && echo "CANH BAO: 19090 van nghe" || echo "19090 trong"
echo "== 2 agent"
cd /opt/rca-lab/observability/collector
sudo -n docker compose -p flash-ticket-collector -f agent-compose.yaml --env-file ../../inventory/oracle-exp.env down
echo "== 3 bay service"
cd /opt/flash-ticket-build/t067-compose/hieu-luc
for s in api-gateway payment-service booking-service ticket-service event-service user-service discovery-server; do
  sudo -n docker compose -p flash-ticket-$s -f $s.yml down -t 60
done
echo "== 4 keycloak"
cd /opt/flash-ticket-app/compose-exp
sudo -n env IMAGE=ft-local/keycloak:arm64-776d9c9e docker compose -p flash-ticket-keycloak -f keycloak.yml down -t 60
echo "== 5 toxiproxy"
sudo -n docker stop -t 30 rca-toxiproxy
sudo -n docker rename rca-toxiproxy rca-toxiproxy-cu
echo "== 6 ha tang"
cd /opt/flash-ticket-infra/deploy
sudo -n docker compose -p flash-ticket-infra --env-file ../.env -f docker-compose.postgresql.yml -f docker-compose.redis.yml -f docker-compose.rabbitmq.yml -f mongodb/compose.yaml -f docker-compose.rca-log.yml down -t 60
echo "== sau dung"
sudo -n docker ps -a --format '{{.Names}} {{.Status}}'
sudo -n docker volume ls --format '{{.Name}}'
sudo -n docker network ls --format '{{.Name}}'
date -u +%FT%TZ
