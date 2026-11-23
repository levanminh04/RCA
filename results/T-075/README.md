# T-075 — W8: LLM giải thích tối thiểu (lượt 1, ngoại tuyến)

Lượt 1 ngày 23/11/2026 làm bước 2–3 của SPEC ở chế độ ngoại tuyến, theo Q6 và Q7 (DECISIONS 23/11). Lượt này không gọi LLM và không gửi dữ liệu ra ngoài.

| File | Nội dung |
|---|---|
| `khuon-dau-vao.md` | Khuôn gói bằng chứng `T075-vao-1`; danh sách trường đề xuất gửi đi; trường loại bỏ |
| `khuon-dau-ra.md` | Khuôn đầu ra `T075-ra-1`; bộ kiểm K1–K9; giới hạn |
| `prompt-mau.md` | Lời hệ thống mẫu, chưa thử với model |
| `de-xuat-minh.md` | Điểm cần Minh quyết: trường gửi đi, nhà cung cấp/model, xử lý khi trượt, file G1 ca E5 |
| `goi_bang_chung.py` | Dựng gói từ file G1 0.5 (kèm `che_do_b`) hoặc file sự cố T-073 |
| `kiem_w8.py` | Bộ kiểm đầu ra (K1–K7) |
| `chay_thu.py` | Chạy thử trên 3 ca thật và 3 ca giả; K8, K9, đối chứng chéo |
| `ca-thu/<ca>/` | `goi.json` (sinh ra); `dau-ra-*.json` (viết tay); `dau-ra-sinh-*.json` (sinh từ đột biến) |
| `ket-qua-thu.json`, `ket-qua-thu.md` | Kết quả thử |
| `SHA256SUMS` | Hash các file trên |

Cách chạy lại (Python 3.12, chỉ thư viện chuẩn):

```
cd results/T-075
py -3 -I -X utf8 chay_thu.py
```

Kiểm một đầu ra:

```
py -3 -I -X utf8 kiem_w8.py ca-thu/e5/goi.json ca-thu/e5/dau-ra-dung.json
```
