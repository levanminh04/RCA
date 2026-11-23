Đã sửa [trien-khai-e5.md](D:/RCA-flashticket/results/T-073/trien-khai-e5.md). Trước khi sửa, tôi đã tạo [bản sao nguyên gốc](D:/RCA-flashticket/results/T-073/trien-khai-e5.truoc-cx16.md) và xác nhận SHA-256 của hai file trùng nhau.

| Mục | Trước | Sau |
|---|---|---|
| 1. K8 | Kiểm ở S4-1, khi bộ điều phối chưa chạy. | Kiểm sau S4-8, trước khi tiêm. Phải xác nhận luật W4, đích webhook, bộ nhận và việc bộ điều phối đã đọc tin Test từ spool. K8 chưa đạt thì dừng trước tiêm. |
| 2. I7 | Kiểm job ở S4-1, thiếu `stage_b` và `inj3`. Các bước hoàn tác chưa yêu cầu kiểm sát lúc đổi checkout. | Ngay trước **mỗi lần** đổi checkout, kể cả hoàn tác, đối chiếu HEAD với commit nguồn, kiểm cây sạch và đủ `chuoi_tai`, `runner4`, `tai_linux`, `stage_b`, `orchestrator`, `inj3`. Sau khi đổi, đối chiếu HEAD với commit đích và ghi commit trước/sau. |
| 3. `inj3` | Gộp `ensure` và `verify` vào S4-1 mang nhãn “chỉ đọc”. | Tách thành S4-1a, ghi rõ thao tác có thể thay đổi trạng thái. Với `PAUSE-PAYMENT`, bước này dùng `verify` cho K10. |
| 4. Mốc cuối E4 | Bấm Test rồi kiểm tin mới ở hai bộ nhận. | Trước khi bấm Test, lưu SHA-256, dòng cuối và giờ UTC của `/srv/rca-lab/runs/t072-e3-01/webhook.jsonl`. Sau đó đối chiếu tin Test ở cả hai đích. |
| 5. Dashboard | Kiểm ca cũ và phát lại. Chưa chỉ cách ghi giờ thấy ca mới hay kiểm trang lưu trữ. | S4-7 kiểm cả sáu dashboard lưu trữ. Ở S4-9, vì `refresh` rỗng, người vận hành làm mới hoặc mở lại trang, ghi giờ UTC lần đầu thấy mã ca, mở ca để xác nhận và lưu bằng chứng. |
| 6. Ô đã bốc | Chỉ ghi “ô đã bốc”. | Ghi `PAUSE-PAYMENT`, hạt `32323232`, theo [LOG T-073](D:/RCA-flashticket/tasks/T-073-w5-rca-truc-tuyen/LOG.md:167). |

Đã soát toàn bộ diff và đối chiếu SHA-256 của hai file khóa. N vẫn là **25 phút**, tiêu chí và ô khớp bản đã khóa. Phiên này chỉ sửa tài liệu trên laptop. Kết quả vận hành E5 còn chờ S4.

**SHA-256 của file mới** `9f1d1b065406eb24990de990d4dceae15c16146d27c93e058bb44cc53f54b8fb`