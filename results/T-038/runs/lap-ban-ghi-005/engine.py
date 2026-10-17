"""Bản ghi nguồn TT → T036 ghim; không nhận nhãn hoặc đọc telemetry thô."""
from collections import defaultdict
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/T-038'
SOURCE = OUT / 'sources/train-ticket-v1.0.0'
REV = 'fa8d9efb35b2ed5ec1d18f60510167767c8fb2bf'


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pinned_api():
    directory = ROOT / 'results/T-036/runs/kiem-r1-after-002/code'
    hashes = load(directory.parent / 'code-hashes.json')
    for path, expected in hashes.items():
        assert checksum(ROOT / path) == expected
        assert checksum(directory / Path(path).name) == expected
    package = types.ModuleType('_t038_pinned_t036')
    package.__path__ = [str(directory)]
    sys.modules[package.__name__] = package
    for name in ['build', 'compare']:
        spec = importlib.util.spec_from_file_location(package.__name__ + '.' + name, directory / (name + '.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return sys.modules[package.__name__ + '.build'], sys.modules[package.__name__ + '.compare']


def op_id(owner, name):
    return json.dumps([owner, name], ensure_ascii=False, separators=(',', ':'))


def exact_operation_candidates(owner, runtime_name, operations):
    """Chỉ descriptor endpoint cùng owner; không đoán GET, concrete ID hoặc repo instrumentation."""
    candidates = sorted({r['name'] for r in operations if r['entity'] == owner and
                         r['name'] == runtime_name and re.match(r'^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS) /', r['name'])})
    return candidates, len(candidates) == 1


def assemble(run_name):
    run = OUT / 'runs' / run_name
    run.mkdir(parents=True, exist_ok=False)
    (run / 'engine.py').write_bytes(Path(__file__).read_bytes())
    paths = {'java': OUT / 'runs/trien-khai-001/java-source/source-facts.json',
             'part': OUT / 'runs/trien-khai-001/coverage/part-document.json',
             'part_registry': OUT / 'runs/trien-khai-001/coverage/part-registry.json',
             'signal_supplement': OUT / 'runs/trien-khai-001/coverage/signals-supplement.json',
             'signal_registry': OUT / 'runs/trien-khai-001/coverage/registry-additional.json'}
    inputs = {}
    for key, path in paths.items():
        inputs[key] = load(path)
        (run / (key + '.json')).write_bytes(path.read_bytes())
    acquired = load(OUT / 'runs/tai-nguon-001/manifest.json')
    assert acquired['ok'] and acquired['commit'] == REV
    source_rows = {r['source_path']: r for r in acquired['files']}
    registry = {r['id']: r for r in inputs['part_registry']['sources']}
    for row in inputs['signal_registry']['sources']:
        prior = registry.get(row['id'])
        if prior:
            assert (prior['path'], prior['sha256'], prior['revision']) == (row['path'], row['sha256'], row['revision'])
        assert checksum(ROOT / row['path']) == row['sha256']
        assert row['revision'] == REV
        registry.setdefault(row['id'], row)
    document = deepcopy(inputs['part'])
    assert document['scope'] == {'system': 'RE2-TT', 'revision': REV}
    entities = {r['id']: r for r in document['entities']}
    operations = {(r['entity'], r['name']): r for r in document['operations']}
    relations = list(document['relations'])
    bindings = list(document['resource_bindings'])
    signals = list(document['signals'])
    assert inputs['signal_supplement']['scope'] == document['scope']
    signals += inputs['signal_supplement']['signals']
    unresolved = []
    catalog = []

    def prov(fact, full_header=False):
        path = fact['source_path']
        assert path in source_rows
        assert '/Json2Shiviz/bin/' not in path and '/example/' not in path
        row = source_rows[path]
        # Chỉ các source dùng làm bằng chứng, không đọc raw sample để tạo registry.
        assert checksum(ROOT / row['path']) == row['sha256']
        ident = 'TT:' + path
        registry[ident] = dict(id=ident, kind='source-code/configuration', revision=REV,
                               sha256=row['sha256'], path=row['path'],
                               condition='release source; dataset/application/deployment link OPEN')
        start = 1 if full_header else fact.get('line', 1)
        end = fact.get('end_line', fact.get('line', 1))
        return [dict(source_id=ident, locator=f'L{start}-L{end}',
                     condition=fact.get('condition', 'source declaration; runtime not verified'))]

    def merge_prov(a, b):
        return [json.loads(k) for k in sorted({canon(x) for x in a + b})]

    def entity(ident, typ, role, fact, granularity='component'):
        p = prov(fact)
        if ident in entities:
            entities[ident]['provenance'] = merge_prov(entities[ident]['provenance'], p)
            return ident
        entities[ident] = dict(id=ident, name=ident, type=typ, granularity=granularity, role=role, provenance=p)
        return ident

    def operation(owner, name, fact, http=False):
        assert owner in entities
        key = owner, name
        p = prov(fact, full_header=http)
        if key not in operations:
            operations[key] = dict(entity=owner, name=name, runtime_name=None, provenance=p)
        else:
            operations[key]['provenance'] = merge_prov(operations[key]['provenance'], p)
        return name

    def relation(source, target, typ, channel, fact, source_op=None, target_op=None, messaging=None, context=None):
        p = prov(fact)
        if fact.get('kind') == 'http_call':
            p[0]['locator'] = 'whole-file; callsite ' + p[0]['locator']
        for extra in fact.get('same_class_argument_evidence', []):
            if isinstance(extra, dict) and extra.get('source_path') in source_rows:
                p = merge_prov(p, prov(extra))
        for key in ['field_declaration_evidence', 'queue_constant_evidence']:
            extra = fact.get(key)
            if isinstance(extra, dict) and extra.get('source_path') in source_rows:
                p = merge_prov(p, prov(extra))
        value = dict(source=dict(entity=source, operation=source_op), target=dict(entity=target, operation=target_op),
                     type=typ, channel=channel, messaging=messaging,
                     context=context or fact.get('condition', 'source possibility; runtime not checked'), provenance=p)
        value['id'] = 'tt-' + hashlib.sha256(canon(value).encode()).hexdigest()[:20]
        relations.append(value)

    java = inputs['java']
    for fact in java['entities']:
        kind = fact['entity_kind']
        typ = 'unknown' if kind == 'library_or_build_module' else 'service'
        if fact['id'] == 'ts-gateway-service':
            typ = 'gateway'
        entity(fact['id'], typ, kind + '; source/build inventory, not RCA candidate selection', fact)
        for evidence in fact.get('additional_source_evidence', []):
            evidence = dict(evidence, condition=fact['condition'])
            entities[fact['id']]['provenance'] = merge_prov(entities[fact['id']]['provenance'], prov(evidence))
    method_index = {r['id']: r for r in java['java_methods'] if r.get('scope') == 'current-main-source'}
    # Một số scanner dùng tên scope current-main; scope kiểm lại theo source_path/main và owner.
    method_index.update({r['id']: r for r in java['java_methods'] if '/src/main/' in r['source_path']
                         and not r['source_path'].startswith('old-docs/') and r['owner'] in entities})
    handler_for_method = defaultdict(list)
    for fact in java['operations']:
        if fact.get('kind') != 'http_handler':
            if fact.get('owner') in entities and fact.get('kind') in {'java_service_method', 'java_repository_method'}:
                operation(fact['owner'], 'java:' + fact['id'].split('::', 1)[-1], fact)
            continue
        name = fact['http_method'] + ' ' + fact['path']
        operation(fact['owner'], name, fact, http=True)
        handler_for_method[fact['java_method_id']].append(name)
        catalog.append(dict(entity=fact['owner'], name=name, kind='http_handler',
                            runtime_name_verified=False, source_path=fact['source_path'], line=fact['line']))

    def method_operation(fact):
        mid = fact.get('java_method_id') or fact.get('caller_method_id')
        if mid and mid in method_index:
            method = method_index[mid]
            name = 'java:' + mid.split('::', 1)[-1]
            operation(method['owner'], name, method)
            return name
        # Không bịa operation nếu không xác định được phương thức bao quanh.
        return None

    for fact in java['relations']:
        kind = fact['kind']
        if kind == 'http_call':
            alternatives = fact.get('url_alternatives') or [fact]
            for alternative in alternatives:
                source, target = fact['source_entity'], alternative.get('target_entity')
                if source not in entities or target is None:
                    unresolved.append(dict(kind='http_target_unresolved_alternative', fact=fact, alternative=alternative))
                    continue
                if target not in entities:
                    entity(target, 'unknown', 'literal HTTP endpoint; server implementation/profile OPEN', fact)
                caller = method_operation(fact)
                target_names = [x.split('::', 1)[1] for x in alternative.get('target_handler_candidates', [])
                                if x.startswith(target + '::')]
                exact_descriptor = str(fact.get('http_method')) + ' ' + str(alternative.get('path_template'))
                target_op = (target_names[0] if not alternative.get('dynamic') and
                             len(set(target_names)) == 1 and target_names[0] == exact_descriptor and
                             (target, target_names[0]) in operations else None)
                relation(source, target, 'gọi-đồng-bộ', 'http', fact, caller, target_op,
                         context=fact['condition'] + '; conservative source assignment alternative HTTP ' +
                         str(fact.get('http_method')) + ' ' + str(alternative.get('url_template')))
                if not target_names:
                    unresolved.append(dict(kind='http_no_handler_evidence', fact=fact, alternative=alternative))
                elif target_op is None:
                    unresolved.append(dict(kind='target_handler_candidate_not_verified', fact=fact, alternative=alternative))
            if fact.get('alternative_resolution_open'):
                unresolved.append(dict(kind='http_path_or_branch_resolution_open', fact=fact))
        elif kind in {'messaging_publish', 'messaging_consume'}:
            owner = fact['owner']
            if owner not in entities:
                unresolved.append(dict(kind='messaging_owner_missing', fact=fact))
                continue
            if 'rabbitmq:quickstart' not in entities:
                unresolved.append(dict(kind='broker_profile_chain_missing', fact=fact))
                continue
            name = method_operation(fact)
            # AMQP 2-arg overload không tự xác minh default exchange từ dependency ngoài snapshot.
            address = dict(broker='rabbitmq:quickstart', broker_scope=None, exchange=None,
                           routing_key=fact.get('routing_key'), queue=fact.get('queue'))
            if kind == 'messaging_publish':
                address['queue'] = None
                relation(owner, 'rabbitmq:quickstart', 'thông-điệp', 'publish', fact, name, messaging=address,
                         context=fact['condition'] + '; conditional quickstart broker; namespace/default exchange OPEN')
            else:
                relation('rabbitmq:quickstart', owner, 'thông-điệp', 'consume', fact, target_op=name, messaging=address,
                         context=fact['condition'] + '; conditional quickstart broker; namespace OPEN')

    # Code/default JDBC: logical schema khác instance, env override/profile giữ nguyên trong condition.
    db_by_owner = {}
    for fact in java['config_facts']:
        owner, key, value = fact['owner'], fact['key'], fact['value_expression']
        if owner not in entities:
            continue
        if key == 'spring.datasource.url' and value.startswith('jdbc:mysql://'):
            resolved = re.sub(r'\$\{[^}:]+:([^}]+)\}', lambda m: m[1], value)
            match = re.match(r'jdbc:mysql://([^:/]+):(\d+)/([^?]+)', resolved)
            if match:
                host, port, schema = match.groups()
                db = 'database-default:' + owner + ':' + schema
                inst = 'mysql-default-instance:' + (owner + ':' if host in {'localhost', '127.0.0.1'} else '') + host + ':' + port
                entity(db, 'database', 'logical schema in source JDBC defaults; env override OPEN', fact, 'logical')
                entity(inst, 'database', 'configured endpoint default, not confirmed physical deployment', fact, 'instance')
                db_by_owner[owner] = db
                for typ, resource in [('hosted_on', inst), ('owned_by', owner)]:
                    bindings.append(dict(id=f'{db}:{typ}:{resource}', entity=db, resource=resource,
                                         relation=typ, provenance=prov(fact)))
                relation(owner, db, 'dữ-liệu', 'data', fact,
                         context='source JDBC defaults; ' + value + '; env/profile/runtime override OPEN')
            else:
                unresolved.append(dict(kind='jdbc_default_parse_open', fact=fact))
        elif key == 'spring.cloud.gateway.routes.uri':
            resolved = re.sub(r'\$\{[^}:]+:([^}]+)\}', lambda m: m[1], value)
            target = resolved.removeprefix('lb://')
            if target in entities:
                relation(owner, target, 'gọi-đồng-bộ', 'http', fact,
                         context='declared gateway route; predicate/config condition; runtime not observed')
            else:
                unresolved.append(dict(kind='gateway_route_target_open', fact=fact))

    for fact in java.get('data_calls', []):
        owner = fact['owner']
        caller = method_operation(fact)
        if owner not in db_by_owner:
            unresolved.append(dict(kind='repository_without_resolved_datasource', fact=fact))
            continue
        # Method owner remains application component; DB does not acquire fake operation nodes.
        relation(owner, db_by_owner[owner], 'dữ-liệu', 'data', fact, caller,
                 context='repository call ' + str(fact.get('repository_class')) + '.' + str(fact.get('repository_method')) +
                         '; concrete query/driver/runtime span name OPEN; configured JDBC default only')

    # Worker/async declarations are operations, not invented incoming calls.
    for fact in java.get('background', []):
        if fact.get('owner') in entities and fact.get('kind') not in {'Bean', 'lexical_pattern'}:
            method_operation(fact)
    document.update(entities=list(entities.values()), operations=list(operations.values()), relations=relations,
                    resource_bindings=bindings, signals=signals)
    # De-duplicate exact provenance/records deterministically before pure shared API.
    for key in ['entities', 'operations', 'relations', 'resource_bindings', 'signals']:
        document[key] = [json.loads(k) for k in sorted({canon(x) for x in document[key]})]
    registry_doc = {'version': 1, 'sources': sorted(registry.values(), key=lambda x: x['id'])}
    build_api, _ = pinned_api()
    entity_graph, operation_graph = build_api.build(document, registry_doc)
    for path, value in [('ban-ghi.json', document), ('nguon.json', registry_doc),
                        ('do-thi/thuc-the.json', entity_graph), ('do-thi/thao-tac.json', operation_graph),
                        ('runs/' + run_name + '/unresolved.json', unresolved),
                        ('runs/' + run_name + '/operation-catalog.json', catalog)]:
        save(OUT / path, value)
        if not path.startswith('runs/'):
            save(run / path, value)
    save(run / 'result.json', {'input_hashes': {k: checksum(v) for k, v in paths.items()},
                              'entities': len(entity_graph['inventory']), 'operations': len(operation_graph['nodes']),
                              'relations': len(document['relations']), 'entity_edges': len(entity_graph['edges']),
                              'operation_edges': len(operation_graph['edges']), 'bindings': len(bindings),
                              'signals': len(signals), 'unresolved': len(unresolved),
                              'source_registry_count': len(registry_doc['sources']),
                              'representation_complete': False,
                              'conditional_reference': True})
    print(canon(load(run / 'result.json')))


if __name__ == '__main__':
    if sys.argv[1] == 'assemble':
        assemble(sys.argv[2])
