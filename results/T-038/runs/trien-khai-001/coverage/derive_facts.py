"""Derive source facts from verified application/configuration only; no sample telemetry."""
from pathlib import Path
import collections, hashlib, json, re
import yaml

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
BASE=ROOT/'results/T-038/sources/train-ticket-v1.0.0'
M=json.loads((ROOT/'results/T-038/runs/tai-nguon-001/manifest.json').read_text('utf-8'))
IDX={x['source_path']:x for x in M['files']}
COMMIT=M['commit']
def read(path):
    assert not path.startswith('old-docs/Json2Shiviz/example/')
    assert not path.startswith(('old-docs/Json2Shiviz/bin/ts-large-output/','old-docs/Json2Shiviz/bin/ts-large-sample/'))
    b=(BASE/path).read_bytes();x=IDX[path]
    assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
    return b.decode('utf-8-sig')
def locator(p,l=None):return f'https://github.com/FudanSELab/train-ticket/blob/{COMMIT}/{p}'+(f'#L{l}' if l else '')
def evidence(p,line,end=None):
    lines=read(p).splitlines();return {'source_path':p,'line':line,'end_line':end or line,'locator':locator(p,line),'text':'\n'.join(lines[line-1:(end or line)])}
facts={'task':'T-038','commit':COMMIT,'scientific_status':'Snapshot tham khảo có điều kiện; chưa xác minh sinh RE2-TT.','raw_sample_independence':'Không dùng telemetry mẫu hoặc đầu ra nghiên cứu lịch sử để tạo facts. Đầu vào derive_facts.py chỉ source runtime/config/deployment đã kiểm manifest.','nonjava_entities':[],'nonjava_operations':[],'relations':[],'runtime_config':[],'deployment_resources':[],'deployment_profiles':[],'external_sources':[],'unsupported_relations':[],'source_limitations':[]}
def ent(name,typ,p,l,condition='Source entrypoint; deployment/profile cần xác định riêng.'):
    facts['nonjava_entities'].append({'name':name,'type':typ,'status':'FACT_SOURCE','condition':condition,**evidence(p,l)})
def op(owner,name,p,l,end=None):facts['nonjava_operations'].append({'owner':owner,'name':name,'runtime_name_verified':False,'status':'FACT_SOURCE_HANDLER','condition':'Khai báo handler nguồn; chưa chứng minh tên operation trong telemetry.',**evidence(p,l,end)})
def rel(source,target,typ,p,l,end=None,condition='',address=None):facts['relations'].append({'source':source,'target':target,'type':typ,'status':'FACT_SOURCE','condition':condition,'address':address,**evidence(p,l,end)})
for name,p,l in [('ts-avatar-service','ts-avatar-service/app.py',12),('ts-news-service','ts-news-service/src/main/main.go',50),('ts-ticket-office-service','ts-ticket-office-service/app.js',10),('ts-voucher-service','ts-voucher-service/server.py',99),('ts-ui-dashboard','ts-ui-dashboard/nginx.conf',25)]:ent(name,'service',p,l)
op('ts-avatar-service','POST /api/v1/avatar','ts-avatar-service/app.py',25,26)
op('ts-news-service','GET /(.*)','ts-news-service/src/main/main.go',51,52)
op('ts-voucher-service','POST /getVoucher','ts-voucher-service/server.py',99,102)
for verb,path,line in [('GET','/',9),('GET','/getRegionList',22),('GET','/getAll',31),('POST','/getSpecificOffices',39),('POST','/addOffice',49),('POST','/deleteOffice',58),('POST','/updateOffice',67)]:op('ts-ticket-office-service',verb+' /office'+('' if path=='/' else path),'ts-ticket-office-service/bin/router.js',line)
rel('ts-ticket-office-service','${TICKET_OFFICE_MYSQL_HOST}','database','ts-ticket-office-service/bin/db.js',4,15,'Đọc HOST/PORT/USER/PASSWORD/DATABASE từ env; createConnection không truyền PORT; không mặc định đích là Mongo.',{'host':'${TICKET_OFFICE_MYSQL_HOST}','database':'${TICKET_OFFICE_MYSQL_DATABASE}','port':'driver default; env PORT not passed'})
rel('ts-voucher-service','ts-voucher-mysql','database','ts-voucher-service/server.py',131,154,'Default nguồn; env VOUCHER_MYSQL_* có thể thay host/port/database.',{'host':'ts-voucher-mysql','port':3306,'database':'ts-voucher-mysql'})
rel('ts-voucher-service','ts-order-service','sync','ts-voucher-service/server.py',49,66,'type != 0; ORDER_SERVICE_URL có thể thay địa chỉ.',{'transport':'HTTP','base_url':'http://ts-order-service:12031','path':'/api/v1/orderservice/order/{orderId}'})
rel('ts-voucher-service','ts-order-other-service','sync','ts-voucher-service/server.py',49,66,'type == 0; ORDER_OTHER_SERVICE_URL có thể thay địa chỉ.',{'transport':'HTTP','base_url':'http://ts-order-other-service:12032','path':'/api/v1/orderOtherService/orderOther/{orderId}'})
rel('ts-ui-dashboard','ts-gateway-service','sync','ts-ui-dashboard/nginx.conf',40,42,'Chỉ location /api/v1/ trong cấu hình Nginx này.',{'transport':'HTTP','base_url':'http://ts-gateway-service:18888'})
facts['source_limitations'].append({'kind':'commented-code-not-active-relation','subject':'ts-news-service → MongoDB','conclusion':'Khối MongoDB bị comment; không ghi cạnh DB hiện hành từ khối này.',**evidence('ts-news-service/src/main/main.go',10,35)})
facts['unsupported_relations'].append({'source':'ts-notification-service','target':'smtp.163.com','target_type':'external','relation':'SMTP mail send','address':{'host':'smtp.163.com','port':465,'transport':'SMTP/TLS'},'status':'UNSUPPORTED_T036_RELATION_ENUM','condition':'Default cấu hình mail; không suy đã gửi thật hoặc là transport HTTP/RPC.','source_chain':[evidence('ts-notification-service/src/main/resources/application.yml',12,14),evidence('ts-notification-service/src/main/java/notification/service/MailService.java',22,23),evidence('ts-notification-service/src/main/java/notification/service/MailService.java',30,46),evidence('ts-notification-service/src/main/java/notification/mq/RabbitReceive.java',78,90)],'impact':'Giữ external/address và phản ví dụ; không ép thành sync/http/rpc để vượt schema. Phần phụ thuộc nghĩa cạnh cần Minh quyết hợp đồng chung.'})
facts['deployment_profiles']=[
 {'profile':'README make deploy / quickstart Kubernetes','status':'SOURCE_DOCUMENTED_DEFAULT','condition':'Cây release v1.0.0, chưa chứng minh RE2 deployment.','evidence':[evidence('README.md',33,36),evidence('Makefile',31,38),evidence('hack/deploy/deploy.sh',18,24),evidence('hack/deploy/utils.sh',30,44)]},
 {'profile':'quickstart --with-tracing','trace_backend':'Skywalking + Elasticsearch','condition':'Bật tùy chọn; không gán Jaeger từ profile lịch sử.','evidence':[evidence('Makefile',34),evidence('hack/deploy/deploy.sh',60,65),evidence('hack/deploy/utils.sh',53,56),evidence('deployment/kubernetes-manifests/skywalking/skywalking.yml',4,9)]},
 {'profile':'quickstart --with-monitoring','monitoring':'Prometheus + Grafana','condition':'Bật tùy chọn; không chứng minh metric đã thu.','evidence':[evidence('Makefile',33),evidence('hack/deploy/utils.sh',48,50)]},
 {'profile':'root docker-compose / old Jaeger / Istio / EFK / PVC-NFS','status':'ALTERNATIVE_OR_HISTORICAL_SOURCE_PROFILES','condition':'Giữ riêng theo source_path; không hợp tất cả thành một deployment thực tế.','evidence':[evidence('.env',1,3),evidence('deployment/docker-compose-manifests/README.md',1)]}
]

def nodes(node,prefix=()):
    if isinstance(node,yaml.MappingNode):
        for k,v in node.value:yield from nodes(v,prefix+(str(k.value),))
    elif isinstance(node,yaml.SequenceNode):
        for i,v in enumerate(node.value):yield from nodes(v,prefix+(str(i),))
    else:yield prefix,node.value,node.start_mark.line+1
for path in IDX:
    # Exact runtime configuration + all deployment YAML, including sample templates as text.
    app=bool(re.match(r'^ts-[^/]+/src/main/resources/application\.ya?ml$',path))
    deployment=path.startswith('deployment/') and path.endswith(('.yml','.yaml','.sample'))
    if not (app or deployment or path=='docker-compose.yml'):continue
    text=read(path)
    try:
        docs=list(yaml.compose_all(text,Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        facts['source_limitations'].append({'kind':'template-not-rendered','source_path':path,'locator':locator(path),'status':'OPEN','reason':'Helm/template YAML chưa render; giữ dòng nguồn trong content-index sạch; không chạy source.','parser_error':str(exc)[:500]});continue
    for doc_no,doc in enumerate(docs):
        if doc is None:continue
        leaves=list(nodes(doc));flat={p:(v,l) for p,v,l in leaves}
        if app:
            for keys,val,line in leaves:
                k='.'.join(keys)
                if any(s in k.lower() for s in ['password','username']):continue
                if any(s in k.lower() for s in ['datasource.url','nacos','rabbitmq','mail.host','mail.port','server.port','application.name','management','logging','sentinel']):
                    facts['runtime_config'].append({'owner':path.split('/')[0],'key':k,'value':val,'source_path':path,'line':line,'locator':locator(path,line),'condition':'Cấu hình nguồn/default và placeholder; không phải giá trị runtime đã xác minh.'})
        if deployment:
            kind=flat.get(('kind',),(None,None))[0];name,nline=flat.get(('metadata','name'),(None,None))
            if kind and name:
                resources={'.'.join(k):v for k,v,l in leaves if any(t in k for t in ['image','containerPort','port','targetPort','nodePort','host','hostPath']) or (k[-1:] in [('name',),('value',)] and any('env' in x.lower() for x in k))}
                facts['deployment_resources'].append({'kind':kind,'name':name,'source_path':path,'line':nline,'locator':locator(path,nline),'document_index':doc_no,'values':resources,'condition':'Chỉ thực thể/cấu hình của profile ở source_path; không mặc định active.'})

facts['external_sources']=[
 {'source':'Wiki Installation Guide','kind':'documentation-not-in-tree','status':'OPEN_NOT_FETCHED','need':'Đối chiếu cách build/runtime ngoài snapshot nếu cần tuyên bố deployment đầy đủ.','evidence':evidence('README.md',87,90)},
 {'source':'train-ticket-auto-query','kind':'workload-external-repository','status':'OPEN_NOT_FETCHED','need':'Workload không nằm trong snapshot; không cần để đọc inventory code, cần khi quy thiếu cạnh do nhánh chưa chạy.','evidence':evidence('README.md',92,93)},
 {'source':'Container images / base images / package registries / Maven / Go modules','kind':'build-and-runtime-external','status':'OPEN_NOT_FETCHED','need':'Tag và POM/requirements/package lock là khai báo; không chứng minh digest hoặc source instrumentation trong image.','evidence':[evidence('ts-avatar-service/Dockerfile',1),evidence('ts-news-service/Dockerfile',1),evidence('deployment/kubernetes-manifests/quickstart-k8s/charts/rabbitmq/values.yaml',9,15)]},
 {'source':'RE2 application/instrumentation/deployment lineage','kind':'dataset-to-application','status':'OPEN','need':'Manifest/digest/source instrumentation sinh RE2-TT; không chọn revision theo graph.'}
]
facts['source_limitations'].extend([
 {'kind':'generated-deployment-not-executed','status':'OPEN','reason':'Đọc template và generator; không chạy script hoặc Helm. Giá trị all-in-one/independent DB có điều kiện.','evidence':[evidence('hack/deploy/gen-mysql-secret.sh',43,62),evidence('hack/deploy/utils.sh',59,86)]},
 {'kind':'source-script-literal-condition','status':'FACT_SOURCE_NOT_RUNTIME','reason':'Điều kiện ghi useOneHost không có $; không tự sửa hoặc nhận host theo ý định comment.','evidence':evidence('hack/deploy/gen-mysql-secret.sh',58,61)},
 {'kind':'source-script-os-condition','status':'FACT_SOURCE_NOT_RUNTIME','reason':'Toán tử = không tách khoảng; chưa chạy source để xác nhận hậu quả.','evidence':[evidence('hack/deploy/gen-mysql-secret.sh',69,76),evidence('hack/deploy/gen-mysql-secret.sh',84,90)]},
 {'kind':'architecture-visual-root','status':'FACT_DIRECT_VISUAL_REPORTED_BY_ROOT','source_path':'image/2.png','line':None,'locator':locator('image/2.png'),'observer':'root agent, message supplied during task','observed':['Gateway','Nacos + Sentinel','Prometheus/Grafana','Skywalking + Elasticsearch','MySQL','RabbitMQ','avatar/news/ticket-office/voucher','wait-order'],'condition':'Sơ đồ tổng quát; không biến mọi mũi tên thành cạnh code hoặc đồng nhất với profile lịch sử.'}
])
facts['messaging_binding_chain']={
 'profile':'README make deploy / quickstart Kubernetes',
 'logical_broker':'rabbitmq','broker_scope':None,'scope_status':'OPEN_NAMESPACE_NOT_SELECTED',
 'condition':'Nguồn nối release → chart ConfigMap → envFrom. Chưa render/run generator hoặc chứng minh deployment RE2. Không gộp localhost của các service thành một instance.',
 'chain':[evidence('hack/deploy/utils.sh',21,22),evidence('hack/deploy/utils.sh',41,44),evidence('hack/deploy/utils.sh',102,106),evidence('hack/deploy/gen-mysql-secret.sh',65,76),evidence('deployment/kubernetes-manifests/quickstart-k8s/charts/rabbitmq/templates/configmap.yaml',1,7),evidence('deployment/kubernetes-manifests/quickstart-k8s/charts/rabbitmq/templates/service.yaml',1,10),evidence('deployment/kubernetes-manifests/quickstart-k8s/charts/rabbitmq/values.yaml',9,15)],
 'deployment_env_from':[], 'active_application_config':[], 'queue_roles':[]}
for owner,line in [('ts-delivery-service',628),('ts-food-service',716),('ts-notification-service',936),('ts-preserve-other-service',1116),('ts-preserve-service',1160)]:
 facts['messaging_binding_chain']['deployment_env_from'].append({'owner':owner,**evidence('deployment/kubernetes-manifests/quickstart-k8s/yamls/deploy.yaml.sample',line-4,line+2)})
 facts['messaging_binding_chain']['active_application_config'].extend(x for x in facts['runtime_config'] if x['owner']==owner and x['key'].startswith('spring.rabbitmq.'))
for owner,pkg,role,queue,line in [('ts-delivery-service','delivery','consume','food_delivery',35),('ts-food-service','foodsearch','publish','food_delivery',21),('ts-notification-service','notification','publish','email',20),('ts-notification-service','notification','consume','email',51),('ts-preserve-service','preserve','publish','email',20),('ts-preserve-other-service','preserveOther','publish','email',22)]:
 file='RabbitReceive.java' if role=='consume' else 'RabbitSend.java'
 facts['messaging_binding_chain']['queue_roles'].append({'owner':owner,'role':role,'queue':queue,'exchange':None,'routing_key':None,'identity_scope':None,'condition':'Khai báo nguồn; không xác minh message instance hoặc delivery runtime. Overload AmqpTemplate cần giữ đúng nghĩa, không tự thêm exchange/routing.','evidence':[evidence(owner+'/src/main/java/'+pkg+'/config/Queues.java',10,14),evidence(owner+'/src/main/java/'+pkg+'/mq/'+file,line)]})
quick=[x for x in facts['deployment_resources'] if x['source_path']=='deployment/kubernetes-manifests/quickstart-k8s/yamls/deploy.yaml.sample']
svcs=[x for x in facts['deployment_resources'] if x['source_path']=='deployment/kubernetes-manifests/quickstart-k8s/yamls/svc.yaml']
facts['source_limitations'].append({'kind':'deployment-template-service-difference','status':'FACT_SOURCE','deployment_count':len(quick),'service_count':len(svcs),'deployment_without_service':sorted({x['name'] for x in quick}-{x['name'] for x in svcs}),'condition':'Không suy service không tồn tại hoặc không chạy; khai báo Deployment khác Kubernetes Service.','locators':{'deployments':[x for x in quick if x['name'] in {'ts-food-delivery-service','ts-wait-order-service'}],'services_source':locator('deployment/kubernetes-manifests/quickstart-k8s/yamls/svc.yaml')}})
mysql_vendor=[p for p in IDX if p.startswith('ts-ticket-office-service/node_modules/mysql/')]
facts['source_limitations'].append({'kind':'declared-dependency-vs-vendor-tree','status':'FACT_SOURCE','declared':'mysql ^2.18.1','vendor_mysql_paths':mysql_vendor,'condition':'Tree không có module mysql dưới node_modules/mysql; không chạy source, base image có thể khác; giữ runtime dependency OPEN.','evidence':[evidence('ts-ticket-office-service/package.json',15,18),evidence('ts-ticket-office-service/bin/db.js',4,15),evidence('ts-ticket-office-service/Dockerfile',8,15)]})
facts['signal_declarations']=[
 {'owner':'ts-avatar-service','kind':'stdout/stderr','address':'container stdout/stderr','condition':'Docker Python unbuffered; chưa có schema log/runtime trace/span correlation.','evidence':evidence('ts-avatar-service/Dockerfile',9)},
 {'owner':'ts-ticket-office-service','kind':'access-log','address':'morgan dev stdout','condition':'Logger middleware; không tự coi log gắn trace/span.','evidence':evidence('ts-ticket-office-service/app.js',17,20)},
 {'owner':'Java service deployments','kind':'trace-agent','address':'skywalking:11800','condition':'Chỉ sw_deploy sample và tùy chọn --with-tracing; không tự áp vào nonJava hoặc RE2.','evidence':evidence('deployment/kubernetes-manifests/quickstart-k8s/yamls/sw_deploy.yaml.sample',21,65)},
 {'owner':'monitoring infrastructure','kind':'metrics','address':'Prometheus/Grafana/node exporter/kube-state-metrics','condition':'Khai báo triển khai và scrape; runtime series/nhãn/host mapping chưa kiểm.','evidence':[evidence('hack/deploy/utils.sh',48,50),evidence('deployment/kubernetes-manifests/prometheus/node-exporter.yml',6,10)]},
 {'owner':'Nacos discovery','kind':'service-registry-address','address':'spring.cloud.nacos.discovery.server-addr','condition':'Địa chỉ có source config; không gán HTTP/RPC khi chưa đọc implementation của client library ngoài snapshot.','evidence':evidence('ts-gateway-service/src/main/resources/application.yml',10,13)}
]
external_refs=[]
for path in IDX:
 if '/node_modules/' in path or path.startswith('old-docs/'):continue
 if path.endswith(('Dockerfile','pom.xml','requirements.txt','package.json')) or path in ['build_upload_image.py','hack/build-image.sh']:
  for line_no,line in enumerate(read(path).splitlines(),1):
   if re.search(r'(^FROM |<groupId>|<artifactId>|<version>|pip install|"[a-z@][a-z0-9@/_-]*"\s*:\s*"[~^<>=*0-9]|^[a-zA-Z][a-zA-Z0-9_-]*(?:==[^ ]+)?$)',line):
    external_refs.append({'source_path':path,'line':line_no,'text':line,'locator':locator(path,line_no),'status':'DECLARED_NOT_RETRIEVED_OR_EXECUTED'})
(OUT/'external-references.json').write_text(json.dumps({'commit':COMMIT,'references':external_refs},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:len(v) for k,v in facts.items() if isinstance(v,list)},ensure_ascii=False))
