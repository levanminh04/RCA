"""Ghi fixture và đáp án từ các literal, trước khi có bộ dựng. Không import bộ dựng."""
import json
from pathlib import Path

def span(s, e, p='', op=None, t='t', start=0, end=10, kind=None, attrs=None, links=None):
    return dict(traceID=t,spanID=s,parentSpanID=p,serviceName=e,operationName=op or s,
                startTime=start,duration=end-start,kind=kind,attributes=attrs or {},links=links or [])

U={'A':'service','B':'service','C':'service','db':'database','cache':'cache','mq':'broker',
   'partner':'external','host':'host'}
def case(name,rows,edges,internal=0,roots=None,orphans=0,duplicate=0,error=None):
    return dict(name=name,spans=rows,universe=U,expected=dict(edges=edges,internal=internal,
        roots=roots,orphans=orphans,duplicate=duplicate,error=error))
u='gọi-chưa-phân-kiểu'; sync='gọi-đồng-bộ'; data='dữ-liệu';msg='thông-điệp';deploy='triển-khai'
rows=[]
rows.append(case('F1',[span('a','A',end=100),span('b','B','a',start=10,end=50),span('c','C','a',start=20,end=60)], [['A','B',u],['A','C',u]],roots=1))
rows.append(case('F2',[span('a','A',attrs={'db.entity':'db','db.type':'database'}),span('b','B',attrs={'db.entity':'db','db.type':'database'}),span('c','A',attrs={'db.entity':'cache','db.type':'cache'})],[['A','db',data],['B','db',data],['A','cache',data]],roots=3))
ma={'messaging.broker':'mq','messaging.destination':'orders','messaging.message_id':'m1'}
link={'traceID':'send','spanID':'p','semantics':'message_creation','semantics_verified':True}
rows.append(case('F3',[span('p','A',t='send',kind='PRODUCER',attrs=ma),span('c','B',t='receive',start=20,end=30,kind='CONSUMER',attrs=ma,links=[link])],[['A','mq',msg],['mq','B',msg],['A','B',msg]],roots=2))
rows.append(case('F4',[span('p','A',t='send',kind='PRODUCER',attrs=ma),span('c1','B',t='r1',start=20,end=30,kind='CONSUMER',attrs=dict(ma,**{'messaging.attempt':1}),links=[link]),span('c2','B',t='r2',start=40,end=50,kind='CONSUMER',attrs=dict(ma,**{'messaging.attempt':2}),links=[link])],[['A','mq',msg],['mq','B',msg],['A','B',msg]],roots=3))
rows.append(case('F5',[span('a','A',op='saga',end=100),span('b','B','a',op='charge',start=10,end=20),span('c','C','a',op='issue',start=30,end=40),span('b2','B','a',op='refund-compensation',start=50,end=60)],[['A','B',u],['A','C',u]],roots=1))
rows.append(case('F6',[span('client','A',t='out',kind='CLIENT',attrs={'peer.entity':'partner','peer.type':'external'}),span('callback','A',t='new',op='callback-validate',start=100,end=110)],[['A','partner',sync]],roots=2))
rows.append(case('F7',[span('timer','A',op='expiry-scheduler')],[],roots=1))
rows.append(case('F8',[span('a','A',end=100),span('b','B','a',start=10,end=80),span('a2','A','b',start=20,end=50)],[['A','B',u],['B','A',u]],roots=1))
rows.append(case('F9',[span('a','A',end=100),span('inner','A','a',start=10,end=80),span('inner2','A','inner',start=20,end=50)],[],internal=2,roots=1))
rows.append(case('F10-orphan',[span('a','A','missing'),span('x','outside')],[],roots=1,orphans=1))
dup=span('a','A');rows.append(case('F10-duplicate',[dup,dict(dup)],[],roots=1,duplicate=1))
rows.append(case('F10-conflict',[dup,dict(dup,serviceName='B')],[],error='duplicate_conflict'))
rows.append(case('F10-empty',[],[],roots=0))
rows.append(case('F10-invalid',[dict(dup,duration=-1)],[],error='invalid_time'))
rows.append(case('F11',[span('a','A',attrs={'host.id':'host','host.identity_verified':True}),span('b','B',attrs={'host.id':'host','host.identity_verified':True})],[['A','host',deploy],['B','host',deploy]],roots=2))
# Phản ví dụ cho điều kiện nối: cùng giao dịch, thiếu ID; nhiều producer cùng ID.
rows.append(case('message-correlation-only',[span('p','A',kind='PRODUCER',attrs={'messaging.broker':'mq','messaging.destination':'orders','correlationId':'order'}),span('c','B',t='r',kind='CONSUMER',attrs={'messaging.broker':'mq','messaging.destination':'orders','correlationId':'order'})],[['A','mq',msg],['mq','B',msg]],roots=2))
rows.append(case('message-ambiguous',[span('p','A',t='s1',kind='PRODUCER',attrs=ma),span('p2','C',t='s2',kind='PRODUCER',attrs=ma),span('c','B',t='r',kind='CONSUMER',attrs=ma)],[['A','mq',msg],['C','mq',msg],['mq','B',msg]],roots=3))
rows.append(case('typed-call',[span('client','A',kind='CLIENT',end=100),span('server','B','client',kind='SERVER',start=10,end=50)],[['A','B',sync]],roots=1))
base=Path(__file__).parent
(base/'inputs.json').write_text(json.dumps([{k:v for k,v in x.items() if k!='expected'} for x in rows],ensure_ascii=False,indent=2),'utf-8')
(base/'expected.json').write_text(json.dumps({x['name']:x['expected'] for x in rows},ensure_ascii=False,indent=2),'utf-8')
print('Wrote literal inputs/expected; no builder imported')
