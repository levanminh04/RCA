"""Pin local design sources and preserve independent inventory; no graph build."""
import hashlib
import json
import pathlib
import re
import subprocess

ROOT=pathlib.Path('D:/RCA-flashticket')
PLATFORM=pathlib.Path('D:/Project/flash-ticket-platform')
BASE=ROOT/'results/T-037'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(PLATFORM),*args]).decode('utf-8',errors='replace').strip()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

run=BASE/'runs/nguon-001'
run.mkdir(parents=True,exist_ok=False)
rev=git('rev-parse','HEAD')
sources={
 'FT-B11':'docs/architecture/B11-C-target-architecture.md',
 'FT-B12':'docs/architecture/B12-data-ownership-and-schema.md',
 'FT-B13':'docs/architecture/B13-api-and-event-contracts.md',
 'FT-B14':'docs/architecture/B14-main-flow-sequences.md',
 'FT-B16':'docs/architecture/B16-observability-baseline.md',
 'FT-DATA-README':'docs/architecture/data/README.md',
 'FT-PG-README':'docs/architecture/data/postgres/README.md',
 'FT-MONGO-README':'docs/architecture/data/mongodb/README.md',
 'FT-KC-README':'docs/architecture/data/keycloak/README.md',
 'FT-AGENTS':'AGENTS.md',
 'FT-SKILL':'.agents/skills/govern-capstone-work/SKILL.md',
 'FT-GATES':'.agents/skills/govern-capstone-work/references/project-authority-and-gates.md',
 'FT-DT18':'docs/evidence/project-direction/2026-09-18-de-tai-va-nhiem-vu.md',
 'FT-ROLES':'docs/project/roles.md'
}
for p in sorted((PLATFORM/'docs/diagrams/src').glob('B11-C-*.puml')):
 sources['FT-'+p.name[:8]]=p.relative_to(PLATFORM).as_posix()
for family in ['B12','B14']:
 for p in sorted((PLATFORM/'docs/diagrams/src').glob(family+'-*.puml')):
  sources['FT-'+p.name[:6]]=p.relative_to(PLATFORM).as_posix()
registry=[]
for sid,rel in sources.items():
 p=PLATFORM/rel;data=p.read_bytes();dest=run/'snapshot'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 text=data.decode('utf-8-sig');lines=text.splitlines()
 registry.append({'id':sid,'kind':'design' if sid not in ['FT-AGENTS','FT-SKILL','FT-GATES','FT-DT18','FT-ROLES'] else 'governance',
  'revision':rev,'sha256':sha(p),'bytes':len(data),'line_count':len(lines),
  'condition':'Local content pinned; design evidence, not application/runtime verification; historical passages keep their original scope',
  'path':str(p),'snapshot':dest.relative_to(ROOT).as_posix(),'dirty':git('status','--porcelain=v1','--',rel),
  'headings':[{'line':i,'text':line} for i,line in enumerate(lines,1) if line.startswith('#')],
  'links':[{'line':i,'target':target} for i,line in enumerate(lines,1) for target in re.findall(r'\]\(([^)]+)\)',line)]})
derived=[]
for p in sorted((PLATFORM/'docs/architecture/data').rglob('*')):
 if not p.is_file() or p.name=='README.md':continue
 rel=p.relative_to(PLATFORM).as_posix()
 is_test=any(x.lower()=='tests' for x in p.parts) or 'test' in p.name.lower() or p.suffix=='.ps1'
 derived.append({'path':rel,'bytes':p.stat().st_size,'status':'excluded_test_execution_material' if is_test else 'metadata_only_pending_content_crosscheck',
  'reason':'No app/runtime or test data opened; not required to reproduce SMTP blocker; detailed source coverage remains incomplete',
  'impact':'Cannot claim derived baseline code/config coverage or runtime readiness from this session'})
nguon={'task':'T-037','state':'PARTIAL_BLOCKED_SMTP','system':'FlashTicket','revision':rev,
 'sources':registry,'platform_dirty_state':git('status','--porcelain=v1','--untracked-files=all'),
 'new_download_bytes':0,'decompressed_bytes':0,'source_closure_complete':False,'derived_scope':derived,
 'exclusions':[
  {'source':'legacy repo/B5.5/B11-B/archive','reason':'Not authorized and not design-formation evidence; references in current docs remain historical, no source code inspected','impact':'No claim of legacy implementation reuse or runtime equivalence'},
  {'source':'external documentation links in B16','reason':'No new source download authorized; this task uses the pinned local baseline, no new technical claims from those URLs','impact':'Instrumentation/exporter behavior still needs P9 validation'},
  {'source':'B12-validation/B15/implementation-readiness','reason':'Runtime status is explicitly not verified; not used to add graph operations','impact':'No runtime acceptance claim'},
  {'source':'unrelated upstream domain/research documents','reason':'B11-C/B12/B13/B14/B16 supply target design scope; no design changes or reinterpretation of requirements','impact':'If a concrete requirement needs such a source, it must be read/pinned before concluding coverage'}],
 'input_manifest':'results/T-037/runs/tu-ra-001/preflight.json','source_notes':[
  'B11-C §1 delegates endpoints/topics/sequences to B13/B14; diagram arrows cannot independently prove transport or direct call.',
  'B14 diagram Gateway is payment gateway by createPayment/IPN/refund context.',
  'APPROVED design headers do not turn candidate realm or OPEN runtime readiness into observed state.']}
write(BASE/'nguon.json',nguon)

def p(sid,loc,condition='Thiết kế; chưa kiểm runtime'):
 return [{'source_id':sid,'locator':loc,'condition':condition}]
def ent(i,n,t,role,prov):return {'id':i,'name':n,'type':t,'granularity':'component','role':role,'provenance':prov}
entities=[]
for i,n,t,role,prov in [
 ('api-gateway','API Gateway','gateway','bề mặt HTTP công bố; không route internal',p('FT-B11','§3.1/§6')+p('FT-B13','§2')),
 ('broker','Broker','broker','trao đổi bản tin; runtime broker/vhost/queue chưa biết',p('FT-B11','§6')+p('FT-B13','§5.1')),
 ('cache','Cache','cache','cache ở máy1; công nghệ và thao tác chi tiết OPEN',p('FT-B11','§6')+p('FT-B11-C-02','L25/L52')),
 ('config-discovery','Config / Discovery','service','hỗ trợ cấu hình/khám phá; không tự tách thành process runtime',p('FT-B11','§6')+p('FT-B11-C-02','L34/L61-L64')),
 ('chatbot-adapter','Chatbot adapter','service','kênh bán vé, qua gateway; không là service nghiệp vụ',p('FT-B11','§3.1/§6')),
 ('web-channel','Kênh web','external','kênh ngoài gateway',p('FT-B11-C-01','L14-L15/L37')),
 ('mobile-channel','Kênh mobile','external','tùy thời gian; không tuyên bố hiện thực',p('FT-B11-C-01','L14')+p('FT-ROLES','L13')),
 ('vnpay','Cổng thanh toán VNPay','external','provider; chỉ có dữ liệu phía client/callback đã xác minh',p('FT-B13','§5.3')),
 ('smtp','SMTP','external','giao email ngoài transaction; channel chưa biểu diễn được trong T-036',p('FT-B14','L82')+p('FT-B14-03','L9-L12')),
 ('gemini-api','Gemini API','external','giải thích sau xếp hạng; evidence đã lọc',p('FT-B11','§5')),
 ('otel-collector','OTel Collector','service','nhận/xuất tín hiệu; lỗi xuất không chứng minh không có nghiệp vụ',p('FT-B16','§2/§7')),
 ('tempo','Tempo','database','kho trace',p('FT-B16','§2')),
 ('loki','Loki','database','kho log',p('FT-B16','§2')),
 ('prometheus','Prometheus','database','kho/thu metric; không là nguồn quyết định giữ chỗ',p('FT-B16','§2/§5')),
 ('grafana','Grafana','service','xem/liên kết tín hiệu; viewer không tự bảo đảm read-only API',p('FT-B16','§2/§6')),
 ('rca','RCA + lớp giải thích','service','đơn vị riêng chỉ đọc kho quan sát; tập ứng viên xếp hạng chưa chọn',p('FT-B11','§5/§6')+p('FT-B16','§1/§6'))]:
 entities.append(ent(i,n,t,role,prov))
rels=[];bindings=[]
for host,members in [('ft-design-machine-1',['api-gateway','booking-service','payment-service','ticket-service','broker','cache']),('ft-design-machine-2',['event-service','user-service','keycloak','config-discovery','chatbot-adapter','otel-collector','tempo','loki','prometheus','grafana','rca'])]:
 for i in members:
  rels.append({'id':'infra-placement-'+i,'source':{'entity':i,'operation':None},'target':{'entity':host,'operation':None},'type':'triển-khai','channel':'deployment','messaging':None,'context':'Bố trí mục tiêu theo B11-C §6; không là deployment/host ID runtime. Chi tiết các kho B16 là đề xuất thành phần trong nhóm kho quan sát.', 'provenance':p('FT-B11','§6')+p('FT-B16','§2')})
rels.append({'id':'infra-cache-booking','source':{'entity':'booking-service','operation':None},'target':{'entity':'cache','operation':None},'type':'dữ-liệu','channel':'data','messaging':None,'context':'B11-C-02 thể hiện phụ thuộc cache; chưa có operation/cấu hình/address runtime để bổ sung', 'provenance':p('FT-B11-C-02','L52')})
signals=[]
for i in ['api-gateway','broker','cache','postgresql-shared-instance','mongodb-instance','ft-design-machine-1','ft-design-machine-2','otel-collector']:
 signals.append({'id':'infra-resource-'+i,'kind':'metric','entity':i,'operation':None,'address':['design:entity='+i,'scope:service/instance/host phải xác minh bằng manifest runtime','metric:CPU/RAM/disk/pool/queue hoặc export failure theo thành phần; tên series OPEN'],'shared':True,'provenance':p('FT-B16','§5/§7')})
doc={'scope':{'system':'FlashTicket','revision':rev},'entities':entities,'operations':[],'relations':rels,'resource_bindings':bindings,'signals':signals}
write(BASE/'records-infra.json',doc)
coverage=[]
for heading,summary,ids in [
 ('§1','Thẩm quyền nguồn: B12 datastore/B13 API-event/B14 sequence/B16 tín hiệu',[]),
 ('§2','Điều kiện chấp nhận kiến trúc; không phải runtime/tải',[]),
 ('§3','5 service; chatbot và support không tính vào5',['api-gateway','chatbot-adapter']),
 ('§4','Một Saga Payment; không tự thêm Saga hủy/rolegrant',[]),
 ('§5','RCA/Gemini/credential read-only, không DB business',['rca','gemini-api']),
 ('§6','Bố trí thiết kế2máy, không HA; source chưa là runtime host IDs',[e['id'] for e in entities]),
 ('§7-§9','Tác động/đối chiếu/ADR lịch sử; không sinh relation runtime',[]),
 ('§10','OPEN ngưỡng/tậpnode/UI nhận kết quả, owner Minh',[]),
 ('§11-§12','Tự kiểm/phiên bản nguồn; không là telemetry',[])]:
 coverage.append({'source_id':'FT-B11','locator':heading,'summary':summary,'entity_ids':ids,'record_ids':[],'operation_names':[],'status':'source_reviewed_partial_mapping','reason':'CANDIDATE inventory; graph blocked by SMTP, no coverage completion claim','owner':'Minh/nhóm hệ thống','required_input':'Triển khai/manifest khi đánh giá runtime; xử lý hợp đồng SMTP trước graph đầy đủ'})
for sid in ['FT-B11-C-01','FT-B11-C-02']:
 coverage.append({'source_id':sid,'locator':'toàn file','summary':'Đọc diagram; giữ mức trừu tượng. Không lấy Ticket→Booking hoặc Booking→Payment làm endpoint trực tiếp; B13/B14 nhận hợp đồng cụ thể.', 'entity_ids':[e['id'] for e in entities], 'record_ids':[],'operation_names':[],'status':'source_reviewed_partial_mapping','reason':'Không suy transport/runtime từ mũi tên kiến trúc','owner':'Minh/nhóm hệ thống','required_input':'Không có bổ sung nguồn cần tải để xác định chặn SMTP'})
write(BASE/'coverage-infra.json',coverage)
print(json.dumps({'sources':len(registry),'snapshot_bytes':sum(x['bytes'] for x in registry),'infra_entities':len(entities),'state':'PARTIAL_BLOCKED_SMTP'},ensure_ascii=False))
