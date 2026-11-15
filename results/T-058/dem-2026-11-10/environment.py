#!/usr/bin/env python3
import datetime
import json
from pathlib import Path
import subprocess
import sys

def command(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return {'command':args,'exit_code':p.returncode,'output':p.stdout.strip()}

role=sys.argv[1]
result={'role':role,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
result['commands']=[command(c) for c in [
    ['uname','-a'], ['cat','/etc/os-release'], ['nproc'], ['free','-m'], ['df','-h','/'],
    ['docker','version'], ['docker','compose','version'], ['chronyc','tracking'],
    ['sudo','iptables','-S','INPUT'], ['sudo','iptables','-S','DOCKER-USER'],
    ['sudo','ss','-ltnp'], ['docker','ps','--format','{{.Names}} {{.Status}} {{.Ports}}'],
    ['systemctl','is-enabled','docker','chrony','netfilter-persistent']]]
containers=[]
ids=subprocess.check_output(['docker','ps','-aq'],text=True).split()
if ids:
    for c in json.loads(subprocess.check_output(['docker','inspect',*ids])):
        containers.append({'name':c['Name'],'image_id':c['Image'],'image_name':c['Config']['Image'],
                           'state':{k:c['State'].get(k) for k in ['Status','Running','OOMKilled','Restarting','StartedAt','Health']},
                           'restart_count':c['RestartCount'],'memory_limit':c['HostConfig']['Memory'],
                           'ports':c['HostConfig']['PortBindings']})
result['containers']=containers
Path(f'/home/ubuntu/t058/environment-{role}.json').write_text(json.dumps(result,indent=2)+'\n')
print('Saved environment-'+role+'.json without container environment or secrets')
