# T-064 — Chú thích thao tác nền ở ca không tiêm lỗi

Sinh bởi `results/T-064/phan-tich/chu_thich_nen.py` từ đầu ra đã lưu; số đầy đủ ở `results/T-064/phan-tich/chu-thich-thao-tac-nen.json`.
Bảng này là báo cáo kèm (tiêu chí §7). **K vẫn đếm thô**, không trừ theo chú thích.
Cột "Gateway" là số đơn vị thao tác của `api-gateway` có cờ thô hướng lên trên tổng đơn vị hợp lệ. Đây là chỉ số thay thế phía M1 cho câu "giao dịch có suy giảm không"; **chưa đối chiếu số liệu k6**.
Với đơn vị `op|…`: ngưỡng `h` và độ vượt tính bằng micro giây; tỉ lệ đuôi = tỉ lệ lần chạy vượt `h`, ghi N → A. Với đơn vị `metric|…`: `h` theo đơn vị của metric đó, n là số mẫu của cửa sổ; kênh log không có các cột này.
Lưu ý mục 3: độ vượt lớn nhất bị bỏ ở nhiều ca nằm sát sàn 1 ms (762–985 µs), nên kết quả K nhạy với giá trị sàn; chưa quét sàn khác.

## 1. Tổng quan

| Tập | Ca | Ô | Bản | Kết luận | Số kênh có cờ | Thực thể có cờ | Gateway |
|---|---|---|---|---|---|---|---|
| dev2 | eb48d6b3 | BINH-THUONG | P7 | CAUSE_FOUND | 4 | booking-service, event-service, payment-service | 0/6 |
| dev2 | eb48d6b3 | BINH-THUONG | V002-H8s1 | CAUSE_FOUND | 1 | event-service | 0/6 |
| dev2 | eb48d6b3 | BINH-THUONG | V028-H1c+H8s1 | CAUSE_FOUND | 1 | event-service | 0/6 |
| dev2 | 729604d2 | BINH-THUONG | P7 | CAUSE_FOUND | 1 | booking-service | 0/6 |
| dev2 | 729604d2 | BINH-THUONG | V002-H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/6 |
| dev2 | 729604d2 | BINH-THUONG | V028-H1c+H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/6 |
| dev2 | fb1cf0e9 | FLASH-HEALTHY | P7 | CAUSE_FOUND | 84 | 7 thực thể | 2/6 |
| dev2 | fb1cf0e9 | FLASH-HEALTHY | V002-H8s1 | CAUSE_FOUND | 58 | 7 thực thể | 2/6 |
| dev2 | fb1cf0e9 | FLASH-HEALTHY | V028-H1c+H8s1 | CAUSE_FOUND | 58 | 7 thực thể | 2/6 |
| dev2 | 83073ed1 | BINH-THUONG | P7 | NO_INTRINSIC_ANOMALY | 0 |  | 0/6 |
| dev2 | 83073ed1 | BINH-THUONG | V002-H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/6 |
| dev2 | 83073ed1 | BINH-THUONG | V028-H1c+H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/6 |
| dev2 | f20b0ca5 | BINH-THUONG | P7 | CAUSE_FOUND | 5 | booking-service, payment-service | 0/6 |
| dev2 | f20b0ca5 | BINH-THUONG | V002-H8s1 | CAUSE_FOUND | 2 | booking-service, payment-service | 0/6 |
| dev2 | f20b0ca5 | BINH-THUONG | V028-H1c+H8s1 | CAUSE_FOUND | 2 | booking-service, payment-service | 0/6 |
| t062 | 00eaea92 | FLASH-HEALTHY | P7 | CAUSE_FOUND | 12 | 5 thực thể | 0/5 |
| t062 | 00eaea92 | FLASH-HEALTHY | V002-H8s1 | CAUSE_FOUND | 9 | 5 thực thể | 0/5 |
| t062 | 00eaea92 | FLASH-HEALTHY | V028-H1c+H8s1 | CAUSE_FOUND | 9 | 5 thực thể | 0/5 |
| t062 | 6c1a9fd8 | BINH-THUONG | P7 | CAUSE_FOUND | 2 | event-service, user-service | 0/5 |
| t062 | 6c1a9fd8 | BINH-THUONG | V002-H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/5 |
| t062 | 6c1a9fd8 | BINH-THUONG | V028-H1c+H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/5 |
| t062 | a5539fba | BINH-THUONG | P7 | CAUSE_FOUND | 2 | keycloak | 0/5 |
| t062 | a5539fba | BINH-THUONG | V002-H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/5 |
| t062 | a5539fba | BINH-THUONG | V028-H1c+H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/5 |
| t062 | e8661e0a | BINH-THUONG | P7 | CAUSE_FOUND | 3 | event-service, ticket-service | 0/5 |
| t062 | e8661e0a | BINH-THUONG | V002-H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/5 |
| t062 | e8661e0a | BINH-THUONG | V028-H1c+H8s1 | NO_INTRINSIC_ANOMALY | 0 |  | 0/5 |

## 2. Kênh có cờ ở ca còn bị kết luận có nguyên nhân dưới V028 (tối đa 8 kênh mạnh nhất mỗi ca)

| Ca | Ô | Thực thể | Đơn vị | Hướng | s | n_N → n_A | Tỉ lệ đuôi N → A | h |
|---|---|---|---|---|---|---|---|---|
| eb48d6b3 | BINH-THUONG | event-service | `op|event-service|event_db` | len | 82.7 | 2677 → 2753 | 0.044 → 0.062 | 1326 |
| fb1cf0e9 | FLASH-HEALTHY | keycloak | `op|keycloak|DELETE keycloak_db.OUTBOX_ENTRY` | len | 569.6 | 300 → 300 | 0.047 → 0.157 | 662 |
| fb1cf0e9 | FLASH-HEALTHY | api-gateway | `metric|api-gateway_workload` | len | 423.2 | 20 → 20 | 0.000 → 0.950 | 5.607 |
| fb1cf0e9 | FLASH-HEALTHY | booking-service | `op|booking-service|GET` | len | 257.3 | 730 → 2164 | 0.047 → 0.077 | 1490 |
| fb1cf0e9 | FLASH-HEALTHY | event-service | `op|event-service|SELECT event_schema.tbl_event_sectors` | len | 218.6 | 720 → 2157 | 0.049 → 0.118 | 1175 |
| fb1cf0e9 | FLASH-HEALTHY | event-service | `op|event-service|Transaction.commit` | len | 215.8 | 1019 → 2456 | 0.040 → 0.090 | 1219 |
| fb1cf0e9 | FLASH-HEALTHY | keycloak | `op|keycloak|SELECT keycloak_db.OFFLINE_CLIENT_SESSION` | len | 208.8 | 71 → 81 | 0.056 → 0.185 | 525 |
| fb1cf0e9 | FLASH-HEALTHY | booking-service | `metric|booking-service_workload` | len | 205.0 | 20 → 20 | 0.000 → 0.950 | 2.794 |
| fb1cf0e9 | FLASH-HEALTHY | event-service | `op|event-service|SELECT event_schema.tbl_ticket_types` | len | 198.6 | 720 → 2157 | 0.046 → 0.095 | 1328 |
| f20b0ca5 | BINH-THUONG | booking-service | `op|booking-service|UPDATE booking_schema.tbl_purchase_limits` | len | 53.4 | 217 → 211 | 0.037 → 0.100 | 840 |
| f20b0ca5 | BINH-THUONG | payment-service | `op|payment-service|SELECT payment_schema.tbl_order_payment_snapshots` | len | 43.9 | 1152 → 1152 | 0.045 → 0.073 | 1543 |
| 00eaea92 | FLASH-HEALTHY | booking-service | `metric|booking-service_workload` | len | 139.0 | 20 → 20 | 0.000 → 1.000 | 1.365 |
| 00eaea92 | FLASH-HEALTHY | api-gateway | `metric|api-gateway_workload` | len | 10.0 | 20 → 20 | 0.000 → 1.000 | 5.253 |
| 00eaea92 | FLASH-HEALTHY | event-service | `metric|event-service_workload` | len | 6.3 | 20 → 20 | 0.000 → 0.950 | 3.003 |
| 00eaea92 | FLASH-HEALTHY | api-gateway | `metric|api-gateway_error` | len | 5.5 | 20 → 20 | 0.000 → 0.900 | 0.630 |
| 00eaea92 | FLASH-HEALTHY | payment-service | `metric|payment-service_workload` | len | 5.5 | 20 → 20 | 0.000 → 0.900 | 0.945 |
| 00eaea92 | FLASH-HEALTHY | ticket-service | `metric|ticket-service_error` | len | 5.2 | 20 → 20 | 0.000 → 0.900 | 0.630 |
| 00eaea92 | FLASH-HEALTHY | ticket-service | `metric|ticket-service_workload` | len | 5.2 | 20 → 20 | 0.000 → 0.900 | 0.630 |
| 00eaea92 | FLASH-HEALTHY | api-gateway | `log|api-gateway|log_loi` | len | 0.7 |  →  |  →  |  |

## 3. Hướng có cờ bị sàn 1 ms (H8-san) bỏ, bản V028

| Ca | Ô | Số hướng bị bỏ | Độ vượt trung bình lớn nhất (µs) | Đơn vị có độ vượt lớn nhất |
|---|---|---|---|---|
| eb48d6b3 | BINH-THUONG | 3 | 762 | `op|booking-service|SELECT booking_schema.tbl_outbox_messages` |
| 729604d2 | BINH-THUONG | 1 | 4 | `op|booking-service|Session.merge com.flashticket.booking_service.entity.PurchaseLimit` |
| fb1cf0e9 | FLASH-HEALTHY | 26 | 977 | `op|payment-service|PaymentWorker.publishOutbox` |
| 83073ed1 | BINH-THUONG | 0 | | |
| f20b0ca5 | BINH-THUONG | 3 | 436 | `op|payment-service|Session.find com.flashticket.payment_service.entity.PaymentAttempt` |
| 00eaea92 | FLASH-HEALTHY | 3 | 985 | `op|payment-service|SELECT payment_schema.tbl_outbox_messages` |
| 6c1a9fd8 | BINH-THUONG | 2 | 551 | `op|user-service|find user_db.tbl_organizer_applications` |
| a5539fba | BINH-THUONG | 2 | 80 | `op|keycloak|DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity` |
| e8661e0a | BINH-THUONG | 3 | 654 | `op|event-service|SELECT event_schema.tbl_outbox_messages` |

## 4. Đọc bảng thế nào

- Quan sát, không phải cơ chế. Cơ chế từng ca và phần chưa xác định ở `results/T-064/phan-tich/ghi-chu-co-che-dev2.md` (Q1, Q4).
- Ca BINH-THUONG còn cờ dưới V028: nguyên nhân chưa xác định (Q4). FLASH-HEALTHY: độ trễ thật tăng dưới tải, việc tính ca này thế nào chờ Minh.

## 5. Bổ sung ca không lỗi bản 3 dưới bản đề xuất V082 (15/11/2026; REVIEW-4 R10)

| Ca | Ô | Thực thể | Đơn vị | Hướng | s | n_N → n_A | Tỉ lệ đuôi N → A | h |
|---|---|---|---|---|---|---|---|---|
| 1e5a3dc5 | BINH-THUONG-X3 (tải ×3 suốt chu kỳ) | payment-service | `metric|payment-service_cpu` | len | 2.765 | 20 → 20 | 0.000 → 0.050 | 0.0816 |
| 7d1ee32f | BINH-THUONG bản 3 (tập độ nhạy, tải ×1) | payment-service | `metric|payment-service_cpu` | len | 3.608 | 20 → 20 | 0.000 → 0.850 | 0.0426 |

Nguồn: `kiem/nhan-luot5/l5/dev3/d0/V082-V066+H8a/<ca>/method-output-1.json#/extra/kenh_co`, `#/extra/don_vi_phan_vi`. Đây là cờ tự sinh duy nhất của mỗi ca; cùng có ở P7. Cơ chế và phần chưa phân xử: `phan-tich/ghi-chu-co-che-dev2.md` Q7.
