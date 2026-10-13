# T-033 — Bộ đầu ra người làm

Đọc nguyen-nhan-phat-hien.md, doc-tay.md và kiem-tiep.md. Các JSON và hai thư mục trung gian cạnh đây là bộ đầu ra mới theo SPEC. Không ghi đè root bao-phu-nhom.json cũ hoặc run nguồn.

Manifest.json giữ nguyên manifest EC2 của các file số/chuỗi. Package-manifest.json khóa cả tài liệu và các file số đã chép byte, không tự gồm chính nó. Source-catalog.json nối đường dẫn nguồn EC2 tới bản gốc laptop đã kiểm hash. Additional-source-verification.json pin nguồn định nghĩa/code chấm/tài liệu đã đọc thêm.

Chỉ hoàn thành phần người làm trong phạm vi SPEC; chờ Claude phản biện và Minh nghiệm thu. Cơ chế tính toán có điều kiện đã phân xử; nguyên nhân vật lý, onset, prior riêng, coverage và lựa chọn/benefit graph còn OPEN. Không thêm quyết định nghiên cứu hoặc mở test.
