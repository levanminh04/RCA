"""Phép đột biến (SPEC T-044 bước 7, tiêu chí 6): mỗi đột biến thay đúng một chỗ trong bản sao tạm của `src/`, chạy
toàn bộ test, ghi số phép trượt. Không sửa repo, không commit đột biến. Lượt đối chứng không đột biến phải xanh.

    python -B results/T-044/scripts/dot_bien.py results/T-044/runs/dot-bien-001
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PY = sys.executable

DOT_BIEN = [
    ('D01-dao-lop-lan', 'src/m1/e5.py', "        if c.lop == 'lan_nguoc':", "        if c.lop == 'lan_xuoi':",
     'E5: đảo quy tắc lan ngược và lan xuôi'),
    ('D02-bo-cat-con-E1', 'src/m1/span.py', "        cat, v = cat_con((s['start'], s['end']), khoang, tau)",
     "        cat, v = list(khoang), 0", 'E1-U: bỏ cắt con về khoảng của cha'),
    ('D03-doi-khoa-hoa', 'src/m1/xep_hang.py', "    return (max(s), len(s), math.fsum(s))",
     "    return (max(s), math.fsum(s), len(s))", 'Khóa K: đổi chỗ số kênh và tổng điểm'),
    ('D04-bo-duyet-list-truong-cam', 'src/m1/hop_dong.py', "    elif isinstance(obj, (list, tuple)):",
     "    elif isinstance(obj, ()):", 'Bộ kiểm trường cấm: không duyệt list, tuple'),
    ('D05-doi-delta-luat-C', 'src/m1_danh_gia/luat_c.py', "DELTA = Fraction(1, 100)", "DELTA = Fraction(2, 100)",
     'Luật C: δ = 0,02 thay 0,01'),
    ('D06-ro-ma-mo-vao-params', 'src/m1/runner.py', "    p['config_id'] = cau_hinh['config_id']",
     "    p['config_id'] = cau_hinh['config_id'] + '@' + ca['opaque_id']", 'Pha 1: đưa mã mờ vào params'),
    ('D07-m1-import-bo-danh-gia', 'src/m1/chuoi.py', "from m1.kieu import Kenh",
     "from m1.kieu import Kenh\nfrom m1_danh_gia import rr as _rr  # noqa: F401", 'src/m1 import bộ đánh giá'),
    ('D08-doc-duong-dan-nhan', 'src/m1/runner.py', "class LoiRoNhan(ValueError):",
     "NHAN = 'results/T-022/nhan-dev.json'\n\n\nclass LoiRoNhan(ValueError):", 'Pha 1 trỏ tới file nhãn'),
    ('D09-bo-tau-CRISP', 'src/m1/span.py', "    if not (c[1] - tau < d[0]):", "    if not (c[1] < d[0]):",
     'E1-CP: bỏ dung sai τ của happensBefore'),
    ('D10-nhom-vong-mac-dinh-ke-canh', 'src/m1/e5.py',
     "def phan_loai(kenh, canh, bat=True, doc_nhom_vong='co_vong',",
     "def phan_loai(kenh, canh, bat=True, doc_nhom_vong='ke_canh',", 'E5: cách đọc nhóm vòng mặc định A thay C′'),
    ('D11-E7-any-thay-all', 'src/m1/e7.py', "                if all((k.thuc_the, k.ten, k.huong) in gt",
     "                if any((k.thuc_the, k.ten, k.huong) in gt", 'E7 cách 1: "mọi kênh có giải thích" thành "một kênh"'),
    ('D12-E9-bien-2-o', 'src/m1/e9.py', "    if all(b - kp_e > 2 * o_s + tau for b in kp_B):",
     "    if all(b - kp_e >= 2 * o_s for b in kp_B):", 'E9: bỏ τ và lấy cả biên đúng 2 ô'),
    ('D13-lambda-dao', 'src/m1/e4.py', "    lam = n_N * T_A / T_N", "    lam = n_N * T_N / T_A",
     'Đơn vị đếm: λ dùng T đảo'),
    ('D14-damping', 'src/m1/xep_hang.py', "DAMPING = 0.85", "DAMPING = 0.80", 'E6b: hệ số tắt dần 0,80'),
    ('D15-bien-cong-chinh-xac', 'src/m1/e4.py', "    if n <= n_exact_max:", "    if n < n_exact_max:",
     'E4: n = 100 chuyển sang xấp xỉ'),
    ('D16-dao-the-gioi', 'src/m1/quan_sat.py', "'S_lo': (Tm['N'], Tc['A']), 'S_hi': (Tc['N'], Tm['A'])",
     "'S_lo': (Tc['N'], Tm['A']), 'S_hi': (Tm['N'], Tc['A'])", 'Ba thế giới: đổi S_lo và S_hi'),
    ('D17-E3-hoan-toan-thanh-nguong', 'src/m1/e3.py',
     "        c = drain.fast_match(trong_la, tokens, 1.0, True) if trong_la else None",
     "        c = drain.fast_match(trong_la, tokens, sim_th, False) if trong_la else None",
     'E3 cách khớp (a): dùng ngưỡng thay khớp hoàn toàn'),
    ('D18-tang-bo-E5', 'src/m1/xep_hang.py',
     "        tang[e] = 1 if K_I[e][1] > 0 else (2 if K_raw[e][1] > 0 else 3)",
     "        tang[e] = 1 if K_raw[e][1] > 0 else 3", 'Tầng: bỏ tầng kế thừa'),
    ('D19-bo-sap-kenh-E5', 'src/m1/e5.py',
     "    co = sorted((k for k in kenh if k.co), key=lambda k: k.ma)  # thứ tự chuẩn: đầu ra không phụ thuộc thứ tự vào",
     "    co = [k for k in kenh if k.co]", 'E5: bỏ thứ tự chuẩn (chỉ lộ khi xáo hàng, chạy với M1_XAO=1)'),
    ('D20-metric-khong-khai-dung-metrics-time', 'src/m1/chuoi.py',
     "            ng = nguon_cua.get(cot)\n", "            ng = nguon_cua.get(cot, 'metric')\n",
     'Chuỗi: cột metric không khai nguồn vẫn được chấm'),
    ('D21-chuoi-mac-dinh-ke-canh', 'src/m1/chuoi.py', "doc_nhom_vong=tham_so_E5.get('doc_nhom_vong', 'co_vong')",
     "doc_nhom_vong=tham_so_E5.get('doc_nhom_vong', 'ke_canh')", 'Chuỗi: thiếu tham_so_E5 thì dùng cách đọc A'),
    # sau phản biện lượt 1 (LOG T-044, mục "Phản hồi phản biện lượt 1 và gói sửa")
    ('D22-luat-C-bo-boi-so-o', 'src/m1_danh_gia/luat_c.py', "        k = boi[o]\n", "        k = 1\n",
     'Luật C: P, M đếm mỗi ô một lần dù ô được lấy k lần'),
    ('D23-M5-bo-boi-so', 'src/m1_danh_gia/pha2.py',
     "            them['M5'] = (sum(_w(trong_so, o) * tat[o]['theo_the_gioi'][w]['M5'] for o in tat),",
     "            them['M5'] = (sum(tat[o]['theo_the_gioi'][w]['M5'] for o in tat),", 'Cờ M5 nhánh tắt: bỏ bội số'),
    ('D24-UV6-bo-boi-so', 'src/m1_danh_gia/uv6.py', "        w = c.get('trong_so', 1)\n", "        w = 1\n",
     'UV-6: bỏ bội số'),
    ('D25-moc-gia-bo-boi-so', 'src/m1_danh_gia/pha2.py', "    n = sum(_w(trong_so, o) for o, _, _ in giu)\n",
     "    n = len(giu)\n", 'Mốc giả: mẫu số không theo bội số'),
    ('D26-bo-coverage-metric', 'src/m1/chuoi.py',
     "                qs[ng_s] = _nguon(ng_s, [m for m in tg[ng_s]['moc'] if lo_ns <= m < hi_ns])\n",
     "                pass\n", 'Chuỗi: không xuất trạng thái quan sát của nguồn metric'),
    ('D27-WD-cap-dau-bang', 'src/m1_danh_gia/the_gioi.py',
     "        vuot = [e for e in chung if _truoc_han(vw[e], vw[root]) and not _truoc_han(vP[e], vP[root])]",
     "        vuot = [e for e in chung if _truoc_han(vw[e], vw[root])]",
     'WORLD_DEPENDENT: lấy mọi thực thể đứng trước root, kể cả thực thể đã đứng trước ở P'),
]
XAO = {'D19-bo-sap-kenh-E5': '1'}


def chay(goc, ra, ma, xao):
    env = dict(os.environ, PYTHONHASHSEED='0', M1_KET_QUA=str(ra / f'{ma}.json'))
    env.pop('M1_XAO', None)
    if xao:
        env['M1_XAO'] = xao
    t0 = time.perf_counter()
    p = subprocess.run([PY, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '-W', 'ignore'],
                       cwd=goc / 'results' / 'T-044' / 'tests', env=env, capture_output=True, text=True, timeout=900)
    (ra / f'{ma}.txt').write_text(p.stdout + p.stderr, encoding='utf-8')
    kq = json.loads((ra / f'{ma}.json').read_text(encoding='utf-8'))
    truot = sorted(r['test'] for r in kq if r['ket_qua'] != 'passed')
    return {'so_phep': len(kq), 'so_truot': len(truot), 'truot': truot, 'exit': p.returncode,
            'giay': round(time.perf_counter() - t0, 2), 'M1_XAO': xao}


def main():
    ra = Path(sys.argv[1]).resolve()
    ra.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        goc = Path(td)
        (goc / 'results').mkdir()
        shutil.copytree(ROOT / 'results' / 'T-043', goc / 'results' / 'T-043',
                        ignore=shutil.ignore_patterns('runs'))
        for d in ('tests', 'fixture'):
            shutil.copytree(ROOT / 'results' / 'T-044' / d, goc / 'results' / 'T-044' / d)
        out = {}
        for ma, tep, cu, moi, mo_ta in [('D00-doi-chung', None, None, None, 'không đột biến')] + DOT_BIEN:
            if (goc / 'src').exists():
                shutil.rmtree(goc / 'src')
            shutil.copytree(ROOT / 'src', goc / 'src', ignore=shutil.ignore_patterns('__pycache__'))
            if tep:
                p = goc / tep
                s = p.read_text(encoding='utf-8')
                if s.count(cu) != 1:
                    raise SystemExit(f'{ma}: chuỗi cũ xuất hiện {s.count(cu)} lần trong {tep}')
                p.write_text(s.replace(cu, moi), encoding='utf-8')
            r = chay(goc, ra, ma, XAO.get(ma))
            r.update({'tep': tep, 'cu': cu, 'moi': moi, 'mo_ta': mo_ta,
                      'bi_bat': (r['so_truot'] > 0) if tep else None})
            out[ma] = r
            print(ma, r['so_truot'], 'trượt /', r['so_phep'], flush=True)
    dc = out['D00-doi-chung']
    tong = {'buoc': 'SPEC T-044 bước 7, tiêu chí 6', 'lenh': 'python -B results/T-044/scripts/dot_bien.py <thư mục>',
            'doi_chung_xanh': dc['so_truot'] == 0, 'so_dot_bien': len(DOT_BIEN),
            'so_bi_bat': sum(1 for k, v in out.items() if v['bi_bat']),
            'song_sot': sorted(k for k, v in out.items() if v['bi_bat'] is False), 'chi_tiet': out}
    (ra / 'tong-hop.json').write_text(json.dumps(tong, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('đối chứng xanh:', tong['doi_chung_xanh'], '| bị bắt:', tong['so_bi_bat'], '/', tong['so_dot_bien'],
          '| sống sót:', tong['song_sot'])


if __name__ == '__main__':
    main()
