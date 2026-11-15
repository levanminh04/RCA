#!/usr/bin/env bash
# T-063 — bảo trì exp-app lượt 1 (gói results/T-063/quan-sat/goi-exp-app-1.md). Chạy TRÊN exp-app: bash -s < bao-tri-exp-app-1.sh <bước>
# Bước: sao-luu | collector | ha-tang | app | kiem. Mỗi bước in JSON tóm tắt; dừng khi lỗi (set -e). Không in nội dung env/bí mật.
set -euo pipefail
B=${1:?bước}
NGAY=20261112
A=/opt/flash-ticket-app; I=/opt/flash-ticket-infra/deploy
LABELS='com.docker.compose.service,com.docker.compose.container-number'
log(){ printf '{"t":"%s","buoc":"%s","msg":"%s"}\n' "$(date -u +%FT%TZ)" "$B" "$1"; }
case "$B" in
sao-luu)
  for f in $A/compose-t062/_common.yml $A/compose-exp/keycloak.yml $A/collector/config.json; do cp -p "$f" "$f.bak-T063-$NGAY-bt1"; done
  sha256sum $A/compose-t062/_common.yml $A/compose-exp/keycloak.yml $A/collector/config.json $I/docker-compose.postgresql.yml
  for c in $(docker ps --format '{{.Names}}' | grep -E '^flash-ticket-'); do echo "$c $(docker inspect $c --format '{{.Config.Image}} {{.Id}}')"; done
  log "sao luu xong";;
collector)
  cd $A/collector && python3 - < /tmp/cach_a.py && cp config.new.json config.json && sha256sum config.json
  docker restart flash-ticket-collector >/dev/null; sleep 20
  docker inspect flash-ticket-collector --format '{{.State.Status}} {{.RestartCount}}'
  docker logs --since 30s flash-ticket-collector 2>&1 | grep -iE '"level":"error"|\berror\b' | grep -v deprecated | head -5 || true
  log "collector moi da chay";;
ha-tang)
  cat > /tmp/docker-compose.rca-log.yml <<EOF
# T-063 (bảo trì lượt 1): nhãn log cách A cho hạ tầng + log autovacuum/checkpoint/lock của Postgres. File chồng, không sửa file gốc.
services:
  postgres:
    command: ["postgres","-c","max_connections=120","-c","shared_buffers=256MB","-c","work_mem=4MB","-c","maintenance_work_mem=128MB","-c","password_encryption=scram-sha-256","-c","log_autovacuum_min_duration=0","-c","log_checkpoints=on","-c","log_lock_waits=on"]
    logging: {driver: json-file, options: {max-size: 10m, max-file: "3", labels: "$LABELS"}}
  redis:
    logging: {driver: json-file, options: {max-size: 10m, max-file: "3", labels: "$LABELS"}}
  rabbitmq:
    logging: {driver: json-file, options: {max-size: 10m, max-file: "3", labels: "$LABELS"}}
  user-db:
    logging: {driver: json-file, options: {max-size: 10m, max-file: "3", labels: "$LABELS"}}
EOF
  sudo install -m 0644 /tmp/docker-compose.rca-log.yml $I/docker-compose.rca-log.yml; sha256sum $I/docker-compose.rca-log.yml
  cd $I && docker compose -p flash-ticket-infra --env-file /opt/flash-ticket-infra/.env -f docker-compose.postgresql.yml -f docker-compose.redis.yml -f docker-compose.rabbitmq.yml -f mongodb/compose.yaml -f docker-compose.rca-log.yml up -d 2>&1 | tail -6
  for i in $(seq 1 30); do n=$(docker ps --filter name=flash-ticket-infra- --format '{{.Status}}' | grep -c healthy || true); [ "$n" -ge 4 ] && break; sleep 5; done
  docker ps --filter name=flash-ticket-infra- --format '{{.Names}} {{.Status}}'
  log "ha tang tao lai";;
app)
  grep -q 'labels:' $A/compose-t062/_common.yml || sed -i 's/^        max-file: "3"$/        max-file: "3"\n        labels: "'"$LABELS"'"/' $A/compose-t062/_common.yml
  grep -q 'labels:' $A/compose-exp/keycloak.yml || sed -i 's/^        max-file: "3"$/        max-file: "3"\n        labels: "'"$LABELS"'"/' $A/compose-exp/keycloak.yml
  grep -q 'OTEL_INSTRUMENTATION_METHODS_INCLUDE' $A/compose-exp/keycloak.yml || sed -i 's#^    env_file: ../env/keycloak.env$#    env_file: ../env/keycloak.env\n    environment:\n      OTEL_INSTRUMENTATION_METHODS_INCLUDE: "org.keycloak.services.scheduled.ScheduledTaskRunner[run];org.keycloak.expiration.jpa.impl.DefaultExpirationTask[run];org.keycloak.expiration.jpa.impl.RealmAwareExpirationTask[run]"#' $A/compose-exp/keycloak.yml
  sha256sum $A/compose-t062/_common.yml $A/compose-exp/keycloak.yml
  IMG=$(docker inspect flash-ticket-keycloak-keycloak-1 --format '{{.Config.Image}}')
  (cd $A/compose-exp && IMAGE=$IMG docker compose -p flash-ticket-keycloak -f keycloak.yml up -d 2>&1 | tail -2)
  for s in discovery-server event-service booking-service payment-service ticket-service user-service api-gateway; do
    c=flash-ticket-$s-$s-1; IMG=$(docker inspect $c --format '{{.Config.Image}}')
    (cd $A/compose-t062 && IMAGE=$IMG docker compose -p flash-ticket-$s -f $s.yml up -d 2>&1 | tail -1)
    sleep 25
  done
  docker ps --format '{{.Names}} {{.Image}} {{.Status}}' | grep flash-ticket | sort
  log "app tao lai";;
kiem)
  for c in $(docker ps --format '{{.Names}}' | grep -E '^flash-ticket-' | grep -v collector); do
    f=$(docker inspect $c --format '{{.LogPath}}'); printf '%s attrs=%s\n' "$c" "$(tail -n 1 "$f" 2>/dev/null | python3 -c 'import json,sys; d=json.loads(sys.stdin.read() or "{}"); print(sorted((d.get("attrs") or {}).items()))' 2>/dev/null)"
  done
  for u in 8082 8083 8084 8085 8086 8761; do printf 'liveness %s %s\n' $u "$(curl -s -o /dev/null -w '%{http_code}' --max-time 2 http://127.0.0.1:$u/actuator/health/liveness)"; done
  printf 'liveness 8081 %s\n' "$(curl -s -o /dev/null -w '%{http_code}' --max-time 2 http://10.0.0.158:8081/actuator/health/liveness)"
  printf 'gateway events %s\n' "$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 'http://10.0.0.158:8081/api/v1/events?size=1')"
  log "kiem xong";;
esac
