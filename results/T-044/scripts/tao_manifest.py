"""T-044: tạo và kiểm results/T-044/manifest.json (SPEC T-044 bước 9; cách làm như results/T-043/scripts/tao_manifest.py).

--tao : ghi sha256, bytes của mọi file trong results/T-044 (trừ manifest.json), src/m1, src/m1_danh_gia (bỏ __pycache__),
        các lượt chạy kể cả lượt hỏng, môi trường.
--kiem: tính lại hash, so với manifest; báo file thiếu, file thừa, hash lệch.
File ngoài results/ (src/…) còn ghi `git_blob` (git hash-object, theo .gitattributes). Trên Windows, git chuyển
src/*.py sang CRLF khi checkout (.gitattributes chỉ đặt -text cho results/**), nên sha256 của byte lệch dù nội dung
cam kết không đổi. Khi đó --kiem so `git_blob` và liệt kê riêng ở `khop_git_blob`; file trong results/ vẫn so sha256.
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
     'ghi_chu': 'cuối giai đoạn 2'},
    {'duong_dan': 'runs/test-xanh-002', 'script': 'pytest -v, PYTHONHASHSEED=0', 'ket_qua': '246/246 qua',
     'ghi_chu': 'sau gói sửa phản biện lượt 1; tổng hợp ở bang-phep-kiem.json (scripts/tao_bang_phep_kiem.py)'},
    {'duong_dan': 'runs/tat-dinh-003', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự',
     'ket_qua': 'PASS (104 bản ghi, 246 phép)', 'ghi_chu': 'sau gói sửa phản biện lượt 1'},
    {'duong_dan': 'runs/dot-bien-003', 'script': 'scripts/dot_bien.py (27 đột biến)', 'ket_qua': '27/27 bị bắt',
     'ghi_chu': 'sau gói sửa phản biện lượt 1; D22–D27 mới'},
    {'duong_dan': 'runs/kiem-hash-t043-003', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'sau gói sửa phản biện lượt 1'},
    {'duong_dan': 'runs/manifest-crlf-001', 'script': 'tao_manifest.py --kiem trên checkout CRLF giả lập (commit 57234546)',
     'ket_qua': 'thiếu .gitattributes: FAIL (lượt hỏng); có .gitattributes: PASS, 29 file khớp git_blob',
     'ghi_chu': 'N1; xem ghi-chu.md'},
    {'duong_dan': 'runs/test-xanh-003', 'script': 'pytest -v, PYTHONHASHSEED=0', 'ket_qua': '254/254 qua',
     'ghi_chu': 'sau gói sửa phản biện lượt 2; tổng hợp ở bang-phep-kiem.json'},
    {'duong_dan': 'runs/tat-dinh-004', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự; so_ban_ghi_truoc_sau.py',
     'ket_qua': 'PASS (104 bản ghi, 254 phép); bỏ trường mới thì giống 9206eaa6', 'ghi_chu': 'sau gói sửa phản biện lượt 2'},
    {'duong_dan': 'runs/dot-bien-004', 'script': 'scripts/dot_bien.py (35 đột biến)', 'ket_qua': '35/35 bị bắt',
     'ghi_chu': 'sau gói sửa phản biện lượt 2; D28–D35 mới; D26, D27 đổi chỗ theo code mới'},
    {'duong_dan': 'runs/kiem-hash-t043-004', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'sau gói sửa phản biện lượt 2'},
    {'duong_dan': 'runs/test-xanh-004', 'script': 'pytest -v, PYTHONHASHSEED=0 (Windows local; scripts/chay_kiem_windows.sh)',
     'ket_qua': '263/263 qua', 'ghi_chu': 'sau gói sửa phản biện lượt 3; tổng hợp ở bang-phep-kiem.json'},
    {'duong_dan': 'runs/tat-dinh-005', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự; so_ban_ghi_truoc_sau.py; '
                                                 'tong_hop_tat_dinh.py',
     'ket_qua': 'PASS (104 bản ghi, 263 phép); bỏ trường mới và so theo nội dung thì giống 253dbe46',
     'ghi_chu': 'sau gói sửa phản biện lượt 3; lần so đầu (so theo thứ tự) cho 2 bản ghi lệch chỉ do thứ tự, đầu ra bị ghi đè, ghi ở LOG'},
    {'duong_dan': 'runs/dot-bien-005', 'script': 'scripts/dot_bien.py', 'ket_qua': 'lượt hỏng (D11 chuỗi cũ; cp1252)',
     'ghi_chu': 'xem GHI-CHU.txt; đầu ra lần chạy 1 bị xóa nhầm'},
    {'duong_dan': 'runs/dot-bien-006', 'script': 'scripts/dot_bien.py (41 đột biến)', 'ket_qua': '41/41 bị bắt',
     'ghi_chu': 'sau gói sửa phản biện lượt 3; D36–D41 mới; D11 đổi chỗ theo code mới'},
    {'duong_dan': 'runs/kiem-hash-t043-005', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'sau gói sửa phản biện lượt 3 (Windows local)'},
    {'duong_dan': 'runs/test-xanh-005', 'script': 'pytest -v, PYTHONHASHSEED=0 (scripts/chay_kiem_windows.sh)',
     'ket_qua': '266/266 qua', 'ghi_chu': 'sau sửa E1-CP và bước 5 (Minh duyệt 30/10/2026)'},
    {'duong_dan': 'runs/tat-dinh-006', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự; so_ban_ghi_truoc_sau.py; '
                                                 'tong_hop_tat_dinh.py',
     'ket_qua': 'PASS (104 bản ghi, 266 phép); bỏ trường mới thì giống 253dbe46', 'ghi_chu': 'sau sửa E1-CP và bước 5; so với 253dbe46'},
    {'duong_dan': 'runs/dot-bien-007', 'script': 'scripts/dot_bien.py (44 đột biến)', 'ket_qua': '44/44 bị bắt',
     'ghi_chu': 'sau sửa E1-CP và bước 5; D42–D44 mới; D30 đổi chỗ theo code mới'},
    {'duong_dan': 'runs/kiem-hash-t043-006', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'sau sửa E1-CP và bước 5'},
    {'duong_dan': 'runs/test-xanh-006', 'script': 'pytest -v, PYTHONHASHSEED=0 (scripts/chay_kiem_windows.sh)',
     'ket_qua': '289/289 qua', 'ghi_chu': 'lượt 4, trước bản cuối (sau đó đổi log T4c sang log1p, khóa C-d2 số thực)'},
    {'duong_dan': 'runs/tat-dinh-007', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự; so_ban_ghi_truoc_sau.py; '
                                                 'tong_hop_tat_dinh.py',
     'ket_qua': 'PASS (104 bản ghi, 289 phép); so với 253dbe46 lệch 104 vì trường mới E6b_pi và khóa C-d2 dạng số',
     'ghi_chu': 'lượt 4, trước bản cuối; đầu ra so sánh bị ghi đè một lần khi người làm thêm bỏ E6b_pi, ghi ở LOG'},
    {'duong_dan': 'runs/dot-bien-008', 'script': 'scripts/dot_bien.py (58 đột biến)', 'ket_qua': '58/58 bị bắt',
     'ghi_chu': 'lượt 4, trước bản cuối'},
    {'duong_dan': 'runs/kiem-hash-t043-007', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'lượt 4, trước bản cuối'},
    {'duong_dan': 'runs/test-xanh-007', 'script': 'pytest -v, PYTHONHASHSEED=0 (scripts/chay_kiem_windows.sh)',
     'ket_qua': '289/289 qua', 'ghi_chu': 'sau gói sửa phản biện lượt 4, bản cuối'},
    {'duong_dan': 'runs/tat-dinh-008', 'script': 'scripts/tat_dinh.py; pytest 3 hash seed × 4 thứ tự; so_ban_ghi_truoc_sau.py; '
                                                 'tong_hop_tat_dinh.py; so_truong_ban_ghi.py',
     'ket_qua': 'PASS (104 bản ghi, 289 phép); so với 253dbe46: 16 bản ghi lệch, chỉ m của T4c chữ số cuối',
     'ghi_chu': 'sau gói sửa phản biện lượt 4, bản cuối'},
    {'duong_dan': 'runs/dot-bien-009', 'script': 'scripts/dot_bien.py (58 đột biến)', 'ket_qua': '58/58 bị bắt',
     'ghi_chu': 'sau gói sửa phản biện lượt 4, bản cuối; D45–D58 mới; D03, D13 đổi chỗ theo code mới'},
    {'duong_dan': 'runs/kiem-hash-t043-008', 'script': 'scripts/kiem_hash_t043.py', 'ket_qua': 'PASS 69/69, 10/10',
     'ghi_chu': 'sau gói sửa phản biện lượt 4, bản cuối'},
]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def git_blob(paths):
    """git hash-object theo đường dẫn (áp chuyển dòng của .gitattributes): cùng blob với bản đã cam kết."""
    if not paths:
        return {}
    r = subprocess.run(['git', 'hash-object', '--'] + [str(p) for p in paths], cwd=ROOT, capture_output=True,
                       text=True, check=True)
    return dict(zip(paths, r.stdout.split()))


def _ngoai_results(p):
    return not str(p.relative_to(ROOT)).replace('\\', '/').startswith('results/')


def tep():
    out = []
    for g in GOC:
        for p in sorted((ROOT / g).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and p != MANIFEST:
                out.append(p)
    return out


def tao():
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    ds = tep()
    gb = git_blob([p for p in ds if _ngoai_results(p)])
    freeze = (ROOT / 'results' / 'T-044' / 'freeze-m1.txt').read_text(encoding='utf-8').split()
    m = {
        'schema': 'T044-manifest-v2', 'task': 'T-044',
        'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'git_head_khi_tao': head,
        'authorization': [['SPEC', 'tasks/T-044-cai-dat-m1/SPEC.md (đã duyệt; Q-212)'],
                          ['giai_doan_2', 'lời Minh trong chat ngày 29/10/2026: "duyệt toàn bộ các đề xuất bên trên của bạn"; '
                                          'ghi ở LOG T-044, giai đoạn 2; dòng DECISIONS chờ Minh duyệt'],
                          ['sua_sau_phan_bien_1', 'lời Minh trong chat ngày 29/10/2026: "DUYỆT SỬA LUÔN"; ghi ở LOG T-044, '
                                                  'mục "Phản hồi phản biện lượt 1 và gói sửa"'],
                          ['sua_sau_phan_bien_2', 'lời Minh trong chat ngày 29/10/2026: "NẾU KHÔNG CÓ ĐIỂM NÀO XUNG '
                                                  'ĐỘT THÌ SỬA NGAY"; ghi ở LOG T-044, mục "Phản hồi phản biện lượt 2 '
                                                  'và gói sửa"'],
                          ['sua_sau_phan_bien_3', 'lời Minh trong chat ngày 30/10/2026: "duyệt sửa"; ghi ở LOG T-044, mục '
                                                  '"Phản hồi phản biện lượt 3 và gói sửa"; S12, S13, S15, S16 (S14, S17 chờ Minh)'],
                          ['E1CP_buoc5', 'lời Minh trong chat ngày 30/10/2026: "duyệt E1-CP, bước 5 như trên"; biên E1-CP: '
                                         '"Biên mở"; ghi ở LOG T-044 và dinh-chinh-cai-dat.md mục C5'],
                          ['sua_sau_phan_bien_4', 'lời Minh trong chat ngày 30/10/2026: "Duyệt cả gói"; ghi ở LOG T-044, '
                                                  'mục "Phản hồi phản biện lượt 4 và gói sửa"; dinh-chinh-cai-dat.md mục C6']],
        'trang_thai': 'xong các bước 0–9 trong phạm vi SPEC; Phần II mục A của dinh-chinh-cai-dat.md đã được Minh duyệt '
                      '(29/10/2026); đã sửa sau phản biện lượt 1 (Phần II mục C2), lượt 2 (mục C3) và lượt 3 (mục C4); E1-CP và bước 5 đã quyết và sửa (mục C5); lượt 4 (mục C6, gồm S14, S17); chờ phản biện kiểm lại',
        'outputs': [dict({'path': str(p.relative_to(ROOT)).replace('\\', '/'), 'sha256': sha(p),
                          'bytes': p.stat().st_size}, **({'git_blob': gb[p]} if p in gb else {}))
                    for p in ds],
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
    lech_sha = sorted(k for k in set(ghi) & set(that) if sha(that[k]) != ghi[k]['sha256'])
    gb = git_blob([that[k] for k in lech_sha if 'git_blob' in ghi[k]])
    khop_git_blob = sorted(k for k in lech_sha if that[k] in gb and gb[that[k]] == ghi[k]['git_blob'])
    lech = [k for k in lech_sha if k not in khop_git_blob]
    luot_thieu = [x['duong_dan'] for x in m['luot_chay']
                  if not (ROOT / 'results' / 'T-044' / x['duong_dan']).exists()]
    ok = not (thieu or thua or lech or luot_thieu)
    print(json.dumps({'so_file_manifest': len(ghi), 'so_file_that': len(that), 'thieu': thieu, 'thua': thua,
                      'lech': lech, 'khop_git_blob': khop_git_blob, 'luot_thieu': luot_thieu, 'PASS': ok}, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--tao', action='store_true')
    g.add_argument('--kiem', action='store_true')
    a = ap.parse_args()
    tao() if a.tao else kiem()
