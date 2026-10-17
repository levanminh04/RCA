"""Prepare T036-schema part document; leave unsupported SMTP outside the graph."""
from pathlib import Path
import hashlib, importlib.util, json

OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[4]
F=json.loads((OUT/'facts.json').read_text('utf-8'))
A=json.loads((ROOT/'results/T-038/runs/tai-nguon-001/manifest.json').read_text('utf-8'))
IDX={x['source_path']:x for x in A['files']}; sources={}
COND='Snapshot v1.0.0 tham khảo có điều kiện; chưa xác minh sinh RE2-TT hoặc deployment runtime.'
def prov(p,l,end=None,condition=None):
    row=IDX[p];b=(ROOT/row['path']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
    sid='TT:'+p
    sources[sid]={'id':sid,'kind':'doc' if p.endswith(('.md','.png')) else 'config' if any(z in p for z in ['application.y','deployment/']) or p.endswith(('.conf','Dockerfile')) else 'source-code','revision':A['commit'],'sha256':row['sha256'],'condition':COND,'path':row['path'],'source_path':p}
    return {'source_id':sid,'locator':f'{p}:L{l}'+(f'-L{end}' if end and end!=l else ''),'condition':condition or COND}
D={'scope':{'system':'RE2-TT','revision':A['commit']},'entities':[],'operations':[],'relations':[],'resource_bindings':[],'signals':[]}
def ent(id,name,typ,role,p,l,condition=None):D['entities'].append({'id':id,'name':name,'type':typ,'granularity':'logical','role':role,'provenance':[prov(p,l,condition=condition)]})
def resource_line(path,name,kind='Deployment'):
    return next(x['line'] for x in F['deployment_resources'] if x['source_path']==path and x['name']==name and x['kind'] in {'Deployment','DaemonSet','StatefulSet'})
for x in F['nonjava_entities']:ent(x['name'],x['name'],x['type'],'application service defined by source entrypoint',x['source_path'],x['line'])
ent('ts-order-service','ts-order-service','service','default HTTP target declared by voucher source','ts-voucher-service/server.py',51)
ent('ts-order-other-service','ts-order-other-service','service','default HTTP target declared by voucher source','ts-voucher-service/server.py',52)
ent('ts-gateway-service','ts-gateway-service','gateway','HTTP reverse proxy upstream for /api/v1/','ts-ui-dashboard/nginx.conf',40)
ent('mysql-logical:ts-ticket-office-service','ticket-office configured MySQL logical database','database','logical database selected by TICKET_OFFICE_MYSQL_DATABASE; actual value not checked','ts-ticket-office-service/bin/db.js',4)
ent('mysql-logical:ts-voucher-service','voucher configured MySQL logical database','database','logical database default ts-voucher-mysql; env override may change value','ts-voucher-service/server.py',131)
ent('rabbitmq:quickstart','rabbitmq','broker','logical broker release in quickstart; namespace not selected','deployment/kubernetes-manifests/quickstart-k8s/charts/rabbitmq/templates/configmap.yaml',4,'Release rabbitmq declared by utils.sh:22,42; ConfigMap rabbitmq_host and Service share release; namespace/generator runtime OPEN.')
ent('nacos:quickstart','nacos','service','service registry/discovery logical component; client transport OPEN','deployment/kubernetes-manifests/quickstart-k8s/charts/nacos/values.yaml',9)
ent('mysql-logical:nacos:quickstart','nacos logical configuration database','database','logical database declared by nacos chart; host/instance values are deployment conditions','deployment/kubernetes-manifests/quickstart-k8s/charts/nacos/values.yaml',22)
for id,name,typ,p,l,role in [
 ('skywalking:quickstart','skywalking','service','deployment/kubernetes-manifests/skywalking/skywalking.yml',18,'optional distributed tracing collector'),
 ('skywalking-ui:quickstart','skywalking-ui','service','deployment/kubernetes-manifests/skywalking/skywalking.yml',89,'optional distributed tracing UI'),
 ('elasticsearch:skywalking','elasticsearch','database','deployment/kubernetes-manifests/skywalking/es.yml',4,'optional Skywalking storage logical component'),
 ('prometheus:quickstart','prometheus','service','deployment/kubernetes-manifests/prometheus/prometheus.yml',261,'optional metrics collector'),
 ('grafana:quickstart','grafana','service','deployment/kubernetes-manifests/prometheus/grafana.yml',4,'optional metrics visualization'),
 ('node-exporter:quickstart','node-exporter','service','deployment/kubernetes-manifests/prometheus/node-exporter.yml',4,'optional node metrics exporter; host identity OPEN'),
 ('kube-state-metrics:quickstart','kube-state-metrics','service','deployment/kubernetes-manifests/prometheus/prometheus.yml',89,'optional Kubernetes state metrics'),
 ('alertmanager:quickstart','alertmanager','service','deployment/kubernetes-manifests/prometheus/alert-manager.yml',4,'optional alert routing'),
 ('alertsnitch:quickstart','alertsnitch','service','deployment/kubernetes-manifests/prometheus/alertsnitch.yml',39,'optional alert logging service'),
 ('mysql-logical:alertsnitch','alertsnitch logical MySQL database','database','deployment/kubernetes-manifests/prometheus/alertsnitch.yml',4,'optional alert history storage'),
 ('smtp.163.com','smtp.163.com','external','ts-notification-service/src/main/resources/application.yml',13,'external mail server source default; SMTP relation unsupported by T036')
]:
 actual_name='grafana-core' if name=='grafana' else 'alertsnitch-mysql' if id=='mysql-logical:alertsnitch' else name
 ent(id,name,typ,role,p,resource_line(p,actual_name) if p.startswith('deployment/') else l,'Optional source profile, not active deployment verified. '+COND)
for x in F['nonjava_operations']:D['operations'].append({'entity':x['owner'],'name':x['name'],'runtime_name':None,'provenance':[prov(x['source_path'],x['line'],x.get('end_line'))]})
def edge(id,s,t,typ,channel,p,l,end=None,op=None,condition=None):D['relations'].append({'id':id,'source':{'entity':s,'operation':op},'target':{'entity':t,'operation':None},'type':typ,'channel':channel,'messaging':None,'context':condition or COND,'provenance':[prov(p,l,end,condition)]})
edge('nonjava:office:mysql','ts-ticket-office-service','mysql-logical:ts-ticket-office-service','dữ-liệu','data','ts-ticket-office-service/bin/db.js',4,15,condition='createConnection uses env HOST/USER/PASSWORD/DATABASE; PORT env is read but not passed. Actual deployment value OPEN.')
edge('nonjava:voucher:mysql','ts-voucher-service','mysql-logical:ts-voucher-service','dữ-liệu','data','ts-voucher-service/server.py',131,154,op='POST /getVoucher',condition='Source logical MySQL default and VOUCHER_MYSQL_* overrides; shared instance unresolved.')
edge('nonjava:voucher:order','ts-voucher-service','ts-order-service','gọi-đồng-bộ','http','ts-voucher-service/server.py',49,66,op='POST /getVoucher',condition='queryOrderByIdAndType type!=0; ORDER_SERVICE_URL override may change default target.')
edge('nonjava:voucher:order-other','ts-voucher-service','ts-order-other-service','gọi-đồng-bộ','http','ts-voucher-service/server.py',49,66,op='POST /getVoucher',condition='queryOrderByIdAndType type==0; ORDER_OTHER_SERVICE_URL override may change default target.')
edge('nonjava:ui:gateway','ts-ui-dashboard','ts-gateway-service','gọi-đồng-bộ','http','ts-ui-dashboard/nginx.conf',40,42,condition='Nginx location /api/v1/ proxies to default gateway upstream; not all paths.')
D['signals']=[
 {'id':'signal:office:access-log','kind':'log','entity':'ts-ticket-office-service','operation':None,'address':['config:morgan','output:stdout','format:dev'],'shared':True,'provenance':[prov('ts-ticket-office-service/app.js',18)]},
 {'id':'signal:avatar:stdout','kind':'log','entity':'ts-avatar-service','operation':None,'address':['container:stdout-stderr','env:PYTHONUNBUFFERED=TRUE'],'shared':True,'provenance':[prov('ts-avatar-service/Dockerfile',9)]},
 {'id':'signal:skywalking:collector','kind':'trace','entity':'skywalking:quickstart','operation':None,'address':['config:SW_AGENT_COLLECTOR_BACKEND_SERVICES','endpoint:skywalking:11800'],'shared':True,'provenance':[prov('deployment/kubernetes-manifests/quickstart-k8s/yamls/sw_deploy.yaml.sample',38,49,'Only optional tracing sample; no operation-level or runtime telemetry claim.')]},
 {'id':'signal:node-exporter:scrape','kind':'metric','entity':'node-exporter:quickstart','operation':None,'address':['config:prometheus.io/scrape=true','config:prometheus.io/port=9100'],'shared':True,'provenance':[prov('deployment/kubernetes-manifests/prometheus/node-exporter.yml',6,10)]}
]
# Every related source in the broker chain is represented in registry for merge/review.
for x in F['messaging_binding_chain']['chain']:prov(x['source_path'],x['line'],x.get('end_line'),F['messaging_binding_chain']['condition'])
registry={'version':1,'sources':list(sources.values())}
mod_path=ROOT/'results/T-036/runs/kiem-r1-after-002/code/build.py'
t036=json.loads((ROOT/'results/T-036/manifest.json').read_text('utf-8'));row=next(x for x in t036['files'] if x['path']==mod_path.relative_to(ROOT).as_posix());assert hashlib.sha256(mod_path.read_bytes()).hexdigest()==row['sha256']
spec=importlib.util.spec_from_file_location('t036_pinned_build',mod_path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
e,o=mod.build(D,registry)
for name,obj in [('part-document.json',D),('part-registry.json',registry),('part-validation.json',{'ok':True,'entities':len(D['entities']),'operations':len(D['operations']),'relations':len(D['relations']),'signals':len(D['signals']),'entity_edges':len(e['edges']),'operation_edges':len(o['edges']),'unsupported_smtp_outside_graph':F['unsupported_relations'],'not_complete_inventory':True})]:
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ok':True,'entities':len(D['entities']),'operations':len(D['operations']),'relations':len(D['relations']),'signals':len(D['signals']),'sources':len(registry['sources'])}))
