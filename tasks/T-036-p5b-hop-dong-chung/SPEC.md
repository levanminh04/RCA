# T-036 — P5b: hợp đồng nguồn tĩnh và đối chiếu

- **Trạng thái:** đã duyệt nội dung ngày 15/10/2026; ghi thành SPEC từ phương án Minh đính kèm và duyệt. Chưa triển khai. Phiên Codex mới phải tự soát trước; cần sửa SPEC thì dừng trình Minh.
- **Người làm:** Codex.
- **Người phản biện:** Claude. Tự soát của Codex không thay phản biện chính thức.
- **Thuộc gói MRP:** P5 — **Cổng:** chuẩn bị G3; không là quyền mở test.
- **Nguồn duyệt:** docs/DECISIONS.md Q-157; nguyên văn phương án và lời duyệt tại LOG.md Phiên 1. Những chữ CANDIDATE/chưa duyệt trong bản phương án lưu là trạng thái trước lời duyệt.

## Mục tiêu

Thiết kế và cài hợp đồng chung cho nguồn kiến trúc/cấu hình/code, bộ dựng đồ thị từ bản ghi quan hệ có nguồn và bộ đối chiếu với trace T-035. Phục vụ DT18-NV2 (docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2–3), bước 1 của cô (docs/reference/sources/advisor-2026-09-23.md §1), MRP P5 và đầu vào RQ3/RQ5. Lý do là mô hình hóa đúng quan hệ và nhu cầu kỹ thuật, chưa phải bằng chứng sửa được một hạn chế RCA.

Giữ lựa chọn “thực thể đầy đủ; thao tác khi có bằng chứng”. Chủ động khảo sát yêu cầu thao tác từ nguồn, không chỉ từ những gì trace TT/OB có. T-036 cung cấp hợp đồng và công cụ chung; T-037 làm đầy đủ FlashTicket, T-038 Train Ticket, T-039 Online Boutique, T-040 tổng hợp. Các task sau cần SPEC riêng; việc chia không xóa nghĩa vụ P5b.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn yêu cầu | Lựa chọn/giải thích khác | Phép kiểm và bằng chứng | Hỗ trợ, bác bỏ hoặc chưa phân xử | Phần thiếu và quyết định phụ thuộc |
|---|---|---|---|---|
| Quan hệ thiết kế và quan sát khác nhau thế nào? DT18-NV2, MRP P5 | Tách nguồn, revision và trạng thái bằng chứng; không xem kiến trúc là runtime ground truth | Bản ghi nguồn → chuẩn hóa → graph → truy ngược; fixture có cùng quan hệ nhưng nguồn khác | Hỗ trợ nếu truy được nguồn và không tạo số sự kiện; bác bỏ nếu gộp mất trạng thái | Độ đầy đủ từng hệ do T-037–039 kiểm; runtime FT chờ P9b |
| Hợp đồng có giữ đủ quan hệ và địa chỉ? DT18, B12–B16 | Phân biệt entity/operation, database logic/instance, broker/queue và vai trò producer/consumer | Fixture HTTP, data, messaging, callback, công việc nền, tài nguyên dùng chung; đối chiếu T-035 | Phản ví dụ mất quan hệ/địa chỉ chặn phần hợp đồng phụ thuộc; thiếu tên runtime giữ OPEN | Cần đổi hợp đồng T-035 thì trình riêng, không tự sửa hoặc bỏ nhu cầu |
| So hai nguồn có diễn giải đúng không? MRP P5 | Khớp cấu trúc khác khớp kiểu; khác revision/alias/miền khác thiếu instrumentation | Oracle độc lập cho tập giao, phần riêng, loại trừ, mẫu số và mapping mơ hồ | Hỗ trợ nếu tập/mẫu số đúng, unknown không thành match; chưa xác minh revision chỉ cho mô tả có điều kiện | T-038/039 truy revision và phân xử chênh lệch thật |
| Bàn giao được gì cho nghiên cứu và hệ thống? MRP P6/P9 | Khả năng biểu diễn khác telemetry thật và lợi ích RCA | Hợp đồng ghi nơi đặt tín hiệu, phép tính so sánh dùng cạnh và thông tin cần cho task sau | Đạt khi có đầu vào cụ thể, không chỉ hình vẽ; chưa chọn thuật toán/tín hiệu/mức đồ thị | T-040 tổng hợp; P6 chọn phương pháp; P9a/P9b kiểm thu thập/chuẩn hóa |

## Đầu vào

- AGENTS.md, docs/STATE.md, docs/MRP.md (RQ3/RQ5, P5/P6/P9, G3), docs/LESSONS.md; quyết định/lý do trực tiếp liên quan trong docs/DECISIONS.md và docs/WHY.md; nguồn đề tài ở trên; tasks/_MAU/SPEC.md, docs/review-prompt.md.
- tasks/T-035-p5-do-thi-tu-trace/SPEC.md và mục LOG hiện hành; results/T-035/manifest.json, dac-ta-do-thi.md, thong-tin-theo-quan-he.md; src/do_thi/README.md và code thực tế. Graph dev chỉ lấy theo manifest/allowlist T-035. Kiểm hash trước sử dụng; lệch thì dừng phần phụ thuộc. Không suy từ việc dùng đầu vào rằng T-035 đã nghiệm thu.
- Nguồn công khai đã lưu: results/T-002/handoff-manifest.json; results/T-003/runs/final-review-003/artifact-manifest.json và nguồn TT/Nezha tương ứng được chúng liệt kê. Chỉ dùng nguồn đã kiểm hash; không dùng thẻ cũ lệch manifest.
- Repo hệ thống chỉ đọc D:/Project/flash-ticket-platform: đọc AGENTS.md và skill bắt buộc trước khi dùng; docs/architecture/B11-C-target-architecture.md, B12-data-ownership-and-schema.md, B13-api-and-event-contracts.md, B14-main-flow-sequences.md, B16-observability-baseline.md. Ghim revision và hash nội dung thực đọc; ghi dirty nếu khác revision, không gọi HEAD là hash của file đã sửa.
- FlashTicket mới chưa có code ứng dụng theo xác nhận Minh. Thiết kế là nguồn thiết kế, không lấy code cũ làm bằng chứng bản mới đã chạy. Revision dataset/code RCA/ứng dụng sinh dữ liệu phải phân biệt.
- Môi trường laptop Windows, Python theo src/do_thi/README.md; dùng chế độ không ghi bytecode ra ngoài phạm vi. Chỉ fixture và graph dev đã lưu, không mở trace thô/test/dataset khóa hoặc repo RCA lưu trữ.

## Đầu ra

Trong results/T-036/:
- hop-dong.md: mô hình bản ghi nguồn, inventory, quan hệ, thao tác, alias, phạm vi so sánh, khóa cấu trúc, nơi đặt tín hiệu và xử lý thiếu/mâu thuẫn; khả năng tương thích với T-035.
- nguon.json: danh mục nguồn đầu vào cho ba nhánh, revision/hash/vị trí đọc, loại nguồn, mức xác minh liên hệ dataset, điều kiện áp dụng và OPEN. Đây là registry ban đầu, không thay khảo sát toàn hệ của task sau.
- fixtures/: đầu vào cùng đáp án độc lập, chỉ rõ nhu cầu nguồn được kiểm. runs/: lệnh, môi trường, đầu vào/trung gian/đầu ra, thời gian, kết quả kiểm và mọi lượt lỗi. kiem-dung-dan.md: báo cáo có con trỏ tới kết quả; manifest.json: nguồn và đầu ra/hash.
- ban-giao.md: phần hợp đồng đã kiểm, phần thiếu, owner/đầu vào cần/đường xử lý và ảnh hưởng T-037–040/P6/P9.

Mã dùng chung: src/do_thi_tinh/__init__.py, build.py, compare.py, README.md. Bộ dựng đọc bản ghi có dẫn nguồn do người đọc lập; không là bộ phân tích tĩnh tổng quát mọi ngôn ngữ.

### Nội dung hợp đồng phải giữ

1. Inventory thực thể đầy đủ tách khỏi nút được quan sát và tập ứng viên RCA. Operation có bằng chứng, giữ owner và tên gốc; tên thao tác thiết kế không tự là operationName runtime. Không tạo operation giả để đủ phép chiếu. Producer/consumer là vai trò, không mặc nhiên là nút thao tác.
2. Mỗi nút/cạnh/bản ghi có nguồn, phiên bản, vị trí, điều kiện. Tách bốn chiều: biểu diễn được; bằng chứng thiết kế/code; quan sát runtime; bằng chứng lợi ích RCA. Không bịa event_count từ số lần tài liệu nhắc tới.
3. Hỗ trợ yêu cầu HTTP/RPC, data/cache, phát–broker–nhận, outbox/inbox, retry/redelivery/dedup, callback, scheduler/background jobs, Saga/bù trừ, thao tác nghiệp vụ/quan sát và thành phần hỗ trợ đã có nguồn. T-036 dùng ví dụ đại diện kiểm hợp đồng; bảng bao phủ đầy đủ từng yêu cầu FT thuộc T-037.
4. Database logic/ownership khác instance tài nguyên dùng chung; không gộp mất DB hoặc tạo nhiều instance độc lập giả. Giữ địa chỉ log/trace/metric và mapping tài nguyên; không nhân metric service thành bằng chứng độc lập mỗi operation. Thiếu biểu diễn trong T-035 thì ghi phản ví dụ/thông tin mất/phương án bổ sung, trình Minh trước sửa nguồn chung.
5. Giữ nguyên graph trace T-035. Phép chiếu giữ ngoại lệ của mô hình đó, kể cả span-parent không thành cạnh phụ thuộc thực thể. Nguồn tĩnh có graph riêng; không bổ sung cạnh để làm tăng quan sát.
6. Alias cần nguồn, scope và tên gốc; mơ hồ giữ riêng, không chọn theo độ khớp. So theo hệ/revision/loại quan hệ/mức/ca/cửa sổ hiện có; Nezha toàn miền vẫn là miền dev adapter, không thành cả ngày.
7. Báo S, T đủ điều kiện, giao, phần riêng hai phía, chưa ánh xạ/chưa rõ kiểu/ngoài miền với lý do. Báo |S∩T|/|S| và |S∩T|/|T|; mẫu số rỗng N/A. Không gọi là precision/recall với ground truth hoàn chỉnh. Tách so đầu mút và so kiểu; unknown không được nâng thành sync.
8. Messaging giữ broker/scope, địa chỉ phát exchange/routing, địa chỉ nhận queue, điều kiện nối message của T-035. Không ép exchange=queue, không mất nhiều queue cùng consumer, không tự coi địa chỉ thiếu là match. Giữ provenance riêng với khóa đối chiếu cấu trúc. Operation chỉ đối chiếu khi mapping xác minh được.
9. Revision chưa nối được dataset phải ghi điều kiện ngay trong kết quả; khác biệt không tự là thiếu instrumentation. Registry/đầu ra giữ các giải thích cạnh tranh: revision, alias, miền/cửa sổ, nhánh chưa chạy, nguồn tĩnh thiếu, telemetry thiếu, lỗi chuyển đổi. Metadata Nezha mức ngày chỉ mô tả theo quyền hiện hành, không dùng chọn P6.
10. Builder/comparator không nhận nhãn gốc, loại lỗi, tên ca/đường dẫn suy nhãn để chọn quan hệ. Metadata điều phối báo cáo tách khỏi đầu vào phương pháp. Không suy quan hệ thực thi từ cùng correlation hoặc cùng broker.

## Phạm vi ghi

Sau tự soát không phát hiện vấn đề cần sửa SPEC, người làm được ghi:
- results/T-036/ (gồm fixture, script kiểm, runs và manifest; giữ mọi lượt).
- src/do_thi_tinh/__init__.py, src/do_thi_tinh/build.py, src/do_thi_tinh/compare.py, src/do_thi_tinh/README.md.
- Nối tasks/T-036-p5b-hop-dong-chung/LOG.md và cập nhật đúng dòng T-036 trong docs/STATE.md.

SPEC khóa sau khi ghi theo lời duyệt. Không tự sửa SPEC, WHY/DECISIONS, nguồn T-035, platform hoặc file task khác khi triển khai. Quyền ghi tài liệu duyệt trong phiên chuẩn bị không kéo dài thành quyền sửa chúng tùy ý. Cần thay thì trình Minh.

## Các bước

1. Phiên Codex sạch đọc nguồn và tự soát SPEC như lần đầu trước khi đọc kết luận lịch sử. Kiểm quyền ghi, trạng thái phụ thuộc và hash đầu vào. Ghi nhận xét độc lập trong LOG. Có vấn đề cần sửa SPEC: nêu bằng chứng, ảnh hưởng, sửa tối thiểu theo file, dừng triển khai và chờ Minh duyệt; không tự sửa rồi làm tiếp. Không có vấn đề: báo kết luận và tiếp tục trong quyền đã có.
2. Lập registry và hợp đồng bằng nguồn; đối chiếu T-035, B12–B16 và yêu cầu cả ba hệ. Nêu phương án khác/điều kiện thất bại. Nếu phát hiện lựa chọn quan trọng chưa có căn cứ/WHY được duyệt thì trình phần cần bổ sung trước khi dùng vào kết quả.
3. Viết fixture và đáp án độc lập trước cài bộ dựng/đối chiếu; dùng ví dụ quan hệ thực có nguồn và trường hợp tổng hợp ghi rõ. Xác định trung gian cần lưu để phân biệt lỗi mapping, dựng và so sánh.
4. Cài bộ dựng và comparator, kiểm từ bản ghi → ID/kiểu/địa chỉ → cạnh/chiếu → tập/mẫu số. Kiểm tương thích định dạng graph dev T-035 sau xác minh manifest; không làm thay toàn bộ đối chiếu TT/OB.
5. Kiểm các trường hợp dưới đây và chạy lại tính xác định. Lỗi thì giữ lượt lỗi; sửa trong phạm vi triển khai, không đổi tiêu chí/spec để đạt. Nếu cần vượt phạm vi, dừng phần phụ thuộc và trình bổ sung.
6. Tổng hợp bằng chứng, phần còn OPEN và bàn giao cho T-037–040. Soát toàn diff, phạm vi ghi, manifest, tính nhất quán kết luận. LOG cuối phiên đủ lệnh/bước tiếp; dòng T-036 chờ phản biện. Soạn prompt Claude theo mẫu, không tự gửi/đóng task.

## Kiểm đúng đắn

- Oracle ghi độc lập các tập ID/cạnh/địa chỉ và kết quả so sánh; không dùng chính hàm đang kiểm để sinh đáp án.
- Fixture alias mơ hồ; cùng đầu mút khác kiểu; nhiều queue cùng consumer; fan-out; retry/republish; callback trace mới; scheduler không caller; database logic chung instance; miền/cửa sổ rỗng.
- Kiểm provenance đầy đủ; unknown/thiếu địa chỉ không thành match; số dòng tài liệu không thành số sự kiện; đúng điều kiện chiếu và không làm mất ngữ nghĩa dữ liệu/messaging.
- Tập giao/phần riêng/ngoài miền có danh sách kiểm độc lập và mẫu số khớp. Không đánh đồng nhiều nguồn cùng quan hệ với nhiều sự kiện hoặc nhiều cạnh cấu trúc.
- Đảo thứ tự bản ghi/chạy lại cho kết quả xác định; lỗi đầu vào phải có chẩn đoán rõ, không chọn tùy thứ tự.
- Kiểm API không lấy nhãn làm đầu vào; báo cáo tách khỏi chọn quan hệ. Đối chiếu đầu vào thật đã xác minh với hợp đồng T-035, lưu lệnh và kết quả.
- Chưa có số công bố phù hợp cho công cụ chuyển bản ghi này: kiểm bằng oracle và bằng chứng nguồn, không bịa baseline. Đây không là thí nghiệm lợi ích RCA; đối chứng bỏ cạnh/đồ thị ngẫu nhiên thuộc đánh giá thiết kế sau.

## Tiêu chí xong

1. Hợp đồng, registry ba nhánh và công cụ cho phép truy từng quan hệ về nguồn; phân biệt thiết kế, code, runtime và lợi ích.
2. Fixture có đáp án độc lập kiểm các nhu cầu đã nêu và đạt; trung gian chỉ ra lỗi nằm bước nào. Không chỉ kiểm chạy không lỗi.
3. Quy tắc miền/alias/kiểu/địa chỉ/tập/mẫu số thể hiện bằng đầu ra kiểm được, không sửa graph trace. Tính xác định và tương thích được kiểm.
4. Nhu cầu chưa biểu diễn được phải có phản ví dụ, giải thích cạnh tranh, phần sửa/thu thêm và quyết định phụ thuộc. Lỗi chặn hợp đồng chưa xử lý không được gọi đạt công cụ chung; OPEN về runtime/revision chưa có vẫn có thể bàn giao đúng giới hạn.
5. Bàn giao đủ để soạn T-037–039 và tổng hợp T-040; ghi rõ chưa có inventory/đối chiếu đầy đủ ba hệ. Chưa đóng P5/RQ3/RQ5/G3, chưa chọn P6, chưa khẳng định runtime FT hoặc lợi ích RCA.
6. Manifest, tự kiểm, LOG và prompt bàn giao đủ; Minh quyết nghiệm thu sau phản biện.

## Không làm

Không triển khai T-037–040 trong task này: khảo sát toàn hệ, truy revision ứng dụng và phân tích chênh lệch thật là nghĩa vụ các task đó. Không dùng thiếu nguồn để loại nhóm quan trọng.

Không sửa kiến trúc/nghiệp vụ FlashTicket; không triển khai hệ thống/collector. P9a nhận yêu cầu trường/khóa và nơi phải ghi; P9b cung cấp trace chuẩn hóa và metadata build/deployment/sampling/drop/clock. So runtime FT phải có SPEC sau, gồm các đường nghiệp vụ/async/phục hồi đã thiết kế.

Không chọn phương pháp/tín hiệu/mức đồ thị P6; không chạy baseline, đọc lại trace thô, mở test/heldout, tải repo/dataset, bật EC2, commit/push hoặc tạo/gửi chat tự động. Tải TT/OB phải có đề xuất riêng về nguồn, revision, file và dung lượng.

## Chi phí ước lượng

Ước lượng chưa đo: T-036 2–4 giờ công; toàn P5b 15–24 giờ công chưa gồm phản biện/chờ nguồn. Dùng laptop và graph đã lưu, không cần dự trù EC2/GPU cho bước này. Không tải mới. Thời gian/RAM chạy phải đo khi triển khai, không coi giờ công là giờ tính toán hay mặc nhiên miễn ngân sách Q-40. Nếu dự kiến một lượt >1 giờ hoặc thao tác tốn kém khác, báo Minh trước theo AGENTS. Không tự dùng subagent.

Hợp đồng làm trước; T-037/038/039 có thể khảo sát độc lập sau đó, chỉnh hợp đồng chung và tổng hợp tuần tự. Nếu thấy không vừa một phiên thì trình tách/checkpoint đúng luật, không giảm độ sâu cho vừa giờ.

## Rủi ro và điều chưa chắc

- Chưa kiểm: T-035 đủ biểu diễn mọi nhu cầu chung. Phản ví dụ tài nguyên dùng chung hoặc bất đồng địa chỉ có thể bác bỏ; fixture và đọc nguồn phải phân xử trong task. Không coi lời duyệt là xác minh đúng mô hình.
- Revision TT/OB sinh dataset còn OPEN; registry giữ thiếu bằng chứng/owner cung cấp, T-038/039 truy nguồn. Không thể quy telemetry thiếu chỉ từ chênh đồ thị.
- FT mới chưa có code ứng dụng: thiết kế không chứng minh nhánh đã chạy. T-037 bao phủ thiết kế, P9/runtime cung cấp dữ liệu; collector không phục hồi thông tin chưa ghi.
- T-035 còn chờ tự soát/phản biện; ghim đúng đầu vào và kiểm thay đổi trước triển khai. Không tự nghiệm thu phụ thuộc hoặc âm thầm đổi schema.

## Prompt bàn giao

Prompt phiên Codex sạch triển khai sau tự soát và prompt Claude soát SPEC theo nguyên văn mẫu được lưu trong LOG.md Phiên 1. Đây là hai vai trò khác nhau. Minh chuyển thủ công. Sau triển khai phải soạn prompt soát kết quả theo mẫu hiện hành.

## Phụ lục V2: đối chiếu SMTP và tiếp nhận phiên bản chung (Minh duyệt Q-164 ngày16/10/2026)

Giữ pin/ngoại lệ/đầu ra lịch sử trong nội dung cũ. T037 đã hỗ trợ SMTP theo delta được duyệt; T039 đã có132graph dùng snapshot gốc. Gói V2 đổi comparator (optional call channel và marker SMTP cả endpoints/typed) và chuyển cả ba nhánh sang manifest results/T-036/runs/doi-chieu-smtp-001/manifest.json sau hồi quy đầy đủ. Builder giữ nguyên byte T037. Quyền ghi đúng plan.json V2 đã duyệt; hồi quy T036/R1/SMTP, full model/fixture T037,1069TT,132OB và so tập/members/exclusions/mẫu số/input/hash/ordering phải đạt, tách comparator khỏi delta TT. Giữ script/output/pin cũ; runner mới kiểm manifest+snapshot/live tường minh. Các bản hiện hành chỉ chuyển sau cả ba PASS. created_utc/SHA manifest mới lấy từ file thực đã kiểm, hiện OPEN. Nguyên lời Minh duyệt tại Q-164 và authorization.json; không suy nghiệm thu task/G3/test/commit.

### Tiếp nhận V2 đã kiểm — 16/10/2026

Phụ lục V2 ở trên đã được triển khai theo Q-164. Manifest chung: results/T-036/runs/doi-chieu-smtp-001/manifest.json; created_utc thực: 2026-10-16T04:22:36.861568+00:00. Đường dẫn/SHA/created_utc và module hashes chính xác nằm pin.json của cả T037/T038/T039 trong runs/doi-chieu-smtp-001/. Loader kiểm các giá trị này trước import. Cả ba đã đạt toàn hồi quy trước đổi bản hiện hành; kết quả cũ vẫn dùng pin đã sinh chúng. Các chữ OPEN/pending của phụ lục trước là mốc trước kiểm, metadata hiện hành theo pin.json và bàn giao, không suy nghiệm thu task/G3/test/commit.
