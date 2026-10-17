# Chọn đúng đầu ra hiện hành

Bàn giao hiện hành là `ban-giao.md`. Manifest cuối trỏ model `lap-ban-ghi-005`, so sánh `doi-chieu-dev-002` và bảng nguồn `bao-phu-nguon.json`. Hai lượt full đều giữ riêng. Bản đầu và bản cuối có toàn bộ SHA kết quả so sánh giống nhau; signal bổ sung không đổi phép tính cạnh.

`de-xuat-nguon-va-tach.md`, `tu-ra-spec.md`, các run preflight/metadata và `finalize.py` là lịch sử trước duyệt gói tải. Minh đã quyết không tách; phần đề nghị tách không được áp dụng. Không chạy lại `finalize.py`: nó dành cho thời điểm chưa tải và có phép parse đệ quy không phù hợp nguồn hiện nay. Kiểm cuối triển khai dùng `finalize_implementation.py`.

Các bản graph/model ở run002–004 và pilot/hỏng được giữ để kiểm diễn tiến, không cộng chúng vào số graph hiện hành. Nguồn Java, coverage và signal của nhánh hỗ trợ đều là công việc hỗ trợ người làm Codex, không phải phản biện chính thức. Claude vẫn là người phản biện kết quả.

Ba index đầu `runs/trien-khai-001/coverage/content-index.json`, `runs/trien-khai-001/coverage/coverage.json`, `runs/trien-khai-001/coverage/archive-structures.json` có ảnh hưởng sự cố telemetry mẫu. Chỉ hash chúng để giữ lịch sử; không đọc/parse lại hoặc dùng làm bằng chứng. Bản `*-clean.json`, `coverage-final.json` và các followup có phạm vi sạch riêng. Đọc metadata sự cố ở `runs/trien-khai-001/coverage/incident.json` trước khi dùng lịch sử; không mở thêm mẫu, workbook hoặc Jaeger screenshot.

`nguon.json` là registry tối giản theo API T036; chuỗi sáu trục và nguồn bằng chứng provenance ở `bao-phu-nguon.json#/lineage` cùng bản trước lưu trong `runs/trien-khai-001/before-nguon.json`. Nguồn ứng dụng tải không phải nguồn đã xác minh sinh dataset.
