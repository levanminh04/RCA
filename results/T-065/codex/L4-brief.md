# Brief L4 cho Codex — T-065 G-c: chọn bản P7 / M1-FT cùng ca, và xử lý phần còn mở của L3 (14/11/2026 ~01:45Z)

Bạn là Codex (`gpt-6.1-sol`, reasoning high), **người làm** T-065 trong repo `D:\RCA-flashticket`. Phiên Claude điều phối chiến dịch M1-FlashTicket giao việc; Claude là **người phản biện**. Quyền: `docs/DECISIONS.md` mục "Bổ sung quyền điều phối chiến dịch nhiều ngày".

## Đọc trước (bắt buộc)
1. `AGENTS.md`.
2. `tasks/T-065-giao-dien-grafana/SPEC.md` toàn bộ gồm phần bổ sung cuối file; `tasks/T-065-giao-dien-grafana/LOG.md` mục cuối.
3. `results/T-065/XONG.md`, `CHECKPOINT.md` (mục cuối), `kiem/001/BAO-CAO.md`, `manifest.json`, `thay-doi-may.md`.
4. `results/T-064/hop-dong-dau-ra.md` và **chỉ mục bản mới**: `results/T-064/ban-xuat/chi-muc-ban.json` (3 bản: `p7` khóa; `V032-H5b` đề xuất tạm; `V041-R1-H1c+H5b+H8s1` thay thế có đầu ra cạnh; mỗi bản 22 ca = 13 ca dev bản 2 + 9 ca T-062, có đường dẫn và SHA-256 từng đầu ra). Kiểm SHA trước khi dùng; lệch thì dừng phần phụ thuộc và ghi checkpoint.

## Việc
- **G-c:** thêm chiều **bản** vào bộ xuất dữ liệu, dashboard và liên kết: người dùng chọn `p7` / `V032-H5b` / `V041-…` cho **cùng ca**; trang ca hiện mã bản, `cau_hinh_sha256`, `ma_nguon_sha256`, trạng thái (khóa/đề xuất/thay thế) và cửa sổ `[t−300, t+300)`. Hiển thị cờ M1 và hạng đúng theo `method-output-1.json` của bản đó (`entity_ranking`, `extra.m1_ft.canh_xep_hang` với V041; V032 không có cạnh — hiện đúng "không có đầu ra cạnh", không suy ra). Giao diện **không** tự xếp lại hay chấm điểm; không hiện đáp án trên trang chính.
- **Phạm vi ca:** 9 ca T-062 (nguồn như L3) cộng 13 ca dev bản 2 **chỉ khi** nguồn trace/metric/log của ca dev có trên `exp-obs` hoặc trong repo dưới dạng bạn dùng được; nếu không có đủ để dựng liên kết bằng chứng, giữ ca dev ở mức bảng xếp hạng (không liên kết bằng chứng) và ghi rõ giới hạn, không dựng bằng chứng giả.
- **Phần còn mở của L3 (Claude quyết cách xử lý):**
  1. Panel diễn giải rỗng: **không** thử thêm biểu thức JSONata (đã 3 lần, AGENTS §5a). Dùng cách khác: bộ xuất ghi sẵn trạng thái từng truy vấn (có dữ liệu / rỗng / lỗi, kèm cửa sổ) vào JSON dữ liệu và panel chỉ hiển thị trường đó; hoặc một cách tĩnh có căn cứ khác. Kiểm bằng API trước, ghi lỗi nếu có.
  2. Bấm thật trong trình duyệt: sandbox của bạn không mở được trình duyệt. Thử lại đúng một lần theo cách bạn đã ghi ở CHECKPOINT; nếu vẫn chặn, ghi lệnh/lỗi/bước chịu ảnh hưởng và dừng ý đó (không tìm cách vòng). Không nhập mật khẩu vào trang đăng nhập thay Minh; chỉ dùng cách đã được cấp ở brief L3.
- **Kiểm:** hồi quy bản P7 (9 ca vẫn khớp nguồn như L3); mỗi bản × ca: số dòng/hạng/cờ khớp đầu ra nguồn (so tự động, ghi số ca và số dòng đã so); mọi liên kết giải mã đúng một lần; API ≥ 3 kho × 3 ca cho cả ba bản. Giữ bản 6 và bản L3 hiện hữu; dashboard mới đặt UID/thư mục mới.

## Quyền máy và phạm vi ghi
Như brief L3 (`results/T-065/codex/L3-brief.md`): `exp-obs` chỉ tạo file mới trong thư mục kết quả và provisioning đã dùng, restart riêng Grafana nếu cần (ghi giờ UTC và hash trước/sau, cách hoàn tác trong `thay-doi-may.md`); không SSH `exp-app` ngoài đọc; không chạm máy 84; không push/merge; không đọc `data/locked/`; không in mật khẩu. Ghi trong `results/T-065/` và mục mở/kết phiên của bạn trong `tasks/T-065-giao-dien-grafana/LOG.md` (chỉ ghi thêm). Không ghi `docs/`, `src/`, `results/T-064/`.

## Checkpoint, hạn mức, dừng
`results/T-065/CHECKPOINT.md` sau mỗi bước con và ≥ 30 phút/lần (giờ UTC, bước, đầu ra, bước tiếp). Hết hạn mức: bộ gọi sẽ `resume`. Có `D:/RCA-overnight/STOP`: dừng ở ranh giới. Lượt dài hơn 1 giờ: ghi trước "lỗi ở 10%/50%/99% xử lý thế nào" (luật 21).

## Báo xong
Cập nhật `XONG.md` (đạt/một phần, chặn, bước tiếp), `manifest.json`, `prompt-ban-giao.md` (kiểm độc lập, nguyên văn mẫu `docs/review-prompt.md`, thông tin trung tính). Tóm tắt cuối lượt: đã làm gì; file đổi; kiểm đã chạy và kết quả; điều chưa chắc.
