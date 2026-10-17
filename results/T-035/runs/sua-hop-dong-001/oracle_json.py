"""Literal contract oracle authored before the four-fix implementation.

No builder helper produces an expected answer. Run with -B. An output directory
is create-only so failures, old builders and later successful runs are retained.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MAX = 2**63 - 1
MAX_US = MAX // 1000
BASE = dict(traceID='t', spanID='s', parentSpanID='', serviceName='A',
            operationName='run', startTime=2, duration=1)
DATA = 'dữ-liệu'
SYNC = 'gọi-đồng-bộ'
MESSAGE = 'thông-điệp'
DEPLOY = 'triển-khai'


def oid(entity, operation):
    # Public ID syntax specified by the contract, not an imported helper.
    return json.dumps([entity, operation], ensure_ascii=False, separators=(',', ':'))


def edge(source, target, typ, witness, messaging=None):
    value = dict(source=source, target=target, type=typ, evidence_source='trace',
                 event_count=1, witness=witness, destination=None)
    if messaging is not None:
        value['messaging'] = messaging
        value['queue_metric_address'] = None
    return value


def sort_json(items):
    return sorted(items, key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True))


def expected_ok(types=None, operations=None, entity_edges=None, operation_edges=None,
                context=None, stats=None, times=None, vocabulary=None,
                projected_edges=None):
    types = {'A': 'service'} if types is None else types
    operations = [('A', 'run')] if operations is None else operations
    entity_edges = [] if entity_edges is None else entity_edges
    operation_edges = [] if operation_edges is None else operation_edges
    context = {} if context is None else context
    answer = {
        'entity_nodes': sort_json([dict(id=k, type=v, source='trace') for k, v in types.items()]),
        'entity_edges': sort_json(entity_edges),
        'operation_nodes': sort_json([dict(id=oid(e, o), entity=e, operation=o, source='trace') for e, o in operations]),
        'operation_edges': sort_json(operation_edges),
        'belongs_to': sort_json([[oid(e, o), e] for e, o in operations]),
        'component_context': sort_json([dict(id=k, type=v, source='trace') for k, v in context.items()]),
        'projected_nodes': sorted(types),
        'projected_edges': sort_json([] if projected_edges is None else projected_edges),
    }
    if stats is not None:
        answer['stats'] = stats
    if times is not None:
        answer['times'] = times
    if vocabulary is not None:
        answer['vocabulary'] = vocabulary
    return answer


def vocab(entries):
    return {'operations': sort_json([
        dict(id=oid(e, o), entity=e, operation=o, span_count=n,
             child_signature_count=1, child_signatures=[[]],
             max_internal_depth=0, cross_entity_child_events=0)
        for e, o, n in entries]), 'internal_span_cycle_count': 0}


def fixture_cases():
    cases = []

    def add(name, rows=None, expected=None, *, dtype=None, aliases=None,
            universe=None, error=None, interval=None, action='build', operation=None):
        cases.append(dict(name=name, rows=[dict(BASE)] if rows is None else rows,
                          expected={'error': error} if error else expected,
                          dtype=dtype or {}, aliases=aliases or {},
                          universe={'A': 'service'} if universe is None else universe,
                          interval=interval, action=action, operation=operation))

    # Missing operations must share the public null key. Literal vocabulary is
    # declared here; it is never read from builder output.
    for label, values, dtype in [
        ('none_object', [None], 'object'),
        ('nan_float', [float('nan')], 'float64'),
        ('nan_object', [float('nan')], 'object'),
        ('pdna_object', [pd.NA], 'object'),
        ('pdna_string', [pd.NA], 'string'),
        ('mixed_none_nan_pdna_object', [None, float('nan'), pd.NA], 'object'),
        ('mixed_named_missing_object', ['run', None, float('nan'), pd.NA], 'object'),
        ('mixed_named_missing_string', ['run', pd.NA, None], 'string'),
        ('none_inferred', [None], None),
    ]:
        rows = [dict(BASE, spanID='s'+str(i), operationName=value) for i, value in enumerate(values)]
        named = label.startswith('mixed_named')
        entries = [('A', 'run', 1), ('A', None, len(values)-1)] if named else [('A', None, len(values))]
        add('missing_'+label, rows, expected_ok(
            operations=[(e, o) for e, o, _ in entries],
            stats=dict(raw_spans=len(rows), unique_spans=len(rows), duplicate_rows=0,
                       missing_operation=len(rows)-int(named)),
            vocabulary=vocab(entries)), dtype={'operationName': dtype} if dtype else {})
    for label, values in [('none_duplicate',[None,None]),
                          ('nan_duplicate',[float('nan'),float('nan')]),
                          ('mixed_missing_duplicate',[None,float('nan'),pd.NA])]:
        rows = [dict(BASE, operationName=value) for value in values]
        add('missing_'+label, rows, expected_ok(operations=[('A',None)],
            stats=dict(raw_spans=len(rows),unique_spans=1,duplicate_rows=len(rows)-1,missing_operation=1),
            vocabulary=vocab([('A',None,1)])), dtype={'operationName':'object'})
    add('missing_null_key_different_entities',
        [dict(BASE,spanID='a',operationName=None),dict(BASE,spanID='b',serviceName='B',operationName=pd.NA)],
        expected_ok(types={'A':'service','B':'service'},operations=[('A',None),('B',None)],
                    stats={'missing_operation':2}, vocabulary=vocab([('A',None,1),('B',None,1)])),
        dtype={'operationName':'object'},universe={'A':'service','B':'service'})
    add('missing_control_null_string_and_empty_string',
        [dict(BASE,spanID='null',operationName='null'),
         dict(BASE,spanID='empty',operationName=''),
         dict(BASE,spanID='none',operationName=None)],
        expected_ok(operations=[('A','null'),('A',''),('A',None)],
                    stats={'missing_operation':1},
                    vocabulary=vocab([('A','null',1),('A','',1),('A',None,1)])),
        dtype={'operationName':'object'})
    add('missing_control_duplicate_named_conflict',
        [dict(BASE,operationName=None),dict(BASE,operationName='run')],
        error='duplicate_conflict',dtype={'operationName':'object'})

    # The two ID domains may use arbitrary strings individually. Their actual
    # intersection must be rejected instead of guessing endpoint ownership.
    endpoints = [
        ('database',{'db.entity':'DB','db.type':'database'},None,'database',DATA,False),
        ('cache',{'db.entity':'DB','db.type':'cache'},None,'cache',DATA,False),
        ('peer',{'peer.entity':'DB','peer.type':'external'},'CLIENT','external',SYNC,False),
        ('broker_producer',{'messaging.broker':'DB'},'PRODUCER','broker',MESSAGE,False),
        ('broker_consumer',{'messaging.broker':'DB'},'CONSUMER','broker',MESSAGE,True),
        ('host',{'host.id':'DB','host.identity_verified':True},None,'host',DEPLOY,False),
    ]
    for name, attrs, kind, typ, relation, reverse in endpoints:
        address = {'broker':'DB','broker_scope':None,'exchange':None,'routing_key':None,'queue':None} if relation==MESSAGE else None
        source,target = ('DB','A') if reverse else ('A','DB')
        osource,otarget = ('DB',oid('A','run')) if reverse else (oid('A','run'),'DB')
        ee = edge(source,target,relation,[['t','s']],address)
        oe = edge(osource,otarget,relation,[['t','s']],address)
        projected = [source,target,relation,'trace',None]
        if address is not None:
            projected.append(json.dumps(address,ensure_ascii=False,sort_keys=True,separators=(',',':')))
        add('identifier_control_'+name,
            [dict(BASE,attributes=attrs,kind=kind)],
            expected_ok(types={'A':'service','DB':typ},context={'DB':typ},
                        entity_edges=[ee],operation_edges=[oe],projected_edges=[projected]))
        for collision_name, target in [('own',oid('A','run')),('other',oid('B','read'))]:
            changed={k:(target if k in ('db.entity','peer.entity','messaging.broker','host.id') else v) for k,v in attrs.items()}
            rows=[dict(BASE,attributes=changed,kind=kind),dict(BASE,spanID='b',serviceName='B',operationName='read')]
            add('identifier_'+name+'_'+collision_name,rows,error='identifier_collision',universe={'A':'service','B':'service'})
    for name, aliases, service in [
        ('service',{},oid('A','run')),
        ('alias',{'raw-alias':oid('A','run')},'raw-alias'),
    ]:
        add('identifier_'+name,
            [dict(BASE),dict(BASE,spanID='b',serviceName=service,operationName='other')],
            aliases=aliases,universe={'A':'service'},error='identifier_collision')
    strange='["B","read"]'
    add('identifier_control_json_entity_name',
        [dict(BASE,serviceName=strange,operationName='different')],
        expected_ok(types={strange:'service'},operations=[(strange,'different')]),universe={strange:'service'})
    add('identifier_reserved_operation_outside_window',
        [dict(BASE,attributes={'db.entity':oid('B','read'),'db.type':'database'}),
         dict(BASE,spanID='b',serviceName='B',operationName='read',startTime=20,duration=1)],
        interval=(0,10000),universe={'A':'service','B':'service'},error='identifier_collision')
    add('identifier_inventory_only_not_observed',expected=expected_ok(),
        universe={'A':'service',oid('A','run'):'database'})
    for name,target in [('own',oid('A','run')),('other',oid('B','read'))]:
        op=dict(nodes=[dict(id=oid('A','run'),entity='A',operation='run',source='trace'),
                       dict(id=oid('B','read'),entity='B',operation='read',source='trace')],
                belongs_to=[[oid('A','run'),'A'],[oid('B','read'),'B']],
                component_context=[dict(id=target,type='database',source='trace')],
                edges=[edge(oid('A','run'),target,DATA,[['t','s']])])
        add('project_identifier_endpoint_'+name,action='project',operation=op,error='identifier_collision')
    op=dict(nodes=[dict(id=oid('A','run'),entity='A',operation='run',source='trace'),
                   dict(id=oid('B','read'),entity=oid('A','run'),operation='read',source='trace')],
            belongs_to=[[oid('A','run'),'A'],[oid('B','read'),oid('A','run')]],component_context=[],edges=[])
    add('project_identifier_service',action='project',operation=op,error='identifier_collision')
    op=dict(nodes=[dict(id=oid('A','run'),entity='A',operation='run',source='trace')],
            belongs_to=[[oid('A','run'),'A']],
            component_context=[dict(id='DB',type='database',source='trace')],
            edges=[edge(oid('A','run'),'DB',DATA,[['t','s']])])
    add('project_identifier_control',action='project',operation=op,
        expected={'projected_nodes':['A','DB'],'projected_edges':[['A','DB',DATA,'trace',None]]})

    # Numeric domain cases declare exact expected ns separately from the input.
    for name, changes, dtype in [
        ('start_negative',{'startTime':-2},{}),
        ('duration_negative',{'duration':-1},{}),
        ('start_ns_negative',{'_start_ns':-2,'_end_ns':1},{}),
        ('end_ns_negative',{'_start_ns':0,'_end_ns':-1},{}),
        ('both_ns_negative',{'_start_ns':-2,'_end_ns':-1},{}),
        ('ns_end_before_start',{'_start_ns':2,'_end_ns':1},{}),
        ('us_multiply_overflow',{'startTime':MAX_US+1},{}),
        ('us_add_representable_but_ns_overflow',{'startTime':MAX_US,'duration':1},{}),
        ('us_duration_multiply_overflow',{'startTime':0,'duration':MAX_US+1},{}),
        ('us_add_int64_overflow',{'startTime':MAX,'duration':1},{}),
        ('us_add_both_max',{'startTime':MAX,'duration':MAX},{}),
        ('start_int64_plus_one_object',{'startTime':MAX+1},{'startTime':'object'}),
        ('start_int64_plus_one_string',{'startTime':str(MAX+1)},{}),
        ('start_uint64_max',{'startTime':2**64-1},{'startTime':'uint64'}),
        ('duration_uint64_max',{'duration':2**64-1},{'duration':'uint64'}),
        ('ns_uint64_overflow',{'_start_ns':MAX+1,'_end_ns':MAX+1},{'_start_ns':'uint64','_end_ns':'uint64'}),
        ('ns_large_string',{'_start_ns':str(MAX+1),'_end_ns':str(MAX+1)},{}),
        ('ns_large_object',{'_start_ns':MAX+1,'_end_ns':MAX+1},{'_start_ns':'object','_end_ns':'object'}),
    ]:
        add('time_'+name,[dict(BASE,**changes)],dtype=dtype,error='invalid_time')
    for column in ['startTime','duration','_start_ns','_end_ns']:
        for label,value in [('fraction',1.5),('nan',float('nan')),('positive_inf',float('inf')),
                            ('negative_inf',-float('inf')),('none',None),('pdna',pd.NA),
                            ('bad_string','not-a-time')]:
            changes={'_start_ns':2,'_end_ns':3} if column.startswith('_') else {}
            changes[column]=value
            add('time_'+column+'_'+label,[dict(BASE,**changes)],error='invalid_time')
        for label,value,dtype in [('int64_plus_one_object',MAX+1,'object'),
                                 ('int64_plus_one_string',str(MAX+1),'object'),
                                 ('uint64_max',2**64-1,'uint64')]:
            changes={'_start_ns':2,'_end_ns':3} if column.startswith('_') else {}
            changes[column]=value
            add('time_domain_'+column+'_'+label,[dict(BASE,**changes)],
                dtype={column:dtype},error='invalid_time')
    valid_times=[
        ('zero',{'startTime':0,'duration':0},{},[0],[0]),
        ('max_safe_us',{'startTime':MAX_US,'duration':0},{},[MAX_US*1000],[MAX_US*1000]),
        ('max_safe_sum_us',{'startTime':MAX_US-1,'duration':1},{},[(MAX_US-1)*1000],[MAX_US*1000]),
        ('integer_strings',{'startTime':'2','duration':'1'},{},[2000],[3000]),
        ('integer_object',{'startTime':2,'duration':1},{'startTime':'object','duration':'object'},[2000],[3000]),
        ('uint64_safe',{'startTime':2,'duration':1},{'startTime':'uint64','duration':'uint64'},[2000],[3000]),
        ('ns_max',{'startTime':0,'duration':0,'_start_ns':MAX,'_end_ns':MAX},{},[MAX],[MAX]),
        ('ns_zero',{'startTime':0,'duration':0,'_start_ns':0,'_end_ns':0},{},[0],[0]),
        ('ns_precedence',{'startTime':20,'duration':10,'_start_ns':2,'_end_ns':3},{},[2],[3]),
        ('ns_precedence_large_us',{'startTime':MAX,'duration':MAX,'_start_ns':2,'_end_ns':3},{},[2],[3]),
    ]
    for name,changes,dtype,start,end in valid_times:
        add('time_control_'+name,[dict(BASE,**changes)],expected_ok(times={'start_ns':start,'end_ns':end}),dtype=dtype)

    # Known declarations agree or fail; unknown contributes no competing claim.
    for name, first, second, error, typ in [
        ('service_database','service','database',True,None),
        ('database_service','database','service',True,None),
        ('known_unknown','service','unknown',False,'service'),
        ('unknown_known','unknown','service',False,'service'),
        ('same_known','database','database',False,'database'),
        ('both_unknown','unknown','unknown',False,'unknown'),
    ]:
        rows=[dict(BASE,spanID='s1',attributes={'entity.type':first}),
              dict(BASE,spanID='s2',attributes={'entity.type':second})]
        add('type_span_'+name,rows,None if error else expected_ok(types={'A':typ}),
            universe={'A':'unknown'},error='conflicting_entity_type' if error else None)
    for name,inv,decl,error,typ in [
        ('inventory_service_span_database','service','database',True,None),
        ('inventory_database_span_service','database','service',True,None),
        ('inventory_known_span_unknown','service','unknown',False,'service'),
        ('inventory_unknown_span_known','unknown','service',False,'service'),
        ('inventory_known_span_known','service','service',False,'service'),
    ]:
        add('type_'+name,[dict(BASE,attributes={'entity.type':decl})],
            None if error else expected_ok(types={'A':typ}),universe={'A':inv},
            error='conflicting_entity_type' if error else None)
    for reverse in [False,True]:
        rows=[dict(BASE,spanID='s1',kind='CLIENT',attributes={'peer.entity':'D','peer.type':'database'}),
              dict(BASE,spanID='s2',kind='CLIENT',attributes={'peer.entity':'D','peer.type':'cache'})]
        add('type_endpoint_conflict_'+str(reverse),rows[::-1] if reverse else rows,error='conflicting_entity_type')
        rows=[dict(BASE,spanID='s1',attributes={'db.entity':'D','db.type':'database'}),
              dict(BASE,spanID='s2',serviceName='D',operationName='read',attributes={'entity.type':'service'})]
        add('type_endpoint_span_conflict_'+str(reverse),rows[::-1] if reverse else rows,
            universe={'A':'service','D':'unknown'},error='conflicting_entity_type')
    add('type_inventory_endpoint_conflict',
        [dict(BASE,attributes={'db.entity':'D','db.type':'database'})],
        universe={'A':'service','D':'service'},error='conflicting_entity_type')
    for name,peer_types,inv in [
        ('known_unknown',['database','unknown'],{'A':'service'}),
        ('unknown_known',['unknown','database'],{'A':'service'}),
        ('inventory_known_unknown',['unknown','unknown'],{'A':'service','D':'database'}),
    ]:
        rows=[dict(BASE,spanID='s'+str(i),kind='CLIENT',attributes={'peer.entity':'D','peer.type':typ}) for i,typ in enumerate(peer_types)]
        # Both endpoint events aggregate to the same edge, preserving two witnesses.
        ee=edge('A','D',SYNC,[['t','s0'],['t','s1']]);ee['event_count']=2
        oe=edge(oid('A','run'),'D',SYNC,[['t','s0'],['t','s1']]);oe['event_count']=2
        add('type_endpoint_control_'+name,rows,
            expected_ok(types={'A':'service','D':'database'},context={'D':'database'},
                        entity_edges=[ee],operation_edges=[oe],
                        projected_edges=[['A','D',SYNC,'trace',None]]),universe=inv)
    return cases


def normal(value):
    if value is pd.NA:
        return {'literal':'pd.NA'}
    if isinstance(value,np.generic):
        return normal(value.item())
    if isinstance(value,float) and not np.isfinite(value):
        return {'literal':repr(value)}
    if isinstance(value,dict):
        return {str(k):normal(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [normal(x) for x in value]
    return value


def capture(fn):
    try:
        value=fn()
        # Reject accidental NaN/pd.NA in graph/vocabulary serialization.
        json.dumps(value,ensure_ascii=False,allow_nan=False)
        return {'value':value}
    except Exception as exc:
        return {'error_type':type(exc).__name__,'error':str(exc)}


def graph_facts(module,frame,case,use_prepared):
    p=module.Prepared(frame,case['aliases'],case['universe'])
    entity,operation=(p.graph(case['interval']) if use_prepared else
                      module.build(frame,case['interval'],case['aliases'],case['universe']))
    nodes,edges=module.project(operation)
    answer={
        'entity_nodes':sort_json(entity['nodes']), 'entity_edges':sort_json(entity['edges']),
        'operation_nodes':sort_json(operation['nodes']), 'operation_edges':sort_json(operation['edges']),
        'belongs_to':sort_json(operation['belongs_to']),
        'component_context':sort_json(operation['component_context']),
        'projected_nodes':sorted(nodes), 'projected_edges':sort_json([list(x) for x in edges]),
    }
    expected=case['expected']
    if 'stats' in expected:
        answer['stats']={k:entity['stats'][k] for k in expected['stats']}
    if 'times' in expected:
        answer['times']={'start_ns':p.start.tolist(),'end_ns':p.end.tolist()}
    if 'vocabulary' in expected:
        value=p.vocabulary(case['interval'])
        value['operations']=sort_json(value['operations'])
        answer['vocabulary']=value
    return answer


def check_case(module,case):
    expected=case['expected']
    if case['action']=='project':
        def project_only():
            nodes,edges=module.project(case['operation'])
            return {'projected_nodes':sorted(nodes),'projected_edges':sort_json([list(x) for x in edges])}
        actual={'project':capture(project_only)}
    else:
        frame=pd.DataFrame(case['rows'])
        for column,dtype in case['dtype'].items():
            frame[column]=pd.Series([row[column] for row in case['rows']],dtype=dtype)
        actual={name:capture(lambda use=use:graph_facts(module,frame,case,use))
                for name,use in [('Prepared.graph',True),('build',False)]}
    def matches(value):
        if 'error' in expected:
            return value=={'error_type':'ValueError','error':expected['error']}
        return json.loads(json.dumps(value,ensure_ascii=False,allow_nan=False))==json.loads(json.dumps({'value':expected},ensure_ascii=False,allow_nan=False))
    return {'name':case['name'],'input':normal({k:v for k,v in case.items() if k!='expected'}),
            'expected':expected,'actual':normal(actual),'pass':all(matches(v) for v in actual.values())}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('output',nargs='?')
    parser.add_argument('--builder-path',default=str(ROOT/'src/do_thi/builder.py'))
    parser.add_argument('--list',action='store_true')
    args=parser.parse_args()
    cases=fixture_cases()
    if args.list:
        print(json.dumps({'case_count':len(cases),'names':[c['name'] for c in cases]},ensure_ascii=False))
        return
    if not args.output:
        parser.error('a new output directory is required')
    output=(HERE/args.output).resolve()
    if not output.is_relative_to(HERE) or output==HERE:
        raise ValueError('output_outside_run')
    output.mkdir(parents=True,exist_ok=False)
    path=Path(args.builder_path).resolve()
    spec=importlib.util.spec_from_file_location('t035_oracle_builder',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results=[check_case(module,case) for case in cases]
    result={'builder_path':str(path),'builder_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'oracle_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'case_count':len(results),'passed':sum(c['pass'] for c in results),
            'pass':all(c['pass'] for c in results),'cases':results}
    with (output/'result.json').open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(result,stream,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps({k:result[k] for k in ['case_count','passed','pass','builder_sha256']},ensure_ascii=False))
    raise SystemExit(0 if result['pass'] else 1)


if __name__=='__main__':
    main()
