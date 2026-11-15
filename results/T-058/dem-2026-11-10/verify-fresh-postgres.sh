#!/usr/bin/env bash
set -Eeuo pipefail
name=ft-init-verify
docker run -d --name "$name" --network none --env-file /opt/flash-ticket-infra/.env \
  --mount type=volume,source=ft-init-verify-data,target=/var/lib/postgresql/data \
  --mount type=bind,source=/opt/flash-ticket-infra/deploy/postgres/00-business-databases.sh,target=/docker-entrypoint-initdb.d/00-business-databases.sh,readonly \
  --mount type=bind,source=/opt/flash-ticket-infra/docs/architecture/data/postgres,target=/opt/flash-ticket/postgres,readonly \
  --mount type=bind,source=/opt/flash-ticket-infra/services/99-table-prefix.sql,target=/opt/flash-ticket/99-table-prefix.sql,readonly \
  --mount type=bind,source=/opt/flash-ticket-infra/services/event-service/database/90-erd-reader.sql,target=/opt/flash-ticket/readers/event.sql,readonly \
  --mount type=bind,source=/opt/flash-ticket-infra/services/booking-service/database/90-erd-reader.sql,target=/opt/flash-ticket/readers/booking.sql,readonly \
  --mount type=bind,source=/opt/flash-ticket-infra/services/payment-service/database/90-erd-reader.sql,target=/opt/flash-ticket/readers/payment.sql,readonly \
  --mount type=bind,source=/opt/flash-ticket-infra/services/ticket-service/database/90-erd-reader.sql,target=/opt/flash-ticket/readers/ticket.sql,readonly \
  postgres:16.15
for i in $(seq 1 60); do
  if docker exec "$name" psql -X -U postgres -d postgres -Atc "SELECT count(*) FROM pg_database WHERE datname IN ('event_db','booking_db','payment_db','ticket_db')" 2>/dev/null | grep -qx 4; then
    sleep 3
    break
  fi
  sleep 2
done
docker logs "$name" > /home/ubuntu/t058/fresh-postgres-init.log 2>&1
count=$(docker exec "$name" psql -X -U postgres -d postgres -Atc "SELECT count(*) FROM pg_database WHERE datname IN ('event_db','booking_db','payment_db','ticket_db')")
test "$count" = 4
for svc in event booking payment ticket; do
  docker exec "$name" psql -X -U postgres -d "${svc}_db" -Atc "SELECT count(*) FROM information_schema.tables WHERE table_schema='${svc}_schema' AND table_name LIKE 'tbl_%'"
done
docker stop "$name"
# Only the explicitly named disposable verification container is removed.
# Its log and volume are retained as evidence.
docker rm "$name"
date -u
touch /home/ubuntu/t058/fresh-postgres-init.done
