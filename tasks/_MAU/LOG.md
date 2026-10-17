# Nhật ký T-xxx

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Phiên <số> — <ngày> — <Claude|Codex> — <thiết bị> — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, SPEC, mục cuối LOG. Kiểm đầu ra phiên trước: <có/không, hợp lệ không>.

**Công đoạn và mục tiêu nguồn:** <trình SPEC / làm / đáp phản biện / sửa / bàn giao; câu hỏi MRP, DT18/cô trực tiếp chi phối; phạm vi được Minh duyệt>.

**Diễn biến** (một dòng mỗi bước con, ghi ngay khi xong):
- <giờ> — <bước> — <kết quả> — <file>

**Quyết định của Minh trong phiên** (nguyên lời, kèm việc đã ghi vào DECISIONS chưa):
- ...

**Tự soát trước khi đọc kết luận phản biện** (ở lượt đáp phản biện):
- <điểm tự tìm được trên yêu cầu/đầu ra gốc; bằng chứng; nếu không có thì nói rõ>. Ghi phần này trước khi mở kết luận các lượt phản biện.

**Đánh giá phản biện và bất đồng** (nếu có):
- <bản lượt/điểm; đúng / đúng một phần / sai / chưa kiểm được; bằng chứng của người làm; quyết định bị ảnh hưởng>.

**Đề xuất sửa gom theo file** (nếu có):
- <file; sửa gì; vì sao; ảnh hưởng; chờ Minh duyệt hoặc nguồn duyệt>. Không tự sửa vì reviewer yêu cầu.

**Kết thúc phiên:**
1. Đã làm gì:
2. File đã thay đổi:
3. Kiểm tra đã chạy và kết quả:
4. Điều chưa chắc hoặc cần Minh quyết:
   - Đầu ra task đạt gì; câu hỏi nguồn trả lời tới đâu; hạn chế xác nhận và điều kiện, hoặc phần chưa xác định.
   - Bất đồng/câu hỏi mở, thiếu đúng bằng chứng gì; quyết định phụ thuộc; đề xuất phần kiểm tiếp theo, chi phí hoặc giới hạn dữ liệu.
   - Đề xuất tiếp tục hay dừng phản biện và lý do. Không che bất đồng bên kia còn giữ; dừng không tự nghiệm thu task hay xác nhận giả thuyết.
5. Bước tiếp theo chính xác:
6. Lệnh cuối cùng đã chạy:

---

## Prompt bàn giao của lượt này cho agent đối phương

Người làm thêm phần này vào mục mới sau mọi lượt trình SPEC, báo cáo, đáp phản biện hoặc kiểm sửa, kể cả đề xuất dừng; không thay prompt hay mục cũ. Chép nguyên văn Prompt chung + đúng khối công đoạn + khối cổng hiện có của `docs/review-prompt.md`. Chỉ điền thông tin trung tính; Minh quyết copy và gửi. Người làm vẫn là người làm, người phản biện vẫn là người phản biện.

```text
<prompt chung + khối công đoạn + khối cổng; đường dẫn và quyền ghi chính xác cho lượt tiếp theo>
```
