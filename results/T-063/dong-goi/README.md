# T-063 — Bộ đóng gói mở rộng (nháp 1, 12/11/2026 22:06Z)

- `xuat_bo_sung.py`: gói metric bổ sung cho M1-FT (22 kênh: H2 throttle/GC/heap/luồng/CPU JVM; H3 pool; H4 queue theo tên queue; H5 restart; H7 theo route; H1 Postgres/Redis). Chạy trên `exp-obs`, chỉ đọc Prometheus, khúc ≤ 10 phút. Định dạng bundle như gói ghim T-058 (bộ ghim `safe-export.py` **không** sửa; gói bổ sung là file riêng).
- **Thử 1** (`thu/bo-sung-1794520800.json`, cửa sổ chứa lần `pause` user-service): 22 kênh, 222 chuỗi, 0 lỗi khúc, ~41 mẫu/chuỗi (bước 15 s, 600 s).
  - `threads-blocked`: 0 chuỗi (JVM không báo trạng thái `blocked` khi số = 0 — vắng = 0, adapter M1-FT phải điền 0 có kiểm).
  - `samples` (`count_over_time(jvm_cpu_recent_utilization_ratio[1m])`): = 1 ở mọi bước, kể cả trong pause — **chưa phân xử**, không dùng; H5 dùng đầu dò hộp đen (`results/T-063/h5/PHAN-TICH.md`).
- **Chưa làm:** wrapper gọi sau mỗi chu kỳ và chép về `results/T-063/ca/<id>/` kèm hash; phục hồi khi stage/M1 lỗi; kiểm thư mục đã tồn tại; adapter M1-FT cho kênh mới (khai `CHANNELS` mở rộng + `ho_so_nguon.kenh_metric.bang`).
