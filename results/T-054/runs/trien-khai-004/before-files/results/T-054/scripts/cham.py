"""Chỉ nối nhãn sau snapshot đủ A4 và kiểm nguồn nhãn độc lập."""
import sys
from collections import defaultdict
from pathlib import Path
from fractions import Fraction

from bien_nhan import (ROOT, OUT, Blocked, atomic, append, fingerprint, read_pin, ref,
                       verify_envelope)
from nguon import compare_labels, validate_execution_links


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


def evaluate(snapshot, plan, label_refs, canonical_refs, runtimes, aliases, inventories, output):
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
    atomic(Path(output) / 'a4.json', result)
    descriptive = describe(plan, records, labels)
    atomic(Path(output) / 'tables.json', descriptive)
    return result


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
    rows, region_rows, ce_rows, positions, missing = [], [], [], [], []
    by_world = defaultdict(dict)
    for (ds, view, oid), arms in sorted(pool.items()):
        root = labels[ds][oid]['root']
        if view == 'ce':
            if 'M1' not in arms:
                missing.append([ds, oid, 'ce', 'M1']); continue
            rec, = arms['M1']
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
