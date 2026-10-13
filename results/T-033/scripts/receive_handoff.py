"""Nhận trực tiếp archive vào file đích, kiểm SHA; không tính nghiên cứu."""
import hashlib
import json
import subprocess
import tarfile
import time
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[3]
home = root / 'results/T-033'
run = home / 'runs/checkpoint-handoff-001'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(2**20), b''):
            digest.update(block)
    return digest.hexdigest()


for name in ['snapshot.json', 'artifact-inventory.json']:
    assert sha(run / name) == (run / (name + '.sha256')).read_text().split()[0]
snapshot = json.loads((run / 'snapshot.json').read_text(encoding='utf-8'))
inventory = json.loads((run / 'artifact-inventory.json').read_text(encoding='utf-8'))
used_local = sum(p.stat().st_size for p in home.rglob('*') if p.is_file())
# Conservative combined footprint; stream avoids retaining a second local tar.
projected_combined = snapshot['resources']['new_bytes_including_archive'] + used_local + snapshot['payload_bytes'] + 8 * 2**20
assert projected_combined < 4 * 2**30, ('Combined checkpoint footprint would exceed 4 GiB', projected_combined)
out = run / 'artifacts'
out.mkdir(exist_ok=False)
command = ['ssh', '-i', 'D:/RCA-ext/keys/keys.pem', '-o',
           'UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts',
           '-o', 'StrictHostKeyChecking=yes', '-o', 'BatchMode=yes',
           'ubuntu@3.107.246.249',
           'cat /home/ubuntu/rca/T-033/runs/checkpoint-handoff-001/artifacts.tar']
begin = time.perf_counter()
verified = {}
state = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
         'command': command, 'files': 0, 'payload_bytes_received': 0,
         'projected_combined_bytes_with_reserve': projected_combined}


def progress():
    state.update(files=len(verified), wall_s=time.perf_counter() - begin)
    (run / 'receive-status.json').write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: state[k] for k in ['status', 'files', 'payload_bytes_received', 'wall_s']}), flush=True)


class HashedStream:
    def __init__(self, stream):
        self.stream = stream
        self.digest = hashlib.sha256()
        self.bytes = 0

    def read(self, size=-1):
        block = self.stream.read(size)
        self.digest.update(block)
        self.bytes += len(block)
        return block


progress()
try:
    with (run / 'receive-stderr.txt').open('xb') as stderr:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=stderr)
        stream = HashedStream(proc.stdout)
        last_report = begin
        with tarfile.open(fileobj=stream, mode='r|') as archive:
            for member in archive:
                assert member.isfile() and member.name in inventory, member.name
                destination = (out / member.name).resolve()
                assert out.resolve() in destination.parents
                assert 'T-032' not in destination.parts and not destination.exists()
                info = inventory[member.name]
                assert member.size == info['bytes']
                destination.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                total = 0
                with archive.extractfile(member) as source, destination.open('xb') as target:
                    for block in iter(lambda: source.read(2**20), b''):
                        target.write(block)
                        digest.update(block)
                        total += len(block)
                        state['payload_bytes_received'] += len(block)
                        if time.perf_counter() - last_report >= 5:
                            progress()
                            last_report = time.perf_counter()
                assert total == info['bytes'] and digest.hexdigest() == info['sha256'], member.name
                verified[member.name] = info
        # Include tar padding/trailer in the whole-archive hash.
        while stream.read(2**20):
            pass
        assert proc.wait() == 0
        assert stream.bytes == snapshot['archive']['bytes']
        assert stream.digest.hexdigest() == snapshot['archive']['sha256']
        assert set(verified) == set(inventory)
        state.update(status='PASS', archive_bytes_received=stream.bytes,
                     archive_sha256=stream.digest.hexdigest(),
                     ended_utc=datetime.now(timezone.utc).isoformat())
except BaseException as exc:
    state.update(status='STOPPED', error=repr(exc))
    if 'proc' in globals() and proc.poll() is None:
        proc.terminate()
        proc.wait()
    raise
finally:
    (run / 'received-files.json').write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding='utf-8')
    progress()
