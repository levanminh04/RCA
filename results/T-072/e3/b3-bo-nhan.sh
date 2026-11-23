#!/bin/bash
set -e
R=/srv/rca-lab/runs/t072-e3-01; C=/srv/rca-lab/runs/t072-e3-01-cfg; E=$C/webhook.env
install -d -m 0700 $R $C
echo "pull_bat_dau=$(date -u +%FT%TZ)"
docker pull -q python:3.12-slim
IMG=$(docker image inspect --format '{{index .RepoDigests 0}}' python:3.12-slim)
docker image inspect --format 'image_id={{.Id}} size={{.Size}}' python:3.12-slim
echo "digest=$IMG $(date -u +%FT%TZ)"
umask 077
cat > $E <<ENV
T073_WEBHOOK_IMAGE=$IMG
T073_SPOOL_DIR=/srv/rca-lab/runs/t073-khong-dung-o-e3/spool
T072_RA_DIR=$R
ENV
chmod 600 $E; echo "--- env"; cat $E
echo "--- obs truoc"; for c in prometheus grafana loki tempo collector; do docker inspect --format "{{.Name}} {{.State.StartedAt}}" flash-ticket-obs-$c; done
cd /opt/rca-lab/observability
echo "up=$(date -u +%FT%TZ)"
docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml up -d t072-bo-nhan 2>&1 | tail -3
for i in $(seq 1 20); do s=$(docker inspect --format '{{.State.Health.Status}}' flash-ticket-t072-bo-nhan); [ "$s" = healthy ] && break; sleep 5; done
echo "health=$s $(date -u +%FT%TZ)"
docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml ps
echo "--- obs sau"; for c in prometheus grafana loki tempo collector; do docker inspect --format "{{.Name}} {{.State.StartedAt}}" flash-ticket-obs-$c; done
docker inspect --format 'user={{.Config.User}} ro={{.HostConfig.ReadonlyRootfs}} ports={{json .HostConfig.PortBindings}} mounts={{range .Mounts}}{{.Source}}->{{.Destination}}:{{.RW}} {{end}}' flash-ticket-t072-bo-nhan
echo "--- tin thu tay $(date -u +%FT%TZ)"
docker run --rm --network flash-ticket-obs-pinned_default --read-only --user 1001:1001 "$IMG" python -c "
import json,urllib.request,datetime
b=json.dumps({'t072_tay':True,'ghi_chu':'tin thu tay E3 buoc 3, khong phai Grafana','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}).encode()
r=urllib.request.urlopen(urllib.request.Request('http://t072-bo-nhan:9172/t072-tay',data=b,headers={'Content-Type':'application/json'}),timeout=10)
print('http',r.status,r.read())"
sleep 1; echo "--- webhook.jsonl"; ls -la $R; cat $R/webhook.jsonl
