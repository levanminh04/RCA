"""Oracle literal, chẩn đoán trung gian và kiểm tương thích graph dev đã lưu."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import inspect
import json
import os
from pathlib import Path
import platform
import random
import re
import sys
import time
import traceback
import tracemalloc

ROOT = Path('D:/RCA-flashticket')
sys.path.insert(0, str(ROOT / 'src'))
from do_thi_tinh import build, compare, project
from do_thi_tinh.build import canonical


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')


def peak_working_set():
    if os.name != 'nt':
        return None
    import ctypes
    from ctypes import wintypes

    class Counters(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
            (name, ctypes.c_size_t) for name in ['PeakWorkingSetSize', 'WorkingSetSize',
              'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
              'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage']]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    get_process = ctypes.windll.kernel32.GetCurrentProcess
    get_process.restype = wintypes.HANDLE
    get_memory = ctypes.windll.psapi.GetProcessMemoryInfo
    get_memory.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
    if not get_memory(get_process(), ctypes.byref(counters), counters.cb):
        raise ctypes.WinError()
    return counters.PeakWorkingSetSize


def main():
    if len(sys.argv) != 2 or not re.fullmatch('[a-z0-9][a-z0-9-]*', sys.argv[1]):
        raise ValueError('new_run_name_required')
    out = Path('D:/RCA-flashticket/results/T-036/runs/doi-chieu-smtp-001/checks/smtp-baseline-002/t036-regression')
    out.mkdir(exist_ok=False)
    started = time.perf_counter()
    tracemalloc.start()
    checks, stages = [], []
    env = dict(command=f'{sys.executable} -X utf8 -B {Path(__file__).as_posix()} {sys.argv[1]}',
               python=sys.version, platform=platform.platform(), hashseed=os.getenv('PYTHONHASHSEED'),
               started_utc=datetime.now(timezone.utc).isoformat())
    save(out / 'environment.json', env)
    code_files = [ROOT / 'src/do_thi_tinh' / p for p in ['__init__.py', 'build.py', 'compare.py']]
    code_files.append(Path(__file__))
    (out / 'code').mkdir()
    for path in code_files:
        (out / 'code' / path.name).write_bytes(path.read_bytes())
    save(out / 'code-hashes.json', {p.relative_to(ROOT).as_posix(): sha(p) for p in code_files})

    def progress(name):
        stages.append(dict(stage=name, elapsed_seconds=time.perf_counter()-started))
        with (out / 'progress.jsonl').open('a', encoding='utf-8') as f:
            f.write(canonical(stages[-1])+'\n')

    def check(name, actual, expected=True):
        ok = actual == expected
        checks.append(dict(name=name, ok=ok, actual=actual, expected=expected))

    def reject(name, fn, expected):
        try:
            fn()
        except ValueError as error:
            check(name, str(error).split(':')[0], expected)
        else:
            check(name, 'accepted', expected)

    try:
        progress('verify-sources-and-oracle')
        registry = read(ROOT / 'results/T-036/nguon.json')
        for source in registry['sources']:
            p = Path(source['path'])
            p = p if p.is_absolute() else ROOT / p
            check('source:'+source['id'], sha(p), source['sha256'])
        receipt = read(ROOT / 'results/T-036/fixtures/oracle-before-code.json')
        check('oracle_before_implementation', receipt['implementation_exists'], False)
        for p, digest in receipt['sha256'].items():
            check('oracle_hash:'+p, sha(ROOT / 'results/T-036/fixtures' / p), digest)
        if not all(c['ok'] for c in checks):
            raise ValueError('input_verification_failed')
        doc = read(ROOT / 'results/T-036/fixtures/input.json')
        expected = read(ROOT / 'results/T-036/fixtures/expected.json')
        before = canonical(doc)
        entity, operation = build(doc, registry)
        save(out / 'entity.json', entity)
        save(out / 'operation.json', operation)
        projected = project(operation)
        save(out / 'projection.json', projected)
        progress('builder-and-projection')
        check('entity_ids_literal', sorted(n['id'] for n in entity['nodes']), expected['entity_ids'])
        signatures = [[r[k] for k in ['source', 'target', 'type', 'channel', 'messaging']] for r in entity['edges']]
        check('entity_edges_literal', sorted(signatures, key=canonical), sorted(expected['entity_edges'], key=canonical))
        check('operation_exclusions_literal', [r['record_id'] for r in operation['operation_exclusions']],
              expected['operation_exclusions'])
        check('projection_record_ids_literal', sorted({x for e in projected['edges'] for x in e['record_ids']}),
              expected['projected_entity_record_ids'])
        for ident in expected['no_incoming_operations']:
            check('root_operation:'+ident, not any(e['target'] == ident for e in operation['edges']))
        check('bindings_literal', len(entity['resource_bindings']), expected['bindings_count'])
        check('shared_instance_literal', sorted({r['resource'] for r in entity['resource_bindings']
                                               if r['entity'] in {'DB1', 'DB2'} and r['relation'] == 'hosted_on'}), ['PG'])
        check('inventory_not_observation', entity['observed_nodes'], [])
        check('no_static_event_count', all('event_count' not in e for g in [entity, operation] for e in g['edges']))
        check('document_unchanged', canonical(doc), before)
        check('retry_preserves_record_members', next(e['record_ids'] for e in entity['edges']
              if e['channel'] == 'publish'), ['publish', 'republish'])
        check('queue_addresses_literal', sorted(e['queue_metric_address'] for e in entity['edges']
              if e['channel'] == 'consume'), [['R', 'vhost-demo', 'q1'], ['R', 'vhost-demo', 'q2'], ['R', 'vhost-demo', 'q3']])
        two = deepcopy(doc)
        next(r for r in two['relations'] if r['id'] == 'http-second-source')['provenance'][0]['source_id'] = 'B14'
        et, _ = build(two, registry)
        check('same_edge_two_source_provenances', sorted(p['source_id'] for e in et['edges'] if e['channel'] == 'http'
              and e['target'] == 'B' for p in e['provenance']), ['B13', 'B14'])
        bad = {}
        bad['unknown_field'] = deepcopy(doc); bad['unknown_field']['new'] = 1
        bad['missing_provenance'] = deepcopy(doc); bad['missing_provenance']['entities'][0]['provenance'] = []
        bad['conflicting_entity'] = deepcopy(doc)
        bad['conflicting_entity']['entities'].append(dict(doc['entities'][0], type='host'))
        bad['missing_operation'] = deepcopy(doc); bad['missing_operation']['relations'][0]['source']['operation'] = 'absent'
        bad['bad_broker'] = deepcopy(doc)
        next(r for r in bad['bad_broker']['relations'] if r['id'] == 'publish')['messaging']['broker'] = 'X'
        bad['shared_operation_metric'] = deepcopy(doc)
        bad['shared_operation_metric']['signals'][0].update(entity='A', operation='send')
        bad['label'] = deepcopy(doc); bad['label']['relations'][0]['root'] = 'A'
        bad['collision'] = deepcopy(doc)
        bad['collision']['entities'].append(dict(doc['entities'][0], id='["A","send"]'))
        for name, value in bad.items():
            reject('negative_build:'+name, lambda d=value: build(d, registry), expected['negative_build'][name])
        check('build_api', list(inspect.signature(build).parameters), ['document', 'registry'])
        check('compare_api', list(inspect.signature(compare).parameters),
              ['static_graph', 'trace_graph', 'mappings', 'context', 'registry'])
        check('no_rca_claim', entity['evidence']['rca_benefit'], 'not_checked')
        check('no_runtime_claim', entity['evidence']['runtime'], 'not_checked')

        progress('comparator-fixtures')
        p = doc['relations'][0]['provenance']
        mapping = [dict(level='entity', original=x.lower(), candidates=[x], verified=True, provenance=p)
                   for x in ['A', 'B', 'C', 'DB1', 'DB2', 'PG', 'R', 'X', 'H', 'unused']]
        context = dict(system='synthetic', level='entity', domain='synthetic', trace_revision='runtime-open',
                       revision_link_verified=False, revision_provenance=[])
        simple_doc = deepcopy(doc); simple_doc['relations'] = [doc['relations'][0]]
        simple, _ = build(simple_doc, registry)

        def trace(edges, nodes=None, level='entity', belongs=None, components=None, interval=None):
            graph = dict(level=level, nodes=nodes or [{'id': 'a'}, {'id': 'b'}],
                         edges=edges, interval_ns=interval)
            if level == 'operation':
                graph.update(belongs_to=belongs or [], component_context=components or [])
            return graph

        def edge(s='a', t='b', typ='gọi-chưa-phân-kiểu', msg=None):
            e = dict(source=s, target=t, type=typ, evidence_source='trace', destination=None,
                     event_count=7, witness=[['trace-synthetic', 'span-synthetic']])
            if msg is not None:
                e['messaging'] = msg
                e['queue_metric_address'] = [msg.get(k) for k in ['broker', 'broker_scope', 'queue']]
            return e

        graph = trace([edge()])
        snapshots = canonical([simple, graph, mapping, context, registry])
        result = compare(simple, graph, mapping, context, registry)
        save(out / 'compare-unknown.json', result)
        for view, oracle in [('typed', 'typed_unknown'), ('endpoints', 'endpoints_unknown')]:
            for key, value in expected['comparisons'][oracle].items():
                check('unknown:'+view+':'+key, result['views'][view][key], value)
        check('unknown_not_sync', result['views']['typed']['exclusions']['trace'][0]['reason'], 'unknown_type')
        check('all_compare_inputs_unchanged', canonical([simple, graph, mapping, context, registry]), snapshots)
        check('revision_conditional', result['conditional_reference'])
        wrong = compare(simple, trace([edge(typ='dữ-liệu')]), mapping, context, registry)
        for key, value in expected['comparisons']['typed_wrong'].items():
            check('wrong_type:'+key, wrong['views']['typed'][key], value)
        # Hai cửa sổ: một trace rỗng, và hai phía rỗng; không biến static thành runtime.
        empty_doc = deepcopy(doc); empty_doc['relations'] = []
        empty, _ = build(empty_doc, registry)
        empty_result = compare(empty, trace([], interval=[10, 10]), mapping, context, registry)
        for key, value in expected['comparisons']['empty'].items():
            check('empty:'+key, empty_result['views']['typed'][key], value)
        check('empty_NA', empty_result['views']['typed']['static_fraction'], None)
        check('empty_NA_trace', empty_result['views']['typed']['trace_fraction'], None)
        check('empty_trace_keeps_static', compare(simple, trace([]), mapping, context, registry)
              ['views']['typed']['static_only'], [['A', 'B', 'gọi-đồng-bộ', None]])
        for name, candidates, verified, reason in [
                ('ambiguous', ['A', 'C'], True, 'ambiguous_mapping:source'),
                ('unverified', ['A'], False, 'unverified_mapping:source'),
                ('missing', [], True, 'unmapped:source')]:
            maps = deepcopy(mapping); maps[0].update(candidates=candidates, verified=verified)
            r = compare(simple, graph, maps, context, registry)
            check('alias_'+name, r['views']['endpoints']['exclusions']['trace'][0]['reason'], reason)
            check('alias_'+name+'_no_match', r['views']['endpoints']['intersection'], [])
        maps = deepcopy(mapping); maps.append(deepcopy(maps[0]))
        reject('duplicate_mapping', lambda: compare(simple, graph, maps, context, registry), 'duplicate_mapping')
        reject('wrong_system', lambda: compare(simple, graph, mapping, dict(context, system='other'), registry), 'scope_mismatch')
        reject('day_domain', lambda: compare(simple, graph, mapping, dict(context, domain='all-day'), registry), 'comparison_domain')
        reject('verified_no_source', lambda: compare(simple, graph, mapping,
               dict(context, revision_link_verified=True), registry), 'provenance')
        reject('label_context', lambda: compare(simple, graph, mapping, dict(context, root='A'), registry), 'unknown_fields')
        reject('label_trace', lambda: compare(simple, dict(graph, root='A'), mapping, context, registry), 'unknown_fields')
        span_parent = compare(simple, trace([edge(typ='span-parent')]), mapping, context, registry)
        check('span_parent_excluded', span_parent['views']['endpoints']['exclusions']['trace'][0]['reason'], 'not_entity_dependency')
        msg_doc = deepcopy(doc)
        msg_doc['relations'] = [r for r in doc['relations'] if r['id'] in {'consume-q1', 'consume-q2'}]
        msg_static, msg_op = build(msg_doc, registry)
        msg1 = dict(broker='r', broker_scope='vhost-demo', exchange=None, routing_key=None, queue='q1')
        msg2 = dict(msg1, queue='q2')
        msg_graph = trace([edge('r', 'b', 'thông-điệp', msg1), edge('r', 'b', 'thông-điệp', msg2)],
                          nodes=[{'id': 'r'}, {'id': 'b'}])
        mr = compare(msg_static, msg_graph, mapping, context, registry)
        save(out / 'compare-two-queues.json', mr)
        check('two_queue_exact_intersection', mr['views']['typed']['intersection'], [
            ['R', 'B', 'thông-điệp', ['consume', dict(broker='R', broker_scope='vhost-demo', queue='q1')]],
            ['R', 'B', 'thông-điệp', ['consume', dict(broker='R', broker_scope='vhost-demo', queue='q2')]],
        ])
        partial = deepcopy(msg_graph); partial['edges'][1]['messaging']['queue'] = None
        partial_result = compare(msg_static, partial, mapping, context, registry)
        check('queue_missing_exclusion', partial_result['views']['typed']['exclusions']['trace'][0]['reason'], 'incomplete_messaging_address')
        check('queue_missing_intersection_literal', partial_result['views']['typed']['intersection'], [
            ['R', 'B', 'thông-điệp', ['consume', dict(broker='R', broker_scope='vhost-demo', queue='q1')]]])
        maps = deepcopy(mapping)
        opmap = dict(level='operation', original='["b","runtime-receive"]',
                     candidates=['["B","receive"]'], verified=True, provenance=p)
        maps.append(opmap)
        ot = trace([edge('r', '["b","runtime-receive"]', 'thông-điệp', msg1)],
                   nodes=[dict(id='["b","runtime-receive"]', entity='b')], level='operation',
                   belongs=[['["b","runtime-receive"]', 'b']], components=[{'id': 'r'}])
        oc = dict(context, level='operation')
        opr = compare(msg_op, ot, maps, oc, registry)
        check('operation_mapped_intersection_literal', opr['views']['typed']['intersection'], [
            ['R', '["B","receive"]', 'thông-điệp', ['consume', dict(broker='R', broker_scope='vhost-demo', queue='q1')]]])
        maps[1]['candidates'] = ['C']
        check('operation_owner_conflict', compare(msg_op, ot, maps, oc, registry)
              ['views']['typed']['exclusions']['trace'][0]['reason'], 'operation_owner_conflict:target')
        maps = deepcopy(mapping); maps[1]['candidates'] = ['A']
        collapsed = compare(simple, graph, maps, context, registry)
        check('mapped_internal_excluded', collapsed['views']['endpoints']['exclusions']['trace'][0]['reason'],
              'mapped_internal_relation')
        check('isolated_node_explicit', next(n['status'] for n in compare(empty, trace([], nodes=[{'id': 'isolated'}]),
              mapping, context, registry)['nodes']['trace']), 'unmapped')
        check('no_logical_message_synthesis', [e for e in entity['edges'] if e['channel'] == 'logical-message'], [])
        check('no_callback_invention', [e for e in operation['edges'] if e['target'] == '["A","callback"]'], [])
        same_missing = deepcopy(msg_static)
        for e in same_missing['edges']:
            e['messaging']['queue'] = None
        both_missing = deepcopy(msg_graph)
        for e in both_missing['edges']:
            e['messaging']['queue'] = None
        missing_result = compare(same_missing, both_missing, mapping, context, registry)
        check('both_missing_queue_not_match', missing_result['views']['endpoints']['intersection'], [])
        check('both_missing_queue_empty_eligible', missing_result['views']['typed']['static_denominator'], 0)
        # Nguồn static khác runtime không được đổi provenance hoặc bịa event_count.
        published_doc = deepcopy(doc)
        published_doc['relations'] = [r for r in doc['relations'] if r['id'] in {'publish', 'republish'}]
        pub, _ = build(published_doc, registry)
        pubmsg = dict(broker='r', broker_scope='vhost-demo', exchange='e', routing_key='k', queue=None)
        pubtrace = trace([edge('a', 'r', 'thông-điệp', pubmsg)], nodes=[{'id': 'a'}, {'id': 'r'}])
        pubresult = compare(pub, pubtrace, mapping, context, registry)
        check('publish_address_literal', pubresult['views']['typed']['intersection'], [
            ['A', 'R', 'thông-điệp', ['publish', dict(broker='R', broker_scope='vhost-demo', exchange='e', routing_key='k')]]])
        check('member_static_no_event_count', 'event_count' not in pubresult['views']['typed']['members']['static'][0]['members'][0]['original'])
        check('member_trace_preserves_count', pubresult['views']['typed']['members']['trace'][0]['members'][0]['original']['event_count'], 7)
        # Default exchange chuỗi rỗng có nghĩa, khác thiếu.
        default_doc = deepcopy(published_doc)
        for e in default_doc['relations']:
            e['messaging'].update(exchange='', routing_key='')
        default_static, _ = build(default_doc, registry)
        default_trace = deepcopy(pubtrace)
        default_trace['edges'][0]['messaging'].update(exchange='', routing_key='')
        default_result = compare(default_static, default_trace, mapping, context, registry)
        check('default_exchange_not_missing', default_result['views']['typed']['numerator'], 1)
        unknown_exchange = deepcopy(default_trace); unknown_exchange['edges'][0]['messaging']['exchange'] = None
        check('unknown_exchange_excluded', compare(default_static, unknown_exchange, mapping, context, registry)
              ['views']['typed']['exclusions']['trace'][0]['reason'], 'incomplete_messaging_address')
        filtered = compare(simple, graph, mapping, dict(context, relation_types=['dữ-liệu']), registry)
        check('outside_relation_domain_static', filtered['views']['typed']['exclusions']['static'][0]['reason'], 'outside_relation_domain')
        reject('invalid_interval', lambda: compare(simple, dict(graph, interval_ns=[10, 2]), mapping, context, registry), 'invalid_interval')

        progress('trace-builder-messaging-integration')
        import pandas as pd
        from do_thi.builder import build as trace_build
        rows = []
        for ident, service, operation_name, kind, attrs, links in [
            ('p', 'a', 'send', 'PRODUCER', {'messaging.broker': 'r', 'messaging.broker_scope': 'vhost-demo',
             'messaging.exchange': 'e', 'messaging.routing_key': 'k'}, []),
            ('c1', 'b', 'receive', 'CONSUMER', {'messaging.broker': 'r', 'messaging.broker_scope': 'vhost-demo',
             'messaging.queue': 'q1'}, [{'traceID': 'trace-demo', 'spanID': 'p',
                                        'semantics': 'message_creation', 'semantics_verified': True}]),
            ('c2', 'b', 'receive', 'CONSUMER', {'messaging.broker': 'r', 'messaging.broker_scope': 'vhost-demo',
             'messaging.queue': 'q2'}, [{'traceID': 'trace-demo', 'spanID': 'p',
                                        'semantics': 'message_creation', 'semantics_verified': True}]),
        ]:
            rows.append(dict(traceID='trace-demo', spanID=ident, parentSpanID='0', serviceName=service,
                             operationName=operation_name, startTime=1, duration=1, kind=kind,
                             attributes=attrs, links=links))
        integ_entity, integ_operation = trace_build(pd.DataFrame(rows), None, {}, {'a': 'service', 'b': 'service', 'r': 'broker'})
        save(out / 'trace-synthetic-messaging.json', dict(entity=integ_entity, operation=integ_operation))
        integration_doc = deepcopy(doc)
        integration_doc['relations'] = [r for r in doc['relations'] if r['id'] in {'publish', 'consume-q1', 'consume-q2'}]
        integ_static, _ = build(integration_doc, registry)
        integ_result = compare(integ_static, integ_entity, mapping, context, registry)
        save(out / 'compare-trace-builder-messaging.json', integ_result)
        check('trace_builder_broker_legs_literal', integ_result['views']['typed']['intersection'], [
            ['A', 'R', 'thông-điệp', ['publish', dict(broker='R', broker_scope='vhost-demo', exchange='e', routing_key='k')]],
            ['R', 'B', 'thông-điệp', ['consume', dict(broker='R', broker_scope='vhost-demo', queue='q1')]],
            ['R', 'B', 'thông-điệp', ['consume', dict(broker='R', broker_scope='vhost-demo', queue='q2')]],
        ])
        check('trace_builder_logical_trace_only_literal', integ_result['views']['typed']['trace_only'], [
            ['A', 'B', 'thông-điệp', ['logical-message', dict(broker='R', broker_scope='vhost-demo', exchange='e', routing_key='k', queue='q1')]],
            ['A', 'B', 'thông-điệp', ['logical-message', dict(broker='R', broker_scope='vhost-demo', exchange='e', routing_key='k', queue='q2')]],
        ])
        check('trace_builder_inferred_provenance', sorted({e['evidence_source'] for e in integ_entity['edges']}), ['inferred', 'trace'])

        progress('r1-role-address-regression')
        r1_path = ROOT / 'results/T-036/fixtures/r1.json'
        r1 = read(r1_path)
        r1_results = []
        for case in r1['consume_cases']:
            source_doc = deepcopy(doc)
            source_doc['relations'] = [r for r in source_doc['relations'] if r['id'] == 'consume-q1']
            source_doc['relations'][0]['messaging'].update(case['static'])
            source_entity, source_operation = build(source_doc, registry)
            address = dict(msg1, **case['trace'])
            traces = {
                'entity': trace([edge('r', 'b', 'thông-điệp', address)], nodes=[{'id': 'r'}, {'id': 'b'}]),
                'operation': trace([edge('r', '["b","runtime-receive"]', 'thông-điệp', address)],
                    nodes=[dict(id='["b","runtime-receive"]', entity='b')], level='operation',
                    belongs=[['["b","runtime-receive"]', 'b']], components=[{'id': 'r'}]),
            }
            for level, source in [('entity', source_entity), ('operation', source_operation)]:
                maps = deepcopy(mapping) + ([deepcopy(opmap)] if level == 'operation' else [])
                before_r1 = canonical([source, traces[level]])
                value = compare(source, traces[level], maps, dict(context, level=level), registry)
                r1_results.append(dict(case=case['name'], level=level, result=value))
                check('r1_input_unchanged:'+case['name']+':'+level,
                      canonical([source, traces[level]]), before_r1)
                for view, data in value['views'].items():
                    label = case['name']+':'+level+':'+view
                    check('r1_counts:'+label,
                          [data[k] for k in ['numerator', 'static_denominator', 'trace_denominator']], case['counts'])
                    if case['counts'][0]:
                        check('r1_intersection:'+label, data['intersection'], [r1['consume_keys'][level][view]])
                        check('r1_static_member_preserved:'+label,
                              data['members']['static'][0]['members'][0]['original'], source['edges'][0])
                        check('r1_trace_member_preserved:'+label,
                              data['members']['trace'][0]['members'][0]['original'], traces[level]['edges'][0])
        # Hai địa chỉ nguồn phát vẫn giữ trong members của một chặng nhận.
        source_doc = deepcopy(doc)
        source_doc['relations'] = [r for r in source_doc['relations'] if r['id'] == 'consume-q1']
        source_doc['relations'][0]['messaging'].update(exchange='e', routing_key='k')
        second = deepcopy(source_doc['relations'][0]); second['id'] = 'consume-q1-other-route'
        second['messaging'].update(exchange='other-exchange', routing_key='other-key')
        source_doc['relations'].append(second)
        source_entity, _ = build(source_doc, registry)
        value = compare(source_entity, trace([edge('r', 'b', 'thông-điệp', msg1)],
                        nodes=[{'id': 'r'}, {'id': 'b'}]), mapping, context, registry)
        r1_results.append(dict(case='two_source_routes_one_consume', result=value))
        for view, data in value['views'].items():
            check('r1_fanin_counts:'+view,
                  [data[k] for k in ['numerator', 'static_denominator', 'trace_denominator']],
                  r1['two_source_routes_one_consume']['counts'])
            check('r1_fanin_members:'+view, len(data['members']['static'][0]['members']),
                  r1['two_source_routes_one_consume']['static_members'])
            check('r1_fanin_originals:'+view,
                  sorted([m['original'] for m in data['members']['static'][0]['members']], key=canonical),
                  sorted(source_entity['edges'], key=canonical))
        changed_publish = deepcopy(pubtrace)
        changed_publish['edges'][0]['messaging']['exchange'] = 'other-exchange'
        value = compare(pub, changed_publish, mapping, context, registry)
        r1_results.append(dict(case='publish_different_exchange', result=value))
        for view, data in value['views'].items():
            check('r1_publish_distinct:'+view,
                  [data[k] for k in ['numerator', 'static_denominator', 'trace_denominator']],
                  r1['publish_different_exchange']['counts'])
        logical_doc = deepcopy(doc)
        logical = deepcopy(next(r for r in doc['relations'] if r['id'] == 'http'))
        logical.update(id='logical-r1', type='thông-điệp', channel='logical-message',
                       messaging=dict(broker='R', broker_scope='vhost-demo', exchange='e', routing_key='k', queue='q1'))
        logical_doc['relations'] = [logical]
        logical_static, _ = build(logical_doc, registry)
        logical_trace = trace([edge('a', 'b', 'thông-điệp',
            dict(broker='r', broker_scope='vhost-demo', exchange='e', routing_key='other-key', queue='q1'))])
        value = compare(logical_static, logical_trace, mapping, context, registry)
        r1_results.append(dict(case='logical_different_routing', result=value))
        for view, data in value['views'].items():
            check('r1_logical_distinct:'+view,
                  [data[k] for k in ['numerator', 'static_denominator', 'trace_denominator']],
                  r1['logical_different_routing']['counts'])
        save(out / 'r1-regression.json', dict(fixture_sha256=sha(r1_path), cases=r1_results))

        progress('deterministic-order-and-membership')
        for seed in [0, 1, 2]:
            shuffled = deepcopy(doc)
            rng = random.Random(seed)
            for key in ['entities', 'operations', 'relations', 'resource_bindings', 'signals']:
                rng.shuffle(shuffled[key])
            check('build_reorder:'+str(seed), canonical(build(shuffled, registry)), canonical((entity, operation)))
            maps = deepcopy(mapping); rng.shuffle(maps)
            check('compare_mapping_reorder:'+str(seed), canonical(compare(simple, graph, maps, context, registry)), canonical(result))
        for name, value in [('unknown', result), ('two-queues', mr), ('missing-queue', partial_result), ('wrong-type', wrong)]:
            for view, data in value['views'].items():
                # Bảo toàn phân hoạch từ danh sách thực, độc lập số tổng.
                ss = {canonical(x) for x in data['S']}; tt = {canonical(x) for x in data['T']}
                ii = {canonical(x) for x in data['intersection']}
                check(f'partition:{name}:{view}', ss == ii | {canonical(x) for x in data['static_only']} and
                      tt == ii | {canonical(x) for x in data['trace_only']} and ii == ss & tt)
                for side in ['static', 'trace']:
                    source = simple if side == 'static' and name in {'unknown', 'wrong-type'} else msg_static if side == 'static' else graph
                    check(f'membership:{name}:{view}:{side}', len(data['members'][side]), len(data['S' if side == 'static' else 'T']))

        progress('saved-dev-graph-compatibility')
        manifest_path = ROOT / 'results/T-035/manifest.json'
        manifest = read(manifest_path)
        graph_rows = [r for r in manifest['files'] if r['path'].startswith('results/T-035/do-thi/') and
                      r['path'].endswith(('/full.json', '/N.json', '/A.json'))]
        compatibility = []
        # Chỉ graph allowlisted được manifest liệt kê; không đọc trace thô hoặc nhãn.
        for row in graph_rows:
            path = ROOT / row['path']
            if sha(path) != row['sha256']:
                raise ValueError('saved_graph_hash_mismatch:'+row['path'])
            actual = read(path)
            dataset = path.relative_to(ROOT / 'results/T-035/do-thi').parts[0]
            empty_source = dict(scope=dict(system=dataset, revision='compatibility-only'),
                                entities=[], operations=[], relations=[], resource_bindings=[], signals=[])
            eg, og = build(empty_source, registry)
            ctx = dict(system=dataset, level=actual['level'], domain='dev-adapter' if dataset == 'Nezha-OB' else 'dev-file',
                       trace_revision='dataset-application-OPEN', revision_link_verified=False, revision_provenance=[])
            before_hash = canonical(actual)
            adapted = compare(eg if actual['level'] == 'entity' else og, actual, [], ctx, registry)
            if canonical(actual) != before_hash:
                raise AssertionError('trace_mutated')
            compatibility.append(dict(path=row['path'], sha256=row['sha256'], level=actual['level'],
                                      edge_count=len(actual['edges']),
                                      excluded_without_mapping=len(adapted['views']['endpoints']['exclusions']['trace']),
                                      conditional=adapted['conditional_reference']))
        save(out / 'compatibility.json', dict(manifest_sha256=sha(manifest_path), graphs=compatibility,
             meaning='schema/không mutation; không là đối chiếu kiến trúc TT/OB',
             all_excluded_without_mapping=all(x['edge_count'] == x['excluded_without_mapping'] for x in compatibility)))
        check('real_graphs_present_both_datasets', sorted({Path(r['path']).parts[3] for r in compatibility}), ['Nezha-OB', 'RE2-TT'])
        check('real_graphs_no_fabricated_mapping', all(x['edge_count'] == x['excluded_without_mapping'] for x in compatibility))
        check('real_graphs_both_levels', sorted({x['level'] for x in compatibility}), ['entity', 'operation'])
        # T-035 project sử dụng độc lập code trace; so phép chiếu với graph entity đã lưu.
        from do_thi.builder import edge_key, project as trace_project
        paired = []
        by_path = {r['path']: r for r in graph_rows}
        for row in graph_rows:
            if '/thao-tac/' not in row['path']:
                continue
            ent_path = row['path'].replace('/thao-tac/', '/thuc-the/')
            if ent_path not in by_path:
                raise ValueError('missing_projection_pair')
            ent, ops = read(ROOT / ent_path), read(ROOT / row['path'])
            pn, pe = trace_project(ops)
            ok = pn == {n['id'] for n in ent['nodes']} and pe == {edge_key(e) for e in ent['edges']}
            paired.append(dict(operation=row['path'], entity=ent_path, ok=ok))
        save(out / 'trace-projections.json', paired)
        check('saved_trace_projection_pairs', bool(paired) and all(x['ok'] for x in paired))
        progress('finished')
        save(out / 'result.json', dict(checks=checks, passed=sum(c['ok'] for c in checks),
             failed=sum(not c['ok'] for c in checks), all_pass=all(c['ok'] for c in checks),
             compatibility_graph_count=len(compatibility), trace_projection_pair_count=len(paired),
             seconds=time.perf_counter()-started, python_tracemalloc_peak_bytes=tracemalloc.get_traced_memory()[1],
             peak_working_set_bytes=peak_working_set(),
             memory_note='Python allocation peak, not whole-process RSS', stages=stages))
        print(canonical(dict(passed=sum(c['ok'] for c in checks), failed=[c['name'] for c in checks if not c['ok']],
                             graphs=len(compatibility), projection_pairs=len(paired), seconds=time.perf_counter()-started)))
        return 0 if all(c['ok'] for c in checks) else 1
    except Exception:
        save(out / 'failure.json', dict(traceback=traceback.format_exc(), checks=checks,
                                        seconds=time.perf_counter()-started, stages=stages))
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
