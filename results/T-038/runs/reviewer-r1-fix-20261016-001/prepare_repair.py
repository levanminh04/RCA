"""Materialize a reviewer-scoped repair proposal; never publish producer outputs."""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import ctypes
import difflib
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = ROOT / 'results/T-038'
PRIOR = BASE / 'runs/doi-chieu-smtp-001'
SOURCE = BASE / 'sources/train-ticket-v1.0.0'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_bytes(relative, data):
    path = HERE / relative
    assert path.resolve().is_relative_to(HERE.resolve())
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == data, 'Retained unequal artifact: ' + relative
        return
    with path.open('xb') as stream:
        stream.write(data)


def save(relative, value):
    write_bytes(relative, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))


def text(relative, value):
    write_bytes(relative, value.encode('utf-8'))


def read_compressed(path):
    return json.loads(gzip.decompress(Path(path).read_bytes()))


def api():
    pin = load(PRIOR / 'pin.json')
    manifest_path = ROOT / pin['manifest']
    assert sha(manifest_path) == pin['manifest_sha256']
    manifest = load(manifest_path)
    assert manifest['created_utc'] == pin['created_utc']
    for name, digest in pin['code_hashes'].items():
        assert sha(manifest_path.parent / 'code' / name) == digest
        assert sha(ROOT / 'src/do_thi_tinh' / name) == digest
    spec = importlib.util.spec_from_file_location('_t038_reviewer_r1_pin',
        manifest_path.parent / 'code/__init__.py',
        submodule_search_locations=[str(manifest_path.parent / 'code')])
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def protected_paths():
    manifest = load(BASE / 'manifest.json')
    paths = {row['path']: row['sha256'] for row in manifest['files']}
    for p in ['results/T-038/manifest.json', 'docs/STATE.md', 'docs/WHY.md',
              'docs/DECISIONS.md', 'tasks/T-038-p5b-trainticket/LOG.md',
              'tasks/T-038-p5b-trainticket/SPEC.md',
              'src/do_thi_tinh/build.py', 'src/do_thi_tinh/compare.py',
              'src/do_thi_tinh/__init__.py', 'src/do_thi_tinh/README.md']:
        paths[p] = sha(ROOT / p)
    return paths


def verify_protected(paths):
    for i, (name, digest) in enumerate(paths.items(), 1):
        assert sha(ROOT / name) == digest, 'Protected input changed: ' + name
        if i % 1500 == 0:
            print(canonical({'protected_hashes_verified': i, 'total': len(paths)}), flush=True)


def source_checks():
    acquisition = load(BASE / 'runs/tai-nguon-001/manifest.json')
    acquired = {row['source_path']: row for row in acquisition['files']}
    oracle = load(HERE / 'oracle.json')
    files = sorted({entry[0] for row in oracle['relations'] for entry in row['evidence']})
    strings, verified = {}, []
    for name in files:
        entry = acquired[name]
        data = (ROOT / entry['path']).read_bytes()
        assert len(data) == entry['bytes']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['git_blob']
        strings[name] = data.decode('utf-8-sig').replace('\r\n', '\n')
        verified.append({k: entry[k] for k in ['source_path', 'path', 'bytes', 'sha256', 'git_blob']})
    sw = strings['deployment/kubernetes-manifests/skywalking/skywalking.yml']
    am = strings['deployment/kubernetes-manifests/prometheus/alertsnitch.yml']
    prefix = 'deployment/kubernetes-manifests/quickstart-k8s/charts/nacos/'
    values, secret, state = [strings[prefix + x] for x in ['values.yaml', 'templates/secrets.yaml', 'templates/statefulset.yaml']]
    hook = strings['deployment/kubernetes-manifests/prometheus/alert-manager-configmap.yml']
    loader = strings['deployment/kubernetes-manifests/prometheus/alert-manager.yml']
    checks = {
        'skywalking_storage_and_address': "STORAGE: 'elasticsearch7'" in sw and "STORAGE_ES_CLUSTER_NODES: 'elasticsearch:9200'" in sw,
        'skywalking_configmap_loader': bool(re.search(r'envFrom:\s*- prefix: SW_\s*configMapRef:\s*name: skywalking-cm', sw)),
        'alertsnitch_backend_and_logical_database': bool(re.search(r'name: ALERTSNITCH_BACKEND\s*value: mysql', am)) and bool(re.search(r'tcp\(alertsnitch-mysql:3306\)/alertsnitch', am)),
        'nacos_values': 'secretName: nacos-mysql' in values and 'name: "nacos"' in values and 'host: "nacos-mysql-leader"' in values,
        'nacos_secret_database_keys': all(x in secret for x in ['with .Values.nacos.db', 'MYSQL_SERVICE_HOST: {{.host}}', 'MYSQL_SERVICE_DB_NAME: {{ .name }}']),
        'nacos_main_container_receives_secret': 'envFrom:' in state.split('      containers:', 1)[1] and 'name: {{ .Values.nacos.secretName }}' in state.split('      containers:', 1)[1],
        'webhook_literal_and_route': 'url: http://alertsnitch:9567/webhook' in hook and '- receiver: alertsnitch' in hook,
        'webhook_configmap_loader': all(x in loader for x in ['--config.file=/etc/config/alertmanager.yml', 'mountPath: /etc/config', 'name: alertmanager-config']),
    }
    assert all(checks.values()), checks
    save('checks/source-verification.json', {'checks': checks, 'all_pass': True,
        'files': verified, 'revision': acquisition['commit'], 'credentials_copied': False,
        'source_execution_or_rendering': False})
    return acquired, acquisition['commit']


def signature(edge):
    return canonical([edge['source'], edge['target'], edge['type'], edge['channel'], edge.get('messaging')])


def prepare():
    paths = protected_paths()
    verify_protected(paths)
    save('protected-before.json', paths)
    names = ['manifest.json', 'ban-ghi.json', 'nguon.json', 'mapping.json',
             'do-thi/thuc-the.json', 'do-thi/thao-tac.json', 'do-thi/chieu-thao-tac.json',
             'do-thi/chi-thuc-the.json', 'phan-tich-chenh-lech.json',
             'phan-tich-chenh-lech.md', 'ban-giao.md', 'kiem-dung-dan.md', 'doi-chieu/index.json']
    for name in names:
        write_bytes('before/' + name, (BASE / name).read_bytes())
    write_bytes('before/comparison-summary.json', (PRIOR / 'summary.json').read_bytes())
    write_bytes('before/registry-compare.json', (PRIOR / 'registry-compare.json').read_bytes())
    write_bytes('pin.json', (PRIOR / 'pin.json').read_bytes())
    acquired, revision = source_checks()
    oracle = load(HERE / 'oracle.json')
    document = load(BASE / 'ban-ghi.json')
    registry = load(BASE / 'nguon.json')
    compare_registry = load(PRIOR / 'registry-compare.json')
    source_index = {row['id']: row for row in registry['sources']}
    compare_index = {row['id']: row for row in compare_registry['sources']}
    entities = {row['id'] for row in document['entities']}
    new_records = []
    for item in oracle['relations']:
        assert item['source'] in entities and item['target'] in entities
        assert not any(r['source']['entity'] == item['source'] and r['target']['entity'] == item['target'] for r in document['relations'])
        provenance = []
        for name, first, last in item['evidence']:
            acquired_row = acquired[name]
            source_id = 'TT:' + name
            entry = dict(id=source_id, kind='source-code/configuration', revision=revision,
                sha256=acquired_row['sha256'], path=acquired_row['path'],
                condition='Conditional source profile; application/instrumentation/deployment linkage to RE2-TT unverified.')
            for index in [source_index, compare_index]:
                if source_id in index:
                    assert (index[source_id]['path'], index[source_id]['sha256'], index[source_id]['revision']) == (entry['path'], entry['sha256'], entry['revision'])
                else:
                    index[source_id] = entry
            provenance.append(dict(source_id=source_id, locator=f'L{first}-L{last}', condition=item['condition']))
        record = dict(id=item['id'], source=dict(entity=item['source'], operation=None),
            target=dict(entity=item['target'], operation=None), type=item['type'], channel=item['channel'],
            messaging=None, context=item['condition'], provenance=provenance)
        new_records.append(record)
    document['relations'] += new_records
    registry['sources'] = sorted(source_index.values(), key=lambda x: x['id'])
    compare_registry['sources'] = sorted(compare_index.values(), key=lambda x: x['id'])
    shared = api()
    before_document = load(BASE / 'ban-ghi.json')
    before_registry = load(BASE / 'nguon.json')
    prior_entity, prior_operation = shared.build(before_document, before_registry)
    assert prior_entity == load(BASE / 'do-thi/thuc-the.json')
    assert prior_operation == load(BASE / 'do-thi/thao-tac.json')
    entity, operation = shared.build(document, registry)
    entity_diff = {signature(e) for e in entity['edges']} - {signature(e) for e in prior_entity['edges']}
    expected_diff = {canonical([r['source'], r['target'], r['type'], r['channel'], None]) for r in oracle['relations']}
    assert entity_diff == expected_diff
    assert len(entity['edges']) == len(prior_entity['edges']) + 4
    assert operation['edges'] == prior_operation['edges']
    assert entity['inventory'] == prior_entity['inventory']
    assert operation['nodes'] == prior_operation['nodes']
    assert entity['signals'] == prior_entity['signals']
    assert entity['resource_bindings'] == prior_entity['resource_bindings']
    projected = shared.project(operation)
    assert projected == shared.project(prior_operation)
    projected_keys = {signature(e) for e in projected['edges']}
    entity_only = [e for e in entity['edges'] if signature(e) not in projected_keys]
    assert len(entity_only) == 48
    assert len(projected['edges']) == 122
    reordered = deepcopy(document)
    for field in ['entities', 'operations', 'relations', 'resource_bindings', 'signals']:
        reordered[field].reverse()
    assert shared.build(reordered, registry) == (entity, operation)
    # Every pre-existing record and its original order is preserved as an exact prefix.
    assert document['relations'][:-4] == before_document['relations']
    for field in ['entities', 'operations', 'signals', 'resource_bindings']:
        assert document[field] == before_document[field]
    save('candidate/ban-ghi.json', document)
    save('candidate/nguon.json', registry)
    save('candidate/registry-compare.json', compare_registry)
    save('candidate/do-thi/thuc-the.json', entity)
    save('candidate/do-thi/thao-tac.json', operation)
    save('candidate/do-thi/chieu-thao-tac.json', projected)
    save('candidate/do-thi/chi-thuc-the.json', {'scope': entity['scope'], 'edges': entity_only,
        'note': 'Entity-only static dependencies, including source-config infrastructure; no fake operations.'})
    save('delta.json', new_records)
    save('checks/model.json', {'all_pass': True, 'old': {'relations': len(before_document['relations']),
        'entity_edges': len(prior_entity['edges']), 'operation_edges': len(prior_operation['edges'])},
        'candidate': {'relations': len(document['relations']), 'entity_edges': len(entity['edges']),
        'operation_edges': len(operation['edges']), 'projection_edges': len(projected['edges']), 'entity_only_edges': len(entity_only)},
        'literal_expected_entity_delta': [json.loads(x) for x in sorted(expected_diff)],
        'unchanged': ['entities', 'operations', 'signals', 'resource_bindings', 'old_relations',
                      'operation_edges', 'projection', 'mapping', 'shared_code', 'trace_graphs'],
        'reordered_build_equal': True, 'runtime_or_semantic_completeness_claimed': False})
    for name in ['ban-ghi.json', 'nguon.json']:
        old = (HERE / 'before' / name).read_text(encoding='utf-8-sig').splitlines(keepends=True)
        new = (HERE / 'candidate' / name).read_text(encoding='utf-8').splitlines(keepends=True)
        text('patches/' + name + '.diff', ''.join(difflib.unified_diff(old, new,
            fromfile='results/T-038/' + name, tofile='candidate/' + name)))
    print(canonical(load(HERE / 'checks/model.json')), flush=True)


def expected_members(graph, side, level, name, mapping, trace_owners, static_owners):
    def resolve(ident):
        lev = 'operation' if ident in trace_owners else 'entity'
        row = mapping.get((lev, ident))
        if not row or not row['verified'] or len(set(row['candidates'])) != 1:
            return None
        target = row['candidates'][0]
        if lev == 'operation' and static_owners[target] != resolve(trace_owners[ident]):
            return None
        return target
    result = defaultdict(list)
    for i, edge in enumerate(graph['edges']):
        if level == 'entity' and (edge['source'] == edge['target'] or edge['type'] == 'span-parent'):
            continue
        if edge['type'] == 'thông-điệp':
            assert side == 'static' and edge['messaging']['broker_scope'] is None
            continue
        first, last = edge['source'], edge['target']
        if side == 'trace':
            first, last = resolve(first), resolve(last)
        if first is None or last is None or (level == 'entity' and first == last):
            continue
        if name == 'typed' and edge['type'] == 'gọi-chưa-phân-kiểu':
            continue
        key = canonical([first, last, edge['type'] if name == 'typed' else None,
            ['smtp', None] if edge.get('channel') == 'smtp' else None])
        result[key].append(i)
    return dict(result)


def check_result(result, static, trace, mappings):
    mapping = {(r['level'], r['original']): r for r in mappings}
    owners = dict(trace.get('belongs_to', []))
    static_owners = dict(static.get('belongs_to', []))
    for name, view in result['views'].items():
        sets = {}
        for side, graph in [('static', static), ('trace', trace)]:
            expected = expected_members(graph, side, trace['level'], name, mapping, owners, static_owners)
            reported = {canonical(group['key']): [m['index'] for m in group['members']] for group in view['members'][side]}
            assert expected == reported
            members = [m for group in view['members'][side] for m in group['members']]
            excluded = view['exclusions'][side]
            assert sorted(m['index'] for m in members + excluded) == list(range(len(graph['edges'])))
            assert all(m['original'] == graph['edges'][m['index']] for m in members + excluded)
            sets[side] = set(expected)
        s, t = sets['static'], sets['trace']
        for key, values in [('S', s), ('T', t), ('intersection', s & t), ('static_only', s - t), ('trace_only', t - s)]:
            assert {canonical(x) for x in view[key]} == values
        assert [view[k] for k in ['numerator', 'static_denominator', 'trace_denominator']] == [len(s & t), len(s), len(t)]
        assert view['static_fraction'] == (len(s & t) / len(s) if s else None)
        assert view['trace_fraction'] == (len(s & t) / len(t) if t else None)
    assert result['interval_ns'] == trace['interval_ns']
    assert result['conditional_reference'] is True


def semantic(result):
    result = deepcopy(result)
    for view in result['views'].values():
        for groups in view['members'].values():
            for group in groups:
                for member in group['members']:
                    member.pop('index')
                group['members'].sort(key=canonical)
            groups.sort(key=canonical)
        for rows in view['exclusions'].values():
            for row in rows:
                row.pop('index')
            rows.sort(key=canonical)
    return canonical(result)


def peak_memory():
    class PMC(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [(name, ctypes.c_size_t) for name in [
            'PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage',
            'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage']]
    value = PMC()
    value.cb = ctypes.sizeof(value)
    ctypes.windll.kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    ctypes.windll.psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
    assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(value), value.cb)
    return value.PeakWorkingSetSize


def compare_all():
    started = time.perf_counter()
    shared = api()
    previous = load(PRIOR / 'summary.json')
    graphs = {level: load(HERE / 'candidate/do-thi' / name) for level, name in [('entity', 'thuc-the.json'), ('operation', 'thao-tac.json')]}
    registry = load(HERE / 'candidate/registry-compare.json')
    mappings = load(BASE / 'mapping.json')
    before_manifest = load(HERE / 'before/manifest.json')
    assert sha(ROOT / 'results/T-035/manifest.json') == before_manifest['input_manifests']['results/T-035/manifest.json']['sha256']
    rows = []
    families = Counter()
    for i, prior_row in enumerate(previous['rows'], 1):
        ip = ROOT / prior_row['input']
        assert sha(ip) == prior_row['input_sha256']
        trace = load(ip)
        old_path = ROOT / prior_row['output']
        assert sha(old_path) == prior_row['output_sha256']
        old = read_compressed(old_path)
        level = prior_row['level']
        allowed_mappings = [m for m in mappings if m['level'] == 'entity' or level == 'operation']
        context = old['context']
        before = canonical([graphs[level], trace, allowed_mappings, context, registry])
        result = shared.compare(graphs[level], trace, allowed_mappings, context, registry)
        check_result(result, graphs[level], trace, allowed_mappings)
        assert result == shared.compare(graphs[level], trace, allowed_mappings, context, registry)
        reversed_trace = deepcopy(trace)
        for field in ['nodes', 'edges', 'belongs_to', 'component_context']:
            if field in reversed_trace:
                reversed_trace[field].reverse()
        reordered = shared.compare(graphs[level], reversed_trace, list(reversed(allowed_mappings)), context, registry)
        assert semantic(result) == semantic(reordered)
        assert before == canonical([graphs[level], trace, allowed_mappings, context, registry])
        if level == 'operation':
            assert result == old
        for name, view in result['views'].items():
            prior_view = old['views'][name]
            for key in ['T', 'intersection', 'trace_only']:
                assert view[key] == prior_view[key]
            for key in ['members', 'exclusions']:
                assert view[key]['trace'] == prior_view[key]['trace']
            s0, s1 = {canonical(k) for k in prior_view['S']}, {canonical(k) for k in view['S']}
            expected_delta = (4 if name == 'endpoints' else 3) if level == 'entity' else 0
            assert s0 <= s1 and len(s1 - s0) == expected_delta
            old_excluded = {canonical({k: v for k, v in x.items() if k != 'index'}) for x in prior_view['exclusions']['static']}
            new_excluded = {canonical({k: v for k, v in x.items() if k != 'index'}) for x in view['exclusions']['static']}
            assert old_excluded <= new_excluded
            assert len(new_excluded - old_excluded) == (1 if level == 'entity' and name == 'typed' else 0)
            for x in new_excluded - old_excluded:
                assert json.loads(x)['reason'] == 'unknown_type'
        tail = prior_row['input'].split('results/T-035/do-thi/RE2-TT/', 1)[1] + '.gz'
        output = 'candidate/doi-chieu/' + tail
        write_bytes(output, gzip.compress(canonical(result).encode('utf-8'), compresslevel=6, mtime=0))
        family = Path(prior_row['input']).stem.split('-')[0]
        families[(level, family)] += 1
        rows.append(dict(input=prior_row['input'], input_sha256=prior_row['input_sha256'], level=level,
            interval_ns=trace['interval_ns'], output=(HERE / output).relative_to(ROOT).as_posix(),
            output_sha256=sha(HERE / output), baseline_output=prior_row['output'],
            baseline_output_sha256=prior_row['output_sha256'], repeat_exact=True,
            reorder_semantic_equal=True, independent_sets_members_denominators=True, input_unchanged=True,
            views={name: {key: (len(view[key]) if isinstance(view[key], list) else view[key]) for key in [
                'S', 'T', 'intersection', 'static_only', 'trace_only', 'static_fraction', 'trace_fraction']} for name, view in result['views'].items()}))
        if i % 25 == 0 or i == len(previous['rows']):
            status = {'done': i, 'total': len(previous['rows']), 'elapsed_seconds': time.perf_counter() - started}
            print(canonical(status), flush=True)
            write_bytes(f'checks/progress/{i:04d}.json', (canonical(status) + '\n').encode())
    assert len(rows) == 1069
    save('candidate/summary.json', dict(task='T-038', status='REVIEWER_PROPOSAL_NOT_ADOPTED',
        all_pass=True, graph_count=len(rows), rows=rows, errors=[], pin=load(HERE / 'pin.json'),
        family_counts=[dict(level=k[0], family=k[1], count=v) for k, v in sorted(families.items())]))
    save('checks/comparison.json', {'all_pass': True, 'graphs': len(rows), 'entity_graphs': 979,
        'operation_exact_equal_to_before': 90, 'entity_endpoints_static_delta_each': 4,
        'entity_typed_static_delta_each': 3, 'entity_typed_unknown_static_exclusion_delta_each': 1,
        'trace_sets_members_exclusions_and_intersections_unchanged': True,
        'source_or_runtime_completeness_confirmed': False})
    save('checks/cost.json', {'elapsed_seconds': time.perf_counter() - started,
        'peak_process_rss_bytes': peak_memory(), 'network_bytes': 0,
        'output_bytes_so_far': sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file()),
        'isolated_benchmark': False, 'interpretation': 'Candidate rebuild/comparison/check accounting, not human labor or RCA experiment.'})


if __name__ == '__main__':
    phase = sys.argv[1]
    try:
        {'prepare': prepare, 'compare': compare_all}[phase]()
    except BaseException:
        i = 1
        while (HERE / f'failure-{phase}-{i:03d}.json').exists():
            i += 1
        save(f'failure-{phase}-{i:03d}.json', {'phase': phase, 'traceback': traceback.format_exc(),
            'created_utc': datetime.now(timezone.utc).isoformat()})
        raise
