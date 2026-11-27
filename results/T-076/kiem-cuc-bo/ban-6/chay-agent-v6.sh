#!/usr/bin/env bash
# T-076 bước 4 bản 6: chạy Booking với env dựng theo đúng thứ tự K8s của nhánh:
#   ConfigMap (deploy/k8s/booking-service/configmap.yaml) → Secret giả (có thể chứa OTEL_AGENT_ENABLED=true)
#   → env: của deployment.yaml (OTEL_AGENT_ENABLED="false", HOST_ID) đặt sau cùng nên thắng.
# Đây là mô phỏng quy tắc "env thắng envFrom" bằng thứ tự dòng trong env_file (dòng sau thắng), không phải K8s thật.
#   bash chay-agent-v6.sh <worktree> <WORK> <thư mục ra> <tên lượt> <secret_agent: true|false|khong> [ghi_de_agent: true]
set -euo pipefail
export MSYS_NO_PATHCONV=1
W=${1:?}; export WORK=${2:?}; RA=${3:?}; LUOT=${4:?}; SECRET_AGENT=${5:?}; GHI_DE=${6:-}
HERE=$(cd "$(dirname "$0")" && pwd)
export SERVICE_VERSION=$(git -C "$W" rev-parse HEAD)
mkdir -p "$RA/$LUOT" "$WORK/out"; rm -f "$WORK/out/"*.jsonl
py -3 - "$W/deploy/k8s/booking-service/configmap.yaml" "$W/deploy/k8s/booking-service/deployment.yaml" \
  "$WORK/booking.env" "$SECRET_AGENT" "$GHI_DE" <<'PY'
import sys, yaml
cm, dep, out, secret_agent, ghi_de = sys.argv[1:]
dong = []
# 1. ConfigMap của nhánh, chỉ trỏ hạ tầng giả
d = dict(yaml.safe_load(open(cm, encoding='utf-8'))['data'])
d.update({'EUREKA_CLIENT_ENABLED': 'false', 'BOOKING_DB_URL': 'jdbc:postgresql://pg:5432/booking_db',
          'BOOKING_DDL_AUTO': 'create', 'REDIS_HOST': 'redis', 'RABBITMQ_HOST': 'rabbit', 'RABBITMQ_USERNAME': 'guest',
          'KEYCLOAK_ISSUER_URI': 'http://keycloak-gia.invalid/realms/thu',
          'KEYCLOAK_TOKEN_URI': 'http://keycloak-gia.invalid/realms/thu/protocol/openid-connect/token',
          'OTEL_TRACES_SAMPLER': 'always_on', 'OTEL_BSP_SCHEDULE_DELAY': '1000', 'OTEL_METRIC_EXPORT_INTERVAL': '5000',
          'SPRING_RABBITMQ_LISTENER_SIMPLE_MISSING_QUEUES_FATAL': 'false', 'POD_IP': '127.0.0.1', 'POD_UID': 'thu'})
dong += list(d.items())
# 2. Secret giả
dong += [('BOOKING_DB_PASSWORD', 'thu'), ('REDIS_PASSWORD', 'thu'), ('RABBITMQ_PASSWORD', 'guest'),
         ('INTERNAL_SERVICE_CLIENT_SECRET', 'SENTINELSECRET-client')]
if secret_agent != 'khong':
    dong.append(('OTEL_AGENT_ENABLED', secret_agent))
# 3. env: của deployment.yaml (sau cùng, thắng)
for doc in [x for x in yaml.safe_load_all(open(dep, encoding='utf-8')) if x]:
    for c in doc['spec']['template']['spec']['containers']:
        for e in c.get('env', []):
            if e['name'] == 'OTEL_AGENT_ENABLED':
                dong.append((e['name'], e['value']))
            if e['name'] == 'HOST_ID':
                dong.append(('HOST_ID', 'node-thu'))  # downward API spec.nodeName
if ghi_de == 'true':  # chỉ cho lượt thử đường bật: ghi đè thủ công
    dong.append(('OTEL_AGENT_ENABLED', 'true'))
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    for k, v in dong:
        f.write(f'{k}={str(v).replace("$", "$$")}\n')
PY
cd "$HERE"
docker compose down -v --remove-orphans > /dev/null 2>&1 || true
docker compose up -d > "$RA/$LUOT/compose-up.log" 2>&1
for i in $(seq 1 90); do
  curl -fsS http://127.0.0.1:18082/actuator/health/readiness > /dev/null 2>&1 && break
  sleep 2
done
{ printf 'san_sang_sau_giay\t%s\n' "$((i*2))"
  printf 'agent_env_cuoi\t%s\n' "$(docker compose exec -T booking sh -c 'echo $OTEL_AGENT_ENABLED')"
  docker stats --no-stream --format '{{.Name}}\t{{.MemUsage}}' | grep booking || true; } > "$RA/$LUOT/tom-tat.tsv"
EV=5e000000-0000-4000-8000-00000000e1d0
for i in 1 2 3; do
  curl -s -o /dev/null "http://127.0.0.1:18082/api/v1/events/$EV/availability?email=sentinel.email%40example.com&phone=0900111222&q=SENTINELQUERYQ&vnp_SecureHash=SENTINELHASHQ&vnp_TxnRef=SENTINELTXNQ" \
    -H 'Authorization: Bearer SENTINELJWT.eyJ.x' -H 'Cookie: session=SENTINELCOOKIE' || true
done
sleep 12
printf 'dong_khoi_dong_agent\t%s\n' "$(docker compose logs booking 2>&1 | grep -c 'opentelemetry-javaagent - version' || true)" >> "$RA/$LUOT/tom-tat.tsv"
docker compose logs booking > "$RA/$LUOT/booking.log" 2>&1 || true
cp "$WORK/out/"*.jsonl "$RA/$LUOT/" 2>/dev/null || true
for f in traces metrics; do printf 'byte_%s\t%s\n' "$f" "$(wc -c < "$WORK/out/$f.jsonl" 2>/dev/null || echo 0)" >> "$RA/$LUOT/tom-tat.tsv"; done
docker compose down -v --remove-orphans > /dev/null 2>&1 || true
