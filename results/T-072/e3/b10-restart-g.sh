#!/bin/bash
C=/srv/rca-lab/runs/t072-e3-01-cfg; L=$C/grafana-log-sau-g.txt
cd /opt/rca-lab; echo "head=$(git rev-parse --short HEAD) sach=[$(git status --porcelain)]"
T0=$(date -u +%FT%TZ); echo "restart=$T0"
docker restart flash-ticket-obs-grafana >/dev/null
docker inspect --format 'StartedAt={{.State.StartedAt}}' flash-ticket-obs-grafana
for i in $(seq 1 60); do h=$(curl -s --max-time 5 http://10.0.0.215:3000/api/health); echo "$h" | grep -q '"database": "ok"' && break; sleep 2; done
echo "health_ok=$(date -u +%FT%TZ) $(echo $h | tr -d '\n ')"
sleep 75
docker logs --since "$T0" flash-ticket-obs-grafana > $L 2>&1; sha256sum $L
echo "--- provisioning.alerting"; grep 'logger=provisioning.alerting' $L | cut -c1-300
echo "--- state cache / scheduler"; grep -E 'State cache|Starting scheduler|first_tick' $L | cut -c1-300
echo "--- truy van scheduler theo 10s"; grep 'Plugin Request Completed' $L | grep 'uname=grafana_scheduler' | grep -o 't=2026-11-22T[0-9:]*' | cut -c3-20 | sort | uniq -c | head -12
echo "--- status"; grep 'Plugin Request Completed' $L | grep 'uname=grafana_scheduler' | grep -o 'status=[a-z]*' | sort | uniq -c
echo "--- error"; grep 'level=error' $L | cut -c1-250
echo "--- bo nhan"; wc -l < /srv/rca-lab/runs/t072-e3-01/webhook.jsonl; docker ps --format '{{.Names}} {{.Status}}' | grep -E 'grafana|t072'
