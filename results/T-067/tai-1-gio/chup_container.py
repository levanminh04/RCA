import json,subprocess,datetime
ids=subprocess.run(['docker','ps','-aq'],capture_output=True,text=True).stdout.split()
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'container':[]}
for d in json.loads(subprocess.run(['docker','inspect']+ids,capture_output=True,text=True).stdout):
    out['container'].append({'name':d['Name'].lstrip('/'),'image':d['Config']['Image'],'status':d['State']['Status'],
        'restarts':d['RestartCount'],'oom_killed':d['State']['OOMKilled'],'started_at':d['State']['StartedAt'],'mem_limit':d['HostConfig']['Memory']})
out['container'].sort(key=lambda x:x['name'])
print(json.dumps(out,indent=1))
