# Dữ liệu

Thư mục `data/` không đưa vào git, trừ file này. Mỗi bộ dữ liệu có trong đây phải có một mục bên dưới, đủ để dựng lại trên máy mới: nguồn, revision, cách lấy, kích thước, cách kiểm.

`data/locked/` chứa dữ liệu chưa ai nhìn, để dành cho tập test hoặc dataset giữ ngoài, và file chứa nhãn của chúng. Không đọc nội dung trước cổng G3 (AGENTS luật cứng 1). Tính hash để kiểm toàn vẹn thì được, vì không đọc nội dung.

## RCAEval — revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`

- **Nguồn:** Hugging Face `phamquiluan/RCAEval`, giấy phép MIT.
- **Cách có:** chép ngày 02/10/2026 từ lần tải trước (20–27/09/2026), theo Q-21.
  - Trước khi chép, từng file đã được so với hash SHA-256 mà Hugging Face công bố cho đúng revision trên: 287/287 file khớp, cộng `cases.parquet` khớp.
  - Sau khi chép, so lại bản chép với bản gốc: 287/287 giống hệt.
- **Còn thiếu:** file `inject_time.txt` của 89 ca, tổng 890 byte, chưa tải. Thời điểm tiêm lỗi vẫn có trong `cases.parquet`.

| Thư mục | Nội dung | Kích thước |
|---|---|---|
| `rcaeval/` | 30 ca RE2-TT từng làm tập dev ở v1; 5 ca mẫu: `re1ob_productcatalogservice_cpu_3`, `re2ob_productcatalogservice_loss_1`, `re2ss_orders_loss_2`, `re3ss_carts_f1_1`, `re3tt_ts-route-service_f2_1` | 642 MB |
| `locked/rcaeval-re2tt-60/` | 60 ca RE2-TT chưa ai nhìn từng ca (tập final của v1) | khoảng 1,3 GB |
| `locked/rcaeval-metadata/cases.parquet` | Mục lục 735 ca RCAEval, **có nhãn service gốc của mọi ca**, kể cả 60 ca bị khóa | 29 KB |

Mỗi ca có `metrics.parquet`, `traces.parquet`, `logs.parquet` (riêng một ca RE2-TT không có log). Vài ca mẫu có thêm `inject_time.txt`.

**Lưu ý:** mang dữ liệu về **không** có nghĩa là đã chọn RE2-TT làm dataset chính. Việc chọn dataset và cách chia dev/test là của P2, duyệt ở G1. Nếu G1 không dùng 60 ca bị khóa làm test thì chuyển chúng ra ngoài `locked/`.

**Lấy lại trên máy mới:** dùng `huggingface_hub.snapshot_download(repo_id="phamquiluan/RCAEval", repo_type="dataset", revision="afeacb11bcc94dadfd1c8f483ee4377b2b8b614e", allow_patterns=[...])`, với danh sách thư mục ca như bảng trên. Lệnh này chưa chạy thử trong repo này.
