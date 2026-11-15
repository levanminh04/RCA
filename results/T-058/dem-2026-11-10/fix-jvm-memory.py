"""STEER #4: deployment copies only; keep failed C3 data and JVM flags."""
import datetime,json,os,re,subprocess,time,urllib.request
from pathlib import Path
root=Path('/home/ubuntu/t058'); app=Path('/opt/flash-ticket-app')
if not (root/'resources-30m-app.done').exists(): raise SystemExit('C3 must finish first')
if (root/'jvm-memory-fixed.done').exists(): raise SystemExit('Correction already completed')
limits={'discovery-server':('384m','768m'),'keycloak':('768m','1536m'),
        'event-service':('512m','1g'),'booking-service':('512m','1g'),'payment-service':('512m','1g')}
images={x['service']:x['image'] for x in json.loads((root/'build-manifest.json').read_text())}
def states():
 ids=subprocess.check_output(['docker','ps','-aq'],text=True).split()
 return [{'name':x['Name'],'id':x['Id'],'limit_bytes':x['HostConfig']['Memory'],
          'restart_count':x['RestartCount'],'started_at':x['State']['StartedAt'],'running':x['State']['Running']}
         for x in json.loads(subprocess.check_output(['docker','inspect',*ids])) if x['Config']['Image'].startswith('ft-local/')]
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':states(),
        'reason':'STEER #4; two booking cgroup OOMs; payment/discovery near limits; event/Keycloak have limited headroom',
        'limits':limits,'scope':'compose-exp deployment copies only; original repo and base compose unchanged'}
for service,(old,new) in limits.items():
 p=app/'compose-exp'/(service+'.yml'); text=p.read_text()
 if len(re.findall('mem_limit: '+re.escape(old),text))!=1: raise SystemExit('Unexpected memory limit: '+service)
 p.write_text(text.replace('mem_limit: '+old,'mem_limit: '+new))
 subprocess.run(['docker','compose','-f',str(p),'-p','flash-ticket-'+service,'up','-d'],env=dict(os.environ,IMAGE=images[service]),check=True)
subprocess.run(['python3',str(root/'setup-collector.py')],check=True)
subprocess.run(['python3',str(root/'pin-images.py'),'app'],check=True)
subprocess.run(['docker','compose','-f',str(app/'collector/compose.json'),'-p','flash-ticket-collector','up','-d','--force-recreate'],check=True)
fixture=json.loads((root/'seed-fixture.json').read_text())
urls=['http://10.0.0.158:8080/realms/flash-ticket/.well-known/openid-configuration',
      'http://127.0.0.1:8761/actuator/health','http://10.0.0.158:8081/api/v1/events',
      'http://10.0.0.158:8081/api/v1/events/'+fixture['event_id']+'/availability']
deadline=time.monotonic()+240; consecutive=0
while time.monotonic()<deadline:
 try:
  for url in urls:
   with urllib.request.urlopen(url,timeout=5) as r:
    r.read()
    if r.status!=200: raise ValueError('not ready')
  consecutive+=1
  if consecutive==3: break
 except Exception: consecutive=0
 time.sleep(3)
else: raise SystemExit('Recovery not confirmed in 240s; inspect redacted logs')
record.update(after=states(),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),consecutive_successful_probes=consecutive)
(root/'jvm-memory-fix.json').write_text(json.dumps(record,indent=2)+'\n')
(root/'jvm-memory-fixed.done').touch()
print(json.dumps(record,indent=2),flush=True)
