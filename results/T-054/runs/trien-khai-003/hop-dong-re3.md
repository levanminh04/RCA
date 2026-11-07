# Chuẩn bị RE3-OB trong pha 1

Đã kiểm metadata công bố và đối chiếu G1: 30 ca, 10 ô. Chưa tải hoặc mở telemetry RE3. Bảng dung lượng, pin nguồn và kiểm code nằm trong `hop-dong-re3.json` cùng thư mục.

Đây là hợp đồng chuẩn bị, chưa phải adapter đã cài. Hồ sơ schema local hiện không có RE3-OB. Adapter đang có còn giả định TT: TORAI lọc cột ts-*, BARO/CIRCA/TraceRCA ghim dataset re2-tt; profile M1 chỉ có TT/Nezha. Do đó không thể đổi nhãn dataset rồi tuyên bố RE3 được hỗ trợ.

Thứ tự cần làm: xác minh schema/đơn vị và inventory phi nhãn → duyệt file/hợp đồng sửa → kiểm adapter bằng mẫu tổng hợp đúng schema → khóa cho bản cuối → mở riêng RE3 một lần và báo bảng riêng. Không dùng RE3 làm pilot hoặc nơi chỉnh phương pháp. Nếu chưa lấy được schema trong quyền hiện có, ghi thiếu đúng nguồn schema/footer và trình quyền, không bỏ nghĩa vụ adapter khỏi kế hoạch.

P7 chính TT/Nezha và nhánh giữ ngoài RE3 có quyền/ma trận riêng. Đầu ra chuẩn bị H0 hiện đã có; H1-H4 còn theo các phụ thuộc trong JSON. Chưa có ETA cài/chạy RE3 vì chưa xác minh schema; dung lượng metadata không thay thời gian xử lý. Không sửa src trong lượt này.
