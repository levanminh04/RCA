# T-071 — lệnh lượt E3 (a) `t071-e3-duong-01` (soạn 21/11, chưa phát)

Mục đích (Minh duyệt (a), LOG T-070 lượt 4): một lượt ×1 1800 s ở E3 để kiểm luật ngưỡng thử của T-072 dưới tải và đo phần thời gian còn thiếu của mục tiêu 25 phút (d). **Ngoài mẫu số E2/E4**: không vào `phan-loai-phut.json` của E2 hay E4. Phát bằng `tai_linux.py` (một lượt, không cần `chuoi_tai.py`).

**Điều kiện phát** (điều phối ghi khung và giờ ở `LICH-MAY.md` — bảng S2 hiện ghi exp-app/máy tải "nghỉ", cần sửa cho lượt này trước khi phát):

- luật thử của T-072 đã nạp và đang đánh giá; T-072 sẵn sàng thu bằng chứng cảnh báo;
- không job khác; không STOP; `/opt/rca-lab` exp-obs `e9a0857` sạch; exp-app `407b4f5` sạch; `inj3.py verify` sạch;
- máy tải 0 container `rca-tai-` chạy; chưa có `/srv/rca-lab/load-runs/t071-e3-duong-01`.

## 1. Đếm đơn trước (exp-app, chỉ đọc)

```sh
docker exec flash-ticket-infra-postgres-1 psql -U postgres -d booking_db -At -F'|' -c "select now(), lifecycle_state, count(*) from booking_schema.tbl_orders group by 2 order by 2"
docker exec flash-ticket-infra-postgres-1 psql -U postgres -d booking_db -At -F'|' -c "select configured_capacity, held, purchased from booking_schema.tbl_ticket_type_inventory where ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453'"
```

Ghi vào `results/T-071/e3/don-truoc.txt`.

## 2. Phát và theo dõi (exp-obs)

```sh
cd /opt/rca-lab && python3 load/controller/tai_linux.py start --tag t071-e3-duong-01 --seconds 1800
cd /opt/rca-lab && python3 load/controller/tai_linux.py get --tag t071-e3-duong-01      # chờ Running=false (~31 phút)
cd /opt/rca-lab && python3 load/controller/tai_linux.py receive --tag t071-e3-duong-01  # khi đã dừng; kiểm hash
```

`start` trả ngay sau `docker run` (preflight ~30 s ở E2). Dừng khẩn: `tai_linux.py stop --tag t071-e3-duong-01` (luôn có `--tag`, I8).

## 3. Đếm đơn sau và ghi riêng số đơn tạo thêm

- Chạy lại hai câu ở mục 1 sau `receive` → `results/T-071/e3/don-sau.txt`.
- Số đơn tạo thêm của lượt = tổng đơn sau − tổng đơn trước, theo trạng thái; đối chiếu với `create_order` 201 trong `tai-out/t071-e3-duong-01/container.log` và `summary.json` (ước danh nghĩa: 1800 s × 0,36 ≈ 648 đơn, ~2/3 hoàn tất). Ghi `results/T-071/e3/don-tao-them.json`, tách khỏi số của E2/E4 (Minh (a): ghi riêng đơn tăng thêm giữa E2–E4).

## 4. Xuất (nếu T-072 cần chuỗi của lượt)

`xuat_chuoi.py` với `bieu-thuc.json` (hoặc bản luật thử T-072 chỉ định) cho cửa sổ [StartedAt − 600 s, FinishedAt + 300 s], khúc ≤ 600 s; ra `/srv/rca-lab/runs/t071-e3-duong-01-xuat/`; kéo về `results/T-071/e3/` kèm hash hai đầu.

## Lỗi giữa chừng (luật 21, lượt 31 phút — dưới ngưỡng 1 giờ, ghi cho đủ)

- Start lỗi: không có dữ liệu, phát lại với tag mới `t071-e3-duong-02` cần điều phối đồng ý (tag không tái dùng).
- Container thoát lỗi hoặc mất telemetry giữa lượt: giữ, receive, ghi loại; T-072 quyết dùng được phần nào.
- Mất kết nối laptop: lượt chạy trên máy tải, 0 phát lại; nối lại thì `get` / `receive`.
