# Chạy thử 5 phút — C1

Máy `tai`; cấu hình 5 req/s, 300 giây. Container exit 0.
Gateway: 1501 request; p95 295.659 ms.

| Route | Request | 2xx | 4xx | 429 | 5xx | p95 (ms) |
|---|---:|---:|---:|---:|---:|---:|
| GET /api/v1/events/{id} | 751 | 100.00% | 0.00% | 0.00% | 0.00% | 294.379 |
| GET /api/v1/orders/{id} | 375 | 100.00% | 0.00% | 0.00% | 0.00% | 289.998 |
| GET /api/v1/orders/{id}/payment | 225 | 100.00% | 0.00% | 0.00% | 0.00% | 300.409 |
| GET /api/v1/orders/{id}/tickets | 150 | 0.00% | 0.00% | 0.00% | 100.00% | 295.439 |

429 là tập con của 4xx; không cộng hai cột. Lỗi transport và mã cụ thể ở `phan-tich.json#/routes`.
Refresh thành công: 4; lỗi refresh: 0; HTTP 401: 0; dropped iterations: 0.

Nguồn số: `chay-thu-5p/phan-tich.json#/routes`, `#/counters`, `#/gateway_requests`, `#/p95_ms`; dữ liệu gốc `raw.json`, summary k6 `summary.json`, hash trong `outputs.sha256`.
Chỉ xác nhận vận hành tải trong lượt này. Không suy nguyên nhân lỗi ứng dụng hoặc chất lượng RCA từ số đo phía k6.
