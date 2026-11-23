#!/bin/bash
# T-072 E3 bước 1: chỉ ĐỌC exp-obs.
echo "date_utc=$(date -u +%FT%T.%NZ | cut -c1-23)Z"
echo "--- /opt/rca-lab"; git -C /opt/rca-lab rev-parse HEAD; git -C /opt/rca-lab status --porcelain | head; stat -c '%U:%G %a %n' /opt/rca-lab /opt/rca-lab/observability
echo "--- STOP"; ls -la /srv/rca-lab/runs/STOP /srv/rca-lab/load-controller/STOP 2>&1
echo "--- job"; pgrep -af "chuoi_tai|runner4|tai_linux|stage_b|orchestrator|inj3|xuat_chuoi" | grep -v pgrep || echo "khong co job"
echo "--- docker ps"; docker ps --format '{{.Names}}\t{{.Status}}\t{{.Image}}'
echo "--- grafana"; docker inspect --format 'StartedAt={{.State.StartedAt}} RestartCount={{.RestartCount}}' flash-ticket-obs-grafana
docker exec flash-ticket-obs-grafana sh -c 'echo "STATE_HISTORY_ENABLED=$GF_UNIFIED_ALERTING_STATE_HISTORY_ENABLED|BACKEND=$GF_UNIFIED_ALERTING_STATE_HISTORY_BACKEND"'
curl -s --max-time 10 http://10.0.0.215:3000/api/health; echo
echo "--- mang"; docker network inspect flash-ticket-obs-pinned_default --format '{{range .Containers}}{{.Name}} {{end}}'
echo "--- runs"; stat -c '%U:%G %a %n' /srv/rca-lab/runs; ls -d /srv/rca-lab/runs/t072-* 2>&1; id ubuntu
echo "--- image python"; docker images python --format '{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}'
echo "--- remote"; git -C /opt/rca-lab remote -v | head -2; git -C /opt/rca-lab branch --show-current
