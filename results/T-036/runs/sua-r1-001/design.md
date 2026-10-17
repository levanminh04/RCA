# Sửa R1 theo lời Minh duyệt — 15/10/2026

Đầu vào/đáp án ở fixtures/r1.json được ghi trước sửa comparator. Bản comparator trước sửa được giữ trong before/. Oracle này thuộc lượt sửa, không thay hoặc gọi là oracle trước implementation ban đầu.

Khóa lưu graph nguồn giữ đủ năm trường messaging. Khóa đối chiếu sau mapping dùng đúng phần địa chỉ theo vai trò: publish = broker/broker_scope/exchange/routing_key; consume = broker/broker_scope/queue; logical-message = cả năm. Những phần cần thiết thiếu vẫn bị loại trừ. Khớp consume chỉ xác nhận chặng broker→consumer qua queue, không xác nhận exchange/routing của nguồn phát hoặc binding runtime.

Địa chỉ nguyên bản trong graph và members giữ nguyên. Nếu hai bản ghi consume khác thông tin exchange/routing nhưng cùng broker/scope/queue, phép so gộp một khóa và giữ cả hai thành viên. Không sửa builder tĩnh, builder trace, mapping, miền hoặc graph dev.

Phép phân xử: tái lập oracle R1 với comparator cũ; sau sửa kiểm hai phía khác độ chi tiết ở hai mức và hai view. Đối chiếu queue/scope khác và queue thiếu; xác nhận địa chỉ phát và logical-message vẫn phân biệt đúng trường bắt buộc. Chạy lại bộ kiểm task, so kết quả không messaging/graph nguồn với lượt trước và kiểm tính xác định. Không chạy baseline, trace thô, test hoặc thực nghiệm RCA.
