"""Deployment-only correction after the failed C3 window is preserved."""
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request

root=Path('/home/ubuntu/t058'); app=Path('/opt/flash-ticket-app')
if not (root/'resources-30m-app.done').exists(): raise SystemExit('C3 must finish before any change')
marker=root/'booking-memory-fixed.done'
if marker.exists(): raise SystemExit('Memory correction already completed')
name='flash-ticket-booking-service-booking-service-1'
def state():
    c=json.loads(subprocess.check_output(['docker','inspect',name]))[0]
    return {'id':c['Id'],'memory_limit':c['HostConfig']['Memory'],'restarts':c['RestartCount'],
            'started_at':c['State']['StartedAt'],'running':c['State']['Running'],'oom_killed':c['State']['OOMKilled']}
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':state(),
        'reason':'Two kernel-confirmed 512 MiB cgroup OOMs during C3; host RAM remained available',
        'scope':'Only deployment compose-exp; source repository and base compose unchanged'}
path=app/'compose-exp/booking-service.yml'
text=path.read_text()
if len(re.findall(r'mem_limit: 512m',text))!=1: raise SystemExit('Unexpected original memory limit')
path.write_text(text.replace('mem_limit: 512m','mem_limit: 1g'))
images=json.loads((root/'build-manifest.json').read_text())
image=next(x['image'] for x in images if x['service']=='booking-service')
subprocess.run(['docker','compose','-f',str(path),'-p','flash-ticket-booking-service','up','-d'],env=dict(os.environ,IMAGE=image),check=True)
subprocess.run(['python3',str(root/'setup-collector.py')],check=True)
subprocess.run(['python3',str(root/'pin-images.py'),'app'],check=True)
subprocess.run(['docker','compose','-f',str(app/'collector/compose.json'),'-p','flash-ticket-collector','up','-d','--force-recreate'],check=True)
fixture=json.loads((root/'seed-fixture.json').read_text())
url='http://10.0.0.158:8081/api/v1/events/'+fixture['event_id']+'/availability'
deadline=time.monotonic()+180
while time.monotonic()<deadline:
    try:
        with urllib.request.urlopen(url,timeout=5) as response:
            response.read(); code=response.status
        if code==200: break
    except Exception:
        pass
    time.sleep(3)
else: raise SystemExit('Gateway availability did not recover within 180 seconds')
record.update(after=state(),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),availability_http_status=code)
if record['after']['memory_limit']!=1024**3: raise SystemExit('New limit not applied')
(root/'booking-memory-fix.json').write_text(json.dumps(record,indent=2)+'\n')
marker.touch()
print(json.dumps(record,indent=2),flush=True)
