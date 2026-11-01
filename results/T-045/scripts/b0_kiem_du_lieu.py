"""T-045 bước 0: kiểm SHA-256 mọi file dữ liệu dev theo allowlist (RE2-TT T-022, Nezha-OB T-026) và hash các file
đầu vào chặng 1. Chỉ đọc byte để băm; không đọc nhãn. Ghi JSON ra thư mục lượt.
Chạy: $PY -B results/T-045/scripts/b0_kiem_du_lieu.py results/T-045/runs/<lượt>
"""
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# hash mong đợi của allowlist: KS-16 pha 1 ghi ở results/T-043/ks16/dem-khong-nhan.json#/inputs
ALLOW = {'results/T-022/allowlist-dev.json': 'fec512d7dbf059b86c7049127c9fd7a899f3e6508d8ba472b160867b74e32ac3',
         'results/T-026/allowlist-dev.json': '33af350c8200abd5be91c12357cc52abe50a0394ba69b7d6abe117da5be78a1a'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    kq = {'allowlist': {}, 'RE2-TT': {'so_ca': 0, 'so_file': 0, 'lech': [], 'thieu': []},
          'Nezha-OB': {'so_ca': 0, 'so_file': 0, 'lech': [], 'thieu': []}}
    for rel, mong in ALLOW.items():
        h = sha(ROOT / rel)
        kq['allowlist'][rel] = {'sha256': h, 'mong_doi_KS16': mong, 'khop': h == mong}
    for rel, ds in (('results/T-022/allowlist-dev.json', 'RE2-TT'), ('results/T-026/allowlist-dev.json', 'Nezha-OB')):
        a = json.loads((ROOT / rel).read_text(encoding='utf-8'))
        for c in a['cases']:
            kq[ds]['so_ca'] += 1
            for _, m in sorted(c['files'].items()):
                if not m:
                    continue
                p = ROOT / m['path']
                if not p.exists():
                    kq[ds]['thieu'].append(m['path'])
                    continue
                kq[ds]['so_file'] += 1
                if sha(p) != m['sha256']:
                    kq[ds]['lech'].append(m['path'])
    kq['PASS'] = (all(v['khop'] for v in kq['allowlist'].values())
                  and not any(kq[d]['lech'] or kq[d]['thieu'] for d in ('RE2-TT', 'Nezha-OB')))
    kq['giay'] = round(time.time() - t0, 1)
    (out / 'du-lieu.json').write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({k: (v if k != 'allowlist' else {x: y['khop'] for x, y in v.items()}) for k, v in kq.items()},
                     ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1])
