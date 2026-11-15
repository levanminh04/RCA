# Brief L7 — T-065: bấm kiểm R1 trên Chrome sau UI06 (Codex app, người làm)

Soạn 14/11/2026 từ phiên Claude `ed8b9c01`. Minh dán brief này vào Codex app.
- Vai trò: Codex là người làm T-065, Claude là người phản biện.
- Lượt này chỉ đóng điểm CHẶN R1 của `tasks/T-065-giao-dien-grafana/REVIEW-2.md`, theo mẫu kiểm Codex tự đề xuất ở mục L6 trong LOG.
- Không làm lại phần L5 đã đạt.

## 0. Đọc trước (bắt buộc)

1. `AGENTS.md`.
2. Tài liệu của task:
   - `tasks/T-065-giao-dien-grafana/SPEC.md`;
   - `LOG.md`: mục L5 và mục L6 cuối file;
   - `REVIEW-2.md`: điểm R1, bảng phản hồi của người làm.
3. Kết quả L5–L6:
   - `results/T-065/BAN-GIAO-L5.md`, `CHECKPOINT.md`, `thay-doi-may.md`;
   - `results/T-065/codex/L6-dap-review2.json`, check `R1_ui06_structure_and_time_variable_consumers`;
   - `results/T-065/kiem/003-trinh-duyet/nhat-ky-bam.jsonl`: định dạng bản ghi bấm đã dùng.
4. `results/T-064/ban-xuat/chi-muc-ban.json`: nguồn số hiển thị và danh sách ca.

## 1. Trạng thái

Ngay khi bắt đầu, tạo `results/T-065/codex/L7-trang-thai.json`.
- Trường bắt buộc: `ten: "L7"`, `nguon: "codex-app"`, `trang_thai: "dang_chay"`, `cap_nhat` (giờ UTC), `buoc`.
- Cập nhật sau mỗi ca.
- Khi kết thúc, đặt `trang_thai` thành `xong`, `mot_phan` hoặc `dung` (kèm lý do).

## 2. Việc chính: bấm thật các liên kết dùng `t_tu`/`t_den` sau UI06

UI06 đổi kiểu và giá trị hai biến `t_tu`/`t_den`. Các liên kết chịu ảnh hưởng:
- dashboard chính `t065-l4-rca`: panel 4, 22, 23;
- trang phát lại `t065-l4-phat-lai`: panel 4.

Đọc lại JSON đang triển khai để xác định đúng các liên kết. Nếu thấy thêm liên kết nào khác dùng hai biến này, đưa nó vào lượt bấm.

Mẫu bấm tối thiểu:
- **3 ca:** bắt buộc có `1ad3afeb`. Hai ca còn lại chọn khác service gốc, và có ít nhất một ca của tập T-062. Ghi lý do chọn trước khi bấm.
- **3 bản:** P7, V032, V041. Mỗi ca bấm trên một bản khác nhau, sao cho ba ca phủ đủ ba bản.
- **Trên mỗi ca:** bấm từng liên kết của panel 4, 22, 23 trên trang chính, ít nhất 9 lần cho cả lượt. Thêm panel 4 của trang phát lại cho từng ca.

Với mỗi lần bấm, ghi lại:
- URL trước và sau khi bấm, không ghi token hay cookie;
- service, operation và cửa sổ thời gian (ISO UTC) ở trang đích, đối chiếu với giá trị nguồn trong `chi-muc-ban.json` của ca đó;
- trang đích có panel sống không:
  - đọc request/response của panel qua công cụ mạng hoặc Inspector: truy vấn, khoảng thời gian, số dòng hay số điểm trả về;
  - panel rỗng thì phân loại theo (i)/(ii)/(iii) như L5, kèm bằng chứng;
- một ảnh chụp trang đích, không chụp vùng có bí mật.

Một lần bấm **đạt** khi cả ba điều sau đúng:
- trang đích đúng service/operation;
- cửa sổ khớp ca;
- panel đích trả dữ liệu, hoặc rỗng có lý do (i)/(ii) đã chứng minh.

Không bấm lại 66 trang hoặc 162 liên kết của L5. Không chạy lại M1.

## 3. An toàn máy

`exp-obs` có 2 lõi. Grafana giới hạn 768 MiB và từng bị hết bộ nhớ.
- Phiên điều phối có thể đang chạy lô M1 (ví dụ dời mốc). Trước mỗi ca, kiểm trên `exp-obs` bằng `pgrep -af "runner4|runner3|chay_ca|chay_bien_the" | grep -v pgrep | head` và đọc `docker stats --no-stream` của Grafana.
- Có lô đang chạy thì vẫn bấm được, nhưng tuần tự, không mở song song và không mở node graph hay tìm kiếm Tempo diện rộng. Ghi lại tình trạng tải.
- Grafana restart thì dừng, ghi sự kiện Docker, giảm nhịp rồi làm tiếp. Không đổi giới hạn bộ nhớ.
- Dùng tab và tunnel sẵn có nếu còn sống (tab Chrome `217961015`, tunnel `127.0.0.1:13000`, PID 24712). Không còn thì tạo lại theo cách đã ghi ở L5 và ghi lại cách làm.

## 4. Gặp lỗi thì làm gì

Lượt này **không sửa dashboard**. Theo AGENTS mục 5 bước 8, Minh quyết sửa sau vòng phản biện.

Nếu một liên kết sai (đích sai, cửa sổ sai, panel lỗi):
- ghi đủ bằng chứng;
- lần nguyên nhân trên JSON đang triển khai;
- đề xuất sửa tối thiểu: file, đoạn cũ → đoạn mới, ảnh hưởng, cách hoàn tác;
- rồi bấm tiếp các liên kết còn lại.

## 5. Đầu ra (bắt buộc)

Thư mục `results/T-065/kiem/004-r1-ui06/`:
- `mau-chon.json`: 3 ca, 3 bản, lý do chọn, ghi trước khi bấm;
- `nhat-ky-bam.jsonl`: mỗi lần bấm một dòng;
- `doi-chieu-dich.json`: kết quả đối chiếu đích với nguồn, kết luận đạt hoặc không của từng lần bấm;
- `anh/`;
- `may.jsonl`: các lần kiểm tải;
- `BAO-CAO.md`: kết luận R1, có tách quan sát, suy luận và phần còn mở.

Ngoài thư mục trên:
- Nối một mục L7 vào `tasks/T-065-giao-dien-grafana/LOG.md` theo AGENTS mục 7. Mục gồm lệnh cuối, bước tiếp, và đề xuất sửa nếu có.
- Dựng lại manifest bằng `node results/T-065/l5-tong-hop.mjs manifest` hoặc cách tương đương, rồi kiểm checksum.
- Cuối mục LOG, soạn prompt cho người phản biện (Claude): chép nguyên văn Prompt chung và khối công đoạn "Kiểm lại phản hồi và sửa" trong `docs/review-prompt.md`, chỉ điền thông tin trung tính. Phạm vi đầu vào gồm phản hồi L6 và đầu ra L7. Người phản biện ghi bản phản biện lượt mới `REVIEW-3.md`. Phạm vi ghi để Minh cấp.

## 6. Giới hạn cứng

- Chỉ ghi `results/T-065/` và mục mới trong LOG T-065.
- Không ghi `docs/` hoặc `docs/STATE.md`. Không sửa `REVIEW-2.md`, kể cả bảng phản hồi đã điền.
- Không sửa dashboard, provisioning hay dữ liệu.
- Không chạm `exp-app` ngoài đọc. Không chạm máy 84 (52.64.237.84).
- Không đọc `data/locked/`, `.env`, `grafana.env`, `~/.ssh`, lịch sử shell.
- Không in hay ghi mật khẩu, token, cookie vào file, log hoặc ảnh. Không nhập mật khẩu thay Minh. Nếu Grafana đòi đăng nhập lại, dừng và báo Minh.
- Không commit, push hay merge.
- Có file `D:/RCA-overnight/STOP` hoặc `~/rca-dieu-phoi/STOP` trên `exp-obs` thì dừng ở ranh giới gần nhất.

## 7. Tóm tắt cuối lượt (trong chat Codex app)

Theo AGENTS mục 7, gồm bốn mục:
1. Đã làm gì.
2. File đã đổi.
3. Kiểm đã chạy và kết quả.
4. R1 đạt hay chưa; có lỗi và đề xuất sửa nào; phần còn mở (G-c chờ bản M1-FT cuối).

Thêm đường dẫn `BAO-CAO.md` và vị trí prompt cho Claude.
