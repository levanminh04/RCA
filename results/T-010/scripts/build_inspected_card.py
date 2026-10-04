import collections,json,re
from pathlib import Path
b=Path('results/T-010');r=b/'runs';raw=json.loads((r/'inspect-002/raw-cases.json').read_text());s=json.loads((r/'inspect-005/summary.json').read_text());graph=json.loads((r/'inspect-005/graph-audit.json').read_text());tab=json.loads((r/'inspect-006/tables.json').read_text())
parents=collections.Counter();status=collections.Counter();logs=collections.Counter()
for x in raw:
    parents.update(x['parent']);status.update(x['is_error_values'])
    for l in x['logs']:
        for k in ('lines','context_lines','trace_matches','span_matches','descending_adjacent'):logs[k]+=l[k]
assert sum(x['span_rows'] for x in raw)==12303544
assert parents['parent_required']==parents['parent_unique']+parents['parent_missing']+parents['parent_ambiguous']
assert sum(x['counts']['graphs'] for x in graph)==s['graph_records']==132485
assert sum(x['error_trace_type'].get('normal',0) for x in graph)==109151
assert sum(v for x in graph for k,v in x['error_trace_type'].items() if k!='normal')==23334
assert s['lineage']['graph_trace_in_raw']+s['lineage']['graph_trace_absent_raw']==s['graph_records']
assert s['graph_bad_edges']==s['edge_attr_length_mismatch']==s['label_inconsistent']==0
normal=[x for x in raw if '/normal/' in x['archive']]
normal_table='\n'.join(f"| {x['case_directory']} | {x['span_rows']} | {x['time_min_ms']} | {x['time_max_ms']} |" for x in normal)
case_table='\n'.join(f'| {k} | {v} | {s["raw_case_trace_counts"].get(k)} |' for k,v in sorted(s['abnormal_case_counts'].items()))
old=b/'the-dataset.md';backup=r/'inspect-005/card-before-update.md'
if not backup.exists():backup.write_bytes(old.read_bytes())
card=f'''# DeepTraLog Train Ticket — thẻ đã kiểm F/normal/all-log/graph được duyệt

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: DeepTraLog ICSE 2022, Chenxi Zhang và cộng sự, FudanSELab; Train Ticket v0.2.0, nhánh code có lỗi; SkyWalking, Elasticsearch. [Repository](https://github.com/FudanSELab/DeepTraLog), [trang tác giả](https://fudanselab.github.io/DeepTraLog/), [paper đã lưu](runs/run-001/sources/paper.pdf). Revision, URL, hash và snapshot ở [manifest nguồn](runs/run-001/manifest.json). Repository/trang tác giả đã lưu chưa cho điều khoản license dữ liệu/code rõ; công khai không chứng minh đầy đủ quyền sử dụng. Không gọi thiếu license là dữ liệu bất hợp pháp.

Q-47 cho kiểm số đo DeepTraLog trên EC2 mới. Đã tải 32 file chính thức: 14 ZIP F, 10 ZIP normal, tám phần GraphData, 515.614.981 byte; [download-002](runs/download-002/manifest.json) giữ byte/checksum/revision. Tám phần graph ghép thành ZIP, CRC mọi member được kiểm. Đã đọc toàn raw/normal/graph và ba bảng CSV trong graph. 5 phần `alllog` chỉ metadata, không nằm trong danh sách tải 32 file: không gọi đó là toàn release đã đọc. `alllog` là bản gộp log cùng lineage theo nguồn, không modality/dataset độc lập.

[Raw/CRC](runs/inspect-002/summary.json), [lineage/graph sửa shape](runs/inspect-005/summary.json), [CSV mapping](runs/inspect-006/tables.json). `inspect-002` đọc nhầm edge_index E×2 thành 2×E: số cạnh/bad-index của graph run này bị thay bằng inspect-005; raw/CRC giữ sau kiểm. Hai lượt bổ sung lỗi header/Counter được giữ trong inspect-003/004, không ghi đè. Chạy `inspect_deep.py`, `inspect_lineage.py` và `inspect_graph_tables.py` trong scripts với `--data /home/ubuntu/rca-t003/data/deeptralog --out <run-mới>`; không training/RCA.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | File tải/CRC được, điều khoản permission OPEN. |
| 2. Root/thời điểm | Nhãn trace bất thường có thật; chưa có nhãn root service hoặc injection/onset riêng. |
| 3. Trace cha–con | 12.303.544 dòng span raw, scoped parent ở mục 4. |
| 4. Metric/log | Log thực có ID ghép; resource metric riêng không có trong tree/raw/graph đã kiểm. Latency span không thay resource metric. |
| 5. Root/vị trí | Raw có 35 service, graph có service ID map; không nhãn root nên không suy vị trí root từ bậc event. |
| 6. Loại lỗi | Paper nhóm inter-service/data consistency/multi-threading/monolithic; 70 nhãn instance code trong graph, chưa mapping root×fault. |
| 7. Ngoài root | Không thể phân loại ngoài-root có căn cứ khi nhãn root thiếu; không tạo nhãn từ log ERROR. |
| 8. Normal | 10 ZIP normal có dữ liệu thực; khoảng/thể tích và nguy cơ nhiễm ở mục 5. |
| 9. Độc lập | Nhóm tác giả/faulty branch/stack có nguồn; cần so reuse với RCAEval/Eadro/Nezha tại G1. |

## 3. Nhãn, số ca và khả năng phân xử

Paper công bố 132.485 trace, 23.334 abnormal trace, 7.705.050 log, 73 fault instances/14 fault cases. Graph thực đếm đúng 132.485 trace-ID duy nhất, 109.151 normal và 23.334 abnormal, không ID trùng hoặc nhãn thiếu/xung đột; 70 `error_trace_type` khác normal. Raw có {len(raw)} thư mục storage được inspector đếm, {sum(x['span_rows']>0 for x in raw)} có span; không coi folder, fault branch và trace là cùng đơn vị incident. Root×fault×lần lặp không có nhãn service-ground-truth nên không tạo census giả.

| Nhãn graph instance | Abnormal trace trong graph | Trace-ID raw cùng thư mục |
|---|---|---|
{case_table}

Raw `F12-04` và `back0729` không có abnormal graph tag cùng tên; nhãn xử lý không được suy từ tên. Tất cả 23.334 abnormal graph ID có mặt raw của đúng named case. 104.369/132.485 graph ID có trong toàn raw tải; 28.116 vắng raw. Không gọi lineage normal đầy đủ: release raw có thể subset, graph có thêm lượt, hoặc khác quá trình xuất; nguồn chưa giải thích. [Từng count](runs/inspect-005/summary.json).

Raw graph service dựng từ parent service→child service, bỏ self-edge, tại từng storage case; [toàn bảng cạnh từng ca](runs/inspect-002/raw-cases.json). Service ID map trong id_service.csv có 35 entity khớp tập raw. Graph xử lý là TEG event graph (đồ thị sự kiện), không coi 27.288.193 event node hay bậc event là vị trí root service. Nhãn root service không được thấy trong các file được duyệt nên không có bảng bậc root thật.

## 4. Schema thật và chất lượng nguồn tín hiệu

FACT raw: CSV StartTime/EndTime (epoch ms), URL, SpanType, Service, SpanId, TraceId, Peer, ParentSpan, Component; 87 CSV header có IsError, ba header thiếu IsError. Span type/status riêng từng case ở raw-cases. Tổng IsError: {status['False']} False, {status['True']} True, {status['MISSING']} thiếu trường; thiếu trường không tự gán False. IsError từng span không bằng nhãn trace/ranking root.

Tổng span 12.303.544; sentinel/root theo file: {parents['sentinel_root']}; parent cần resolve {parents['parent_required']}. Khóa `(TraceId,SpanId)` trong storage case: {parents['parent_unique']} tìm một dòng cha, {parents['parent_missing']} thiếu, {parents['parent_ambiguous']} nhiều dòng. Đây là strict-row resolution; span ID trùng giữ riêng trong từng ca, không coi row duplicate là parent mất. Tỷ lệ cộng tử/mẫu, không trung bình tỷ lệ từng ca. File/time bị cắt, instrumentation hoặc dòng export trùng cũng giải thích thiếu/ambiguous.

Log {logs['lines']} dòng trong F/normal; {logs['context_lines']} dòng có SW_CTX. Không cột trace_id riêng; context chứa trace/segment/span. {logs['trace_matches']} dòng ghép trace, {logs['span_matches']} ghép scoped span bằng `segment+'.'+span`; quality riêng từng ca/file và reverse order được giữ. Nhiều file log có thứ tự giảm thời gian; không dùng row order thay clock. Số log thấp hơn paper, vì phạm vi F/normal đọc khác all-log gộp chưa tải; chưa kết luận corpus thiếu log.

Graph: cả tám JSONS đúng sáu trường trace_id/trace_bool/error_trace_type/node_info/edge_index/edge_attr. edge_index **E×2**, {s['graph_total_edges']} cạnh, {s['graph_total_nodes']} event node; 0 endpoint sai/edge-attr length mismatch. trace_bool True→normal (code y=0), False→abnormal; type/label nhất quán với error_trace_type. Ba CSV graph: id_service 35 dòng, id_url+temp 1.513, id_url+type 1.878; first-ID duy nhất, không trường rỗng hoặc width sai. Loader còn đòi embedding_id_url+type.csv, file này không có trong ZIP graph kiểm; chưa chạy loader/baseline, không gọi distribution này chạy được nguyên trạng.

## 5. Bình thường và mốc thời gian

10 ZIP normal chứa 9.999.974 dòng span, 81.037 trace-ID duy nhất. Khoảng min/max là phạm vi xuất file, không duration normal liên tục hay lượng label injection. Có normal graph ID ghép raw normal {s['normal_graph_in_raw_normal']}; abnormal graph không ghép raw normal ({s['abnormal_graph_in_raw_normal']}). Warm-up/khôi phục/đại diện tải vẫn không được tên normal chứng minh.

| Normal storage | Dòng span | Min epoch ms | Max epoch ms |
|---|---|---|---|
{normal_table}

Raw có clock span ms/log text; timezone log không được xác nhận từ file. Graph không có timestamp injection/onset/window, chỉ trace ID. Không suy injection từ phần số trong SkyWalking ID hoặc chuyển graph label thành nhãn thời gian. Không tự nối các phiên normal/fault thành một chuỗi.

## 6. Triệu chứng ngoài root — tiêu chí 7

OPEN do **release được kiểm không có ground truth root service và resource metric riêng**, không do còn chờ quyền đọc. Span latency/log level đã kiểm trong toàn phạm vi; không thể gọi service “ngoài root” có căn cứ. Trace_bool/error_trace_type là nhãn trace, không root; log ERROR có thể symptom chứ không nguyên nhân. Không tạo root/region từ regex hoặc coi nhiều service trong trace là propagation. Cần nguồn nhãn root nếu muốn thực hiện q theo service ngoài root; chưa có bằng chứng để lấp nhãn này trong task.

## 7. Task chấm được

| Task | Nhãn thực và phạm vi |
|---|---|
| Trace anomaly | Có toàn 132.485 label, nhất quán; P/R/F1 theo đơn vị trace có căn cứ, chưa chạy phương pháp. |
| Ranking root | Không root service per instance; error_trace_type không thay root, MRR/Hit@k OPEN. |
| Phát hiện thời gian | Không onset/injection interval thật trong graph/nhãn đã kiểm; không chấm window bằng suy đoán ID. |
| Vùng ảnh hưởng | Không label tập service bị ảnh hưởng, không chấm từ event graph hoặc IsError. |

Loader normal-only training/split theo paper/code là giao thức nguồn, không quyết định G1. Ngân sách label và phương pháp chuyển hệ chưa chọn.

## 8. Rò nhãn và độc lập

Tên F/normal, tên file SUCCESS/ERROR, trace_bool/error_trace_type có thể lộ class; chỉ census/chấm hoặc ngân sách học được duyệt. Adapter không dùng path/name/root-derived SLI; chưa có adapter nên không claim đã an toàn. Graph giữ fault type trong Data; cần loại khỏi input phương pháp. Không chia raw và graph của cùng trace sang hai phía dev/test. Lineage mapping abnormal đã xác minh; normal raw→processed chỉ một phần, không ép được đầy đủ từ số tổng.

Nhóm Fudan/faulty branches/SkyWalking khác nguồn Eadro Chaosblade/Jaeger; Train Ticket là hệ dùng chung. Khác stack/tác giả không chứng minh độc lập mọi trục hoặc không reuse. Chưa quyết dataset/split/holdout.

## 9. Dung lượng và chi phí

32 file tải 515.614.981 byte theo manifest; download-002 giữ thời gian từng file/checksum. Raw/CRC run-002 123,845 giây; audit lineage/graph inspect-005 {s['elapsed_seconds']} giây; bảng CSV inspect-006 chạy streaming. EC2 mới, không instance T-007, timeout mỗi lệnh <1 giờ. Không cài training environment; không RCA. Byte member của ZIP/part và graph-combined ở archive-directory; chi phí RAM đỉnh/adapter/phương pháp chưa đo, không ngoại suy từ parsing.

## 10. OPEN và kết luận phạm vi

Đã kiểm toàn raw/normal/graph trong danh sách Q-47 được tải, tự kiểm graph shape/label/lineage và lưu lỗi. License chưa chứng minh đủ permission; tác giả/nguồn điều khoản cần làm rõ khi dùng ngoài inspection. Nhãn root/injection/region không thấy trong corpus được kiểm; muốn chấm các task đó cần nguồn nhãn thật, không suy từ IsError. 28.116 graph normal ID vắng raw cần giải thích lineage nếu dùng raw vs graph. Alllog chưa đọc theo danh sách tải hiện hành; loader embedding còn thiếu. Những điều này không phủ định trace-label census đã kiểm và không là lý do tự chọn/bỏ dataset thay Minh.
'''
if (r/'inspect-007/summary.json').exists() and (r/'inspect-008/summary.json').exists():
    allog=json.loads((r/'inspect-007/summary.json').read_text());coverage=json.loads((r/'inspect-008/summary.json').read_text())
    assert allog['log_counts']['lines']==7705050 and allog['all_members_crc_ok']
    assert coverage['normal_graph_raw_span_missing']==28116 and coverage['all_balances_ok']
    card=card.replace('5 phần `alllog` chỉ metadata, không nằm trong danh sách tải 32 file: không gọi đó là toàn release đã đọc. `alllog` là bản gộp log cùng lineage theo nguồn, không modality/dataset độc lập.', 'Sau khi thấy thiếu lineage normal/coverage log, thực hiện bước 4 có điều kiện trong SPEC/kế hoạch: tải thêm năm phần all-log 213.216.632 byte, tổng Deep 37 file/728.831.613 byte. Root xác nhận đây là tiếp phạm vi đã trình, không ứng viên/phương pháp mới. [Download thêm](runs/download-003/manifest.json), [all-log CRC/schema/count](runs/inspect-007/summary.json), [coverage từng nhãn](runs/inspect-008/per-label-coverage.json). All-log là bản gộp cùng lineage, không modality/dataset độc lập. Toàn F/normal/all-log/graph của inventory dữ liệu đã đọc; không full-unpack log ra đĩa.')
    card=card.replace('Số log thấp hơn paper, vì phạm vi F/normal đọc khác all-log gộp chưa tải; chưa kết luận corpus thiếu log.', f"All-log stream đếm đúng 7.705.050 dòng paper, cùng SW_CTX; {allog['unique_context_trace_ids']} trace-ID trong log. {allog['graph_ids_covered']}/132.485 graph ID có log: {allog['graph_normal_ids_covered']}/109.151 normal, {allog['graph_abnormal_ids_covered']}/23.334 abnormal. {allog['graph_ids_missing_log']} graph ID không có log ({allog['normal_graph_ids_missing_log']} normal, {allog['abnormal_graph_ids_missing_log']} abnormal). ID có trong log chưa chứng minh span raw/clock sạch hoặc root. All-log có {allog['log_counts']['descending_adjacent']} cặp dòng đảo thời gian; không dùng thứ tự dòng làm timeline.")
    card=card.replace('[Từng count](runs/inspect-005/summary.json).', f"[Từng count](runs/inspect-005/summary.json). Trong 28.116 normal graph ID vắng span raw, {coverage['normal_graph_raw_span_missing_with_alllog']} ID có all-log và {coverage['normal_graph_raw_span_missing_without_alllog']} vắng cả hai. All-log giúp chứng minh có log cho phần lớn normal graph nhưng không khôi phục parent/span vắng; provenance normal vẫn chỉ nhãn trace. [Partition từng label](runs/inspect-008/per-label-coverage.json).")
    card=card.replace('32 file tải 515.614.981 byte theo manifest;', '37 file tải 728.831.613 byte theo hai manifest download-002/003;')
    card=card.replace('chi phí RAM đỉnh/adapter/phương pháp chưa đo, không ngoại suy từ parsing.', f"all-log member 3.085.469.085 byte được stream (run-007 {allog['elapsed_seconds']} giây) và CRC xác nhận, không ghi member ra đĩa. Coverage run-008 {coverage['elapsed_seconds']} giây. Chi phí RAM đỉnh/adapter/phương pháp chưa đo, không ngoại suy từ parsing.")
    card=card.replace('Alllog chưa đọc theo danh sách tải hiện hành; loader embedding còn thiếu.', 'All-log đã kiểm toàn phần có điều kiện; loader embedding còn thiếu.')
if (r/'inspect-008/logical-member-sizes.json').exists():
    size=json.loads((r/'inspect-008/logical-member-sizes.json').read_text())
    card=card.replace('Byte member của ZIP/part và graph-combined ở archive-directory;', f"[Byte member sau giải nén chính xác](runs/inspect-008/logical-member-sizes.json): raw F {size['groups']['fault_raw']['all_member_bytes']} byte, normal {size['groups']['normal']['all_member_bytes']}, graph {size['groups']['graph']['all_member_bytes']}, all-log {size['groups']['alllog']['all_member_bytes']}; tổng {size['total_all_member_bytes']} byte, gồm 1.320 byte ancillary ẩn. Tất cả member đã CRC kiểm; đây là dung lượng logical uncompressed, không phải disk đã ghi khi stream;")
old.write_text(card,encoding='utf-8');assert len(re.findall(r'^## [0-9]+\.',card,flags=re.M))==10
(r/'inspect-005/validation.json').write_text(json.dumps(dict(ok=True,parent_count_balances=True,graph_label_count_balances=True,graph_edge_shape_verified='E_by_2',graph_lineage_balances=True,no_abnormal_normal_id_overlap=True,card_sections=10),indent=2),encoding='utf-8')
print('Deep card/independent count validation PASS')
