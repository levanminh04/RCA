#!/bin/bash
# T-072 E4 tự kiểm: CHỈ ĐỌC. Không truy vấn Prometheus. grafana.db: alert_rule, alert_instance, annotation (cột cần).
C=/srv/rca-lab/runs/t072-e3-01-cfg; M=1795327554000
echo "date=$(date -u +%FT%TZ)"
echo "--- bo nhan"; wc -l < /srv/rca-lab/runs/t072-e3-01/webhook.jsonl; tail -1 /srv/rca-lab/runs/t072-e3-01/webhook.jsonl | cut -c1-120; sha256sum /srv/rca-lab/runs/t072-e3-01/webhook.jsonl
docker inspect --format 'bo_nhan {{.State.Status}} {{.State.Health.Status}} StartedAt={{.State.StartedAt}} Restart={{.RestartCount}}' flash-ticket-t072-bo-nhan
docker inspect --format 'grafana {{.State.Status}} StartedAt={{.State.StartedAt}} Restart={{.RestartCount}}' flash-ticket-obs-grafana
git -C /opt/rca-lab rev-parse --short HEAD
echo "--- db"
sudo -n python3 - <<PY
import sqlite3, json
c=sqlite3.connect('file:/var/lib/docker/volumes/flash-ticket-obs-pinned_grafana-data/_data/grafana.db?mode=ro', uri=True)
R={r[0]:r[1] for r in c.execute('select id,uid from alert_rule')}
A=[(R.get(a),b,cc,d) for a,b,cc,d in c.execute('select alert_id,prev_state,new_state,epoch from annotation where alert_id>0 and epoch>=? order by epoch',($M,))]
I=c.execute('select count(*) from alert_instance').fetchone()[0]
print(json.dumps({'so_luat':len(R),'uid':sorted(R.values()),'annotation_tu_G':A,'so_instance':I}))
PY
echo "--- log grafana tu 06:05:54"
docker logs --since 2026-11-22T06:05:54Z flash-ticket-obs-grafana > $C/grafana-log-e4.txt 2>&1
sha256sum $C/grafana-log-e4.txt; wc -l < $C/grafana-log-e4.txt
python3 - $C/grafana-log-e4.txt <<'PY'
import re, sys, collections, json
dem=collections.Counter(); st=collections.Counter(); err=collections.Counter(); khac=collections.Counter()
for l in open(sys.argv[1], errors='replace'):
    m=re.search(r' t=(\d{4}-\d\d-\d\dT\d\d:\d\d)', l)
    if 'Plugin Request Completed' in l and 'uname=grafana_scheduler' in l and m:
        dem[m.group(1)]+=1; st[re.search(r'status=(\w+)', l).group(1)]+=1
    elif 'level=error' in l:
        err[(re.search(r'logger=(\S+)', l) or re.search(r'(msg="[^"]*")', l) or ['?','?'])[1]]+=1
    if 'logger=ngalert' in l and ('level=warn' in l or 'level=error' in l): khac[l[:160]]+=1
ph=sorted(dem); full=[p for p in ph if dem[p]==66]; le=[(p,dem[p]) for p in ph if dem[p]!=66]
print(json.dumps({'phut_dau':ph[0] if ph else None,'phut_cuoi':ph[-1] if ph else None,'so_phut':len(ph),'phut_du_66':len(full),
 'phut_khac_66':le[:40],'so_phut_khac_66':len(le),'status':dict(st),'error_theo_logger':dict(err),'ngalert_warn_error':list(khac.items())[:10]}))
PY
