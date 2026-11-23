#!/bin/bash
# T-072 E3 bước 7: một lần đọc (chỉ đọc). In 1 dòng JSON.
python3 - <<'PY'
import json, os, subprocess, time
D='/srv/rca-lab/runs/t071-e3/DA-PHAT'; W='/srv/rca-lab/runs/t072-e3-01/webhook.jsonl'
o={'now':time.time()}
o['da_phat']=os.path.getmtime(D) if os.path.exists(D) else None
fire={}; res={}; n=0
for l in open(W, encoding='utf-8'):
    n+=1; d=json.loads(l)
    if d['duong_dan']!='/t072': continue
    try: b=json.loads(d['than'])
    except Exception: continue
    for a in b.get('alerts',[]):
        u=a.get('labels',{}).get('t072_uid','?')
        (fire if a.get('status')=='firing' else res).setdefault(u,0)
        if a.get('status')=='firing': fire[u]+=1
        else: res[u]+=1
o['dong']=n; o['firing']=fire; o['resolved']=res
g=subprocess.run(['python3','load/controller/tai_linux.py','get','--tag','t071-e3-duong-01'],cwd='/opt/rca-lab',capture_output=True,text=True,timeout=170)
try:
    j=json.loads(g.stdout.strip().splitlines()[-1]); st=(j.get('result') or {}).get('state') or {}
    o['tai']={'ok':j.get('ok'),'Running':st.get('Running'),'StartedAt':st.get('StartedAt'),'FinishedAt':st.get('FinishedAt'),'ExitCode':st.get('ExitCode'),'loi':str(j.get('error'))[:150] if not j.get('ok') else None}
except Exception as e:
    o['tai']={'ok':False,'loi':(repr(e)+' '+g.stdout[-150:]+g.stderr[-150:])}
print(json.dumps(o))
PY
