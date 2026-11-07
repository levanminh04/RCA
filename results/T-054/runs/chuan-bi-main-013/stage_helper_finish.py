"""Re-pin final helper metadata only; the five wrappers and their 101 fixtures are unchanged."""
from concurrent.futures import ThreadPoolExecutor
from activate import ROOT,RUN,pin
from bien_nhan import atomic,read_pin,ref
from main import HOSTS,REMOTE,remote_json,transfer,verify_cloud_environment,verify_local_environment


def run(host):
    files={rel:(ROOT/meta.get('source_path',rel),meta)for rel,meta in read_pin(pin(RUN/'main-packet.json'))['files'].items()}
    files[(RUN/'main-packet.json').relative_to(ROOT).as_posix()]=(RUN/'main-packet.json',ref(RUN/'main-packet.json'))
    expected={rel:meta['sha256']for rel,(p,meta)in files.items()}
    code="""
from pathlib import Path
import hashlib,json
r=Path(BASE).resolve();moved=[]
for rel,sha in EXPECTED.items():
 p=r/'work'/rel;q=r/'before-local-upstream-check'/rel
 assert p.resolve().is_relative_to(r) and q.resolve().is_relative_to(r)
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
  assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True);p.rename(q);moved.append(rel)
print(json.dumps({'preserved_changed_paths':moved}))
""".replace('BASE',repr(REMOTE)).replace('EXPECTED',repr(expected))
    before=remote_json(host,code)
    staged=transfer(host,files,REMOTE+'/work',host+'-final-helper-code-metadata.json')
    environment=verify_cloud_environment(host)
    atomic(RUN/(host+'-final-execution-environment.json'),dict(PASS=True,before=before,staging=staged,environment=environment,
           source_test_transferred=False,wrappers_unchanged_since_101_fixture=True))
    print(host,'final helper environment PASS',flush=True)


if __name__=='__main__':
    local=verify_local_environment()
    atomic(RUN/'local-final-code-environment.json',local)
    with ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(run,HOSTS))
