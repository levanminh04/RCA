import datetime
import json
from pathlib import Path
import subprocess
import sys

role=sys.argv[1]
path=Path('/opt/flash-ticket-app/collector/compose.json' if role=='app' else '/opt/flash-ticket-obs/pinned/compose.json')
compose=json.loads(path.read_text())
pins=[]
for svc,config in compose['services'].items():
    image=config['image']
    item=json.loads(subprocess.check_output(['docker','image','inspect',image]))[0]
    digest=item['RepoDigests'][0]
    config['image']=digest
    pins.append({'service':svc,'requested_image':image,'pinned_image':digest,'image_id':item['Id'],'architecture':item['Architecture']})
path.write_text(json.dumps(compose,indent=2)+'\n')
Path('/home/ubuntu/t058/image-pins-'+role+'.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'images':pins},indent=2)+'\n')
print('Pinned',len(pins),'images by registry digest on',role)
