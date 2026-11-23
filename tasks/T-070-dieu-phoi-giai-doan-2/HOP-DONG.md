# Hợp đồng giữa các phiên — giai đoạn 2 (T-070)

Áp dụng cho mọi phiên T-070–T-075 và mọi job Codex do phiên điều phối phát. Chỉ phiên điều phối sửa file này; phiên làm việc thấy cần đổi thì báo về điều phối (kết thúc lượt bằng câu đề xuất), không tự làm khác. I1–I6 từ kế hoạch bản 4 §2.3 (đã sửa theo `thong-nhat.md` §1); I7–I15 thêm ở bản 5.

## I1 — Bản ghi cảnh báo (chủ định dạng: điều phối; T-072 sinh, T-073 tiêu thụ)

Mỗi cảnh báo một bản ghi JSON, ba thời điểm tách riêng:
- `t_hat`: lúc luật chuyển sang firing theo lần đánh giá (lấy từ trạng thái luật của Grafana, không lấy giờ webhook);
- `nhan_webhook_utc`: giờ bộ nhận ghi khi webhook tới;
- `du_lieu_loi`: khoảng dữ liệu lõi RCA thực nhận (T-073 điền).
Kèm: mã luật, nhãn, giá trị tín hiệu lúc kích hoạt, `eval_interval`, `for`. Chế độ (b) không đọc sổ tiêm. Bản 0 của schema: T-072 đề xuất trong `results/T-072/i1-schema.json`, T-073 đọc và báo khác biệt; điều phối chốt và ghi phiên bản vào file này.

**Chốt 20/11/2026 ~14:05Z (điều phối, theo `T072-i1-0` và khác biệt (a)–(e) ở LOG T-073 lượt 2):** schema hiệu lực là `T072-i1-1` (T-072 ra bản), gồm `T072-i1-0` cộng:
- (a) `luat.t072_tin_hieu` thêm giá trị `khong-ro` cho cảnh báo thiếu nhãn `t072_*` (luật lạ, DatasourceError/NoData); bản ghi đó xếp lớp quan sát, không chạy RCA.
- (b) Nguồn t̂ của dịch vụ chỉ `webhook-startsAt`; bỏ tùy chọn `annotation:<khóa>` khỏi T-073.
- (c) `ma` = sha256 của chuỗi `"<fingerprint>|<t_hat.epoch_s dạng số nguyên giây>"`, lấy 16 ký tự hex đầu; schema ghi rõ cách in.
- (d) Nguồn t̂ chuẩn để chấm vẫn là lịch sử trạng thái Grafana (T-072). E3 đo lệch `startsAt` so với lịch sử trạng thái; lệch > 1 nhịp đánh giá thì điều phối mở việc mới, không tự sửa.
- (e) Nhãn quy tắc gom trong code T-073 đổi thành `T072-gom-2` (quy tắc không đổi).

## I2 — Lịch tải nền

Lượt ×1: 3600 s, không tăng bậc. Lượt flash: 1800 s, tăng ×3 ở 600 s (cấu hình ca `124242f0`). Khai trước thứ tự lượt và số phút khỏe cần thu theo mức tải. Biên giữa hai lượt loại khỏi mẫu số. "Không tiêm" ≠ "khỏe": giờ khỏe đạt tiêu chí độc lập (k6: hành trình xong, `dropped_iterations`, 429, lỗi HTTP; cộng kiểm backend). Mất quan sát, quota, suy giảm thật ghi riêng. Liveness ba trạng thái: dò tốt, dò lỗi, thiếu lần dò. Flash chỉ mô tả. Dưới 360 phút ×1 khỏe sau loại trừ thì báo "chưa đủ sáu giờ khỏe ×1".

## I3 — Phân tích nặng

Chỉ trên dữ liệu đã xuất ra file riêng. Không truy vấn Prometheus đang phục vụ đo nền (xem I11).

## I4 — Một chủ theo khung giờ

exp-app, máy tải AWS, Grafana, phần exp-obs chịu tải (Prometheus, Collector capture, `/opt/rca-lab`): mỗi khung một chủ, ghi ở `LICH-MAY.md`. Bàn giao chủ ghi vào `LICH-MAY.md` (dòng nhật ký) và `TRANG-THAI.json` trước khi chủ mới thao tác.

## I5 — Code

Code đang phát triển ở nhánh/worktree riêng (I10). `/opt/rca-lab` (exp-app, exp-obs) chỉ checkout commit đã được Minh duyệt và đã push; cây phải sạch.

## I6 — File chung trong repo RCA

Mỗi phiên chỉ sửa dòng task của mình trong `docs/STATE.md` (I10 cách ghi). `docs/DECISIONS.md`, `docs/WHY.md`, `docs/MRP.md`, `docs/LESSONS.md`, `AGENTS.md` chỉ phiên điều phối ghi, sau khi Minh duyệt.

## I7 — Đổi checkout `/opt/rca-lab` trên máy

Chỉ chủ khung của máy đó đổi, chỉ khi **không có job nào** (runner, `tai_linux`, bộ chuỗi, `inj3`) đang chạy trên máy đó. Lý do: `runner4.py` gọi `stage_m1.py`, `run_m1.py`, `xuat_bo_sung.py`, `safe_export.py`, `sau_v082.py` từ cây git lúc gọi (đổi giữa chừng = đổi code giữa lượt); `tai_linux.py` từ chối khi cây bẩn. Trên exp-obs, `observability/compose.yaml` gắn `./grafana/provisioning` vào Grafana: đổi checkout ở exp-obs **là đổi Grafana** → chỉ ở khung có Grafana (S2, S4). *Làm rõ 20/11 ~14:30Z:* nếu `git diff --stat <cũ> <mới> -- observability/` rỗng thì Grafana không đổi, nên được đổi checkout exp-obs ngoài S2/S4 (vẫn phải không có job, cây sạch, ghi `LICH-MAY.md`). Mỗi lần đổi ghi commit trước/sau vào `LICH-MAY.md`.

## I8 — File STOP

`/srv/rca-lab/runs/STOP` và `/srv/rca-lab/load-controller/STOP` là toàn cục (dừng mọi runner/bộ tải). Chỉ chủ khung tạo/xóa. Phiên khác thấy sự cố thì báo điều phối. Ngoại lệ khẩn (dữ liệu đang hỏng): `tai_linux.py stop --tag <tag của mình>`, rồi báo. **Không bao giờ gọi `tai_linux.py stop` không kèm `--tag`**: bộ lọc `name=^rca-tai-` dừng mọi lượt tải đang chạy (`tai_linux.py:270–275`, CX-01).

## I9 — Vùng ghi trên server

Mỗi task chỉ ghi thư mục mang mã của mình: `/srv/rca-lab/runs/t07x-*`, `/srv/rca-lab/load-runs/<tag t07x-…>` (máy tải), `/home/ubuntu/t07x/` (exp-app). Chỉ mục G1 `/srv/rca-lab/rca-results/t065-l11-001/` chỉ do `sau_v082.py` của runner ghi; T-073 ghi `rca-results/t073-*`. Đổi nguồn hiển thị của dashboard sang vùng T-073 chỉ ở S4.

## I10 — Checkout repo

- **Repo RCA:** mọi phiên dùng chung `D:\RCA-flashticket` (nhiều file chưa commit). Không đổi nhánh, không `git checkout/reset/stash/clean/add/commit`. Chỉ ghi file trong Phạm vi ghi của SPEC mình. File chung (`docs/STATE.md`): chỉ dùng công cụ Edit, đọc lại ngay trước khi sửa, sửa đúng dòng của mình; không dùng Write.
- **Repo lab:** checkout chính `D:/Project/flashticket-rca-lab` giữ ở `main` `407b4f5`, chỉ đọc. Phiên viết code: `git -C D:/Project/flashticket-rca-lab worktree add D:/Project/rca-lab-wt/T-07x -b t07x-<tên> 407b4f5`. Không commit/push khi Minh chưa duyệt (luật cứng 11); khi cần triển khai lên máy, trình diff và commit đề xuất cho điều phối gom trình Minh.
- **FlashTicket** `D:/Project/flash-ticket-platform`: chỉ đọc.

## I11 — Prometheus, Loki, Tempo, Collector capture trên exp-obs

- Trong E2 và E4: chỉ chủ khung (T-071) truy vấn, theo khúc ≤ 10 phút, nghỉ giữa khúc, ưu tiên ở khoảng chuyển lượt hoặc sau khoảng. Phiên khác **không** truy vấn, không chạy `stage_m1`/`xuat_bo_sung` trên dữ liệu sống. Minh xem dashboard bình thường.
- Ngoài E2/E4: truy vấn nhẹ theo khúc được; chạy `stage_m1` trên capture sống cần chủ exp-obs của khung đồng ý (ghi `LICH-MAY.md`).
- Mỗi lượt dài kiểm Prometheus sống và số mẫu để phát hiện sớm mất telemetry.

## I12 — Webhook

Bộ nhận thật của chế độ (b) thuộc T-073. T-072 chỉ dùng bộ nhận nhẹ để kiểm giao nhận ở E3, đường dẫn/cổng riêng, ghi trong `LICH-MAY.md`. Định dạng theo I1.

## I13 — Trạng thái DB

Từ lúc chụp mốc ở E1 tới hết E5: không khôi phục, không sửa dữ liệu DB (DB tích lũy tự nhiên; đo độ trôi). E6 (W6) chỉ sau E5. Mọi sửa dữ liệu khác cần Minh.

## I14 — Codex qua terminal

`codex exec ... -s read-only` cho việc phụ có đầu vào, đầu ra, tiêu chí rõ. Mỗi job có mã việc `CX-nn` và thread ID trong `TRANG-THAI.json`. Hết usage → báo Minh đổi account ngay; mất mạng → thử lại; lỗi lệnh → sửa brief. Không thay lượt phản biện chính thức (AGENTS §9).

## I15 — Trạng thái và báo cáo

`TRANG-THAI.json`, `LICH-MAY.md`, `HOP-DONG.md` chỉ phiên điều phối ghi. Phiên làm việc ghi tiến độ vào LOG task mình (mỗi bước con một dòng, giờ UTC); kết thúc mỗi lượt bằng báo cáo 4 mục (AGENTS §7) cộng: tài nguyên đang giữ, job server đang chạy (tag, máy, lệnh theo dõi), việc cần điều phối quyết. Phiên làm việc **không** mở phiên khác, không gửi prompt sang Codex, không bật lịch.
