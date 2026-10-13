# T-033 — Ledger thời gian xử lý, phiên 5

Ledger INCOMPLETE. Đã kiểm endpoint birth/mtime trực tiếp trên EC2 và đọc code đặt marker. Khoảng marker bao phần có bằng chứng, không phải đo đủ process hay upper bound các đoạn thiếu. Không lấy thời gian lịch/khoảng nghỉ và không cộng lồng unit/pilot tái dùng.

`ledger.json` giữ từng lượt, endpoint, số giây và phần không tái dựng. `remaining_approved_s` để null: chưa được cấp giờ mới. Hash/source/time mới ở `../session5-open-001/timing-source-verification-001.json`. Một timer do trợ lý báo được tách riêng, không thay xác minh người làm.

Cần Minh quyết cách hạch toán phần không tái dựng, hoặc cung cấp bằng chứng thời gian còn thiếu; không tự đặt khoản dự phòng hay coi subtotal là tổng đủ. Guard mới phải từ chối khi ledger chưa hợp lệ. Chưa có pilot mới.
