"""Assemble sourced records and coverage; no graph API calls. Graph oracle exists already."""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037';PLAT=Path('D:/Project/flash-ticket-platform')
RUN=BASE/'runs'/sys.argv[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prov(s,l,c='Thiết kế có nguồn; chưa kiểm runtime'):return [dict(source_id=s,locator=l,condition=c)]
def end(e,o=None):return dict(entity=e,operation=o)
def rel(i,s,t,typ,ch,p,c):return dict(id=i,source=s,target=t,type=typ,channel=ch,messaging=None,context=c,provenance=p)
RUN.mkdir(parents=True,exist_ok=False)
assert load(BASE/'runs/smtp-regression-001/result.json')['all_pass'], 'SMTP must pass before continuation'
assert (BASE/'oracle-v2.json').is_file()
registry=load(BASE/'nguon.json')
for s in registry['sources']:
 assert sha(Path(s['path']))==s['sha256'],s['path']
extra={
 'FT-PG-BOOTSTRAP':'docs/architecture/data/postgres/00-bootstrap.sql',
 'FT-PG-EVENT':'docs/architecture/data/postgres/10-event.sql',
 'FT-PG-BOOKING':'docs/architecture/data/postgres/20-booking.sql',
 'FT-PG-PAYMENT':'docs/architecture/data/postgres/30-payment.sql',
 'FT-PG-TICKET':'docs/architecture/data/postgres/40-ticket.sql',
 'FT-PG-GRANTS':'docs/architecture/data/postgres/90-grants.sql',
 'FT-PG-RATIONALE':'docs/architecture/data/postgres/95-design-rationale.sql',
 'FT-MONGO-SCHEMA':'docs/architecture/data/mongodb/schema.cjs',
 'FT-MONGO-BOOTSTRAP':'docs/architecture/data/mongodb/bootstrap.js',
 'FT-KC-REALM':'docs/architecture/data/keycloak/flash-ticket-realm.candidate.json'}
for sid,r in extra.items():
 if sid in {s['id'] for s in registry['sources']}:
  current=next(s for s in registry['sources'] if s['id']==sid)
  assert sha(PLAT/r)==current['sha256']
  continue
 p=PLAT/r;target=RUN/'snapshot'/r;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());txt=p.read_text(encoding='utf-8-sig')
 registry['sources'].append(dict(id=sid,kind='design-derived',revision=registry['revision'],sha256=sha(p),bytes=p.stat().st_size,line_count=len(txt.splitlines()),condition='Dẫn xuất baseline local; chỉ đối chiếu định danh/owner/ràng buộc, không là runtime',path=str(p),snapshot=target.relative_to(ROOT).as_posix(),dirty=subprocess.check_output(['git','-C',str(PLAT),'status','--porcelain=v1','--',r]).decode().strip(),headings=[],links=[]))
registry['state']='DESIGN_SCOPE_REVIEWED_RUNTIME_OPEN'
registry['source_closure_complete']=True
registry['source_closure_meaning']='Closed for selected target-design B11-C/B12/B13/B14/B16 and directly relevant diagrams/baseline definitions; not entire platform tree/runtime or upstream domain re-design'
for row in registry['derived_scope']:
 if row['path'] in extra.values():row.update(status='content_read_and_crosschecked',reason='Read definition from local baseline against B12 ownership/dictionary; no execution',impact='No new runtime nodes inferred from fields/client IDs or SQL FK')
registry['exclusions'].append(dict(source='Other platform tree, build/deployment implementations not referenced as current design',reason='This is a target-design model; no new application runtime supplied; source unit registry defines the scope explicitly',impact='No claim of complete runtime inventory/observed deployment'))
dump(BASE/'nguon.json',registry)

parts=[load(BASE/f'records-{n}.json') for n in ['data','infra','flow','completion']]
doc={'scope':parts[0]['scope']}
for col in ['entities','operations','relations','resource_bindings','signals']:
 doc[col]=sum([p[col] for p in parts],[])
assert len({e['id'] for e in doc['entities']})==len(doc['entities'])
ops={(o['entity'],o['name']) for o in doc['operations']}
entities={e['id']:e for e in doc['entities']}
corrections=[]
# Correct numeric locators from the earlier partial inventory against the actual source.
for row in doc['relations']:
 if row['id']=='infra-cache-booking':
  corrections.append(dict(record_id=row['id'],old_locator='L52',new_locator='L47',reason='BKG --> CACHE is L47, not L52'))
  row['provenance']=prov('FT-B11-C-02','L47')
for ident,loc in [('cache','L23/L47'),('config-discovery','L31/L54-L57')]:
 for p in entities[ident]['provenance']:
  if p['source_id']=='FT-B11-C-02':p['locator']=loc
# Placement of the observation group is conditional on B11-C §6; no runtime host IDs.
for row in doc['relations']:
 if row['id'].startswith('infra-placement-'):
  row['context']='Bố trí mục tiêu B11-C §6; host ID thiết kế, chưa là deployment thật. Tempo/Loki/Prometheus/Grafana là chi tiết nhóm kho quan sát B16 §2 theo cùng bố trí nhóm; phải kiểm manifest runtime.'

root_relations=[]
for i,owner,name,sid,loc in [
 ('create-order','booking-service','POST /orders','FT-B14','L24-L28'),
 ('promotion','booking-service','POST /orders/{orderId}/promotion','FT-B14','L29'),
 ('cancel-order','booking-service','POST /orders/{orderId}/cancel','FT-B14','L59-L61'),
 ('freeze','booking-service','POST /internal/v1/orders/{id}/freeze-payment','FT-B14','L30'),
 ('expiry','booking-service','Worker tìm đơn PENDING_PAYMENT đến hạn','FT-B14','L59-L61'),
 ('failed-release','booking-service','Booking nhận FAILED','FT-B14','L53'),
 ('attempt','payment-service','POST /orders/{orderId}/payment-attempts','FT-B14','L31'),
 ('charge','payment-service','Chọn một candidate charge/order','FT-B14','L39-L40'),
 ('confirmation','payment-service','tạo confirmation unique(order,charge)','FT-B14','L43'),
 ('refund-claim','payment-service','Transaction claim refund','FT-B14','L63'),
 ('refund-run','payment-service','tạo event_refund_run duy nhất/cancellation','FT-B14','L73-L75'),
 ('saga-result','payment-service','Nhận COMPLETED hợp lệ','FT-B14','L46'),
 ('reconciliation','payment-service','đối soát thủ công','FT-B14','L96-L98'),
 ('event-cancel','event-service','chốt CANCELLED + cancellationId/outbox','FT-B14','L69'),
 ('terminal-fence','ticket-service','ghi FAILED/failed_at/failure_code và outbox FAILED','FT-B14','L51'),
 ('delivery-claim','ticket-service','Worker claim bằng khóa hàng/lease','FT-B14','L82'),
 ('checkin','ticket-service','POST /api/v1/events/{eventId}/check-ins','FT-B14','L84'),
 ('qr-read','ticket-service','GET /tickets/{ticketId}/qr','FT-B13','L197'),
 ('role-worker','user-service','Worker quét PENDING có roleGrant','FT-B13','L292'),
 ('projection','user-service','Worker quét ACTIVE','FT-B13','L292')]:
 assert (owner,name) in ops,(owner,name)
 db={'event-service':'event_db','booking-service':'booking_db','payment-service':'payment_db','ticket-service':'ticket_db','user-service':'user_db'}[owner]
 root_relations.append(rel('detail-data-'+i,end(owner,name),end(db),'dữ-liệu','data',prov(sid,loc)+prov('FT-B12','§2'), 'Thao tác đọc/ghi cục bộ được nguồn mô tả; cùng owner/DB, giữ transaction/deadline/retry/state guard tại nguồn, chưa là SQL/span runtime'))
for owner in ['event-service','booking-service','payment-service','ticket-service']:
 name='Relay chọn unpublished theo next_attempt_at';assert (owner,name) in ops
 db=owner.replace('-service','_db')
 root_relations.append(rel('detail-outbox-data-'+owner,end(owner,name),end(db),'dữ-liệu','data',prov('FT-B14','L90-L92')+prov('FT-B12','§4'), 'Relay đọc outbox cùng DB owner, chọn next_attempt_at/SKIP LOCKED; publisher confirm mới published_at; crash có thể publish lại. Không ghép trace bằng correlation'))
for target in ['tempo','loki','prometheus']:
 root_relations.append(rel('obs-read-'+target,end('rca'),end(target),'dữ-liệu','data',prov('FT-B11','§5')+prov('FT-B16','§6'), 'RCA chỉ đọc kho quan sát; data biểu diễn phụ thuộc dữ liệu, không khẳng định protocol/endpoint/operation runtime'))
for target in ['tempo','loki']:
 root_relations.append(rel('obs-write-'+target,end('otel-collector'),end(target),'dữ-liệu','data',prov('FT-B16','L24'), 'Đường xuất baseline của collector tới kho trace/log; protocol receiver/exporter và endpoint cụ thể OPEN. Không giả định mọi log/trace đã thu đủ'))
doc['relations']+=root_relations
dump(BASE/'records-root-completion.json',dict(scope=doc['scope'],entities=[],operations=[],relations=root_relations,resource_bindings=[],signals=[]))

# Every operation gets a schema-address requirement, never an invented runtime operation name.
existing={(s['entity'],s['operation'],s['kind']) for s in doc['signals']}
for i,o in enumerate(doc['operations'],1):
 for kind in ['log','trace']:
  if (o['entity'],o['name'],kind) in existing:continue
  doc['signals'].append(dict(id=f'address-{kind}-{i:03}',kind=kind,entity=o['entity'],operation=o['name'],address=['design:entity='+o['entity'],'design:operation='+o['name'], 'schema:B16 serviceName/operation/traceId/spanId; runtime alias pending'],shared=False,provenance=prov('FT-B16','§3/§4/§5','Yêu cầu đối chiếu địa chỉ schema; không xác nhận operation có span/log thực hoặc tất cả tên cần manual span')+copy.deepcopy(o['provenance'])))
dump(BASE/'ban-ghi.json',doc)
dump(RUN/'input-corrections.json',corrections)

base_units=load(BASE/'coverage-data.json')+load(BASE/'coverage-infra.json')+load(BASE/'coverage-flow.json')['units']
completion=load(BASE/'coverage-completion.json');base_units+=completion['units']
for r in root_relations:
 for p in r['provenance']:
  base_units.append(dict(source_id=p['source_id'],locator=p['locator'],summary=r['context'],record_ids=[r['id']],entity_ids=[r['source']['entity'],r['target']['entity']],operation_names=[r['source']['operation']] if r['source']['operation'] else [],status='covered_design',owner=r['source']['entity']+' / P9',reason='Đối chiếu chuỗi thao tác → owner → DB hoặc kho quan sát; không suy runtime',required_input='P9 xác minh build/config/span/địa chỉ; không còn thiếu biểu diễn để giữ bản ghi nguồn này'))
all_ids={x['id'] for col in ['entities','relations','resource_bindings','signals'] for x in doc[col]}
by_source={s['id']:s for s in registry['sources']}
units=[]
for i,u in enumerate(base_units,1):
 u=copy.deepcopy(u);u['unit_id']=f'FT-U{i:04}'
 if 'status' not in u:u['status']=u.get('classification','source_reviewed')
 u['origin_state']=u.get('status','source_reviewed')
 if 'record_ids' not in u:u['record_ids']=[]
 if 'entity_ids' not in u:u['entity_ids']=[]
 if 'operation_names' not in u:u['operation_names']=[]
 # Input coverage identifies records, with op names kept literal. Missing runtime names remain OPEN.
 assert u['source_id'] in by_source,u
 assert all(x in all_ids for x in u['record_ids']),u
 assert all(x in entities for x in u['entity_ids']),u
 units.append(u)

derived_checks=[]
for sid,r in extra.items():
 s=by_source[sid];txt=Path(s['path']).read_text(encoding='utf-8-sig');tables=re.findall(r'^CREATE TABLE (\w+)',txt,flags=re.M)
 dbowner={'FT-PG-EVENT':('event_db','event-service'),'FT-PG-BOOKING':('booking_db','booking-service'),'FT-PG-PAYMENT':('payment_db','payment-service'),'FT-PG-TICKET':('ticket_db','ticket-service')}.get(sid)
 if dbowner:
  db,owner=dbowner;expected_tables=[u for u in units if u['source_id']=='FT-B12' and any(t in u.get('summary','') for t in tables)]
  records=['d-'+owner+'-'+db]
 else:records=[]
 derived_checks.append(dict(source_id=sid,tables=tables,table_count=len(tables),db_owner=list(dbowner) if dbowner else None,interpretation='Local definitions only; no execution or runtime acceptance'))
 units.append(dict(unit_id=f'FT-D-{sid}',source_id=sid,locator=f'L1-L{s["line_count"]}',summary='Baseline definition read in full: '+r,record_ids=records,entity_ids=list(dbowner) if dbowner else [],operation_names=[],status='design_derived_definition',reason='Crosscheck source ownership/names; table/column/client ID never becomes a runtime graph node/operation. Tests/runners excluded explicitly.',owner='Nhóm hệ thống / P9',required_input='Runtime build/image/config/permissions/export for deployment validation'))
dump(RUN/'derived-definition-check.json',derived_checks)

# All source lines retain evidence classification. A line ledger is a navigation aid, not a semantic PASS.
ledger=[]
for s in registry['sources']:
 text=(ROOT/s['snapshot']).read_text(encoding='utf-8-sig');ls=text.splitlines()
 refs=[u['unit_id'] for u in units if u['source_id']==s['id']]
 kind='governance_context' if s['kind']=='governance' else 'design_definition' if s['id'] in extra else 'design_source'
 ledger.append(dict(source_id=s['id'],line_range=[1,len(ls)],content_sha256=s['sha256'],all_lines_read=True,coverage_units=refs,classification=kind,
  meaning='All text retained/read; semantic requirement checks are listed per unit, not inferred from line count. Metadata/history do not create graph edges.',
  open_rows=[u['unit_id'] for u in units if u['source_id']==s['id'] and 'OPEN' in u.get('status','')]))
matrix=[]
for i,o in enumerate(doc['operations'],1):
 sig=[s for s in doc['signals'] if s['entity']==o['entity'] and s['operation']==o['name']]
 matrix.append(dict(entity=o['entity'],design_name=o['name'],runtime_name=None,operation_id=json.dumps([o['entity'],o['name']],ensure_ascii=False,separators=(',',':')),provenance=o['provenance'],signal_ids=[s['id'] for s in sig],keys=['environment','serviceName/service.name','instanceId','timestamp','operation/span.name mapping','traceId','spanId'],writer=o['entity']+' instrumentation/application',owner=o['entity']+' / P9a/P9b',status='DESIGN_ADDRESS_RUNTIME_MAPPING_OPEN',test='Export a declared path/job run; validate schema/namespace/alias and compare graph separately; no correlation-created parent/message'))
dump(BASE/'dia-chi-tin-hieu.json',dict(operations=matrix,queue_address_open=dict(broker='broker',broker_scope=None,queue=None,required=['broker_id','deployment/vhost','queue'],writer='broker/config/exporter',owner='Nhóm nền tảng / P9a',test='Two queues same consumer remain two addresses; binding/export matches runtime namespace'),shared_signal_ids=[s['id'] for s in doc['signals'] if s['shared']],protocol_limit='Compare endpoint/type does not verify transport; SMTP explicit only in static source'))
coverage=dict(task='T-037',state='READY_FOR_GRAPH_CHECKS',source_scope=registry['source_closure_meaning'],units=units,line_ledger=ledger,open_items=completion.get('open_items',[]),inventory_is_runtime=False,source_closure_complete=True,
 groups=['HTTP/RPC/gateway','DB logic/shared instance/cache','messaging/queue/fanout/retry','outbox/inbox/confirm/ACK','callback/query','scheduler/background','Saga/compensation/terminal fence','delivery/check-in','role-grant/projection','support/operations'],
 note='OPEN source/runtime facts preserved with owner/input; all records require graph check results before completion claim')
dump(BASE/'bao-phu-nguon.json',coverage)
dump(RUN/'assembly.json',dict(counts={c:len(doc[c]) for c in ['entities','operations','relations','resource_bindings','signals']},source_count=len(registry['sources']),coverage_unit_count=len(units),oracle_sha256=sha(BASE/'oracle-v2.json'),fixtures_sha256=sha(BASE/'fixtures-runtime-v2.json'),script_sha256=sha(Path(__file__))))
print(json.dumps(load(RUN/'assembly.json'),ensure_ascii=False))
