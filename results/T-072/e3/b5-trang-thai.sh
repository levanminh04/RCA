#!/bin/bash
# T-072 E3 bước 5: CHỈ ĐỌC 3 bảng (alert_rule, alert_instance, annotation), chỉ cột cần; 3 lần cách 15 s.
for lan in 1 2 3; do
sudo -n python3 - "$lan" <<'PY'
import sqlite3, json, sys, datetime
db='/var/lib/docker/volumes/flash-ticket-obs-pinned_grafana-data/_data/grafana.db'
c=sqlite3.connect(f'file:{db}?mode=ro', uri=True)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
R=[dict(zip(['id','uid','rule_group','interval_seconds','for','no_data_state','exec_err_state','is_paused','updated','folder_fullpath'],r))
   for r in c.execute('select id,uid,rule_group,interval_seconds,"for",no_data_state,exec_err_state,is_paused,updated,folder_fullpath from alert_rule order by uid')]
I=[]
for r in c.execute('select rule_uid,labels,current_state,current_reason,current_state_since,last_eval_time,last_error,evaluation_duration_ns from alert_instance order by rule_uid'):
    lab=json.loads(r[1]) if r[1] else {}
    I.append({'rule_uid':r[0],'khoa':lab.get('http_url') or lab.get('http_route') or lab.get('alertname'),'state':r[2],'reason':r[3],
              'since':r[4],'last_eval':r[5],'last_error':(r[6] or '')[:200],'eval_ns':r[7]})
ids=[x['id'] for x in R]
A=[dict(zip(['alert_id','prev_state','new_state','epoch','text'],(a,b,cc,d,(e or '')[:120]))) for a,b,cc,d,e in
   c.execute('select alert_id,prev_state,new_state,epoch,text from annotation where alert_id>0 and epoch>=? order by epoch',(1795324624000,))]
print(json.dumps({'lan':int(sys.argv[1]),'doc_utc':now,'so_luat':len(R),'luat':R,'so_instance':len(I),'instance':I,'annotation_tu_restart':A}))
PY
[ $lan -lt 3 ] && sleep 15
done
