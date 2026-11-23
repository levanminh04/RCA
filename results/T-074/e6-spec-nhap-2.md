# Nháp SPEC bổ sung T-074 — E6 (khung S5), bản 2

- **Trạng thái:** NHÁP, chưa duyệt. Claude (phiên `danh-gia-w6`), 23/11/2026. Thay `e6-spec-nhap.md` (giữ hash ở `SHA256SUMS-4`).
- **Sửa theo:** tự soát S1–S3, S6 (LOG phiên 5); Codex CX-29 #1, #2 và CX-29b (đều **đúng**).
- **Quyết định đã có:** R9 (sửa hạn bán, sức chứa ở E6, sau E5); Q8 (phát E6 khi bản thiết kế đã qua hai phiên Codex); Q9 (E7 được đi trước E6 nếu đủ điều kiện) — `docs/DECISIONS.md` dòng 753, 781–782.
- **Người làm:** Claude (`danh-gia-w6`). **Phản biện:** Codex. **Cổng:** chuẩn bị G6.
- Bản này chỉ gồm việc **cần cho máy**. Phần khóa W7 (không chặn E6) ở `thiet-ke-w6-5.md`.

## 1. Mục tiêu (nhánh K0, đề xuất)

1. Theo R9: đặt hạn bán, ngày diễn và sức chứa của sự kiện tải đủ cho W7 (giá trị đích, mọi bản sao).
2. Chụp **mốc PostgreSQL** sau sửa, ở trạng thái **yên** đã kiểm (đường hoàn tác, mô tả DB đầu W7).
3. Đọc các mục khóa bản ở **trạng thái sau thay đổi cuối cùng được duyệt** (sau E6b nếu có).

Không thu ca RCA, không chạy runner, không phát tải. Không đo khôi phục (nhánh K2 ở §9, chỉ khi Minh chọn K2). Không đặt proxy/quota (E6b riêng).

## 2. Quyền máy (điều phối ghi `LICH-MAY.md`, khung S5)

| Máy | Quyền | Bước | Vì sao |
|---|---|---|---|
| exp-app | **chủ khung**; đọc mọi thứ trừ bí mật; **ghi** đúng các dòng/cột đã duyệt ở bước 1; tạo `/home/ubuntu/t074/` | 0–7 | sửa ngày/sức chứa, dump |
| exp-obs | **chỉ đọc**: `date`/`chronyc tracking`, `git -C /opt/rca-lab rev-parse`, `docker inspect` (khóa bản phía quan sát) | 0, 7 | khóa bản, đồng hồ |
| máy tải AWS | **chỉ đọc**: `date`/`chronyc tracking`, phiên bản k6 (image) | 7 | khóa bản, đồng hồ |
| Grafana, Prometheus | không | — | — |

Không job nào khác ghi DB trong khung (runner, `tai_linux`, `inj3`); bộ điều phối T-073 nếu còn chạy chỉ đọc exp-obs (kiểm ở bước 0). Không đổi checkout `/opt/rca-lab` (I7).

## 3. Phạm vi DB (bước 1 liệt kê, Minh duyệt trước khi ghi)

- **Ghi:** chỉ cột ngày (`sale_ends_at`, `starts_at`, `ends_at`, `checkin_*` và trường tương ứng trong JSON snapshot) và sức chứa (`configured_quantity`, `configured_capacity`, `configuredQuantity` trong JSON) của sự kiện `3e7c1df9-…` và ticket type `ffb36fc7-…`, ở `event_db`, `booking_db`, `ticket_db`, `payment_db`. Đã biết một phần (`results/T-071/e1/sau.jsonl`, `suc-chua.json`); danh sách đầy đủ **chưa kiểm**.
- **Không ghi:** đơn, giữ chỗ, vé, thanh toán, outbox/inbox, bảng khác.
- **Không đọc được (giới hạn ghi rõ):** Redis (`NOAUTH`, `results/T-071/e1/moc-db.json#/bo_sung_luot_2/redis`) và MongoDB `user-db` (cần xác thực). Thông tin xác thực nằm trong cấu hình bí mật, AGENTS §12 cấm đọc. Mốc E6 là **mốc PostgreSQL**; trạng thái Redis/MongoDB không có trong mốc.

## 4. Giá trị đích (đề xuất; câu A3 `cau-hoi-minh-5.md`)

Theo cách đặt giá trị đích (Q2 `thong-nhat.md` §1.2), không "+N ngày":

| Trường | Hiện tại (E1) | Đích |
|---|---|---|
| hạn bán | 2026-12-02T22:16:31.402736Z | 2026-12-30T22:16:31.402736Z |
| bắt đầu diễn, bắt đầu check-in | 2026-12-03T22:16:31.402736Z | 2026-12-31T22:16:31.402736Z |
| kết thúc diễn, kết thúc check-in | 2026-12-04T22:16:31.402736Z | 2027-01-01T22:16:31.402736Z |
| sức chứa | 100.000 | `purchased` đọc ở bước 1 + 1,5 × nhu cầu **cả đợt K0** của phương án ô Minh chọn (`du-toan-4.json#/phuong_an/*/K0_don_ca_dot_bao_thu`; nếu chọn kéo dài tải +90 s thì dùng số ở `thiet-ke-w6-5.md` §7), làm tròn lên nghìn |

Dùng nhu cầu cả đợt (không phải nhu cầu một khối K2) là chủ ý: K0 tích lũy cả đợt; nếu sau này đổi sang K2 vẫn đủ vé (CX-29b mục CX-08 #5).

## 5. Các bước

0. **Kiểm chỉ đọc** (như `results/T-071/e0-trang-thai.md`): container, image, `/opt/rca-lab` sạch, không STOP, không runner/`tai_linux`/`inj3`/`k6`; `inj3 verify` sạch; không tải từ máy tải (không container `rca-tai-*` chạy). Lệch → dừng, báo điều phối.
1. **Liệt kê chỉ đọc** mọi cột ngày/sức chứa liên quan (theo tên cột và khóa `event_id`/`ticket_type_id`, cả trường JSON) ở 4 DB → `danh-sach-cot.json`. Đọc `tbl_ticket_type_inventory` (`purchased`, `held`). Đọc code Event (laptop, chỉ đọc) xem có API sửa sự kiện đã PUBLISHED lan sang các snapshot không. **Dừng, trình Minh:** danh sách dòng sẽ sửa, cách sửa (API hay SQL theo giá trị đích), giá trị sức chứa tính được.
2. **Đưa hệ về trạng thái yên và chụp trước sửa:**
   - Điều kiện yên (khai trước): không tải ≥ 10 phút; đơn ở trạng thái không kết thúc = 0; `held` = 0; outbox chưa gửi = 0 ở 4 DB; mọi hàng đợi RabbitMQ 0 message, 0 unacked (`rabbitmqctl list_queues`, như E1).
   - Chưa yên → chờ tối đa 30 phút (worker hết hạn đơn tự xử lý); vẫn chưa → dừng, báo.
   - Dump `pg_dump -Fc` từng DB; sha256; **đọc lại** các đại lượng yên **sau** dump. Đổi → dump lại (tối đa 2 lần), vẫn đổi → dừng.
3. **Sửa** theo danh sách đã duyệt; ghi giá trị cũ (`truoc.jsonl`) và mới (`sau.jsonl`); đọc lại mọi bản sao.
   - Xác nhận dịch vụ thấy giá trị mới **không bằng giao dịch mua**: gọi `GET /api/v1/events/{id}` và `GET /api/v1/events/{id}/availability` qua gateway từ exp-app (chỉ đọc, không tạo đơn). Phản hồi không chứa trường ngày bán → ghi "chưa xác nhận phía dịch vụ"; lần mua đầu tiên của pilot W7 là phép xác nhận (pilot có SPEC riêng).
   - Nếu service giữ cấu hình trong bộ nhớ (phát hiện ở bước 1 khi đọc code) → khởi động lại đúng service đó là một bước cần duyệt riêng ở bước 1.
4. **Chụp mốc PostgreSQL sau sửa:** kiểm lại điều kiện yên như bước 2; dump từng DB; đọc lại sau dump; `moc-w7.json` (giờ, số dòng bảng chính, tồn kho, outbox, hàng đợi, mock, sha256 dump, giới hạn Redis/MongoDB).
5. *(bỏ — đo khôi phục chỉ ở nhánh K2, §9)*
6. *(bỏ — chu kỳ BINH-THUONG qua runner tạo ca RCA; xem S1/CX-29 #1)*
7. **Khóa bản** (chỉ đọc), sau thay đổi cuối cùng được duyệt (nếu có E6b thì làm **sau** E6b): `docker inspect` Id/RepoDigests mọi container app và quan sát; sha256 file compose hiệu lực; commit `/opt/rca-lab` hai máy; phiên bản k6; độ lệch đồng hồ ba máy → `khoa-ban.json`.
8. LOG, `SHA256SUMS`, báo điều phối, trả S5.

## 6. Đầu ra, phạm vi ghi

`results/T-074/e6/`: `e0-trang-thai.md`, `danh-sach-cot.json`, `truoc.jsonl`, `sau.jsonl`, `yen.json` (kiểm yên trước/sau mỗi dump), `moc-w7.json`, `khoa-ban.json`, `thay-doi-may.md`, `SHA256SUMS`. exp-app `/home/ubuntu/t074/` (dump, nhật ký). LOG T-074, dòng STATE. Không ghi repo lab, FlashTicket, Grafana, Prometheus.

## 7. Lỗi giữa chừng (luật 21; nhánh K0)

| Khi | Ví dụ | Xử lý | Chạy lại | Mất |
|---|---|---|---|---|
| ~10% (bước 0–2) | liệt kê thiếu; hệ không yên; dump lỗi | dừng; chưa ghi gì | bước lỗi | ≤ 30 phút (gồm chờ yên) |
| ~50% (bước 3, sửa dở giữa các DB) | sửa xong Event, lỗi ở Booking | **trả đúng các dòng đã sửa về giá trị cũ** từ `truoc.jsonl` bằng UPDATE theo khóa (không `pg_restore`, để không mất giao dịch hay dòng khác); đọc lại | bước 3 sau khi tìm nguyên nhân | 20–40 phút |
| ~99% (bước 3 xong, đọc lại hoặc xác nhận phía dịch vụ trượt) | một bản sao không nhận giá trị mới | trả mọi dòng về giá trị cũ từ `truoc.jsonl`; đọc lại; máy **giữ ở điều phối**, không giao pilot/W7 cho tới khi trạng thái nhất quán được xác nhận | báo Minh trước khi thử lại | 20–40 phút + thời gian điều tra |
| Bước 4 dump đổi giữa chừng | trạng thái không yên | dump lại (tối đa 2), rồi dừng | bước 4 | ≤ 15 phút |
| Hạ tầng (mất SSH, máy treo) | — | dừng; trước khi tiếp, làm lại bước 0 | — | — |

Đường lui cuối cùng nếu UPDATE ngược không dùng được: `pg_restore` từ dump bước 2 **cho đúng DB bị lỗi**, rồi làm lại bước 3 cho DB đó (dump bước 2 chụp lúc yên nên không mất giao dịch sau đó — không có giao dịch nào giữa bước 2 và 3 vì không có tải). Chạy lại toàn bộ chỉ khi sai giá trị đích hoặc sai DB; trình Minh trước.

## 8. Chi phí ước lượng (CHƯA-KIỂM)

| Bước | Phút |
|---|---|
| 0, 1 (chỉ đọc, đọc code) | 30–45 |
| 2 (chờ yên ≤ 30, dump, đọc lại) | 5–35 |
| 3 (sửa, đọc lại, GET) | 20–40 |
| 4 | 5–15 |
| 7 | 10–15 |
| **Tổng nhánh K0** | **~1,2–2,5 giờ exp-app**, cộng vài phút chỉ đọc ở exp-obs và máy tải |

## 9. Nhánh K2 (chỉ khi Minh chọn K2; cần SPEC bổ sung lần nữa trước khi chạy)

Phải giải quyết trước (CX-29 #2):
- **Quyền Redis/service:** đường xác thực Redis được Minh cấp (không đọc `.env`); quyền dừng/khởi động 7 service app; danh sách nhóm khóa Redis giữ chỗ/cache phải xóa, rút từ code (chưa có).
- **Trạng thái yên trước dump:** như bước 2, cộng Redis không còn khóa giữ chỗ.
- **Tải ngắn tạo chênh:** máy tải AWS + `tai_linux` trên exp-obs **không qua runner** (không tạo ca RCA); ≤ 600 s ×1.
- **Đường lui khi restore dở:** dump trước restore (chụp ở trạng thái yên, đã chứa ngày/sức chứa mới) — không dùng dump E1 hay dump bước 2 (giá trị cũ).
- **Khi kiểm nhất quán trượt và chưa đưa được hệ về trạng thái nhất quán:** giữ máy ở điều phối; **không** giao K0 chạy trên trạng thái đó; báo Minh.
- Thời gian khôi phục thật là số cần đo; không suy từ tốc độ dump E1.
- Bỏ chu kỳ BINH-THUONG qua runner (6(c) cũ); tiêu chí K2 là kiểm nhất quán + một hành trình mua.

## 10. Rủi ro và điều chưa chắc

- Danh sách bản sao ngày/sức chứa chưa đầy đủ; service có thể giữ giá trị trong bộ nhớ.
- Redis/MongoDB ngoài mốc.
- `pg_dump` từng DB không có snapshot chung; dùng điều kiện yên đã kiểm trước và sau dump thay cho snapshot chung.
- Giá trị đích giả định W7 xong trước 23/12.
- Không có giao dịch mua trong E6 → xác nhận "còn bán" phía dịch vụ có thể chỉ hoàn tất ở pilot W7.
