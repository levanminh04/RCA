"""Preserve the failed pre-launch attempt and rerun only the missing large-host cover."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shlex
import tarfile
from cloud import old, RUN

host = old.HOSTS[0]
remote = '/home/ubuntu/rca-p7/T-054/checkpoint013'
script = remote + '/work/results/T-054/runs/chuan-bi-main-013/remote_dev_r2.py'
payload = (RUN / 'remote_dev.py').read_bytes()
command = 'python3 -B -c ' + shlex.quote('from pathlib import Path; import sys; p=Path(' + repr(script) + '); p.open("xb").write(sys.stdin.buffer.read())')
r, out, err = old.ssh(host, command, payload=payload)
old.save_attempt(RUN / 'ec2-large-disk-stage-r2.json', r, out, err)
assert r['exit'] == 0
command = ('cd ' + remote + '/work && PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1'
           + ' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ' + remote + '/envs/main/bin/python -B '
           + script + ' ec2-large-disk checkpoint013-results-002')
r, out, err = old.ssh(host, command, timeout=3500)
old.save_attempt(RUN / 'ec2-large-disk-pilot-r2.json', r, out, err)
exit_code = r['exit']
output = 'results/T-054/runs/checkpoint013-results-002'
r, data, err = old.ssh(host, 'tar -C ' + remote + '/work -czf - ' + output, timeout=240)
r.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
old.save_attempt(RUN / 'ec2-large-disk-receive-r2.json', r, b'', err)
assert r['exit'] == 0
archive = RUN / 'ec2-large-disk-received-r2.tar.gz'
archive.open('xb').write(data)
target = RUN / 'received/ec2-large-disk-r2'
target.mkdir(parents=True, exist_ok=False)
with tarfile.open(archive) as tar:
    for member in tar.getmembers():
        path = PurePosixPath(member.name)
        assert path.is_relative_to(output) and '..' not in path.parts and (member.isfile() or member.isdir())
    tar.extractall(target, filter='data')
print('large-host r2 received', len(data), flush=True)
raise SystemExit(exit_code)
