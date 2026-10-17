"""Publish one coherent T-038 generation after the full producer replay passes."""
from repair import *
import shutil
CHECK=HERE/'checks/full1069-002'
RUN=rel(HERE); SUMMARY=rel(CHECK/'summary.json')
RETIRED=['engine.py','compare_dev.py','analyze.py','finish_reports.py','finalize_implementation.py','finalize.py','fix_report_references.py']
ROOT_CHANGED=['ban-ghi.json','nguon.json','do-thi/thuc-the.json','do-thi/thao-tac.json','do-thi/chieu-thao-tac.json','do-thi/chi-thuc-the.json','doi-chieu/index.json','inventory-index.json','phan-tich-chenh-lech.json','phan-tich-chenh-lech.md','bao-phu-nguon.json','bao-phu-nguon.md','ban-giao.md','kiem-dung-dan.md','hoan-tat-trong-quyen.json','hoan-tat-trong-quyen.md','de-nghi-tiep-theo.md','LICH-SU.md','goi-sua-SMTP.md','prompt-claude.txt','prompt-claude-smtp.txt','commands.json','manifest.json']+RETIRED
def textfile(path,s):Path(path).write_text(s,encoding='utf-8')
def prompt():
 source=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
 def block(title):return re.search(r'```text\n([\s\S]*?)\n```',source[source.index(title):]).group(1)
 common=block('## Prompt chung');values=[
 ('mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn','T-038; tasks/T-038-p5b-trainticket/SPEC.md; results/T-038/; '+RUN+'/'),
 ('soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa','kiểm lại phản hồi và sửa'),
 ('gói, cổng hiện tại; ngoài task thì ghi loại đề xuất','P5b, chuẩn bị G3'),
 ('tên theo SPEC; ngoài task thì ghi vai trò dự kiến','Codex người làm; Codex phiên độc lập do Minh chỉ định là người phản biện kết quả tại REVIEW.md. Giữ vai trò lịch sử'),
 ('danh sách đường dẫn và git diff từ commit gốc nếu có','AGENTS.md; docs/STATE.md; SPEC.md, LOG.md T-038; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; registry và nguồn được dẫn trong T-038; SPEC/LOG T-040'),
 ('đường dẫn theo thứ tự thời gian; không có thì ghi không có','tasks/T-038-p5b-trainticket/REVIEW.md; LOG.md T-038 theo thứ tự phiên; '+RUN+'/authorization.txt'),
 ('đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng','src/do_thi/; src/do_thi_tinh/; results/T-035/manifest.json; results/T-036/runs/doi-chieu-smtp-001/manifest.json; results/T-038/manifest.json; results/T-038/runs/reviewer-r1-fix-20261016-001/manifest.json; '+RUN+'/manifest.json, repair.py, reproduction-inputs.json; Windows Python 3.12, dùng -X utf8 -B'),
 ('chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác','chỉ đọc và trả lời trong chat; chưa được ghi bản REVIEW mới hoặc sửa file. Được kiểm hash và tính lại trong bộ nhớ trên các đầu ra dev đã lưu. Không mở raw telemetry, dữ liệu cách ly, test/heldout/archive, tải nguồn, EC2, RCA mới, subagent hay tự mở/gửi chat')]
 for old,new in values:common=common.replace('<'+old+'>',new)
 assert not re.search(r'<[^>]+>',common)
 return common+'\n\n'+block('### Kiểm lại phản hồi và sửa')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n'

def analysis(summary):
 grouped=defaultdict(list);full=[];union=defaultdict(set);chains=[];excluded={}
 selected={('ts-admin-basic-info-service','ts-config-service'),('ts-food-service','ts-station-service'),('ts-seat-service','ts-travel-service'),('ts-seat-service','ts-travel2-service'),('ts-travel-service','ts-order-service'),('ts-travel2-service','ts-order-other-service')}
 selected|={(r['source']['entity'],r['target']['entity']) for r in load(HERE/'accepted-delta.json')}
 for row in summary['rows']:
  family=Path(row['input']).stem.split('-')[0]
  for vn,counts in row['views'].items():grouped[(row['level'],family,vn)].append(counts)
  if family!='full':continue
  p=ROOT/row['output'];assert sha(p)==row['output_sha256'];result=read_result(p)
  full.append({k:row[k] for k in ['input','output','level','views']})
  for vn,v in result['views'].items():
   for cat in ['S','T','intersection','static_only','trace_only']:union[(row['level'],vn,cat)].update(canon(k) for k in v[cat])
   for side,items in v['exclusions'].items():
    for x in items:excluded.setdefault((row['level'],vn,side,x['reason']),dict(output=row['output'],exclusion=x))
  if row['level']=='entity':
   v=result['views']['endpoints']
   for key in v['S']+v['trace_only']:
    if (key[0],key[1]) not in selected:continue
    cat='intersection' if key in v['intersection'] else 'static_only' if key in v['static_only'] else 'trace_only'
    chains.append(dict(input=row['input'],output=row['output'],key=key,category=cat,static_members=[g for g in v['members']['static'] if g['key']==key],trace_members=[g for g in v['members']['trace'] if g['key']==key]))
 stats=[]
 for (level,family,vn),rows in sorted(grouped.items()):
  values={}
  for k in ['S','T','intersection','static_only','trace_only','static_fraction','trace_fraction']:
   distinct=sorted({r[k] for r in rows if r[k] is not None})
   values[k]=dict(min=min(distinct) if distinct else None,max=max(distinct) if distinct else None,null_count=sum(r[k] is None for r in rows),distinct=distinct)
  stats.append(dict(level=level,family=family,view=vn,graph_count=len(rows),values=values))
 d=load(BEFORE/'phan-tich-chenh-lech.json');doc=load(BASE/'ban-ghi.json')
 d.update(task='T-038',status='PRODUCER_R1_ADOPTED_AWAITING_INDEPENDENT_CHECK',comparison_run=rel(CHECK),numerical_source=SUMMARY,family_stats=stats,full_graphs=full,full_union=[dict(level=k[0],view=k[1],category=k[2],keys=[json.loads(x) for x in sorted(v)]) for k,v in sorted(union.items())],exclusions=[dict(level=k[0],view=k[1],side=k[2],reason=k[3],**v) for k,v in sorted(excluded.items())],chain_examples=chains,source_counts=dict(entities=len(doc['entities']),operations=len(doc['operations']),relations=len(doc['relations']),bindings=len(doc['resource_bindings']),signals=len(doc['signals']),entity_types=dict(Counter(r['type'] for r in doc['entities'])),signal_kinds=dict(Counter(r['kind'] for r in doc['signals'])),entity_graph_edges=170,operation_graph_edges=343,projection_edges=122,entity_only_edges=48),historical_analysis=rel(BEFORE/'phan-tich-chenh-lech.json'),R1_infrastructure_delta=rel(HERE/'accepted-delta.json'),R1_source_audit=rel(HERE/'source-audit.json'),task_accepted=False,producer_outputs_modified=True,numerical_comparison_unchanged=False)
 d['historical_SMTP_V2_evidence']=dict(diff=d.pop('SMTP_V2_diff',None),non_SMTP_comparator_only_exact_unchanged_graphs=d.pop('non_SMTP_comparator_only_exact_unchanged_graphs',None),meaning='Historical comparator-only regression before R1/SMTP description correction; not a byte-equality claim for this generation.')
 d['intentional_metadata_correction']=rel(HERE/'metadata-correction.json')
 candidate=load(REVIEW/'candidate/phan-tich-chenh-lech.json')
 for k in ['family_stats','full_union']:assert d[k]==candidate[k],k
 assert len(d['chain_examples'])==len(candidate['chain_examples'])
 save(HERE/'analysis-checks.json',dict(all_pass=True,family_stats_equal_to_verified_candidate=True,full_unions_equal=True,full_graphs=len(full),chain_examples=len(chains)))
 return d

def main():
 assert load(CHECK/'verification.json')['all_pass']
 summary=load(CHECK/'summary.json');assert summary['all_pass'] and summary['graph_count']==1069
 plan=dict(intent='EXECUTE',authorization=rel(HERE/'authorization.txt'),root_replacements=ROOT_CHANGED,append_only=['tasks/T-038-p5b-trainticket/LOG.md'],restricted_parts=['tasks/T-038-p5b-trainticket/REVIEW.md#Phản hồi của người làm','docs/STATE.md#T-038'],preserve=['all sources','all pre-existing run history','mapping','src','T-035','T-036','T-040 outputs'],order='repair.py declared and applied authoritative record/registry before graphs; publication follows full official replay. This file records the full final publication impact map.',impact='S/static-only and static fractions change at entity level; trace side and intersection unchanged; operation views/members/exclusions unchanged; one documented SMTP node-role description differs; inventory index additionally receives the previously omitted SMTP row; no method/threshold/mapping/pin/acceptance change.')
 save(HERE/'impact-map.json',plan)
 doc=load(BASE/'ban-ghi.json');registry=load(BASE/'nguon.json');mapping=load(BASE/'mapping.json')
 for name,v in [('ban-ghi.json',doc),('nguon.json',registry),('mapping.json',mapping)]:save(HERE/'model'/name,v)
 data=analysis(summary);overwrite(BASE/'phan-tich-chenh-lech.json',data)
 inventory=[dict(entity=e,operations=sum(o['entity']==e['id'] for o in doc['operations']),outgoing_relations=sum(r['source']['entity']==e['id'] for r in doc['relations']),incoming_relations=sum(r['target']['entity']==e['id'] for r in doc['relations']),signals=sum(s['entity']==e['id'] for s in doc['signals'])) for e in sorted(doc['entities'],key=lambda x:x['id'])]
 old_inventory=load(BEFORE/'inventory-index.json');old_by_id={r['entity']['id']:r for r in old_inventory}
 old_doc=load(BASE/'runs/lap-ban-ghi-005/ban-ghi.json');assert len(old_doc['relations'])==508
 old_ids={r['id'] for r in old_doc['relations']};added_records=[r for r in doc['relations'] if r['id'] not in old_ids];assert len(added_records)==5
 outgoing=Counter(r['source']['entity'] for r in added_records);incoming=Counter(r['target']['entity'] for r in added_records)
 differences=[]
 for row in inventory:
  ident=row['entity']['id'];prior=old_by_id[ident]
  for k in ['operations','outgoing_relations','incoming_relations','signals']:
   expected=outgoing[ident] if k=='outgoing_relations' else incoming[ident] if k=='incoming_relations' else 0
   assert row[k]-prior[k]==expected,(ident,k)
   if row[k]!=prior[k]:differences.append(dict(entity=ident,field=k,before=prior[k],after=row[k],delta=expected))
 save(HERE/'inventory-index-delta.json',dict(all_pass=True,before_relations=sum(r['outgoing_relations'] for r in old_inventory),after_relations=sum(r['outgoing_relations'] for r in inventory),added_record_ids=[r['id'] for r in added_records],explanation='Root inventory-index was still at 508 before SMTP. Its +5 includes the previously omitted SMTP record and the four R1 infrastructure records; this is not five new relations against the 509-record V2 source.',rows=differences,SMTP_role_description_updated=True))
 overwrite(BASE/'inventory-index.json',inventory)
 index=dict(current_run=rel(CHECK),current_model=rel(HERE/'model'),summary=SUMMARY,graph_count=1069,outputs=[r['output'] for r in summary['rows']],manifest=rel(BASE/'manifest.json'),pin=rel(HERE/'pin.json'),model={n:rel(BASE/'do-thi'/n) for n in ['thuc-the.json','thao-tac.json','chieu-thao-tac.json','chi-thuc-the.json']},status='PRODUCER_R1_ADOPTED_AWAITING_INDEPENDENT_CHECK')
 overwrite(BASE/'doi-chieu/index.json',index)
 table=['| Mức/miền/view | Graph | S | T | Giao | Riêng tĩnh | Riêng trace |','|---|---:|---:|---:|---:|---:|---:|']
 def span(z):return str(z['min']) if z['min']==z['max'] else str(z['min'])+'–'+str(z['max'])
 for r in data['family_stats']:table.append('| '+'/'.join([r['level'],r['family'],r['view']])+' | '+str(r['graph_count'])+' | '+' | '.join(span(r['values'][k]) for k in ['S','T','intersection','static_only','trace_only'])+' |')
 original=(BEFORE/'phan-tich-chenh-lech.md').read_text(encoding='utf-8-sig')
 qualitative=original[original.index('## Đầu mút khớp'):original.index('## Hàm ý nghiên cứu')]
 old_smtp=qualitative.index('SMTP có cấu hình');qualitative=qualitative[:old_smtp]+'''SMTP đã biểu diễn theo pin V2; record giữ kiểu chưa phân loại, không suy authority/TLS/delivery hoặc runtime. Hậu tố proposed-only trong ID SMTP là định danh lịch sử được giữ để truy provenance; trạng thái áp dụng nằm ở manifest hiện hành. Bốn dependency cấu hình bổ sung cũng chỉ là khả năng có điều kiện trong snapshot. Không biến nguồn tĩnh thành graph runtime đã xác minh.

'''
 qualitative=qualitative.replace('`edge-groups.json`','`runs/doi-chieu-dev-002/edge-groups.json`').replace('raw không được mở ở task này','raw RE2 không được mở để phân xử trong phép này')
 report=f'''# Đối chiếu hiện hành T-038 sau tiếp nhận R1

Người làm đã kiểm nguồn rồi sửa chính thức. Chờ người phản biện kiểm bản sửa và Minh quyết; chưa nghiệm thu task. Nguồn số: `{SUMMARY}#/rows`, `phan-tich-chenh-lech.json#/family_stats` và `{RUN}/model-checks.json`.

Mô hình có 110 thực thể, 993 thao tác, 513 relation, 50 binding và 139 signal. Có 170 cạnh thực thể, 343 cạnh thao tác; phép chiếu 122 cạnh và phần chỉ có ở mức thực thể 48 cạnh. Từng nhóm giữ locator và điều kiện nguồn, không xác nhận quan hệ đã chạy trong dataset.

R1 là lỗi trích/lập bản ghi: cấu hình → bản ghi từng bỏ Skywalking→Elasticsearch, Alertsnitch→MySQL, Nacos→MySQL và webhook Alertmanager→Alertsnitch. Nguồn gốc đủ để ghi quan hệ cấu hình có điều kiện; chưa đủ để nói runtime hoạt động. Ba cạnh đầu là dữ liệu; webhook giữ gọi-chưa-phân-kiểu/http, không tự nâng thành đồng bộ. Bằng chứng: `{RUN}/source-checks.json#/checks`, `accepted-delta.json` trong cùng run; từng cạnh→record_ids→provenance→locator đi vào members của output.

So với bản SMTP V2 trước sửa: 979 graph entity thêm 4 S/static-only ở endpoints, 3 S/static-only ở typed và 1 unknown exclusion typed. Mẫu số tĩnh tăng tương ứng; tỷ lệ phải đọc lại. T/giao/trace_only, members và exclusions phía trace giữ nguyên. 90 output operation giữ nguyên cấu trúc/tập/số, chỉ đồng bộ mô tả SMTP; JSON graph operation có thêm 4 record/operation exclusion nhưng cạnh không đổi. Root phép chiếu cũ thiếu SMTP đã được thay: 121→122; entity-only44→48. So với phép chiếu V2 đúng trong run cũ, projection122 không đổi. Một mô tả entity.role SMTP được đổi từ ghi chú unsupported lịch sử sang hỗ trợ V2 có điều kiện; chỉ metadata node đổi, không đổi ID/type/provenance hay phép tính. inventory-index trước còn đếm508 relation, nên bản đồng bộ513 gồm4 R1 và1 SMTP đã bị bỏ khỏi chỉ mục. Xem metadata-correction.json và inventory-index-delta.json trong run sửa. Bảng delta từng graph: `{rel(CHECK/'delta.json')}#/rows`.

'''+'\n'.join(table)+f'''

Bảng là min–max từng graph, không phải hợp độc nhất. Có 979 entity, 90 operation, 739 cửa sổ s60 và 150 s300; 30 full/N/A mỗi mức. Các interval và tập graph giữ nguyên. S/T là khóa cạnh đủ điều kiện, không là số inventory. Mẫu số T rỗng giữ null; typed T rỗng không phải không có traffic. Members và exclusions phân hoạch từng chỉ số cạnh; không cộng chúng thành tỷ lệ nguyên nhân.

'''+qualitative+f'''## Phần còn mở và vai trò tính toán

Đã kiểm các địa chỉ còn lại từ nguồn hiện có tại `{RUN}/source-audit.json#/further_source_addresses`. UI→OAP và Prometheus→Alertmanager thiếu protocol đã xác minh; discovery/scrape thiếu binding/owner, Grafana chưa có datasource address trong file. Hợp đồng đang ghim không nhận call channel unknown. Không dùng port/image/role để lấp; thay hợp đồng hoặc lấy semantics image/client cần quyền riêng. Điều này giới hạn kết luận đầy đủ cấu hình, không phủ nhận bốn quan hệ đã có bằng chứng.

Đồ thị dùng nút thực thể/thao tác, cạnh gọi/thông điệp/dữ liệu và provenance để chiếu, tạo khóa có hướng, tính giao/phần riêng. Signal log/trace/metric là địa chỉ khai báo gắn entity/operation theo nguồn; chưa tính anomaly score, vùng ảnh hưởng hoặc rank. Phần này phục vụ DT18-NV2/NV3 và bước1 của cô; chưa chọn P6 hoặc xác nhận lợi ích RCA.

Coverage toàn cây là bookkeeping, không là toàn semantics. Revision ứng dụng→image→instrumentation→deployment→RE2, body PDF lịch sử, dynamic override/binding/runtime đều còn OPEN. Các chuỗi nguồn/match/mismatch không chịu R1 được dùng lại sau kiểm hash, xem các đường dẫn gốc ở trên. Không chạy lại RCA, mở raw/test/heldout/archive hoặc tải nguồn.
'''
 textfile(BASE/'phan-tich-chenh-lech.md',report)
 coverage=load(BEFORE/'bao-phu-nguon.json');coverage.update(current_relation_generation=RUN,semantic_source_inventory_complete=False,configured_dependency_inventory_complete=False,current_relation_correction=rel(HERE/'source-checks.json'),current_source_audit=rel(HERE/'source-audit.json'),current_report='ban-giao.md')
 overwrite(BASE/'bao-phu-nguon.json',coverage)
 oldcov=(BEFORE/'bao-phu-nguon.md').read_text(encoding='utf-8-sig');oldcov=oldcov[:oldcov.rfind('Kết luận hiện hành:')]
 textfile(BASE/'bao-phu-nguon.md',oldcov+f'''Kết luận hiện hành ngày17/10/2026: bookkeeping cây nguồn và declared module/build inventory giữ nguyên; R1 xác nhận phần relation cấu hình từng bị bỏ trước bộ dựng. Đã tiếp nhận bốn relation có nguồn, không còn gọi bản thiếu đó là hiện hành. Bằng chứng tại `{RUN}/source-checks.json`; `source-audit.json` trong cùng run nêu đúng phần protocol/binding/semantics còn thiếu và owner. Không nhận inventory cấu hình/ngữ nghĩa/runtime đầy đủ. SMTP V2 đã tiếp nhận; các gói đề nghị trước đó là lịch sử. Không mở nội dung PDF hoặc dữ liệu cách ly trong lượt này.
''')
 handoff=dict(task='T-038',status='PRODUCER_FIX_READY_FOR_INDEPENDENT_CHECK_NOT_ACCEPTED',current_manifest=rel(BASE/'manifest.json'),current_run=rel(CHECK),current_model=rel(HERE/'model'),summary=SUMMARY,index=rel(BASE/'doi-chieu/index.json'),static_models=dict(entity=rel(BASE/'do-thi/thuc-the.json'),operation=rel(BASE/'do-thi/thao-tac.json'),projection=rel(BASE/'do-thi/chieu-thao-tac.json'),entity_only=rel(BASE/'do-thi/chi-thuc-the.json')),pin=rel(HERE/'pin.json'),delta=rel(CHECK/'delta.json'),analysis=rel(BASE/'phan-tich-chenh-lech.json'),source_audit=rel(HERE/'source-audit.json'),T040_required_changes=['Đổi STATIC_MODELS[TT] trong tong_hop.py từ run SMTP cũ sang static_models ở file này; không sửa lịch sử SMTP','Đổi summary TT từ runs/doi-chieu-smtp-001/checks/full1069-002/summary.json sang summary ở đây; pin chung giữ nguyên','Tổng hợp lại số relation/cạnh/entity-only, S/static_only/mẫu số/tỷ lệ tĩnh và full/family/union của TT từ output mới','Cập nhật OM-01/OM-02 và trạng thái R1 theo REVIEW/LOG mới và kết quả kiểm độc lập; không tự coi đã nghiệm thu','Phần T/giao/trace_only, mapping/exclusions phía trace và 90 operation structural result giữ nguyên tập/số và chỉ đổi mô tả SMTP; phần followup HTTP có thể dùng lại theo hash nếu giữ đúng điều kiện'],unchanged=['mapping','thresholds','method','common pin','T-035 inputs','entity/operation IDs/types/provenance','signals','bindings','trace-side output semantics'],source_decisions_open=['lineage/runtime','unknown protocol and discovery binding','PDF safe-source access','formal record of reviewer assignment and current authorization when Minh grants document scope'],not_accepted=True,not_G3_or_test_permission=True)
 handoff['T040_path_replacements']={
  'results/T-038/runs/doi-chieu-smtp-001/do-thi/thuc-the.json':rel(BASE/'do-thi/thuc-the.json'),
  'results/T-038/runs/doi-chieu-smtp-001/do-thi/thao-tac.json':rel(BASE/'do-thi/thao-tac.json'),
  'results/T-038/runs/doi-chieu-smtp-001/do-thi/chieu-thuc-the.json':rel(BASE/'do-thi/chieu-thao-tac.json'),
  'results/T-038/runs/doi-chieu-smtp-001/checks/full1069-002/summary.json':SUMMARY}
 handoff['T040_manifest_intake']='Kiểm manifest bản sửa và lưu pin của lần tiếp nhận mới; giữ pin cũ làm lịch sử. Không dùng expected hash cũ cho artifact cố ý chuyển phiên bản, hoặc sửa expected của pin lịch sử để hợp thức hóa lệch.'
 save(HERE/'ban-giao-T040.json',handoff)
 textfile(BASE/'ban-giao.md',f'''# Bàn giao hiện hành T-038 — sửa R1 và đồng bộ phiên bản

Gói Minh giao ngày17/10/2026 đã được người làm tiếp nhận và tự kiểm; chờ kiểm bản sửa, chưa nghiệm thu T-038. Điểm vào máy đọc: `{RUN}/ban-giao-T040.json`. Manifest: `results/T-038/manifest.json`; index: `doi-chieu/index.json`; model: `{rel(HERE/'model')}`; summary: `{SUMMARY}`. Graph canonical ở `do-thi/`, cùng byte với snapshot model. Pin chung SMTP V2 giữ nguyên, được kiểm bằng `{RUN}/pin.json`.

R1 đúng ở khâu nguồn→bản ghi, đã bổ sung bốn relation có provenance và profile condition. Mô hình:110 thực thể/993 thao tác/513 relation/50 binding/139 signal; cạnh170 entity/343 operation, projection122 và entity-only48. Delta từ SMTP V2:979 entity graph thêm4 S endpoints hoặc3 S typed; phần riêng tĩnh/mẫu số tăng tương ứng, typed thêm1 unknown exclusion. T/giao/phía trace giữ nguyên;90 output operation giữ nguyên cấu trúc/tập/số, chỉ đồng bộ mô tả SMTP. Nguồn số: `{RUN}/model-checks.json`, `{rel(CHECK/'verification.json')}`, `{rel(CHECK/'delta.json')}#/rows` và `phan-tich-chenh-lech.json#/source_counts`.

T-040 cần đổi các đường dẫn TT hardcode trong `results/T-040/tong_hop.py`: STATIC_MODELS[TT] dùng graph canonical nêu trong JSON bàn giao; summary TT dùng summary mới; pin vẫn cùng bản. Tính lại số nguồn/cạnh/entity-only, S/phần riêng tĩnh/mẫu số/tỷ lệ phía tĩnh và bảng family/full/union. Cập nhật OM-01/OM-02 theo phản hồi và kiểm bản sửa, giữ trạng thái chưa nghiệm thu. Một mô tả entity.role SMTP cũng đã đồng bộ V2; chỉ payload metadata node đổi. Chỉ mục inventory508→513 gồm1 SMTP tồn đọng và4 R1, xem inventory-index-delta.json trong run sửa. Phần T/giao/trace_only, mapping và HTTP match/mismatch không bị thay; chỉ dùng lại với hash và điều kiện phù hợp. Không dùng candidate reviewer hay run SMTP lịch sử làm nguồn hiện hành. Người làm T-040 xử lý trong quyền riêng; lượt này không sửa kết quả T-040.

Giới hạn: cấu hình không chứng minh runtime đã chạy; source khác revision RE2. UI→OAP, alert transport, scrape/discovery, Grafana datasource và Nacos client còn thiếu semantics/binding, nêu riêng trong `{RUN}/source-audit.json`. Cần chủ nguồn cung cấp semantics image/client, provisioning/discovery/override, hoặc Minh duyệt phạm vi đổi hợp đồng unknown protocol. Chủ dataset/Minh cần cung cấp source→build→image→instrumentation→deployment→dataset để nâng lineage. Body PDF cần bản/vùng an toàn từ chủ nguồn. Đây giới hạn kết luận đầy đủ và chọn đầu vào P6/P9, không phải bằng chứng thiếu collector. Không tự tải, đổi hợp đồng hoặc mở dữ liệu để lấp.

Tiêu chí task: (1) snapshot/bookkeeping đúng với giới hạn; chưa đủ semantic/runtime inventory; (2) bốn relation và SMTP đã dựng/chiếu/giữ entity-only đúng trong hợp đồng, còn protocol/binding OPEN; (3) đủ1069 graph và kiểm các tập/members/exclusions/mẫu số/interval; (4) phân tích mô tả và cơ chế bỏ bản ghi được chứng minh, nguyên nhân runtime mismatch còn OPEN; (5) bàn giao/prompt/manifest đủ để kiểm và tổng hợp lại. Không tự đóng P5/G3/RQ3/RQ5, chọn P6 hoặc mở test.

Tái lập hiện hành, vào tên lượt mới để giữ lịch sử:
`py -3 -X utf8 -B {RUN}/repair.py check replay-002`

Runner dùng bản ghi chính thức, kiểm baseline+accepted delta, pin, input và mọi graph; chỉ ghi run mới, không tái sinh model thiếu quan hệ hoặc ghi đè report. Các entrypoint cũ ghi root đã chặn chạy và có bản nguyên byte trong before/. Không chạy lại downloader/assembler cũ. Kiểm nhận và chi phí tại `{rel(CHECK/'cost.json')}`; thời gian máy không là giờ công hay benchmark cách ly. Prompt để Minh chuyển thủ công: `prompt-claude.txt`; chưa cấp quyền viết REVIEW mới.
''')
 textfile(BASE/'kiem-dung-dan.md',f'''# Tự kiểm bản sửa hiện hành

Nguồn kiểm: `{RUN}/source-checks.json` (11 điều kiện nguồn), `model-checks.json`, `{rel(CHECK/'verification.json')}`, `analysis-checks.json` và `final-verification.json` trong run sửa sau bước seal. Manifest bảo vệ nguồn, lịch sử, pin chung và input. Không đổi expected hash để chấp nhận nguồn lệch.

Đã kiểm bản ghi chính thức→build→graph→project→entity-only cùng bản; projection122 hợp entity-only48 bằng170 cạnh entity và không giao. 110 entity/993 operation/139 signal/50 binding, record cũ và mapping giữ nguyên; đồng bộ một mô tả role SMTP lịch sử; relation509→513. Operation edges343 giữ nguyên; thêm4 exclusion do không có operation evidence. Root phép chiếu121 là lỗi chưa tiếp nhận SMTP, đã sửa thành122.

Đủ1069/1069 graph theo index trước sửa và manifest T035:979 entity/90 operation. Tính độc lập từng khóa/members/reason exclusions/phân hoạch chỉ số/mẫu số/null/interval; replay bằng pin chung, lặp/đảo thứ tự/input bất biến và so toàn candidate đã kiểm. Delta từng graph được lưu, không sửa oracle theo kết quả. Operation output giữ nguyên tập/số và chỉ đổi mô tả SMTP; trace và giao của mọi graph giữ nguyên. Đã tổng hợp lại bảng theo family/full/union cùng chains.

Dùng lại các kiểm lịch sử nguồn/coverage/SMTP sau kiểm hash khi đầu vào không đổi; không chạy lại RCA hoặc ba nhánh không bị đổi. Tự kiểm này không thay phản biện chính thức hoặc nghiệm thu. Độ đủ nguồn ngữ nghĩa/runtime, lineage, protocol/binding và lợi ích RCA giữ OPEN theo source-audit và bàn giao.

Sự cố lượt này: công cụ đọc nguồn in lọt credential mặc định do che lọc chưa đủ. Đã báo Minh ngay; không chép giá trị đó vào file kết quả/báo cáo mới, không sử dụng để kết nối. Chi tiết không chứa giá trị tại `{RUN}/incident.json`. Sự cố phạm vi đọc lịch sử vẫn được giữ ở coverage/incident.json, không bị nhận là đã hoàn tác.
''')
 completion=dict(task='T-038',intent='EXECUTE',authorized_execution_complete=True,full_task_accepted=False,current_model=rel(HERE/'model'),current_comparison=rel(CHECK),source_counts=coverage['statuses'],criteria=[dict(id=1,status='PARTIAL_SEMANTIC_RUNTIME_COMPLETENESS_OPEN'),dict(id=2,status='R1_AND_SMTP_ADOPTED_KNOWN_UNKNOWN_PROTOCOL_LIMITS'),dict(id=3,status='MET_1069_ALL_DEV_GRAPHS'),dict(id=4,status='MET_DESCRIPTIVE_AND_SOURCE_OMISSION_MECHANISM_RUNTIME_OPEN'),dict(id=5,status='HANDOFF_READY_AWAITING_INDEPENDENT_CHECK')],evidence=[rel(HERE/'source-checks.json'),rel(CHECK/'verification.json'),rel(HERE/'ban-giao-T040.json')],research_questions_closed=False,method_changed=False,semantic_inventory_complete=False)
 overwrite(BASE/'hoan-tat-trong-quyen.json',completion)
 textfile(BASE/'hoan-tat-trong-quyen.md','# Mức hoàn tất hiện hành\n\nGói sửa R1 và trộn phiên bản đã tiếp nhận, đủ tự kiểm trên1069 graph; chờ kiểm độc lập bản sửa. Tiêu chí và phần còn thiếu tại hoan-tat-trong-quyen.json, ban-giao.md và source-audit của run sửa. Không nhận semantic/runtime inventory đầy đủ, nghiệm thu task, chọn P6 hoặc đóng G3/RQ3/RQ5. Các báo cáo trước SMTP là lịch sử trong before/, không là việc còn chờ duyệt hiện tại.\n')
 textfile(BASE/'de-nghi-tiep-theo.md',f'''# Bước kế tiếp của T-038

Minh chuyển `prompt-claude.txt` để kiểm độc lập bản sửa nếu chọn. Người làm không còn phản đối chưa xử lý đối với bốn relation R1 và sự nhất quán phiên bản; đề nghị dừng phản biện sau khi kiểm độc lập xác nhận, Minh quyết cuối. Chưa tự nghiệm thu.

T-040 dùng `{RUN}/ban-giao-T040.json`, cập nhật nguồn hardcode/bảng phụ thuộc S và OM-01/02 trong quyền task ấy. Giới hạn và input/owner cần để phân xử protocol/binding/lineage/PDF tại `{RUN}/source-audit.json` và ban-giao.md. Muốn mở rộng hợp đồng, nguồn hoặc ghi DECISIONS về lời giao/phân công reviewer cần Minh duyệt phạm vi riêng; không xin lại quyền sửa R1 đã giao.

Nội dung có thể ghi tài liệu quyết định sau duyệt riêng: Minh giao Codex người làm tiếp nhận R1, đồng bộ bản hiện hành và bàn giao T-040 ngày17/10/2026 trong phạm vi authorization.txt; giữ vai trò lịch sử, chưa nghiệm thu/G3/test/commit. Ngoại lệ reviewer kết quả theo REVIEW.md cần ghi đúng lời Minh, không tự áp cho lượt khác.

Commit chỉ đề nghị, chưa thực hiện: `T-038: tiếp nhận R1, đồng bộ graph và bàn giao T-040`.
''')
 textfile(BASE/'LICH-SU.md',f'''# Chọn đúng đầu ra hiện hành

Nguồn hiện hành là manifest.json, doi-chieu/index.json, ban-giao.md và `{RUN}/ban-giao-T040.json`. Model `{rel(HERE/'model')}` khớp graph canonical do-thi/; so sánh `{rel(CHECK)}`. Bản SMTP V2 ở runs/doi-chieu-smtp-001 và candidate reviewer giữ nguyên lịch sử, không còn là selector hiện hành. Pin chung vẫn SMTP V2.

before/ trong run sửa giữ nguyên byte mọi root được thay và LOG/REVIEW/STATE trước lượt. Các run/lượt lỗi cũ không sửa/xóa. Các script root ghi report/model trước đây đã được chặn chạy; runner hiện hành ở ban-giao.md và commands.json. Nguồn tải/metadata/tool tải là lịch sử; không chạy để tái lập gói sửa.

SPEC giữ mốc lịch sử; quyền thực hiện theo authorization.txt và LOG. Codex là người làm, reviewer kết quả là Codex phiên độc lập do Minh chỉ định trong REVIEW.md; không đổi phân công lịch sử. Task chưa nghiệm thu.

Giữ hạn chế đọc lịch sử: ba index coverage/content/archive ban đầu đã cách ly do telemetry mẫu, chỉ hash, không parse. Chỉ dùng bản clean và followup có phạm vi đã kiểm. Không mở mẫu/raw/test/heldout/archive hoặc body PDF; xem metadata incident trong báo cáo coverage.
''')
 oldsmtp=(BEFORE/'goi-sua-SMTP.md').read_text(encoding='utf-8-sig')
 textfile(BASE/'goi-sua-SMTP.md',f'''# Gói SMTP lịch sử

SMTP V2 đã được duyệt và tiếp nhận16/10/2026; nội dung đề nghị cũ nguyên byte tại `{rel(BEFORE/'goi-sua-SMTP.md')}`. Không dùng trạng thái chờ duyệt trong bản ấy làm trạng thái hiện hành. Bản sửa hiện hành và pin ở ban-giao.md và manifest.json. Lượt sửa R1 này giữ chung pin V2, không đổi hợp đồng.
''')
 for name in RETIRED:
  textfile(BASE/name,'"""Historical root writer retired; original bytes retained in the current repair before/."""\nif __name__ == "__main__":\n    raise SystemExit("Entrypoint lịch sử đã ngừng. Tái lập hiện hành: py -3 -X utf8 -B '+RUN+'/repair.py check <fresh-run-name>. Xem results/T-038/ban-giao.md")\n')
 commands=load(BEFORE/'commands.json');commands['current_reproduction']=dict(command='py -3 -X utf8 -B '+RUN+'/repair.py check <fresh-run-name>',published_run=rel(CHECK),no_root_overwrite=True,historical_root_writers_retired=RETIRED);commands['client_dates']=sorted(set(commands['client_dates']+['2026-10-17']));overwrite(BASE/'commands.json',commands)
 p=prompt();textfile(HERE/'prompt-kiem-ban-sua.txt',p);textfile(BASE/'prompt-claude.txt',p);textfile(BASE/'prompt-claude-smtp.txt',p)
 save(HERE/'incident.json',dict(type='credential-defaults-visible-in-tool-output',cause='Line-based redaction failed to suppress following YAML values and a misspelled key.',reported_immediately=True,new_artifacts_contain_values=False,credential_used_for_connection=False,mitigation='No further literal source dumps; record checks only booleans, locators and hashes. Existing tool output cannot be undone.',task_effect='Disclosure in tool output; not scientific evidence or runtime access. No secret values repeated here.'))
 with (ROOT/'tasks/T-038-p5b-trainticket/LOG.md').open('a',encoding='utf-8') as f:
  f.write(f'\n### Kết thúc gói sửa và bàn giao Phiên 3 — 17/10/2026\n\nQuyết định của Minh trong phiên: thực hiện nguyên gói authorization.txt; không có lựa chọn phương pháp mới, không tự ghi DECISIONS ngoài quyền. Giữ vai trò người làm; reviewer chính thức theo REVIEW.md.\n\n1. Đã làm: tự soát trước review; kiểm manifest/pin/package reviewer, nguồn trực tiếp và từng delta; R1 đúng, lỗi nguồn→bản ghi. Đã tiếp nhận bốn relation có điều kiện và dựng lại graph canonical/projection/entity-only. Tự kiểm đủ1069 graph, tổng hợp lại số và bàn giao T040; không dừng ở candidate. Bằng chứng: {RUN}/source-checks.json, model-checks.json, {rel(CHECK/"verification.json")}, analysis-checks.json và ban-giao-T040.json.\n2. File đổi: đúng impact-map.json; results/T-038/ bản hiện hành/run mới, nối LOG này, chỉ bảng phản hồi REVIEW và chỉ dòng T038 STATE. Nguồn/lịch sử/mapping/pin chung/src/T035/T036/T040 không sửa. before/ giữ byte trước và file-set/diff ở final-verification.\n3. Kiểm:11 điều kiện nguồn; rebuild/chiếu170=122+48;110 entity/993 operation/513 relation/139 signal/50 binding.979 entity: endpoints+4 S/static-only, typed+3 và1unknown exclusion;90 operation output giữ nguyên tập/members/exclusions/số, chỉ đổi mô tả SMTP. Toàn T/giao/trace members/exclusions giữ nguyên. Kiểm độc lập tập/members/reason/mẫu số/null/interval, replay/candidate/lặp/đảo/input bất biến. Chi phí máy ở checks/full1069-002/cost.json, không là giờ công hoặc benchmark. Các kiểm cũ có input không đổi được dùng lại sau hash.\n4. Phần thiếu/cần Minh quyết: gói sửa đáp ứng biểu diễn bốn relation, thống nhất phiên bản và kiểm/bàn giao; task tiêu chí1/2 còn giới hạn semantic inventory/protocol/binding/lineage; tiêu chí3 đạt,4 đạt mô tả và cơ chế bỏ bản ghi,5 có bàn giao để kiểm. Chưa trả lời lợi ích RCA, nguyên nhân runtime mismatch/RQ3/RQ5/P6/G3/test. Owner/đầu vào cần ở source-audit và ban-giao.md. Đề nghị dừng phản biện sau kiểm độc lập xác nhận bản sửa; Minh quyết, chưa nghiệm thu.\n\nĐáp REVIEW: R1 đúng/CHẶN trước sửa; đã xử lý phạm vi có nguồn. N1 đúng/CHẶN trước sửa, đã đồng bộ; N2 đúng/CHẶN trước sửa, đã công bố runner và chặn entrypoint cũ; N3 kiểm thành R1 đúng có giới hạn. N4 phát hiện trong kiểm cuối: inventory-index còn508 và role SMTP ghi unsupported; đã đồng bộ chỉ mục513 và mô tả V2, không đổi định danh/type/provenance/phép tính. Lượt full1069-001 được giữ cùng model/script đã dùng; sau sửa metadata kiểm lại đầy đủ ở full1069-002. Các nhận xét lịch sử về SMTP/harness/cờ initializer được dùng lại sau đối chiếu nguồn/hash; sự cố raw trước đây không thể hoàn tác. Bảng chi tiết trong REVIEW chỉ do người làm điền phần được phép.\n\nSự cố phiên3 đã báo ngay: lượt in nguồn để lọt credential mặc định do bộ che lọc chưa đủ. Không đưa giá trị vào file kết quả/báo cáo mới hoặc dùng để kết nối; lưu metadata không chứa giá trị tại incident.json của run sửa. Không thể hoàn tác đầu ra công cụ đã hiển thị.\n\nBước tiếp chính xác: đọc {RUN}/final-verification.json, ban-giao-T040.json và manifest.json; Minh chuyển prompt dưới để reviewer kiểm độc lập. T040 đổi đường dẫn TT hardcode và tổng hợp lại đúng danh sách trong JSON bàn giao, theo quyền task đó; không tự chạy/sửa T040 trong phiên này. Tái lập khi cần: py -3 -X utf8 -B {RUN}/repair.py check replay-002. Lệnh cuối bước tính: py -3 -X utf8 -B {RUN}/repair.py check full1069-002; lệnh kết phiên: py -3 -X utf8 -B {RUN}/final_verify.py. Không có tiến trình cần chuyển giao sau kiểm kết thúc.\n\nCommit đề nghị khi Minh cho phép riêng: T-038: tiếp nhận R1, đồng bộ graph và bàn giao T-040. Chưa commit/push.\n\n### Prompt kiểm độc lập bản sửa — Minh chuyển thủ công\n\n```text\n'+p+'```\n')
 review=ROOT/'tasks/T-038-p5b-trainticket/REVIEW.md';raw=review.read_text(encoding='utf-8-sig');old='| R1 | | | |';assert raw.count(old)==1
 rows=f'''| R1 | Đúng; CHẶN bản thiếu trước sửa, đã tiếp nhận, chờ kiểm bản sửa | Kiểm độc lập11 điều kiện nguồn; thêm4 relation cấu hình có điều kiện vào bản chính thức, dựng170/343, projection122/entity-only48; kiểm đủ1069 graph. Ba data+webhook unknown không chứng minh runtime. Bằng chứng: {RUN}/source-checks.json; model-checks.json; checks/full1069-002/verification.json; ban-giao-T040.json. Không còn candidate-only; chưa tự nghiệm thu. | |
| N1 | Đúng; CHẶN trước sửa, đã sửa | Tự tìm trước REVIEW: root graph V2 với projection121/entity-only44 cũ. Canonical hiện tại122+48=170; snapshot và index cùng bản. Bằng chứng model-checks.json và final-verification.json trong run sửa. | |
| N2 | Đúng; CHẶN trước sửa, đã sửa | Root runner ghim R1 và bỏ SMTP. Đã giữ byte cũ, chặn các root writer lịch sử; repair.py công bố nhận pin tường minh, kiểm bản ghi gốc+delta và đủ1069 graph, chỉ ghi lượt mới. | |
| N3 | Đúng một phần; đã phân xử phần nguồn của R1 | Tự soát chỉ nêu nghi vấn độ đủ relation support. Sau kiểm nguồn xác nhận4 omission; các địa chỉ thiếu protocol/binding vẫn OPEN với input/owner tại source-audit.json, không nhận đủ toàn semantics/runtime. | |
| N4 | Đúng; lỗi mô tả/chỉ mục hiện hành, đã sửa | inventory-index cũ chỉ đếm508; bản513 gồm4 R1 và1 SMTP đã thiếu trong chỉ mục. Sửa một entity.role SMTP lịch sử thành mô tả V2; chỉ metadata node đổi. Xem metadata-correction.json, metadata-checks.json và inventory-index-delta.json; full1069-002 kiểm lại toàn phạm vi. | |
| Lịch sử SMTP, initializer, harness | Đúng trong phạm vi bằng chứng được giữ | Pin V2/đầu vào lịch sử khớp;90 operation replay giữ nguyên tập/số, chỉ đổi mô tả SMTP và mọi T/giao không đổi.9 cờ initializer có if/else cùng source đã kiểm hash, không thành runtime proof. Sai harness001 là phép kiểm cũ, không đổi oracle để PASS. | |
| Sự cố đọc mẫu lịch sử | Đúng; giữ vi phạm đã xảy ra | Incident metadata và registry không tham chiếu đường cách ly; không mở lại nội dung mẫu ở lượt này. Sự cố credential tool-output phiên3 đã báo riêng, lưu incident.json không có giá trị; không thể hoàn tác lần hiển thị. | |'''
 # Preserve every reviewer byte outside the table, including CRLF.
 rb=review.read_bytes();assert old.encode() in rb;review.write_bytes(rb.replace(old.encode(),rows.replace('\n','\r\n').encode(),1))
 state=ROOT/'docs/STATE.md'
 with state.open('r+b') as f:
  original=f.read();decoded=original.decode('utf-8-sig');oldrow=next(x for x in decoded.splitlines() if x.startswith('| T-038 |'))
  newrow='| T-038 | P5b: nguồn tĩnh Train Ticket và RE2-TT dev | P5 (G3) | Codex | Claude (kết quả; ngoại lệ Codex theo REVIEW) | Chờ kiểm bản sửa17/10/2026: người làm đã đáp/tiếp nhận R1, đồng bộ graph170/343, chiếu122 và entity-only48; đủ1069graph đạt,90operation giữ tập/số,đổi mô tả SMTP,T/giao giữ nguyên. Current manifest/index và bàn giao T040 tại results/T-038/runs/sua-r1-20261017-001/. Giữ pin SMTP V2 và lịch sử. Semantic/protocol/binding/lineage/runtime OPEN; chưa nghiệm thu/P6/G3/test/commit. | `tasks/T-038-p5b-trainticket/` |'
  assert original.count(oldrow.encode())==1;new=original.replace(oldrow.encode(),newrow.encode(),1);f.seek(0);f.write(new);f.truncate()
 save(HERE/'publication.json',dict(all_pass=True,summary=SUMMARY,current_model=rel(HERE/'model'),current_run=rel(CHECK),metadata_correction=rel(HERE/'metadata-correction.json'),inventory_delta=rel(HERE/'inventory-index-delta.json'),task_accepted=False,awaiting_independent_check=True))
 print(canon(dict(published=True,awaiting_independent_check=True,root_changes=len(ROOT_CHANGED))),flush=True)
if __name__=='__main__':main()
