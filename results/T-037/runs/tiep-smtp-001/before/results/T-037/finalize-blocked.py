"""Assemble partial source artifacts and an explicit blocked handoff; no graph conversion."""
import collections
import difflib
import hashlib
import json
import msvcrt
import pathlib
import re
import subprocess
import sys

ROOT=pathlib.Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037'
LOG=ROOT/'tasks/T-037-p5b-flashticket/LOG.md';STATE=ROOT/'docs/STATE.md'
RUN=BASE/'runs/ket-phien-001'
RUN.mkdir(parents=True,exist_ok=False)

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,s):p.write_text(s,encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()

pre=load(BASE/'runs/tu-ra-001/preflight.json');source=load(BASE/'nguon.json')
docs=[load(BASE/f'records-{name}.json') for name in ['data','infra','flow']]
doc={'scope':docs[0]['scope']}
for col in ['entities','operations','relations','resource_bindings','signals']:
 doc[col]=sum([d[col] for d in docs],[])
dump(BASE/'ban-ghi.json',doc)
units=load(BASE/'coverage-data.json')+load(BASE/'coverage-infra.json')+load(BASE/'coverage-flow.json')['units']
counts={k:len(doc[k]) for k in ['entities','operations','relations','resource_bindings','signals']}
source_index={s['id']:s for s in source['sources']}
entities={r['id']:r for r in doc['entities']}
ops={(r['entity'],r['name']):r for r in doc['operations']}
all_ids=set(entities)|{r['id'] for col in ['relations','resource_bindings','signals'] for r in doc[col]}
checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
check('unique entity IDs',len(entities)==len(doc['entities']))
check('unique operation pairs',len(ops)==len(doc['operations']))
check('all runtime operation names remain null',all(x['runtime_name'] is None for x in doc['operations']))
check('every operation has an inventory owner',all(x['entity'] in entities for x in doc['operations']))
check('signals address existing entity/operation',all(x['entity'] in entities and (x['operation'] is None or (x['entity'],x['operation']) in ops) for x in doc['signals']))
check('shared signals are not copied onto operation',all(not x['shared'] or x['operation'] is None for x in doc['signals']))
check('all relation endpoints exist',all(e['entity'] in entities and (e['operation'] is None or (e['entity'],e['operation']) in ops) for x in doc['relations'] for e in [x['source'],x['target']]))
check('all binding references exist',all(x['entity'] in entities and x['resource'] in entities for x in doc['resource_bindings']))
check('partial records do not coerce SMTP into any accepted channel',all(not (x['source']['entity']=='ticket-service' and x['target']['entity']=='smtp') for x in doc['relations']))
check('no invented Ticket to Booking dependency',all(not (x['source']['entity']=='ticket-service' and x['target']['entity']=='booking-service') for x in doc['relations']))
check('all provenance sources pinned',all(p['source_id'] in source_index and p['locator'] and p['condition'] for col in ['entities','operations','relations','resource_bindings','signals'] for x in doc[col] for p in x['provenance']))
check('every coverage row references pinned source',all(u['source_id'] in source_index for u in units))
check('every coverage record id exists',all(i in all_ids for u in units for i in u['record_ids']))
check('every coverage entity exists',all(i in entities for u in units for i in u['entity_ids']))
check('every snapshot matches source hash',all(sha(ROOT/s['snapshot'])==s['sha256'] for s in source['sources']))
check('live platform source unchanged',all(sha(pathlib.Path(s['path']))==s['sha256'] for s in source['sources']))
check('oracle source lists six DB owner edges',{(r['source']['entity'],r['target']['entity']) for r in doc['relations'] if r['id'].startswith('d-')}=={tuple(x) for x in load(BASE/'oracle.json')['data_edges']})
check('five logical PG databases remain separate on one PG instance',sorted(x['entity'] for x in doc['resource_bindings'] if x['relation']=='hosted_on' and x['resource']=='postgresql-shared-instance')==sorted(load(BASE/'oracle.json')['shared_postgresql_databases']))
smtp=load(BASE/'runs/smtp-002/result.json')
check('SMTP rejection reproduced against pinned API for both candidate types',smtp['all_reproduced'] and len(smtp['cases'])==2)
input_checks=[]
for manifest in pre['manifests']:
 for row in manifest['files']:
  p=(ROOT/row['path']).resolve()
  assert p.is_relative_to(ROOT) and not p.is_relative_to(ROOT/'data')
  input_checks.append({'path':row['path'],'matches':p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256']})
check('all T035/T036 protected result hashes unchanged',all(x['matches'] for x in input_checks),len(input_checks))
for x in pre['current_code']:
 check('pinned common code unchanged: '+x['current'],sha(pathlib.Path(x['current']))==x['sha256'])
dump(RUN/'input-hashes-final.json',input_checks)
dump(RUN/'partial-record-checks.json',checks)
dump(BASE/'bao-phu-nguon.json',{'task':'T-037','state':'PARTIAL_BLOCKED_SMTP','coverage_completion_claim':False,
 'sources_read':list(source_index),'source_closure_complete':False,'counts':counts,'units':units,
 'remaining':['No full source requirement→record→graph/projection/binding/signal verification',
              'No full graph or runtime correspondence fixtures','Derived code/config content crosscheck not complete',
              'Oracle initial HTTP/SMTP error invalidated; must write correct full oracle before conversion after contract resolution'],
 'unsupported_counterexample':'results/T-037/counterexample-smtp.json'})

write(BASE/'bao-phu-nguon.md',f'''# Bao phủ nguồn T-037 — phần đã làm, chưa hoàn tất

**Trạng thái: PARTIAL / chờ Minh quyết chặn SMTP.** Không phải inventory/graph toàn phạm vi đã kiểm.

Đã đọc năm nguồn thiết kế chính, 10 sơ đồ và bốn README baseline. Nguồn cùng hash, revision, dirty state và bản nội dung ghim ở nguon.json; snapshot ở runs/nguon-001/. Năm nguồn chính: 2.237 dòng / 192.902 byte. Sơ đồ: 743 dòng / 23.050 byte. Đọc nguồn không tự chứng minh mọi yêu cầu đã ánh xạ đúng.

Lưu {len(units)} đơn vị nguồn và {counts['entities']} thực thể, {counts['operations']} thao tác có tên thiết kế, {counts['relations']} bản ghi quan hệ, {counts['resource_bindings']} binding, {counts['signals']} địa chỉ tín hiệu dự thảo. Số lấy từ bao-phu-nguon.json#/counts và #/units. Không có event_count hoặc observed_nodes/tập ứng viên runtime được suy từ các số này.

| Nhóm bắt buộc | Bằng chứng đã lưu | Phần còn thiếu / ảnh hưởng |
|---|---|---|
| HTTP/RPC/gateway | B13 buyer API, freeze/probe/financial summary; records-flow | Không có nguồn RPC riêng để tự thêm; graph/chiếu chưa kiểm |
| DB logic/instance chung | B12 §2/§12/§13, năm ERD; records-data | 47 bảng/467 cột SQL, 4 collection được giữ theo datastore; không tạo 467 operation. Endpoint/process/host runtime OPEN |
| Cache | B11-C-02 Booking→cache; records-infra | Công nghệ/địa chỉ/tên thao tác chưa có nguồn; không tự điền Redis từ bối cảnh cũ |
| Messaging/queue/fan-out/retry | B13 §5; routes giữ exchange/routing/consumer có nguồn | Queue và broker scope vẫn null; chưa thể đối chiếu địa chỉ runtime hoặc coi fan-out đã chạy |
| Outbox/inbox | Mỗi SQL owner có bảng riêng; B13/B14 ghi transaction/confirm/ACK/dedup | Không suy bảng tồn tại là worker chạy đúng; relay/processing/attempt phải kiểm fixture sau |
| Callback/query | B13 §5.3/B16 §3; thiết kế callback mới và provider query | Không nối trace từ correlation; chưa có telemetry hoặc toàn fixture đối chiếu |
| Scheduler | B14 expiry/refund/delivery/relay; B13 role-grant/projection | Không tạo caller; tên runtime/frequency/lease còn phải kiểm triển khai |
| Saga/bù trừ/terminal fence | B13 commands và B14 §3–§5 | Không Ticket→Booking giả. Chưa graph/chiếu/fixture terminal fence đầy đủ |
| Delivery/check-in | B13 §6/B14 §6/B14-03 | **SMTP không biểu diễn được theo channel hiện hành; chặn graph đầy đủ** |
| Role-grant/projection | B12 §4.5/§6, B13 §9, B16 §5 | Admin API quyền/tên endpoint/token/realm runtime OPEN; không bịa Keycloak→User message |
| Hỗ trợ/vận hành | B11-C §5/§6, B16 stack/resource/retention/quyền | Inventory riêng; chưa chọn tập ứng viên P6. Địa chỉ metric thật và transport pipeline chưa xác minh |

Các status `covered_design` trong coverage-data.json chỉ nói đoạn dữ liệu được dẫn vào bản ghi nguồn, không là toàn graph hay cơ chế đã kiểm. Các status `represented_design_partial` ở coverage-flow cũng là phần trích nguồn chưa được converter/graph kiểm. Tổng không phải tỷ lệ hoàn thành task.

Nguồn dẫn xuất SQL/Mongo/realm chỉ thống kê metadata trong nguon.json#/derived_scope; chưa đọc nội dung test. Chưa gọi nguồn đóng đầy đủ. Phần legacy/archive và URL bên ngoài được loại có lý do/ảnh hưởng, không tự tải để bù.
''')

write(BASE/'kiem-dung-dan.md',f'''# T-037 — tự rà và phản ví dụ chặn triển khai

**Task chưa đạt tiêu chí xong; không có graph toàn phạm vi được dựng.** Không sửa SPEC/hợp đồng chung. Tự rà người làm không thay Claude phản biện chính thức.

Pin/hash trước dùng: runs/tu-ra-001/preflight.json. T-036 187/187 và T-035 5.667/5.667 entries khớp; mã hiện hành khớp snapshot đã giao. Chưa mở REVIEW cũ trước khi ghi nhận xét độc lập trong LOG Phiên2. Sau đó đọc REVIEW và mốc đóng T-036: công cụ đã được nghiệm thu trong phạm vi trước, không là chứng cứ nó phủ SMTP.

## Chặn đã tái lập

B13 L199, B14 L82, B14-03 L9–12 quy định Ticket gửi SMTP ngoài transaction, timeout có thể đã gửi. T-036 hop-dong.md §2 và snapshot code/build.py L10–11, L161–169 chỉ nhận channel gọi http/rpc/internal. Với transport SMTP giữ nguyên, cả hai nhãn gọi tổng hợp đều bị `ValueError('relation_type')`. Kết quả: runs/smtp-002/result.json#/cases; input không bị sửa. Phản ví dụ và oracle literal: counterexample-smtp.json, được ghi trước runner phản ví dụ.

Đây là thiếu biểu diễn của hợp đồng nguồn tĩnh, không phải lỗi dataset, collector hoặc kết luận về thuật toán RCA. Không gán SMTP thành HTTP/RPC/internal, không biến nó thành messaging broker. Các trường context/provenance có thể giữ chữ SMTP nhưng không thay địa chỉ/channel cấu trúc bị thiếu. Cần Minh duyệt xử lý hợp đồng chung trước phần graph phụ thuộc.

## Tự phát hiện và giữ lỗi của lượt này

- oracle.json ban đầu xếp Ticket→SMTP vào http_edges. Nguồn bác bỏ đáp án ấy. Giữ file gốc, vô hiệu cho dựng graph; không sửa kết quả để theo oracle sai. Chưa có converter riêng T-037 tại thời điểm phát hiện.
- runs/smtp-001 giữ input/registry/oracle/code/failure. Lượt này lỗi ở phép đo RAM do ctypes chưa khai argtypes; đã sửa riêng runner T-037 và chạy tên mới smtp-002. Không phải finding khác của T-036.
- Lượt đọc gộp có đường dẫn WHY/DECISIONS nhầm cwd platform đã báo lỗi không có file; đã đọc đúng bản RCA. Các output bị cắt không được dùng thay toàn nguồn.

## Kiểm độc lập còn làm được

Partial records chỉ kiểm JSON/ID/reference/provenance/shared signal và các cạnh DB literal. Kết quả {sum(x['pass'] for x in checks)}/{len(checks)} tại runs/ket-phien-001/partial-record-checks.json. Đây không là kiểm build/project đầy đủ. Coverage từng requirement tới graph/chiếu chưa thực hiện vì graph dừng tại chặn SMTP.

Không mở test/heldout/telemetry thô, không chạy baseline/P6/T040/EC2. Không tải nguồn. Không commit/push hoặc sửa code chung. Các nhánh hỗ trợ là thu thập nguồn của người làm, không reviewer chính thức hay chat ngoài.

## Chi phí

Dự toán trước triển khai: 5–8 giờ công tổng, 5–15 phút máy, peak RAM <0,5 GiB và tối đa 200 MB kết quả cho 10 lượt, **chưa đo**. Không xác nhận dự toán full task từ phản ví dụ nhỏ. Full pilot, tự kiểm/phân xử/bàn giao đầy đủ vẫn chưa chạy; sau khi giải quyết hợp đồng phải dự toán lại theo phạm vi không đổi.

Phép đo nhỏ smtp-002: hai build calls {smtp['seconds_two_build_calls']:.9f} giây; peak working set {smtp['process_memory']['peak_working_set_bytes']} byte cho process. Trước chạy đã lấy mẫu CPU1giây không process vượt0,25CPU-second; chỉ có thu thập/ghi nguồn nhẹ. Không dừng process khác. Số này chỉ mô tả phản ví dụ, không ngoại suy whole task. Hash preflight khi hai nhánh đọc nguồn đồng thời không là benchmark.

Kích thước thực của tất cả lượt và snapshot sẽ ghi manifest.json#/total_output_bytes, gồm lượt lỗi, bản oracle bị vô hiệu, metadata, nguồn và script. Không sao lại toàn graph T035/T036 vào từng run; tải/giải nén mới =0. Q40 áp ngân sách baseline, không dùng nó để giảm coverage thiết kế.
''')

write(BASE/'hop-dong-runtime.md','''# Đầu vào đối chiếu runtime — bản chưa hoàn thiện

PARTIAL. Đây là bàn giao yêu cầu quan sát từ thiết kế; chưa là hợp đồng runtime đã xác minh hoặc đã thu dữ liệu. Graph/fixture đầy đủ dừng vì SMTP. Tên thao tác thiết kế không là span.name/operationName thực.

| Phần | Nơi phải ghi / owner | Trường và kiểm cần |
|---|---|---|
| HTTP/gateway/internal | instrumentation ứng dụng và gateway | build, service/instance/environment, peer, kind, method/route logic, trace/span/parent, requestId; alias có revision; internal không mở qua gateway |
| DB logic/instance/host | config/deployment + instrumentation/metric exporter | owner, database logic, instance/resource ID, hostId đã xác minh và thời gian hiệu lực. Giữ 5 DB logic trên một PG instance; không suy instance từ tên DB |
| Broker/message | ứng dụng outbox/inbox + broker/config | broker/scope/vhost/exchange/routing/queue/binding và message identity scope; logical message, publish/delivery/processing attempts khác nhau; link semantics đã kiểm. Correlation không nối bản tin |
| Queue/shared metric | exporter + P9b | một địa chỉ broker+scope+queue; CPU/RAM/pool đúng service/instance/host. Metric chung operation=null, không nhân theo số cạnh/operation |
| Callback/query | Payment/adapter provider | callback trace mới; attempt/charge liên kết sau verify; provider client span + response/query, không tuyên bố lỗi bên trong provider |
| Scheduler/relay | owner ứng dụng | mỗi item/lần xử lý trace riêng, job/message/lease/retry/outcome; không caller giả, không nối parent bằng correlation |
| Saga/terminal fence | Payment/Booking/Ticket | quyết định trước/sau, reason, accepted charge, command/result, commit/outbox/ACK và terminal failure; timeout không là FAILED |
| SMTP delivery | Ticket/SMTP adapter | transport SMTP, delivery ID/attempt/outcome/latency, trace mới và correlation từ job; timeout có thể đã gửi, không tạo vé/refund. Hợp đồng tĩnh hiện chưa giữ được channel này |
| Check-in | Ticket | mỗi receipt/replay_of và result, trạng thái trước/sau, owner/window; không raw QR/JWT |
| Role-grant/projection | User/Keycloak | operationId/subject/kết quả/query/retry/sourceVersion, nguồn login đúng identity. Quyền Admin API/realm phải kiểm, không log token |
| Kho quan sát/RCA | vận hành/P9b | UTC/observed time/clock offset, sampling/drop/exporter/retention và manifest workload/build; RCA chỉ đọc, không DB nghiệp vụ |

Sau giải quyết hợp đồng: viết oracle và fixture tổng hợp đúng nguồn trước converter; kiểm nhiều queue/shared instance, thiếu mapping/address, callback trace mới, scheduler không caller và correlation không tạo edge. Chưa có các fixture đối chiếu đầy đủ này trong T037. Collector không thể khôi phục trường chưa được nguồn ghi.
''')

write(BASE/'ban-giao.md','''# T-037 — bàn giao phần dừng do chặn hợp đồng

**Cần Minh quyết gói sửa chung. Task chưa hoàn tất, chưa chờ nghiệm thu.** Người làm Codex; Claude phản biện kết quả. Không tự mở lại T-036 đã đóng, không đổi pin hoặc gửi sang chat khác.

Đã có pin/hash và snapshot nguồn, bản ghi thiết kế một phần, coverage một phần và phản ví dụ SMTP tái lập. Xem kiem-dung-dan.md, bao-phu-nguon.json và runs/smtp-002/result.json. Chưa có graph/chiếu/binding/signal được kiểm toàn phạm vi hoặc oracle đúng đầy đủ sau chặn. Các bản ghi hiện có không được dùng như đầu vào P6 đã nghiệm thu.

## Vấn đề và phương án cần duyệt

Nguồn B13 §6/B14 §6 đòi Ticket→SMTP. T036 chỉ cho channel gọi http/rpc/internal. Không có channel vừa giữ đúng SMTP vừa được builder nhận. Chữ trong context/provenance không thay được transport ở cấu trúc; gán rpc/internal/http hoặc bỏ cạnh đều làm đổi nghĩa/phạm vi. Đây là lỗi thiết kế hợp đồng trong trường hợp mới được khảo sát, không là bằng chứng phương pháp RCA thất bại.

**CANDIDATE khuyến nghị:** bổ sung channel `smtp` tường minh cho quan hệ gọi, giữ type là vấn đề riêng phải đối chiếu nguồn. Giữ nguyên ID/provenance và phép chiếu; không tạo broker/email queue giả. Chỉ phần mới có channel SMTP; đầu vào cũ phải giữ kết quả. Comparator non-messaging hiện so đầu mút/type không xác nhận transport, vì vậy phải khai giới hạn HTTP/RPC/SMTP tương ứng; không đổi typed agreement thành xác minh protocol. Chưa chọn hoặc thực hiện phương án này.

Phương án khác: trường transport riêng với channel chung. Nó tổng quát hơn nhưng đổi schema/địa chỉ và phạm vi hồi quy rộng hơn; cần thiết kế và duyệt riêng. Giữ nguyên hợp đồng và ghi unsupported là trạng thái dừng hiện tại, không đủ để nhận mô hình FT đầy đủ hoặc bỏ delivery khỏi nghiên cứu.

## Phạm vi sửa đề nghị — chưa được phép làm

| File/phạm vi | Cũ → mới dự kiến; lý do/ảnh hưởng |
|---|---|
| src/do_thi_tinh/build.py | CHANNELS và guard gọi chỉ http/rpc/internal → nhận smtp theo phương án được Minh chọn; không sửa nghĩa internal/rpc để lách |
| results/T-036/hop-dong.md | Mô tả channel/kiểu/chiếu và giới hạn so transport → bổ sung SMTP/điều kiện loại gọi; không tự thay đổi quy tắc messaging |
| results/T-036/fixtures/smtp-input.json, smtp-expected.json | Thêm phản ví dụ literal/đáp án trước mã, cả hai mức, entity-only, shared signal và projection; chưa là fixture runtime |
| results/T-036/check.py | Thêm kiểm representation SMTP và hồi quy đầu vào cũ; không chạy lại vào tên run cũ |
| results/T-036/kiem-dung-dan.md, ban-giao.md, manifest.json và runs/<tên mới được giao>/ | Giữ mọi lượt, đo/kiểm/diff, snapshot/code-hashes/manifest mới; pin cũ giữ nguyên lịch sử |
| tasks/T-036-p5b-hop-dong-chung/LOG.md và đúng dòng T036 trong docs/STATE.md | Chỉ khi Minh quyết mở gói sửa; không tự mở lại từ T037 |
| docs/WHY.md, docs/DECISIONS.md | Trình và lưu riêng lựa chọn cùng quyền sửa/pin mới sau Minh duyệt; không ghi trong lượt này |
| tasks/T-037-p5b-flashticket/SPEC.md, tasks/T-038-p5b-trainticket/SPEC.md, tasks/T-039-p5b-online-boutique/SPEC.md | Pin hiện hành bị khóa. Sau sửa chung, trình cập nhật đúng đoạn pin ở cả ba SPEC và dòng tương ứng STATE theo quyền riêng; chưa đổi bất kỳ pin nào |
| results/T-037/oracle-v2.json và outputs/runs T037 tiếp theo | Viết oracle đúng đầy đủ trước converter, kiểm lại coverage/graph/chiếu/runtime fixture và bàn giao; không xóa oracle sai/lượt lỗi cũ |

Đây là bản đồ tác động để Minh chọn/duyệt gói cụ thể, không là lệnh mở task hoặc quyền sửa. T036 đã đóng: cần Minh quyết cách ghi nhận gói sửa và phạm vi, không tự đổi trạng thái vật chất của quyết định. Không đề nghị sửa platform/B13/B14 vì SMTP là nhu cầu thiết kế hiện có.

## Ảnh hưởng ba nhánh và nơi nhận

- T037: dừng graph/phép chiếu/khẳng định coverage đầy đủ; giữ nguồn/records độc lập. Không thu hẹp tiêu chí vì SMTP.
- T038/T039: không khẳng định hai hệ này có SMTP vì chưa khảo sát trong phiên này. Có thể tiếp tục phần độc lập với pin cũ; phần cần transport ngoài enum phải dừng. Không tự chuyển pin, không tự gửi cảnh báo sang chat khác. Sau gói sửa chung phải thống nhất một pin trước kết luận tổng hợp.
- T040: chưa được làm; tổng hợp không được gọi hợp đồng đã phủ FT từ kết quả T036 cũ.
- P6: phép dùng cạnh/binding/shared metric còn phải thiết kế trên dev; chưa chọn thuật toán/mức/tín hiệu. T037 không chứng minh sửa hạn chế P4 hoặc lợi ích đồ thị.
- P9a/P9b/nhóm hệ thống: cần địa chỉ/transport/message scope/host/instance và build/export/sampling/clock; riêng SMTP phải ghi tại Ticket/adapter, không giao collector tái tạo. Hợp đồng runtime hiện chỉ bàn giao phần chưa hoàn thiện.
- RQ3/RQ5/G3 vẫn OPEN; chưa kiểm hiệu quả trên public test hoặc FlashTicket. Không mở dữ liệu khóa.

## Nội dung cần lưu chính thức sau duyệt riêng

Đề nghị thêm một mục DECISIONS (không tự cấp mã): “Minh giao Codex triển khai T-037 theo SPEC hiện hành sau tự rà và kiểm khả thi một phiên; Claude phản biện kết quả; phạm vi ghi results/T-037/, nối LOG và đúng dòng T037 trong STATE; chưa duyệt tải nguồn mới.” Nguồn là nguyên văn lời giao tại LOG Phiên2, không gộp suy luận hay chấp thuận sửa hợp đồng SMTP vào quyết định này.

Vật liệu báo cáo đồ án: phân biệt nguồn thiết kế/quan sát/runtime/lợi ích; DB logic khác instance; shared metric không nhân bằng chứng; protocol/channel phải giữ đúng nghĩa. Các OPEN, record counts và phản ví dụ hiện tại không phải kết quả hiệu quả RCA.
''')

# Correct the duplicated transcription only by appending; preserve every prior LOG byte.
text=LOG.read_text(encoding='utf-8-sig')
start=text.index('**Nguyên văn lời giao của Minh:**',text.index('## Phiên 2'))
raw=text[start:].split('```text\n',1)[1].split('\n```',1)[0]
extra='\n\nQuyết định cần ghi sổ chính thức thì trình nội dung và phạm vi riêng.\n\n'
assert raw.count(extra)==1
raw=raw.replace(extra,'\n\n',1)
write(BASE/'authorization.txt',raw+'\n')
with LOG.open('a',encoding='utf-8') as f:
 f.write('\n\n### Bản chép chuẩn lời giao — thay bản chép có đoạn lặp, giữ nguyên lịch sử\n\n```text\n'+raw+'\n```\n')

template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(start,end):return template.split(start,1)[1].split(end,1)[0].split('```text\n',1)[1].split('\n```',1)[0]
common=block('## Prompt chung','## Khối công đoạn')
stage=block('### Soát kết quả','### Người làm đáp phản biện')
gate=block('### G3 — Khóa thiết kế trước khi mở test','### G4 — Kết quả')
values=[
 'T-037; D:/RCA-flashticket/tasks/T-037-p5b-flashticket/SPEC.md và LOG.md',
 'soát kết quả', 'P5; chuẩn bị G3', 'Codex người làm, Claude người phản biện chính thức kết quả',
 'AGENTS.md; docs/STATE.md; tasks/T-037-p5b-flashticket/SPEC.md và LOG.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-037/nguon.json và các nguồn/snapshot được liệt kê',
 'Không có REVIEW kết quả T-037; lời giao và lịch sử chuẩn bị tại LOG Phiên1–2; T-036 có tasks/T-036-p5b-hop-dong-chung/REVIEW.md và LOG.md',
 'results/T-037/manifest.json, ban-ghi.json, bao-phu-nguon.md/json, kiem-dung-dan.md, ban-giao.md, hop-dong-runtime.md, counterexample-smtp.json, oracle.json và runs/; pin T-036 runs/kiem-r1-after-002/code/ cùng code-hashes.json, manifest.json và đầu vào SPEC; Windows11/Python3.12; py -3 -X utf8 -B results/T-037/check-counterexample.py <tên run mới> chỉ khi được Minh giao chạy; không chạy checker T036 vào thư mục T036',
 'Chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, kết quả, code hoặc nguồn chung. Minh chuyển prompt thủ công'
]
placeholders=re.findall(r'<[^>]+>',common)
assert len(placeholders)==len(values)
filled=common
for old,new in zip(placeholders,values):filled=filled.replace(old,new,1)
prompt=filled+'\n\n'+stage+'\n\n'+gate+'\n'
write(BASE/'prompt-claude.txt',prompt)
dump(RUN/'prompt-check.json',{'common_fixed_text_preserved':re.sub(r'<[^>]+>','<value>',common)==re.sub('|'.join(re.escape(x) for x in sorted(values,key=len,reverse=True)),'<value>',filled), 'stage_exact':stage in prompt,'gate_exact':gate in prompt,'unfilled_placeholders':re.findall(r'<[^>]+>',filled)})

# Acquire the current STATE sequentially, read fresh under the lock, update one line only.
new_line='| T-037 | P5b: FlashTicket đầy đủ theo thiết kế | P5 (G3) | Codex | Claude (kết quả) | Đang làm có điều kiện; dừng graph do chặn SMTP (16/10/2026). Pin/hash đạt; nguồn/bản ghi/coverage một phần, phản ví dụ ở results/T-037/runs/smtp-002/. Chờ Minh quyết gói sửa hợp đồng chung; chưa hoàn tất/nghiệm thu, không đổi pin. Prompt Claude tại results/T-037/prompt-claude.txt và LOG Phiên2. | `tasks/T-037-p5b-flashticket/` |'
state_status={}
with STATE.open('r+b') as f:
 try:
  msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
  f.seek(0);old=f.read();lines=old.decode('utf-8-sig').splitlines(keepends=True)
  indices=[i for i,line in enumerate(lines) if line.startswith('| T-037 |')];assert len(indices)==1
  i=indices[0];newline='\r\n' if lines[i].endswith('\r\n') else '\n'
  before_line=lines[i];lines[i]=new_line+newline;after=''.join(lines).encode('utf-8')
  if old.startswith(b'\xef\xbb\xbf'):after=b'\xef\xbb\xbf'+after
  (RUN/'state-immediately-before.md').write_bytes(old)
  f.seek(0);f.write(after);f.truncate();f.flush()
  state_status={'updated':True,'only_T037_line_changed':[x for x in old.decode('utf-8-sig').splitlines() if not x.startswith('| T-037 |')]==[x for x in after.decode('utf-8-sig').splitlines() if not x.startswith('| T-037 |')],'old_line':before_line.strip(),'new_line':new_line}
 finally:
  f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
dump(RUN/'state-update.json',state_status)

write(BASE/'runs/commands.md','''# Lệnh trong phiên

Các lượt đọc nguồn dùng Get-Content, rg và metadata Get-Item/Get-ChildItem trong đúng hai repo hiện hành. Đọc AGENTS/STATE/SPEC/LOG trước, rồi DT18/cô/MRP/LESSONS/WHY/DECISIONS/review-prompt/LOG T036 Phiên1; đọc source/code/output trước REVIEW T036. READMEs/diagrams do helper đọc theo source scope ở nguon.json. Không đọc data/locked hay test data.

Lệnh tạo/kiểm artifact (thứ tự):
1. `py -3 -X utf8 -B results/T-037/preflight.py`
2. Ghi oracle.json, nhận xét độc lập và nguyên lời giao trong LOG; hai helper chỉ tạo records-data/coverage-data và records-flow/coverage-flow.
3. Ghi counterexample-smtp.json trước runner; lấy mẫu CPU với Get-Process hai lần cách1giây, không process >0,25CPU-second.
4. `py -3 -X utf8 -B results/T-037/check-counterexample.py smtp-001` — lỗi đo RAM; giữ failure/code/input/oracle.
5. `py -3 -X utf8 -B results/T-037/check-counterexample.py smtp-002` — tái lập chặn2/2, không sửa input.
6. `py -3 -X utf8 -B results/T-037/collect-sources.py`
7. `py -3 -X utf8 -B results/T-037/finalize-blocked.py`
8. `py -3 -X utf8 -B results/T-037/verify-final.py` — kiểm cuối chỉ đọc kết quả/phạm vi, không thực nghiệm mới.

Hash đọc bằng SHA256 streaming1MiB, byte size và manifest; Python -B không tạo bytecode. Snapshot nguồn chỉ là tài liệu thiết kế đã đọc. Không chạy checker T036 (sẽ ghi ngoài phạm vi) hoặc full T037 graph converter sau chặn. Không download/giải nén/EC2/commit/push/chat ngoài.
''')

checks_ok=all(x['pass'] for x in checks)
with LOG.open('a',encoding='utf-8') as f:
 f.write(f'''\n\n### Kết thúc phiên — 16/10/2026 — dừng phần phụ thuộc, chưa hoàn thành T037

1. Đã tự rà nguồn/pin và khảo sát nguồn độc lập; lưu {len(source['sources'])} nguồn/snapshot, {len(units)} đơn vị coverage dự thảo và bản ghi một phần ({counts}). Chặn SMTP được tái lập2/2 ở runs/smtp-002/result.json. Không có graph/phép chiếu toàn phạm vi được dựng, không gọi task đạt. Năm nguồn/diagram/readme được đọc; content DDL/schema/realm dẫn xuất chỉ metadata, source closure chưa hoàn tất.
2. Phạm vi thay đổi: results/T-037/, LOG này chỉ nối thêm, đúng dòng T037 trong STATE. Không sửa SPEC/REVIEW/WHY/DECISIONS/src/T035/T036/platform/task khác. Oracle HTTP/SMTP ban đầu sai được giữ và vô hiệu, lượt đo lỗi được giữ. Bản chép chuẩn lời giao ở trên sửa lỗi chép lặp bằng cách nối thêm. Không tải, mở test/heldout/telemetry, chọn P6/làm T040/EC2, commit/push hoặc tự gửi chat.
3. Kiểm input/snapshot/common code trước và cuối đều khớp; partial-record checks {sum(x['pass'] for x in checks)}/{len(checks)}, không thay kiểm graph. CPU sample không việc nặng khác; memory32.768.000byte và thời gian hai build calls chỉ cho phản ví dụ nhỏ. Full cost dự toán chưa đo còn điều kiện; không dùng sample để nhận khả thi full task khi contract đang chặn. Kiểm diff/phạm vi cuối bằng verify-final.py sau ghi, xem runs/ket-phien-001/final-verification.json.
4. Phần nguồn đã trả lời: B12 giữ DB logic/instance chung; thao tác là tên thiết kế; B13/B14 đòi SMTP và pin hiện hành không nhận transport này. Chưa trả lời lợi ích RCA/RQ3/RQ5, chưa nhận full coverage/model hoặc G3. OPEN cần Minh quyết gói sửa chung/pin cho ba nhánh theo ban-giao.md; queue/scope/runtime names/deployment/telemetry và đầy đủ fixture còn phải xác minh. Không tự mở lại T036 đã đóng, không tự nghiệm thu T037. Đây là phần hỗ trợ mô hình/P9, không là cơ chế đã xác nhận.

**Bước tiếp chính xác:** Minh xem results/T-037/ban-giao.md mục phạm vi sửa và kiem-dung-dan.md. Chờ duyệt gói xử lý hợp đồng/pin chung; không chạy graph từ bản ghi hiện tại. Sau quyền phù hợp, viết oracle đúng đầy đủ trước converter, đọc/ghim nguồn dẫn xuất cần thiết, hoàn tất coverage từng requirement→record→ID/type/address→graph/chiếu/binding/signal và fixture runtime tổng hợp; chạy dưới tên run mới. Không tự đổi SPEC/pin hoặc giảm tiêu chí. Quyết định triển khai có điều kiện cần lưu DECISIONS được trình nguyên ý trong ban-giao.md, chưa ghi do ngoài quyền.

**Lệnh cuối dự kiến/được giao chạy trong phiên:** py -3 -X utf8 -B results/T-037/verify-final.py. Lệnh đó chỉ kiểm artifact/diff/hash/prefix/phạm vi. Đề xuất commit sau khi Minh giải quyết chặn và duyệt: `docs: preserve T-037 design survey and SMTP contract counterexample`; chưa commit/push.

**Prompt Claude — soát kết quả một phần (Minh chuyển thủ công):**\n\n```text\n{prompt}```\n''')

# Store complete changes owned by this turn, using the preflight LOG/STATE as base.
old_log=(BASE/'runs/tu-ra-001/log-before.md').read_text(encoding='utf-8-sig').splitlines(keepends=True)
new_log=LOG.read_text(encoding='utf-8-sig').splitlines(keepends=True)
old_state=(RUN/'state-immediately-before.md').read_text(encoding='utf-8-sig').splitlines(keepends=True)
new_state=STATE.read_text(encoding='utf-8-sig').splitlines(keepends=True)
parts=list(difflib.unified_diff(old_log,new_log,fromfile='before/tasks/T-037-p5b-flashticket/LOG.md',tofile='after/tasks/T-037-p5b-flashticket/LOG.md'))
parts+=list(difflib.unified_diff(old_state,new_state,fromfile='before/docs/STATE.md',tofile='after/docs/STATE.md'))
for p in sorted(BASE.rglob('*')):
 if not p.is_file() or p.name in {'changes.diff','manifest.json','final-verification.json'}:continue
 try:lines=p.read_text(encoding='utf-8-sig').splitlines(keepends=True)
 except UnicodeError:continue
 parts+=list(difflib.unified_diff([],lines,fromfile='/dev/null',tofile=rel(p)))
write(RUN/'changes.diff',''.join(parts))
(BASE/'runs/smtp-002/code-used.py').write_bytes((BASE/'check-counterexample.py').read_bytes())
files=[{'path':rel(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file() and p.name not in {'manifest.json','final-verification.json'}]
manifest={'task':'T-037','state':'PARTIAL_BLOCKED_SMTP_AWAITING_MINH_DECISION','coverage_complete':False,'full_graph_built':False,
 'source_revision':source['revision'],'pin':pre['pin'],'pin_manifest_sha256':pre['manifests'][0]['manifest_sha256'],
 'source_registry':'nguon.json','current_counterexample_run':'runs/smtp-002','failed_run_retained':'runs/smtp-001',
 'oracle_status':'oracle.json initial full-graph oracle invalidated; counterexample-smtp.json is current only for blocker reproduction',
 'counts_partial_records':counts,'coverage_unit_count':len(units),'checks_partial_pass':checks_ok,
 'files':files,'total_output_bytes':sum(x['bytes'] for x in files),'manifest_self_included':False,
 'total_byte_scope':'Every output including all failed/success runs and snapshots except this manifest and final verification report; latter reported separately',
 'tests_or_heldout_opened':False,'downloads_bytes':0,'unpacked_bytes':0,
 'authorization':'authorization.txt','log':'tasks/T-037-p5b-flashticket/LOG.md','state_row':'T-037',
 'prompt':'prompt-claude.txt','validation':'runs/ket-phien-001/final-verification.json'}
dump(BASE/'manifest.json',manifest)
print(json.dumps({'state':manifest['state'],'counts':counts,'coverage_units':len(units),'checks_pass':checks_ok,'failed_checks':[x for x in checks if not x['pass']], 'state_updated':state_status['updated'],'manifest_files':len(files),'output_bytes_excluding_manifest_and_final_report':manifest['total_output_bytes']},ensure_ascii=False))
