"""Allowlisted deployment metadata only; never serialize full Docker Config.Env."""
import datetime
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

role=sys.argv[1]
result={'role':role,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'containers':[],'files':{}}
ids=subprocess.check_output(['docker','ps','-aq'],text=True).split()
for c in json.loads(subprocess.check_output(['docker','inspect',*ids])):
    image=json.loads(subprocess.check_output(['docker','image','inspect',c['Image']]))[0]
    env=dict(x.split('=',1) for x in c['Config'].get('Env',[]) if '=' in x)
    safe={k:env[k] for k in ['JAVA_TOOL_OPTIONS','OTEL_SERVICE_NAME','OTEL_RESOURCE_ATTRIBUTES',
                            'OTEL_EXPORTER_OTLP_ENDPOINT','OTEL_EXPORTER_OTLP_PROTOCOL',
                            'OTEL_TRACES_SAMPLER','OTEL_LOGS_EXPORTER','OTEL_METRIC_EXPORT_INTERVAL',
                            'KC_HOSTNAME','KEYCLOAK_ISSUER_URI','SERVER_ADDRESS'] if k in env}
    result['containers'].append({'name':c['Name'],'id':c['Id'],'requested_image':c['Config']['Image'],
                                 'image_id':c['Image'],'repo_digests':image.get('RepoDigests',[]),
                                 'architecture':image['Architecture'],
                                 'source_revision':(image['Config'].get('Labels') or {}).get('org.opencontainers.image.revision'),
                                 'created':c['Created'],'started_at':c['State']['StartedAt'],
                                 'running':c['State']['Running'],'paused':c['State']['Paused'],
                                 'oom_killed':c['State']['OOMKilled'],'restart_count':c['RestartCount'],
                                 'network_mode':c['HostConfig']['NetworkMode'],'ports':c['HostConfig']['PortBindings'],
                                 'safe_settings':safe})
if role=='app':
    specs=json.loads(Path('/home/ubuntu/t058/revisions.json').read_text())['service']
    result['worktree_heads']={name:subprocess.check_output(['git','-C','/opt/flash-ticket-build/'+name,'rev-parse','HEAD'],text=True).strip() for name in specs if name!='frontend'}
    jar=Path('/opt/flash-ticket-app/otel/opentelemetry-javaagent.jar')
    result['agent']={'version':'2.33.1','sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'path':str(jar)}
    result['private_file_modes']={str(p):oct(stat.S_IMODE(p.stat().st_mode)) for p in Path('/opt/flash-ticket-app/env').glob('*.env')}
    result['private_file_modes']['/opt/flash-ticket-src/.env']=oct(stat.S_IMODE(Path('/opt/flash-ticket-src/.env').stat().st_mode))
    files=list(Path('/opt/flash-ticket-app/compose-exp').glob('*.yml'))+[Path('/opt/flash-ticket-app/collector/config.json'),Path('/opt/flash-ticket-app/collector/compose.json')]
else:
    files=list(Path('/opt/flash-ticket-obs/pinned').glob('*.json'))
for p in files:
    result['files'][str(p)]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out=Path('/home/ubuntu/t058')/('runtime-'+role+'.json')
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
out.chmod(0o644)
print('Saved allowlisted runtime metadata:',out)
