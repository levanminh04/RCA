"""T-044: tạo và kiểm results/T-044/manifest.json (SPEC T-044 bước 9; cách làm như results/T-043/scripts/tao_manifest.py).

--tao : ghi sha256, bytes của mọi file trong results/T-044 (trừ manifest.json), src/m1, src/m1_danh_gia (bỏ __pycache__),
        các lượt chạy kể cả lượt hỏng, môi trường.
--kiem: tính lại hash, so với manifest; báo file thiếu, file thừa, hash lệch.
Chạy: python -B results/T-044/scripts/tao_manifest.py --tao ; python -B results/T-044/scripts/tao_manifest.py --kiem
"""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / 'results' / 'T-044' / 'manifest.json'
GOC = ['results/T-044', 'src/m1', 'src/m1_danh_gia']

LUOT = [
    {'duong_dan': 'runs/kiem-hash-t043-001', 'script': 'scripts/kiem_hash_t043.py; tao_manifest.py --kiem của T-043',
     'ket_qua': 'trực tiếp FAIL (luot_thieu runs/khe-open-001); qua script PASS 69/69, 10/10', 'ghi_chu': 'đầu giai đoạn 2'},
    {'duong_dan': 'runs/test-do-001', 'script': 'pytest trên package rỗng', 'ket_qua': '206/208 đỏ',
     'ghi_chu': 'bước 3: khung test trước khi cài'},
    {'duong_dan': 'runs/tat-dinh-000-truoc-sua', 'script': 'pytest, M1_XAO=1, e2.py và e5.py trước khi sửa',
     'ket_qua': 'FAIL 6 phép', 'ghi_chu': 'dựng lại trên bản sao tạm để lưu; xem ghi-chu.md'},
    {'duong_dan': 'runs/tat-dinh-001', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự',
     'ket_qua': 'PASS (104 bản ghi, 226 phép)', 'ghi_chu': 'lượt chạy thử đầu của tat_dinh.py dừng vì thiếu lớp metric; đầu ra lỗi bị ghi đè (LOG)'},
    {'duong_dan': 'runs/dot-bien-001', 'script': 'scripts/dot_bien.py (20 đột biến)', 'ket_qua': '18/20 bị bắt',
     'ghi_chu': 'D02, D10 sống sót; đã vá test'},
    {'duong_dan': 'runs/dot-bien-002', 'script': 'scripts/dot_bien.py (21 đột biến)', 'ket_qua': '21/21 bị bắt',
     'ghi_chu': 'lượt dùng cho tiêu chí 6'},
    {'duong_dan': 'runs/test-xanh-001', 'script': 'pytest -v, PYTHONHASHSEED=0', 'ket_qua': '235/235 qua',
     'ghi_chu': 'lượt dùng cho tiêu chí 2; tổng hợp ở bang-phep-kiem.json'},
    {'duong_dan': 'runs/tat-dinh-002', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự',
     'ket_qua': 'PASS (104 bản ghi, 235 phép)', 'ghi_chu': 'lượt dùng cho tiêu chí 5'},
    {'duong_dan': 'runs/kiem-hash-t043-002', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'cuối phiên'},
]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def tep():
    out = []
    for g in GOC:
        for p in sorted((ROOT / g).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and p != MANIFEST:
                out.append(p)
    return out


def tao():
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    freeze = (ROOT / 'results' / 'T-044' / 'freeze-m1.txt').read_text(encoding='utf-8').split()
    m = {
        'schema': 'T044-manifest-v1', 'task': 'T-044',
        'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'git_head_khi_tao': head,
        'authorization': [['SPEC', 'tasks/T-044-cai-dat-m1/SPEC.md (đã duyệt; Q-212)'],
                          ['giai_doan_2', 'lời Minh trong chat ngày 29/10/2026: "duyệt toàn bộ các đề xuất bên trên của bạn"; '
                                          'ghi ở LOG T-044, giai đoạn 2; dòng DECISIONS chờ Minh duyệt']],
        'trang_thai': 'xong các bước 0–9 trong phạm vi SPEC; chờ Minh quyết Phần II mục A của dinh-chinh-cai-dat.md; '
                      'chờ phản biện',
        'outputs': [{'path': str(p.relative_to(ROOT)).replace('\\', '/'), 'sha256': sha(p), 'bytes': p.stat().st_size}
                    for p in tep()],
        'luot_chay': LUOT,
        'mutable_governance_links_not_hashed': ['tasks/T-044-cai-dat-m1/LOG.md', 'tasks/T-044-cai-dat-m1/SPEC.md',
                                                'docs/STATE.md'],
        'runtime': {'python': platform.python_version(), 'freeze': freeze},
        'manifest_note': 'git_head_khi_tao là commit trước commit chứa manifest này.',
    }
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'so_file': len(m['outputs']), 'git_head_khi_tao': head}, ensure_ascii=False))


def kiem():
    m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    ghi = {x['path']: x for x in m['outputs']}
    that = {str(p.relative_to(ROOT)).replace('\\', '/'): p for p in tep()}
    thieu = sorted(set(ghi) - set(that))
    thua = sorted(set(that) - set(ghi))
    lech = sorted(k for k in set(ghi) & set(that) if sha(that[k]) != ghi[k]['sha256'])
    luot_thieu = [x['duong_dan'] for x in m['luot_chay']
                  if not (ROOT / 'results' / 'T-044' / x['duong_dan']).exists()]
    ok = not (thieu or thua or lech or luot_thieu)
    print(json.dumps({'so_file_manifest': len(ghi), 'so_file_that': len(that), 'thieu': thieu, 'thua': thua,
                      'lech': lech, 'luot_thieu': luot_thieu, 'PASS': ok}, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--tao', action='store_true')
    g.add_argument('--kiem', action='store_true')
    a = ap.parse_args()
    tao() if a.tao else kiem()
