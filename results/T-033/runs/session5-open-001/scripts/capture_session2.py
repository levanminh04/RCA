"""Checkpoint metadata T-033; hash đầu ra, không tính lại detector/dataset."""
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
assert H == Path('/home/ubuntu/rca/T-033')
R = H / 'runs/checkpoint-session2-001'
R.mkdir(exist_ok=False)
M = R / 'metadata'
M.mkdir()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(2**20), b''):
            h.update(block)
    return h.hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def relative(path):
    path = path.resolve()
    assert H in path.parents and 'T-032' not in path.parts
    return str(path.relative_to(H))


def metadata_copy(path):
    destination = M / relative(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(path.read_bytes())


def verify_manifest(directory, name='manifest.json'):
    manifest = directory / name
    doc = load(manifest)
    checked = {}
    for filename, info in doc.items():
        path = directory / filename
        relative(path)
        assert path.is_file() and path.stat().st_size == info['bytes'], str(path)
        assert sha(path) == info['sha256'], str(path)
        checked[relative(path)] = info
    metadata_copy(manifest)
    return {'manifest_sha256': sha(manifest), 'files': checked}


names = ['nsigma-first-001', 'nsigma-rest-001', 'bocpd-first-001',
         'bocpd-first-002', 'bocpd-rest-001', 'bocpd-factorial-first-001',
         'bocpd-factorial-rest-001', 'nsigma-frozen-first-001',
         'nsigma-frozen-rest-001']
snapshot = {'utc': datetime.now(timezone.utc).isoformat(), 'task_complete': False,
            'research_questions_closed': False, 'statuses': {},
            'completed_manifests_verified': {}, 'live_completed_branches_verified': [],
            'live_completed_cases': [], 'scripts': {}, 'anchors': {}}
for name in names:
    directory = H / 'runs' / name
    status_path = directory / 'status.json'
    # Atomic driver status is copied at this point; live progress can advance later.
    content = status_path.read_bytes()
    status = json.loads(content)
    snapshot['statuses'][name] = status
    destination = M / relative(status_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    if name in ['bocpd-factorial-first-001', 'nsigma-frozen-first-001', 'nsigma-frozen-rest-001']:
        assert status['status'] == 'PASS', name
        snapshot['completed_manifests_verified'][name] = verify_manifest(directory)
        if (directory / 'logs-manifest.json').is_file():
            verify_manifest(directory, 'logs-manifest.json')
        for path in directory.glob('*.json'):
            metadata_copy(path)
    elif name == 'bocpd-factorial-rest-001':
        for oid, case in status['cases'].items():
            if case['status'] != 'PASS':
                continue
            snapshot['live_completed_cases'].append(oid)
            for branch, record in case['branches'].items():
                assert record['status'] == 'PASS' and all(record['checks'].values())
                original = H / record['reused_record'] if record.get('reused_record') else directory / (oid + '--' + branch + '.json')
                doc = load(original)
                path = original.parent / doc['npz']
                assert path.stat().st_size == doc['bytes'] and sha(path) == doc['sha256']
                snapshot['live_completed_branches_verified'].append({
                    'opaque_id': oid, 'branch': branch, 'record': relative(original),
                    'npz': relative(path), 'sha256': doc['sha256']})
                metadata_copy(original)
            metadata_copy(directory / case['factorial_record'])

fixed = [entry for name in ['nsigma-frozen-first-001', 'nsigma-frozen-rest-001']
         for case in snapshot['statuses'][name]['cases'].values() for entry in case.values()]
assert len(fixed) == 60 and all(e['status'] == 'PASS' and all(e['checks'].values()) for e in fixed)
snapshot['nsigma_fixed_units_verified'] = len(fixed)
core_audit = H / 'runs/core-audit-002/verification.json'
assert load(core_audit)['status'] == 'PASS'
metadata_copy(core_audit)
snapshot['core_audit_sha256'] = sha(core_audit)
for path in [H / 'inputs/source.json', H / 'runs/preflight-002/inventory.json',
             H / 'runs/preflight-002/verification.json',
             H / 'runs/bocpd-first-002/manifest.json', H / 'runs/bocpd-rest-001/manifest.json',
             H / 'runs/nsigma-first-001/manifest.json', H / 'runs/nsigma-rest-001/manifest.json']:
    snapshot['anchors'][relative(path)] = {'sha256': sha(path), 'bytes': path.stat().st_size}
    metadata_copy(path)
for path in (H / 'scripts').glob('*'):
    if path.is_file():
        snapshot['scripts'][path.name] = sha(path)
snapshot['progress_tail'] = (H / 'trang-thai.txt').read_text().splitlines()[-30:]
pid = snapshot['statuses']['bocpd-factorial-rest-001']['pid']
snapshot['ps'] = subprocess.run(['ps', '-p', str(pid), '-o', 'pid,etimes,rss,pcpu,args'],
                                capture_output=True, text=True).stdout
snapshot['tmux'] = subprocess.run(['tmux', '-S', str(H / 'tmux.sock'), 'list-sessions'],
                                  capture_output=True, text=True).stdout
snapshot['resources'] = {
    'new_bytes': sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
    'ram_available_bytes': psutil.virtual_memory().available,
    'disk_free_bytes': shutil.disk_usage(H).free}
assert snapshot['resources']['new_bytes'] < 4 * 2**30
(R / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
with tarfile.open(R / 'metadata.tar.gz', 'w:gz') as archive:
    archive.add(M, arcname='metadata')
for filename in ['snapshot.json', 'metadata.tar.gz']:
    path = R / filename
    (R / (filename + '.sha256')).write_text(sha(path) + '  ' + filename + '\n')
print(json.dumps({'status': 'PASS', 'utc': snapshot['utc'],
                  'fixed_units_verified': len(fixed),
                  'factorial_status': snapshot['statuses']['bocpd-factorial-rest-001']['status'],
                  'factorial_cases_verified': snapshot['live_completed_cases'],
                  'resources': snapshot['resources'],
                  'metadata_archive_bytes': (R / 'metadata.tar.gz').stat().st_size}))
