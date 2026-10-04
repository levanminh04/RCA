# T-016 — Hồ sơ kỹ thuật TORAI, kèm lõi RCD và biến thể RCD

- **Trạng thái:** đã duyệt 04/10/2026, theo ủy quyền tự duyệt SPEC của Minh (prompt Đợt 1 ngày 04/10/2026; ghi ở LOG phiên 1). Ngoại lệ chỉ cho bước duyệt SPEC; mọi luật khác của AGENTS giữ nguyên.
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1 — **Cổng:** G1

## Mục tiêu

- Trả lời nhận xét đầu tiên của cô: "chưa sâu kỹ thuật của từng phương pháp" (MRP §2.1, P1). Phục vụ RQ1 (cơ chế của phương pháp đã có).
- Minh đọc hiểu cơ chế TORAI và lõi RCD mà không cần đọc code.
- Task tổng hợp G1 có đủ dữ kiện về đầu vào, điều kiện chạy và chi phí của TORAI, RCD (file `yeu-cau-dau-vao.csv`).
- Câu hỏi cụ thể:
  1. TORAI và RCD làm từng bước gì, bằng công thức nào, tham số mặc định ở đâu trong code?
  2. Code chính thức (RCAEval `259ea41`) khác bài TORAI và RCD gốc ở đâu? Riêng lỗi giảm mẫu hai lần: lỗi hay chủ ý, ảnh hưởng ra sao, nên dùng bản nào ở P3?
  3. Muốn chạy TORAI trên dataset ngoài RCAEval thì phải dựng `logts`, `tracets` thế nào?
  4. Kết quả dao động bao nhiêu giữa các lần chạy, do đâu?
  5. Ở quy mô Train Ticket, TORAI chạy có đúng và có tốn không?
  6. Hai điểm còn mở của T-006 (RCD torai-OB cửa sổ 20 chỉ 46/90 ca; chạy lại trên Linux) giải được đến đâu trong Q-40?

## Đầu vào

| Đầu vào | Đường dẫn | Ghi chú |
|---|---|---|
| Danh sách phương pháp, revision | `results/T-001/danh-sach-phuong-phap.md` (mục 3a dòng 9, 8.1, 9) | RCAEval `259ea41…`, RCD gốc `373882c…` |
| Đo khả thi | `results/T-005/do-kha-thi.md`, `results/T-005/runs/` | thời gian TORAI, RCD trên một ca TT |
| Ghi chú REVIEW T-005 R1 | cuối `tasks/T-006-kiem-dung-dan-laptop/LOG.md` | giả thuyết giảm mẫu hai lần |
| Kiểm đúng đắn T-006 | `results/T-006/kiem-dung-dan.md` mục 6, 7, 10, 11; `results/T-006/cham/`; `results/T-006/runs/*.tar.gz` | kết quả RCD, TORAI chưa đặt seed |
| Code RCAEval | `D:\RCA-ext\src\RCAEval` (`259ea41`): `RCAEval/e2e/torai.py`, `rcd.py`, `__init__.py`, `RCAEval/io/time_series.py`, `main.py`, `RCAEval/benchmark/evaluation.py`, `lib/` (5 file vá) | chỉ đọc |
| RCD gốc | `D:\RCA-ext\work\T-016\src\rcd` (`azamikram/rcd` `373882c`) | chỉ đọc |
| Bài TORAI | arXiv `2604.13522v1`, bản HTML | chép text vào scratchpad để đọc; không vào repo |
| Bài RCD | NeurIPS'22, PDF chính và phụ lục trên proceedings.neurips.cc | như trên |
| Môi trường | `D:\RCA-ext\envs\py38-rcdlock` (chạy TORAI, RCD); `py312-pin` (chấm điểm bằng `Evaluator` của RCAEval); `T-016-cong-cu` (đọc parquet, Drain) | không sửa hai môi trường đầu |
| Dữ liệu | `D:\RCA-ext\data\torai-OB`, `torai-SS` (90 + 90 ca), `torai-TT/ts-route-service_socket/1`; `data/rcaeval/re2ob_productcatalogservice_loss_1`; 30 ca dev `data/rcaeval/re2tt_*` (chỉ để chứng minh trùng ca); `D:\RCA-ext\dl\torai-data.zip` (chỉ 30 thư mục `torai-TT` trùng tên ca dev) | xem "Dữ liệu được dùng" |

### Dữ liệu được dùng (gioi_han của prompt)

- Không mở `data/locked/`.
- `torai-TT` trong zip có 90 thư mục, gồm cả ca test. Chỉ giải nén đúng 30 thư mục mang tên trùng 10 ô dev × 3 lần (`ts-auth-service_cpu/1..3`, …). Trước khi dùng một ca, chứng minh trùng ca dev: cùng mốc tiêm (mốc tiêm của `torai-TT` = thời điểm đầu + 720 s, như cách cắt đối xứng của RCAEval), và `simple_metrics.csv` trùng từng giá trị với `metrics.parquet` của ca dev cùng tên. Ca nào không trùng thì không dùng, không chạy phương pháp, ghi lại.
- Chỉ chạy phương pháp trên ca đã từng được chạy: torai-OB, torai-SS, `torai-TT/ts-route-service_socket/1`, 30 ca dev RE2-TT (dưới dạng `torai-TT` đã chứng minh trùng). `re2ob_productcatalogservice_loss_1` chỉ dùng để dựng `logts`/`tracets` và so; nếu dựng được thì được chạy TORAI trên bản dựng của ca này (ca có trong danh sách được phép).
- Ghi mọi ca đã chạy vào `results/T-016/ca-da-chay.csv`.

## Đầu ra

Trong `results/T-016/`:

| File | Nội dung |
|---|---|
| `ho-so-torai.md` | Hồ sơ TORAI đủ 7 mục của MRP P1 + 2 mục thêm (đường nhãn; yêu cầu đầu vào trên dataset khác). Có phần riêng giải thích lõi RCD (Ψ-PC cục bộ, F-node, chia khối, vòng α, cách xếp). Có đoạn "Biến thể RCD" (khác TORAI ở bước nào). |
| `giam-mau-hai-lan.md` | Lỗi giảm mẫu hai lần và ghép theo chỉ số: bằng chứng trên code, trên ca (cửa sổ 10, 20), lỗi hay chủ ý, bản sửa, số trước/sau sửa so với số công bố, xung đột "tái lập" và "chạy đúng", đề xuất bản cho P3. |
| `dung-logts-tracets.md` | Đặc tả dựng `logts`, `tracets_err`, `tracets_lat` từ log/trace thô; kết quả dựng lại trên `re2ob_productcatalogservice_loss_1` so với ca trùng trong torai-OB. |
| `ngau-nhien.md` | Nguồn ngẫu nhiên, seed, số lần chạy, phương sai giữa các lần. |
| `quy-mo-tt.md` | TORAI (gốc, sửa) và RCD ở quy mô Train Ticket. |
| `diem-mo-t006.md` | T-006 mục 11 điểm 3 và 5. |
| `kiem-khong-nhan.md` | Kết quả các phép kiểm không cần nhãn (mục "Kiểm đúng đắn"). |
| `vi-du-tinh-tay.md` | Ví dụ tính tay trên một ca, script độc lập khớp code chính thức. |
| `yeu-cau-dau-vao.csv` | Đúng 16 cột prompt quy định; một dòng mỗi phương pháp/biến thể/bộ phát hiện. |
| `ca-da-chay.csv` | ca, file nguồn, phương pháp, mục đích, lý do (a/b/c). |
| `dinh-chinh-task-cu.md` | Vấn đề ở T-000…T-012 (task, file:dòng, sai gì, bằng chứng, kết luận bị ảnh hưởng, đã làm gì, đề xuất đoạn cũ → đoạn mới). Không có thì ghi "không có". |
| `de-xuat-tai-lieu-chung.md` | Nháp nguyên văn cho WHY, LESSONS, DECISIONS… (file đích, đoạn cũ → đoạn mới, lý do, kết luận phụ thuộc). |
| `moi-truong.md` | Cách dựng môi trường mới (`T-016-cong-cu`, môi trường Python 3.8 trên EC2), phiên bản ghim. |
| `moc-cong-bo.json` | Số công bố tra trước khi chạy (Bảng 2, 3, 4, 8, 9 bài TORAI; Bảng 1 bài RCD; `docs/TORAI.md`; `docs/SETUP.md`). |
| `scripts/`, `runs/`, `cham/` | Script, log và đầu ra từng lượt (nén), điểm. |

Trong `src/torai/`: bản sửa TORAI (`torai_sua.py`, `__init__.py`). Chỉ đổi đúng các dòng lỗi; phần còn lại gọi lại code RCAEval.

## Phạm vi ghi

Chỉ ghi vào các đường dẫn dưới, cộng `LOG.md` của task này và đúng một dòng T-016 trong `docs/STATE.md` (đọc lại trước và sau khi ghi; thay đúng chuỗi; không ghi lại cả file).

- `tasks/T-016-ho-so-torai/` (SPEC.md, LOG.md)
- `results/T-016/`
- `src/torai/`
- `D:\RCA-ext\work\T-016\` (code RCD gốc, dữ liệu giải nén từ zip, thư mục làm việc từng lượt)
- `D:\RCA-ext\envs\T-016-<tên>` (môi trường mới, nếu cần)
- `~/rca/T-016/` trên EC2 (môi trường, dữ liệu được phép, lượt chạy, cache, tmp)

Không ghi: AGENTS, CLAUDE, MRP, WHY, DECISIONS, LESSONS, `docs/knowledge/`, `docs/reference/`, `docs/review-prompt.md`, `data/README.md`, `requirements.txt`, file của task khác, `D:\RCA-ext\envs\` (trừ môi trường mới), `D:\RCA-ext\src\`, `~/rca/envs`, `~/rca/src`, `~/rca/data`.

## Các bước

Xếp theo phụ thuộc thật (SL32). Cột "Cần" ghi bước nào phải xong trước. Việc không phụ thuộc thì làm ngay, song song được.

| Bước | Việc | Cần | Đầu ra | Lệnh kiểm |
|---|---|---|---|---|
| S0 | Chèn dòng T-016 "đang làm" vào STATE (đọc lại trước/sau). Kiểm đầu vào: revision RCAEval, RCD gốc; file dữ liệu; môi trường. Chứng minh trùng ca: (a) `torai-TT/ts-route-service_socket/1` ≡ `re2tt_ts-route-service_socket_1`; (b) `torai-OB/productcatalogservice_loss/1` ≡ `re2ob_productcatalogservice_loss_1` | — | `runs/s0-cung-ca.json` | Script so mốc tiêm và **mọi** giá trị metric (cột chung, cùng mốc thời gian); in số ô lệch. Đạt khi 0 ô lệch và tập cột như nhau (sau khi bỏ cột `time`) |
| S1 | Tra số công bố **trước khi chạy** (SL28): Bảng 2, 3, 4 (dòng TORAI, RCD), 8 (thời gian), 9 (ablation) bài TORAI; Bảng 1 bài RCD; `docs/TORAI.md`; `docs/SETUP.md` | — | `moc-cong-bo.json`, `scripts/moc_torai.py` | So bằng máy dòng OB/SS với `results/T-006/scripts/moc.py`: 0 ô lệch. Đếm đủ 21 số mỗi dòng |
| S2 | Đọc code tĩnh: luồng dữ liệu `main.py` → `torai` → `_rcd_multimodal` → `run_multi_phase` → `run_psi_pc` → `local_skeleton_discovery` → `chisq`; ghi file:dòng; so RCD gốc với RCAEval (AST) | — | ghi chú trong `ho-so-torai.md` | Mỗi khẳng định có file:dòng; phần so AST lưu `runs/s2-so-ast.txt` |
| S3 | Harness `scripts/chay_torai.py`: dựng đầu vào đúng như `main.py:268-430` cho `torai`/`rcd`; tùy chọn biến thể (gốc/sửa), `--length`, seed theo ca, hoán vị cột, cửa sổ giả (placebo), thu giá trị trung gian qua wrapper chỉ quan sát; ghi tiến độ từng ca và thời gian (SL25) | S0 | `scripts/chay_torai.py` | (a) Tương đương `main.py`: chạy `main.py` nguyên văn qua `runpy`, chỉ chèn `np.random.seed(seed)` trước mỗi lời gọi `torai`; so với harness cùng seed trên 90 ca torai-OB, cửa sổ 10: 90/90 thứ hạng giống hệt. (b) Bật/tắt thu giá trị trung gian, cùng seed: 90/90 giống hệt (wrapper không tiêu số ngẫu nhiên). (c) Chạy lại cùng seed: giống hệt |
| S4 | Kiểm lỗi giảm mẫu trên code và trên ca: với mọi lời gọi `_rcd_multimodal`, ghi số dòng metric trước/sau lần giảm thứ hai, số dòng normal/anomal, số cột metric còn lại, số cột log, số dòng sau `concat` (dòng giả do lệch chỉ số), có rơi vào nhánh dự phòng (`torai.py:330-334`) không | S3 | `runs/s4-*.jsonl`, bảng tóm tắt trong `giam-mau-hai-lan.md` | Cửa sổ 10 và 20; 90 ca OB, 90 ca SS, ca TT. Đối chiếu số tính tay từ code (ví dụ `range(600)[::15][::15]`) |
| S5 | Bản sửa `src/torai/torai_sua.py`: (A) bỏ lần giảm mẫu thứ hai (`torai.py:29`); (B) ghép metric với logts theo vị trí trong từng nửa normal/anomal sau khi đặt lại chỉ số, cắt về độ dài chung. Không đổi gì khác | S2, S4 | `src/torai/`, `runs/s5-*.jsonl` | Harness ở chế độ thu giá trị trung gian: metric vào được RCD, số dòng = 2 × L·2 (20+20 với cửa sổ 10, 40+40 với cửa sổ 20), 0 dòng giả. `diff` giữa bản sửa và `torai.py` chỉ ở các dòng đã nêu (`runs/s5-diff.txt`) |
| S6 | Thử thời gian: 10 ca đầu torai-OB (theo thứ tự `sorted` của `main.py`), cửa sổ 10, seed 0, gốc và sửa | S3, S5 | `runs/s6-thu-thoi-gian.log` | Ước lượng tổng chi phí S7, S10 trước khi chạy; ghi vào LOG |
| S7 | Chạy chính trên laptop: TORAI gốc và sửa × cửa sổ 10, 20 × torai-OB, torai-SS × N seed (luật chọn N ở "Chi phí"); chấm bằng `Evaluator` của RCAEval như `main.py:540-600`; so với S1. Khối nào ước lượng > 1 giờ thì chạy trên EC2 | S1, S6 | `runs/s7-*.tar.gz`, `cham/s7-*.json`, bảng trong `giam-mau-hai-lan.md` | Mỗi khối: số ca = 90, 0 lỗi, 0 rỗng. Gốc cửa sổ 10: trung bình AVERAGE Avg@5 qua các seed lệch trung bình 3 lần T-006 (`results/T-006/cham/tong-hop.json`) ≤ 0,02. Tiêu chí "khớp số công bố" (mục Kiểm đúng đắn 1) chỉ áp cho bản gốc; bản sửa chỉ báo độ lệch |
| S8 | Kiểm không cần nhãn (mục "Kiểm đúng đắn"): chạy lại cùng seed; hoán vị cột; cửa sổ giả; đầu ra rỗng; trùng thứ tự cột; tỉ lệ nhánh dự phòng; soi giá trị trung gian | S3, S5 | `kiem-khong-nhan.md`, `runs/s8-*` | Xem mục "Kiểm đúng đắn" |
| S9 | Dựng `logts`, `tracets`: viết đặc tả; thử dựng trên `re2ob_productcatalogservice_loss_1` (đã chứng minh trùng ở S0); so với `torai-OB/productcatalogservice_loss/1`. Nếu dựng được: chạy TORAI gốc và sửa (seed 0, cửa sổ 10) trên bản dựng và bản Figshare của ca này, so thứ hạng | S0 | `dung-logts-tracets.md`, `scripts/dung_logts.py`, `runs/s9-*` | Luật ghép cột (ghi trước khi so): `tracets_*` ghép theo đúng tên cột `service_operation`; `logts` (tên `service_<số mẫu>`) ghép một-một trong từng service bằng phép gán tối ưu (Hungarian) cực đại số ô bằng nhau; cột không ghép được tính là sai. Tiêu chí "dựng lại được": ≥ 95 % ô trùng chính xác trên toàn bảng (kể cả cột không ghép được). Không đạt thì ghi tỉ lệ đạt được, giả thuyết đã thử và nguyên nhân. Vì phép gán chọn cách ghép có lợi nhất, tỉ lệ `logts` là cận trên; ghi rõ |
| S10 | Train Ticket: chứng minh trùng 30 ca dev trong zip (giải nén đúng 30 thư mục vào `D:\RCA-ext\work\T-016\data\torai-TT\`); chạy TORAI gốc, sửa trên các ca đã chứng minh; RCD (biến thể) cửa sổ 10 seed 0 trên ca `ts-route-service_socket/1`; thu giá trị trung gian như S4; đo thời gian. Điểm trên 30 ca dev chỉ là chẩn đoán, không phải benchmark P3 | S3, S5 | `quy-mo-tt.md`, `runs/s10-*` | Mỗi ca trước khi chạy có dòng "trùng" trong `runs/s10-cung-ca.json`; chạy không lỗi; ghi tỉ lệ nhánh dự phòng, số cột vào RCD, lỗi `assert` |
| S11 | EC2 (Linux): dựng Python 3.8 riêng trong `~/rca/T-016/envs/` cùng bộ gói như `py38-rcdlock`; chép torai-OB, torai-SS vào `~/rca/T-016/data/`; (i) TORAI gốc cửa sổ 10 seed 0 trên OB, SS; RCD torai-SS cửa sổ 10 seed 0 → so từng ca với cùng lượt trên laptop; (ii) RCD torai-OB cửa sổ 20, seed 0, theo thứ tự đã định, trần 3 giờ | S3 | `diem-mo-t006.md`, `runs/s11-*` | Trước khi chạy: `uptime`, `free -m`, `ps`; một tiến trình nặng mỗi lúc; `nohup`; log tiến độ; chép kết quả về sau mỗi khối |
| S11b | Lượt laptop đối ứng: RCD torai-SS cửa sổ 10 seed 0 | S3 | `runs/s11b-*` | 90 ca, 0 lỗi |
| S12 | Ví dụ tính tay: chọn ca theo luật dưới; script độc lập `scripts/tinh_tay.py` (không gọi hàm của TORAI, RCD, RCAEval, causal-learn, không gọi `KBinsDiscretizer`) tính lại mọi bước. Được dùng numpy, pandas, `scipy.stats.chi2.sf` (hàm phân phối). Riêng GMM: gọi `sklearn.mixture.GaussianMixture` (thư viện, không phải code tác giả) với đúng tham số của `torai.py:244-261`, rồi tự tính lại log-likelihood và BIC từ tham số đã khớp; so với giá trị trung gian thu từ lượt chính thức cùng seed | S3, S5 | `vi-du-tinh-tay.md`, `runs/s12-*` | Khớp tới từng điểm số: vectơ mức nghiêm trọng, BIC từng số cụm, nhãn cụm, điểm cụm, bins rời rạc hóa, từng p-value của phép kiểm với F-node, danh sách nút gốc của RCD, thứ hạng cuối. Sai số số thực ≤ 1e-9 tương đối; nhãn và thứ hạng phải giống hệt |
| S13 | Viết hồ sơ, `yeu-cau-dau-vao.csv`, `ngau-nhien.md`, `quy-mo-tt.md`, `diem-mo-t006.md` | S1–S12 | các file đầu ra | Mọi số có đường dẫn file kết quả; đối chiếu Tiêu chí xong |
| S14 | `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md`, `ca-da-chay.csv`; mục kết thúc phiên trong LOG; prompt phản biện; dòng STATE | S13 | — | Đọc lại STATE sau khi ghi: các dòng khác không đổi |

Việc làm ngay, song song: S1, S2, S9 không cần gì; S11 cần S3 (harness) rồi chạy nền trên EC2 trong lúc làm S7–S12 trên laptop.

### Luật chọn ca cho ví dụ tính tay (S12), ghi trước khi chạy

- Cấu hình chính: code chính thức RCAEval, torai-OB, cửa sổ 10 (lệnh của `docs/TORAI.md`), seed 0.
- Ca: ca đầu tiên theo thứ tự `sorted()` đường dẫn mà `main.py` dùng, thỏa: có ít nhất một cụm từ 2 service trở lên (để bước RCD thật sự chạy). Điều kiện này dựa trên cấu trúc trung gian, không dựa trên nhãn hay việc service gốc đứng hạng mấy.
- Ví dụ phụ: cùng ca, bản sửa, seed 0 (để thấy metric vào RCD).
- Nhãn (service gốc) chỉ mở sau khi đã có thứ hạng, để giải thích vì sao nó đứng ở hạng đó.

### Luật thứ tự ca cho RCD torai-OB cửa sổ 20 trên EC2 (S11 ii), ghi trước khi chạy

- Chạy trước 44 ca mà T-006 chưa chạy được (mọi ca không có trong `rcd-torai-ob-len20-lan1.tar.gz`), theo thứ tự `sorted()`; rồi tới 46 ca còn lại theo thứ tự `sorted()`.
- Dừng ở 3 giờ (Q-40). Không chọn ca theo kết quả.
- Báo cáo: (1) nếu xong 44 ca đầu: số 90 ca ghép (46 ca T-006 laptop, trung bình 3 lần + 44 ca EC2 một lần), ghi rõ là ghép hai máy; (2) nếu xong cả 90 ca trên EC2: số 90 ca thuần Linux một lần; (3) không xong 44: báo số ca đạt và hệ quả.

### Bản sửa (S5), ghi trước khi nhìn số

- Chỉ sửa hai chỗ: (A) bỏ `metric.iloc[::15, :]` ở `_rcd_multimodal` (`torai.py:29`), vì `torai()` đã giảm mẫu ở `:81` và truyền metric đã giảm vào cụm (`:295`); (B) trước `pd.concat(axis=1)` ở `:47-48`, đặt lại chỉ số của bốn bảng (metric normal/anomal, logts normal/anomal) và cắt mỗi nửa về số dòng chung nhỏ nhất. Lý do (B): metric giữ chỉ số dòng gốc (0, 15, 30, …), logts có chỉ số 0…39; `concat` theo chỉ số sẽ ghép sai dòng và thêm dòng giả điền 0.
- Không sửa: chuẩn hóa điểm, GMM, nhánh dự phòng, việc bỏ trace trong RCD, cách lấy tiền tố tên service. Những chỗ này ghi ở mục "chỗ code khác bài", không sửa, vì không chắc là lỗi.
- Một biến thể phụ chỉ (A) (không (B)) chạy trên torai-OB, cửa sổ 10, một seed, để tách tác động của từng chỗ sửa. Không dùng để chọn.

## Edge case (liệt kê trước khi làm)

| # | Edge case | Cách kiểm | Cách xử lý |
|---|---|---|---|
| E1 | Số bins rời rạc hóa: `bins=5` (`rcd.py:455`, `torai.py:22`), K-means 1 chiều (`rcd.py:278-289`). Cột có < 5 giá trị khác nhau, hoặc 40 dòng ít điểm | S12 đếm số bin thực của từng cột; S4 ghi số giá trị khác nhau | Ghi số bin thực; không sửa |
| E2 | Tham số k: RCAEval không có k; pha 2 cố xếp mọi nút (`rcd.py:165-167`) nhưng có thể trả ít hơn | S4/S12 đếm độ dài `rc` so với số cột | Ghi; chiều dài ngắn → nhánh dự phòng của TORAI |
| E3 | α: pha 1 bắt đầu 0,01, pha 2 bắt đầu 0,001, bước 0,1, tới < 1 (`rcd.py:23-25, 189, 302, 361`) | S12 ghi α lúc mỗi nút được nhận | Ghi đúng dãy α thực tế (số thực cộng dồn) |
| E4 | γ = 5: khối cuối nhỏ hơn 5, có thể 1 cột | S12 | Ghi |
| E5 | Cụm chỉ có một service: bỏ qua RCD (`torai.py:283-286`) | S4 đếm | Ghi tỉ lệ ca mà mọi cụm đều 1 service (RCD không đóng góp) |
| E6 | Service không có log, không có trace (torai-SS không có trace; vài service OB không có log) | S4: ghi cột theo nguồn của từng service | Điểm nguồn thiếu = 0 (`torai.py:236`), đúng bài §3.2; ghi |
| E7 | Tập ứng viên là service (tiền tố trước `_` của mọi cột metric, log, trace), không phải metric; có thể gồm thứ không phải service (`redis`, `frontend-external`, `traceservice`, `health`) và đổi tên `frontendservice`→`frontend` chỉ cho trace (`torai.py:225-226`). `str.startswith` có thể lấy nhầm cột của service khác có cùng tiền tố (`frontend` lấy cả `frontend-external_*`, `torai.py:295-310`) | S4: liệt kê tập ứng viên từng dataset; đếm va chạm tiền tố | Ghi; không sửa |
| E8 | RCD (biến thể) xếp **metric**, chấm ở mức service bằng `split("_")[0].replace("-db","")` và bỏ trùng (`main.py:560-572`); đầu ra chỉ 1–23 phần tử | Đếm độ dài, số service khác nhau trong đầu ra | Ghi; so ứng viên của hai bên |
| E9 | Đơn vị thời gian: metric 1 dòng/giây, `time` giây Unix; logts/tracets 15 s/dòng; `inject_time.txt` giây; log thô `timestamp` giây; trace thô `startTime` micro giây, `startTimeMillis` mili giây, `duration` (đơn vị cần xác định ở S9) | S0, S9 | Ghi đơn vị mỗi cột; S9 thử cả hai giả thuyết đơn vị nếu chưa rõ |
| E10 | Mốc tiêm không nằm trên lưới 15 s của logts: dòng logts chứa mốc tiêm bị tính là normal (`time < inject_time`) | S4 đo độ lệch pha (inject − đầu lưới) mod 15 | Ghi; không sửa |
| E11 | Ca lỗi trả thứ tự cột (MRP P3): `torai`, `rcd` **không** bọc `@rca` ở Python 3.8 (`__init__.py:81-83`); `main.py` `raise e` (`main.py:425-426`) nên lỗi làm dừng cả lượt. Trong `torai` có nhánh dự phòng riêng: khi RCD không xếp đủ service của cụm thì lấy thứ tự mức nghiêm trọng (`torai.py:330-334`) | Harness bắt lỗi từng ca, ghi file `*_failed.json`, không chấm như dự đoán; S4 đếm nhánh dự phòng; S8 kiểm trùng thứ tự cột | Ca lỗi tính là lỗi, không bỏ khỏi mẫu (MRP P3); báo tỉ lệ nhánh dự phòng theo cấu hình |
| E12 | `assert min_nodes < len(data)` (`rcd.py:168`): nhiều cột hơn số dòng ở pha 2 → lỗi | S4, S10 bắt lỗi `AssertionError` | Ghi là lỗi |
| E13 | Độ lệch chuẩn bằng 0 ở normal: `StandardScaler` dùng thang 1; `trace_err` nhân 1e9 khi trung bình và phương sai đều 0 (`torai.py:162-163`); tổng điểm bằng 0 → chia 0 ra NaN (`torai.py:132`, `149`, `166`, `181`) | S4/S12 đếm NaN, đếm lần nhân 1e9 | Ghi; soi ảnh hưởng tới GMM |
| E14 | GMM chọn số cụm bằng BIC trên N điểm 4 chiều, N nhỏ (OB khoảng 14); nhiều service cùng vectơ 0 | S12 tính lại BIC; S8 hoán vị dòng | Ghi độ nhạy theo thứ tự dòng |
| E15 | `logts` có thể thiếu dòng (lưới không đều) → `tail/head` theo dòng không còn là theo thời gian | S4 kiểm bước thời gian liên tiếp = 15 s | Ghi số ca lệch |
| E16 | Trùng tên cột sau `concat` metric + log (`torai.py:50, 53`) | S4 đếm | Ghi |
| E17 | Tất định: ngoài `np.random`, có nguồn nào khác (thứ tự `set`, băm) | S3(c), S8: cùng seed chạy hai lần, và với `PYTHONHASHSEED` khác nhau | Ghi |
| E18 | Train Ticket: `main.py:299-302` chỉ giữ cột metric bắt đầu bằng `ts-`; logts/tracets có thể có tên service khác dạng | S10 so tiền tố giữa ba nguồn | Ghi |
| E19 | Cửa sổ giả (placebo) cửa sổ 20 cần 1200 s trước mốc, file chỉ có 720 s | S8 | Chỉ làm placebo với cửa sổ 10; ghi kết luận nào yếu đi |

## Kiểm đúng đắn

1. **Số công bố tra trước khi chạy** (S1). Mốc: Bảng 2 (OB, dòng TORAI Metric+Log+Trace, RCD Metric), Bảng 3 (SS, TORAI Metric+Log, RCD Metric), Bảng 4 (TT, chỉ dùng để ghi; không so được vì 60/90 ca TT là test), Bảng 8 (thời gian), `docs/TORAI.md` (OB, Avg@5 từng lỗi). Tiêu chí so (giữ như T-006 cho TORAI và RCD, có ngẫu nhiên): trung bình các seed; ô AVERAGE Avg@5 lệch ≤ 0,05 là "khớp"; báo từng ô và khoảng giữa các seed. Không chỉnh tham số cho khớp.
2. **Chạy lại cùng kết quả**: cùng seed hai lần → thứ hạng giống hệt mọi ca (S3c, S8). Khác seed → đo phương sai (S7, `ngau-nhien.md`): độ lệch chuẩn của AVERAGE Avg@5 giữa các seed; số ca có thứ hạng khác nhau giữa các seed.
3. **Đầu ra không rỗng**: đếm ca rỗng, ca lỗi theo từng khối.
4. **Không trùng thứ tự cột, không rơi nhánh dự phòng**: (a) so thứ hạng với thứ tự xuất hiện của service trong dòng tiêu đề metric; (b) đếm số cụm ≥ 2 service rơi vào nhánh `torai.py:330-334`, và số ca mà thứ hạng cuối trùng hệt thứ hạng "chỉ mức nghiêm trọng" (`aa` của mọi cụm). Báo tỉ lệ theo cấu hình; nếu ≈ 100 % thì kết luận "RCD không đóng góp" cho cấu hình đó.
5. **Đổi thứ tự cột đầu vào**: hoán vị cột metric, logts, tracets bằng một hoán vị cố định (seed hoán vị 12345), cùng seed phương pháp. Ghi: (a) vectơ mức nghiêm trọng có đổi không (phải không đổi, chỉ đổi thứ tự dòng); (b) phân cụm có đổi không; (c) thứ hạng cuối đổi ở bao nhiêu ca; (d) AVERAGE Avg@5 so với khoảng giữa các seed. Thứ tự cột đổi chuỗi số ngẫu nhiên mà RCD dùng, nên (c) phải đọc cùng với phương sai theo seed.
6. **Cửa sổ giả**: với cửa sổ 10, lấy 600 s trước mốc tiêm, đặt "mốc giả" = mốc tiêm − 300 s; cả hai nửa đều bình thường. Chạy TORAI gốc và sửa, seed 0, 90 ca OB và 90 ca SS. Kỳ vọng: AC@1 của service gốc thật xấp xỉ mức may rủi (1/số ứng viên); điểm mức nghiêm trọng lớn nhất nhỏ hơn rõ so với ca thật. Nếu AC@1 giả ≫ may rủi: dừng, tìm đường rò (nhãn, biên file, thứ tự ứng viên). Cửa sổ 20 không làm được (E19): kết luận về rò ở cửa sổ 20 yếu đi, chỉ dựa trên phân tích tĩnh.
7. **Soi giá trị trung gian**: số cụm, kích thước cụm, số cột và số dòng vào RCD, số cột metric còn lại, số dòng giả, NaN, lần nhân 1e9, điểm lớn bất thường (> 1e6) (QT5).
8. **Tương đương harness với `main.py`** (S3a) và **wrapper không đổi hành vi** (S3b).
9. **Ví dụ tính tay khớp code chính thức tới từng điểm số** (S12).
10. **Linux và Windows** (S11 i): cùng seed, so từng ca. Giống hệt → hệ điều hành không phải nguyên nhân lệch; khác → báo số ca khác và độ lệch điểm.

Phép kiểm bị bỏ và hệ quả (SL26):
- Không so được số TT với Bảng 4: 60/90 ca TT là test, không được mở. Hệ quả: tính đúng của TORAI ở quy mô TT chỉ dựa trên phép kiểm không cần nhãn và điểm trên 30 ca dev (chẩn đoán, không phải benchmark).
- Không chạy placebo cửa sổ 20 (E19). Hệ quả: như trên.
- Không cài FineGrainer (code RCAEval không có): không tái lập Bảng 5–7 (xếp hạng mức chỉ báo). Hệ quả: hồ sơ chỉ mô tả FineGrainer theo bài, ghi "code không có".

## Tiêu chí xong

Mỗi dòng kiểm được. Mọi báo cáo phân biệt "chạy hết không lỗi" với "đúng" (khớp mốc, qua phép kiểm không cần nhãn) (SL24).

1. `ho-so-torai.md` có đủ 9 mục (7 của MRP P1 + 2 mục thêm), phần lõi RCD và đoạn biến thể RCD; mọi tham số mặc định có file:dòng; mọi số có đường dẫn file kết quả.
2. `giam-mau-hai-lan.md` có: bảng S4 cho cửa sổ 10 và 20 trên OB, SS, TT; kết luận lỗi/chủ ý kèm các nguyên nhân khả thi khác (Q-33); bảng số gốc và sửa (mọi seed, mọi cấu hình đã chạy) so với số công bố; đoạn xung đột; đề xuất cho P3 kèm trỏ tới nháp WHY trong `de-xuat-tai-lieu-chung.md`.
3. `src/torai/torai_sua.py` chạy được trên 90/90 ca OB và SS ở cửa sổ 10 và 20 (hoặc ghi rõ ca lỗi), S5 kiểm đạt.
4. `dung-logts-tracets.md` có đặc tả đủ để người khác dựng lại, kết quả S0(b) chứng minh trùng ca, và tỉ lệ khớp của từng chuỗi.
5. `ngau-nhien.md` có: mọi nguồn ngẫu nhiên kèm file:dòng; số seed đã chạy; độ lệch chuẩn và khoảng AVERAGE giữa các seed theo cấu hình; kết quả kiểm tất định (cùng seed, khác `PYTHONHASHSEED`).
6. `quy-mo-tt.md` có kết quả trên ca `ts-route-service_socket/1` và trên các ca dev TT đã chứng minh trùng (hoặc lý do không có), thời gian, giá trị trung gian.
7. `diem-mo-t006.md` trả lời điểm 3 và 5 với số liệu, hoặc ghi hệ quả nếu không làm được.
8. `vi-du-tinh-tay.md` khớp code chính thức theo S12 (mọi mục so sánh ghi "khớp" kèm sai số lớn nhất).
9. `kiem-khong-nhan.md` có kết quả mục 2–7, 10 của "Kiểm đúng đắn".
10. `yeu-cau-dau-vao.csv` đúng 16 cột theo thứ tự prompt; ô chưa kiểm ghi `chua_kiem: <lý do>`.
11. `ca-da-chay.csv`, `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md` có nội dung hoặc "không có".
12. LOG có mục kết thúc phiên đủ 6 ý, báo cáo A–H, prompt phản biện Codex; STATE dòng T-016 "chờ phản biện (ngày)".

## Không làm

- Không benchmark toàn dataset (P3): không chạy TORAI/RCD trên dataset mới, không chạy RE2-OB đầy đủ, không làm bảng so sánh phương pháp.
- Không phân tích hạn chế bằng số liệu (P4): giả thuyết về chỗ TORAI hỏng chỉ ghi dạng "chưa kiểm".
- Không thiết kế phương pháp đồ thị.
- Không sửa TORAI ngoài hai chỗ (A), (B). Không thêm trace vào RCD, không cài FineGrainer, không đổi nhánh dự phòng.
- Không sửa file của task cũ, không ghi file chung (đề xuất ở `de-xuat-tai-lieu-chung.md`).
- Không commit, không push. Không đọc repo RCA cũ.

## Chi phí ước lượng

Số dưới là ước lượng trước khi thử thời gian (S6); S6 xong thì ghi số thật vào LOG và chốt N theo luật.

| Việc | Máy | Ước lượng | Căn cứ |
|---|---|---|---|
| TORAI gốc, một lượt 90 ca OB cửa sổ 10 | laptop | 5–15 phút | T-006 torai-OB, T-005 TT 7 s/ca |
| TORAI sửa, một lượt | laptop | chưa biết; có thể gấp nhiều lần vì RCD nhận thêm cột metric | S6 sẽ đo |
| RCD torai-SS cửa sổ 10, một lượt | laptop / EC2 | 27–40 phút | T-006 `luong-khoi-rcd-torai-ss-*.out` |
| RCD torai-OB cửa sổ 20, 90 ca | EC2 | > 3 giờ có thể | T-006: 46 ca / 3 giờ |
| Dựng môi trường EC2 | EC2 | 15–30 phút, tải < 1 GB | T-007 |
| Chép torai-OB, torai-SS lên EC2 | — | khoảng 220 MB | `results/T-006/moi-truong.md` mục 4 |
| Giải nén 30 ca TT | laptop | khoảng 190 MB | ca T-005 6,4 MB |

**Ngân sách Q-40** (tổng mỗi phương pháp trên mỗi dataset ≤ 3 giờ chờ, chạy tuần tự). Ở đây TORAI gốc và TORAI sửa tính chung một ngân sách cho mỗi dataset (torai-OB, torai-SS, TT dev).

**Luật chọn số seed N** (chốt sau S6, trước khi nhìn điểm): N = 5 (như bài, §4.2) nếu tổng ước lượng của 4 cấu hình (gốc/sửa × cửa sổ 10/20) ≤ 2,5 giờ cho dataset đó; nếu không, N = 3; nếu vẫn vượt, bỏ theo thứ tự ưu tiên ngược: (4) gốc cửa sổ 20, (3) sửa cửa sổ 20. Luôn giữ (1) sửa cửa sổ 10 và (2) gốc cửa sổ 10. Dataset TT dev: N = 3 nếu vừa, không thì 1.

**Tổng ước lượng cả task** (SL27, trước S6): laptop tối đa 3 giờ × 3 dataset cho TORAI (trần, thực tế có thể ít hơn nhiều) + khoảng 40 phút RCD torai-SS + vài phút ví dụ tính tay và kiểm; EC2 khoảng 5 giờ (dựng 30 phút, TORAI và RCD-SS khoảng 1 giờ 30, RCD-OB cửa sổ 20 tới 3 giờ). Chạy EC2 song song với laptop. Số thật ghi vào LOG sau S6.

Không có việc nào cần báo trước theo luật cứng 8: không deep research, ≤ 2 subagent, tải < 1 GB, mỗi lượt ≤ 3 giờ (EC2) và lượt nào ước lượng > 1 giờ thì chạy trên EC2.

Thời gian trên laptop không là số chính thức (máy dùng chung với các phiên khác, SL30). Số thời gian chính thức lấy từ EC2 khi máy chỉ chạy một tiến trình của task này (kiểm `ps` trước và sau).

## Rủi ro và điều chưa chắc

- Bài TORAI không nêu chu kỳ 15 s (đã kiểm văn bản HTML); chu kỳ này chỉ có ở `docs/TORAI.md` và chú thích code. Kết luận "lỗi hay chủ ý" dựa trên code, tài liệu RCAEval và hành vi; không có lời tác giả. (chưa kiểm ý định tác giả; không hỏi được trong task)
- Bản sửa (B) ghép theo vị trí: là một cách hiểu ý định "ghép cột cùng thời điểm". Cách khác (ghép theo thời gian bằng `merge_asof` như `mmrcd.py`) cho lưới thời gian khác. (chưa kiểm cách nào đúng ý tác giả)
- Dựng `logts` cần Drain; cấu hình Drain tác giả dùng chưa biết. Có thể không dựng lại được chính xác.
- EC2 dùng chung với phiên khác; nếu máy bận thì chờ, không chạy song song tiến trình nặng.
- Laptop RAM trống khoảng 2 GB lúc mở phiên; lượt nặng có thể bị chậm hoặc thiếu RAM.

## Thay đổi trong lúc làm

1. **S0, tiêu chí "trùng ca" (04/10, 09:40).** SPEC ghi "0 ô lệch". Lượt đầu cho 98 986/540 375 ô (TT) và 24 163/103 752 ô (OB) lệch chính xác, nhưng sai số tương đối lớn nhất chỉ 6,5e-14: `simple_metrics.csv` của torai ghi số thực 16 chữ số có nghĩa, còn `metrics.parquet` giữ float64 đủ. Đổi tiêu chí thành: 0 ô lệch quá ngưỡng làm tròn (`np.isclose`, rtol 1e-12, atol 1e-15), cùng vị trí NaN, cùng tập cột, cùng mốc thời gian, cùng mốc tiêm; báo kèm số ô lệch chính xác và sai số tương đối lớn nhất. Lý do: ngưỡng này lớn hơn sai số làm tròn 16 chữ số khoảng 100 lần, nhưng nhỏ hơn mọi khác biệt đo đạc thật nhiều bậc.
2. **S7, thêm cấu hình Metric+Log trên OB (04/10, 11:05).** Thêm gốc và sửa, cửa sổ 10, 5 seed, không nạp tracets (`--khong-trace`), để so với dòng "Metric + Log / TORAI" của Bảng 2 (OB). Lý do: Bảng 2 có hai dòng TORAI (M+L và M+L+T); chỉ so một dòng thì không tách được ảnh hưởng của trace. Chi phí nhỏ (khoảng 10 % ngân sách OB). Ghi trước khi chạy.
3. **S9, chỉ số phụ cho `logts` (04/10, 11:30).** Sau khi thấy tỉ lệ ô trùng thấp (66,8 %) và tổng mỗi service trùng hệt, thêm hai chỉ số: số cặp cột cùng tổng (ghép bằng phép gán cực đại tương quan + ưu tiên cùng tổng) và tương quan trung bình. Chỉ số chính và tiêu chí 95 % giữ nguyên; chỉ số phụ chỉ để tách hai nguyên nhân (cách tách mẫu Drain và mốc thời gian). Thêm thử ngưỡng Drain 0,3–0,7 và chế độ C (một Drain trên "<service> <message>").
4. **S10, thêm RCD và đo thời gian TORAI trên 30 ca TT dev ở EC2 (04/10, 14:20).** SPEC chỉ chạy RCD trên 1 ca TT. Khi rà việc chưa làm trước khi báo xong, thấy chi phí nhỏ (EC2 khoảng 35 s/ca RCD, 2 s/ca TORAI), dữ liệu được phép (30 ca dev đã chứng minh trùng), nên làm ngay: RCD cửa sổ 10 seed 0; TORAI gốc, sửa cửa sổ 10 seed 0 (thời gian chính thức, và so Linux/Windows trên 30 ca). Trần 1 giờ. Ghi trước khi chạy.
