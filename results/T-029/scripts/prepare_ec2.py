"""Chuẩn bị input đã khóa và bản chép runner; chỉ ghi results/T-029."""
import hashlib
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

R = Path(__file__).resolve().parents[3]
O = R / 'results/T-029'
L = R / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'

def log(s):
    with L.open('a', encoding='utf-8') as f:
        f.write('\n- ' + datetime.now(timezone(timedelta(hours=7))).isoformat() + ' — ' + s + '\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

log('Lệnh có ghi: T-014-main python -B -W ignore results/T-029/scripts/prepare_ec2.py. Tạo inputs/ và bản chép rca_b.py/chay_b.py trong scripts/, giữ nguyên nguồn T-025; lưu manifest chuẩn bị trong runs/prepare-ec2-001/.')
num = 1
while (O / f'runs/prepare-ec2-{num:03d}').exists():
    num += 1
run = O / f'runs/prepare-ec2-{num:03d}'
run.mkdir(parents=True, exist_ok=False)
inp = run / 'inputs'
inp.mkdir(exist_ok=False)
manifest = {'task': 'T-029', 'sources': {}, 'inputs': {}}
for name in ('rca_b.py', 'chay_b.py'):
    src = R / 'results/T-025/scripts' / name
    dst = O / 'scripts' / name
    shutil.copyfile(src, dst)
    manifest['sources'][src.relative_to(R).as_posix()] = sha(src)
    assert sha(dst) == sha(src)
for src, name in [('results/T-022/allowlist-dev.json', 'allowlist-dev.json'), ('results/T-025/bao-dong.json', 'bao-dong.json')]:
    shutil.copyfile(R / src, inp / name)
    manifest['sources'][src] = sha(R / src)
from p3.nhan import nap_moc
moc = nap_moc(R / 'results/T-022/nhan-dev.json')
(inp / 'moc.json').write_text(json.dumps(moc, indent=2), encoding='utf-8')
manifest['sources']['results/T-022/nhan-dev.json'] = sha(R / 'results/T-022/nhan-dev.json')
prev = json.loads((O / 'runs/buoc0-001/manifest.json').read_text(encoding='utf-8'))
files = sorted((R / 'src/p3').rglob('*.py'), key=lambda p: p.relative_to(R).as_posix())
assert {p.relative_to(R).as_posix(): sha(p) for p in files} == prev['src_p3']['tep'], 'V1 src/p3 lệch'
(inp / 'src-p3-expected.json').write_text(json.dumps(prev['src_p3'], indent=2), encoding='utf-8')
bd = json.loads((inp / 'bao-dong.json').read_text(encoding='utf-8'))['bo_phat_hien']
v4id = min(oid for oid, rec in bd['nsigma'].items() if moc[oid] in rec['alarms'])
frozen = json.loads((R / 'results/T-024/ban-ghi-dua-vao-cham.json').read_text(encoding='utf-8'))
expected = []
for rec in frozen['records']:
    if rec['opaque_id'] != v4id or rec['method'] not in ('baro', 'circa', 'torai'):
        continue
    if rec['method'] == 'torai' and rec['variant'] != 'B':
        continue
    if rec['method'] == 'circa' and rec['variant'] not in ('ols+rht', 'ols+rht_da'):
        continue
    p = R / rec['path']
    assert sha(p) == rec['sha256'], 'V4 nguồn chế độ a lệch hash'
    rr = json.loads(p.read_text(encoding='utf-8'))
    expected.append({'method': rr['method'], 'variant': rr['variant'], 'seed': rr['seed'], 'status': rr['status'],
                     'ranking_native': rr['ranking_native'], 'source_path': rec['path'], 'source_sha256': sha(p)})
assert len(expected) == 6, len(expected)
(inp / 'v4-expected.json').write_text(json.dumps({'opaque_id': v4id, 'records': expected}, ensure_ascii=False, indent=2), encoding='utf-8')
manifest['sources']['results/T-024/ban-ghi-dua-vao-cham.json'] = sha(R / 'results/T-024/ban-ghi-dua-vao-cham.json')
for p in sorted(inp.iterdir()):
    manifest['inputs'][p.name] = {'sha256': sha(p), 'bytes': p.stat().st_size}
(run / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
log(f'Chuẩn bị xong: inputs guard + báo động + mốc (không root/fault) + V4 expected 6 bản ghi/{v4id}; rca_b.py/chay_b.py chép nguyên văn và kiểm hash khớp. Chưa chép EC2 hoặc chạy phương pháp.')
print(json.dumps({'status': 'PASS', 'v4id': v4id, 'v4_records': len(expected), 'inputs': str(inp)}))
