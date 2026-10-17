"""Đầu vào và đáp án literal, ghi trước mã build/compare. Không import mã đang kiểm."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).parent


def write(name, value):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')


def prov(source, locator):
    return [{'source_id': source, 'locator': locator, 'condition': 'ví dụ tổng hợp theo nhu cầu nguồn; chưa runtime'}]


def entity(ident, typ='service', granularity='component'):
    return dict(id=ident, name=ident, type=typ, granularity=granularity,
                role='fixture', provenance=prov('B12', '§2'))


def op(owner, name):
    return dict(entity=owner, name=name, runtime_name=None, provenance=prov('B16', '§5'))


def rel(ident, s, t, typ, channel, msg=None, context=''):
    return dict(id=ident, source=dict(entity=s[0], operation=s[1]),
                target=dict(entity=t[0], operation=t[1]), type=typ, channel=channel,
                messaging=msg, context=context or 'fixture', provenance=prov('B13', '§5'))


def main():
    entities = [entity('A'), entity('B'), entity('C'), entity('unused'),
                entity('DB1', 'database', 'logical'), entity('DB2', 'database', 'logical'),
                entity('PG', 'database', 'instance'), entity('R', 'broker'),
                entity('X', 'external'), entity('H', 'host')]
    operations = [op('A', 'send'), op('A', 'callback'), op('A', 'scheduler'),
                  op('A', 'outbox'), op('B', 'receive'), op('C', 'receive')]
    publish = dict(broker='R', broker_scope='vhost-demo', exchange='e', routing_key='k', queue=None)
    q1 = dict(broker='R', broker_scope='vhost-demo', exchange=None, routing_key=None, queue='q1')
    q2 = dict(q1, queue='q2')
    doc = dict(scope=dict(system='synthetic', revision='design-v1'), entities=entities,
               operations=operations, relations=[
                   rel('http', ('A', 'send'), ('B', 'receive'), 'gọi-đồng-bộ', 'http'),
                   rel('http-second-source', ('A', 'send'), ('B', 'receive'), 'gọi-đồng-bộ', 'http'),
                   rel('data', ('A', 'outbox'), ('DB1', None), 'dữ-liệu', 'data'),
                   rel('entity-only', ('B', None), ('DB2', None), 'dữ-liệu', 'data'),
                   rel('publish', ('A', 'send'), ('R', None), 'thông-điệp', 'publish', publish),
                   rel('republish', ('A', 'send'), ('R', None), 'thông-điệp', 'publish', publish, 'retry cùng logical message; không count'),
                   rel('consume-q1', ('R', None), ('B', 'receive'), 'thông-điệp', 'consume', q1),
                   rel('consume-q2', ('R', None), ('B', 'receive'), 'thông-điệp', 'consume', q2),
                   rel('fanout', ('R', None), ('C', 'receive'), 'thông-điệp', 'consume', dict(q1, queue='q3')),
                   rel('callback-out', ('A', 'send'), ('X', None), 'gọi-đồng-bộ', 'http'),
                   rel('internal', ('A', 'scheduler'), ('A', 'outbox'), 'gọi-chưa-phân-kiểu', 'internal'),
                   rel('span-parent', ('A', 'send'), ('B', 'receive'), 'span-parent', 'span-parent'),
                   rel('saga-compensate', ('A', None), ('B', None), 'gọi-đồng-bộ', 'rpc', context='bù trừ; giữ chiều A→B'),
               ], resource_bindings=[
                   dict(id='own1', entity='DB1', resource='A', relation='owned_by', provenance=prov('B12', '§2')),
                   dict(id='own2', entity='DB2', resource='B', relation='owned_by', provenance=prov('B12', '§2')),
                   dict(id='share1', entity='DB1', resource='PG', relation='hosted_on', provenance=prov('B12', '§2')),
                   dict(id='share2', entity='DB2', resource='PG', relation='hosted_on', provenance=prov('B12', '§2')),
                   dict(id='placement', entity='PG', resource='H', relation='hosted_on', provenance=prov('B11', '§6')),
               ], signals=[
                   dict(id='metric-shared', kind='metric', entity='PG', operation=None,
                        address=['instance', 'PG'], shared=True, provenance=prov('B16', '§5/7')),
                   dict(id='metric-queue', kind='metric', entity='R', operation=None,
                        address=['R', 'vhost-demo', 'q1'], shared=True, provenance=prov('B16', '§5')),
                   dict(id='log-callback', kind='log', entity='A', operation='callback',
                        address=['serviceName', 'traceId', 'spanId'], shared=False, provenance=prov('B16', '§3/4')),
               ])
    write('input.json', doc)
    write('expected.json', {
        'entity_ids': ['A', 'B', 'C', 'DB1', 'DB2', 'H', 'PG', 'R', 'X', 'unused'],
        'entity_edges': [
            ['A', 'B', 'gọi-đồng-bộ', 'http', None],
            ['A', 'B', 'gọi-đồng-bộ', 'rpc', None],
            ['A', 'DB1', 'dữ-liệu', 'data', None],
            ['A', 'R', 'thông-điệp', 'publish', publish],
            ['A', 'X', 'gọi-đồng-bộ', 'http', None],
            ['B', 'DB2', 'dữ-liệu', 'data', None],
            ['R', 'B', 'thông-điệp', 'consume', q1],
            ['R', 'B', 'thông-điệp', 'consume', q2],
            ['R', 'C', 'thông-điệp', 'consume', dict(q1, queue='q3')],
        ],
        'operation_exclusions': ['entity-only', 'saga-compensate'],
        'no_incoming_operations': ['["A","callback"]', '["A","scheduler"]'],
        'projected_entity_record_ids': ['callback-out', 'consume-q1', 'consume-q2', 'data', 'fanout',
                                        'http', 'http-second-source', 'publish', 'republish'],
        'bindings_count': 5, 'single_shared_resource': 'PG',
        'comparisons': {
            'typed_unknown': {'S': [['A', 'B', 'gọi-đồng-bộ', None]], 'T': [], 'intersection': [],
                              'static_only': [['A', 'B', 'gọi-đồng-bộ', None]], 'trace_only': [],
                              'numerator': 0, 'static_denominator': 1, 'trace_denominator': 0},
            'endpoints_unknown': {'S': [['A', 'B', None, None]], 'T': [['A', 'B', None, None]],
                                  'intersection': [['A', 'B', None, None]], 'static_only': [], 'trace_only': [],
                                  'numerator': 1, 'static_denominator': 1, 'trace_denominator': 1},
            'typed_wrong': {'S': [['A', 'B', 'gọi-đồng-bộ', None]], 'T': [['A', 'B', 'dữ-liệu', None]],
                            'intersection': [], 'static_only': [['A', 'B', 'gọi-đồng-bộ', None]],
                            'trace_only': [['A', 'B', 'dữ-liệu', None]], 'numerator': 0,
                            'static_denominator': 1, 'trace_denominator': 1},
            'empty': {'S': [], 'T': [], 'intersection': [], 'static_only': [], 'trace_only': [],
                      'numerator': 0, 'static_denominator': 0, 'trace_denominator': 0},
        },
        'negative_build': {
            'unknown_field': 'unknown_fields', 'missing_provenance': 'provenance',
            'conflicting_entity': 'duplicate_conflict', 'missing_operation': 'unknown_operation',
            'bad_broker': 'messaging_endpoint', 'shared_operation_metric': 'shared_signal_operation',
            'label': 'unknown_fields', 'collision': 'identifier_collision'},
        'comparison_requirements': ['ambiguous_alias_excluded', 'unverified_alias_excluded',
                                    'missing_alias_excluded', 'missing_queue_excluded',
                                    'two_queues_retained', 'republish_not_event_count',
                                    'revision_unverified_conditional', 'operation_owner_consistent',
                                    'span_parent_not_entity_dependency', 'scope_mismatch_rejected',
                                    'input_unchanged', 'deterministic_reorder'],
    })
    write('oracle-before-code.json', {'definition': 'define.py không import builder/comparator',
          'implementation_exists': any(Path('src/do_thi_tinh', p).exists() for p in ['build.py', 'compare.py']),
          'sha256': {p: hashlib.sha256((OUT / p).read_bytes()).hexdigest()
                     for p in ['define.py', 'input.json', 'expected.json']}})


if __name__ == '__main__':
    main()
