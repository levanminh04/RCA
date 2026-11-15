# D2 — xác nhận can thiệp (lượt `d2-a2a95419`)

Mỗi ô bật 150 s dưới tải 5 req/s; so cửa sổ 65 s trước bật với [bật+15 s, tắt). Quy tắc: `phan-tich-d2.py`.

| Ô | Xác nhận | Bằng chứng |
|---|---|---|
| EVENT-DB-LAT | **ĐẠT** | RTT PG qua proxy [202.54, 208.38] ms, trực tiếp [0.97, 11.94] ms; p50 event +6304 ms; order +-1 ms (đối chứng); lượt k6 bị rơi trong lỗi: 197 |
| REDIS-BOOK | **KHÔNG** | Redis PING qua proxy [204.01, 202.38] ms, trực tiếp [1.98, 1.86] ms; p50 order +-2, payment +-5, event +-3 ms; toxic có trên tuyến nhưng các route trong hỗn hợp tải không đổi → tải không đi qua Redis của Booking; lượt k6 bị rơi trong lỗi: 0 |
| NET-GW-BOOK | **ĐẠT** | health Booking qua proxy [310.1, 311.4] ms, trực tiếp [8.7, 9.3] ms; p50 order +297, payment +-4, event +-2 ms (đối chứng); lượt k6 bị rơi trong lỗi: 0 |
| HTTP5-EVENT | **ĐẠT** | audit Event: {'http.error.executed': 392}; event 5xx 350/350; order 5xx 0/157 (đối chứng); lượt k6 bị rơi trong lỗi: 0 |
| SLOW-BOOK | **ĐẠT** | audit Booking: {'http.delay.finished': 200, 'http.delay.started': 200}; p50 order +1002, payment +1, event +0 ms; lượt k6 bị rơi trong lỗi: 0 |
| CPU-BOOK | **ĐẠT** | burn_procs 2,2,0; nr_throttled 1850→3116→3192; pressure lúc lỗi: some avg10=52.27 avg60=46.88 avg300=19.98 total=196281606; p50 order +43, event +-2 ms; lượt k6 bị rơi trong lỗi: 0 |

FLASH-HEALTHY không có can thiệp hệ thống; không thuộc D2 (xác nhận bằng số k6 trong chu kỳ E1).
