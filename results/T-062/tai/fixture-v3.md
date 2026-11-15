# Fixture dùng cho C1 v3

`k6/fixtures.json` hiện hành giữ một event và một order ID. Nguồn: `fixture-read-003.txt`, `k6/fixture-evidence.json`. Order ID là khóa tra từ smoke receipt T-058; hash receipt khớp manifest (`kiem-hash-nguon.json`). Quyền buyer và tồn tại của đơn được kiểm lại bằng GET hiện tại trên AWS, không suy từ trạng thái cũ. Không có API liệt kê đơn trong OrderController; không truy vấn DB.

Đầu ra v2 `fixture.md`, `fixture-doc*.json`, `doc-fixture.py`, metadata PKCE obs và các container kiểm tra obs được giữ nguyên làm lịch sử. Chúng mô tả một lần chuẩn bị dự phòng với ba đơn; không phải fixture của lượt AWS v3. Không có tải k6 nào ở obs trong phần C1 v3 này.

Không tạo đơn mới vì đã có một đơn đọc được bằng buyer, đủ cho hỗn hợp bốn route đã duyệt. Payment trả 200, tickets trả 500 trước A2. Giữ đúng 10% tickets, không bỏ route để che lỗi. Sau A2, `doi-va-chay-thu.ps1` đăng nhập mới, xác minh lại qua API và lưu `fixture-sau-a2.txt`; chỉ khi không còn đơn nào đọc được mới cho phép tạo tối đa một đơn bằng API với idempotency key giữ trước POST. Nếu token, API hoặc hạ tầng lỗi thì dừng và giữ đầu ra, không suy là không có đơn.

Đã kiểm lại sau marker A2 (18:56:08Z): event/order/payment 200, tickets 500. Không có POST trong bằng chứng `fixture-sau-a2.txt`, không tạo đơn mới. Lượt k6 dùng đúng một event, một order như snapshot `chay-thu-5p/fixtures.json`; hash và byte khớp file hiện hành theo `kiem-sau-chay.json`.

Một fixture đọc không thay thực nghiệm vòng đời giao dịch ghi/thanh toán/phát vé. C1 chỉ cung cấp tải đọc cố định theo brief.
