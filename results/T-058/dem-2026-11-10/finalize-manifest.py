"""Join raw build records to allowlisted final runtime snapshots."""
import datetime
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
build_file=root/'build-manifest.json'
if not build_file.exists():
    raw=json.loads((root/'manifest-digest.json').read_text(encoding='utf8'))
    if not isinstance(raw,list): raise SystemExit('Original build records must be preserved first')
    build_file.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf8')
build=json.loads(build_file.read_text(encoding='utf8'))
revisions=json.loads((root.parent/'inputs/revisions.json').read_text(encoding='utf8'))['service']
app=json.loads((root/'runtime-app.json').read_text(encoding='utf8'))
obs=json.loads((root/'runtime-obs.json').read_text(encoding='utf8'))
services=[]
for record in build:
    service=record['service']
    if revisions[service]['commit']!=record['commit']: raise SystemExit('Build revision differs from input')
    if app['worktree_heads'].get(service)!=record['commit']: raise SystemExit('Worktree HEAD differs from requested source revision')
    runtime=next(c for c in app['containers'] if c['name']==f'/flash-ticket-{service}-{service}-1')
    if runtime['source_revision']!=record['commit'] or runtime['image_id']!=record['image_id']:
        raise SystemExit('Runtime image does not match the build manifest')
    if runtime['architecture']!='arm64': raise SystemExit('Wrong image architecture')
    services.append(dict(record,runtime=runtime,digest_scope='Local Docker image store; not a registry publication'))
result={'schema_version':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'purpose':'T-058 overnight feasibility, not an efficacy evaluation',
        'source_clone':{'url':'https://github.com/levanminh04/flash-ticket-platform.git',
                        'path':'/opt/flash-ticket-src','root_commit':'220678030517c46a1db815a44779fe1075cc8b46',
                        'service_worktrees':'/opt/flash-ticket-build/<service>'},
        'source_revisions_file_sha256':hashlib.sha256((root.parent/'inputs/revisions.json').read_bytes()).hexdigest(),
        'services':services,'agent':app['agent'],
        'application_infrastructure':[c for c in app['containers'] if not c['requested_image'].startswith('ft-local/')],
        'observability_runtime':obs['containers'],
        'observability_pins':json.loads((root/'image-pins-obs.json').read_text(encoding='utf8')),
        'local_collector_pin':json.loads((root/'image-pins-app.json').read_text(encoding='utf8')),
        'configuration_hashes':{'app':app['files'],'obs':obs['files']},
        'sampling':{'head':'parentbased_always_on','tail_sampling':False,'health_spans_filtered':True},
        'clock_evidence':['environment-app.json#/commands','environment-obs.json#/commands'],
        'source_model':json.loads((root/'flashticket-inventory-source.json').read_text(encoding='utf8')),
        'm1_source_pins':json.loads((root/'m1-source-pins.json').read_text(encoding='utf8')),
        'deviations':['ARM local builds rather than production amd64 images; no production host access',
                      'Frontend omitted','Seven Spring builds skip tests; Keycloak Maven verify runs tests',
                      'All secrets and data initialized fresh; no VNPay or email completion',
                      'C3 shortened from 1h+1h to 30m+30m by STEER #3',
                      'C4 restricted to one pause and one normal window by STEER #3',
                      'No full static model/runtime revision equivalence established'],
        'source_of_authorization':['AGENTS.md','PROMPT.md','out/STEER.md']}
(root/'manifest-digest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Manifest verified:',len(services),'ARM service revisions match build and runtime; agent SHA256',app['agent']['sha256'])
