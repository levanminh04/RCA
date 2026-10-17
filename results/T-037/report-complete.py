"""Publish verified T037 outputs and concise scientific handoff, preserving prior runs."""
from pathlib import Path
import collections
import hashlib
import json
import shutil

ROOT=Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037';RUN=BASE/'runs/graph-003'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(name,txt):(BASE/name).write_text(txt,encoding='utf-8')
r=load(RUN/'result.json');assert r['all_pass'];st=r['stats'];reg=load(BASE/'runs/smtp-regression-001/result.json');assert reg['all_pass']
cov=load(BASE/'bao-phu-nguon.json');src=load(BASE/'nguon.json');doc=load(BASE/'ban-ghi.json')
out=BASE/'do-thi';out.mkdir(exist_ok=True)
for a,b in [('entity.json','thuc-the.json'),('operation.json','thao-tac.json'),('projection.json','phep-chieu.json'),('entity-only.json','entity-only.json')]:shutil.copyfile(RUN/a,out/b)
dump(out/'inventory.json',dict(inventory=doc['entities'],observed_nodes=[],ranking_candidates=None,meaning='Inventory thiết kế; chưa là tập quan sát hoặc tập ứng viên P6'))
dump(out/'index.json',dict(current_run='runs/graph-003',source_registry='nguon.json',records='ban-ghi.json',operation_address_requirements='dia-chi-tin-hieu.json',source_relation_OPEN='quan-he-nguon-chua-dinh-kieu.json',base_contract='results/T-036/hop-dong.md',approved_addendum='hop-dong-smtp.md',runtime_verified=False))
cov['state']='DESIGN_MODEL_CHECKED_AWAITING_CLAUDE_REVIEW'
cov['graph_check']='runs/graph-003/result.json';cov['requirement_record_graph_matrix']='runs/graph-003/requirement-record-graph-matrix.json'
cov['coverage_meaning']='Every selected source is read/pinned and every source requirement is classified/mapped or OPEN with owner/input. Not proof of complete runtime graph or scientific efficacy.'
cov['counts']=st;dump(BASE/'bao-phu-nguon.json',cov)

write('bao-phu-nguon.md',f'''# Bao phủ nguồn và mô hình thiết kế FlashTicket

**Chờ Claude phản biện kết quả.** Inventory đủ thực thể tìm được trong phạm vi nguồn thiết kế ghim; graph giữ các quan hệ có đủ căn cứ về loại/địa chỉ. Những quan hệ nguồn chưa xác định đủ transport hoặc hành vi được giữ nguyên ở bảng OPEN, không bị xóa khỏi phạm vi nghiên cứu.

Nguồn: 5 tài liệu B11-C/B12/B13/B14/B16, 10 sơ đồ trực tiếp, 4 README baseline, 10 định nghĩa SQL/Mongo/realm và 5 nguồn quản trị/phạm vi. Tổng {st['source_count']} nguồn, 4.585 dòng theo runs/assemble-002/coverage-resolution.json. Đây là phạm vi **thiết kế đích được liệt kê**, không là toàn bộ cây platform hay runtime. Revision/hash/dirty state và snapshot ở nguon.json; 10 baseline definitions đã đọc nội dung và đối chiếu, không còn chỉ metadata. Tests/runners/legacy/archive/remote tham khảo không làm nguồn sinh mô hình; lý do/ảnh hưởng ở registry.

652 đơn vị nguồn tại bao-phu-nguon.json#/units. B13/B14/B16 có ledger 562 dòng giữ nguyên văn; 239 đoạn trích được kiểm lại khớp snapshot tại runs/assemble-002/semantic-source-audit.json. B12 và năm ERD có đơn vị theo bảng/đoạn; 47 bảng SQL đối chiếu tên với dictionary đủ 12/15/13/7, bốn collection User giữ owner/source version. Số dòng/đơn vị chỉ là điều hướng; bằng chứng nghĩa nằm trong từng đoạn, bản ghi và chuỗi truy vết.

| Nhóm | Kết quả mô hình / nguồn | Điều kiện và phần mở |
|---|---|---|
| HTTP/RPC/gateway | Buyer/API hỗ trợ/seat-map/check-in, freeze/probe/financial summary theo B13. Không tìm thấy hợp đồng RPC riêng để tự thêm | B13 User §9 có path nhóm chưa method; không tự tách handler runtime. Prefix/method rút gọn cần P9 kiểm |
| DB/cache/shared instance | Sáu service/identity→DB logic; Booking→cache; năm DB trên một PG instance qua binding; Mongo User riêng theo B12 | DB/instance/host mục tiêu, chưa là địa chỉ triển khai thật. Cache technology/operation OPEN |
| Messaging/fan-out | 9 message type, 11 tuyến logical gồm cancellation ba consumer; publish→broker và broker→consume giữ riêng | Exchange flash-ticket.v1/routing có nguồn; queue/scope null, không bịa tên queue hoặc đếm bản tin từ tài liệu |
| Outbox/inbox/retry | DB đúng owner, relay, confirm rồi published_at; commit rồi ACK; hash/dedup/attempt giữ trong context/coverage | Bảng có mặt không chứng minh worker chạy đúng; retry không tạo operation/cạnh logic mới |
| Callback/query | Payment verify/create/query/refund và tra cứu hoàn; callback có quan hệ thiết kế provider→Payment | Fixture giữ trace callback mới; correlation không tạo parent hay message edge |
| Scheduler | Expiry/refund/relay/delivery/role-grant/projection có owner và nguồn | Root không cần caller. Frequency/lease/tên span runtime còn cần triển khai |
| Saga/bù trừ/fence | Chỉ một Saga Payment; kết quả phát vé/quyết định Booking/hoàn theo B13/B14 | Không đảo cạnh bù trừ, không Ticket→Booking giả. Timeout chưa là terminal FAILED; source state không bị graph thay thế |
| Delivery/check-in | SMTP được giữ đúng channel, kiểu gọi chưa phân kiểu; QR/read/claim/audit/replay giữ nguồn | Email timeout có thể gửi trùng; không thêm vé/refund. Không runtime claim; không raw QR/JWT |
| Role-grant/projection | User API + Admin API request/query, worker nguồn application/version; Mongo local | Không Keycloak→User message giả hoặc Saga thứ hai; quyền/client realm runtime OPEN |
| Hỗ trợ/vận hành | Gateway/identity/config-discovery/chatbot/kho quan sát/RCA/Gemini/host có inventory; data dependencies đọc kho giữ riêng | Arrow kiến trúc chưa đủ caller/transport được giữ ở quan-he-nguon-chua-dinh-kieu.json; không lấy local JWT verify thành HTTP request mỗi lần |

Mô hình đã kiểm: {st['inventory_nodes']} thực thể, {st['operations']} tên thao tác thiết kế, {st['source_relations']} bản ghi quan hệ → {st['entity_edges']} cạnh thực thể; {st['operation_edges']} cạnh thao tác, {st['projection_edges']} cạnh chiếu; {st['bindings']} binding và {st['signals']} địa chỉ/schema tín hiệu, trong đó {st['shared_signals']} dùng chung. Con trỏ: runs/graph-003/result.json#/stats. Không có observed nodes hoặc tập ứng viên P6 được suy từ inventory. Các nhãn B16 và endpoint có thể mô tả cùng thực thi; không cộng số tên thành số request hoặc độ phân giải runtime.

DB instance có thể không có dependency edge nhưng vẫn nằm trong inventory/binding/signal. P6 cần đề xuất phép dùng binding riêng nếu tính ảnh hưởng tài nguyên chung. Lớp operation không thay cây/thời gian span; phần entity-only là hợp lệ, không tạo operation giả để ép phép chiếu bằng graph đầy đủ.

Các OPEN còn lại được định danh tại bao-phu-nguon.json#/open_items: queue/scope, runtime operation mapping, deployment/resource, config/identity protocol, pipeline/export, quyền/UI/retention và đánh giá RCA. Mỗi mục có owner/input/hệ quả. Không còn chặn hỗ trợ SMTP trong phạm vi đã kiểm; chưa có quyền coi OPEN là quyết định đã chốt.
''')

write('kiem-dung-dan.md',f'''# Tự kiểm T-037 — kết quả hiện hành

**Hoàn tất phần mô hình thiết kế có điều kiện và bàn giao để Claude phản biện.** Minh chưa nghiệm thu task. Không xác nhận runtime FlashTicket, lợi ích RCA hoặc đóng RQ3/RQ5/G3.

## Đầu vào và pin

Trước sử dụng, kiểm manifest T036/T037 và nguồn/mã tại runs/tiep-smtp-001/preflight.json: 287 kiểm đều khớp. T036 manifest/snapshot cũ giữ nguyên. Mã hiện hành chỉ thêm smtp vào hai guard; T037 dùng pin nền + bổ sung đã được Minh duyệt, ghi rõ tại hop-dong-smtp.md và snapshot code của graph-003. T038/T039 giữ SPEC/pin; phiên này không ghi code/kết quả của hai nhánh.

Oracle nguồn ban đầu, thiếu sót, phản ví dụ và các run lỗi được giữ; không dùng việc T036 đã đóng để bỏ nhu cầu SMTP. Bổ sung SMTP có oracle literal fixtures-smtp.json trước checker/mã, source requirement B13 L199/B14 L82/B14-03 L9–12. Full graph dùng oracle-v2 trước converter; oracle-v3 chỉ sửa phía missing operation mapping của fixture broker→consumer thành target trước lượt kiểm mới. Tên runtime vẫn null.

## Kiểm đã chạy và ý nghĩa

| Phép kiểm | Kết quả / file | Điều chứng minh |
|---|---|---|
| SMTP mới/âm/chiếu/không mutation/typed giới hạn transport | {reg['passed']}/{reg['passed']}, runs/smtp-regression-001/result.json#/checks | Giữ smtp qua hai mức/chiếu; sai type/channel bị từ chối; endpoints/type agreement không xác nhận protocol |
| Toàn checker T036 cũ, redirect output vào T037 | 221/221; 312 graph,156 cặp chiếu; #/original_regression | Logic kiểm cũ không đổi; mọi221 check records và 10 artifact cũ so nội dung giữ nguyên. Adapter chỉ ROOT/output/nhãn lệnh, có diff |
| Bản ghi→ID/type/address→graph/binding/signal; oracle literal và hàm độc lập | {r['passed']}/{r['passed']}, runs/graph-003/result.json | Chính xác từng record ID/provenance/context/endpoint/type/address và phần phép chiếu được hứa, không chỉ tổng số |
| Từng requirement→record→graph index/binding/signal | runs/graph-003/requirement-record-graph-matrix.json | References tồn tại; nguồn semantic/OPEN vẫn phải được xem, crossref PASS không tự chứng minh khoa học |
| Quote/schema đối chiếu nguồn | 239 đoạn khớp;47 bảng SQL, runs/assemble-002/semantic-source-audit.json | Nội dung nguồn nguyên văn và owner/dictionary không lệch; không thay unit/integration runtime test |
| Fixture ranh giới runtime tổng hợp | graph-003/fixture-* | Hai queue cùng consumer giữ2địa chỉ; shared PG một metric; thiếu mapping/address loại rõ; unknown không typed; callback2root/scheduler không caller; correlation không nối message; identity xác minh cho fan-out3; retry giữ operation và witness attempts |
| Xác định/không nhãn/không sửa input | graph-003/result.json#/checks | Reorder seed0/1/2 giữ output; label field bị API từ chối; graph tĩnh/trace tách riêng |

## Tự phát hiện lỗi và lịch sử

- oracle.json cũ xếp Ticket→SMTP trong HTTP: sai, đã vô hiệu, chưa dùng converter ở thời điểm phát hiện. Không sửa graph cho khớp đáp án sai.
- smtp-001 lỗi ctypes khi đo RAM; smtp-002 tái lập thiếu channel cũ. Cả hai giữ đủ input/oracle/failure/code.
- fixtures-runtime.json v1 đặt sender fan-out Payment (có một cùng owner) và callback correlation chưa đồng nhất. Trước converter đã giữ v1 và viết fixtures-runtime-v2 đúng Event→3consumer, callback cùng correlation nhưng trace khác.
- graph-001 có một lỗi harness: các data relation ngoài miền messaging bị loại đúng, nhưng kiểm đòi mọi exclusion là thiếu địa chỉ. Sửa kiểm chỉ xét messaging, giữ run lỗi/code/input. graph-002 đạt, graph-003 dùng oracle-v3 lý do mapping phía target, không đổi graph/fixture để chạy theo số.
- Locator cache trong partial infra trước ghi L52; đọc lại source đúng BKG→CACHE L47. Bản tích hợp sửa locator, bản cũ giữ trong checkpoint. Lệnh đọc sai cwd/wildcard và lệnh quá dài không tạo file đã ghi LOG; nguồn đúng đọc lại.

Không có finding của reviewer kết quả được tự áp dụng trong lượt này. Helper chỉ hỗ trợ người làm, không là reviewer. Tự rà không thay Claude kiểm độc lập.

## Chi phí và giới hạn

SMTP+checker cũ: tổng {reg['seconds']:.3f}s; child T036 {reg['original_regression']['seconds']:.3f}s, peak working set {reg['original_regression']['peak_working_set_bytes']} byte. Lượt graph hiện hành {r['seconds']:.3f}s, peak {r['peak_working_set_bytes']} byte (runs/graph-003/result.json). Đây là chi phí máy của input hiện tại, không ngoại suy giờ đọc nguồn. Trước lượt đo không process vượt0,35CPU-second trong mẫu1giây; helpers đã ngừng build/đo và chỉ thu nguồn nhẹ. Không dừng process khác.

Dự toán giờ công còn lại 3–5 giờ ở checkpoint là chưa đo; wall-clock qua ngắt usage/chờ Minh không là giờ công liên tục. Tổng dung lượng thực cho **mọi** lượt gồm lỗi/snapshot/bản trước/script/diff nằm trong manifest.json; tải/giải nén mới0. Không EC2/GPU hoặc lượt >1giờ. Không giảm coverage/tiêu chí để tiết kiệm thời gian.

Giới hạn nguồn: graph các quan hệ có đủ type/address, các arrow support còn chưa phân kiểu lưu nguyên văn/owner/input; topology là thiết kế. Queue/scope/runtime names/telemetry chưa xác minh. Phép tính P5 dùng cạnh để gộp, chiếu, giữ địa chỉ và đối chiếu cấu trúc; không phát hiện/ranking. Shared resource binding chưa là cạnh computational của T035. Không mở test/heldout/trace/log/metric thô hoặc chọn P6.
''')

write('hop-dong-runtime.md','''# Hợp đồng đối chiếu runtime FlashTicket — đầu vào cho P9

Đây là **yêu cầu địa chỉ và phép kiểm** rút từ nguồn thiết kế, chưa là telemetry hoặc nghiệm thu instrumentation. Tên thao tác trong ban-ghi.json là nhãn thiết kế; runtime_name=null. Bảng chi tiết từng65thao tác/signalID/owner/nơi ghi/keys ở dia-chi-tin-hieu.json#/operations. Không dùng tên thiết kế tự điền operationName/span.name.

| Nhóm / nguồn | Trường bắt buộc để chuẩn hóa | Nơi ghi / owner | Phép kiểm trước đối chiếu thật |
|---|---|---|---|
| Identity chung — B16 §4 | environment, serviceName/service.name mapping, serviceVersion/build, instanceId, hostId đã xác minh, timestamp UTC/observed time | ứng dụng+deployment/P9b | Cùng service ở3tínhiệu có alias rõ; host logic khác host runtime |
| HTTP/API — B13/B16 | kind, method/route, peer entity/type, trace/span/parent/request IDs; code/outcome/duration monotonic | gateway/resource server/client instrumentation | Probe freeze/issuance/financial summary và lỗi timeout; không lộ internal route hoặc credential |
| DB/cache — B12/B16 | db.entity/type, DB logic/schema, instance/resource ID, host/time scope | ứng dụng/deployment/exporter | Giữ5DBlogic chungPG, UserMongo riêng; đối chiếu client span→DBlogic→instance→host, không suy từ tên |
| Message — B13 §5/B16 §3 | broker/scope(vhost)/exchange/routing/queue, producer/consumer role; messageId/identity namespace, attempt, correlation/causation, verified creation link khi có | outbox/relay/inbox/broker config | Publish confirm rồi published_at, consumer commit rồi ACK; fan-out nhiều queue; duplicate/collision/batch/retry. Cùng correlation không đủ nối |
| Queue/shared metric — B16 §5/§7 | broker+scope+queue hoặc resource/instance/host ID; metric name/unit/labels hữu hạn/sampling interval | exporter+P9b | Hai queue cùng consumer vẫn2địa chỉ. MộtPGresource metric dùng chung, operation=null; không sao thành evidence độc lập mỗi operation |
| Callback/query — B13 §5.3/B16 §3 | attempt/charge được verify, request/trace mới, provider outcome/query/deadline | Payment/provider adapter | Callback trace mới không ghép parent từ correlation; timeout UNKNOWN/query cùng ID; không claim nội bộ VNPay |
| Scheduler/relay — B14/B16 | job/item/attempt/lease, trace mới, correlation từ bản ghi bền, duration/outcome | service owner | Restart/retry cùng job; batch mỗi item đúng correlation; không caller giả |
| Saga/bù trừ/fence — B13/B14 | saga/order/command/message/charge IDs, stateBefore/After/reason, input hash/fence decision, outbox/inbox | Payment/Booking/Ticket | Timeout≠FAILED; failed terminal chặn phát muộn; bù trừ giữ đúng chiều thiết kế, kiểm cả thành công/lặp |
| SMTP — B13 §6/B14 §6 | transport SMTP, delivery/job/attempt, new trace/outcome/duration; provider response nếu có | Ticket/SMTP adapter | Gửi ngoài DB TX; timeout có thể đã gửi; retry không tạo vé/refund; static channel smtp không xác minh span kind runtime |
| Delivery/check-in/QR — B13 §6 | receipt/replay_of, actor đúng quyền, owner/window/state/outcome, delivery input hash | Ticket | Một success/vé, mỗi receipt/replay có audit; email lỗi không VOID/refund; không raw QR/JWT |
| Role-grant/projection — B13 §9 | operationId/subject/request/result/query/retry, sourceApplicationId/sourceVersion | User/Keycloak | ACTIVE chỉ sau role confirm; retry/rebuild projection từ nguồn; realm fixture không chứng minh quyền Admin API |
| Pipeline — B16 §2/§6/§7 | receiver/exporter endpoint/protocol/config version, dropped/export failures, clock offsets, sampling/retention | vận hành/P9a/P9b | Một đường xuất mỗi tín hiệu, kiểm allow/deny RCA API backend; collector không khôi phục dữ liệu chưa ghi |

Address hiện tại là namespace/schema thiết kế, chưa phải địa chỉ truy vấn runtime. Queue/scope hoặc endpoint chưa biết phải null/OPEN trong adapter mapping; không dùng placeholder symbolic như queue thật. Log dùng trace/span khi hợp lệ, thiếu thì entity+time; operation chỉ gắn khi mapping rõ. Label không chứa orderId/traceId/messageId/email/URL cóID.

Ví dụ dưới **tổng hợp** để minh họa biên, không là schema OTel đã ban hành:

```json
{"serviceName":"payment-service","operation":"verifyNotification(rawRequest)","runtime_name":null,"traceId":"synthetic-callback-trace","parentSpanId":null,"correlationId":"synthetic-order","outcome":"UNKNOWN"}
```

Request trước đó có traceId khác, cùng correlationId. Không thêm edge cha–con hoặc message từ ví dụ này. Khi đối chiếu thật, trace/span IDs phải đúng định dạng nguồn và alias/runtime operationName phải được P9 xác minh; ví dụ không dùng làm log B16 hợp lệ để thu dataset.

Fixture đã chạy: fixtures-runtime-v2.json và runs/graph-003/fixture-*; SMTP fixture/typed protocol caveat tại runs/smtp-regression-001/. Chúng là phép kiểm hợp đồng tổng hợp, không chứng minh telemetry FT đủ.

Manifest thực nghiệm sau phải ghim build/image/config, workload/nhánh, khoảng thu, seed, sampling/drop/retention, clock offset và export hashes. Nhãn lỗi/mốc tiêm nằm riêng cho chấm; không đưa vào graph builder. P9b nhận graph trace riêng, không thêm cạnh tĩnh vào trace để tăng khớp. P6/P10 cần SPEC và quyền riêng cho lựa chọn/đánh giá/mở test.
''')

write('ban-giao.md',f'''# Bàn giao T-037 — mô hình thiết kế và hợp đồng quan sát

**Chờ Claude phản biện kết quả; Minh quyết nghiệm thu.** Phần hỗ trợ SMTP đã được sửa/kiểm theo lời giao. Không đổi pin/SPEC/đầu ra T-038/T-039 hoặc snapshot/manifest T036; không đóng task/G3.

## Kết quả dùng để kiểm tiếp

- nguon.json:34nguồn local đã đọc/ghim, revision/hash/dirty/snapshot/phạm vi loại trừ. Giữ lịch sử nguồn trước đó trong runs/.
- ban-ghi.json và do-thi/:32thực thể,65tên thao tác,115bản ghi quan hệ; graph72cạnh thực thể/55cạnh thao tác/17cạnh chiếu;14binding,153địa chỉ/schema tín hiệu. Số tại runs/graph-003/result.json#/stats. Inventory không là observed nodes/tập ứng viên P6; tên thiết kế có thể là nhiều nhãn của cùng thao tác runtime.
- bao-phu-nguon.json:652đơnvị; raw source quote/ledger, classification, owner/input và references. Chuỗi từng unit→record→graph index/binding/signal trong runs/graph-003/requirement-record-graph-matrix.json. quan-he-nguon-chua-dinh-kieu.json giữ các arrow chưa đủ protocol/call semantics, không dùng chúng làm cạnh runtime.
- hop-dong-smtp.md: pin nền T036 + bổ sung đã duyệt; graph-003/code/ là snapshot actual. typed/endpoints comparison không xác minh transport. Nguồn SMTP không chứng minh span CLIENT/SERVER nên FT giữ gọi-chưa-phân-kiểu.
- dia-chi-tin-hieu.json và hop-dong-runtime.md: từng operation/schema keys/nơi ghi/owner/phép kiểm cho P9.
- kiem-dung-dan.md, manifest.json và runs/: oracle trước converter, kiểm từng bản ghi/chiếu/signal/binding, fixture boundaries, môi trường/thời gian/RAM/mọi lượt lỗi.

## Câu hỏi nguồn đã trả lời tới đâu

**FACT từ nguồn và phép kiểm:** có thể giữ owner/datastore, mộtPGinstance chung, địa chỉ message còn thiếu đúng trường, thao tác có tên thiết kế và SMTP trong graph tĩnh với bổ sung được duyệt. Quan hệ async có3chặng giữ riêng; operation thiếu được báo entity-only. Cạnh được dùng tính gộp/projection/đối chiếu cấu trúc, chưa dùng anomaly/ranking.

**Suy luận có điều kiện:** inventory đủ ở phạm vi selected design sources; source graph giữ các quan hệ đủ type/address. Không suy mọi arrow kiến trúc là endpoint trực tiếp. B11-C §1 giao endpoint/sequence cho B13/B14, vì vậy không tạo Ticket→Booking trực tiếp từ diagram. B14 Gateway là payment provider theo ngữ cảnh, khác API Gateway. Source-gap OPEN không là lỗi dataset/cơ chế RCA.

**Chưa phân xử:** process/operationName/queue/scope/host/endpoint thật, đủ telemetry/nhánh chạy, hiệu quả RCA. Lý do: task được giao nguồn thiết kế, không có quyền/đầu vào runtime. Cần P9 export/config/build và SPEC đối chiếu sau; không thể chứng minh bằng collector hoặc fixture tổng hợp. RQ3/RQ5/G3 vẫn mở; T040 tổng hợp và P6 chọn thiết kế chưa được làm.

## Nơi nhận và bằng chứng thiếu

| Nơi nhận | Đầu vào cụ thể và quyết định phụ thuộc |
|---|---|
| Claude/Minh | Soát nguồn gốc/graph/coverage/kiểm, đọc source trước lịch sử. Xác định mô hình thiết kế có điều kiện có đạt SPEC; chưa là nghiệm thu runtime |
| T040 | Pin nền+delta SMTP/hash code actual cùng schema/namespace. T038/T039 giữ pin gốc; không tự chuyển. Kiểm khả năng ghép theo delta/hồi quy khi được giao tổng hợp, chưa nhận ba nhánh đều đủ |
| P6 | Node/type/cạnh/operation/context/provenance, entity-only, shared-resource bindings và signal namespace. Nếu dùng tài nguyên chung phải nêu phép tính dùng binding; T035 chưa so DB→instance. Cây/timing span phải nhận riêng; không suy từ graph gộp |
| P9a/nhóm hệ thống | Mỗi operation tại dia-chi-tin-hieu.json có writer/owner/keys/test. Cần broker config/vhost/queue, DBlogic→instance→host, runtime names/alias, SMTP adapter, logs3tínhiệu và sampling/drop/clock/retention; kiểm thật theo từng biên |
| P9b | Graph/trace tách, manifest build/config/time, aliases có nguồn, queue metric đúng scope, label riêng. Không sửa trace từ nguồn static, không nối bằng correlation |
| P10 | Workload/nhánh/tiêm lỗi/nhãn giao thức riêng và quyền đánh giá; chưa được mở test hoặc dùng số cấu trúc làm bằng chứng lợi ích |

Các7nhóm OPEN có owner/input/hệ quả ở bao-phu-nguon.json#/open_items. Không có chặn cài đặt SMTP còn lại theo bộ kiểm hiện tại; source gaps vẫn giữ OPEN. Hai agent đồng ý không thay bằng chứng khoa học.

## Quyết định cần ghi sổ chính thức — trình riêng, chưa ghi

Phạm vi cần duyệt riêng: nối docs/DECISIONS.md và docs/WHY.md. Nội dung quyết định nguyên tử đề nghị: “Minh giao sửa hỗ trợ SMTP và kiểm lại; sau khi kiểm đạt tiếp tục T-037; giữ nguyên T-038/T-039 và không tự đổi pin hai nhánh.” Nguồn: nguyên văn LOG T037 Phiên3. Không gộp nghiệm thu hoặc lựa chọn P6 vào quyết định này.

WHY đề nghị ghi: bổ sung channel smtp cho quan hệ gọi để giữ đúng B13/B14; phương án ép http/rpc/internal làm đổi nghĩa, trường transport mới rộng hơn delta tối thiểu; điều kiện thất bại/protocol comparison caveat và kết quả kiểm dẫn file. Đây là lý do kỹ thuật cùng WHY52/53, chưa là bằng chứng lợi ích RCA. Không tự sửa hai sổ trong lượt này.

Nội dung đưa vào báo cáo đồ án: ranh giới thiết kế/quan sát/lợi ích, DBlogic/instance/host dùng chung, message/correlation/trace khác nhau, protocol chưa biết không tự điền, nguồn+oracle/phép chiếu có kiểm và các OPEN ảnh hưởng tích hợp. Không biến inventory/fixture thành runtime measurement.
''')
dump(BASE/'runs/tiep-smtp-001/report-summary.json',dict(current_run='runs/graph-003',checks=r['passed'],smtp_checks=reg['passed'],prior_checks=reg['original_regression']['passed'],stats=st,open_items=len(cov['open_items']),status='awaiting_review_not_acceptance'))
print(json.dumps(load(BASE/'runs/tiep-smtp-001/report-summary.json'),ensure_ascii=False))
