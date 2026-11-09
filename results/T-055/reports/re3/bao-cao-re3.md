# Báo cáo RE3-OB bản cuối — M1 khóa P7(a) trên lỗi mã nguồn

T-055. Người làm: Claude. Người phản biện: Codex (phản biện sau, theo lựa chọn của Minh). Ngày 08/11/2026.
Trạng thái: **chờ phản biện**. Mọi quyết định Claude tự đưa ra (D-55-1 … D-55-9) nằm trong `tasks/T-055-re3-ban-cuoi/LOG.md` để Minh kiểm.

Nguồn số (đường dẫn tính từ gốc repo):

- **R** = `results/T-055/reports/re3/phan-tich-re3.json` (sinh bởi `results/T-055/scripts/phan_tich_re3.py`).
- **G** = `results/T-054/reports/re3-ban-cuoi-001/re3-tables.json` (lượt chính, bảng tách khỏi A4).
- **C** = `results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json` (CIRCA bổ sung).
- **D** = `results/T-054/reports/re3-ban-cuoi-001/tables-describe.json` (vế dẫn xuất C-d1/C-d2/C-c/C-g, vùng, vị trí N).

Theo WHY-06/Q-246, RE3 chỉ có mô tả: cỡ chênh kèm CI bootstrap cặp theo ô (10 ô, 10.000 mẫu, seed 20261005). Không có phép kiểm định, không gộp với TT hay Nezha.

---

## 0. Tóm tắt

- **Đã chạy:** 420 slot lượt chính (30 ca × 12 vế, TORAI B ba seed) trên hai EC2 và 30 slot CIRCA bổ sung trên laptop. Tất cả VERIFIED; seal xong mới ghép nhãn (`results/T-055/runs/cham-001/main-receipt.json#/states`).
- **Kết quả chính (world P):**
  - M1: MRR 0,925, Hit@1 0,867, Hit@5 1,000.
  - SimpleRCA M4: MRR 0,975, Hit@1 0,950. Chênh M1 − M4 = −0,050, CI [−0,133; 0,033]; 1 ca M1 thắng, 4 ca thua, 25 hòa.
  - TORAI B: MRR 0,544. M1 hơn +0,381, CI [0,256; 0,481].
  - Nguồn: `R#/bang_theo_ve_P`, `R#/so_cap/M1-simplerca|rr`, `R#/so_cap/M1-torai_B|rr`.
- **RQ3d:** M1 bằng C-a0 (bỏ E1/E2/E5), Δ = 0, 1 thắng/1 thua. Bỏ từng thành phần không làm kém đi: bo-E1 0,942, bo-E2 0,936, bo-E5 0,933, C-a1 0,944. Quy tắc trên cùng đồ thị: C-d1 (sâu nhất) 0,950 > M1. C-g (SimpleRCA + PageRank trên cạnh của M1) 0,992 là cao nhất.
- **Đọc theo bảng diễn giải đã khóa:** RE3 không cho bằng chứng việc dùng quan hệ trong M1 có ích. M1 thua M4 theo điểm ước lượng; CI chứa 0, nên chưa phân biệt được.
- **Vì sao M1 thấp hơn M4:** 4 ca M1 sai đều có cơ chế đọc được từ trung gian (§4). Hai cơ chế chính đều là cách tính điểm của E4/E6a, không phải đồ thị:
  1. Một kênh khác root có z cực lớn: do z tính từ max(A), hoặc do IQR nền bằng 0 nên z bị tính theo đơn vị gốc (byte).
  2. Kênh log lỗi, tín hiệu chính của lỗi mã nguồn, có điểm bị chặn ở 1 nên không bao giờ đứng đầu khóa xếp hạng.

## 1. Lượt chạy và sự cố

| Bước | Kết quả | Nguồn |
|---|---|---|
| Tải 30 ca lên hai EC2 (131,7 MiB) | 90/90 file khớp sha256 LFS | `results/T-055/runs/tai-001/` |
| Preflight không nhãn khóa trước | Đơn vị: span µs, log s, metric 1 s; lồng cha–con 100%. R7 chặn ở 24 ca vì có mã 400 → D-55-8 khai thêm 400 | `results/T-055/runs/preflight-001/decision-002.json` |
| Lượt chính 420 slot, 2 EC2 × 2 worker | 420 VERIFIED (thời lượng theo `events.jsonl` trên EC2; chưa tổng hợp) | `results/T-055/runs/cham-001/main-receipt.json` |
| Lỗi đã phân loại | 30 CIRCA `ModuleNotFoundError` (môi trường, **không hợp lệ**, D-55-9); MicroRank 2 và TraceRCA 2 lỗi phương pháp thật (operation `currencyservice_Export` mới trong A, khớp preflight R9) | `R#/loi_phuong_phap` |
| CIRCA bổ sung (laptop, môi trường CIRCA đã kiểm, lớp phủ v2) | 30 VERIFIED, cả hai biến thể OK | `C`, `results/T-055/runs/cham-001/circa-verified-before-labels.json` |
| Nhận về laptop | Chỉ kết quả, biên nhận và bảng chuẩn bị CSV của TORAI B (cần để kiểm chuỗi liên kết); parquet thô ở lại EC2. Lượt nhận đầu thiếu CSV nên verify dừng; giữ bản đó ở `received-001-thieu-csv` | `score_re3.py` |
| Ghi sổ xem test | `results/T-054/reports/re3-ban-cuoi-001/exposure.jsonl` (RE3_LABEL_JOIN) | — |

CIRCA trong bảng lượt chính `G` là 30 hàng không hợp lệ (ERROR môi trường, chấm 0). Báo cáo này dùng `C` cho CIRCA.

## 2. Bảng theo vế (world P, 30 ca)

`R#/bang_theo_ve_P/<vế>`:

| Vế | MRR | Hit@1 | Hit@3 | Hit@5 | Trạng thái |
|---|---:|---:|---:|---:|---|
| C-g (M4 + PageRank E6b) | 0,992 | 0,983 | 1,000 | 1,000 | OK 30 |
| SimpleRCA M4 | 0,975 | 0,950 | 1,000 | 1,000 | OK 30 |
| C-d1 (sâu nhất có cờ) | 0,950 | 0,900 | 1,000 | 1,000 | OK 30 |
| C-a1 (chỉ E1) | 0,944 | 0,900 | 1,000 | 1,000 | OK 30 |
| bỏ E1 / bỏ E2 / bỏ E5 | 0,942 / 0,936 / 0,933 | 0,900 / 0,900 / 0,867 | — | 1,000 | OK 30 |
| **M1** | **0,925** | **0,867** | 0,967 | 1,000 | OK 30 |
| C-a0 (bỏ E1/E2/E5) | 0,925 | 0,867 | 0,967 | 1,000 | OK 30 |
| CIRCA (RHT+DA, bổ sung) | 0,917 | 0,833 | 1,000 | 1,000 | OK 30 |
| CIRCA RHT, phụ | 0,878 | 0,767 | 1,000 | 1,000 | OK 30 |
| C-d2 (khởi phát sớm nhất) | 0,789 | 0,667 | 0,867 | 0,933 | OK 30 |
| TORAI B (ba seed) | 0,544 | 0,133 | 0,933 | 1,000 | OK 90 |
| BARO | 0,487 | 0,000 | 0,967 | 0,967 | OK 30 |
| C-c (RRF BARO+M4+TraceRCA) | 0,313 | 0,200 | 0,200 | 0,200 | OK 30 |
| MicroRank | 0,080 | 0,000 | 0,033 | 0,033 | OK 28, ERROR 2 |
| TraceRCA | 0,061 | 0,033 | 0,067 | 0,067 | OK 28, ERROR 2 |

Hit@5 của M1, M4 và mọi vế M1-family đều bằng 1 ở cả 30 ca: độ đo chạm trần. MRR và Hit@1 mới phân biệt được.

**So cặp với M1** (`R#/so_cap/M1-<vế>|rr`; Δ = M1 − vế; CI theo ô):

| Vế | Δ MRR | Thắng/hòa/thua | CI |
|---|---:|---|---|
| SimpleRCA M4 | −0,050 | 1/25/4 | [−0,133; 0,033] |
| C-g | −0,067 | 0/26/4 | [−0,133; 0,000] |
| C-d1 | −0,025 | 0/28/2 | [−0,058; 0,000] |
| C-a0 | 0,000 | 1/28/1 | [−0,025; 0,025] |
| C-a1 | −0,019 | 1/27/2 | [−0,061; 0,011] |
| bo-E1 / bo-E2 / bo-E5 | −0,017 / −0,011 / −0,008 | 0/29/1 · 1/28/1 · 0/29/1 | — |
| CIRCA | +0,008 | 4/23/3 | [−0,092; 0,117] |
| C-d2 | +0,136 | 8/20/2 | [0,028; 0,258] |
| TORAI B | +0,381 | 25/4/1 | [0,256; 0,481] |
| BARO | +0,438 | 27/3/0 | [0,367; 0,500] |

**Theo loại lỗi** (`R#/tach/fault`, MRR):

| Lỗi | n | M1 | M4 | C-a0 | CIRCA | TORAI B | BARO |
|---|---:|---:|---:|---:|---:|---:|---:|
| f1 sai tham số | 9 | 0,889 | 0,944 | 0,861 | 0,889 | 0,509 | 0,500 |
| f2 thiếu tham số | 3 | 0,833 | 1,000 | 0,833 | 1,000 | 0,583 | 0,500 |
| f3 thiếu lời gọi hàm | 6 | 1,000 | 1,000 | 1,000 | 1,000 | 0,500 | 0,500 |
| f4 sai giá trị trả về | 6 | 1,000 | 1,000 | 1,000 | 0,917 | 0,500 | 0,500 |
| f5 thiếu xử lý ngoại lệ | 6 | 0,875 | 0,958 | 0,917 | 0,833 | 0,667 | 0,433 |

Có 10 ô và 4 service gốc (emailservice 15 ca, adservice 9, currencyservice 3, cartservice 3). Số ca mỗi nhóm nhỏ; một nhóm không là mẫu hình.

## 3. Quan sát về baseline (mô tả, chưa lần cơ chế sâu)

- **Đầu bảng của từng baseline** (đọc `result.json` đã VERIFIED; lệnh ở LOG):
  - BARO xếp `redis` đầu ở 30/30 ca, nên Hit@1 = 0 và root thường ở hạng 2–3.
  - TORAI B xếp `frontend` (14) hoặc `checkoutservice` (12) đầu, là các bên gọi.
  - TraceRCA chỉ trả 7 thực thể và thường không có root.
- **SimpleRCA có Hit@1 = 0,950.** Thực thể nó xếp đầu (email 15, ad 9, currency 3, cart 2) gần trùng phân bố root (email 15, ad 9, currency 3, cart 3).
  - Ứng viên (chưa kiểm): với lỗi mã nguồn, log lỗi và metric của chính service hỏng là tín hiệu trực tiếp; cách bỏ phiếu đơn giản trên ba nguồn khai thác được ngay.
  - Bài FSE 2026 cũng báo SimpleRCA mạnh trên RCAEval (LESSONS ST10). Kết quả này nhất quán với nhận định đó, nhưng chưa là kiểm chứng.
- **Baseline trace-latency (MicroRank, TraceRCA) gần như mất tác dụng** (MRR 0,08 và 0,06).
  - Ứng viên: lỗi mã nguồn không làm tăng độ trễ span. Hai baseline này còn lỗi phương pháp ở 2 ca có operation mới.
- **C-c thấp (0,313)** dù M4 rất cao.
  - Ứng viên: RRF cộng hạng của TraceRCA (thường thiếu root) và BARO (luôn đặt redis đầu), nên kéo thực thể khác lên trên root.

## 4. Vì sao M1 sai 4/30 ca — lần trung gian (luật 15)

Trung gian: `R#/trung_gian_M1_family/<ca>/M1`. Code: `src/m1/e4.py` (z = (max(A) − trung vị N)/IQR N; nếu IQR < 10·eps thì c = 1, dòng 279); `src/m1/xep_hang.py` (khóa E6a = tầng, max s, …).

| Ca | Ô | Root ở khối | Thực thể đứng trên | Kênh thắng | Kênh mạnh nhất của root |
|---|---|---|---|---|---|
| `test-0d4b3947ca` | currencyservice f1 | 2 | shippingservice | metric mem, s = 376 832; r_len_A = r_len_N = 0 | E2 s = 654,7 (rộng 0,076); mem s = 57,7 (rộng 0,89) |
| `test-cde8f873f5` | currencyservice f1 | 2 | checkoutservice (bên gọi) | self-time E1, s = 814,1, rộng 0,105 | latency-90 s = 241,9; self-time rộng 0,76 |
| `test-d07d23cade` | emailservice f2 | 2 | currencyservice | E2 frontend→currency, s = 241,7, rộng 0,014 | mem s = 134,2, rộng 0,957 |
| `test-428cf2c868` | emailservice f5 | 4 | payment, checkout | workload s = 6,3; cpu s = 5,0 | log lỗi s = 1,0; latency-90 s = 0,2 |

**Cơ chế 1 — z cực trị của kênh hẹp hoặc của nền hằng** (3 ca đầu).

- **Quan sát:** kênh thắng có độ rộng ≤ 0,105 (hoặc bằng 0), còn root có kênh rộng 0,76–0,96.
- Ở `0d4b`: kênh `shippingservice_mem` không có mẫu A nào vượt ngưỡng trên, nhưng s = 376 832, đúng bằng 368 KiB.
- **Suy luận:** khi nhiều hơn nửa mẫu N bằng nhau, IQR = 0, nên E4 đặt c = 1 và z thành chênh tuyệt đối theo byte. **Trong điều kiện metric nền có IQR = 0, bước chuẩn hóa z của E4 đánh giá sai độ lớn lệch (phụ thuộc đơn vị đo), và khóa E6a đặt kênh đó lên đầu.**
- **Ca đúng có điều kiện tương ứng:** cùng nhánh này giúp root ở `test-299b7a94b2` và `test-b826c34da1` (emailservice mem s = 44,9 triệu và 6,3 triệu). Vì vậy đây là đặc tính hai chiều của cách tính, không phải nguyên nhân riêng của ca sai.
- Hiện tượng này giống 6/10 ca sai ở P7(a) (`results/T-054/reports/p7a-013-v2/bao-cao.md` §7.5). Đây là lần lặp lại thứ hai, trên dữ liệu độc lập.

**Cơ chế 2 — log lỗi không cạnh tranh được trong khóa xếp hạng** (ca `428c`, và nói chung).

- **Quan sát:** kênh đếm log lỗi có điểm `e` thuộc [0, 1] (`src/m1/e4.py:226`; NEW_OP = 1,0). Trên RE3, 41/42 kênh log có s = 1,0. Root có cờ log ở 12/30 ca.
- **Suy luận:** khóa E6a đặt max s ngay sau tầng. Vì vậy log lỗi chỉ giúp root vào tầng 1, không bao giờ thắng được một kênh metric hay trace có z > 1. **Trong điều kiện lỗi mã nguồn mà tín hiệu chính của root là log lỗi hoặc mã lỗi (f5 thiếu xử lý ngoại lệ), bước xếp E6a bỏ qua độ lớn của bằng chứng log, vì kênh đếm và kênh phân vị khác thang.**
- Ở `428c`, root chỉ có log lỗi s = 1,0 và latency s = 0,2, nên đứng thứ 4 sau các thực thể có workload/cpu s ≈ 5–6.

**Thông tin M1 không đọc.** M1 không dùng `statusCode` của span. Preflight cho thấy mã lỗi gRPC/HTTP khác 0 xuất hiện chủ yếu ở frontend, checkout và payment (`results/T-055/runs/preflight-001/*-status-values.json`, gộp, không theo ca). Chưa kiểm được mã lỗi có tập trung ở root hay không (cần đọc theo ca sau ghép nhãn), nên giữ là câu hỏi mở.

**Tách nguồn hạn chế (luật 17):**
- Dữ liệu: 2 ca có operation mới làm TraceRCA/MicroRank lỗi.
- Giao thức: Hit@5 chạm trần; 10 ô.
- Adapter/cài đặt: CIRCA thiếu môi trường trên EC2 (đã xử lý).
- Giả định phương pháp: c = 1 khi IQR = 0; thang kênh đếm khác thang kênh phân vị; không có kênh status span.

Không cộng các cờ trên thành tỷ lệ nguyên nhân.

## 5. RQ3d trên RE3

- **Bỏ quan hệ:** bỏ E1, E2, E5 (C-a0) cho đúng MRR của M1. Bỏ từng thành phần thì nhỉnh hơn một chút. CI của các chênh đều chứa 0 hoặc chạm 0. Không có bằng chứng quan hệ giúp trên RE3.
- **Quy tắc đơn giản trên cùng đồ thị:** C-d1 0,950 ≥ M1 (0/28/2). C-d2 0,789 < M1 (8/20/2). Hỗn hợp; không có quy tắc nào bị M1 vượt rõ.
- **Bước lan trên đồ thị gắn với baseline mạnh:** C-g (SimpleRCA + PageRank trên cạnh quan sát của M1) 0,992 > M4 0,975, nhờ 1 ca. Trên P7(a), C-g kém M4 ở cả TT và OB. Kết quả trái dấu giữa dataset, nên không khẳng định gì (không có đồ thị ngẫu nhiên, WHY-07).

## 6. So với P7(a) và hệ quả

| | TT (P7a) | OB Nezha (P7a) | RE3-OB |
|---|---|---|---|
| M1 MRR | 0,975 | 0,875 | 0,925 |
| Mốc so sánh | TORAI B 0,931 | M4 0,689 | M4 0,975 |
| M1 − C-a0 | 0 | +0,164 | 0 |
| Cơ chế sai chính | z cực trị hẹp | z cực trị hẹp | z cực trị / IQR = 0; log bị chặn |

- **Điều kiện M1 hơn baseline:** lỗi tài nguyên và mạng, khi E1/E2 tách được độ lệch của chính root (OB Nezha).
- **Điều kiện M1 không hơn:** TT (gần trần, quan hệ không thêm gì) và lỗi mã nguồn RE3 (M4 bỏ phiếu đơn giản tốt hơn).
- **Hệ quả cho FlashTicket (P9/P10):** lỗi nghiệp vụ trong bán vé (ngoại lệ, sai giá trị trả về, thiếu xử lý lỗi) giống RE3 hơn là giống lỗi tài nguyên. Kho quan sát hiện tại trên `origin/main` (08/11) chưa có tracing, chưa có metric Prometheus (chỉ mở `health,info`), log là console thường; B16 mới là kế hoạch. Đề xuất (chưa kiểm, để Minh quyết):
  1. Khi triển khai B16, ghi đủ span status và exception event của OTel, metric lỗi theo service/endpoint (`http.server.requests` có `status`/`outcome`), và log JSON có `errorType`/`errorCode`.
  2. Nếu giữ M1 cho FlashTicket, cần thiết kế lại trên dev FlashTicket (không trên RE3): (i) kênh lỗi từ span status; (ii) đưa kênh đếm và kênh phân vị về cùng thang trước khóa max s; (iii) bỏ nhánh c = 1 phụ thuộc đơn vị khi IQR = 0. Kiểm độc lập trên lượt FlashTicket mới (C-15 B), vì RE3 đã dùng.
  3. Luôn giữ SimpleRCA M4 làm baseline bắt buộc trên FlashTicket.

## 7. OPEN

- Mã lỗi span có tập trung ở root không (cần đọc theo ca sau ghép nhãn).
- Cơ chế của BARO (luôn chọn redis) và TORAI B (chọn bên gọi): chưa lần trung gian.
- H1 giữ "chưa kiểm": đơn vị, r và U là giả định đã qua preflight; chưa có xác nhận của tác giả.
- Vùng nghi ngờ và vị trí N đã tính trong D (`#/regions`, `#/position_N`), chưa diễn giải trong báo cáo này.
- Không có kiểm định; 10 ô; Hit@5 chạm trần.

## 8. Tái lập

```text
py -3 -B results/T-055/scripts/re3_build.py           # nguồn độc lập (đã chạy; file 'x' sẽ từ chối ghi đè)
<env main> -B results/T-055/scripts/score_re3.py main|circa   # nhận/kiểm/chấm (đã chạy)
<env main> -B results/T-055/scripts/phan_tich_re3.py <file-ra>  # phân tích, ghi file mới
```
