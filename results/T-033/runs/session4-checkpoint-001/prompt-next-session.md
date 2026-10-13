Đọc AGENTS.md, tiếp T-033 trong STATE. Codex là người làm, Claude là người phản biện. Phiên mới chỉ dùng repo; ghi dòng mở phiên vào LOG.

Đọc toàn SPEC T-033, LOG phiên 3 và phiên 4; checkpoint-handoff-001/README.md, snapshot.json, artifact-locator.json, output-presence.json; session4-checkpoint-001/README.md, checkpoint.json, integrity-verification.json, remote-status.json, script-reading-evidence.json, script-reading-notes.md. Đọc MRP RQ2/P4, DT18 NV2/NV3, advisor §1, LESSONS và WHY-41 trước diễn giải.

Phiên 4 dừng do ngữ cảnh bị nén theo AGENTS §5a.2. Không có lượt nghiên cứu mới. Script độ trễ/kênh chưa chạy, guard chưa sửa, archive EC2 chưa xóa, ledger tổng giờ chưa tính, khóa nhóm mới chưa cập nhật. Các báo cáo trợ lý là tự soát chỉ đọc; không thay kiểm độc lập của người làm hay phản biện Claude.

Minh cung cấp hai lời duyệt ngày 10/10/2026 trong phiên 4; nguyên văn ở LOG và checkpoint.json:
1. DUYỆT: ngân sách thời gian tính bằng tổng giờ xử lý cộng dồn của các lượt, gồm lượt hỏng và lượt kiểm, trần 12 giờ; bỏ mốc lịch 11:46 ngày 10/10. Chỉ sửa đúng phần guard trong script; giữ bản cũ; kiểm hash hai đầu; ghi cách tính và số giờ đã dùng vào LOG trước khi khởi lượt mới.
2. DUYỆT: xóa đúng một file ~/rca/T-033/runs/checkpoint-handoff-001/artifacts.tar trên EC2, sau khi tự kiểm lại bản laptop khớp artifact-inventory.json. Trần 4 GiB tính trên đầu ra tại EC2. Không xóa gì khác. Ghi dung lượng trước và sau vào LOG.
Hai lời duyệt này không mở rộng sang việc khác. Chưa có quyền ghi docs/DECISIONS.md để lưu hai lời duyệt; kiểm Minh đã trả lời đề xuất lưu ở cuối LOG hay chưa. Nếu chưa, tiếp việc đã được duyệt và giữ phần ghi DECISIONS chờ duyệt; không tự ghi.

Việc còn phải hoàn tất của chặng tính EC2:
- Kiểm process/hash/source mới, không khởi trùng. Lời duyệt guard đã có hiệu lực; lập ledger tổng wall xử lý các lượt (kể cả hỏng và kiểm), không lấy thời gian lịch/chỉ subtotal có status làm ngân sách đủ. Nếu thiếu thời gian không tái dựng được, nêu đúng phần thiếu/ảnh hưởng trước cấp giờ mới.
- Tự kiểm lại bản laptop trước xóa đúng archive được duyệt, ghi byte EC2 trước/sau. Không xóa gì khác.
- Đọc và tự kiểm đủ nsigma_delay.py, bocpd_delay.py, channel_context.py theo SPEC/native. Lỗi dict status lặp ở channel_context.py đã được người làm xác nhận trong script-reading-evidence.json; sửa tối thiểu key statusCode thành status_code, giữ bản cũ/kiểm hai đầu. Các nhận xét khác cần tự xác nhận trước sửa. Không thay tham số/tiêu chí/SPEC.
- Mỗi script chạy ca đầu trên EC2 trong lượt mới, fixture/intermediates/source/time/flags/CP/schema và time/RAM/bytes đạt mới chạy rest; tái dùng đơn vị PASS qua nguồn hash, không chạy lại. Lượt dài tmux/nohup độc lập laptop/SSH, progress/stdout/stderr/PID/status/lệnh xem LOG, tự dừng khi lỗi.
- Cập nhật khóa nhóm/đối chứng theo quy tắc SPEC sau phân rã và trước diễn giải. Giữ bốn trạng thái input trùng, collapse hợp lệ, không có kênh, lỗi và mẫu số từng loại. Chưa viết kết luận cơ chế hay báo cáo tổng hợp trong chặng tính này; phần thiếu giữ OPEN với bằng chứng cần.

Phạm vi ghi đúng SPEC: results/T-033/, LOG chỉ nối, duy nhất dòng T-033 STATE (đọc ngay trước sửa), EC2 ~/rca/T-033/. Không ghi nguồn cũ, SPEC, DECISIONS/WHY ngoài lời duyệt cụ thể. Laptop chỉ điều khiển/tài liệu/nhận/kiểm hash, tính nghiên cứu EC2 pin; không cài package. Không test/locked/heldout, không results/T-032 hoặc ~/rca/T-032, không commit/push, không bật/tắt EC2.

Thiết kế không phân xử được/hash hoặc CP lệch/sắp vượt trần thì checkpoint, dừng phần phụ thuộc và trình Minh; không tự đổi cách làm. Ngữ cảnh nén thì checkpoint ngay, đề nghị phiên mới.

Báo CẦN GIỮ LAPTOP MỞ khi đang kiểm pilot, kèm lý do/thời gian ước lượng/mốc báo lại. Chỉ báo EC2 T-033 ĐÃ ỔN ĐỊNH — Minh có thể tắt laptop sau ca đầu kiểm đạt và đo đủ tài nguyên/ngân sách, lỗi tự dừng; kèm run/ước lượng xong/lệnh tiến độ/việc tiếp khi mở lại.

Cuối phiên LOG đủ AGENTS §7, last command/bước tiếp chính xác, STATE chỉ dòng T-033, trạng thái EC2/việc Minh cần làm. Khi phần tính đạt mới soạn prompt phiên tiếp đọc tay + tổng hợp. Prompt phản biện chính thức Claude chỉ soạn khi task hoàn tất theo nguyên văn Common + Soát kết quả + G2 trong docs/review-prompt.md; không tự gửi hay mở review.
