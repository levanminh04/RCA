"""Phân tích chỉ đọc cho báo cáo P7(a) main013-v2 (T-054). Không chạy phương pháp, không đọc telemetry test.

Đầu vào:
- reports/main-013-v2/{a4.json, tables.json}: kiểm sha256 theo received-main-002/report-receipt.json.
- result.json của các vế M1-family trong ba queue main-013-v2; mỗi file kiểm sha256/bytes theo verified.json cùng attempt.
Đầu ra: phan-tich-nhom.json cạnh script (tạo mới, không ghi đè).

Chạy: py -3 -B results/T-054/reports/p7a-013-v2/phan_tich.py  (từ gốc repo)
"""
import glob
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
T054 = os.path.join(ROOT, 'results', 'T-054')
RUN = os.path.join(T054, 'runs', 'chuan-bi-main-013-v2')
REP = os.path.join(T054, 'reports', 'main-013-v2')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phan-tich-nhom.json')
if len(sys.argv) > 1:  # chỉ để thử ở thư mục nháp ngoài repo
    OUT = os.path.abspath(sys.argv[1])
QUEUES = {
    'ec2_1': os.path.join(RUN, 'received-main-002', 'ec2_1', 'results', 'T-054', 'runs', 'main-013-v2', 'queue'),
    'ec2_2': os.path.join(RUN, 'received-main-002', 'ec2_2', 'results', 'T-054', 'runs', 'main-013-v2', 'queue'),
    'local': os.path.join(T054, 'runs', 'main-013-v2', 'queue'),
}
M1_ARMS = ('M1', 'C-a0', 'C-a1', 'bo-E1', 'bo-E2', 'bo-E5', 'T12-on')
METRICS = ('rr', 'hit@1', 'hit@3', 'hit@5', 'ndcg@5', 'avg@5')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def frac(pq):
    return Fraction(pq['phan_so'][0], pq['phan_so'][1])


def fs(x):
    """Fraction → [tử, mẫu] cùng số thực để đọc."""
    x = Fraction(x)
    return {'phan_so': [x.numerator, x.denominator], 'xap_xi': float(x)}


# ------------------------------------------------------------------ kiểm đầu vào
receipt_path = os.path.join(RUN, 'received-main-002', 'report-receipt.json')
receipt = json.load(open(receipt_path, encoding='utf-8'))
inputs = {}
for k, name in (('A4', 'a4.json'), ('tables', 'tables.json')):
    p = os.path.join(REP, name)
    h = sha(p)
    if h != receipt[k]['sha256'] or os.path.getsize(p) != receipt[k]['bytes']:
        sys.exit(f'HASH_MISMATCH {name}')
    inputs[rel(p)] = {'sha256': h, 'bytes': os.path.getsize(p), 'checked_against': rel(receipt_path)}
inputs[rel(receipt_path)] = {'sha256': sha(receipt_path), 'bytes': os.path.getsize(receipt_path)}
a4 = json.load(open(os.path.join(REP, 'a4.json'), encoding='utf-8'))
tables = json.load(open(os.path.join(REP, 'tables.json'), encoding='utf-8'))

# ------------------------------------------------------------------ chỉ mục kết quả M1-family đã VERIFIED
results = {}
checked = Counter()
for host, q in QUEUES.items():
    for vf in glob.glob(os.path.join(q, '*', 'attempt-*', 'verified.json')):
        d = os.path.dirname(vf)
        job = json.load(open(os.path.join(d, 'job.json'), encoding='utf-8'))
        if job['kind'] != 'm1':
            continue
        s = job['slot']
        v = json.load(open(vf, encoding='utf-8'))
        rp = os.path.join(d, 'result.json')
        if sha(rp) != v['result']['sha256'] or os.path.getsize(rp) != v['result']['bytes']:
            sys.exit(f'RESULT_HASH_MISMATCH {rp}')
        key = (s['dataset'], s['opaque_id'], s['arm'], s['view'])
        if key in results:
            sys.exit(f'DUPLICATE_VERIFIED {key}')
        results[key] = rp
        checked[(host, s['dataset'], s['arm'], s['view'])] += 1
expect = {(ds, arm, 'main'): n for ds, n in (('RE2-TT', 60), ('Nezha-OB', 34)) for arm in M1_ARMS}
got = Counter()
for (ds, _, arm, view) in results:
    got[(ds, arm, view)] += 1
for k, n in expect.items():
    if got[k] != n:
        sys.exit(f'COUNT_MISMATCH {k} {got[k]} != {n}')

# ------------------------------------------------------------------ hàng chấm tại P
rows = {}
for r in tables['rows']:
    if r['world'] != 'P':
        continue
    rows[(r['dataset'], r['opaque_id'], r['arm'])] = r
cases = defaultdict(dict)
for (ds, oid, arm), r in rows.items():
    cases[ds][oid] = {'cell': r['cell'], 'fault': r['fault'], 'root': r['cell'].split('|')[1]}
ARMS = sorted({a for (_, _, a) in rows})


def rr(ds, oid, arm):
    r = rows.get((ds, oid, arm))
    return None if r is None else frac(r['metrics']['RR'])


def h5(ds, oid, arm):
    r = rows.get((ds, oid, arm))
    return None if r is None else frac(r['metrics']['Hit5_Q'])


# ------------------------------------------------------------------ 1. bảng theo vế
bang = {}
for ds in cases:
    for arm in ARMS:
        rs = [rows[(ds, o, arm)] for o in sorted(cases[ds]) if (ds, o, arm) in rows]
        if not rs:
            continue
        st = Counter(s for r in rs for s in r['statuses'])
        ent = {'n': len(rs), 'auxiliary': any(r.get('auxiliary') for r in rs), 'status_counts': dict(st)}
        ent['MRR'] = fs(sum((frac(r['metrics']['RR']) for r in rs), Fraction(0)) / len(rs))
        ent['Hit5_Q'] = fs(sum((frac(r['metrics']['Hit5_Q']) for r in rs), Fraction(0)) / len(rs))
        for m in METRICS[1:]:
            ent[m] = sum(r['metrics'][m] for r in rs) / len(rs)
        bang[f'{ds}|{arm}'] = ent

# ------------------------------------------------------------------ 2. so cặp theo ca
summ = {(s['dataset'], s['world']): s for s in tables['summaries']}


def ci_cap(ds, a, b):
    """CI bootstrap cặp theo ô trong tables summaries (khóa 'X - Y' theo thứ tự tên), đổi dấu về a − b."""
    h = summ[(ds, 'P')]['bootstrap']['hieu']
    for k, sign in ((f'{a} - {b}', 1), (f'{b} - {a}', -1)):
        if k in h:
            out = {}
            for m in ('rr', 'hit@1', 'hit@5'):
                lo, hi = h[k][m]['lo'], h[k][m]['hi']
                out[m] = {'lo': lo, 'hi': hi} if sign == 1 else {'lo': -hi, 'hi': -lo}
            return {'pointer': f"tables.json#/summaries[dataset={ds},world=P]/bootstrap/hieu/{k}", 'sign': sign,
                    'CI': out}
    return None


def so_cap(ds, a, b, metric='RR'):
    get = rr if metric == 'RR' else h5
    per, by_cell = [], defaultdict(Fraction)
    for o in sorted(cases[ds]):
        x, y = get(ds, o, a), get(ds, o, b)
        if x is None or y is None:
            continue
        d = x - y
        by_cell[cases[ds][o]['cell']] += d
        if d != 0:
            per.append({'opaque_id': o, 'cell': cases[ds][o]['cell'], a: float(x), b: float(y), 'd': float(d)})
    n = sum(1 for o in cases[ds] if get(ds, o, a) is not None and get(ds, o, b) is not None)
    tot = sum((p['d'] for p in per), 0.0)
    exact = sum((get(ds, o, a) - get(ds, o, b) for o in cases[ds]
                 if get(ds, o, a) is not None and get(ds, o, b) is not None), Fraction(0))
    return {'metric': metric, 'n': n, 'delta_mean': fs(exact / n) if n else None,
            'win': sum(p['d'] > 0 for p in per), 'loss': sum(p['d'] < 0 for p in per), 'tie': n - len(per),
            'cells_nonzero': sum(1 for v in by_cell.values() if v != 0),
            'cells_negative': sum(1 for v in by_cell.values() if v < 0),
            'cell_totals_nonzero': {c: float(v) for c, v in sorted(by_cell.items()) if v != 0},
            'cases': per, 'CI_bootstrap_cell': ci_cap(ds, a, b)}


CAPS = {
    'RE2-TT': [('M1', 'torai_B'), ('M1', 'C-a0'), ('M1', 'C-a1'), ('M1', 'bo-E1'), ('M1', 'bo-E2'), ('M1', 'bo-E5'),
               ('M1', 'C-d1'), ('M1', 'C-d2'), ('M1', 'C-d3'), ('M1', 'C-c'), ('M1', 'C-g'), ('M1', 'T12-on'),
               ('M1', 'simplerca'), ('M1', 'baro'), ('C-a0', 'torai_B'), ('C-a1', 'C-a0'), ('C-d2', 'torai_B')],
    'Nezha-OB': [('M1', 'simplerca'), ('M1', 'C-a0'), ('M1', 'C-a1'), ('M1', 'bo-E1'), ('M1', 'bo-E2'),
                 ('M1', 'bo-E5'), ('M1', 'C-d1'), ('M1', 'C-d2'), ('M1', 'C-c'), ('M1', 'C-g'), ('M1', 'T12-on'),
                 ('M1', 'baro'), ('C-a0', 'simplerca'), ('C-a1', 'C-a0')],
}
cap = {}
for ds, ps in CAPS.items():
    for a, b in ps:
        for metric in ('RR', 'Hit5'):
            cap[f'{ds}|{a}-{b}|{metric}'] = so_cap(ds, a, b, metric)

# ------------------------------------------------------------------ 3. trung gian M1-family theo ca
def fam(k):
    p = k['don_vi'].split('|')[0]
    if p == 'op':
        return 'E1_self' if k['lop'] == 'khong_lan' else 'op_full'
    return {'canh': 'E2_edge', 'metric': 'metric', 'log': 'log'}.get(p, p)


def doc(rp, root):
    r = json.load(open(rp, encoding='utf-8'))['records'][0]
    ex = r.get('extra') or {}
    blocks = r['worlds']['P']['blocks']
    tang = ex.get('tang_P', {})
    pos, root_blk, size = 0, None, None
    out_blocks = []
    for i, b in enumerate(blocks):
        g = [e for gg in b['groups'] for e in gg]
        if root in g and root_blk is None:
            root_blk, size, start = i, len(g), pos
        if i < 5:
            out_blocks.append({'entities': g, 'tier': sorted({tang.get(e) for e in g}, key=str), 'key': b['key']})
        pos += len(g)
    ch_all = ex.get('kenh_co', [])
    ch = [k for k in ch_all if k['thuc_the'] == root]
    rr_exp = (sum(Fraction(1, start + j) for j in range(1, size + 1)) / size) if root_blk is not None else Fraction(0)
    inh = [{'kenh': x['kenh'], 'by': x['giai_thich'], 'rule': x['quy_tac'], 'state': x['trang_thai']}
           for x in r.get('inherited_by', []) if x['thuc_the'] == root]
    above = []
    if root_blk is not None:
        for b in blocks[:root_blk]:
            for e in [e for gg in b['groups'] for e in gg]:
                fe = Counter(fam(k) for k in ch_all if k['thuc_the'] == e and k['F_I'] == 1)
                fr = Counter(fam(k) for k in ch_all if k['thuc_the'] == e)
                above.append({'entity': e, 'tier': tang.get(e), 'fam_F_I': dict(fe), 'fam_F_raw': dict(fr),
                              'edge_to_root': [x for x in ex.get('canh', []) if root in x and e in x]})
    smax = max((k['s'] for k in ch_all), default=None)
    return {
        'status': r['status'], 'verdict': r.get('verdict'), 'n_tier1': sum(1 for v in tang.values() if v == 1),
        'root_block': root_blk, 'root_block_size': size, 'root_rr_from_blocks': float(rr_exp),
        'root_tier': tang.get(root), 'root_in_returned': root_blk is not None,
        'root_key_P': (blocks[root_blk]['key'] if root_blk is not None else None),
        'root_channels': [{'fam': fam(k), 'ten': k['ten'], 'lop': k['lop'], 's': k['s'], 'F_I': k['F_I']}
                          for k in sorted(ch, key=lambda k: -k['s'])][:12],
        'root_fam_F_raw': dict(Counter(fam(k) for k in ch)),
        'root_fam_F_I': dict(Counter(fam(k) for k in ch if k['F_I'] == 1)),
        'root_inherited_by': inh[:12], 'n_root_inherited': len(inh),
        'above_root': above[:8], 'n_above_root': len(above), 'top_blocks': out_blocks[:3],
        'scc': [g for g in ex.get('nhom_vong_P', []) if root in g], 'max_s_all_channels': smax,
        'n_edges_observed': len(ex.get('canh', [])), 'E2_fallback': (r.get('diagnostics') or {}).get('E2_du_phong'),
    }


trung_gian = defaultdict(dict)
khop_rr = Counter()
for (ds, oid, arm, view), rp in sorted(results.items()):
    if view != 'main':
        continue
    root = cases[ds][oid]['root']
    t = doc(rp, root)
    t['result'] = rel(rp)
    t['rr_table'] = float(rr(ds, oid, arm))
    ok = abs(t['rr_table'] - t['root_rr_from_blocks']) < 1e-12
    khop_rr[(ds, arm, ok)] += 1
    trung_gian[f'{ds}|{oid}'][arm] = t

# ------------------------------------------------------------------ 4. đổi xếp hạng khi bỏ thành phần (không chỉ RR root)
def top1(ds, oid, arm):
    t = trung_gian[f'{ds}|{oid}'].get(arm)
    return t['top_blocks'][0]['entities'] if t and t['top_blocks'] else None


doi_top = {}
for ds in cases:
    for arm in ('bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'T12-on'):
        doi = [o for o in sorted(cases[ds]) if top1(ds, o, 'M1') != top1(ds, o, arm)]
        doi_rr = [o for o in doi if rr(ds, o, 'M1') != rr(ds, o, arm)]
        doi_top[f'{ds}|M1 vs {arm}'] = {'n_top_block_changed': len(doi), 'n_root_rr_changed': len(doi_rr),
                                        'top_changed_rr_same': [o for o in doi if o not in doi_rr]}

# ------------------------------------------------------------------ 5. hồ sơ nhóm M1 theo tầng root
ho_so = {}
for ds in cases:
    c = Counter()
    for o in cases[ds]:
        t = trung_gian[f'{ds}|{o}']['M1']
        c[(t['root_tier'], t['root_block'] == 0, t['root_block_size'] == 1 if t['root_block'] == 0 else None)] += 1
    ho_so[ds] = {f'tier={k[0]}|root_in_top_block={k[1]}|alone={k[2]}': v for k, v in sorted(c.items(), key=str)}

# ------------------------------------------------------------------ 5b. đối chiếu ca sai/ca đúng của M1 (và C-a0) theo kênh mạnh nhất
# Mỗi kênh có cờ: s = z của E4 (max(A) − trung vị N)/IQR N (src/m1/e4.py:276); độ rộng = r_len_A − r_len_N (tỷ lệ span/mẫu
# trong A vượt ngưỡng trên so với N) lấy từ đơn vị phân vị cùng mã. Đơn vị đếm (log) không có độ rộng này → None.
def kenh_manh(r, ent):
    dv = {u['ma']: u for u in r['extra'].get('don_vi_phan_vi', [])}
    ks = [k for k in r['extra'].get('kenh_co', []) if k['thuc_the'] == ent and k['F_I'] == 1]
    out = []
    for k in ks:
        u = dv.get(k['don_vi'])
        w = (u['r_len_A'] - u['r_len_N']) if u and k['huong'] == 'len' and u.get('r_len_A') is not None else None
        out.append({'fam': fam(k), 'don_vi': k['don_vi'], 's': k['s'], 'do_rong': w,
                    'r_len_A': u.get('r_len_A') if u else None, 'r_len_N': u.get('r_len_N') if u else None,
                    'n_A': u.get('n_A') if u else None})
    top_s = max(out, key=lambda x: x['s'], default=None)
    rong = [x for x in out if x['do_rong'] is not None]
    top_w = max(rong, key=lambda x: x['do_rong'], default=None)
    return {'kenh_s_max': top_s, 'kenh_rong_nhat': top_w, 'n_kenh_F_I': len(out)}


doi_chieu = {}
for ds in cases:
    for arm in ('M1', 'C-a0'):
        ds_rows = []
        for o in sorted(cases[ds]):
            t = trung_gian[f'{ds}|{o}'][arm]
            r = json.load(open(os.path.join(ROOT, t['result']), encoding='utf-8'))['records'][0]
            root = cases[ds][o]['root']
            blocks = r['worlds']['P']['blocks']
            order = [e for b in blocks for g in b['groups'] for e in g]
            tang = r['extra'].get('tang_P', {})
            if t['root_block'] == 0 and t['root_block_size'] == 1:
                comp = next((e for e in order if e != root), None)
                nhom = 'dung'
            else:
                comp = order[0] if order and order[0] != root else None
                nhom = 'sai'
            canh = r['extra'].get('canh', [])
            rel_c = [x for x in canh if comp in x and root in x] if comp else []
            ds_rows.append({'opaque_id': o, 'cell': cases[ds][o]['cell'], 'nhom': nhom, 'rr': t['rr_table'],
                            'root': kenh_manh(r, root), 'doi_thu': comp, 'doi_thu_tier': tang.get(comp),
                            'doi_thu_kenh': kenh_manh(r, comp) if comp else None, 'canh_root_doi_thu': rel_c})
        doi_chieu[f'{ds}|{arm}'] = ds_rows

# ------------------------------------------------------------------ 5c. E5 có tác dụng ở đâu (M1): số thực thể tầng 2, kênh bị giải thích
e5_tac_dung = {}
for ds in cases:
    n2, nap = [], []
    for o in sorted(cases[ds]):
        r = json.load(open(os.path.join(ROOT, trung_gian[f'{ds}|{o}']['M1']['result']), encoding='utf-8'))['records'][0]
        n2.append(sum(1 for v in r['extra'].get('tang_P', {}).values() if v == 2))
        nap.append(sum(1 for x in r.get('inherited_by', []) if x['trang_thai'] == 'ap_dung'))
    e5_tac_dung[ds] = {'so_ca': len(n2), 'ca_co_thuc_the_tang2': sum(1 for x in n2 if x > 0),
                       'tong_thuc_the_tang2': sum(n2), 'tong_dong_inherited_ap_dung': sum(nap)}

# ------------------------------------------------------------------ 6. phụ: C-e, vùng, vị trí N, thiếu
ce = Counter(x['status'] for x in tables['ce'])
# C-e (cửa sổ t′ = t − 300, trước tiêm; mô tả, ngoài A4): V0, N1 (số thực thể tầng 1), thực thể đứng đầu, RR của root tương lai
ce_ok = [x for x in tables['ce'] if x['status'] == 'OK']
ce_top = Counter(e for x in ce_ok for e, v in x['top_mass'].items() if frac(v) > 0)
ce_sum = {
    'n_OK': len(ce_ok), 'V0': dict(Counter(x['V0'] for x in ce_ok)),
    'N1_mean': fs(Fraction(sum(x['N1'] for x in ce_ok), len(ce_ok))) if ce_ok else None,
    'top_mass_entities': dict(ce_top.most_common()),
    'future_root_MRR': fs(sum((frac(x['future_root_score']['RR']) for x in ce_ok), Fraction(0)) / len(ce_ok)),
    'future_root_hit1_count': sum(1 for x in ce_ok if x['future_root_score']['hit@1'] > 0),
    'chance_returned_MRR': fs(sum((frac(x['chance_returned_RR']) for x in ce_ok), Fraction(0)) / len(ce_ok)),
    'pointer': 'reports/main-013-v2/tables.json#/ce',
}
# Ca E5 quyết định (M1 khác bo-E5 về RR root): tầng của các thực thể đứng trên root ở bo-E5 khi chạy M1
e5_quyet = {}
for ds in cases:
    for o in sorted(cases[ds]):
        if rr(ds, o, 'M1') != rr(ds, o, 'bo-E5'):
            r = json.load(open(os.path.join(ROOT, trung_gian[f'{ds}|{o}']['M1']['result']), encoding='utf-8'))['records'][0]
            tren = [x['entity'] for x in trung_gian[f'{ds}|{o}']['bo-E5']['above_root']]
            e5_quyet[f'{ds}|{o}'] = {
                'cell': cases[ds][o]['cell'], 'M1_rr': float(rr(ds, o, 'M1')), 'boE5_rr': float(rr(ds, o, 'bo-E5')),
                'tren_root_o_boE5': {e: r['extra']['tang_P'].get(e) for e in tren},
                'giai_thich_M1': [{'thuc_the': x['thuc_the'], 'kenh': x['kenh'], 'by': x['giai_thich'],
                                   'rule': x['quy_tac']} for x in r.get('inherited_by', [])
                                  if x['thuc_the'] in tren and x['trang_thai'] == 'ap_dung'][:10]}
# Vùng E7 (src/m1_danh_gia/e7.py): p = tỷ lệ kỳ vọng vùng chứa root; R_ky_vong = cỡ vùng kỳ vọng; trên O = chia số thực thể quan sát.
reg = defaultdict(lambda: Counter())
for x in tables['regions']:
    for cach in ('cach_1', 'cach_2'):
        g = reg[(x['dataset'], x['arm'], cach)]
        g['n'] += 1
        g['tong_p'] += x[cach]['p']
        g['tong_R_ky_vong'] += x[cach]['R_ky_vong']
        g['tong_R_tren_O'] += x[cach]['R_ky_vong_tren_O'] or 0
        g['so_O_0'] += 1 if not x['O'] else 0
for g in reg.values():
    for k in ('p', 'R_ky_vong', 'R_tren_O'):
        g['tb_' + k] = g['tong_' + k] / g['n']
posN = Counter((x['dataset'], x['p75']['group']) for x in tables['position_N'])
# Tách theo loại lỗi và nhóm vị trí N (p75) cho các vế chính; MRR trung bình và số ca
nhom_N = {(x['dataset'], x['opaque_id']): x['p75']['group'] for x in tables['position_N']}
VE_TACH = {'RE2-TT': ('M1', 'torai_B', 'C-a0', 'C-d2', 'simplerca'), 'Nezha-OB': ('M1', 'simplerca', 'C-a0', 'C-d2')}
tach = {}
for ds, ves in VE_TACH.items():
    for chieu, khoa in (('fault', lambda o: cases[ds][o]['fault']), ('vi_tri_N_p75', lambda o: nhom_N[(ds, o)])):
        g = defaultdict(list)
        for o in cases[ds]:
            g[khoa(o)].append(o)
        tach[f'{ds}|{chieu}'] = {
            k: {'n': len(v), **{a: round(float(sum((rr(ds, o, a) for o in v), Fraction(0)) / len(v)), 6) for a in ves},
                'M1_thang_thua_' + ves[1]: [sum(rr(ds, o, 'M1') > rr(ds, o, ves[1]) for o in v),
                                             sum(rr(ds, o, 'M1') < rr(ds, o, ves[1]) for o in v)]}
            for k, v in sorted(g.items())}
missing = Counter((m[3], m[4]) for m in tables['missing'])

out = {
    'schema': 'T054-P7A-PHAN-TICH-1', 'note': 'Chỉ đọc; không chạy phương pháp; root lấy từ ô đã ghép nhãn sau seal.',
    'inputs': inputs,
    'verified_results_checked': {f'{k[0]}|{k[1]}|{k[2]}|{k[3]}': v for k, v in sorted(checked.items())},
    'rr_blocks_vs_table': {f'{k[0]}|{k[1]}|match={k[2]}': v for k, v in sorted(khop_rr.items())},
    'bang_theo_ve_P': bang, 'so_cap': cap, 'doi_top_khi_bo': doi_top, 'ho_so_tang_root_M1': ho_so,
    'doi_chieu_sai_dung': doi_chieu, 'E5_tac_dung_M1': e5_tac_dung,
    'trung_gian_theo_ca': trung_gian,
    'ce_status': dict(ce), 'ce_tom_tat': ce_sum, 'E5_ca_quyet_dinh': e5_quyet, 'regions': {f'{k[0]}|{k[1]}|{k[2]}': {kk: float(vv) for kk, vv in v.items()}
                                       for k, v in sorted(reg.items())},
    'position_N_p75': {f'{k[0]}|{k[1]}': v for k, v in sorted(posN.items())}, 'tach_MRR': tach,
    'missing': {f'{k[0]}|{k[1]}': v for k, v in missing.items()},
    'cases': cases,
}
if os.path.exists(OUT):
    sys.exit(f'OUTPUT_EXISTS {OUT}')
with open(OUT, 'x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
print(json.dumps({'ok': True, 'out': OUT.replace('\\', '/'), 'sha256': sha(OUT), 'checked': sum(checked.values()),
                  'rr_match': {f'{k}': v for k, v in khop_rr.items()}}, ensure_ascii=False))
