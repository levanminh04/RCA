# T-005 — Đo khả thi môi trường và thời gian chạy

Đo ngày 03/10/2026. Task này không chấm điểm phương pháp: thứ hạng trả ra được lưu ở `D:\RCA-ext\work\T-005\out\`, không ai đọc.

Mọi số dưới đây lấy từ `runs/ket-qua-do.jsonl` (mỗi dòng một lượt chạy). Log từng lượt ở `runs/do-<mục>-<biến thể>-lan<N>.log`. Cách dựng môi trường ở `moi-truong.md`.

## 1. Cách đo

**Máy:** laptop Windows 11, i5-1240P (16 luồng logic), RAM 16 GB, không GPU. Lúc đo, các ứng dụng khác (ChatGPT, Chrome, Claude, Zalo) vẫn mở. RAM trống lúc bắt đầu mỗi lượt là 3,4–6,9 GB (cột `ram_trong_truoc_mb`).

**Ca đo:** `re2tt_ts-route-service_socket_1`. Đây là ca có `metrics.parquet` + `traces.parquet` lớn nhất (36 007 800 B) trong 35 ca có sẵn ở `data/rcaeval/`, chọn theo kích thước file, không theo tên hay nhãn. Ca dài 24 phút: 1441 dòng metric (1 điểm/giây), 375 metric, 1 535 674 span. Chọn ca này không phải là chọn dataset (MRP §4, Q-31).

**Hai biến thể đầu vào** (Minh quyết 03/10):
- `win`: cấu hình `--length 10` của RCAEval (lệnh trong `docs/TORAI.md`), tức 300 dòng metric trước mốc tiêm + 300 dòng sau. Mặc định của `main.py` là `--length 20` (`main.py:122`). Với cấu hình này còn có 20 + 20 dòng chuỗi log/trace của TORAI. Cửa sổ trace cho MicroRank, TraceRCA (span có `startTime` trong 300 s trước và 300 s sau mốc) là lựa chọn của người làm, cùng độ dài với cửa sổ metric: `main.py` không có nhánh đọc trace.
- `full`: toàn ca, cùng các bước làm sạch, không cắt.

Kích thước đầu vào (`runs/12-chuan-bi-dau-vao.log`): metric `win` 600×347, `full` 1441×347 (292 cột không hằng ở cả hai, `runs/14-dem-bien.log`); trace `win` 644 810 span, `full` 1 535 674 span.

**"Chạy được" trong file này = chạy hết không lỗi; chưa kiểm đúng sai.**

**Mỗi lượt** chạy trong một tiến trình con riêng, giới hạn 1 giờ (`scripts/do.py`). Ghi:
- **Thời gian hàm**: chỉ phần gọi hàm phương pháp, đo bằng `time.perf_counter` trong tiến trình con. Không gồm import và đọc file.
- **Tổng tiến trình**: từ lúc tạo tiến trình con tới lúc nó kết thúc, đo ở tiến trình cha. Gồm cả import thư viện (3–7 s ở `py312`, vì `RCAEval.e2e` nạp cả torch).
- **RAM đỉnh**: RSS đỉnh của tiến trình con, psutil lấy mẫu mỗi 0,1 s. Kèm bộ nhớ riêng (commit) đỉnh do Windows ghi; số này luôn lớn hơn vì gồm cả vùng nhớ thư viện đã cấp mà chưa dùng tới. Riêng thư viện và dữ liệu đã nạp (đo ngay trước khi gọi hàm, cột `ws_before_method_mb`) đã chiếm khoảng 370 MB khi nạp RCAEval và metric ở `py312` (580–890 MB khi nạp trace), 115 MB khi chỉ nạp repo BARO (hai bộ phát hiện), 150 MB ở `py38-rcd`, 385 MB ở `py38-gdn`.

**Lượt chạy lại.** Bảy lượt đầu (BARO full, N-Sigma, TraceRCA, RCD) chạy song song với một lệnh `du` đo dung lượng đĩa. Cả bảy được chạy lại (lan2); bảng ghi cả hai lần.

## 2. Kết quả

Thời gian tính bằng giây; RAM tính bằng MB. "win / full" là hai biến thể đầu vào. Lần 1 / lần 2 cách nhau bằng dấu "·".

### 2a. Phương pháp RCA

| Mục | Môi trường | Cài được | Chạy được | Thời gian hàm (win / full) | Tổng tiến trình (win / full) | RSS đỉnh (win / full) | Commit đỉnh (win / full) | Lỗi gặp và cách xử lý | Kết luận cho P1/P3 |
|---|---|---|---|---|---|---|---|---|---|
| BARO (RCAEval) | py312 | có | có | 0,21 / 0,17 · 0,31 | 6,9 / 5,5 · 7,0 | 378 / 384 · 383 | 1312 / 1318 · 1317 | không | Rất nhẹ. Chạy trên mọi ca không đáng kể |
| N-Sigma (RCAEval) | py312 | có | có | 0,53 · 0,25 / 0,16 · 0,21 | 7,5 · 8,3 / 6,2 · 8,0 | 379 · 378 / 384 · 384 | 1314 · 1313 / 1318 · 1318 | không | Như BARO |
| CIRCA-PC (RCAEval) | py312 | có | **không xong trong 1 giờ** | > 3600 / > 3600 | 3600 (dừng) / 3600 (dừng) | 1497 / 1568 | — (bị dừng nên không có) | Vượt giới hạn 1 giờ ở cả hai biến thể, kể cả cửa sổ 10 phút | **Không chạy được nguyên trạng ở P3.** Xem mục 4 |
| MicroRank (RCAEval) | py312 | có | có | 101 / 238 | 106 / 242 | 1202 / 2342 | 2290 / 3494 | không | Chạy được. Toàn ca cần khoảng 2,3 GB RSS; nên chạy tuần tự hoặc tối đa 2 ca song song trên máy 16 GB |
| TraceRCA (RCAEval) | py312 | có | có | 3,5 · 2,9 / 7,7 · 6,5 | 9,5 · 10,5 / 14,0 · 13,7 | 778 · 795 / 1280 · 1319 | 1841 · 1857 / 2434 · 2470 | không | Nhẹ |
| RCD (RCAEval) | py38-rcd | có (2 file vá) | có | 69 · 99 / 174 · 170 | 74 · 114 / 177 · 172 | 158 · 158 / 166 · 166 | 1184 · 1184 / 1289 · 1289 | không | Chạy được. Thời gian dao động giữa các lần (69 và 99 s trên cùng đầu vào), có thể do RCD không đặt seed; chưa kiểm |
| TORAI (RCAEval) | py38-rcd | có (2 file vá) | có | 7,1 / 15,1 | 9,4 / 17,5 | 156 / 163 | 1150 / 1155 | không | Nhẹ. Thời gian của bản RCAEval nguyên trạng. Lõi giảm mẫu metric hai lần (15 × 15; `torai.py:81` và `_rcd_multimodal` dòng 29): ở `win` chỉ còn 1 điểm sau mốc nên `drop_constant` bỏ mọi cột, lõi không nhận metric; ở `full` còn 3 điểm sau mốc. Chưa tách được nguyên nhân chênh thời gian với RCD |

### 2b. Bộ phát hiện (chạy trên toàn ca; BOCPD có thêm cửa sổ 600 điểm)

| Mục | Môi trường | Cài được | Chạy được | Thời gian hàm | Tổng tiến trình | RSS đỉnh | Commit đỉnh | Lỗi gặp và cách xử lý | Kết luận cho P1/P3 |
|---|---|---|---|---|---|---|---|---|---|
| BOCPD (repo BARO), toàn ca 1441 điểm | py312 | có | **không xong trong 1 giờ** | > 3600 | 3600 (dừng) | 264 | — | Vượt giới hạn 1 giờ | Không chạy một lần trên chuỗi dài được. Xem mục 4 |
| BOCPD, cửa sổ 600 điểm (cùng cách cắt 300 + 300 như `reproduce_bocpd` của BARO; Minh duyệt 03/10. Khác tập cột: `bocpd()` tự chọn 76 cột (latency -50 và -90, error; 60 không hằng, `runs/14-dem-bien.log`), còn `reproduce_bocpd` chỉ lấy latency-50 và error) | py312 | có | có | 1440 | 1448 | 227 | 1227 | không | 24 phút cho một cửa sổ 10 phút. Chậm hơn thời gian thực |
| N-Sigma phát hiện (repo BARO, mọi cột, k=3, `startsfrom=100`) | py312 | có | có | 59 | 60 | 129 | 597 | không | Chạy được. Chạy trên mọi cột; chọn cột vẫn là việc mở (T-001 mục 8.1) |
| GDN — học (30 epoch, 5 ca × 720 điểm trước mốc, 333 cột) | py38-gdn | có (sau 2 lượt sửa gói, xem `moi-truong.md` mục 5) | có | 1029 | 1035 | 720 | 3293 | Hai chỗ không chạy nguyên trạng trên Windows, xử lý trong script (`moi-truong.md` mục 6) | Chạy được ở cỡ 3600 điểm học (17 phút, RSS dưới 1 GB); với nhiều giờ dữ liệu thì chưa kiểm |
| GDN — suy luận (toàn ca đo, 1436 cửa sổ) | py38-gdn | có | có | 11,7 | 15,2 | 712 | 3235 | như trên | Nhẹ |

**GDN, chi tiết:** cấu hình theo `run.sh` của GDN (batch 32, cửa sổ trượt 5, dim 64, topk 5, out_layer_inter_dim 128, val_ratio 0,2, seed 5), `report='val'`. Chạy đủ 30 epoch (log có 30 dòng epoch); 2876 cửa sổ học, 719 cửa sổ kiểm định. Học khoảng 34 s mỗi epoch. Thời gian học tăng gần tuyến tính theo số điểm học và số epoch (chưa kiểm).

## 3. Mục không đo, và lý do

| Mục | Lý do |
|---|---|
| SimpleRCA (cài lại theo mô tả bài) | Chưa có code; phải cài lại theo bài (mức M4). SPEC mục "Không làm": phần tính toán của nó nhẹ hơn CIRCA-PC |
| CIRCA, biến thể đồ thị kiến trúc | Phải viết bộ dựng cấu hình đồ thị (mức M2). SPEC mục "Không làm". Bước chấm điểm (`rht`) dùng chung với CIRCA-PC; chỉ khác bước dựng đồ thị. Thời gian của bước chấm điểm riêng **chưa đo**, vì CIRCA-PC chưa chạy xong lần nào |
| Luật trace (μ+3σ theo span) | Không đo riêng. Luật này là bước đầu bên trong hàm `microrank` và `tracerca` của RCAEval, nên đã nằm trong thời gian của hai mục đó |
| SPOT | Không dùng (Q-38) |

## 4. Đề xuất cho P3 (tất cả **chưa kiểm**)

**CIRCA-PC.** Một ca, cửa sổ 10 phút, 292 biến không hằng, chạy hơn 1 giờ mà chưa xong; toàn ca cũng vậy. Với vài chục ca, chạy nguyên trạng không khả thi. Chưa biết phần nào chậm (bước PC của causal-learn hay bước chấm điểm `rht`), vì chưa đo riêng. Các hướng, mỗi hướng phải có mục WHY trước khi dùng:
1. Đo riêng bước PC và bước `rht` trên ca này, với giới hạn dài hơn (ví dụ 3 giờ, cần Minh đồng ý theo luật cứng 8). Đây là bước nên làm trước, vì các hướng dưới phụ thuộc vào nó.
2. Giảm số biến: tùy chọn `dk_select_useful=True` có sẵn trong RCAEval. Giả định: PC chậm do số biến. Sai nếu phần chậm là `rht`. Lệch so với cách RCAEval chạy để công bố số.
3. Giới hạn bậc của tập điều kiện trong PC (`depth`). Lệch khỏi mặc định; có thể đổi đồ thị và kết quả.
4. Chạy song song nhiều ca. PC trong causal-learn chạy một luồng (chưa kiểm); máy có 16 luồng nhưng RAM trống chỉ 3–7 GB, mỗi lượt cần khoảng 1,5 GB RSS.

**Số tác giả công bố (bài BARO, arXiv 2405.09330, Bảng 5, 6 và chú thích Bảng 3; dữ liệu `fse-tt` của BARO, không phải RE2-TT):** CIRCA trên Train Ticket mất trung bình 7564,88 s mỗi ca (khoảng 2,1 giờ) và chỉ chạy được 15/100 ca vì bước PC thất bại; BOCPD (phát hiện của BARO) 173,37 s mỗi ca; N-Sigma phát hiện 0,53 s mỗi ca. Kết quả CIRCA-PC "> 1 giờ" ở trên phù hợp với số này. BOCPD và N-Sigma phát hiện ở T-005 chậm hơn số công bố khoảng 8 và 100 lần; chưa rõ lý do, việc tìm lý do thuộc T-008. Nguyên nhân khả thi, **chưa kiểm**: BOCPD ở T-005 chạy trên 76 cột (cả latency-90) thay vì tập cột của `reproduce_bocpd`; N-Sigma phát hiện của repo BARO là vòng lặp tính lại trung bình và độ lệch chuẩn trên toàn quá khứ ở mỗi bước (O(n²) mỗi cột), và T-005 chạy nó trên mọi cột thô (375).

**BOCPD.** Toàn ca 1441 điểm vượt 1 giờ; cửa sổ 600 điểm mất 24 phút. Nếu thời gian tăng theo bình phương độ dài như cấu trúc vòng lặp của code (`_bocpd.py`, mỗi bước xử lý mọi độ dài chạy đã có), toàn ca cần khoảng (1441/600)² × 24 ≈ 140 phút. Ở chế độ tự phát hiện:
- Chạy theo cửa sổ trượt ngắn thay vì một lần trên cả chuỗi. Chi phí phụ thuộc độ dài cửa sổ và bước trượt; chưa đo.
- Thử giảm số cột (BOCPD tự chọn khoảng 60 cột độ trễ và lỗi không hằng ở ca này; `runs/14-dem-bien.log`, số này đếm thô, có thể lệch vài cột vì giá trị thiếu).

**Cho P1 (chạy tay một ca):** BARO, N-Sigma, TraceRCA, TORAI chạy dưới 20 s; RCD, MicroRank dưới 5 phút; GDN học 17 phút. Không có trở ngại. CIRCA-PC và BOCPD toàn ca thì chưa.

**Ước lượng thô cho P3** (nhân thời gian toàn ca với số ca, chạy tuần tự; chưa kiểm vì ca khác có thể nặng hơn hoặc nhẹ hơn): 90 ca × (MicroRank 238 s + RCD 174 s + các mục nhẹ khoảng 30 s) ≈ 11 giờ, chưa kể CIRCA-PC và BOCPD. Đây là cận trên: dùng thời gian `full` của ca lớn nhất, trong khi `main.py` chạy theo cửa sổ.

## 5. Giới hạn của phép đo

- Một ca duy nhất. Ca khác, nhất là ca dài hơn hoặc nhiều span hơn, có thể nặng hơn.
- Máy không dành riêng: các ứng dụng khác chiếm RAM và CPU. Thời gian là chỉ báo, không phải số chuẩn.
- RCD cho thời gian khác nhau giữa hai lần chạy (69 và 99 s); lần 2 máy bận hơn (import 14,0 s so với 4,4 s). Các mục khác chạy hai lần lệch dưới 1,5 s.
- `py312` dùng pandas 3.0.6 do RCAEval không ghim (`moi-truong.md` mục 3). Thời gian có thể khác khi dùng pandas 2.x; chưa kiểm.
