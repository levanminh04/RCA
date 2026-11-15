# C3 — tài nguyên và OOM trong môi trường có agent

**Không đạt ổn định ở cả hai pha.** Booking bị kernel giết vì chạm giới hạn cgroup 512 MiB lúc 21:04:18Z và 21:40:18Z. Cả hai xảy ra trước lỗi chủ động. Host vẫn còn RAM available. Không dùng hai cửa sổ này làm nền sạch hoặc kết quả dung lượng ổn định.

Đây là phép đo 30 phút rảnh + 30 phút tải đọc 1 request/giây theo STEER #3, rút từ SPEC 1 giờ + 1 giờ. Mỗi host có 241 mẫu, bước 15 giây. Hai đầu mút chung dùng cho delta; CPU tính theo khoảng thời gian sau đầu cửa sổ. Dữ liệu gốc và summary giữ nguyên.

| Máy/pha | CPU host trung bình | RAM available nhỏ nhất | Tăng kho, GB/giờ | Restart mới | OOM kernel |
|---|---:|---:|---:|---:|---:|
| app/idle | 20.44% | 59.01% | 0.1207 | 1 | 1 |
| app/light_load | 21.23% | 58.63% | 0.1573 | 1 | 1 |
| obs/idle | 3.26% | 86.50% | 0.8442 | 0 | 0 |
| obs/light_load | 3.25% | 86.55% | 0.8612 | 0 | 0 |

CPU host tính trên toàn máy; Docker CPU 100% tương ứng một logical CPU. GB/giờ là ngoại suy từ tăng byte trong 30 phút, gồm file capture/queue và dữ liệu backend; không phải đo retention ổn định. RAM thực tế khoảng 11,65 GiB app và 10,66 GiB obs, không phải máy 8 GiB của SPEC.

## 1. Bộ nhớ từng JVM trước sửa

Bảng dùng Docker working set từ sampler, không gọi nó là RSS của tiến trình. Số ở đây bao gồm hoạt động bình thường và hai lần restart; không chỉ lấy đỉnh để bỏ phần lỗi.

| Container | Limit MiB | Working set lớn nhất MiB | Tỷ lệ lớn nhất |
|---|---:|---:|---:|
| flash-ticket-api-gateway-api-gateway-1 | 768 | 383.60 | 49.95% |
| flash-ticket-booking-service-booking-service-1 | 512 | 503.60 | 98.36% |
| flash-ticket-discovery-server-discovery-server-1 | 384 | 345.50 | 89.97% |
| flash-ticket-event-service-event-service-1 | 512 | 412.30 | 80.53% |
| flash-ticket-keycloak-keycloak-1 | 768 | 609.70 | 79.39% |
| flash-ticket-payment-service-payment-service-1 | 512 | 488.50 | 95.41% |
| flash-ticket-ticket-service-ticket-service-1 | 768 | 412.50 | 53.71% |
| flash-ticket-user-service-user-service-1 | 768 | 346.80 | 45.16% |

RSS trực tiếp lúc 21:46:37Z của booking là 522868 KiB; payment 528496 KiB; discovery 374236 KiB. RSS gồm trang chia sẻ nên có thể khác số charge của cgroup. `memory-before-fix.json` ghi PID1; riêng PID1 Keycloak là shell, hàng đó **không** dùng làm RSS JVM Keycloak. Theo dõi sau sửa đọc đúng tiến trình `java` trong cgroup.

## 2. Heap và non-heap của booking

| Đại lượng | Nhỏ nhất MiB | Lớn nhất MiB |
|---|---:|---:|
| heap_used | 48.92 | 129.21 |
| non_heap_used | 80.03 | 238.86 |
| heap_committed | 65.96 | 176.54 |
| non_heap_committed | 82.12 | 241.56 |

Nguồn là bốn query Prometheus cố định trong `memory-history.py`; raw matrix ở `memory-heap-history.json`. Bước query 15 giây ở đây chỉ phục vụ mô tả. Đây không phải clock nguồn dùng trong adapter M1.

Heap dùng không đạt limit 512 MiB trong các mẫu đã có; non-heap đáng kể. Điều đó phù hợp với việc giới hạn tổng cgroup bao gồm nhiều vùng ngoài heap. Nó chưa chỉ ra phần nào do agent. Không lấy RSS trừ heap used thành số overhead chính xác: heap used/committed, RSS, working set và bộ nhớ native khác nhau.

OPEN: chưa có đối chứng cùng máy ARM, cùng JDK/revision/tải và không agent. Thông tin máy 84 dùng 512 MiB không tạo được đối chứng có kiểm soát; không truy cập máy 84. Các giải thích còn lại gồm chi phí instrumentation/class metadata, heap/native/JIT/thread của ứng dụng và khác biệt nền ARM/JDK/thư viện. Cần lượt A/B cùng môi trường được duyệt để định lượng Δagent; đêm nay chỉ xác nhận cấu hình có agent này không vừa cgroup cũ.

## 3. Collector và giới hạn quan sát

Các chuỗi receiver_refused xuất hiện đầy đủ có delta 0 ở cả hai Collector trong hai pha; xem `so-do-tai-nguyen.json#/hosts/*/windows/*/collector_counter_series`. Không có chuỗi send_failed/enqueue_failed được xuất trong các mẫu này; không đổi sự vắng mặt đó thành số đo drop SDK bằng 0. Queue max và counter thô được giữ theo từng exporter/loại tín hiệu. Collector không đo được span chưa tới receiver.

`State.OOMKilled` ở các mẫu có thể là false sau automatic restart. Vì vậy `oom_seen=false` trong summary thô không chứng minh không OOM. Báo cáo tổng hợp bổ sung kernel journal, Docker exit137 và delta restart. Docker event buffer chỉ còn giữ lần OOM sau; journal giữ cả hai lần. Nguồn: `unplanned-oom.json`, raw sampler.

## 4. Sửa triển khai theo STEER #4

Sau khi C3 kết thúc, `fix-jvm-memory.py` đổi **compose-exp**: booking/payment/event 512→1024 MiB, discovery 384→768 MiB, Keycloak 768→1536 MiB. Các service còn lại dưới mức cần đổi trong mẫu. Giữ `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC`. Đây là lệch giới hạn so với compose của nhóm/máy 84 được cung cấp; không sửa repo. Chọn khoảng dư lớn hơn 768 MiB cho các JVM 512 MiB vì non-heap đáng kể và thời gian còn lại cần một cửa sổ ổn định; không coi giới hạn mới là tối ưu.

Các container đó và Collector được recreate, log allowlist tạo lại và image Collector ghim lại digest. API được xác nhận ba lần liên tiếp, hoàn tất 21:50:53.940859Z; xem `jvm-memory-fix.json`. Plan v1 giữ nguyên, plan v2 khóa trước M1 và chờ thêm 10 phút ổn định. Monitor mới đọc `memory.events` cgroup, bao gồm `oom_kill`, và RSS đúng tiến trình Java; file `memory-after-fix.jsonl` sẽ là bằng chứng sau sửa. Chưa có phép đo C3 đủ 1h+1h hoặc phép so overhead sau sửa.

C3 trả lời được: giới hạn booking 512 MiB không đủ cho cấu hình hiện tại. Chưa trả lời được máy 8 GiB có đủ hoặc chi phí riêng của agent là bao nhiêu. Không đề xuất tăng toàn máy chỉ từ OOM cgroup khi host còn RAM.

## 5. Theo dõi sau sửa đã kết thúc

`memory-after-fix-summary.json` tổng hợp159mẫu từ21:52:44.371949Z tới22:32:37.978800Z, khoảng39phút54giây giữa mẫu đầu/cuối. Cả tám cgroup không có `oom_kill` hoặc restart mới. Có20mẫu eventpaused theo đúng can thiệp chủ động; không gọi đó là sự cố tự phát.

Mức `memory.current` lớn nhất lấy mẫu chia limit mới: gateway58,42%; booking52,00%; discovery44,12%; event40,66%; Keycloak43,57%; payment49,85%; ticket56,23%; user49,76%. Đây là cgroup charge của monitor sau sửa, khác Docker working set trong bảng trước; không trừ hai bảng để tính overhead. Chưa có bằng chứng ổn định dài hạn hoặc phép đo1h+1h sau sửa.
