"""T037 design graph + independent projection + declared synthetic runtime boundaries."""
from pathlib import Path
import copy
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import platform
import random
import re
import sys
import time
import traceback

ROOT=Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def package(name,d):
 spec=importlib.util.spec_from_file_location(name,d/'__init__.py',submodule_search_locations=[str(d)])
 m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def ram():
 class M(ctypes.Structure):
  _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
 m=M();m.cb=ctypes.sizeof(m);gp=ctypes.windll.kernel32.GetCurrentProcess;gp.restype=wintypes.HANDLE
 gm=ctypes.windll.psapi.GetProcessMemoryInfo;gm.argtypes=[wintypes.HANDLE,ctypes.POINTER(M),wintypes.DWORD]
 if not gm(gp(),ctypes.byref(m),m.cb):raise ctypes.WinError()
 return m.PeakWorkingSetSize

def main(out):
 out.mkdir(parents=True,exist_ok=False);started=time.perf_counter();checks=[];stages=[]
 def progress(stage):
  r=dict(stage=stage,elapsed_seconds=time.perf_counter()-started);stages.append(r)
  with (out/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(canonical(r)+'\n')
 def check(name,actual,expected=True):
  ok=actual==expected;r=dict(name=name,ok=ok)
  if not ok:r.update(actual=actual,expected=expected)
  checks.append(r)
  return ok
 def require(name,a,e=True):
  if not check(name,a,e):raise ValueError('required_check_failed:'+name)
 try:
  progress('input-hash-and-snapshot')
  registry=load(BASE/'nguon.json');doc=load(BASE/'ban-ghi.json');oracle=load(BASE/'oracle-v3.json');fi=load(BASE/'fixtures-runtime-v2.json')
  require('smtp-regression-passed',load(BASE/'runs/smtp-regression-001/result.json')['all_pass'])
  for s in registry['sources']:
   require('source:'+s['id'],sha(Path(s['path'])),s['sha256']);require('snapshot:'+s['id'],sha(ROOT/s['snapshot']),s['sha256'])
  pre=load(BASE/'runs/tiep-smtp-001/preflight.json')
  for rel in ['results/T-036/manifest.json','results/T-036/runs/kiem-r1-after-002/code-hashes.json','tasks/T-038-p5b-trainticket/SPEC.md','tasks/T-039-p5b-online-boutique/SPEC.md']:
   require('protected-pin:'+rel,sha(ROOT/rel),pre['protected'][rel])
  adapted=load(BASE/'runs/smtp-regression-001/input-code-verification.json')
  for row in adapted:require('verified-current-code:'+row['path'],sha(ROOT/row['path']),row['current_sha256'])
  code=out/'code';code.mkdir()
  for p in (ROOT/'src/do_thi_tinh').glob('*.py'):(code/p.name).write_bytes(p.read_bytes())
  (out/'runner.py').write_bytes(Path(__file__).read_bytes())
  for name in ['oracle-v3.json','fixtures-runtime-v2.json','ban-ghi.json','nguon.json']:(out/name).write_bytes((BASE/name).read_bytes())
  dump(out/'input-code-hashes.json',{p.relative_to(ROOT).as_posix():sha(p) for p in [BASE/'oracle-v3.json',BASE/'fixtures-runtime-v2.json',BASE/'ban-ghi.json',BASE/'nguon.json']+sorted(code.glob('*.py'))})
  dump(out/'environment.json',dict(python=sys.version,executable=sys.executable,platform=platform.platform(),device=platform.node(),started_utc=datetime.now(timezone.utc).isoformat(),command=[sys.executable,'-X','utf8','-B',str(Path(__file__)),out.name],source_kind='design; runtime fixtures synthetic only'))
  mod=package('t037_complete_static',code)
  before=canonical([doc,registry]);entity,operation=mod.build(doc,registry);projection=mod.project(operation)
  check('build_and_project_do_not_mutate_input',canonical([doc,registry]),before)
  dump(out/'entity.json',entity);dump(out/'operation.json',operation);dump(out/'projection.json',projection)
  progress('independent-record-to-id-type-address-oracle')
  def oid(e,n):return json.dumps([e,n],ensure_ascii=False,separators=(',',':'))
  def normprov(ps):return [json.loads(x) for x in sorted({canonical(p) for p in ps})]
  def independent_edges(rows,level):
   groups={}
   for r in rows:
    se,te=r['source']['entity'],r['target']['entity'];so,to=r['source']['operation'],r['target']['operation']
    if level=='operation' and so is None and to is None:continue
    if level=='entity' and (se==te or r['type']=='span-parent'):continue
    s=oid(se,so) if level=='operation' and so is not None else se
    t=oid(te,to) if level=='operation' and to is not None else te
    edge=dict(source=s,target=t,type=r['type'],channel=r['channel'],messaging=r['messaging'],evidence_source='static',destination=None)
    if r['messaging'] is not None:
     q=[r['messaging'][k] for k in ['broker','broker_scope','queue']];edge['queue_metric_address']=q if all(q) else None
    key=canonical([s,t,r['type'],r['channel'],r['messaging']])
    row=groups.setdefault(key,dict(edge,record_ids=[],provenance=[],contexts=[]))
    row['record_ids']=sorted(set(row['record_ids']+[r['id']]))
    row['provenance']=normprov(row['provenance']+r['provenance']);row['contexts']=sorted(set(row['contexts']+[r['context']]))
   return [groups[k] for k in sorted(groups)]
  want_entity=independent_edges(doc['relations'],'entity');want_operation=independent_edges(doc['relations'],'operation')
  eligible=[r for r in doc['relations'] if r['source']['operation'] is not None or r['target']['operation'] is not None]
  want_projection=independent_edges(eligible,'entity')
  check('entity_edges_exact_independent_records',entity['edges'],want_entity)
  check('operation_edges_exact_independent_ID_type_address',operation['edges'],want_operation)
  check('projection_exact_independent_supported_subset',projection['edges'],want_projection)
  check('records_preserve_all_IDs_and_provenance',{x['id'] for x in entity['records']},{x['id'] for x in doc['relations']})
  check('all_operation_IDs_literal_pair',sorted(x['id'] for x in operation['nodes']),sorted(oid(o['entity'],o['name']) for o in doc['operations']))
  for col in ['resource_bindings','signals']:
   target=copy.deepcopy(doc[col])
   for x in target:x['provenance']=normprov(x['provenance'])
   check(col+'_preserved',entity[col],sorted(target,key=lambda x:x['id']))
  check('entity_only_exclusions_exact',operation['operation_exclusions'],[dict(record_id=r['id'],reason='no_operation_evidence') for r in sorted(doc['relations'],key=lambda x:x['id']) if r['source']['operation'] is None and r['target']['operation'] is None])
  ids={n['id'] for n in entity['nodes']};check('literal_inventory_complete_for_design',ids,set(oracle['required_entities']))
  pairs={(r['source']['entity'],r['target']['entity']) for r in doc['relations']}
  check('required_data_pairs',all(tuple(x) in pairs for x in oracle['data_pairs']))
  hpairs={(r['source']['entity'],r['target']['entity']) for r in doc['relations'] if r['channel']=='http'}
  check('required_http_pairs',all(tuple(x) in hpairs for x in oracle['http_pairs']))
  check('forbidden_dependencies_absent',not (pairs & {tuple(x) for x in oracle['forbidden_pairs']}))
  messages=sorted([r['messaging']['routing_key'],r['source']['entity'],r['target']['entity']] for r in doc['relations'] if r['channel']=='logical-message')
  check('literal_B13_routes_including_three_target_fanout',messages,sorted(oracle['messages']))
  check('business_exchange_exact',{r['messaging']['exchange'] for r in doc['relations'] if r['messaging']}, {oracle['business_exchange']})
  check('runtime_scope_and_queue_not_invented',all(r['messaging']['broker_scope'] is None and r['messaging']['queue'] is None for r in doc['relations'] if r['messaging']))
  check('source_queue_metric_addresses_remain_null',all(e['queue_metric_address'] is None for e in entity['edges'] if e['messaging']))
  smtp=[r for r in doc['relations'] if r['channel']=='smtp'];require('one_smtp_record',len(smtp),1)
  check('smtp_exact_source_owner_type_address',dict(source=smtp[0]['source']['entity'],operation=smtp[0]['source']['operation'],target=smtp[0]['target']['entity'],type=smtp[0]['type'],channel=smtp[0]['channel'],runtime_name=None),oracle['smtp'])
  check('five_DBs_one_PG_instance',sorted(b['entity'] for b in entity['resource_bindings'] if b['relation']=='hosted_on' and b['resource']=='postgresql-shared-instance'),sorted(oracle['shared_pg_databases']))
  check('no_runtime_operation_names',all(n['runtime_name'] is None for n in operation['nodes']))
  check('inventory_not_observed_or_candidates',entity['observed_nodes'],[])
  check('no_static_event_count',all('event_count' not in e for g in [entity,operation] for e in g['edges']))
  check('shared_metric_not_on_operation',all(s['operation'] is None for s in entity['signals'] if s['shared']))
  for seed in [0,1,2]:
   shuffled=copy.deepcopy(doc);rng=random.Random(seed)
   for col in ['entities','operations','relations','resource_bindings','signals']:rng.shuffle(shuffled[col])
   result=mod.build(shuffled,registry);check('reorder_'+str(seed),hashlib.sha256(canonical(result).encode()).hexdigest(),hashlib.sha256(canonical((entity,operation)).encode()).hexdigest())
  progress('source-coverage-to-graph-address-matrix')
  coverage=load(BASE/'bao-phu-nguon.json');allrecord={r['id']:r for col in ['relations','resource_bindings','signals'] for r in doc[col]};matrix=[]
  for u in coverage['units']:
   references=[]
   for rid in u['record_ids']:
    require('coverage_record_exists:'+u['unit_id']+':'+rid,rid in allrecord or rid in ids)
    references.append(dict(record_id=rid,entity_edge_indices=[i for i,e in enumerate(entity['edges']) if rid in e['record_ids']],operation_edge_indices=[i for i,e in enumerate(operation['edges']) if rid in e['record_ids']],binding=next((b['id'] for b in entity['resource_bindings'] if b['id']==rid),None),signal=next((s['id'] for s in entity['signals'] if s['id']==rid),None)))
   matrix.append(dict(unit_id=u['unit_id'],source_id=u['source_id'],locator=u['locator'],classification=u.get('status'),references=references,entity_ids=u['entity_ids'],operation_names=u['operation_names'],owner=u.get('owner'),required_input=u.get('required_input')))
  dump(out/'requirement-record-graph-matrix.json',matrix)
  dump(out/'entity-only.json',dict(operation_exclusions=operation['operation_exclusions'],entity_only_edges=[e for e in entity['edges'] if not set(e['record_ids']) & {r['id'] for r in eligible}],meaning='No fake operation; projected subset plus entity-only supported inventory'))
  dump(out/'independent-expected-edges.json',dict(entity=want_entity,operation=want_operation,projection=want_projection))
  progress('synthetic-runtime-boundary-fixtures')
  # Verify T035 code before loading it; no raw telemetry or datasets are opened.
  tm=load(ROOT/'results/T-035/manifest.json');th={x['path']:x for x in tm['files']}
  for relpath in ['src/do_thi/builder.py','src/do_thi/__init__.py']:
   require('T035_code_hash:'+relpath,sha(ROOT/relpath),th[relpath]['sha256'])
  sys.path.insert(0,str(ROOT/'src'));from do_thi.builder import build as trace_build
  import pandas as pd
  fxregistry=dict(sources=[dict(id='FT-SYNTHETIC',kind='synthetic',revision='fixture-v2',sha256=sha(BASE/'fixtures-runtime-v2.json'),condition='Declared synthetic data; not runtime')])
  fd=fi['static_document'];fe,fo=mod.build(fd,fxregistry);fp=mod.project(fo)
  fexpected=oracle['synthetic_runtime_fixtures'];fx=[]
  def trace_case(name):
   spans=copy.deepcopy(fi['trace_cases'][name]);original=canonical(spans)
   te,to=trace_build(pd.DataFrame(spans),None,{},fi['universe'])
   check('trace_fixture_input_unchanged:'+name,canonical(spans),original)
   fx.append(dict(name=name,entity=te,operation=to));return te,to
  callback,_=trace_case('callback-new-trace');check('callback_keeps_two_trace_roots',callback['stats']['roots'],2);check('callback_correlation_no_edge',callback['edges'],[])
  scheduler,_=trace_case('scheduler-root');check('scheduler_no_caller',scheduler['edges'],[])
  corr,_=trace_case('correlation-only-message');check('correlation_does_not_join_message',sum(e['evidence_source']=='inferred' for e in corr['edges']),0)
  fan,_=trace_case('verified-fanout');check('verified_message_fanout_three_targets',sorted(e['target'] for e in fan['edges'] if e['evidence_source']=='inferred'),fexpected['verified_message_fanout_targets'])
  queues,queueops=trace_case('two-queues');retry,retryops=trace_case('retry-same-operation')
  check('retry_reuses_operation_node',len(retryops['nodes']),1)
  check('retry_two_attempts_single_structural_consume',len(retry['edges']),1)
  check('retry_keeps_attempt_events_as_witness_count',retry['edges'][0]['event_count'],2)
  check('two_queue_consume_stays_two_edges',len(queues['edges']),2)
  check('two_queue_addresses_exact',sorted(e['queue_metric_address'] for e in queues['edges']),fexpected['two_queue_consume_addresses'])
  check('static_two_queue_projection_keeps_addresses',sorted(e['queue_metric_address'] for e in fp['edges'] if e['channel']=='consume'),fexpected['two_queue_consume_addresses'])
  check('two_queue_metric_only_two_addresses',len([s for s in fe['signals'] if s['entity']=='broker']),2)
  check('shared_pg_one_instance_one_shared_metric',len([s for s in fe['signals'] if s['entity']=='pg' and s['operation'] is None and s['shared']]),1)
  mapping=[dict(level='entity',original=i,candidates=[i],verified=True,provenance=prov('FT-SYNTHETIC','identity explicitly declared for synthetic test')) for i in ['payment-service','booking-service','ticket-service','broker','smtp']]
  ctx=dict(system='synthetic-FT',level='entity',domain='synthetic',trace_revision='synthetic-only',revision_link_verified=False,revision_provenance=[],relation_types=['thông-điệp'])
  snap=canonical([fe,queues,mapping,ctx,fxregistry]);comp=mod.compare(fe,queues,mapping,ctx,fxregistry)
  for view in ['endpoints','typed']:check('two_queue_match:'+view,[comp['views'][view][k] for k in ['numerator','static_denominator','trace_denominator']],[2,3,2])
  check('compare_preserves_static_trace_inputs',canonical([fe,queues,mapping,ctx,fxregistry]),snap)
  dump(out/'fixture-compare-two-queues.json',comp)
  missing=copy.deepcopy(fd)
  for r in missing['relations']:
   if r['messaging']:r['messaging']['broker_scope']=None;r['messaging']['queue']=None
  me,_=mod.build(missing,fxregistry);mc=mod.compare(me,queues,mapping,ctx,fxregistry)
  check('missing_address_never_matches',mc['views']['endpoints']['numerator'],0)
  check('missing_address_reported',all(x['reason']=='incomplete_messaging_address' for x in mc['views']['endpoints']['exclusions']['static'] if x['original']['type']=='thông-điệp'))
  dump(out/'fixture-compare-missing-address.json',mc)
  opt=copy.deepcopy(ctx);opt['level']='operation';unmapped=mod.compare(fo,queueops,mapping,opt,fxregistry)
  check('operation_mapping_missing_excludes_two_consume',sorted(x['reason'] for x in unmapped['views']['endpoints']['exclusions']['trace']),[fexpected['no_operation_mapping_reason']]*2)
  check('missing_operation_mapping_does_not_create_fake_operation',unmapped['views']['endpoints']['numerator'],0)
  dump(out/'fixture-compare-missing-operation.json',unmapped)
  ud=copy.deepcopy(fd);ud['relations']=[dict(id='unknown-call',source=end('ticket-service'),target=end('smtp'),type='gọi-chưa-phân-kiểu',channel='smtp',messaging=None,context='Synthetic unknown type',provenance=prov('FT-SYNTHETIC','unknown literal'))]
  ue,_=mod.build(ud,fxregistry);ut=dict(level='entity',nodes=[dict(id='ticket-service'),dict(id='smtp')],interval_ns=None,edges=[dict(source='ticket-service',target='smtp',type='gọi-chưa-phân-kiểu',evidence_source='trace',destination=None,event_count=1,witness=[['syn','span']])])
  uc=copy.deepcopy(ctx);uc.pop('relation_types');unknown=mod.compare(ue,ut,mapping,uc,fxregistry)
  check('unknown_only_endpoint_match',unknown['views']['endpoints']['numerator'],1)
  check('unknown_not_typed_match',unknown['views']['typed']['static_denominator'],0)
  dump(out/'fixture-compare-unknown.json',unknown)
  invalid=copy.deepcopy(doc);invalid['label']='must-not-enter-method'
  try:mod.build(invalid,registry);check('reject_label_field',False)
  except ValueError as e:check('reject_label_field',str(e).startswith('unknown_fields:'))
  dump(out/'fixture-trace-graphs.json',fx)
  progress('finished')
  stats=dict(inventory_nodes=len(entity['inventory']),observed_nodes=len(entity['observed_nodes']),operations=len(operation['nodes']),source_relations=len(doc['relations']),entity_edges=len(entity['edges']),operation_edges=len(operation['edges']),projection_edges=len(projection['edges']),entity_only_relation_count=len(operation['operation_exclusions']),bindings=len(entity['resource_bindings']),signals=len(entity['signals']),shared_signals=sum(s['shared'] for s in entity['signals']),source_count=len(registry['sources']),coverage_units=len(coverage['units']))
  result=dict(task='T-037',all_pass=all(x['ok'] for x in checks),passed=sum(x['ok'] for x in checks),failed=sum(not x['ok'] for x in checks),checks=checks,stats=stats,seconds=time.perf_counter()-started,peak_working_set_bytes=ram(),stages=stages,runtime_verified=False,rca_benefit_verified=False)
  dump(out/'result.json',result);print(canonical({k:result[k] for k in ['all_pass','passed','failed','stats','seconds','peak_working_set_bytes']}))
  return 0 if result['all_pass'] else 1
 except Exception:
  dump(out/'failure.json',dict(traceback=traceback.format_exc(),checks=checks,stages=stages,seconds=time.perf_counter()-started));raise

def end(e,o=None):return dict(entity=e,operation=o)
def prov(s,l):return [dict(source_id=s,locator=l,condition='Synthetic only')]
if __name__=='__main__':
 if len(sys.argv)!=2 or not re.fullmatch('[a-z0-9-]+',sys.argv[1]):raise ValueError('new run name required')
 raise SystemExit(main(BASE/'runs'/sys.argv[1]))
