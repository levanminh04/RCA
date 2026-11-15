import json
from pathlib import Path
import subprocess

def read(path):
    return dict(x.split('=',1) for x in Path(path).read_text().splitlines() if x and not x.startswith('#'))
root=read('/opt/flash-ticket-infra/.env')
containers=json.loads(subprocess.check_output(['docker','inspect','flash-ticket-infra-postgres-1']))
pg=dict(x.split('=',1) for x in containers[0]['Config']['Env'])
for svc in ['event','booking','payment','ticket']:
    name=svc.upper()
    env=read('/opt/flash-ticket-app/env/'+svc+'-service.env')
    print(svc,'env matches infra:',env[name+'_DB_PASSWORD']==root[name+'_DB_ADMIN_PASSWORD'],
          'container matches infra:',pg[name+'_DB_ADMIN_PASSWORD']==root[name+'_DB_ADMIN_PASSWORD'])
    password=env[name+'_DB_PASSWORD']
    sh='export PGPASSWORD='+password+'\npsql -h 127.0.0.1 -U '+svc+'_admin -d '+svc+'_db -Atc "select current_user"\n'
    p=subprocess.run(['docker','exec','-i','flash-ticket-infra-postgres-1','sh'],input=sh,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(svc,'TCP authentication exit:',p.returncode,'diagnostic:',p.stderr.replace(password,'<redacted>').strip())
