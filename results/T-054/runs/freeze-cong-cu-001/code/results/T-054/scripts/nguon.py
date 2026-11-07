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


def compare_labels(labels, independent, runtime, aliases, universe):
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
    if slot['arm'] == 'torai_B' and slot['dataset'] == 'RE2-TT':
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
    if mode not in ('dev', 'test'):
        raise Blocked('mode chưa được cấp')
    if not authority.get('source') or not authority.get('plan_sha256') == fingerprint(plan):
        raise Blocked('quyền không trỏ đúng plan')
    read_pin(authority['source'])
    if not plan.get('budget') or plan.get('open_before_run'):
        raise Blocked('WAIT_POLICY_BUDGET')
