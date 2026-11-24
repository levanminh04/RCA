set -euo pipefail
cd /opt/flashticket-rca/observability
sudo -n docker compose --env-file ../inventory/oracle-exp.env config --format json | python3 -c "import json,sys;d=json.load(sys.stdin);print('project',d['name']);print({k:[v.get('source') for v in s.get('volumes',[]) if v.get('type')=='bind'] for k,s in d['services'].items()})"
sudo -n docker compose --env-file ../inventory/oracle-exp.env up -d 2>&1 | tail -8
echo "== volume"; sudo -n docker volume ls --format '{{.Name}}'
cd alert-receiver
sudo -n docker compose -p t073-webhook --env-file /srv/flashticket-rca/alerts/receiver.env -f compose.yaml up -d t072-bo-nhan 2>&1 | tail -4
sleep 45
sudo -n docker ps --format '{{.Names}} {{.Status}} {{.Label "com.docker.compose.project"}}'
