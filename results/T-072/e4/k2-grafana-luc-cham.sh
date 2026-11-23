#!/bin/bash
# T-072 E4 lúc chấm: CHỈ ĐỌC (grafana.db 3 bảng, bộ nhận, trạng thái container). Không Prometheus.
echo "date=$(date -u +%FT%TZ)"
wc -l < /srv/rca-lab/runs/t072-e3-01/webhook.jsonl; sha256sum /srv/rca-lab/runs/t072-e3-01/webhook.jsonl
docker inspect --format 'grafana StartedAt={{.State.StartedAt}} Restart={{.RestartCount}}' flash-ticket-obs-grafana
docker inspect --format 'bo_nhan {{.State.Health.Status}} Restart={{.RestartCount}}' flash-ticket-t072-bo-nhan
git -C /opt/rca-lab rev-parse --short HEAD
sudo -n python3 - <<'PY'
import sqlite3, json
c=sqlite3.connect('file:/var/lib/docker/volumes/flash-ticket-obs-pinned_grafana-data/_data/grafana.db?mode=ro', uri=True)
R={r[0]:r[1] for r in c.execute('select id,uid from alert_rule')}
A=[(R.get(a),b,cc,d) for a,b,cc,d in c.execute('select alert_id,prev_state,new_state,epoch from annotation where alert_id>0 and epoch>=1795327554000 order by epoch')]
print(json.dumps({'so_luat':len(R),'annotation_tu_G':A,'so_instance':c.execute('select count(*) from alert_instance').fetchone()[0]}))
PY
docker logs --since 2026-11-22T10:00:00Z --until 2026-11-22T18:10:00Z flash-ticket-obs-grafana 2>&1 | python3 -c "
import sys,re,collections
d=collections.Counter(); s=collections.Counter()
for l in sys.stdin:
    if 'Plugin Request Completed' in l and 'uname=grafana_scheduler' in l:
        m=re.search(r' t=(\d{4}-\d\d-\d\dT\d\d:\d\d)',l); d[m.group(1)]+=1; s[re.search(r'status=(\w+)',l).group(1)]+=1
ph=sorted(d); print('phut',len(ph),ph[0],ph[-1],'du66',sum(1 for p in ph if d[p]==66),'khac',[(p,d[p]) for p in ph if d[p]!=66][:10],dict(s))"
