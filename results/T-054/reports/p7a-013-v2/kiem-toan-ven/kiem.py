"""Luồng A — kiểm toàn vẹn số liệu P7(a) main013-v2. Chỉ đọc; không chạy phương pháp; không import cham/danh_gia.

A1 chấm lại độc lập mọi hàng world P từ ranking thô (result.json đã VERIFIED), nhãn lấy thẳng từ CSV G1.
   Ngữ nghĩa hòa viết lại từ đặc tả (khối cùng khóa liền nhau hoán vị đều; trong khối giữ thứ tự nhóm; trong nhóm
   thứ tự ngẫu nhiên đều): liệt kê chính xác khi số khối cùng khóa <= 7, còn lại Monte Carlo 20000 mẫu (seed 1).
A2 phép thử giả: xáo root giữa các ca; xếp ngẫu nhiên đều; xếp theo chữ cái; đếm bản ghi suy biến (một khối duy nhất
   chứa mọi thực thể = không phân biệt).
A3 quét rò nhãn: tên ca G1, đường dẫn riêng và chuỗi '<root>_<fault>' trong job/invocation/launch của mọi slot.
A5 đối chiếu các số trích trong bao-cao.md với file nguồn.
Chạy: py -3 -B results/T-054/reports/p7a-013-v2/kiem-toan-ven/kiem.py  (từ gốc repo)
"""
import csv
import glob
import hashlib
import itertools
import json
import math
import os
import random
import re
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
T = ROOT / 'results/T-054'
OUT = Path(__file__).resolve().parent / 'ket-qua.json'
QUEUES = [T / 'runs/chuan-bi-main-013-v2/received-main-002/ec2_1/results/T-054/runs/main-013-v2/queue',
          T / 'runs/chuan-bi-main-013-v2/received-main-002/ec2_2/results/T-054/runs/main-013-v2/queue',
          T / 'runs/main-013-v2/queue']


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- nhãn độc lập từ G1
labels, case_names = {}, {}
for r in csv.DictReader(open(ROOT / 'results/T-021/chia-theo-o/A-phan-tang.csv', encoding='utf-8')):
    if r['dataset'] in ('RE2-TT', 'Nezha-OB') and r['vai_tro'] == 'test':
        m = hashlib.sha256(json.dumps([r['dataset'], r['case']], separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        labels[(r['dataset'], 'test-' + m[:10])] = (r['root'], r['fault'])
        case_names[r['case']] = r['dataset']
assert sum(1 for k in labels if k[0] == 'RE2-TT') == 60 and sum(1 for k in labels if k[0] == 'Nezha-OB') == 34


# ---------------------------------------------------------------- khối và ngữ nghĩa hòa (viết lại)
def blocks_of(rec):
    if rec.get('blocks') is not None:
        return [(tuple(b['key']), [list(g) for g in b['groups']]) for b in rec['blocks']]
    out = []
    for row in rec.get('entity_ranking') or []:
        if out and out[-1][2] == row['tie_group']:
            out[-1][1][0].append(row['entity'])
        else:
            out.append([tuple(row['key']), [[row['entity']]], row['tie_group']])
    return [(k, g) for k, g, _ in out]


def metrics_from_rank_dist(dist):
    if not dist:
        return dict(rr=0.0, **{f'hit@{k}': 0.0 for k in (1, 3, 5)}, ndcg5=0.0)
    rr = sum(p / r for r, p in dist.items())
    h = {f'hit@{k}': sum(p for r, p in dist.items() if r <= k) for k in (1, 3, 5)}
    nd = sum(p / math.log2(1 + r) for r, p in dist.items() if r <= 5)
    return dict(rr=float(rr), **{k: float(v) for k, v in h.items()}, ndcg5=float(nd))


def rank_dist(bl, root, rng):
    pos, i = 0, 0
    while i < len(bl):
        j = i
        while j + 1 < len(bl) and bl[j + 1][0] == bl[i][0]:
            j += 1
        sg = bl[i:j + 1]
        idx = [n for n, (_, gs) in enumerate(sg) if any(root in g for g in gs)]
        if idx:
            jb = idx[0]
            before_in_block = 0
            for g in sg[jb][1]:
                if root in g:
                    gsize = len(g); break
                before_in_block += len(g)
            sizes = [sum(len(g) for g in gs) for _, gs in sg]
            dist = defaultdict(Fraction)
            if len(sg) <= 7:
                perms = list(itertools.permutations(range(len(sg))))
                for perm in perms:
                    w = sum(sizes[b] for b in perm[:perm.index(jb)])
                    for q in range(1, gsize + 1):
                        dist[pos + w + before_in_block + q] += Fraction(1, len(perms) * gsize)
            else:
                n = 20000
                for _ in range(n):
                    perm = list(range(len(sg))); rng.shuffle(perm)
                    w = sum(sizes[b] for b in perm[:perm.index(jb)])
                    for q in range(1, gsize + 1):
                        dist[pos + w + before_in_block + q] += Fraction(1, n * gsize)
            return dist, len(sg) > 7
        pos += sum(sum(len(g) for g in gs) for _, gs in sg)
        i = j + 1
    return {}, False


# ---------------------------------------------------------------- đọc mọi kết quả đã VERIFIED
rng = random.Random(1)
recs = defaultdict(list)       # (ds, oid, arm) -> list of (seed, rec)
jobs_text = []
for q in QUEUES:
    for vf in glob.glob(str(q / '*/attempt-*/verified.json')):
        d = Path(vf).parent
        job = json.loads((d / 'job.json').read_bytes())
        s = job['slot']
        if s['view'] != 'main' or s['arm'] == 'torai_A':
            continue
        v = json.loads(Path(vf).read_bytes())
        res = d / 'result.json'
        if sha(res) != v['result']['sha256']:
            raise SystemExit('hash result khác verified: ' + str(res))
        env = json.loads(res.read_bytes())
        for rec in env['records']:
            recs[(s['dataset'], s['opaque_id'], s['arm'])].append((s['seed'], rec))
        for name in ('job.json', 'invocation.json', 'launch.json'):
            if (d / name).exists():
                jobs_text.append((str(d / name), (d / name).read_text(encoding='utf-8', errors='replace')))

# ---------------------------------------------------------------- A1 chấm lại
tables = json.loads((T / 'reports/main-013-v2/tables.json').read_bytes())
rows = {(r['dataset'], r['opaque_id'], r['arm']): r for r in tables['rows'] if r['world'] == 'P'}
VARIANT = {'circa': 'ols+rht_da'}
a1 = {'rows_checked': 0, 'max_abs_diff': {}, 'mismatch': [], 'monte_carlo_cases': 0, 'by_arm': {}}
mine = {}
for key, lst in sorted(recs.items()):
    ds, oid, arm = key
    root = labels[(ds, oid)][0]
    per_seed = []
    for seed, rec in sorted(lst, key=lambda x: (x[0] is None, x[0] or 0)):
        if arm in VARIANT and rec.get('variant') != VARIANT[arm]:
            continue
        if rec['status'] != 'OK':
            per_seed.append(metrics_from_rank_dist({}))
            continue
        world = rec['worlds']['P'] if 'worlds' in rec else rec
        dist, mc = rank_dist(blocks_of(world), root, rng)
        a1['monte_carlo_cases'] += int(mc)
        per_seed.append(metrics_from_rank_dist(dist))
    m = {k: sum(x[k] for x in per_seed) / len(per_seed) for k in per_seed[0]}
    mine[key] = m
    r = rows.get(key)
    if r is None:
        a1['mismatch'].append({'key': list(key), 'why': 'không có trong tables'}); continue
    tm = {'rr': r['metrics']['rr'], 'hit@1': r['metrics']['hit@1'], 'hit@3': r['metrics']['hit@3'],
          'hit@5': r['metrics']['hit@5'], 'ndcg5': r['metrics']['ndcg@5']}
    a1['rows_checked'] += 1
    for k in tm:
        dlt = abs(tm[k] - m[k])
        a1['max_abs_diff'][k] = max(a1['max_abs_diff'].get(k, 0), dlt)
        if dlt > (2e-3 if False else 1e-9):
            a1['mismatch'].append({'key': list(key), 'metric': k, 'tables': tm[k], 'doc_lap': m[k]})
missing = [list(k) for k in rows if k not in mine and k[2] != 'torai_A' and k[2] not in ('C-d1', 'C-d2', 'C-d3', 'C-c', 'C-g', 'circa_rht_aux')]
a1['rows_in_tables_without_raw'] = missing
for (ds, oid, arm), m in mine.items():
    a1['by_arm'].setdefault(f'{ds}|{arm}', []).append(m['rr'])
a1['by_arm'] = {k: {'n': len(v), 'MRR_doc_lap': sum(v) / len(v)} for k, v in sorted(a1['by_arm'].items())}

# Kiểm lại đúng A4 bằng số độc lập.
def mean_delta(ds, a, b):
    ks = [o for (d, o) in labels if d == ds]
    return sum(mine[(ds, o, a)]['rr'] - mine[(ds, o, b)]['rr'] for o in ks) / len(ks)
a4 = json.loads((T / 'reports/main-013-v2/a4.json').read_bytes())
a1['A4_TT_delta'] = {'doc_lap': mean_delta('RE2-TT', 'M1', 'torai_B'),
                     'a4': a4['TT']['P']['delta']['phan_so'][0] / a4['TT']['P']['delta']['phan_so'][1]}
ob = [o for (d, o) in labels if d == 'Nezha-OB']
a1['A4_OB_delta_hit5'] = {'doc_lap': sum(mine[('Nezha-OB', o, 'M1')]['hit@5'] - mine[('Nezha-OB', o, 'simplerca')]['hit@5'] for o in ob) / len(ob),
                          'a4': a4['OB']['P']['delta']['phan_so'][0] / a4['OB']['P']['delta']['phan_so'][1]}

# ---------------------------------------------------------------- A2 thử giả
a2 = {}
for ds in ('RE2-TT', 'Nezha-OB'):
    oids = [o for (d, o) in labels if d == ds]
    for arm in sorted({k[2] for k in recs if k[0] == ds}):
        shuf, rand, alpha, single, n = [], [], [], 0, 0
        for o in oids:
            lst = [r for s, r in recs[(ds, o, arm)] if not (arm in VARIANT and r.get('variant') != VARIANT[arm])]
            ok = [r for r in lst if r['status'] == 'OK']
            if not ok:
                continue
            rec = ok[0]; world = rec['worlds']['P'] if 'worlds' in rec else rec
            bl = blocks_of(world)
            ents = [e for _, gs in bl for g in gs for e in g]
            n += 1
            if len(bl) == 1:
                single += 1
            others = sorted({labels[(ds, p)][0] for p in oids} - {labels[(ds, o)][0]})
            shuf.append(sum(metrics_from_rank_dist(rank_dist(bl, r, rng)[0])['rr'] for r in others) / len(others))
            root = labels[(ds, o)][0]
            rand.append((sum(1 / i for i in range(1, len(ents) + 1)) / len(ents)) if root in ents else 0.0)
            al = sorted(ents)
            alpha.append(1 / (al.index(root) + 1) if root in al else 0.0)
        a2[f'{ds}|{arm}'] = {'n_OK_seed0': n, 'MRR_xao_root': sum(shuf) / len(shuf) if shuf else None,
                             'MRR_ngau_nhien_deu': sum(rand) / len(rand) if rand else None,
                             'MRR_theo_chu_cai': sum(alpha) / len(alpha) if alpha else None,
                             'ban_ghi_mot_khoi_duy_nhat': single}

# ---------------------------------------------------------------- A3 rò nhãn
pat_cases = re.compile('|'.join(re.escape(c) for c in case_names))
pat_private = re.compile(r'RCA-ext[/\\]private|labels\.json|canonical-label')
pat_rootfault = re.compile('|'.join(re.escape(f'{r}_{f}') for (r, f) in set(labels.values())))
hits = Counter()
examples = []
for path, txt in jobs_text:
    for name, pat in (('case_name', pat_cases), ('private_path', pat_private), ('root_fault_token', pat_rootfault)):
        mm = pat.search(txt)
        if mm:
            hits[name] += 1
            if len(examples) < 10:
                examples.append({'file': os.path.relpath(path, ROOT).replace('\\', '/'), 'kind': name, 'match': mm.group(0)})
a3 = {'files_scanned': len(jobs_text), 'hits': dict(hits), 'examples': examples}

# ---------------------------------------------------------------- A5 số trong báo cáo
pt = json.loads((T / 'reports/p7a-013-v2/phan-tich-nhom.json').read_bytes())
claims = [
    ('TT M1 MRR 0,975', pt['bang_theo_ve_P']['RE2-TT|M1']['MRR']['xap_xi'], 0.975, 5e-4),
    ('TT TORAI B MRR 0,931', pt['bang_theo_ve_P']['RE2-TT|torai_B']['MRR']['xap_xi'], 0.931, 5e-4),
    ('TT C-a0 MRR 0,975', pt['bang_theo_ve_P']['RE2-TT|C-a0']['MRR']['xap_xi'], 0.975, 5e-4),
    ('TT bo-E1 MRR 0,882', pt['bang_theo_ve_P']['RE2-TT|bo-E1']['MRR']['xap_xi'], 0.882, 5e-4),
    ('OB M1 MRR 0,875', pt['bang_theo_ve_P']['Nezha-OB|M1']['MRR']['xap_xi'], 0.875, 5e-4),
    ('OB M4 MRR 0,689', pt['bang_theo_ve_P']['Nezha-OB|simplerca']['MRR']['xap_xi'], 0.689, 5e-4),
    ('OB C-a0 MRR 0,711', pt['bang_theo_ve_P']['Nezha-OB|C-a0']['MRR']['xap_xi'], 0.711, 5e-4),
    ('OB C-d2 MRR 0,878', pt['bang_theo_ve_P']['Nezha-OB|C-d2']['MRR']['xap_xi'], 0.878, 5e-4),
    ('TT ΔMRR 0,0440', a4['TT']['P']['delta']['phan_so'][0] / a4['TT']['P']['delta']['phan_so'][1], 0.0440, 5e-5),
    ('TT CI lo −0,033333333333', float(a4['TT']['P']['E04']['lo_12']), -0.033333333333, 1e-12),
    ('OB ΔHit@5 3/34', a4['OB']['P']['delta']['phan_so'][0] / a4['OB']['P']['delta']['phan_so'][1], 3 / 34, 1e-12),
    ('OB p 1/8', a4['OB']['P']['cell_sign_at_zero']['p_exact']['phan_so'][0] / a4['OB']['P']['cell_sign_at_zero']['p_exact']['phan_so'][1], 0.125, 1e-12),
    ('OB M1−C-a0 ΔRR 0,164', pt['so_cap']['Nezha-OB|M1-C-a0|RR']['delta_mean']['xap_xi'], 0.164, 5e-4),
    ('OB M1−bo-E2 ΔRR 0,115', pt['so_cap']['Nezha-OB|M1-bo-E2|RR']['delta_mean']['xap_xi'], 0.115, 5e-4),
    ('OB M1−C-d2 ΔRR −0,0025', pt['so_cap']['Nezha-OB|M1-C-d2|RR']['delta_mean']['xap_xi'], -0.0025, 5e-5),
    ('TT M1−bo-E1 ΔRR 0,093', pt['so_cap']['RE2-TT|M1-bo-E1|RR']['delta_mean']['xap_xi'], 0.093, 5e-4),
]
a5 = [{'claim': c, 'file_value': v, 'report_value': rv, 'ok': abs(v - rv) <= tol} for c, v, rv, tol in claims]
# Số MRR theo vế trong bảng báo cáo khớp số chấm độc lập (A1) tới 3 chữ số.
for k, v in a1['by_arm'].items():
    if k in pt['bang_theo_ve_P']:
        a5.append({'claim': 'bảng §4 ' + k, 'file_value': v['MRR_doc_lap'],
                   'report_value': round(pt['bang_theo_ve_P'][k]['MRR']['xap_xi'], 3),
                   'ok': abs(round(v['MRR_doc_lap'], 3) - round(pt['bang_theo_ve_P'][k]['MRR']['xap_xi'], 3)) < 1e-9})

out = {'schema': 'T054-KIEM-TOAN-VEN-1', 'inputs': {
    'tables': sha(T / 'reports/main-013-v2/tables.json'), 'a4': sha(T / 'reports/main-013-v2/a4.json'),
    'phan_tich_nhom': sha(T / 'reports/p7a-013-v2/phan-tich-nhom.json'),
    'g1': sha(ROOT / 'results/T-021/chia-theo-o/A-phan-tang.csv')},
    'A1_cham_lai_doc_lap': a1, 'A2_thu_gia': a2, 'A3_ro_nhan': a3, 'A5_so_bao_cao': a5,
    'A5_fail': [x for x in a5 if not x['ok']]}
with open(OUT, 'x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
print(json.dumps({'A1_rows': a1['rows_checked'], 'A1_mismatch': len(a1['mismatch']), 'A1_maxdiff': a1['max_abs_diff'],
                  'A1_missing_raw': len(missing), 'A4': [a1['A4_TT_delta'], a1['A4_OB_delta_hit5']],
                  'A3': a3['hits'], 'A5_fail': out['A5_fail']}, ensure_ascii=False, indent=0))
