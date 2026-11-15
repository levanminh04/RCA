#!/usr/bin/env bash
set -Eeuo pipefail
cd /opt/flash-ticket-infra
files=(--env-file .env -f deploy/docker-compose.postgresql.yml -f deploy/docker-compose.redis.yml -f deploy/docker-compose.rabbitmq.yml -f deploy/mongodb/compose.yaml -p flash-ticket-infra)
docker compose "${files[@]}" config --quiet
docker compose "${files[@]}" up -d --wait --wait-timeout 300
docker compose "${files[@]}" ps
date -u
touch /home/ubuntu/t058/infra.done
