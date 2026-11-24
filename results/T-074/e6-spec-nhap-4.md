# Nháp SPEC bổ sung T-074 — E6 (khung S5, nhánh K0), bản 4

- **Trạng thái:** NHÁP. Thay `e6-spec-nhap-3.md` (giữ hash `SHA256SUMS-6`). Claude (phiên `danh-gia-w6`), 24/11/2026.
- **Sửa theo:** CX-37, CX-37b (đáp ở LOG phiên 7).
- **Quyền hiện có:** điều phối mở S5 cho **pha đọc** (bước 0–1, lập SQL). **Pha ghi** (bước 2+) chỉ giao sau khi hai phiên Codex kiểm bộ SQL không còn CHẶN và Minh/điều phối giao.
- Quyết định đã có: R9; Q8, Q9; A1 K0, A2, A3 (`purchased` + 1,5 × 35.640, làm tròn lên nghìn), A4 mốc PostgreSQL, B1 phương án A, B2 không kéo dài tải; phương án C.

## 1. Mục tiêu

Pha đọc: xác nhận máy đúng trạng thái bàn giao; đọc mọi bản sao ngày/sức chứa và số tồn kho; lập giá trị đích, danh sách dòng, SQL thuận, SQL nghịch, lệnh kiểm sau ghi.
Pha ghi: sửa đúng các dòng; chụp mốc PostgreSQL; khóa bản.

## 2. Quyền máy

| Máy | Pha đọc (bước 0–1) | Pha ghi (bước 2+, chưa giao) |
|---|---|---|
| exp-app | đọc: `docker ps -a`, `docker inspect`, `docker image inspect`; `git status/rev-parse` `/opt/rca-lab`; `ps -eo pid,args` toàn máy; `ls /home/ubuntu/t063/inj/`; Toxiproxy `GET /proxies` (127.0.0.1:8474); `sudo cat` lease hook; `docker exec postgres psql` **chỉ SELECT**; `rabbitmqctl list_queues`; `crontab -l`, `systemctl list-timers`; `date`, `chronyc tracking`. **Không** gọi `inj3.py`, không GET qua gateway, không ghi file | UPDATE đúng dòng đã duyệt; `pg_dump`; tạo `/home/ubuntu/t074/` |
| exp-obs | đọc: `git status/rev-parse` `/opt/rca-lab` (kỳ vọng `1bb40ca`, sạch); STOP; `ps -eo pid,args`; `docker ps -a`, `docker compose ls`; `docker inspect`/`image inspect`; `crontab -l`, `systemctl list-timers`; `date`, `chronyc tracking`; dùng khóa bộ điều khiển `/etc/rca-lab/controller/` (không đọc nội dung khóa) để SSH sang máy tải | như pha đọc |
| máy tải AWS (qua exp-obs) | `sudo -n docker ps -a --filter name=rca-tai-`; `ps -eo pid,args`; `crontab -l`; `date`, `chronyc tracking`; `docker images` (k6) | như pha đọc |

Không: `.env`, `grafana.env`, `~/.ssh` (đọc), Redis, MongoDB, Grafana/Prometheus, dừng/khởi động container.

## 3. Phạm vi DB

Như bản 3 §3, thêm: `payment_schema.tbl_event_payouts` của sự kiện được **đếm** ở bước 1; có dòng → dừng, trình lại phạm vi. Dump ở pha ghi: `event_db`, `booking_db`, `ticket_db`, `payment_db` (không `keycloak_db`, không ghi gì vào đó).

## 4. Giá trị đích (A3 nguyên văn)

Ngày: như bản 3 §4 (hạn bán 2026-12-30T22:16:31.402736Z; diễn/check-in 31/12 → 01/01/2027). JSON Booking (số epoch): `saleEndsAt` 1798668991.402736, `eventStartsAt` 1798755391.402736, `eventEndsAt` 1798841791.402736.
Sức chứa = `purchased` (bước 1) + 53.460, làm tròn **lên** nghìn. Nếu nhỏ hơn sức chứa hiện tại thì đây là **giảm** sức chứa: ghi rõ ở điểm dừng bước 1, Minh xác nhận.

## 5. Các bước

**Pha đọc**
0. Kiểm chỉ đọc (bảng §2). Đạt khi: exp-app HEAD `407b4f5`, exp-obs HEAD `1bb40ca`, cả hai sạch; không STOP; không tiến trình `runner4`, `tai_linux`, `chuoi_tai`, `inj3`, `_het_han`, `_renew`, `rcaburn`, `k6`, `stage_m1`, `run_m1`, `xuat_bo_sung`, `sau_v082`, `safe_export`, `orchestrator.py` (đọc toàn máy có đối số); không container `rca-tai-*` **đang chạy** (Exited được phép); `flash-ticket-t073-webhook` không chạy (`flash-ticket-t072-bo-nhan` được phép); đủ container kỳ vọng theo `results/T-071/e0-trang-thai.md` và đang chạy, không Paused; không deadline/pid ở `/home/ubuntu/t063/inj/`; không toxic; không lease hook còn hạn; không cron/timer lạ. Lệnh đọc lỗi → "chưa kiểm được" = không đạt. Không đạt → dừng, báo điều phối.
1. Đọc (SELECT): mọi cột ngày/sức chứa của sự kiện/ticket type ở 4 DB (giá trị và kiểu, gồm kiểu JSON); `tbl_ticket_type_inventory` (`configured_capacity`, `held`, `purchased`); đếm payout; trạng thái yên (đơn chưa kết thúc, outbox chưa gửi, hàng đợi). Lập: `results/T-074/e6/doc-buoc1.json`, `gia-tri-dich.json`, `danh-sach-dong.json`, `sql-thuan.sql`, `sql-nghich.sql`, `kiem-sau-ghi.sql`, `SHA256SUMS`. **Dừng**, báo điều phối.

**Pha ghi (chưa giao)**
2. Trạng thái yên (như bản 3 bước 2), dump 4 DB, đọc lại trước/sau dump.
3. Chạy `sql-thuan.sql` từng DB: mỗi DB một giao dịch; `SELECT … FOR UPDATE`; so **mọi** giá trị đã khóa với `doc-buoc1.json` (khác → `RAISE`, rollback, dừng); in `TRUOC` (giá trị cũ) trước UPDATE; UPDATE theo khóa và điều kiện giá trị cũ; kiểm `ROW_COUNT`; in `SAU`; COMMIT. Sau đó `kiem-sau-ghi.sql` (giá trị và kiểu, gồm `jsonb_typeof`).
4. Mốc PostgreSQL: yên, dump, đọc lại.
7. Khóa bản: `.Image` → `docker image inspect` cho **mọi** container kỳ vọng (đối chiếu danh sách E0; thiếu container → không nhận `khoa-ban.json`); compose sha256; HEAD hai máy; k6; đồng hồ.
8. LOG, băm, báo, trả S5.

## 6. Đầu ra

`results/T-074/e6/` như trên + `e0-trang-thai.md`, `yen.json`, `moc-w7.json`, `khoa-ban.json`, `thay-doi-may.md`.

## 7. Lỗi và hoàn tác (luật 21)

| Khi | Xử lý | Mất |
|---|---|---|
| ~10% (pha đọc; bước 2) | chưa ghi dữ liệu nghiệp vụ; dừng; giữ hiện vật dở | ≤ 30 phút chờ yên + ≤ 15 phút dump/đọc lại |
| ~50% (bước 3, mất kết nối lúc COMMIT) | chờ giao dịch cũ kết thúc (`pg_stat_activity` không còn phiên đó); đọc lại dưới khóa; so với nhật ký `TRUOC`: bằng cũ → chưa ghi; bằng đích → đã ghi; khác cả hai → dừng (99%). Trường mà cũ = đích từ đầu không thuộc danh sách sửa (bước 1 đã loại) | 20–40 phút (ước lượng) |
| ~99% (giá trị thứ ba; mất bằng chứng dòng đã sửa; kiểm sau ghi trượt) | dừng; giữ máy ở điều phối; trình Minh. Nếu chỉ thấy cũ/đích: sau khi Minh quyết, chạy `sql-nghich.sql` (đảo từng trường còn mang giá trị đích, có điều kiện; JSON đảo từng đường dẫn, không thay cả tài liệu) | thời gian điều tra |
| bước 7 lỗi | DB đã xác nhận → chỉ làm lại hiện vật | ≤ 15 phút |

Không `pg_restore`.

## 8. Chi phí (CHƯA-KIỂM)

Pha đọc: 30–45 phút. Pha ghi: bước 2 5–35, bước 3 20–40, bước 4 5–15, bước 7 10–15 → 40–105 phút. **Tổng 70–150 phút** (≈ 1,2–2,5 giờ), chưa gồm chờ duyệt giữa hai pha và điều tra khi gặp giá trị thứ ba.

## 9. Phạm vi kết luận

E6 chỉ kết luận: các bản sao trong PostgreSQL mang giá trị đích (đọc lại đúng kiểu). Không kết luận dịch vụ đã dùng giá trị mới (cache, bộ nhớ); một lần mua ở pilot W7 trước 02/12 không phân biệt hai hạn bán.
