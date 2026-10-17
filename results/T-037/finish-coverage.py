"""Resolve prior SMTP coverage flags and audit source requirements without changing their text."""
import copy
import json
from pathlib import Path
import re

BASE=Path('D:/RCA-flashticket/results/T-037');ROOT=BASE.parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry=load(BASE/'nguon.json');cov=load(BASE/'bao-phu-nguon.json');comp=load(BASE/'coverage-completion.json');doc=load(BASE/'ban-ghi.json')
dump(BASE/'runs/assemble-002/coverage-before-resolution.json',cov)
for u in cov['units']:
 if u['status']=='OPEN_UNSUPPORTED' and 'smtp' in u['entity_ids']:
  u.update(status='design',record_ids=['completion-ticket-smtp'],operation_names=['gửi SMTP'],reason='Bổ sung SMTP Minh đã duyệt; giữ type chưa phân kiểu và channel smtp. Chặn biểu diễn cũ đã được kiểm xử lý, runtime/instrumentation vẫn OPEN.',required_input='P9 xác minh adapter SMTP/span/log/outcome/deployment; không còn cần duyệt hỗ trợ SMTP trong lượt này',resolution=dict(date='2026-10-16',authority='LOG Phiên3',check='runs/smtp-regression-001/result.json',original_reason=u['reason']))
 if u['status']=='source_reviewed_partial_mapping':
  u['status']='source_context_or_design_inventory';u['reason']='Đã đối chiếu toàn đoạn; giữ ngữ cảnh/phạm vi nguồn. Đồ thị là mô hình thiết kế, không sinh runtime từ câu kiến trúc.'
 if u['status'].startswith('represented_design'):
  u['status']='design_runtime_mapping_OPEN' if 'address_open' in u['status'] else 'design'
cov['source_line_ledger']=comp['line_ledger']
cov['completion_checks']=comp['checks']
cov['state']='SOURCE_ACCOUNTED_GRAPH_CHECK_PENDING'
cov['remaining_representation_blockers']=[]
cov['open_items']=[
 {'id':'FT-OPEN-QUEUE','observation':'B13 quy queue riêng theo owner/consumer, chưa có tên/scope/vhost cụ thể; exchange/routing có nguồn','owner':'Nhóm nền tảng / P9a','required_input':'Broker config/export, identity namespace và build','effect':'Địa chỉ queue runtime/so khớp messaging chưa đủ điều kiện; null không tính khớp'},
 {'id':'FT-OPEN-OPERATION','observation':'Tên thiết kế/nhóm path không xác nhận runtime operationName/method','owner':'Owner service / P9a/P9b','required_input':'Instrumentation route/span.name mapping cùng version','effect':'Chưa so operation runtime hoặc chọn mức P6'},
 {'id':'FT-OPEN-DEPLOYMENT','observation':'DB/host/instance là topology mục tiêu/ứng viên','owner':'Nhóm triển khai / P9','required_input':'Build/image/deployment/resource IDs, endpoint binding và thời gian hiệu lực','effect':'Không khẳng định process/host/failure domain runtime đã xác minh'},
 {'id':'FT-OPEN-CONFIG','observation':'Sơ đồ có config/discovery và identity arrows nhưng chưa đặc tả caller/receiver/protocol; local JWT verify không tự là request Keycloak mỗi lần','owner':'Nhóm nền tảng và identity','required_input':'Config/discovery/identity integration, JWKS/introspection/refresh và client config','effect':'Giữ inventory và raw source relations; không tạo network edge giả'},
 {'id':'FT-OPEN-PIPELINE','observation':'B16 đường collector/exporter và truy kho, chưa pin endpoint/protocol từng receiver','owner':'Nhóm nền tảng / P9a/P9b','required_input':'Receiver/exporter/query API version, endpoint, sampling/drop/clock/retention','effect':'Data dependency vào kho giữ được; chưa xác nhận transport hoặc độ đầy đủ telemetry'},
 {'id':'FT-OPEN-ACCESS','observation':'Keycloak Admin API/realm fixture chưa là quyền đã kiểm; RES039/RPO/RTO còn OPEN','owner':'Minh / nhóm hệ thống / P9','required_input':'Provisioned permissions and runtime deny/allow checks; user/UI and retention decisions','effect':'Không tự bật service/identity hoặc nhận tích hợp runtime'},
 {'id':'FT-OPEN-RCA','observation':'T037 chỉ mô hình thiết kế/địa chỉ có điều kiện','owner':'Minh và người làm P6/P7/P9/P10','required_input':'Thiết kế P6 trên dev, baseline/đối chứng, runtime/workload/export và phép đánh giá sau quyền test','effect':'RQ3/RQ5/G3/lợi ích RCA vẫn mở'}]

# Explicitly preserve unresolved architecture arrows as source facts outside typed runtime graph.
raw=[]
for u in cov['units']:
 if u.get('classification')=='OPEN' and u['source_id'].startswith('FT-B11'):
  raw.append(dict(unit_id=u['unit_id'],source_id=u['source_id'],locator=u['locator'],text=u.get('original_source_text',u['summary']),entities=u['entity_ids'],owner=u['owner'],required_input=u['required_input'],reason='Architecture relation exists at its abstraction level; transport/call semantics not established. No source requirement removed.'))
dump(BASE/'quan-he-nguon-chua-dinh-kieu.json',raw)
source_index={s['id']:s for s in registry['sources']};facts=[];errors=[]
for u in cov['units']:
 if 'original_source_text' not in u or 'line_start' not in u:continue
 ls=(ROOT/source_index[u['source_id']]['snapshot']).read_text(encoding='utf-8-sig').splitlines()
 actual='\n'.join(ls[u['line_start']-1:u['line_end']])
 ok=actual==u['original_source_text'];facts.append(dict(unit_id=u['unit_id'],source_id=u['source_id'],line_start=u['line_start'],line_end=u['line_end'],source_quote_matches=ok))
 if not ok:errors.append(u['unit_id'])
# SQL names are independently compared with B12 dictionary headings, never inferred as operations.
b12=(ROOT/source_index['FT-B12']['snapshot']).read_text(encoding='utf-8-sig')
sql=[]
for sid,owner in [('FT-PG-EVENT','event'),('FT-PG-BOOKING','booking'),('FT-PG-PAYMENT','payment'),('FT-PG-TICKET','ticket')]:
 content=(ROOT/source_index[sid]['snapshot']).read_text(encoding='utf-8-sig')
 names=re.findall(r'^CREATE TABLE (\w+)',content,flags=re.M)
 dictionary=re.findall(r'^### '+owner+r'_schema\.(\w+)',b12,flags=re.M)
 sql.append(dict(source_id=sid,owner=owner,names=names,dictionary_names=dictionary,equal=set(names)==set(dictionary)))
assert all(x['equal'] for x in sql),sql
assert not errors,errors
dump(BASE/'runs/assemble-002/semantic-source-audit.json',dict(source_quote_checks=facts,all_quotes_match=not errors,sql_dictionary_tables=sql,total_sql_tables=sum(len(x['names']) for x in sql),note='Checks source text and schema names, not business correctness or runtime'))
cov['source_quote_check']='runs/assemble-002/semantic-source-audit.json'
cov['open_source_relation_file']='quan-he-nguon-chua-dinh-kieu.json'
dump(BASE/'bao-phu-nguon.json',cov)
dump(BASE/'runs/assemble-002/coverage-resolution.json',dict(units=len(cov['units']),original_quote_units_checked=len(facts),all_quotes_match=True,source_lines=sum(s['line_count'] for s in registry['sources']),sql_tables=sum(len(x['names']) for x in sql),representation_blockers=cov['remaining_representation_blockers'],open_items=len(cov['open_items'])))
print(json.dumps(load(BASE/'runs/assemble-002/coverage-resolution.json'),ensure_ascii=False))
