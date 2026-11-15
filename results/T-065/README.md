> Bản hiện hành L4: [README-L4.md](README-L4.md), [báo cáo 002](kiem/002/BAO-CAO.md), [XONG.md](XONG.md). Phần dưới giữ nguyên hồ sơ L3 lịch sử.

# T-065 — dashboard Grafana, nhánh L3

Nguồn P7: 9 ca T-062. Đầu ra giao diện 0.3 có chiều `ban` ngay từ đầu, tách bản phát lại. Không chạy lại M1 và không sửa task cũ.

- Dựng và kiểm cục bộ: `node results/T-065/chay.mjs` (Node 22+ có `JSON.rawJSON`, không cần package ngoài). Trong phiên này dùng Node REPL vì Python ghim không khởi chạy trong sandbox. Mã sinh dashboard là `dung-dashboard.mjs`, thay cho tên `.py` dự kiến trong SPEC; không thay đổi phạm vi chức năng.
- `xuat-du-lieu.mjs`: kiểm manifest/pin, mở rộng dữ liệu, chỉ mục bản/ca/service/thao tác.
- `dung-dashboard.mjs`: giữ panel hồi quy bản 6, thêm lớp thao tác, nhãn điều hướng và mô tả rỗng. Chọn ca qua danh sách, bộ chọn ca ẩn để tránh đổi ca mà giữ thời gian cũ. Chọn service/thao tác vẫn dùng biến. Mọi link đổi ca đặt range đúng ca.
- `kiem.mjs`: kiểm schema 0.3 và các bất biến nguồn, cờ, tiền xử lý, cạnh/URL.
- `api-obs.py`: chạy qua SSH stdin ở `exp-obs`, chỉ đọc cấu hình/mật khẩu trong bộ nhớ và truy vấn API. `inventory`, `verify`, `links`, `links-extra` là bốn chế độ. Không ghi credential ra stdout/file, không tạo API key.
- `doi-chieu-api.mjs::verifyApi(<tên file API>)`: đối chiếu từng dòng API với dữ liệu nguồn đã xuất.

UID mới: `t065-rca` và `t065-phat-lai`. Dữ liệu mới ở `/opt/flash-ticket-obs/rca-ket-qua/t065-l3-001`. Dashboard bản 6 giữ UID `rca-g2` và `rca-g2-phat-lai`.

Miền phương pháp là `[lo,hi)`. Grafana có range cuối bao gồm điểm cuối, nên URL/dashboard dùng `to=hi−1ms`; truy vấn Loki API trực tiếp dùng `end=hi−1ns`. Trường nguồn `cua_so_ms` và cột kết thúc loại trừ vẫn ghi `hi`, không đổi nghĩa dữ liệu gốc.

Kiểm trình duyệt chưa hoàn tất vì browser host không khả dụng trong lượt này. API thành công không thay bằng chứng bấm thật, màu/bố cục render, hoặc nghiệm thu G-a/G-b. Xem `kiem/001/BAO-CAO.md` và `CHECKPOINT.md`.

G-c còn chờ chỉ mục xuất/bản phù hợp từ T-064 và lần kiểm trên ứng viên đề xuất cuối. Lựa chọn `ban` hiện chỉ có P7.

Hai panel thử hiện diễn giải rỗng riêng từng truy vấn chưa đạt sau ba lần và đã được rút. Bản bàn giao giữ hướng dẫn ở panel text cùng mô tả có điều kiện của panel sống. Phần diễn giải động và mức nhìn thấy của lời hướng dẫn vẫn OPEN, không phải chức năng đã nghiệm thu.
