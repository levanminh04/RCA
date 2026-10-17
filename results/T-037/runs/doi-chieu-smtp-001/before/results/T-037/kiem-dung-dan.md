# Tự kiểm T-037 — kết quả hiện hành

**Hoàn tất phần mô hình thiết kế có điều kiện và bàn giao để Claude phản biện.** Minh chưa nghiệm thu task. Không xác nhận runtime FlashTicket, lợi ích RCA hoặc đóng RQ3/RQ5/G3.

## Đầu vào và pin

Trước sử dụng, kiểm manifest T036/T037 và nguồn/mã tại runs/tiep-smtp-001/preflight.json: 287 kiểm đều khớp. T036 manifest/snapshot cũ giữ nguyên. Mã hiện hành chỉ thêm smtp vào hai guard; T037 dùng pin nền + bổ sung đã được Minh duyệt, ghi rõ tại hop-dong-smtp.md và snapshot code của graph-003. T038/T039 giữ SPEC/pin; phiên này không ghi code/kết quả của hai nhánh.

Oracle nguồn ban đầu, thiếu sót, phản ví dụ và các run lỗi được giữ; không dùng việc T036 đã đóng để bỏ nhu cầu SMTP. Bổ sung SMTP có oracle literal fixtures-smtp.json trước checker/mã, source requirement B13 L199/B14 L82/B14-03 L9–12. Full graph dùng oracle-v2 trước converter; oracle-v3 chỉ sửa phía missing operation mapping của fixture broker→consumer thành target trước lượt kiểm mới. Tên runtime vẫn null.

## Kiểm đã chạy và ý nghĩa

| Phép kiểm | Kết quả / file | Điều chứng minh |
|---|---|---|
| SMTP mới/âm/chiếu/không mutation/typed giới hạn transport | 100/100, runs/smtp-regression-001/result.json#/checks | Giữ smtp qua hai mức/chiếu; sai type/channel bị từ chối; endpoints/type agreement không xác nhận protocol |
| Toàn checker T036 cũ, redirect output vào T037 | 221/221; 312 graph,156 cặp chiếu; #/original_regression | Logic kiểm cũ không đổi; mọi221 check records và 10 artifact cũ so nội dung giữ nguyên. Adapter chỉ ROOT/output/nhãn lệnh, có diff |
| Bản ghi→ID/type/address→graph/binding/signal; oracle literal và hàm độc lập | 1598/1598, runs/graph-003/result.json | Chính xác từng record ID/provenance/context/endpoint/type/address và phần phép chiếu được hứa, không chỉ tổng số |
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

SMTP+checker cũ: tổng 27.669s; child T036 26.759s, peak working set 115253248 byte. Lượt graph hiện hành 1.252s, peak 81518592 byte (runs/graph-003/result.json). Đây là chi phí máy của input hiện tại, không ngoại suy giờ đọc nguồn. Trước lượt đo không process vượt0,35CPU-second trong mẫu1giây; helpers đã ngừng build/đo và chỉ thu nguồn nhẹ. Không dừng process khác.

Dự toán giờ công còn lại 3–5 giờ ở checkpoint là chưa đo; wall-clock qua ngắt usage/chờ Minh không là giờ công liên tục. Tổng dung lượng thực cho **mọi** lượt gồm lỗi/snapshot/bản trước/script/diff nằm trong manifest.json; tải/giải nén mới0. Không EC2/GPU hoặc lượt >1giờ. Không giảm coverage/tiêu chí để tiết kiệm thời gian.

Giới hạn nguồn: graph các quan hệ có đủ type/address, các arrow support còn chưa phân kiểu lưu nguyên văn/owner/input; topology là thiết kế. Queue/scope/runtime names/telemetry chưa xác minh. Phép tính P5 dùng cạnh để gộp, chiếu, giữ địa chỉ và đối chiếu cấu trúc; không phát hiện/ranking. Shared resource binding chưa là cạnh computational của T035. Không mở test/heldout/trace/log/metric thô hoặc chọn P6.
