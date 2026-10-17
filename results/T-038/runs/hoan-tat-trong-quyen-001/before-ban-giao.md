# Bàn giao T-038 cho Minh và Claude

Đạt một phần, chờ phản biện kết quả; chưa đề nghị nghiệm thu đầy đủ. Minh yêu cầu không tách và đã duyệt gói tải; đã làm trong cùng phiên, không tạo task/SPEC mới. Full dev comparison đã xong trên bản nguồn có điều kiện. Các tiêu chí còn phụ thuộc SMTP/coverage/lineage được nêu cụ thể, không biến thiếu nguồn thành thu hẹp mục tiêu.

Điểm vào: `bao-phu-nguon.md/json` (toàn cây, lineage, phần OPEN), `nguon.json` (registry), `ban-ghi.json`, `inventory-index.json`, `mapping.json`, `mapping-summary.json`, `do-thi/`, `doi-chieu/index.json`, `phan-tich-chenh-lech.md/json`, `kiem-dung-dan.md`, `kha-thi.json`, `manifest.json`. Bản chụp assembly cuối là runs/lap-ban-ghi-005; comparer cuối là runs/doi-chieu-dev-002; giữ mọi lượt trước. Hash/revision tập trung ở manifests và registry.

| Bên nhận | Thông tin cung cấp được | Phần thiếu/điều kiện và phép phân xử |
|---|---|---|
| T-040 | Inventory/operations và quan hệ có provenance; toàn graph/cửa sổ, tập/members/exclusions, nhóm chênh lệch source→key→set | Không cộng các cờ thành tỷ lệ nguyên nhân; tổng hợp ba nhánh phải cùng pin, giữ revision conditional; chưa đủ inventory ngữ nghĩa |
| P6, RQ3/RQ5 | Entity/operation khác địa chỉ, data/broker/worker/shared signals, cấu trúc nguồn ngoài trace; đồ thị đã có vai trò tính toán tập | Chưa chọn mức/thuật toán/tín hiệu; cần bằng chứng dev cho thiết kế và đối chứng tương đương, chưa có lợi ích RCA từ phép giao |
| P9 FlashTicket | Cần owner/component ID ổn định; endpoint method+route và client callsite; kind/transport; logical DB và physical instance riêng; broker namespace/exchange/routing/queue; trace/span correlation cho log và địa chỉ scrape/resource của metric | Đây là yêu cầu quan sát rút ra từ thiếu địa chỉ hiện có, không chứng minh collector sửa được lịch sử. Cần kiểm schema/runtime FT với baseline quan sát trong task được duyệt; không sửa FT ở đây |
| Chủ dữ liệu qua Minh | App commit/image digest/build metadata; instrumentation version/config; deployment manifest/env/namespace/time scope; workload và schema capture | Dùng để phân xử revision, alias, nhánh/workload, telemetry và conversion; chưa có thì quan hệ nguồn chỉ tham khảo |

SMTP relation dừng riêng vì T036 không biểu diễn được, external entity còn trong inventory; phản ví dụ ở fixtures/smtp-counterexample.json. Không fork nghĩa chung cho TT. 27 blob OPEN và nguồn ngoài chưa được phép lấy có danh sách/input/owner/ước tính ở coverage và de-nghi-tiep-theo.md. Không cần chạy lại graph chỉ để làm đẹp coverage; phép bổ sung phải giải quyết đúng câu hỏi còn thiếu.

Sự cố đọc telemetry mẫu công khai của nhánh hỗ trợ đã được báo ngay và ghi trong LOG/coverage incident. Đã giữ bản lỗi, không dùng cho facts/model/mapping/kết luận; không có RE2 raw/test/heldout/data khóa được mở. Reviewer cần kiểm phạm vi phụ thuộc từ artifacts thực, không dựa lời khẳng định của người làm.

Tiếp theo chính xác: Minh chuyển `prompt-claude.txt` cho Claude để soát kết quả. Chưa có quyền ghi REVIEW thì Claude chỉ đọc/trả lời chat; Minh quyết phạm vi review riêng. Root không tự gửi. Minh quyết hướng xử lý phần thiếu sau xem đề xuất cụ thể. Không commit/push nếu chưa được yêu cầu. Commit đề nghị sau duyệt: `T-038: khảo sát nguồn Train Ticket và đối chiếu dev có điều kiện` (chỉ file T038/LOG và dòng STATE hợp lệ).
