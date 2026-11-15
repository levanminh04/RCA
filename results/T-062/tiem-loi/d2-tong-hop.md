# D2 (B4) — tổng hợp xác nhận can thiệp

| Lượt | Tag | Kết quả |
|---|---|---|
| 1 | `d2-93651d4c` (19:22Z) | **Hỏng**: k6 thoát ngay (exit 107) vì `/secret/tokens.json` có BOM UTF-8 khi bộ chạy gọi PowerShell → không có tải. Đầu dò hạ tầng (toxic, RTT) vẫn đúng; hook không chạy vì không có request. Giữ nguyên, không dùng. |
| 2 | (19:49Z) | Bộ chạy (đã thêm bước kiểm k6 sống sau 20 s) dừng ngay vì lỗi trên. Sửa: `chay/tai-e1.ps1` gỡ BOM trên máy tải sau khi ghi token. |
| 3 | `d2-a2a95419` (19:50–20:16Z) | 6 ô, tải 5 req/s đủ. Chi tiết `d2-xac-nhan-a2a95419.md`. |
| 4 | `d2-39831c56` (20:18–20:25Z) | Chỉ EVENT-DB-LAT, cường độ hạ 200→30 ms. Chi tiết `d2-xac-nhan-39831c56.md`. |

## Kết luận từng ô (dùng cho E1)

| Ô | D2 | Bằng chứng chính | Dùng ở E1 |
|---|---|---|---|
| EVENT-DB-LAT | ĐẠT ở 30 ms | RTT PG qua proxy ~33 ms (trực tiếp ~1 ms); GET event p50 +332 ms; order ±1 ms; k6 rơi 1 lượt. Ở 200 ms: GET event +6,3 s, k6 rơi 197 lượt (đổi tải) → không dùng. | có (30 ms) |
| REDIS-BOOK | KHÔNG | Toxic có trên tuyến (PING qua proxy ~202 ms) nhưng không route nào trong hỗn hợp cố định đổi → tải không đi qua Redis Booking | **bỏ** (ghi `chay/lich-sau-d2.json`) |
| NET-GW-BOOK | ĐẠT | health Booking qua proxy ~310 ms (trực tiếp ~9 ms); GET order p50 +297 ms; payment, event không đổi | có |
| HTTP5-EVENT | ĐẠT | audit `http.error.executed` 392; event 5xx 350/350; order 5xx 0/157 | có |
| SLOW-BOOK | ĐẠT | audit `http.delay.started/finished` 200/200; GET order p50 +1002 ms; payment +1, event 0 ms | có |
| CPU-BOOK | ĐẠT | 2 tiến trình đốt trong cgroup Booking; nr_throttled +1266 trong 150 s; cpu.pressure some avg10 52%; hết lỗi về 0 tiến trình; GET order p50 +43 ms | có |
| FLASH-HEALTHY | (không thuộc D2) | không can thiệp hệ thống | có (khám phá; chưa có ngưỡng khỏe khóa) |

Ghi chú trung thực:
- Quy tắc xác nhận EVENT-DB-LAT trong `phan-tich-d2.py` được đổi **sau** khi thấy kết quả lượt 4: ngưỡng cứng 150 ms (viết cho 200 ms) → tỷ lệ theo cường độ (≥ 0,75·L trên tuyến proxy, GET event ≥ +100 ms, đối chứng |Δ| < 100 ms, rơi ≤ 5 lượt). Lý do: cường độ đổi do B4; ý của quy tắc giữ nguyên.
- Lượt 3 chạy lúc phân tích có lỗi chọn nhầm đầu dò của lượt 1 (cùng sổ) → đã sửa lọc theo tag; bảng đúng là bản sau sửa.
- Mọi lần bật lỗi D2 nằm trước E1 và ngoài cửa sổ các ca RCA.
- GET event đọc DB ~30 lần mỗi request (200 ms → +6,3 s): đặc điểm của mã Event (có thể N+1), ghi để nhóm hệ thống xem; không sửa.
