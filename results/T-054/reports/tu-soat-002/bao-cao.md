# T-054 — Tự soát và checkpoint triển khai 002

Ngày 05/11/2026. Codex là người làm; Claude vẫn là người phản biện chính thức. Đây là báo cáo tiếp tục triển khai, không thay một lượt REVIEW. **Pha 1 chưa hoàn tất; chưa đủ khóa G3 hoặc chạy test.**

## 1. Yêu cầu nguồn và nhận xét riêng

Quyền tiếp tục được giữ nguyên tại `runs/trien-khai-002/quyen-minh.txt`. Minh cho triển khai phần đủ quyền và yêu cầu dừng đúng nhánh còn chặn. Lượt này đã biết lịch sử, nên không nhận là soát mù mới. Báo cáo 001 §1 giữ nguyên giới hạn lần đầu đọc 48 dòng SPEC cùng năm nhận xét riêng trước đối chiếu toàn SPEC/phản biện. Không viết lại lịch sử này.

- **Câu hỏi nguồn:** DT18-NV2/NV3, hướng dẫn cô §1/§3, MRP RQ3/P7 cần phương pháp có vai trò tính toán của quan hệ, so sánh tương đương và đánh giá độc lập sau chọn thiết kế. P7(a) bao phủ xếp hạng và can thiệp tính toán; chưa trả lời detector, độ đúng vùng ảnh hưởng, hiệu quả LLM hoặc áp dụng FlashTicket. C-a0/a1 và việc bỏ thành phần chưa chứng minh topology thật hoặc hơn một phương pháp không quan hệ được chọn độc lập.
- **Bằng chứng sẵn có:** P4/P5 và chuỗi dev cho thấy cơ chế tính toán có điều kiện; các tác động đổi dấu giữa nhóm, TT và OB. T-041 §5/§8, T-040 `ban-giao-p6.md`, T-052 `phan-tich-bo-sung-002.json#/mechanisms` và hồ sơ 004 là điểm vào. Chưa phân xử cơ chế vật lý giữa vị trí tiêm, tải, mạng và thiếu quan sát. Không dùng trạng thái nghiệm thu hoặc hash để xác nhận phương pháp đúng.
- **Tái dùng:** các số dev đã hợp lệ vẫn giữ, với đúng ca/cửa sổ/cấu hình/seed/variant/máy nguồn và các trường trung gian tương ứng. Kiểm hash trước phiên xác nhận checkpoint trước; kiểm cuối phiên xác nhận lại 93 pin code nền. Không tính lại toàn bộ T-052/T-053. Không dùng pin LOG/STATE lịch sử để ép trạng thái hiện tại quay về trước.
- **Nhận xét riêng trước đối chiếu lại:** fixture cũ chưa thay pilot thật; quản lý trần tổng, DRAIN TORAI và journal cắt dở có thể chặn một lô thật dù các phép tính hạng đúng. Đọc code và tái hiện vận hành xác nhận các thiếu sót dưới đây. Không có căn cứ dừng phần cài công cụ độc lập đã được Minh cho phép.
- **Bước cần trước khóa:** liên kết nguồn gốc độc lập, đầu vào thực xử lý và seal→nhãn phải đi qua driver thật, đủ vế; có parity dev, phân loại lỗi, thời hạn, mẫu số và quyết định trước test. Sau quyền G3/test mới chạy bản khóa; giữ kết quả đầu, khai riêng mọi bản sửa có dùng test. Không suy quyền RE3 hoặc TORAI A từ quyền triển khai.

## 2. Lỗi công cụ xác nhận và xử lý

| Điểm | Bằng chứng và hậu quả | Thay đổi trong phạm vi T-054 | Phép kiểm |
|---|---|---|---|
| Journal có đuôi JSON dở | Tái hiện `runs/trien-khai-002/reproduce-journal-001.json`: nối event mới vào đuôi cũ có thể làm mất event, sau đó lịch sử không đọc được. Chặn tiếp nhận lô nếu xảy ra. | Khóa ghi theo hệ điều hành; giữ nguyên byte dở trong tệp riêng trước cắt phần chưa commit; event phục hồi giữ offset/hash. Không bỏ qua dòng hỏng đã có newline. | `queue-fixtures-004/summary.json#/checks`: đuôi dở, dòng hỏng hoàn chỉnh, 100 event ghi đồng thời không mất, đọc lịch sử lớn theo dòng. |
| Chưa thực thi trần tổng/nhóm và DRAIN ở pipeline | Timeout mỗi job không phải trần lô; TORAI đi nhánh riêng có thể tiếp tục phát sau DRAIN. Chặn phát lô thật an toàn theo thời gian. | Lưu mốc/cost qua resume; kiểm trần toàn lô và method×dataset, cả prep/method. DRAIN kiểm trước mọi job mới. Hết trần vận hành giữ WAIT/BLOCKED, chưa chấm TIMEOUT khoa học. | Cùng summary: giới hạn tổng/nhóm, resume không reset; không sinh attempt TORAI chưa phát khi DRAIN. |
| Kiểm restart cũ dừng launcher trên Windows | `regression-transport-001/fixture-failure.json`: khóa supervisor vẫn bị giữ. PID launcher có thể khác Python thật; phép thử cũ chưa chứng minh đã kill supervisor. | Lưu danh tính supervisor thật; worker thật phải có quan hệ cha/token/thời điểm tạo phù hợp. Phép thử kill đúng supervisor và nhận lại worker còn sống. | `regression-transport-002/recovery-target.json`; summary có nhận lại đúng một attempt và một method-start. |
| Phụ thuộc main→C-d3 chưa đăng ký bất biến | Hash output main chưa tồn tại lúc khai plan. Tự đổi job sau chạy sẽ làm sai identity; payload seal rời không đủ provenance. | Khai slot và pin job cha trước; sau verify tạo seal liên kết receipt/output cha, execution-job riêng; giữ plan và job gốc. Seal được kiểm lại khi chấm. | `queue-fixtures-004/summary.json`: main và C-d3 VERIFIED, plan bất biến, tráo payload rồi rehash bị bác, sai thứ tự dependency bị bác. |
| A4 chưa kiểm toàn bộ tập đăng ký trước reader nhãn | Snapshot đủ các slot do plan tự khai chưa chứng minh plan đủ ca/seed/vế; có thể đưa A hoặc thiếu B vào A4. | Đối chiếu runtime metadata, cửa sổ và nguồn; TT M1+B ba seed, OB M1+M4; kiểm trước đọc nhãn. A là phụ. | `a4-guard-fixtures-001/summary.json`: tám phản ví dụ, `label_reads_on_bad_input=0`; regression báo cáo dương chạy riêng. |

Đây là lỗi triển khai đã có bằng chứng, không phải sửa thiết kế nghiên cứu. Chín script trong `results/T-054/scripts/` được đổi; không sửa src hoặc nguồn lịch sử. Diff đầy đủ so freeze003 được giữ tại `runs/trien-khai-002/diff-*.patch`.

## 3. Kiểm thực tế và giới hạn

Tất cả đường dẫn bảng này nằm dưới `runs/trien-khai-002/`. Không cộng số kiểm trùng giữa các lượt thành tổng độc lập.

| File / con trỏ | Kết quả | Phạm vi thực sự |
|---|---|---|
| `queue-fixtures-004/summary.json#/count` | 25 kiểm, PASS | Vận hành/nguồn tổng hợp, process thật; không telemetry công khai. |
| `regression-transport-002/summary.json#/count` | 60 kiểm, PASS | Liên kết nguồn/nhãn/pha, phục hồi controller, A4 và worker C-d3 trên cấu trúc tự sinh. |
| `torai-a-fixtures-001/summary.json#/three_seeds` | Seed 0/1/2 đều OK và VERIFIED | Prep A và method TORAI Python 3.8 thật trên parquet/CSV tự sinh. Không đọc nguồn CSV A thật, không là tái lập benchmark. |
| `torai-a-fixtures-001/summary.json#/prep_seed_independent_bytes` | true | Bốn bảng prep khớp byte giữa ba seed trong fixture này. Chưa chứng minh cache đúng/nhanh trên ca A/B thật. |
| `a4-guard-fixtures-001/summary.json` | Tám đầu vào sai bị bác, không đọc nhãn | Kiểm gate metadata; seal được cô lập bằng spy. Không thay regression toàn tuyến. |
| `regression-report-001/summary.json` | PASS: 28 slot, 89 dòng, bốn dòng vùng, hai vị trí N | Nhãn và baseline tổng hợp; đầu ra M1 từ dữ liệu tự sinh của checkpoint trước. Không là pilot dataset thật. |

Giữ toàn bộ lượt hỏng. `queue-fixtures-003/failure.json` giữ lỗi khóa byte Windows trước khi sửa cách mở khóa; bản 004 đạt. `regression-transport-001/fixture-failure.json` giữ sai PID trong phép thử; bản 002 đạt. Tái hiện journal đầu tiên còn nguyên. Lệnh in JSON lần đầu bị cp1252 sau khi file đã lưu; không coi là phép kiểm phương pháp thất bại. Các lượt lỗi từ checkpoint 001 cũng không bị đổi.

Kiểm đóng gói tại `runs/trien-khai-002/validation.json`: PASS. Đối chiếu 1.377 file đầu phiên; 1.366 file giữ nguyên, 11 file đổi đúng phạm vi (chín script, LOG chỉ nối và đúng một dòng T-054 STATE). Toàn bộ 93 pin code nền khớp; chín script qua kiểm cú pháp. Freeze004 có 107 file và archive khớp byte nguồn. Không còn worker/supervisor T-054 đang chạy. Kiểm lại toàn bộ pin đầu ra theo manifest là bước cuối chỉ đọc.

## 4. Quyết định Minh và đề xuất thời gian

Nguồn lời Minh: `manifest-quyet-dinh-001.json#/raw_answers` và mục bổ sung trong LOG. **USER_CONFIRMED:** cho tăng thời gian; giữ TORAI A bảng phụ ngoài A4, cấp quyền nguồn riêng sau. Không còn OPEN về việc giữ/bỏ A. Mức trần mới bằng số và cách chấm lúc cạn trần vẫn chưa được chọn. Tăng trần lô không tự đổi timeout phương pháp.

`runs/trien-khai-002/pilot-proposal.json` là **CANDIDATE, CHƯA KIỂM**, chưa là plan phát việc. Đề xuất 58 M1-family, 14 baseline slot và bốn C-d3; 14 slot baseline gồm hai slot OB không hỗ trợ, không có solver tương ứng. Chia local 59, EC2-1 chín, EC2-2 tám đơn vị; OB giữ local. Đề xuất trần pilot 3 giờ trôi, tối đa 9 giờ-máy trên ba máy; khởi đầu một worker/máy, timeout method đề nghị 600 giây, C-d3 60 giây. Đây là trần quản trị dự kiến, **không là ETA**. Chưa đo setup/sync/env/parity hiện tại, nên có thể cao hơn hoặc thấp hơn nhu cầu. Chỉ dùng EC2-2 nếu tổng setup/sync/parity có ích so với nhánh local được giải phóng. Không tạo lượt chạy chỉ để dùng máy.

Pilot chính đề xuất chưa gồm A vì nguồn chưa cấp. A có ca/ba seed đề nghị riêng trong cùng file; vẫn là nghĩa vụ trước G3 nếu giữ. Các số trên không bao hàm pilot A. Khả năng chạy hai/ba worker chưa cài trong scheduler hiện tại; cần hoàn thiện và đo theo SPEC trước khi dùng. Chưa xin Minh duyệt phát lô khi plan nguồn/môi trường chưa hoàn chỉnh.

Đề xuất ghi chính thức, **chưa ghi** vào `docs/DECISIONS.md`: “Minh cho tăng thời gian thực hiện T-054, mức cụ thể cần dự toán; giữ TORAI A ở bảng phụ ngoài A4, cấp quyền nguồn riêng sau.” Lý do giữ bảng phụ vẫn cần nguồn lý do đã duyệt trước dùng trong kết quả; không tự gán lý do khoa học cho lời Minh.

## 5. Phần còn thiếu và tiếp nhận

**Chặn chấm lỗi và khóa G3:** ERROR/TIMEOUT thật vẫn BLOCKED; chưa có đường hoàn tất phân loại có pin đủ chứng cứ và chính sách đã duyệt để tính trượt. Chưa phân xử xung đột P3 §8.3 với đề nghị PENDING/BLOCKED khi cạn trần. Không lấy hành vi dừng vận hành fixture làm chính sách chấm mới.

**Chặn pilot thật:** chưa có plan thực dựng từ nguồn dev gốc độc lập, runtime/label bindings, grant materialize/pilot/SSH/sync, môi trường từng máy/pha và dung sai parity khai trước. Đề xuất pilot mới có tham chiếu ca nhưng chưa chứng minh phủ đủ mọi nhánh SPEC §7. C-e cần chứng nhận hỗ trợ lịch sử/A0 từ nguồn có thẩm quyền; không tự tạo hai bản đồ giống nhau rồi gọi độc lập. Chưa có số đo cold/warm/tải cạnh tranh/cost toàn tuyến. Thiếu grant nguồn A chặn đúng nhánh A.

**Hồ sơ chưa đồng bộ:** protocol/matrix/pilot-plan/root source-manifest và ho-so-g3 từ checkpoint 001 còn chứa trạng thái cũ. Đặc biệt A còn ghi OPEN và own_scripts trỏ byte trước sửa. Giữ chúng như lịch sử, không dùng để tuyên bố bản hiện tại đã khóa. Checkpoint hiện tại dùng `manifest-trien-khai-002.json` và `runs/trien-khai-002/source-current.json`; freeze004 chỉ là gói công cụ, không là khóa G3. Không chạy lại `lap_ho_so.build_documents()` vì nó sẽ ghi đè hồ sơ từ giả định trước câu trả lời Minh. Phiên mới phải cập nhật generator và hồ sơ theo nguồn quyết định trước dùng.

**Còn mở về nghiên cứu:** hiệu quả độc lập RQ3b/d, các giải thích vật lý, detector RQ3a, nhãn vùng độc lập và phần P8–P10. Fixture đạt không trả lời các câu này. Không đề nghị nghiệm thu task hoặc chuyển pha.

Ngữ cảnh bị nén trong lượt này. Theo AGENTS §5a.2 đã nối checkpoint ngay vào LOG, rồi chỉ kiểm và đóng gói bàn giao. Đề nghị Minh mở phiên mới để tiếp tục T-054; không tự tạo chat hay gửi sang Claude. LOG chứa prompt chuẩn trung tính và thứ tự tiếp nhận cụ thể.
