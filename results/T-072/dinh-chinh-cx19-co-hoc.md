# Đính chính cơ học W4 · T-072 · Giờ hiệu lực E4

Ngày 22/11/2026, **06:06:10Z** là nhịp truy vấn tổng hợp đầu tiên sau khi Grafana báo khỏe. Nhật ký ghi nhịp đầu của bộ lập lịch lúc 06:06:00Z, kiểm tra sức khỏe thành công lúc 06:06:01Z và 11 truy vấn trong nhóm 10 giây bắt đầu lúc 06:06:10Z. Số đếm theo nhóm không cho biết thời điểm đánh giá của từng luật. Bằng chứng chung cho các mục dưới là `results/T-072/e3/b10-restart-g.txt:4,14–18` và tiêu chí tại `results/T-072/ke-hoach-e3.md:40,45`.

**R5 giữ nguyên.** Cửa sổ chấm E4 bắt đầu lúc 10:13Z, lượt đầu phát lúc 10:13:37Z. Cả hai mốc hiệu lực đều trước cửa sổ chấm, nên tử số vẫn là 0 sự cố và mẫu số vẫn là 383 phút khỏe ×1. Xem `tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md:33` và `results/T-072/bang-bao-dong-gia.md:9,13–14`.

## Vị trí ghi mốc cũ

Các trích đoạn dưới đây được định vị bằng `Select-String -SimpleMatch '06:06:00'`. Mũi tên nối chữ gốc với cách đọc đã đính chính.

- `results/T-072/e3.md:9` — `` **2026-11-22T06:06:00Z** — tick đầu sau commit G có đủ 11 truy vấn luật, cả 11 ok; DB chỉ còn đúng 11 luật thật `` → `` **2026-11-22T06:06:10Z** — nhịp truy vấn tổng hợp đầu tiên sau khi Grafana báo khỏe ở commit G, với 11 truy vấn trong nhóm 10 giây. DB còn đúng 11 luật thật. ``.
- `results/T-072/bang-bao-dong-gia.md:13` — `` Cửa sổ nằm trọn sau giờ hiệu lực E4 (06:06:00Z). `` → `` Cửa sổ nằm trọn sau giờ hiệu lực E4 (06:06:10Z). ``.
- `results/T-072/bang-bao-dong-gia.json:9`, `results/T-072/e4/grafana-dem.json:4`, `tasks/T-070-dieu-phoi-giai-doan-2/TRANG-THAI.json:288` — `` "gio_hieu_luc_E4": "2026-11-22T06:06:00Z" `` → `` "gio_hieu_luc_E4": "2026-11-22T06:06:10Z" ``.
- `results/T-071/khai-truoc-e4.json:344` — `` "gio_hieu_luc_e4_utc": "2026-11-22T06:06:00Z" `` → `` "gio_hieu_luc_e4_utc": "2026-11-22T06:06:10Z" ``.
- `results/T-071/khai-truoc-e4.json:305`, `tasks/T-071-w4a-nen/LOG.md:297` — `` gio_hieu_luc_e4_utc = 2026-11-22T06:06:00Z `` → `` gio_hieu_luc_e4_utc = 2026-11-22T06:06:10Z ``.
- `results/T-071/khai-truoc-e4.json:345` — `` Giờ hiệu lực E4 2026-11-22T06:06:00Z — tick đầu sau commit G có đủ 11 truy vấn luật, cả 11 ok; DB chỉ còn đúng 11 luật thật `` → `` Giờ hiệu lực E4 2026-11-22T06:06:10Z — nhịp truy vấn tổng hợp đầu tiên sau kiểm tra sức khỏe, với 11 truy vấn. DB còn đúng 11 luật thật. ``.
- `tasks/T-072-w4b-luat-canh-bao/LOG.md:191` — `` **Giờ hiệu lực E4 = 2026-11-22T06:06:00Z** (tick đầu sau G có đủ 11 truy vấn ok; DB đúng 11 luật thật). `` → `` Giờ hiệu lực E4 = 2026-11-22T06:06:10Z (nhịp truy vấn tổng hợp đầu tiên sau kiểm tra sức khỏe sau G, với 11 truy vấn). DB còn đúng 11 luật thật. ``.
- `tasks/T-071-w4a-nen/LOG.md:296` — `` **giờ hiệu lực E4 2026-11-22T06:06:00Z** (e3.md dòng 9: tick đầu sau commit G có đủ 11 truy vấn luật, cả 11 ok; DB chỉ còn 11 luật thật — đã đối chiếu file) `` → `` giờ hiệu lực E4 2026-11-22T06:06:10Z (nhịp truy vấn tổng hợp đầu tiên sau kiểm tra sức khỏe, với 11 truy vấn). DB còn đúng 11 luật thật ``.
- `tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md:31`, `tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:273`, `docs/STATE.md:15` — `` giờ hiệu lực E4 06:06:00Z `` → `` giờ hiệu lực E4 06:06:10Z ``.
- `tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:271` — `` giờ hiệu lực E4 **06:06:00Z** `` → `` giờ hiệu lực E4 **06:06:10Z** ``.
- `tasks/T-072-w4b-luat-canh-bao/LOG.md:201` — `` sau giờ hiệu lực E4 06:06:00Z `` → `` sau giờ hiệu lực E4 06:06:10Z ``.
- `tasks/T-071-w4a-nen/LOG.md:306` — `` Khoảng 06:06:00Z (giờ hiệu lực E4) → 10:12:58Z `` → `` Khoảng 06:06:10Z (giờ hiệu lực E4) → 10:12:58Z ``.
- `tasks/T-071-w4a-nen/LOG.md:312` — `` Khoảng 06:06:00Z → 10:12:58Z không tải, không vào mẫu số. `` → `` Khoảng 06:06:10Z → 10:12:58Z không tải, không vào mẫu số. ``.
- `tasks/T-071-w4a-nen/LOG.md:341` — `` 0 phút trước giờ hiệu lực 06:06:00Z `` → `` 0 phút trước giờ hiệu lực 06:06:10Z ``.
- `docs/STATE.md:14` — `` giờ hiệu lực 06:06:00Z `` → `` giờ hiệu lực 06:06:10Z ``.
- `tasks/T-073-w5-rca-truc-tuyen/LOG.md:153` — `` hiệu lực 06:06:00Z `` → `` hiệu lực 06:06:10Z ``.

Ở `results/T-072/e3.md:29` và `tasks/T-072-w4b-luat-canh-bao/LOG.md:188`, 06:06:00Z là nhịp đầu của bộ lập lịch. Mốc này khớp trường `first_tick` tại `results/T-072/e3/b10-restart-g.txt:14`.
