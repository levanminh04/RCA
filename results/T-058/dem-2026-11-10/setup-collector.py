#!/usr/bin/env python3
"""Create statistics-only DB users and local Collector config on exp-app."""
import json
import os
from pathlib import Path
import subprocess
import urllib.request
import base64
import ipaddress

os.umask(0o077)
app=Path('/opt/flash-ticket-app')
folder=app/'collector'
folder.mkdir(exist_ok=True)
(folder/'data').mkdir(exist_ok=True)
(folder/'data/queue').mkdir(exist_ok=True)
# Keycloak uses the repository's bridge network; Spring services use host mode.
network=json.loads(subprocess.check_output(['docker','network','inspect','flash-ticket-infra']))[0]
subnet=next(c['Subnet'] for c in network['IPAM']['Config'] if ':' not in c['Subnet'])
assert ipaddress.ip_network(subnet).is_private
rule=['INPUT','-s',subnet,'-d','10.0.0.158','-p','tcp','--dport','4318','-j','ACCEPT']
if subprocess.run(['sudo','iptables','-C',*rule],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
    subprocess.run(['sudo','iptables','-I','INPUT','2',*rule[1:]],check=True)
subprocess.run(['sudo','netfilter-persistent','save'],check=True,stdout=subprocess.DEVNULL)

def envread(path):
    return dict(line.split('=',1) for line in path.read_text().splitlines() if line and not line.startswith('#'))

def secret():
    return subprocess.check_output(['openssl','rand','-hex','24'],text=True).strip()

def checked(args, data=None):
    p=subprocess.run(args,input=data,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('Provisioning command failed; output withheld to protect credentials')
    return p.stdout

if not (folder/'collector.env').exists():
    root=envread(Path('/opt/flash-ticket-infra/.env'))
    env={k:secret() for k in ['POSTGRES_MONITOR_PASSWORD','MONGODB_MONITOR_PASSWORD','RABBITMQ_MONITOR_PASSWORD']}
    env['REDIS_PASSWORD']=root['REDIS_PASSWORD']
    sql=f"CREATE ROLE otel_monitor LOGIN PASSWORD '{env['POSTGRES_MONITOR_PASSWORD']}';\nGRANT pg_monitor TO otel_monitor;\n"
    for name in ['keycloak_db','event_db','booking_db','payment_db','ticket_db']:
        sql+=f'GRANT CONNECT ON DATABASE {name} TO otel_monitor;\n'
    checked(['docker','exec','-i','flash-ticket-infra-postgres-1','psql','-X','-v','ON_ERROR_STOP=1','-U',root['POSTGRES_USER'],'-d','postgres'],sql)
    js="const a=db.getSiblingDB('admin'); a.auth('user_admin',"+json.dumps(root['USER_DB_ADMIN_PASSWORD'])+"); a.createUser({user:'otel_monitor',pwd:"+json.dumps(env['MONGODB_MONITOR_PASSWORD'])+",roles:[{role:'clusterMonitor',db:'admin'}]}); print('MongoDB statistics user ready');"
    checked(['docker','exec','-i','flash-ticket-infra-user-db-1','mongosh','--quiet','--file','/dev/stdin'],js)
    basic=base64.b64encode((root['RABBITMQ_ADMIN_USERNAME']+':'+root['RABBITMQ_ADMIN_PASSWORD']).encode()).decode()
    for endpoint,body in [('/api/users/otel_monitor',{'password':env['RABBITMQ_MONITOR_PASSWORD'],'tags':'monitoring'}),
                          ('/api/permissions/%2F/otel_monitor',{'configure':'^$','write':'^$','read':'^$'})]:
        req=urllib.request.Request('http://127.0.0.1:15672'+endpoint,data=json.dumps(body).encode(),method='PUT',headers={'Authorization':'Basic '+basic,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=10) as response:
            assert response.status in [201,204]
    (folder/'collector.env').write_text(''.join(k+'='+v+'\n' for k,v in env.items()))
    (folder/'collector.env').chmod(0o600)

receivers={
 'otlp':{'protocols':{'grpc':{'endpoint':'127.0.0.1:4317'},'http':{'endpoint':'127.0.0.1:4318'}}},
 'otlp/keycloak':{'protocols':{'http':{'endpoint':'10.0.0.158:4318'}}},
 'docker_stats':{'endpoint':'unix:///var/run/docker.sock','collection_interval':'10s',
                 'excluded_images':['*pumba*','*toxiproxy*','*k6*','otel/opentelemetry-collector-contrib*'],
                 'container_labels_to_metric_labels':{'com.docker.compose.service':'service.name'}},
 'hostmetrics':{'root_path':'/hostfs','collection_interval':'10s','scrapers':{'cpu':{},'memory':{},'load':{},'disk':{},'network':{},'filesystem':{}}},
 'postgresql':{'endpoint':'127.0.0.1:5432','username':'otel_monitor','password':'${env:POSTGRES_MONITOR_PASSWORD}',
                'databases':['keycloak_db','event_db','booking_db','payment_db','ticket_db'],'collection_interval':'10s','tls':{'insecure':True}},
 'mongodb':{'hosts':[{'endpoint':'127.0.0.1:27017'}],'username':'otel_monitor','password':'${env:MONGODB_MONITOR_PASSWORD}',
             'collection_interval':'10s','tls':{'insecure':True}},
 'redis':{'endpoint':'127.0.0.1:6379','password':'${env:REDIS_PASSWORD}','collection_interval':'10s'},
 'rabbitmq':{'endpoint':'http://127.0.0.1:15672','username':'otel_monitor','password':'${env:RABBITMQ_MONITOR_PASSWORD}','collection_interval':'10s'},
 'prometheus/self':{'config':{'scrape_configs':[{'job_name':'local-collector','scrape_interval':'10s','static_configs':[{'targets':['127.0.0.1:8888']}]}]}},
}
ids=subprocess.check_output(['docker','ps','-aq'],text=True).split()
logs=[]
for container in json.loads(subprocess.check_output(['docker','inspect',*ids])):
    image=container['Config']['Image']
    svc=container['Config'].get('Labels',{}).get('com.docker.compose.service')
    if not image.startswith('ft-local/') or not svc:
        continue
    rid='filelog/'+svc
    logs.append(rid)
    receivers[rid]={
      'include':['/var/lib/docker/containers/'+container['Id']+'/'+container['Id']+'-json.log'],
      'start_at':'beginning','storage':'file_storage', 'include_file_path':True,
      'operators':[
        {'type':'json_parser','id':'docker','parse_to':'attributes.docker','timestamp':{'parse_from':'attributes.docker.time','layout_type':'gotime','layout':'2006-01-02T15:04:05.999999999Z07:00'}},
        {'type':'move','from':'attributes.docker.log','to':'body'},
        {'type':'add','field':'resource["service.name"]','value':svc},
        {'type':'add','field':'resource["service.instance.id"]','value':svc+'-1'},
        {'type':'json_parser','id':'spring','parse_from':'body','parse_to':'attributes.app','if':'body matches "^\\\\s*\\\\{"','on_error':'send'},
      ]}
config={
 'extensions':{'file_storage':{'directory':'/data/queue','create_directory':True},'health_check':{'endpoint':'127.0.0.1:13133'}},
 'receivers':receivers,
 'processors':{
   'memory_limiter':{'check_interval':'1s','limit_mib':384,'spike_limit_mib':64},
   'resource/host':{'attributes':[{'key':'host.id','value':'exp-app','action':'upsert'},{'key':'deployment.environment','value':'exp','action':'upsert'}]},
   'batch':{'timeout':'1s','send_batch_size':1024},
   'filter/health':{'error_mode':'ignore','traces':{'span':['attributes["http.route"] == "/actuator/health"']}},
   'transform/sanitize':{'error_mode':'ignore','trace_statements':[{'context':'span','statements':[
       'delete_key(attributes, "url.query")',
       'replace_pattern(attributes["url.full"], "[?].*", "") where attributes["url.full"] != nil',
       'replace_pattern(attributes["http.url"], "[?].*", "") where attributes["http.url"] != nil',
       'replace_pattern(attributes["http.target"], "[?].*", "") where attributes["http.target"] != nil',
   ]}]},
 },
 'exporters':{
   'otlp':{'endpoint':'10.0.0.215:4317','tls':{'insecure':True},
           'retry_on_failure':{'enabled':True,'initial_interval':'1s','max_interval':'30s','max_elapsed_time':'0s'},
           'sending_queue':{'enabled':True,'queue_size':1000,'storage':'file_storage'}},
   'file/traces':{'path':'/data/traces.jsonl','rotation':{'max_megabytes':100,'max_backups':10}},
   'file/logs':{'path':'/data/logs.jsonl','rotation':{'max_megabytes':50,'max_backups':5}},
 },
 'service':{'extensions':['file_storage','health_check'],
   'telemetry':{'metrics':{'readers':[{'pull':{'exporter':{'prometheus':{'host':'127.0.0.1','port':8888}}}}]}},
   'pipelines':{
     'traces':{'receivers':['otlp','otlp/keycloak'],'processors':['memory_limiter','filter/health','transform/sanitize','resource/host','batch'],'exporters':['otlp','file/traces']},
     'metrics':{'receivers':['otlp','otlp/keycloak','docker_stats','hostmetrics','postgresql','mongodb','redis','rabbitmq','prometheus/self'],'processors':['memory_limiter','resource/host','batch'],'exporters':['otlp']},
     'logs':{'receivers':logs,'processors':['memory_limiter','resource/host','batch'],'exporters':['otlp','file/logs']},
   }}
}
(folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
compose={'services':{'collector':{
  'image':'otel/opentelemetry-collector-contrib:0.165.0','container_name':'flash-ticket-collector','user':'0:0','network_mode':'host','restart':'unless-stopped','mem_limit':'512m',
  'command':['--config=/etc/otel/config.json'],'env_file':['collector.env'],
  'volumes':[str(folder/'config.json')+':/etc/otel/config.json:ro',str(folder/'data')+':/data',
             '/var/lib/docker/containers:/var/lib/docker/containers:ro','/var/run/docker.sock:/var/run/docker.sock:ro','/:/hostfs:ro'],
  'logging':{'driver':'json-file','options':{'max-size':'10m','max-file':'3'}}}}}
(folder/'compose.json').write_text(json.dumps(compose,indent=2)+'\n')
print('Local Collector config ready; log input allowlist contains',len(logs),'application containers; no injection or load-tool logs.')
