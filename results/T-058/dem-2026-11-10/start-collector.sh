#!/usr/bin/env bash
set -Eeuo pipefail
python3 /home/ubuntu/t058/setup-collector.py
mkdir -p /opt/flash-ticket-app/otel
curl -fSL https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v2.33.1/opentelemetry-javaagent.jar -o /opt/flash-ticket-app/otel/opentelemetry-javaagent.jar
chmod 644 /opt/flash-ticket-app/otel/opentelemetry-javaagent.jar
sha256sum /opt/flash-ticket-app/otel/opentelemetry-javaagent.jar > /home/ubuntu/t058/agent.sha256
docker pull otel/opentelemetry-collector-contrib:0.165.0
docker compose -f /opt/flash-ticket-app/collector/compose.json -p flash-ticket-collector run --rm --no-deps collector validate --config=/etc/otel/config.json
docker compose -f /opt/flash-ticket-app/collector/compose.json -p flash-ticket-collector up -d
date -u
touch /home/ubuntu/t058/collector.started
