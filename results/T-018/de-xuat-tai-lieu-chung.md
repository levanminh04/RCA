# Đề xuất cho tài liệu chung (chờ Minh duyệt)

T-018 không ghi file chung. Mỗi mục: file đích; đoạn cũ → đoạn mới (nguyên văn); lý do; kết luận nào phụ thuộc. Mã WHY-17, WHY-18 là tạm; khi ghi thì lấy mã kế tiếp còn trống (đọc lại `docs/WHY.md` ngay trước khi ghi, vì nhiều phiên đang chạy song song; xem sự cố mất WHY-16 ngày 04/10).

## E1. `docs/WHY.md` — thêm mục: cách chạy GDN ở chế độ b

- **Đoạn cũ:** không có.
- **Đoạn mới:**

```markdown
## WHY-17. Lý do của phép chẩn đoán GDN ở T-018 (bộ cột cố định, điền cột thiếu, chuẩn hóa và ngưỡng từ tập kiểm định) — Đề xuất (G1); không phải cấu hình P3

- **Trạng thái:** ứng viên, **chưa đạt**: trên dữ liệu bình thường giữ ngoài, cách này vẫn báo động sai 45–100 % số tick (`results/T-018/ho-so-gdn.md` mục 9.4). Mục này chỉ ghi lý do của các lựa chọn đã dùng trong phép chẩn đoán T-018; cấu hình GDN cho P3 chốt sau, khi đã xử lý lệch mức (REVIEW R6).
- **Đã dùng trong T-018:** (1) bộ cột chốt từ siêu dữ liệu dev trước khi thấy ca được chấm; ca thiếu cột thì điền trung vị tập học và ghi số cột đã điền; (2) dữ liệu học là đoạn bình thường không thuộc ca được chấm (với RCAEval: đoạn trước mốc tiêm của các ca dev, tức nhãn dev dùng để học); (3) cột hằng trong tập học xử lý trước khi chuẩn hóa, không để chia cho 1; (4) học theo `run.sh` của GDN, epoch chọn theo val loss như code; (5) trung vị/IQR để chuẩn hóa điểm lệch lấy từ tập kiểm định, giữ cố định; (6) ngưỡng = max điểm đã làm trơn trên tập kiểm định (`report='val'`); (7) chấm theo luồng trên toàn file, không dùng mốc tiêm của ca được chấm.
- **Vì sao:** code gốc chọn ngưỡng theo nhãn test khi `report='best'` (mặc định) và ở mọi chế độ chuẩn hóa điểm test bằng trung vị/IQR của chính tập test, tức dùng dữ liệu tương lai; với file RCAEval, mốc tiêm nằm đúng giữa file nên thống kê cả file mang thông tin về vị trí sự cố. Bộ cột của RE2-TT khác nhau giữa các ca và tương quan với service gốc. Cột hằng trong tập học bị chia cho 1 nên ở dữ liệu mới mang đơn vị thô.
- **Phương án đã xét:** dùng nguyên code (`report='val'`): giữ G2–G4 của hồ sơ; bộ cột theo giao ca học và ca test như T-005: phụ thuộc ca được chấm.
- **Bằng chứng:** `results/T-018/ho-so-gdn.md` mục 7–9; `results/T-018/runs/b6b7-phan-tich.json`.
- **Chưa kiểm:** cách xử lý cột hằng tốt nhất và mức ảnh hưởng tới P/R/F1 (việc của P3).
- **Kết luận phụ thuộc:** mọi số phát hiện của GDN ở P3 chế độ b.
```

- **Lý do:** hồ sơ dùng biến thể "chuẩn hóa từ tập kiểm định" và bộ cột L\* trong kết quả chẩn đoán (mục 7–9); MRP P3 chế độ b cần một cách chạy không dùng nhãn.
- **Kết luận phụ thuộc:** `ho-so-gdn.md` mục 8.2, 9.1, 9.2; bảng "bình thường vs bình thường".

## E2. `docs/WHY.md` — thêm mục: báo Retrieval@K và Rerank@1 ở P3

- **Đoạn cũ:** không có.
- **Đoạn mới:**

```markdown
## WHY-18. Vì sao báo Retrieval@K và Rerank@1 (K tính theo service) cùng MRR, Hit@k — Đề xuất (G1, dùng ở P3)

- **Chọn:** với mọi phương pháp RCA, báo thêm Retrieval@K (nguyên nhân gốc nằm trong K service đầu của thứ hạng mức service) và Rerank@1 = Hit@1 / Retrieval@K, với K ∈ {5, 10}; dùng `Evaluator.retrieval_service` và `rerank_service` của RCAEval `259ea41`.
- **Vì sao:** Hit@k gộp hai kiểu hỏng khác nhau: không tìm ra nguyên nhân, và tìm ra nhưng xếp sai. Phép tách cho P4 biết nên tìm cơ chế ở bước nào (bài DecompRCA, NeurIPS 2026 E&D). Tính được từ thứ hạng đã có, không tốn chạy thêm.
- **Phương án đã xét:** dùng định nghĩa ở Bảng 1 của DecompRCA (K metric, trúng nếu bất kỳ metric nào của service gốc nằm trong K): với hệ ít service, bộ chọn ngẫu nhiên 15 metric đã trúng 0,82–0,90 (RE1-OB, RE1-SS), nên mức trần chủ yếu do cấu trúc.
- **Bằng chứng:** `results/T-018/decomprca.md` mục 3 (K7–K9), mục 4; `results/T-018/runs/b9-retrieval-ngau-nhien.json`.
- **Kết luận phụ thuộc:** phân loại hạn chế ở P4 (lỗi truy hồi hay lỗi xếp lại).
```

- **Lý do:** đề xuất P3 ý 1 của `decomprca.md`.
- **Kết luận phụ thuộc:** `decomprca.md` mục 4, 5.

## E3. `docs/MRP.md` — P2, ý "Kiểm rò nhãn": thêm đường rò qua bộ cột

- **Đoạn cũ** (dòng 151, câu cuối): "Nếu một baseline cần biết trước vị trí triệu chứng thì ghi rõ đầu vào đó và nguồn hợp lệ."
- **Đoạn mới:** "Nếu một baseline cần biết trước vị trí triệu chứng thì ghi rõ đầu vào đó và nguồn hợp lệ. Kiểm cả bộ cột: ở RE2-TT, tập cột metric khác nhau giữa các ca và tương quan với service gốc (T-018); phương pháp học xuyên ca phải dùng bộ cột cố định chốt từ dữ liệu học."
- **Lý do:** `dinh-chinh-task-cu.md` D1.
- **Kết luận phụ thuộc:** giao thức P3, mọi phương pháp học xuyên ca.

## E4. `docs/knowledge/K1-phuong-phap-rca.md` — §C.11 GDN

- **Đoạn cũ** (dòng 250): "directed edge được học bằng top-k cosine similarity giữa sensor embeddings, có thể giới hạn candidate relations bằng prior."
- **Đoạn mới:** "directed edge được học bằng top-k cosine similarity giữa sensor embeddings. Bài cho phép giới hạn candidate relations bằng prior, nhưng code `d-ailin/GDN@9853899` không cài (forward luôn tính top-k trên mọi nút); top-k của code gồm cả chính nút nên mỗi nút có k − 1 láng giềng khác nó (T-018, `results/T-018/ho-so-gdn.md` mục 5)."
- **Lý do:** K1 là kiến thức nền "chưa kiểm lại"; điểm này đã kiểm trên code.
- **Kết luận phụ thuộc:** mọi ý tưởng "đưa đồ thị gọi vào GDN" ở P6 (WHY-10): phải sửa code, không chỉ đổi cấu hình.

## E5. `docs/LESSONS.md` — thêm một sai lầm

- **Đoạn cũ:** không có (sau dòng SL33 của bảng).
- **Đoạn mới:**

```markdown
| SL34 | Viết câu phổ quát ("30 ca đều có `inject_time.txt`") sau khi chỉ nhìn một thư mục; ghi giờ vào LOG theo ước đoán thay vì đọc đồng hồ (T-018, đã đính chính trong LOG) | Câu "mọi/đều" phải có lệnh đếm trên đủ đối tượng; giờ trong LOG lấy bằng `date` |
```

- **Lý do:** lỗi của chính T-018, đã tự phát hiện và đính chính (LOG dòng 09:10 và đính chính giờ).
- **Kết luận phụ thuộc:** không.

## E6. `docs/MRP.md` — P1, dòng 143 (không bắt buộc)

- **Đoạn cũ:** "\"Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition\" (RCAEval ghi là NeurIPS 2026 Evaluations and Datasets)."
- **Đoạn mới:** "\"Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition\" (arXiv 2609.36686, NeurIPS 2026 Evaluations and Datasets; đã đọc ở T-018)."
- **Lý do:** đã xác nhận nơi đăng trên PDF và trang arXiv.
- **Kết luận phụ thuộc:** không.

Không đề xuất gì cho `AGENTS.md`, `CLAUDE.md`, `docs/DECISIONS.md` (không có quyết định nào của Minh trong phiên), `docs/reference/`, `docs/review-prompt.md`, `data/README.md`, `requirements.txt`.

Ghi chú cho `data/README.md` (không phải đề xuất sửa, để Minh biết): `inject_time.txt` của 30 ca dev đã tải về `D:\RCA-ext\work\T-018\nguon\rcaeval-inject\` (ngoài `data/`), kiểm oid HF 30/30. Nếu muốn đưa vào `data/rcaeval/`, cần một đề xuất riêng.
