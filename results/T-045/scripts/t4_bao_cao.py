"""T-045 bước 4 — T4, T4b (chỉ báo cáo; SPEC T-045 bước 4; SPEC T-043 B4 T4, T4b; Q5). Đọc nhãn: chạy sau khi hash
pha 1 đã ghi ở LOG. Dùng `m1_danh_gia.pha2.cham` trên từng phần cấu hình (`tach_cau_hinh.py`).

T4: 9 cấu hình ε ∈ {0; 0,05; 0,2} × α ∈ {0,001; 0,01; 0,05} trên 52 ca; MRR theo dataset và gộp; chênh so với R0
(`T4-e0.05-a0.01`, cùng mã nội dung với R0); số ca Hit@1 hỏng/sửa so với R0. Mốc giả RE2-TT (Q-c, Minh duyệt
01/11/2026): tỷ lệ `CAUSE_FOUND` tuyệt đối và số kênh có cờ theo nhóm đơn vị, từng cấu hình.
T4c: thứ tự thứ hai trong bản ghi R0 (`extra.T4c.blocks`, CĐ7) so với thứ tự R0.
T4b: nhánh z (`T4b-z`) so với R0; vế (1) của Q5: điểm từng kênh của E4 hữu hạn và thuộc [0; 1] (bản ghi R0, T4, khối K);
điểm z được dùng hữu hạn, không áp [0; 1]; phân bố điểm z. Vế (2): ΔMRR, ca được sửa, ca đúng bị hỏng (chỉ mô tả).
Chạy: $PY -B results/T-045/scripts/t4_bao_cao.py --ra-t4 results/T-045/t4.json --ra-t4b results/T-045/t4b.json
"""
import argparse
import collections
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1_danh_gia import pha2, rr  # noqa: E402
import pha2_khoi_k as pk  # noqa: E402

RUNS = ROOT / 'results/T-045/runs'
R0 = 'T4-e0.05-a0.01'


def f(x):
    return None if x is None else float(x)


def cham_tach(Ls, nhan):
    out = {}
    for L in Ls:
        for cid, x in pk.cham_luot(L, nhan).items():
            out.setdefault(cid, {'ca': {}})['ca'].update(x['ca'])
    return out


def cham_mot(Ls, nhan):
    out = {}
    for L in Ls:
        meta = json.loads((RUNS / L / 'pha1.json').read_text(encoding='utf-8'))
        for cid, x in pha2.cham(RUNS / L, meta['sha256'], nhan)['cau_hinh'].items():
            out.setdefault(cid, {'ca': {}})['ca'].update(x['ca'])
    return out


def mrr(ca, w='P'):
    r = {o: c['theo_the_gioi'][w]['RR'] for o, c in ca.items()}
    out = {'gop': f(rr.mrr(r))}
    for d in ('RE2-TT', 'Nezha-OB'):
        s = {o for o, c in ca.items() if c['dataset'] == d}
        if s:
            out[d] = f(rr.mrr(r, s))
    return out


def so_voi(ca, ca0):
    hong = sum(1 for o in ca if ca0[o]['theo_the_gioi']['P']['hit1'] == 1 and ca[o]['theo_the_gioi']['P']['hit1'] < 1)
    sua = sum(1 for o in ca if ca0[o]['theo_the_gioi']['P']['hit1'] < 1 and ca[o]['theo_the_gioi']['P']['hit1'] == 1)
    tang = sum(1 for o in ca if ca[o]['theo_the_gioi']['P']['RR'] > ca0[o]['theo_the_gioi']['P']['RR'])
    giam = sum(1 for o in ca if ca[o]['theo_the_gioi']['P']['RR'] < ca0[o]['theo_the_gioi']['P']['RR'])
    return {'hit1_hong': hong, 'hit1_sua': sua, 'RR_tang': tang, 'RR_giam': giam}


def quet_diem(L, chi_cfg=None):
    """Điểm kênh có cờ ở P (extra.kenh_co), theo dòng."""
    out = []
    with open(RUNS / L / json.loads((RUNS / L / 'pha1.json').read_text(encoding='utf-8'))['tep'], encoding='utf-8') as fh:
        for x in fh:
            if x.strip():
                r = json.loads(x)
                if chi_cfg is None or r['config_id'] in chi_cfg:
                    out += [k['s'] for k in r['extra']['kenh_co']]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra-t4', required=True)
    ap.add_argument('--ra-t4b', required=True)
    a = ap.parse_args()
    nhan = pk.nap_nhan(False)
    # T4
    t4 = cham_tach(['b4-t4-re2-001', 'b4-t4-nezha-001'], nhan)
    t4mg = cham_tach(['b4-t4-re2-mocgia-001'], nhan)
    ca0 = t4[R0]['ca']
    kq4 = {'tham_chieu_R0': R0, 'cau_hinh': {}}
    for cid in sorted(t4):
        m = mrr(t4[cid]['ca'])
        m0 = mrr(ca0)
        vd = collections.Counter(c['verdict'] for c in t4mg[cid]['ca'].values())
        n = sum(v for k, v in vd.items() if k not in ('INSUFFICIENT_EVIDENCE', None))
        kq4['cau_hinh'][cid] = {'MRR_P': m, 'chenh_so_R0': {k: m[k] - m0[k] for k in m}, 'so_voi_R0': so_voi(t4[cid]['ca'], ca0),
                                'moc_gia': {'verdict': dict(vd), 'mau_so': n,
                                            'ti_le_CAUSE_FOUND': vd.get('CAUSE_FOUND', 0) / n if n else None}}
    # kênh có cờ ở mốc giả theo nhóm đơn vị, từng cấu hình (không cần nhãn)
    nhom = collections.defaultdict(collections.Counter)
    with open(RUNS / 'b4-t4-re2-mocgia-001' / 'ban-ghi.jsonl', encoding='utf-8') as fh:
        for x in fh:
            if x.strip():
                r = json.loads(x)
                for k in r['extra']['kenh_co']:
                    nhom[r['config_id']][k['don_vi'].split('|', 1)[0]] += 1
                nhom[r['config_id']]['thuc_the_tang_1'] += sum(1 for v in r['extra']['tang_P'].values() if v == 1)
    for cid, c in nhom.items():
        kq4['cau_hinh'][cid]['moc_gia']['kenh_co_theo_nhom'] = dict(c)
    # T4c (thứ tự thứ hai trên bản ghi R0 của T1 seed 0)
    t4c = {'ca': {}}
    for L in ('b2-t1-re2-seed0-001', 'b2-t1-nezha-seed0-001'):
        with open(RUNS / L / 'ban-ghi.jsonl', encoding='utf-8') as fh:
            for x in fh:
                if x.strip():
                    r = json.loads(x)
                    o = r['opaque_id']
                    root = nhan[o]['root']
                    ok = r['status'] == 'OK'
                    t4c['ca'][o] = {'dataset': nhan[o]['dataset'],
                                    'RR_R0': rr.rr_ca(r['blocks'] or [], root, ok),
                                    'RR_T4c': rr.rr_ca((r['extra'].get('T4c') or {}).get('blocks') or [], root, ok)}
    for k in ('RR_R0', 'RR_T4c'):
        t4c[f'MRR_{k[3:]}'] = {'gop': f(sum((c[k] for c in t4c['ca'].values()), Fraction(0)) / len(t4c['ca'])),
                               **{d: f(sum((c[k] for c in t4c['ca'].values() if c['dataset'] == d), Fraction(0))
                                       / sum(1 for c in t4c['ca'].values() if c['dataset'] == d)) for d in ('RE2-TT', 'Nezha-OB')}}
    t4c['RR_tang'] = sum(1 for c in t4c['ca'].values() if c['RR_T4c'] > c['RR_R0'])
    t4c['RR_giam'] = sum(1 for c in t4c['ca'].values() if c['RR_T4c'] < c['RR_R0'])
    t4c['ca'] = {o: {k: (f(v) if isinstance(v, Fraction) else v) for k, v in c.items()} for o, c in t4c['ca'].items()}
    kq4['T4c'] = t4c
    Path(a.ra_t4).write_text(json.dumps(pha2.ma_hoa_json(kq4), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    # T4b
    z = cham_mot(['b4-t4b-re2-001', 'b4-t4b-nezha-001'], nhan)['T4b-z']['ca']
    diem_E4 = []
    for L, cfg in (('b2-t1-re2-seed0-001', None), ('b2-t1-nezha-seed0-001', None), ('b4-t4-re2-001', None),
                   ('b4-t4-nezha-001', None), ('b2b-k16-re2-001', None), ('b5-k16-nezha-001', None)):
        s = quet_diem(L, cfg)
        diem_E4.append({'luot': L, 'so_kenh': len(s), 'khong_huu_han': sum(1 for v in s if not math.isfinite(v)),
                        'ngoai_0_1': sum(1 for v in s if not (0 <= v <= 1)), 'nho_nhat': min(s, default=None),
                        'lon_nhat': max(s, default=None)})
    sz = quet_diem('b4-t4b-re2-001') + quet_diem('b4-t4b-nezha-001')
    sz_sap = sorted(sz)
    q = lambda p: sz_sap[min(len(sz_sap) - 1, int(p * (len(sz_sap) - 1)))] if sz_sap else None  # noqa: E731
    kq4b = {'MRR_z': mrr(z), 'MRR_R0': mrr(ca0), 'so_voi_R0': so_voi(z, ca0),
            'Q5_ve1_E4': {'dat': all(x['khong_huu_han'] == 0 and x['ngoai_0_1'] == 0 for x in diem_E4), 'luot': diem_E4},
            'Q5_ve1_z': {'so_kenh': len(sz), 'khong_huu_han': sum(1 for v in sz if not math.isfinite(v)),
                         'dat': all(math.isfinite(v) for v in sz)},
            'phan_bo_z': {'p50': q(0.5), 'p90': q(0.9), 'p99': q(0.99), 'lon_nhat': sz_sap[-1] if sz_sap else None,
                          'tren_1': sum(1 for v in sz if v > 1), 'tren_10': sum(1 for v in sz if v > 10),
                          'tren_100': sum(1 for v in sz if v > 100), 'tren_1000': sum(1 for v in sz if v > 1000),
                          'tren_1e6': sum(1 for v in sz if v > 1e6)},
            'T4c_dan': 'xem t4.json#/T4c (T4b dẫn kết quả T4c của T4, không chạy lại)'}
    Path(a.ra_t4b).write_text(json.dumps(pha2.ma_hoa_json(kq4b), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'T4': {c: (round(v['MRR_P']['gop'], 4), v['moc_gia']['ti_le_CAUSE_FOUND']) for c, v in kq4['cau_hinh'].items()},
                      'T4c': {k: v for k, v in t4c.items() if k != 'ca'},
                      'T4b': {k: v for k, v in kq4b.items() if k in ('MRR_z', 'MRR_R0', 'so_voi_R0', 'phan_bo_z')},
                      'Q5_ve1': (kq4b['Q5_ve1_E4']['dat'], kq4b['Q5_ve1_z']['dat'])}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
