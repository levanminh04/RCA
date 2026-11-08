"""Đóng gói lượt dev EC2: kiểm code cục bộ = pin của dev-ob-001, kiểm hash dữ liệu dev, chia ca hai máy.
Chạy từ gốc repo. Ghi goi/{code.tar.gz, data-ec2_1.tar, data-ec2_2.tar, ca-ec2_1.json, ca-ec2_2.json, goi.json}."""
import hashlib
import json
import tarfile
from pathlib import Path

GOC = Path.cwd()
RUN = GOC / 'results/T-054/runs/sua-cd3-ob-001'
G = RUN / 'goi'
G.mkdir(exist_ok=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# pin/config lấy từ job M1 Nezha-OB của main-013-v2 (code đã chạy test); chỉ đọc pin/config, không đọc dữ liệu
_pt = json.loads((GOC / 'results/T-054/reports/p7a-013-v2/phan-tich-nhom.json').read_text(encoding='utf-8'))
_k = sorted(k for k in _pt['trung_gian_theo_ca'] if k.startswith('Nezha-OB|'))[0]
JOB_PIN = (GOC / _pt['trung_gian_theo_ca'][_k]['M1']['result']).parent / 'job.json'
job = json.loads(JOB_PIN.read_text(encoding='utf-8'))
assert job['slot']['arm'] == 'M1' and job['slot']['dataset'] == 'Nezha-OB'
lech = [p for p, h in job['code_pins'].items() if sha(GOC / p) != h]
assert not lech, lech
code = sorted(p for p in job['code_pins'] if p.startswith('src/') or p.startswith('results/T-054/scripts/'))
code += ['results/T-043/hop-dong.json', 'results/T-054/runs/sua-cd3-ob-001/lane.py',
         'results/T-054/runs/sua-cd3-ob-001/dev_ec2.py']
assert sha(GOC / 'results/T-043/hop-dong.json') == job['m1_contract']['sha256']
with tarfile.open(G / 'code.tar.gz', 'w:gz') as t:
    for p in code:
        t.add(GOC / p, arcname=p)
a = json.loads((GOC / 'results/T-026/allowlist-dev.json').read_text(encoding='utf-8'))
cases = {c['opaque_id']: c for c in a['cases']}
ids = sorted(cases)
assert len(ids) == 22 and 'dev-607751ac0a' in ids
ids.remove('dev-607751ac0a')
chia = {'ec2_1': ['dev-607751ac0a'] + ids[0::2], 'ec2_2': ids[1::2]}
info = {'job_pin': str(JOB_PIN.relative_to(GOC)), 'code_pins_khop': len(job['code_pins']), 'code_files': {p: sha(GOC / p) for p in code}, 'chia': chia,
        'config_sha256_slot': job['slot']['config_sha256']}
for host, ds in chia.items():
    rows = {o: {'files': cases[o]['files'], 't_ns': cases[o]['t_ns'], 'trace_guard_s': cases[o]['trace_guard_s']} for o in ds}
    files = sorted({m['path'] for o in ds for m in cases[o]['files'].values()})
    for o in ds:
        for m in cases[o]['files'].values():
            assert (GOC / m['path']).stat().st_size == m['bytes'] and sha(GOC / m['path']) == m['sha256'], m['path']
    (G / f'ca-{host}.json').write_text(json.dumps({'config': job['config'], 'inventory': job['inventory'], 'cases': rows},
                                                  ensure_ascii=False, sort_keys=True), encoding='utf-8')
    with tarfile.open(G / f'data-{host}.tar', 'w') as t:
        for p in files:
            t.add(GOC / p, arcname=p)
    info[host] = {'n_ca': len(ds), 'n_file': len(files), 'bytes': sum((GOC / p).stat().st_size for p in files)}
for f in sorted(G.iterdir()):
    if f.name != 'goi.json':
        info.setdefault('goi_sha256', {})[f.name] = sha(f)
(G / 'goi.json').write_text(json.dumps(info, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
print(json.dumps({k: info[k] for k in ('code_pins_khop', 'ec2_1', 'ec2_2')}))
