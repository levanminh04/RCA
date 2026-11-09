"""T-056 phần 2: vì sao SimpleRCA cao nhất, "dữ liệu đơn giản", độ khó ca I/II/III. Chỉ đọc.

Đầu vào: results/T-056/runs/ec2-002/rules-ec2_{1,2}.json (rules_ec2.py chạy trên EC2, theo mã mờ, không nhãn),
bảng đã chấm T-054/T-055, nhãn G1 CSV và nhãn riêng RE3. Đầu ra: results/T-056/ket-qua-002.json (tạo mới).
Quy tắc (theo service, cửa sổ N=[t-300,t), A=[t,t+300) trên metric):
 R1 = tổng số mẫu A vượt mean_N + 3·std_N qua mọi cột (đúng phần metric của src/simplerca/core.py, aggregation 'events')
 R1b = số cột có ít nhất một mẫu vượt; R2 = max |mean_A − mean_N|/std_N; R3 = max (max_A − median_N)/IQR_N (c=1 khi IQR=0, như E4);
 R4 = số dòng log ERROR/FAIL/EXCEPTION trong A.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

REPO = Path('D:/RCA-flashticket')
OUT = REPO / 'results/T-056/ket-qua-002.json' if len(sys.argv) < 2 else Path(sys.argv[1])


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


R = {}
for h in ('ec2_1', 'ec2_2'):
    R.update(json.loads((REPO / f'results/T-056/runs/ec2-002/rules-{h}.json').read_bytes()))
roots = {}
for r in csv.DictReader(open(REPO / 'results/T-021/chia-theo-o/A-phan-tang.csv', encoding='utf-8')):
    if r['dataset'] in ('RE2-TT', 'Nezha-OB') and r['vai_tro'] == 'test':
        m = hashlib.sha256(json.dumps([r['dataset'], r['case']], separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        roots[(r['dataset'], 'test-' + m[:10])] = (r['root'], r['fault'])
for o, v in json.loads(Path('D:/RCA-ext/private/T-055/labels.json').read_bytes())['cases'].items():
    roots[('RE3-OB', o)] = (v['root'], v['fault'])


def exp_rr(sc, root):
    if root not in sc:
        return 0.0
    s = sc[root]
    hi = sum(1 for v in sc.values() if v > s)
    ti = sum(1 for v in sc.values() if v == s)
    return float(sum(Fraction(1, hi + k) for k in range(1, ti + 1)) / ti)


rr = {}
for r in json.loads((REPO / 'results/T-054/reports/main-013-v2/tables.json').read_bytes())['rows']:
    if r['world'] == 'P':
        rr[(r['dataset'], r['opaque_id'], r['arm'])] = r['metrics']['rr']
for r in json.loads((REPO / 'results/T-054/reports/re3-ban-cuoi-001/re3-tables.json').read_bytes())['per_case']:
    if r['world'] == 'P' and r['arm'] != 'circa':
        rr[('RE3-OB', r['opaque_id'], r['arm'])] = r['metrics']['rr']
for r in json.loads((REPO / 'results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json').read_bytes())['per_case']:
    if r['world'] == 'P' and r['variant'] == 'ols+rht_da':
        rr[('RE3-OB', r['opaque_id'], 'circa')] = r['metrics']['rr']

per = []
for o, c in sorted(R.items()):
    ds = c['dataset']; root, fault = roots[(ds, o)]; sv = c['svc']
    rules = {'R1_events': {e: v['events'] for e, v in sv.items()}, 'R1b_cols': {e: v['n_cols_ev'] for e, v in sv.items()},
             'R2_zmean': {e: v['max_zmean'] for e, v in sv.items()}, 'R3_zpoint': {e: v['max_zpoint'] for e, v in sv.items()}}
    if c['logerr_A'] and '_err' not in c['logerr_A']:
        rules['R4_logerr'] = dict(c['logerr_A'])
    row = {'dataset': ds, 'opaque_id': o, 'root': root, 'fault': fault,
           'root_events': sv.get(root, {}).get('events'),
           'max_other_events': max([v['events'] for e, v in sv.items() if e != root] or [0])}
    for k, sc in rules.items():
        row[k] = exp_rr(sc, root)
    for a in ('M1', 'simplerca', 'C-a0'):
        row[a] = rr.get((ds, o, a))
    per.append(row)

tom = {}
for ds in ('RE2-TT', 'RE3-OB'):
    sub = [r for r in per if r['dataset'] == ds]
    keys = [k for k in ('R1_events', 'R1b_cols', 'R2_zmean', 'R3_zpoint', 'R4_logerr', 'M1', 'simplerca', 'C-a0')
            if all(k in r and r[k] is not None for r in sub)]
    lv = Counter('I' if r['R1_events'] == 1.0 else ('II' if r['M1'] == 1.0 else 'III') for r in sub)
    tom[ds] = {'n': len(sub), 'MRR': {k: sum(r[k] for r in sub) / len(sub) for k in keys},
               'R1_top1_trung_M4_top1': sum((r['R1_events'] == 1.0) == (r['simplerca'] == 1.0) for r in sub),
               'root_events_hon_moi_service_khac': sum((r['root_events'] or 0) > r['max_other_events'] for r in sub),
               'M1_top1_R1_top1': {f'{a}|{b}': v for (a, b), v in Counter((r['M1'] == 1.0, r['R1_events'] == 1.0) for r in sub).items()},
               'ca_lech_M1_R1': [r for r in sub if (r['M1'] == 1.0) != (r['R1_events'] == 1.0)],
               'do_kho_theo_du_lieu': {'dinh_nghia': 'I = R1 đặt root hạng 1; II = chỉ M1 đặt root hạng 1; III = cả hai không',
                                       'dem': dict(lv),
                                       'theo_loi': {f: dict(Counter('I' if r['R1_events'] == 1.0 else ('II' if r['M1'] == 1.0 else 'III')
                                                                    for r in sub if r['fault'] == f))
                                                    for f in sorted({r['fault'] for r in sub})}}}

METH = {'RE2-TT': ['M1', 'simplerca', 'torai_B', 'baro', 'circa', 'tracerca', 'microrank'],
        'Nezha-OB': ['M1', 'simplerca', 'baro', 'tracerca', 'microrank'],
        'RE3-OB': ['M1', 'simplerca', 'torai_B', 'baro', 'circa', 'tracerca', 'microrank']}
theo_pp = {}
for ds, ms in METH.items():
    oids = sorted({o for (d, o, a) in rr if d == ds})
    lv, byf = Counter(), defaultdict(Counter)
    for o in oids:
        k = sum(1 for a in ms if rr.get((ds, o, a)) == 1.0)
        L = 'I' if k >= len(ms) / 2 else ('II' if k >= 1 else 'III')
        lv[L] += 1; byf[roots[(ds, o)][1]][L] += 1
    theo_pp[ds] = {'dinh_nghia': 'I = ≥ nửa số phương pháp đặt root hạng 1; II = 1..<nửa; III = không', 'phuong_phap': ms,
                   'dem': dict(lv), 'theo_loi': {f: dict(c) for f, c in sorted(byf.items())}}

out = {'schema': 'T056-KET-QUA-2', 'inputs': {
    'rules_ec2_1': sha(REPO / 'results/T-056/runs/ec2-002/rules-ec2_1.json'),
    'rules_ec2_2': sha(REPO / 'results/T-056/runs/ec2-002/rules-ec2_2.json'),
    'rules_script': sha(REPO / 'results/T-056/scripts/rules_ec2.py'),
    'main_tables': sha(REPO / 'results/T-054/reports/main-013-v2/tables.json'),
    're3_tables': sha(REPO / 'results/T-054/reports/re3-ban-cuoi-001/re3-tables.json'),
    're3_circa': sha(REPO / 'results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json')},
    'tom_tat': tom, 'do_kho_theo_phuong_phap': theo_pp, 'theo_ca': per,
    'gioi_han': 'OB (Nezha) không tính R1 vì dữ liệu thô không có trên EC2; R1 là tái lập phần metric của M4, kiểm bằng trùng hạng 1 với M4 thật.'}
with open(OUT, 'x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
print(json.dumps({'out': str(OUT), 'sha256': sha(OUT)}))
