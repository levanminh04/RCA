#!/usr/bin/env python3
import base64
from collections import Counter, defaultdict
import datetime
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

role=sys.argv[1]
folder=Path('/opt/flash-ticket-app/collector/data' if role=='app' else '/opt/flash-ticket-obs/pinned/data/capture')
def value(v):
    for kind in ['stringValue','intValue','doubleValue','boolValue','bytesValue']:
        if kind in v: return v[kind]
    if 'kvlistValue' in v: return attrs(v['kvlistValue'].get('values',[]))
    if 'arrayValue' in v: return [value(x) for x in v['arrayValue'].get('values',[])]
    return None
def attrs(items): return {x['key']:value(x['value']) for x in items}
def documents(path):
    if not path.exists(): return
    with path.open() as f:
        for line in f:
            try: yield json.loads(line)
            except ValueError: pass # exporter may be appending its final line
spans={}
services=Counter(); kinds=Counter(); db=Counter(); messaging=Counter(); routes=Counter()
allowed={'http.route','http.request.method','http.response.status_code','server.address','server.port','db.system','db.system.name',
         'db.namespace','db.operation.name','db.collection.name','messaging.system','messaging.destination.name',
         'messaging.destination.routing_key','messaging.operation.type','messaging.message.id','messaging.rabbitmq.destination.routing_key'}
examples={}
for doc in documents(folder/'traces.jsonl'):
    for rs in doc.get('resourceSpans',[]):
        resource=attrs(rs.get('resource',{}).get('attributes',[]))
        svc=resource.get('service.name','?')
        for scope in rs.get('scopeSpans',[]):
            for span in scope.get('spans',[]):
                a=attrs(span.get('attributes',[]))
                record={k:span.get(k) for k in ['traceId','spanId','parentSpanId','name','kind','startTimeUnixNano','endTimeUnixNano','status']}
                record.update(service=svc,attributes={k:v for k,v in a.items() if k in allowed},
                              resource={k:v for k,v in resource.items() if k in ['service.name','service.instance.id','service.version','host.id','deployment.environment']},
                              instrumentation=scope.get('scope',{}).get('name'))
                spans[(span['traceId'],span['spanId'])]=record
                services[svc]+=1; kinds[str(span.get('kind'))]+=1
                for key in ['db.system.name','db.system']:
                    if key in a: db[str(a[key])]+=1; break
                if 'messaging.system' in a: messaging[str(a['messaging.system'])]+=1
                if a.get('http.route'): routes[svc+' '+str(a['http.route'])]+=1
                for category,condition in [('http_route',bool(a.get('http.route'))),('postgresql',any(a.get(k)=='postgresql' for k in ['db.system','db.system.name'])),
                                           ('redis',any(a.get(k)=='redis' for k in ['db.system','db.system.name'])),('rabbitmq',a.get('messaging.system')=='rabbitmq'),('mongodb',any(a.get(k)=='mongodb' for k in ['db.system','db.system.name']))]:
                    if condition and category not in examples: examples[category]=record
logcounts=Counter(); correlated=Counter(); joined=Counter(); examples_log=[]; totalwithids=0
for doc in documents(folder/'logs.jsonl'):
    for rl in doc.get('resourceLogs',[]):
        resource=attrs(rl.get('resource',{}).get('attributes',[])); svc=resource.get('service.name','?')
        for scope in rl.get('scopeLogs',[]):
            for record in scope.get('logRecords',[]):
                logcounts[svc]+=1
                body=value(record.get('body',{}))
                try: body=json.loads(body) if isinstance(body,str) else body
                except ValueError: body={}
                body=body if isinstance(body,dict) else {}
                a=attrs(record.get('attributes',[])); body=body or a.get('app',{})
                tid=body.get('traceId') or body.get('trace_id') or record.get('traceId')
                sid=body.get('spanId') or body.get('span_id') or record.get('spanId')
                if tid:
                    correlated[svc]+=1
                if tid and sid:
                    totalwithids+=1
                    match=(tid,sid) in spans
                    if match: joined[svc]+=1
                    if match and len(examples_log)<8:
                        examples_log.append({'service':svc,'trace_id':tid,'span_id':sid,'span_exists':True,
                                             'log_keys':sorted(body),'resource_host_id':resource.get('host.id'),
                                             'resource_instance_id':resource.get('service.instance.id')})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':role,'source_folder':str(folder),
        'unique_spans':len(spans),'services':dict(services),'kinds':dict(kinds),'db_systems':dict(db),'messaging_systems':dict(messaging),
        'http_routes':dict(routes),'examples':examples,'logs_by_service':dict(logcounts),'logs_with_trace_id':dict(correlated),
        'logs_with_both_ids':totalwithids,'logs_joined_to_span':dict(joined),'joined_log_examples':examples_log}
smoke=Path('/home/ubuntu/t058/smoke-api-agent.json')
if smoke.exists():
    target=json.loads(smoke.read_text())
    result['request_traces']=[]
    for req in target['checks']:
        chain=[s for s in spans.values() if s['traceId']==req['trace_id']]
        chain.sort(key=lambda x:int(x.get('startTimeUnixNano') or 0))
        result['request_traces'].append({'request':{k:req[k] for k in ['method','path','status','trace_id']},'spans':chain})

def get(url,auth=None):
    headers={'Authorization':auth} if auth else {}
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=20) as r:
        return json.load(r)
try:
    with urllib.request.urlopen('http://127.0.0.1:8888/metrics') as r: text=r.read().decode()
    result['collector_counters']=[line for line in text.splitlines() if not line.startswith('#') and any(word in line for word in ['receiver_accepted','receiver_refused','exporter_sent','exporter_send_failed','exporter_enqueue_failed','exporter_queue_size','exporter_queue_capacity'])]
except Exception as e: result['collector_counters_error']=type(e).__name__
if role=='obs':
    try:
        names=get('http://127.0.0.1:9090/api/v1/label/__name__/values')['data']
        result['prometheus_metric_names']=[x for x in names if re.match(r'(jvm_|http_|container_|system_|postgresql_|redis_|mongodb_|rabbitmq_|traces_)',x)]
        expressions=['count by (service_name) (http_server_request_duration_seconds_count)',
                     'count by (service_name) (jvm_memory_used_bytes)',
                     'count by (service_name) (traces_span_metrics_calls_total)',
                     'sum by (client,server) (traces_service_graph_request_total)']
        result['promql']={q:get('http://127.0.0.1:9090/api/v1/query?'+urllib.parse.urlencode({'query':q}))['data'] for q in expressions}
        result['loki_labels']=get('http://127.0.0.1:3100/loki/api/v1/labels')
        query=urllib.parse.urlencode({'query':'{service_name="booking-service"}','limit':10})
        data=get('http://127.0.0.1:3100/loki/api/v1/query_range?'+query)['data']
        result['loki_booking_streams']=len(data['result'])
        result['loki_booking_rows']=sum(len(x['values']) for x in data['result'])
        e=dict(line.split('=',1) for line in Path('/opt/flash-ticket-obs/grafana.env').read_text().splitlines() if '=' in line)
        basic='Basic '+base64.b64encode((e['GF_SECURITY_ADMIN_USER']+':'+e['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
        result['grafana_datasources']=[{k:d[k] for k in ['name','uid','type','url']} for d in get('http://10.0.0.215:3000/api/datasources',basic)]
        result['grafana_datasource_health']={uid:get('http://10.0.0.215:3000/api/datasources/uid/'+uid+'/health',basic) for uid in ['prometheus','loki','tempo']}
    except Exception as e:
        result['backend_query_error']=type(e).__name__+': '+str(e)[:200]
out=Path('/home/ubuntu/t058/telemetry-'+role+'.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['utc','role','unique_spans','services','kinds','db_systems','messaging_systems','logs_by_service','logs_with_trace_id','logs_joined_to_span']},indent=2))
if 'backend_query_error' in result: print('backend_query_error',result['backend_query_error'])
