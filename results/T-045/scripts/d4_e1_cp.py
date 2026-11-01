"""T-045 D4 (không nhãn, chỉ mô tả; LOG phiên 1, Đ-10): trên Nezha-OB, mô tả u_CP − u_U của các span cha có con
chồng lấn hơn 1 ms. u_U, u_CP lấy từ `m1.span.chuan_bi` (đúng mẫu E1-U, E1-CP của chuỗi; quy tắc E1-CP ở T-044 C5,
S32). Cha chọn theo định nghĩa chồng lấn của KS-16 (`dem-khong-nhan.json#/dinh_nghia/chong_lan`; code
`results/T-043/ks16/ks16_pha1_v11.py:150–167`): con cắt về [s_p, e_p), sắp theo start; con chồng lấn khi
min(e_i, max e của anh em trước) − s_i > 1 ms. Kiểm tổng số cha bằng `#/cases/*/trace/parents_with_overlap`.
Không đổi ma trận; K-b vẫn không chạy E1-CP.
Chạy: $PY -B results/T-045/scripts/d4_e1_cp.py --ra results/T-045/e1-cp.json
"""
import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1 import adapter, span  # noqa: E402
from p3 import nezha  # noqa: E402

US = 10 ** 6
TOL_US = 1000


def cha_chong_lan(prep):
    """Khóa span cha có con chồng lấn theo định nghĩa KS-16."""
    sp = prep['spans']
    out = []
    for k, s in sp.items():
        if len(s['con']) < 2:
            continue
        con = []
        for c in s['con']:
            a, b = max(sp[c]['start'], s['start']), min(sp[c]['end'], s['end'])
            if b > a:
                con.append((a, b))
        con.sort(key=lambda x: x[0])  # mergesort ổn định theo cs, như KS-16
        mx = None
        co = False
        for a, b in con:
            if mx is not None and min(b, mx) - a > TOL_US:
                co = True
                break
            mx = b if mx is None else max(mx, b)
        if co:
            out.append(k)
    return out


def qtl(x, q):
    if not x:
        return None
    x = sorted(x)
    i = (len(x) - 1) * q
    lo = int(i)
    hi = min(lo + 1, len(x) - 1)
    return x[lo] + (x[hi] - x[lo]) * (i - lo)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    t0 = time.time()
    hd = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
    ks = {c['opaque_id']: c for c in json.loads((ROOT / 'results/T-043/ks16/dem-khong-nhan.json')
                                               .read_text(encoding='utf-8'))['cases']}
    al = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    kq = {'ca': {}, 'nguon': 'm1.span.chuan_bi (u, u_CP); cha theo định nghĩa chồng lấn KS-16'}
    tat_ca_hieu, tat_ca_ti_le = [], []
    for oid in sorted(al):
        ca = adapter.ca_nezha(al, oid, ROOT, hd)
        t = ca['t']
        lo, hi = (t - 300) * US, (t + 300) * US
        rows = [r for r in ca['spans'] if r['start_us'] >= lo and r['start_us'] + r['duration_us'] < hi]
        prep = span.chuan_bi(rows, t=t * US, tau=TOL_US)
        ds = cha_chong_lan(prep)
        sp = prep['spans']
        hieu = [sp[k]['u_CP'] - sp[k]['u'] for k in ds]
        ti_le = [(sp[k]['u_CP'] - sp[k]['u']) / sp[k]['d'] for k in ds if sp[k]['d'] > 0]
        tat_ca_hieu += hieu
        tat_ca_ti_le += ti_le
        kq['ca'][oid] = {
            'so_cha_chong_lan': len(ds), 'KS16_parents_with_overlap': ks[oid]['trace']['parents_with_overlap'],
            'khop_KS16': len(ds) == ks[oid]['trace']['parents_with_overlap'],
            'so_cha_boc': sum(1 for k in ds if sp[k]['boc']),
            'hieu_us': {'n': len(hieu), 'bang_0': sum(1 for x in hieu if x == 0), 'duong': sum(1 for x in hieu if x > 0),
                        'am': sum(1 for x in hieu if x < 0), 'trung_vi': qtl(hieu, 0.5), 'max': max(hieu, default=None),
                        'tren_1ms': sum(1 for x in hieu if x > 1000)},
            'theo_thao_tac': sorted({(sp[k]['chu'], sp[k]['op']) for k in ds}),
            'phia': {'N': sum(1 for k in ds if sp[k]['phia'] == 'N'), 'A': sum(1 for k in ds if sp[k]['phia'] == 'A')}}
        print(oid, len(ds), ks[oid]['trace']['parents_with_overlap'], flush=True)
    kq['tong_hop'] = {
        'so_cha': len(tat_ca_hieu), 'KS16_tong': sum(c['KS16_parents_with_overlap'] for c in kq['ca'].values()),
        'so_ca_khop_KS16': sum(1 for c in kq['ca'].values() if c['khop_KS16']), 'so_ca': len(kq['ca']),
        'hieu_us': {'bang_0': sum(1 for x in tat_ca_hieu if x == 0), 'duong': sum(1 for x in tat_ca_hieu if x > 0),
                    'am': sum(1 for x in tat_ca_hieu if x < 0), 'p10': qtl(tat_ca_hieu, 0.1), 'p50': qtl(tat_ca_hieu, 0.5),
                    'p90': qtl(tat_ca_hieu, 0.9), 'max': max(tat_ca_hieu, default=None),
                    'trung_binh': statistics.fmean(tat_ca_hieu) if tat_ca_hieu else None,
                    'tren_1ms': sum(1 for x in tat_ca_hieu if x > 1000)},
        'ti_le_tren_d': {'p50': qtl(tat_ca_ti_le, 0.5), 'p90': qtl(tat_ca_ti_le, 0.9), 'max': max(tat_ca_ti_le, default=None)},
        'giay': round(time.time() - t0, 1)}
    Path(a.ra).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(kq['tong_hop'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
