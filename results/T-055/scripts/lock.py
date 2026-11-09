"""T-055: dựng gói khóa RE3-OB bản cuối (chỉ metadata, không đọc telemetry).

Đầu vào: preregistration, nguồn độc lập, biên nhận tải EC2, quyết định preflight (đã điều chỉnh R7 theo D-55-8),
plan main013-v2 của EC2 làm mẫu trường vận hành. Đầu ra (tương đối từ gốc repo, giống nhau trên EC2):
results/T-054/runs/re3-ban-cuoi-001/meta/{profile,runtime,binding,failure-policy,protocol,grant,ec2_1-plan,ec2_2-plan}.json
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'results/T-054/scripts'), str(ROOT / 'src')]
from bien_nhan import fingerprint  # noqa: E402

META = 'results/T-054/runs/re3-ban-cuoi-001/meta'
REMOTE = '/home/ubuntu/rca-p7/T-054/checkpoint013/work-re3'
DATA_ROOT = '/home/ubuntu/rca-p7/T-055/data-root'
MAIN = 'results/T-054/runs/chuan-bi-main-013-v2'


def L(p):
    return json.loads((ROOT / p).read_bytes())


def write(rel, value):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, ensure_ascii=False, indent=1, sort_keys=True).encode()
    with open(p, 'xb') as f:
        f.write(raw)
    return {'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def ref(rel):
    raw = (ROOT / rel).read_bytes()
    return {'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def main():
    pre = L('results/T-055/runs/khoa-truoc-001/preregistration.json')
    dec = L('results/T-055/runs/preflight-001/decision-002.json')
    assert dec['decision']['PASS'] is True, 'preflight chưa PASS'
    ind_ref = ref('results/T-055/runs/nguon-001/independent-source.json')
    ind = L(ind_ref['path'])
    part = L('results/T-055/runs/nguon-001/partition.json')['hosts']
    stage = {h: L(f'results/T-055/runs/tai-001/{h}-stage.json') for h in ('ec2_1', 'ec2_2')}
    h1 = pre['h1_assumptions_unverified']
    inv = h1['inventory']['value']
    d = dec['decision']
    status_values = dec['declared_status_values']
    profile = {
        'schema': 'RE3-OB-PROFILE-1', 'dataset': 'RE3-OB', 'status': 'DECLARED',
        'time_units': {'metric': 's', 'log': d['log'][0], 'span_start': d['span_start'][0],
                       'span_duration': d['span_start'][0]},
        'observation_r_ns': {'trace': 1000, 'log': 10**9, 'metric': int(d['metric_step_s'][0] * 10**9)},
        'inventory': inv, 'aliases': h1['aliases']['value'], 'metric_channels': h1['metric_channels'],
        'log_rule': {'kieu': 'tu_khoa', 'tu_khoa': h1['log_rule']['tu_khoa']},
        'trace_status_kind': 'grpc_status_code', 'trace_status_values': status_values,
        'evidence': {
            'time_units': 'metric s: dataset card; span/log: preflight R3–R5 khóa trước (results/T-055/runs/preflight-001/decision-002.json). CHƯA KIỂM bằng nguồn tác giả.',
            'observation_r_ns': 'R8: metric bước trung vị chung 1 s; trace 1 µs; log 1 s như TT/Nezha. CHƯA KIỂM.',
            'inventory': h1['inventory']['why'] + ' CHƯA KIỂM.',
            'aliases': h1['aliases']['why'],
            'metric_channels': 'Ánh xạ 8 hậu tố như H2 (src/p3/re3.py CHANNELS/KINDS).',
            'log_rule': h1['log_rule']['source'],
            'trace_status_kind': 'Tác giả: gRPC, 0 OK (issue #64). D-55-8: thêm 400 quan sát gộp sau preflight R7, không nhãn; TORAI cộng mã native.'}}
    profile_ref = write(META + '/profile.json', profile)
    g1 = ind['g1_revision']
    cases = {}
    for m, row in ind['cases_by_member'].items():
        oid = 'test-' + m[:10]
        rec = stage[part[oid]]['cases'][oid]
        files = {n: {'path': row['files'][n]['path'], 'bytes': rec[n]['bytes'], 'sha256': rec[n]['sha256']}
                 for n in row['files']}
        cases[oid] = {'files': files, 'member_sha256': m, 't': row['t']}
    runtime_ref = write(META + '/runtime.json', {'dataset': 'RE3-OB', 'g1_revision': g1, 'inventory': inv,
                                                 'aliases': profile['aliases'], 'profile_sha256': profile_ref['sha256'],
                                                 'cases': cases,
                                                 'note': 'bytes/sha256 từ biên nhận tải EC2; t từ inject_time.txt HF (cùng nguồn độc lập)'})
    fp = write(META + '/failure-policy.json', {
        'schema': 'T054-FAILURE-POLICY-1', 'scope': 'LOCKED_RE3', 'dataset': 'RE3-OB',
        'error_rules': ['RE3_METHOD_ERROR_IS_MISS'], 'code_evidence': [],
        'monitor': pre['failure']['monitor'], 'timeout_s': {'main_slot': 600},
        'unknown_errors': 'ERROR phương pháp ở pha method trên output đã đóng: trượt (D-55-5). Lỗi nguồn/adapter/hạ tầng: BLOCKED, dừng phát.',
        'preregistration': ref('results/T-055/runs/khoa-truoc-001/preregistration.json')})
    # Mẫu trường vận hành từ plan main EC2 đã chạy.
    tmpl_plan = L(MAIN + '/activated-001/ec2_1-plan.json')
    tmpl = {}
    for j in tmpl_plan['jobs']:
        a = j['slot']['arm']
        if j['slot']['dataset'] == 'RE2-TT' and a not in tmpl:
            tmpl[a] = j
    contract = L(MAIN + '/dispatch-contract.json')
    m1_conf = L(MAIN + '/activated-001/protocol.json')['configurations']
    arms = pre['matrix']['arms']
    configs = {}
    for a in arms:
        configs[a] = (m1_conf[a]['config'] if a in m1_conf else
                      {'half_width_s': 300, 'method': a, 'mode': 'a', 'source': 'P3-v2/Q85'})
        if a in m1_conf:
            assert fingerprint(configs[a]) == m1_conf[a]['sha256']
    code_pins = dict(L(MAIN + '/code-pins.json')['code_pins'])
    overlay = ref('results/T-055/overlay/results/T-054/scripts/bien_nhan.py')
    code_pins['results/T-054/scripts/bien_nhan.py'] = overlay['sha256']
    m1_contract = tmpl['M1']['m1_contract']
    hosts, partitions, slots = {}, {'ec2_1': [], 'ec2_2': []}, []
    for h in ('ec2_1', 'ec2_2'):
        c = contract['hosts'][h]
        hosts[h] = {'code_pins': code_pins, 'configurations': configs,
                    'environments': c['environment_sha256'], 'm1_contract_ref': m1_contract,
                    'failure_policy_ref': fp, 'data_root': DATA_ROOT,
                    'pythonpath': [REMOTE + '/upstream/rcaeval'],
                    'executable': c['executable'], 'prep_executable': c['prep_executable'],
                    'method_executable': c['method_executable']}
    members = sorted(ind['cases_by_member'])
    for m in members:
        oid = 'test-' + m[:10]
        row = cases[oid]
        for a, seeds in arms.items():
            for s in seeds:
                env = hosts[part[oid]]['environments']['py38' if a == 'torai_B' else 'main']
                slot = {'dataset': 'RE3-OB', 'opaque_id': oid, 'member_sha256': m, 'arm': a, 'view': 'main',
                        'seed': s, 'window': {'t': row['t'], 'half_width_s': 300},
                        'source_sha256': fingerprint(row), 'config_sha256': fingerprint(configs[a]),
                        'environment_sha256': env}
                slots.append(slot)
                partitions[part[oid]].append(fingerprint(slot))
    assert len(slots) == 420
    protocol = {
        'schema': 'T054-RE3-PROTOCOL-1', 'dataset': 'RE3-OB', 'status': 'LOCKED_FINAL_RE3', 'final_version': True,
        'case_count': 30, 'cell_count': 10, 'members': members, 'g1_revision': g1, 'arms': arms, 'slots': slots,
        'worlds': pre['matrix']['worlds'], 'metrics': pre['matrix']['metrics'],
        'seed_aggregation': pre['matrix']['seed_aggregation'], 'support_policy': pre['matrix']['support_policy'],
        'variants': pre['matrix']['variants'], 'partitions': partitions, 'dispatch': {'hosts': hosts},
        'preregistration': ref('results/T-055/runs/khoa-truoc-001/preregistration.json'),
        'preflight_decision': ref('results/T-055/runs/preflight-001/decision-002.json'),
        'derived_after_seal': pre['matrix']['derived_after_seal'], 'statistics': pre['matrix']['statistics'],
        'm1_version_note': 'M1 đúng bản khóa P7(a) main013-v2 (configurations cùng sha256); D-55-1.',
        'review_note': 'Mở trước khi Codex phản biện theo lựa chọn của Minh (D-55-6).'}
    protocol_ref = write(META + '/protocol.json', protocol)
    binding_ref = write(META + '/runtime-binding.json', {
        'protocol_sha256': protocol_ref['sha256'], 'profile_sha256': profile_ref['sha256'],
        'runtime_sha256': runtime_ref['sha256'], 'independent_source_sha256': ind_ref['sha256']})
    grant_ref = write(META + '/grant.json', {
        're3_grant': True, 'g3': True, 'source': ref('results/T-055/grants/minh-re3-source.json'),
        'protocol_sha256': protocol_ref['sha256'], 'profile_sha256': profile_ref['sha256'],
        'runtime_sha256': runtime_ref['sha256'], 'independent_source_sha256': ind_ref['sha256'],
        'runtime_binding_sha256': binding_ref['sha256'], 'commit_push_grant': False,
        'operator': 'Claude; reviewer Codex (sau)'})
    plans = {}
    for h in ('ec2_1', 'ec2_2'):
        jobs = []
        for s in slots:
            if fingerprint(s) not in set(partitions[h]):
                continue
            a = s['arm']
            base = copy.deepcopy(tmpl['torai_B'] if a == 'torai_B' else tmpl[a] if a in tmpl else tmpl['baro'])
            for k in ('main_dependency', 'main_seal', 'main_key', 'author_source_ref', 'ce_support'):
                base.pop(k, None)
            kind = 'm1' if a in m1_conf else 'torai_pipeline' if a == 'torai_B' else 'baseline'
            hd = hosts[h]
            job = dict(base, kind=kind, slot=s, config=configs[a], code_pins=code_pins, evaluation_mode='heldout',
                       source=cases[s['opaque_id']], t=s['window']['t'], g1_revision=g1, inventory=inv,
                       data_root=DATA_ROOT, pythonpath=hd['pythonpath'], executable=hd['executable'],
                       prep_executable=hd['prep_executable'], method_executable=hd['method_executable'],
                       timeout_s=600, protocol_ref=protocol_ref, runtime_ref=runtime_ref,
                       independent_source_ref=ind_ref, runtime_binding_ref=binding_ref, re3_grant_ref=grant_ref,
                       re3_profile_ref=profile_ref, failure_policy_ref=fp, re3_host=h, a4=False,
                       static_snapshot=None)
            if kind == 'm1':
                job['m1_contract'] = m1_contract
            else:
                job.pop('m1_contract', None)
            if a == 'torai_B':
                job['prep_environment_sha256'] = hd['environments']['main']
            jobs.append(job)
        # Thứ tự: baseline nhẹ trước, TORAI, rồi M1-family; xen theo ca để kết quả sớm có đủ vế.
        order = {'baro': 0, 'simplerca': 1, 'tracerca': 2, 'microrank': 3, 'circa': 4, 'torai_B': 5,
                 'M1': 6, 'C-a0': 7, 'C-a1': 8, 'bo-E1': 9, 'bo-E2': 10, 'bo-E5': 11}
        jobs.sort(key=lambda j: (j['slot']['opaque_id'], order[j['slot']['arm']], j['slot']['seed'] or 0))
        peak = {f'RE3-OB|{a}': 2147483648 for a in arms}
        plan = {'schema': 'T054-PLAN-1', 'mode': 'heldout', 'host_role': h, 'jobs': jobs,
                'directory': REMOTE + '/results/T-054/runs/re3-ban-cuoi-001/queue',
                'protocol_ref': protocol_ref, 're3_grant_ref': grant_ref, 're3_profile_ref': profile_ref,
                'budget': tmpl_plan['budget'], 'monitor': tmpl_plan['monitor'], 'open_before_run': [],
                'preparation_only': False, 'workers': 2,
                'resources': {'expected_peak_bytes': peak, 'factor': 1.25, 'reserve_bytes': 805306368,
                              'note': 'RE3 chưa đo; giữ 2 GiB/slot thận trọng; scheduler kiểm RAM trước mỗi lượt phát'},
                'inventories': {'RE3-OB': inv}}
        plans[h] = write(META + f'/{h}-plan.json', plan)
    out = {'profile': profile_ref, 'runtime': runtime_ref, 'failure_policy': fp, 'protocol': protocol_ref,
           'binding': binding_ref, 'grant': grant_ref, 'plans': plans, 'overlay': overlay}
    write(META + '/lock-receipt.json', out)
    print(json.dumps({k: (v['sha256'][:12] if 'sha256' in v else {kk: vv['sha256'][:12] for kk, vv in v.items()})
                      for k, v in out.items()}, indent=0))


if __name__ == '__main__':
    main()
