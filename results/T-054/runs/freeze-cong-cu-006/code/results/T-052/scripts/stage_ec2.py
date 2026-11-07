"""Đóng gói chỉ code, metadata và đầu ra dev đã ghim cho pilot cùng máy."""
import gzip
import pathlib
import shutil
import shlex
import subprocess
import tarfile
import time

from common import ROOT, RUN, digest, dump, metadata, native_index, native_rows, pin, read, save, timing

SSH = ['ssh', '-i', 'D:/RCA-ext/keys/key2.pem', '-o', 'HostKeyAlias=3.26.62.217',
       '-o', 'StrictHostKeyChecking=yes', '-o', 'UpdateHostKeys=no', '-o', 'BatchMode=yes',
       '-o', 'ConnectTimeout=8', '-o', 'ServerAliveInterval=30', '-o', 'ServerAliveCountMax=3',
       'ubuntu@3.107.156.186']
REMOTE = '/home/ubuntu/rca-t053/results/T-052/ec2-pilot-002'


def main():
    start = time.perf_counter()
    target = RUN / 'ec2-pilot-002'
    stage = target / 'stage'
    stage.mkdir(parents=True)
    entries, base, lineage = metadata()
    m, index = native_index()
    files = [p.relative_to(ROOT).as_posix() for package in ('m1', 'm1_danh_gia', 'p3')
             for p in (ROOT / 'src' / package).rglob('*.py') if '__pycache__' not in p.parts]
    files += ['results/T-048/scripts/chay.py', 'results/T-048/scripts/kiem.py', 'results/T-048/scripts/cham.py',
              'results/T-045/scripts/chay_pha1.py', 'results/T-043/hop-dong.json',
              'results/T-022/allowlist-dev.json', 'results/T-022/mappings/universe-re2tt-dev.json',
              'results/T-026/allowlist-dev.json']
    for path in files:
        dest = stage / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, dest)
    shutil.copyfile(ROOT / 'results/T-052/scripts/pilot_ec2.py', stage / 'pilot_ec2.py')
    jobs = []
    configs = {'M1': 'K-E1+E2+E5', 'C-a0': 'K-R0', 'C-a1': 'K-E1'}
    for n in (0, 1, 53, 62, 79):
        j = entries[n]['job']
        item, command = index[j['opaque_id'], j['window']]
        assert 'k-ec2' in item['path']  # Cùng máy với nguồn, không nới so số thực.
        records = native_rows(item, m, set(configs.values()))
        side = native_rows({'path': item['trace'], 'sha256': item['trace_sha256']}, m, set(configs.values()))
        input_hashes = {s['trace']['normalized_input_sha256'] for s in side.values()}
        assert len(input_hashes) == 1
        filename = f'expected-{n:02d}.json'
        save(stage / filename, {'records': records, 'normalized_input_sha256': input_hashes.pop(),
             'samples': {cid: {u: d['mau_sha256'] for u, d in s['trace']['phan_vi'].items()} for cid, s in side.items()},
             'source': item, 'source_fields_verified': True})
        jobs.append({'index': n, 'job': j, 'expected': filename,
                     'configurations': {cid: command['configs'][cid] for cid in configs.values()}})
    hashes = {p.relative_to(stage).as_posix(): digest(p) for p in stage.rglob('*') if p.is_file()}
    save(stage / 'plan.json', {'jobs': jobs, 'configs': configs, 'stage_files': hashes, 'lineage': lineage,
                             'native_timeout_seconds': 2400, 'cd3': 'not scheduled in this parity pilot'})
    archive = target / 'stage.tar.gz'
    with tarfile.open(archive, 'w:gz') as tar:
        for p in sorted(stage.rglob('*')):
            if p.is_file(): tar.add(p, arcname='stage/' + p.relative_to(stage).as_posix())
    with archive.open('rb') as stream:
        subprocess.run(SSH + [f'mkdir -p {REMOTE.rsplit("/", 1)[0]} && mkdir {REMOTE} && tar -xzf - -C {REMOTE}'],
                       stdin=stream, check=True, timeout=120)
    launch = ("import subprocess,pathlib,json; r=pathlib.Path(" + repr(REMOTE) + "); "
              "p=subprocess.Popen(['timeout','2400s','/home/ubuntu/rca/T-025/envs/main/bin/python','-B','stage/pilot_ec2.py'],"
              "cwd=r,stdin=subprocess.DEVNULL,stdout=(r/'stdout.log').open('wb'),stderr=(r/'stderr.log').open('wb'),"
              "start_new_session=True,close_fds=True); (r/'pid.json').write_text(json.dumps({'pid':p.pid})); print(p.pid)")
    command = shlex.join(['python3', '-c', launch])
    launched = subprocess.run(SSH + [command], check=True, capture_output=True, text=True, timeout=20)
    save(target / 'launch.json', timing('stage_ec2', start, remote=REMOTE, ip='3.107.156.186',
         stage_archive_sha256=digest(archive), archive_bytes=archive.stat().st_size,
         source_files=len(hashes), remote_command=command, pid=int(launched.stdout.strip()), returncode=launched.returncode,
         labels_in_bundle=False, raw_data_transferred=False))
    print(dump({'staged': archive.stat().st_size, 'remote': REMOTE}), flush=True)


if __name__ == '__main__':
    main()
