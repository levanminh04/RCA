# Nháp SPEC bổ sung T-074 — E6 (khung S5, nhánh K0), bản 3

- **Trạng thái:** NHÁP, chưa duyệt. Claude (phiên `danh-gia-w6`), 24/11/2026. Thay `e6-spec-nhap-2.md` (giữ hash ở `SHA256SUMS-5`).
- **Sửa theo:** Codex CX-32 #1–#4 và CX-32b M1 (đều đúng; bảng đáp ở LOG phiên 6).
- **Quyết định đã có:** R9 (sửa ở E6, sau E5); Q8, Q9; Minh duyệt `results/T-070/cho-duyet-2026-11-23-chieu.md` mục 13–24: A1 **K0**, A2, A3, A4 **mốc PostgreSQL**, B1 **phương án A**, B2 **G = 370 s, không kéo dài tải**; phương án C (E6 là khung máy đầu tiên, W7 sau) — tin điều phối 24/11.
- **Người làm:** Claude. **Phản biện:** Codex. Phần khóa W7 không nằm ở đây (`thiet-ke-w6-5.md`, `con-mo-w6.md`).

## 1. Mục tiêu

1. Đặt hạn bán, ngày diễn và sức chứa của sự kiện tải `3e7c1df9-…` / ticket type `ffb36fc7-…` theo giá trị đích, ở mọi bản sao trong PostgreSQL.
2. Chụp **mốc PostgreSQL** sau sửa ở trạng thái yên đã kiểm.
3. Đọc khóa bản sau thay đổi cuối cùng được duyệt.

Không thu ca RCA; không runner, không tải, không bộ tiêm; không đo khôi phục; không proxy/quota.

## 2. Quyền máy (khung S5; điều phối ghi `LICH-MAY.md`)

| Máy | Đọc (chỉ đọc) | Ghi | Bước |
|---|---|---|---|
| **exp-app** (chủ khung) | `docker ps`, `docker inspect` (container và image), `docker image inspect`; `git -C /opt/rca-lab status --porcelain`, `rev-parse HEAD`; tiến trình (`ps`): `runner4`, `tai_linux`, `inj3`, `_het_han`, `_renew`, `rcaburn`, `k6`; `ls /home/ubuntu/t063/inj/` (file `*.pause-deadline`, `*.pid`) — **không** gọi `inj3.py`; Toxiproxy `GET /proxies` (toxic); `docker inspect -f '{{.State.Paused}}'` mọi container app; lease hook (`/opt/flash-ticket-app/rca-faults/*/control/control.json`, `sudo cat`); `psql` SELECT trên 4 DB nghiệp vụ; `rabbitmqctl list_queues name messages messages_unacknowledged`; `crontab -l`, `systemctl list-timers`; `date`, `chronyc tracking`; sha256 file compose hiệu lực | `psql` UPDATE **đúng các dòng/cột đã duyệt ở bước 1**; `pg_dump -Fc`; tạo `/home/ubuntu/t074/` | 0–7 |
| **exp-obs** | `git -C /opt/rca-lab status --porcelain`, `rev-parse HEAD` (kỳ vọng `1bb40ca` = lab `main`, cây sạch); có/không `/srv/rca-lab/runs/STOP`, `/srv/rca-lab/load-controller/STOP`; `ps` các tiến trình `runner4`, `chuoi_tai`, `tai_linux`, `stage_m1`, `run_m1`, `xuat_bo_sung`, `sau_v082`, `safe_export`, `orchestrator.py`, `k6`; `docker ps` và `docker compose ls` (container `flash-ticket-t073-webhook`, dịch vụ W5); `docker inspect` + `docker image inspect` container quan sát; sha256 file Compose quan sát; `crontab -l`, `systemctl list-timers`; `date`, `chronyc tracking` | không | 0, 7 |
| **máy tải AWS** | `docker ps -a --filter name=rca-tai-` (không container nào **đang chạy**); `ps` k6; `crontab -l`; `docker image inspect` image k6 (phiên bản); `date`, `chronyc tracking` | không | 0, 7 |
| Grafana, Prometheus, Loki, Tempo | không truy vấn | không | — |

Không có quyền: đọc `.env`, `grafana.env`, `~/.bash_history`, `~/.ssh`; Redis; MongoDB; dừng/khởi động bất kỳ container nào; đổi checkout `/opt/rca-lab` (I7).

## 3. Phạm vi DB

- **Ghi:** chỉ các cột ngày bán/diễn/check-in và sức chứa của đúng sự kiện và ticket type trên, ở `event_db`, `booking_db`, `ticket_db`, `payment_db` (cả trường JSON snapshot), theo danh sách bước 1 đã duyệt. Đã biết một phần (`results/T-071/e1/sau.jsonl`, `suc-chua.json`).
- **Cách sửa:** SQL theo giá trị đích, giữ đúng kiểu đã thấy ở E1 (timestamp có phần lẻ micro giây; epoch có phần lẻ trong JSON; `configuredQuantity` là **chuỗi** trong JSON Booking). Không dùng API: đường sửa sự kiện của Event đòi trạng thái `DRAFT`, sự kiện tải là `PUBLISHED` (CX-32 #3, `EventService.java`).
- **Không ghi:** mọi bảng/cột khác (đơn, giữ chỗ, vé, thanh toán, outbox/inbox).
- **Giới hạn (A4):** Redis (`NOAUTH`) và MongoDB `user-db` không đọc, không ghi; mốc E6 là mốc PostgreSQL. Cache Booking có thể còn giá trị cũ sau SQL (không phát sự kiện đổi generation) — chỉ xác nhận ở pilot W7.

## 4. Giá trị đích (A3; ngân sách theo B1 = A, B2)

| Trường | Hiện tại (E1) | Đích |
|---|---|---|
| hạn bán | 2026-12-02T22:16:31.402736Z | 2026-12-30T22:16:31.402736Z |
| bắt đầu diễn, bắt đầu check-in | 2026-12-03T22:16:31.402736Z | 2026-12-31T22:16:31.402736Z |
| kết thúc diễn, kết thúc check-in | 2026-12-04T22:16:31.402736Z | 2027-01-01T22:16:31.402736Z |
| sức chứa | 100.000 | `max(sức chứa hiện tại, purchased_bước1 + 1,5 × 35.640)`, làm tròn lên nghìn |

35.640 = nhu cầu bảo thủ phương án A, dùng lại 3 đối chứng làm mốc, tải 1.800 s (`du-toan-4.json#/phuong_an/0/K0_don_ca_dot_bao_thu`; CX-32b tính lại khớp). Nếu sau này mở rộng ô W7 thì xét lại sức chứa (trình Minh). Ví dụ theo mô hình: `purchased` ≈ 44.000 → 44.000 + 53.460 = 97.460 → 98.000 < 100.000 → **giữ 100.000** (không sửa sức chứa). Số thật đọc ở bước 1.

## 5. Các bước

0. **Kiểm chỉ đọc** theo bảng §2, ghi `e0-trang-thai.md`. Đạt khi: không runner/tải/bộ tiêm/k6 trên ba máy; không container `rca-tai-*` đang chạy; không STOP; `/opt/rca-lab` sạch ở hai máy (exp-obs ở `1bb40ca`); không deadline/pid trong `/home/ubuntu/t063/inj/` (hoặc thư mục không tồn tại); không toxic, không container Paused, không lease hook còn hạn; không cron/timer lạ. **Dịch vụ W5 (`orchestrator.py`, `flash-ticket-t073-webhook`) còn chạy → dừng ở bước 0, trả điều phối** (nó có thể tạo ca từ webhook). Lệch khác → dừng, báo.
1. **Liệt kê chỉ đọc** mọi cột ngày/sức chứa liên quan ở 4 DB (theo tên cột và khóa `event_id`/`ticket_type_id`, cả JSON) → `danh-sach-cot.json` (bảng, khóa, cột, kiểu, giá trị hiện tại). Đọc `purchased`, `held`, sức chứa hiện tại. **Dừng, trình Minh:** danh sách dòng, câu SQL, giá trị đích (gồm sức chứa có giữ nguyên hay không).
2. **Trạng thái yên và dump trước sửa:** điều kiện yên — không tải ≥ 10 phút; đơn ở trạng thái chưa kết thúc = 0; `held` = 0; outbox chưa gửi = 0 ở 4 DB; mọi hàng đợi 0 message, 0 unacked. Chưa yên → chờ tối đa 30 phút rồi dừng. Dump `pg_dump -Fc` từng DB, sha256 → `yen.json` ghi các đại lượng trước và sau dump. Dump chỉ là **hiện vật tham chiếu**, không dùng để restore trong K0.
3. **Sửa theo DB:** với mỗi DB, trong một giao dịch: `SELECT … FOR UPDATE` các dòng đã duyệt → ghi giá trị cũ vào `truoc.jsonl` (trước commit) → UPDATE theo khóa → kiểm số dòng bị ảnh hưởng đúng bằng danh sách → commit. Sau mỗi DB: đọc lại đúng cột, đúng kiểu → `sau.jsonl`. **Đạt** khi mọi bản sao bằng giá trị đích. GET Event công khai (từ exp-app qua gateway): chỉ đối chiếu `startsAt`, `endsAt` (trường nó trả); không trả về → ghi "không đối chiếu được", **không** là trượt. **Không** dùng GET `availability` Booking.
4. **Mốc PostgreSQL sau sửa:** kiểm yên như bước 2; dump từng DB; đọc lại sau dump → `moc-w7.json` (giờ, số dòng bảng chính, tồn kho, outbox, hàng đợi, sha256 dump, giới hạn Redis/MongoDB, ghi chú cache Booking chưa xác nhận).
5. *(không có trong K0)*
6. *(không có trong K0)*
7. **Khóa bản** (chỉ đọc): với mỗi container app và quan sát, lấy `.Image` từ `docker inspect` rồi `docker image inspect` chính ID đó → image ID, `RepoTags`, `RepoDigests` (rỗng với image build cục bộ: vẫn lưu image ID); sha256 file compose hiệu lực; commit `/opt/rca-lab` hai máy; image k6; độ lệch đồng hồ ba máy → `khoa-ban.json`. (Nếu có E6b sau này, làm lại bước 7 sau E6b.)
8. LOG, `SHA256SUMS`, báo điều phối, trả S5.

## 6. Đầu ra, phạm vi ghi

`results/T-074/e6/`: `e0-trang-thai.md`, `danh-sach-cot.json`, `truoc.jsonl`, `sau.jsonl`, `yen.json`, `moc-w7.json`, `khoa-ban.json`, `thay-doi-may.md`, `SHA256SUMS`. exp-app `/home/ubuntu/t074/` (dump, nhật ký). LOG T-074, dòng STATE. Không ghi repo lab, FlashTicket, Grafana, Prometheus.

## 7. Lỗi giữa chừng và hoàn tác (luật 21)

| Khi | Ví dụ | Xử lý | Chạy lại | Mất |
|---|---|---|---|---|
| **~10%** (bước 0–2; chưa ghi DB) | bước 0 lệch; liệt kê thiếu; hệ không yên; dump lỗi | dừng; không có gì để hoàn tác | bước lỗi, sau khi rõ nguyên nhân | ≤ 30 phút (gồm chờ yên) |
| **~50%** (bước 3, giữa các DB hoặc giữa giao dịch) | mất kết nối trong lúc commit; DB thứ hai lỗi | đọc lại từng khóa của các DB đã đụng: cột mang giá trị **cũ** → chưa sửa; mang giá trị **đích** → đã sửa; giá trị **thứ ba** → dừng. Quyết theo Minh: tiếp tục các DB còn lại, hoặc đảo các DB đã sửa — đảo **chỉ** cột còn mang giá trị đích về giá trị cũ trong `truoc.jsonl`, theo khóa, trong giao dịch; đọc lại | bước 3 cho DB còn lại | 20–40 phút (ước lượng cho hoàn tác theo dòng) |
| **~99%** (bước 3 xong, đọc lại không khớp đích; hoặc bước 4 phát hiện giá trị thứ ba) | một bản sao giữ giá trị khác | dừng; không tự đảo nếu gặp giá trị thứ ba hoặc không xác định được tập dòng đã sửa; **giữ máy ở điều phối**, trình Minh; không giao pilot/W7 | theo quyết định Minh | thời gian điều tra |
| Bước 4 không yên giữa hai lần đọc | worker Payment ghi | dump lại (tối đa 2), rồi dừng, trình | bước 4 | ≤ 15 phút |
| Bước 7 lỗi (băm, inspect) | mất SSH | DB đã xác nhận ở bước 3–4 → chỉ làm lại hiện vật thiếu | bước 7 | ≤ 15 phút |
| Hạ tầng (mất SSH, máy treo) | — | dừng; trước khi tiếp, làm lại bước 0 và đọc lại các cột đã sửa | — | — |

Không `pg_restore` trong nhánh K0: restore cả DB đụng dữ liệu ngoài phạm vi (worker Payment chạy định kỳ khi không có tải) và có thể để các DB lệch nhau. Chưa có số đo thời gian restore.

## 8. Chi phí (CHƯA-KIỂM; thay `du-toan-4.json#/viec_them/E6`)

| Bước | Phút |
|---|---|
| 0 (ba máy, chỉ đọc) | 15–20 |
| 1 (liệt kê) + chờ Minh duyệt | 20–30 + thời gian chờ |
| 2 (yên ≤ 30, dump) | 5–35 |
| 3 (sửa, đọc lại) | 20–40 |
| 4 | 5–15 |
| 7 | 10–15 |
| **Tổng** | **~1,3–2,5 giờ exp-app** (chưa gồm thời gian chờ Minh ở bước 1) |

## 9. Rủi ro và điều chưa chắc

- Danh sách bản sao ngày/sức chứa chưa đầy đủ trước bước 1.
- Cache Booking (Redis) và cấu hình trong bộ nhớ service có thể giữ giá trị cũ; E6 không xác nhận được phía dịch vụ — lần mua đầu của pilot W7 xác nhận.
- Redis/MongoDB ngoài mốc.
- Giá trị đích giả định W7 xong trước 23/12.
