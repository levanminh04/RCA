# Bàn giao tiền kiểm T-039 — chờ Minh quyết

**Trạng thái:** chưa triển khai đầy đủ SPEC. Đã hoàn tất phần độc lập có nguồn hợp lệ và lập các đề xuất cần duyệt. Không nghiệm thu task, đổi SPEC, chuyển pin, chọn P6 hoặc mở test.

Đọc theo thứ tự:

1. `tasks/T-039-p5b-online-boutique/LOG.md` Phiên 2: nguyên lời giao, nhận xét độc lập và kết thúc tiền kiểm.
2. `tu-ra-va-kha-thi.md`: phần đạt, phần chưa làm, dự toán giờ công/máy/RAM/tổng đĩa và bằng chứng.
3. `de-xuat-tai.md/json`: nguồn/URL/commit/tree/từng blob/byte, phần loại trừ và vị trí ghi; chưa là quyền tải.
4. `de-xuat-tach.md`: impact map và hai phương án xử lý metadata loại object; chưa là SPEC mới hoặc quyết định của Minh.
5. `manifest.json` và `runs/tien-kiem-001/`: kiểm hash, inventory graph, metadata object, capacity snapshot, phạm vi/diff/lệnh.

## Phụ thuộc còn mở

| Câu hỏi/việc | Đầu vào và owner cần | Quyết định bị ảnh hưởng |
|---|---|---|
| Tổ chức task cho một phiên | Minh quyết tách/giữ; nếu tách cần trình SPEC cụ thể và duyệt trước ghi | Phạm vi/tiêu chí xong T-039 và task nhận phần còn lại; T-040 không thay khảo sát |
| Tải ứng dụng/code bổ sung | Minh duyệt đúng danh sách/revision/byte/path | Coverage toàn snapshot, quan hệ/thao tác, alias và mapping |
| Loại object trong registry | Minh quyết ghi chứng cứ riêng hay trình sửa registry chung/pin ba nhánh | Phát biểu provenance commit→tree; không thay nội dung code hay chứng minh dataset deployment |
| Revision ứng dụng/image/deployment sinh dataset | Manifest thu, image digest, build/config từ tác giả hoặc nguồn công bố có nối revision | Có được quy chênh lệch cho instrumentation hay chỉ đối chiếu tham khảo |
| Nguồn phụ mức ngày và Node/host | Code/export schema tạo nguồn và thời gian/namespace/owner, từ tác giả Nezha | Tính độc lập nguồn, ánh xạ host/metric; không lấy tên hoặc ổn định tên làm chứng cứ |
| Bản ghi/mapping/đối chiếu/phân tích | Source đã đọc đủ, oracle riêng trước code, nguyên pin T-036 và graph hiện hành | Các tiêu chí đầu ra còn lại, đầu vào T-040/P6/P9; chưa có số khớp cấu trúc T-039 |

Không dùng bảng proposal như bảng coverage đã đọc. Không có nguồn bổ sung tự cho quyền mở Weight, chuỗi số, Node/log/metric/trace thô, cửa sổ mới, test/heldout/archive hoặc nguồn ngoài danh sách. Không chạy Nezha/RCA. Không sửa code chung từ gói này.

Để đọc tiếp: `Get-Content -Raw -LiteralPath 'results/T-039/de-xuat-tai.md'`. Trước dùng kết quả cũ, kiểm manifest T-039 rồi pin T-036 và nguồn T-035 theo JSON input-verification; nguồn thay thì dừng phụ thuộc. Không chạy lại preflight trên tên run cũ.

Prompt trung tính Prompt chung + Soát SPEC + G3 nằm ở `prompt-claude-soat-spec.txt` và nguyên văn cuối LOG. Minh chọn chuyển thủ công. Lượt này chưa có bản REVIEW; không tự cấp quyền reviewer ghi file hoặc coi đồng thuận là quyền tải/đóng task.

Nội dung cần ghi chính thức sau khi Minh quyết: nguyên lời về quyền tải, cách tách/giữ và cách xử lý metadata. Chưa ghi DECISIONS/WHY vì ngoài phạm vi lời giao. Nội dung có thể dùng trong báo cáo hiện tại chỉ là provenance/miền/giới hạn tiền kiểm; không là kết quả khảo sát đầy đủ, lợi ích RCA hoặc yêu cầu collector đã chứng minh hiệu quả.
