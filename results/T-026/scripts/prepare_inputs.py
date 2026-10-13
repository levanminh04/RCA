"""Tạo manifest T-026 từ audit hợp lệ; không đọc CSV dữ liệu hoặc gọi phương pháp."""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path


def strict_json(text):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(text, object_pairs_hook=unique)


def build_documents(repo_root):
    """Trả các document manifest; mọi nhãn chỉ nằm trong nhan-dev riêng."""
    root = Path(repo_root).resolve()
    sys.path.insert(0, str(root / 'src'))
    from p3.nezha import (FRONT_CHANNELS, POD_ALIASES, RESOURCE_CHANNELS,
                          SERVICE_ALIASES, UNIVERSE, _validate_case)
    report = root / 'results/T-026/kiem-dau-vao.md'
    text = report.read_text(encoding='utf-8')
    match = re.search(r'<!-- T026_AUDIT_JSON_START -->\s*(.*?)\s*<!-- T026_AUDIT_JSON_END -->', text, re.S)
    if not match:
        raise ValueError('missing T026 audit 001')
    audit = strict_json(match.group(1))
    if audit.get('run') != 'kiem-na-001' or audit.get('derived_payload_files') != []:
        raise ValueError('audit 001 contract changed')
    with (root / 'results/T-021/chia-theo-o/A-phan-tang.csv').open(encoding='utf-8-sig', newline='') as f:
        split = [r for r in csv.DictReader(f) if r['dataset'] == 'Nezha-OB']
    dev = {r['case']: r for r in split if r['vai_tro'] == 'dev'}
    tests = {r['case'] for r in split if r['vai_tro'] == 'test'}
    if len(dev) != 22 or len(tests) != 34 or set(dev) & tests:
        raise ValueError('dev/test split differs from approved cohort')
    mains = {r['case']: r for r in audit['cases'] if r['view'] == 'main'}
    alternate = {r['case']: r for r in audit['cases'] if r['view'] == 'sensitivity_A'}
    if len(audit['cases']) != 23 or set(mains) != set(dev) or len(alternate) != 1:
        raise ValueError('Q-84 audit views differ from approved cohort')
    disputed = 'OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43'
    if set(alternate) != {disputed}:
        raise ValueError('unexpected sensitivity A case')
    manifest = {m['path']: m for m in audit['manifest']}
    if len(manifest) != 154 or len(manifest) != len(audit['manifest']):
        raise ValueError('source manifest count/uniqueness differs from audit 001')

    def paths(view):
        return {x['path'] for x in view['metric']} | {
            x['path'] for kind in ('trace', 'log') for x in view[kind]['sources']}

    cases, labels, opaque_ids = [], [], set()
    for case_name in sorted(dev):
        row, observed = dev[case_name], mains[case_name]
        oid = 'dev-' + hashlib.sha256(case_name.encode('utf-8')).hexdigest()[:10]
        if oid in opaque_ids:
            raise ValueError('opaque ID collision')
        opaque_ids.add(oid)
        source_paths = paths(observed)
        if case_name in alternate and paths(alternate[case_name]) != source_paths:
            raise ValueError('sensitivity A changed selected source files')
        if not source_paths <= set(manifest):
            raise ValueError('case references unverified source')
        dates = {Path(p).parts[-3] for p in source_paths}
        if len(dates) != 1:
            raise ValueError('one case spans unexpected source days')
        day = next(iter(dates))
        files = {}
        for rel in sorted(source_paths):
            original = manifest[rel]
            repo_path = 'data/ngoai-rcaeval/nezha/' + rel
            files[repo_path] = {'path': repo_path, 'sha256': original['sha256'], 'bytes': original['bytes']}
        item = {'opaque_id': oid, 't_ns': observed['t_ns'],
                't_ns_sensitivity_A': alternate[case_name]['t_ns'] if case_name in alternate else None,
                'trace_guard_s': {'2022-08-22': 41, '2022-08-23': 32}[day], 'files': files}
        _validate_case(item)
        cases.append(item)
        labels.append({'opaque_id': oid, 'case': case_name, 'root': row['root'], 'fault': row['fault'],
                       'cell': row['root'] + '|' + row['fault'], 'nhom_loi': row['nhom_loi'],
                       'nhom_vi_tri_p75': row['nhom_vi_tri_p75'], 'rep': row['rep'],
                       't_ns': observed['t_ns'], 't_ns_sensitivity_A': item['t_ns_sensitivity_A'],
                       'time_source': 'inject_time', 'sensitivity_A_time_source': 'inject_timestamp'
                       if case_name in alternate else 'inject_time'})
    report_hash = hashlib.sha256(report.read_bytes()).hexdigest()
    allowlist = {'dataset': 'Nezha-OB', 'schema_version': 1, 'so_ca': len(cases),
                 'source_audit': {'path': 'results/T-026/kiem-dau-vao.md', 'sha256': report_hash,
                                  'block': 'T026_AUDIT_JSON_START', 'run': audit['run']},
                 'cases': cases}
    nhan = {'dataset': 'Nezha-OB', 'so_ca': len(labels), 'cases': labels,
            'views': {'main': '22 cases, inject_time',
                      'sensitivity_A': '22 cases, only disputed case changes time',
                      'sensitivity_B': '21 cases with agreeing time fields'},
            'sensitivity_A_opaque_id': next(x['opaque_id'] for x in labels if x['case'] == disputed),
            'sensitivity_B_opaque_ids': [x['opaque_id'] for x in labels if x['case'] != disputed]}
    mappings = {'dataset': 'Nezha-OB', 'universe': UNIVERSE, 'pod_aliases': POD_ALIASES,
                'service_aliases': SERVICE_ALIASES, 'resource_channels': RESOURCE_CHANNELS,
                'front_channels': FRONT_CHANNELS, 'metric_columns_before_preprocess': 165,
                'excluded': ['NodeCpuUsageRate(%)', 'NodeMemoryUsageRate(%)', 'NodeNetworkReceiveBytes',
                             'source_50.csv', 'destination_50.csv', 'dependency.csv'],
                'trace': {'serviceName': 'explicit PodName alias', 'methodName': 'OperationName unchanged',
                          'operationName': 'OperationName unchanged', 'startTime': 'StartTimeUnixNano // 1000',
                          'duration': 'native Duration in integer us'},
                'duplicates': 'identical source rows retained; conflicting span identity is runner error'}
    config = {'config_id': 't026-ob-q85-native-v1', 'mode': 'a', 'window_s': 300,
              'methods': ['baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai'],
              'unsupported': {'circa': 'Only 1-2 real train measurements per source; loader interpolates before train split and 19/22 main cases can use A anchors in the train tail; Q-85',
                              'torai': 'B requires missing statusCode; native metric cadence incompatible with row stride 15'},
              'metric': {'baro': 'ordinal native values, front Time_ns marker, P3 preprocess after cut',
                         'simplerca': 'native per-channel N/A arrays, no filling'},
              'trace_sensitivity': {'2022-08-22': 41, '2022-08-23': 32,
                                   'normal': 'end_ns < t_ns - guard_s*1e9',
                                   'anomalous': 'unchanged method split', 'clock_shift_ns': 0},
              'hashseed': 0, 'microrank_pilot_hashseeds': [0, 1], 'timeout_s': 3600,
              'labels_visible_to_methods': False, 'payload_storage': 'RAM only',
              'why_ids': ['WHY-22', 'WHY-26', 'WHY-27', 'WHY-31', 'WHY-32', 'WHY-33', 'WHY-37']}
    return {'allowlist-dev.json': allowlist, 'nhan-dev.json': nhan,
            'mappings/ob.json': mappings, 'config/adapter-config.json': config}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', default=str(Path(__file__).resolve().parents[3]))
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    docs = build_documents(root)
    out_root = root / 'results/T-026'
    # Không ghi đè đầu ra: lượt chuẩn bị hỏng/đã tồn tại phải được giữ và báo.
    destinations = {name: out_root / name for name in docs}
    if any(path.exists() for path in destinations.values()):
        raise FileExistsError('T-026 prepared output already exists; preserve the previous run')
    for name, doc in docs.items():
        path = destinations[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x', encoding='utf-8', newline='\n') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write('\n')
        print(json.dumps({'output': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()},
                         ensure_ascii=True), flush=True)


if __name__ == '__main__':
    main()
