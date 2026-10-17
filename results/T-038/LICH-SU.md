# Chọn đúng đầu ra hiện hành

Nguồn hiện hành là manifest.json, doi-chieu/index.json, ban-giao.md và `results/T-038/runs/sua-r1-20261017-001/ban-giao-T040.json`. Model `results/T-038/runs/sua-r1-20261017-001/model` khớp graph canonical do-thi/; so sánh `results/T-038/runs/sua-r1-20261017-001/checks/full1069-002`. Bản SMTP V2 ở runs/doi-chieu-smtp-001 và candidate reviewer giữ nguyên lịch sử, không còn là selector hiện hành. Pin chung vẫn SMTP V2.

before/ trong run sửa giữ nguyên byte mọi root được thay và LOG/REVIEW/STATE trước lượt. Các run/lượt lỗi cũ không sửa/xóa. Các script root ghi report/model trước đây đã được chặn chạy; runner hiện hành ở ban-giao.md và commands.json. Nguồn tải/metadata/tool tải là lịch sử; không chạy để tái lập gói sửa.

SPEC giữ mốc lịch sử; quyền thực hiện theo authorization.txt và LOG. Codex là người làm, reviewer kết quả là Codex phiên độc lập do Minh chỉ định trong REVIEW.md; không đổi phân công lịch sử. Task chưa nghiệm thu.

Giữ hạn chế đọc lịch sử: ba index coverage/content/archive ban đầu đã cách ly do telemetry mẫu, chỉ hash, không parse. Chỉ dùng bản clean và followup có phạm vi đã kiểm. Không mở mẫu/raw/test/heldout/archive hoặc body PDF; xem metadata incident trong báo cáo coverage.
