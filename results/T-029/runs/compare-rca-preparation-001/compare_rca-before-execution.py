"""T-029 step5/G: compare (a), first alarm and first post-injection alarm.

Preparation may occur before I3. Execution requires the root's confirmation and
EC2 chain completion/V4 PASS copied back under results/T-029/runs.
Only scores existing records; never runs a ranker or alters a baseline.
"""
import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import bocpd_features as bf

sys.path.insert(0, str(bf.ROOT / 'src'))
from p3 import danh_gia

METHODS = {'baro': ('baro', 'native'), 'circa_ols_rht': ('circa', 'ols+rht'),
           'circa_ols_da': ('circa', 'ols+rht_da'), 'torai_B': ('torai', 'B')}
KEYS_B = {'baro': 'baro:native', 'circa_ols_rht': 'circa:ols+rht',
          'circa_ols_da': 'circa:ols+rht_da', 'torai_B': 'torai_B'}
METRICS = ('hit@1', 'hit@5')
HIGH = 1e10
PREEXISTING_NEZHA = {'src/p3/nezha.py', 'src/p3/nezha_worker.py', 'src/p3/adapters/nezha.py'}


def local(path):
    path = Path(path)
    path = path.resolve() if path.is_absolute() else (bf.ROOT / path).resolve()
    path.relative_to(bf.ROOT)
    if 'locked' in path.relative_to(bf.ROOT).parts:
        raise ValueError('Không đọc locked')
    return path


def read(path, hashes, expected=None):
    path = local(path)
    actual = bf.digest(path)
    if expected is not None and actual != expected:
        raise RuntimeError(f'V1/source SHA lệch: {path.relative_to(bf.ROOT)}')
    hashes[path.relative_to(bf.ROOT).as_posix()] = actual
    return json.loads(path.read_text(encoding='utf-8-sig'))


def method_name(rec):
    return next((name for name, pair in METHODS.items() if pair == (rec['method'], rec['variant'])), None)


def verify_source_versions(idx_a, idx_b, hashes):
    """Full T029 baseline is immutable; the A/B aggregate covers its legacy subset."""
    baseline = read('results/T-029/runs/buoc0-001/manifest.json', hashes)['src_p3']
    paths = sorted((bf.ROOT / 'src/p3').rglob('*.py'), key=lambda p: p.relative_to(bf.ROOT).as_posix())
    current_files = {p.relative_to(bf.ROOT).as_posix(): bf.digest(p) for p in paths}
    if current_files != baseline['tep'] or len(current_files) != 20:
        raise RuntimeError('V1 full src/p3 file set/SHA khác baseline T029 bước0')
    full = hashlib.sha256()
    legacy = hashlib.sha256()
    legacy_files = {}
    for path in paths:
        name = path.relative_to(bf.ROOT).as_posix()
        full.update(path.read_bytes())
        if name not in PREEXISTING_NEZHA:
            legacy.update(path.read_bytes())
            legacy_files[name] = current_files[name]
    if full.hexdigest() != baseline['tong']:
        raise RuntimeError('V1 full20 src/p3 aggregate khác baseline T029 bước0')
    if not PREEXISTING_NEZHA <= set(current_files) or len(legacy_files) != 17:
        raise RuntimeError('V1 tập legacy17/preexisting3 khác baseline đã ghi')
    if legacy.hexdigest() != idx_a['src_p3_sha256'] or legacy.hexdigest() != idx_b['src_p3_sha256']:
        raise RuntimeError('V1 legacy17 src/p3 aggregate khác frozen A/B')
    return {'full20': {'sha256': full.hexdigest(), 'files': current_files},
            'legacy17': {'sha256': legacy.hexdigest(), 'files': legacy_files},
            'preexisting3': {name: current_files[name] for name in sorted(PREEXISTING_NEZHA)},
            'baseline_source': 'results/T-029/runs/buoc0-001/manifest.json#/src_p3'}


def load_frozen_records(path, kind, hashes):
    doc = read(path, hashes)
    rows = doc['records'] if kind == 'a' else doc['ban_ghi']
    data = {}
    for meta in rows:
        if kind != 'a' and meta['loai'] != 'rca':
            continue
        mid = method_name(meta)
        if mid is None:
            continue
        source = meta['path'] if kind == 'a' else meta['duong_dan']
        rec = read(source, hashes, meta['sha256'])
        if any(rec.get(k) != meta.get(k) for k in ('method', 'variant', 'seed', 'opaque_id')):
            raise RuntimeError('Frozen metadata khác bản ghi: ' + source)
        if rec['mode'] != ('a' if kind == 'a' else 'b'):
            raise RuntimeError('Mode khác frozen index: ' + source)
        det = 'a' if kind == 'a' else meta['nhom']
        key = (det, mid, rec['opaque_id'], rec.get('seed'))
        if key in data:
            raise RuntimeError('Trùng bản ghi frozen: ' + repr(key))
        data[key] = (rec, source)
    return doc, data


def load_plus(artifact_root, chain_run, hashes):
    artifact_root = local(artifact_root)
    artifact_root.relative_to(bf.OUT / 'runs')
    end = read(artifact_root / 'runs' / chain_run / 'ket-thuc.json', hashes)
    v4 = read(artifact_root / 'runs' / chain_run / 'v4-check.json', hashes)
    if end['status'] != 'PASS' or v4['status'] != 'PASS':
        raise RuntimeError('Chưa có I3 chain PASS và V4 PASS; không chấm G')
    rows, sources = {}, {}
    for folder in sorted((artifact_root / 'runs').glob('i3-*-dev-*-*')):
        if not (folder / 'source-tplus.json').is_file():
            raise RuntimeError('I3 source-tplus thiếu: ' + str(folder))
        source = read(folder / 'source-tplus.json', hashes)
        key_ca = (source['detector'], source['opaque_id'])
        if key_ca in sources:
            raise RuntimeError('Nhiều I3 run cho cùng cặp; cần root chỉ artifactroot chính xác')
        sources[key_ca] = source
        summary = read(folder / 'tom-tat.json', hashes)
        if not summary['xong'] or summary['so_loi_runner'] != 0:
            raise RuntimeError('I3 run chưa xong hoặc lỗi runner')
        records = sorted(folder.glob('luot/*/ban-ghi-*.json'))
        if len(records) != 6:
            raise RuntimeError('I3 không đủ sáu bản ghi mỗi cặp')
        for path in records:
            rec = read(path, hashes)
            mid = method_name(rec)
            if mid is None or rec['opaque_id'] != source['opaque_id'] or rec['detector'] != source['detector']:
                raise RuntimeError('I3 metadata không khớp source-tplus')
            key = (source['detector'], mid, rec['opaque_id'], rec.get('seed'))
            if key in rows:
                raise RuntimeError('Trùng bản ghi I3')
            rows[key] = (rec, path.relative_to(bf.ROOT).as_posix())
    if len(sources) != 60 or len(rows) != 360:
        raise RuntimeError('I3 chưa đủ 60 cặp/360 bản ghi')
    return rows, sources


def score_one(entry, root):
    rec, path = entry
    value = danh_gia.cham_ca(rec, root)
    nodes = (rec.get('diagnostics') or {}).get('nodes') or {}
    high = sorted(n for n, item in nodes.items() if float(item.get('rht_score', 0)) > HIGH)
    return {**{k: value[k] for k in METRICS}, 'status': rec['status'], 'seed': rec.get('seed'),
            'rank_min': value['rank_min'], 'rank_max': value['rank_max'], 'source_record': path,
            'circa_nodes_gt_1e10': high, 'circa_has_node_diagnostics': bool(nodes)}


def point(entries, root):
    per_seed = {str(seed) if seed is not None else 'single': score_one(entry, root) for seed, entry in entries}
    return {**{k: sum(row[k] for row in per_seed.values()) / len(per_seed) for k in METRICS},
            'status_counts': dict(Counter(row['status'] for row in per_seed.values())), 'per_seed': per_seed,
            'circa_any_node_gt_1e10': any(row['circa_nodes_gt_1e10'] for row in per_seed.values())}


def changes(a, plus, first):
    return {'a_to_tplus': {k: plus[k] - a[k] for k in METRICS},
            'tplus_to_first': {k: first[k] - plus[k] for k in METRICS}}


def aggregate(rows):
    n = len(rows)
    return {'n': n, 'case_ids': [row['opaque_id'] for row in rows],
            'points': {p: {k: sum(row['points'][p][k] for row in rows) / n if n else None for k in METRICS}
                       for p in ('a', 't_hat_plus', 't_hat')},
            'signed_deltas': {d: {k: sum(row['signed_deltas'][d][k] for row in rows) / n if n else None for k in METRICS}
                              for d in ('a_to_tplus', 'tplus_to_first')}}


def by_field(rows, field):
    groups = sorted({row[field] for row in rows})
    return {group: aggregate([row for row in rows if row[field] == group]) for group in groups}


def main(args):
    bf.audit('Lệnh có ghi: T-014-main python -B -W ignore compare_rca.py ' + ' '.join(sys.argv[1:]) + '; kiểm I3/V4 trước đọc nhãn G.')
    if not args.confirm_i3_pass:
        raise RuntimeError('Root chưa xác nhận 2d I3 PASS')
    hashes = {}
    plus, plus_sources = load_plus(args.ec2_root, args.chain_run, hashes)
    idx_a, rec_a = load_frozen_records('results/T-024/ban-ghi-dua-vao-cham.json', 'a', hashes)
    idx_b, rec_b = load_frozen_records('results/T-025/ban-ghi-dua-vao-cham.json', 'b', hashes)
    source_versions = verify_source_versions(idx_a, idx_b, hashes)
    labels = {row['opaque_id']: row for row in read('results/T-022/nhan-dev.json', hashes)['cases']}
    allow = read('results/T-022/allowlist-dev.json', hashes)['cases']
    ids = sorted(row['opaque_id'] for row in allow)
    if len(ids) != 30 or set(ids) != set(labels):
        raise RuntimeError('Allowlist/nhãn không đúng 30 ca')
    frozen_a = read('results/T-024/cham-a.json', hashes)
    frozen_b = read('results/T-025/cham-b.json', hashes)
    analysis_b = read('results/T-025/cham/phan-tich-b.json', hashes)['theo_ca']
    alarms = read('results/T-025/bao-dong.json', hashes)['bo_phat_hien']
    bf.audit('G: I3/V4 PASS đã kiểm, frozen records đã kiểm SHA trước nối nhãn; đọc nhãn/cham-a/cham-b/nhóm A_chua_moc để chấm 240 dòng theo ca.')
    started = time.perf_counter()
    result, verification = {}, []
    for detector in ('bocpd', 'nsigma'):
        result[detector] = {}
        for mid in METHODS:
            rows = []
            seeds = [0, 1, 2] if mid == 'torai_B' else [None]
            for oid in ids:
                root = labels[oid]['root']
                entries_a = [(seed, rec_a[('a', mid, oid, seed)]) for seed in seeds]
                entries_b = [(seed, rec_b[(detector, mid, oid, seed)]) for seed in seeds]
                entries_plus = [(seed, plus[(detector, mid, oid, seed)]) for seed in seeds]
                points = {'a': point(entries_a, root), 't_hat': point(entries_b, root), 't_hat_plus': point(entries_plus, root)}
                published_a = frozen_a['methods'][mid]['per_case'][oid]
                published_b = frozen_b['theo_bo_phat_hien'][detector][KEYS_B[mid]]['ca'][oid]
                for key in METRICS:
                    for which, source in (('a', published_a), ('t_hat', published_b)):
                        delta = abs(points[which][key] - source[key])
                        okay = math.isclose(points[which][key], source[key], abs_tol=1e-12, rel_tol=0)
                        verification.append({'detector': detector, 'method': mid, 'opaque_id': oid, 'point': which,
                                             'metric': key, 'absolute_difference': delta, 'pass': okay})
                        if not okay:
                            raise RuntimeError('G chấm lại khác frozen A/B: ' + repr(verification[-1]))
                        points[which][key] = source[key]
                if mid == 'torai_B':
                    for seed in seeds:
                        for key in METRICS:
                            if points['a']['per_seed'][str(seed)][key] != published_a['seed_metrics'][str(seed)][key]:
                                raise RuntimeError('TORAI A per-seed khác frozen metric')
                inj = labels[oid]['inject_time']
                first = alarms[detector][oid]['luot_rca']['t_hat']
                post = [a for a in alarms[detector][oid]['alarms'] if a >= inj]
                chosen = plus_sources[(detector, oid)]
                if not post or chosen['time'] != min(post) or chosen['index'] != chosen['time'] - labels[oid]['metric_time_min']:
                    raise RuntimeError('I3 source t_hat_plus khác báo động đã chốt')
                for entry in entries_b:
                    win = entry[1][0].get('window')
                    if win and win['t'] != first:
                        raise RuntimeError('B record window khác t_hat')
                for entry in entries_plus:
                    win = entry[1][0].get('window')
                    if win and win['t'] != chosen['time']:
                        raise RuntimeError('I3 record window khác source t_hat_plus')
                group = 'Miss' if not post else 'S' if first is not None and first >= inj else ('E-gần' if analysis_b[oid][detector]['A_chua_moc'] else 'E-xa')
                row = {'opaque_id': oid, 'root': root, 'fault': labels[oid]['fault'], 'cell': labels[oid]['cell'],
                       'group': group, 'A_chua_moc': analysis_b[oid][detector]['A_chua_moc'],
                       't_hat': first, 't_hat_plus': chosen['time'], 't_hat_plus_index': chosen['index'],
                       'points': points, 'signed_deltas': changes(points['a'], points['t_hat_plus'], points['t_hat']),
                       'frozen_score_sources': {'a': f'results/T-024/cham-a.json#/methods/{mid}/per_case/{oid}',
                                               't_hat': f'results/T-025/cham-b.json#/theo_bo_phat_hien/{detector}/{KEYS_B[mid]}/ca/{oid}'},
                       'group_source': f'results/T-025/cham/phan-tich-b.json#/theo_ca/{oid}/{detector}/A_chua_moc'}
                if mid == 'torai_B':
                    row['signed_deltas_by_seed'] = {str(seed): changes(points['a']['per_seed'][str(seed)], points['t_hat_plus']['per_seed'][str(seed)], points['t_hat']['per_seed'][str(seed)]) for seed in seeds}
                rows.append(row)
            table = {'per_case': rows, 'all30': aggregate(rows), 'by_cell': by_field(rows, 'cell'),
                     'by_event_group': by_field(rows, 'group')}
            if mid == 'torai_B':
                table['by_seed_on_30_cases'] = {str(seed): aggregate([{**row, 'points': {p: row['points'][p]['per_seed'][str(seed)] for p in row['points']}, 'signed_deltas': row['signed_deltas_by_seed'][str(seed)]} for row in rows]) for seed in seeds}
            if mid.startswith('circa'):
                high_by_point = {p: [row['opaque_id'] for row in rows if row['points'][p]['circa_any_node_gt_1e10']] for p in ('a', 't_hat', 't_hat_plus')}
                paired = [row for row in rows if not any(row['points'][p]['circa_any_node_gt_1e10'] for p in ('a', 't_hat', 't_hat_plus'))]
                table['circa_threshold'] = {'threshold': HIGH, 'high_case_ids_by_point': high_by_point,
                                            'high_count_by_point': {p: len(v) for p, v in high_by_point.items()},
                                            'paired_no_node_exceeds_at_any_point': aggregate(paired),
                                            'paired_by_cell': by_field(paired, 'cell'),
                                            'note': 'Giữ non-OK bằng0 trong mọi mẫu số; ngưỡng dựa trên node rht_score quan sát trong bản ghi.'}
            result[detector][mid] = table
            bf.audit(f'G xong {detector}/{mid}:30ca ghép cặp, giữ non-OK; source hashes giữ trong output.')
    output = {'status': 'PASS', 'schema_version': 1, 'row_count': 240, 'by_detector': result,
              'signed_delta_definition': {'a_to_tplus': 'Hit(t_hat_plus) - Hit(a)', 'tplus_to_first': 'Hit(t_hat) - Hit(t_hat_plus)'},
              'interpretation': 'I3 RCA tại báo động đầu sau mốc, chọn nhờ nhãn mốc; không là cận trên chất lượng RCA.',
              'TORAI': 'Chấm từng seed, trung bình theo ca trước gộp trên30ca; seed bảng riêng.',
              'source_hashes': hashes, 'src_p3_sha256': source_versions['full20']['sha256'],
              'src_p3_versions': source_versions, 'script_sha256': bf.digest(__file__),
              'verification': {'frozen_A_B_numeric_absolute_tolerance': 1e-12, 'checks': verification,
                               'mismatches': sum(not x['pass'] for x in verification)}, 'seconds': time.perf_counter() - started}
    bf.write_json(bf.OUT / 'a-so-b.json', output)
    print(json.dumps({'status': 'PASS', 'rows': 240, 'frozen_score_checks': len(verification)}))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ec2-root', required=True)
    parser.add_argument('--chain-run', default='chuoi-002')
    parser.add_argument('--confirm-i3-pass', action='store_true')
    arguments = parser.parse_args()
    run = bf.OUT / 'runs/compare-rca-001'
    if run.exists():
        raise RuntimeError('Không ghi đè lượt G đã có: ' + str(run))
    bf.audit('Tạo runs/compare-rca-001 để giữ manifest/thời gian và mọi lượt G, kể cả lượt hỏng.')
    run.mkdir(parents=True)
    started_at, started = bf.now(), time.perf_counter()
    invocation = {'started_at': started_at, 'script_sha256': bf.digest(__file__),
                  'command': 'python -B -W ignore compare_rca.py ' + ' '.join(sys.argv[1:])}
    bf.write_json(run / 'invocation.json', invocation)
    try:
        result = main(arguments)
        bf.write_json(run / 'manifest.json', {**invocation, 'status': 'PASS', 'completed_at': bf.now(),
                      'seconds': time.perf_counter() - started,
                      'input_hashes': result['source_hashes'],
                      'output_hashes': {'results/T-029/a-so-b.json': bf.digest(bf.OUT / 'a-so-b.json')},
                      'rows': result['row_count'], 'frozen_score_mismatches': result['verification']['mismatches']})
    except Exception as error:
        bf.write_json(run / 'manifest-stop.json', {**invocation, 'status': 'STOP', 'completed_at': bf.now(),
                      'seconds': time.perf_counter() - started,
                      'error': type(error).__name__ + ': ' + str(error)})
        bf.audit(f'DỪNG compare_rca.py: {type(error).__name__}: {error}; giữ output/lượt, báo root; không tự xử lý.')
        raise
