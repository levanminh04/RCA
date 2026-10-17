# Bổ sung SMTP cho hợp đồng nguồn tĩnh — 16/10/2026

Minh duyệt sửa hỗ trợ SMTP và kiểm lại, rồi tiếp tục T-037; giữ nguyên T-038/T-039 và pin của hai nhánh đó. Nguyên văn tại LOG T-037 Phiên 3 và runs/tiep-smtp-001/authorization.txt. Đây là bổ sung biểu diễn kỹ thuật theo nhu cầu đã có trong B13 §6/B14 §6, cùng căn cứ WHY-52/53; không chọn phương pháp P6 hoặc sửa thiết kế hệ thống.

Hợp đồng nền vẫn là `results/T-036/hop-dong.md` theo snapshot `runs/kiem-r1-after-002`. Bổ sung duy nhất: channel `smtp` hợp lệ cho quan hệ `gọi-đồng-bộ` và `gọi-chưa-phân-kiểu`. Các type/channel khác không đổi. Schema, ID, provenance, resource binding, signals, messaging và phép chiếu không đổi. `smtp` không hợp lệ cho dữ-liệu, triển-khai, span-parent hoặc thông-điệp; không tạo broker giả để gửi email.

Kênh SMTP cho biết giao thức được nguồn thiết kế nêu. Nó không xác nhận loại span hoặc quan hệ đồng bộ runtime. T-037 dùng `gọi-chưa-phân-kiểu` cho Ticket→SMTP vì nguồn chỉ xác nhận gửi SMTP ngoài transaction, chưa có quan sát span. Hai type trong fixture bổ sung kiểm phạm vi hỗ trợ của bộ dựng, không là kết luận rằng SMTP luôn đồng bộ.

`compare` giữ hành vi nền: non-messaging so đầu mút và type, chưa xác minh channel/transport. Một cạnh SMTP có thể khớp đầu mút với HTTP; khi đó chỉ được nói khớp cấu trúc, không được nói khớp giao thức. Type gọi-chưa-phân-kiểu bị loại khỏi phép so typed, giữ trong endpoints. Mỗi member vẫn giữ channel nguồn; graph trace không có transport không được điền SMTP từ thiết kế.

T-037 ghi snapshot riêng của mã chung sau sửa và cả hash pin nền trong manifest; không cập nhật manifest/snapshot của T-036 hoặc pin trong SPEC T-038/T-039. Đây là một bổ sung đã được duyệt của cùng hợp đồng chung, không fork nghĩa cạnh. Hai nhánh còn lại tiếp tục dùng snapshot nền; việc tổng hợp khác phiên bản phải xét delta SMTP và bằng chứng hồi quy, không tự chuyển pin.

Điều kiện thất bại: source protocol/owner bị dẫn sai; SMTP bị ép thành http/rpc/internal; fixture không giữ channel qua graph/chiếu; kết quả cũ thay đổi. Khi đó dừng phần phụ thuộc. Metric dùng chung vẫn một địa chỉ với operation=null; delivery attempt/retry không làm tăng số cạnh hay tạo operation runtime. Kết quả kiểm sẽ ở runs/smtp-regression-*/; tài liệu này được viết trước sửa mã.
