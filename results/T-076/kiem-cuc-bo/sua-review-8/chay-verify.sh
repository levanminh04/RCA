#!/usr/bin/env bash
# T-076, kiểm bản sửa theo REVIEW-8 (28/11), main f0a5d30 không đổi. Gốc: ../sua-review-6/chay-verify.sh;
# khác: chỉ Payment (service duy nhất có code sửa); bỏ bộ kiểm K8s (không đổi file K8s/CD, main không tiến).
#   bash chay-verify.sh <worktree> <thư mục ra> <python có jsonschema==4.25.1>
# Mỗi bước ghi log riêng và một dòng tien-do.tsv (bước, mã thoát, giây). Không dừng khi một bước lỗi.
set -uo pipefail
W=${1:?worktree}; RA=${2:?thư mục ra}; PY=${3:?python}
mkdir -p "$RA/log"
T="$RA/tien-do.tsv"; printf 'buoc\tma_thoat\tgiay\tbat_dau_utc\n' > "$T"

buoc() { # buoc <tên> <thư mục> <lệnh...>
  local ten=$1 dir=$2; shift 2
  local t0; t0=$(date +%s); local u; u=$(date -u +%FT%TZ)
  (cd "$W/$dir" && "$@") > "$RA/log/$ten.log" 2>&1
  local rc=$?
  printf '%s\t%s\t%s\t%s\n' "$ten" "$rc" "$(( $(date +%s) - t0 ))" "$u" >> "$T"
}

# Dịch vụ phụ như CI (cùng image, cùng tài khoản thử).
docker rm -f pr17-ci-postgres pr17-ci-rabbitmq > /dev/null 2>&1
docker run -d --name pr17-ci-postgres -e POSTGRES_DB=ticket_test_c1 -e POSTGRES_USER=ticket_ci \
  -e POSTGRES_PASSWORD=ticket_ci_disposable -p 127.0.0.1:15432:5432 postgres:16.15 > /dev/null
docker run -d --name pr17-ci-rabbitmq --user 999:999 -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest \
  -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-rabbit loopback_users none' -p 127.0.0.1:5672:5672 rabbitmq:4.3.6-management > /dev/null
for i in $(seq 1 60); do
  docker exec pr17-ci-postgres pg_isready -U ticket_ci -d ticket_test_c1 > /dev/null 2>&1 \
    && docker exec pr17-ci-rabbitmq rabbitmq-diagnostics -q ping > /dev/null 2>&1 && break
  sleep 5
done
printf 'dich_vu_phu_san_sang\t%s\t-\t%s\n' "$i" "$(date -u +%FT%TZ)" >> "$T"

export JAVA_TOOL_OPTIONS=-Duser.timezone=UTC
buoc payment-service-verify services/payment-service ./mvnw -B -ntp verify
buoc payment-service-b16 . "$PY" deploy/observability/verify_logs.py services/payment-service/target/b16-log-samples.jsonl

docker rm -f pr17-ci-postgres pr17-ci-rabbitmq > /dev/null 2>&1
printf 'xong\t-\t-\t%s\n' "$(date -u +%FT%TZ)" >> "$T"
