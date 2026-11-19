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
- R5: cạnh hạ tầng chỉ vẽ khi đích thuộc `classes`; file đồ thị ghi `dem.dich_ngoai_classes` (84 đồ thị có bộ đếm = 0; p7/ebd5ef38 không có đầu ra nên `dem` rỗng). Bộ đếm độc lập kiểm cả điều kiện này và link (`kiem_link`). Đối chứng âm: bỏ `cache` khỏi `classes` của một bản sao → bộ dựng không vẽ cạnh tới `cache` và ghi `ngoai_classes: {cache: 3}`; cài cạnh ngoài `classes`, link trên cạnh, link sai dịch vụ → bộ đếm bắt đủ.
- R2: README bỏ `folder`/`folderUid` khỏi ví dụ provider tạm (chưa chạy thử nạp lại trên Grafana).
- R6, R3: `thay-doi-may.md` sửa cách hoàn tác (giữ `.bak-t066`; sinh lại đồ thị sau khi đổi mã hoặc nhãn) và ghi R3.
- Kiểm lại sau triển khai: `dem-doc-lap-may.json` 85/85; cây `du-lieu` không đổi (`sau-du-lieu-3.sha256`).

## Phương án A — đồ thị từ trace gốc (Minh duyệt 18/11; SPEC mục "Bổ sung đã duyệt 18/11 — phương án A")

Mục này thay phần "cạnh hạ tầng" và mục Giới hạn 1–2 ở trên cho đồ thị đang phục vụ. Phiên bản đồ thị: `service-graph-4` (lab `9f4eb5c`; dashboard `6a0def7`).

**Bước 0 rà soát** (`results/T-068/a/ra-soat-tong-hop.json`, chi tiết từng ca `a/ra-soat/<ca>.json`): 29/29 gói trace khớp hash theo manifest; kiểm chéo quan hệ cha–con khác chủ (theo nguồn, đích, N/A) với `canh_thao_tac` của file ca: 0 lệch ở 29/29 ca (trước khi viết bộ dựng); 9/9 ca T-062 không có span RabbitMQ; mọi span DB là CLIENT; `classes` không có `user_db`. Không có điểm CHẶN.

**Đồ thị đang phục vụ (85 cặp):**
- Cạnh dịch vụ → dịch vụ: như cũ về tập cạnh (84 cặp lịch sử: 1.386 cạnh, bằng số phiên 1), thêm số lỗi (status ERROR của span con) và p50/p95 thời lượng span con theo nền/sự cố.
- Cạnh tới DB: theo `db.name` khi là thực thể của ca (booking_db, event_db, payment_db, ticket_db, keycloak_db), redis → `cache`, MongoDB `user_db`/`admin` gộp về `mongodb-instance` (ghi "gộp về instance"). Đơn vị: span DB phía client. 84 cặp lịch sử: 664 cạnh DB.
- RabbitMQ: 168 cạnh PRODUCER (dịch vụ → broker, exchange + routing key) và 168 cạnh CONSUMER (broker → dịch vụ, queue) trên 84 cặp; 27 cặp của 9 ca T-062 không có cạnh broker, nút broker ghi "trace của ca không có span RabbitMQ".
- Span RabbitMQ không phải PRODUCER/CONSUMER (`basic.ack`, `Channel.waitForConfirms`, `confirm.select`) không có exchange/queue → không vẽ, ghi số trong `ghi_chu` (bảng panel 43).
- Ca 7ffb2305 (V082): 18 cạnh dịch vụ, 8 cạnh DB, 3 + 3 cạnh RabbitMQ; `payment-service → payment_db` nền 8.880, sự cố 2; `broker → payment-service` và `payment-service → broker` sự cố 0. 72 span lỗi ở cửa sổ sự cố đều là span của chính `api-gateway` (ghi ở nút, `detail__loi_A`), không là span con của cạnh nào nên mọi cạnh có lỗi 0.

**Kiểm:**
| Phép kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Bộ kiểm độc lập đọc thẳng trace (viết khác bộ dựng) | 84/84 cặp trên laptop + 1/1 (7ffb2305) trên exp-obs = **85/85**, 1 "không có đầu ra" (p7/ebd5ef38) | `kiem/dem-doc-lap-a-laptop.json`, `/srv/rca-lab/runs/t068-a/dem-doc-lap-may-7ffb2305.json` (script cùng sha256 hai đầu) |
| Đối chứng âm | bản gốc 0 lệch; sai số, cạnh ngoài `classes`, link trên cạnh, sai p95, sai cửa sổ (kỳ vọng dịch 1.000 ms) → đều bị bắt; bộ dựng với cửa sổ dịch 1.000 ms dừng ở kiểm chéo, không ghi file | `a/doi-chung-am.json` |
| Cô lập lỗi ở `sau_v082.py` (bản sao trong `t068-a/thu`) | lỗi cố ý và gói sai → status `loi`, file ca không đổi; gọi đúng → đồ thị trùng byte bản sinh thật | LOG phiên 2 |
| Chuyển file | tar trùng sha256 hai đầu; 168/168 file khớp sau giải nén và sau khi chép vào thư mục thật; 170/170 file đồ thị là `service-graph-4`, status `ok` | `a/sg4-laptop.sha256` |
| Toàn vẹn | `a-truoc.sha256` = `a-sau.sha256` (trùng byte; 200 file bảo vệ + 2.184 file `du-lieu`) | |
| Cấu trúc dashboard | panel cũ giống hệt `ab1c52c` sau dịch y +42; chỉ thêm 40–43; grep khóa đáp án: 0 | LOG phiên 2 |
| Bấm thật | 7ffb2305 V082: cạnh tới booking_db, payment_db…, cạnh broker, chi tiết cạnh không có link; bảng số liệu đúng thứ tự cột; ebd5ef38 P7 "không có đầu ra", V082 và V071 17 nút/32 cạnh, payment-service #1; 1ad3afeb V082: 17 nút/22 cạnh, không cạnh broker, nút broker có ghi chú | LOG phiên 2 |

**Thời gian:** sinh 84 file trên laptop 3 phút 52 giây (28 gói, mỗi gói đọc một lần cho 3 bản); 7ffb2305 trên exp-obs 5,9 giây. File đồ thị tổng 1,87 MiB, lớn nhất 24 KiB; truy vấn Infinity của panel 40 mất 173–200 ms. Đo lại khi pane trình duyệt hiện thật (18/11; 3 ca, có/không `var-dv`, mỗi ô một lần; bảng ở LOG T-068 mục "Phiên 2 (tiếp)"): panel 40 vẽ xong sau 7,1–9,9 s kể từ lúc mở URL (lượt đầu 11,3 s); 2–5 s đầu là Grafana khởi động phía trình duyệt (trang danh sách dashboard cũng mất 4,2 s), 8 truy vấn xong trong 1–1,4 s, vẽ 0,5–1 s. `var-dv=` rỗng không làm chậm nhất quán (chênh trong dao động −1,7…+2,1 s). Dashboard đầy đủ với `var-dv=` rỗng: 1 truy vấn biến trả 400, các panel vẫn hiện. Số 10–60 s đo trước đó là do pane bị ẩn.

*Đính chính 19/11 (LOG T-068 phiên 3, đính chính 5–6; đoạn trên giữ nguyên):* truy vấn 400 là của biến `op` (gọi `thao-tac-vue/<ca>/.json` khi `dv` rỗng), không phải biến `dv`; nguồn chính tạo `dv` rỗng là link nút chú thích, đã sửa ở `service-graph-5`. Câu "2–5 s đầu là Grafana khởi động" và "10–60 s do pane bị ẩn" là **suy luận chưa kiểm**: bằng chứng gián tiếp (`document.visibilityState` = `hidden` lúc đo; khi pane hiện đo được 7,1–9,9 s), chưa đo ghép cặp ẩn/hiện.

**Giới hạn còn lại:** đồ thị dùng nguồn khác file ca (trace gốc); file đồ thị ghi `nguon_trace` (đường gói, sha256). Gói trace của 28 ca lịch sử chỉ có trên laptop: muốn sinh lại 84 cặp phải chạy trên laptop rồi chuyển lên (`service_graph.py --tat-ca --nguon-trace results/T-068/a/nguon-trace.json --du-lieu results/T-065/may-l11/du-lieu --ra-do-thi <thư mục>`); `--tat-ca` trên máy dừng nếu thiếu gói. Ca mới qua `sau_v082.py` đọc gói ở `/srv/rca-lab/m1/cases/<ca>`; W5 phải giữ đường tới gói.

*Đính chính 19/11 (LOG T-068 phiên 3, đính chính 3–4):* "28 ca lịch sử chỉ có trên laptop" sai — `46aab4be`, `ebd5ef38` đã có ở `/srv/rca-lab/m1/cases/`, nên 26 gói chỉ có trên laptop; nay 26 gói đã chép lên `/srv/rca-lab/trace-goi/` (xem mục dưới). "`--tat-ca` dừng nếu thiếu gói" nói quá với v4 (chỉ kiểm tên ca); v5 kiểm mọi gói trước khi ghi.

## Sửa theo phản biện Codex lượt phương án A (Minh duyệt 8 bước 19/11; lab `ee91432`, `service-graph-5`)

- **Quy tắc v5:** cạnh chỉ vẽ khi hai đầu thuộc `classes`, phần còn lại ghi `khong_ve`; span DB không phải CLIENT ghi `khong_ve`; bộ đếm kiểm chéo `canh_thao_tac` vẫn tính trên mọi cặp cha–con khác chủ. `--tat-ca` kiểm đủ gói, dựng hết trong bộ nhớ rồi mới ghi. Nút chú thích giữ link panel 3, không đặt `var-dv`/`var-op` (WHY-101, chờ duyệt ghi). `sau_v082.py`: lỗi dựng đồ thị ghi đè `<ca>.json` bằng đồ thị "lỗi dựng đồ thị" thay vì để bản cũ.
- **Khác với v4 trên dữ liệu hiện có:** chỉ trường `phien_ban` (168 file) và 2 URL nút chú thích của p7/ebd5ef38. Dữ liệu hiện có không có cạnh ngoài `classes` và không có span DB không phải CLIENT.

| Phép kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Bộ kiểm độc lập (bỏ miễn trừ `classes` cho cạnh cha–con; kiểm link nút chú thích) | 84/84 cặp trên laptop; 1/1 (7ffb2305) trên exp-obs, cùng sha256 script | `kiem/dem-doc-lap-v5-laptop-2.json` (bản LF; bản `-v5-laptop.json` CRLF giữ lại), `/srv/rca-lab/runs/t068-a/dem-doc-lap-may-7ffb2305-v5.json` |
| Đối chứng âm bản 2 | 16/16 đạt (bộ kiểm: 0, 0b, 1–5, 7, 11, 12; bộ dựng: 6, 8, 9, 10a–c) | `a/doi-chung-am-2.json`, `a/doi_chung_am_2.py` |
| Nhánh lỗi `sau_v082.py` (bản sao `t068-a/thu5`) | lỗi cố ý và gói không tồn tại → đồ thị lỗi + status `loi`; gọi đúng lại → trùng hash cũ; file ca không đổi | LOG phiên 3 |
| Chuyển file | tar trùng sha256 hai đầu; 168/168 khớp; 170/170 file trên máy là `service-graph-5`, status `ok` | `a/sg5-laptop.sha256` |
| Gói trace trên exp-obs | 26 gói, 71 file, `sha256sum -c` 71/71 | `trace-goi.sha256` |
| Toàn vẹn | `p3-truoc.sha256` = `p3-sau.sha256` = `a-sau.sha256` (trùng byte); không file mới dưới `/srv/rca-lab/m1` | |
| Bấm thật (19/11) | 7ffb2305, 1ad3afeb (V082): đủ nút DB logic và broker; p7/ebd5ef38: link nút chú thích mở panel 3, mọi truy vấn 200, console không lỗi — lỗi 400 không còn | LOG phiên 3 |
| CRLF → LF | 6 file đầu ra cũ đổi sang LF, sha256 cũ/mới ghi ở LOG | LOG phiên 3 |

**Điểm 4 (link nút DB/broker/cache):** Minh quyết giữ link (19/11). Trang `dv=booking_db` mở được; ở 84 file ca có cờ M1 trỏ tới thực thể DB, nên trang có bằng chứng cờ. Còn mở: câu "chưa phân xử không phát sinh hay không được thu" ở panel lớp thao tác sai nghĩa với DB (DB không có span riêng theo thiết kế); nguồn `l8b-xuat.py:388`, `sau_v082.py:120`; chưa sửa.
