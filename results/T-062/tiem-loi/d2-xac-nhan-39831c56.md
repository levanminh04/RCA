# D2 — xác nhận can thiệp (lượt `d2-39831c56`)

Mỗi ô bật 150 s dưới tải 5 req/s; so cửa sổ 65 s trước bật với [bật+15 s, tắt). Quy tắc: `phan-tich-d2.py`.

| Ô | Xác nhận | Bằng chứng |
|---|---|---|
| EVENT-DB-LAT | **ĐẠT** | RTT PG qua proxy [32.45, 34.15] ms, trực tiếp [0.79, 1.6] ms; p50 event +332 ms; order +-1 ms (đối chứng); lượt k6 bị rơi trong lỗi: 1 |

FLASH-HEALTHY không có can thiệp hệ thống; không thuộc D2 (xác nhận bằng số k6 trong chu kỳ E1).
