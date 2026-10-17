# Phản biện T-xxx

- **Người phản biện:** <Claude|Codex> — **Ngày:** — **Commit/diff đã đọc:**
- **Công đoạn/cổng và bản lượt:** <soát SPEC / soát kết quả / kiểm phản hồi và sửa; cổng; file được Minh cho phép>. Giữ vai trò và các bản cũ.
- **Đã đọc:** <danh sách file>
- **Tự soát độc lập:** <nguồn và đầu ra gốc đã kiểm trước khi đọc kết luận các lượt trước>.

## Kết luận chung

Một đến ba câu. Tách đạt SPEC với đạt phần mục tiêu nguồn và đủ căn cứ cho quyết định tiếp theo. Không có lỗi đáng kể thì nói thẳng là không có; câu hỏi mở không tự là lỗi hoặc đã được giải đáp.

## Các điểm

### R1. <tên ngắn> — CHẶN | KHÔNG CHẶN

- **Ở đâu:** file, mục, dòng.
- **Sai gì:**
- **Bằng chứng:** trích dẫn, số liệu, phản ví dụ, lệnh đã chạy và kết quả.
- **Bước và quyết định chịu ảnh hưởng:** lỗi đã xảy ra / mâu thuẫn thiết kế / nguy cơ chưa kiểm; chặn kết luận hay quyết định nào, hậu quả gì.
- **Đề xuất sửa:**

Số làm bằng chứng có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả. Xét cả phần có thể bác bỏ finding. Không tìm cho đủ số lượng; không sửa thay người làm.

## Đối chiếu các lượt trước

Nếu có, đánh giá từng điểm và phản hồi: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa. Không mặc nhiên đồng ý.

## Tuân thủ quy trình

Nêu việc đã kiểm và vi phạm có bằng chứng, nếu có: quyền ghi/duyệt, nguồn quyết định, tự kiểm, LOG/bàn giao, trạng thái kết luận và phụ thuộc khoa học. Kiểm theo nghĩa vụ của vai trò; người phản biện không phải ghi LOG/STATE. Findings có ảnh hưởng ghi chung ở mục Các điểm, không tạo lỗi thủ tục hình thức.

## Điều đã kiểm và thấy đúng

Ngắn. Giúp Minh biết phần nào đã được soát.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã làm gì:
2. File đã thay đổi, hoặc không sửa file nào:
3. Kiểm đã chạy và kết quả:
4. Bất đồng/câu hỏi mở, bằng chứng thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết:

Đề xuất tiếp tục hoặc dừng, kèm lý do. Không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn kết luận khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết dừng/sửa/chạy bổ sung/chấp nhận giới hạn. Hai agent đồng ý không thay bằng chứng; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

## Prompt bàn giao cho người làm

Người phản biện chép nguyên văn Prompt chung + khối Người làm đáp phản biện + khối cổng hiện có từ `docs/review-prompt.md`, chỉ điền thông tin trung tính. Vẫn soạn khi đề xuất dừng; Minh quyết gửi. Không ghi LOG/STATE hoặc sửa bản lượt cũ.

```text
<prompt với đường dẫn và phạm vi ghi chính xác; nếu chưa có quyền ghi thì chỉ trả lời trong chat>
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong mục LOG mới hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
