# Nhật ký T-xxx

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Phiên <số> — <ngày> — <Claude|Codex> — <thiết bị> — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, SPEC, mục cuối LOG. Kiểm đầu ra phiên trước: <có/không, hợp lệ không>.

**Diễn biến** (một dòng mỗi bước con, ghi ngay khi xong):
- <giờ> — <bước> — <kết quả> — <file>

**Quyết định của Minh trong phiên** (nguyên lời, kèm việc đã ghi vào DECISIONS chưa):
- ...

**Kết thúc phiên:**
1. Đã làm gì:
2. File đã thay đổi:
3. Kiểm tra đã chạy và kết quả:
4. Điều chưa chắc hoặc cần Minh quyết:
5. Bước tiếp theo chính xác:
6. Lệnh cuối cùng đã chạy:

---

## Prompt phản biện cho agent còn lại

Người làm viết phần này khi task chờ phản biện, theo `docs/review-prompt.md`. Minh dán nguyên văn vào phiên mới của agent còn lại.

```text
<prompt>
```
