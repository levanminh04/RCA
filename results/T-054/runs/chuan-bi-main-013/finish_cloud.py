"""Add the missing fixture metadata and run fixtures only; do not repeat DEV methods."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path, PurePosixPath
import shlex
import tarfile
from cloud import old, RUN

ROOT = RUN.parents[3]
rel = 'results/T-052/giao-thuc-p7-a-003.json'
payload = (ROOT / rel).read_bytes()
manifest = json.loads((ROOT / 'results/T-052/manifest-dinh-chinh-g3-004.json').read_bytes())['outputs']
assert hashlib.sha256(payload).hexdigest() == manifest[rel]['sha256']


def extract(archive, target, prefix):
    target.mkdir(parents=True, exist_ok=False)
    with tarfile.open(archive) as tar:
        for m in tar.getmembers():
            path = PurePosixPath(m.name)
            assert path.is_relative_to(prefix) and '..' not in path.parts
            assert m.isfile() or m.isdir() or (m.islnk() and PurePosixPath(m.linkname).is_relative_to(prefix)
                                               and '..' not in PurePosixPath(m.linkname).parts)
        tar.extractall(target, filter='data')


def run(host):
    remote = '/home/ubuntu/rca-p7/T-054/checkpoint013'
    path = remote + '/work/' + rel
    code = 'from pathlib import Path;import sys;p=Path(' + repr(path) + ');p.open("xb").write(sys.stdin.buffer.read())'
    r, out, err = old.ssh(host, 'python3 -B -c ' + shlex.quote(code), payload=payload)
    old.save_attempt(RUN / (host[0] + '-fixture-metadata.json'), r, out, err)
    assert r['exit'] == 0
    output = 'results/T-054/runs/checkpoint013-fixture-final'
    command = ('cd ' + remote + '/work && PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1'
               + ' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ' + remote + '/envs/main/bin/python -B '
               + 'results/T-054/scripts/fixtures.py ' + output)
    r, out, err = old.ssh(host, command, timeout=400)
    old.save_attempt(RUN / (host[0] + '-fixture-final.json'), r, out, err)
    r, data, err = old.ssh(host, 'tar -C ' + remote + '/work -czf - ' + output, timeout=180)
    r.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    old.save_attempt(RUN / (host[0] + '-fixture-receive.json'), r, b'', err)
    assert r['exit'] == 0
    archive = RUN / (host[0] + '-fixture-final.tar.gz')
    archive.open('xb').write(data)
    extract(archive, RUN / 'received' / (host[0] + '-fixture-final'), output)
    print(host[0], 'final fixture received', len(data), flush=True)


if __name__ == '__main__':
    archive = RUN / 'ec2-small-disk-received.tar.gz'
    receipt = json.loads((RUN / 'ec2-small-disk-receive.json').read_bytes())
    assert archive.stat().st_size == receipt['bytes'] and hashlib.sha256(archive.read_bytes()).hexdigest() == receipt['sha256']
    extract(archive, RUN / 'received/ec2-small-disk-initial', 'results/T-054/runs/checkpoint013-results')
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, old.HOSTS))
