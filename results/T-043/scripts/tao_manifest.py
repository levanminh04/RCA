"""T-043 phiên 8, cập nhật phiên 9 (Q-207): tạo và kiểm results/T-043/manifest.json. Chỉ đọc file trong results/T-043 và git HEAD.

--tao : ghi manifest (sha256, bytes của mọi file trong results/T-043 trừ manifest.json), lượt chạy kể cả lượt hỏng,
        hash đóng băng ghi ở LOG phiên 7, hai bản luật F.
--kiem: tính lại hash mọi file, so với manifest; báo file thiếu, file thừa, hash lệch; kiểm hash đóng băng phiên 7.
Chạy: python -B results/T-043/scripts/tao_manifest.py --tao ; python -B results/T-043/scripts/tao_manifest.py --kiem
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GOC = ROOT / 'results/T-043'
MANIFEST = GOC / 'manifest.json'

# Hash ghi ở LOG phiên 7 khi đóng băng (tasks/T-043-thiet-ke-rca-m1/LOG.md, mục "Tiến độ thực hiện").
DONG_BANG_PHIEN7 = {
    'ks16/dem-khong-nhan.json': '4e9bef52181fd96e853cf8e17bd7fce1f42f20f8de175577ab620d51675fbd8d',
    'ks16/ks16_pha1.py': '92b1994a13620d4c678004d6f1e6e5047c613c087255968d0bd7f91dc7d56de6',
    'dinh-nghia-pha2.json': '7521100b56ac75993735efcd1369b5cb7919b30844da0f469d7c67418abc5e3d',
    'dac-ta-phuong-phap-v1.md': 'a2c04ad693ea03950653dd6aedf90d4d82327b73e2f4c963d7c1221fc9e7f014',
    'hop-dong.json': '35f3c603d0260c897d163346c09120fab2bc624e680bab6ec7a08cc508a9f446',
    'ks16/dem-sau-ghep-nhan.json': '7b58756bf95a68acb187dc0e7cb0509b57715fddad0341a85434acc42cf46e9a',
    'ks16/ks16_pha2.py': '1801378eaeb87d53c39b4c1ac005eec51367ce1c981ec25ce5006ac0b56ea479',
    'fixture-dac-ta.json': 'af0c914757ca31f59e999efde7f39c1da16b563074bd7bef3d91600c143196e4',
    'fixture/kiem_fixture.py': '5a95bcbee3a0f441ac4fdebe1ecf9b8036cbe0289d646c6e202ce214bc01df04',
    'ma-tran-thu.json': 'db475fcc477bae3240ea4613427b61e829147866d49ecf74a3d8196fe39d332f',
}

LUOT = [
    {'duong_dan': 'runs/hash-nguon-001', 'script': 'scripts/kiem_hash_nguon.py', 'ket_qua': 'FAIL',
     'ghi_chu': 'đọc sai khóa ghim allowlist T-022, chưa tách file dùng/không dùng; giữ'},
    {'duong_dan': 'runs/hash-nguon-002', 'script': 'scripts/kiem_hash_nguon.py', 'ket_qua': 'PASS', 'ghi_chu': 'mọi nguồn T-043 dùng'},
    {'duong_dan': 'runs/hash-nguon-003', 'script': 'scripts/kiem_hash_nguon.py', 'ket_qua': 'PASS', 'ghi_chu': 'thêm T-038, T-039'},
    {'duong_dan': 'ks16/runs/thu-nhanh-001', 'script': 'ks16/ks16_pha1.py (bản trước khi sửa luật H)', 'ket_qua': 'giữ, không dùng',
     'ghi_chu': '2 ca, không nhãn; thấy OPEN giả do H theo từng phía; luật H sửa trước khi chạy đủ (LOG phiên 7)'},
    {'duong_dan': 'ks16/runs/pha1-001', 'script': 'ks16/ks16_pha1.py', 'ket_qua': 'PASS 52/52', 'luat_F': 'v1',
     'ghi_chu': 'không nhãn; chép thành ks16/dem-khong-nhan.json'},
    {'duong_dan': 'ks16/runs/pha2-001', 'script': 'ks16/ks16_pha2.py', 'ket_qua': 'PASS', 'luat_F': 'v1',
     'ghi_chu': 'ghép nhãn sau barrier; chép thành ks16/dem-sau-ghep-nhan.json'},
    {'duong_dan': 'fixture/runs/kiem-001.json', 'script': 'fixture/kiem_fixture.py (bản trước)', 'ket_qua': '108/109',
     'ghi_chu': 'mục 47 thiếu hai trường đầu ra trong script; giữ'},
    {'duong_dan': 'fixture/runs/kiem-002.json', 'script': 'fixture/kiem_fixture.py', 'ket_qua': '109/109',
     'ghi_chu': 'chép thành fixture/ket-qua-kiem.json'},
    {'duong_dan': 'runs/bien-F-001', 'script': 'scripts/kiem_bien_F.py', 'ket_qua': 'PASS', 'ghi_chu': 'phiên 8; căn cứ F_s, không nhãn'},
    {'duong_dan': 'ks16/runs/thu-nhanh-002', 'script': 'ks16/ks16_pha1_v11.py', 'ket_qua': 'PASS 2 ca', 'luat_F': 'v1.1',
     'ghi_chu': 'phiên 8; thử nhanh luật v1.1'},
    {'duong_dan': 'ks16/runs/pha1-002', 'script': 'ks16/ks16_pha1_v11.py', 'ket_qua': 'PASS 52/52', 'luat_F': 'v1.1', 'ghi_chu': 'phiên 8; không nhãn'},
    {'duong_dan': 'ks16/runs/pha2-002', 'script': 'ks16/ks16_pha2_v11.py', 'ket_qua': 'PASS', 'luat_F': 'v1.1',
     'ghi_chu': 'phiên 8; kiểm hash pha1-002 trước khi ghép nhãn'},
    {'duong_dan': 'runs/so-v1-v11-001', 'script': 'scripts/so_v1_v11.py (bản đầu, không giữ)', 'ket_qua': 'giữ, thay bằng 004',
     'ghi_chu': 'chưa tách khác kiểu số; stdout in ra màn hình, không lưu'},
    {'duong_dan': 'runs/so-v1-v11-002', 'script': 'scripts/so_v1_v11.py (bản thứ hai, không giữ)', 'ket_qua': 'giữ, thay bằng 004',
     'ghi_chu': 'tính cả thời gian chạy theo ca là khác giá trị'},
    {'duong_dan': 'runs/so-v1-v11-003', 'script': 'scripts/so_v1_v11.py (bản thứ ba, không giữ)', 'ket_qua': 'giữ, thay bằng 004',
     'ghi_chu': 'chưa có phần điểm đơn vị đếm; phần chung trùng 004'},
    {'duong_dan': 'runs/so-v1-v11-004', 'script': 'scripts/so_v1_v11.py', 'ket_qua': 'PASS', 'ghi_chu': 'bản dùng trong báo cáo'},
    {'duong_dan': 'runs/khe-open-001', 'script': 'scripts/the_gioi_khe_open.py (bản đầu)', 'ket_qua': 'FAIL', 'luat_F': '(a)',
     'ghi_chu': 'phiên 9; ghép thừa tiền tố đường dẫn khi đối chiếu manifest, dừng ở bước kiểm hash, không ghi kết quả; giữ'},
    {'duong_dan': 'runs/khe-open-002', 'script': 'scripts/the_gioi_khe_open.py', 'ket_qua': 'PASS', 'luat_F': '(a)',
     'ghi_chu': 'phiên 9; ba thế giới khi khe giữa file là OPEN; không nhãn'},
    {'duong_dan': 'fixture/runs/kiem-bo-sung-001.json', 'script': 'fixture/kiem_bo_sung.py', 'ket_qua': '7/7',
     'ghi_chu': 'phiên 9; fixture bổ sung B1–B7 (Q-207)'},
    {'duong_dan': 'fixture/runs/kiem-bo-sung-002.json', 'script': 'fixture/kiem_bo_sung.py (bản hợp khoảng, Đ20)', 'ket_qua': '8/8',
     'ghi_chu': 'phiên 10; thêm B8 (file lồng nhau); lượt 001 chạy bản hàm cũ, giữ'},
]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def liet_ke():
    out = []
    for p in sorted(GOC.rglob('*')):
        if p.is_file() and p != MANIFEST:
            out.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size})
    return out


def kiem_dong_bang():
    return [{'path': f'results/T-043/{rel}', 'sha256_LOG_phien7': exp, 'sha256_hien_tai': sha(GOC / rel), 'khop': sha(GOC / rel) == exp}
            for rel, exp in DONG_BANG_PHIEN7.items()]


def tao():
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    db = kiem_dong_bang()
    if not all(x['khop'] for x in db):
        raise SystemExit('Hash đóng băng phiên 7 lệch: ' + json.dumps([x for x in db if not x['khop']], ensure_ascii=False))
    for l in LUOT:
        if not (GOC / l['duong_dan']).exists():
            raise SystemExit(f'Thiếu lượt: {l["duong_dan"]}')
    m = {
        'schema': 'T043-manifest-v1',
        'task': 'T-043',
        'generated_at': datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds'),
        'root': 'D:/RCA-flashticket',
        'git_head': head,
        'authorization': {'record': 'docs/DECISIONS.md Q-206, Q-207, Q-208, Q-209',
                          'pham_vi': 'Q-206: results/T-043/ theo SPEC; nối tasks/T-043-thiet-ke-rca-m1/LOG.md; dòng T-043 trong docs/STATE.md; một dòng DECISIONS (Q-206). Q-207: gói ghi phiên 9. Phiên 10: dinh-chinh-phien10.md (Đ15–Đ22), why-de-xuat.md, bao-cao.md, the-doc/prism.md, the-doc/crisp.md, fixture B8 và kiem-bo-sung-002, manifest'},
        'trang_thai': 'xong phạm vi SPEC; đã qua ba lượt Codex kiểm kết quả; gói sửa phiên 9 theo Q-207 (dinh-chinh-phien9.md) đã ghi; sửa R1–R4 và F1–F3 phiên 10 (dinh-chinh-phien10.md Đ15–Đ22) đã ghi; đã nghiệm thu trong phạm vi thiết kế (Q-209)',
        'outputs': liet_ke(),
        'dong_bang_phien7': db,
        'luat_F': {
            'v1': {'dinh_nghia': 'dac-ta-phuong-phap-v1.md §2.2 điểm 2 và hop-dong.json#/quan_sat (đóng băng); code lấy bao của mọi bản ghi',
                   'luot': ['ks16/runs/pha1-001', 'ks16/runs/pha2-001'],
                   'ban_chot': ['ks16/dem-khong-nhan.json', 'ks16/dem-sau-ghep-nhan.json']},
            'v1_1': {'dinh_nghia': 'dinh-chinh-phien8.md Đ1 (đề xuất phiên 8; không dùng theo Q-207): hợp các khoảng của từng file, khe dương ngoài F',
                     'luot': ['ks16/runs/thu-nhanh-002', 'ks16/runs/pha1-002', 'ks16/runs/pha2-002'],
                     'so_sanh': 'runs/so-v1-v11-004/ket-qua.json'},
            'a_Q207': {'dinh_nghia': 'dinh-chinh-phien9.md Đ9 (Q-207): F là bao các file; khe dương giữa hai file là OPEN; T^chắc lấy theo v1.1, T^max theo v1; mép ngoài là giả định chưa kiểm',
                       'luot': ['runs/khe-open-002'], 'luot_hong': ['runs/khe-open-001']},
        },
        'luot_chay': LUOT,
        'mutable_governance_links_not_hashed': ['tasks/T-043-thiet-ke-rca-m1/LOG.md', 'docs/STATE.md', 'docs/DECISIONS.md'],
        'self_hash': None,
        'runtime': {
            'python': 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe (Python 3.12.10, numpy 1.26.4, scipy 1.14.1, pandas 2.2.3, psutil 6.1.1)',
            'parquet': 'pyarrow 18.1.0 từ D:/RCA-ext/envs/T-014-main/Lib/site-packages (ks16_pha1*.py tự thêm khi thiếu)',
            'phep_doc_nhe': 'py -3 -B (Python 3.12, chỉ thư viện chuẩn)',
            'co': '-B; PYTHONHASHSEED=0 cho lượt KS-16 và so sánh; PYTHONIOENCODING=utf-8',
        },
        'manifest_note': 'Chỉ đầu ra trong results/T-043 là đối tượng bất biến. Manifest không tự băm. Sau mọi sửa được duyệt, tạo lại và kiểm lại manifest.',
    }
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'so_file': len(m['outputs']), 'tong_bytes': sum(x['bytes'] for x in m['outputs']), 'so_luot': len(LUOT),
                      'dong_bang_khop': sum(x['khop'] for x in db)}, ensure_ascii=False))


def kiem():
    m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    ghi = {x['path']: x for x in m['outputs']}
    that = {x['path']: x for x in liet_ke()}
    thieu = sorted(set(ghi) - set(that))
    thua = sorted(set(that) - set(ghi))
    lech = sorted(p for p in set(ghi) & set(that) if (ghi[p]['sha256'], ghi[p]['bytes']) != (that[p]['sha256'], that[p]['bytes']))
    db = kiem_dong_bang()
    luot_thieu = [l['duong_dan'] for l in m['luot_chay'] if not (GOC / l['duong_dan']).exists()]
    kq = {'so_file_manifest': len(ghi), 'so_file_that': len(that), 'thieu': thieu, 'thua': thua, 'lech': lech,
          'dong_bang_phien7_khop': f"{sum(x['khop'] for x in db)}/{len(db)}", 'luot_thieu': luot_thieu,
          'PASS': not (thieu or thua or lech or luot_thieu) and all(x['khop'] for x in db)}
    print(json.dumps(kq, ensure_ascii=False))
    sys.exit(0 if kq['PASS'] else 1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--tao', action='store_true')
    g.add_argument('--kiem', action='store_true')
    a = ap.parse_args()
    tao() if a.tao else kiem()
