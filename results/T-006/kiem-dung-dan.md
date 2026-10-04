# T-006 — Kiểm đúng đắn bảy phương pháp trên laptop

Người làm: Claude. Phiên 1 và 2, ngày 03/10/2026. Máy: laptop Windows 11, i5-1240P, RAM 16 GB.
Phạm vi: BARO, N-Sigma, CIRCA-PC, RCD, TORAI, N-Sigma phát hiện, GDN. MicroRank, TraceRCA, BOCPD thuộc T-007.
Task này không trả lời câu hỏi nghiên cứu nào và không chọn dataset. Dữ liệu chỉ dùng để tái lập số đã công bố.

## 0. Cách đọc

**Ba loại mốc** (SPEC): **A** = có lệnh tái lập và đầu ra mong đợi của tác giả; **B** = chỉ có số trong bài, phải dựng lại cách chạy; **C** = không có mốc.

**Tiêu chí khớp** (chốt trong SPEC trước khi chạy, không đổi):
- Phương pháp tất định: mỗi ô lệch ≤ 0,02.
- RCD, TORAI (có ngẫu nhiên): trung bình 3 lần; ô AVERAGE lệch ≤ 0,05; báo từng ô và độ lệch giữa các lần.
- Loại B: ghi độ lệch và nêu các nguyên nhân khả thi (Q-33); không kết luận "sai" chỉ vì lệch.
- Không chỉnh tham số để cho khớp.

**Nguồn số.** Mọi số trong file này lấy từ file kết quả, ghi đường dẫn tương đối với `results/T-006/`:
- Điểm từng khối: chấm bằng `scripts/cham.py` (dùng `RCAEval.benchmark.evaluation.Evaluator`, gộp như `main.py`) từ file từng ca trong `runs/<khối>.tar.gz`. Bảng đầy đủ từng ô (AC@1, AC@3, Avg@5, mốc, độ lệch, các lần chạy): **`cham/bang-so-sanh.md`**, tự sinh từ `cham/tong-hop.json` bằng `scripts/tong_hop.py` và `scripts/bang_so_sanh.py`. Các bảng tóm tắt dưới đây chép từ file đó.
- Mốc: `scripts/moc.py`. Số mốc được so bằng máy với bảng HTML của hai bài (`scripts/kiem_moc/`): 0 ô lệch.
- Kiểm từng khối (trạng thái, số ca, `--test`, Traceback): `cham/kiem-khoi.txt`. Kết quả: 83 khối chính, 80 đạt. 3 khối không đạt là `rcd-torai-ob-len20-lan1..3`, bị dừng ở 3 giờ theo Q-40 với 46/90 ca mỗi khối (mục 6). Ngoài ra có 2 lượt hỏng giữ lại (`*-hong`) và 3 khối chạy thử (`thu-*`); không khối nào trong số này dùng làm bằng chứng.
- "AVERAGE" là trung bình trên mọi ca. Số ca mỗi loại lỗi bằng nhau ở mọi dataset dùng ở đây, nên bằng trung bình các ô.

## 1. Tóm tắt

| Mục | Mốc chính | Kết luận | Căn cứ chính |
|---|---|---|---|
| BARO | A: README BARO (ví dụ cơ bản; `reproduce_baro` OB; RQ4 OB); B: Bảng 3 bài BARO (OB, SS), Bảng 3 bài TORAI (SS) | **Khớp** mốc A; mốc B khớp với cửa sổ 10 (fse) và 20 (torai-SS), **lệch ở cấu hình SPEC/phiên 1** | mọi mốc A trùng hệt; mốc B ≤ 0,004 mỗi ô với cửa sổ 10 (fse), 20 (torai-SS); ở cấu hình SPEC/phiên 1 lệch fse-ss LOSS +0,028, torai-SS MEM +0,05 |
| N-Sigma (RCA) | B: Bảng 3 bài BARO, N-Sigma[t_inject] | **Khớp** với `--length 10`; lệch với `--length 20` (đã tìm ra nguyên nhân) | ≤ 0,004 mỗi ô với `--length 10`; DELAY lệch −0,26 với `--length 20` |
| CIRCA-PC | B: Bảng 2, 3 bài TORAI; Bảng 3 bài BARO | **Lệch ở mức ô** (loại B), chưa tìm ra đủ nguyên nhân | với cửa sổ 20 (cấu hình bổ sung; ứng viên cấu hình bài TORAI, chưa xác nhận), AVERAGE lệch −0,010 (OB), +0,018 (SS), nhưng có ô lệch tới ±0,08; trên fse AVERAGE lệch +0,064 / −0,028, có ô tới +0,148 |
| RCD | A: `docs/SETUP.md` (RE1-OB); B: Bảng 2, 3 bài TORAI | **Khớp mốc A** theo tiêu chí AVERAGE (mốc là 1 lần chạy, không có ô AVERAGE nên so với trung bình 5 ô; 3/5 ô mốc nằm ngoài khoảng 3 lần của tôi); mốc B: khớp ở SS, lệch ở OB (cấu hình SPEC); chưa tìm ra nguyên nhân | RE1-OB AVERAGE +0,009 (cửa sổ 10, ×3); torai-OB −0,063, torai-SS −0,037 (cửa sổ 10); torai-SS +0,094 (cửa sổ 20) |
| TORAI | A: `docs/TORAI.md` (OB); B: Bảng 2, 3 bài TORAI | **Khớp số công bố** (xem T-016: lõi nhân quả gần như không đóng góp ở cấu hình này) | AVERAGE Avg@5 lệch +0,003 (A), −0,017 (B, OB), +0,011 (B, SS) |
| N-Sigma phát hiện | B: Bảng 2 bài BARO | **OB: biến thể full khớp, biến thể w300 (chép đúng `reproduce_bocpd`) lệch nhỏ; SS lệch** (chưa tìm ra nguyên nhân) | OB full P −0,019, F1 −0,015; OB w300 P −0,025, F1 −0,020; SS P −0,039, F1 −0,035 |
| GDN | C: không có số mốc | **Không có mốc**; chạy ổn định | loss giảm, hai lần giống hệt, điểm hữu hạn |

## 2. Phát hiện chung, ảnh hưởng nhiều mục

### 2.1 Độ dài cửa sổ `--length` của `main.py` đã đổi theo thời gian

`main.py` của RCAEval cắt dữ liệu thành `L·30` dòng trước và `L·30` dòng sau mốc tiêm (dữ liệu 1 dòng/giây), với `L` = `--length`.
- Từ commit `a8425e0` (14/08/2024, khi script còn tên `rq2.py`) tới `977c1a8` (22/12/2024): mặc định `L = 10` (`args.length = 10`).
- Từ commit `61326e5` (27/12/2024): mặc định `L = 20`. Revision dùng ở đây (`259ea41`) mặc định 20.
- Nguồn: `git log -S` trên repo RCAEval, ghi trong LOG phiên 2.

Hệ quả, mỗi điều có bằng chứng riêng:
- **Bài BARO** (2024): cửa sổ 10 tái lập được các dòng RobustScorer[t_inject] và N-Sigma[t_inject]. Dòng CIRCA[t_inject] với cửa sổ 10 vẫn lệch, nên chưa biết bài dùng cấu hình nào cho CIRCA. Bằng chứng: `baro` và `nsigma` với `--length 10` khớp ≤ 0,004 mọi ô Bảng 3 bài BARO, còn với 20 thì `nsigma` lệch tới −0,26 (mục 3, 4).
- **Mốc RCD trong `docs/SETUP.md`** được ghi ở commit `a48f98e` (24/08/2024), tức cửa sổ 10. SPEC ghi chạy L3 "độ dài mặc định", nên lượt chạy theo SPEC dùng 20 (mục 6).
- **Bài TORAI** (2026): cửa sổ 20 tái lập được dòng BARO Bảng 3. BARO `--length 20` trên torai-SS trùng đến 2 chữ số mọi ô T1, T3, A5, còn `--length 10` thì không (mục 3). Đây là ứng viên cho cấu hình các baseline khác (CIRCA, RCD), **chưa xác nhận**: bài chỉ ghi dùng mã công khai với "default hyperparameter settings suggested in their respective papers" (§4.3). `docs/TORAI.md` chỉ ghi `--length 10` cho chính TORAI. SPEC đặt RCD trên torai là `--length 10`.
- **Ảnh hưởng tới T-007** (chưa kiểm ở đây): mốc MicroRank, TraceRCA của T-007 là dòng Trace Bảng 2 bài TORAI, nhiều khả năng cũng chạy với cửa sổ 20.

Minh duyệt (03/10/2026, LOG phiên 2) chạy thêm cấu hình cửa sổ của tác giả cho các mục liên quan. Các lượt theo SPEC được giữ nguyên và báo song song.

Độ dài cửa sổ giải thích được mức nào, theo từng mục:
- **BARO, N-Sigma:** giải thích toàn bộ phần lệch, mọi ô khớp ≤ 0,006 (mục 3, 4).
- **CIRCA trên torai:** giải thích phần lớn ở AVERAGE, nhưng không giải thích hết từng ô (mục 5).
- **CIRCA trên fse:** không giải thích được (mục 5).
- **RCD:** chưa phân xử được. Ở torai-SS (đủ 90 ca), cả cửa sổ 10 lẫn 20 đều không tái lập được số của bài, nhưng ảnh hưởng của cửa sổ nói chung chưa loại được. Ở torai-OB, cửa sổ 20 đủ 90 ca (T-016) cho 0,742 so với 0,74 của bài; nhưng torai-SS không khớp ở cả hai cửa sổ, nên vẫn chưa phân xử được cửa sổ của bài cho RCD.

Đây là lựa chọn có ảnh hưởng lớn: đổi cửa sổ làm một ô N-Sigma đổi 0,26, và làm AVERAGE của RCD đổi 0,13.

### 2.2 RE1-OB không phải dữ liệu của bài BARO

`main.py --dataset re1-ob`/`online-boutique` đọc dữ liệu Zenodo 13305663. Dữ liệu này giống hệt RE1-OB của Zenodo 14590730 (401/401 file trùng CRC-32 và kích thước; `runs/02-so-zip-13305663-re1.log`).

So RE1 với `fse-*` của bài BARO (`runs/05b-…`, `05c-…`, `05d-…`):
- **OB:** 80 ca trùng tên. Trong đó delay và loss (40 ca) giống từng byte. Còn cpu và mem (40 ca) là lượt ghi khác: mốc tiêm khác, RE1 có 4 201 dòng, fse có 721 dòng.
- **SS:** RE1-SS gồm đúng 100 ca của fse-ss, cộng 25 ca lỗi disk.

Vì vậy các dòng `[t_inject]` của bài BARO được so trên `fse-*`, bằng script dựng lại `process()` của `main.py` (`scripts/chay_fse.py`; loại B).
- Script này được kiểm bằng `main.py` thật. Ở 40 ca có dữ liệu giống từng byte, thứ hạng trùng hệt 40/40 cho cả `baro` và `nsigma` (`cham/kiem-chay-fse-vs-main.txt`).
- Đầu vào là `simple_data.csv`; lý do ở LOG bước 0.4.

### 2.3 Biên cửa sổ file cắt đối xứng quanh mốc tiêm (REVIEW T-002, điểm R1)

R1 của T-002 chỉ ra rằng file telemetry RCAEval được cắt đối xứng quanh mốc tiêm. Đo trên `fse-*` (`runs/27-bien-cua-so-fse.log`):
- 199/200 ca cắt đúng [−360 s, +360 s] quanh mốc tiêm: 360 dòng trước, 361 dòng từ mốc.
- 1 ca (`fse-ss/user_mem/1`) dừng ở +246 s và có 114 dòng `time` rỗng.

Phạm vi ảnh hưởng tới phép kiểm bộ phát hiện trong task này:
- **N-Sigma phát hiện:**
  - Biến thể "w300" cắt 300 + 300 dòng quanh mốc tiêm, tức dùng mốc tiêm trực tiếp, đúng như `reproduce_bocpd` của tác giả.
  - Biến thể "full" nhận nguyên file. Mốc tiêm nằm đúng giữa file, nên vị trí lỗi lộ qua biên file.
  - Cả hai chỉ dùng được để **tái lập số công bố**. Không dùng làm số đo khả năng tự phát hiện (luật cứng 6).
  - Thêm nữa, luật chấm của tác giả tính TP cho mọi ca có ít nhất một cảnh báo, nên R luôn bằng 1. P chỉ phụ thuộc số ca có cảnh báo đầu tiên trước mốc tiêm (mục 8).
- **GDN:** chỉ chạy trên dữ liệu MSL mẫu của repo GDN, không phải dữ liệu RCAEval. Train và test tách sẵn theo repo, không dùng mốc tiêm. R1 không áp dụng cho phép kiểm GDN ở đây. R1 sẽ áp dụng khi GDN chạy trên RCAEval (ví dụ học trên đoạn trước mốc tiêm như T-005).
- **Các phương pháp RCA "biết mốc tiêm"** (BARO, N-Sigma, CIRCA, RCD, TORAI qua `main.py`): mốc tiêm là đầu vào hợp lệ của chế độ này. R1 không thêm rò.

### 2.4 Không có đường nhãn vào phương pháp

- **Kiểm tĩnh (LOG bước 0.2):** `baro`, `nsigma`, `circa`, `rcd`, `torai` không đọc `sli`, cũng không đọc đường dẫn ca. `main.py` có truyền `sli` suy từ tên service gốc, nhưng không hàm nào trong năm hàm này đọc nó.
- `scripts/chay_fse.py` truyền `sli=None`.
- Nhãn (service gốc, loại lỗi lấy từ tên file kết quả) chỉ dùng để chấm.

### 2.5 Bộ thư viện

Mọi khối Python 3.12 sau X1 chạy bằng `py312-pin` (`x1-chot-moi-truong.md`). X1 xác nhận hai điều: (a) cả hai bộ khớp mọi mốc A; (b) CIRCA (mốc B) lệch quá 0,02 ở nhiều ô, giống nhau ở cả hai bộ. Luật X1 trong SPEC không tách mốc A với mốc B. Minh quyết ngày 04/10/2026: giữ `py312-pin`. Quyết định được làm rõ sau khi đã thấy kết quả, nhưng kết quả không phụ thuộc cách hiểu vì hai bộ giống nhau (WHY-15; mục 11.7). RCD, TORAI chạy bằng `py38-rcd`; L3 chạy bằng `py38-rcdlock` (`moi-truong.md`).

## 3. BARO

**Kết luận: khớp.** Thuật toán BARO (BOCPD đa biến + RobustScorer, code repo BARO) và hàm `baro` của RCAEval (RobustScorer khi biết mốc tiêm) đều tái lập được số công bố.

Mốc A, lệnh của tác giả, bằng `py312-pin` (`cham/baro-lenh-tac-gia.txt`):

| Phép kiểm | Mốc | Của mình | Lệch |
|---|---|---|---|
| Ví dụ cơ bản README | bước 243; top 5 `checkoutservice_latency, cartservice_mem, cartservice_latency, cartservice_cpu, main_mem` | bước 243; top 5 trùng đúng thứ tự | 0 |
| `reproduce_baro` OB (CPU / MEM / DELAY / LOSS / ALL) | 0,91 / 0,96 / 0,95 / 0,62 / 0,86 (README; Bảng 3) | 0,91 / 0,96 / 0,95 / 0,62 / 0,86 | 0 |
| RQ4 OB, 40 giá trị theo `t_bias` | danh sách trong README | trùng 40/40 (`cham/them-reproduce-rq4-fse-ob.txt`) | 0 |
| `reproduce_baro` SS (thêm, mốc B Bảng 3 dòng BARO) | 0,97 / 0,98 / 0,98 / 0,87 / 0,95 | 0,97 / 0,98 / 0,98 / 0,87 / 0,95 | 0 |
| RQ4 SS ở `t_bias = 0` (thêm, mốc B RobustScorer[t_inject] AVG) | 0,95 | 0,95 | 0 |

Hai dòng "thêm" ngoài danh sách khối của SPEC, chạy theo Q-41 (lệnh tác giả có sẵn, vài phút). `py312` (bản mới nhất) cũng khớp ví dụ cơ bản và `reproduce_baro` OB (X1).

Mốc B, hàm `baro` của RCAEval (cột lệch = của mình − mốc; nguồn `cham/bang-so-sanh.md`):

| Dữ liệu, cửa sổ | Mốc | Avg@5 mỗi ô của mình (lệch) | AVERAGE (lệch) |
|---|---|---|---|
| fse-ob, `--length 10` | Bảng 3 bài BARO, RobustScorer[t_inject] 0,9/0,94/0,94/0,65 | 0,896 (−0,004) / 0,944 (+0,004) / 0,936 (−0,004) / 0,648 (−0,002) | 0,856 (−0,004) |
| fse-ss, `--length 10` | 0,98/0,98/0,98/0,86 | 0,984 (+0,004) / 0,976 (−0,004) / 0,984 (+0,004) / 0,864 (+0,004) | 0,952 (+0,002) |
| fse-ob, `--length 20` | như trên | 0,904 (+0,004) / 0,936 (−0,004) / 0,920 (−0,020) / 0,648 (−0,002) | 0,852 (−0,008) |
| fse-ss, `--length 20` | như trên | 0,984 (+0,004) / 0,984 (+0,004) / 0,984 (+0,004) / 0,888 (**+0,028**) | 0,960 (+0,010) |
| torai-SS, `--length 20` | Bảng 3 bài TORAI, dòng Metric, A5 0,80/0,83/0,77/0,71/0,68/0,80 | 0,800 / 0,827 / 0,773 / 0,707 / 0,680 / 0,800 (mọi ô ≤ 0,003; T1, T3 cũng trùng đến 2 chữ số) | 0,764 (+0,004) |
| torai-SS, `--length 10` | như trên | 0,800 / 0,880 (**+0,05**) / 0,800 (**+0,03**) / 0,733 (**+0,023**) / 0,680 / 0,787 | 0,780 (+0,020) |
| torai-OB, `--length 10` và `20` | không có mốc (dòng BARO Bảng 2 bài TORAI trùng từng số với Bảng 4, nghi chép nhầm; SPEC) | AVERAGE 0,731 (10), 0,742 (20) | — |

Thứ tự cột: fse là CPU / MEM / DELAY / LOSS; torai là CPU / MEM / DISK / SOCKET / DELAY / LOSS.

Lệch ở cấu hình theo SPEC/phiên 1 (fse `--length 20`, torai-SS `--length 10`) được giải thích bằng độ dài cửa sổ (mục 2.1): đổi về cửa sổ của tác giả thì mọi ô khớp.

Kiểm không cần nhãn: mọi khối có 0 thứ hạng rỗng, 0 dự phòng (`baro` không có wrapper `@rca`). Chạy lại cùng đầu vào cho thứ hạng giống hệt ở 90/90 ca (torai) và 100/100 ca (fse).

**Giá trị trung gian (QT5), torai-OB.** `redis_diskio` đứng đầu thứ hạng ở 78/90 ca. Cơ chế (`scripts/soi_baro_redis.py`, `runs/20-soi-baro-redis-diskio.log`):
- Trong đoạn trước mốc tiêm, kênh này có IQR = 0. sklearn `RobustScaler` khi đó đặt scale = 1.
- Vì vậy điểm của kênh là độ lệch thô theo byte (18 503–50 264), trong khi kênh thứ hai có trung vị 2 280.
- Hệ quả: AC@1 của BARO trên torai-OB chỉ 0,133. Đây là hành vi của code tác giả trên dữ liệu này, không phải lỗi chạy.

## 4. N-Sigma (RCA khi biết mốc tiêm)

**Kết luận: khớp với cấu hình cửa sổ của tác giả (`--length 10`); lệch với `--length 20`, nguyên nhân đã tìm ra.**

Hàm `nsigma` của RCAEval (`RCAEval/e2e/__init__.py:109`), mốc B: Bảng 3 bài BARO, N-Sigma[t_inject] (`cham/bang-so-sanh.md`):

| Dữ liệu, cửa sổ | Mốc CPU/MEM/DELAY/LOSS, AVG | Của mình (lệch) | AVERAGE (lệch) |
|---|---|---|---|
| fse-ob, `--length 10` | 0,9 / 0,93 / 0,94 / 0,66; 0,86 | 0,896 (−0,004) / 0,928 (−0,002) / 0,936 (−0,004) / 0,656 (−0,004) | 0,854 (−0,006) |
| fse-ss, `--length 10` | 0,98 / 0,98 / 0,98 / 0,9; 0,96 | 0,984 (+0,004) / 0,984 (+0,004) / 0,984 (+0,004) / 0,896 (−0,004) | 0,962 (+0,002) |
| fse-ob, `--length 20` | như trên | 0,920 (+0,020) / 0,904 (−0,026) / **0,680 (−0,260)** / 0,640 (−0,020) | 0,786 (−0,074) |
| fse-ss, `--length 20` | như trên | 0,984 (+0,004) / 0,960 (−0,020) / **0,816 (−0,164)** / 0,832 (−0,068) | 0,898 (−0,062) |

Tìm nguyên nhân lệch ở DELAY (Minh yêu cầu tìm trước khi kết luận). Mọi biến thể dưới đây chỉ để chẩn đoán, không thay kết quả chính thức:
1. **Cơ chế** (`scripts/soi_nsigma_delay.py`, `runs/22-soi-nsigma-delay.log`). Biến thể "goc" tái tạo đúng số chính thức. Ở các ca delay hỏng, kênh latency của service gốc chỉ có z 10–18, vì đoạn trước mốc tiêm có gai làm độ lệch chuẩn phình. Trong khi đó kênh gần hằng số của service khác có z hàng trăm; ví dụ `recommendationservice_mem` có độ lệch chuẩn ~1e-3.
2. **Code đổi sau bài?** Không. `nsigma` bản đầu của repo BARO (`9d84cbf`, 16/04/2024) giống hệt bản `e35f4ec` và bản RCAEval.
3. **`dk_select_useful=True`?** Không: mọi ô tụt còn 0,16–0,62 (`runs/23-…`).
4. **N-Sigma kiểu CIRCA gốc** (max \|z\|, cửa sổ ngắn theo mặc định `CaseData`): SS khớp ≤ 0,012, nhưng OB lệch 0,06 ở CPU, LOSS (`runs/24-…`). Giải thích được một phần.
5. **Độ dài cửa sổ.** Cửa sổ 10 (300 + 300 dòng, mặc định của RCAEval tới 27/12/2024) bỏ 60 dòng đầu của đoạn bình thường. Với cửa sổ này, mọi ô khớp ≤ 0,006 ở cả OB và SS (khối chính thức `l4-nsigma-fse-*-len10-*`, Minh duyệt). **Đây là nguyên nhân.**

Ghi chú trung thực: tôi tìm ra (5) sau khi đã thấy kết quả. Căn cứ chọn cửa sổ 10 là lịch sử code (mục 2.1) và việc nó giải thích đồng thời cả BARO và N-Sigma ở hai dataset, không phải dò tham số.

Kiểm không cần nhãn: 0 rỗng, 0 dự phòng (`nsigma` không có wrapper). Chạy lại giống hệt 100/100 ca.

## 5. CIRCA-PC

**Kết luận: lệch ở mức ô (loại B); chưa tìm ra đủ nguyên nhân.**
- Với cửa sổ 20 (cấu hình bổ sung Minh duyệt; ứng viên cấu hình của bài TORAI, chưa xác nhận), AVERAGE khớp sát: OB −0,010, với AC@1 và AC@3 lệch ≤ 0,003; SS +0,018.
- Nhưng từng ô vẫn lệch tới ±0,08, vượt tiêu chí ≤ 0,02 cho phương pháp tất định.
- Trên fse lệch rõ hơn, và độ dài cửa sổ không giải thích được.
- Đây là mốc loại B, nên không kết luận code chạy sai. Hàm `circa` của RCAEval tính lại được: `cham.py` khớp `main.py` mọi ô, và hai bộ thư viện cho cùng điểm.

Hàm `circa` của RCAEval (PC của causal-learn + RHT), `py312-pin`; nguồn `cham/bang-so-sanh.md`:

| Dữ liệu, cửa sổ | Mốc | AVERAGE Avg@5 mình (lệch) | Ô lệch lớn nhất |
|---|---|---|---|
| torai-OB, `--length 20` (cấu hình bổ sung Minh duyệt) | Bảng 2 bài TORAI, Metric: A5 AVG 0,85; T1 0,67; T3 0,89 | 0,840 (−0,010); AC@1 0,667 (−0,003); AC@3 0,889 (−0,001) | CPU 0,800 so với 0,88 (−0,080); MEM 0,960 so với 0,89 (+0,070) |
| torai-SS, `--length 20` (cấu hình bổ sung Minh duyệt) | Bảng 3 bài TORAI, Metric: A5 AVG 0,90; T1 0,74; T3 0,92 | 0,918 (+0,018); AC@1 0,778 (+0,038); AC@3 0,944 (+0,024) | LOSS 0,880 so với 0,81 (+0,070) |
| torai-OB, `--length 10` (phiên 1), 2 lần | như trên | 0,887 (+0,037) | DISK 1,000 so với 0,85 (+0,150) |
| torai-OB, `--length 10`, bộ `py312` | như trên | 0,887 (+0,037), giống hệt `py312-pin` mọi ô | như trên |
| torai-SS, `--length 10` (phiên 1) | như trên | 0,929 (+0,029) | LOSS 0,920 so với 0,81 (+0,110) |
| fse-ob, `--length 10` (cấu hình bổ sung Minh duyệt) | Bảng 3 bài BARO, CIRCA[t_inject]: AVG 0,77 | 0,834 (+0,064) | MEM 0,888 so với 0,74 (+0,148) |
| fse-ss, `--length 10` (cấu hình bổ sung Minh duyệt) | Bảng 3 bài BARO, CIRCA[t_inject]: AVG 0,95 | 0,922 (−0,028) | CPU 0,928 so với 0,97 (−0,042) |
| fse-ob, `--length 20` (phiên 1) | như trên | 0,826 (+0,056) | MEM 0,856 so với 0,74 (+0,116) |
| fse-ss, `--length 20` (phiên 1) | như trên | 0,898 (−0,052) | MEM 0,888 so với 0,98 (−0,092) |

Nguyên nhân khả thi của lệch (Q-33):
- **Kiểm rồi, loại:**
  - Bản thư viện: `py312` (causal-learn 0.1.4.8, pandas 3) và `py312-pin` (0.1.3.8, pandas 2.2.3) cho cùng điểm mọi ô (X1).
  - Revision code: `circa()` trong `circa.py`, cùng `rht.py`, `pc.py`, giống hệt giữa nhánh `fse26` (bài TORAI) và `main`.
  - Thứ tự nút do hash: không đổi top 5 (dưới).
- **Kiểm rồi, giải thích một phần:**
  - Độ dài cửa sổ: trên torai, AVERAGE từ +0,037 / +0,029 về −0,010 / +0,018. Trên fse không giải thích.
  - Ca dự phòng: ở torai-OB `--length 20`, bỏ 4 ca dự phòng thì DISK đổi +0,133. Nếu bản thư viện của tác giả dựng được đồ thị ở các ca này thay vì báo lỗi, các ô đó sẽ khác.
- **Chưa kiểm được:**
  - Bản causal-learn tác giả dùng: bài không ghi.
  - Bài BARO (04/2024) ra trước RCAEval (08/2024) và ghi rằng mã CIRCA công khai. Có thể bài dùng repo CIRCA gốc (PC qua gói R `pcalg`, có lưới alpha, xem LOG T-005). Kiểm việc này cần cài R và dựng CIRCA gốc; ngoài phạm vi SPEC, chi phí chưa ước lượng.
  - Bài TORAI viết "CIRCA relies on a provided call graph", trong khi code RCAEval chỉ dùng PC.
  - Windows thay vì Linux.

**Các ca rơi vào nhánh dự phòng** của wrapper `@rca` (trả thứ tự cột). Nguồn `cham/circa-du-phong.txt`, `scripts/ca_du_phong_circa.py`; hai cách phát hiện (dòng "failed (" trong stderr, và thứ hạng trùng thứ tự cột) khớp nhau ở mọi khối:

| Khối | Ca | Lỗi | Ảnh hưởng (bỏ ca − giữ ca), Avg@5 |
|---|---|---|---|
| torai-OB (cả 3 khối: X1 hai bộ, `l4-…-lan2`) | `checkoutservice_cpu_2` | `ValueError: Data correlation matrix is singular. Cannot run fisherz test.` | CPU +0,018; AVERAGE +0,003; ô khác 0 |
| torai-SS `l4-circa-torai-ss-lan1` | `carts_delay_2`, `carts_disk_3` | như trên | DELAY −0,011; DISK −0,007; AVERAGE −0,002 |
| fse-ob `l4-circa-fse-ob-lan1` | không có | — | — |
| fse-ss `l4-circa-fse-ss-lan1` | `payment_mem_3` | như trên | MEM +0,029; AVERAGE +0,007 |
| torai-OB `l4-circa-torai-ob-len20-lan1` | `checkoutservice_cpu_2`, `productcatalogservice_delay_1`, `productcatalogservice_disk_3`, `recommendationservice_disk_1` | như trên | CPU +0,014; DELAY +0,050; DISK +0,133; AVERAGE +0,032 |
| torai-SS `l4-circa-torai-ss-len20-lan1` | `orders_delay_1` | như trên | DELAY +0,030; AVERAGE +0,006 |
| fse-ob, fse-ss `--length 10` | không có | — | — |

Bảng đầy đủ AC@1, AC@3, Avg@5 theo cả hai cách: `cham/circa-du-phong.txt`.
- Hai ca torai-SS là ca của `carts`. Thứ hạng dự phòng (thứ tự cột) lại đặt `carts` đứng đầu, nên khi giữ ca thì hai ca này được tính đúng do tình cờ.
- Nguyên nhân suy biến nằm trong dữ liệu (`runs/21-soi-circa-ma-tran-suy-bien.log`): ma trận thiếu hạng (51/53, 52/53, 47/48 cột), có cặp cột giống hệt (`payment_workload` = `shipping_workload`; `front-end_error` = `orders_error`). Ca đối chứng đủ hạng.
- Lỗi xảy ra ở cả causal-learn 0.1.3.8 và 0.1.4.8.

**Tất định.** Chạy lại cùng bộ, cùng đầu vào: thứ hạng giống hệt 75/90 ca, mọi ô điểm giống nhau. Nguyên nhân (`scripts/soi_circa_hashseed.py`, `runs/25-soi-circa-hashseed.log`):
- Thứ tự các nút bằng điểm phụ thuộc hash chuỗi của Python (`rht.py` dùng `list(set(...))`).
- Cố định `PYTHONHASHSEED` thì hai lần giống hệt.
- Đổi seed thì thứ hạng chỉ khác từ vị trí 21–47, top 5 giữ nguyên ở 6 seed, nên Avg@5 không đổi.

## 6. RCD

**Kết luận: khớp mốc A (RE1-OB, `docs/SETUP.md`). Mốc B trên torai: khớp ở SS, lệch ở OB theo cấu hình SPEC (`--length 10`); chưa tìm ra nguyên nhân.**

Lệnh `main.py --method rcd`; nguồn `cham/bang-so-sanh.md`, `cham/rcd-torai-ob-len20-46ca.txt`. Tiêu chí của RCD là AVERAGE trung bình 3 lần lệch ≤ 0,05.

| Dữ liệu, cửa sổ, số lần, môi trường | Mốc | AVERAGE Avg@5 mình (lệch); các lần | Ô lệch lớn nhất (trung bình các lần); khoảng giữa các lần |
|---|---|---|---|
| RE1-OB, `--length 10` (cửa sổ lúc tác giả ghi mốc), ×3, `py38-rcdlock` | A: `docs/SETUP.md` (1 lần), trung bình 5 ô 0,61 | 0,619 (+0,009); 0,616 / 0,626 / 0,614 | DISK 0,757 so với 0,68 (+0,077); CPU 0,869 so với 0,94 (−0,071; các lần 0,808–0,920); LOSS các lần 0,400–0,600 |
| RE1-OB, `--length 20` (mặc định hiện tại; SPEC), ×1, `py38-rcdlock` | như trên | 0,634 (+0,024) | MEM 0,824 so với 0,67 (+0,154) |
| torai-OB, `--length 10` (SPEC), ×3, `py38-rcd` | B: Bảng 2 bài TORAI, Metric, A5 AVG 0,74 | 0,677 (**−0,063**); 0,658 / 0,702 / 0,671 | MEM 0,578 so với 0,81 (−0,232; các lần 0,547–0,600); DISK các lần 0,640–0,840 |
| torai-OB, `--length 20` (cấu hình bổ sung Minh duyệt), ×3 | như trên | **không so được với bài**: mỗi lần bị dừng ở 3 giờ (Q-40) với 46/90 ca. T-016 chạy đủ 90 ca trên EC2 (1 lần, seed 0): 0,742 (+0,002); 46 ca chung 0,865 so với 0,857 (TB 3 lần ở đây) (`results/T-016/diem-mo-t006.md`) | chỉ so ghép cặp trên 46 ca chung (checkoutservice 18, currencyservice 18, emailservice 10; theo lỗi CPU 9, DELAY 9, DISK 9, LOSS 7, MEM 6, SOCKET 6): AVERAGE 0,857 so với 0,758 của `--length 10` cùng ca (+0,099) |
| torai-SS, `--length 10` (SPEC), ×3 | B: Bảng 3 bài TORAI, Metric, A5 AVG 0,57 | 0,533 (−0,037); 0,540 / 0,518 / 0,542 | DELAY 0,462 so với 0,64 (−0,178); DISK −0,166 |
| torai-SS, `--length 20` (cấu hình bổ sung Minh duyệt), ×3 | như trên | 0,664 (**+0,094**); 0,649 / 0,656 / 0,687 | MEM 0,618 so với 0,36 (+0,258); CPU +0,236 |

Đọc kết quả:
- **Mốc A.** Với cấu hình của tác giả, AVERAGE lệch +0,009, đạt tiêu chí. Từng ô của tác giả là 1 lần chạy. Ở 3/5 ô (CPU, MEM, DISK), mốc nằm ngoài khoảng 3 lần của tôi, nhưng sát biên: lệch so với biên gần nhất 0,020, 0,010, 0,032.
- **Mốc B.** torai-SS (đủ 90 ca): 0,533 (cửa sổ 10) < 0,57 < 0,664 (cửa sổ 20). Riêng từng cấu hình không tái lập được số của bài, nhưng ảnh hưởng của cửa sổ nói chung chưa loại được. torai-OB: cửa sổ 20 chỉ có 46/90 ca; tập này không chứng minh là đại diện (46 ca có trung bình 0,857 thì trung bình đủ 90 ca có thể nằm trong khoảng 0,438–0,927), nên không suy ra số 90 ca và chưa phân xử được vai trò của cửa sổ.

RCD không có wrapper `@rca`, và stderr không có dòng "failed (". Phép kiểm "trùng thứ tự cột" gắn cờ 3 ca, nhưng đây là báo động giả: thứ hạng RCD chỉ dài 1–23 phần tử, và 3 ca này chỉ có 3–4 phần tử, tình cờ theo thứ tự cột. RCD có ngẫu nhiên (`np.random` không đặt seed): giữa các lần, chỉ 2–6/90 ca có thứ hạng giống hệt.

Nguyên nhân khả thi của lệch trên torai (Q-33):
- **Kiểm rồi, chưa phân xử được:**
  - Độ dài cửa sổ: ở SS, riêng cửa sổ 10 hay 20 đều không tái lập được; ở OB, cửa sổ 20 chưa đủ ca (trên).
- **Kiểm rồi, loại:**
  - Revision code: `rcd.py`, các file vá `lib/` và `requirements_torai.lock` giống hệt giữa nhánh `fse26` của bài TORAI và `main`.
- **Chưa kiểm được:**
  - Môi trường: `py38-rcd` và `py38-rcdlock` cùng bản causal-learn, numpy, pandas, scikit-learn, scipy, và cùng 2 file vá RCD dùng (`moi-truong.md`). Chưa chạy cùng khối bằng hai môi trường; chi phí ~1 giờ mỗi khối.
  - Ngẫu nhiên: bài TORAI lấy trung bình 5 lần ("we repeat each experiment five times and report the average results", §4.2); seed chưa xác định. Ba lượt của task cho khoảng giữa các lần tới 0,20 ở một ô và 0,044 ở AVERAGE (torai-OB cửa sổ 10). Con số đó chỉ mô tả biến thiên quan sát được, không phải giới hạn của phân phối, nên chưa phân xử được phần lệch do ngẫu nhiên.
  - Một cấu hình khác của tác giả mà bài không ghi.
  - Windows thay vì Linux: đã loại cho TORAI và RCD ở T-016 (cùng seed, thứ hạng giống hệt; `results/T-016/diem-mo-t006.md`).

## 7. TORAI

**Kết luận: khớp.** Lệnh `main.py --method torai --dataset torai-ob|torai-ss --length 10` (đúng `docs/TORAI.md`), `py38-rcd`, ×3 mỗi dataset (`cham/bang-so-sanh.md`):

| Dữ liệu | Mốc | AVERAGE Avg@5 mình (lệch) | Ô lệch lớn nhất |
|---|---|---|---|
| torai-OB | A: `docs/TORAI.md` (6 ô Avg@5; trung bình 0,910) | 0,913 (+0,003) | LOSS 0,867 so với 0,84 (+0,027); SOCKET −0,010; các ô khác 0 đến +0,003 |
| torai-OB | B: Bảng 2 bài TORAI, Metric+Log+Trace (AVG A5 0,93, T1 0,83, T3 0,95) | 0,913 (−0,017); AC@1 0,778 (−0,052); AC@3 0,944 (−0,006) | LOSS A5 −0,093; AC@1 LOSS −0,137 |
| torai-SS | B: Bảng 3 bài TORAI, Metric+Log (AVG A5 0,94, T1 0,84, T3 0,96) | 0,951 (+0,011); AC@1 0,848 (+0,008); AC@3 0,978 (+0,018) | LOSS AC@1 +0,133; DELAY AC@1 −0,128 |

- Mốc B của torai-OB là dòng Metric+Log+Trace, vì `main.py` nạp cả log và trace cho `torai` trên torai-OB (`main.py:367-401`). torai-SS không có trace.
- Ba lần trên torai-OB cho cùng điểm. Thứ hạng giống hệt lần 1 ở 86/90 và 84/90 ca (RCD bên trong TORAI dùng `np.random` không đặt seed).
- Ba lần trên torai-SS cho AVERAGE 0,949 / 0,951 / 0,953.
- 0 rỗng, 0 Traceback. `cham.py` khớp `main.py` mọi ô.
- Khớp ở đây là khớp số công bố, chưa phải chạy đúng phương pháp. T-016 đo trên cùng cấu hình: lõi RCD không nhận cột metric nào (lỗi giảm mẫu hai lần) và 176/184 cụm (OB), 171/173 (SS) rơi nhánh dự phòng về thứ tự mức nghiêm trọng (`results/T-016/giam-mau-hai-lan.md`).

## 8. N-Sigma phát hiện

**Kết luận: khớp ở OB; lệch nhỏ ở SS, chưa tìm ra nguyên nhân.** Đây là cách chạy tái lập: dùng mốc tiêm để cắt cửa sổ và để chấm. Không dùng được cho chế độ tự phát hiện ở P3 (luật cứng 6; mục 2.3).

- Bộ phát hiện: `baro.anomaly_detection.nsigma(k=3, startsfrom=100)`.
- Chuẩn bị dữ liệu và luật chấm chép từ `reproduce_bocpd` (`scripts/nsigma_phat_hien.py`). TP nếu có cảnh báo; FP nếu cảnh báo đầu tiên trước mốc tiêm.
- Nguồn số: `cham/nsigma-phat-hien.txt`.

| Dữ liệu | Mốc Bảng 2 bài BARO (P / R / F1) | w300 (P / R / F1) | full (P / R / F1) |
|---|---|---|---|
| fse-ob | 0,54 / 1 / 0,70 | 0,5155 / 1 / 0,6803 (FP 94/100) | 0,5208 / 1 / 0,6849 (FP 92/100) |
| fse-ss | 0,56 / 1 / 0,72 | 0,5208 / 1 / 0,6849 (FP 92/100) | 0,5208 / 1 / 0,6849 (FP 92/100) |

- Theo tiêu chí ≤ 0,02, OB "full" khớp (P −0,019, F1 −0,015). OB "w300" lệch rất nhỏ (P −0,025, F1 −0,020). SS lệch (P −0,039, F1 −0,035).
- Hai lần chạy giống hệt cả danh sách điểm phát hiện (200/200 bản ghi).

**Kiểm cách chấm** (`scripts/tom_tat_phat_hien_va_moc_a.py`, `cham/phat-hien-luu-san.txt`), chấm lại các file phát hiện tác giả lưu sẵn trong `fse-*`:
- `naive_bocpd.json` với ngưỡng 300 cho OB 0,7634 / 1 / 0,8658, đúng đầu ra mong đợi của README (BOCPD, 0,76 / 1,00 / 0,87). Tức luật chấm được dựng lại đúng.
- `nsigma.json` với ngưỡng 360 (cả ca) cho OB 0,5435 / 1 / 0,7042, đúng Bảng 2. Cho SS cũng 0,5435 / 1 / 0,7042, tức chính file của tác giả cũng không ra 0,56 / 0,72 cho SS.
- Điểm phát hiện đầu tiên của tôi trùng `nsigma.json` ở 24/100 (OB) và 28/100 (SS) ca. Như vậy cấu hình N-Sigma tác giả dùng (cột, ngưỡng k, `startsfrom`) khác cấu hình mặc định ở đây. Bài không ghi cấu hình này, nên không kiểm tiếp được.

**Đọc số cho đúng.** R luôn bằng 1, vì TP tính cho mọi ca có ít nhất một cảnh báo. Do đó P = 100 / (100 + FP), sàn là 0,50. Mốc 0,54 ứng với FP ≈ 85; 0,56 ứng với FP ≈ 79. Chênh 0,02–0,04 ở P tương ứng 7–13 ca.

## 9. GDN

**Kết luận: không có mốc số (loại C); chạy ổn định.** Lệnh như nhánh `cpu` của `run.sh` trên MSL mẫu của repo (`scripts/chay_gdn.py`, `cham/gdn-msl.txt`):
- Loss giảm từ 0,4695 (epoch 0) xuống 0,1115 (epoch 29), có vài epoch tăng nhẹ.
- Hai lần cùng seed giống hệt: loss từng epoch, SHA-256 trọng số, `test_scores.npy` từng byte.
- Điểm hữu hạn: −1,61 đến 347,4.
- F1 0,878 (`report='best'`, ngưỡng tốt nhất theo nhãn test của MSL mẫu; chỉ ghi lại, không phải mốc).

Chỗ xử lý vì Windows: `get_save_path` đặt tên file có `|` và `:`. Tôi chỉ thay `strftime` của tên `datetime` trong module `main.py`; khối `__main__` chạy nguyên văn. Phạm vi R1: mục 2.3.

## 10. Không kiểm được trong task, và hệ quả (SL26)

- **Chưa kiểm ở cỡ Train Ticket.** Task này không dùng `fse-tt`, cũng không dùng RE2-TT (có ca khóa). Bài BARO chỉ có số CIRCA trên Train Ticket cho 15/100 ca. Hệ quả: tính đúng của các phương pháp trên dữ liệu cỡ Train Ticket (64 service, ~200–400 kênh) chưa được kiểm trực tiếp. Những hành vi phụ thuộc kích thước, như PC của CIRCA suy biến hay chạy lâu, có thể khác.
- **BARO trên torai-OB không có mốc** (dòng BARO Bảng 2 bài TORAI nghi chép nhầm). Hệ quả: chỉ biết BARO khớp ở torai-SS và fse.
- **GDN không có số mốc.** Hệ quả: chỉ biết GDN chạy ổn định, không biết nó cho kết quả đúng như bài.
- **N-Sigma phát hiện:** không biết cấu hình tác giả dùng cho `nsigma.json`. Hệ quả: lệch ở SS chưa giải thích được.
- **Cách chạy BOCPD và N-Sigma phát hiện** của tác giả đưa mốc tiêm vào đầu vào (cắt cửa sổ quanh mốc tiêm, hoặc biên file đối xứng). Dùng được để tái lập, không dùng cho chế độ tự phát hiện ở P3 (luật cứng 6).
- **Windows thay vì Linux** cho RCD, CIRCA: chưa so trên cùng máy Linux (đã kiểm cho RCD, TORAI ở T-016: cùng seed, thứ hạng giống hệt; CIRCA chưa).
- **RCD torai-OB với cửa sổ 20 chỉ có 46/90 ca.** Mỗi lần bị dừng ở 3 giờ (Q-40, Minh quyết giữ ngân sách). Hệ quả: chưa có số RCD torai-OB đủ 90 ca ở cấu hình của bài, chỉ có so sánh trên 46 ca chung.
- **Cấu hình CIRCA của bài BARO** (có thể là repo CIRCA gốc với `pcalg` của R): chưa dựng. Hệ quả: lệch của CIRCA trên fse chưa giải thích.

## 11. Điều chưa chắc, cần Minh quyết

1. **Độ dài cửa sổ cho P3. Minh quyết (04/10/2026): chưa chốt; chốt trong task tổng hợp G1, cùng với chọn dataset, chia dev/test và cách dùng nhãn.** Theo lời Minh: hiện chưa đủ căn cứ để chọn một con số cụ thể; 10 và 20 phút chỉ là các cấu hình đã dùng để kiểm tái lập. Số liệu liên quan: lựa chọn này làm đổi kết quả nhiều (một ô N-Sigma đổi 0,26; AVERAGE RCD đổi 0,13). Cửa sổ 10 tái lập được RobustScorer[t_inject], N-Sigma[t_inject] của bài BARO và là cấu hình lúc ghi mốc `SETUP.md`; cửa sổ 20 tái lập được dòng BARO của bài TORAI (các baseline khác chưa xác nhận); TORAI dùng 10 theo `docs/TORAI.md`.
2. **T-007.** Mốc MicroRank, TraceRCA của T-007 (dòng Trace Bảng 2 bài TORAI) nhiều khả năng chạy với cửa sổ 20, trong khi T-007 dùng 10. Minh quyết có cho T-007 kiểm thêm không. **Minh quyết (04/10/2026): T-007 không kiểm thêm cửa sổ 20.**
3. **RCD torai-OB cửa sổ 20 chưa đủ ca.** Nếu cần số đủ 90 ca, có thể chạy riêng khi máy rảnh. Ước lượng chưa kiểm: 1,5–3 giờ mỗi khối nếu chạy một mình. Đã làm ở T-016: 90/90 ca trên EC2 trong 5 624 s, Avg@5 0,742 (`results/T-016/diem-mo-t006.md`).
4. **CIRCA lệch ở mức ô, và trên fse.** Có hai hướng: (a) chấp nhận là lệch loại B, kèm các nguyên nhân khả thi ở mục 5; (b) dựng CIRCA gốc của NetManAIOps (cần cài R và `pcalg`) để kiểm giả thuyết bài BARO dùng code gốc. Chi phí của (b) chưa ước lượng.
5. **Chạy lại trên Linux.** SPEC ghi: nếu một mục lệch, đề xuất chạy lại mục đó trên EC2 trong T-007. Hai mục ứng viên là RCD torai-OB và CIRCA. Minh quyết.
6. **N-Sigma phát hiện, SS lệch 0,04.** Chính file `nsigma.json` của tác giả cũng không ra số Bảng 2 cho SS. Đề xuất: chấp nhận, ghi là lệch chưa giải thích.
7. **Luật X1 với mốc B (REVIEW R1). Minh quyết (04/10/2026): giữ `py312-pin`, không dừng.** Ghi thẳng: luật được làm rõ sau khi đã thấy kết quả; kết quả không phụ thuộc cách hiểu, vì hai bộ giống nhau ở mọi ô CIRCA. Căn cứ: WHY-15.
