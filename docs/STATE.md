# Trạng thái

Cập nhật: 15/11/2026. Quyết định ở [DECISIONS.md](DECISIONS.md); chi tiết, giới hạn, lịch sử ở LOG từng task. Kế hoạch: [giai đoạn 2](techstack/KE-HOACH-GIAI-DOAN-2.md) §3 (chặng 0–6), §7 (nhánh G); chặng 6: [PLAN-TRIEN-KHAI](techstack/PLAN-TRIEN-KHAI.md) §6.2.

## Task đang mở

- **T-062 — chặng 1–4 trên FlashTicket:** lượt E1 xong 12/11; LOG 12/11 ~15:00Z ghi đã sửa theo `REVIEW-2.md` (Minh duyệt). **Chưa nghiệm thu, chưa đóng.** Còn: `results/T-062/manifest.json` chưa bao phủ `_metric-bo-sung/`. Thư mục task chứa cả hồ sơ chiến dịch M1-FT (đã đóng 15/11). [SPEC](../tasks/T-062-dem-chang-1-4/SPEC.md), [LOG](../tasks/T-062-dem-chang-1-4/LOG.md).
- **T-057 — hồ sơ G4, báo cáo cho cô:** G4 duyệt 09/11 (phạm vi P7(a)). Còn: câu xin cô, `.docx`, nghiệm thu. [LOG](../tasks/T-057-ho-so-g4/LOG.md).

- **T-066 — W1, repo lab chạy được; dựng lại exp-obs và máy tải:** SPEC bản 2 Minh duyệt 17/11. Phiên 2 (17/11): xong bước 0–9 (hồi quy V082 trùng byte 2 ca; R9 tổng quát trùng 7/7 gói; cách ly đạt; compose quan sát chạy từ repo lab `ab1c52c`; tuyến một ca `e2e-001` chạy trọn). Bước 10 dừng sớm, giữ Tempo 14 ngày (Minh 17/11). Nhóm 1 và nhóm 2 danh sách xóa đã xử lý (2.6, 2.7 giữ làm đường hoàn tác T-067); giao diện Grafana ca 7ffb2305 đã kiểm (17/11). **Chờ:** commit repo RCA (Minh duyệt), Codex phản biện. Người làm Claude, phản biện Codex. [SPEC](../tasks/T-066-repo-lab-dung-lai-may/SPEC.md), [LOG](../tasks/T-066-repo-lab-dung-lai-may/LOG.md).
- **T-067 — W2, bản FlashTicket thử nghiệm ghim (`rca/exp-2026-11`):** SPEC bản 2 duyệt 17/11. Xong bước 0–9 (18/11): nhánh `36a3725` chạy trên exp-app (image `arm64-t067-36a3725d`, migration `main` áp tại chỗ theo A); kiểm tín hiệu đạt các mục đã khai, bổ sung R1/R2 sau phản biện đạt; tải 1 giờ đạt; danh sách bảo vệ trùng byte. Codex phản biện 3 lượt (chat 18–19/11), đã sửa báo cáo theo phản biện; tiêu chí 2 chấp nhận giới hạn, tiêu chí 8 bỏ (DECISIONS 19/11). **Chờ Minh nghiệm thu.** Còn mở: chặng gateway → kho và `batch` chưa xác định; hoàn tác Collector agent chưa thử; WHY cho ngưỡng log 95%. [SPEC](../tasks/T-067-ban-flashticket-ghim/SPEC.md), [LOG](../tasks/T-067-ban-flashticket-ghim/LOG.md).
- **T-068 — dọn và dựng lại Grafana (P10):** SPEC bản 4 duyệt 18/11; bổ sung phương án A (Minh duyệt 18/11, mục cuối SPEC). Phiên 1–2 (18/11): 4 thư mục tiếng Việt, trang hệ thống, nhãn `t066`; đồ thị dịch vụ đọc trace gốc (`service-graph-4`). Phiên 3 (19/11): Minh duyệt 8 bước sửa theo phản biện Codex; lab `ee91432` (`service-graph-5`) chạy trên exp-obs; kiểm độc lập 84/84 + 1/1, đối chứng âm 16/16, toàn vẹn trước = sau; 26 gói trace ở `/srv/rca-lab/trace-goi/`; bấm thật hết 400; điểm 4 giữ link (Minh). **Chờ:** Minh duyệt WHY-100, WHY-101, DECISIONS và commit repo RCA; Codex kiểm lại (prompt cuối LOG). Người làm Claude. [SPEC](../tasks/T-068-don-grafana/SPEC.md), [LOG](../tasks/T-068-don-grafana/LOG.md).

## Chiến dịch M1-FlashTicket (13–15/11): đã đóng

- T-063 (thu dev bản 2–3), T-064 (chọn **V082** = H5b + H8s1 + H8a; dev bản 3: AC@1 9/11, AC@3 11/11, K 4/6), T-065 (giao diện Grafana): Minh nghiệm thu 15/11 (DECISIONS "M4 chiến dịch…"). OPEN: H3/H4; CPU Payment ở ca không lỗi bản 3; S3 của T-065. [Hồ sơ chọn](../results/T-064/ho-so-chon.md).
- Mục 9: commit/push file nhẹ xong (`25550d2a`, 15/11). Kéo về theo quyết định 16/11 đã xong, cùng gói đầu vào lịch sử của M1 (gói bổ sung, R9, bản chụp mã `goc-*`; Minh duyệt 17/11): `D:/RCA-archive/` (README, danh sách sha256 khớp). Còn: `manifest-3` T-063.
- Dọn đĩa 15/11: nén gzip file nặng chưa track của T-045, T-047, T-048, T-049, T-053 (manifest `results/T-0xx/NEN-2026-11-15.jsonl`, chưa commit); xóa env `py38-gdn`, `py38-rcd`.

## Việc kế tiếp

1. **Tái cơ cấu (Minh 16/11, DECISIONS "Tái cơ cấu hạ tầng RCA…"):** Oracle làm chính; repo vận hành mới [`flashticket-rca-lab`](https://github.com/levanminh04/flashticket-rca-lab) (`D:/Project/flashticket-rca-lab`, commit đầu `a46c009`: cấu hình đang chạy, Grafana, k6, tiêm lỗi; chưa dùng để dựng lại máy); `deploy/rca-test` đã bỏ khỏi PR #17 (`bb84d64`); dữ liệu kéo về `D:/RCA-archive/`. Còn: dựng lại exp-obs và máy tải từ repo mới theo `/opt|/etc|/srv/rca-lab`, rồi dọn máy; chạy dạng Compose trước, bản K8s sau demo.
2. **Kế hoạch bản 3 (Minh duyệt 17/11):** [giai đoạn 2 §8](techstack/KE-HOACH-GIAI-DOAN-2.md). Nhánh demo W0–W5, W8, W9a (chế độ (b) trên FlashTicket); nhánh đánh giá W6–W7 (D14, M7 theo ô), lịch chờ dự toán. D16 hoãn (DECISIONS 17/11). Codex rà 3 lượt; gói sửa S1–S7 Minh duyệt 17/11. Kế tiếp: soạn SPEC W1 và W2.

## Chờ Minh

- P8 (mức LLM), người phụ trách NV1, phạm vi R-07 (kế hoạch §8.5); PR FlashTicket #17 (xung đột với `main`); đóng T-062, T-057.
- Ghi sổ tồn đọng: DECISIONS cho T-044 (phiên 1, lượt 1–4), T-047 (C1/Q-233), Q-224, T-057, M6; WHY cho D-55 và ba đề xuất WHY T-044; QĐ-3–QĐ-6, QĐ-8 (T-045); E-MRP-1…3.
- Code M1 ở nhánh `claude/sweet-hawking-dy078d` (đã push), chưa merge `master`.

## Lưu ý cho mọi agent

- **Máy:** `exp-app` Oracle ARM `129.221.208.47` (2 nhân, 11 GiB; FlashTicket Compose, Toxiproxy, quota CPU Booking 1.0 vẫn bật); `exp-obs` `213.35.116.128` (Prometheus/Loki/Tempo/Grafana + Infinity, compose `-p flash-ticket-obs-pinned`, `pinned/compose.json` sha256 `684d39bd…`; điều khiển tải bằng `tai_linux.py`); **máy tải AWS `3.24.8.49`** (k6 chạy ở đây). Khóa ở `D:/RCA-ext/keys/`, cách gọi `results/T-058/dem-2026-11-10/remote.ps1`. Không copy khóa vào repo/prompt/LOG; không đọc `.env`, `grafana.env`, `~/.bash_history`, `~/.ssh`. Chỉ lệnh đọc; thay đổi trên máy cần Minh duyệt.
- Prometheus `exp-obs` giữ 30 ngày hoặc 40 GB (cờ chạy; dữ liệu từ 10/11 ~20:00Z; ghi "2 ngày" trước đây là sai). Tempo giữ 14 ngày (mặc định), Loki không giới hạn. Truy vấn nặng làm Prometheus khởi động lại → cắt khúc thời gian.
- Repo FlashTicket `D:/Project/flash-ticket-platform`: hook tiêm lỗi ở `src/rca-test/`, chỉ build với `-P rca-test`; bản sao lưu `D:/RCA-ext/backup-flashticket-20261112/`.
- Lỗi đã biết chưa sửa: `src/m1/adapter.py::ca_nezha` không đổi `ParentID = "root"` (WHY-79; sửa khi có lượt Nezha-OB mới).
- Nghiệm thu khi lượt kiểm cuối chưa làm: T-041, T-047, T-051, T-052, T-053, T-054, T-056, T-058, T-059, T-061 (chi tiết ở LOG từng task).

## Nền nghiên cứu

G0/G1/G2 duyệt (Q-36/Q-70/Q-149); P5 đóng (Q-176); G4 duyệt (T-057). RQ2/RQ3/RQ5 OPEN. Test RE2-TT, Nezha-OB, RE3-OB đã dùng một lần cho bản khóa P7(a); phần sau khi xem test báo riêng (C-15 B/Q-247). Eadro không dùng (Q-83). Phần nặng T-032 giữ local (Q-181). OPEN nền: T-041 §8, [OPEN P5](../results/T-040/con-mo.json), [R-01–R-10](../results/T-040/yeu-cau-quan-sat-p9.md).

## Mục lục task đã đóng

| Chặng | Task (liên kết LOG) |
|---|---|
| P0–P2 | [T-000](../tasks/T-000-nen-tang/LOG.md), [T-001](../tasks/T-001-danh-sach-phuong-phap/LOG.md), [T-002](../tasks/T-002-the-dataset-rcaeval/LOG.md), [T-003](../tasks/T-003-the-dataset-ngoai-rcaeval/LOG.md), [T-005](../tasks/T-005-do-kha-thi/LOG.md)–[T-019](../tasks/T-019-the-sock-shop/LOG.md) |
| P3–P4 | [T-020](../tasks/T-020-tong-hop-g1/LOG.md)–[T-034](../tasks/T-034-g2-goi-trinh/LOG.md) (trừ T-027) |
| P5 | [T-035](../tasks/T-035-p5-do-thi-tu-trace/LOG.md)–[T-040](../tasks/T-040-p5b-tong-hop/LOG.md) |
| Chuẩn bị P6, P6 | [T-041](../tasks/T-041-ra-soat-nen-p3-p5/LOG.md)–[T-053](../tasks/T-053-kiem-z-chay-lai-k/LOG.md) |
| P7, G4 | [T-054](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md), [T-055](../tasks/T-055-re3-ban-cuoi/LOG.md), [T-056](../tasks/T-056-phan-tich-bo-sung/LOG.md) |
| Giai đoạn 2 | [T-058](../tasks/T-058-ha-tang-rca-ban-dau/LOG.md), [T-059](../tasks/T-059-danh-muc-loi/LOG.md), [T-061](../tasks/T-061-dinh-dang-ket-qua-rca/LOG.md), [T-063](../tasks/T-063-quan-sat-thu-dev-2/LOG.md), [T-064](../tasks/T-064-m1-flashticket/LOG.md), [T-065](../tasks/T-065-giao-dien-grafana/LOG.md) |

Danh sách đầy đủ từng mã ở `tasks/`. Đóng task không có nghĩa đã phản biện đủ; xem LOG.
