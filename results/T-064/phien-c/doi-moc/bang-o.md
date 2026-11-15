# Dời mốc ±30 s — bảng theo ô (phiên C, T-064)

Nguồn: `results/T-064/phien-c/cham/doi-moc.json` (`cham_phien_c.py`, spec `cham/spec-doi-moc.json`). Ô lỗi: hạng kỳ vọng của đáp án (quy ước hòa P7(a); — = không có trong thứ hạng). Ô không lỗi: K = 1 nếu kết luận khác `NO_INTRINSIC_ANOMALY`. Cạnh: hạng kỳ vọng của cạnh đáp án trong bảng cạnh (V041). Vai trò: kiểm độ nhạy, **không dùng để chọn**.

## 13 ca dev bản 2 (tập chọn)

| Ca | Ô | P7 | P7 −30 | P7 +30 | V032 | V032 −30 | V032 +30 | V041 | V041 −30 | V041 +30 | P7 −300 (thử giả) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| eb48d6b3 | BINH-THUONG | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=0 | K=1 | K=1 |
| 4af494a5 | EVENT-DB-LAT | 2 | 2 | 1 | 2 | 2 | 1 | 1 / cạnh 2 | 1 / cạnh 2 | 1 / cạnh 2 | 2 |
| 19b17e22 | CPU-BOOK-1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 |
| e9c9679b | HTTP5-EVENT | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 2.5 | 2.5 | 10.5 |
| 729604d2 | BINH-THUONG | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=0 | K=0 | K=0 | K=1 |
| 6949870c | REDIS-BOOK | 1 | 1 | 1 | 1 | 1 | 1 | 1 / cạnh 2 | 1 / cạnh 2 | 2.5 / cạnh 30.5 | 2 |
| fb1cf0e9 | FLASH-HEALTHY | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 |
| 5fb8208f | NET-GW-BOOK | 1 | 1 | 1 | 1 | 1 | 1 | 1 / cạnh 2 | 1 / cạnh 2 | 1 / cạnh 2 | 1 |
| 83073ed1 | BINH-THUONG | K=0 | K=1 | K=1 | K=0 | K=1 | K=1 | K=0 | K=1 | K=0 | K=1 |
| 60166807 | CPU-BOOK-2 | 1 | 1 | 1 | 1 | 1 | 1 | 2.5 | 4 | 1 | 2 |
| 98ea5ba4 | HTTP5-EVENT-FLASH | 2 | 1 | 3 | 2 | 1 | 3 | 2.5 | 1 | 4 | 10 |
| 46aab4be | PAUSE-PAYMENT | — | 3 | — | 1 | 1 | 3 | 1 | 1 | 3 | 10 |
| f20b0ca5 | BINH-THUONG | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 |
| **Tổng** | AC@1 / AC@3 / tổng hạng cắt / K | 5 / 7 / 15 / 4 | 5 / 8 / 12 / 5 | 5 / 7 / 16 / 5 | 6 / 8 / 10 / 4 | 6 / 8 / 10 / 5 | 5 / 8 / 13 / 5 | 6 / 8 / 11 / 3 | 6 / 7 / 12.5 / 3 | 4 / 7 / 16 / 3 | 1 / 5.133 / 25.99 / 5 |

## 9 ca T-062 (không hồi quy)

| Ca | Ô | P7 | P7 −30 | P7 +30 | V032 | V032 −30 | V032 +30 | V041 | V041 −30 | V041 +30 | P7 −300 (thử giả) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 00eaea92 | FLASH-HEALTHY | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 |
| 1ad3afeb | EVENT-DB-LAT | 1 | 1 | 1 | 1 | 1 | 1 | 1 / cạnh 2 | 1 / cạnh 2 | 1 / cạnh 3 | 1 |
| 2e2a5541 | SLOW-BOOK | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10.5 |
| 6c1a9fd8 | BINH-THUONG | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=0 | K=0 | K=0 | K=1 |
| a5539fba | BINH-THUONG | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=0 | K=1 | K=0 | K=1 |
| a89954d1 | HTTP5-EVENT | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 9 |
| bf17acbf | CPU-BOOK | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10.5 |
| e8661e0a | BINH-THUONG | K=1 | K=1 | K=1 | K=1 | K=1 | K=1 | K=0 | K=0 | K=0 | K=1 |
| f728fce2 | NET-GW-BOOK | 1 | 1 | 3 | 1 | 1 | 3 | 1 / cạnh 2 | 1 / cạnh 2 | 2 / cạnh 25.5 | 7.33333 |
| **Tổng** | AC@1 / AC@3 / tổng hạng cắt / K | 5 / 5 / 5 / 4 | 5 / 5 / 5 / 4 | 3 / 5 / 8 / 4 | 5 / 5 / 5 / 4 | 5 / 5 / 5 / 4 | 3 / 5 / 8 / 4 | 5 / 5 / 5 / 1 | 5 / 5 / 5 / 2 | 4 / 5 / 6 / 1 | 1.059 / 1.31 / 22.93 / 4 |

