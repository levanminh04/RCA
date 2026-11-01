"""T-045 D2 (SPEC T-045 bước 6, trước luật C; đọc nhãn): dùng `src/m1_danh_gia` tính lại MRR và số ca có cờ M5 của sáu
baseline từ bản ghi P3 đã đóng băng, G_N lấy từ `call_rows` của KS-16 (cạnh a → b, a ≠ b, n_N > 0;
`dinh-nghia-pha2.json#/do_thi_quan_sat/G_N`), rồi so với `results/T-034/bang-baseline.json#/ranking_mode_a` và
`results/T-043/ks16/dem-sau-ghep-nhan.json#/hinh_dang_xep_hang_baseline`.

- Đầu vào kiểm hash như `results/T-043/ks16/ks16_pha2_v11.py` (HASH), và sha256 từng bản ghi P3 theo chỉ mục.
- RR theo ca: `rr.rr_ca` (phân số chính xác) trên khối `p3.danh_gia.khoi_tu_ban_ghi`; ca nhiều seed (TORAI B) lấy trung
  bình các seed, như KS-16 và bảng G2. MRR = trung bình trên ca.
- Cờ M5 theo hai quy tắc, để tách nguồn lệch nếu có: `m5.co_M5` của M1 (khối khác có khóa lớn hơn, hoặc cùng khối và
  nhóm đứng trước; PII-08) và quy tắc của KS-16 (chỉ so khóa khối). Ca có cờ khi ít nhất một seed có cờ.
Chạy: $PY -B results/T-045/scripts/d2_baseline.py --ra results/T-045/tai-lap-baseline.json
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1_danh_gia import m5, rr  # noqa: E402
from p3 import danh_gia  # noqa: E402

HASH = {  # results/T-043/ks16/ks16_pha2_v11.py:33–43
    'results/T-022/nhan-dev.json': '34846de381e8863b882a49661b02a8a0f8efee6f13103985166199a0d127d269',
    'results/T-026/nhan-dev.json': '5127993d0b2016d961ba3382ec8bd353602872a11fcbc4e51c3ae1ecc73c46f4',
    'results/T-024/ban-ghi-dua-vao-cham.json': '2d8a11fa8beb83e07989d89f08fc604dff9bd85d1856acc707326a52e9f2e285',
    'results/T-026/ban-ghi-dua-vao-cham.json': 'c2926067fbbc9c227c735a5d22a44b849c7bcfd44fa7de57d249aeef486511d6',
    'results/T-034/bang-baseline.json': 'e5c6b015a5df8f37a9fffffef869a46cd1b84ce',
    'results/T-043/dinh-nghia-pha2.json': '7521100b56ac75993735efcd1369b5cb7919b30844da0f469d7c67418abc5e3d',
}
TEN_G2 = {'RE2-TT': {('baro', 'native'): 'baro', ('simplerca', 'native'): 'simplerca', ('microrank', 'full'): 'microrank_full',
                     ('tracerca', 'native'): 'tracerca', ('circa', 'ols+rht_da'): 'circa_ols_da', ('torai', 'B'): 'torai_B'},
          'Nezha-OB': {('baro', 'native'): 'baro', ('simplerca', 'M4'): 'simplerca', ('microrank', 'full'): 'microrank_full',
                       ('tracerca', 'finite'): 'tracerca', ('circa', 'ols+rht_da'): 'circa_ols_da', ('torai', 'B'): 'torai_B'}}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def doc(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def M5_ks16(blocks, root, G_N):
    key_of = {e: b['key'] for b in blocks for g in b['groups'] for e in g}
    if root not in key_of:
        return False
    anc = m5._toi({(a, b) for a, b in G_N if a != b}, root) - {root}
    return any(e in key_of and key_of[e] > key_of[root] for e in anc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    kiem = {}
    for rel, exp in HASH.items():
        got = sha(ROOT / rel)
        kiem[rel] = got.startswith(exp)
        if not kiem[rel]:
            raise SystemExit(f'HASH LỆCH: {rel}')
    dn = doc('results/T-043/dinh-nghia-pha2.json')
    labs = {}
    for ds, rel in (('RE2-TT', 'results/T-022/nhan-dev.json'), ('Nezha-OB', 'results/T-026/nhan-dev.json')):
        for c in doc(rel)['cases']:
            labs[c['opaque_id']] = {'root': c['root'], 'dataset': ds}
    ks = doc('results/T-043/ks16/dem-khong-nhan.json')
    G_N = {c['opaque_id']: {(r[0], r[1]) for r in c['call_rows'] if r[0] != r[1] and r[2] > 0} for c in ks['cases']}
    recs = {}
    chon24 = {tuple(x) for x in dn['ban_ghi_baseline']['RE2-TT']['chon']}
    for r in doc('results/T-024/ban-ghi-dua-vao-cham.json')['records']:
        if (r['method'], r['variant']) in chon24:
            recs.setdefault(('RE2-TT', r['method'], r['variant']), []).append(r)
    for r in doc('results/T-026/ban-ghi-dua-vao-cham.json')['unique_records']:
        if r['source_view'] == 'main':
            recs.setdefault(('Nezha-OB', r['method'], r['variant']), []).append(r)
    bb = doc('results/T-034/bang-baseline.json')['ranking_mode_a']
    g2 = {'RE2-TT': bb['RE2-TT_dev30']['methods'], 'Nezha-OB': bb['Nezha-OB_main']['methods']}
    hinh = doc('results/T-043/ks16/dem-sau-ghep-nhan.json')['hinh_dang_xep_hang_baseline']
    out = {'kiem_hash': kiem, 'phuong_phap': {}, 'lech_hash': []}
    for ds, ten in TEN_G2.items():
        for (m, v), ten_g2 in ten.items():
            theo_ca = {}
            for r in recs.get((ds, m, v), []):
                p = ROOT / r['path']
                if sha(p) != r['sha256']:
                    out['lech_hash'].append(r['path'])
                    continue
                rec = json.loads(p.read_text(encoding='utf-8'))
                root = labs[r['opaque_id']]['root']
                ok = rec.get('status') == 'OK'
                blocks = danh_gia.khoi_tu_ban_ghi(rec) if ok else []
                gn = G_N[r['opaque_id']]
                theo_ca.setdefault(r['opaque_id'], []).append(
                    {'RR': rr.rr_ca(blocks, root, ok), 'M5_m1': bool(ok and m5.co_M5(blocks, root, gn)),
                     'M5_ks16': bool(ok and M5_ks16(blocks, root, gn))})
            rr_ca = {o: sum((x['RR'] for x in xs), Fraction(0)) / len(xs) for o, xs in theo_ca.items()}
            mrr = sum(rr_ca.values(), Fraction(0)) / len(rr_ca) if rr_ca else None
            ca_m5 = sum(1 for xs in theo_ca.values() if any(x['M5_m1'] for x in xs))
            ca_m5_ks = sum(1 for xs in theo_ca.values() if any(x['M5_ks16'] for x in xs))
            h = hinh[ds][f'{m}/{v}']
            mrr_g2 = g2[ds][ten_g2]['mrr']
            out['phuong_phap'][f'{ds}|{m}/{v}'] = {
                'so_ca': len(rr_ca), 'so_ban_ghi': sum(len(x) for x in theo_ca.values()),
                'MRR': {'phan_so': [mrr.numerator, mrr.denominator]} if mrr is not None else None,
                'MRR_so': float(mrr) if mrr is not None else None, 'MRR_bang_G2': mrr_g2,
                'MRR_khop_G2': mrr is not None and abs(float(mrr) - mrr_g2) < 1e-9,
                'MRR_KS16': h['mrr'], 'MRR_khop_KS16': mrr is not None and abs(float(mrr) - h['mrr']) < 1e-9,
                'ca_M5_m1': ca_m5, 'ca_M5_quy_tac_KS16': ca_m5_ks, 'ca_M5_KS16': h['ca_M5'],
                'M5_khop_KS16': ca_m5 == h['ca_M5'], 'M5_quy_tac_KS16_khop': ca_m5_ks == h['ca_M5']}
    pp = out['phuong_phap'].values()
    out['tong_hop'] = {'so_phuong_phap': len(out['phuong_phap']), 'MRR_khop_G2': sum(x['MRR_khop_G2'] for x in pp),
                       'MRR_khop_KS16': sum(x['MRR_khop_KS16'] for x in pp), 'M5_khop_KS16': sum(x['M5_khop_KS16'] for x in pp),
                       'M5_quy_tac_KS16_khop': sum(x['M5_quy_tac_KS16_khop'] for x in pp), 'lech_hash': len(out['lech_hash'])}
    out['dat'] = (out['tong_hop']['MRR_khop_G2'] == len(out['phuong_phap']) and not out['lech_hash']
                  and out['tong_hop']['M5_khop_KS16'] == len(out['phuong_phap']))
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(out['tong_hop'], ensure_ascii=False), 'dat', out['dat'])
    for k, x in out['phuong_phap'].items():
        print(k, round(x['MRR_so'], 4), x['MRR_bang_G2'], x['MRR_khop_G2'], 'M5', x['ca_M5_m1'], x['ca_M5_quy_tac_KS16'], x['ca_M5_KS16'])


if __name__ == '__main__':
    main()
