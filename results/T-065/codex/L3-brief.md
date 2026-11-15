# Brief L3 cho Codex — T-065 giao diện Grafana: G-a và G-b trên đầu ra P7 (12/11/2026 22:15Z)

Bạn là Codex (`gpt-6.1-sol`, reasoning high), **người làm** T-065 trong repo `D:\RCA-flashticket`. Phiên Claude điều phối chiến dịch M1-FlashTicket giao việc; Claude là **người phản biện**. Minh đã duyệt SPEC và giao Claude toàn quyền điều phối (`docs/DECISIONS.md`, mục "Bổ sung quyền điều phối chiến dịch nhiều ngày").

## Đọc trước (bắt buộc)

1. `AGENTS.md` (Luật 0 ngoại lệ 7: bạn được ghi trong "Phạm vi ghi" của SPEC đã duyệt).
2. `tasks/T-065-giao-dien-grafana/SPEC.md` **toàn bộ, gồm phần bổ sung cuối file** — đề bài.
3. `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md` mục 1, 2 (đoạn Grafana bản 6), 6.
4. Mốc hồi quy: bản 6 `results/T-062/giao-dien/` (`dung-dashboard.py`, `chi-muc-*.py`, `grafana/`, `thay-doi.md`), báo cáo kiểm thật `results/T-062/codex/g1-that-2/BAO-CAO.md`, phản biện `tasks/T-062-dem-chang-1-4/REVIEW-G1-5.md` (G-2, G-3). Bối cảnh lớp thao tác: `tasks/T-062-dem-chang-1-4/BOI-CANH.md` mục "Lớp thao tác". Định dạng T-061 (`results/T-061/`, **chỉ đọc**).
5. **Hợp đồng đầu ra với T-064:** `results/T-064/hop-dong-dau-ra.md` (bản 1). Thiết kế dữ liệu có **chiều bản** (`p7` bây giờ, M1-FT sau) ngay từ G-a/G-b để G-c chỉ cần thêm bản.

## Việc

- **G-a:** liên kết Loki ở bảng bằng chứng (hiện 0 URL); điều hướng danh sách → ca → chi tiết → phát lại; khung thời gian đúng cửa sổ ca `[t−300, t+300)` ở mọi panel và liên kết; diễn giải panel rỗng có căn cứ (mô tả kết quả truy vấn, không suy nguyên nhân khi chưa có bằng chứng); vùng nghi ngờ; nhãn điều hướng (G-3).
- **G-b:** bấm một service → bảng thao tác (HTTP/SQL/job/message theo dữ liệu thực có; trạng thái/cờ M1 từ `method-output-1.json` kênh `op`; điểm `e` chỉ ở chi tiết; kích thước nút cố định) và đồ thị thao tác (cạnh cha–con quan sát được, áp đúng tiền xử lý `src/m1/chuoi.py`: cắt cửa sổ, `he_span`, alias) → mở bằng chứng từng thao tác ở Tempo/Loki/Prometheus. Ghi loại quan hệ **đã hỗ trợ và đã kiểm**; loại chưa có dữ liệu (span link message) ghi "chưa hỗ trợ". Mở rộng định dạng thì ra phiên bản định dạng mới trong `results/T-065/dinh-dang/` kèm bộ kiểm lược đồ (không sửa T-061).
- Dữ liệu nguồn: 9 ca T-062 `results/T-062/ca/<id>/outputs/<id>/method-output-1.json` và `method-input.json`. Trang chính **không** hiển thị đáp án; trang phát lại tách như bản 6.
- **Kiểm:** 9 ca hiển thị khớp nguồn (hồi quy bản 6); mọi liên kết bằng chứng giải mã đúng một lần, mở đúng datasource/cửa sổ/truy vấn; bấm thật ít nhất một liên kết mỗi loại (Tempo, Loki, Prometheus) ở ít nhất 3 ca; lớp thao tác: số thao tác và cờ khớp `method-output-1.json`. Lưu `results/T-065/kiem/<lượt>/BAO-CAO.md` + ảnh chụp + bảng đối chiếu.

## Quyền máy

- **`exp-obs`** (`ubuntu@213.35.116.128`, khóa `D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key`, known_hosts `D:/RCA-ext/overnight-T058/out/known_hosts`): **chỉ** tạo file dashboard **mới** trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/` (giữ dashboard bản 6), thư mục con **mới** trong `/opt/flash-ticket-obs/rca-ket-qua/`, `docker restart flash-ticket-obs-grafana` khi cần nạp provisioning. **Không** đổi `pinned/compose.json`, `prometheus.json`, `collector.json`, Loki/Tempo/Prometheus/Collector (thuộc T-063 — Claude). Cần đổi compose thì ghi yêu cầu vào checkpoint và báo, không tự đổi. Truy vấn Prometheus cắt khúc ≤ 10 phút.
- Mật khẩu Grafana: Minh cho Codex đọc file mật khẩu trên máy; **không in** vào file, log, báo cáo, lệnh hiển thị.
- Không SSH `exp-app` ngoài lệnh đọc; không chạm máy 84; không push/merge; không đọc `data/locked/`.

## Phạm vi ghi

`results/T-065/` (mã, dashboard nguồn, `dinh-dang/`, `du-lieu/`, `kiem/`, `thay-doi-may.md` có hash trước/sau và cách hoàn tác, `CHECKPOINT.md`, `codex/`); `tasks/T-065-giao-dien-grafana/LOG.md` (chỉ ghi thêm, mục mở phiên/kết thúc phiên của bạn). Không ghi `docs/`, `src/`, `tasks/` khác, results của task khác.

## Chế độ chạy

Lượt này chạy trong sandbox `workspace-write` (ghi được `D:\RCA-flashticket`, có mạng). Nếu một lệnh cần thiết bị sandbox chặn (mở trình duyệt, ghi ngoài repo…), **không tìm cách vòng**: ghi lệnh, lỗi, bước bị ảnh hưởng vào `results/T-065/CHECKPOINT.md` và báo cáo; làm phần độc lập (dashboard JSON, chỉ mục, kiểm qua API Grafana/Infinity). Claude sẽ quyết cách kiểm phần trình duyệt.

## Checkpoint, hạn mức, dừng

- `results/T-065/CHECKPOINT.md` sau mỗi bước con và ít nhất 30 phút/lần (giờ UTC, bước, đầu ra, lệnh nền/đường hầm đang mở, bước tiếp). Đóng đường hầm/trình duyệt khi xong.
- Hết hạn mức: bộ gọi của Claude sẽ `resume` phiên này khi hồi — đọc checkpoint, không làm lại phần đã có đầu ra hợp lệ.
- Có `D:/RCA-overnight/STOP`: dừng ở ranh giới, ghi checkpoint.

## Báo xong

File `-o`: dòng đầu `L3 XONG`, `L3 XONG MỘT PHẦN` hoặc `L3 CHẶN`; rồi: đã làm gì; file đã tạo; kiểm đã chạy và kết quả (số, đường dẫn); phần chưa làm/bị chặn và vì sao; thay đổi máy (hash). Tiếng Việt, câu ngắn.
