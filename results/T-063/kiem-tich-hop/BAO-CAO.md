# T-063 — Kiểm tích hợp trên cấu hình cuối (đáp REVIEW T-063 R2), 13/11/2026

| Lần | Gói | Kết quả | Ghi chú |
|---|---|---|---|
| 1 | `kte4878e` (t 03:09:57Z, cửa sổ pilot L1 sau bảo trì) | P7 **lỗi** adapter `Log service outside the fixed source inventory` | log hạ tầng mang tên compose sau cách A → **TD-09** đổi tên ở Collector |
| 2 | `kteb5f6d` (t 04:03:28Z, tải `kt2-9e85b4` 03:57–04:08Z) | P7 vẫn lỗi | `stage-m1.py:61` đóng gói ±600 s → còn log tên cũ trước TD-09 (03:56:51Z); adapter kiểm tên trên mọi log của gói |
| 3 | `kt57fcd7` (t 04:07:30Z, gói sau TD-09) | stage xong 04:19Z; các bước sau hỏng do **mạng laptop mất** (SSH reset/timeout) | máy chủ không bị ảnh hưởng (kiểm 05:03Z: không khởi động lại, Prometheus restart=0, môi trường sạch) |
| 3 tiếp | `kt57fcd7` | **ĐẠT**: run-m1 `status OK`, hai lần trùng SHA, 39/39 pin; stage và run-m1 lần 2 cùng mã bị chặn (`FileExistsError`, đúng chốt chặn); safe-export + gói bổ sung bản 3 nhận về, hash khớp | [`ket-qua-kt57fcd7.json`](ket-qua-kt57fcd7.json), gói ở `results/T-063/ca/kt57fcd7/` |

**Kiểm R trên gói cuối** ([`kiem-r-kt57fcd7.json`](kiem-r-kt57fcd7.json)): R-02, R-03, R-04 (960/960 PRODUCER/CONSUMER), R-06, R-10 đạt; R-09 0 span mồ côi; R-01 thiếu chỉ ở thao tác điều khiển AMQP (như gói trước bảo trì); R-05 một phần (không đổi); **R-08: 120/3.535 log request Gateway không có span SERVER** — cả 120 có `routeId = unmatched`, đúng nhịp đầu dò liveness Gateway (1/10 s × 1.200 s gói), span bị `filter/health` theo `url.path` bỏ đúng thiết kế (TD-04) → lưu lượng đầu dò, không phải mất giao dịch. Bộ kiểm R cần loại lưu lượng đầu dò khi đánh giá R-08 (ghi giới hạn; không sửa bộ kiểm T-062).

**Span gốc** ([`phan-loai-goc-kt57fcd7.json`](phan-loai-goc-kt57fcd7.json)): job Keycloak nay là `job_hop_le` 612 (TD-08 có tác dụng; trước bảo trì 3.204 SQL gốc); Keycloak `diem_vao_http` 100 = đầu dò `/realms/master` (đều 10 s, cả N và A); CONSUMER gốc 0.

**Kết luận:** đường tải → quan sát → đóng gói → P7 → nhận gói chạy trọn trên cấu hình cuối. Lưu ý vận hành: mọi gói thu phải có cửa sổ ±600 s sau 03:56:51Z 13/11 (TD-09).
