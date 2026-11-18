# T-068 — Báo cáo kiểm

Ngày 18/11/2026. Người làm Claude. SPEC bản 4. Repo lab: `5495877`, sau đó `82e813a` (sửa sau khi bấm thật), `8dccb34` (sửa theo phản biện R1, R2, R5; Minh duyệt 18/11). Repo RCA: chưa commit.

## Kết quả theo tiêu chí xong

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| 1. Chỉ còn 4 folder mới; không còn dashboard lưu trữ hay tạo tay; `loki-1` | **Đạt.** `/api/search` cuối: 4 folder (`rca-bat-dau`, `rca-he-thong`, `rca-su-co`, `rca-phat-lai`), 4 dashboard (`t065-l5-muc-luc`, `flashticket-he-thong`, `t065-l8b-rca`, `t065-l8b-phat-lai`); datasource còn 4 (Infinity, Loki, Prometheus, Tempo). 6 dashboard lưu trữ tự gỡ khi bỏ provider cũ; 9 folder cũ rỗng xóa sau khi `counts` toàn 0; `t061-infinity`, `t058-flashticket`, `loki-1` xóa (HTTP 200). | LOG T-068 các dòng 02:2x–02:28Z; `truoc/grafana-truoc.json` |
| 2. Đồ thị dịch vụ đúng trên 85 cặp | **Đạt.** `dem_doc_lap.py` chạy trên dữ liệu máy: 85/85 khớp, 1 ca "không có đầu ra" (p7/ebd5ef38); 1.404 cạnh liên dịch vụ, 546 cạnh hạ tầng; 0 status lỗi. Đối chứng âm trên bản sao bắt đủ 3 lỗi cài vào. | `kiem/dem-doc-lap-may.json`, `kiem/dem_doc_lap.py` |
| 3. Hồi quy, nhãn, tách đáp án, toàn vẹn | **Đạt** (chi tiết dưới). | — |
| 4. Trang hệ thống: lượng gọi, độ trễ, lỗi | **Đạt.** Cửa sổ ca 7ffb2305: cả 4 panel số (request/giây, p90, 5xx/giây, JVM) có dữ liệu; bản đồ Tempo hiện nút và cạnh; log ứng dụng có dòng. `t058-flashticket` vì vậy đã xóa. | `truoc/prometheus-ca-7ffb2305.json`; bấm thật 02:27Z |
| 5. Ảnh chụp 9 + 2 UID; README nạp lại 90-archive | **Đạt.** | `truoc/grafana-truoc.json`; repo lab `observability/grafana/README.md` |

## Hồi quy bằng bấm thật (trình duyệt trong app, phiên Minh đăng nhập)

| Ca | Bản | Thấy |
|---|---|---|
| 7ffb2305 | V082 | Mục lục mới: dòng `7ffb2305 … t066`; bấm mã → trang sự cố mở `from=2026-11-17T12:20:04.000Z`, `to=…12:30:03.999Z` (= `cua_so_ms[1] − 1`). Đồ thị: tiêu đề "ca 7ffb2305 (t066)", `payment-service` #1 đỏ (tự sinh). |
| ebd5ef38 | P7 | Lần đầu: node graph báo "id field is required in the edges data frame" (danh sách cạnh rỗng). Đã sửa (`82e813a`): hiện nút "không có đầu ra / LOI_CHAY" nối nút "xem bảng trạng thái" bằng cạnh ghi "chú thích, không phải dữ liệu". |
| ebd5ef38 | V082 | Bảng xếp hạng: `payment-service` hạng 1, `tu_sinh`, `so_kenh_co` 35. |
| ebd5ef38 | V071 | Bảng "Cạnh xếp hạng M1-FT": 24 dòng (đếm bằng cuộn hết bảng). |
| 1ad3afeb | P7 → V071 → V082 | Đổi bản bằng menu thật. P7: `keycloak` #2 đỏ (tự sinh). V071, V082: `keycloak` #3 xám (bình thường). Đường dẫn panel gửi đi (ghi bằng móc `fetch` trong trang): `…/service-graph/V071-V041+H8a/1ad3afeb.json`, rồi `…/service-graph/V082-V066+H8a/1ad3afeb.json`. |

Trang phát lại mở được (HTTP 200), nội dung giữ nguyên bản gốc (chỉ đổi `title`, `tags`).

## Cấu trúc dashboard so với bản gốc `ab1c52c`

- Trang sự cố: thêm panel 40 (đồ thị dịch vụ), 41 (chú giải); dịch y +23 cho panel có y ≥ 45; mọi panel cũ còn lại giống hệt; các trường ngoài panel giống hệt trừ `title`, `tags`, `editable`, `version`, `id`.
- Trang phát lại: chỉ khác `title`, `tags`.
- Mục lục: viết mới (không còn liên kết tới 6 UID lưu trữ); bảng ca V082 có `from`/`to`, cột theo thứ tự mã → nguồn → trạng thái → kết luận → từ → đến.
- Tách đáp án: grep `phat_lai|dap_an|tap_chap_nhan|root_khai_truoc` trong 3 trang chính: 0.

## Toàn vẹn

- Mốc (a) 2.143 file lịch sử khớp manifest T-065; (b) 5/5 file khớp danh sách T-066; (c) bản chụp trước `truoc/du-lieu.sha256`.
- Sau triển khai (`sau-du-lieu.sha256`, `sau-du-lieu-2.sha256` trùng nhau): chỉ `V082…/7ffb2305.json` và `V082…/chi-muc.json` đổi, cộng 2 bản sao `.bak-t066` mang hash cũ; so JSON chỉ khác `/nguon_ca` và `/su_co/28/nguon`. `chi-muc-ban.json` giữ `7dfdf42c…`.
- Đầu ra V082 của 7ffb2305 vẫn `183a405d…`; không file nào dưới `/srv/rca-lab/m1` mới hơn chỉ mục T-066. Commit lab chỉ chạm 12 file trong phạm vi ghi.

## Giới hạn và phát hiện

1. **Cạnh hạ tầng không đều giữa các ca (do trường của file ca, không phải lỗi đồ thị).** Trường `dich_quan_sat` được ba nhánh xuất của T-065 sinh theo hai quy ước: 9 ca T-062 (`results/T-065/xuat-du-lieu.mjs:112`, L4 đọc lại bản P7) và 13 ca dev2 (`results/T-065/l4-raw.mjs:20`) ghi `địa chỉ (db.system)`; 6 ca dev3 và mọi ca mới (`l8b-xuat.py:202–203`, nhánh `dev3_template`) chỉ ghi `server.address`. Theo SPEC, đích không ánh xạ được thì không vẽ. Ví dụ 7ffb2305: 125/146 đích không ánh xạ (`127.0.0.1` ×109), chỉ còn cạnh `keycloak → postgresql-shared-instance` (host `postgres`).
2. **DB logic chưa là đích của đồ thị (giới hạn của nguồn đã chọn, không phải của dữ liệu).** Đồ thị T-068 dùng trường `dich_quan_sat` của file ca. Trường này không giữ `db.name`, nên bảng ánh xạ hiện tại dừng ở mức instance. Trace gốc có tên DB logic: ở 29/29 ca, trong cửa sổ phương pháp, span PostgreSQL mang đủ `booking_db`, `event_db`, `payment_db`, `ticket_db`, `keycloak_db`; Redis có `db.system=redis` nhưng không có `db.name`; MongoDB có `user_db` và `admin` (kiểm bởi Codex lượt kiểm lại; số 7ffb2305 trong LOG T-068). Bản trước của mục này viết DB logic "chỉ nhận diện được từ nhãn metric" — sai, đã sửa theo phản biện R4.
   Hướng sửa đã thống nhất, chờ Minh duyệt riêng: (A) đồ thị đọc trace gốc, đếm "span DB phía client" theo cửa sổ ca, đích phải thuộc `classes`; (B) bộ xuất chung ở W5 giữ `db.system`, `db.name` cho mọi nhánh, gồm cả mẫu lịch sử. Chi tiết ở LOG T-068.
3. **Mở trang sự cố chỉ bằng `var-ca`** vẫn giữ khung giờ mặc định 14/11 (hành vi có sẵn). Đường đúng: bấm mã ca trong mục lục hoặc bảng ca.
4. **Đồ thị không là bằng chứng phương pháp.** Cạnh là quan sát trace; không kết luận lợi ích của quan hệ (thuộc D14/W6, RQ3d).
5. Nhãn `t066` nghĩa là tuyến xuất T-066, không phải đợt thu.

## Sửa theo phản biện (Minh duyệt 18/11, lab `8dccb34`)

- R1: link "Mở chi tiết" lấy từ trường `detail__url` của nút, dựng sẵn trong file đồ thị (bản, ca, cửa sổ, dịch vụ). Bấm thật: nút `payment-service` (V082/7ffb2305) mở `var-dv=payment-service`, `from=1794918004000`, `to=1794918603999`; cạnh `event-service → config-discovery` chỉ hiện thông tin, không có link; nút chú thích P7/ebd5ef38 mở panel 3 "Bản, hash, trạng thái và cửa sổ".
- R5: cạnh hạ tầng chỉ vẽ khi đích thuộc `classes`; file đồ thị ghi `dem.dich_ngoai_classes` (85/85 ca = 0). Bộ đếm độc lập kiểm cả điều kiện này và link (`kiem_link`). Đối chứng âm: bỏ `cache` khỏi `classes` của một bản sao → bộ dựng không vẽ cạnh tới `cache` và ghi `ngoai_classes: {cache: 3}`; cài cạnh ngoài `classes`, link trên cạnh, link sai dịch vụ → bộ đếm bắt đủ.
- R2: README bỏ `folder`/`folderUid` khỏi ví dụ provider tạm (chưa chạy thử nạp lại trên Grafana).
- R6, R3: `thay-doi-may.md` sửa cách hoàn tác (giữ `.bak-t066`; sinh lại đồ thị sau khi đổi mã hoặc nhãn) và ghi R3.
- Kiểm lại sau triển khai: `dem-doc-lap-may.json` 85/85; cây `du-lieu` không đổi (`sau-du-lieu-3.sha256`).
