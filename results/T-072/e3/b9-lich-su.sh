#!/bin/bash
# T-072 E3 bước 9: CHỈ ĐỌC grafana.db (mode=ro; alert_rule, alert_instance, annotation; cột cần). Không chép DB.
sudo -n python3 - <<'PY'
import sqlite3, json, datetime
db='/var/lib/docker/volumes/flash-ticket-obs-pinned_grafana-data/_data/grafana.db'
c=sqlite3.connect(f'file:{db}?mode=ro', uri=True)
R={r[0]:r[1] for r in c.execute('select id,uid from alert_rule')}
A=[dict(zip(['alert_id','uid','prev_state','new_state','epoch','epoch_end','text'],(a,R.get(a),b,cc,d,e,(t or '')[:300]))) for a,b,cc,d,e,t in
   c.execute('select alert_id,prev_state,new_state,epoch,epoch_end,text from annotation where alert_id>0 and epoch>=? order by epoch,id',(1795324624000,))]
I=[]
for r in c.execute('select rule_uid,labels,current_state,current_reason,current_state_since,current_state_end,last_eval_time,fired_at,resolved_at,last_sent_at,last_error from alert_instance order by rule_uid'):
    lab=json.loads(r[1]) if r[1] else {}
    I.append(dict(zip(['rule_uid','khoa','state','reason','since','state_end','last_eval','fired_at','resolved_at','last_sent_at','last_error'],
      (r[0],lab.get('http_url') or lab.get('http_route') or lab.get('alertname'),r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],(r[10] or '')[:200]))))
print(json.dumps({'doc_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'so_luat':len(R),'annotation':A,'instance':I}))
PY
