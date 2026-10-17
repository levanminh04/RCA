# T-xxx — <tên ngắn>

- **Trạng thái:** đề xuất | đã duyệt (ngày) | xong (ngày)
- **Người làm:** Claude | Codex
- **Người phản biện:** Codex | Claude (phải khác người làm)
- **Thuộc gói MRP:** P? — **Cổng:** G?

## Mục tiêu

Task này phục vụ câu nào của cô, DT18, RQ nào trong MRP. Ghi đường dẫn và đoạn nguồn trực tiếp chi phối. Nêu câu hỏi trước khi chọn phép đo hoặc thành phần.

Task là mô tả hiện tượng, phân xử cơ chế, thiết kế, cài đặt hay đánh giá? Phần nào của mục tiêu nguồn được bao phủ? Đạt task này có đủ căn cứ cho quyết định tiếp theo không?

## Câu hỏi, bằng chứng và quyết định

Điền cho các nhận định hoặc lựa chọn quan trọng; không ép mọi task giải hết RQ. Không dùng mục tiêu nguồn chưa bao phủ như điều đã hoàn thành.

| Câu hỏi và nguồn yêu cầu | Kết luận/lựa chọn cần phân xử; giải thích khác | Phép kiểm và bằng chứng cần có | Kết quả hỗ trợ, bác bỏ hoặc chưa phân xử | Phần còn thiếu, quyết định phụ thuộc và hướng xử lý |
|---|---|---|---|---|
| ... | ... | Đầu vào, bước xử lý, trung gian, đầu ra; phần đã lưu và phần phải chạy | ... | Nêu phạm vi/chi phí cần trình Minh hoặc giới hạn dữ liệu |

## Đầu vào

File, dữ liệu, kết quả của task trước. Có đường dẫn, revision/code và manifest phù hợp để kiểm đầu ra cũ. Chỉ rõ quyền đọc dữ liệu và môi trường/lệnh chạy đã được duyệt; không mặc nhiên cho phép mở test hoặc dataset giữ ngoài.

## Đầu ra

File sẽ tạo, mỗi file chứa gì và trả lời câu hỏi nào. Số liệu phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.

Với task phân tích hạn chế, đầu ra phải nêu:
1. Hạn chế đã xác nhận và điều kiện tồn tại.
2. Hạn chế thuộc lỗi cài đặt hoặc thiếu đầu vào.
3. Hạn chế thuộc giả định/cách tính của phương pháp, với giải thích cạnh tranh.
4. Quan hệ giữa dịch vụ có thể bổ sung thông tin gì, chưa coi là bằng chứng đồ thị đã giúp.
5. Câu chưa trả lời, thiếu đúng bằng chứng gì và quyết định nghiên cứu bị ảnh hưởng.

Khi đủ bằng chứng cơ chế, kết luận theo dạng: "Trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z", dẫn đầu vào → xử lý → trung gian → đầu ra. Nếu chưa biết Y, giữ đúng câu chưa trả lời, không điền nguyên nhân cho đủ mẫu. Hạn chế dữ liệu xác nhận cần nêu hệ quả cho đánh giá và yêu cầu quan sát FlashTicket có thể rút ra.

Với task thiết kế/kiểm phương pháp đồ thị, chỉ rõ nút, cạnh, nơi đặt log/trace/metric và phép tính dùng cạnh; phân biệt căn cứ sửa hạn chế, đáp ứng DT18 và nhu cầu kỹ thuật.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

Phạm vi này dành cho người làm sau khi SPEC được duyệt. Người phản biện chỉ ghi bản phản biện lượt được Minh cho phép. Chưa duyệt tạo file thì SPEC và prompt được trình trong chat.

- `results/T-xxx/`
- ...

## Các bước

Mỗi bước có phép/lệnh kiểm và phụ thuộc thật. Đọc code và trung gian đã lưu trước khi đề xuất chạy thêm. Với nhóm quan trọng, xem cả ca sai và ca đúng có điều kiện tương ứng. Thiếu trung gian thì trình đúng phần cần chạy; không loại câu hỏi bằng "ngoài SPEC".

1. ... — kiểm bằng: ...
2. ...

## Kiểm đúng đắn

Mỗi đầu ra kiểm bằng gì: số công bố để đối chiếu (nguồn, bảng), phép kiểm không cần nhãn, giá trị trung gian và giải thích khác. Tách lỗi dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định phương pháp. Điều gì không kiểm được trong task, vì sao, kết luận nào yếu đi và cách xử lý cần Minh quyết.

Đối chứng cấu trúc dùng khi đánh giá tác dụng của cơ chế đồ thị; không là điều kiện trì hoãn mọi phân tích hạn chế baseline. Khi so cấu trúc, nêu thông tin giữ/bỏ, điều kiện so sánh và yếu tố thay cùng. Trước G3 phải kiểm hành vi trên dev và khóa cách xử lý ca lỗi/nhánh dự phòng/tập ứng viên; không chỉ kiểm chạy không lỗi.

## Tiêu chí xong

Điều kiện kiểm được, không chỉ là đủ file hoặc số khớp. Nêu mức câu trả lời cần đạt và quyết định được phép rút ra. Kết quả bác bỏ hoặc chưa phân xử có thể là đầu ra hợp lệ nếu đã thực hiện phép kiểm cần thiết trong quyền được duyệt và báo rõ giới hạn; không tự gọi là đã xác nhận cơ chế hoặc đủ căn cứ chọn thiết kế.

## Không làm

Những việc dễ lan sang nhưng nằm ngoài task. Với phần cần cho mục tiêu nguồn mà chưa làm, ghi lý do, bằng chứng thiếu, quyết định phụ thuộc và đề xuất phạm vi/task nối tiếp. Không coi giới hạn quyền ghi là quyết định bỏ nghĩa vụ nghiên cứu.

## Chi phí ước lượng

Thời gian chạy, dung lượng tải, có cần báo trước theo luật cứng 8 không. So với ngân sách Q-40.

## Rủi ro và điều chưa chắc

Ghi rõ "chưa kiểm", giả định, khi nào sai, vì sao chưa kiểm và kết luận phụ thuộc. Không dùng ứng viên này làm căn cứ đã xác nhận; Minh duyệt thử không xác nhận giả thuyết.

## Prompt bàn giao

Sau mỗi lượt trình SPEC, báo cáo, đáp phản biện hoặc kiểm sửa, chép nguyên văn Prompt chung, khối công đoạn và khối cổng hiện có từ `docs/review-prompt.md`; chỉ điền thông tin trung tính. Người làm ghi prompt trong mục LOG mới nếu có quyền; chưa có quyền ghi thì trình trong chat. Vẫn soạn khi đề xuất dừng để Minh quyết gửi hay dừng. Không tự gửi sang agent đối phương.
