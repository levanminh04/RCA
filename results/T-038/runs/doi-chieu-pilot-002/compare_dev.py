"""Đối chiếu toàn graph dev đã lưu; mapping nguồn độc lập với tên ca/nhãn."""
from collections import Counter, defaultdict
from copy import deepcopy
import ctypes
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

from engine import (OUT, ROOT, REV, canon, checksum, exact_operation_candidates,
                    load, op_id, pinned_api, save)


def rss_peak():
    class Counters(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong),
                    ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                    ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                    ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                    ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb)
    return counters.PeakWorkingSetSize


def fixture_check(run):
    oracle_path = OUT / 'fixtures/oracle.json'
    oracle = load(oracle_path)
    b, c = pinned_api()
    provenance = [dict(source_id='fixture', locator='literal oracle before root transform code',
                       condition='synthetic fixture, not Train Ticket data')]
    registry = dict(sources=[dict(id='fixture', kind='synthetic-oracle', revision='literal-v1',
                                 sha256=checksum(oracle_path), condition='synthetic, no runtime claim')])
    document = dict(scope=dict(system='RE2-TT', revision='fixture'),
                    entities=[dict(x, name=x['id'], granularity='component', role='fixture', provenance=provenance)
                              for x in oracle['entities']],
                    operations=[dict(x, runtime_name=None, provenance=provenance) for x in oracle['operations']],
                    relations=[dict(x, messaging=None, context='fixture', provenance=provenance) for x in oracle['relations']],
                    resource_bindings=[], signals=[])
    entity, operation = b.build(document, registry)
    checks = {}
    expected = oracle['expected']
    checks['entity_count'] = len(entity['edges']) == expected['entity_edge_count']
    checks['operation_count'] = len(operation['edges']) == expected['operation_edge_count']
    checks['projection_literal'] = sorted([[x['source'], x['target']] for x in b.project(operation)['edges']]) == expected['projected_entity_edges']
    checks['entity_only_literal'] = sorted(x['record_id'] for x in operation['operation_exclusions']) == expected['entity_only_record_ids']
    for i, test in enumerate(expected['mapping_cases']):
        got, verified = exact_operation_candidates(test['entity'], test['runtime_operation'], document['operations'])
        checks['mapping_literal_' + str(i)] = got == test['candidates'] and verified == test['verified']
    aliases = oracle['trace_entity_aliases']
    reverse = {v: k for k, v in aliases.items()}
    trace = dict(level='entity', interval_ns=None,
                 nodes=[dict(id=x) for x in aliases],
                 edges=[dict(source=reverse[e['source']], target=reverse[e['target']], type='gọi-chưa-phân-kiểu',
                             evidence_source='trace', destination=None, event_count=1, witness=[]) for e in entity['edges']])
    mappings = [dict(level='entity', original=k, candidates=[v], verified=True, provenance=provenance) for k, v in aliases.items()]
    context = dict(system='RE2-TT', level='entity', domain='synthetic', trace_revision='fixture',
                   revision_link_verified=False, revision_provenance=[])
    before = canon([entity, trace, mappings, context, registry])
    result = c.compare(entity, trace, mappings, context, registry)
    for name in ['endpoints', 'typed']:
        view = result['views'][name]
        literal = expected['entity_' + name]
        for key in ['S', 'T', 'intersection', 'static_only', 'trace_only']:
            checks['view_' + name + '_' + key] = len(view[key]) == literal[key]
    checks['typed_NA'] = result['views']['typed']['trace_fraction'] is None
    reordered = deepcopy(document)
    for key in ['entities', 'operations', 'relations', 'resource_bindings', 'signals']:
        reordered[key].reverse()
    checks['build_reorder_invariant'] = canon(b.build(reordered, registry)) == canon((entity, operation))
    checks['input_unchanged'] = before == canon([entity, trace, mappings, context, registry])
    # Counterexample bổ sung sau khi đọc nguồn SMTP: không đổi enum dùng chung.
    smtp_doc = deepcopy(document)
    smtp_doc['relations'][0]['channel'] = 'smtp'
    rejected = None
    try:
        b.build(smtp_doc, registry)
    except ValueError as exc:
        rejected = str(exc)
    checks['smtp_not_silently_coerced'] = rejected == 'relation_type'
    save(run / 'fixture-input.json', document)
    save(run / 'fixture-result.json', dict(checks=checks, ok=all(checks.values()), result=result,
                                           oracle_sha256=checksum(oracle_path), smtp_rejection=rejected,
                                           smtp_check_chronology='supplemental after source; not pre-code oracle'))
    assert all(checks.values()), checks
    return checks


def make_mappings(graphs, document, registry, java):
    inventory = {r['id']: r for r in document['entities']}
    operations = document['operations']
    known_ops = {(r['entity'], r['name']): r for r in operations}
    trace_entities, trace_ops = set(), set()
    for graph in graphs:
        if graph['level'] == 'entity':
            trace_entities.update(n['id'] for n in graph['nodes'])
        else:
            trace_entities.update(n['entity'] for n in graph['nodes'])
            trace_entities.update(n['id'] for n in graph.get('component_context', []))
            trace_ops.update((n['id'], n['entity'], n['operation']) for n in graph['nodes'])
    tree_prov = [dict(source_id='TT:tree', locator='complete identified tree and source inventory',
                      condition='descriptor absent/unverified in inspected source; semantic completeness OPEN')]
    mappings, notes = [], []
    for ident in sorted(trace_entities):
        found = inventory.get(ident)
        mappings.append(dict(level='entity', original=ident, candidates=[ident] if found else [],
                             verified=bool(found), provenance=found['provenance'] if found else tree_prov))
        notes.append(dict(level='entity', original=ident,
                          basis='exact declared source component identifier' if found else 'no verified source identity',
                          runtime_implementation_revision_verified=False))
    for ident, owner, name in sorted(trace_ops):
        candidates, verified = exact_operation_candidates(owner, name, operations)
        reason = 'exact HTTP descriptor and source owner; dataset revision remains conditional'
        if not candidates and name in {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}:
            mids = {r.get('java_method_id') for r in java['relations'] if r['kind'] == 'http_call' and
                    r['owner'] == owner and r.get('http_method') == name}
            candidates = sorted({'java:' + mid.split('::', 1)[-1] for mid in mids if mid and
                                 (owner, 'java:' + mid.split('::', 1)[-1]) in known_ops})
            reason = 'generic client verb; callsite/instrumentation unresolved; all source candidates retained'
            verified = False
        if not candidates and '.' in name and ' ' not in name:
            cls, method = name.rsplit('.', 1)
            candidates = sorted({r['name'] for r in operations if r['entity'] == owner and
                                 ('.' + cls + '#' + method + '(') in r['name']})
            reason = 'class/method descriptor candidate; runtime instrumentation name not verified'
            verified = False
        candidate_ids = [op_id(owner, candidate) for candidate in candidates]
        provenance = []
        for candidate in candidates:
            provenance.extend(known_ops[(owner, candidate)]['provenance'])
        provenance = [json.loads(k) for k in sorted({canon(x) for x in provenance})] or tree_prov
        mappings.append(dict(level='operation', original=ident, candidates=candidate_ids,
                             verified=verified, provenance=provenance))
        notes.append(dict(level='operation', original=ident, basis=reason, runtime_name_verified=False,
                          descriptor_mapping_verified=verified, candidates=candidate_ids,
                          runtime_implementation_revision_verified=False))
    return mappings, notes


def semantic_result(result):
    values = {}
    for name, view in result['views'].items():
        values[name] = {k: view[k] for k in ['S', 'T', 'intersection', 'static_only', 'trace_only',
                                          'numerator', 'static_denominator', 'trace_denominator',
                                          'static_fraction', 'trace_fraction']}
        values[name]['members'] = {side: sorted([dict(key=r['key'],
                originals=sorted([m['original'] for m in r['members']], key=canon)) for r in view['members'][side]], key=canon)
                for side in ['static', 'trace']}
        values[name]['exclusions'] = {side: sorted([dict(reason=r['reason'], original=r['original'])
                                    for r in view['exclusions'][side]], key=canon) for side in ['static', 'trace']}
    return canon(values)


def independent_sets(static, trace, mappings, level, view):
    """Reference set algebra for current all-untyped nonmessaging trace input."""
    mapping = {(r['level'], r['original']): r for r in mappings}
    owners = dict(trace.get('belongs_to', []))
    static_owners = dict(static.get('belongs_to', []))

    def resolved(ident):
        lev = 'operation' if ident in owners else 'entity'
        row = mapping.get((lev, ident))
        if not row or not row['verified'] or len(set(row['candidates'])) != 1:
            return None
        target = row['candidates'][0]
        if lev == 'operation':
            parent = resolved(owners[ident])
            if parent is None or static_owners[target] != parent:
                return None
        return target

    s, t = set(), set()
    for edge in static['edges']:
        if edge['type'] == 'thông-điệp':
            # Current source namespace/default exchange deliberately incomplete → excluded.
            assert edge['messaging']['broker_scope'] is None
            continue
        if level == 'entity' and (edge['source'] == edge['target'] or edge['type'] == 'span-parent'):
            continue
        if view == 'typed' and edge['type'] == 'gọi-chưa-phân-kiểu':
            continue
        s.add(canon([edge['source'], edge['target'], edge['type'] if view == 'typed' else None, None]))
    for edge in trace['edges']:
        assert edge['type'] == 'gọi-chưa-phân-kiểu'
        if view == 'typed':
            continue
        a, b = resolved(edge['source']), resolved(edge['target'])
        if a is None or b is None or (level == 'entity' and a == b):
            continue
        t.add(canon([a, b, None, None]))
    return s, t


def compare_all(run_name, pilot=False):
    run = OUT / 'runs' / run_name
    run.mkdir(parents=True, exist_ok=False)
    (run / 'compare_dev.py').write_bytes(Path(__file__).read_bytes())
    (run / 'engine.py').write_bytes((OUT / 'engine.py').read_bytes())
    start = time.monotonic()
    fixture = fixture_check(run)
    b, c = pinned_api()
    document, registry = load(OUT / 'ban-ghi.json'), load(OUT / 'nguon.json')
    source_metadata = OUT / 'sources/train-ticket-v1.0.0/_acquisition-tree.json'
    registry['sources'].append(dict(id='TT:tree', kind='Git-tree-metadata', revision=REV,
                                    sha256=checksum(source_metadata), path=source_metadata.relative_to(ROOT).as_posix(),
                                    condition='complete tree metadata; source semantic completeness OPEN'))
    graphs_by_level = {'entity': load(OUT / 'do-thi/thuc-the.json'),
                       'operation': load(OUT / 'do-thi/thao-tac.json')}
    java = load(OUT / 'runs/lap-ban-ghi-004/java.json')
    manifest35 = load(ROOT / 'results/T-035/manifest.json')
    entries = [r for r in manifest35['files'] if r['path'].startswith('results/T-035/do-thi/RE2-TT/')]

    def verified_graph(entry):
        path = ROOT / entry['path']
        assert path.stat().st_size == entry['bytes'] and checksum(path) == entry['sha256']
        return load(path)

    def all_graphs():
        for entry in entries:
            yield verified_graph(entry)

    mappings, mapping_notes = make_mappings(all_graphs(), document, registry, java)
    save(run / 'mapping.json', mappings)
    save(run / 'mapping-notes.json', mapping_notes)
    save(run / 'registry.json', registry)
    save(run / 'input-hashes.json', {name: checksum(OUT / name) for name in ['ban-ghi.json', 'nguon.json',
                                                                                'do-thi/thuc-the.json', 'do-thi/thao-tac.json']})
    if not pilot:
        save(OUT / 'mapping.json', mappings)
        save(OUT / 'mapping-notes.json', mapping_notes)
    if pilot:
        chosen = []
        for level in ['thuc-the', 'thao-tac']:
            chosen.append(next(r for r in entries if '/' + level + '/full.json' in r['path']))
            chosen.append(next(r for r in entries if '/' + level + '/N.json' in r['path']))
        entries = chosen
    rows, errors = [], []
    grouped = defaultdict(lambda: defaultdict(set))
    relation_examples = {}
    self_checks = []
    compression_bytes = uncompressed_bytes = 0
    for i, entry in enumerate(entries):
        try:
            graph = verified_graph(entry)
            static = graphs_by_level[graph['level']]
            active_mappings = [r for r in mappings if r['level'] == 'entity' or graph['level'] == 'operation']
            context = dict(system='RE2-TT', level=graph['level'], domain='dev-file',
                           trace_revision='T035-v2.1-manifest:' + checksum(ROOT / 'results/T-035/manifest.json'),
                           revision_link_verified=False, revision_provenance=[])
            before = canon([static, graph, active_mappings, context, registry])
            result = c.compare(static, graph, active_mappings, context, registry)
            unchanged = before == canon([static, graph, active_mappings, context, registry])
            assert unchanged and result['conditional_reference'] and result['interval_ns'] == graph['interval_ns']
            view_rows = {}
            for view_name, view in result['views'].items():
                s, t = independent_sets(static, graph, active_mappings, graph['level'], view_name)
                expected = {'S': s, 'T': t, 'intersection': s & t, 'static_only': s - t, 'trace_only': t - s}
                assert all({canon(x) for x in view[key]} == value for key, value in expected.items())
                assert view['static_fraction'] == (len(s & t) / len(s) if s else None)
                assert view['trace_fraction'] == (len(s & t) / len(t) if t else None)
                for side, original in [('static', static), ('trace', graph)]:
                    indices = [r['index'] for group in view['members'][side] for r in group['members']]
                    indices += [r['index'] for r in view['exclusions'][side]]
                    assert sorted(indices) == list(range(len(original['edges'])))
                    assert all(r['original'] == original['edges'][r['index']]
                               for group in view['members'][side] for r in group['members'])
                view_rows[view_name] = {key: len(value) for key, value in expected.items()}
                view_rows[view_name].update(static_fraction=view['static_fraction'], trace_fraction=view['trace_fraction'],
                                            exclusions={side: dict(Counter(x['reason'] for x in view['exclusions'][side]))
                                                        for side in ['static', 'trace']})
                for category in ['intersection', 'static_only', 'trace_only']:
                    for key in view[category]:
                        ident = canon([graph['level'], view_name, key])
                        grouped[ident][category].add(entry['path'])
                        relation_examples.setdefault(ident, dict(level=graph['level'], view=view_name, key=key))
            repeated = c.compare(static, graph, active_mappings, context, registry)
            trace_reordered = deepcopy(graph)
            trace_reordered['nodes'].reverse()
            trace_reordered['edges'].reverse()
            if 'belongs_to' in trace_reordered:
                trace_reordered['belongs_to'].reverse()
                trace_reordered['component_context'].reverse()
            reordered = c.compare(static, trace_reordered, list(reversed(active_mappings)), context, registry)
            repeat_same = canon(result) == canon(repeated)
            reorder_same = semantic_result(result) == semantic_result(reordered)
            assert repeat_same and reorder_same
            tail = entry['path'].split('results/T-035/do-thi/RE2-TT/', 1)[1]
            dest = OUT / 'doi-chieu' / run_name / (tail + '.gz')
            payload = canon(result).encode()
            compressed = gzip.compress(payload, compresslevel=6, mtime=0)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(compressed)
            assert json.loads(gzip.decompress(compressed)) == result
            compression_bytes += len(compressed)
            uncompressed_bytes += len(payload)
            rows.append(dict(input=entry['path'], input_sha256=entry['sha256'], level=graph['level'], interval_ns=graph['interval_ns'],
                             output=dest.relative_to(ROOT).as_posix(), output_sha256=checksum(dest),
                             conditional_reference=result['conditional_reference'], views=view_rows,
                             mapping_status=dict(Counter(x['status'] for x in result['nodes']['trace'])),
                             raw_trace_edge_types=dict(Counter(x['type'] for x in graph['edges']))))
            self_checks.append(dict(input=entry['path'], input_unchanged=unchanged, same_input_identical=repeat_same,
                                    reordered_semantically_identical=reorder_same,
                                    same_input_result_sha256=hashlib.sha256(canon(repeated).encode()).hexdigest(),
                                    semantic_sha256=hashlib.sha256(semantic_result(result).encode()).hexdigest()))
            if i % 25 == 0 or i == len(entries) - 1:
                print(canon(dict(done=i+1, total=len(entries), elapsed_progress_seconds=time.monotonic()-start,
                                peak_working_set_bytes=rss_peak())), flush=True)
        except Exception as exc:
            error = dict(input=entry['path'], error=repr(exc), traceback=traceback.format_exc())
            errors.append(error)
            save(run / ('error-' + str(i) + '.json'), error)
            raise
    save(run / 'self-checks.json', dict(ok=all(r['input_unchanged'] and r['same_input_identical'] and
                                                r['reordered_semantically_identical'] for r in self_checks),
                                         description='Repeated/reordered runs retained as per-graph verification outputs/hashes; full mismatch results saved on failure.',
                                         rows=self_checks))
    edges = [dict(relation_examples[k], groups={category: sorted(paths) for category, paths in grouped[k].items()})
             for k in sorted(grouped)]
    save(run / 'edge-groups.json', edges)
    summary = dict(task='T-038', run=run_name, pilot=pilot, created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                   graph_count=len(rows), graph_family_counts=dict(Counter((r['level'] + ':' + Path(r['input']).stem.split('-')[0]) for r in rows)),
                   conditional_reference_count=sum(r['conditional_reference'] for r in rows), rows=rows, errors=errors,
                   fixture_checks_passed=sum(fixture.values()), fixture_checks_total=len(fixture),
                   compressed_output_bytes=compression_bytes, uncompressed_json_bytes=uncompressed_bytes,
                   elapsed_progress_seconds=time.monotonic()-start, peak_working_set_bytes=rss_peak(),
                   cost_condition='Observed execution accounting; no concurrent Python workload seen in preflight, not an isolated benchmark.',
                   own_input_unchanged_checks=len(self_checks), repeated_and_reordered_checks=len(self_checks),
                   complete_source_inventory_claim=False, benefit_or_instrumentation_claim=False)
    save(run / 'summary.json', summary)
    if not pilot:
        save(OUT / 'doi-chieu/index.json', dict(current_run=run_name, summary='results/T-038/runs/' + run_name + '/summary.json',
                                               graph_count=len(rows), outputs=[r['output'] for r in rows]))
    print(canon({k: summary[k] for k in ['graph_count', 'compressed_output_bytes', 'elapsed_progress_seconds', 'peak_working_set_bytes']}))


if __name__ == '__main__':
    compare_all(sys.argv[1], pilot='--pilot' in sys.argv[2:])
