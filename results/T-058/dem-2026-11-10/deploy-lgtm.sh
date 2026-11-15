#!/usr/bin/env bash
set -Eeuo pipefail
while [ ! -f /home/ubuntu/t058/bootstrap.done ]; do sleep 10; done
sudo mkdir -p /opt/flash-ticket-obs
sudo chown ubuntu:ubuntu /opt/flash-ticket-obs
umask 077
if [ ! -f /opt/flash-ticket-obs/grafana.env ]; then
  printf 'GF_SECURITY_ADMIN_USER=admin\nGF_SECURITY_ADMIN_PASSWORD=%s\nGF_AUTH_ANONYMOUS_ENABLED=false\nENABLE_LOGS_OTELCOL=true\n' "$(openssl rand -hex 24)" > /opt/flash-ticket-obs/grafana.env
fi
cat > /opt/flash-ticket-obs/compose-lgtm.yml <<'YAML'
services:
  lgtm:
    image: grafana/otel-lgtm:0.40.0
    container_name: flash-ticket-lgtm
    restart: unless-stopped
    mem_limit: 6g
    env_file: grafana.env
    ports:
      - "10.0.0.215:3000:3000"
      - "10.0.0.215:4317:4317"
      - "10.0.0.215:4318:4318"
      - "127.0.0.1:9090:9090"
      - "127.0.0.1:3100:3100"
      - "127.0.0.1:3200:3200"
    volumes:
      - lgtm-data:/data
    logging:
      driver: json-file
      options: {max-size: 10m, max-file: "3"}
volumes:
  lgtm-data:
YAML
docker compose -f /opt/flash-ticket-obs/compose-lgtm.yml -p flash-ticket-obs config --quiet
docker compose -f /opt/flash-ticket-obs/compose-lgtm.yml -p flash-ticket-obs up -d
python3 - <<'PY'
import json, subprocess, pathlib
x=json.loads(subprocess.check_output(['docker','image','inspect','grafana/otel-lgtm:0.40.0']))[0]
pathlib.Path('/home/ubuntu/t058/lgtm-manifest.json').write_text(json.dumps({k:x[k] for k in ['Id','RepoDigests','Architecture']},indent=2)+'\n')
PY
date -u
touch /home/ubuntu/t058/lgtm.started
