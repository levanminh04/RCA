# Bàn giao T-037 — tiếp nhận SMTP V2

Minh duyệt triển khai gói theo Q-164 ngày16/10/2026; code/pin chung đã tiếp nhận sau đủ kiểm ba nhánh. Chờ Claude phản biện kết quả; chưa tự nghiệm thu.

1598/1598 kiểm full model/fixture; graph/binding/signal/nguồn giữ nguyên. Unknown SMTP + trace thiếu channel đổi endpoint numerator1→0 đúng oracle trước chạy.

Pin hiện hành là pin.json trong runs/doi-chieu-smtp-001/, manifest chung results/T-036/runs/doi-chieu-smtp-001/manifest.json. Loader kiểm exact path/SHA/created_utc và code live+snapshot; không HEAD/fallback R1. Mọi kết quả cũ, script/oracle/snapshot lịch sử giữ nguyên. Root report/model/index được giữ byte trước ở before/; không gán pin mới cho output cũ. Kế hoạch V2 ban đầu và các báo cáo “chờ duyệt” trước lượt này là tài liệu lịch sử; trạng thái hiện hành theo manifest và bàn giao này.

Runtime/build/instrumentation/deployment lineage, authority/port/TLS/delivery và các OPEN nguồn giữ nguyên. Chưa xác nhận lợi ích RCA/RQ3/RQ5, chọn P6, nghiệm thu task hoặc mở G3/test.

Bằng chứng: checks/ trong run, diff.json và manifest; báo cáo chung tại results/T-036/runs/doi-chieu-smtp-001/ban-giao.md. Chi phí thực theo cost.json trong run; không là benchmark cô lập, không suy từ thời gian tổng thành giờ công. Không tải nguồn/SMTP thật/test/heldout/commit/push. T040/P6/P9 nhận thêm semantics protocol đã ghi; telemetry channel cần nguồn riêng, không suy từ static.

Bước tiếp: Minh chuyển prompt-claude.txt để Claude soát độc lập nếu muốn. Không tự gửi; chỉ Minh nghiệm thu/đóng task.
