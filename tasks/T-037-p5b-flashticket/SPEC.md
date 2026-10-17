# T-037 — P5b: FlashTicket đầy đủ theo thiết kế

- **Trạng thái:** ĐỀ XUẤT / CHỜ PHẢN BIỆN SPEC. Minh duyệt ghi tài liệu chuẩn bị ngày 15/10/2026; chưa duyệt triển khai, tải nguồn hoặc chạy khảo sát.
- **Người làm:** Codex.
- **Người phản biện:** Claude theo phân công P5; riêng lượt soát ba SPEC T-037–039 là Codex phiên sạch độc lập theo ngoại lệ Minh chỉ định. Ngoại lệ chỉ ở công đoạn SPEC, chưa cho ghi REVIEW và không tự áp sang phản biện kết quả.
- **Thuộc gói MRP:** P5 — **Cổng:** chuẩn bị G3; chưa là quyền mở test.
- **Nguồn quyền:** Q-159–Q-163; nguyên lời Minh lưu tại LOG T-037 Phiên 1. Các bước triển khai và phạm vi kết quả dưới đây là đề xuất chờ Minh duyệt.

## Mục tiêu

Từ nguồn kiến trúc, dữ liệu, hợp đồng giao tiếp, luồng và chuẩn quan sát hiện hành của FlashTicket, lập inventory thực thể đầy đủ trong phạm vi nguồn được ghim; chủ động khảo sát thao tác khi có bằng chứng; dựng graph tĩnh và địa chỉ tín hiệu theo T-036. Phục vụ DT18-NV2, bước 1 của cô, MRP P5 và đầu vào RQ3/RQ5/P6/P9.

Đây là khảo sát và mô hình hóa nguồn thiết kế. FT mới chưa có code ứng dụng theo xác nhận đã lưu; không lấy code cũ hoặc ví dụ tổng hợp làm bằng chứng runtime. Graph dùng cạnh để biểu diễn/chiếu và chuẩn bị đối chiếu; chưa có phép phát hiện bất thường/xếp hạng hoặc bằng chứng sửa hạn chế P4. T-037 bao phủ nhánh FlashTicket của P5b; T-040 tổng hợp, P6 chọn thiết kế và P9/P10 kiểm dữ liệu/thực nghiệm thật.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn/giải thích khác | Phép phân xử và bằng chứng | Hỗ trợ, bác bỏ hoặc chưa phân xử | Phần thiếu và quyết định phụ thuộc |
|---|---|---|---|---|
| Có đủ thực thể/quan hệ theo B11–B16 không? DT18-NV2 | Chỉ các service hoặc đường thành công có thể bỏ DB, broker, callback, nền và hỗ trợ | Bảng yêu cầu từng nguồn → inventory/bản ghi → cạnh/binding/địa chỉ; rà cả nhóm ngoài trace benchmark | Chỉ nhận đầy đủ ở phạm vi nguồn đã ghim và kiểm coverage; phản ví dụ còn bỏ sót bác bỏ nhận định đầy đủ | Nguồn thiết kế chưa rõ hoặc mô hình không giữ được phải trình, ảnh hưởng T-040/P6/P9 |
| Operation nào có căn cứ? lựa chọn Minh trong P5b | Mỗi hàm, role producer/consumer và operationName runtime là những thứ khác nhau | Dẫn từng thao tác/owner/tên gốc; runtime_name chỉ khi có nguồn xác minh | Hỗ trợ khi truy về yêu cầu/luồng; thiếu tên runtime giữ null/OPEN, không tạo operation giả | P9 xác minh instrumentation; P6 chưa chọn mức thao tác |
| DB và async giữ đúng nghĩa không? B12–B14 | DB logic khác instance chung; message khác lần thử; callback/scheduler không cần caller giả | Bản ghi → ID/kiểu/địa chỉ/owner → graph/chiếu, kiểm nhiều queue, fan-out, bù trừ, tài nguyên chung | Không gộp mất DB/queue, không bịa sự kiện hoặc nối từ correlation; cần lớp ngoài trace phải khai rõ | Hợp đồng chung thiếu thì trình sửa, không xóa nhu cầu hoặc sửa T-035 |
| Tín hiệu đặt ở đâu và runtime phải cung cấp gì? DT18, B16 | Có địa chỉ thiết kế không chứng minh đã thu đúng | Ma trận log/trace/metric → thực thể/operation/resource/queue → khóa nối và nơi ghi | Đủ để đề xuất hợp đồng quan sát; chưa xác nhận telemetry, nhánh đã chạy hoặc lợi ích RCA | P9a instrumentation/config, P9b chuẩn hóa, SPEC đối chiếu runtime sau |

## Đầu vào

- AGENTS.md, docs/STATE.md; docs/MRP.md §3 (RQ3/RQ5), P5/P6/P9 và G3; docs/LESSONS.md; WHY-52/53 và các quyết định trực tiếp liên quan trong docs/DECISIONS.md.
- docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2–3 và docs/reference/sources/advisor-2026-09-23.md §1; phương án P5b gốc tại LOG T-036 Phiên 1; tasks/_MAU/SPEC.md và docs/review-prompt.md.
- T-036 đã nghiệm thu theo Q-158: results/T-036/{manifest.json,hop-dong.md,nguon.json,ban-giao.md}, REVIEW và mốc đóng trong LOG T-036; src/do_thi_tinh/README.md và code. Kiểm hash trước dùng; lệch thì dừng phần phụ thuộc, không tự cập nhật hash để hợp thức hóa nguồn.
- D:/Project/flash-ticket-platform chỉ đọc: AGENTS.md, skill .agents/skills/govern-capstone-work/SKILL.md và các nguồn trực tiếp mà skill yêu cầu; docs/architecture/B11-C-target-architecture.md, B12-data-ownership-and-schema.md, B13-api-and-event-contracts.md, B14-main-flow-sequences.md, B16-observability-baseline.md. Ghim revision/hash nội dung và dirty state thực đọc; registry T-036 là đầu mối, không thay việc đọc nguồn.
- T-035: results/T-035/manifest.json, dac-ta-do-thi.md, thong-tin-theo-quan-he.md và code/schema cần đối chiếu sau kiểm hash. Không tự nghiệm thu T-035 từ việc dùng nó, không đọc trace thô hoặc dataset khóa.
- Python/môi trường theo README T-036; dùng -X utf8 -B để không ghi bytecode ngoài phạm vi. Không cần tải repo hoặc dựng hệ thống trong gói đề xuất này.

### Ghim chung và song song

Cả T-037/T-038/T-039 dùng cùng snapshot hợp đồng nguồn tĩnh v1 sau sửa R1: results/T-036/manifest.json, created_utc 2026-10-15T13:45:08.305188+00:00, current_run runs/kiem-r1-after-002. Code tham chiếu là snapshot ở results/T-036/runs/kiem-r1-after-002/code/ và code-hashes.json; hợp đồng/registry được manifest T-036 phủ. Hash nằm trong manifest, không dùng HEAD thay nội dung file. Khi triển khai, lưu pin đầu vào của task vào manifest riêng và kiểm code hiện hành so với snapshot này. Không tự chuyển sang phiên bản khác nếu nguồn thay đổi.

Ba task chỉ được triển khai song song sau khi **từng SPEC được Minh duyệt triển khai**. Mỗi nhánh chỉ ghi phạm vi riêng. Nếu cần đổi hợp đồng/code chung, dừng phần phụ thuộc và trình Minh về phản ví dụ, phạm vi sửa và ảnh hưởng ba nhánh; không tự fork một nghĩa cạnh hoặc alias chung để chạy tiếp.

Cập nhật STATE thực hiện tuần tự: đọc lại bản mới nhất ngay trước ghi, chỉ thay đúng dòng task; nếu file đổi trong lúc chuẩn bị thì đọc lại và áp vào bản mới, không ghi đè nhánh khác. Quyền chuẩn bị không là quyền tự mở/gửi chat.

## Đầu ra

Sau khi được duyệt triển khai, trong results/T-037/:
- nguon.json và bao-phu-nguon.md/json: nguồn/revision/hash/điều kiện; bảng từng yêu cầu/đoạn nguồn, đã đọc/loại trừ/chưa rõ và ảnh hưởng. “Đầy đủ” phải chỉ đúng phạm vi nguồn thiết kế, không là toàn runtime.
- ban-ghi.json: inventory, operations, relations, resource_bindings, signals có provenance theo T-036; bảng coverage nối từng yêu cầu tới bản ghi hoặc OPEN có owner/đầu vào cần.
- do-thi/: graph thực thể/thao tác, phép chiếu, phần entity-only, inventory riêng với observed nodes/tập ứng viên.
- hop-dong-runtime.md: trường/khóa và ví dụ tổng hợp có khai báo, cách đối chiếu runtime khi có dữ liệu; không làm phép đối chiếu FT thật.
- kiem-dung-dan.md, manifest.json và runs/: oracle độc lập, lệnh/môi trường/mã chạy, trung gian, thời gian/RAM/đĩa và mọi lượt kể cả lỗi.
- ban-giao.md: thông tin cụ thể cho T-040/P6/P9, phần chưa biểu diễn/quan sát được, owner, nguồn hoặc phép kiểm cần và quyết định phụ thuộc.

## Phạm vi ghi

**Hiện tại chỉ được tạo SPEC/LOG và tài liệu chuẩn bị trong gói chín file Minh duyệt.** Phạm vi tương lai sau duyệt triển khai: results/T-037/, nối LOG T-037 và đúng dòng T-037 trong STATE. Không bao gồm src/, WHY/DECISIONS, nguồn T-035/T-036, repo platform hoặc task khác. Nếu cần thay hợp đồng chung, trình riêng trước sửa.

## Các bước

1. Kiểm quyền, nguồn trực tiếp, manifest và pin chung; đọc dữ liệu bàn giao đã có, không làm lại đầu ra hợp lệ.
2. Kiểm revision/dirty/hash nguồn thiết kế; lập bảng coverage toàn B11–B16 và nguồn được chúng dẫn trực tiếp khi cần. Mục chưa đủ nguồn giữ rõ, không lấy số fixture làm bằng chứng coverage.
3. Khảo sát đầy đủ các nhóm có nguồn: HTTP/RPC/gateway; ownership/DB logic/instance/cache; publish–broker–consume, exchange/routing/queue, outbox/inbox, ACK/confirm, retry/redelivery/dedup/fan-out; callback/query; scheduler/background/relay; Saga/bù trừ/terminal fence; delivery/check-in; role-grant/projection và hỗ trợ/vận hành. Đây là nhóm cần rà, không thay danh sách yêu cầu cụ thể trong nguồn. Không tự thêm nghiệp vụ.
4. Lập inventory và thao tác có owner/tên gốc; giữ điều kiện nhánh/phục hồi. Lập địa chỉ log/trace/metric, resource binding và các tên runtime còn OPEN. Nguồn gián tiếp, cấu hình hoặc phần bị loại nếu có phải được xét về ảnh hưởng, không chỉ đọc tệp dễ thấy.
5. Viết oracle độc lập cho các chuyển đổi riêng; dùng build/project T-036 đã ghim. Lần từ bản ghi → ID/type/address → cạnh/phép chiếu/provenance. Thiếu biểu diễn thì giữ phản ví dụ, thông tin mất/phương án và dừng phần phụ thuộc để trình Minh.
6. Kiểm hợp đồng đối chiếu runtime bằng fixture rõ là tổng hợp: nhiều queue/shared instance, operation thiếu mapping, callback trace mới, scheduler không caller, unknown/thiếu địa chỉ; giữ graph nguồn và trace riêng. Không tạo caller/message edge từ correlation.
7. Tự kiểm coverage từng nguồn và từng nhóm; đối chiếu cả quan hệ có operation lẫn entity-only. Đo pilot sau có quyền, tính tổng chi phí; nếu không vừa một phiên thì trình tách, không giảm độ sâu.
8. Soát toàn diff/phạm vi, manifest và kết luận; bàn giao trường/khóa/nơi ghi/phép kiểm cho P9 và thông tin có thể dùng cho P6. Ghi LOG, dòng STATE và prompt theo mẫu; Minh quyết nghiệm thu.

## Kiểm đúng đắn

Kiểm từng requirement → bản ghi → graph/binding/signal hoặc OPEN có lý do, không chỉ tổng số thực thể/cạnh. DB logic không gộp thành instance, không tạo nhiều instance giả; shared metric không sao thành bằng chứng độc lập mọi operation. Producer/consumer là role; broker/scope/exchange/routing/queue giữ riêng và không bịa event_count. Giữ quan hệ nội bộ/span-parent trong records/lớp thao tác, không chiếu chúng thành cạnh phụ thuộc thực thể; báo riêng phần entity-only/thiếu operation theo hợp đồng. Không tạo thao tác để làm đẹp tỷ lệ chiếu.

Tách thiết kế/code/runtime/lợi ích; giữ chiều bù trừ theo nguồn, callback/scheduler theo trace riêng dự kiến. Mỗi signal có địa chỉ/namespace/owner và nơi phải ghi; collector không phục hồi dữ liệu chưa từng ghi. Kiểm tính xác định, lỗi mapping/schema, không sửa input hoặc dùng nhãn. Có mâu thuẫn nguồn/hợp đồng thì dừng phần phụ thuộc, trình rõ thay vì chọn nguồn thuận tiện. Không có số công bố cho phép chuyển bản ghi này; dùng oracle và nguồn, không dựng baseline hiệu quả RCA.

## Tiêu chí xong

1. Inventory, thao tác có bằng chứng và bảng coverage toàn bộ phạm vi nguồn thiết kế ghim; mọi khoảng trống quan trọng có bằng chứng, owner và hướng xử lý, không bị che bởi tuyên bố “toàn hệ”.
2. Quan hệ/địa chỉ/binding có provenance truy ngược; phản ví dụ về DB chung/async/callback/nền/Saga và nhóm còn lại được kiểm, không chỉ chạy không lỗi.
3. Graph/phép chiếu và tín hiệu đúng T-036; nhu cầu chưa biểu diễn phải nêu thông tin mất và đề xuất cần Minh duyệt. Lỗi chặn công cụ/bản ghi chưa xử lý không được gọi đạt.
4. Bàn giao đủ để P9 xác minh/thu/chuẩn hóa và so runtime bằng SPEC sau; P6 nhận dữ liệu mô hình, chưa chọn thuật toán/mức/tín hiệu.
5. Kiểm/manifest/LOG/prompt đầy đủ. Task chỉ cho phép nhận mô hình thiết kế và hợp đồng quan sát có điều kiện; không xác nhận runtime FT, lợi ích RCA, đóng P5b/RQ3/RQ5/G3 hoặc mở test.

## Không làm

Không sửa kiến trúc/nghiệp vụ/code hệ thống; không đọc repo RCA archive hoặc code hệ thống cũ để chứng minh bản mới. Không dựng collector, thu runtime, đọc telemetry thô/test/heldout, chạy baseline, chọn P6, làm thay T-040, bật EC2, tải nguồn, commit/push hoặc tự mở/gửi chat từ quyền này. Nghĩa vụ runtime và thực nghiệm vẫn thuộc P9/P10 và SPEC sau, không bị loại khỏi nghiên cứu.

## Chi phí ước lượng

Dự toán lịch sử FT **4–6 giờ công**, chưa đo, chưa gồm phản biện/chờ nguồn; không là cam kết hoặc trần để giảm kiểm. Thời gian máy và peak RAM còn OPEN, phải đo lượt thử sau khi có quyền, ghi kích thước đầu vào và ngoại suy tổng. Dung lượng tải mới dự kiến không cần cho nguồn local đã nêu; nếu phát sinh tải phải trình nguồn/revision/tệp/byte riêng. Dung lượng kết quả/trung gian/tổng lưu chưa đo và **chưa có dự toán bao phủ mọi lượt chạy**, gồm lượt lỗi, chạy lại và bản cần giữ.

Phân biệt giờ đọc/phân xử với giờ máy; tổng chi phí tính mọi bước/đối tượng và lượt dự kiến, so với ngân sách Q-40 ở phần tính toán có liên quan. Không chạy việc nặng khác khi đo. Thao tác thuộc luật cứng 8 phải báo trước. **Đề xuất trước duyệt triển khai:** kiểm tính khả thi một phiên; nếu phạm vi đầy đủ vượt một phiên, Minh quyết tách phần nguồn/coverage và phần dựng/kiểm/bàn giao. Không tự chia mã task hoặc thu hẹp mục tiêu để vừa dự toán.

## Rủi ro và điều chưa chắc

Chưa kiểm độ đủ/nhất quán của toàn nguồn thiết kế, tên operation runtime, mapping resource và độ phù hợp hợp đồng chung với mọi nhóm. Giả định có thể sai khi một nguồn bị bỏ, ownership/địa chỉ không đủ nghĩa hoặc hợp đồng làm mất thông tin; ảnh hưởng nhận định đầy đủ và đầu vào P6/P9. FT mới chưa có code theo xác nhận đã lưu nên không kiểm triển khai/runtimes trong task; phải yêu cầu build/deployment/export và instrumentation từ nhóm hệ thống, không coi thiết kế là bằng chứng đã thu dữ liệu.

## Prompt bàn giao

Prompt soát **cả ba SPEC** được chép nguyên văn từ Prompt chung + khối Soát SPEC + khối G3 của docs/review-prompt.md tại LOG.md Phiên 1 của từng task. Chỉ điền thông tin trung tính. Minh chuyển thủ công cho Codex phiên sạch theo ngoại lệ đã chỉ định; phiên đó chỉ đọc/trả lời chat, chưa được ghi REVIEW, sửa tài liệu, triển khai hoặc tải nguồn. Không tự mở/gửi phiên.

## Phụ lục V2: đối chiếu SMTP và tiếp nhận phiên bản chung (Minh duyệt Q-164 ngày16/10/2026)

Giữ pin/ngoại lệ/đầu ra lịch sử trong nội dung cũ. T037 đã hỗ trợ SMTP theo delta được duyệt; T039 đã có132graph dùng snapshot gốc. Gói V2 đổi comparator (optional call channel và marker SMTP cả endpoints/typed) và chuyển cả ba nhánh sang manifest results/T-036/runs/doi-chieu-smtp-001/manifest.json sau hồi quy đầy đủ. Builder giữ nguyên byte T037. Quyền ghi đúng plan.json V2 đã duyệt; hồi quy T036/R1/SMTP, full model/fixture T037,1069TT,132OB và so tập/members/exclusions/mẫu số/input/hash/ordering phải đạt, tách comparator khỏi delta TT. Giữ script/output/pin cũ; runner mới kiểm manifest+snapshot/live tường minh. Các bản hiện hành chỉ chuyển sau cả ba PASS. created_utc/SHA manifest mới lấy từ file thực đã kiểm, hiện OPEN. Nguyên lời Minh duyệt tại Q-164 và authorization.json; không suy nghiệm thu task/G3/test/commit.

### Tiếp nhận V2 đã kiểm — 16/10/2026

Phụ lục V2 ở trên đã được triển khai theo Q-164. Manifest chung: results/T-036/runs/doi-chieu-smtp-001/manifest.json; created_utc thực: 2026-10-16T04:22:36.861568+00:00. Đường dẫn/SHA/created_utc và module hashes chính xác nằm pin.json của cả T037/T038/T039 trong runs/doi-chieu-smtp-001/. Loader kiểm các giá trị này trước import. Cả ba đã đạt toàn hồi quy trước đổi bản hiện hành; kết quả cũ vẫn dùng pin đã sinh chúng. Các chữ OPEN/pending của phụ lục trước là mốc trước kiểm, metadata hiện hành theo pin.json và bàn giao, không suy nghiệm thu task/G3/test/commit.
