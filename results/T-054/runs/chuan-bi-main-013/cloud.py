"""Bounded SSH stages on the two approved instances; preserve all receipts."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import hashlib
from pathlib import Path
import shlex
import tarfile
from pathlib import PurePosixPath
import sys

RUN = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('cloud012', RUN.parent / 'danh-gia-ec2-moi-012/cloud.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def bootstrap(host):
    result, out, err = old.ssh(host, 'python3 -B -', payload=(RUN / 'bootstrap.py').read_bytes(), timeout=1500)
    result.update(stdout=out.decode(errors='replace'), stderr=err.decode(errors='replace'))
    with (RUN / (host[0] + '-bootstrap.json')).open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(host[0], 'bootstrap', result['exit'], round(result['seconds'], 2), flush=True)
    if result['exit']:
        print(result['stdout'][-3000:], result['stderr'][-1500:], flush=True)
    return result['exit']


def pilot(host):
    name = host[0]
    remote = '/home/ubuntu/rca-p7/T-054/checkpoint013'
    archive = RUN / 'dev-package.tar.gz'
    package = json.loads((RUN / 'dev-package.json').read_bytes())
    data = archive.read_bytes()
    assert hashlib.sha256(data).hexdigest() == package['archive']['sha256']
    code = """
import hashlib,json,sys,tarfile
from pathlib import Path,PurePosixPath
root=Path('/home/ubuntu/rca-p7/T-054/checkpoint013')
archive=root/'dev-package.tar.gz'
with archive.open('xb')as f:f.write(sys.stdin.buffer.read())
assert hashlib.sha256(archive.read_bytes()).hexdigest()==EXPECTED
work=root/'work';work.mkdir(exist_ok=False)
with tarfile.open(archive)as tar:
 for m in tar.getmembers():
  p=PurePosixPath(m.name)
  assert m.isfile()and not p.is_absolute()and '..'not in p.parts
 tar.extractall(work,filter='data')
pins=json.loads((work/'files.json').read_bytes())
for name,pin in pins.items():
 b=(work/name).read_bytes()
 assert len(b)==pin['bytes']and hashlib.sha256(b).hexdigest()==pin['sha256'],name
print(json.dumps({'verified':len(pins),'instance_id':Path('/var/lib/cloud/data/instance-id').read_text().strip()}))
""".replace('EXPECTED', repr(package['archive']['sha256']))
    result, out, err = old.ssh(host, 'python3 -B -c ' + shlex.quote(code), payload=data, timeout=240)
    old.save_attempt(RUN / (name + '-stage.json'), result, out, err)
    if result['exit']:
        return result['exit']
    command = ('cd ' + remote + '/work && PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0'
               + ' OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 '
               + remote + '/envs/main/bin/python -B results/T-054/runs/chuan-bi-main-013/remote_dev.py ' + name)
    result, out, err = old.ssh(host, command, timeout=3600)
    old.save_attempt(RUN / (name + '-pilot.json'), result, out, err)
    pilot_exit = result['exit']
    output = 'results/T-054/runs/checkpoint013-results'
    result, data, err = old.ssh(host, 'tar -C ' + remote + '/work -czf - ' + output, timeout=240)
    result.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    old.save_attempt(RUN / (name + '-receive.json'), result, b'', err)
    if result['exit']:
        return result['exit']
    archive = RUN / (name + '-received.tar.gz')
    with archive.open('xb') as stream:
        stream.write(data)
    target = RUN / 'received' / name
    target.mkdir(parents=True, exist_ok=False)
    with tarfile.open(archive) as tar:
        for item in tar.getmembers():
            p = PurePosixPath(item.name)
            assert p.is_relative_to(output) and '..' not in p.parts and (item.isfile() or item.isdir())
        tar.extractall(target, filter='data')
    print(name, 'received', len(data), flush=True)
    return pilot_exit


if __name__ == '__main__':
    assert sys.argv[1:] in (['bootstrap'], ['pilot'])
    action = bootstrap if sys.argv[1] == 'bootstrap' else pilot
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(action, old.HOSTS))
    raise SystemExit(0 if results == [0, 0] else 1)
