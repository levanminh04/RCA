# Nháp SPEC bổ sung T-074 — E6 (khung S5): sửa hạn bán và sức chứa, chụp mốc W7, đo khôi phục DB

- **Trạng thái:** NHÁP, chưa duyệt. Soạn bởi Claude (phiên `danh-gia-w6`), 23/11/2026, trong `results/T-074/` theo giao việc của điều phối T-070. Khi Minh duyệt, điều phối/người làm chép thành mục bổ sung SPEC T-074 (SPEC T-074 "Phạm vi ghi": "E6 cần SPEC bổ sung khi tới S5").
- **Người làm:** Claude (phiên `danh-gia-w6`). **Người phản biện:** Codex.
- **Cổng:** chuẩn bị G6. **Phụ thuộc:** E5 xong (`results/T-073/e5-ket-qua.md`, 23/11); I13 hết hiệu lực sau E5.

## Mục tiêu

1. Theo **R9** (`docs/DECISIONS.md` dòng 753: "hạn bán và sức chứa vé cho W7: chưa sửa; sửa ở E6 sau E5"): đặt hạn bán và sức chứa của sự kiện tải đủ cho W7 theo phương án ô Minh chọn.
2. Chụp **mốc DB cho W7** sau khi sửa (dump có sha256). Mốc này là điểm khôi phục nếu Minh chọn K2, và là đường hoàn tác.
3. **Đo khôi phục** (chỉ nếu Minh muốn giữ K2 là ứng viên; câu 1 `cau-hoi-minh-4.md`): thời gian và tính nhất quán của PostgreSQL với Redis, RabbitMQ, mock.
4. Ghi các mục khóa bản đọc được bằng lệnh chỉ đọc (digest image, cấu hình hiệu lực, độ lệch đồng hồ; `thiet-ke-w6-2.md` §1).

Không trả lời câu khoa học nào. Không thu ca RCA. Không đặt proxy mới hay quota Event (D2: thuộc W6; nếu Minh chọn phạm vi B/CPU-EVENT thì cần **SPEC riêng E6b** có diff cấu hình đã duyệt).

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác / rủi ro | Phép kiểm | Phần còn mở |
|---|---|---|---|
| Hạn bán, ngày diễn nằm ở những bảng nào? | Sửa sót một bản sao → các service hiểu lệch (như trước E1) | Liệt kê chỉ đọc mọi cột ngày/sức chứa của sự kiện tải ở `event_db`, `booking_db`, `ticket_db`, `payment_db` (đã biết: `event_schema.tbl_events`; `booking_schema.tbl_event_sales_snapshots` cả cột và `configuration_snapshot`; Ticket/Payment snapshot — `results/T-071/e1/sau.jsonl`) | Danh sách đầy đủ **chưa kiểm** |
| Sửa qua API hay SQL? | API (nếu có) phát sự kiện đồng bộ đúng như hệ thống; SQL trực tiếp phải sửa tay mọi bản sao | Đọc code Event (chỉ đọc) xem có đường sửa sự kiện đã PUBLISHED lan sang snapshot không | Chọn khi trình duyệt bước 3 |
| Sức chứa nằm ở đâu? | `event_db.tbl_ticket_types.configured_quantity`, `booking_schema.tbl_ticket_type_inventory.configured_capacity`, `configurationSnapshot.ticketTypes[].configuredQuantity` (`results/T-071/e1/suc-chua.json`, `sau.jsonl`) | Như dòng 1 | — |
| Khôi phục có nhất quán? | Redis còn khóa giữ chỗ/cache cũ; RabbitMQ còn message; outbox/inbox lệch; mock lệch; MongoDB `user-db` không dump được (cần xác thực; `moc-db.json#/bo_sung_luot_2`) | Bước 5–6 | Nếu không nhất quán → K2 loại, giữ K0 |

## Giá trị đích (đề xuất, Minh chọn — câu 8 `cau-hoi-minh-4.md`)

Theo cách đã thống nhất ở Q2 (`thong-nhat.md` §1.2): đặt **giá trị đích**, không "+N ngày".

| Trường | Hiện tại (E1) | Đích đề xuất | Vì sao |
|---|---|---|---|
| `sale_ends_at` (mọi bản sao) | 2026-12-02T22:16:31.402736Z | 2026-12-30T22:16:31.402736Z | ≥ 7 ngày sau giờ kết thúc dự kiến muộn nhất của W7 (chưa có lịch; giả định W7 xong trước 23/12) |
| `starts_at`, `checkin_starts_at` | 2026-12-03T22:16:31.402736Z | 2026-12-31T22:16:31.402736Z | giữ thứ tự bán → diễn như dữ liệu gốc (bán kết thúc 1 ngày trước diễn) |
| `ends_at`, `checkin_ends_at` | 2026-12-04T22:16:31.402736Z | 2027-01-01T22:16:31.402736Z | giữ độ dài diễn 1 ngày |
| Sức chứa (`configured_*`) | 100.000 | `purchased_E6 + nhu_cau × 1,5`, làm tròn lên nghìn | `nhu_cau` = `K0_don_ca_dot_bao_thu` của phương án ô Minh chọn (`du-toan-4.json`); hệ số 1,5 cho lặp/bù và sai số mô hình ×3 |

Ví dụ (không phải số chốt): theo mô hình, `purchased_E6` ≈ 26.166 (E1) + 0,65 × 27.432 (đơn của E2, E4, D1, E3, E5) ≈ 44.000; phương án A+B+CPU-EVENT dùng lại đối chứng (74.520) → 44.000 + 111.780 = 155.780 → 156.000. Số thật đọc ở bước 1.

Mặt trái: thêm một lần sửa dữ liệu nghiệp vụ; ngày diễn chuyển sang 2026–2027 (khác dữ liệu dev); giá trị đích dựa trên giả định W7 xong trước 23/12.

## Đầu vào

`results/T-071/e1/` (`moc-db.json`, `suc-chua.json`, `sau.jsonl`, `sua_ngay.sh`), `results/T-073/e5-ket-qua.md` §6 (trạng thái máy sau E5), `du-toan-4.json`, `thiet-ke-w6-4.md`, HOP-DONG T-070 (I4, I7, I9, I13), `LICH-MAY.md` (S5), cách gọi máy `results/T-058/dem-2026-11-10/remote.ps1`. Không đọc `.env`, `grafana.env`, `~/.bash_history`, `~/.ssh`.

## Đầu ra

- `results/T-074/e6/e0-trang-thai.md` (bước 0), `truoc.jsonl`, `sau.jsonl` (mọi dòng sửa, giá trị cũ/mới), `danh-sach-cot.json` (bước 1).
- `results/T-074/e6/moc-w7.json`: thời điểm, số dòng bảng chính, tồn kho ticket type, outbox, RabbitMQ, Redis keyspace (chỉ đọc), mock, đường dẫn và sha256 dump.
- `results/T-074/e6/khoi-phuc.json` (nếu làm bước 5–6): thời gian từng bước, kết quả từng phép kiểm nhất quán, kết luận K2 khả thi / không.
- `results/T-074/e6/khoa-ban.json`: Id/RepoDigests image các container, sha256 file cấu hình hiệu lực, độ lệch đồng hồ ba máy.
- `results/T-074/e6/thay-doi-may.md`: mọi thay đổi, giờ, hoàn tác. `SHA256SUMS`.

## Phạm vi ghi

Repo RCA: `results/T-074/e6/`, `tasks/T-074-w6-thiet-ke-danh-gia/LOG.md`, dòng T-074 trong `docs/STATE.md`. Máy: exp-app `/home/ubuntu/t074/` (dump, nhật ký); các bảng/cột ngày và sức chứa đã liệt kê ở bước 1 và được duyệt ở bước 3; khôi phục DB (bước 5) chỉ khi Minh chọn. Không ghi repo lab, FlashTicket, Grafana, Prometheus.

## Quyền máy (khung S5, ghi `LICH-MAY.md` bởi điều phối)

- Chủ **exp-app** trong S5; không job nào khác (runner, `tai_linux`, `inj3`, bộ điều phối T-073 phải dừng hoặc xác nhận không ghi DB — E5 §6: bộ điều phối T-073 vẫn chạy; nó chỉ đọc exp-obs, xác nhận lại).
- **Máy tải AWS** và **exp-obs** (runner) chỉ nếu chạy chu kỳ BINH-THUONG ở bước 6c; nếu không thì không cần.
- Không đổi checkout `/opt/rca-lab` (I7).

## Các bước

0. Kiểm chỉ đọc như `results/T-071/e0-trang-thai.md`: container, cây `/opt/rca-lab` sạch, không STOP, không job, `inj3 verify` sạch (gồm Payment đã unpause sau E5). Lệch → dừng, báo.
1. Liệt kê chỉ đọc mọi cột ngày và sức chứa liên quan sự kiện `3e7c1df9-…` ở 4 DB (theo tên cột và theo khóa `event_id`/`ticket_type_id`, cả trường JSON). Ghi `danh-sach-cot.json`. Đọc code Event (laptop, chỉ đọc) xem có API sửa sự kiện PUBLISHED. **Dừng, trình Minh** danh sách dòng sẽ sửa + cách sửa (API/SQL) + giá trị đích.
2. Dump hiện trạng (trước sửa): `pg_dump -Fc` từng DB như E1, sha256 — đường hoàn tác.
3. Sửa theo danh sách đã duyệt; lưu giá trị cũ; đọc lại mọi bản sao; một hành trình mua trọn (k6 smoke 1 vòng hoặc lệnh tay đã có ở T-069) xác nhận còn bán.
4. Chụp **mốc W7**: dump từng DB, sha256; số dòng, tồn kho, outbox, RabbitMQ, Redis keyspace, mock → `moc-w7.json`.
5. *(chỉ nếu Minh giữ K2 là ứng viên)* Tạo chênh có kiểm soát: chạy 1 lượt tải ×1 ngắn (≤ 600 s) để DB khác mốc. Dừng tải. Dừng 7 service app (DB, Redis, RabbitMQ chạy). `pg_restore --clean --if-exists` từng DB nghiệp vụ từ dump mốc W7. Xử lý Redis theo quy tắc khai ở bước 1 (không flush mù; chỉ xóa nhóm khóa giữ chỗ/cache đã xác định). Khởi động service. Đo thời gian từng phần.
6. Kiểm nhất quán sau khôi phục: (a) số dòng mọi bảng chính = `moc-w7.json`; tồn kho `held` = 0, `purchased` = mốc; outbox chưa gửi = 0; mọi hàng đợi 0 message/0 unacked; Redis không còn khóa giữ chỗ mồ côi; liveness 8 đích tốt. (b) Một hành trình mua trọn. (c) *(tùy chọn, ~31 phút)* một chu kỳ BINH-THUONG bằng runner, so tín hiệu nền với đầu E4 (mô tả).
   Bước 6(b) tạo 1 đơn → khôi phục lại một lần nữa nếu muốn mốc sạch (thời gian đo lần 2 làm số lặp).
7. Đọc khóa bản (chỉ đọc): `docker inspect` Id/RepoDigests, sha256 file compose hiệu lực, `chronyc tracking` hoặc so `date` ba máy.
8. Ghi LOG, `SHA256SUMS`, báo điều phối; trả S5.

## Kiểm đúng đắn

Mọi sửa có giá trị cũ, giá trị mới và đọc lại. Dump có sha256 và `pg_restore -l` đọc được. Không suy "K2 khả thi" từ việc lệnh chạy xong: phải đạt đủ 6(a) và 6(b). Không dùng DB đã khôi phục cho ca RCA nào trong E6.

## Tiêu chí xong

Hạn bán và sức chứa đúng giá trị đích ở mọi bản sao; mốc W7 có dump và số dòng; (nếu làm) kết luận K2 khả thi hay không, kèm thời gian đo; khóa bản ghi đủ mục đọc được.

## Không làm

Thu ca RCA; đặt proxy/quota (E6b); sửa lõi, bộ tải, runner; khôi phục về dump E1 (sức chứa và ngày cũ); xóa dữ liệu nghiệp vụ ngoài phạm vi khôi phục đã duyệt; đụng MongoDB `user-db`.

## Chi phí ước lượng (CHƯA-KIỂM, theo E1)

| Bước | Phút |
|---|---|
| 0, 1 (chỉ đọc + đọc code) | 30–45 |
| 2, 4 (dump; E1 mất 16 s cho 90 MB) | 5 |
| 3 (sửa, đọc lại, hành trình) | 20–40 |
| 5 (tải ngắn, dừng, `pg_restore`, khởi động) | 25–40 |
| 6 (a)(b) | 15 |
| 6 (c) tùy chọn | 31 |
| 7 | 10 |
| **Tổng** | **~1,5 giờ (không 5–6) – ~3,0 giờ (đủ)** |

Không tới 1 giờ máy cho riêng một lượt dài; vẫn ghi mục lỗi theo luật 21 vì có sửa dữ liệu.

## Lỗi giữa chừng (luật 21)

| Khi lỗi ở | Ví dụ | Xử lý | Chạy lại gì | Mất |
|---|---|---|---|---|
| ~10% (bước 1–2) | liệt kê thiếu cột; dump lỗi | dừng; chưa sửa gì | làm lại bước lỗi | ≤ 15 phút |
| ~50% (bước 3, sửa dở giữa các DB) | sửa xong Event, lỗi ở Booking | khôi phục các dòng đã sửa từ `truoc.jsonl` (giá trị cũ) hoặc `pg_restore` từ dump bước 2 cho DB đã sửa; đọc lại | bước 3 | 20–40 phút |
| ~50% (bước 5, khôi phục dở) | `pg_restore` lỗi giữa chừng | service đang dừng; khôi phục lại từ dump mốc W7; nếu lỗi lặp → khôi phục dump bước 2, khởi động, kết luận K2 không khả thi | bước 5 | 25–40 phút |
| ~99% (bước 6 trượt kiểm nhất quán) | Redis còn khóa mồ côi, hàng đợi có message | ghi kết quả "không nhất quán"; đưa hệ về mốc W7 đã kiểm (hoặc trạng thái sau bước 4 nếu chưa khôi phục); **K2 loại, giữ K0** | không chạy lại phép đo; báo Minh | 0 thu thêm |

Lỗi hạ tầng (mất SSH, máy treo): dừng, giữ nguyên trạng, kiểm lại bước 0 trước khi tiếp. Chạy lại toàn bộ chỉ khi sai giá trị đích hoặc sai DB (tính đúng); trình Minh trước.

## Rủi ro và điều chưa chắc

- Danh sách bản sao ngày/sức chứa chưa đầy đủ; có thể còn cache trong Redis hoặc trong bộ nhớ service (cần khởi động lại service để đọc giá trị mới — kiểm ở bước 3 bằng hành trình mua).
- MongoDB `user-db` không dump được; nếu tải ghi vào đó, khôi phục chỉ PostgreSQL không trả hệ về mốc hoàn toàn (ghi giới hạn).
- `pg_dump` từng DB không có snapshot chung; an toàn vì dump khi không có tải (như E1).
- Giá trị đích dựa trên giả định W7 xong trước 23/12.
