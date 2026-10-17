"""Source-backed R1 adoption and complete dev replay. No raw telemetry or labels."""
from pathlib import Path
from collections import Counter, defaultdict
from copy import deepcopy
import datetime, difflib, gzip, hashlib, importlib.util, json, re, sys, time, traceback
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'results/T-038'; HERE=Path(__file__).resolve().parent
BEFORE=HERE/'before/results/T-038'; REVIEW=BASE/'runs/reviewer-r1-fix-20261016-001'
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p):return Path(p).relative_to(ROOT).as_posix()
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 data=(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
 if p.exists():assert p.read_bytes()==data,'unequal retained file: '+str(p)
 else:p.write_bytes(data)
def overwrite(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def read_result(p):return json.loads(gzip.decompress(Path(p).read_bytes()))
def api():
 pin=load(HERE/'pin.json');p=ROOT/pin['manifest'];assert sha(p)==pin['manifest_sha256']
 m=load(p);assert m['created_utc']==pin['created_utc'] and m['code_hashes']==pin['code_hashes']
 for row in m['files']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 for name,h in pin['code_hashes'].items():assert sha(p.parent/'code'/name)==sha(ROOT/'src/do_thi_tinh'/name)==h
 spec=importlib.util.spec_from_file_location('_T038_repair_common',p.parent/'code/__init__.py',submodule_search_locations=[str(p.parent/'code')])
 module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);return module
def signature(e):return canon([e['source'],e['target'],e['type'],e['channel'],e.get('messaging')])
def historical_description(value):
 """Normalize only the documented SMTP role annotation for historical comparison."""
 if isinstance(value,list):return [historical_description(x) for x in value]
 if isinstance(value,dict):
  d={k:historical_description(v) for k,v in value.items()}
  if d.get('id')=='smtp.163.com' and d.get('role')=='external mail server source default; SMTP V2 source relation; runtime unverified':
   d['role']='external mail server source default; SMTP relation unsupported by T036'
  return d
 return value

def prepare():
 m=load(REVIEW/'manifest.json')
 for row in m['files']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 assert sha(BEFORE/'manifest.json')==m['baseline_manifest_sha256']
 save(HERE/'reviewer-package-verified.json',dict(all_pass=True,files=len(m['files']),manifest_sha256=sha(REVIEW/'manifest.json')))
 save(HERE/'pin.json',load(BASE/'runs/doi-chieu-smtp-001/pin.json'))
 acquisition=load(BASE/'runs/tai-nguon-001/manifest.json');acquired={r['source_path']:r for r in acquisition['files']}
 oracle=load(REVIEW/'oracle.json');expected=[
 ('infra:skywalking:elasticsearch','skywalking:quickstart','elasticsearch:skywalking','dữ-liệu','data'),
 ('infra:alertsnitch:mysql','alertsnitch:quickstart','mysql-logical:alertsnitch','dữ-liệu','data'),
 ('infra:nacos:mysql','nacos:quickstart','mysql-logical:nacos:quickstart','dữ-liệu','data'),
 ('infra:alertmanager:alertsnitch-webhook','alertmanager:quickstart','alertsnitch:quickstart','gọi-chưa-phân-kiểu','http')]
 assert [(r['id'],r['source'],r['target'],r['type'],r['channel']) for r in oracle['relations']]==expected
 files={x[0] for r in oracle['relations'] for x in r['evidence']}
 files|={x[0] for r in load(REVIEW/'source-audit.json')['further_source_addresses'] for x in r['evidence']}
 texts={};verified=[]
 for name in sorted(files):
  row=acquired[name];p=ROOT/row['path'];data=p.read_bytes()
  assert len(data)==row['bytes'] and sha(p)==row['sha256']
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob']
  texts[name]=data.decode('utf-8-sig').replace('\r\n','\n');verified.append(row)
 sw=texts['deployment/kubernetes-manifests/skywalking/skywalking.yml']
 es=texts['deployment/kubernetes-manifests/skywalking/es.yml']
 sn=texts['deployment/kubernetes-manifests/prometheus/alertsnitch.yml']
 prefix='deployment/kubernetes-manifests/quickstart-k8s/charts/nacos/'
 nv,ns,nd=[texts[prefix+n] for n in ['values.yaml','templates/secrets.yaml','templates/statefulset.yaml']]
 hook=texts['deployment/kubernetes-manifests/prometheus/alert-manager-configmap.yml'];am=texts['deployment/kubernetes-manifests/prometheus/alert-manager.yml']
 checks=dict(
  sw_backend="STORAGE: 'elasticsearch7'" in sw and "STORAGE_ES_CLUSTER_NODES: 'elasticsearch:9200'" in sw,
  sw_loader=bool(re.search(r'envFrom:\s*- prefix: SW_\s*configMapRef:\s*name: skywalking-cm',sw)),
  es_target=bool(re.search(r'kind: Service[\s\S]*?name: elasticsearch',es)) and 'run: elasticsearch' in es,
  sn_backend=bool(re.search(r'name: ALERTSNITCH_BACKEND\s*value: mysql',sn)),
  sn_database=bool(re.search(r'tcp\(alertsnitch-mysql:3306\)/alertsnitch',sn)) and bool(re.search(r'name: MYSQL_DATABASE\s*value: alertsnitch',sn)),
  sn_service=bool(re.search(r'kind: Service[\s\S]*?name: alertsnitch-mysql',sn)),
  nacos_values='secretName: nacos-mysql' in nv and 'name: "nacos"' in nv and 'host: "nacos-mysql-leader"' in nv,
  nacos_template='with .Values.nacos.db' in ns and 'MYSQL_SERVICE_DB_NAME: {{ .name }}' in ns and 'MYSQL_SERVICE_HOST: {{.host}}' in ns,
  nacos_main_container='envFrom:' in nd.split('      containers:',1)[1] and 'name: {{ .Values.nacos.secretName }}' in nd.split('      containers:',1)[1],
  webhook_route='url: http://alertsnitch:9567/webhook' in hook and '- receiver: alertsnitch' in hook,
  webhook_loader=all(s in am for s in ['--config.file=/etc/config/alertmanager.yml','mountPath: /etc/config','name: alertmanager-config']))
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 save(HERE/'source-checks.json',dict(all_pass=True,checks=checks,files=verified,source_execution=False,credential_values_recorded=False,interpretation='Configured possibilities; effective image/deployment/runtime and RE2 lineage unverified.'))
 doc=load(BEFORE/'ban-ghi.json');reg=load(BEFORE/'nguon.json');creg=load(BASE/'runs/doi-chieu-smtp-001/registry-compare.json')
 entities={r['id'] for r in doc['entities']};delta=[]
 for item in oracle['relations']:
  assert item['source'] in entities and item['target'] in entities
  assert not any(r['source']['entity']==item['source'] and r['target']['entity']==item['target'] for r in doc['relations'])
  provenance=[]
  for name,first,last in item['evidence']:
   assert 1<=first<=last<=len(texts[name].splitlines())
   row=acquired[name];sid='TT:'+name
   entry=dict(id=sid,kind='source-code/configuration',revision=acquisition['commit'],sha256=row['sha256'],path=row['path'],condition='Conditional source profile; application/instrumentation/deployment linkage to RE2-TT unverified.')
   for registry in [reg,creg]:
    prior=next((s for s in registry['sources'] if s['id']==sid),None)
    if prior:assert all(prior[k]==entry[k] for k in ['path','sha256','revision'])
    else:registry['sources'].append(entry)
   provenance.append(dict(source_id=sid,locator=f'L{first}-L{last}',condition=item['condition']))
  delta.append(dict(id=item['id'],source=dict(entity=item['source'],operation=None),target=dict(entity=item['target'],operation=None),type=item['type'],channel=item['channel'],messaging=None,context=item['condition'],provenance=provenance))
 for registry in [reg,creg]:registry['sources'].sort(key=lambda r:r['id'])
 assert delta==load(REVIEW/'delta.json');save(HERE/'accepted-delta.json',delta)
 doc['relations']+=delta
 assert doc==load(REVIEW/'candidate/ban-ghi.json') and reg==load(REVIEW/'candidate/nguon.json')
 save(HERE/'registry-compare.json',creg)
 # Authoritative records precede every derived publication. Historical bytes remain in before/.
 overwrite(BASE/'ban-ghi.json',doc);overwrite(BASE/'nguon.json',reg)
 model=build_model(doc,reg)
 for name,value in model.items():
  save(HERE/'model'/name,value);overwrite(BASE/'do-thi'/name,value)
 save(HERE/'model-checks.json',dict(all_pass=True,before=dict(relations=509,entity_edges=166,operation_edges=343,root_projection=121,root_entity_only=44),after=dict(relations=513,entity_edges=170,operation_edges=343,projection=122,entity_only=48),unchanged=['entities','operations','signals','bindings','mapping','operation edge structure','shared pin','trace inputs'],candidate_model_equal=True))
 audit=load(REVIEW/'source-audit.json');audit['applied_to_producer_outputs']=True;audit['producer_validation']=rel(HERE/'source-checks.json')
 for row in audit['further_source_addresses']:
  row['producer_source_inspected']=True
  row['current_state']='OPEN' if row['source']!='grafana:quickstart' else 'NO_EDGE_JUSTIFIED_FROM_AVAILABLE_SOURCE'
  row['within_scope_resolution']='Đã đọc nguồn hiện có. Cần semantics image/client ngoài nguồn hoặc binding/discovery; hợp đồng hiện hành không có call channel unknown. Không đổi hợp đồng hoặc dựng cạnh từ port/role.' if row['source']!='grafana:quickstart' else 'Không có khai báo datasource trong nguồn này; không suy cạnh từ vai trò Grafana.'
 save(HERE/'source-audit.json',audit)
 save(HERE/'reproduction-inputs.json',dict(files=[dict(path=rel(p),sha256=sha(p)) for p in [BEFORE/'ban-ghi.json',BASE/'ban-ghi.json',BASE/'nguon.json',BASE/'mapping.json',HERE/'accepted-delta.json',HERE/'registry-compare.json',HERE/'pin.json',BASE/'runs/doi-chieu-smtp-001/summary.json',REVIEW/'candidate/summary.json']],common_pin=load(HERE/'pin.json'),method_changed=False))
 print(canon(dict(prepare=True,source_checks=len(checks),entity_edges=170,projection=122,entity_only=48)),flush=True)

def build_model(doc,reg):
 shared=api();snap=canon([doc,reg]);e,o=shared.build(doc,reg);assert snap==canon([doc,reg])
 rd=deepcopy(doc)
 for k in ['entities','operations','relations','signals','resource_bindings']:rd[k].reverse()
 assert shared.build(rd,reg)==(e,o)
 old=load(BEFORE/'ban-ghi.json');assert doc['relations'][:-4]==old['relations']
 for k in ['entities','operations','signals','resource_bindings']:assert historical_description(doc[k])==old[k]
 pe=shared.project(o);keys={signature(x) for x in pe['edges']};eo=[x for x in e['edges'] if signature(x) not in keys]
 assert keys<={signature(x) for x in e['edges']}
 assert (len(e['edges']),len(o['edges']),len(pe['edges']),len(eo))==(170,343,122,48)
 for name,value in [('thuc-the.json',e),('thao-tac.json',o),('chieu-thao-tac.json',pe)]:assert historical_description(value)==load(REVIEW/'candidate/do-thi'/name)
 assert eo==load(REVIEW/'candidate/do-thi/chi-thuc-the.json')['edges']
 assert o['edges']==load(BEFORE/'do-thi/thao-tac.json')['edges']
 return {'thuc-the.json':e,'thao-tac.json':o,'chieu-thao-tac.json':pe,'chi-thuc-the.json':dict(scope=e['scope'],edges=eo,note='Entity-only configured dependencies; no invented operation nodes.')}

def independent(result,static,trace,mappings):
 mi={(r['level'],r['original']):r for r in mappings};to=dict(trace.get('belongs_to',[]));so=dict(static.get('belongs_to',[]))
 def resolve(x):
  lev='operation' if x in to else 'entity';m=mi.get((lev,x))
  if m is None:return None,'unmapped'
  c=set(m['candidates'])
  if len(c)!=1:return None,'ambiguous_mapping' if c else 'unmapped'
  if not m['verified']:return None,'unverified_mapping'
  target=next(iter(c))
  if lev=='operation':
   owner,reason=resolve(to[x])
   if reason:return None,'operation_owner_'+reason
   if so[target]!=owner:return None,'operation_owner_conflict'
  return target,None
 for name,v in result['views'].items():
  sets={}
  for side,g in [('static',static),('trace',trace)]:
   groups=defaultdict(list);excluded={}
   for i,e in enumerate(g['edges']):
    s,t=e['source'],e['target'];reason=None
    if trace['level']=='entity' and (s==t or e['type']=='span-parent'):reason='not_entity_dependency'
    if not reason and side=='trace':
     for end in ['source','target']:
      x,r=resolve(e[end])
      if r:reason=r+':'+end;break
      if end=='source':s=x
      else:t=x
    if not reason and trace['level']=='entity' and s==t:reason='mapped_internal_relation'
    if not reason and e['type']=='thông-điệp':
     assert side=='static' and e['messaging']['broker_scope'] is None
     reason='incomplete_messaging_address'
    if not reason and name=='typed' and e['type']=='gọi-chưa-phân-kiểu':reason='unknown_type'
    if reason:excluded[i]=reason
    else:groups[canon([s,t,e['type'] if name=='typed' else None,['smtp',None] if e.get('channel')=='smtp' else None])].append(i)
   reported={canon(g['key']):[m['index'] for m in g['members']] for g in v['members'][side]}
   assert dict(groups)==reported
   assert excluded=={r['index']:r['reason'] for r in v['exclusions'][side]}
   members=[m for g in v['members'][side] for m in g['members']]+v['exclusions'][side]
   assert sorted(m['index'] for m in members)==list(range(len(g['edges'])))
   assert all(m['original']==g['edges'][m['index']] for m in members)
   sets[side]=set(groups)
  s,t=sets['static'],sets['trace']
  for k,x in [('S',s),('T',t),('intersection',s&t),('static_only',s-t),('trace_only',t-s)]:assert {canon(z) for z in v[k]}==x
  assert [v[k] for k in ['numerator','static_denominator','trace_denominator']]==[len(s&t),len(s),len(t)]
  assert v['static_fraction']==(len(s&t)/len(s) if s else None) and v['trace_fraction']==(len(s&t)/len(t) if t else None)
 assert result['interval_ns']==trace['interval_ns'] and result['conditional_reference'] is True
def semantic(v):
 v=deepcopy(v)
 for view in v['views'].values():
  for groups in view['members'].values():
   for g in groups:
    for m in g['members']:m.pop('index',None)
    g['members'].sort(key=canon)
   groups.sort(key=canon)
  for rows in view['exclusions'].values():
   for r in rows:r.pop('index',None)
   rows.sort(key=canon)
 return canon(v)
def peak():
 import ctypes
 class PMC(ctypes.Structure):
  _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
 m=PMC();m.cb=ctypes.sizeof(m);ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
 ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
 assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(m),m.cb)
 return m.PeakWorkingSetSize
def check(name):
 assert re.fullmatch('[a-z0-9-]+',name)
 out=HERE/'checks'/name;out.mkdir(parents=True,exist_ok=False);start=time.perf_counter();rows=[];deltas=[]
 try:
  inputs=HERE/('reproduction-inputs-v2.json' if (HERE/'reproduction-inputs-v2.json').exists() else 'reproduction-inputs.json')
  for item in load(inputs)['files']:assert sha(ROOT/item['path'])==item['sha256'],item['path']
  shared=api();doc=load(BASE/'ban-ghi.json');reg=load(BASE/'nguon.json');mapping=load(BASE/'mapping.json');cr=load(HERE/'registry-compare.json')
  model=build_model(doc,reg)
  for file,value in model.items():assert value==load(BASE/'do-thi'/file),'canonical '+file
  e,o=model['thuc-the.json'],model['thao-tac.json'];graphs={'entity':e,'operation':o}
  baseline=load(BASE/'runs/doi-chieu-smtp-001/summary.json');candidate=load(REVIEW/'candidate/summary.json')
  assert len(baseline['rows'])==len(candidate['rows'])==1069
  ci={r['input']:r for r in candidate['rows']};t35=ROOT/'results/T-035/manifest.json'
  assert sha(t35)==load(BEFORE/'manifest.json')['input_manifests']['results/T-035/manifest.json']['sha256']
  m35={r['path']:r['sha256'] for r in load(t35)['files']}
  idx=load(BEFORE/'doi-chieu/index.json');assert set(idx['outputs'])=={r['output'] for r in baseline['rows']}
  for i,prior in enumerate(baseline['rows'],1):
   p=ROOT/prior['input'];assert sha(p)==prior['input_sha256']==m35[prior['input']]
   trace=load(p);level=prior['level'];sg=graphs[level];mp=[m for m in mapping if m['level']=='entity' or level=='operation']
   oldp=ROOT/prior['output'];assert sha(oldp)==prior['output_sha256'];old=read_result(oldp)
   crow=ci[prior['input']];cp=ROOT/crow['output'];assert sha(cp)==crow['output_sha256'];proposed=read_result(cp)
   snap=canon([sg,trace,mp,cr,old['context']]);result=shared.compare(sg,trace,mp,old['context'],cr)
   independent(result,sg,trace,mp);assert historical_description(result)==proposed,'producer replay differs beyond documented role annotation'
   # Candidate already has full repeat/reorder evidence. Recheck against official inputs here.
   assert result==shared.compare(sg,trace,mp,old['context'],cr)
   rt=deepcopy(trace)
   for k in ['nodes','edges','belongs_to','component_context']:
    if k in rt:rt[k].reverse()
   assert semantic(result)==semantic(shared.compare(sg,rt,list(reversed(mp)),old['context'],cr))
   assert snap==canon([sg,trace,mp,cr,old['context']])
   if level=='operation':assert historical_description(result)==old
   vd={}
   for vn,v in result['views'].items():
    pv=old['views'][vn];new={canon(k) for k in v['S']}-{canon(k) for k in pv['S']};removed={canon(k) for k in pv['S']}-{canon(k) for k in v['S']}
    assert not removed and len(new)==((4 if vn=='endpoints' else 3) if level=='entity' else 0)
    for k in ['T','intersection','trace_only']:assert v[k]==pv[k]
    for k in ['members','exclusions']:assert v[k]['trace']==pv[k]['trace']
    def members(z):return {canon([g['key'],m['original']]) for g in z['members']['static'] for m in g['members']}
    def exclusions(z):return {canon({k:v for k,v in r.items() if k!='index'}) for r in z['exclusions']['static']}
    assert members(pv)<=members(v) and len(members(v)-members(pv))==len(new)
    assert exclusions(pv)<=exclusions(v)
    assert len(exclusions(v)-exclusions(pv))==(1 if level=='entity' and vn=='typed' else 0)
    vd[vn]=dict(added_S=[json.loads(x) for x in sorted(new)],removed_S=[],static_fraction_before=pv['static_fraction'],static_fraction_after=v['static_fraction'],trace_fraction_before=pv['trace_fraction'],trace_fraction_after=v['trace_fraction'])
   tail=p.relative_to(ROOT/'results/T-035/do-thi/RE2-TT').as_posix()+'.gz';dest=out/'doi-chieu'/tail;dest.parent.mkdir(parents=True,exist_ok=True)
   dest.write_bytes(gzip.compress(canon(result).encode(),compresslevel=6,mtime=0))
   row=dict(input=prior['input'],input_sha256=prior['input_sha256'],level=level,interval_ns=trace['interval_ns'],output=rel(dest),output_sha256=sha(dest),baseline_output=prior['output'],candidate_output=crow['output'],documented_SMTP_role_annotation_changed=True,repeat_exact=True,reorder_semantic_equal=True,independent_sets_members_exclusions_denominators=True,input_unchanged=True,conditional_reference=True,revision_link_verified=False,views={n:{k:len(v[k]) if isinstance(v[k],list) else v[k] for k in ['S','T','intersection','static_only','trace_only','static_fraction','trace_fraction']} for n,v in result['views'].items()})
   rows.append(row);deltas.append(dict(input=row['input'],level=level,views=vd))
   if i%25==0 or i==1069:
    progress=dict(done=i,total=1069,elapsed_seconds=time.perf_counter()-start);print(canon(progress),flush=True)
    with (out/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(canon(progress)+'\n')
  families=Counter((r['level'],Path(r['input']).stem.split('-')[0]) for r in rows)
  save(out/'summary.json',dict(task='T-038',all_pass=True,graph_count=1069,errors=[],rows=rows,pin=load(HERE/'pin.json'),family_counts=[dict(level=k[0],family=k[1],count=v) for k,v in sorted(families.items())]))
  save(out/'delta.json',dict(graphs=1069,entity=979,operation_structure_views_unchanged=90,only_documented_SMTP_role_payload_difference=True,rows=deltas))
  save(out/'verification.json',dict(all_pass=True,graphs=1069,official_model_checked=True,independent=True,compared_to_candidate=True,only_documented_role_payload_difference=True,operation_views_exact_unchanged=True,trace_and_intersections_unchanged=True,repeat_reorder_input_unchanged=True))
  save(out/'cost.json',dict(elapsed_seconds=time.perf_counter()-start,peak_process_rss_bytes=peak(),network_bytes=0,output_bytes=sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),isolated_benchmark=False,python=sys.version))
 except BaseException:
  save(out/'failure.json',dict(traceback=traceback.format_exc(),completed=len(rows),elapsed_seconds=time.perf_counter()-start));raise
if __name__=='__main__':
 try:
  if sys.argv[1]=='prepare':raise SystemExit('Initial preparation is historical and already completed; use check <fresh-run-name>.')
  elif sys.argv[1]=='check':check(sys.argv[2])
  else:raise SystemExit('Use prepare, or check <fresh-run-name>')
 except BaseException:
  p=HERE/('failure-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json');save(p,dict(traceback=traceback.format_exc()));raise
