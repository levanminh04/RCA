"""Bản ghi có nguồn → graph tĩnh. Hợp đồng: results/T-036/hop-dong.md."""
from copy import deepcopy
import json
import re

ENTITY_TYPES = {'service', 'gateway', 'database', 'cache', 'broker', 'identity-provider',
                'external', 'host', 'unknown'}
RELATION_TYPES = {'gọi-đồng-bộ', 'gọi-chưa-phân-kiểu', 'dữ-liệu', 'thông-điệp',
                  'triển-khai', 'span-parent'}
CHANNELS = {'http', 'rpc', 'smtp', 'data', 'publish', 'consume', 'logical-message',
            'deployment', 'internal', 'span-parent'}
MESSAGE_FIELDS = {'broker', 'broker_scope', 'exchange', 'routing_key', 'queue'}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def fields(row, required, optional=()):
    if not isinstance(row, dict):
        raise ValueError('record_type')
    if set(row) - set(required) - set(optional):
        raise ValueError('unknown_fields:' + ','.join(sorted(set(row) - set(required) - set(optional))))
    if set(required) - set(row):
        raise ValueError('missing_fields:' + ','.join(sorted(set(required) - set(row))))


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('nonempty_string')
    return value


def registry_index(registry):
    if not isinstance(registry, dict) or not isinstance(registry.get('sources'), list):
        raise ValueError('registry')
    result = {}
    for source in registry['sources']:
        for key in ['id', 'kind', 'revision', 'sha256', 'condition']:
            string(source.get(key))
        if not re.fullmatch('[0-9a-f]{64}', source['sha256']):
            raise ValueError('source_sha256')
        if source['id'] in result:
            raise ValueError('duplicate_source')
        result[source['id']] = source
    return result


def provenance(rows, sources):
    if not isinstance(rows, list) or not rows:
        raise ValueError('provenance')
    out = {}
    for row in rows:
        fields(row, ['source_id', 'locator', 'condition'])
        for value in row.values():
            string(value)
        if row['source_id'] not in sources:
            raise ValueError('unknown_source')
        out[canonical(row)] = deepcopy(row)
    return [out[k] for k in sorted(out)]


def operation_id(entity, operation):
    return json.dumps([entity, operation], ensure_ascii=False, separators=(',', ':'))


def unique_rows(rows, key):
    if not isinstance(rows, list):
        raise ValueError('record_list')
    out = {}
    for row in rows:
        ident = key(row)
        if ident in out and canonical(out[ident]) != canonical(row):
            raise ValueError('duplicate_conflict:' + str(ident))
        out[ident] = deepcopy(row)
    return [out[k] for k in sorted(out)]


def edge_signature(edge):
    return [edge['source'], edge['target'], edge['type'], edge['channel'], edge.get('messaging')]


def message_address(value):
    if value is None:
        return None
    fields(value, MESSAGE_FIELDS)
    for key, item in value.items():
        if item is not None and (not isinstance(item, str) or
                                  (not item and key not in {'exchange', 'routing_key'})):
            raise ValueError('messaging_attribute_type')
    return deepcopy(value)


def build(document, registry):
    """Không suy quan hệ; nguồn do người đọc lập. Không đọc đường dẫn/nhãn."""
    fields(document, ['scope', 'entities', 'operations', 'relations', 'resource_bindings', 'signals'])
    fields(document['scope'], ['system', 'revision'])
    for value in document['scope'].values():
        string(value)
    sources = registry_index(registry)
    doc = deepcopy(document)
    for collection in ['entities', 'operations', 'relations', 'resource_bindings', 'signals']:
        if not isinstance(doc[collection], list):
            raise ValueError('record_list')
        for row in doc[collection]:
            if not isinstance(row, dict):
                raise ValueError('record_type')
            row['provenance'] = provenance(row.get('provenance'), sources)
    entities = unique_rows(doc['entities'], lambda r: string(r['id']))
    index = {}
    for row in entities:
        fields(row, ['id', 'name', 'type', 'granularity', 'role', 'provenance'])
        for key in ['id', 'name', 'role']:
            string(row[key])
        if row['type'] not in ENTITY_TYPES or row['granularity'] not in {'logical', 'instance', 'component'}:
            raise ValueError('entity_type')
        index[row['id']] = row
    operations = unique_rows(doc['operations'], lambda r: operation_id(r['entity'], r['name']))
    op_index = {}
    for row in operations:
        fields(row, ['entity', 'name', 'runtime_name', 'provenance'])
        string(row['name'])
        if row['entity'] not in index:
            raise ValueError('unknown_entity')
        if row['runtime_name'] is not None:
            string(row['runtime_name'])
        ident = operation_id(row['entity'], row['name'])
        if ident in index:
            raise ValueError('identifier_collision')
        op_index[ident] = dict(row, id=ident)

    def endpoint(row):
        fields(row, ['entity', 'operation'])
        if row['entity'] not in index:
            raise ValueError('unknown_entity')
        if row['operation'] is not None:
            string(row['operation'])
            if operation_id(row['entity'], row['operation']) not in op_index:
                raise ValueError('unknown_operation')
        return operation_id(row['entity'], row['operation']) if row['operation'] is not None else row['entity']

    relations = unique_rows(doc['relations'], lambda r: string(r['id']))
    ent_edges, op_edges, exclusions = {}, {}, []
    context_ids = set()

    def add(target, edge, record):
        key = canonical(edge_signature(edge))
        if key not in target:
            target[key] = dict(edge, record_ids=[], provenance=[], contexts=[])
        row = target[key]
        row['record_ids'] = sorted(set(row['record_ids'] + [record['id']]))
        row['provenance'] = provenance(row['provenance'] + record['provenance'], sources)
        row['contexts'] = sorted(set(row['contexts'] + [record['context']]))

    for row in relations:
        fields(row, ['id', 'source', 'target', 'type', 'channel', 'messaging', 'context', 'provenance'])
        string(row['context'])
        s, t = endpoint(row['source']), endpoint(row['target'])
        se, te = row['source']['entity'], row['target']['entity']
        typ, channel = row['type'], row['channel']
        if typ not in RELATION_TYPES or channel not in CHANNELS:
            raise ValueError('relation_type')
        if (typ == 'thông-điệp') != (channel in {'publish', 'consume', 'logical-message'}):
            raise ValueError('relation_channel')
        if ((typ == 'dữ-liệu' and channel != 'data') or
                (typ == 'triển-khai' and channel != 'deployment') or
                (typ == 'span-parent' and channel != 'span-parent') or
                (typ in {'gọi-đồng-bộ', 'gọi-chưa-phân-kiểu'} and channel not in {'http', 'rpc', 'smtp', 'internal'})):
            raise ValueError('relation_channel')
        msg = message_address(row['messaging'])
        if typ == 'thông-điệp':
            if msg is None or msg['broker'] not in index or index[msg['broker']]['type'] != 'broker':
                raise ValueError('messaging_endpoint')
            if ((channel == 'publish' and (te != msg['broker'] or msg['queue'] is not None)) or
                    (channel == 'consume' and se != msg['broker'])):
                raise ValueError('messaging_endpoint')
        elif msg is not None:
            raise ValueError('unexpected_messaging')
        if typ == 'dữ-liệu' and index[te]['type'] not in {'database', 'cache'}:
            raise ValueError('data_endpoint')
        if typ == 'triển-khai' and index[te]['type'] != 'host':
            raise ValueError('deployment_endpoint')
        edge = dict(source=s, target=t, type=typ, channel=channel, messaging=msg,
                    evidence_source='static', destination=None)
        if msg is not None:
            q = [msg[k] for k in ['broker', 'broker_scope', 'queue']]
            edge['queue_metric_address'] = q if all(q) else None
        if se != te and typ != 'span-parent':
            add(ent_edges, dict(edge, source=se, target=te), row)
        if s in op_index or t in op_index:
            add(op_edges, edge, row)
            context_ids.update(x for x in [s, t] if x not in op_index)
        else:
            exclusions.append(dict(record_id=row['id'], reason='no_operation_evidence'))
    bindings = unique_rows(doc['resource_bindings'], lambda r: string(r['id']))
    for row in bindings:
        fields(row, ['id', 'entity', 'resource', 'relation', 'provenance'])
        if row['entity'] not in index or row['resource'] not in index:
            raise ValueError('unknown_resource')
        if row['relation'] not in {'hosted_on', 'owned_by'} or row['entity'] == row['resource']:
            raise ValueError('resource_relation')
        if row['relation'] == 'hosted_on' and index[row['resource']]['granularity'] != 'instance' and index[row['resource']]['type'] != 'host':
            raise ValueError('resource_target')
    signals = unique_rows(doc['signals'], lambda r: string(r['id']))
    for row in signals:
        fields(row, ['id', 'kind', 'entity', 'operation', 'address', 'shared', 'provenance'])
        endpoint(dict(entity=row['entity'], operation=row['operation']))
        if row['kind'] not in {'log', 'trace', 'metric'} or not isinstance(row['shared'], bool):
            raise ValueError('signal_type')
        if not isinstance(row['address'], list) or not row['address']:
            raise ValueError('signal_address')
        for part in row['address']:
            string(part)
        if row['shared'] and row['operation'] is not None:
            raise ValueError('shared_signal_operation')
    evidence = dict(representation='supported', runtime='not_checked', rca_benefit='not_checked',
                    source_evidence=sorted({sources[p['source_id']]['kind']
                                            for col in [entities, operations, relations, bindings, signals]
                                            for row in col for p in row['provenance']}))
    common = dict(schema_version=1, scope=doc['scope'], evidence=evidence,
                  resource_bindings=bindings, signals=signals, records=relations)
    entity = dict(deepcopy(common), level='entity', nodes=entities, inventory=entities,
                  observed_nodes=[], edges=[ent_edges[k] for k in sorted(ent_edges)])
    operation = dict(deepcopy(common), level='operation',
                     inventory=entities,
                     nodes=[op_index[k] for k in sorted(op_index)],
                     belongs_to=[[k, op_index[k]['entity']] for k in sorted(op_index)],
                     component_context=[index[k] for k in sorted(context_ids)],
                     edges=[op_edges[k] for k in sorted(op_edges)], operation_exclusions=exclusions)
    return entity, operation


def project(operation):
    """Chiếu phần có bằng chứng operation; không bổ sung cạnh entity-only."""
    if operation['level'] != 'operation':
        raise ValueError('level')
    owner = dict(operation['belongs_to'])
    nodes = set(owner.values()) | {n['id'] for n in operation['component_context']}
    if set(owner) & nodes:
        raise ValueError('identifier_collision')
    edges = {}
    for row in operation['edges']:
        s, t = owner.get(row['source'], row['source']), owner.get(row['target'], row['target'])
        if s == t or row['type'] == 'span-parent':
            continue
        e = deepcopy(dict(row, source=s, target=t))
        key = canonical(edge_signature(e))
        if key not in edges:
            edges[key] = e
        else:
            for field in ['record_ids', 'contexts']:
                edges[key][field] = sorted(set(edges[key][field] + e[field]))
            edges[key]['provenance'] = [json.loads(k) for k in sorted(
                {canonical(p) for p in edges[key]['provenance'] + e['provenance']})]
    return dict(nodes=sorted(nodes), edges=[edges[k] for k in sorted(edges)])
