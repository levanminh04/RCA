#!/usr/bin/env python3
import json
import os
from pathlib import Path

base=Path('/opt/flash-ticket-obs/pinned')
base.mkdir(parents=True,exist_ok=True)
os.chmod(base,0o755)
def config(name,data):
    p=base/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.parent.chmod(0o755)
    p.write_text(json.dumps(data,indent=2)+'\n')
    p.chmod(0o644)

config('prometheus.json',{
 'global':{'scrape_interval':'10s'},
 'storage':{'tsdb':{'out_of_order_time_window':'30m'}},
 'otlp':{'promote_resource_attributes':['service.name','service.instance.id','host.id','deployment.environment','container.name','container.id','db.namespace','postgresql.database.name']},
 'scrape_configs':[{'job_name':'prometheus','static_configs':[{'targets':['127.0.0.1:9090']}]}]
})
config('loki.json',{
 'auth_enabled':False,'server':{'http_listen_port':3100,'grpc_listen_port':9096,'log_level':'warn'},
 'common':{'instance_addr':'127.0.0.1','path_prefix':'/loki',
           'storage':{'filesystem':{'chunks_directory':'/loki/chunks','rules_directory':'/loki/rules'}},
           'replication_factor':1,'ring':{'kvstore':{'store':'inmemory'}}},
 'schema_config':{'configs':[{'from':'2020-10-24','store':'tsdb','object_store':'filesystem','schema':'v13','index':{'prefix':'index_','period':'24h'}}]},
 'limits_config':{'allow_structured_metadata':True,'reject_old_samples_max_age':'48h'},
 'analytics':{'reporting_enabled':False}
})
config('tempo.json',{
 'target':'all','stream_over_http_enabled':True,
 'server':{'http_listen_port':3200,'log_level':'warn'},
 'distributor':{'receivers':{'otlp':{'protocols':{'grpc':{'endpoint':'0.0.0.0:4317'},'http':{'endpoint':'0.0.0.0:4318'}}}}},
 'storage':{'trace':{'backend':'local','wal':{'path':'/var/tempo/wal'},'local':{'path':'/var/tempo/blocks'}}},
 'usage_report':{'reporting_enabled':False}
})
extensions={'file_storage':{'directory':'/data/queue','create_directory':True},'health_check':{'endpoint':'127.0.0.1:13133'}}
processors={'memory_limiter':{'check_interval':'1s','limit_mib':640,'spike_limit_mib':128},'batch':{'timeout':'1s','send_batch_size':1024},
            'resource/obs':{'attributes':[{'key':'host.id','value':'exp-obs','action':'upsert'},{'key':'service.name','value':'central-collector','action':'upsert'}]}}
exporters={
 'otlp/tempo':{'endpoint':'127.0.0.1:14317','tls':{'insecure':True}},
 'otlp_http/prometheus':{'endpoint':'http://127.0.0.1:9090/api/v1/otlp'},
 'otlp_http/loki':{'endpoint':'http://127.0.0.1:3100/otlp'},
 'file/traces':{'path':'/data/capture/traces.jsonl','rotation':{'max_megabytes':100,'max_backups':20}},
 'file/logs':{'path':'/data/capture/logs.jsonl','rotation':{'max_megabytes':100,'max_backups':10}},
 'file/metrics':{'path':'/data/capture/metrics.jsonl','rotation':{'max_megabytes':100,'max_backups':20}},
}
for name in ['otlp/tempo','otlp_http/prometheus','otlp_http/loki']:
    exporters[name].update(retry_on_failure={'enabled':True,'max_elapsed_time':'0s'},
                           sending_queue={'enabled':True,'queue_size':1000,'storage':'file_storage'})
config('collector.json',{
 'extensions':extensions,
 'receivers':{'otlp':{'protocols':{'grpc':{'endpoint':'10.0.0.215:4317'},'http':{'endpoint':'10.0.0.215:4318'}}},
              'prometheus/self':{'config':{'scrape_configs':[{'job_name':'central-collector','scrape_interval':'10s','static_configs':[{'targets':['127.0.0.1:8888']}]}]}}},
 'processors':processors,
 'connectors':{'span_metrics':{'histogram':{'unit':'s'},'dimensions':[{'name':'http.route'},{'name':'http.request.method'}],
                              'metrics_flush_interval':'10s','add_resource_attributes':True},
                'service_graph':{'dimensions':['db.system.name','messaging.system'],'metrics_flush_interval':'10s','store':{'ttl':'10s','max_items':50000}}},
 'exporters':exporters,
 'service':{'extensions':list(extensions),
             'telemetry':{'metrics':{'readers':[{'pull':{'exporter':{'prometheus':{'host':'127.0.0.1','port':8888}}}}]}},
             'pipelines':{
               'traces':{'receivers':['otlp'],'processors':['memory_limiter','batch'],'exporters':['otlp/tempo','span_metrics','service_graph','file/traces']},
               'metrics':{'receivers':['otlp','span_metrics','service_graph'],'processors':['memory_limiter','batch'],'exporters':['otlp_http/prometheus','file/metrics']},
               'metrics/self':{'receivers':['prometheus/self'],'processors':['resource/obs','batch'],'exporters':['otlp_http/prometheus']},
               'logs':{'receivers':['otlp'],'processors':['memory_limiter','batch'],'exporters':['otlp_http/loki','file/logs']},
             }}
})
datasources=[
 {'name':'Prometheus','uid':'prometheus','type':'prometheus','access':'proxy','url':'http://prometheus:9090','isDefault':True,'jsonData':{'httpMethod':'POST'}},
 {'name':'Loki','uid':'loki','type':'loki','access':'proxy','url':'http://loki:3100','jsonData':{'derivedFields':[{'name':'TraceID','matcherRegex':'"traceId"\\s*:\\s*"([a-f0-9]{32})"','datasourceUid':'tempo','url':'$${__value.raw}'}]}},
 {'name':'Tempo','uid':'tempo','type':'tempo','access':'proxy','url':'http://tempo:3200','jsonData':{'httpMethod':'GET','serviceMap':{'datasourceUid':'prometheus'},'tracesToLogsV2':{'datasourceUid':'loki','spanStartTimeShift':'-1m','spanEndTimeShift':'1m','tags':[{'key':'service.name','value':'service_name'}],'filterByTraceID':True}}},
]
config('provisioning/datasources/sources.yaml',{'apiVersion':1,'datasources':datasources})
services={
 'prometheus':{'image':'prom/prometheus:v3.16.0','mem_limit':'1536m','command':['--config.file=/etc/prometheus/config.json','--web.enable-otlp-receiver','--storage.tsdb.path=/prometheus','--storage.tsdb.retention.time=48h'],
               'ports':['127.0.0.1:9090:9090'],'volumes':[str(base/'prometheus.json')+':/etc/prometheus/config.json:ro','prometheus-data:/prometheus']},
 'loki':{'image':'grafana/loki:3.7.9','mem_limit':'1g','user':'0:0','command':['-config.file=/etc/loki/config.json'],
         'ports':['127.0.0.1:3100:3100'],'volumes':[str(base/'loki.json')+':/etc/loki/config.json:ro','loki-data:/loki']},
 'tempo':{'image':'grafana/tempo:3.1.1','mem_limit':'2g','user':'0:0','command':['--config.file=/etc/tempo/config.json'],
          'environment':{'GOMEMLIMIT':'1536MiB'},'ports':['127.0.0.1:3200:3200','127.0.0.1:14317:4317'],
          'volumes':[str(base/'tempo.json')+':/etc/tempo/config.json:ro','tempo-data:/var/tempo']},
 'grafana':{'image':'grafana/grafana:13.3.0','mem_limit':'768m','env_file':['/opt/flash-ticket-obs/grafana.env'],
            'ports':['10.0.0.215:3000:3000'],'volumes':['grafana-data:/var/lib/grafana',str(base/'provisioning')+':/etc/grafana/provisioning:ro']},
 'collector':{'image':'otel/opentelemetry-collector-contrib:0.165.0','mem_limit':'768m','user':'0:0','network_mode':'host',
              'command':['--config=/etc/otel/config.json'],'volumes':[str(base/'collector.json')+':/etc/otel/config.json:ro',str(base/'data')+':/data']},
}
for name,service in services.items():
    service.update(container_name='flash-ticket-obs-'+name,restart='unless-stopped',logging={'driver':'json-file','options':{'max-size':'10m','max-file':'3'}})
config('compose.json',{'services':services,'volumes':{x+'-data':{} for x in ['prometheus','loki','tempo','grafana']}})
(base/'data/capture').mkdir(parents=True,exist_ok=True)
(base/'data/queue').mkdir(parents=True,exist_ok=True)
print('Prepared independently pinned five-container observability stack; LGTM remains running until deployment switch')
