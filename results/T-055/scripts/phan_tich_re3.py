"""T-055: phân tích RE3-OB sau chấm. Chỉ đọc bảng đã chấm và trung gian đã VERIFIED; không chạy phương pháp.

Nguồn: results/T-054/reports/re3-ban-cuoi-001/{re3-tables.json, tables-describe.json} (lượt chính, CIRCA không hợp lệ),
results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json (CIRCA bổ sung), result.json M1-family trong bản nhận
ở D:/RCA-ext/T-055/work-re3-score-v1 (kiểm sha256 theo verified.json). Đầu ra: results/T-055/reports/re3/phan-tich-re3.json
"""
import glob
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

REPO = Path('D:/RCA-flashticket')
S1 = Path('D:/RCA-ext/T-055/work-re3-score-v1')
RECV = S1 / 'results/T-054/runs/re3-ban-cuoi-001/received'
OUT = REPO / 'results/T-055/reports/re3/phan-tich-re3.json'
if len(sys.argv) > 1:
    OUT = Path(sys.argv[1])
M1F = ('M1', 'C-a0', 'C-a1', 'bo-E1', 'bo-E2', 'bo-E5')
METRICS = ('rr', 'hit@1', 'hit@3', 'hit@5', 'ndcg@5', 'avg@5')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def L(p):
    return json.loads(Path(p).read_bytes())


main_t = L(REPO / 'results/T-054/reports/re3-ban-cuoi-001/re3-tables.json')
circa_t = L(REPO / 'results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json')
desc = L(REPO / 'results/T-054/reports/re3-ban-cuoi-001/tables-describe.json')
inputs = {str(p.relative_to(REPO)).replace('\\', '/'): sha(p) for p in [
    REPO / 'results/T-054/reports/re3-ban-cuoi-001/re3-tables.json',
    REPO / 'results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json',
    REPO / 'results/T-054/reports/re3-ban-cuoi-001/tables-describe.json']}

# ---------------------------------------------------------------- hàng theo ca, world P
rows = {}   # (oid, arm) -> {'cell','metrics','supported','status'}
cells = {}
for r in main_t['per_case']:
    if r['world'] != 'P' or r['arm'] == 'circa':
        continue
    rows[(r['opaque_id'], r['arm'])] = r
    cells[r['opaque_id']] = r['cell']
for r in circa_t['per_case']:
    if r['world'] != 'P':
        continue
    arm = 'circa' if r['variant'] == 'ols+rht_da' else 'circa_rht_aux'
    rows[(r['opaque_id'], arm)] = r
if isinstance(desc.get('rows'), list):
    for r in desc['rows']:
        if r.get('world') == 'P' and r.get('arm') in ('C-d1', 'C-d2', 'C-c', 'C-g'):
            m = r['metrics']
            rows[(r['opaque_id'], r['arm'])] = {'cell': cells.get(r['opaque_id'], r.get('cell')), 'supported': True,
                                                'metrics': {k: m.get(k) for k in METRICS},
                                                'seed_status': r.get('statuses')}
oids = sorted(cells)
assert len(oids) == 30
ARMS = sorted({a for _, a in rows})


def val(oid, arm, k='rr'):
    r = rows.get((oid, arm))
    if r is None:
        return None
    v = r['metrics'].get(k)
    return 0.0 if v is None else float(v)


fault = {o: cells[o].split('|')[2] for o in oids}
root = {o: cells[o].split('|')[1] for o in oids}
bang = {}
for a in ARMS:
    have = [o for o in oids if (o, a) in rows]
    st = Counter(s for o in have for s in (rows[(o, a)].get('seed_status') or []))
    bang[a] = {'n': len(have), 'status': dict(st),
               **{k: float(np.mean([val(o, a, k) for o in have])) if have else None for k in METRICS}}

tach = {}
for key, g in (('fault', fault), ('cell', cells), ('root', root)):
    grp = defaultdict(list)
    for o in oids:
        grp[g[o]].append(o)
    tach[key] = {k: {'n': len(v), **{a: {'rr': float(np.mean([val(o, a) for o in v])),
                                         'hit@5': float(np.mean([val(o, a, 'hit@5') for o in v]))}
                                     for a in ARMS if all((o, a) in rows for o in v)}}
                 for k, v in sorted(grp.items())}

# ---------------------------------------------------------------- so cặp + bootstrap theo ô (cách src/p3/danh_gia.bootstrap §8.8)
cell_list = sorted(set(cells.values()))
rng = np.random.default_rng(20261005)
draw = rng.integers(0, len(cell_list), size=(10000, len(cell_list)))
W = np.zeros((10000, len(oids)))
for ci, c in enumerate(cell_list):
    cnt = (draw == ci).sum(axis=1)
    for i, o in enumerate(oids):
        if cells[o] == c:
            W[:, i] += cnt
tot = W.sum(axis=1)


def ci(diff):
    s = W @ np.array(diff) / tot
    lo, hi = np.percentile(s, [2.5, 97.5])
    return [float(lo), float(hi)]


pairs = {}
for b in ARMS:
    if b == 'M1':
        continue
    for k in ('rr', 'hit@5', 'hit@1'):
        if not all((o, b) in rows for o in oids):
            continue
        d = [val(o, 'M1', k) - val(o, b, k) for o in oids]
        per_cell = defaultdict(float)
        for o, x in zip(oids, d):
            per_cell[cells[o]] += x
        pairs[f'M1-{b}|{k}'] = {'delta': float(np.mean(d)), 'CI_o': ci(d),
                                'win': sum(x > 1e-12 for x in d), 'loss': sum(x < -1e-12 for x in d),
                                'tie': sum(abs(x) <= 1e-12 for x in d),
                                'cells_nonzero': sum(abs(v) > 1e-12 for v in per_cell.values()),
                                'cells_negative': sum(v < -1e-12 for v in per_cell.values()),
                                'cases': [{'opaque_id': o, 'cell': cells[o], 'M1': val(o, 'M1', k), b: val(o, b, k)}
                                          for o, x in zip(oids, d) if abs(x) > 1e-12]}

# ---------------------------------------------------------------- trung gian M1-family theo ca
def fam(k):
    p = k['don_vi'].split('|')[0]
    if p == 'op':
        return 'E1_self' if k['lop'] == 'khong_lan' else 'op_full'
    return {'canh': 'E2_edge', 'metric': 'metric', 'log': 'log'}.get(p, p)


results = {}
for vf in glob.glob(str(RECV / '*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/verified.json')):
    d = Path(vf).parent
    job = L(d / 'job.json')
    s = job['slot']
    if s['arm'] not in M1F:
        continue
    v = L(vf)
    if sha(d / 'result.json') != v['result']['sha256']:
        raise SystemExit('hash result khác verified')
    results[(s['opaque_id'], s['arm'])] = d / 'result.json'

trung_gian = defaultdict(dict)
for (oid, arm), rp in sorted(results.items()):
    rec = L(rp)['records'][0]
    rt = root[oid]
    if rec['status'] != 'OK':
        trung_gian[oid][arm] = {'status': rec['status'], 'error': str(rec.get('error'))[:200]}
        continue
    ex = rec['extra']
    blocks = rec['worlds']['P']['blocks']
    tang = ex.get('tang_P', {})
    order = [e for b in blocks for g in b['groups'] for e in g]
    pos = 0; rb = None
    for i, b in enumerate(blocks):
        g = [e for gg in b['groups'] for e in gg]
        if rt in g:
            rb = (i, len(g), pos); break
        pos += len(g)
    dv = {u['ma']: u for u in ex.get('don_vi_phan_vi', [])}

    def chans(ent):
        out = []
        for k in ex.get('kenh_co', []):
            if k['thuc_the'] != ent:
                continue
            u = dv.get(k['don_vi'])
            w = (u['r_len_A'] - u['r_len_N']) if u and k['huong'] == 'len' and u.get('r_len_A') is not None else None
            out.append({'fam': fam(k), 'ten': k['ten'], 'lop': k['lop'], 's': k['s'], 'F_I': k['F_I'], 'do_rong': w})
        return sorted(out, key=lambda x: -x['s'])
    rc = chans(rt)
    top = order[0] if order else None
    comp = top if top != rt else (order[1] if len(order) > 1 else None)
    trung_gian[oid][arm] = {
        'status': 'OK', 'verdict': rec.get('verdict'), 'n_tier1': sum(1 for x in tang.values() if x == 1),
        'root_tier': tang.get(rt), 'root_block': rb[0] if rb else None, 'root_block_size': rb[1] if rb else None,
        'root_in_returned': rb is not None, 'root_channels': rc[:10], 'root_fam_F_raw': dict(Counter(c['fam'] for c in rc)),
        'root_fam_F_I': dict(Counter(c['fam'] for c in rc if c['F_I'] == 1)), 'n_root_channels': len(rc),
        'root_inherited': [{'kenh': x['kenh'], 'by': x['giai_thich'], 'rule': x['quy_tac']}
                           for x in rec.get('inherited_by', []) if x['thuc_the'] == rt and x['trang_thai'] == 'ap_dung'][:8],
        'top_or_runner_up': comp, 'comp_tier': tang.get(comp), 'comp_channels': chans(comp)[:5] if comp else [],
        'edges_root_comp': [e for e in ex.get('canh', []) if comp in e and rt in e] if comp else [],
        'top_blocks': [{'entities': [e for g in b['groups'] for e in g], 'key': b['key']} for b in blocks[:3]],
        'n_edges': len(ex.get('canh', [])), 'n_flagged_entities': len({k['thuc_the'] for k in ex.get('kenh_co', [])}),
        'coverage': {k: v.get('trang_thai') for k, v in rec.get('coverage', {}).items()}}

# Tín hiệu root theo loại lỗi (M1): có kênh có cờ không, họ kênh nào.
tin_hieu = defaultdict(lambda: Counter())
for o in oids:
    t = trung_gian[o].get('M1', {})
    if t.get('status') != 'OK':
        tin_hieu[fault[o]]['M1_not_OK'] += 1; continue
    tin_hieu[fault[o]]['n'] += 1
    tin_hieu[fault[o]]['root_has_flag'] += int(t['n_root_channels'] > 0)
    tin_hieu[fault[o]]['root_top1_alone'] += int(t['root_block'] == 0 and t['root_block_size'] == 1)
    for f in t['root_fam_F_raw']:
        tin_hieu[fault[o]]['fam:' + f] += 1

errors = []
for vf in glob.glob(str(RECV / '*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/method-failure.json')):
    c = L(vf); a = c['audit']
    job = L(Path(vf).parent / 'job.json')
    errors.append({'opaque_id': job['slot']['opaque_id'], 'arm': a['arm'], 'seed': job['slot']['seed'],
                   'error': a['errors'][0][:160]})

out = {'schema': 'T055-PHAN-TICH-RE3-1', 'inputs': inputs, 'n_cases': len(oids), 'cells': cell_list,
       'bang_theo_ve_P': bang, 'tach': tach, 'so_cap': pairs, 'trung_gian_M1_family': trung_gian,
       'tin_hieu_root_theo_loi': {k: dict(v) for k, v in tin_hieu.items()}, 'loi_phuong_phap': sorted(errors, key=str),
       'cases': {o: {'cell': cells[o]} for o in oids},
       'describe_regions': desc.get('regions'), 'describe_position_N': desc.get('position_N'),
       'describe_error': desc.get('describe_error')}
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, 'x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
print(json.dumps({'out': str(OUT), 'sha256': sha(OUT), 'arms': len(ARMS)}))
