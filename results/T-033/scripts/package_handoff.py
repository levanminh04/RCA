"""Đóng băng đầu ra hiện có của T-033; không chạy detector/diễn giải dữ liệu."""
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path
import psutil

H = Path(os.environ['T033_HOME']).resolve()
assert H == Path('/home/ubuntu/rca/T-033') and os.name == 'posix'
R = H / 'runs/checkpoint-handoff-001'
R.mkdir(exist_ok=False)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(2**20), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def relative(path):
    path = path.resolve()
    assert H in path.parents and 'T-032' not in path.parts
    return path.relative_to(H).as_posix()


statuses = {}
for path in sorted((H / 'runs').glob('*/status.json')):
    doc = read(path)
    assert doc.get('status') not in ('RUNNING', 'PREPARING'), str(path)
    pid = doc.get('pid')
    if pid and psutil.pid_exists(pid):
        assert str(H) not in ' '.join(psutil.Process(pid).cmdline()), ('Worker still active', pid)
    statuses[path.parent.name] = doc
assert statuses['bocpd-factorial-rest-001']['status'] == 'PASS'
assert len(statuses['bocpd-factorial-rest-001']['cases']) == 30
assert all(case['status'] == 'PASS' for case in statuses['bocpd-factorial-rest-001']['cases'].values())
fixed = [entry for name in ['nsigma-frozen-first-001', 'nsigma-frozen-rest-001']
         for case in statuses[name]['cases'].values() for entry in case.values()]
assert len(fixed) == 60 and all(e['status'] == 'PASS' and all(e['checks'].values()) for e in fixed)
assert read(H / 'runs/core-audit-002/verification.json')['core_records'] == 120
verified = {}
manifest_paths = list((H / 'runs').glob('*/manifest.json')) + list((H / 'runs').glob('*/logs-manifest.json'))
for path in sorted(manifest_paths):
    manifest = read(path)
    assert isinstance(manifest, dict) and manifest
    for name, info in manifest.items():
        target = path.parent / name
        relative(target)
        assert isinstance(info, dict) and set(['sha256', 'bytes']) <= set(info), str(path)
        assert target.is_file() and target.stat().st_size == info['bytes'], str(target)
        assert sha(target) == info['sha256'], str(target)
    verified[relative(path)] = {'sha256': sha(path), 'files': len(manifest)}

# provenance ca pilot được tái dùng: không giả định NPZ nằm ở run rest.
reuse = []
for oid, case in statuses['bocpd-factorial-rest-001']['cases'].items():
    for branch, entry in case['branches'].items():
        assert entry['status'] == 'PASS' and all(entry['checks'].values())
        if entry.get('reused_record'):
            original = H / entry['reused_record']
            record = read(original)
            assert record['sha256'] == entry['sha256']
            assert sha(original.parent / record['npz']) == record['sha256']
            reuse.append({'opaque_id': oid, 'branch': branch, 'record': relative(original),
                          'npz': relative(original.parent / record['npz'])})
assert len(reuse) == 2

files = sorted(p for p in H.rglob('*') if p.is_file() and R not in p.parents)
assert all(not p.is_symlink() for p in files)
inventory = {relative(p): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in files}
payload_bytes = sum(info['bytes'] for info in inventory.values())
used = sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
tar_upper = payload_bytes + len(files) * 8192 + 8 * 2**20
assert used + tar_upper < 4 * 2**30, ('Package would exceed 4 GiB', used, tar_upper)
assert shutil.disk_usage(H).free > tar_upper + 16 * 2**20
archive = R / 'artifacts.tar'
with tarfile.open(archive, 'w') as bundle:
    for p in files:
        bundle.add(p, arcname=relative(p), recursive=False)
for p in files:
    assert p.stat().st_size == inventory[relative(p)]['bytes'] and sha(p) == inventory[relative(p)]['sha256'], ('File changed while packaging', str(p))
durations = [{'run': name, 'status': s['status'], 'started_utc': s.get('started_utc'),
              'ended_utc': s.get('ended_utc'), 'wall_s': s.get('wall_s')}
             for name, s in statuses.items()]
snapshot = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
            'task_complete': False, 'research_questions_closed': False,
            'purpose': 'Complete current artifact checkpoint for independent review; no new experiment',
            'statuses': statuses, 'core_records_previously_audited': 120,
            'nsigma_fixed_units': 60, 'factorial_cases': 30,
            'manifests_verified': verified, 'factorial_reuse': reuse,
            'payload_files': len(files), 'payload_bytes': payload_bytes,
            'run_durations_from_status': durations,
            'sum_available_run_wall_s': sum(row['wall_s'] for row in durations if row['wall_s'] is not None),
            'time_accounting_status': 'Partial process-wall sum, includes overlap; excludes some audits/preflight/idle. Not AWS bill or approved replacement guard.',
            'guard_status': 'Calendar guard remains unchanged; replacement proposal pending Minh approval',
            'pending_research': ['delay/density/flag segments', 'trace/log/workload context',
                                 'updated group/controls lock', 'manual mechanism chains/controls',
                                 'synthesis and further discriminating checks'],
            'progress_tail': (H / 'trang-thai.txt').read_text().splitlines()[-20:],
            'tmux': subprocess.run(['tmux', '-S', str(H / 'tmux.sock'), 'list-sessions'], capture_output=True, text=True).stdout,
            'resources': {'new_bytes_including_archive': sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
                          'ram_available_bytes': psutil.virtual_memory().available,
                          'disk_free_bytes': shutil.disk_usage(H).free},
            'archive': {'name': archive.name, 'sha256': sha(archive), 'bytes': archive.stat().st_size}}
assert snapshot['resources']['new_bytes_including_archive'] < 4 * 2**30
(R / 'artifact-inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
(R / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
for name in ['snapshot.json', 'artifact-inventory.json', 'artifacts.tar']:
    (R / (name + '.sha256')).write_text(sha(R / name) + '  ' + name + '\n')
print(json.dumps({'status': 'PASS', 'utc': snapshot['utc'], 'payload_files': len(files),
                  'payload_bytes': payload_bytes, 'archive_bytes': archive.stat().st_size,
                  'factorial_cases': 30, 'fixed_units': 60, 'manifest_count': len(verified),
                  'resources': snapshot['resources']}))
