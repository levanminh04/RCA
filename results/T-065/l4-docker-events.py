import json, subprocess
args=['docker','events','--since','2026-11-14T01:39:00Z','--until','2026-11-14T01:40:10Z','--filter','container=flash-ticket-obs-grafana','--format','{{json .}}']
p=subprocess.run(args,capture_output=True,text=True,check=True)
for line in p.stdout.splitlines():
 d=json.loads(line); a=d.get('Actor',{}).get('Attributes',{}); print(json.dumps({'time':d.get('timeNano'),'action':d.get('Action'),'exitCode':a.get('exitCode'),'signal':a.get('signal')}))
