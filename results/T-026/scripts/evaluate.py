"""T-026: chấm bốn bảng đã chốt; chỉ nối nhãn sau khi kiểm mọi bản ghi/hash.

Không chạy phương pháp, không chọn lại bản ghi, không đọc dữ liệu đo thô.
Nhãn T-026 dùng t_ns nên bộ nạp riêng không gọi p3.nhan (hợp đồng RE2).
"""
import argparse
import copy
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-026'
sys.path.insert(0, str(ROOT / 'src'))
from p3.runner import PYTHONPATH
for dependency_path in PYTHONPATH['main']:
    if dependency_path not in sys.path:
        sys.path.append(dependency_path)
PRIMARY = ('baro', 'simplerca', 'microrank_full', 'tracerca', 'circa_ols_da', 'torai_B')
METHODS = PRIMARY + ('microrank_top11',)
TABLES = ('main', 'sensitivity_A', 'sensitivity_B', 'trace_guard')
STATES = ('OK', 'NO_EVIDENCE', 'ERROR', 'TIMEOUT', 'UNSUPPORTED')
METRICS = tuple(f'hit@{k}' for k in range(1, 11)) + ('rr', 'ndcg@5', 'avg@5')
NAMES = {'baro': 'BARO', 'simplerca': 'SimpleRCA M4', 'microrank_full': 'MicroRank xếp đầy đủ',
         'microrank_top11': 'MicroRank top-11 dẫn xuất', 'tracerca': 'TraceRCA lọc hữu hạn',
         'circa_ols_da': 'CIRCA kiến trúc OLS+RHT+DA — UNSUPPORTED trên OB',
         'torai_B': 'TORAI nguồn B — UNSUPPORTED trên OB'}


def read_json(path):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise ValueError('duplicate JSON key: ' + k)
            out[k] = v
        return out
    def reject(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),
                      object_pairs_hook=unique, parse_constant=reject)


def local(name):
    p = (ROOT / name).resolve()
    relative = p.relative_to(ROOT)
    if 'locked' in relative.parts:
        raise ValueError('không được đọc data/locked')
    return p


def rel(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def code_hash():
    h = hashlib.sha256()
    for p in sorted((ROOT / 'src/p3').rglob('*.py')):
        h.update(p.read_bytes())
    return h.hexdigest()


def dump(path, doc):
    path = local(path)
    path.relative_to(OUT)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, allow_nan=False)
        f.write('\n')


def method_id(rec):
    key = (rec['method'], rec['variant'])
    mids = {('baro', 'native'): 'baro', ('simplerca', 'M4'): 'simplerca',
            ('microrank', 'full'): 'microrank_full', ('tracerca', 'finite'): 'tracerca',
            ('circa', 'ols+rht_da'): 'circa_ols_da', ('torai', 'B'): 'torai_B'}
    if key not in mids:
        raise ValueError('phương pháp/variant ngoài Q-85: ' + str(key))
    return mids[key]


def load_manifest(path, require_frozen=True):
    """Mọi kiểm dữ liệu chọn, cấu hình, mã và bản ghi xảy ra trước nạp nhãn.

    require_frozen=False chỉ dùng kiểm bằng nhãn giả trên manifest nháp.
    """
    doc = copy.deepcopy(path) if isinstance(path, dict) else read_json(path)
    if require_frozen and not doc.get('frozen_at'):
        raise ValueError('manifest chưa chốt')
    if code_hash() != doc['src_p3_sha256']:
        raise ValueError('hash src/p3 khác manifest')
    sources = doc['source_hashes']
    for name, expected in sources.items():
        if sha(local(name)) != expected:
            raise ValueError('nguồn đã đổi sau khai/chốt: ' + name)
    for name, expected in doc.get('external_source_hashes', {}).items():
        p = Path(name).resolve()
        p.relative_to(Path('D:/RCA-ext').resolve())
        if sha(p) != expected:
            raise ValueError('mã phụ thuộc đã đổi: ' + name)
    run_hashes = doc.get('run_file_hashes', {})
    if require_frozen and not run_hashes:
        raise ValueError('manifest chưa ghim hash mọi file lượt chạy')
    for name, expected in run_hashes.items():
        p = local(name)
        p.relative_to(OUT / 'runs')
        if sha(p) != expected:
            raise ValueError('file lượt chạy đã đổi sau chốt: ' + name)
    required = {'results/T-026/allowlist-dev.json', 'results/T-026/mappings/ob.json',
                'results/T-026/config/adapter-config.json'}
    if not required <= set(sources):
        raise ValueError('manifest thiếu hash allowlist/mapping/config')
    if sha(local(doc['plan_path'])) != doc['plan_sha256']:
        raise ValueError('kế hoạch chạy đã đổi')
    plan = read_json(local(doc['plan_path']))
    planned_fields = ('opaque_id', 'method', 'variant', 'seed', 'hashseed', 'path', 'source_view', 'reused_pilot')
    for table in TABLES:
        frozen_table, planned_table = doc['tables'][table], plan['tables'][table]
        if frozen_table['case_ids'] != planned_table['case_ids']:
            raise ValueError('cohort khác kế hoạch trước chạy: ' + table)
        frozen_keys = [tuple(m.get(k) for k in planned_fields) for m in frozen_table['records']]
        planned_keys = [tuple(m.get(k) for k in planned_fields) for m in planned_table['records']]
        if frozen_keys != planned_keys:
            raise ValueError('bản ghi chọn khác kế hoạch trước chạy: ' + table)
    allow = read_json(OUT / 'allowlist-dev.json')
    byid = {x['opaque_id']: x for x in allow['cases']}
    ids = set(byid)
    if len(ids) != 22 or allow['so_ca'] != 22 or len(allow['cases']) != 22:
        raise ValueError('không đúng 22 ca dev')
    disputed = [o for o, c in byid.items() if c.get('t_ns_sensitivity_A') is not None]
    if len(disputed) != 1:
        raise ValueError('không đúng một ca đổi mốc Q-84')
    disputed = disputed[0]
    universe = read_json(OUT / 'mappings/ob.json')['universe']
    if len(universe) != 10 or len(set(universe)) != len(universe):
        raise ValueError('universe không đúng mapping Q-85')
    config_id = read_json(OUT / 'config/adapter-config.json')['config_id']
    if set(doc['tables']) != set(TABLES):
        raise ValueError('không đúng bốn bảng khai trước')
    if not any(x.get('id') == 'microrank_top11' and x.get('source_variant') == 'full'
               for x in doc.get('derived', [])):
        raise ValueError('chưa khai trước phép dẫn xuất MicroRank top11')
    tables, metadata, selected_paths, cache = {}, {}, set(), {}
    for table in TABLES:
        entry = doc['tables'][table]
        expected_ids = ids - {disputed} if table == 'sensitivity_B' else ids
        actual_ids = entry['case_ids']
        if set(actual_ids) != expected_ids or len(actual_ids) != len(expected_ids):
            raise ValueError('cohort khác khai trước: ' + table)
        tables[table] = {m: {} for m in PRIMARY}
        metadata[table] = {m: {} for m in PRIMARY}
        for meta in entry['records']:
            name = meta['path']
            p = local(name)
            p.relative_to(OUT / 'runs')
            if name not in cache:
                if sha(p) != meta['sha256']:
                    raise ValueError('bản ghi đổi: ' + name)
                cache[name] = read_json(p)
            rec = cache[name]
            if sha(p) != meta['sha256']:
                raise ValueError('hash tham chiếu khác: ' + name)
            if rec['status'] not in STATES:
                raise ValueError('trạng thái lạ: ' + name)
            mid, oid = method_id(rec), rec['opaque_id']
            if rec['mode'] != 'a' or oid not in expected_ids:
                raise ValueError('bản ghi ngoài chế độ/dev cohort: ' + name)
            if rec['config_id'] != config_id:
                raise ValueError('config_id khác cấu hình đã khóa: ' + name)
            for key in ('opaque_id', 'variant', 'seed', 'hashseed'):
                if rec.get(key) != meta.get(key):
                    raise ValueError('meta khác bản ghi ' + key + ': ' + name)
            if rec['method'] != meta['method']:
                raise ValueError('meta khác method: ' + name)
            unsupported = mid in ('circa_ols_da', 'torai_B')
            if rec.get('seed') is not None or rec.get('hashseed') != (None if unsupported else 0):
                raise ValueError('seed/hashseed ngoài cấu hình: ' + name)
            if unsupported and (rec['status'] != 'UNSUPPORTED' or not rec.get('error')
                                or rec.get('diagnostics', {}).get('method_called') is not False):
                raise ValueError('UNSUPPORTED thiếu lý do hoặc có gọi phương pháp: ' + name)
            if oid in tables[table][mid]:
                raise ValueError('trùng method/ca trong bảng: ' + table + '/' + oid)
            view = meta['source_view']
            wanted_view = ('sensitivity_A' if table == 'sensitivity_A' and oid == disputed
                           else 'trace_guard' if table == 'trace_guard' and mid != 'baro' else 'main')
            if view != wanted_view:
                raise ValueError('view khác bảng đã khai: ' + name)
            marker = byid[oid]['t_ns_sensitivity_A'] if view == 'sensitivity_A' else byid[oid]['t_ns']
            guard = byid[oid]['trace_guard_s'] if view == 'trace_guard' else 0
            window = rec.get('window')
            if window is None:
                if rec['status'] != 'TIMEOUT' or not rec.get('cost', {}).get('timed_out'):
                    raise ValueError('bản ghi thiếu cửa sổ: ' + name)
            elif window.get('t_ns') != marker or window.get('trace_guard_s', 0) != guard:
                raise ValueError('mốc/cắt trace khác hợp đồng: ' + name)
            from p3 import ban_ghi, danh_gia as dg
            ban_ghi.kiem(rec)
            if rec['status'] == 'OK':
                dg.khoi_tu_ban_ghi(rec)
            if 'observed_entities' not in rec.get('sets', {}):
                raise ValueError('thiếu tập quan sát: ' + name)
            if rec['status'] != 'TIMEOUT':
                wanted_input_hashes = {p: m['sha256'] for p, m in byid[oid]['files'].items()}
                if rec.get('input_sha256') != wanted_input_hashes:
                    raise ValueError('hash/path đầu vào bản ghi khác allowlist dev: ' + name)
            tables[table][mid][oid] = rec
            metadata[table][mid][oid] = meta
            selected_paths.add(name)
        if any(set(rr) != expected_ids for rr in tables[table].values()):
            raise ValueError('không đủ ca/method: ' + table)
    unique = doc['unique_records']
    unique_paths = {m['path'] for m in unique}
    if len(unique_paths) != len(unique) or unique_paths != selected_paths:
        raise ValueError('unique_records không khớp bản ghi bốn bảng')
    if require_frozen and not selected_paths <= set(run_hashes):
        raise ValueError('run_file_hashes thiếu bản ghi được chọn')
    for meta in unique:
        if sha(local(meta['path'])) != meta['sha256']:
            raise ValueError('hash unique_records khác: ' + meta['path'])
    for mid in PRIMARY:
        for oid in ids - {disputed}:
            main_path = metadata['main'][mid][oid]['path']
            if metadata['sensitivity_A'][mid][oid]['path'] != main_path or metadata['sensitivity_B'][mid][oid]['path'] != main_path:
                raise ValueError('phần bất biến Q-84 không tái dùng đúng')
        if metadata['sensitivity_A'][mid][disputed]['path'] == metadata['main'][mid][disputed]['path']:
            raise ValueError('ca đổi mốc A không có bản ghi riêng')
    if any(metadata['trace_guard']['baro'][o]['path'] != metadata['main']['baro'][o]['path'] for o in ids):
        raise ValueError('BARO bất biến trace_guard không dùng lại main')
    return doc, allow, tables, metadata, universe


def top11_record(rec):
    out = copy.deepcopy(rec)
    out['variant'] = 'top11-derived'
    if rec['status'] != 'OK':
        out.update(ranking_native=[], ranking=[], entity_ranking=[], blocks=None)
        out['sets']['returned'] = 0
        return out
    native = rec.get('extra', {}).get('top11_ranks')
    services = rec.get('extra', {}).get('service_ranks_top11')
    if native is None or services is None:
        raise ValueError('MicroRank OK thiếu top11 gốc')
    items = {row['item']: row for row in rec['ranking']}
    rows = [items[name] for name in native]
    from p3.ban_ghi import xep_thuc_the
    entities = xep_thuc_the([(r['item'], r['entity'], r['key']) for r in rows])
    if [r['entity'] for r in entities] != services:
        raise ValueError('top11 dẫn xuất khác service_ranks_top11 gốc')
    out.update(ranking_native=list(native), ranking=rows, entity_ranking=entities, blocks=None)
    out['sets']['returned'] = len(entities)
    return out


def independent_metrics(rec, root):
    """Mã riêng: nhóm từ KHÓA đúng, không dùng tie_group hoặc helper danh_gia.

    T-026 không có phương pháp có khối TORAI OK. Hạng root phân bố đều
    trên nhóm cùng khóa; các trạng thái khác OK và root vắng có độ đo 0.
    """
    if rec['status'] not in STATES:
        raise ValueError('trạng thái độc lập không hợp lệ')
    rank_min = rank_max = None
    if rec['status'] == 'OK':
        if rec.get('blocks') is not None:
            raise ValueError('T-026 không có khối TORAI OK')
        rows = rec['entity_ranking']
        if not rows or len({x['entity'] for x in rows}) != len(rows):
            raise ValueError('thứ hạng OK rỗng hoặc trùng')
        keys = [tuple(float(v) for v in row['key']) for row in rows]
        if not all(math.isfinite(v) for key in keys for v in key) or keys != sorted(keys, reverse=True):
            raise ValueError('khóa không hữu hạn hoặc không giảm dần')
        hits = [i for i, x in enumerate(rows) if x['entity'] == root]
        if hits:
            ranks = [i + 1 for i, key in enumerate(keys) if key == keys[hits[0]]]
            rank_min, rank_max = min(ranks), max(ranks)
    def at(r):
        d = {f'hit@{k}': float(r is not None and r <= k) for k in range(1, 11)}
        d['rr'] = 0.0 if r is None else 1.0 / r
        d['ndcg@5'] = 1.0 / math.log2(1 + r) if r is not None and r <= 5 else 0.0
        d['avg@5'] = sum(d[f'hit@{k}'] for k in range(1, 6)) / 5
        return d
    dist = {} if rank_min is None else {r: Fraction(1, rank_max - rank_min + 1) for r in range(rank_min, rank_max + 1)}
    expected = {k: sum(float(p) * at(r)[k] for r, p in dist.items()) for k in METRICS}
    expected.update(rank_min=rank_min, rank_max=rank_max, status=rec['status'],
                    root_trong_tra_ve=bool(dist), opt=at(rank_min) if dist else None,
                    pes=at(rank_max) if dist else None,
                    rank_distribution={str(r): str(p) for r, p in dist.items()})
    return expected


def native_metrics(rec, root):
    """RCAEval kiểm riêng bằng hạng gốc, bỏ trùng thực thể lần đầu."""
    native = rec.get('ranking_native') or [] if rec['status'] == 'OK' else []
    services = []
    for item in native:
        service = item.split('_')[0].replace('-db', '')
        if service not in services:
            services.append(service)
    rank = services.index(root) + 1 if root in services else None
    vals = {f'AC@{k}': float(rank is not None and rank <= k) for k in range(1, 11)}
    vals['Avg@5'] = sum(vals[f'AC@{k}'] for k in range(1, 6)) / 5
    vals['rank'] = rank
    return vals


def check_case(rec, root, got):
    want = independent_metrics(rec, root)
    for k in METRICS:
        if not math.isclose(want[k], got[k], abs_tol=1e-12, rel_tol=1e-12):
            raise ValueError('kiểm độc lập khác độ đo: ' + k)
    for side in ('opt', 'pes'):
        if (want[side] is None) != (got[side] is None):
            raise ValueError('kiểm độc lập khác cận hòa')
        if want[side] is not None and any(not math.isclose(want[side][k], got[side][k], abs_tol=1e-12, rel_tol=1e-12) for k in METRICS):
            raise ValueError('kiểm độc lập khác giá trị cận hòa')
    if any(want[k] != got[k] for k in ('rank_min', 'rank_max', 'status', 'root_trong_tra_ve')):
        raise ValueError('kiểm độc lập khác hạng/trạng thái')
    return want


def native_summary(per_case):
    n = len(per_case)
    out = {f'AC@{k}': sum(v[f'AC@{k}'] for v in per_case.values()) / n for k in (1, 3, 5)}
    out['Avg@5'] = sum(v['Avg@5'] for v in per_case.values()) / n
    for K in (5, 10):
        den = sum(v[f'AC@{K}'] for v in per_case.values()) / n
        out[f'retrieval_service({K})'] = den
        out[f'rerank_service(1,{K})'] = out['AC@1'] / den if den else None
    out['n'] = n
    return out


def load_labels(path, allow):
    """Chỉ caller thật gọi sau load_manifest; giữ nhãn root khỏi mọi runner."""
    doc = read_json(path)
    needed = {'opaque_id', 'root', 'fault', 'cell', 'nhom_loi', 'nhom_vi_tri_p75', 't_ns'}
    if doc['so_ca'] != 22 or len(doc['cases']) != 22:
        raise ValueError('nhãn không đúng 22 ca')
    labels = {}
    markers = {c['opaque_id']: c for c in allow['cases']}
    for c in doc['cases']:
        if not needed <= set(c) or c['opaque_id'] in labels or c['opaque_id'] not in markers:
            raise ValueError('schema/ID nhãn T-026 khác cohort')
        if c['t_ns'] != markers[c['opaque_id']]['t_ns'] or c['cell'] != c['root'] + '|' + c['fault']:
            raise ValueError('mốc/ô nhãn khác metadata')
        labels[c['opaque_id']] = {k: c[k] for k in needed - {'opaque_id'}}
    if set(labels) != set(markers):
        raise ValueError('nhãn khác allowlist')
    return labels


def fake_labels(allow, universe):
    ids = sorted(c['opaque_id'] for c in allow['cases'])
    # 13 ô không đều: 9 ô x 2 ca + 4 ô x 1 ca. Đây là nhãn giả, không biết ô thật.
    cells = [i for i in range(9) for _ in range(2)] + list(range(9, 13))
    return {o: {'root': universe[cells[i] % len(universe)], 'fault': 'fake-' + str(cells[i]),
                'cell': 'fake-cell-' + str(cells[i]), 'nhom_loi': 'synthetic',
                'nhom_vi_tri_p75': 'synthetic', 't_ns': next(c['t_ns'] for c in allow['cases'] if c['opaque_id'] == o)}
            for i, o in enumerate(ids)}


def score_tables(records, metadata, labels, universe):
    from p3 import danh_gia as dg
    tables, validation = {}, {'all_per_case_independent': [], 'rcaeval_native_parity': [], 'non_OK_in_denominator': True}
    for table in TABLES:
        ids = sorted(next(iter(records[table].values())))
        seeds = {m: dict(rr) for m, rr in records[table].items()}
        seeds['microrank_top11'] = {o: top11_record(r) for o, r in seeds['microrank_full'].items()}
        metas = {m: dict(rr) for m, rr in metadata[table].items()}
        metas['microrank_top11'] = metas['microrank_full']
        methods = {}
        for mid in METHODS:
            rr = seeds[mid]
            per = {}
            for oid in ids:
                rec, lab, meta = rr[oid], labels[oid], metas[mid][oid]
                got = dg.cham_ca(rec, lab['root'])
                independent = check_case(rec, lab['root'], got)
                native = native_metrics(rec, lab['root'])
                rca_one = dg.bang_rcaeval({oid: rec}, labels)
                expect_rca = native_summary({oid: native})
                if rca_one != expect_rca:
                    raise ValueError('RCAEval native khác kiểm độc lập: ' + table + '/' + mid + '/' + oid)
                four = dg.bon_tap(rec, universe)
                random = dg.muc_ngau_nhien(rec, lab['root'], universe)
                O = rec['sets']['observed_entities']
                if len(O) != len(set(O)) or rec['sets']['observed'] != len(O):
                    raise ValueError('tập quan sát trùng hoặc lệch số đếm')
                for k in (1, 3, 5, 10):
                    o_random = min(k, len(O)) / len(O) if O and lab['root'] in O else 0.0
                    u_random = min(k, len(universe)) / len(universe) if lab['root'] in universe else 0.0
                    if random[f'O_hit@{k}'] != o_random or random[f'U_hit@{k}'] != u_random:
                        raise ValueError('mức ngẫu nhiên khác công thức độc lập')
                per[oid] = {**got, 'label': lab, 'source_path': meta['path'], 'source_sha256': meta['sha256'],
                            'source_view': meta['source_view'], 'random': random, 'four_sets': four,
                            'independent': independent, 'rcaeval_native': native,
                            'input_shape': rec.get('input_shape') or {}, 'sets': rec['sets'],
                            'diagnostics': rec.get('diagnostics') or {}, 'cost': rec.get('cost') or {}}
                validation['all_per_case_independent'].append({'table': table, 'method': mid, 'opaque_id': oid, 'pass': True})
                validation['rcaeval_native_parity'].append({'table': table, 'method': mid, 'opaque_id': oid, 'pass': True})
            main = dg.tong_hop(per)
            if main['n'] != len(ids) or sum(main['trang_thai'].values()) != len(ids):
                raise ValueError('mẫu số trạng thái khác cohort')
            native = native_summary({o: per[o]['rcaeval_native'] for o in ids})
            rca = dg.bang_rcaeval(rr, labels)
            if any(not (rca[k] == native[k] or isinstance(rca[k], float) and isinstance(native[k], float) and math.isclose(rca[k], native[k], abs_tol=1e-12)) for k in native):
                raise ValueError('RCAEval gộp khác kiểm độc lập')
            grouped = {field: {str(g): dg.tong_hop({o: per[o] for o in ids if labels[o][field] == g})
                               for g in sorted({labels[o][field] for o in ids})}
                       for field in ('fault', 'nhom_loi', 'cell', 'nhom_vi_tri_p75')}
            rand = {key: sum(per[o]['random'][key] for o in ids) / len(ids)
                    for key in ('O_hit@1', 'O_hit@3', 'O_hit@5', 'O_hit@10', 'U_hit@1', 'U_hit@3', 'U_hit@5', 'U_hit@10')}
            rand.update(O_size_mean=sum(per[o]['random']['O_size'] for o in ids) / len(ids),
                        root_coverage_O=sum(per[o]['random']['root_trong_O'] for o in ids) / len(ids),
                        root_coverage_returned=sum(per[o]['root_trong_tra_ve'] for o in ids) / len(ids))
            methods[mid] = {'name': NAMES[mid], 'primary': mid in PRIMARY, 'per_case': per,
                            'summary': {'main': main, 'rcaeval': rca, 'random': rand, 'grouped': grouped},
                            'source_records': [metas[mid][o] for o in ids]}
        cells = {o: labels[o]['cell'] for o in ids}
        tables[table] = {'case_ids': ids, 'n_cases': len(ids), 'n_cells': len(set(cells.values())),
                         'cell_sizes': dict(sorted(Counter(cells.values()).items())), 'methods': methods,
                         'bootstrap': dg.bootstrap({m: methods[m]['per_case'] for m in METHODS}, cells,
                                                   B=10_000, seed=20261005)}
    validation['n_independent_case_checks'] = len(validation['all_per_case_independent'])
    validation['n_rcaeval_case_checks'] = len(validation['rcaeval_native_parity'])
    return tables, validation


def run(manifest_path, output_path, check_path):
    if local(output_path).exists() or local(check_path).exists():
        raise FileExistsError('giữ mọi lượt; không ghi đè evaluator')
    manifest, allow, records, metas, universe = load_manifest(manifest_path)
    # Nhãn thật lần đầu được parse ở đây, sau toàn bộ kiểm manifest/bản ghi.
    label_path = OUT / 'nhan-dev.json'
    label_sha = sha(label_path)
    if manifest['source_hashes'].get(rel(label_path)) != label_sha:
        raise ValueError('manifest chưa ghim hash nhãn thật')
    labels = load_labels(label_path, allow)
    if any(x['root'] not in universe for x in labels.values()):
        raise ValueError('root ngoài U; dừng kiểm trước bảng khoa học')
    started = datetime.now(timezone.utc).isoformat()
    tables, validation = score_tables(records, metas, labels, universe)
    sources = {'manifest': rel(manifest_path), 'manifest_sha256': sha(manifest_path),
               'labels': rel(label_path), 'labels_sha256': label_sha,
               'allowlist': 'results/T-026/allowlist-dev.json', 'mapping': 'results/T-026/mappings/ob.json',
               'config': 'results/T-026/config/adapter-config.json', 'protocol': 'results/T-022/giao-thuc-v2.md',
               'evaluator': 'src/p3/danh_gia.py', 'script': rel(__file__), 'script_sha256': sha(__file__),
               'src_p3_sha256': manifest['src_p3_sha256'], 'frozen_at': manifest['frozen_at'],
               'unique_record_count': len(manifest['unique_records']), 'source_hashes': manifest['source_hashes'],
               'external_source_hashes': manifest.get('external_source_hashes', {})}
    result = {'schema_version': 1, 'dataset': 'Nezha-OB', 'mode': 'a', 'generated_at_utc': started,
              'sources': sources, 'universe': universe,
              'definitions': {'primary_methods': list(PRIMARY), 'derived': ['microrank_top11'],
                              'ties': 'Khóa đúng bằng nhau, kỳ vọng đều trong nhóm. RCAEval trên thứ tự gốc báo riêng.',
                              'status_denominator': 'Mọi ca, mọi trạng thái; khác OK tính 0.',
                              'rerank': 'Tổng Hit@1 / tổng Hit@K; denominator 0 là N/A; không cận hòa Rerank.',
                              'bootstrap': 'Ô root×fault thực tế, mang mọi ca; B=10000 seed20261005 ghép cặp; ratio tính lại và đếm N/A.',
                              'Q84_bound': '1/22 chỉ là cận đổi trung bình Hit@k một phương pháp; không cho hiệu hai phương pháp, Rerank hay bootstrap.',
                              'Q85_limits': 'Metric khoảng60s,5N+5A; không quy khác T024 riêng cho đổi hệ thống. Nền sạch/recovery/thời điểm tiêm thật/đồng bộ tuyệt đối/lệch trace theo ngày OPEN; không kết luận đồ thị.'},
              'tables': tables, 'validation': validation}
    dump(output_path, result)
    dump(check_path, {'sources': sources, **validation})
    print(json.dumps({'output': rel(output_path), 'checks': rel(check_path), 'independent_case_checks': validation['n_independent_case_checks']}, ensure_ascii=True), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-frozen', action='store_true')
    parser.add_argument('--manifest', default='results/T-026/ban-ghi-dua-vao-cham.json')
    parser.add_argument('--output', default='results/T-026/cham-a.json')
    parser.add_argument('--checks-output', default='results/T-026/runs/evaluator-001/checks.json')
    args = parser.parse_args()
    if not args.confirm_frozen:
        parser.error('cần chốt manifest và ghi giờ LOG trước evaluator thật')
    run(local(args.manifest), local(args.output), local(args.checks_output))
