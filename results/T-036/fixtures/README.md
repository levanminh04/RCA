# Ví dụ kiểm trước mã

`input.json` là dữ liệu tổng hợp, không là danh mục FlashTicket thật. A/B/C, DB1/DB2/PG, R/X/H đều là ID giả. Provenance chỉ đoạn nguồn quy định nhu cầu được mô phỏng: B12 §2 ownership/tài nguyên chung; B13 §5 message và Saga; B14 §3–7 retry/bù trừ/worker; B16 §3–5 callback/scheduler/địa chỉ. Không coi các ID/queue giả là tên runtime đã duyệt.

`expected.json` ghi đích literal trước builder/comparator. Hai bản ghi HTTP cùng đầu mút/kiểu/channel phải gộp cạnh nhưng giữ hai nguồn bản ghi. Publish lặp giữ cấu trúc, không tạo event_count. Hai queue cùng B.receive và fan-out sang C phải riêng. Callback/scheduler có operation gốc không caller. Saga vẫn A→B. DB1/DB2 khác nhau, cùng trỏ một PG; PG có metric chung, không sao thành metric từng thao tác.

Phép so đơn A→B có đích tập literal cho unknown, khác kiểu, cửa sổ rỗng. Các biến thể thiếu/mơ hồ mapping và địa chỉ có đích loại trừ; unknown chỉ khớp đầu mút. Tập dự kiến được viết độc lập; checker không được dùng hàm đang kiểm để tính expected. Biên nhận oracle ghi hash và xác nhận chưa có implementation, không phải bằng chứng các phép kiểm đã đạt.
