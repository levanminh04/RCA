"""Write declared synthetic inputs; no graph API is imported or called."""
import json
from pathlib import Path

BASE=Path('D:/RCA-flashticket/results/T-037')
def prov():return [{'source_id':'FT-SYNTHETIC','locator':'fixture requirement oracle-v2.json','condition':'Tổng hợp kiểm hợp đồng, không telemetry hay operation FT thật'}]
def entity(i,t='service',g='logical'):return dict(id=i,name=i,type=t,granularity=g,role='synthetic fixture',provenance=prov())
def op(e,n):return dict(entity=e,name=n,runtime_name=None,provenance=prov())
def end(e,o=None):return dict(entity=e,operation=o)
def msg(q=None):return dict(broker='broker',broker_scope='synthetic-vhost',exchange='flash-ticket.v1',routing_key='event.cancelled.v1',queue=q)
def relation(i,s,t,typ,ch,m=None):return dict(id=i,source=s,target=t,type=typ,channel=ch,messaging=m,context='Synthetic, not runtime',provenance=prov())
doc=dict(scope=dict(system='synthetic-FT',revision='fixture-v2'),entities=[entity(i) for i in ['payment-service','booking-service','ticket-service']]+[entity('broker','broker'),entity('smtp','external'),entity('db-A','database'),entity('db-B','database'),entity('pg','database','instance')],
 operations=[op('payment-service','publish-synthetic'),op('ticket-service','consume-synthetic'),op('booking-service','expiry-synthetic'),op('payment-service','callback-synthetic')],relations=[],resource_bindings=[],signals=[])
doc['relations']=[relation('publish',end('payment-service','publish-synthetic'),end('broker'),'thông-điệp','publish',msg()),
 relation('consume-A',end('broker'),end('ticket-service','consume-synthetic'),'thông-điệp','consume',msg('q-A')),
 relation('consume-B',end('broker'),end('ticket-service','consume-synthetic'),'thông-điệp','consume',msg('q-B')),
 relation('data-A',end('booking-service','expiry-synthetic'),end('db-A'),'dữ-liệu','data'),
 relation('data-B',end('payment-service'),end('db-B'),'dữ-liệu','data')]
doc['resource_bindings']=[dict(id='bind-'+d,entity=d,resource='pg',relation='hosted_on',provenance=prov()) for d in ['db-A','db-B']]
doc['signals']=[dict(id='queue-'+q,kind='metric',entity='broker',operation=None,address=['broker','synthetic-vhost',q],shared=True,provenance=prov()) for q in ['q-A','q-B']]+[dict(id='pg-shared',kind='metric',entity='pg',operation=None,address=['instance','pg'],shared=True,provenance=prov())]
def span(tr,si,owner,name,kind='INTERNAL',attrs=None,parent='root',links=None):return dict(traceID=tr,spanID=si,parentSpanID=parent,serviceName=owner,operationName=name,startTime=100,duration=10,kind=kind,attributes=attrs or {},links=links or [])
def attrs(q=None,identity=False):
 a={'messaging.broker':'broker','messaging.broker_scope':'synthetic-vhost','messaging.exchange':'flash-ticket.v1','messaging.routing_key':'event.cancelled.v1','correlationId':'synthetic-same-transaction'}
 if q:a['messaging.queue']=q
 if identity:a.update({'messaging.identity_scope':'synthetic-publisher','messaging.identity_scope_verified':True,'messaging.message_id':'synthetic-message'})
 return a
cases={
 'callback-new-trace':[span('t-request','s1','payment-service','start-synthetic',attrs={'correlationId':'same'}),span('t-callback','s2','payment-service','callback-synthetic',attrs={'correlationId':'same'})],
 'scheduler-root':[span('t-expiry','s1','booking-service','expiry-synthetic',attrs={'correlationId':'same'})],
 'correlation-only-message':[span('t-p','p','payment-service','publish-synthetic','PRODUCER',attrs()),span('t-c','c','ticket-service','consume-synthetic','CONSUMER',attrs('q-A'))],
 'verified-fanout':[span('t-p','p','event-service','publish-synthetic','PRODUCER',attrs(identity=True))]+[span('t-'+x,'c',x,'consume-synthetic','CONSUMER',attrs('q-'+x,True)) for x in ['booking-service','payment-service','ticket-service']],
 'two-queues':[span('t-a','c','ticket-service','consume-synthetic','CONSUMER',attrs('q-A')),span('t-b','c','ticket-service','consume-synthetic','CONSUMER',attrs('q-B'))],
 'retry-same-operation':[span('t-r1','c1','ticket-service','consume-synthetic','CONSUMER',dict(attrs('q-A'),**{'messaging.attempt':1})),span('t-r2','c2','ticket-service','consume-synthetic','CONSUMER',dict(attrs('q-A'),**{'messaging.attempt':2}))]
}
value={'task':'T-037','purpose':'synthetic-only','static_document':doc,'trace_cases':cases,'universe':{'event-service':'service','payment-service':'service','booking-service':'service','ticket-service':'service','broker':'broker'},
 'comparison_cases':{'missing_operation_mapping':{'mapping':'entity identities only; deliberately no operation mapping'},'missing_scope_or_queue':{'broker_scope':None,'queue':None},'unknown_type':{'type':'gọi-chưa-phân-kiểu'}}}
with (BASE/'fixtures-runtime-v2.json').open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
print('fixtures saved before converter; no graph functions called')
