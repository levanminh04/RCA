"""Chuyển code ghim, chạy cửa sổ và nhận bản ghi từ đúng máy EC2."""
import argparse
import io
import os
import shlex
import subprocess
import sys
import tarfile
from pathlib import Path

from chuan_bi import OUT, ROOT, read, sha

SSH = ['ssh', '-i', 'D:/RCA-ext/keys/key2.pem', '-o', 'HostKeyAlias=3.26.62.217',
       '-o', 'StrictHostKeyChecking=yes', '-o', 'UpdateHostKeys=no', '-o', 'BatchMode=yes',
       '-o', 'ConnectTimeout=7', '-o', 'ServerAliveInterval=30', '-o', 'ServerAliveCountMax=3',
       'ubuntu@3.107.156.186']
REMOTE_ROOT = '/home/ubuntu/rca-t049'
PY = '/home/ubuntu/rca/T-025/envs/main/bin/python'
DEV = ['--re-root', '/home/ubuntu/rca-t048/staging', '--nz-root', '/home/ubuntu/rca/T-032/repo']
RUNNER = 'results/T-049/scripts/chay_cua_so.py'


def ssh(command, **kwargs):
    return subprocess.run(SSH + [command], check=True, **kwargs)


def stage():
    paths = set(read(OUT / 'ma-tran.json')['sources'])
    paths.update((RUNNER, 'results/T-049/scripts/chuan_bi.py', 'results/T-049/ma-tran.json'))
    payload = io.BytesIO()
    with tarfile.open(fileobj=payload, mode='w:gz') as archive:
        for path in sorted(paths):
            archive.add(ROOT / path, arcname=path, recursive=False)
    ssh(f'mkdir -p {REMOTE_ROOT}/results/T-049/runs && tar -xzf - -C {REMOTE_ROOT}',
        input=payload.getvalue(), timeout=120)


def receive(run, target):
    result = ssh(f'cd {REMOTE_ROOT}/results/T-049/runs && tar -czf - -- {shlex.quote(run)}',
                 stdout=subprocess.PIPE, timeout=300)
    folder = OUT / 'runs' / run
    folder.mkdir()
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode='r:gz') as archive:
        for member in archive:
            path = Path(member.name)
            if member.isdir() and path.parts == (run,):
                continue
            if not member.isfile() or len(path.parts) != 2 or path.parts[0] != run or path.name in ('.', '..'):
                raise ValueError(f'Tệp trả về ngoài lượt: {member.name}')
            with (folder / path.name).open('xb') as stream:
                stream.write(archive.extractfile(member).read())
    proof = read(folder / 'kiem.json')
    for name, value in proof['files'].items():
        path = folder / name
        if path.stat().st_size != value['bytes'] or sha(path) != value['sha256']:
            raise ValueError(f'Dữ liệu nhận từ EC2 lệch: {path}')
    print(f'{run}: nhận và kiểm {proof["records"]} bản ghi', file=target, flush=True)


def window(host, job, run, configs, flags=(), *, timeout=7200):
    args = ['-B', RUNNER, str(job), run, *configs, *flags]
    if host == 'laptop':
        env = {**os.environ, 'PYTHONHASHSEED': '0', 'OPENBLAS_NUM_THREADS': '1'}
        subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True, timeout=timeout)
        return
    command = shlex.join(['timeout', '--kill-after=15s', str(timeout), PY, *args, *DEV])
    ssh(f'cd {REMOTE_ROOT} && PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 {command}', timeout=timeout + 60)
    receive(run, sys.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'pilot'))
    args = parser.parse_args()
    if args.action == 'stage':
        stage()
        return
    for i, dataset, configs in ((1, 're2', ['K-thang-C', 'K-thang-VC', 'K-day-du-C', 'K-day-du-VC']),
                                (70, 'nezha', ['K-thang-C', 'T6-C-E3b'])):
        window('ec2', i, f'pilot-ec2-{dataset}-002', configs, ('--pilot',), timeout=650)


if __name__ == '__main__':
    main()
