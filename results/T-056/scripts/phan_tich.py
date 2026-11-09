"""T-056 phân tích trên laptop (chỉ đọc). Đầu ra: results/T-056/ket-qua.json (tạo mới)."""
import csv
import glob
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

REPO = Path('D:/RCA-flashticket')
OUT = REPO / 'results/T-056/ket-qua.json' if len(sys.argv) < 2 else Path(sys.argv[1])
EC2 = {}
for h in ('ec2_1', 'ec2_2'):
    EC2.update(json.loads((REPO / f'results/T-056/runs/ec2-001/{h}.json').read_bytes()))
REQ = {}
for h in ('ec2_1', 'ec2_2'):
    REQ.update(json.loads((REPO / f'results/T-056/runs/yeu-cau-001/{h}.json').read_bytes())['cases'])


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- nhãn
roots = {}
for r in csv.DictReader(open(REPO / 'results/T-021/chia-theo-o/A-phan-tang.csv', encoding='utf-8')):
    if r['dataset'] in ('RE2-TT', 'Nezha-OB') and r['vai_tro'] == 'test':
        m = hashlib.sha256(json.dumps([r['dataset'], r['case']], separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        roots[(r['dataset'], 'test-' + m[:10])] = (r['root'], r['fault'])
for o, v in json.loads(Path('D:/RCA-ext/private/T-055/labels.json').read_bytes())['cases'].items():
    roots[('RE3-OB', o)] = (v['root'], v['fault'])


def exp_rr(scores, root):
    """RR kỳ vọng khi xếp giảm theo điểm, hòa ngẫu nhiên đều; root vắng/điểm <= 0 vẫn xếp theo điểm."""
    if root not in scores:
        return 0.0
    sr = scores[root]
    higher = sum(1 for e, s in scores.items() if s > sr)
    tie = sum(1 for e, s in scores.items() if s == sr)
    return float(sum(Fraction(1, higher + k) for k in range(1, tie + 1)) / tie)


# ---------------------------------------------------------------- kết quả M1/M4 theo ca (đã chấm)
re3 = json.loads((REPO / 'results/T055_dummy').read_bytes()) if False else None
re3_rows = {(r['opaque_id'], r['arm']): r['metrics']['rr'] for r in
            json.loads((REPO / 'results/T-054/reports/re3-ban-cuoi-001/re3-tables.json').read_bytes())['per_case']
            if r['world'] == 'P'}
tt_rows = {(r['dataset'], r['opaque_id'], r['arm']): r['metrics']['rr'] for r in
           json.loads((REPO / 'results/T-054/reports/main-013-v2/tables.json').read_bytes())['rows'] if r['world'] == 'P'}

# ---------------------------------------------------------------- 2.1 & 2.2 RE3: status span và log lỗi
s21, s22 = [], []
for o, r in sorted(EC2.items()):
    if r['dataset'] != 'RE3-OB':
        continue
    root, fault = roots[('RE3-OB', o)]
    sp, lg = r['spans'], r['logs']
    d_err = {e: v['err_A'] - v['err_N'] for e, v in sp.items()}
    d_own = {e: v['own_A'] - v['own_N'] for e, v in sp.items()}
    rate = {e: (v['err_A'] / max(v['spans_A'], 1)) - (v['err_N'] / max(v['spans_N'], 1)) for e, v in sp.items()}
    d_log = {e: v['err_A'] - v['err_N'] for e, v in lg.items()}
    m1, m4 = re3_rows.get((o, 'M1')), re3_rows.get((o, 'simplerca'))
    s21.append({'opaque_id': o, 'root': root, 'fault': fault, 'root_in_traces': root in sp,
                'root_err_N': sp.get(root, {}).get('err_N'), 'root_err_A': sp.get(root, {}).get('err_A'),
                'root_own_A': sp.get(root, {}).get('own_A'), 'root_own_N': sp.get(root, {}).get('own_N'),
                'top_d_err': max(d_err, key=d_err.get) if d_err else None, 'top_d_own': max(d_own, key=d_own.get) if d_own else None,
                'rr_d_err': exp_rr(d_err, root), 'rr_d_own': exp_rr(d_own, root), 'rr_rate': exp_rr(rate, root),
                'n_services_with_err_increase': sum(1 for v in d_err.values() if v > 0), 'M1_rr': m1, 'M4_rr': m4})
    s22.append({'opaque_id': o, 'root': root, 'fault': fault, 'root_in_logs': root in lg,
                'root_logerr_N': lg.get(root, {}).get('err_N'), 'root_logerr_A': lg.get(root, {}).get('err_A'),
                'top_d_log': max(d_log, key=d_log.get) if d_log else None, 'rr_d_log': exp_rr(d_log, root),
                'n_containers_with_logerr_increase': sum(1 for v in d_log.values() if v > 0), 'M1_rr': m1, 'M4_rr': m4})


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def by_fault(rows, key):
    g = defaultdict(list)
    for r in rows:
        g[r['fault']].append(r[key])
    return {f: {'n': len(v), 'MRR': mean(v)} for f, v in sorted(g.items())}


tom21 = {'MRR_rule_d_err': mean([r['rr_d_err'] for r in s21]), 'MRR_rule_d_own': mean([r['rr_d_own'] for r in s21]),
         'MRR_rule_rate': mean([r['rr_rate'] for r in s21]), 'MRR_M1': mean([r['M1_rr'] for r in s21]),
         'MRR_M4': mean([r['M4_rr'] for r in s21]), 'root_top_by_d_own': sum(r['top_d_own'] == r['root'] for r in s21),
         'root_has_err_increase': sum((r['root_err_A'] or 0) > (r['root_err_N'] or 0) for r in s21),
         'root_has_own_err_A': sum((r['root_own_A'] or 0) > 0 for r in s21),
         'by_fault_d_own': by_fault(s21, 'rr_d_own'), 'top_d_own_counter': dict(Counter(r['top_d_own'] for r in s21)),
         'M1_wrong_cases': [r for r in s21 if (r['M1_rr'] or 0) < 1]}
tom22 = {'MRR_rule_d_log': mean([r['rr_d_log'] for r in s22]), 'root_top_by_d_log': sum(r['top_d_log'] == r['root'] for r in s22),
         'root_in_logs': sum(r['root_in_logs'] for r in s22),
         'root_has_logerr_increase': sum((r['root_logerr_A'] or 0) > (r['root_logerr_N'] or 0) for r in s22),
         'by_fault': by_fault(s22, 'rr_d_log'), 'top_d_log_counter': dict(Counter(r['top_d_log'] for r in s22)),
         'M1_wrong_cases': [r for r in s22 if (r['M1_rr'] or 0) < 1]}

# ---------------------------------------------------------------- 2.3 IQR = 0 / z theo đơn vị gốc
M1_RESULT = {}
for pat in ['D:/RCA-flashticket/results/T-054/runs/chuan-bi-main-013-v2/received-main-002/*/results/T-054/runs/main-013-v2/queue/*/attempt-*/job.json',
            'D:/RCA-flashticket/results/T-054/runs/main-013-v2/queue/*/attempt-*/job.json',
            'D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json']:
    for jf in glob.glob(pat):
        j = json.loads(Path(jf).read_bytes())
        if j['slot']['arm'] == 'M1' and j['slot']['view'] == 'main' and (Path(jf).parent / 'verified.json').exists():
            M1_RESULT[(j['slot']['dataset'], j['slot']['opaque_id'])] = Path(jf).parent / 'result.json'
match, nflag, n_c1 = 0, 0, 0
per_ds = defaultdict(lambda: Counter())
case23 = []
for (ds, o), rp in sorted(M1_RESULT.items()):
    rec = json.loads(rp.read_bytes())['records'][0]
    root = roots[(ds, o)][0]
    ec = EC2.get(o, {}).get('metrics', {}) if ds != 'Nezha-OB' else {}
    dv = {u['ma']: u for u in rec['extra'].get('don_vi_phan_vi', [])}
    best = {}
    for k in rec['extra'].get('kenh_co', []):
        e = k['thuc_the']
        info = {'don_vi': k['don_vi'], 's': k['s'], 'fam': k['don_vi'].split('|')[0]}
        if k['don_vi'].startswith('metric|'):
            col = k['don_vi'].split('|', 1)[1]
            st = ec.get(col)
            if st and 'z_len' in st:
                z = st['z_len'] if k['huong'] == 'len' else st['z_xuong']
                ok = abs(z - k['s']) <= 1e-6 * max(1, abs(k['s']))
                per_ds[ds]['metric_flagged_checked'] += 1
                per_ds[ds]['z_recompute_match'] += int(ok)
                per_ds[ds]['c_is_1'] += int(st['c_is_1'])
                info.update(c_is_1=st['c_is_1'], z_match=ok)
            elif ds == 'Nezha-OB':
                u = dv.get(k['don_vi'], {})
                w = (u.get('r_len_A') or 0) - (u.get('r_len_N') or 0)
                proxy = k['s'] >= 100 and w <= 0.05
                per_ds[ds]['metric_flagged_proxy'] += 1
                per_ds[ds]['proxy_large_s_narrow'] += int(proxy)
                info.update(proxy_large_narrow=proxy)
        if e not in best or k['s'] > best[e]['s']:
            best[e] = info
    blocks = rec['worlds']['P']['blocks']
    order = [e for b in blocks for g in b['groups'] for e in g]
    top = order[0] if order else None
    alone = bool(blocks) and len([e for g in blocks[0]['groups'] for e in g]) == 1
    wrong = not (top == root and alone)
    comp = top if wrong else (order[1] if len(order) > 1 else None)
    case23.append({'dataset': ds, 'opaque_id': o, 'wrong': wrong, 'comp': comp,
                   'comp_best': best.get(comp), 'root_best': best.get(root)})


def summ(ds):
    rows = [c for c in case23 if c['dataset'] == ds]
    def flag(x):
        if not x:
            return False
        return bool(x.get('c_is_1') or x.get('proxy_large_narrow'))
    return {'cases': len(rows), 'wrong': sum(r['wrong'] for r in rows),
            'wrong_comp_best_c1': sum(r['wrong'] and flag(r['comp_best']) for r in rows),
            'correct_root_best_c1': sum((not r['wrong']) and flag(r['root_best']) for r in rows),
            'correct_comp_best_c1': sum((not r['wrong']) and flag(r['comp_best']) for r in rows),
            'wrong_cases': [r for r in rows if r['wrong']]}


tom23 = {'counts': {k: dict(v) for k, v in per_ds.items()}, 'by_dataset': {ds: summ(ds) for ds in ('RE2-TT', 'Nezha-OB', 'RE3-OB')},
         'note': 'TT/RE3: IQR tính lại trên dữ liệu thật ở EC2, kiểm z khớp s của M1. OB: chỉ dấu hiệu thay thế (s >= 100 và độ rộng <= 0,05), vì reader metric Nezha thô không được chạy lại.'}

# ---------------------------------------------------------------- 2.4 BARO và TORAI B trên RE3
S1 = Path('D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received')
baro_items, torai_top, torai_caller = Counter(), Counter(), Counter()
baro_rows = []
for jf in glob.glob(str(S1 / '*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json')):
    j = json.loads(Path(jf).read_bytes()); s = j['slot']
    if s['arm'] == 'baro':
        rec = json.loads((Path(jf).parent / 'result.json').read_bytes())['records'][0]
        rk = rec.get('ranking') or []
        root = roots[('RE3-OB', s['opaque_id'])][0]
        top_items = [x['item'] for x in rk[:3]]
        baro_items.update([top_items[0]] if top_items else [])
        rpos = next((i + 1 for i, x in enumerate(rk) if x['entity'] == root), None)
        root_item = next((x for x in rk if x['entity'] == root), None)
        baro_rows.append({'opaque_id': s['opaque_id'], 'top3_items': top_items, 'top_key': rk[0]['key'] if rk else None,
                          'root_first_item_rank': rpos, 'root_item': root_item['item'] if root_item else None,
                          'root_key': root_item['key'] if root_item else None})
    if s['arm'] == 'torai_B' and s['seed'] == 0:
        rp = Path(jf).parent / 'result.json'
        rec = json.loads(rp.read_bytes())['records'][0]
        er = [e for b in (rec.get('blocks') or []) for g in b['groups'] for e in g]
        root = roots[('RE3-OB', s['opaque_id'])][0]
        if er:
            torai_top[er[0]] += 1
            m1 = M1_RESULT.get(('RE3-OB', s['opaque_id']))
            canh = json.loads(m1.read_bytes())['records'][0]['extra'].get('canh', []) if m1 else []
            callers = {a for a, b in canh if b == root}
            torai_caller['top_is_direct_caller_of_root'] += int(er[0] in callers)
            torai_caller['top_is_root'] += int(er[0] == root)
            torai_caller['n'] += 1
redis_cols = Counter()
for o, r in EC2.items():
    if r['dataset'] != 'RE3-OB':
        continue
for o, c in REQ.items():
    pass
tom24 = {'baro_top_item': dict(baro_items), 'baro_cases': sorted(baro_rows, key=lambda x: x['opaque_id']),
         'torai_seed0_top': dict(torai_top), 'torai_top_vs_root': dict(torai_caller)}

# ---------------------------------------------------------------- 2.5 vùng nghi ngờ và vị trí N
tabs = json.loads((REPO / 'results/T-054/reports/main-013-v2/tables.json').read_bytes())
desc = json.loads((REPO / 'results/T-054/reports/re3-ban-cuoi-001/tables-describe.json').read_bytes())
reg = defaultdict(lambda: defaultdict(list))
for src in (tabs['regions'], desc['regions']):
    for x in src:
        for cach in ('cach_1', 'cach_2'):
            reg[(x['dataset'], x['arm'], cach)]['p'].append(x[cach]['p'])
            reg[(x['dataset'], x['arm'], cach)]['R'].append(x[cach]['R_ky_vong'])
            reg[(x['dataset'], x['arm'], cach)]['RO'].append(x[cach]['R_ky_vong_tren_O'] or 0)
            reg[(x['dataset'], x['arm'], cach)]['contains_root_all'].append(x[cach]['p'] == 1.0)
regions = {f'{k[0]}|{k[1]}|{k[2]}': {'n': len(v['p']), 'p_tb': mean(v['p']), 'R_tb': mean(v['R']),
                                     'R_tren_O_tb': mean(v['RO']), 'ca_chac_chua_root': sum(v['contains_root_all'])}
           for k, v in sorted(reg.items())}
pos = {}
for src in (tabs['position_N'], desc['position_N']):
    for x in src:
        pos[(x['dataset'], x['opaque_id'])] = x['p75']['group']
re3_rr = {o: v for (o, a), v in re3_rows.items()}
posg = defaultdict(lambda: defaultdict(list))
for (ds, o), g in pos.items():
    for arm, bl in (('M1', None), ('simplerca', None), ('torai_B', None)):
        v = tt_rows.get((ds, o, arm)) if ds != 'RE3-OB' else re3_rows.get((o, arm))
        if v is not None:
            posg[(ds, g)][arm].append(v)
positions = {f'{k[0]}|{k[1]}': {arm: {'n': len(v), 'MRR': mean(v)} for arm, v in d.items()} for k, d in sorted(posg.items())}

out = {'schema': 'T056-KET-QUA-1', 'inputs': {
    'ec2_ec2_1': sha(REPO / 'results/T-056/runs/ec2-001/ec2_1.json'), 'ec2_ec2_2': sha(REPO / 'results/T-056/runs/ec2-001/ec2_2.json'),
    're3_tables': sha(REPO / 'results/T-054/reports/re3-ban-cuoi-001/re3-tables.json'),
    'main_tables': sha(REPO / 'results/T-054/reports/main-013-v2/tables.json'),
    're3_describe': sha(REPO / 'results/T-054/reports/re3-ban-cuoi-001/tables-describe.json'),
    'labels_re3': sha('D:/RCA-ext/private/T-055/labels.json')},
    '2_1_status_span_RE3': {'tom_tat': tom21, 'theo_ca': s21}, '2_2_log_loi_RE3': {'tom_tat': tom22, 'theo_ca': s22},
    '2_3_iqr0': tom23, '2_4_baro_torai_RE3': tom24, '2_5_vung': regions, '2_5_vi_tri_N': positions}
with open(OUT, 'x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
print(json.dumps({'out': str(OUT), 'sha256': sha(OUT)}))
