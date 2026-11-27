#!/usr/bin/env bash
# T-076 bước 4: Assistant (image dựng từ nhánh PR) khởi động với agent bật, cấu hình ConfigMap của nhánh, gửi tới
# Collector thử. Mục đích: kiểm agent + SPRING_AUTOCONFIGURE_EXCLUDE (Lettuce) không làm hỏng khởi động. Dùng lại
# WORK (CA, token) của chay-agent.sh.   bash chay-assistant.sh <worktree> <WORK> <thư mục ra>
set -euo pipefail
export MSYS_NO_PATHCONV=1
W=${1:?}; export WORK=${2:?}; RA=${3:?}/assistant
HERE=$(cd "$(dirname "$0")" && pwd)
export SERVICE_VERSION=$(git -C "$W" rev-parse HEAD)
mkdir -p "$RA" "$WORK/out"; rm -f "$WORK/out/"*.jsonl
export TOKEN_THU=token-thu-$(od -An -N8 -tx1 /dev/urandom | tr -d ' \n')
py -3 - "$W/deploy/k8s/assistant-service/configmap.yaml" "$WORK/assistant.env" "$WORK/tls/ca.crt" "$TOKEN_THU" <<'PY'
import base64, sys, yaml
cm, out, ca, token = sys.argv[1:]
d = dict(yaml.safe_load(open(cm, encoding='utf-8'))['data'])
d.update({
  'OTEL_EXPORTER_OTLP_ENDPOINT': 'https://otel-thu:4318', 'OTEL_CA_PEM_B64': base64.b64encode(open(ca, 'rb').read()).decode(),
  'OTEL_TRACES_SAMPLER': 'always_on', 'ENVIRONMENT': 'thu-cuc-bo', 'HOST_ID': 'laptop-thu', 'OTEL_BSP_SCHEDULE_DELAY': '1000',
  'POD_IP': '127.0.0.1', 'POD_UID': 'thu', 'EUREKA_CLIENT_ENABLED': 'false', 'REDIS_HOST': 'redis',
  'KEYCLOAK_ISSUER_URI': 'http://keycloak-gia.invalid/realms/thu',
  'REDIS_PASSWORD': 'thu', 'ASSISTANT_MODEL_API_KEY': 'SENTINELSECRET-model',
  'OTEL_AGENT_ENABLED': 'true', 'OTEL_EXPORTER_OTLP_HEADERS': 'Authorization=Bearer%20' + token,
})
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    for k, v in d.items():
        f.write(f'{k}={v}\n')
PY
cd "$HERE"
docker compose down -v --remove-orphans > /dev/null 2>&1 || true
docker compose up -d redis otel-thu > "$RA/compose-up.log" 2>&1
PORT=$(grep -E '^ASSISTANT_SERVICE_PORT=' "$WORK/assistant.env" | cut -d= -f2)
docker run -d --name pr17-thu-assistant --network pr17-agent-thu_default --memory 768m --env-file "$WORK/assistant.env" \
  "pr17-thu/assistant-service:$SERVICE_VERSION" > /dev/null
ok=khong
for i in $(seq 1 60); do
  if docker exec pr17-thu-assistant curl -fsS "http://127.0.0.1:${PORT}/actuator/health/readiness" > /dev/null 2>&1; then ok=co; break; fi
  docker ps --filter name=pr17-thu-assistant --format '{{.Status}}' | grep -q Up || break
  sleep 2
done
sleep 8
{ printf 'san_sang\t%s\t%s giay\n' "$ok" "$((i*2))"; docker stats --no-stream --format '{{.Name}}\t{{.MemUsage}}' pr17-thu-assistant || true; } > "$RA/tom-tat.tsv"
docker logs pr17-thu-assistant > "$RA/assistant.log" 2>&1 || true
cp "$WORK/out/"*.jsonl "$RA/" 2>/dev/null || true
docker rm -f pr17-thu-assistant > /dev/null 2>&1 || true
docker compose down -v --remove-orphans > /dev/null 2>&1 || true
