"""Additional T036 signal records from verified current Java/config only."""
from pathlib import Path, PurePosixPath
import collections, hashlib, json, re
import yaml

OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[4]
A=json.loads((ROOT/'results/T-038/runs/tai-nguon-001/manifest.json').read_text('utf-8'))
IDX={x['source_path']:x for x in A['files']};REG={};READ=set();COMMIT=A['commit']
COND='Snapshot source v1.0.0 tham khảo có điều kiện; deployment runtime và lineage RE2-TT chưa xác minh.'
def read(p):
 assert p.startswith('ts-') or p.startswith(('deployment/','hack/')) or p in ['Makefile','pom.xml']
 assert '/node_modules/' not in p and '/src/test/' not in p
 x=IDX[p];b=(ROOT/x['path']).read_bytes()
 assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 READ.add(p);return b.decode('utf-8-sig')
def prov(p,l,end=None,cond=None):
 read(p);sid='TT:'+p;x=IDX[p]
 REG[sid]={'id':sid,'kind':'config' if p.startswith('deployment/') or '/resources/' in p else 'source-code','revision':COMMIT,'sha256':x['sha256'],'condition':COND,'path':x['path'],'source_path':p}
 return {'source_id':sid,'locator':f'{p}:L{l}'+(f'-L{end}' if end and end!=l else ''),'condition':cond or COND}
signals=[];open_items=[];logger_calls=[];javafiles=[];modules=set();pattern_hits=[]
for p in IDX:
 if not(p.startswith('ts-') and '/src/main/java/' in p and p.endswith('.java')):continue
 javafiles.append(p);modules.add(p.split('/')[0]);text=read(p);package=re.search(r'^\s*package\s+([\w.]+)\s*;',text,re.M)
 for line_no,line in enumerate(text.splitlines(),1):
  if 'LoggerFactory.getLogger' not in line:continue
  match=re.search(r'LoggerFactory\.getLogger\((\w+)\.class\)',line)
  if not match:
   open_items.append({'kind':'unresolved-logger-expression','source_path':p,'line':line_no,'expression':line.strip()});continue
  cls=match.group(1);assert cls==PurePosixPath(p).stem
  fqcn=(package.group(1)+'.' if package else '')+cls;owner=p.split('/')[0]
  record={'owner_module':owner,'class':fqcn,'source_path':p,'line':line_no,'expression':match.group(0)};logger_calls.append(record)
  if owner=='ts-common':
   open_items.append({'kind':'shared-library-logger-owner','source_path':p,'line':line_no,'class':fqcn,'reason':'ts-common là thư viện, không tự tạo service hoặc nhân logger cho mọi module. Cần callpath/placement để gán owner.','provenance':[prov(p,line_no)]});continue
  signals.append({'id':'signal:slf4j:'+fqcn,'kind':'log','entity':owner,'operation':None,'address':['slf4j:factory=org.slf4j.LoggerFactory.getLogger','slf4j:class='+fqcn],'shared':True,'provenance':[prov(p,line_no,cond='Class literal khai báo logger nguồn; không khẳng định output backend/pattern, trace/span correlation hoặc operation runtime. '+COND)]})
 # Do not interpret message text as log schema or route it to all operations.
configfiles=[]
for p in IDX:
 if p.startswith('ts-') and ('/src/main/resources/' in p or p.endswith(('pom.xml','Dockerfile'))) and p.endswith(('.xml','.yml','.yaml','.properties','Dockerfile')):
  configfiles.append(p)
  for line_no,line in enumerate(read(p).splitlines(),1):
   if re.search(r'logging\.(?:pattern|level)|logback|log4j|%X\{|%trace|%span|logging:',line,re.I):pattern_hits.append({'source_path':p,'line':line_no,'text':line})
logconfigpaths=[p for p in IDX if p.startswith('ts-') and '/node_modules/' not in p and any(k in p.lower() for k in ['logback','log4j'])]
open_items.append({'kind':'log-output-schema','reason':'Không thấy dedicated logback/log4j file; các logger declarations không xác minh backend/default pattern hoặc structured trace/span keys. Không lấy defaults framework ngoài snapshot làm schema thật.','dedicated_config_paths':logconfigpaths,'config_pattern_hits':pattern_hits})

def walk(node,prefix=()):
 if isinstance(node,yaml.MappingNode):
  for k,v in node.value:yield from walk(v,prefix+(str(k.value),))
 elif isinstance(node,yaml.SequenceNode):
  for i,v in enumerate(node.value):yield from walk(v,prefix+(str(i),))
 else:yield prefix,node.value,node.start_mark.line+1
sw='deployment/kubernetes-manifests/quickstart-k8s/yamls/sw_deploy.yaml.sample';chains=[];swowners=[]
for doc_no,doc in enumerate(yaml.compose_all(read(sw),Loader=yaml.SafeLoader)):
 if doc is None:continue
 flat={keys:(value,line) for keys,value,line in walk(doc)};owner=flat.get(('metadata','name'),(None,None))[0]
 envs=[]
 for keys,(name,line) in flat.items():
  if keys[-1:]!=('name',) or 'env' not in keys:continue
  if name not in ['SW_AGENT_NAME','SW_AGENT_COLLECTOR_BACKEND_SERVICES','SW_GRPC_LOG_SERVER_HOST','SW_GRPC_LOG_SERVER_PORT','JAVA_TOOL_OPTIONS']:continue
  parent=keys[:-1];val=flat.get(parent+('value',),(None,None));field=flat.get(parent+('valueFrom','fieldRef','fieldPath'),(None,None))
  envs.append({'name':name,'declaration_line':line,'value':val[0],'value_line':val[1],'field_path':field[0],'field_path_line':field[1]})
 if not envs:continue
 swowners.append(owner);label=flat.get(('spec','template','metadata','labels','app'),(None,None));name_env=next((x for x in envs if x['name']=='SW_AGENT_NAME'),None);collector=next((x for x in envs if x['name']=='SW_AGENT_COLLECTOR_BACKEND_SERVICES'),None)
 chains.append({'owner':owner,'document_index':doc_no,'template_label_app':label[0],'template_label_line':label[1],'env':envs,'condition':'Optional tracing source sample, copied by generator; actual namespace/overrides/agent execution not verified.'})
 if owner not in modules or owner=='ts-common':
  open_items.append({'kind':'java-agent-env-on-nonjava-owner','owner':owner,'reason':'Template declares Java agent/env for a nonJava module. Preserve literal config in override table; do not treat as working trace instrumentation or add signal record.','provenance':[prov(sw,name_env['declaration_line'] if name_env else label[1])]})
  continue
 if name_env and name_env['field_path']=="metadata.labels['app']" and collector:
  assert label[0]==owner
  address=['env:SW_AGENT_NAME<-fieldRef:'+name_env['field_path'],'kubernetes:spec.template.metadata.labels.app='+owner,'env:SW_AGENT_COLLECTOR_BACKEND_SERVICES='+collector['value']]
  signals.append({'id':'signal:skywalking-source:'+owner,'kind':'trace','entity':owner,'operation':None,'address':address,'shared':True,'provenance':[prov(sw,label[1],cond='Owner/source label and fieldRef are declared; no runtime telemetry observation. '+COND),prov(sw,name_env['declaration_line'],name_env['field_path_line']),prov(sw,collector['declaration_line'],collector['value_line'])]})
 else:open_items.append({'kind':'skywalking-owner-resolution','owner':owner,'reason':'No matching fieldRef/collector declaration; source address not fabricated.'})
chains.append({'scope':'source override path','chain':[prov('Makefile',34,38),prov('hack/deploy/deploy.sh',60,65),prov('hack/deploy/utils.sh',110,114),prov('hack/deploy/gen-mysql-secret.sh',80,90)],'explanation':'--with-tracing selects sw deployment template; helper copies and substitutes Nacos/RabbitMQ names. It does not rewrite SW_AGENT_NAME or collector values. OS condition/runtime execution remains OPEN.'})

prom='deployment/kubernetes-manifests/prometheus/prometheus-configmap.yml';ptext=read(prom);pdocs=list(yaml.safe_load_all(ptext));promcfg=yaml.safe_load(pdocs[0]['data']['prometheus.yml']);jobs=[]
for job in promcfg['scrape_configs']:
 name=job['job_name'];line=next(i for i,l in enumerate(ptext.splitlines(),1) if 'job_name:' in l and l.split('job_name:',1)[1].strip().strip("'\"")==name)
 jobs.append({'job_name':name,'source_path':prom,'line':line,'config':job,'provenance':[prov(prom,line)],'status':'SOURCE_SCRAPE_CONFIGURATION_NOT_RUNTIME_SERIES'})
 # Target ownership is known only for the self scrape and node-exporter name selector.
 if name in ['prometheus','node-exporter']:
  owner='prometheus:quickstart' if name=='prometheus' else 'node-exporter:quickstart'
  address=['prometheus:job_name='+name]
  if name=='prometheus':address+=['prometheus:static_configs.targets=localhost:9090']
  else:address+=['kubernetes_sd:role=endpoints','relabel:__meta_kubernetes_endpoints_name=node-exporter']
  signals.append({'id':'signal:prometheus-job:'+name,'kind':'metric','entity':owner,'operation':None,'address':address,'shared':True,'provenance':[prov(prom,line,cond='Scrape address/config only; no runtime samples, series or host identity supplied. '+COND)]})
 else:open_items.append({'kind':'metric-job-dynamic-targets','job_name':name,'reason':'Kubernetes discovery chooses actual service/pod/node at runtime; do not invent host entities or copy shared metrics to every operation.','provenance':[prov(prom,line)]})
annotations=[]
for p in ['deployment/kubernetes-manifests/prometheus/node-exporter.yml','deployment/kubernetes-manifests/prometheus/prometheus.yml','deployment/kubernetes-manifests/quickstart-k8s/yamls/svc.yaml','deployment/kubernetes-manifests/quickstart-k8s/yamls/deploy.yaml.sample',sw]:
 for line_no,line in enumerate(read(p).splitlines(),1):
  if 'prometheus.io/' in line:annotations.append({'source_path':p,'line':line_no,'text':line.strip(),'provenance':[prov(p,line_no)]})
mysql_metric={'status':'DISABLED_BY_CHART_DEFAULT_SOURCE','evidence':[prov('deployment/kubernetes-manifests/quickstart-k8s/charts/mysql/values.yaml',114,129),prov('deployment/kubernetes-manifests/quickstart-k8s/charts/mysql/templates/service.yaml',86,105),prov('deployment/kubernetes-manifests/quickstart-k8s/charts/mysql/templates/servicemonitor.yaml',1,26)],'enabled':False,'serviceMonitor_enabled':False,'port_if_enabled':9104,'condition':'No declared enable override in deploy utils; actual Helm values/runtime remains OPEN. README table defaults are not substituted for values.yaml.'}
open_items.append({'kind':'mysql-metrics-conditional-disabled','detail':mysql_metric})
result={'scope':{'system':'RE2-TT','revision':COMMIT},'signals':signals,'coverage':{'current_java_files_read':len(javafiles),'java_source_modules':sorted(modules),'logger_calls':len(logger_calls),'logger_owner_service_count':len({s['entity'] for s in signals if s['kind']=='log'}),'shared_library_logger_count':len([x for x in open_items if x['kind']=='shared-library-logger-owner']),'config_files_screened':len(configfiles),'dedicated_log_config_paths':logconfigpaths,'skywalking_declared_owners':swowners,'source_files_verified_read_count':len(READ),'body_read_scope':'Only current Java source, runtime/deployment/build config; no sample, telemetry, data or images read.','raw_sample_independence':True},'logger_calls':logger_calls,'source_override_chains':chains,'metric_scrape_jobs':jobs,'metric_annotations':annotations,'mysql_metric_condition':mysql_metric,'open':open_items,'notes':'Each signals row uses exact T036 fields; auxiliary tables are source analysis outside document schema. Source addresses are declarations, not invented OTel keys or observed telemetry.'}
assert all(s['operation'] is None and s['shared'] for s in signals)
for filename,value in [('signals-supplement.json',result),('registry-additional.json',{'version':1,'sources':list(REG.values())})]:
 (OUT/filename).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'signals':len(signals),'by_kind':dict(collections.Counter(x['kind'] for x in signals)),'logger_calls':len(logger_calls),'shared_library_unassigned':3,'skywalking_owners':len(swowners),'metric_jobs':len(jobs),'source_files':len(READ),'registry_sources':len(REG)}))
