# T-018 — Hồ sơ kỹ thuật GDN và đọc bài DecompRCA

- **Trạng thái:** đã duyệt 04/10/2026 theo ủy quyền tự duyệt SPEC (prompt Đợt 1 ngày 04/10/2026; ghi ở LOG). Không ai duyệt trước khi làm.
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1 — **Cổng:** G1

## Mục tiêu

Phục vụ nhận xét đầu tiên của cô: "chưa sâu kỹ thuật của từng phương pháp" (MRP §2.1, P1), và Q-30 (bộ phát hiện bất thường có hồ sơ riêng). Trả lời RQ1 ở phần cơ chế của GDN.

Task trả lời bốn câu:
1. GDN tính điểm bất thường thế nào, từng bước, bằng công thức; code khác bài ở đâu; nhãn hoặc dữ liệu test có thể lọt vào ở đâu; chạy hợp lệ ở chế độ b (không dùng mốc tiêm) thế nào.
2. GDN cần đầu vào gì: bộ cột cố định (RE2-TT có 340–375 cột, khác nhau giữa các ca), bao nhiêu dữ liệu bình thường; từ đó dataset ứng viên nào chạy được GDN.
3. Bài "Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition" (DecompRCA) làm gì về kỹ thuật; khẳng định nào đúng với bản PDF và repo; hệ quả cho P3 (giao thức, tập ứng viên, độ đo), P4 (giả thuyết, **chưa kiểm**) và chọn dataset ở G1.
4. Kết quả T-000 đến T-012 có vấn đề nào liên quan GDN/DecompRCA cần đính chính không.

Task **không** chấm GDN trên dataset (P3), không phân tích hạn chế bằng số liệu (P4), không thiết kế phương pháp đồ thị.

## Đầu vào

- `results/T-001/danh-sach-phuong-phap.md` (mục 3 D5, mục 4 L8, mục 6, mục 9 revision).
- `results/T-005/` (do-kha-thi.md mục 2b, moi-truong.md mục 5–6, scripts/chuan_bi_dau_vao.py, scripts/chay_mot_luot.py, runs/do-gdn_*.log).
- `results/T-006/kiem-dung-dan.md` mục 9, 10; `results/T-006/scripts/chay_gdn.py`.
- Code GDN `D:\RCA-ext\src\GDN`, revision `9853899da860682669a134e4af315d036aab4eca` (đã kiểm: `git status` sạch). Môi trường `D:\RCA-ext\envs\py38-gdn` (freeze trùng `results/T-005/runs/freeze-py38-gdn.txt`). Chỉ dùng, không sửa.
- Đầu ra GDN của T-005 ở `D:\RCA-ext\work\T-005\gdn\` (`model_re2tt5.pt`, `data/re2tt5/{train,test,list}`), chỉ đọc.
- Bài GDN: arXiv 2106.06947v1 (bản arXiv của bài AAAI'21). Bài DecompRCA: arXiv 2609.36686v1. Repo `cruiseresearchgroup/DecompRCA` commit `f99d2172ad3ba1d584d947c075d69fc9bbc09064`. Tải về `D:\RCA-ext\work\T-018\nguon\` (LOG 08:36; hash ở `results/T-018/nguon-tai.md`).
- RCAEval `D:\RCA-ext\src\RCAEval` (HEAD `259ea41`, có commit `fb8f20a6` mà DecompRCA ghim), chỉ đọc.
- Dữ liệu: 30 ca dev `data/rcaeval/re2tt_*` (metrics.parquet, inject_time.txt). Không đọc traces/logs (GDN chỉ dùng metric). `D:\RCA-ext\data\RE1-OB`, `RE1-SS` chỉ đọc tên cột và tên ca (bước B9).
- Thẻ dataset: `results/T-002/the-rcaeval.md`, `results/T-003/bang-tieu-chi.md`, `results/T-008..T-012/the-dataset.md` (chỉ đọc, để suy ra dataset nào chạy được GDN).

## Đầu ra

Trong `results/T-018/`:
- `ho-so-gdn.md`: hồ sơ GDN đủ 7 mục MRP P1 + 2 mục thêm (đường nhãn; yêu cầu đầu vào khi chạy trên dataset khác) + cách chạy hợp lệ ở chế độ b.
- `decomprca.md`: tóm tắt kỹ thuật, bảng kiểm khẳng định (PDF và repo), hệ quả P3/P4/G1.
- `yeu-cau-dau-vao.csv`: đúng 16 cột theo prompt; mỗi phương pháp/biến thể/bộ phát hiện một dòng (GDN theo ba cách chạy; hai giai đoạn của DecompRCA chỉ ở mức "đã đọc").
- `ca-da-chay.csv`: mọi ca đã chạy GDN trong task (ca, file nguồn, phương pháp, mục đích, lý do a/b/c).
- `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md` (ghi "không có" nếu trống).
- `moi-truong.md` (không tạo môi trường mới thì ghi rõ), `nguon-tai.md` (nguồn, kích thước, SHA-256).
- `cot-re2tt/`: thống kê bộ cột, cột hằng, nhịp cập nhật của 30 ca dev.
- `runs/`: log từng lượt GDN, file JSON tóm tắt, bảng so sánh. Mô hình và mảng lớn để ở `D:\RCA-ext\work\T-018\`.
- `scripts/`: mọi script đã chạy.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng T-018 trong `docs/STATE.md`. Ghi ra ngoài thì dừng, ghi vào LOG và mục "Cần Minh quyết".

- `tasks/T-018-ho-so-gdn-decomprca/SPEC.md`, `LOG.md`
- `results/T-018/`
- `D:\RCA-ext\work\T-018\`
- Một dòng của T-018 trong `docs/STATE.md` (đọc lại trước và sau khi ghi; thay chuỗi chính xác).

Không ghi: file của task khác (kể cả `D:\RCA-ext\work\T-005\`), `docs/*` ngoài dòng STATE, `data/`, `D:\RCA-ext\src\`, `D:\RCA-ext\envs\`.

## Quy tắc chọn trước (ghi trước khi nhìn kết quả)

- **R-ca (ví dụ tính tay):** ca `re2tt_ts-route-service_socket_1`, mô hình học theo đúng cấu hình T-005. Lý do: đây là ca T-005 đã chọn theo kích thước file, không theo nhãn; T-005 đã chạy GDN trên nó ("ca đã thấy").
- **R-tick:** hai mốc. t\* = tick có A(t) lớn nhất trên cả ca, A(t) tính theo đúng code (chuẩn hóa bằng trung vị/IQR của file test), chọn theo đầu ra, không theo nhãn. t0 = chỉ số cửa sổ 100 (dòng thô 105). Ghi thẳng: người làm biết file RCAEval cắt đối xứng quanh mốc tiêm (T-002), nên biết t0 nằm ở nửa đầu; t0 chỉ dùng làm điểm so sánh khi giải thích, không đưa vào phương pháp.
- **R-giữ-ngoài:** tập học lớn nhất (10 ca) = 5 ca học của T-005 + 5 ca đầu tiên theo thứ tự SHA-256 của tên thư mục, trong 24 ca dev còn lại (bỏ ca R-ca). Tập học 1 ca = ca đầu danh sách T-005 (`re2tt_ts-order-service_loss_1`). 19 ca dev còn lại là **tập bình thường giữ ngoài**: chỉ lấy 720 dòng trước mốc tiêm của mỗi ca. Thứ tự SHA-256 không phụ thuộc nhãn hay kết quả.
- **R-cột (bộ cột cố định L\*):** giao các cột của 30 ca dev sau cùng bước làm sạch như T-005 (bỏ `time.1`, bỏ `*_latency-50`, đổi `*_latency-90` → `*_latency`). Chỉ dùng tên cột, không dùng nhãn. Vì L\* dùng cả tên cột của ca giữ ngoài, phép kiểm trên L\* đo riêng khả năng tổng quát trên dữ liệu bình thường mới, không gồm ảnh hưởng của cột thiếu. Ảnh hưởng cột thiếu được đo trên mô hình R1 (bộ cột của T-005, điền theo R-thiếu-cột).
- **R1 không phải cấu hình chế độ b hợp lệ:** bộ 333 cột của T-005 là giao của 5 ca học **và ca test** R-ca, tức dùng thông tin của ca test khi dựng mô hình. R1 chỉ dùng để lặp T-005 và làm ví dụ tính tay.
- **R-thiếu-cột:** khi một ca thiếu cột có trong bộ cột của mô hình, điền bằng trung vị của cột đó trong tập học (thang thô, trước chuẩn hóa) và ghi số cột đã điền. Không dùng dữ liệu của ca bị thiếu.
- **R-chuẩn-hóa-b (biến thể chế độ b):** a_i(t) = (Err_i(t) − med_val,i) / (|IQR_val,i| + 0,01); làm trơn và ngưỡng giữ như code. Chỉ khác code ở chỗ trung vị/IQR lấy từ tập kiểm định thay vì tập test.

## Edge case (liệt kê trước khi làm)

| # | Edge case | Cách kiểm | Cách xử lý |
|---|---|---|---|
| E1 | **Seed.** GDN dùng `random` (vị trí khối kiểm định, `main.py:132`), numpy, torch (khởi tạo, xáo batch). Kết quả có thể phụ thuộc seed và số luồng CPU | So SHA-256 trọng số lượt lặp R1 với `model_re2tt5.pt` của T-005; ba seed {5, 1, 2} trên L\* | Giữ seed 5 như `run.sh`; báo độ lệch giữa seed (ngưỡng, số báo động trên dữ liệu bình thường, tương quan A(t)) |
| E2 | **Cột hằng.** (a) Hằng trong tập học: min-max có khoảng 0, T-005 thay bằng 1 (như `MinMaxScaler`), nên ở test cột đó mang đơn vị thô; (b) lỗi dự báo gần hằng: IQR ≈ 0, chia cho 0,01 làm điểm phóng to | Đếm cột hằng ở mỗi tập học; giá trị tuyệt đối lớn nhất của test sau chuẩn hóa; số cột có IQR < 1e-6 (val, test); tỷ lệ tick mà cột đó là argmax của A(t) | Không đổi cách của code khi tái lập; báo hệ quả; đề xuất cho chế độ b ghi "(chờ WHY)" |
| E3 | **Độ dài cửa sổ trượt** w = 5 điểm (bài §4.4, `run.sh`). RE2-TT lấy mẫu 1 s nhưng nhiều metric có thể chỉ cập nhật mỗi vài giây rồi được ffill, nên cửa sổ 5 giây có thể toàn giá trị lặp | Đo nhịp cập nhật: tỷ lệ bước 1 s có giá trị đổi, theo loại metric (B2) | Giữ w = 5 (prior work); ghi hệ quả; độ nhạy theo w không đo (P3/P6), ghi kết luận nào yếu đi |
| E4 | **Ngưỡng lấy từ tập kiểm định.** τ = max của điểm đã làm trơn trên tập kiểm định (`evaluate.py:109`). Tập kiểm định là một khối liền 20 % cửa sổ học, cùng giai đoạn với tập học, nên τ có thể thấp với dữ liệu bình thường mới | (i) Chấm lại chính tập kiểm định: phải 0 báo động; (ii) chấm tập bình thường giữ ngoài: đếm báo động sai mỗi giờ | Báo cả hai cách chuẩn hóa (code và R-chuẩn-hóa-b) |
| E5 | **Lệch thời gian giữa các cột.** Metric từ nhiều nguồn (container, mesh/trace) được đặt chung cột `time` 1 s; GDN giả định mọi cột cùng tick | Kiểm bước thời gian đều (diff = 1 s), số ô thiếu và vị trí ô thiếu đầu file theo loại metric, thời điểm đổi giá trị đầu tiên theo loại | Lệch đồng hồ thật giữa các nguồn không có chuẩn để đo: ghi "chưa kiểm" kèm lý do, nêu hệ quả với dự báo chéo cột |
| E6 | **Bộ cột khác nhau giữa các ca** (340–375 cột) | Giao, hợp, số cột thiếu ở từng ca so với bộ cột của mô hình | R-cột, R-thiếu-cột; sau khi đếm xong (không trước) mới so cột thiếu với service gốc để xem bộ cột có lộ nhãn không |
| E7 | **Ghép đoạn học của nhiều ca.** Cửa sổ trượt cắt ngang ranh giới hai ca | Đếm số cửa sổ cắt ngang | Giữ như T-005 khi lặp (để so SHA); báo tỷ lệ |
| E8 | **Mốc tiêm lộ qua biên file** (T-002: mốc tiêm ở giữa file). Chuẩn hóa theo trung vị/IQR của cả file test dùng cả nửa sau sự cố | Lý luận trên code; so hai cách chuẩn hóa trên ca R-ca | Chế độ b dùng R-chuẩn-hóa-b |
| E9 | **Khởi động:** 5 tick đầu không có dự báo, 3 tick đầu của điểm làm trơn bằng 0 (`evaluate.py:62-65`) | Đọc code; kiểm trong script tính tay | Ghi vào hồ sơ |
| E10 | **Top-k gồm chính nút i** (cos = 1 với chính nó), rồi `remove_self_loops` + `add_self_loops` | Đếm số nút có i ∈ TopK(i); kiểm trùng điểm cos | Ghi là chỗ code khác bài (bài loại i khỏi C_i, Eq. 1) |
| E11 | **Ô thiếu:** ffill rồi fillna(0); 0 có thể giống giá trị thật | Đếm ô thiếu đầu file theo cột | Ghi hệ quả |
| E12 | **Cột `attack` toàn 0** trong test.csv (code bắt buộc) | Runner không gọi `get_score` (tránh F1 vô nghĩa) | Như T-005 |
| E13 | **Máy đang chạy việc khác** (tới 8 phiên song song) | Ghi tải CPU, RAM trống lúc bắt đầu mỗi lượt | Thời gian chỉ để tham khảo, không phải số chính thức |
| E14 | **Tập bình thường giữ ngoài được cắt bằng mốc tiêm** | — | Chỉ dùng để chấm phép kiểm "bình thường vs bình thường", không đưa vào phương pháp |
| E15 | **Số luồng CPU ảnh hưởng thứ tự cộng số thực** | Nếu R1 khác SHA của T-005: chạy R1 lần hai để tách "không tất định" khỏi "khác môi trường" | Ghi rõ |

## Các bước (xếp theo phụ thuộc)

| Bước | Việc | Cần đầu ra của | Lệnh kiểm |
|---|---|---|---|
| B0 | Mở phiên, kiểm đầu vào, tải nguồn | — | (đã xong, LOG 08:28–08:40) |
| B1 | Đọc bài GDN + code, viết hồ sơ mục 1–6, đường nhãn, chế độ b (file:dòng) | B0 | `grep -n` lại từng file:dòng dẫn trong hồ sơ bằng script `scripts/kiem_dan_dong.py` (in đúng dòng được dẫn) |
| B2 | Thống kê bộ cột 30 ca dev: số cột, giao, hợp, cột thiếu, cột hằng trước mốc, nhịp cập nhật, ô thiếu, bước thời gian (`scripts/dem_cot.py`, py312-pin) | B0 | File `cot-re2tt/*.csv` không rỗng; tổng số ca = 30 |
| B3 | Dựng lại dữ liệu GDN của T-005 bằng script độc lập, so SHA-256 với file của T-005; dựng dữ liệu L\*, tập học 1/5/10 ca, tập bình thường giữ ngoài (`scripts/chuan_bi_gdn.py`) | B0 (B2 chỉ để so L\*) | SHA-256 khớp hoặc ghi lệch; kích thước các tập |
| B4 | R1: học lại đúng cấu hình T-005 (seed 5, luồng mặc định), nhưng truyền `test_dataloader=None` vào `train()`; lưu mô hình, dự báo val/test, điểm, ngưỡng (`scripts/chay_gdn.py`, py38-gdn; log từng epoch kèm giờ). T-005 truyền loader test thật; nếu SHA-256 trùng thì vừa chứng minh lặp được, vừa chứng minh dữ liệu test không ảnh hưởng việc học và chọn epoch | B3 | SHA-256 trọng số so với `model_re2tt5.pt`; điểm hữu hạn |
| B5 | Tính tay độc lập bằng numpy trên ca R-ca (`scripts/tinh_tay_gdn.py`): chỉ dùng torch để nạp trọng số; không gọi hàm nào của GDN | B4 | So mọi dự báo và mọi điểm với đầu ra chính thức theo dung sai ở "Tiêu chí xong" |
| B6 | Phép kiểm không cần nhãn trên mô hình R1: đổi thứ tự cột CSV; hoán vị nút trong bản numpy; chấm lại tập kiểm định; chấm tập bình thường giữ ngoài (hai cách chuẩn hóa); soi giá trị trung gian (E2, E4, E10) | B4, B5 | Bảng kết quả trong `runs/` |
| B7 | Lượt trên L\*: cỡ tập học 1, 5, 10 ca (seed 5); seed 1, 2 (5 ca); hoán vị thứ tự cột trong `list.txt` (5 ca, seed 5). Mỗi lượt chấm tập bình thường giữ ngoài và ca R-ca (chỉ số không cần nhãn) | B3 | Mỗi lượt có log epoch, JSON tóm tắt |
| B8 | Viết mục yêu cầu đầu vào + bảng dataset nào chạy được GDN (từ thẻ dataset) + dòng GDN trong `yeu-cau-dau-vao.csv` | B2, B6, B7 | CSV đúng 16 cột, không ô rỗng |
| B9 | DecompRCA: tóm tắt, kiểm khẳng định trên PDF và repo, tính Retrieval@15 ngẫu nhiên mức service trên tên cột RE1-OB/RE1-SS (`scripts/retrieval_ngau_nhien.py`; không chạy phương pháp), hệ quả P3/P4/G1 | B0 | Mỗi khẳng định có kết luận và bằng chứng (dòng PDF hoặc file:dòng) |
| B10 | Soi task cũ T-000–T-012 phần liên quan GDN/DecompRCA; ghi `dinh-chinh-task-cu.md` | B1, B4–B7, B9 | Mỗi vấn đề có bằng chứng |
| B11 | `de-xuat-tai-lieu-chung.md`, `ca-da-chay.csv`, `moi-truong.md`, `nguon-tai.md` | B1–B10 | Tồn tại, không rỗng |
| B12 | Rà Tiêu chí xong, LOG kết thúc, prompt phản biện, dòng STATE | tất cả | Đối chiếu từng dòng |

B1, B2, B3, B9 độc lập nhau: làm xen trong lúc B4, B7 chạy nền (Q-43).

## Kiểm đúng đắn

**Số công bố, tra trước khi chạy** (ghi ngày 04/10 trước B4):
- Bài GDN, Bảng 2: SWaT P 99,35 %, R 68,12 %, F1 0,81; WADI P 97,50 %, R 40,19 %, F1 0,57 (văn bản PDF dòng 361–370). Bảng 1: SWaT 51 cột, 47 515 điểm học, 44 986 điểm test; WADI 127 cột, 118 795 / 17 275 (dòng 279–283). Dữ liệu sau khi lấy mẫu 10 s và bỏ 2160 điểm đầu (dòng 339–345).
- Bài không báo thời gian chạy. Không có số công bố nào của GDN trên dữ liệu microservice; DecompRCA, RCAEval không dùng GDN.
- Mốc nội bộ (không phải số công bố): T-005 học 30 epoch trên 3600 điểm × 333 cột mất 1029 s; loss epoch 0 là 0,13699762, epoch 29 là 0,01829656 (`results/T-005/runs/do-gdn_hoc-full-lan1.log`). R1 phải ra đúng các loss này nếu tất định.
- Vì SWaT/WADI cần xin iTrust và OT đã bỏ khỏi phạm vi (Q-47), task **không tái lập** Bảng 2. Kết luận yếu đi: hồ sơ chỉ nói được "code chạy, tất định, khớp công thức đã đọc"; không nói được "code ở revision này cho đúng số bài".

**Chạy lại:** R1 so SHA-256 với T-005. Seed {5, 1, 2} cho phương sai (GDN có ngẫu nhiên). Nếu R1 khác T-005: chạy R1 lần hai, lần này truyền loader test thật như T-005, để tách ba nguyên nhân: không tất định, khác môi trường/luồng, dữ liệu test có ảnh hưởng.

**Đầu ra không rỗng:** số cửa sổ, kích thước mảng, mọi điểm hữu hạn.

**Đổi thứ tự cột:** (i) đảo cột trong CSV, giữ `list.txt`: kỳ vọng giống hệt từng byte; (ii) hoán vị nút trong bản numpy (hoán vị cả hàng embedding và cột đầu vào): kỳ vọng đầu ra hoán vị tương ứng, trong dung sai; (iii) học lại với `list.txt` hoán vị: kỳ vọng khác (khởi tạo gắn với chỉ số nút), đo mức khác. Nếu (iii) khác nhiều thì thứ tự cột là một nguồn ngẫu nhiên như seed.

**Hai cửa sổ đều bình thường:** chấm 19 đoạn bình thường giữ ngoài (mỗi đoạn 12 phút, tổng khoảng 3,8 giờ). Báo số tick báo động, số đoạn có báo động, báo động sai mỗi giờ, cho cả hai cách chuẩn hóa. Chấm lại tập kiểm định: phải 0 báo động.

**Soi giá trị trung gian:** phân bố IQR lỗi; cột nào thường là argmax của A(t); độ lớn điểm; cột hằng trong tập học; nút có i ∈ TopK(i).

**Không làm, và kết luận yếu đi:**
- P/R/F1 phát hiện trên RE2-TT: thuộc P3. Hồ sơ không nói GDN phát hiện tốt hay dở trên RE2-TT; chỉ có tính chất không cần nhãn và một ca được giải thích.
- Độ nhạy theo w, theo top-k, theo tham số bài (β2 = 0,99, 50 epoch, patience 10, k = 15): không chạy. Không biết các khác biệt code–bài ảnh hưởng bao nhiêu.
- Lệch đồng hồ thật giữa nguồn metric: không có chuẩn đo (E5).
- Chạy BARO trên RE1-SS để kiểm câu "0,57 so với 0,95" trong repo DecompRCA: không chạy vì prompt cấm chạy benchmark ở phần DecompRCA; chỉ đối chiếu với số T-006 đã có.

## Tiêu chí xong

1. `ho-so-gdn.md` có đủ 7 mục + 2 mục thêm + mục chế độ b; mọi tham số mặc định có file:dòng; mỗi chỗ code khác bài có dòng văn bản PDF và file:dòng; `scripts/kiem_dan_dong.py` in đúng các dòng được dẫn.
2. Tính tay (B5): max |ŝ_tay − ŝ_code| ≤ 1e-5 trên mọi tick × cột; max |a_tay − a_code| ≤ 1e-3 + 1e-5·|a_code|; argmax cột của A(t) trùng ở mọi tick trừ tick có hai cột chênh dưới dung sai (báo số tick đó); quyết định báo động trùng ở mọi tick trừ tick có |A(t) − τ| dưới dung sai (báo số tick đó).
3. R1: báo SHA-256 trùng hay không; nếu không, có lần chạy thứ hai và độ lệch số.
4. Có bảng "bình thường vs bình thường" cho mô hình R1 (hai cách chuẩn hóa) và bảng các lượt L\* (cỡ tập học, seed, hoán vị).
5. `yeu-cau-dau-vao.csv` đúng 16 cột theo thứ tự prompt, mỗi dòng không có ô rỗng (ô chưa kiểm ghi `chua_kiem: <lý do>`).
6. `decomprca.md` có tóm tắt, bảng kiểm khẳng định (mỗi dòng: khẳng định, nơi trong PDF, nơi trong repo, kết luận khớp/lệch/chưa kiểm, bằng chứng), hệ quả P3, P4 (mỗi giả thuyết ghi "chưa kiểm", giả định, khi nào sai, việc nào kiểm được), G1.
7. `ca-da-chay.csv` có mọi ca đã chạy GDN; `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md`, `moi-truong.md`, `nguon-tai.md` tồn tại.
8. LOG có mục kết thúc đủ 6 ý, báo cáo A–H, prompt phản biện; dòng T-018 trong STATE là "chờ phản biện (04/10)".

## Không làm

- Không chấm P/R/F1 của GDN trên dataset; không chạy GDN trên ca ngoài danh sách được phép.
- Không cài DecompRCA, không gọi LLM, không chạy baseline của DecompRCA.
- Không sửa code GDN, RCAEval, môi trường, file task cũ.
- Không đọc `data/locked/`; không đọc/giải nén ca RE2-TT nào ngoài 30 ca dev.
- Không chọn dataset, không chốt cách chia, không chốt độ dài cửa sổ (Q-54).

## Chi phí ước lượng

- Tải: khoảng 4 MB (đã tải).
- Học GDN (thời gian máy rảnh, ngoại suy tuyến tính từ T-005: 34 s/epoch cho 3600 điểm): R1 khoảng 17 phút; L\* cỡ 1 ca khoảng 3,5 phút, cỡ 5 ca khoảng 17 phút × 4 lượt (seed 5, 1, 2, hoán vị), cỡ 10 ca khoảng 34 phút. Tổng khoảng 2 giờ CPU; chạy hai lượt song song (mỗi lượt 6 luồng) thì khoảng 70–90 phút chờ. Máy đang có nhiều phiên khác nên có thể dài hơn; mỗi lượt đặt giới hạn 60 phút, quá thì dừng, ghi lượt hỏng, không chạy lại cỡ lớn hơn.
- Suy luận, tính tay, thống kê cột: vài phút.
- Không lượt nào dự kiến quá 1 giờ; không quá 2 subagent (dự kiến không dùng); không deep research; không quá 5 GB. Không cần báo trước theo luật cứng 8. Ngân sách Q-40 (3 giờ/phương pháp/dataset) không áp dụng vì không chạy toàn dataset.

## Rủi ro và điều chưa chắc

- R1 có thể không tất định trên CPU nhiều luồng (E15).
- Cỡ 10 ca có thể vượt 60 phút nếu máy bận; khi đó kết luận về lượng dữ liệu bình thường chỉ dựa trên cỡ 1 và 5.
- So cỡ tập học 1/5/10 ca lẫn hai yếu tố: lượng dữ liệu và độ đa dạng ca (mỗi ca là một lượt chạy hệ thống riêng). Không tách được hai yếu tố này với số lượt hiện có.
- Kết luận về RE2-TT chỉ đúng cho 30 ca dev và cấu hình đã chạy; chưa kiểm trên ca khóa.

## Thay đổi trong lúc làm

1. **(04/10, khoảng 08:58) Đổi cơ sở của phép kiểm seed và hoán vị cột từ L\* sang `re2tt5`.** Lý do: máy đang tải 100 % (nhiều phiên khác); một epoch 5 ca mất 65–115 s thay vì 34 s của T-005, nên mỗi lượt 5 ca mất 30–60 phút. Dùng R1 (`re2tt5`, seed 5) làm lượt gốc thì bớt được một lượt 5 ca trên L\* mà vẫn đo được phương sai seed (seed 1, 2) và hoán vị `list.txt` (`re2tt5_hoanvi`). Đường cong theo lượng dữ liệu vẫn làm trên L\* (1 ca, 5 ca). Hệ quả: phương sai seed đo trên bộ 333 cột của T-005 (có dùng cột của ca test, SPEC "R1 không phải cấu hình chế độ b"), không trên L\*; tính chất cần đo (độ nhạy theo seed và thứ tự cột) không phụ thuộc bộ cột nào.
2. **Lượt 10 ca trên L\*:** theo ước lượng từ lượt 1 ca đang chạy (23 s/epoch cho 572 cửa sổ học, 6 luồng, máy bận), lượt 10 ca (khoảng 5750 cửa sổ) cần khoảng 230 s/epoch, tức gần 2 giờ cho 30 epoch. Vượt giới hạn 1 giờ một lượt nên **không chạy** trừ khi máy rảnh lại và ước lượng mới dưới 1 giờ. Kết luận về lượng dữ liệu bình thường khi đó chỉ dựa trên 1 và 5 ca.
3. Thêm dữ liệu `re2tt5_daocot` cho phép kiểm (i) đảo cột trong CSV (`scripts/tao_bien_the.py`).
4. **(04/10, khoảng 09:05) Thay mục 1.** Đo thêm cho thấy lượt 5 ca (6 luồng, chạy song song) mất khoảng 115 s/epoch, tức sát 60 phút một lượt, quá rủi ro với giới hạn 1 giờ. Kế hoạch mới: phương sai seed đo ở **hai cỡ**: cấu hình 1 ca L\* (seed 5, 1, 2; khoảng 10 phút/lượt) và cấu hình 5 ca L\* (seed 5, 1); hoán vị `list.txt` đo ở cấu hình 1 ca (`lstar_n1_hoanvi`). R1 (`re2tt5`) chỉ dùng để lặp T-005 và tính tay. Bỏ `re2tt5_hoanvi`, `lstar_n5_hoanvi` (đã dựng, không chạy). Hệ quả: độ nhạy theo thứ tự cột chỉ đo khi học trên 1 ca (ít dữ liệu, dễ dao động hơn), nên là cận trên; ghi rõ ở hồ sơ.
5. **(04/10, 09:25) Hàng đợi lượt 5 ca.** Lượt 1 ca thứ nhất mất khoảng 17 phút học + hơn 9 phút chấm (19 đoạn giữ ngoài) khi chạy song song với R1. Lượt `l5-lstar-n5-seed5` chỉ chạy sau khi R1 và ba lượt 1 ca xong, với luồng mặc định; lượt `l6-lstar-n5-seed1` chỉ chạy nếu l5 xong dưới 45 phút (nếu không, ghi file `runs/l6-...-KHONG-CHAY.txt` và hồ sơ ghi phương sai seed ở cỡ 5 ca là chưa kiểm). Lý do: giới hạn 1 giờ một lượt.
6. **(04/10, 09:47) Bỏ lượt 5 ca trên L\* (l5, l6).** R1 (5 ca, máy bận) mất 59 phút chỉ cho 29 epoch học và bị dừng ở giới hạn 1 giờ trước bước chấm. Lượt 5 ca L\* cùng cỡ nên dự kiến quá 1 giờ: theo giới hạn của prompt thì không chạy. Thay bằng: so 1 ca (l1, L\*) với 5 ca (R1 chấm lại bằng `--chi-cham`, bộ 333 cột, đoạn giữ ngoài điền cột thiếu), cộng chẩn đoán lệch phân bố ở mức dữ liệu cho 1/5/10 ca (`scripts/chan_doan_lech_phan_bo.py`). Hệ quả: (a) phương sai theo seed chỉ đo ở cỡ 1 ca; ở cỡ 5 ca **chưa kiểm**; (b) so 1 ca với 5 ca lẫn thêm khác biệt bộ cột (317 so với 333) và việc điền cột thiếu; (c) không có mô hình học trên 10 ca.
7. **(04/10, 13:43) Chạy lại l5, có điều kiện l6.** Sau thời gian dừng phiên, máy rảnh (tải CPU trung bình 8 %, RAM trống 1,7 GB). Lượt 1 ca khi máy rảnh học 30 epoch trong khoảng 6 phút (l3), nên lượt 5 ca ước lượng 20–35 phút cộng khoảng 6 phút chấm, dưới 1 giờ. Theo yêu cầu "việc làm được trong giới hạn thì làm ngay", chạy `l5-lstar-n5-seed5`; chỉ chạy `l6-lstar-n5-seed1` nếu l5 xong dưới 30 phút. Mục 6 vẫn giữ nguyên làm lịch sử.
8. **(04/10, 14:25) Kết quả của mục 7.** l5 xong trong 22 phút nên l6 cũng chạy (18 phút). Hệ quả (a) và (b) của mục 6 không còn: đã có so sánh 1 ca với 5 ca trên cùng bộ cột L\*, và phương sai theo hai seed ở cỡ 5 ca. Hệ quả (c) vẫn còn: không có mô hình học trên 10 ca (ước lượng khi máy rảnh khoảng 45 phút học + chấm; không chạy để giữ thời gian phiên, xem mục "Chưa kiểm" của LOG).
9. **(04/10, 14:27) Sửa mục 8 về lượt 10 ca:** lý do "giữ thời gian phiên" không đủ theo yêu cầu "việc làm được trong giới hạn thì làm ngay". Máy đang rảnh, ước lượng dưới 1 giờ, nên chạy `l7-lstar-n10-seed5`. Nếu bị dừng ở 1 giờ thì ghi lượt hỏng và giữ hệ quả (c).
10. **(04/10, phiên 3; REVIEW R5) Độ lệch phạm vi đọc ở B9.** SPEC chỉ cho đọc tên cột và tên ca RE1-OB/RE1-SS, nhưng `scripts/retrieval_ngau_nhien.py` đã đọc toàn bộ số đo và mốc tiêm để bỏ cột hằng theo từng cửa sổ (như loader DecompRCA). Không vượt giới hạn của prompt (prompt cho chạy phương pháp trên hai bộ này), nhưng vượt SPEC và không được ghi lúc làm. Minh duyệt giữ số ngày 04/10 ("duyệt sửa đổi").
