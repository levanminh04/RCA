"""Chỉ nối nhãn sau snapshot đủ A4 và kiểm nguồn nhãn độc lập."""
import sys
from collections import defaultdict
from pathlib import Path
from fractions import Fraction

from bien_nhan import (ROOT, OUT, Blocked, atomic, append, fingerprint, read_pin, ref,
                       verify_envelope)
from nguon import compare_labels, validate_execution_links


def merge_partitions(full_plan, parts):
    """Ghép bản sao đã kiểm hash; giữ receipt gốc, chưa đọc nhãn."""
    from nguon import placement_key
    slots = {}; jobs = {}; hosts = set(); placements = set()
    for item in parts:
        plan = read_pin(item['plan']); snapshot = read_pin(item['snapshot'])
        host = plan['host_role']
        if host in hosts or snapshot['plan_sha256'] != fingerprint(plan):
            raise Blocked('phân lô trùng máy hoặc sai plan')
        hosts.add(host); verify_snapshot(snapshot,plan['jobs'])
        for job in plan['jobs']:
            key=fingerprint(job['slot'])
            identity=placement_key(job['slot'])
            if key in jobs or identity in placements:
                raise Blocked('slot kết quả bị trùng giữa các máy')
            placements.add(identity)
            jobs[key]=fingerprint(job);slots[key]=snapshot['slots'][key]
    expected={fingerprint(j['slot']):fingerprint(j)for j in full_plan['jobs']}
    if len(expected)!=len(full_plan['jobs']) or jobs!=expected:
        raise Blocked('kết quả thiếu/thừa/sai job so với plan toàn đợt')
    return dict(schema='T054-SNAPSHOT-1',plan_sha256=fingerprint(full_plan),slots=slots,
                transfer_sources=parts,labels_joined=False)


def verify_snapshot(snapshot, jobs):
    wanted = {fingerprint(j['slot']): j for j in jobs}
    got = snapshot['slots']
    if set(got) != set(wanted):
        raise Blocked('snapshot thiếu/thừa slot đã đăng ký')
    results = {}
    for key, job in wanted.items():
        slot = got[key]
        if slot['state'] not in ('VERIFIED', 'BLOCKED'):
            raise Blocked('snapshot còn PENDING/RUNNING')
        if job.get('a4') and slot['state'] != 'VERIFIED':
            raise Blocked('A4 BLOCKED: chưa ghép nhãn cho bảng nào')
        if slot['state'] == 'VERIFIED':
            receipt = read_pin(slot['receipt'])
            envelope = read_pin(receipt['result'])
            invocation = read_pin(receipt['invocation'])
            if receipt['job_sha256'] != fingerprint(job):
                raise Blocked('receipt không cùng job')
            results[key] = verify_envelope(envelope, invocation, job['slot'], slot['token'])
            if any(r.get('status') in ('ERROR', 'TIMEOUT') for r in results[key]):
                if receipt.get('method_failure'):
                    from bien_nhan import verify_method_failure
                    verify_method_failure(receipt['method_failure'], job, envelope, invocation)
                    validate_execution_links(job, invocation)
                    continue
                from bien_nhan import verify_dev_error_reproduction
                if not receipt.get('dev_error_reproduction'):
                    raise Blocked('snapshot lỗi chưa có finalization/phân loại được duyệt')
                verify_dev_error_reproduction(receipt['dev_error_reproduction'], job, envelope, invocation)
            validate_execution_links(job, invocation)
    return results


def snapshot_from_status(plan, state):
    slots = {}
    for job in plan['jobs']:
        key = fingerprint(job['slot'])
        last = state['jobs'].get(key)
        if last is None or last['state'] not in ('VERIFIED', 'BLOCKED'):
            raise Blocked('chưa đủ trạng thái cuối cho snapshot')
        slots[key] = {k: last[k] for k in ('state', 'token', 'receipt', 'reason') if k in last}
    return {'schema': 'T054-SNAPSHOT-1', 'plan_sha256': fingerprint(plan), 'slots': slots}


def validate_a4_slots(plan, runtimes):
    """Đủ cohort/arm/seed được kiểm bằng metadata trước lần đọc nhãn đầu."""
    if set(runtimes) != {'RE2-TT', 'Nezha-OB'}:
        raise Blocked('A4 cần cả hai dataset trước ghép nhãn')
    wanted = {}; expected_windows = {}; expected_sources = {}
    for ds, runtime in runtimes.items():
        if runtime.get('dataset') != ds:
            raise Blocked('runtime sai dataset')
        if plan['mode'] == 'test' and len(runtime['cases']) != {'RE2-TT': 60, 'Nezha-OB': 34}[ds]:
            raise Blocked('A4 khác toàn bộ cohort test đã khai')
        for oid, row in runtime['cases'].items():
            t = row.get('t', row.get('t_ns') // 10**9 if row.get('t_ns') is not None else None)
            if plan['mode'] != 'synthetic' and type(t) is not int:
                raise Blocked('mốc A4 chưa có nguồn kiểu số trước ghép nhãn')
            expected_windows[(ds, oid)] = {'t': t, 'half_width_s': 300} if t is not None else None
            expected_sources[(ds, oid)] = fingerprint(row)
            wanted[(ds, oid, 'M1', None)] = row['member_sha256']
            if ds == 'RE2-TT':
                for seed in (0, 1, 2):
                    wanted[(ds, oid, 'torai_B', seed)] = row['member_sha256']
            else:
                wanted[(ds, oid, 'simplerca', None)] = row['member_sha256']
    selected = {}
    for job in plan['jobs']:
        if not job.get('a4'):
            continue
        s = job['slot']; key = (s['dataset'], s['opaque_id'], s['arm'], s['seed'])
        if (s['view'] != 'main' or key in selected or key not in wanted
                or s['member_sha256'] != wanted[key]
                or (s['seed'] is not None and type(s['seed']) is not int)):
            raise Blocked('A4 trùng/sai arm/seed/window/member trước ghép nhãn')
        expected_window = expected_windows[(s['dataset'], s['opaque_id'])]
        if expected_window is not None and s['window'] != expected_window:
            raise Blocked('cửa sổ A4 khác runtime trước ghép nhãn')
        if plan['mode'] != 'synthetic' and s['source_sha256'] != expected_sources[(s['dataset'], s['opaque_id'])]:
            raise Blocked('nguồn slot A4 khác runtime trước ghép nhãn')
        selected[key] = s['member_sha256']
    if selected != wanted:
        raise Blocked('A4 chưa đủ mọi ca/seed trước ghép nhãn')
    if plan['mode'] == 'test':
        validate_ce_plan(plan, runtimes['RE2-TT'])


def validate_ce_plan(plan, runtime):
    """Mỗi ca TT có một lượt C-e hỗ trợ hoặc dòng insufficient đã ràng buộc nguồn."""
    covered = set()
    for job in plan['jobs']:
        s = job['slot']
        if s['view'] != 'ce':
            continue
        oid = s['opaque_id']; row = runtime['cases'].get(oid)
        if (s['dataset'] != 'RE2-TT' or s['arm'] != 'M1' or s['seed'] is not None or oid in covered
                or row is None or row.get('ce_history') != 'verified'
                or s['source_sha256'] != fingerprint(row)
                or s['window'] != {'t': row['t']-300, 'half_width_s': 300}):
            raise Blocked('C-e job khác nguồn/hỗ trợ hoặc bị trùng')
        covered.add(oid)
    for support in plan.get('ce_support', []):
        oid = support['opaque_id']; row = runtime['cases'].get(oid)
        if (support.get('dataset') != 'RE2-TT' or support.get('status') != 'INSUFFICIENT_EVIDENCE'
                or oid in covered or row is None or row.get('ce_history') != 'insufficient'
                or support.get('source_sha256') != fingerprint(row)):
            raise Blocked('C-e insufficient không có hỗ trợ nguồn riêng hoặc trùng lượt')
        covered.add(oid)
    if covered != set(runtime['cases']):
        raise Blocked('C-e thiếu ca/dòng hỗ trợ trước ghép nhãn')


def evaluate(snapshot, plan, label_refs, canonical_refs, runtimes, aliases, inventories, output):
    if plan.get('mode') == 'heldout':
        return evaluate_re3(snapshot, plan, label_refs, canonical_refs, runtimes, aliases, inventories, output)
    records = verify_snapshot(snapshot, plan['jobs'])  # trước mọi label reader
    validate_a4_slots(plan, runtimes)
    if snapshot['plan_sha256'] != fingerprint(plan):
        raise Blocked('snapshot khác plan')
    labels = {}
    for ds in runtimes:
        labels[ds] = compare_labels(read_pin(label_refs[ds]), read_pin(canonical_refs[ds]),
                                    runtimes[ds], aliases[ds], inventories[ds])
    append(Path(output) / 'exposure.jsonl', {'event': 'LABEL_JOIN', 'snapshot_sha256': fingerprint(snapshot)})
    sys.path[:0] = [str(ROOT / 'results/T-052/scripts'), str(ROOT / 'src')]
    from m1_danh_gia.pha2 import giai_ma_json
    import a4_v2
    tables = {}
    for ds in runtimes:
        left, right = {}, defaultdict(list)
        for job in plan['jobs']:
            s = job['slot']; key = fingerprint(s)
            if s['dataset'] != ds or not job.get('a4'):
                continue
            rows = giai_ma_json(records[key])
            if len(rows) != 1:
                raise Blocked('A4 cần đúng một record mỗi slot/seed')
            if s['arm'] == 'M1':
                left[s['opaque_id']] = rows[0]
            else:
                right[s['opaque_id']].append(rows[0])
        tables[ds] = left, right, labels[ds]
    expected = (60, 34) if plan['mode'] == 'test' else tuple(len(labels[ds]) for ds in ('RE2-TT', 'Nezha-OB'))
    result = a4_v2.evaluate(tables['RE2-TT'], tables['Nezha-OB'], torai_seeds=(0, 1, 2), expected_counts=expected)
    if plan.get('sensitivity_decision_ref'):
        approved_sensitivities(result, tables, plan['sensitivity_decision_ref'])
    atomic(Path(output) / 'a4.json', result)
    descriptive = describe(plan, records, labels)
    atomic(Path(output) / 'tables.json', descriptive)
    return result


def validate_re3_slots(plan, runtime):
    from nguon import validate_re3_protocol
    protocol = validate_re3_protocol(read_pin(plan['protocol_ref']))
    if (plan.get('mode') != 'heldout' or runtime.get('dataset') != 'RE3-OB'
            or len(runtime.get('cases', {})) != protocol['case_count']
            or {r['member_sha256'] for r in runtime['cases'].values()} != set(protocol['members'])):
        raise Blocked('RE3 report needs complete separate held-out cohort')
    wanted = {fingerprint(s) for s in protocol['slots']}
    if len(plan['jobs']) != len(wanted) or {fingerprint(j['slot']) for j in plan['jobs']} != wanted:
        raise Blocked('RE3 report missing/extra registered slots')
    metrics = protocol.get('metrics', [])
    if (not metrics or len(metrics) != len(set(metrics)) or not set(metrics) <= {
            'rr', 'ndcg@5', 'avg@5', 'hit@1', 'hit@3', 'hit@5'}
            or protocol.get('seed_aggregation') != 'mean_complete_case'
            or set(protocol.get('support_policy', {})) != {'NO_EVIDENCE', 'ERROR', 'TIMEOUT', 'UNSUPPORTED'}
            or any(v not in ('zero', 'separate') for v in protocol['support_policy'].values())
            or not protocol.get('worlds') or not set(protocol['worlds']) <= {'P', 'S_lo', 'S_hi'}):
        raise Blocked('WAIT_RE3_METRICS_SUPPORT_SEED_PROTOCOL')
    return protocol


def evaluate_re3(snapshot, plan, label_refs, canonical_refs, runtimes, aliases, inventories, output):
    """Separate descriptive held-out table. No A4 threshold, test or denominator."""
    if set(runtimes) != {'RE3-OB'} or set(label_refs) != {'RE3-OB'} or set(canonical_refs) != {'RE3-OB'}:
        raise Blocked('RE3 cannot share a main A4 label join')
    protocol = validate_re3_slots(plan, runtimes['RE3-OB'])
    if snapshot.get('plan_sha256') != fingerprint(plan):
        raise Blocked('RE3 snapshot not bound to complete plan')
    if any(v.get('state') != 'VERIFIED' for v in snapshot.get('slots', {}).values()):
        raise Blocked('RE3 unresolved slot: no labels joined')
    records = verify_snapshot(snapshot, plan['jobs'])
    from p3.re3 import validate_profile
    profile = validate_profile(read_pin(plan['re3_profile_ref']))
    if (aliases != {'RE3-OB': profile['aliases']} or inventories != {'RE3-OB': profile['inventory']}
            or runtimes['RE3-OB'].get('profile_sha256') != plan['re3_profile_ref']['sha256']):
        raise Blocked('RE3 report U/alias/profile differs from frozen inputs')
    # Structural result/variant checks precede the very first label reader.
    sys.path[:0] = [str(ROOT/'src')]
    from m1_danh_gia.pha2 import giai_ma_json
    from p3 import danh_gia
    decoded = {}
    for job in plan['jobs']:
        key = fingerprint(job['slot'])
        rows = giai_ma_json(records[key])
        variants = protocol.get('variants', {}).get(job['slot']['arm'])
        if not variants or [r.get('variant') for r in rows] != variants:
            raise Blocked('RE3 variants differ from declared report contract')
        for r in rows:
            if r['status'] == 'OK':
                for w in protocol['worlds']:
                    danh_gia.khoi_tu_ban_ghi(r['worlds'][w] if 'worlds' in r else r)
        decoded[key] = rows
    labels = compare_labels(read_pin(label_refs['RE3-OB']), read_pin(canonical_refs['RE3-OB']),
                            runtimes['RE3-OB'], profile['aliases'], profile['inventory'])
    if len({v['cell'] for v in labels.values()}) != protocol['cell_count']:
        raise Blocked('RE3 cell count differs from registered metadata')
    append(Path(output)/'exposure.jsonl', {'event': 'RE3_LABEL_JOIN', 'snapshot_sha256': fingerprint(snapshot)})
    rows, pooled = [], defaultdict(list)
    for job in plan['jobs']:
        s = job['slot']
        for rec in decoded[fingerprint(s)]:
            for world in protocol['worlds']:
                v = rec['worlds'][world] if 'worlds' in rec else rec
                status = rec['status']
                scored = danh_gia.cham_ca(dict(v, status=status), labels[s['opaque_id']]['root'])
                supported = status == 'OK' or protocol['support_policy'][status] == 'zero'
                scores = {m: scored[m] if supported else None for m in protocol['metrics']}
                row = dict(dataset='RE3-OB', opaque_id=s['opaque_id'], arm=s['arm'], seed=s['seed'],
                           variant=rec['variant'], world=world, status=status, supported=supported,
                           cell=labels[s['opaque_id']]['cell'], metrics=scores)
                rows.append(row)
                pooled[(s['opaque_id'], s['arm'], rec['variant'], world)].append(row)
    cases = []
    for (oid, arm, variant, world), seeds in pooled.items():
        if {r['seed'] for r in seeds} != set(protocol['arms'][arm]) or len(seeds) != len(protocol['arms'][arm]):
            raise Blocked('RE3 incomplete seed group; no surviving-seed average')
        supported = all(r['supported'] for r in seeds)
        cases.append(dict(dataset='RE3-OB', opaque_id=oid, arm=arm, variant=variant, world=world,
                          cell=labels[oid]['cell'], supported=supported,
                          seed_status=[r['status'] for r in seeds],
                          metrics={m: sum(r['metrics'][m] for r in seeds)/len(seeds) if supported else None
                                   for m in protocol['metrics']}))
    def summarize(groups):
        out = []
        for key, values in sorted(groups.items()):
            valid = [r for r in values if r['supported']]
            out.append({'group': list(key), 'total_cases': len(values), 'supported_cases': len(valid),
                        'separate_cases': len(values)-len(valid),
                        'metrics': {m: sum(r['metrics'][m] for r in valid)/len(valid) if valid else None
                                    for m in protocol['metrics']}})
        return out
    by_arm, by_cell = defaultdict(list), defaultdict(list)
    for r in cases:
        k = (r['arm'], r['variant'], r['world'])
        by_arm[k].append(r); by_cell[k+(r['cell'],)].append(r)
    result = dict(schema='T054-RE3-TABLES-1', dataset='RE3-OB', case_count=len(labels),
                  cell_count=protocol['cell_count'], per_seed=rows, per_case=cases,
                  by_arm=summarize(by_arm), by_cell=summarize(by_cell),
                  support_policy=protocol['support_policy'], protocol_ref=plan['protocol_ref'])
    atomic(Path(output)/'re3-tables.json', result)
    return result


def approved_sensitivities(result, tables, decision_ref):
    """Hai độ nhạy Minh duyệt; không đổi E04 hoặc mức OB từ phép chính."""
    from math import lcm
    import numpy as np
    import a4_v2
    from p3 import danh_gia
    decision = read_pin(decision_ref)
    if decision.get('status') != 'USER_CONFIRMED' or not decision.get('sensitivity'):
        raise Blocked('thiếu quyết định công thức độ nhạy')
    for ds, key in [('RE2-TT', 'TT'), ('Nezha-OB', 'OB')]:
        left, right, labels = tables[ds]
        cells = {oid: labels[oid]['cell'] for oid in left}
        kept = [oid for oid in left if left[oid]['status'] not in ('ERROR', 'TIMEOUT')
                and not any(r['status'] in ('ERROR', 'TIMEOUT') for r in right[oid])]
        for world, row in result[key].items():
            a = {oid: a4_v2._score(left[oid], labels[oid]['root'], world) for oid in left}
            b = {oid: a4_v2._mean_scores([a4_v2._score(r, labels[oid]['root']) for r in right[oid]]) for oid in left}
            metric = 'RR' if ds == 'RE2-TT' else 'Hit5_Q'
            delta = {oid: a[oid][metric] - b[oid][metric] for oid in left}
            if ds == 'RE2-TT':
                # Số nguyên chính xác: không dùng epsilon của helper ứng viên cũ.
                scale = lcm(*(v.denominator for v in delta.values()))
                values = [int(scale * delta[o]) for o in sorted(delta)]
                observed = abs(sum(values))
                rng = np.random.default_rng(20261005)
                signs = 2 * rng.integers(0, 2, size=(10000, len(values))) - 1
                exceed = sum(abs(sum(int(s) * v for s, v in zip(sample, values))) >= observed for sample in signs)
                row.pop('case_permutation_candidate', None)
                row['case_permutation'] = dict(p=Fraction(exceed + 1, 10001), draws=10000, seed=20261005,
                    status='USER_CONFIRMED_SENSITIVITY_ONLY', decision=decision_ref,
                    limit='Ca cùng ô có thể phụ thuộc; không điều khiển A4/chuyển mức.')
            excluded = row.pop('error_excluded_candidate')
            excluded.update(status='USER_CONFIRMED_SENSITIVITY_ONLY', decision=decision_ref,
                n=len(kept), cells=len({cells[o] for o in kept}),
                bootstrap=danh_gia.bootstrap({'M1': {o:a[o] for o in kept}, 'baseline': {o:b[o] for o in kept}},
                                             {o:cells[o] for o in kept}) if kept else None)
            row['error_excluded'] = excluded


def main_records_from_seal(seal_ref, key):
    bundle = read_pin(seal_ref)
    if key not in bundle['records']:
        raise Blocked('không có đúng khóa dataset/case/arm/window/seed trong main seal')
    return bundle['records'][key]


def seal_main(snapshot, jobs, destination):
    verified = verify_snapshot(snapshot, jobs)
    records = {}
    for job in jobs:
        slot = job['slot']; key = fingerprint(slot)
        if key not in verified or slot['arm'] == 'C-d3':
            continue
        record_key = '|'.join(str(slot[k]) for k in ('dataset', 'opaque_id', 'arm', 'view', 'seed'))
        if record_key in records:
            raise Blocked('trùng khóa main seal')
        rows = verified[key]
        records[record_key] = rows[0] if len(rows) == 1 else rows
    return atomic(destination, {'schema': 'T054-MAIN-SEAL-1', 'snapshot_sha256': fingerprint(snapshot), 'records': records})


def cd3_after_main(seal_ref, key, solver):
    """Lỗi solver không có quyền ghi vào main seal."""
    original = read_pin(seal_ref)
    record = main_records_from_seal(seal_ref, key)
    try:
        result = solver(record['extra']['dau_vao_cd3'])
    except Exception as exc:
        result = {'trang_thai': 'ERROR', 'error_type': type(exc).__name__}
    if fingerprint(read_pin(seal_ref)) != fingerprint(original):
        raise Blocked('solver làm đổi main seal')
    return result


def controls(m1, baselines):
    sys.path.insert(0, str(ROOT / 'src'))
    from m1 import doi_chung
    from p3 import danh_gia
    from m1_danh_gia.pha2 import giai_ma_json
    m1, baselines = giai_ma_json(m1), giai_ma_json(baselines)
    ranks = {k: [group for block in danh_gia.khoi_tu_ban_ghi(v) for group in block['groups']]
             if v['status'] == 'OK' else [] for k, v in baselines.items()}
    cc = doi_chung.cc({k: ranks[k] for k in ('baro', 'simplerca', 'tracerca')})
    simple = baselines['simplerca']
    votes = simple.get('extra', {}).get('phieu')
    if votes is None:
        # Điểm vote ở bản ghi M4, không tái dùng điểm M1 để tạo C-g.
        votes = {r['entity']: r['key'][0] for r in simple.get('entity_ranking', [])}
    graph = m1.get('extra', {}).get('canh')
    if graph is None:
        if m1.get('status') in ('ERROR', 'TIMEOUT'):
            return {'C-c': cc}  # C-c độc lập; C-g thiếu graph, không dựng/rút từ nhãn.
        raise Blocked('M1 thiếu graph cho C-g; không dựng từ nhãn')
    return {'C-c': cc, 'C-g': doi_chung.cg(votes, ranks['simplerca'], [tuple(e) for e in graph])}


def describe(plan, sealed_records, labels):
    """Ba world, seed trong ca, vùng/C-e/N và đối chứng dẫn xuất; không chạy lại phương pháp."""
    sys.path[:0] = [str(ROOT / 'results/T-052/scripts'), str(ROOT / 'src')]
    from m1_danh_gia.pha2 import giai_ma_json
    from m1_danh_gia import e7
    from p3 import danh_gia
    from bang_doc_lap import exact_score
    from vung_ce import position
    pool = defaultdict(lambda: defaultdict(list))
    for job in plan['jobs']:
        key = fingerprint(job['slot'])
        if key not in sealed_records:
            continue
        s = job['slot']
        actual = giai_ma_json(sealed_records[key])
        if s['arm'] == 'circa' and s['dataset'] == 'RE2-TT':
            primary = [r for r in actual if r.get('variant') == 'ols+rht_da']
            auxiliary = [r for r in actual if r.get('variant') == 'ols+rht']
            if len(primary) != 1 or len(auxiliary) != 1:
                raise Blocked('CIRCA thiếu vế chính/phụ; không bình quân hai variant')
            pool[(s['dataset'], s['view'], s['opaque_id'])]['circa'].extend(primary)
            pool[(s['dataset'], s['view'], s['opaque_id'])]['circa_rht_aux'].extend(auxiliary)
        else:
            pool[(s['dataset'], s['view'], s['opaque_id'])][s['arm']].extend(actual)
    rows, region_rows, ce_rows, positions = [], [], [], []
    missing = [[j['slot']['dataset'], j['slot']['opaque_id'], j['slot']['view'], j['slot']['arm'],
                'BLOCKED_NO_VERIFIED_RESULT'] for j in plan['jobs'] if fingerprint(j['slot']) not in sealed_records]
    by_world = defaultdict(dict)
    for support in plan.get('ce_support', []):
        ce_rows.append(dict(support, U=len(plan['inventories']['RE2-TT']), top_mass=None,
                           O=None, returned=None, V0=None, N1=None,
                           future_root_score=None, limit='Không đủ lịch sử; ngoài mẫu số miền C-e hỗ trợ.'))
    for (ds, view, oid), arms in sorted(pool.items()):
        root = labels[ds][oid]['root']
        if view == 'ce':
            if 'M1' not in arms:
                missing.append([ds, oid, 'ce', 'M1']); continue
            rec, = arms['M1']
            if rec['status'] in ('ERROR', 'TIMEOUT'):
                ce_rows.append({'dataset': ds, 'opaque_id': oid, 'status': rec['status'],
                    'U': len(plan['inventories'][ds]), 'top_mass': None, 'O': None, 'returned': None,
                    'V0': None, 'N1': None, 'future_root_score': exact_score(rec, root),
                    'limit': 'Lỗi phương pháp trên cửa sổ hỗ trợ; chưa có hạng/trung gian, không gán N1/O/V0=0.'})
                continue
            ranked = danh_gia.khoi_tu_ban_ghi(rec) if rec['status'] == 'OK' else []
            returned = [e for block in ranked for group in block['groups'] for e in group]
            mass = {e: danh_gia.phan_bo_hang(ranked, e).get(1, Fraction(0)) for e in returned}
            n = len(returned)
            ce_rows.append({'dataset': ds, 'opaque_id': oid, 'status': rec['status'], 'top_mass': {k: v for k, v in mass.items() if v},
                'U': len(plan['inventories'][ds]), 'O': rec['sets']['observed'], 'returned': n,
                'V0': rec['verdict'], 'N1': sum(v == 1 for v in rec['extra']['tang_P'].values()),
                'future_root_score': exact_score(rec, root),
                'chance_returned_RR': sum((Fraction(1, r) for r in range(1, n+1)), Fraction(0)) / n if n and root in returned else None,
                'limit': 'Trước tiêm chưa xác nhận lành; root tương lai không hiệu chuẩn detector.'})
            continue
        if 'M1' in arms:
            m1, = arms['M1']
            if all(k in arms for k in ('baro', 'simplerca', 'tracerca')):
                derived = controls(m1, {k: arms[k][0] for k in ('baro', 'simplerca', 'tracerca')})
                if 'C-g' not in derived:
                    missing.append([ds, oid, 'main', 'C-g', 'MAIN_METHOD_DID_NOT_RETURN_GRAPH'])
                for name, item in derived.items():
                    arms[name] = [dict(item, status=item['trang_thai'])]
            for name, item in m1.get('extra', {}).get('doi_chung', {}).items():
                if name in ('C-d1', 'C-d2'):
                    arms[name] = [dict(item, status=item['trang_thai'])]
            for name in ('M1', 'T12-on'):
                if name in arms and arms[name][0].get('region') is not None:
                    rec = arms[name][0]; region = rec['region']
                    region_rows.append({'dataset': ds, 'opaque_id': oid, 'arm': name,
                        'O': rec['sets']['observed'],
                        **{f'cach_{k}': e7.mo_ta(region['T'], region[f'cach_{k}'], root, rec['sets']['observed']) for k in (1, 2)}})
        if 'C-a0' in arms:
            rec = arms['C-a0'][0]
            if {'G_N', 'don_vi_phan_vi'} <= set(rec.get('extra', {})):
                nodes = {u['ma'].split('|', 2)[1] for u in rec['extra']['don_vi_phan_vi'] if u['ma'].startswith('op|') and u['n_N'] > 0}
                edges = {tuple(e) for e in rec['extra']['G_N']}
                if not all(a in nodes and b in nodes for a, b in edges):
                    raise Blocked('vị trí N có cạnh ngoài node N')
                positions.append({'dataset': ds, 'opaque_id': oid, 'p75': position(nodes, edges, root, 75),
                                  'p90': position(nodes, edges, root, 90)})
            else:
                missing.append([ds, oid, 'position_N', 'MISSING_FIELDS'])
        for arm, records in sorted(arms.items()):
            worlds = ('P', 'S_lo', 'S_hi') if arm not in ('C-c', 'C-g', 'C-d1', 'C-d2', 'C-d3', 'torai_A') else ('P',)
            if arm in ('torai_A', 'torai_B') and ds == 'RE2-TT' and (len(records) != 3 or {r.get('seed') for r in records} != {0, 1, 2}):
                raise Blocked('bảng mô tả không bình quân seed sống')
            for world in worlds:
                scored = []
                for record in records:
                    if record.get('method') == 'M1' and record['status'] == 'OK':
                        record = dict(record, blocks=record['worlds'][world]['blocks'])
                    scored.append(exact_score(record, root))
                mean = {k: sum(r[k] for r in scored) / len(scored) for k in (*danh_gia.DO_DO_BOOT, 'RR', 'Hit5_Q')}
                row = {'dataset': ds, 'opaque_id': oid, 'arm': arm, 'world': world, 'seed_count': len(scored),
                       'statuses': [r['status'] for r in records], 'metrics': mean,
                       'cell': labels[ds][oid]['cell'], 'fault': labels[ds][oid]['fault'],
                       'auxiliary': arm.endswith('_aux') or arm == 'torai_A'}
                rows.append(row)
                by_world[(ds, world)].setdefault(arm, {})[oid] = mean
    summaries = []
    for (ds, world), table in by_world.items():
        complete = {arm: ca for arm, ca in table.items() if set(ca) == set(labels[ds])}
        cells = {oid: labels[ds][oid]['cell'] for oid in labels[ds]}
        summaries.append({'dataset': ds, 'world': world,
                          'complete_arms': sorted(complete), 'incomplete_arms': sorted(set(table)-set(complete)),
                          'bootstrap': danh_gia.bootstrap(complete, cells) if complete else None,
                          'paired_RR': {a + ' - ' + b: {
                              'win': sum(complete[a][o]['RR'] > complete[b][o]['RR'] for o in cells),
                              'tie': sum(complete[a][o]['RR'] == complete[b][o]['RR'] for o in cells),
                              'loss': sum(complete[a][o]['RR'] < complete[b][o]['RR'] for o in cells)}
                              for a in sorted(complete) for b in sorted(complete) if a < b},
                          'by_fault': {fault: {arm: {metric: sum(ca[o][metric] for o in ca if labels[ds][o]['fault'] == fault) /
                               sum(labels[ds][o]['fault'] == fault for o in ca) for metric in danh_gia.DO_DO_BOOT}
                               for arm, ca in complete.items()} for fault in sorted({v['fault'] for v in labels[ds].values()})}})
    return {'rows': rows, 'summaries': summaries, 'regions': region_rows, 'ce': ce_rows, 'position_N': positions,
            'missing': missing, 'limits': ['Vùng nghi ngờ; không có P/R/F1 vùng ảnh hưởng.',
            'Không suy causal topology thật; tín hiệu/chọn cấu hình D23 vẫn có điều kiện.',
            'C-d3 cần main seal và output worker riêng; OB không có solver mới.']}
