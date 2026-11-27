#!/usr/bin/env bash
# T-076 bước 4: chạy Booking (image dựng từ nhánh PR, agent bật) gửi tới Collector thử không processor (TLS + token),
# gửi request mang sentinel giả, rồi tìm sentinel trong payload thô. Dữ liệu và khóa đều giả, ở thư mục WORK.
#   bash chay-agent.sh <worktree> <WORK> <thư mục ra> <tên lượt> [KEY=VALUE thêm vào env Booking ...]
set -euo pipefail
export MSYS_NO_PATHCONV=1
W=${1:?worktree}; export WORK=${2:?WORK}; RA=${3:?ra}; LUOT=${4:?tên lượt}; shift 4
HERE=$(cd "$(dirname "$0")" && pwd)
export SERVICE_VERSION=$(git -C "$W" rev-parse HEAD)
mkdir -p "$RA/$LUOT" "$WORK/tls" "$WORK/out"
rm -f "$WORK/out/"*.jsonl

# CA + chứng chỉ thử (chỉ cho lượt này, không dùng ở đâu khác)
if [ ! -f "$WORK/tls/ca.crt" ]; then
  openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 2 -subj "/CN=pr17 thu CA" \
    -keyout "$WORK/tls/ca.key" -out "$WORK/tls/ca.crt" 2>/dev/null
  openssl req -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -subj "/CN=otel-thu" \
    -keyout "$WORK/tls/server.key" -out "$WORK/tls/server.csr" 2>/dev/null
  printf 'subjectAltName=DNS:otel-thu\nextendedKeyUsage=serverAuth\n' > "$WORK/tls/ext"
  openssl x509 -req -in "$WORK/tls/server.csr" -CA "$WORK/tls/ca.crt" -CAkey "$WORK/tls/ca.key" -CAcreateserial \
    -days 2 -extfile "$WORK/tls/ext" -out "$WORK/tls/server.crt" 2>/dev/null
  chmod 644 "$WORK/tls/"*
fi
export TOKEN_THU=token-thu-$(od -An -N8 -tx1 /dev/urandom | tr -d ' \n')

# env Booking = ConfigMap của nhánh (khối agent + cấu hình app) + ghi đè trỏ hạ tầng giả + Secret giả
py -3 - "$W/deploy/k8s/booking-service/configmap.yaml" "$WORK/booking.env" "$WORK/tls/ca.crt" "$TOKEN_THU" "$@" <<'PY'
import base64, sys, yaml
cm, out, ca, token, *extra = sys.argv[1:]
d = dict(yaml.safe_load(open(cm, encoding='utf-8'))['data'])
d.update({
  'OTEL_EXPORTER_OTLP_ENDPOINT': 'https://otel-thu:4318',
  'OTEL_CA_PEM_B64': base64.b64encode(open(ca, 'rb').read()).decode(),
  'OTEL_TRACES_SAMPLER': 'always_on', 'ENVIRONMENT': 'thu-cuc-bo', 'HOST_ID': 'laptop-thu',
  'OTEL_BSP_SCHEDULE_DELAY': '1000', 'OTEL_METRIC_EXPORT_INTERVAL': '5000',
  'POD_IP': '127.0.0.1', 'POD_UID': 'thu', 'EUREKA_CLIENT_ENABLED': 'false',
  'BOOKING_DB_URL': 'jdbc:postgresql://pg:5432/booking_db', 'BOOKING_DDL_AUTO': 'create',
  'REDIS_HOST': 'redis', 'RABBITMQ_HOST': 'rabbit', 'RABBITMQ_USERNAME': 'guest',
  'KEYCLOAK_ISSUER_URI': 'http://keycloak-gia.invalid/realms/thu',
  'KEYCLOAK_TOKEN_URI': 'http://keycloak-gia.invalid/realms/thu/protocol/openid-connect/token',
  # Secret giả
  'BOOKING_DB_PASSWORD': 'thu', 'REDIS_PASSWORD': 'thu', 'RABBITMQ_PASSWORD': 'guest',
  'INTERNAL_SERVICE_CLIENT_SECRET': 'SENTINELSECRET-client',
  'OTEL_AGENT_ENABLED': 'true', 'OTEL_EXPORTER_OTLP_HEADERS': 'Authorization=Bearer%20' + token,
})
for kv in extra:
    k, _, v = kv.partition('='); d[k] = v
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    for k, v in d.items():
        f.write(f'{k}={v.replace("$", "$$")}\n')  # env_file của Compose nội suy ${...}; $$ giữ nguyên ký tự $
PY

cd "$HERE"
docker compose down -v --remove-orphans > /dev/null 2>&1 || true
docker compose up -d > "$RA/$LUOT/compose-up.log" 2>&1
for i in $(seq 1 90); do
  curl -fsS http://127.0.0.1:18082/actuator/health/readiness > /dev/null 2>&1 && break
  sleep 2
done
printf 'san_sang_sau_giay\t%s\n' "$((i*2))" > "$RA/$LUOT/tom-tat.tsv"
docker stats --no-stream --format '{{.Name}}\t{{.MemUsage}}' | grep booking >> "$RA/$LUOT/tom-tat.tsv" || true

# Token: đúng / sai / không có / không TLS (gọi thẳng Collector từ một container trong cùng mạng)
NET=pr17-agent-thu_default
for ca in "sai:Bearer token-sai" "khong:" "dung:Bearer $TOKEN_THU"; do
  ten=${ca%%:*}; h=${ca#*:}
  code=$(docker run --rm --network "$NET" -v "$WORK/tls:/tls:ro" curlimages/curl:8.11.1 -s -o /dev/null -w '%{http_code}' \
    --cacert /tls/ca.crt ${h:+-H "Authorization: $h"} -H 'Content-Type: application/json' -d '{"resourceSpans":[]}' \
    https://otel-thu:4318/v1/traces || true)
  printf 'token_%s\t%s\n' "$ten" "$code" >> "$RA/$LUOT/tom-tat.tsv"
done
code=$(docker run --rm --network "$NET" curlimages/curl:8.11.1 -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer $TOKEN_THU" -d '{}' http://otel-thu:4318/v1/traces || true)
printf 'khong_tls\t%s\n' "$code" >> "$RA/$LUOT/tom-tat.tsv"

# Request mang sentinel: query (email, token, chữ ký kiểu VNPay), header Authorization/Cookie, body; một id ở path (bind DB/Redis)
EV=5e000000-0000-4000-8000-00000000e1d0
for i in 1 2 3; do
  curl -s -o /dev/null "http://127.0.0.1:18082/api/v1/events/$EV/availability?email=sentinel.email%40example.com&phone=0900111222&token=SENTINELTOKENQ&vnp_SecureHash=SENTINELHASHQ" \
    -H 'Authorization: Bearer SENTINELJWT.eyJ.x' -H 'Cookie: session=SENTINELCOOKIE' || true
  curl -s -o /dev/null -X POST "http://127.0.0.1:18082/api/v1/orders?code=SENTINELCODEQ" \
    -H 'Authorization: Bearer SENTINELJWT.eyJ.x' -H 'Content-Type: application/json' -d '{"note":"SENTINELBODY","email":"sentinel.body@example.com"}' || true
  curl -s -o /dev/null "http://127.0.0.1:18082/api/v1/events/SENTINELPATHBAD/availability" || true
done
sleep 12
docker compose logs booking > "$RA/$LUOT/booking.log" 2>&1 || true
docker compose logs otel-thu > "$RA/$LUOT/collector.log" 2>&1 || true
docker compose logs pg > "$RA/$LUOT/pg.log" 2>&1 || true
cp "$WORK/out/"*.jsonl "$RA/$LUOT/" 2>/dev/null || true
docker compose down -v --remove-orphans > /dev/null 2>&1 || true
