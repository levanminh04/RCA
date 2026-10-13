# T-033 — Checkpoint phiên 5

Chốt 2026-10-11T07:31:57.851917+07:00. Codex người làm, Claude phản biện. Task/chặng tính chưa hoàn tất; không có run nghiên cứu mới. Dừng cấp giờ vì ledger chưa đủ, theo yêu cầu Minh về thời gian không tái dựng.

- Laptop825 và raw EC2 89 file hash/byte PASS. Đã xóa duy nhất archive được duyệt, byte trước/sau và SHA tại `../session5-open-001/archive-deletion-001.json`.
- Key trace summary status_code đã sửa tối thiểu. Hai time guard cộng dồn đã stage và hash hai đầu; kiểm EC2 từ chối ledger thiếu đạt. AST ngoài guard/key giữ nguyên; bản cũ trong `../session5-open-001/scripts/`. Đường guard hợp lệ/fixture/pilot còn chưa kiểm.
- `../session5-budget-001/ledger.json`: từng khoảng marker/timer, phần thiếu và owner. Khoảng marker không là tổng đủ hoặc upper bound mọi process. `remaining_approved_s` null. `ledger-delta.json`: timer mới sau ledger pin, cần hạch toán trước run sau.
- `remote-status.json`: không worker/tmux, archive không còn, byte/disk mới. Laptop có thể tắt trong lúc chờ; EC2 còn cần cho phần tính, agent không bật/tắt máy. Không gọi lượt mới ổn định.
- `checkpoint.json` và `prompt-next-session.md`: phần đã/chưa làm, nguồn/file/lệnh/phạm vi. Đây là nối chặng tính, chưa chuyển đọc tay+tổng hợp hay Claude review chính thức.
- `scope-verification.json`: LOG chỉ nối, STATE chỉ T-033, tài liệu nguồn giữ nguyên. Manifest khóa các file checkpoint này.

Cần Minh quyết cách hạch toán các đoạn xử lý không tái dựng hoặc bổ sung timing. Không tự đặt reserve, đánh dấu ledger đầy đủ hoặc cấp `12 − subtotal` giờ.
