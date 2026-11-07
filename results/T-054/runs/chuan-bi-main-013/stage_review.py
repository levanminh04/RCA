"""Stage metadata revision only; retain prior cloud bytes and reuse unchanged code/DEV evidence."""
from concurrent.futures import ThreadPoolExecutor
from activate import ROOT,RUN,pin
from bien_nhan import atomic,read_pin,ref
from main import HOSTS,REMOTE,remote_json,transfer,verify_cloud_environment,verify_host


def run(host):
    files={rel:(ROOT/meta.get('source_path',rel),meta)for rel,meta in read_pin(pin(RUN/'main-packet.json'))['files'].items()}
    files[(RUN/'main-packet.json').relative_to(ROOT).as_posix()]=(RUN/'main-packet.json',ref(RUN/'main-packet.json'))
    expected={rel:meta['sha256']for rel,(p,meta)in files.items()}
    code="""
from pathlib import Path
import hashlib,json
root=Path(BASE).resolve();moved=[]
for rel,sha in EXPECTED.items():
 p=root/'work'/rel;q=root/'before-review-fix-001'/rel
 assert p.resolve().is_relative_to(root) and q.resolve().is_relative_to(root)
 if p.exists()and hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
  assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True);p.rename(q);moved.append(rel)
print(json.dumps({'preserved_changed_paths':moved}))
""".replace('BASE',repr(REMOTE)).replace('EXPECTED',repr(expected))
    before=remote_json(host,code)
    stage=transfer(host,files,REMOTE+'/work',host+'-after-review-metadata.json')
    env=verify_cloud_environment(host)
    resources=verify_host(host,read_pin(pin(RUN/'launch-conditions.json'))['hosts'][host])
    atomic(RUN/(host+'-after-review-environment.json'),dict(PASS=True,before=before,staging=stage,environment=env,
           resources=resources,test_data_transferred=False,new_method_runs=0))
    print(host,'after-review metadata and environment PASS',flush=True)


if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(run,HOSTS))
