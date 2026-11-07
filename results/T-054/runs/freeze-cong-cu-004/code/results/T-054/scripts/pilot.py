"""Pilot chỉ sau grant ghim plan; so field chính xác với bản nguồn."""
import copy
import gzip
import json
from pathlib import Path
from bien_nhan import ROOT, Blocked, digest, fingerprint, read_pin


def comparable(record, control=False):
    record = copy.deepcopy(record)
    for k in ('opaque_id', 'config_id', 'variant'):
        record.pop(k, None)
    if control:
        record['region'] = None
    if 'extra' in record:
        record['extra'].pop('dau_vao_cd3', None)
        record['extra'].get('doi_chung', {}).pop('C-d3', None)
    return record


def reference(pin, config_id=None):
    p = Path(pin['path'])
    if not p.is_absolute(): p = ROOT / p
    if p.suffix != '.gz':
        return read_pin(pin)
    if digest(p) != pin['sha256']:
        raise Blocked('native reference khác pin')
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        rows = [json.loads(line) for line in f]
    found = [r for r in rows if r.get('config_id') == config_id]
    if len(found) != 1:
        raise Blocked('native reference thiếu/trùng config')
    return found[0]


def compare(reference_pin, observed, *, source_machine, target_machine, tolerance=None,
            config_id=None, control=False):
    expected = reference(reference_pin, config_id)
    a, b = comparable(expected, control), comparable(observed, control)
    if a == b:
        return {'PASS': True, 'comparison': 'exact', 'source_machine': source_machine,
                'target_machine': target_machine, 'reference': reference_pin}
    # Dung sai chưa được Minh khóa: không tự chọn để cho qua.
    if source_machine != target_machine and tolerance is None:
        raise Blocked('parity khác máy lệch, dung sai chưa khóa')
    raise Blocked('status/intermediate/ranking/region parity lệch; cần phân xử từng field')


def plan_candidate():
    return {'status': 'CANDIDATE_WAIT_PILOT_GRANT', 'measured_runtime': None,
            'local': ['TT nhẹ/nặng + C-e', 'OB E2/C-d2 giúp và đối chiếu', 'T12 vùng đổi/không đổi',
                      'TORAI 3 seed + prep cache byte parity', 'đo throughput 1 rồi 2/3 worker'],
            'ec2_1': ['TT có native cùng máy và nhánh driver còn thiếu, sau identity/env/sync grant'],
            'ec2_2': 'Chỉ phát khi có nhánh driver cần thiết và giảm đường găng; chưa tự dựng thêm lô.',
            'reference_sources': ['T-024', 'T-026', 'T-050', 'T-053', 'T-051'],
            'source_machine_per_window': 'required_before_run', 'budget': None,
            'cross_machine_tolerance': None, 'ssh_performed': False, 'dev_pilot_run': False,
            'note': 'Không dùng thiếu quyền pilot để dừng việc cài/fixture độc lập.'}


def concrete_pilot_proposal(protocol, native_candidates, baseline_tables):
    """Chỉ dùng metadata/kết quả dev đã pin; không mở telemetry hoặc map private."""
    arms = tuple(protocol['configurations'])
    owners = {'dev-a915aa2424': 'ec2_1', 'dev-bcbd4f46ae': 'ec2_2',
              'dev-a5cabe5fa7': 'local', 'dev-03d4910932': 'local',
              'dev-607751ac0a': 'local', 'dev-2bfc97b01e': 'local',
              'dev-63c30faf34': 'local', 'dev-5467884de4': 'local'}
    ce_cases = {'dev-a915aa2424', 'dev-a5cabe5fa7'}
    specs = []
    for candidate in native_candidates:
        oid = candidate['opaque_id']; window = candidate['window']
        if oid not in owners or (window == 'ce' and oid not in ce_cases):
            continue
        for arm in (('M1',) if window == 'ce' else arms):
            specs.append({'dataset': candidate['dataset'], 'opaque_id': oid,
                          'view': 'ce' if window == 'ce' else 'main', 'arm': arm, 'seed': None,
                          'host': owners[oid], 'timeout_s_proposed': 600,
                          'reference_machine': candidate['native_machine'], 'native_ref': candidate['native_record'],
                          'command_ref': candidate['native_command_pin']})
    name_map = {'microrank': 'microrank_full', 'circa': 'circa_ols_da'}
    baseline_refs = []
    for ds, oid in [('RE2-TT', 'dev-a5cabe5fa7'), ('Nezha-OB', 'dev-607751ac0a')]:
        methods = (baseline_tables[ds]['methods'] if ds == 'RE2-TT'
                   else baseline_tables[ds]['tables']['main']['methods'])
        for arm in ('baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai_B'):
            seeds = (0, 1, 2) if ds == 'RE2-TT' and arm == 'torai_B' else (None,)
            for seed in seeds:
                selected = []
                for pin in methods[name_map.get(arm, arm)]['source_records']:
                    if pin['opaque_id'] != oid:
                        continue
                    record = read_pin(pin)
                    if record.get('seed') == seed:
                        selected.append(pin)
                if len(selected) != 1:
                    raise Blocked('pilot thiếu/trùng baseline reference đúng seed')
                baseline_refs.append({'dataset': ds, 'opaque_id': oid, 'arm': arm, 'seed': seed,
                                      'host': 'local', 'view': 'main', 'timeout_s_proposed': 600,
                                      'source_ref': selected[0]})
    cd3 = [{'dataset': 'RE2-TT', 'opaque_id': oid, 'arm': 'C-d3', 'host': owner, 'view': 'main',
            'timeout_s_proposed': 60, 'dependency': 'M1 main sealed first'}
           for oid, owner in owners.items() if oid in {'dev-a915aa2424','dev-bcbd4f46ae','dev-a5cabe5fa7','dev-03d4910932'}]
    counts = {host: sum(j['host'] == host for j in specs+baseline_refs+cd3) for host in ('local','ec2_1','ec2_2')}
    return {'schema': 'T054-PILOT-PROPOSAL-2', 'status': 'PROPOSED_NOT_GRANTED',
            'method_jobs': specs, 'baseline_jobs': baseline_refs, 'cd3_jobs': cd3,
            'counts': {'M1_family': len(specs), 'baseline_slots': len(baseline_refs),
                       'cd3_workers': len(cd3), 'by_host': counts},
            'budget_proposed': {'whole_pilot_wall_s': 10800, 'machine_seconds_max': 32400,
                                'per_host_wall_s': 10800, 'method_dataset_s': 10800,
                                'initial_workers_per_host': 1, 'method_timeout_s': 600, 'cd3_timeout_s': 60},
            'estimate_status': 'CHUA_KIEM: administrative caps, not ETA or proof of machine equivalence',
            'why_time_increase': 'Cover full driver, references, three seeds and source/receive/verify in finite time; keep scope rather than reduce cases.',
            'torai_A': {'scope': 'side table outside A4, confirmed by Minh', 'state': 'WAIT_SOURCE_GRANT',
                        'later_pilot_opaque_id': 'dev-a5cabe5fa7', 'seeds': [0,1,2],
                        'source_not_opened': True, 'not_in_approved_main_pilot': True},
            'ec2_conditions': ['SSH identity/env inventory and exact TT dev sync must be granted',
                'EC2 2 only if setup/sync/parity is cheaper than local branch it frees; otherwise retain branch locally with recorded plan before run',
                'OB remains local; no test or test-derived data on cloud'],
            'local_concurrency': 'Stage 1 is one worker. 2/3 need resource/throughput measurement and scheduler support before use.',
            'remaining_before_dispatch': ['pilot/source-map/label grant for exact selected DEV set',
                'resolve runtime/source/env references from approved originals; do not synthesize source authority',
                'pin each host and final plan; time caps above are proposals only'],
            'test_grant': False, 'G3': False, 'commit_push': False}
