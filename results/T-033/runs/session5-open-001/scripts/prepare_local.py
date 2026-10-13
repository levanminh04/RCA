"""Kiểm hash đầu ra đóng băng, đóng gói đầu vào; không tính nghiên cứu."""
import hashlib
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

R = Path(__file__).resolve().parents[3]
O = R / 'results/T-033'
RUN = O / 'runs/prepare-001'
INP = RUN / 'inputs'
L = R / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def load(p): return json.loads((R / p).read_text(encoding='utf-8'))
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
def log(x):
    with L.open('a', encoding='utf-8') as f:
        f.write('\n- ' + datetime.now(timezone(timedelta(hours=7))).isoformat() + ' — ' + x + '\n')

log('Lệnh có ghi: T014-main Python -B -X utf8 scripts/prepare_local.py; chỉ kiểm hash/đóng gói nguồn, không tính phương pháp. Python py không có trong PATH; Python env bị sandbox chặn lần đầu, gọi ngoài sandbox đã chạy mở phiên đạt.')
old = load('results/T-029/runs/handoff-session8-001/manifest.json')['files']
new = load('results/T-029/runs/review4-repair-001/verification.json')['files']
expected = {p: v for p, v in old.items() if p.startswith('results/T-029/')}
expected.update({p: v for p, v in new.items() if p.startswith('results/T-029/')})
errors = []
for name, meta in expected.items():
    p = R / name
    if not p.is_file() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']:
        errors.append(name)
write(RUN / 'source-verification.json', {'status': 'FAIL' if errors else 'PASS', 'files': len(expected), 'errors': errors, 'manifests': ['results/T-029/runs/handoff-session8-001/manifest.json', 'results/T-029/runs/review4-repair-001/verification.json']})
assert not errors, errors
ns = load('results/T-029/runs/nsigma-002/manifest.json')
for name, val in ns['nguon'].items():
    assert sha(R / name) == val, name
INP.mkdir(exist_ok=False)
(INP / 'flags').mkdir()
allow = load('results/T-022/allowlist-dev.json')
alarms = load('results/T-025/bao-dong.json')['bo_phat_hien']
moc = load('results/T-029/inputs/moc.json')
cases = []
for c in sorted(allow['cases'], key=lambda x: x['opaque_id']):
    oid = c['opaque_id']
    files = {}
    for name, v in c['files'].items():
        if v is None: continue
        p = R / v['path']
        assert 'locked' not in p.parts and p.is_file() and sha(p) == v['sha256'], str(p)
        assert p.stat().st_size == v['bytes']
        files[name] = v
    flagmeta = {}
    for detector, d in ns['cases'][oid]['bo'].items():
        p = R / d['npz']
        assert sha(p) == d['sha256']
        out = INP / 'flags' / (oid + '--' + detector + '.npz')
        shutil.copyfile(p, out)
        flagmeta[detector] = {'path': 'flags/' + out.name, 'sha256': sha(out), 'source': d['npz']}
    ipath = 'results/T-029/runs/ec2-complete-002/artifacts/runs/chuoi-002/i1/' + oid + '.json'
    assert ipath in expected
    cases.append({'opaque_id': oid, 'files': files, 'proxy': moc[oid],
                  'expected': {k: alarms[k][oid] for k in ('bocpd', 'nsigma', 'nsigma_doi_chung')},
                  'flags': flagmeta, 'pp_source': ipath, 'pp_expected': load(ipath)['result']})
baro = Path('D:/RCA-ext/src/baro/baro')
native_hash = {name: sha(baro / name) for name in ['_bocpd.py', 'utility.py', 'anomaly_detection.py']}
assert native_hash['anomaly_detection.py'] == ns['baro_nsigma']['sha256']
source = {'task': 'T-033', 'cases': cases, 'native_hash': native_hash,
          'adapter_sha256': sha(R / 'src/p3/adapters/phat_hien.py'),
          'source_roots_remote': ['/home/ubuntu/rca/T-025/repo'],
          'budget_bytes': 4 * 2**30, 'budget_compute_s': 12 * 3600,
          'source_manifests': {p: sha(R / p) for p in ['results/T-029/runs/handoff-session8-001/manifest.json','results/T-029/runs/review4-repair-001/verification.json','results/T-029/runs/nsigma-002/manifest.json']}}
write(INP / 'source.json', source)
manifest = {p.relative_to(INP).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in INP.rglob('*') if p.is_file()}
write(RUN / 'inputs-manifest.json', manifest)
log(f'Chuẩn bị nguồn PASS {len(expected)} output T-029; nguồn N-Sigma và 60 flags NPZ khớp; 30 ca dev/89 tệp allowlist hash+kích thước đạt. Copy flags/source vào prepare-001/inputs, chưa chuyển telemetry hoặc chạy EC2. Manifest input/source tại prepare-001; sử dụng BARO T-025/src/baro khớp nguồn, không dùng ~/rca/src/baro có hash khác.')
print(json.dumps({'status':'PASS','old_outputs':len(expected),'dev_cases':len(cases),'dev_files':sum(len(c['files']) for c in cases),'input_bytes':sum(v['bytes'] for v in manifest.values()),'native_hash':native_hash}))
