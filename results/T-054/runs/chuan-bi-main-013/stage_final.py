"""Stage only final code/opaque metadata, then exercise changed fixtures on each EC2."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

from activate import ROOT, RUN, pin
from bien_nhan import atomic, read_pin, ref
from main import HOSTS, REMOTE, remote_json, ssh_args, transfer, verify_cloud_environment, verify_host
from finish_cloud import extract


def run(host):
    packet = read_pin(pin(RUN / 'main-packet.json'))['files']
    files = {rel: (ROOT / meta.get('source_path', rel), meta) for rel, meta in packet.items()}
    files[(RUN/'main-packet.json').relative_to(ROOT).as_posix()] = (RUN/'main-packet.json', ref(RUN/'main-packet.json'))
    expected = {rel: meta['sha256'] for rel, (path, meta) in files.items()}
    # Retain old DEV code byte-for-byte before replacing exactly the reviewed packet paths.
    code = """
from pathlib import Path
import hashlib,json,os
root=Path(BASE).resolve();work=root/'work';backup=root/'before-final-stage';moved=[]
for rel,sha in EXPECTED.items():
 p=work/rel;q=backup/rel
 assert p.resolve().is_relative_to(root) and q.resolve().is_relative_to(root)
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
  assert not q.exists(),str(q)
  q.parent.mkdir(parents=True,exist_ok=True);p.rename(q);moved.append(rel)
print(json.dumps({'preserved_changed_paths':moved}))
""".replace('BASE', repr(REMOTE)).replace('EXPECTED', repr(expected))
    before = remote_json(host, code)
    atomic(RUN / (host+'-final-stage-before.json'), before)
    staged = transfer(host, files, REMOTE+'/work', host+'-preparation-code-metadata.json')
    environment = verify_cloud_environment(host)
    conditions = read_pin(pin(RUN/'launch-conditions.json'))['hosts'][host]
    resources = verify_host(host, conditions)
    atomic(RUN / (host+'-final-environment.json'), dict(PASS=True, staging=staged, environment=environment,
          resources=resources, conditions=conditions, data_test_transferred=False))
    output = 'results/T-054/runs/checkpoint013-fixture-current'
    command = ('cd '+REMOTE+'/work && PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 '
               'OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 '+REMOTE+'/envs/main/bin/python -B '
               'results/T-054/scripts/fixtures.py '+output)
    done = subprocess.run(ssh_args(host,command), capture_output=True, timeout=400)
    atomic(RUN/(host+'-fixture-current.json'), dict(exit=done.returncode,stdout=done.stdout.decode(errors='replace'),
           stderr=done.stderr.decode(errors='replace'),command=command))
    received = subprocess.run(ssh_args(host,'tar -C '+REMOTE+'/work -czf - '+output),capture_output=True,timeout=180)
    if received.returncode:
        raise RuntimeError(received.stderr.decode(errors='replace'))
    archive = RUN/(host+'-fixture-current.tar.gz')
    archive.open('xb').write(received.stdout)
    extract(archive,RUN/'received'/(host+'-fixture-current'),output)
    summary = RUN/'received'/(host+'-fixture-current')/output/'summary.json'
    value = json.loads(summary.read_bytes())
    atomic(RUN/(host+'-fixture-current-received.json'),dict(exit=done.returncode,archive=ref(archive),summary=ref(summary),
           checks=len(value['checks']),PASS=done.returncode==0))
    print(host,'current fixtures',done.returncode,len(value['checks']),flush=True)
    assert done.returncode==0


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run,HOSTS))
