set -euo pipefail
date -u +%FT%TZ
cd /opt/rca-lab/observability
sudo -n docker compose -p t073-webhook --env-file /srv/rca-lab/runs/t072-e3-01-cfg/webhook.env -f compose.t073-webhook.yaml down
sudo -n docker compose -p flash-ticket-obs-pinned --env-file /opt/rca-lab/inventory/oracle-exp.env down
echo "== sau down"; sudo -n docker ps -a --format '{{.Names}} {{.Status}}'; sudo -n docker volume ls --format '{{.Name}}'
date -u +%FT%TZ
