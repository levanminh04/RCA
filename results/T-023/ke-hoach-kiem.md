# T-023 — Kế hoạch kiểm trước đọc số đo mới

Ngày 05/10/2026. SPEC đã duyệt; danh sách phiên **chưa duyệt**. Đây là kế hoạch kiểm điều kiện dữ liệu, không benchmark và không chọn nhánh Eadro. Căn cứ: Q-61, Q-63, Q-64; hồ sơ T-013–T-017; metadata T-009. Phạm vi đề nghị tại `de-xuat-chia-phien.md` và `allowlist-phien.json`.

## 1. Đọc đúng phiên

Sau Minh duyệt danh sách cụ thể, ghi lời duyệt và provenance vào allowlist trong phạm vi T-023; không tự nâng trạng thái khi chỉ có SPEC. Selector phải từ chối `proposed`, test, unlabelled, đường dẫn thoát cây, origin/member không kê và member không suy được đúng một session. Known-answer fixture (mẫu có đáp án biết trước) dùng dữ liệu tổng hợp trong `work/`, không mượn test thật.

Giữ canonical (bản đại diện) outer fault vì metadata byte/hash khớp nested. Không mở TT-all để kiểm lặp; xác minh SHA-256 và byte của member **được phép thực đọc** với nguồn cũ. Với normal, chỉ stream hai TAR.XZ riêng, trước extractfile kiểm từng path thuộc allowlist. Payload test không được mở rồi mới lọc. Directory ZIP chỉ là metadata; không giải nén vào input, không unpickle hoặc chạy code tác giả. Hash toàn compressed ZIP khi được phép bước 2 chỉ kiểm danh tính archive, không decode member test; nếu cần thao tác khác phải trình trước.

Manifest ghi từng member thực mở, bytes, hash, timestamp bắt đầu/kết thúc và lỗi; cuối lượt so tập đã mở với tập được phép, không suy từ tập dự định. Fixture phải chứng minh bị từ chối trước mở payload. Giữ run hỏng và lỗi hash/conflict; không last-wins (lấy bản cuối ghi đè).

## 2. Thời gian, session và cửa sổ

Giữ timestamp native của span start/duration, metric và mốc label; log giữ chuỗi gốc và thông tin timezone có thật. Candidate schema từ thẻ/parser T-009: Jaeger microsecond cho start/duration, metric/label epoch second. Kiểm loại, độ lớn, cadence và phép chuyển đơn vị bằng fixture; độ lớn phù hợp không tự xác minh clock nguồn. Tên session chỉ dùng nhận diện, không là clock authority.

Parser cũ `inspect_files.py` gán UTC cho log không timezone. Code tác giả đã lưu không chứng minh timezone hoặc offset export. Bản inspector T-023 phải giữ parse với giả định được ghi riêng; không mặc định cộng/trừ 8h hoặc 16h để khớp hình. Nếu thiếu nguồn clock, giữ OPEN; không lựa clock theo accuracy/root.

Theo Q-64, phần incident là 300 s sau mốc tiêm. Đoạn trước tối đa 300 s, không chồng injection trước và không vượt biên phiên. Khi triển khai, ghi rõ quy ước biên nửa mở `[start,end)` như một lựa chọn giao thức cần đồng bộ T-022; không tự áp kết quả trước khi lựa chọn có hiệu lực. Mốc tiêm chỉ dùng audit chế độ biết trước; không truyền nó hoặc tên fault vào input phương pháp tự phát hiện. Phần normal riêng không được đổi timestamp để ghép thành lịch sử liên tục của phiên fault.

Kiểm toàn phần dev được phép và mỗi cửa sổ: số điểm/span/log, tỷ lệ nằm trong/ngoài phiên/cửa sổ, missing service/operation, khoảng phủ và gap. Không lấy min/max giao nhau hay một phiên tốt làm bằng chứng toàn dataset khớp.

## 3. Phân biệt lệch clock với trace export lịch sử

Ghép log đúng cấu trúc `Span reported` với `(session,traceID,spanID)` và service; giữ cả parent ID/flags nếu schema có. Không regex nhặt mọi chuỗi hex thành ID. Báo phân bố chênh log–span theo phiên, service, trace; số exact match, không match, conflict và các ID lặp liên phiên. Với ID lặp khác nội dung, không gộp để tăng match.

Kiểm các giải thích khả thi: offset cố định của clock; trễ export/report; trace cũ được xuất lại; span ID chỉ unique trong scope; thiếu/lấy mẫu log; payload reported không cùng nghĩa start time. Đối chiếu quan hệ thời gian trong cùng trace, cadence metric và mốc label. Chênh gần hằng nhưng thiếu semantics clock/export vẫn OPEN. Cần bằng chứng identity và thời gian theo từng cửa sổ để kết luận trace thuộc đúng phiên; không kết luận từ tên file.

## 4. Identity và cấu trúc

Khóa scoped `(session,traceID,spanID)`; signature gồm toàn span và service đã resolve qua processes. Bản cùng khóa/cùng nội dung là exact-copy (bản sao giống hệt), lưu multiplicity; cùng khóa/khác nội dung là conflict. Không gộp các conflict hoặc chọn bản đầu/cuối. Parent `CHILD_OF` tìm trong đúng scope trace; đếm root không parent, unique parent, orphan (không tìm được cha), conflict parent, multiple-parent và ambiguous parent riêng.

Kiểm toàn phiên và từng cửa sổ, tách parent ở ngoài cửa sổ nhưng trong phiên khỏi parent thiếu toàn phiên. Giữ bảng intermediate và phép đếm độc lập để mẫu số cân bằng. Fixture: repeated identity exact/conflict, same ID khác session/trace, parent ngoài cửa sổ, nested duplicate metadata, time-unit/boundary. Root chỉ gắn sau kiểm; root vắng trace là thiếu evidence, không tự là service cô lập.

## 5. No-fault: reference/control khác phiên

Kiểm cả hai phiên được phép. Không chọn đoạn sạch sau nhìn dữ liệu để thay reference. Theo service × kênh × phiên: số điểm finite, cadence/gaps/duplicate timestamp, thiếu/hằng, quantile/min/max và độ phủ thời gian. Báo lần lượt các phần thời gian để thấy warm-up/trôi mức/tải; không chốt ngưỡng cắt warm-up mới hoặc detector trong task này.

Đối chiếu service/operation/schema giữa reference, control và từng dev. Tên rx/tx không chứng minh byte hay rate; giữ đơn vị/biến đổi OPEN nếu không có nguồn. Traffic/operation mix có thể là proxy tải nhưng không tự là ground truth tải. Báo normal–normal differences, zero variance, sample coverage; không gán mọi khác biệt là fault hoặc chứng minh calibration. Không chạy ranking/detector để chọn normal theo root accuracy. Nếu không có evidence sạch/đại diện, kết luận reference có điều kiện hoặc OPEN và trình Minh.

## 6. Điều kiện cần theo chức năng

| Phương pháp/chức năng | Phần kiểm dữ liệu cần trả lời | Nguồn hồ sơ |
|---|---|---|
| BARO, N-Sigma, BOCPD | Chuỗi metric numeric finite, clock/cadence/missing, normal khác phiên có phù hợp; unit/source còn thiếu | T-013, Q-67; cấu hình detector do T-022 khóa |
| TORAI bản sửa | Metric và logts có service/time nhất quán; nguồn normal/incident và phép giảm mẫu/ghép thật; trace không tự cứu thiếu log/metric | T-016; WHY-19 |
| SimpleRCA M4 | Metric/latency normal và incident, log theo service/time; thiếu channel khác bảng rỗng; identity/units và constant normal | T-017; không áp regex đoán service |
| MicroRank bản sửa | Trace đúng phiên/cửa sổ, operation/service và latency, đủ normal theo operation; kind/entry/root/parent/instance khi hồ sơ đòi; normal operation mix | T-015; danh sách cắt/output và mapping do T-022 quyết |
| TraceRCA bản finite | Trace thuộc đúng phiên/cửa sổ; latency finite theo caller/callee và đủ normal; policy conflict/parent/mapping | T-015; không chấm ranking |
| CIRCA kiến trúc | Metric sở hữu service, mapping Traffic/Latency/Error/Saturation và SLI có căn cứ; graph caller→callee có provenance; metric thiếu semantic giữ OPEN | T-014; không lấy root để chọn SLI |

Đây là điều kiện cần, không xác nhận phương pháp chạy đúng hoặc đạt accuracy. Có trace export không đồng nghĩa có graph tại injection. Nếu trace không ghép được, không tự chọn metric/log hoặc bỏ; trình Minh nhánh theo Q-61. Không chạy tầng 2 để lấp evidence còn thiếu.

## 7. Kết quả và chi phí

Sau có quyền và thực kiểm, `bang-dieu-kien.csv`/`kiem-eadro.md` ghi PASS/FAIL/OPEN theo phiên/cửa sổ/kênh/phương pháp, đường dẫn intermediate và alternative explanations. PASS chỉ cho điều kiện được chứng minh; nhãn injection không phải onset/recovery và không chứng minh causal graph. Hiện chỉ có metadata, chưa kết luận trace/normal dùng được.

Stream một phiên một lần; bước 3–5 có thể cùng một lượt I/O nhưng lưu evidence riêng, giữ RAM giới hạn theo SPEC. Ghi progress, thời gian và byte ngay từ đầu; RAM đo nếu có, nếu không ghi OPEN. Không cùng parsing nặng với đo pilot cost T-022. Nháp WHY ở `de-xuat-why.md` chưa thay `docs/WHY.md`; chưa được dùng lựa chọn mới làm cấu hình benchmark.

## 8. Bổ sung trước raw — lời duyệt và B1 ngày 05/10/2026

**USER_CONFIRMED:** Minh duyệt đúng 5 phiên/145 member và các điều kiện trong LOG phiên 2. Không đổi seed/danh sách, không mở TT-all.txz hoặc TT-no-fault.txz. Phần quyền đọc có hiệu lực sau cập nhật allowlist; kết luận clock/normal chưa được duyệt thành FACT.

**Giả thuyết clock cố định cho loại bỏ**, khóa trước đọc trace/log:

| Mã | Tọa độ đem so với khoảng session metadata |
|---|---|
| H0 | timestamp native |
| H+8 | timestamp native + 28.800 giây |
| H−8 | timestamp native − 28.800 giây |

Thêm H−8 để bao phủ cách hiểu ngược: clock trace/log cao hơn clock session 8h. Bằng chứng metadata cho reference có trace lịch sử rơi vào phiên không nhãn ở chiều này. Ba giả thuyết chỉ tạo union loại bỏ; không chọn offset, không đổi timestamp hoặc dùng giả thuyết để làm trace khớp injection. Log không timezone dùng tọa độ wall-time (chuỗi giờ địa phương quy ra trục số để so), không khẳng định UTC thật.

Khoảng test dùng bao đóng bảo thủ của start/end label và min/max metric đã lưu; khoảng không nhãn ngày 20/04 lấy min/max metric metadata vì không có label. Kiểm cả hai endpoint thuộc vùng cấm. Mỗi bản ghi timestamp được phân loại vào các khoảng ở từng H. Nếu trúng bất kỳ khoảng test/unlabelled ở bất kỳ H, chỉ đếm theo interval×hypothesis; không lưu/đếm service, ID, latency, edge, level hoặc message. Timestamp không hợp lệ/không có thì fail closed, chỉ đếm thiếu clock. Áp cho cả 5 phiên và cả span/log. Với span, kiểm toàn khoảng [start,start+duration] (duration chỉ là tọa độ kết thúc dùng loại bỏ, không thống kê latency cho record bị loại); record vắt biên vùng cấm bị loại. Đây là bảo vệ bổ sung, không là căn chỉnh.

Parser phải lexical-scan JSON để lấy timestamp trước semantic decode/callback. Framing cần đi qua byte opaque của file được phép; không json.loads cả trace/envelope hoặc service→log map rồi mới lọc. Không ghi payload thô vào work/run. Process/service metadata chỉ resolve đúng processID của span đã được phép, không decode toàn bảng processes. Log đọc prefix timestamp trước giải mã/đọc nội dung còn lại; key service chỉ resolve sau record qua B1. Fixture có payload bẫy ở record cấm, callback giải mã phải không được gọi; kiểm thứ tự gate→decode, denied test ở mọi H và normal lịch sử; riêng fixture time units/ID/conflict/parent/nested duplicates.

Sau fixture đạt, kiểm byte/SHA-256 của ZIP theo manifest T-009 trước mở payload; không testzip toàn ZIP. Mỗi member thực đọc có hash/byte so metadata cũ. Container normal phải chỉ có member đã kê; không extract test/unknown. Giữ cả run hỏng.

**Reference:** so toàn reference với control và với mọi đoạn pre-injection của 3 dev đã xác định từ label trước số đo (khoảng nghỉ 114–124s; đoạn đầu rất ngắn được báo riêng). Không chọn lại đoạn sạch/warm-up sau xem dữ liệu. Chỉ kiểm mô tả từng service/kênh, không chạy detector/ranking hoặc chọn ngưỡng.

**Giới hạn quần thể:** số span trước B1 từ raw-sessions.json T-009 được chép vào run metadata, phân biệt với số sau B1. Dev có 18.544, 18.429, 18.491 span; test có hai phiên 33.250 và 33.332 span. Không suy kết luận dev cho hai kiểu export lớn này. B1 cắt bớt dữ liệu có thể làm trace/normal không đủ; phải ghi mẫu số loại bỏ và kết luận có điều kiện/OPEN, không gọi cả file đã được kiểm nội dung.

### 8a. Sửa phép kiểm sau stream-001, trước stream-002

Giữ nguyên toàn bộ stream-001; không dùng cho kết luận cuối. Kiểm độc lập phát hiện code audit dùng biên đóng chung pre/post, chưa chặn ID thiếu trong usable identity, và ghi hash progress trước cập nhật complete. Sửa thành cửa sổ audit [start,end), để mốc injection chỉ thuộc post; B1 vẫn đóng hai đầu bảo thủ. ID thiếu/không phải hex chỉ đếm invalid, không dựng cạnh/identity usable. Quarters normal chia đều [metric-min,metric-max+1), không chọn đoạn sạch. Sửa thứ tự manifest và đo RAM bằng Windows API có khai báo pointer. Không đổi split, giả thuyết clock, dữ liệu hoặc chọn kết quả theo độ đẹp; không điều chỉnh ngưỡng. Fixture-002 kiểm thêm invalid ID và biên injection trước chạy lại đúng 145 member.
