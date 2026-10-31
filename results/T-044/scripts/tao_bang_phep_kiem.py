"""T-044: tổng hợp kết quả từng phép kiểm (biến M1_KET_QUA của tests/conftest.py) thành results/T-044/bang-phep-kiem.json
(SPEC T-044 tiêu chí 2, 3). Lượt đầu (runs/test-xanh-001) dùng cùng đoạn code này chạy trực tiếp trong phiên; từ gói sửa
sau phản biện lượt 1 đoạn code được lưu thành script.

    python -B results/T-044/scripts/tao_bang_phep_kiem.py results/T-044/runs/test-xanh-002/ket-qua.json
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D13 = ['59-59', '61-61', '62-62a', '62-62b', '63-63', '64-64a', '64-64b', '65-65', '66-66', '67-67a', '67-67b',
       '67-67c']
MOD = {'test_k01_hop_dong.py': 'm1.hop_dong',
       'test_k02_quan_sat.py': 'm1.quan_sat, m1.e4, m1.xep_hang, m1_danh_gia.the_gioi, m1.chuoi (H1–H6 qua chuỗi)',
       'test_k03_span.py': 'm1.span', 'test_k04_e4.py': 'm1.e4, m1.xep_hang (T4c)', 'test_k05_kenh.py': 'm1.kenh, m1.e3',
       'test_k06_e1_e2.py': 'm1.span, m1.e2', 'test_k07_e3.py': 'm1.e3, m1.kenh',
       'test_k08_e5_e6_e7_e9.py': 'm1.e5, m1.xep_hang, m1.e7, m1.e9, m1_danh_gia.e7, m1.chuoi',
       'test_k09_chuoi.py': 'm1.chuoi, m1.xep_hang, m1.e7, m1.e5',
       'test_k10_doi_chung.py': 'm1.doi_chung, m1_danh_gia.moc_gia, m1.chuoi',
       'test_k11_danh_gia.py': 'm1_danh_gia.luat_c, chon_khoi, boi_canh, m5, uv6, dau_vet, rr, pha2',
       'test_runner.py': 'm1.runner, m1_danh_gia.pha2', 'test_adapter.py': 'm1.adapter, m1.runner',
       'test_tinh.py': 'kiểm tĩnh src/m1',
       'test_k12_luot4.py': 'm1.e4, m1.xep_hang, m1.chuoi, m1.runner, m1_danh_gia.rr, luat_c, uv6, pha2, chon_khoi (lượt 4)',
       'test_k13_luot5.py': 'm1_danh_gia.chon_khoi, luat_c, rr, uv6, pha2, moc_gia; m1.runner, chuoi, e4, e5, e9, span, '
                            'xep_hang, e3 (lượt 5)',
       'test_k14_luot5b.py': 'm1_danh_gia.chon_khoi, pha2, rr, m5, the_gioi; m1.runner, chuoi, e5 (lượt 5b)',
       'test_k15_luot5c.py': 'm1.xep_hang, chuoi, runner; m1_danh_gia.pha2, rr (lượt 5c)'}


def _ids(ten):
    return [m['id'] for m in json.loads((ROOT / 'results' / 'T-044' / 'fixture' / ten).read_text(encoding='utf-8'))['muc']]


def main(nguon):
    kq = json.loads(Path(nguon).read_text(encoding='utf-8'))
    t043 = json.loads((ROOT / 'results' / 'T-043' / 'fixture' / 'ket-qua-kiem.json').read_text(encoding='utf-8'))
    ids = [str(x['id']) for x in t043['ket_qua']]
    tp, dc, vb = _ids('dap-an-thanh-phan.json'), _ids('dap-an-doi-chung.json'), _ids('dap-an-van-ban.json')

    def nhom(ma):
        if ma in ids:
            return 'T043'
        if re.fullmatch(r'B[1-8]', ma):
            return 'B'
        if re.fullmatch(r'U[1-6]', ma):
            return 'U'
        if re.fullmatch(r'H[1-6]', ma):
            return 'H'
        if re.fullmatch(r'H[1-6]-chuoi', ma):
            return 'H_qua_chuoi'
        for ten, ds in (('tu_lap_thanh_phan', tp), ('tu_lap_doi_chung', dc), ('tu_lap_van_ban', vb)):
            if any(ma == i or ma.startswith(i + '-') for i in ds):
                return ten
        return 'bo_sung_nguoi_lam'

    phep = [{'ma': r['ma'], 'test': r['test'], 'ket_qua': r['ket_qua'], 'nhom': nhom(r['ma']),
             'module': MOD[r['test'].split('::')[0]]} for r in sorted(kq, key=lambda r: r['test'])]
    dem = defaultdict(lambda: [0, 0])
    for p in phep:
        dem[p['nhom']][0] += 1
        dem[p['nhom']][1] += p['ket_qua'] == 'passed'
    pham_vi = [i for i in ids if i not in D13]
    ma_qua = {p['ma'] for p in phep if p['ket_qua'] == 'passed'}
    out = {'schema': 'T044-bang-phep-kiem-v1', 'nguon': str(Path(nguon).resolve().relative_to(ROOT)).replace('\\', '/'),
           'ghi_chu': 'mã phép của fixture T-043 theo results/T-043/fixture/ket-qua-kiem.json#/ket_qua/*/id; phép trong '
                      'phạm vi = 109 − 12 phép của fixture D13 (59, 61–67), ngoại lệ Minh duyệt cùng SPEC',
           'tong': {'so_phep': len(phep), 'qua': sum(p['ket_qua'] == 'passed' for p in phep)},
           'T043': {'so_phep_T043': len(ids), 'pham_vi': len(pham_vi),
                    'qua_trong_pham_vi': sum(i in ma_qua for i in pham_vi), 'loai_tru_D13': D13,
                    'thieu': [i for i in pham_vi if i not in ma_qua]},
           'theo_nhom': {k: {'so_phep': v[0], 'qua': v[1]} for k, v in sorted(dem.items())},
           'dap_an_tu_lap': {'dap-an-thanh-phan.json': len(tp), 'dap-an-doi-chung.json': len(dc),
                             'dap-an-van-ban.json': len(vb), 'dau': 'đáp án của người làm T-044, chưa qua phản biện'},
           'phep': phep}
    (ROOT / 'results' / 'T-044' / 'bang-phep-kiem.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n',
                                                                     encoding='utf-8')
    print(json.dumps({k: out[k] for k in ('tong', 'T043', 'theo_nhom', 'dap_an_tu_lap')}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
