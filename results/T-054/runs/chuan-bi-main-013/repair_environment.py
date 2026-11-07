"""Apply the already frozen RCD environment patches and rerun only missing DEV slots."""
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import shlex
import tarfile
from cloud import old, RUN

paths = ('causallearn/utils/PCUtils/SkeletonDiscovery.py', 'causallearn/utils/Fas.py',
         'causallearn/graph/GraphClass.py', 'causallearn/search/ConstraintBased/FCI.py')
patches = {}
for relative in paths:
    upstream = Path('D:/RCA-ext/src/RCAEval/lib') / relative
    installed = Path('D:/RCA-ext/envs/py38-rcdlock/Lib/site-packages') / relative
    data = upstream.read_bytes()
    assert hashlib.sha256(data).hexdigest() == hashlib.sha256(installed.read_bytes()).hexdigest()
    patches[relative] = dict(data=base64.b64encode(data).decode(), sha256=hashlib.sha256(data).hexdigest())
payload = json.dumps(dict(patches=patches, runner=base64.b64encode((RUN / 'remote_dev.py').read_bytes()).decode())).encode()
(RUN / 'environment-patches.json').open('xb').write(payload)


def run(host):
    code = """
from pathlib import Path
import base64,hashlib,json,shutil,sys
r=Path('/home/ubuntu/rca-p7/T-054/checkpoint013')
j=json.load(sys.stdin)
for rel,meta in j['patches'].items():
 p=r/'envs/py38/lib/python3.8/site-packages'/rel
 assert p.resolve().is_relative_to(r.resolve())
 old=p.read_bytes();bak=p.with_name(p.name+'.pre013')
 with bak.open('xb')as f:f.write(old)
 data=base64.b64decode(meta['data']);assert hashlib.sha256(data).hexdigest()==meta['sha256']
 p.write_bytes(data)
shutil.copytree(r/'work/upstream/RCAEval',r/'work/upstream/rcaeval')
p=r/'work/results/T-054/runs/chuan-bi-main-013/remote_dev_r3.py'
with p.open('xb')as f:f.write(base64.b64decode(j['runner']))
print(json.dumps({'PASS':True,'patches':{k:v['sha256']for k,v in j['patches'].items()},'upstream_case_path':'rcaeval'}))
"""
    r, out, err = old.ssh(host, 'python3 -B -c ' + shlex.quote(code), payload=payload)
    old.save_attempt(RUN / (host[0] + '-environment-repair.json'), r, out, err)
    assert r['exit'] == 0
    remote = '/home/ubuntu/rca-p7/T-054/checkpoint013'
    command = ('cd ' + remote + '/work && PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1'
               + ' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ' + remote + '/envs/main/bin/python -B '
               + 'results/T-054/runs/chuan-bi-main-013/remote_dev_r3.py ' + host[0] + ' checkpoint013-results-repair missing')
    r, out, err = old.ssh(host, command, timeout=2000)
    old.save_attempt(RUN / (host[0] + '-pilot-repair.json'), r, out, err)
    output = 'results/T-054/runs/checkpoint013-results-repair'
    r, data, err = old.ssh(host, 'tar -C ' + remote + '/work -czf - ' + output, timeout=240)
    r.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    old.save_attempt(RUN / (host[0] + '-receive-repair.json'), r, b'', err)
    assert r['exit'] == 0
    archive = RUN / (host[0] + '-received-repair.tar.gz')
    archive.open('xb').write(data)
    target = RUN / 'received' / (host[0] + '-repair')
    target.mkdir(parents=True, exist_ok=False)
    with tarfile.open(archive) as tar:
        for m in tar.getmembers():
            p = PurePosixPath(m.name)
            assert p.is_relative_to(output) and '..' not in p.parts
            assert m.isfile() or m.isdir() or (m.islnk() and PurePosixPath(m.linkname).is_relative_to(output) and '..' not in PurePosixPath(m.linkname).parts)
        tar.extractall(target, filter='data')
    print(host[0], 'repair received', len(data), flush=True)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, old.HOSTS))
