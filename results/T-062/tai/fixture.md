# Fixture C1

`k6/fixtures.json` giữ một event và ba order ID. Lấy event qua GET danh sách công khai rồi GET chi tiết. Không tạo đơn: ba ID ứng viên từ smoke receipt T-058 được xác minh lại quyền buyer bằng GET order hiện tại; cả ba trả 200, state CANCELLED. Không dùng trạng thái hay số đo cũ làm bằng chứng. Không có manifest hash cho các smoke receipt dùng làm khóa tra cứu; mọi giá trị được dùng đã đọc lại qua API hiện tại.

Nguồn trực tiếp: `fixture-doc-02.json` (UTC 18:40:55Z), `doc-fixture.py`. GET order/payment 200, GET order/tickets 500 cả ba đơn. Không sửa DB hoặc tạo giao dịch. Cần kiểm lại sau A2; nếu vẫn 500 thì nền ứng dụng chưa đạt ổn định. Không đổi mixture để che route lỗi.

Không có API liệt kê đơn buyer trong OrderController hiện tại; dùng ID ứng viên rồi xác minh quyền qua API. Chỉ ID event/order đi vào k6; không có tên ca, nhãn, trạng thái can thiệp, email hoặc mật khẩu.
