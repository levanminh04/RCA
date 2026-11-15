#!/usr/bin/env python3
import datetime
import json
from pathlib import Path
import subprocess
import time
import urllib.request

root = Path('/home/ubuntu/t058')
deadline = time.monotonic()+900
while not all((root / f).exists() for f in ['build.done', 'infra.done']):
    if time.monotonic() > deadline:
        raise SystemExit('Timed out waiting for build.done and infra.done')
    time.sleep(5)
images = {s['service']: s for s in json.loads((root/'build-manifest.json').read_text())}
ports = {'discovery-server':8761, 'keycloak':8080, 'api-gateway':8081,
         'booking-service':8082, 'payment-service':8083, 'ticket-service':8084,
         'user-service':8085, 'event-service':8086}
records = []
for svc in ['discovery-server','keycloak','user-service','event-service','ticket-service','booking-service','payment-service','api-gateway']:
    rec = {'service':svc, 'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    if images[svc].get('architecture') != 'arm64':
        rec['result']='build unavailable'
        records.append(rec)
        continue
    print(rec['started_at'], svc, 'START', flush=True)
    import os
    env = dict(os.environ, IMAGE=images[svc]['image'])
    cmd = ['docker','compose','-f',f'/opt/flash-ticket-app/compose/{svc}.yml','-p','flash-ticket-'+svc,'up','-d']
    run = subprocess.run(cmd, env=env)
    rec['compose_exit'] = run.returncode
    url = ('http://10.0.0.158:8080/realms/flash-ticket/.well-known/openid-configuration'
           if svc=='keycloak' else f'http://{"10.0.0.158" if svc=="api-gateway" else "127.0.0.1"}:{ports[svc]}/actuator/health')
    rec['health_url']=url
    limit = time.monotonic()+180
    while run.returncode == 0 and time.monotonic()<limit:
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                result=json.load(r)
            rec['health'] = 'UP' if svc=='keycloak' else result.get('status')
            if rec['health']=='UP':
                break
        except Exception as e:
            rec['last_health_error']=type(e).__name__
            if svc not in ['keycloak','discovery-server']:
                try:
                    req=urllib.request.Request('http://127.0.0.1:8761/eureka/apps',headers={'Accept':'application/json'})
                    with urllib.request.urlopen(req,timeout=5) as response:
                        apps=json.load(response)['applications'].get('application',[])
                    found=next((a for a in apps if a['name']==svc.upper()),None)
                    if found and any(i['status']=='UP' for i in (found['instance'] if isinstance(found['instance'],list) else [found['instance']])):
                        rec['health']='UP'; rec['health_source']='Eureka (HTTP health protected)'
                        break
                except Exception:
                    pass
        time.sleep(5)
    rec['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    records.append(rec)
    (root/'startup-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    if rec.get('health')=='UP':
        Path(f'/opt/flash-ticket-app/state/{svc}.current').write_text(images[svc]['image_id']+'\n')
    print(rec['finished_at'],svc,rec.get('health','NOT_UP'),flush=True)
date = datetime.datetime.now(datetime.timezone.utc).isoformat()
print(date, 'STARTUP_COMPLETE',flush=True)
(root/'startup.done').touch()
