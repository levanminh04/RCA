"""Tập hai chiều theo miền và mapping có nguồn, không suy runtime từ thiết kế."""
from copy import deepcopy
import json

from .build import (RELATION_TYPES, canonical, fields, message_address, provenance,
                    registry_index, string)


def _trace_shape(graph, level):
    """Đọc graph đã lưu v2.1, không đọc span/labels/dataset hoặc đổi graph."""
    if graph.get('level') != level:
        raise ValueError('level_mismatch')
    fields(graph, ['level', 'nodes', 'edges', 'interval_ns'],
           ['inventory', 'coverage', 'outside_inventory', 'stats', 'belongs_to',
            'component_context', 'messaging_diagnostics'])
    interval = graph['interval_ns']
    if interval is not None and (not isinstance(interval, (tuple, list)) or len(interval) != 2 or
                                 any(type(x) is not int or x < 0 for x in interval) or interval[1] < interval[0]):
        raise ValueError('invalid_interval')
    nodes = {row['id'] for row in graph['nodes']}
    owner = dict(graph.get('belongs_to', []))
    if level == 'operation':
        if nodes != set(owner) or any(row.get('entity') != owner[row['id']] for row in graph['nodes']):
            raise ValueError('belongs_to')
        components = {row['id'] for row in graph.get('component_context', [])}
        if set(owner) & (set(owner.values()) | components):
            raise ValueError('identifier_collision')
        nodes |= components
    for row in graph['edges']:
        fields(row, ['source', 'target', 'type', 'evidence_source', 'destination', 'event_count', 'witness'],
               ['messaging', 'queue_metric_address'])
        if row['source'] not in nodes or row['target'] not in nodes:
            raise ValueError('unknown_trace_endpoint')
        if row['type'] not in RELATION_TYPES or row['evidence_source'] not in {'trace', 'inferred', 'dataset-other'}:
            raise ValueError('trace_relation')
        if type(row['event_count']) is not int or row['event_count'] < 0:
            raise ValueError('event_count')
        if row['type'] == 'thông-điệp' and row.get('messaging') is not None:
            message_address(row['messaging'])
    return owner


def compare(static_graph, trace_graph, mappings, context, registry):
    """Một hệ/mức/miền/cửa sổ. Report orchestration và nhãn ở ngoài API."""
    fields(context, ['system', 'level', 'domain', 'trace_revision', 'revision_link_verified',
                     'revision_provenance'], ['relation_types'])
    if context['level'] not in {'entity', 'operation'} or context['domain'] not in {'synthetic', 'dev-file', 'dev-adapter'}:
        raise ValueError('comparison_domain')
    for key in ['system', 'trace_revision']:
        string(context[key])
    if context['system'] == 'Nezha-OB' and context['domain'] != 'dev-adapter':
        raise ValueError('comparison_domain')
    if type(context['revision_link_verified']) is not bool:
        raise ValueError('revision_verified_type')
    sources = registry_index(registry)
    if context['revision_link_verified']:
        provenance(context['revision_provenance'], sources)
    elif context['revision_provenance']:
        provenance(context['revision_provenance'], sources)
    if (static_graph['scope']['system'] != context['system'] or
            static_graph['level'] != context['level']):
        raise ValueError('scope_mismatch')
    relation_types = context.get('relation_types', sorted(RELATION_TYPES))
    if not isinstance(relation_types, list) or not set(relation_types) <= RELATION_TYPES:
        raise ValueError('relation_types')
    owner = _trace_shape(trace_graph, context['level'])
    static_entities = {r['id'] for r in static_graph['inventory']}
    static_owner = dict(static_graph.get('belongs_to', []))
    static_operations = set(static_owner)
    mapping_index = {}
    if not isinstance(mappings, list):
        raise ValueError('mappings')
    for row in mappings:
        fields(row, ['level', 'original', 'candidates', 'verified', 'provenance'])
        string(row['original'])
        if row['level'] not in {'entity', 'operation'} or type(row['verified']) is not bool:
            raise ValueError('mapping_type')
        provenance(row['provenance'], sources)
        if not isinstance(row['candidates'], list):
            raise ValueError('mapping_candidates')
        for candidate in row['candidates']:
            string(candidate)
            if candidate not in (static_entities if row['level'] == 'entity' else static_operations):
                raise ValueError('mapping_target')
        key = row['level'], row['original']
        if key in mapping_index:
            raise ValueError('duplicate_mapping')
        mapping_index[key] = deepcopy(row)

    def resolve(ident, level):
        row = mapping_index.get((level, ident))
        if row is None:
            return None, 'unmapped'
        candidates = sorted(set(row['candidates']))
        if len(candidates) != 1:
            return None, 'ambiguous_mapping' if candidates else 'unmapped'
        if not row['verified']:
            return None, 'unverified_mapping'
        target = candidates[0]
        if level == 'operation':
            if ident not in owner:
                return None, 'operation_without_owner'
            mapped_owner, reason = resolve(owner[ident], 'entity')
            if reason:
                return None, 'operation_owner_' + reason
            if static_owner[target] != mapped_owner:
                return None, 'operation_owner_conflict'
        return target, None

    def normalized(side, edge, position):
        typ = edge['type']
        if typ not in relation_types:
            return None, 'outside_relation_domain'
        if context['level'] == 'entity' and (typ == 'span-parent' or edge['source'] == edge['target']):
            return None, 'not_entity_dependency'
        converted = {}
        for end in ['source', 'target']:
            original = edge[end]
            if side == 'trace':
                converted[end], reason = resolve(original, 'operation' if original in owner else 'entity')
                if reason:
                    return None, reason + ':' + end
            else:
                converted[end] = original
        if context['level'] == 'entity' and converted['source'] == converted['target']:
            return None, 'mapped_internal_relation'
        address = deepcopy(edge.get('messaging'))
        channel = None
        if typ == 'thông-điệp':
            if address is None:
                return None, 'missing_messaging_address'
            address = message_address(address)
            original_broker = address['broker']
            if side == 'trace':
                if original_broker is None:
                    return None, 'incomplete_messaging_address'
                address['broker'], reason = resolve(original_broker, 'entity')
                if reason:
                    return None, reason + ':broker'
                se, te = owner.get(edge['source'], edge['source']), owner.get(edge['target'], edge['target'])
                channel = 'publish' if te == original_broker else 'consume' if se == original_broker else 'logical-message'
            else:
                channel = edge['channel']
            required = ['broker', 'broker_scope'] + (
                ['exchange', 'routing_key'] if channel == 'publish' else
                ['queue'] if channel == 'consume' else ['exchange', 'routing_key', 'queue'])
            if any(address[k] is None for k in required):
                return None, 'incomplete_messaging_address'
            if channel == 'publish' and address['queue'] is not None:
                return None, 'invalid_publish_queue'
            # Khóa so theo vai trò; địa chỉ đầy đủ vẫn ở graph và members gốc.
            address = {key: address[key] for key in required}
        # Type bỏ riêng cho phép so endpoints; provenance luôn ở member riêng.
        return dict(source=converted['source'], target=converted['target'], type=typ,
                    address=[channel, address] if address is not None else None,
                    position=position), None

    prepared = {'static': [], 'trace': []}
    common_exclusions = {'static': [], 'trace': []}
    for side, graph in [('static', static_graph), ('trace', trace_graph)]:
        for position, edge in enumerate(graph['edges']):
            normalized_row, reason = normalized(side, edge, position)
            if reason:
                common_exclusions[side].append(dict(index=position, reason=reason,
                                                     original=deepcopy(edge)))
            else:
                prepared[side].append(normalized_row)
    views = {}
    for view in ['endpoints', 'typed']:
        sets = {'static': {}, 'trace': {}}
        exclusions = deepcopy(common_exclusions)
        for side in ['static', 'trace']:
            graph = static_graph if side == 'static' else trace_graph
            for row in prepared[side]:
                original = graph['edges'][row['position']]
                if view == 'typed' and row['type'] == 'gọi-chưa-phân-kiểu':
                    exclusions[side].append(dict(index=row['position'], reason='unknown_type',
                                                 original=deepcopy(original)))
                    continue
                key = canonical([row['source'], row['target'],
                                 row['type'] if view == 'typed' else None, row['address']])
                sets[side].setdefault(key, []).append(dict(index=row['position'], original=deepcopy(original)))
        s, t = set(sets['static']), set(sets['trace'])
        intersection = s & t
        groups = dict(S=s, T=t, intersection=intersection, static_only=s-t, trace_only=t-s)
        views[view] = {key: [json.loads(k) for k in sorted(values)] for key, values in groups.items()}
        views[view].update(
            numerator=len(intersection), static_denominator=len(s), trace_denominator=len(t),
            static_fraction=len(intersection)/len(s) if s else None,
            trace_fraction=len(intersection)/len(t) if t else None,
            members={side: [dict(key=json.loads(k), members=sets[side][k]) for k in sorted(sets[side])]
                     for side in ['static', 'trace']}, exclusions=exclusions)
    node_mapping = []
    for node in trace_graph['nodes'] + trace_graph.get('component_context', []):
        level = 'operation' if node['id'] in owner else 'entity'
        mapped, reason = resolve(node['id'], level)
        node_mapping.append(dict(original=deepcopy(node), level=level, canonical_id=mapped,
                                 status=reason or 'mapped'))
    # Không sửa trace/static hay coi revision ứng viên là deployment đã xác minh.
    return dict(schema_version=1, context=deepcopy(context),
                static_scope=deepcopy(static_graph['scope']), interval_ns=deepcopy(trace_graph['interval_ns']),
                conditional_reference=not context['revision_link_verified'],
                interpretation='structural_agreement; not runtime ground truth or RCA benefit',
                views=views, mappings=sorted(deepcopy(mappings), key=canonical),
                nodes=dict(static=deepcopy(static_graph['nodes']),
                           trace=sorted(node_mapping, key=canonical),
                           static_inventory=deepcopy(static_graph['inventory'])),
                competing_explanations=['revision', 'alias', 'domain/window', 'branch_not_executed',
                                       'incomplete_static_source', 'missing_telemetry', 'conversion_error'])
