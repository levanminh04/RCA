#!/usr/bin/env bash
set -Eeuo pipefail
export MAVEN_OPTS='-Xmx768m -Djava.awt.headless=true'
export DOCKER_BUILDKIT=1
root=/home/ubuntu/t058
while [ ! -f "$root/bootstrap.done" ]; do sleep 10; done
sudo mkdir -p /opt/flash-ticket-src /opt/flash-ticket-build /opt/flash-ticket-app/{compose,compose-exp,env,state,secrets/ticket-qr,otel} /opt/flash-ticket-infra
sudo chown -R ubuntu:ubuntu /opt/flash-ticket-src /opt/flash-ticket-build /opt/flash-ticket-app /opt/flash-ticket-infra
if [ ! -d /opt/flash-ticket-src/.git ]; then
 GIT_TERMINAL_PROMPT=0 git -c credential.helper= clone https://github.com/levanminh04/flash-ticket-platform.git /opt/flash-ticket-src
fi
git -C /opt/flash-ticket-src checkout --detach 220678030517c46a1db815a44779fe1075cc8b46
python3 - <<'PY'
import json, subprocess, pathlib, datetime, os
root=pathlib.Path('/home/ubuntu/t058')
spec=json.loads((root/'revisions.json').read_text())['service']
order=['discovery-server','api-gateway','user-service','event-service','ticket-service','booking-service','payment-service','keycloak']
records=[]
for svc in order:
 s=spec[svc]; rev=s['commit']; tree=pathlib.Path('/opt/flash-ticket-build')/svc
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 print(start,svc,'START',flush=True)
 log=root/(svc+'-build.log')
 rec={'service':svc,'commit':rev,'source_path':s['path'],'image':'ft-local/'+svc+':arm64-'+rev[:8], 'started_at':start,'tests':'skipped' if svc!='keycloak' else 'maven clean verify'}
 with log.open('a') as f:
  p=subprocess.run(['git','-C','/opt/flash-ticket-src','worktree','add','--detach',str(tree),rev],stdout=f,stderr=subprocess.STDOUT) if not tree.exists() else subprocess.CompletedProcess([],0)
  if p.returncode==0:
   path=tree/s['path']
   cmd=['mvn','-B','-ntp','clean','verify'] if svc=='keycloak' else ['bash','./mvnw','-B','-ntp','-DskipTests','package']
   p=subprocess.run(cmd,cwd=path,stdout=f,stderr=subprocess.STDOUT)
  rec['maven_exit']=p.returncode
  if p.returncode==0:
   p=subprocess.run(['docker','build','--label','org.opencontainers.image.revision='+rev,'-t',rec['image'],'.'],cwd=path,stdout=f,stderr=subprocess.STDOUT)
   rec['docker_exit']=p.returncode
   if p.returncode==0:
    info=json.loads(subprocess.check_output(['docker','image','inspect',rec['image']]))[0]
    rec.update(image_id=info['Id'],architecture=info['Architecture'],repo_digests=info.get('RepoDigests',[]))
 rec['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 records.append(rec)
 (root/'build-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
 print(rec['finished_at'],svc,'DONE',rec.get('architecture','FAILED'),flush=True)
PY
date -u
docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
touch /home/ubuntu/t058/build.done