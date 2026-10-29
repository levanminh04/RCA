"""KS-16 pha 2, bản v1.1 (T-043 phiên 8): như ks16_pha2.py, chỉ đổi đầu vào pha 1 sang lượt v1.1 (tham số --pha1, --pha1-sha256).
Định nghĩa ô kích hoạt (dinh-nghia-pha2.json) giữ nguyên và vẫn kiểm hash.

Bản gốc: ghép nhãn SAU khi số đếm không nhãn đã chốt và băm.

Đầu vào (đều kiểm hash trước khi dùng):
- ks16/dem-khong-nhan.json (pha 1, đã băm ở LOG phiên 7);
- dinh-nghia-pha2.json (định nghĩa ô kích hoạt, O1–O4, hình dạng xếp hạng; băm ở LOG trước pha 2);
- nhãn dev: results/T-022/nhan-dev.json (ghim ở results/T-034/bang-baseline.json#/sources),
  results/T-026/nhan-dev.json (ghim ở results/T-026/runs/session-005/handoff-manifest.json);
- bản ghi baseline P3 đã đóng băng (results/T-024, results/T-026 ban-ghi-dua-vao-cham.json; kiểm sha256 từng bản ghi);
- đồ thị tĩnh T-038, T-039 (kiểm ở runs/hash-nguon-003);
- results/T-032/runs/call-interval-001/summary.json (đối chiếu số lời gọi; file có nhãn nên chỉ dùng ở pha 2).
Chạy: python -B results/T-043/ks16/ks16_pha2.py --run results/T-043/ks16/runs/pha2-001
"""
import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
import psutil
from scipy.stats import binom

from p3 import danh_gia

HASH = {
    'results/T-043/dinh-nghia-pha2.json': '7521100b56ac75993735efcd1369b5cb7919b30844da0f469d7c67418abc5e3d',
    'results/T-022/nhan-dev.json': '34846de381e8863b882a49661b02a8a0f8efee6f13103985166199a0d127d269',
    'results/T-026/nhan-dev.json': '5127993d0b2016d961ba3382ec8bd353602872a11fcbc4e51c3ae1ecc73c46f4',
    'results/T-024/ban-ghi-dua-vao-cham.json': '2d8a11fa8beb83e07989d89f08fc604dff9bd85d1856acc707326a52e9f2e285',
    'results/T-026/ban-ghi-dua-vao-cham.json': 'c2926067fbbc9c227c735a5d22a44b849c7bcfd44fa7de57d249aeef486511d6',
    'results/T-038/do-thi/thuc-the.json': 'ee8859de3828429b729f0ae3becab2e0229dd80745f12a98046219a3d164f653',
    'results/T-039/do-thi/thuc-the.json': '593adabc905ff0065a5d87346c19d457451fc8658d28fb8fbecf8bb1465fea04',
    'results/T-032/runs/call-interval-001/summary.json': None,  # lấy hash kỳ vọng từ chuoi-bang-chung.json
    'results/T-034/bang-baseline.json': 'e5c6b015a5df8f37a9fffffef869a46cd1b84ce',  # tiền tố; khớp đủ ở runs/hash-nguon-003
}
M_SPAN = 20
ALPHA = 0.01


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def doc(rel):
    with open(ROOT / rel, encoding='utf-8') as f:
        return json.load(f)


def kiem_hash(pha1, pha1_sha):
    HASH[pha1] = pha1_sha
    cb = doc('results/T-032/chuoi-bang-chung.json')['nguon_da_dung']
    HASH['results/T-032/runs/call-interval-001/summary.json'] = cb['results/T-032/runs/call-interval-001/summary.json']['sha256']
    out = {}
    for rel, exp in HASH.items():
        got = sha(ROOT / rel)
        ok = got.startswith(exp) if len(exp) < 64 else got == exp
        if not ok:
            raise SystemExit(f'HASH LỆCH: {rel}: {got} != {exp}')
        out[rel] = got
    return out


def nhan(path):
    d = doc(path)
    return {c['opaque_id']: {'root': c['root'], 'fault': c['fault'], 'cell': c['cell']} for c in d['cases']}


def do_thi(case):
    gN, gNA = set(), set()
    for a, b, nN, nA, *_ in case['call_rows']:
        if a == b:
            continue
        if nN > 0:
            gN.add((a, b))
        if nN + nA > 0:
            gNA.add((a, b))
    return gN, gNA


def to_tien(edges, root):
    """Các thực thể có đường có hướng tới root theo cạnh gọi."""
    nguoc = {}
    for a, b in edges:
        nguoc.setdefault(b, set()).add(a)
    seen, st = set(), [root]
    while st:
        x = st.pop()
        for p in nguoc.get(x, ()):
            if p not in seen and p != root:
                seen.add(p)
                st.append(p)
    return seen


def thuc_the_co_du_lieu(case):
    ents = set()
    for e, v in case.get('entities', {}).items():
        if v.get('spans_N', 0) + v.get('spans_A', 0) + v.get('log_N', 0) + v.get('log_A', 0) > 0:
            ents.add(e)
    for name, nN, nA in case.get('metric_rows', []):
        if nN + nA > 0:
            ents.add(name.split('_')[0])
    return ents


def kieu_quan_sat(case, root, gNA):
    ent = case.get('entities', {}).get(root, {})
    has_span = ent.get('spans_N', 0) + ent.get('spans_A', 0) > 0
    has_in = any(b == root and a != root for a, b in gNA)
    has_metric = any(name.split('_')[0] == root and nN + nA > 0 for name, nN, nA in case.get('metric_rows', []))
    has_log = ent.get('log_N', 0) + ent.get('log_A', 0) > 0
    if has_span and has_in:
        return 'O1'
    if has_span:
        return 'O2'
    if has_metric or has_log:
        return 'O3'
    return 'O4'


def kich_hoat(case, lab, gN, gNA, tinh, m5_flag):
    root = lab['root']
    out = {}
    calls = [r for r in case['call_rows'] if r[1] == root and r[0] != root]
    out['E1'] = any(r[2] >= M_SPAN and r[3] >= M_SPAN for r in calls)
    out['E1-CP'] = out['E1'] and case['trace']['parents_with_overlap'] > 0
    out['E2'] = any(r[2] >= M_SPAN and r[3] >= M_SPAN and r[6] is not None and r[7] is not None and r[6] > 0
                    and r[7] / r[6] >= 2 for r in calls)
    deg = sum(1 for r in case['edge_rows'] if root in (r[0], r[1]) and r[2] >= M_SPAN and r[3] >= M_SPAN)
    out['E2-VC'] = deg >= 2
    fault = lab['fault']
    out['E3'] = case['dataset'] == 'Nezha-OB' and fault in ('return', 'exception')
    TN, TA = case['quan_sat']['trace']['worlds']['P']
    e3b, e3b_ly_do = False, []
    for r in case['op_rows']:
        if r[0] != root:
            continue
        nN, nA = r[2], r[3]
        if nN == 0 and nA > 0:
            e3b = True
            e3b_ly_do.append(['NEW_OP', r[1], nN, nA])
        elif nN > 0 and nA == 0:
            e3b = True
            e3b_ly_do.append(['STOPPED', r[1], nN, nA])
        elif nN + nA >= 10 and TN > 0 and TA > 0:
            p0 = TA / (TN + TA)
            n = nN + nA
            p_len = float(binom.sf(nA - 1, n, p0))
            p_xuong = float(binom.cdf(nA, n, p0))
            if p_len < ALPHA or p_xuong < ALPHA:
                e3b = True
                e3b_ly_do.append(['TAN_SUAT', r[1], nN, nA, p_len, p_xuong])
    out['E3b'] = e3b
    out['E5'] = m5_flag
    out['E6b'] = any(root in (a, b) for a, b in gNA)
    out['E9'] = any(a == root and b != root for a, b in gNA)
    ents = thuc_the_co_du_lieu(case)
    them = [(a, b) for (a, b) in tinh if a != b and a in ents and b in ents and root in (a, b) and (a, b) not in gNA]
    out['T12'] = bool(them)
    return out, {'E3b': e3b_ly_do[:20], 'T12_canh_them': sorted(them)[:20], 'E2-VC_bac': deg}


def m5_va_hinh_dang(rec, root, gN):
    """Hình dạng xếp hạng một bản ghi và cờ M5 cơ sở tại k = 1."""
    d = danh_gia.cham_ca(rec, root)
    out = {'status': rec['status'], 'rr': d['rr'], 'hit@1': d['hit@1'], 'rank_min': d['rank_min'], 'rank_max': d['rank_max'],
           'root_trong_tra_ve': d['root_trong_tra_ve'], 'n_tra_ve': 0, 'co_nhom_dau': 0, 'root_trong_nhom_dau': False, 'M5': False}
    if rec['status'] != 'OK':
        return out
    blocks = danh_gia.khoi_tu_ban_ghi(rec)
    out['n_tra_ve'] = sum(len(g) for b in blocks for g in b['groups'])
    if blocks:
        k0 = blocks[0]['key']
        dau = [e for b in blocks if b['key'] == k0 for g in b['groups'] for e in g]
        out['co_nhom_dau'] = len(dau)
        out['root_trong_nhom_dau'] = root in dau
    key_of = {e: b['key'] for b in blocks for g in b['groups'] for e in g}
    if root in key_of:
        anc = to_tien(gN, root)
        out['M5'] = any(e in key_of and key_of[e] > key_of[root] for e in anc)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--pha1', required=True)
    ap.add_argument('--pha1-sha256', required=True)
    args = ap.parse_args()
    run = ROOT / args.run
    run.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    hashes = kiem_hash(args.pha1, args.pha1_sha256)
    p1 = doc(args.pha1)
    dn = doc('results/T-043/dinh-nghia-pha2.json')
    labs = {'RE2-TT': nhan('results/T-022/nhan-dev.json'), 'Nezha-OB': nhan('results/T-026/nhan-dev.json')}
    tinh = {}
    for ds, rel in (('RE2-TT', 'results/T-038/do-thi/thuc-the.json'), ('Nezha-OB', 'results/T-039/do-thi/thuc-the.json')):
        tinh[ds] = {(e['source'], e['target']) for e in doc(rel)['edges']}
    # bản ghi baseline
    recs = {'RE2-TT': {}, 'Nezha-OB': {}}
    idx24 = doc('results/T-024/ban-ghi-dua-vao-cham.json')['records']
    chon24 = {tuple(x) for x in dn['ban_ghi_baseline']['RE2-TT']['chon']}
    for r in idx24:
        if (r['method'], r['variant']) in chon24:
            recs['RE2-TT'].setdefault(r['opaque_id'], []).append(r)
    idx26 = doc('results/T-026/ban-ghi-dua-vao-cham.json')['unique_records']
    for r in idx26:
        if r['source_view'] == 'main':
            recs['Nezha-OB'].setdefault(r['opaque_id'], []).append(r)
    loi_hash = []
    per_case, shape_rows = [], []
    for case in p1['cases']:
        ds, oid = case['dataset'], case['opaque_id']
        lab = labs[ds][oid]
        gN, gNA = do_thi(case)
        m5_any = False
        shapes = []
        for r in recs[ds].get(oid, []):
            p = ROOT / r['path']
            if sha(p) != r['sha256']:
                loi_hash.append(r['path'])
                continue
            with open(p, encoding='utf-8') as f:
                rec = json.load(f)
            s = m5_va_hinh_dang(rec, lab['root'], gN)
            s.update({'method': r['method'], 'variant': r['variant'], 'seed': r.get('seed')})
            shapes.append(s)
            m5_any = m5_any or s['M5']
            shape_rows.append(dict(s, dataset=ds, opaque_id=oid, cell=lab['cell']))
        act, ly_do = kich_hoat(case, lab, gN, gNA, tinh[ds], m5_any)
        per_case.append({'dataset': ds, 'opaque_id': oid, 'root': lab['root'], 'fault': lab['fault'], 'cell': lab['cell'],
                         'kich_hoat': act, 'ly_do': ly_do, 'kieu_quan_sat_root': kieu_quan_sat(case, lab['root'], gNA),
                         'baseline': shapes})
    # tổng hợp ô kích hoạt
    comps = ['E1', 'E1-CP', 'E2', 'E2-VC', 'E3', 'E3b', 'E5', 'E6b', 'E9', 'T12']
    cells = {ds: sorted({c['cell'] for c in per_case if c['dataset'] == ds}) for ds in ('RE2-TT', 'Nezha-OB')}
    o_kh = {}
    for comp in comps:
        res = {}
        for ds in ('RE2-TT', 'Nezha-OB'):
            act_cells = sorted({c['cell'] for c in per_case if c['dataset'] == ds and c['kich_hoat'][comp]})
            res[ds] = {'so_o': len(act_cells), 'tren': len(cells[ds]), 'o': act_cells,
                       'so_ca': sum(1 for c in per_case if c['dataset'] == ds and c['kich_hoat'][comp])}
        res['tong_o'] = res['RE2-TT']['so_o'] + res['Nezha-OB']['so_o']
        res['it_ca'] = res['tong_o'] < 6
        o_kh[comp] = res
    # O1–O4
    otype = {ds: {} for ds in ('RE2-TT', 'Nezha-OB')}
    for c in per_case:
        otype[c['dataset']][c['kieu_quan_sat_root']] = otype[c['dataset']].get(c['kieu_quan_sat_root'], 0) + 1
    # hình dạng xếp hạng baseline: MRR theo phương pháp, đối chiếu bảng G2
    bb = doc('results/T-034/bang-baseline.json')['ranking_mode_a']
    ten_g2 = {'RE2-TT': {('baro', 'native'): 'baro', ('simplerca', 'native'): 'simplerca', ('microrank', 'full'): 'microrank_full',
                         ('tracerca', 'native'): 'tracerca', ('circa', 'ols+rht_da'): 'circa_ols_da', ('torai', 'B'): 'torai_B'},
              'Nezha-OB': {('baro', 'native'): 'baro', ('simplerca', 'M4'): 'simplerca', ('microrank', 'full'): 'microrank_full',
                           ('tracerca', 'finite'): 'tracerca', ('circa', 'ols+rht_da'): 'circa_ols_da', ('torai', 'B'): 'torai_B'}}
    bang_g2 = {'RE2-TT': bb['RE2-TT_dev30']['methods'], 'Nezha-OB': bb['Nezha-OB_main']['methods']}
    hinh = {}
    for ds in ('RE2-TT', 'Nezha-OB'):
        hinh[ds] = {}
        for (m, v), g2 in ten_g2[ds].items():
            rows = [s for s in shape_rows if s['dataset'] == ds and s['method'] == m and s['variant'] == v]
            by_case = {}
            for s in rows:
                by_case.setdefault(s['opaque_id'], []).append(s)
            rr = [sum(x['rr'] for x in v_) / len(v_) for v_ in by_case.values()]
            mrr = sum(rr) / len(rr) if rr else None
            hinh[ds][f'{m}/{v}'] = {
                'so_ca': len(by_case), 'so_ban_ghi': len(rows), 'mrr': mrr,
                'mrr_bang_G2': bang_g2[ds][g2]['mrr'], 'khop_G2': (mrr is not None and abs(mrr - bang_g2[ds][g2]['mrr']) < 1e-9),
                'ca_root_chac_hang_1': sum(1 for v_ in by_case.values() if all(x['rank_max'] == 1 for x in v_)),
                'ca_hoa_o_dau': sum(1 for v_ in by_case.values() if any(x['co_nhom_dau'] > 1 for x in v_)),
                'ca_M5': sum(1 for v_ in by_case.values() if any(x['M5'] for x in v_)),
                'ca_khong_OK': sum(1 for v_ in by_case.values() if all(x['status'] != 'OK' for x in v_)),
            }
    # đối chiếu T-032 (số lời gọi)
    t32 = doc('results/T-032/runs/call-interval-001/summary.json')
    p1map = {(c['dataset'], c['opaque_id']): c for c in p1['cases']}
    dc = {'so_ca_so': 0, 'n_khop': 0, 'lech': []}
    for c in t32['cases']:
        if c.get('status') != 'OK':
            continue
        mine = p1map[(c['dataset'], c['opaque_id'])]['trace']['all_calls']
        dc['so_ca_so'] += 1
        ok = True
        for side in ('before', 'after'):
            a, b = c['all_calls'][side], mine[side]
            if a['n'] != b['n']:
                ok = False
            for k in ('nested_share', 'pre_negative_share', 'post_negative_share', 'gap_negative_share', 'median_d_p_us', 'median_d_c_us', 'median_gap_us'):
                if a.get(k) is not None and b.get(k) is not None and abs(a[k] - b[k]) > 1e-9 * max(1.0, abs(a[k])):
                    ok = False
        if ok:
            dc['n_khop'] += 1
        else:
            dc['lech'].append({'dataset': c['dataset'], 'opaque_id': c['opaque_id'],
                               'T032': c['all_calls'], 'T043': mine})
    # đối chiếu nhãn T-022 với nhãn trong call-interval-001 (cùng opaque_id)
    nh = {'so_ca_so': 0, 'khop': 0, 'lech': []}
    for c in t32['cases']:
        mine = labs[c['dataset']].get(c['opaque_id'])
        nh['so_ca_so'] += 1
        if mine and (mine['root'], mine['fault'], mine['cell']) == (c['root'], c['fault'], c['cell']):
            nh['khop'] += 1
        else:
            nh['lech'].append(c['opaque_id'])
    out = {'schema': 'T043-KS16-pha2-v1.1', 'pha1': args.pha1, 'task': 'T-043', 'run': args.run, 'created_utc': datetime.now(timezone.utc).isoformat(),
           'labels_read': True, 'hash_dau_vao': hashes, 'ban_ghi_lech_hash': loi_hash,
           'so_o': {ds: len(v) for ds, v in cells.items()}, 'o_kich_hoat': o_kh, 'kieu_quan_sat_root': otype,
           'hinh_dang_xep_hang_baseline': hinh, 'doi_chieu_T032_loi_goi': dc, 'doi_chieu_nhan_T032': nh,
           'cases': per_case, 'cost': {'giay': round(time.time() - t0, 1), 'rss_bytes': psutil.Process().memory_info().rss}}
    with open(run / 'dem-sau-ghep-nhan.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({'o_kich_hoat': {k: (v['RE2-TT']['so_o'], v['Nezha-OB']['so_o'], v['tong_o'], v['it_ca']) for k, v in o_kh.items()},
                      'O': otype, 'T032': {k: v for k, v in dc.items() if k != 'lech'}, 'nhan': {k: v for k, v in nh.items() if k != 'lech'},
                      'lech_hash': len(loi_hash), 'giay': out['cost']['giay']}, ensure_ascii=False))
    print(json.dumps({ds: {k: (v['mrr'], v['mrr_bang_G2'], v['khop_G2'], v['ca_M5']) for k, v in h.items()} for ds, h in hinh.items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
