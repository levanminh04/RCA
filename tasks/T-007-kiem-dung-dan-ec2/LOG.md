# Nhật ký T-007

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Tạo task — 03/10/2026 — Claude (phiên T-005)

Minh duyệt SPEC ngày 03/10/2026 ("DUYỆT CẢ 3 MỤC", gồm SPEC T-006, SPEC T-007 và các sửa đổi T-005). Duyệt SPEC này gồm cả ngoại lệ "task kéo dài 2 phiên".

Bối cảnh đã có, không cần làm lại:
- EC2 đã tạo, SSH chạy được (kiểm 03/10, lệnh chỉ đọc): xem `tasks/T-005-do-kha-thi/LOG.md`, mục "Phần thêm 3" và các dòng sau. Quyền file khóa đã sửa theo duyệt của Minh.
- Q-42: Minh bật, tắt máy; chỉ Stop, không Terminate; không đưa khóa AWS; không chép dữ liệu khóa lên EC2.
- Mốc đối chiếu: SPEC mục Đầu vào.

Phối hợp với T-006: T-006 chạy song song ở phiên khác. E0, E1 làm ngay; E2, E3 chờ file `results/T-006/x1-chot-moi-truong.md`.

Chưa làm bước nào. Bước tiếp theo: E0.

---

## Phiên 1 — 03/10/2026 — Claude — laptop Windows (i5-1240P) điều khiển EC2 qua SSH — vai trò: người làm

- Mở phiên. EC2 `3.104.124.160` trả lời SSH: Ubuntu 24.04.4, 2 vCPU, RAM 7,6 GiB, đĩa trống 27 GB, chưa có `~/rca`, chưa có uv, gcc. T-006 chưa có `results/T-006/` (chưa có X1).
- 06:40 UTC: chép `scripts/e0_dung_moi_truong.sh`, `scripts/e1_tai_du_lieu.py` lên `~/rca/scripts/`; chạy nền E0 và E1 song song (`nohup`; log `~/rca/runs/e0/e0.log`, `~/rca/runs/e1/e1.log`). Cache pip, uv, matplotlib và thư mục tạm đặt trong `~/rca` để không ghi ngoài Phạm vi ghi. E1 lấy danh sách ca bằng cây thư mục HF, lọc ngay tiền tố `re2ob_`; tên ca khác không lưu, không in. Không tải `cases.parquet`.

### Quyết định của Minh trong phiên
- E3: chạy qua script bọc mỏng gọi đúng `reproduce_bocpd("fse-ob")` của BARO, chỉ chặn `find_cps` và vòng tqdm để ghi thêm kết quả, thời gian từng ca (so được với `naive_bocpd.json` của tác giả). Thay cho lệnh nguyên văn `main.py --anomaly-detection`; P/R/F1 in ra giữ nguyên.
- Lúc chờ X1: T-006 đang chạy song song. Khi E0, E1 xong thì kiểm `results/T-006/x1-chot-moi-truong.md`. Nếu chưa có thì chạy thử ít ca như đề xuất (MicroRank, TraceRCA 2 ca; BOCPD 1 ca; cả `py312` và `py312-pin`; chỉ để bắt lỗi đường ống, không dùng làm số).

### Quy ước chấm, chốt trước khi chạy
- Chấm như `main.py` RCAEval: thứ hạng thao tác đổi về service bằng `x.split("_")[0].replace("-db", "")`, bỏ trùng giữ thứ tự đầu tiên; `Evaluator` theo từng loại lỗi; báo Avg@5 từng loại lỗi, AVERAGE, cộng AC@1, AC@3.
- Ca lỗi: `main.py` RCAEval ném lỗi và dừng cả lượt (`raise e`), nên không có quy ước của tác giả. Báo cả hai cách: bỏ ca lỗi khỏi mẫu số, và tính ca lỗi là trượt. Số ca lỗi ghi riêng.
- **E0 xong** (06:40–06:45 UTC, `runs/e0/e0.log` trên EC2, sẽ chép về `results/T-007/runs/`): apt cài đủ gói của SPEC; RCAEval `259ea41`, BARO `e35f4ec` khớp; uv 0.12.22 trong `envs/tools`. `py312`: pip, bản mới nhất (pandas 3.0.6, numpy 1.26.4, scipy 1.17.1, scikit-learn 1.7.2, causal-learn 0.1.4.8, torch 2.8.0+cu128, pyarrow 25.0.1). `py312-pin`: `uv pip install --exclude-newer 2024-12-22` cài đủ, **không phải dùng phương án dự phòng** (pandas 2.2.3, numpy 1.26.4, scipy 1.14.1, scikit-learn 1.6.0, causal-learn 0.1.3.8, torch 2.5.1+cu124, pyarrow 18.1.0). `pip check` sạch cả hai. Import `microrank`, `tracerca`, `baro.anomaly_detection`, `baro.reproducibility` được ở cả hai. Dòng "causallearn LOI" trong log chỉ là gói không có thuộc tính `__version__`, không phải lỗi import. Lưu ý: TZ của EC2 là UTC, nên mốc `2024-12-22` hiểu là 00:00 UTC; trên laptop (UTC+7) là 17:00 UTC ngày 21/12. Đĩa: `py312` 7,6 GB, `py312-pin` 5,9 GB (torch bản CUDA, pip mặc định trên Linux); trống 12 GB.
- **E1 xong** (06:40–06:50 UTC, `runs/e1/`): `fse-ob.zip` 150 740 576 B, MD5 khớp Zenodo; giải nén 100 ca, mỗi ca 12 file (có `naive_bocpd.json`, `bocpd_time.json`). RE2-OB: gốc repo HF có 738 mục, lọc được 90 ca `re2ob_*` (5 service × 6 loại lỗi × 3 lần); 180 file (traces.parquet: SHA-256 LFS; inject_time.txt: git blob oid) **khớp hết**, 879,3 MB. Manifest: `runs/e1/manifest-*.json`.
- Kiểm X1 lúc 06:51 UTC: chưa có (T-006 đang ở bước 0). Theo quyết định của Minh: chạy thử.
- **Chạy thử** (`scripts/thu_duong_ong.sh`, 06:53–06:55 UTC, `runs/thu/`): MicroRank, TraceRCA trên `re2ob_checkoutservice_cpu_1`, `re2ob_checkoutservice_delay_1`; BOCPD (script bọc) trên `fse-ob/cartservice_cpu/1`; cả hai bộ thư viện. Không lỗi. File kết quả MicroRank, TraceRCA của hai bộ **giống từng byte**; điểm đổi BOCPD hai bộ giống nhau và **giống hệt `naive_bocpd.json` của tác giả** (8 điểm đổi). Giá trị trung gian: cửa sổ 164–171 nghìn span, chia trước/sau mốc gần đều (82 279 / 82 223), 7 service, khoảng 10 nghìn trace; MicroRank trả 11 thao tác, TraceRCA 33–34. Thời gian (không phải số đo): MicroRank khoảng 13 s/ca, TraceRCA khoảng 1 s/ca, BOCPD khoảng 20 s/ca; RSS đỉnh khoảng 1,1 GB. Ước lượng E2 khoảng 25 phút, E3 khoảng 35 phút, thấp hơn nhiều ước lượng của SPEC.
- Soạn sẵn `scripts/chay_e2_e3.sh <env>` (E2 MicroRank → TraceRCA → chạy lại 6 ca mỗi phương pháp trong tiến trình mới, so từng byte → E3 BOCPD; mỗi khối xong nén ngay vào `~/rca/runs/<env>/`). 6 ca chạy lại chọn trước khi xem kết quả: mỗi service một ca, đủ 6 loại lỗi.
- **Kiểm giả định dữ liệu của mốc:** torai-OB (dữ liệu Bảng 2 bài TORAI, đã giải nén ở `D:\RCA-ext\data\torai-OB` bởi T-006; chỉ đọc `inject_time.txt`) và RE2-OB trùng cả 90 tên ca và 90 mốc tiêm (0 ca lệch). Tức Bảng 2 và E2 dùng cùng các lượt ghi; khác nhau ở chỗ torai-OB chỉ có chuỗi trace đã gộp 15 s, E2 dùng span thô của RE2-OB.
- **Kiểm chính script chấm** (`scripts/cham.py`): chạy trên đầu ra `main.py` của T-006 (TORAI trên torai-OB, 3 lượt, `results/T-006/runs/torai-torai-ob-lan{1,2,3}.tar.gz`, giải nén vào thư mục tạm, chỉ đọc). Avg@5 của `cham.py` khớp số `main.py` in ra ở 18/18 ô (6 loại lỗi × 3 lượt). Thêm `sys.stdout.reconfigure(encoding="utf-8")` để in được trên Windows.

### Quyết định của Minh trong phiên (lượt 2)
- Chạy trọn E2 + E3 bằng **cả hai bộ** ngay, không chờ X1: `py312-pin` trước, rồi `py312`. X1 chọn bộ nào thì số chính thức lấy từ bộ đó; bộ kia giữ làm bằng chứng về ảnh hưởng của phiên bản thư viện. X1 ghi "dừng" thì không dùng số nào, báo Minh. (Lệch SPEC: E2, E3 không còn chờ X1; lý do: chạy thử cho thấy mỗi bộ chỉ khoảng 1 giờ.)
- Làm E4 luôn trong phiên này (SPEC chia 2 phiên chỉ vì tưởng phải chờ qua đêm).
- 07:01 UTC: chạy nền `chay_e2_e3.sh py312-pin` rồi `chay_e2_e3.sh py312` nối tiếp (log tổng `~/rca/runs/chay-<env>.log`).
- Trích mốc Bảng 2 bài TORAI (dòng Trace, MicroRank và TraceRCA) bằng máy từ HTML arXiv 2604.13522v1 (`scripts/trich_moc.py` → `moc-torai-bang2-trace.json`, có SHA-256 của trang). Tính lại cột AVERAGE = trung bình 6 loại lỗi: khớp cả 6 ô (AC@1, AC@3, Avg@5 của hai phương pháp), nên `cham.py` báo AVERAGE theo cách đó. Nhận xét trước khi xem kết quả: MicroRank có cùng bộ số (0,00; 0,40; 0,36) ở 5/6 loại lỗi; Bảng 8 bài TORAI ghi MicroRank 77,56 s/ca, TraceRCA 2,55 s/ca trên OB (mình chạy thử khoảng 13 s và 1 s/ca với cửa sổ 600 s).
- Soạn `scripts/so_moc.py` (so từng ô, ngưỡng 0,02) và bản nháp `moi-truong-ec2.md`.
- So `freeze-py312-pin` EC2 với của T-006 (laptop): mọi gói chung cùng phiên bản; khác chỉ ở gói riêng hệ điều hành, cách viết tên, và `pyarrow` (chỉ EC2). Lệch múi giờ của `--exclude-newer` không đổi bản gói nào.
- 07:19 UTC: MicroRank `py312-pin` xong 90/90 ca, 0 lỗi, đã nén (`runs/py312-pin/microrank.tar.gz` trên EC2).
- **X1 đã có** (`results/T-006/x1-chot-moi-truong.md`, ghi khoảng 14:20 giờ VN): **chốt `py312-pin`, không dừng.** Theo quyết định của Minh ở lượt 2: số chính thức của T-007 lấy từ `py312-pin`; `py312` giữ làm bằng chứng về ảnh hưởng của phiên bản. Khác nhỏ về cách dựng: T-006 tạo môi trường bằng `uv venv`, T-007 bằng `python3 -m venv` rồi `uv pip install --python`; bản gói như nhau (đã so freeze).
- **Chấm MicroRank `py312-pin`** (chép `microrank.tar.gz` về `results/T-007/runs/py312-pin/`; `cham/py312-pin-microrank.json`; chạy `cham.py` bằng `D:\RCA-ext\envs\py312`, chỉ đọc, `PYTHONDONTWRITEBYTECODE=1`): 90/90 ca ok. So Bảng 2 (`so_moc.py`): **19/21 ô lệch 0,000**; 2 ô vượt 0,02 đều ở LOSS (AC@3 0,333 so với 0,27; Avg@5 0,280 so với 0,19). AVERAGE Avg@5 0,347 so với 0,33 (+0,017). Theo tiêu chí: "lệch" (2 ô).
- **Giá trị trung gian MicroRank (QT5):** 87/90 ca có cùng 4 service đầu `frontendservice, currencyservice, productcatalogservice, recommendationservice`, bất kể loại lỗi và service gốc; 3 ca khác đều là LOSS (`currencyservice_loss_1`, `productcatalogservice_loss_1`, `recommendationservice_loss_1`). checkoutservice, emailservice không bao giờ xuất hiện. Một thứ hạng cố định như vậy cho đúng AC@1 0, AC@3 0,40, Avg@5 0,36 (currency hạng 2 → 0,8; productcatalog hạng 3 → 0,6; recommendation hạng 4 → 0,4; hai service còn lại 0; trung bình 0,36). Tức số mốc 0,00/0,40/0,36 ở 5 loại lỗi trong bài cũng khớp với một thứ hạng cố định.
- Đọc code `RCAEval/e2e/microrank.py` (chỉ đọc), hai điểm giải thích một phần: (1) `calculate_spectrum_without_delay_list` chỉ trả `top_max + 6` = 11 thao tác (`top_max=5`), nên thứ hạng chỉ có 3–4 service, AC@5 tối đa 0,6 ở OB; (2) trong `microrank()`, đồ thị "bất thường" dựng từ mọi span sau mốc tiêm (`anomal_df`), không chỉ trace bất thường; đồ thị "bình thường" dựng từ span trước mốc. **Chưa kiểm** rằng (2) là nguyên nhân thứ hạng gần như cố định; định kiểm bằng cách bắt giá trị trung gian (số trace bất thường, điểm phổ) trên vài ca sau khi các lượt chính chạy xong.
- 07:21 UTC: TraceRCA `py312-pin` xong 90/90 ca, 0 lỗi. **Chấm** (`cham/py312-pin-tracerca.json`): AVERAGE AC@1 0,111 / AC@3 0,656 / Avg@5 0,616 so với mốc 0,10 / 0,65 / 0,62 (lệch +0,011 / +0,006 / −0,004). 14/21 ô trong ngưỡng 0,02; 7 ô vượt ở DISK (AC@1 −0,067, AC@3 −0,067, Avg@5 −0,040), SOCKET (AC@1 +0,063, AC@3 +0,137), LOSS (AC@1 +0,063, AC@3 −0,063). Mỗi ô vượt tương đương 1–2 ca trên 15, lệch cả hai chiều. Theo tiêu chí: "lệch" (7 ô).
- Giá trị trung gian TraceRCA: service đứng đầu là frontendservice ở 72/90 ca, checkoutservice 17/90, recommendationservice 1/90. Tên thao tác ghép từ `serviceName` của span (service phát span), nên span client của bên gọi (ví dụ `checkoutservice_GetProduct`) đứng trước service bị lỗi; hạng của đáp án thường là 2–4. Phù hợp AC@1 thấp trong bài (0,10).
- 07:22–07:23 UTC: chạy lại 6 ca mỗi phương pháp (`py312-pin`) trong tiến trình mới (hash seed ngẫu nhiên khác): **12/12 file kết quả giống từng byte** với lượt chính (`runs/py312-pin/{microrank,tracerca}-lai.tar.gz` trên EC2). 07:23 UTC: bắt đầu E3 BOCPD `py312-pin`.
- 07:23–07:59 UTC: **E3 BOCPD `py312-pin` xong** (`runs/py312-pin/bocpd.tar.gz`). `reproduce_bocpd` in **P 0,76 / R 1,00 / F1 0,87**, đúng từng số với README BARO (mốc loại A). Kiểm từng ca (`tien-do.jsonl` của script bọc): **100/100 ca có điểm đổi giống hệt `naive_bocpd.json` tác giả lưu**; tính lại từ jsonl: TP 100, FP 31, FN 0 → P 0,7634, R 1,0000, F1 0,8658. FP (điểm đổi đầu tiên trước điểm 300) theo loại lỗi: cpu 10, loss 10, delay 9, mem 2. So Bảng 2 bài BARO (0,69 / 1 / 0,82): P +0,07, F1 +0,05; README tác giả tự ghi "a bit better than the numbers presented in the paper (Table 2)". Thời gian (không phải số đo): 16–23 s/ca, tổng 2163 s.
- Ghi chú kỹ thuật: khối nén `bocpd.tar.gz` chứa liên kết `data` → `~/rca/data/fse`; giải nén trên Windows phải `--exclude=bocpd/data`.
- 07:59 UTC: bắt đầu `chay_e2_e3.sh py312`. Chép về `results/T-007/runs/py312-pin/`: `microrank-lai.tar.gz`, `tracerca-lai.tar.gz`, `bocpd.tar.gz`.
- Ghi bảng so mốc `py312-pin` ra `cham/so-moc-py312-pin.json`.
- Chuẩn bị phép kiểm thêm (không cần nhãn, không đổi tham số), chạy sau khi lượt `py312` xong để không tranh CPU: `scripts/trung_gian_microrank.py` (bọc `trace_pagerank`, `calculate_spectrum_without_delay_list` để ghi số trace bất thường, ef/ep/nf, điểm Dstar2 từng thao tác; đọc code thấy `nf = w·(anomaly_list_len − anomaly_num_list)` có thể âm vì `anomaly_num_list` đếm mọi trace sau mốc qua thao tác, còn `anomaly_list_len` chỉ đếm trace bất thường; chưa kiểm); thêm tùy chọn `--tron <seed>` vào `chay_e2.py` (xáo thứ tự dòng span, mặc định tắt, lượt chính không đổi); `scripts/chay_kiem_them.sh` chạy hai việc trên bằng `py312-pin`.
- Bản nháp `results/T-007/kiem-dung-dan.md` (có các chỗ ghi "CHỜ") và `scripts/bang_md.py` (sinh bảng từ `cham/so-moc-*.json`). Sửa số TraceRCA trả 26–36 thao tác (không phải 33–34 như lượt thử).
- Giá trị trung gian thêm: tỉ lệ span trước/sau mốc trong cửa sổ 0,96–6,27; > 1,3 ở 8 ca: `checkoutservice_cpu_2` 6,27; `productcatalogservice_loss_{1,2,3}` 2,81/3,93/1,71; `currencyservice_loss_1` 1,84; `productcatalogservice_mem_{1,3}` 1,58/1,62; `recommendationservice_loss_1` 1,49. Cả 3 ca MicroRank lệch khỏi thứ hạng chung đều nằm trong nhóm này (chưa kiểm là nguyên nhân).

### Kết thúc phiên 1 — 03/10/2026 (bị cắt vì hết lượt dùng; E4 chưa xong)

**1. Đã làm:** E0, E1 xong; chạy thử; E2 + E3 `py312-pin` xong (số chính thức, X1 chốt bộ này): MicroRank lệch 2/21 ô (19 ô lệch 0,000; 2 ô ở LOSS), TraceRCA lệch 7/21 ô (AVERAGE khớp), BOCPD khớp README 0,76/1,00/0,87 và 100/100 ca trùng `naive_bocpd.json`. Chạy lại 12/12 ca giống từng byte. Lượt `py312` đang chạy nền trên EC2 (bắt đầu 07:59 UTC, dự kiến xong khoảng 09:00 UTC).
**2. File đã thay đổi:** `tasks/T-007-kiem-dung-dan-ec2/LOG.md`; `docs/STATE.md` (dòng T-007); `results/T-007/` (`kiem-dung-dan.md` nháp, `moi-truong-ec2.md` nháp, `moc-torai-bang2-trace.json`, `cham/`, `runs/py312-pin/` 5 khối, `scripts/`). EC2: chỉ `~/rca/` và gói apt.
**3. Kiểm tra:** hash dữ liệu; `pip check`; script chấm khớp `main.py` 18/18 ô; freeze `py312-pin` EC2 trùng bản laptop.
**4. Chưa chắc / chờ:** nguyên nhân các ô lệch (loại B) chưa kiểm; giả thuyết thứ hạng MicroRank gần cố định do đồ thị "bất thường" dựng từ mọi span sau mốc, và `nf` có thể âm: chưa kiểm.

**Bước tiếp theo chính xác (phiên sau, người làm):**
1. Kiểm `~/rca/runs/chay-py312.log` có `XONG_TAT_CA py312`. Chép `~/rca/runs/py312/*.tar.gz` về `results/T-007/runs/py312/`; chấm bằng `cham.py` → `cham/py312-{microrank,tracerca}.json`; `so_moc.py ... --json cham/so-moc-py312.json`; `bang_md.py cham/so-moc-py312-pin.json cham/so-moc-py312.json`; so BOCPD `py312`.
2. Chép lên EC2 bản mới của `scripts/chay_e2.py` (thêm `--tron`), `trung_gian_microrank.py`, `chay_kiem_them.sh` (nhớ `sed -i "s/\r$//"`), chạy `nohup bash ~/rca/scripts/chay_kiem_them.sh > ~/rca/runs/kiem-them.log 2>&1 &` (khoảng 25 phút; đã báo Minh). Chép `~/rca/runs/py312-pin/{microrank-trung-gian,tracerca-tron,microrank-tron}.tar.gz` và log E0, E1, thu (`~/rca/runs/e0`, `e1`, `thu`, `chay-*.log`) về `results/T-007/runs/`.
3. Điền mọi chỗ "CHỜ" trong `kiem-dung-dan.md` (grep "CHỜ"); hoàn tất `moi-truong-ec2.md` (dung lượng cuối); viết prompt phản biện Codex theo `docs/review-prompt.md` ở cuối LOG; cập nhật STATE "chờ phản biện"; báo Minh **Stop** EC2 (không Terminate).

**Lệnh cuối cùng đã chạy:** đọc tỉ lệ span trước/sau từ `tien-do.jsonl` MicroRank `py312-pin` (scratchpad). Một lệnh chờ nền (`bn5weswgy`) đang đợi lượt `py312` xong; vô hại nếu bị dừng.
- (Sau mục kết thúc phiên, 08:57 UTC) **Lượt `py312` xong** (`~/rca/runs/chay-py312.log`): MicroRank 90/90 ok, TraceRCA 90/90 ok, chạy lại 12/12 giống từng byte, BOCPD P/R/F1 0,76/1,00/0,87. Khối nén ở `~/rca/runs/py312/` trên EC2, **chưa chép về, chưa chấm**. Bước 1 của "Bước tiếp theo" chỉ còn chép và chấm. EC2 đang rảnh.

---

## Phiên 2 — 03/10/2026 — Claude — laptop Windows (i5-1240P) điều khiển EC2 qua SSH — vai trò: người làm

- Mở phiên. Việc Minh giao: kiểm lại trạng thái trên EC2 và file thật (không tin tóm tắt LOG); làm "Bước tiếp theo" 1–3 của phiên 1; so từng ô và nêu nguyên nhân khả thi; ghi phạm vi ảnh hưởng của R1 (REVIEW T-002) tới phép kiểm BOCPD; viết prompt phản biện nguyên văn mẫu (Q-44); chép đủ kết quả rồi mới báo Stop EC2.
- **Kiểm lại trên EC2, file thật** (10:41 UTC; đọc thẳng trong các khối nén `~/rca/runs/<env>/*.tar.gz`, không dựa LOG). EC2 vẫn bật, IP `3.104.124.160`, không còn tiến trình chạy.
  - `chay-py312-pin.log`, `chay-py312.log`: mỗi file có 1 dòng `XONG_TAT_CA <env>`; 0 dòng chứa "traceback"/"error".
  - Cả hai bộ: `microrank.tar.gz`, `tracerca.tar.gz` mỗi khối 90 file `results/*.json`, 0 `_failed.json`, `tien-do.jsonl` 90 dòng, 90 "ok", 0 Traceback trong `chay.log`, có dòng `XONG <phương pháp>`. `*-lai.tar.gz`: 6 file, `so-sanh.txt` 6 GIONG, 0 KHAC. `bocpd.tar.gz`: `tien-do.jsonl` 100 dòng, 100 `giong_tac_gia: true`, 0 dòng VUOT_NGAN_SACH/LOI, 0 Traceback, có `XONG E3`; `chay.log` in Precision 0.76, Recall 1.00.
  - `runs/e0/e0.log`, `runs/e1/e1.log`, `runs/thu/thu.log`: 0 Traceback; dòng cuối lần lượt `E0_XONG`, `E1_XONG, tổng lỗi: 0`, `THU_XONG`.
  - Kết luận: khớp tóm tắt phiên 1. Thiếu một việc: thư mục làm việc của lượt chạy thử (`~/rca/work/thu/`) chưa được nén; sẽ nén trước khi chép về.
- 10:41 UTC: chép lên EC2 `chay_e2.py` (có `--tron`), `trung_gian_microrank.py`, `chay_kiem_them.sh` (SHA-256 trên EC2 trùng bản repo); chạy nền `chay_kiem_them.sh` (log `~/rca/runs/kiem-them.log`).
- **Lượt hỏng** (giữ lại, luật cứng 10): bước 1 (soi trung gian MicroRank) dừng sau 3 s với `AttributeError: 'function' object has no attribute 'trace_pagerank'`. Nguyên nhân: lỗi của script tôi, `import RCAEval.e2e.microrank as M` trả về hàm vì `RCAEval/e2e/__init__.py` gán tên `microrank` của gói thành hàm. Sửa: `importlib.import_module("RCAEval.e2e.microrank")`. Lượt hỏng giữ ở `runs/py312-pin/microrank-trung-gian-hong1.tar.gz`; chạy lại bằng `scripts/chay_trung_gian_lai.sh` (10:43 UTC), song song với bước xáo (không ảnh hưởng tính đúng; thời gian không phải số đo).
- **Lỗi trong script bash của tôi, phát hiện khi đọc lượt hỏng:** dòng `echo "$(ts) mã thoát $?"` luôn in 0 vì `$(ts)` chạy trước và đặt lại `$?`. Ảnh hưởng: các dòng "mã thoát 0" trong `chay-py312-pin.log`, `chay-py312.log`, `kiem-them.log` không phản ánh mã thoát thật. Kết quả không bị ảnh hưởng: mọi khối đã kiểm độc lập (90/90 ok, 0 Traceback, có dòng XONG). `chay_trung_gian_lai.sh` đã viết đúng (`rc=$?`). Sửa `chay_e2_e3.sh`, `chay_kiem_them.sh` trong repo sau khi lượt xáo xong (không thay file trên EC2 khi bash đang chạy nó).
- **Chép và chấm `py312`** (`results/T-007/runs/py312/` 5 khối; `cham/py312-{microrank,tracerca}.json`; `cham/so-moc-py312.json`): MicroRank 2/21 ô lệch, TraceRCA 7/21 ô lệch, như `py312-pin`. **So hai bộ:** MicroRank 90/90 file và TraceRCA 90/90 file giống từng byte; BOCPD 100/100 ca cùng điểm đổi, P/R/F1 0,7634 / 1,0000 / 0,8658, `chay.log` in 0.76/1.00/0.87; `bang_md.py`: "cùng giá trị ở mọi ô" cho cả hai phương pháp. Tức bản thư viện (pandas 2.2.3 hay 3.0.6, v.v.) không đổi kết quả ba phương pháp trên dữ liệu này.
- **Soi trung gian MicroRank** (chạy lại 10:43 UTC, `runs/py312-pin/microrank-trung-gian.tar.gz`; lượt hỏng `-hong1`): 6/6 ca thứ hạng giống lượt chính (bọc không đổi kết quả). Đồ thị "bất thường" có đúng số trace bằng số trace sau mốc (3584/3584, 2388/2388, ...): **xác nhận** đồ thị này dựng từ mọi trace sau mốc. `nf < 0` ở 1–14/37 thao tác mỗi ca. Thứ tự điểm Dstar2 theo sát lưu lượng: hệ số tương quan hạng (Spearman) giữa điểm và số trace sau mốc qua thao tác, trên 37 thao tác, là 0,957 / 0,969 / 0,820 / 0,940 / 0,932 / 0,750 (currency_loss_1, productcatalog_loss_1, recommendation_loss_1, checkout_cpu_1, email_delay_1, currency_mem_1). Đọc `online_anomaly_detect_RCA` trong cùng file (vòng chạy chuyển từ MicroRank gốc): chia trace của cùng một cửa sổ thành `anomaly_list`, `normal_list` rời nhau rồi dựng hai đồ thị riêng; `microrank()` thì dựng đồ thị bất thường từ mọi span sau mốc, đồ thị bình thường từ span trước mốc. Chưa đọc code MicroRank gốc (`IntelligentDDS/MicroRank`).
- **Xáo thứ tự span, TraceRCA** (`runs/py312-pin/tracerca-tron.tar.gz`): 0/90 file giống lượt chính; cùng tập thao tác; hạng của đáp án đổi ở 22/90 ca; điểm sau xáo AVERAGE AC@1 0,16 / AC@3 0,67 / Avg@5 0,63 (lượt chính 0,111 / 0,656 / 0,616), ô đổi nhiều nhất DISK AC@1 0,13 → 0,33 (`tracerca-tron/cham.txt`).
- **Hòa điểm TraceRCA** (`scripts/hoa_diem_tracerca.py`, bọc tên `sorted` trong module, chạy thứ tự gốc và thứ tự xáo seed 1; `runs/py312-pin/tracerca-hoa.tar.gz`): thứ tự gốc giống lượt chính 90/90; điểm ji **giống hệt giữa hai thứ tự ở 90/90 ca**; 44/90 ca có nhóm hòa chạm top 10. Kết luận: TraceRCA đổi thứ hạng theo thứ tự dòng chỉ vì phá hòa theo thứ tự xuất hiện (`sorted` ổn định trên `anomal_df.operation.unique()`), không do sai số làm tròn.
- **R1 (REVIEW T-002) trên dữ liệu T-007:** `fse-ob/*/*/simple_data.csv`: 100/100 ca có `time` từ mốc −360 s đến +360 s, 360 dòng trước mốc, 361 dòng từ mốc. RE2-OB `traces.parquet`: `startTime` bắt đầu ở mốc −720 s ở 90/90 ca; kết thúc ở +720 s ở 87 ca, sớm hơn ở 3 ca: `checkoutservice_cpu_2` +39 s (cửa sổ 600 s chỉ có 10 846 span sau mốc so với 67 959 trước), `checkoutservice_mem_2` +432 s, `emailservice_disk_3` +590 s (hai ca sau không ảnh hưởng cửa sổ ±300 s).
- **Sắp xếp với khóa NaN trong TraceRCA** (phát hiện khi script khoảng hòa điểm cho giá trị lượt chính nằm ngoài khoảng, tức giả định "thứ hạng đã sắp giảm dần" sai). Ở `currencyservice_cpu_1` thứ hạng không giảm dần theo ji. Cơ chế khả dĩ: `ji = 2sc/(s+c)` = NaN khi thao tác không có span bất thường (0/0); `tracerca.py` gọi `sorted(..., reverse=True)` trên cả NaN rồi mới bỏ NaN. Kiểm (`scripts/hoa_diem_tracerca.py` lượt 3 ghi nguyên danh sách đưa vào `sorted`, `runs/py312-pin/tracerca-hoa3.tar.gz`; `scripts/phan_tich_sap_xep_tracerca.py` → `cham/sap-xep-tracerca-py312-pin.json`): áp đúng phép sắp của hàm lên danh sách đã ghi dựng lại thứ hạng **90/90 ca ở cả thứ tự gốc và thứ tự xáo** (xác nhận cơ chế); 90/90 ca có ji NaN (1–11 thao tác mỗi ca); **79/90 ca có thứ hạng không giảm dần theo ji**. Số ô lệch mốc > 0,02: lượt chính 7/21, thứ tự xáo 12/21, bỏ NaN trước khi sắp 11/21 (thứ tự gốc) và 11/21 (thứ tự xáo). Bỏ NaN trước khi sắp đổi hạng đáp án ở 13/90 ca. Một ô đổi tới 0,2 giữa hai thứ tự dòng (DISK AC@1 0,133 / 0,333; LOSS AC@3 0,467 / 0,600).
- Script `khoang_hoa_tracerca.py` (lượt `tracerca-hoa2`, `cham/khoang-hoa-tracerca-py312-pin.json`): khoảng tính theo giả định sắp đúng (bỏ NaN trước), nên không mô tả lượt đã chạy; chỉ dùng như khoảng cho biến thể "bỏ NaN trước khi sắp". `tracerca-hoa`, `tracerca-hoa2` là các lượt trước của cùng phép kiểm, ghi ít trường hơn; giữ lại (luật cứng 10).
- **Xáo thứ tự span, MicroRank** (10:44–11:11 UTC, `runs/py312-pin/microrank-tron.tar.gz`): 46/90 file giống, 44/90 khác (thứ tự thao tác trong nhóm hòa); **thứ hạng service giống 90/90 ca**, hạng đáp án giống 90/90; điểm (`microrank-tron/cham.txt`) trùng lượt chính ở mọi ô. Tức thứ tự dòng không giải thích 2 ô LOSS của MicroRank. `chay_kiem_them.sh` xong (`XONG_KIEM_THEM`).
- Nguyên nhân khả thi còn lại cho MicroRank LOSS chưa kiểm: tập span khác (cửa sổ dài hơn, hoặc bộ đọc lọc span khác). Kiểm cần chạy biến thể cửa sổ khác `--length 10` của SPEC → đề xuất với Minh, chưa chạy.

### Quyết định của Minh trong phiên 2
- Chạy biến thể cửa sổ ±600 s (`--length 20`) cho **cả MicroRank và TraceRCA, 90 ca**, bộ `py312-pin` (lệch SPEC: SPEC ghi ±300 s; chỉ để chẩn đoán và xác định cấu hình). Minh nêu bằng chứng từ T-006: BARO trên torai-SS với `--length 20` trùng đến 2 chữ số mọi ô Bảng 3 bài TORAI, tức các baseline trong bài TORAI chạy `--length 20` (mặc định của `main.py` từ 27/12/2024; trước đó là 10). Yêu cầu: báo cả hai cấu hình; chọn cấu hình chính thức theo bằng chứng về cấu hình của tác giả, không theo cấu hình nào khớp hơn; ghi bằng chứng vào `kiem-dung-dan.md`.
- Kiểm bằng chứng Minh nêu (chỉ đọc): T-006 LOG ghi BARO `--length 20` trên torai-SS trùng mọi ô T1/T3/A5 dòng BARO Bảng 3 bài TORAI (`results/T-006/runs/soi-baro-torai-ss-length20.tar.gz`). Lịch sử git RCAEval (`D:\RCA-ext\src\RCAEval`): commit `61326e5` (27/12/2024) đổi `parser.add_argument("--length", ..., default=None)` thành `default=20` trong `main.py` (trước đó `None` được gán 10).
- Thêm `--length` vào `scripts/chay_e2.py` (mặc định 10; ghi `length` vào từng dòng tiến độ); `scripts/chay_l20.sh` (kiểm hồi quy + biến thể ±600 s). 11:21 UTC: **kiểm hồi quy** `chay_e2.py` bản mới, mặc định, TraceRCA 6 ca: 6/6 file giống từng byte lượt chính (`runs/py312-pin/tracerca-hoi-quy.tar.gz`). Bắt đầu biến thể `--length 20` (TraceRCA rồi MicroRank, 90 ca, `py312-pin`; log `~/rca/runs/chay-l20.log`).
- 11:21–11:24 UTC: **TraceRCA ±600 s** (`runs/py312-pin/tracerca-L20.tar.gz`; `cham/py312-pin-tracerca-L20.json`, `cham/so-moc-py312-pin-tracerca-L20.json`): 90/90 ok. **3/21 ô lệch > 0,02**: DISK AC@3 −0,067, DISK Avg@5 −0,027, SOCKET AC@1 +0,063 (mỗi ô 1 ca trên 15); AVERAGE 0,111 / 0,644 / 0,618 so với mốc 0,10 / 0,65 / 0,62. Theo tiêu chí: "lệch". MicroRank ±600 s đang chạy (bắt đầu 11:24 UTC).
- Viết lại `results/T-007/kiem-dung-dan.md` (bản đủ, còn chỗ "CHỜ L20" cho MicroRank ±600 s). Thêm `scripts/thong_ke.py` (đọc thẳng các khối nén, ghi `cham/thong-ke.json`) và `scripts/bien_file.py` (chạy trên EC2, `runs/bien-file.tar.gz`) để mọi số trong báo cáo có file nguồn; đối chiếu lại các số đã viết với `thong-ke.json`: khớp.
- 11:24–12:18 UTC: **MicroRank ±600 s** (`runs/py312-pin/microrank-L20.tar.gz`; `cham/py312-pin-microrank-L20.json`, `cham/so-moc-py312-pin-microrank-L20.json`): 90/90 ok. **0/21 ô lệch > 0,02** (lệch lớn nhất 0,003; LOSS AC@3 0,267, Avg@5 0,187 so với mốc 0,27 / 0,19). Theo tiêu chí: **khớp**. So với ±300 s: hạng đáp án đổi ở đúng 3 ca LOSS (`recommendationservice_loss_2`, `_loss_3`, `productcatalogservice_loss_2`, đều thành trượt); 82/90 ca vẫn cùng 4 service đầu (`cham/thong-ke.json`). Cấu hình so mốc chính thức (±600 s) đã viết trong `kiem-dung-dan.md` mục 1.3 trước khi xem kết quả biến thể, theo bằng chứng Minh nêu và lịch sử git.
- Chép về repo: `runs/e0/`, `runs/e1/`, `runs/thu/` (thêm `thu-work.tar.gz`: thư mục làm việc lượt thử, bỏ bản chép dữ liệu `fse-ob`), log tổng `runs/chay-py312-pin.log`, `chay-py312.log`, `kiem-them.log`, `trung-gian-lai.log`, `chay-l20.log`. Cập nhật `moi-truong-ec2.md` (lệnh phép kiểm thêm, tùy chọn mới của `chay_e2.py`, lỗi ghi mã thoát, giải nén `bocpd.tar.gz`). Điền hết chỗ "CHỜ" trong `kiem-dung-dan.md` (grep "CHỜ" = 0).
- **Đối chiếu trước khi báo Stop:** 34/34 file trong `~/rca/runs` trên EC2 có trong `results/T-007/runs/`, SHA-256 trùng từng file; không file nào chỉ có ở một bên. Không còn tiến trình chạy. Dung lượng `~/rca` 15 GB; đĩa trống 11 GB (ghi vào `moi-truong-ec2.md` mục 5).
- **Tác dụng phụ ngoài Phạm vi ghi (báo theo Luật 0 mục 8):** `~/.sudo_as_admin_successful` (file rỗng, 06:40 UTC phiên 1), do Ubuntu tự tạo khi `sudo apt-get` của E0 chạy lần đầu. Đề xuất hoàn tác: `rm ~/.sudo_as_admin_successful` (chờ Minh duyệt; không ảnh hưởng gì nếu để nguyên). `~/.cache` có từ 05:51 UTC (trước E0), không bị task này ghi.
- Soát lại toàn bộ `kiem-dung-dan.md`: sửa mục 9 (MicroRank đã khớp ở ±600 s); tự đối chiếu bằng chứng T-006 (`results/T-006/cham/soi-baro-torai-ss-length20.txt` so với dòng BARO Bảng 3 trong `results/T-006/scripts/moc.py`): 21/21 ô trùng khi làm tròn 2 chữ số. Chạy lại `thong_ke.py` sau khi có MicroRank ±600 s (`cham/thong-ke.json` cập nhật).

### Kết thúc phiên 2 — 03/10/2026

**1. Đã làm:**
- Kiểm lại trạng thái trên EC2 bằng file thật (mọi khối đủ ca, có dấu xong, 0 Traceback).
- Chép, chấm `py312`: giống hệt `py312-pin` ở mọi ca và mọi ô.
- Phép kiểm thêm, đều không đổi tham số của phương pháp:
  - soi trung gian MicroRank: thứ hạng theo lưu lượng; đồ thị bất thường dựng từ mọi trace sau mốc;
  - xáo thứ tự span: MicroRank không đổi điểm, TraceRCA đổi;
  - hòa điểm và sắp xếp NaN của TraceRCA: 79/90 ca thứ hạng không giảm dần; cơ chế dựng lại được 90/90 ca;
  - biên file theo R1.
- Biến thể ±600 s (Minh duyệt): MicroRank khớp 21/21 ô; TraceRCA lệch 3/21 ô (mỗi ô 1 ca; AVERAGE khớp).
- Viết xong `kiem-dung-dan.md` (grep "CHỜ" = 0) và `moi-truong-ec2.md`.
- Chép đủ kết quả về repo (34/34 file trùng SHA-256 với EC2).

**2. File đã thay đổi trong phiên:**
- `tasks/T-007-kiem-dung-dan-ec2/LOG.md`; `docs/STATE.md` (dòng T-007).
- `results/T-007/`:
  - `kiem-dung-dan.md`, `moi-truong-ec2.md`;
  - `cham/` (thêm `py312-*.json`, `so-moc-py312*.json`, `*-L20.json`, `sap-xep-tracerca-py312-pin.json`, `khoang-hoa-tracerca-py312-pin.json`, `thong-ke.json`);
  - `runs/` (thêm `py312/`, các khối kiểm thêm trong `py312-pin/`, `bien-file.tar.gz`, `e0/`, `e1/`, `thu/`, log tổng);
  - `scripts/`: sửa `chay_e2.py` (`--tron`, `--length`), `trung_gian_microrank.py`, `chay_e2_e3.sh`, `chay_kiem_them.sh`, `hoa_diem_tracerca.py`, `khoang_hoa_tracerca.py`; thêm `chay_trung_gian_lai.sh`, `phan_tich_sap_xep_tracerca.py`, `chay_l20.sh`, `bien_file.py`, `thong_ke.py`, `bang_md.py`.
- EC2: chỉ `~/rca/` (script, work, runs). Tác dụng phụ từ phiên 1: `~/.sudo_as_admin_successful`, chờ Minh quyết xóa.

**3. Kiểm tra:**
- Kiểm hồi quy `chay_e2.py`: 6/6 file giống.
- Bọc hàm không đổi kết quả: 6/6 ca MicroRank, 90/90 ca TraceRCA giống lượt chính.
- Đối chiếu bằng chứng T-006: 21/21 ô.
- Đối chiếu số trong báo cáo với `cham/thong-ke.json`.
- SHA-256: 34/34 file.

**4. Chưa chắc / cần Minh quyết:**
- Cấu hình ±600 s là cấu hình so mốc chính thức dựa trên bằng chứng gián tiếp (mục 1.3 `kiem-dung-dan.md`).
- Chưa đối chiếu code MicroRank gốc.
- Hai phát hiện về bản RCAEval cần Minh biết trước khi dùng số ở P3:
  - MicroRank xếp hạng theo lưu lượng;
  - TraceRCA sắp xếp với khóa NaN.
- Đề xuất xóa `~/.sudo_as_admin_successful` trên EC2.
- Báo Minh **Stop** EC2: đã chép đủ kết quả.

**Bước tiếp theo:** Minh Stop EC2 (không Terminate); mở phiên Codex phản biện bằng prompt dưới đây. Sau khi có `REVIEW.md`: phiên mới của người làm theo "Prompt cho người làm phản hồi phản biện" trong `docs/review-prompt.md`.

**Lệnh cuối cùng đã chạy:** dựng prompt phản biện từ `docs/review-prompt.md` (kiểm nguyên văn bằng máy), rồi ghi mục này.

### Prompt phản biện (Codex)

Chạy: `codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-007-kiem-dung-dan-ec2\REVIEW.md "<dán prompt>"`

Prompt = nguyên văn "Prompt chung" của `docs/review-prompt.md` (chỉ điền chỗ `<...>`) + nguyên văn khối trọng tâm G1 (cổng hiện tại).

```text
Bạn là người phản biện độc lập cho task T-007 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-007-kiem-dung-dan-ec2/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-007-kiem-dung-dan-ec2/SPEC.md, tasks/T-007-kiem-dung-dan-ec2/LOG.md, các file đầu ra: results/T-007/kiem-dung-dan.md, results/T-007/moi-truong-ec2.md, results/T-007/moc-torai-bang2-trace.json, results/T-007/cham/, results/T-007/scripts/, results/T-007/runs/; code tác giả (chỉ đọc): D:\RCA-ext\src\RCAEval (revision 259ea41), D:\RCA-ext\src\baro (revision e35f4ec); dữ liệu thô chỉ có trên EC2, không truy cập từ laptop; kết quả và log từng ca nằm trong results/T-007/runs/*.tar.gz,
và kết quả `git diff 38d3c1b` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```

---

## Phiên 3 — 03/10/2026 — Claude — laptop Windows — vai trò: người làm, bước 7 (phản hồi phản biện)

- Mở phiên. Minh báo đã có `REVIEW.md`. Làm theo "Prompt cho người làm phản hồi phản biện" (`docs/review-prompt.md`).

### Tự soát độc lập (ghi trước khi mở REVIEW.md)
- **N1 — thiếu mục WHY cho cấu hình cửa sổ ±600 s.** `kiem-dung-dan.md` mục 1.3 chọn ±600 s làm cấu hình so mốc chính thức (lệch SPEC ±300 s), nhưng `docs/WHY.md` chưa có mục nào (grep WHY trong `kiem-dung-dan.md`: 0). Luật cứng 3 yêu cầu có mục WHY trước khi dùng trong kết quả. Mức: KHÔNG CHẶN cho tính đúng của số (hai cấu hình đều báo đủ), nhưng thiếu theo luật. Sửa: đề xuất mục WHY (chọn gì, bằng chứng, phương án đã xét, kết luận phụ thuộc).
- **N2 — câu "hash seed ngẫu nhiên khác" chưa kiểm.** LOG phiên 1 và `kiem-dung-dan.md` mục 2.4/3.5 nói chạy lại trong tiến trình mới với hash seed khác. Script không đặt `PYTHONHASHSEED` (grep: 0), nên seed khác là do mặc định của Python (ngẫu nhiên mỗi tiến trình), không ghi lại giá trị. Kết luận "6/6 file giống" vẫn đúng; chỉ câu về seed là suy ra. Mức: KHÔNG CHẶN. Sửa: đổi câu thành "tiến trình mới (Python chọn hash seed ngẫu nhiên mặc định; không ghi giá trị)".
- **N3 — file `cham/khoang-hoa-tracerca-py312-pin.json` dễ đọc sai.** Khoảng trong file giả định thứ hạng đã sắp đúng, nên cột lượt chính nằm ngoài khoảng ở nhiều ô. Docstring script đã ghi; `kiem-dung-dan.md` không dùng file này. Mức: KHÔNG CHẶN. Sửa: thêm trường chú thích vào JSON, hoặc để nguyên vì báo cáo không dẫn.
- **N4 — đổi cấu hình sau khi thấy kết quả lệch (AGENTS mục 11).** Biến thể ±600 s chạy sau khi thấy ±300 s lệch. Giảm nhẹ: bằng chứng (git `61326e5`, BARO torai-SS của T-006) có trước khi chạy; Minh duyệt kèm điều kiện chọn theo bằng chứng; báo cả hai cấu hình. Rủi ro còn lại: bằng chứng gián tiếp cho trace. Đã nêu trong báo cáo mục 1.3, 9. Mức: KHÔNG CHẶN.
- Đã soát không thấy: nhãn lọt vào phương pháp (mốc tiêm dùng ở chế độ biết mốc như SPEC; tên ca chỉ đặt tên file và chấm); số trong báo cáo đã đối chiếu `cham/thong-ke.json`, `so-moc-*.json`; Tiêu chí xong của SPEC đạt (trừ việc Stop EC2 do Minh làm).

### Đánh giá từng điểm của reviewer (chi tiết ở bảng cuối `REVIEW.md`)
- **R1 (CHẶN) — đúng.** Hướng dẫn E0/E1 chuyển hướng log vào thư mục chưa tồn tại. Lượt thật chạy được vì phiên 1 đã `mkdir` tay qua SSH, nhưng lệnh đó không vào tài liệu. Phạm vi rộng hơn một chút: `thu_duong_ong.sh` cùng lỗi; thiếu lệnh `scp`.
- **R2 — đúng.** Đã kiểm `microrank.py:626–627` (đặt lại cạnh ở mỗi span) và đọc code gốc `IntelligentDDS/MicroRank@efd85e8` (`preprocess_data.py` tích lũy cạnh trên trace của tập đã chia; `online_rca.py` chia trace bằng `trace_list_partition` rồi dựng hai đồ thị). Hai nhóm chồng nhau: ít nhất 699 trace ở `checkoutservice_cpu_1` (`cham/thong-ke.json`). Chưa đo tác động của hai sai lệch lên điểm.
- **R3 — đúng.** Trùng N1, N4.
- **R4 — đúng.** AC@5 thực tế 52/90 (±300 s), 49/90 (±600 s); trần 0,6 do hai service vắng, không do cắt 11 thao tác.
- Không có điểm nào tôi không đồng ý. Không thấy đề xuất sửa nào của reviewer có mặt trái đáng kể; R2 đề xuất không suy tác động, tôi đồng ý.

### Đề xuất sửa, gom theo file (chưa sửa; chờ Minh quyết)
1. `results/T-007/moi-truong-ec2.md` (R1): thêm bước 0 vào mục 2, trước E0:
   `ssh ... 'mkdir -p ~/rca/scripts ~/rca/runs/e0 ~/rca/runs/e1 ~/rca/runs/thu'`; `scp -i ... results/T-007/scripts/* ubuntu@<IP>:rca/scripts/`. Ghi rằng phiên 1 đã chạy các lệnh này tay.
2. `results/T-007/scripts/thu_duong_ong.sh`, `e0_dung_moi_truong.sh`, `e1_tai_du_lieu.py` (R1): sửa dòng "Chạy:" trong chú thích đầu file, thêm `mkdir -p` trước `nohup`. Chỉ đổi chú thích, không đổi hành vi.
3. `results/T-007/kiem-dung-dan.md`:
   - §2.3 (R2): thêm hai sai lệch của `microrank()` bản RCAEval so với code gốc `efd85e8`: cạnh gọi bị đặt lại ở mỗi span; hai nhóm trace chồng nhau (≥ 699 trace ở `checkoutservice_cpu_1`, cả 6 ca có chồng). Ghi rõ chưa đo tác động. Thay câu "chưa kiểm với code gốc" bằng nội dung đã đối chiếu.
   - §2.3 (R4): đổi "AC@5 tối đa ở OB vì vậy là 0,6" thành: hàm chỉ trả 11 thao tác; trên các thứ hạng thu được, checkoutservice và emailservice luôn vắng nên 36/90 ca chắc chắn trượt, AC@5 tối đa 0,6 cho tập thứ hạng này (thực tế 52/90 ở ±300 s, 49/90 ở ±600 s).
   - §9 (R2): bỏ gạch "code MicroRank gốc chưa đọc"; thay bằng giới hạn: chưa đo tác động của hai sai lệch.
   - §10 (R3): đổi câu "So với số của bài thì phải dùng ±600 s" thành "T-007 dùng ±600 s làm cấu hình tham chiếu theo bằng chứng gián tiếp (mục 1.3); cửa sổ tác giả dùng cho baseline trace chưa xác minh". Câu MicroRank ở §10: thêm "khớp số của bản RCAEval trong cấu hình đã chạy; không xác nhận cơ chế MicroRank gốc".
   - §2.4, §3.5 (N2): "hash seed" → "tiến trình mới; Python dùng hash seed ngẫu nhiên mặc định, không ghi giá trị".
4. `docs/WHY.md` (R3, N1): thêm mục (số theo thứ tự sau WHY-15 của T-006 nếu được duyệt, tạm WHY-16):
   > **WHY-16. Cấu hình cửa sổ tham chiếu khi so MicroRank, TraceRCA với Bảng 2 bài TORAI — Đề xuất (G1)**
   > - Chọn: ±600 s quanh mốc tiêm (`--length 20`) làm cấu hình tham chiếu khi so với số bài TORAI; báo kèm ±300 s (SPEC T-007).
   > - Vì sao: `main.py` RCAEval đổi mặc định `--length` thành 20 từ commit `61326e5` (27/12/2024), trước bài TORAI (2026); BARO `--length 20` trùng 21/21 ô Bảng 3 bài TORAI (T-006).
   > - Phương án đã xét: ±300 s theo `docs/TORAI.md` (đó là lệnh chạy chính TORAI, không phải baseline); toàn ca (±720 s), không có bằng chứng.
   > - Giới hạn: bằng chứng gián tiếp với hai baseline trace; tác giả không công bố bộ đọc trace. Kết quả biến thể không dùng để chọn.
   > - Kết luận phụ thuộc: kết luận "khớp" của MicroRank và số ô lệch của TraceRCA trong `results/T-007/kiem-dung-dan.md`.
5. `results/T-007/cham/khoang-hoa-tracerca-py312-pin.json` (N3, tùy chọn): thêm trường `ghi_chu` nêu khoảng giả định sắp đúng.
6. EC2 (từ phiên trước, vẫn chờ): `rm ~/.sudo_as_admin_successful`; Stop EC2.

### Kết thúc phiên 3 — 03/10/2026
1. Đã làm: tự soát (N1–N4, ghi trước khi mở REVIEW); kiểm lại bằng chứng R1–R4 trên file, code RCAEval và code MicroRank gốc (tải `preprocess_data.py`, `online_rca.py` ở `efd85e8` vào thư mục tạm, chỉ đọc); điền bảng phản hồi cuối `REVIEW.md`; đề xuất sửa theo file.
2. File đã thay đổi: `tasks/T-007-kiem-dung-dan-ec2/REVIEW.md` (chỉ bảng phản hồi), `tasks/T-007-kiem-dung-dan-ec2/LOG.md`, `docs/STATE.md` (dòng T-007). Không sửa file đầu ra nào.
3. Kiểm tra: grep dòng lệnh, đọc code hai bản MicroRank, tính lại số chồng trace và AC@5 từ `cham/*.json`.
4. Cần Minh quyết: sửa điểm nào trong danh sách 1–6; duyệt WHY-16; Stop EC2.
- Bước tiếp theo: Minh quyết; người làm sửa trong task (AGENTS mục 5 bước 8), ghi LOG.
- Lệnh cuối: ghi mục này và sửa STATE.

---

## Phiên 3 (tiếp) — 03/10/2026 — sửa theo phản biện (AGENTS mục 5 bước 8)

### Quyết định của Minh
- "duyệt": cả 6 mục đề xuất sửa ở phiên 3 (gồm WHY-16 và xóa `~/.sudo_as_admin_successful` trên EC2).
- Mục 6 (EC2): SSH tới `3.104.124.160` hết thời gian chờ (máy có lẽ đã Stop). **Chưa xóa** `~/.sudo_as_admin_successful`; làm khi máy bật lại (cần IP mới).
- Mục 1–2 (R1): `moi-truong-ec2.md` mục 2 thêm "Bước 0" (`mkdir -p ~/rca/scripts ~/rca/runs/{e0,e1,thu}`, `scp` script, `sed` bỏ CR nếu cần); hai lệnh E0, E1 thêm `mkdir -p` trước `nohup`. Dòng "Chạy:" ở đầu `e0_dung_moi_truong.sh`, `e1_tai_du_lieu.py`, `thu_duong_ong.sh` thêm `mkdir -p` (chỉ chú thích; `bash -n`, `ast.parse` đạt).
- Mục 3: `kiem-dung-dan.md` §2.3 thêm đối chiếu code MicroRank gốc (hai sai lệch, chưa đo tác động) và tách trần AC@5 (R2, R4); §2.4, §3.5 sửa câu hash seed (N2); §9 thay gạch "code gốc chưa đọc"; §10 sửa hai câu (R3); §1.3 trỏ WHY-16.
- Mục 4: thêm WHY-16 vào `docs/WHY.md`. Lưu ý: WHY-15 (đề xuất của T-006) chưa có trong file, nên tạm có khoảng trống số 15.
- Mục 5: thêm trường `ghi_chu` vào `cham/khoang-hoa-tracerca-py312-pin.json`.
- File thay đổi: `results/T-007/{moi-truong-ec2.md,kiem-dung-dan.md}`, `results/T-007/scripts/{e0_dung_moi_truong.sh,e1_tai_du_lieu.py,thu_duong_ong.sh}`, `results/T-007/cham/khoang-hoa-tracerca-py312-pin.json`, `docs/WHY.md`, LOG, STATE (dòng T-007).
- Bước tiếp theo: Minh duyệt đóng task; khi bật EC2: `rm ~/.sudo_as_admin_successful`; đề xuất commit nếu Minh muốn.
