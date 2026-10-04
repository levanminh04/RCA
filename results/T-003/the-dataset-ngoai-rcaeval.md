# Tổng hợp thẻ dataset ngoài RCAEval — T-003

Cập nhật 03/10/2026 theo Q-47/Q-50. Codex là người làm; Claude phản biện gộp. Đã kiểm số đo Nezha/Eadro/DeepTraLog và bốn ZIP LEMMA IT được duyệt. T-012 đã kiểm ba archive nhỏ; Bank chỉ metadata/nhãn bảo toàn tới G3. OT bỏ khỏi phạm vi mới. Không score, chọn dataset G1 hoặc chia dev/test.

## 1. Danh tính, nguồn và phạm vi đã kiểm

| Nhánh | Phạm vi file thực | Giới hạn suy rộng |
|---|---|---|
| [Nezha OB/TT](../T-008/the-dataset.md) | Toàn 566 OB/599 TT CSV tải theo inventory duyệt, bốn ngày construct/rca | Release/artifact khác chưa kiểm |
| [Eadro SN/TT](../T-009/the-dataset.md) | Toàn hai ZIP và mọi nested; 7 SN/12 TT phiên raw duy nhất | 11/21 bản biểu diễn không là phiên độc lập |
| [DeepTraLog TT](../T-010/the-dataset.md) | Toàn 14 F/10 normal/8 graph/5 all-log: 37 file tải | Đọc toàn inventory không nghĩa đủ span raw cho mọi graph ID |
| [LEMMA PR/Cloud](../T-011/the-dataset.md) | Toàn member bốn ZIP Preprocessed PR20211203/Cloud20240124: 2.431 file, 64.107.208 CSV rows, 42 NPY | Original/ngày khác chỉ metadata; hai ngày mẫu không là toàn release |
| [T-012](../T-012/the-dataset.md) | 14 thẻ biến thể, 6 truy vấn/11 hồ sơ; nguồn ghim và ba archive bổ sung | Ba archive AnoMod/TRCA/FSE full kiểm; Bank chỉ metadata/nhãn; các profile khác nguồn-only |

Hash/revision/byte ở manifest nhánh; giữ mọi lượt lỗi/interrupt. OpenRCA Bank và AIOps Bank cùng lineage bảo toàn Q-49/WHY-13, chỉ metadata/schema/nhãn riêng đúng quyền tới G3. Không raw/file dự đoán Bank. Bảo toàn có điều kiện chưa chốt tập thí nghiệm hoặc đủ độc lập.

## 2. Chín tiêu chí MRP §4

[Bảng đối chiếu](bang-tieu-chi.md) giữ đủ chín tiêu chí cho mọi biến thể. Public/download khác permission; injection khác onset; trace call graph khác TEG/sơ đồ kiến trúc. Chi phí không thành điểm phân xử. RCAEval dẫn [T-002](../T-002/the-rcaeval.md), không sửa hoặc tự giải REVIEW của T-002. Sock Shop thuộc T-002/P2; không tự thêm raw vào gói. G1 vẫn phải trả lời vì sao dùng/không dùng Sock Shop và LEMMA theo MRP.

## 3. Nhãn, số ca và vị trí

| Biến thể | Đơn vị/số đếm | Giới hạn vị trí/coverage |
|---|---|---|
| Nezha OB | 56 record tiêm,10 root,33 ô | Minute-file quanh injection±60s, hai clock; không onset |
| Nezha TT | 45 record,10 root,23 ô | Clock text/epoch lệch; root vắng không gọi cô lập |
| Eadro SN | 36 record,12 root,36 ô; mỗi ô1 lần | Paper72; nested trùng hash không tạo lần lặp; nginx-thrift alias CANDIDATE |
| Eadro TT | 81 record,27 root,81 ô; mỗi ô1 lần | Paper162; graph whole-file không là graph interval tiêm |
| Deep | 132.485 trace labels:109.151 normal/23.334 abnormal;70 error_trace_type | Không root service GT; fault instance không incident có root/time |
| LEMMA mẫu | Hai ngày Preprocessed | PR benchmark MongoDB-v1 khác external NFS cause; Cloud root instance trực tiếp |
| T-012 | FSE:10folder/2invalid;8không invalid/11roots/8fault codes; AnoMod13captures/hệ; Bank136labels/14roots/8reasons | FSE reduced không toàn bài; AnoMod source-target không runtime gold; TRCA raw identicalNezha |

Nguồn: [Nezha census](../T-008/runs/run-001/summary.json), [Eadro census](../T-009/runs/run-001/summary.json), [Deep lineage](../T-010/runs/inspect-005/summary.json), [LEMMA mẫu](../T-011/kiem-file.md). Chênh số có thể do revision/scope/export/đơn vị; chưa chọn giải thích khi chưa phân xử.

## 4. Schema và chất lượng ba nguồn

Nezha parent scoped (TraceID,SpanID), sentinel/unique/missing/ambiguous riêng, log ghép scoped file. [SQL độc lập](../T-008/runs/independent-check-001/result.json) kiểm12 file; census toàn file ở file-audit. [Duration unit](../T-008/runs/units-001/result.json) so End−Start; không chữa trace bằng lỗi metric clock.

Eadro tách strict-row parent khỏi identity sau gộp dòng **giống hệt nội dung/service**; TT identity conflict vẫn giữ. Log TT payload ghép ID được; SN không thấy cấu trúc tương ứng trong phần đọc, không suy mọi log thiếu ID. [Toàn/nested](../T-009/runs/inspect-004/summary.json).

Deep12.303.544 span raw; parent theo storage case20 thiếu/36.980 nhiều dòng. Graph E×2 được sửa ở inspect-005, không dùng số cạnh sai inspect-002. All-log7.705.050 dòng;130.920/132.485 graph ID có log. **28.116 normal graph ID vắng span raw đều có all-log**, nhưng log không khôi phục parent/span;1.565 graph ID không có log. [Coverage](../T-010/runs/inspect-008/per-label-coverage.json). TEG không thay service graph; resource metric riêng không thấy trong distribution kiểm.

LEMMA static NPY reader không thực thi payload. [KPI độc lập](../T-011/runs/validate-001/validation.json): Cloud14/14 Sequence case khớp; PR46/46 không nối đủ hoặc khác giá trị. [Linkage](../T-011/runs/validate-003/validation.json) giữ metric/log CSV/log-feature riêng. Không span/parent table trong mẫu, không suy Original thiếu trace.

## 5. Bình thường và thời gian

Nezha construct metric có bản trùng fault. [Strict bounds](../T-008/runs/symptoms-003/result.json) không đủ ≥2 reference+≥2 control, calibration0; symptoms-001 invalid/002 limited giữ, không dùng kết luận. Trace normal chỉ cửa sổ ngắn/ngày, span tương quan.

Eadro normal thực đã đọc, nhưng warm-up/load/recovery chưa được tên no-fault chứng minh; clock trace/log/metric còn lệch. Deep normal graph↔raw thiếu một phần lineage. LEMMA PR thiếu timeline normal/injection đáng tin; Cloud24h trước bug theo PPTX đã có502 trước lỗi, chỉ là reference timeline, không healthy GT. JSON Cloud lệch6h so PPTX UTCZ. Không tự dịch clock/chữa nhãn/nối phiên. Injection, narrative failure time, onset và recovery khác nhau.

## 6. Mô tả ngoài root — tiêu chí7

| Nhánh | Phép kiểm đã làm | Giới hạn |
|---|---|---|
| Nezha | [Duration µs](../T-008/runs/trace-symptoms-002/result.json), pod×operation, chronological reference/control, ba q | Tail n thấp/tương quan; clock/window chưa interval lỗi thật; resource normal không đủ |
| Eadro | [Metric](../T-009/runs/inspect-004/symptom-metrics.json), service×kênh, no-fault reference/control riêng, ba q | Alias/zero-band/control/load cần đọc cùng số |
| Deep | Toàn span/log/labels inventory tải | Thiếu root GT nên ngoài-root OPEN; không tạo root từ ERROR |
| LEMMA Cloud | [Bands](../T-011/cloud-descriptive-bands.csv),12h reference/12h control/24h sau bug | Timeline không healthy; log11 mẫu/nửa; PCA fault denominator0 |
| LEMMA PR | Chất lượng toàn mẫu | Normal/timeline/KPI provenance thiếu; không chọn phần đầu tùy ý |
| T-012 | FSE metric/duration3q; AnoMod duration3q theo source-target; TRCA dùng lại kiểm Nezha | Không causal/region gold; Bank tiêu chí7 OPEN tớiG3 |

q=.95/.99/.995; root gắn sau đo, giữ missing/zero-band/tử mẫu/ca ô kênh. Không OR/regex thành nhãn vùng/epsilon. Workload, mix operations, recovery, clock/exporter có thể giải thích đồng thời vượt band. Không chứng minh propagation nhân quả hoặc giá trị đồ thị.

## 7. Task chấm được

[Ma trận task](task-cham-duoc.md) ghi nhãn/unit/phạm vi/limit. Nezha/Eadro ranking service có điều kiện clock/mapping/protocol; Deep nhãn trace thật nhưng thiếu root/time/region; LEMMA ranking CANDIDATE theo entity mẫu; T-012 đã kiểm ba archive; label-level quyết khả năng chấm. Root/bậc graph/IsError/attention/exceedance không tự là nhãn vùng. Injection-delay không onset-delay thật.

## 8. Rò nhãn và độc lập

Tên ca/path/nhãn tiêm/PPTX/error_trace_type chỉ census/chấm hoặc ngân sách học G1. Không chọn SLI/operation theo root. Eadro align/shuffle có nguy cơ overlap; LEMMA case-dependent selector chưa adapter an toàn. Raw/processed/export cùng trace không là quan sát độc lập.

[Lineage](../T-012/independence-matrix.md) tách author/injector/collector/reuse. OpenRCA dùng AIOps; OpenRCA2TT dùng Fang/FSE; LEMMA Original/Preprocessed và LO2v1/v2 chung lineage. Cùng collector không chứng minh reuse byte; khác tên/hệ không tự đạt ba trục. **Tiêu chí9 OPEN**, gồm Bank. [Bảo toàn](bao-toan-openrca-bank.md) chấp nhận quality chưa kiểm theoủy quyền, không dựa điểm phương pháp.

## 9. Chi phí và dựng lại

Byte Nezha/Eadro ở manifest tải; Deep37 file728.831.613byte; LEMMA bốn ZIP1.583.143.326byte, stream17.500.872.729member-byte. Member-byte không nhu cầu đĩa khi streaming. T-012 ba archive628.411.611byte đạt checksum; lượt TRCA lỗi335.055.240byte giữ riêng. Parsing không benchmark phương pháp/adapter. EC2 mới Q47, không instanceT007. Không RCA/commit/push. Lệnh dựng/chạy lại ở thẻ/inspection-plan nhánh, dùng run-id mới.

## 10. OPEN và handoff

| OPEN | Người/đầu vào | Kết luận phụ thuộc |
|---|---|---|
| License artifact/data/code | Chủ nguồn đúng release; NC/ND không tự chọn một | Permission/tiêu chí1 |
| Clock/alias/timeline | Nguồn đồng hồ/mapping; Codex ghi, Minh quyếtprotocol | Ranking/time/graph đúng ca |
| Deep normal span/embedding loader | Chủ nguồn giải lineage; log không tạo span | So raw↔graph/loader nguyên trạng |
| LEMMA PR KPI/normal, storage/pod unit | Preprocessing/labels, không sửa payload | Ranking/probe/graph |
| T-012 ngoài ba archive đã kiểm | TrainTicketTrace/LO2 lớn ngoài phần tải; OpenRCA2 chưa public archive ghim; Bank quality tớiG3 | Không suy chất lượng từ nguồn/metadata hoặc gọi không làm do budget là không thể |
| G1/tập độc lập | Minh xét cùng RCAEval/Sock Shop | Chọn dataset/thí nghiệm/dev-test |

Đã kiểm file trong phạm vi Q-47 và tổng hợp Q-50; handoff không nghĩa mọi dataset đạt hoặc mọi OPEN đã giải. [Phân công](phan-cong.md), [tự phản biện](tu-phan-bien-nguon-va-giao-thuc.md); Claude phản biện gộp độc lập.



## Phản hồi và sửa REVIEW — 04/10/2026

R1 đúng: đã thiếu kiểm ba archive nhỏ và bàn giao sớm. Nay đã tải/checksum/CRC/fullinput AnoMod, TRCA, FSE; [thẻ cập nhật](../T-012/the-dataset.md). FSE reduced có10folder,2marker.invalid,8ca không marker/11rootservice/8mãfault; không suy1.430ca. AnoMod có13capture mỗi hệ (12fault-name+1baseline), targets có trong script/config nhưng không runtime gold; probe có điều kiện, không nhãn root tự tạo. Không trace-ID overlap giữa capture, TT không span trước name timestamp; lookback24h là cấu hình, không bằng chứng contamination thực.

R2 đúng về selection leakage: [toàn101ca](../T-008/runs/sampling-leakage-001/result.json), mỗi trace/log/traceid đúng ba minute-file quanh tiêm. Đổi tên không phục hồi negative coverage. Không continuous blind F1 từ trace/log release riêng; metric calendar là phạm vi khác. R4 đúng về thiếu nguồn catalog, nhưng F5/F12 chỉ gợi ý kiểu lỗi; F23–F25 còn vắng catalog, không biến thành root gold. [Catalog](../T-010/runs/catalog-review-001/catalog.json).

R3 đã kiểm inventory/census nhãn Bank; không mở số đo. Lý do bảo toàn và giới hạn không lỗi mã nguồn sửa tại WHY13, không thay lựa chọn theo measurement. TRCA xác minh1.165CSV và4nhãn identicalNezha; [fullhash](../T-012/runs/trca-reuse-001/result.json), không corpus độc lập mới. [Phản hồi từng điểm](../../tasks/T-003-the-dataset-ngoai-rcaeval/REVIEW.md). Minh chưa đóngtask/G1.
