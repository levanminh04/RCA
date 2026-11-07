"""Nguồn phi nhãn và nhãn evaluator là hai đầu vào độc lập."""
from pathlib import Path
from bien_nhan import ROOT, Blocked, fingerprint, digest, read_pin, no_labels


def source_row(row, data_root):
    no_labels(row)
    paths = {}
    base = Path(data_root).resolve()
    for name, meta in row['files'].items():
        rel = meta['path']
        if '\\' in rel or ':' in rel or any(p in ('', '.', '..') for p in rel.split('/')):
            raise Blocked('locator không hợp lệ')
        p = (base / rel).resolve()
        if not p.is_relative_to(base) or not p.is_file():
            raise Blocked('nguồn ngoài gốc/không tồn tại')
        if p.stat().st_size != meta['bytes'] or digest(p) != meta['sha256']:
            raise Blocked('byte/hash nguồn khác bản đã cấp')
        paths[name] = str(p)
    return paths


def compare_sources(runtime, independent, dataset, revision):
    """Ref independent do người cấp chỉ định ngoài runtime, không lấy từ runtime."""
    if independent.get('schema') == 'T054-DEV-ORIGINALS-1':
        independent = original_dev_sources(independent)
    no_labels(runtime); no_labels(independent)
    if (runtime['dataset'] != dataset or independent['dataset'] != dataset or
            independent['g1_revision'] != revision or runtime['g1_revision'] != revision):
        raise Blocked('dataset/revision nguồn khác G1')
    by_member = independent['cases_by_member']
    rows = runtime['cases']
    if len({r['member_sha256'] for r in rows.values()}) != len(rows):
        raise Blocked('trùng thành viên')
    if set(by_member) != {r['member_sha256'] for r in rows.values()}:
        raise Blocked('cohort khác nguồn độc lập')
    for oid, row in rows.items():
        if fingerprint(row) != fingerprint(by_member[row['member_sha256']]):
            raise Blocked('file/mốc/support khác nguồn độc lập')
    return {oid: fingerprint(r) for oid, r in rows.items()}


def original_dev_sources(descriptor):
    """Dựng lại nguồn chuẩn từ G1/allowlist/command gốc, không tin bản runtime mới."""
    import csv
    import io
    allow = read_pin(descriptor['allowlist_ref'])
    g1_pin = descriptor['g1_ref']
    path = Path(g1_pin['path'])
    if not path.is_absolute():
        path = ROOT / path
    if digest(path) != g1_pin['sha256'] or descriptor['g1_revision'] != g1_pin['sha256']:
        raise Blocked('G1 gốc khác pin')
    ds = descriptor['dataset']
    members = [r for r in csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig')))
               if r['dataset'] == ds and r['vai_tro'] == 'dev']
    original = {r['opaque_id']: r for r in allow['cases']}
    chosen = descriptor['selected_ids']
    if len(chosen) != len(set(chosen)) or not set(chosen) <= set(original):
        raise Blocked('dev selection không thuộc allowlist gốc')
    out = {}
    for oid in chosen:
        row = original[oid]
        if ds == 'RE2-TT':
            case = Path(row['case_dir']).name
            found = [m for m in members if m['case'] == case]
            if oid != 'dev-' + row['files']['metrics.parquet']['sha256'][:10]:
                raise Blocked('mã TT không cùng file gốc')
            command = read_pin(descriptor['command_refs'][oid])
            job = command['job']
            if job['opaque_id'] != oid or job['dataset'] != ds or job['window'] != 'that':
                raise Blocked('mốc TT không từ command main đúng ca')
            normalized = {'t': job['t'], 'ce_history': 'unknown'}
            if oid in descriptor.get('ce_evidence', {}):
                evidence = descriptor['ce_evidence'][oid]
                ce_job = read_pin(evidence['command'])['job']
                from pilot import reference
                record = reference(evidence['record'], evidence['config_id'])
                t_ns = (job['t'] - 300) * 10**9
                if (ce_job['opaque_id'] != oid or ce_job['dataset'] != ds or ce_job['window'] != 'ce'
                        or ce_job['t'] != job['t'] - 300 or record.get('opaque_id') != oid
                        or record.get('status') != 'OK'
                        or record['window']['N'] != [t_ns-300*10**9, t_ns]
                        or record['window']['A'] != [t_ns, t_ns+300*10**9]
                        or ce_job['source_bytes'] != sum(v['bytes'] for v in row['files'].values())):
                    raise Blocked('C-e evidence không cùng source/case/window đã ghim')
                coverage = record.get('coverage', {})
                if set(coverage) != {'trace', 'metric', 'log'} or any(
                    c.get('trang_thai') != 'OK' or not c.get('F')
                    or c['F'][0] > t_ns-300*10**9 or c['F'][1] < t_ns+300*10**9
                    or any(c['o'][w].get('OPEN', 0) for w in ('N', 'A')) for c in coverage.values()):
                    raise Blocked('C-e lịch sử/A0 chưa đủ căn cứ; không tự gán verified')
                normalized['ce_history'] = 'verified'

        elif ds == 'Nezha-OB':
            import hashlib
            found = [m for m in members if 'dev-' + hashlib.sha256(m['case'].encode()).hexdigest()[:10] == oid]
            case = found[0]['case'] if len(found) == 1 else None
            normalized = {k: row[k] for k in ('t_ns', 'trace_guard_s')}
        else:
            raise Blocked('originals chỉ dev TT/Nezha')
        if len(found) != 1:
            raise Blocked('thành viên không khớp duy nhất G1 dev')
        member = fingerprint([ds, case])
        normalized.update(member_sha256=member, files=row['files'])
        out[member] = normalized
    return {'dataset': ds, 'g1_revision': descriptor['g1_revision'], 'cases_by_member': out}


def compare_labels(labels, independent, runtime, aliases, universe):
    if independent.get('schema') == 'T054-DEV-LABEL-ORIGINALS-1':
        independent = original_dev_labels(independent, aliases)
    if (labels['dataset'] != runtime['dataset'] or independent['dataset'] != runtime['dataset']
            or labels['g1_revision'] != runtime['g1_revision']
            or independent['g1_revision'] != runtime['g1_revision']
            or labels.get('alias_sha256') != fingerprint(aliases)
            or independent.get('alias_sha256') != fingerprint(aliases)):
        raise Blocked('nhãn sai dataset/G1 revision/alias')
    if set(labels['cases']) != set(runtime['cases']):
        raise Blocked('nhãn thiếu/thừa ca')
    if set(independent['by_member']) != {r['member_sha256'] for r in runtime['cases'].values()}:
        raise Blocked('nguồn nhãn thiếu/thừa thành viên')
    result = {}
    for oid, binding in runtime['cases'].items():
        row = labels['cases'][oid]
        trusted = independent['by_member'][binding['member_sha256']]
        if row != trusted or row['member_sha256'] != binding['member_sha256']:
            raise Blocked('root/fault/cell không khớp nguồn nhãn độc lập')
        canonical_root = aliases.get(row['root'], row['root'])
        if canonical_root != row['root'] or canonical_root not in universe:
            raise Blocked('root ngoài U hoặc chưa canonicalize: đối chiếu nguồn')
        expected_cell = [runtime['dataset'], canonical_root, row['fault']]
        if row['cell'] != expected_cell:
            raise Blocked('ô không theo dataset/root/fault G1')
        result[oid] = dict(row, cell='|'.join(expected_cell))
    return result


def validate_slot(slot, policy):
    no_labels(slot)
    required = {'dataset', 'opaque_id', 'member_sha256', 'arm', 'view', 'seed', 'window',
                'source_sha256', 'config_sha256', 'environment_sha256'}
    if not required <= set(slot) or slot['dataset'] not in ('RE2-TT', 'Nezha-OB', 'SYNTHETIC'):
        raise Blocked('slot thiếu khóa hoặc dataset ngoài grant')
    if slot['view'] == 'ce' and (slot['dataset'] != 'RE2-TT' or slot['arm'] != 'M1'):
        raise Blocked('C-e chỉ TT/M1')
    if slot['arm'] == 'torai_A' and slot['dataset'] != 'RE2-TT':
        raise Blocked('TORAI A chỉ là bảng phụ TT đã khai')
    if slot['arm'] in ('torai_A', 'torai_B') and slot['dataset'] == 'RE2-TT':
        if type(slot['seed']) is not int or slot['seed'] not in (0, 1, 2):
            raise Blocked('TORAI B cần seed 0/1/2')
    elif slot['seed'] is not None:
        raise Blocked('seed ngoài ma trận')
    if policy.get('mode') != 'synthetic' and any(slot[k] is None for k in required):
        # None là seed hợp lệ cho vế tất định, không là bằng chứng env/window.
        if any(slot[k] is None for k in required - {'seed'}):
            raise Blocked('slot thực chưa ghim đủ')


def authorize(plan, authority, action):
    """Authority là hồ sơ của lời Minh, không phải cờ --granted từ worker."""
    mode = plan['mode']
    if mode == 'synthetic':
        if action not in ('run', 'report'):
            raise Blocked('hành động fixture lạ')
        if any(j.get('kind') != 'synthetic' for j in plan['jobs']):
            raise Blocked('fixture không được gọi tuyến dữ liệu thật')
        return
    if authority.get('pilot_grant') is not True and mode == 'dev':
        raise Blocked('WAIT_PILOT_GRANT')
    if mode == 'test':
        if authority.get('g3') is not True:
            raise Blocked('WAIT_G3')
        if authority.get('test_grant') is not True:
            raise Blocked('WAIT_TEST_GRANT')
        if plan.get('host_role') != 'local':
            raise Blocked('test chỉ local, chưa có ngoại lệ cloud')
        if not plan.get('protocol_ref') or read_pin(plan['protocol_ref']).get('status') != 'LOCKED_G3':
            raise Blocked('WAIT_LOCKED_PROTOCOL')
        validate_locked_plan(plan, read_pin(plan['protocol_ref']))
    if mode not in ('dev', 'test'):
        raise Blocked('mode chưa được cấp')
    if any(j.get('evaluation_mode') != mode or j.get('kind') == 'synthetic' for j in plan['jobs']):
        raise Blocked('miền quyền của job khác plan')
    if any(j['slot']['arm'] == 'torai_A' for j in plan['jobs']) and authority.get('torai_A_source_grant') is not True:
        raise Blocked('WAIT_TORAI_A_SOURCE_GRANT')
    for job in plan['jobs']:
        if job['slot']['arm'] == 'torai_A':
            declared = authority.get('torai_A_source_sha256')
            if declared != job.get('author_source_ref', {}).get('sha256') or declared != job['slot'].get('author_source_sha256'):
                raise Blocked('grant TORAI A không trỏ đúng nguồn đã pin')
    if not authority.get('source') or not authority.get('plan_sha256') == fingerprint(plan):
        raise Blocked('quyền không trỏ đúng plan')
    authority_pin = authority['source']
    authority_path = Path(authority_pin['path'])
    if not authority_path.is_absolute():
        authority_path = ROOT / authority_path
    if (digest(authority_path) != authority_pin['sha256'] or
            authority_path.stat().st_size != authority_pin.get('bytes', authority_path.stat().st_size)):
        raise Blocked('nguồn quyền khác pin')
    if not plan.get('budget') or plan.get('open_before_run'):
        raise Blocked('WAIT_POLICY_BUDGET')
    from dieu_phoi import check_budget
    check_budget(plan)


def validate_locked_plan(plan, protocol):
    """Plan được grant vẫn phải khớp code/config/env/policy khóa, trước I/O dữ liệu."""
    c = read_pin(protocol['dispatch_contract_ref'])
    if (c.get('schema') != 'T054-DISPATCH-CONTRACT-1'
            or plan.get('workers', 1) != c['workers'] or plan.get('monitor') != c['monitor']
            or plan.get('budget') != c['budget']
            or plan.get('sensitivity_decision_ref') != c['sensitivity_decision_ref']):
        raise Blocked('plan vận hành/độ nhạy khác bản khóa')
    from bien_nhan import failure_policy
    for job in plan['jobs']:
        s = job['slot']; arm = s['arm']
        family = arm in protocol['configurations']
        expected = (protocol['configurations'][arm]['sha256'] if family else
                    fingerprint({'cd3': 'same sealed M1'}) if arm == 'C-d3' else c['baseline_config_sha256'].get(arm))
        if (not expected or s['config_sha256'] != expected
                or (arm != 'C-d3' and fingerprint(job['config']) != expected)
                or job.get('code_pins') != c['code_pins'] or job.get('protocol_ref') != plan['protocol_ref']):
            raise Blocked('job code/config/protocol khác bản khóa')
        torai = arm in ('torai_A','torai_B') and s['dataset'] == 'RE2-TT'
        kind = 'm1' if family else 'cd3' if arm == 'C-d3' else 'torai_pipeline' if torai else 'baseline'
        if job['kind'] != kind or job['timeout_s'] != c['timeout_s']['C-d3' if arm=='C-d3' else 'main_slot']:
            raise Blocked('kind/timeout khác vế khóa')
        if s['environment_sha256'] != c['environment_sha256']['py38' if torai else 'main']:
            raise Blocked('environment slot khác bản khóa')
        if torai and job.get('prep_environment_sha256') != c['environment_sha256']['main']:
            raise Blocked('TORAI prep environment khác bản khóa')
        if arm == 'T12-on' and job.get('static_snapshot') != protocol['snapshots'][s['dataset']]:
            raise Blocked('T12 dùng snapshot khác bản khóa')
        policy = failure_policy(job)
        candidate = read_pin(c['failure_policy_candidate_ref'])
        if ({k:v for k,v in policy.items() if k not in ('scope','main_allowed')}
                != {k:v for k,v in candidate.items() if k not in ('scope','main_allowed')}):
            raise Blocked('chính sách phân loại lỗi khác bản khóa')


def main_dependency_record(job, seal_ref):
    """Dependency được khai trước; hash output main chỉ được nối sau khi seal."""
    from bien_nhan import verify_envelope
    dep = job['main_dependency']; seal = read_pin(seal_ref)
    parent = dep['slot']; own = job['slot']
    if (parent.get('arm') != 'M1' or parent.get('view') != 'main' or parent.get('seed') is not None
            or any(parent.get(k) != own.get(k) for k in ('dataset', 'opaque_id', 'member_sha256', 'window', 'source_sha256'))):
        raise Blocked('C-d3 dependency khác ca/cửa sổ/nguồn main')
    key = '|'.join(str(parent[k]) for k in ('dataset', 'opaque_id', 'arm', 'view', 'seed'))
    if (seal.get('schema') != 'T054-MAIN-SEAL-2' or seal.get('parent_slot_sha256') != fingerprint(parent)
            or seal.get('parent_job_sha256') != dep['job_sha256'] or set(seal.get('records', {})) != {key}):
        raise Blocked('seal không cùng dependency đã đăng ký')
    receipt = read_pin(seal['producer_receipt'])
    if receipt['job_sha256'] != dep['job_sha256']:
        raise Blocked('producer của main không khớp plan')
    envelope = read_pin(receipt['result']); invocation = read_pin(receipt['invocation'])
    records = verify_envelope(envelope, invocation, parent, envelope['token'])
    if len(records) != 1 or records[0] != seal['records'][key]:
        raise Blocked('main seal khác output đã verify của producer')
    return records[0], key


def validate_execution_links(job, invocation):
    if job.get('main_dependency'):
        if invocation.get('dependency_sha256') != fingerprint(job['main_dependency']):
            raise Blocked('invocation đổi dependency đã đăng ký')
        _, key = main_dependency_record(job, invocation['main_seal_ref'])
        if invocation.get('main_key') != key:
            raise Blocked('C-d3 sai lookup trong invocation')
    if job['kind'] == 'torai_pipeline' or job.get('pipeline_fixture'):
        prep = read_pin(invocation['prepared_ref'])
        if prep['token'] != invocation['token'] or prep['slot_sha256'] != fingerprint(job['slot']):
            raise Blocked('TORAI method không cùng prep đã xử lý')
        for pin in prep['tables'].values():
            path = Path(pin['path'])
            if path.stat().st_size != pin['bytes'] or digest(path) != pin['sha256']:
                raise Blocked('CSV khác prep đã thực chạy')
        if job['slot']['arm'] == 'torai_A':
            source = prep.get('author_source_ref')
            if not source or source != job.get('author_source_ref') or source['sha256'] != job['slot'].get('author_source_sha256'):
                raise Blocked('prep TORAI A khác nguồn đã khai/grant')
            read_pin(source)


def author_source(job):
    """Chỉ gọi sau grant ở CLI; không suy đường dẫn A từ tên ca/nhãn."""
    pin = job['author_source_ref']
    if pin['sha256'] != job['slot'].get('author_source_sha256'):
        raise Blocked('TORAI A source ref khác slot')
    source = read_pin(pin); no_labels(source)
    if job['kind'] == 'synthetic':
        from bien_nhan import OUT
        fixture_root = Path(source['data_root']).resolve()
        if not fixture_root.is_relative_to(OUT / 'runs') or fixture_root.name != 'synthetic-data':
            raise Blocked('nguồn A giả ngoài vùng dữ liệu tự sinh')
    if (source.get('schema') != 'T054-TORAI-A-SOURCE-1' or source.get('dataset') != 'RE2-TT'
            or source.get('g1_revision') != job['g1_revision']):
        raise Blocked('sai dataset/revision nguồn TORAI A')
    row = source['cases_by_member'][job['slot']['member_sha256']]
    if set(row['files']) != {'logts', 'tracets_err', 'tracets_lat'}:
        raise Blocked('TORAI A cần đúng ba CSV đã cấp')
    return source_row(row, source['data_root'])


def original_dev_labels(descriptor, aliases):
    """Chỉ evaluator sau seal gọi. G1 gốc là nguồn nhãn, tách khỏi runtime mới."""
    import csv
    import io
    source = original_dev_sources(descriptor['source_descriptor'])
    pin = descriptor['source_descriptor']['g1_ref']
    path = Path(pin['path'])
    if not path.is_absolute():
        path = ROOT / path
    if digest(path) != pin['sha256']:
        raise Blocked('nguồn G1 nhãn đổi hash')
    ds = descriptor['source_descriptor']['dataset']
    by_member = {}
    for row in csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'))):
        if row['dataset'] != ds or row['vai_tro'] != 'dev':
            continue
        member = fingerprint([ds, row['case']])
        if member not in source['cases_by_member']:
            continue
        canonical = aliases.get(row['root'], row['root'])
        by_member[member] = {'member_sha256': member, 'root': canonical,
                             'fault': row['fault'], 'cell': [ds, canonical, row['fault']]}
    if set(by_member) != set(source['cases_by_member']):
        raise Blocked('G1 dev label thiếu/thừa thành viên')
    return {'dataset': ds, 'g1_revision': pin['sha256'],
            'alias_sha256': fingerprint(aliases), 'by_member': by_member}
