#!/bin/bash
C=/srv/rca-lab/runs/t072-e3-01-cfg
cd /opt/rca-lab; echo "head=$(git rev-parse HEAD) sach=[$(git status --porcelain)]"
pgrep -af "chuoi_tai|runner4|tai_linux|stage_b|orchestrator|inj3|xuat_chuoi" | grep -v pgrep && { echo "CO JOB - dung"; exit 3; }
T0=$(date -u +%FT%TZ); echo "restart=$T0"
docker restart flash-ticket-obs-grafana >/dev/null
docker inspect --format 'StartedAt={{.State.StartedAt}}' flash-ticket-obs-grafana
for i in $(seq 1 60); do h=$(curl -s --max-time 5 http://10.0.0.215:3000/api/health); echo "$h" | grep -q '"database": "ok"' && break; sleep 2; done
echo "health_ok=$(date -u +%FT%TZ) $(echo $h | tr -d '\n ')"
sleep 90
echo "doc_log=$(date -u +%FT%TZ)"
docker logs --since "$T0" flash-ticket-obs-grafana > $C/grafana-log-sau-restart.txt 2>&1
wc -l < $C/grafana-log-sau-restart.txt
echo "--- dem theo logger"; grep -o 'logger=[^ ]*' $C/grafana-log-sau-restart.txt | sort | uniq -c | sort -rn | head -25
echo "--- level"; grep -o 'level=[a-z]*' $C/grafana-log-sau-restart.txt | sort | uniq -c
echo "--- provisioning/alerting"; grep -i -E 'provision|alerting' $C/grafana-log-sau-restart.txt | grep -v -i 'dashboard' | cut -c1-400 | head -40
echo "--- error/warn"; grep -E 'level=(error|warn)' $C/grafana-log-sau-restart.txt | cut -c1-400 | head -30
echo "--- t072"; grep -c -i t072 $C/grafana-log-sau-restart.txt; grep -i -o 't072-[a-z0-9-]*' $C/grafana-log-sau-restart.txt | sort | uniq -c
echo "--- bo nhan"; wc -l < /srv/rca-lab/runs/t072-e3-01/webhook.jsonl; cut -c1-200 /srv/rca-lab/runs/t072-e3-01/webhook.jsonl
docker ps --format '{{.Names}}\t{{.Status}}' | grep -E 'grafana|t072'
