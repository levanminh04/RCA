# T-069 — bảng theo ô (sinh bằng `bang_theo_o.py`; nguồn số: `bang-theo-o.json`)

Lượt chính: t069-chinh. Tiêu chí: `tieu-chi.json` (sha256 `600bc7885222…`).

| Ô | Mã cũ → mới | Ghép được | V082 cũ → mới | P7 cũ → mới | Tụt V082 | Nhóm | V082 verdict mới | trung_sha V082 / lặp P7 | Lần lặp V082/P7 |
|---|---|---|---|---|---|---|---|---|---|
| BINH-THUONG | eb48d6b3 → 1e5debb6 | có | k=1 → k=1 | k=1 → k=1 | – | – | CAUSE_FOUND | 1 / 1 | – |
| EVENT-DB-LAT | 4af494a5 → bd976df6 | có | 1 → 1 | 2 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| CPU-BOOK-1 | 19b17e22 → 03573b63 | có | 1 → 3 | 1 → 3 | 1 | a | CAUSE_FOUND | 1 / 1 | – |
| HTTP5-EVENT | e9c9679b → 30ae6ac0 | có | 1 → 2 | 1 → 2 | 0 | a | CAUSE_FOUND | 1 / 1 | – |
| BINH-THUONG | 729604d2 → f4b94c66 | có | k=0 → k=0 | k=1 → k=1 | – | – | NO_INTRINSIC_ANOMALY | 1 / 1 | – |
| REDIS-BOOK | 6949870c → 8bc98881 | có | 1 → 1 | 1 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| FLASH-HEALTHY | fb1cf0e9 → 124242f0 | có | k=1 → k=1 | k=1 → k=1 | – | – | CAUSE_FOUND | 1 / 1 | – |
| NET-GW-BOOK | 5fb8208f → e773f564 | có | 1 → 1 | 1 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| BINH-THUONG | 83073ed1 → a06231fd | có | k=0 → k=1 | k=0 → k=1 | – | – | CAUSE_FOUND | 1 / 1 | – |
| CPU-BOOK-2 | 60166807 → c446b6ae | có | 2 → 1 | 1 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| HTTP5-EVENT-FLASH | 98ea5ba4 → 81de370b | có | 2 → 1 | 2 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| PAUSE-PAYMENT | 46aab4be → 81af0b51 | có | 1 → 1 | 6 → 6 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| BINH-THUONG | f20b0ca5 → b30c9581 | có | k=1 → k=1 | k=1 → k=1 | – | – | CAUSE_FOUND | 1 / 1 | – |
| POOL-EVENT | 86dea661 → 368d7b1e | có | 1 → 1 | 1 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| CONSUMER-BOOK-SLOW-X3 | 659a9dfb1ab0 → 785bfd0c | có | 1 → 1 | 1 → 1 | 0 | – | CAUSE_FOUND | 1 / 1 | – |
| BINH-THUONG-X3 | 1e5a3dc5 → 0bec9eca | có | k=1 → k=0 | k=1 → k=1 | – | – | NO_INTRINSIC_ANOMALY | 1 / 1 | – |
| RECREATE-PAY | ebd5ef38 → c4d7999f | có | 1 → 1 | 6 → 6 | 0 | – | CAUSE_FOUND | 1 / – | – |

**Tổng trên 17 ô ghép được** (AC@1, AC@3 trên 11 ô lỗi; K trên 6 ô không lỗi):

| Bản | AC@1 | AC@3 | Tổng hạng cắt | K |
|---|---|---|---|---|
| V082_cu | 9 | 11 | 13 | 4 |
| V082_moi | 9 | 11 | 14 | 4 |
| P7_cu | 7 | 9 | 23 | 5 |
| P7_moi | 7 | 9 | 24 | 6 |

**Điều kiện dừng:** D1 = 0, D2 = 0, D3 = 0, D4_ung_vien = [], D5 = 0, D4 = 0

**Ô cần lặp theo quy tắc khai trước:** [('CPU-BOOK-1', '19b17e22'), ('HTTP5-EVENT', 'e9c9679b'), ('CPU-BOOK-2', '60166807'), ('HTTP5-EVENT-FLASH', '98ea5ba4')] (vượt 4: 1)

Đối chiếu `cham_dev3.py` nguyên bản: `cham/cham-moi-A.txt` — P7 {'moi': (7.0, 9.0, 24.0, 'K', 6, 'c', 0, 'thieu', 0, 'loi', 1)}
V082-V066+H8a {'moi': (9.0, 11.0, 14.0, 'K', 4, 'c', 0, 'thieu', 0, 'loi', 0)}
