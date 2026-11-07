"""Tiếp nhận phần đóng từ EC2, kiểm byte/hash từng file trước dùng."""
import json
import pathlib
import shlex
import subprocess
import tarfile
import time
from common import ROOT, RUN, digest, read, save, timing
from stage_ec2 import SSH


def main():
    start = time.perf_counter()
    for name in ('ec2-pilot-001', 'ec2-pilot-002'):
        remote = '/home/ubuntu/rca-t053/results/T-052/' + name
        target = RUN / name
        probe = ("import pathlib,json,hashlib; r=pathlib.Path(" + repr(remote) + "); "
                 "ps=[p for d in [r/'output'] if d.exists() for p in d.rglob('*') if p.is_file()]+"
                 "[r/n for n in ['stdout.log','stderr.log','pid.json'] if (r/n).is_file()]; "
                 "print(json.dumps({p.relative_to(r).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in ps}))")
        expected = json.loads(subprocess.check_output(SSH + [shlex.join(['python3','-c',probe])],timeout=20))
        save(target / 'remote-receipt.json', expected)
        archive = target / 'received.tar.gz'
        names = ' '.join(shlex.quote(p) for p in expected)
        with archive.open('xb') as file:
            subprocess.run(SSH + [f'cd {shlex.quote(remote)} && tar -czf - {names}'],stdout=file,check=True,timeout=120)
        dest = target / 'received'
        dest.mkdir()
        with tarfile.open(archive, 'r:gz') as tar:
            for item in tar.getmembers():
                p = pathlib.PurePosixPath(item.name)
                assert not p.is_absolute() and '..' not in p.parts and item.isfile()
            tar.extractall(dest, filter='data')
        for name2, meta in expected.items():
            p = dest / name2
            assert p.stat().st_size == meta['bytes'] and digest(p) == meta['sha256'], name2
        save(target / 'receive-summary.json', timing('receive_ec2', start,PASS=True,files=len(expected),
                   remote=remote,archive_sha256=digest(archive)))
    summary = read(RUN / 'ec2-pilot-002/received/output/summary.json')
    assert summary['PASS'] and summary['native_comparisons'] == 15
    print('EC2 pilot PASS: 15 comparisons; all received bytes/hash verified',flush=True)


if __name__ == '__main__': main()
