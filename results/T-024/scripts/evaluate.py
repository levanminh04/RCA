"""T-024: chấm manifest đã chốt, không chạy hoặc chọn lại phương pháp.

Chạy bằng môi trường T-014-main, Python -B, sau dòng LOG chốt manifest:
    python -B results/T-024/scripts/evaluate.py --confirm-frozen

Chỉ đọc nhãn sau khi đã kiểm manifest, hash mã, hash và cohort mọi bản ghi.
Không sửa src/p3 hoặc các đầu ra T-022/T-030/T-031. Đầu ra mới phải chưa tồn tại.
"""
import argparse
import copy
import hashlib
import itertools
import json
import math
import os
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-024'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ.setdefault('MPLCONFIGDIR', str(OUT / 'work/matplotlib'))
sys.path.insert(0, str(ROOT / 'src'))

METRICS = tuple(f'hit@{k}' for k in range(1, 11)) + ('rr', 'ndcg@5', 'avg@5')
SIDE_METRICS = METRICS
PRIMARY = ('baro', 'simplerca', 'tracerca', 'microrank_full', 'circa_ols_da', 'torai_B')
NAMES = {
    'baro': 'BARO', 'simplerca': 'SimpleRCA M4', 'tracerca': 'TraceRCA lọc hữu hạn',
    'microrank_full': 'MicroRank xếp đầy đủ', 'microrank_top11': 'MicroRank top11',
    'circa_ols_da': 'CIRCA kiến trúc, OLS+RHT+DA, cấu hình P3',
    'circa_ols_rht': 'CIRCA kiến trúc, OLS+RHT-only, cấu hình P3',
    'circa_svr_da': 'CIRCA kiến trúc, SVR(sigmoid)+RHT+DA, cấu hình phụ',
    'circa_svr_rht': 'CIRCA kiến trúc, SVR(sigmoid)+RHT-only, cấu hình phụ',
    'torai_B': 'TORAI sửa, nguồn B', 'torai_A': 'TORAI sửa, nguồn A (hồi cứu)',
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def rel(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def local(path):
    p = (ROOT / path).resolve()
    p.relative_to(ROOT)
    if 'locked' in p.relative_to(ROOT).parts:
        raise ValueError('Không được đọc data/locked')
    return p


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def code_hash():
    h = hashlib.sha256()
    files = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'src/p3').rglob('*.py'))
    for name in files:
        h.update((ROOT / name).read_bytes())
    return h.hexdigest()


def method_id(rec):
    m, v = rec['method'], rec['variant']
    if m in ('baro', 'simplerca', 'tracerca'):
        return m
    if m == 'microrank' and v == 'full':
        return 'microrank_full'
    if m == 'circa':
        model, scorer = v.split('+', 1)
        if model in ('ols', 'svr') and scorer in ('rht_da', 'rht'):
            return f'circa_{model}_{"da" if scorer == "rht_da" else "rht"}'
    if m == 'torai' and v in ('A', 'B'):
        return 'torai_' + v
    raise ValueError(f'Phương pháp/biến thể ngoài SPEC: {m}/{v}')


def top11_record(rec):
    """Giữ thứ tự service_ranks_top11; điểm cao nhất lấy từ full, không chạy lại."""
    r = copy.deepcopy(rec)
    r['variant'] = 'top11-derived'
    if r['status'] != 'OK':
        r.update(ranking_native=[], ranking=[], entity_ranking=[], blocks=None)
        return r
    services = rec.get('extra', {}).get('service_ranks_top11')
    native = rec.get('extra', {}).get('top11_ranks')
    if services is None or native is None:
        raise ValueError('MicroRank OK thiếu đầu ra top11 gốc')
    if len(services) != len(set(services)):
        raise ValueError('MicroRank service_ranks_top11 trùng thực thể')
    by_item = {row['item']: row for row in rec['ranking']}
    items = [by_item[name] for name in native]
    from p3.ban_ghi import xep_thuc_the
    rows = xep_thuc_the([(x['item'], x['entity'], x['key']) for x in items])
    if [x['entity'] for x in rows] != services:
        raise ValueError('MicroRank top11 dẫn xuất lệch service_ranks_top11 của code gốc')
    r.update(ranking_native=list(native), ranking=items, entity_ranking=rows, blocks=None)
    r['sets']['returned'] = len(rows)
    return r


def load_frozen(path):
    doc = read_json(path)
    if not doc.get('frozen_at') or not doc.get('records'):
        raise ValueError('Manifest chưa chốt hoặc rỗng')
    expected = doc['src_p3_sha256']
    if code_hash() != expected:
        raise ValueError('Hash src/p3 đã đổi; không được dùng lại bản ghi T-031')
    allow = read_json(ROOT / 'results/T-022/allowlist-dev.json')
    ids = {x['opaque_id'] for x in allow['cases']}
    if len(ids) != 30 or allow['so_ca'] != 30:
        raise ValueError('Allowlist không đúng 30 ca')
    records, metas, seen = {}, {}, set()
    for meta in doc['records']:
        p = local(meta['path'])
        if meta['src_p3_sha256'] != expected or sha(p) != meta['sha256']:
            raise ValueError(f'Hash bản ghi/mã lệch manifest: {meta["path"]}')
        rec = read_json(p)
        for key in ('method', 'variant', 'seed', 'opaque_id'):
            if rec.get(key) != meta.get(key):
                raise ValueError(f'Manifest lệch {key}: {meta["path"]}')
        if rec['mode'] != 'a' or rec['opaque_id'] not in ids:
            raise ValueError('Bản ghi ngoài chế độ (a) hoặc allowlist')
        if 'observed_entities' not in rec.get('sets', {}):
            raise ValueError(f'Bản ghi thiếu O đã đo: {meta["path"]}; dừng trước bảng khoa học')
        cfg_path = local(meta['source_config'])
        if meta.get('source_config_sha256') and sha(cfg_path) != meta['source_config_sha256']:
            raise ValueError(f'Hash tệp cấu hình đổi sau chốt: {meta["source_config"]}')
        cfg = read_json(cfg_path)
        cfg_hash = cfg.get('src_p3', {}).get('tong', cfg.get('src_p3_sha256'))
        if cfg_hash != expected:
            raise ValueError(f'Hash cấu hình run lệch manifest: {meta["source_config"]}')
        mid = method_id(rec)
        sk = 'single' if rec.get('seed') is None else str(rec['seed'])
        key = (mid, sk, rec['opaque_id'])
        if key in seen:
            raise ValueError(f'Bản ghi trùng: {key}')
        seen.add(key)
        records.setdefault(mid, {}).setdefault(sk, {})[rec['opaque_id']] = rec
        metas.setdefault(mid, []).append(meta)
    expected_methods = set(NAMES) - {'microrank_top11'}
    if set(records) != expected_methods:
        raise ValueError(f'Không đủ biến thể: thiếu {expected_methods-set(records)}; dư {set(records)-expected_methods}')
    for mid, seeds in records.items():
        wanted = {'0', '1', '2'} if mid.startswith('torai_') else {'single'}
        if set(seeds) != wanted or any(set(rr) != ids for rr in seeds.values()):
            raise ValueError(f'Không đủ 30 ca/seed: {mid}')
    if not any(d.get('id') == 'microrank_top11' and d.get('source_variant') == 'full'
               for d in doc.get('derived', [])):
        raise ValueError('Manifest chưa khai phép dẫn xuất top11')
    records['microrank_top11'] = {'single': {o: top11_record(r)
                                                  for o, r in records['microrank_full']['single'].items()}}
    metas['microrank_top11'] = metas['microrank_full']
    return doc, allow, records, metas


def average_cases(ds):
    """Trung bình độ đo theo seed; status mixed giữ tường minh, không bỏ lượt lỗi."""
    n = len(ds)
    out = {k: sum(d[k] for d in ds) / n for k in METRICS}
    for side in ('opt', 'pes'):
        out[side] = {k: sum((d[side] or {}).get(k, 0.0) for d in ds) / n for k in SIDE_METRICS}
    statuses = {d['status'] for d in ds}
    out['status'] = next(iter(statuses)) if len(statuses) == 1 else 'MIXED_SEEDS'
    out['status_by_seed_counts'] = dict(Counter(d['status'] for d in ds))
    out['root_trong_tra_ve'] = all(d['root_trong_tra_ve'] for d in ds)
    out['root_returned_seed_fraction'] = sum(d['root_trong_tra_ve'] for d in ds) / n
    mins = [d['rank_min'] for d in ds if d['rank_min'] is not None]
    maxs = [d['rank_max'] for d in ds if d['rank_max'] is not None]
    out['rank_min'] = min(mins) if mins else None
    out['rank_max'] = max(maxs) if maxs else None
    return out


def summary_main(per, dg):
    out = dg.tong_hop(per)
    if any(d['status'] == 'MIXED_SEEDS' for d in per.values()):
        out['trang_thai']['MIXED_SEEDS'] = sum(d['status'] == 'MIXED_SEEDS' for d in per.values())
    assert out['n'] == len(per)
    assert sum(out['trang_thai'].values()) == len(per)
    return out


def mean_tables(tables):
    keys = next(iter(tables.values())).keys()
    out = {}
    for k in keys:
        vals = [t[k] for t in tables.values()]
        out[k] = None if any(v is None for v in vals) else sum(vals) / len(vals)
    out['n'] = next(iter(tables.values()))['n']
    # RCAEval cũng định nghĩa Rerank bằng tỉ số AC/ Retrieval gộp.
    # Cohort cùng cỡ qua seed: trung bình AC và Retrieval trước khi chia.
    for K in (5, 10):
        den = out[f'retrieval_service({K})']
        out[f'rerank_service(1,{K})'] = out['AC@1'] / den if den else None
    return out


def diag_summary(seeds, ids, paths):
    routes, with_fallback, big_cases = Counter(), set(), set()
    fallback_nodes = big_nodes = clusters = multi = fallback_clusters = 0
    n_nodes, n_edges = [], []
    for rr in seeds.values():
        for oid in ids:
            d = rr[oid].get('diagnostics') or {}
            routes.update(d.get('regression_routes') or {})
            nodes = d.get('nodes') or {}
            vf = [name for name, node in nodes.items()
                  if node.get('regression_route') == 'value_error_fallback']
            if 'value_error_fallback_nodes' in d and nodes:
                assert len(vf) == len(d.get('value_error_fallback_nodes') or [])
            if not nodes:
                vf = d.get('value_error_fallback_nodes') or []
            fallback_nodes += len(vf)
            if vf:
                with_fallback.add(oid)
            bn = sum(float(v.get('rht_score', 0)) > 1e10 for v in nodes.values())
            big_nodes += bn
            if bn:
                big_cases.add(oid)
            gr = d.get('graph') or {}
            if gr.get('metric_nodes') is not None:
                n_nodes.append(gr['metric_nodes'])
            if gr.get('metric_edges') is not None:
                n_edges.append(gr['metric_edges'])
            clusters += d.get('cum', 0)
            multi += d.get('cum_nhieu_service', 0)
            fallback_clusters += d.get('cum_du_phong', 0)
    return {'n_cases': len(ids), 'n_records': len(seeds) * len(ids), 'regression_routes': dict(routes),
            'value_error_fallback_nodes_n': fallback_nodes,
            'cases_with_value_error_fallback': sorted(with_fallback),
            'rht_gt_1e10_nodes_n': big_nodes, 'cases_with_rht_gt_1e10': sorted(big_cases),
            'graph': {'metric_nodes_min': min(n_nodes) if n_nodes else None,
                      'metric_nodes_max': max(n_nodes) if n_nodes else None,
                      'metric_edges_min': min(n_edges) if n_edges else None,
                      'metric_edges_max': max(n_edges) if n_edges else None},
            'torai': {'clusters': clusters, 'multi_service_clusters': multi,
                      'fallback_clusters': fallback_clusters,
                      'fallback_rate': fallback_clusters / multi if multi else None},
            'source_paths': paths}


def cost_summary(mid, seeds, ids, metas):
    """Chi phí từ bản ghi đã chốt, không lấy thời gian phiên có lúc nghỉ làm benchmark."""
    selected = [rr[o] for rr in seeds.values() for o in ids]
    walls = [r.get('cost', {}).get('wall_s') for r in selected]
    walls = [float(v) for v in walls if v is not None]
    rss = [r.get('cost', {}).get('peak_rss_mb') for r in selected]
    rss = [float(v) for v in rss if v is not None]
    worker_wall = [float(p['wall_s']) for r in selected
                   for p in r.get('cost', {}).get('tien_trinh', []) if p.get('wall_s') is not None]
    configs = sorted({m['source_config'] for m in metas if m['opaque_id'] in ids})
    platforms = sorted({str(read_json(local(p)).get('may')) for p in configs
                        if read_json(local(p)).get('may') is not None})
    return {'n_cases': len(ids), 'n_records': len(selected),
            'n_distinct_run_ids': len({r['run_id'] for r in selected}),
            'recorded_wall_s_n': len(walls), 'recorded_wall_s_sum': sum(walls),
            'recorded_wall_s_min': min(walls) if walls else None,
            'recorded_wall_s_max': max(walls) if walls else None,
            'recorded_wall_s_median': statistics.median(walls) if walls else None,
            'worker_process_wall_s_n': len(worker_wall),
            'worker_process_wall_s_sum': sum(worker_wall),
            'worker_process_wall_s_min': min(worker_wall) if worker_wall else None,
            'worker_process_wall_s_max': max(worker_wall) if worker_wall else None,
            'peak_rss_mb_max': max(rss) if rss else None,
            'execution_host': {'category': 'EC2' if mid.startswith('torai_') else 'Windows laptop',
                               'recorded_platforms': platforms,
                               'source': 'SPEC T-024: bản ghi TORAI chạy EC2 ở T-031; phương pháp khác chạy laptop.'},
            'source_configs': configs,
            'source_paths': sorted({m['path'] for m in metas if m['opaque_id'] in ids}),
            'note': 'Chi phí cost.wall_s và cost.tien_trinh của từng lượt. CIRCA DA/RHT chia sẻ lượt; MicroRank full/top11 chia sẻ lượt; không cộng qua các biến thể. Không so tốc độ TORAI EC2 với laptop, không dùng thời gian phiên/test có lúc nghỉ làm benchmark.'}


def raw_audit(records, metas):
    rr = records['circa_ols_da']['single']
    source = {x['opaque_id']: x for x in metas['circa_ols_da']}
    columns = {o: r['input_shape'].get('metric_columns') for o, r in rr.items()}
    if any(v is None for v in columns.values()):
        raise ValueError('Thiếu danh sách cột raw trong bản ghi đã chốt')
    union = sorted({c for cc in columns.values() for c in cc})
    cases = {}
    for o, cc in sorted(columns.items()):
        missing = sorted(set(union) - set(cc))
        cases[o] = {'n_columns': len(cc), 'columns': cc, 'missing_from_union': missing,
                    'n_missing': len(missing), 'source_path': source[o]['path'],
                    'source_sha256': source[o]['sha256']}
    return {'union_columns': union, 'union_n': len(union), 'by_case': cases,
            'note': 'Cột metric thô, bỏ time; runner ghi read_columns trước tiền xử lý, worker.py:63, runner.py:196.'}


def independent_dist(rec, root):
    """Kiểm tay: nhóm phẳng tính trực tiếp; TORAI liệt kê hoán vị khối, độc lập DP."""
    if rec['status'] != 'OK':
        return {}, 'Trạng thái khác OK: hạng vô cùng, mọi độ đo 0.'
    blocks = rec.get('blocks')
    if blocks is None:
        rows = rec['entity_ranking']
        for i, r in enumerate(rows):
            if r['entity'] == root:
                grp = r['tie_group']
                ranks = [j+1 for j, x in enumerate(rows) if x['tie_group'] == grp]
                return {p: Fraction(1, len(ranks)) for p in ranks}, f'Nhóm hòa hạng {ranks}: xác suất 1/{len(ranks)} mỗi hạng.'
        return {}, 'Root không được trả về: mọi độ đo 0.'
    pos, i = 0, 0
    while i < len(blocks):
        j = i + 1
        while j < len(blocks) and blocks[j]['key'] == blocks[i]['key']:
            j += 1
        same = blocks[i:j]
        target = next((b for b in same if any(root in g for g in b['groups'])), None)
        if target is not None:
            if len(same) > 9:
                raise ValueError('Phép tính tay >9 khối hòa; cần kiểm độc lập khác trước báo cáo')
            inner, before = [], 0
            for grp in target['groups']:
                if root in grp:
                    inner = list(range(before+1, before+len(grp)+1))
                    break
                before += len(grp)
            counts = Counter()
            total = math.factorial(len(same)) * len(inner)
            for perm in itertools.permutations(range(len(same))):
                ahead = 0
                for bidx in perm:
                    if same[bidx] is target:
                        for p in inner:
                            counts[pos+ahead+p] += 1
                        break
                    ahead += sum(len(g) for g in same[bidx]['groups'])
            return {r: Fraction(c, total) for r, c in sorted(counts.items())}, f'Liệt kê {math.factorial(len(same))} hoán vị của {len(same)} khối cùng điểm; {len(inner)} vị trí nội khối.'
        pos += sum(len(g) for b in same for g in b['groups'])
        i = j
    return {}, 'Root không được trả về: mọi độ đo 0.'


def manual_metrics(dist):
    out = {f'hit@{k}': float(sum(p for r, p in dist.items() if r <= k)) for k in range(1, 11)}
    out['rr'] = float(sum(p/r for r, p in dist.items()))
    out['ndcg@5'] = sum(float(p)/math.log2(1+r) for r, p in dist.items() if r <= 5)
    out['avg@5'] = sum(out[f'hit@{k}'] for k in range(1, 6))/5
    return out


def torai_tie_census(records, methods):
    """Đếm hòa khóa chính xác trên mọi cặp khối của 180 bản ghi đã chốt."""
    total = Counter(source_records=0, records_with_equal_blocks=0, equal_block_pairs=0,
                    records_with_inner_ties=0, blocks_total=0)
    by_source_seed, paths = {}, []
    for mid in ('torai_A', 'torai_B'):
        by_source_seed[mid[-1]] = {}
        for seed, rr in records[mid].items():
            stats = Counter(source_records=0, records_with_equal_blocks=0, equal_block_pairs=0,
                            records_with_inner_ties=0, blocks_total=0)
            for rec in rr.values():
                blocks = rec.get('blocks') or []
                pairs = sum(blocks[i]['key'] == blocks[j]['key']
                            for i in range(len(blocks)) for j in range(i+1, len(blocks)))
                stats.update(source_records=1, records_with_equal_blocks=int(pairs > 0),
                             equal_block_pairs=pairs,
                             records_with_inner_ties=int(any(len(g)>1 for b in blocks for g in b['groups'])),
                             blocks_total=len(blocks))
            by_source_seed[mid[-1]][seed] = dict(stats)
            total.update(stats)
        paths.extend(m['path'] for m in methods[mid]['source_records'])
    assert total['source_records'] == 180
    return {**dict(total), 'by_source_seed': by_source_seed,
            'comparison': 'Exact key equality, every block pair; no rounding or tolerance.',
            'source_paths': sorted(paths)}


def torai_block_fixture(dg):
    """Ví dụ AB/CD chỉ kiểm công thức V2-R2, không thuộc manifest hoặc cohort."""
    rec = {'status': 'OK', 'blocks': [{'key': [0.5], 'groups': [['A'], ['B']]},
                                     {'key': [0.5], 'groups': [['C'], ['D']]}]}
    root = 'A'
    dist, calculation = independent_dist(rec, root)
    expected_dist = {1: Fraction(1, 2), 3: Fraction(1, 2)}
    assert dist == expected_dist
    manual = manual_metrics(expected_dist)
    manual.update(opt=manual_metrics({1: Fraction(1)}), pes=manual_metrics({3: Fraction(1)}),
                  rank_min=1, rank_max=3)
    got = dg.cham_ca(rec, root)
    assert manual['hit@1'] == 1/2 and manual['rr'] == 2/3 and manual['avg@5'] == 4/5
    assert all(math.isclose(manual[k], got[k], abs_tol=1e-12, rel_tol=1e-12) for k in METRICS)
    for side in ('opt', 'pes'):
        assert all(math.isclose(manual[side][k], got[side][k], abs_tol=1e-12, rel_tol=1e-12)
                   for k in SIDE_METRICS)
    assert (got['rank_min'], got['rank_max']) == (1, 3)
    assert dg.phan_bo_hang(dg.khoi_tu_ban_ghi(rec), root) == expected_dist
    return {'kind': 'synthetic_validation_only', 'record': rec, 'root': root,
            'rank_distribution': {str(r): str(p) for r, p in expected_dist.items()},
            'manual': manual, 'evaluator': got, 'calculation': calculation, 'pass': True,
            'excluded_from_cohort': True,
            'reason': '180 bản ghi TORAI A/B đã chốt không có hòa khối. Minh duyệt SPEC:62: kiểm V2-R2 bằng fixture riêng trong validation; không đưa vào manifest, bảng khoa học hoặc bootstrap.'}


def manual_checks(records, methods, labels, universe, dg):
    choices = []
    flat = [(mid, sk, o, r) for mid in PRIMARY if not mid.startswith('torai')
            for sk, rr in records[mid].items() for o, r in sorted(rr.items()) if r['status'] == 'OK']
    tied = [(m, s, o, r) for m, s, o, r in flat
            if len(independent_dist(r, labels[o]['root'])[0]) > 1]
    if not tied:
        tied = [(m, s, o, r) for m, s, o, r in flat
                if len({x['tie_group'] for x in r['entity_ranking']}) < len(r['entity_ranking'])]
    if not tied:
        raise ValueError('Không tìm được ca có hòa ở phương pháp khóa đơn để kiểm theo SPEC')
    choices.append(('flat_tie', tied[0]))
    choices.append(('flat_other', next(x for x in flat if x[2] != tied[0][2])))
    used_oids = {x[1][2] for x in choices}
    tb = [('torai_B', sk, o, r) for sk, rr in records['torai_B'].items() for o, r in sorted(rr.items())
          if o not in used_oids and r['status'] == 'OK']
    if not tb:
        raise ValueError('Không tìm được ca TORAI dev khác hai ca đã chọn để kiểm theo SPEC')
    with_root_tie = [x for x in tb if len(independent_dist(x[3], labels[x[2]]['root'])[0]) > 1]
    choices.append(('torai_dev', (with_root_tie or tb)[0]))
    assert len({x[1][2] for x in choices}) >= 3
    checks = []
    for kind, (mid, sk, oid, rec) in choices:
        dist, calculation = independent_dist(rec, labels[oid]['root'])
        want = manual_metrics(dist)
        got = methods[mid]['per_case'][oid]['seed_metrics'][sk]
        assert all(math.isclose(want[k], got[k], abs_tol=1e-12, rel_tol=1e-12) for k in METRICS)
        checks.append({'kind': kind, 'method': mid, 'seed': sk, 'opaque_id': oid,
                       'root': labels[oid]['root'], 'calculation': calculation,
                       'rank_distribution': {str(r): str(p) for r, p in dist.items()},
                       'manual': want, 'evaluator': {k: got[k] for k in METRICS}, 'pass': True,
                       'source_paths': methods[mid]['per_case'][oid]['source_paths']})
    m, sk, oid, rec = choices[0][1]
    O = rec['sets']['observed_entities']
    root = labels[oid]['root']
    random = {f'O_hit@{k}': min(k, len(O))/len(O) if O and root in O else 0.0 for k in (1,3,5,10)}
    assert all(math.isclose(v, methods[m]['per_case'][oid]['random']['by_seed'][sk][k], abs_tol=1e-12)
               for k, v in random.items())
    u_hit5 = min(5, len(universe))/len(universe) if universe and root in universe else 0.0
    assert math.isclose(u_hit5, methods[m]['per_case'][oid]['random']['by_seed'][sk]['U_hit@5'], abs_tol=1e-12)
    census = torai_tie_census(records, methods)
    result = {'rank_checks': checks, 'random_check': {'method': m, 'opaque_id': oid, 'O_size': len(O),
              'root_in_O': root in O, 'formula': 'min(k,|O|)/|O| nếu root thuộc O; ngược lại 0',
              'manual': random, 'U_size': len(universe), 'U_hit@5': u_hit5, 'pass': True},
              'torai_cohort_ties': census}
    if census['records_with_equal_blocks'] == 0:
        result['torai_block_fixture'] = torai_block_fixture(dg)
    return result


def run(manifest_path, output_path, check_path):
    manifest, allow, records, metas = load_frozen(manifest_path)
    # Đây là chỗ đầu tiên import evaluator và đọc nhãn; manifest đã được kiểm ở trên.
    from p3 import danh_gia as dg, nhan
    labels = nhan.nap_nhan(ROOT / 'results/T-022/nhan-dev.json')
    universe = read_json(ROOT / 'results/T-022/mappings/universe-re2tt-dev.json')['U']
    ids = sorted(x['opaque_id'] for x in allow['cases'])
    if set(labels) != set(ids) or len(universe) != 68:
        raise ValueError('Nhãn/universe không khớp cohort đã chốt')
    excluded_doc = read_json(ROOT / 'results/T-031/kiem-11-ca-hashseed.json')
    excluded = excluded_doc['theo_hashseed']['0']['ca']
    assert len(excluded) == 11 and set(excluded) <= set(ids)
    cohorts = {'dev30': ids, 'dev19': [o for o in ids if o not in excluded]}
    methods, parity_checks = {}, []
    for mid in NAMES:
        print(f'Chấm {mid}', flush=True)
        seeds = records[mid]
        scored = {s: {o: dg.cham_ca(r, labels[o]['root']) for o, r in rr.items()} for s, rr in seeds.items()}
        per = {}
        for oid in ids:
            ds = [rr[oid] for rr in scored.values()]
            pc = average_cases(ds)
            random = {s: dg.muc_ngau_nhien(rr[oid], labels[oid]['root'], universe) for s, rr in seeds.items()}
            four = {s: dg.bon_tap(rr[oid], universe) for s, rr in seeds.items()}
            pc.update(label=labels[oid], seed_metrics={s: rr[oid] for s, rr in scored.items()},
                      source_paths=[m['path'] for m in metas[mid] if m['opaque_id'] == oid],
                      rank_distribution_by_seed={s: {str(k): str(v) for k, v in dg.phan_bo_hang(dg.khoi_tu_ban_ghi(rr[oid]), labels[oid]['root']).items()}
                                                 if rr[oid]['status'] == 'OK' else {} for s, rr in seeds.items()},
                      random={'by_seed': random, 'mean': {k: sum(x[k] for x in random.values())/len(random) for k in next(iter(random.values()))}},
                      four_sets={'by_seed': four, 'mean': {k: sum(x[k] for x in four.values())/len(four) for k in ('inventory','quan_sat','cham','tra_ve')},
                                 'outside_U_union': {k: sorted({e for f in four.values() for e in f[k+'_ngoai_U']}) for k in ('quan_sat','tra_ve')}},
                      diagnostics={s: {k: v for k, v in (rr[oid].get('diagnostics') or {}).items() if k != 'nodes'} for s, rr in seeds.items()},
                      cost_by_seed={s: rr[oid].get('cost', {}) for s, rr in seeds.items()})
            per[oid] = pc
        summary, seed_range = {}, {}
        for cohort, co in cohorts.items():
            sub = {o: per[o] for o in co}
            main = summary_main(sub, dg)
            tables = {s: dg.bang_rcaeval({o: rr[o] for o in co}, labels) for s, rr in seeds.items()}
            paths = sorted({p for o in co for p in per[o]['source_paths']})
            rand = {'n': len(co), **{k: sum(per[o]['random']['mean'][k] for o in co)/len(co)
                                    for k in ('O_hit@1','O_hit@3','O_hit@5','O_hit@10','U_hit@1','U_hit@3','U_hit@5','U_hit@10')},
                    'O_size_mean': sum(per[o]['random']['mean']['O_size'] for o in co)/len(co),
                    'root_coverage_O': sum(per[o]['random']['mean']['root_trong_O'] for o in co)/len(co),
                    'root_coverage_returned': sum(per[o]['root_returned_seed_fraction'] for o in co)/len(co),
                    'source_paths': paths}
            grouped = {}
            for field in ('fault','cell','nhom_vi_tri_p75'):
                grouped[field] = {str(g): summary_main({o: per[o] for o in co if labels[o][field] == g}, dg)
                                  for g in sorted({labels[o][field] for o in co})}
            summary[cohort] = {'main': main, 'rcaeval': {'mean': mean_tables(tables), 'by_seed': tables,
                                'note': 'Thứ tự gốc, bỏ trùng; không dùng để kết luận khi hòa. Nhiều seed: trung bình AC/Avg/Retrieval, Rerank tính từ AC/Retrieval gộp; kèm bảng từng seed.'},
                              'random': rand, 'grouped': grouped,
                              'status_source_runs': dict(Counter(rr[o]['status'] for rr in seeds.values() for o in co)),
                              'diagnostics': diag_summary(seeds, co, paths),
                              'cost_summary': cost_summary(mid, seeds, co, metas[mid]), 'source_paths': paths}
            by_seed = {s: summary_main({o: rr[o] for o in co}, dg) for s, rr in scored.items()}
            metric_keys = ('hit@1','hit@3','hit@5','avg@5','mrr','ndcg@5','retrieval@5','retrieval@10','rerank@1(K=5)','rerank@1(K=10)')
            ranges = {}
            for k in metric_keys:
                vs = {s: t[k] for s, t in by_seed.items()}
                finite = [x for x in vs.values() if x is not None]
                ranges[k] = {'min': min(finite) if finite else None, 'max': max(finite) if finite else None, 'by_seed': vs}
            seed_range[cohort] = {'by_seed': by_seed, 'range': ranges}
        methods[mid] = {'name': NAMES[mid], 'primary': mid in PRIMARY, 'source_records': metas[mid],
                        'per_case': per, 'summaries': summary, 'seed_range': seed_range}
        for sk, rr in seeds.items():
            for oid, rec in sorted(rr.items()):
                blocks = dg.khoi_tu_ban_ghi(rec) if rec['status'] == 'OK' else []
                tied = any(len(g)>1 for b in blocks for g in b['groups']) or any(a['key']==b['key'] for a,b in zip(blocks,blocks[1:]))
                if not tied:
                    theirs = dg.bang_rcaeval({oid: rec}, labels)
                    for k in (1,3,5):
                        if not math.isclose(scored[sk][oid][f'hit@{k}'], theirs[f'AC@{k}'], abs_tol=1e-12):
                            raise ValueError(f'RCAEval không hòa lệch {mid}/{sk}/{oid}/k{k}')
                    parity_checks.append({'method': mid, 'seed': sk, 'opaque_id': oid, 'pass': True})
                if rec['status'] != 'OK':
                    assert all(scored[sk][oid][k] == 0 for k in METRICS)
    boots = {}
    for cohort, co in cohorts.items():
        cells = {o: labels[o]['cell'] for o in co}
        bang = {m: {o: methods[m]['per_case'][o] for o in co} for m in NAMES}
        print(f'Bootstrap {cohort}, B=10000, seed=20261005; kiểm lặp lại', flush=True)
        a = dg.bootstrap(bang, cells, B=10_000, seed=20261005)
        b = dg.bootstrap(bang, cells, B=10_000, seed=20261005)
        if a != b:
            raise ValueError('Bootstrap cùng seed không giống hệt')
        boots[cohort] = a
    checks = manual_checks(records, methods, labels, universe, dg)
    # Phép thử giả rẻ: đổi nhãn root giữa ca, chỉ ở evaluator, cùng phép hoán vị cho mọi phương pháp.
    import numpy as np
    perm = np.random.default_rng(20261005).permutation(len(ids)).tolist()
    fake_roots = {o: labels[ids[perm[i]]]['root'] for i,o in enumerate(ids)}
    shuffled = {}
    for mid, seeds in records.items():
        avg = {o: average_cases([dg.cham_ca(rr[o], fake_roots[o]) for rr in seeds.values()]) for o in ids}
        shuffled[mid] = summary_main(avg, dg)
    checks.update(bootstrap_same_seed_exact={'dev30': True, 'dev19': True},
                  rcaeval_no_tie_parity={'n_checked': len(parity_checks), 'cases': parity_checks},
                  non_OK_in_denominator=True,
                  shuffled_root_check={'seed': 20261005, 'permutation_case_ids': [ids[j] for j in perm],
                                       'root_unchanged_n': sum(fake_roots[o] == labels[o]['root'] for o in ids),
                                       'summaries': shuffled, 'note': 'Phép thử giả, không dùng chọn cấu hình hoặc chạy lại phương pháp.'})
    sources = {'manifest': rel(manifest_path), 'manifest_sha256': sha(manifest_path),
               'labels': 'results/T-022/nhan-dev.json', 'allowlist': 'results/T-022/allowlist-dev.json',
               'universe': 'results/T-022/mappings/universe-re2tt-dev.json',
               'excluded_cases': 'results/T-031/kiem-11-ca-hashseed.json',
               'protocol': 'results/T-022/giao-thuc-v2.md', 'config': 'results/T-022/cau-hinh/p3-re2tt-v2.json',
               'evaluator': 'src/p3/danh_gia.py', 'script': rel(__file__), 'script_sha256': sha(__file__),
               'src_p3_sha256': manifest['src_p3_sha256'], 'frozen_at': manifest['frozen_at']}
    result = {'schema_version': 1, 'mode': 'a', 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
              'sources': sources,
              'definitions': {'main_methods': list(PRIMARY), 'seed_aggregation': 'Trung bình độ đo từng ca trước bootstrap; Rerank là tỉ số tổng Hit.',
                              'bounds': 'Chỉ độ đo đơn điệu, không cận Rerank.',
                              'mode_limit': 'Biết đúng mốc tiêm; nguồn TORAI A chỉ có sau cuối file.'},
              'cohorts': {k: {'case_ids': co, 'n_cases': len(co), 'n_cells': len({labels[o]['cell'] for o in co}),
                               **({'excluded_case_ids': excluded, 'selection_note': '19 ca chọn từ đầu ra CIRCA, không phải mẫu ngẫu nhiên; cùng tập cho mọi phương pháp, WHY-36.'} if k == 'dev19' else {})}
                          for k, co in cohorts.items()},
              'methods': methods, 'bootstrap': boots, 'raw_column_audit': raw_audit(records, metas), 'validation': checks}
    payload = json.dumps(result, ensure_ascii=False, indent=1, allow_nan=False)
    check_payload = json.dumps({'sources': sources, **checks}, ensure_ascii=False, indent=1, allow_nan=False)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    check_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(payload + '\n')
    with check_path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(check_payload + '\n')
    print(f'Đã ghi {rel(output_path)} và {rel(check_path)}; JSON strict, bootstrap lặp khớp.', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--confirm-frozen', action='store_true', help='Root xác nhận đã chốt manifest và ghi LOG trước lượt evaluator đầu tiên')
    ap.add_argument('--manifest', default='results/T-024/ban-ghi-dua-vao-cham.json')
    ap.add_argument('--output', default='results/T-024/cham-a.json')
    ap.add_argument('--checks-output', default='results/T-024/work/kiem-dung-dan.json')
    args = ap.parse_args()
    if not args.confirm_frozen:
        ap.error('Chỉ được chạy sau khi root xác nhận manifest đã chốt và LOG đã ghi')
    out, check = local(args.output), local(args.checks_output)
    out.relative_to(OUT)
    check.relative_to(OUT)
    if out.exists() or check.exists():
        ap.error('Không ghi đè lượt chấm trước; chỉ định đường dẫn đầu ra mới trong results/T-024')
    run(local(args.manifest), out, check)
