# Giao thức P3 trên RE2-TT dev — bản 2

Ngày 05/10/2026. T-022, phiên 3, người làm Claude. Viết theo DECISIONS Q-64–Q-67, Q-72 và Q-74.

**Trạng thái.** Mọi lựa chọn ở đây đã có quyết định của Minh, trừ các chi tiết thực thi đánh dấu **[D1]–[D12]** (mục 15): đó là cách hiện thực Q-74 mà Q-74 chưa nói tới, chờ Minh xác nhận cùng văn bản WHY. Không lựa chọn nào được dùng cho số khoa học trước khi mục WHY tương ứng được ghi vào `docs/WHY.md` (luật cứng 3). Văn bản WHY đề xuất ở `de-xuat-why-v2.md`. **Cập nhật 06/10/2026:** Minh duyệt văn bản WHY, gồm D1–D12 (DECISIONS Q-76); đã chép vào `docs/WHY.md` thành WHY-22–35. Từ đây các lựa chọn trong giao thức này đã có WHY hiệu lực.

**Bản cũ.** `giao-thuc.md`, `lua-chon-can-duyet.md`, `de-xuat-why.md`, `quy-tac-cot.json`, `cau-hinh/p3-re2tt-de-xuat.json` giữ nguyên làm lịch sử. Mục 0 liệt kê chỗ bản 1 sai và đã sửa ở đây.

**Ai cài.** T-030 (Q-74 Q1) cài `src/p3/`, fixture, pilot theo giao thức này. T-022 không viết code.

**Sửa sau phản biện V2 (06/10/2026).** Minh duyệt "sửa theo đề xuất" ở LOG phiên 4; sửa tại chỗ, không tạo bản 3. Phản biện và phản hồi ở `tasks/T-022-giao-thuc-p3/REVIEW.md` (phần "Phản biện T-022 — giao thức P3 bản 2"). Chỗ đã sửa:
- §4, §5.1: ghi ngoại lệ về thời điểm có kết quả của TORAI A, BOCPD, và tập cột của bộ phát hiện (V2-R3).
- §6.6 nguồn B: thêm luật tên cột trace TT (N1). K-B1 so theo tên cột, không gộp về service (V2-R1).
- §6.6 khóa, §8.4: xếp hạng hai cấp cho TORAI; bỏ câu "mọi service của hai cụm tính là một nhóm hòa" (V2-R2).
- §7.1: thay lý do chọn cả bản ghi; thêm giới hạn nền 720 s (N2).
- §15: dòng D4, D10.

**Sửa sau phản biện tiếp (06/10/2026).** Minh duyệt "sửa theo đề xuất" ở LOG "Phiên 5 (tiếp 2)"; sửa tại chỗ. Phản biện và phản hồi ở `REVIEW.md` (phần "Phản biện tiếp T-022 — bản V2 sau sửa ngày 06/10/2026"). Chỗ đã sửa:
- §7.2, §8.3, §11.7, §15 dòng D12: posterior BOCPD không hữu hạn → `ERROR` (V2-S1).
- §8.4: cận lạc quan/bi quan chỉ cho độ đo đơn điệu theo hạng; Rerank@1 không có cận (V2-S2).
- §4 dòng "Bộ phát hiện", §10: tách BOCPD (hồi cứu) và N-Sigma (danh sách cột theo cả bản ghi không đổi báo động tới τ); giữ t̂+300 cho N-Sigma (V2-S3).

**Sửa sau kiểm lại (06/10/2026).** Minh duyệt "sửa theo đề xuất" ở LOG "Phiên 6 (tiếp)"; sửa tại chỗ. Phản biện và phản hồi ở `REVIEW.md` (phần "Kiểm lại T-022 sau sửa V2-S1–S3"). Chỗ đã sửa:
- §6.5 K-SVR2 và gạch "Route hồi quy", §13 `diagnostics.regression_routes`, §15 dòng D5: nút có cha hiệu lực rơi về z-score sau `ValueError` không tính là SVR chạy thành công; ghi route từng nút cho mô hình được khóa, cả OLS (V2-T1).
- §8.3 dòng `TIMEOUT`: giới hạn khai trước khi chạy; cách tính khi hết ngân sách tổng (N3).

Ký hiệu: `t` là mốc chia (mốc tiêm ở chế độ (a), thời điểm báo động `t̂` ở chế độ (b)). N là đoạn bình thường, A là đoạn sự cố. "Thực thể" (entity) là tiền tố trước dấu `_` đầu tiên của tên cột metric, hoặc `serviceName` của span.

---

## 0. Chỗ bản 1 sai và cách sửa

| # | Bản 1 nói | Sai vì | Bản 2 | Bằng chứng |
|---|---|---|---|---|
| 1 | Span vào cửa sổ theo `startTime` trong [t−300, t+300) (`lua-chon-can-duyet.md:30`) | Span bắt đầu trước t+300 nhưng kết thúc sau đó chưa có lúc t+300 | Span vào khi `startTime ≥ t−300` và kết thúc `< t+300` (mục 5.2) | Q-74 Q2 |
| 2 | CIRCA test 10 điểm cuối tới t+300 (`lua-chon-can-duyet.md:31, 90`) | `CaseData` nạp khoảng đóng tới `current = t+300`, thêm NaN ở biên rồi nội suy (`RCAEval/classes/data.py:89–104`; `src/circa_kien_truc/scoring.py:38`). Cửa sổ nửa mở không có điểm t+300 | `current` = thời điểm quan sát thật cuối cùng < t+300 (mục 6.5) | Q-74 Q2 |
| 3 | `main.py` ffill/điền 0 rồi cắt, "runner không thêm bước chung" (`giao-thuc.md:54`) | `main.py:308–309` ffill trên toàn file trước khi cắt (`:314–315`), nên ô trống đầu cửa sổ có thể nhận giá trị trước t−300 | Cắt trước, tiền xử lý của tác giả sau, trên đúng dữ liệu trong cửa sổ [D1] | Q-74 Q2 |
| 4 | TORAI dùng dữ liệu tác giả, lệch lưới "giữ như code" (`lua-chon-can-duyet.md:30, 48`) | Ở ca auth_cpu_1, N phủ [t−295, t+5), A phủ [t+5, t+305); ngưỡng `tracets_lat` tính trên toàn file | Chạy A và B; B làm chính nếu qua phép kiểm K-B (mục 6.6) | REVIEW điểm 1; Q-74 Q3 |
| 5 | "Chạy riêng từng ca nên không học quy luật cột vắng" (`lua-chon-can-duyet.md:76`) | Chỉ loại đường học xuyên ca. Số cột vẫn đổi số alert, số chiều, tập ứng viên, đồ thị | Bỏ lập luận; schema là một kênh thông tin, kiểm ở P4 (mục 10) | REVIEW điểm 6; Q-74 Q5 |
| 6 | MicroRank: operation không có nền "không bị cờ"; thiếu trace bình thường → ERROR (`lua-chon-can-duyet.md:106–107`) | Code báo `ValueError` khi có operation mới hoặc std NaN (`src/microrank/__init__.py:54–56`); thiếu trace bình thường là trả về bình thường với status `no_normal_traces` (`:68–70`) | Giữ đúng hợp đồng của code (mục 6.3) | REVIEW điểm 2; Q-74 Q7 |
| 7 | TraceRCA: "lọc trong src/p3" sau khi hàm trả `ranks` (`giao-thuc.md:76`) | Hàm sắp cả NaN rồi mới bỏ (`RCAEval/e2e/tracerca.py:86–93`); lọc danh sách trả về không sửa được thứ tự | Lấy `ji_dict` trước khi sắp (mục 6.4) | REVIEW điểm 3; Q-74 Q8 |
| 8 | Hòa: kỳ vọng cho Hit/RR/DCG, phá theo tên cho hàm RCAEval, rồi gọi là trùng nghĩa (`lua-chon-can-duyet.md:139–142`) | Hai quy tắc cho hai kết quả khác nhau (Hit@1 = 0,5 so với AC@1 = 1). Điểm bằng nhau chưa chắc là hòa (CIRCA DA sắp theo `key`) | Một quy tắc cho bảng chính, theo khóa xếp hạng thật; bảng RCAEval riêng (mục 8.4–8.6) | REVIEW điểm 4; Q-74 Q10 |
| 9 | BOCPD "dùng posterior tới i" (`lua-chon-can-duyet.md:163`) | `maxes[t] = R[:, t].argmax()` là posterior trước khi thấy `x_t` (`baro/_bocpd.py:212–225`); `maxes[T]` không gán, sinh sentinel | Tính lại `maxes` từ R; không còn sentinel (mục 7.2) | REVIEW điểm 5; Q-74 Q11 |
| 10 | Chấm phát hiện theo episode với thời gian trơ 300 s (`lua-chon-can-duyet.md:174, 176`) | Báo động sai trước mốc mở episode và che báo động đúng | Chấm bằng báo động thô; thời gian trơ chỉ cho lượt RCA (mục 7.4–7.5) | REVIEW điểm 5, Q13; Q-74 Q13 |
| 11 | Nhãn phát hiện theo bài BARO (`lua-chon-can-duyet.md:175`) | Bài BARO dùng corpus khác | Nhãn proxy theo README RCAEval (mục 7.4) | `results/T-002/public-metadata/run-002/sources/hf-README.md:97` |
| 12 | Cặp detector–ranker "có cơ sở prior work" (`lua-chon-can-duyet.md:177`) | Bài BARO ghép detector với CIRCA bản PC, không phải bản kiến trúc; chưa ai kiểm các cặp ở đây | Gọi là "tích hợp P3" (mục 7.5) | Q-74 Q14 |
| 13 | RCA sau báo động sai "vẫn chấm theo root của ca" (`lua-chon-can-duyet.md:178`) | RCA sau báo động sai có thể trúng root do may | Thành công chung đòi báo động ghép đúng sự kiện (mục 7.5) | Q-74 Q14 |
| 14 | Mức ngẫu nhiên tính trên U (`lua-chon-can-duyet.md:60`) | Ứng viên thật của phương pháp khác U | Bốn tập; mức ngẫu nhiên trên tập quan sát của phương pháp (mục 8.1, 8.7) | Q-74 Q4 |
| 15 | Bootstrap theo ô, không ghép cặp (`lua-chon-can-duyet.md:143`) | So hai phương pháp cần cùng mẫu lấy lại | Bootstrap theo cặp ô (mục 8.8) | Q-74 Q10 |
| 16 | Ca pilot chọn theo số cột thô/số span toàn file (`lua-chon-can-duyet.md:195`) | Chi phí phụ thuộc kích thước sau tiền xử lý | Chọn theo kích thước sau xử lý (mục 12) | Q-74 "Thêm" |
| 17 | Phản biện kết quả ghi `REVIEW-ket-qua.md` (`lua-chon-can-duyet.md:219`) | AGENTS §9: người phản biện chỉ ghi `REVIEW.md` | Ghi tiếp `REVIEW.md`; T-030 có REVIEW riêng | Q-74 Q16 |

**Ảnh hưởng tới `dung-lai-bang-chung.csv`** (giữ nguyên file; đọc cùng bảng này):
- R9 (SimpleRCA): cột "dung_lai_cho_P3" ghi có thể dùng lại số 30 ca nếu Minh xác nhận cấu hình. Q-74 đã xác nhận cấu hình, nhưng cửa sổ bản 2 đòi span kết thúc trước t+300, còn adapter T-017 lọc span theo `startTime` (`src/simplerca/adapter.py:63–69`). Số `run-dev-005` không dùng lại nguyên trạng; dùng lại code.
- E1 (bộ chấm): dùng `Evaluator` chỉ cho bảng RCAEval riêng, với `max_k = 10`; bảng chính do evaluator P3 tính theo quy tắc hòa mục 8.4.
- R1 (BARO), R3 (CIRCA), R8 (TORAI): thêm phần thiếu do bản 2: lấy khóa xếp hạng (mục 8.4); CIRCA thêm `current`, đồ thị từ span kết thúc trước t, khóa mô hình K-SVR; TORAI thêm nguồn B và K-B.

---

## 1. Phạm vi

- Dataset: 30 ca dev RE2-TT (`allowlist-dev.json`). Không mở 60 ca test, không mở RE3-OB (luật cứng 1).
- Phương pháp tầng 1 (Q-62): BARO (RobustScorer), SimpleRCA (M4, quy ước T-017), MicroRank-RCAEval sửa đầu vào, TraceRCA lọc hữu hạn, CIRCA đồ thị kiến trúc, TORAI bản sửa (WHY-19). Bộ phát hiện: N-Sigma, BOCPD (tập cột Q-67).
- Ngoài phạm vi: benchmark đủ 30 ca (T-024), chế độ (b) đủ (T-025), Nezha/Eadro (T-026/T-027), tầng 2.

## 2. Trạng thái từng thành phần

| Thành phần | Quyết định | Chi tiết thực thi chờ xác nhận |
|---|---|---|
| Dataset, chia dev | Q-61, Q-63 | — |
| Cửa sổ, cách cắt | Q-64; Q-74 Q2 | D1, D2, D3 |
| Mốc tiêm ở (a), ngân sách nhãn 0 | Q-66 | — |
| Universe và bốn tập | Q-74 Q4 | — |
| Bộ cột | Q-67 (BOCPD), Q-74 Q5 | — |
| BARO | Q-62; Q-74 Q10 (khóa) | D10 |
| SimpleRCA | Q-74 "Thêm" (WHY-17) | — |
| MicroRank | Q-74 Q7 | D6, D12 |
| TraceRCA | Q-74 Q8 | D11, D12 |
| CIRCA kiến trúc | Q-74 Q6 | D3, D5 |
| TORAI | WHY-19, WHY-20; Q-74 Q3 | D4, D10 |
| Trạng thái, hòa, độ đo, bootstrap | MRP P7, Q-65; Q-74 Q9, Q10 | D10, D12 |
| Chế độ (b) | Q-72; Q-74 Q11–Q14 | D7, D8, D9 |
| Ca pilot | Q-74 "Thêm" | — |

## 3. Dữ liệu và tách nhãn

- `allowlist-dev.json`: 30 ca, mã mờ `dev-<10 hex>`, đường dẫn dưới `data/rcaeval/`, SHA-256 và byte từng file. Chỉ runner đọc.
- `nhan-dev.json`: root, loại lỗi, ô (root × loại lỗi), nhóm vị trí, mốc tiêm và nguồn mốc. Runner chỉ đọc mốc tiêm cho chế độ (a). Evaluator đọc phần còn lại.
- Phương pháp và bộ phát hiện không nhận tên ca, mã mờ, đường dẫn hay file nhãn.
- Trước mỗi lượt: SHA-256 file đọc phải trùng allowlist; sai thì runner dừng, ghi lỗi runner (không phải lỗi phương pháp, mục 8.3).

## 4. Ai biết gì, lúc nào

| Tác nhân | Chế độ (a) | Chế độ (b) |
|---|---|---|
| Runner | allowlist; mốc tiêm để cắt cửa sổ | allowlist; không đọc mốc tiêm |
| Bộ phát hiện | — | bảng metric cả bản ghi, chỉ cột `time` và cột đã chọn; tập cột chọn theo tên cột có trong file của cả bản ghi. Với BOCPD đây là thông tin hồi cứu; với N-Sigma nó không đổi báo động tới mọi thời điểm τ (mục 10) |
| Ranker | dữ liệu trong [t−300, t+300) và `t` | dữ liệu trong [t̂−300, t̂+300) và `t̂` |
| Evaluator | bản ghi đầu ra đã lưu + nhãn | báo động và bản ghi RCA đã lưu + nhãn |
| Kết quả RCA có sẵn lúc | t+300 (cộng thời gian chạy); **ngoại lệ:** nhánh dùng TORAI A chỉ có kết quả sau cuối file | t̂+300 (cộng thời gian chạy) với N-Sigma; **ngoại lệ:** với BOCPD, chính t̂ chỉ có sau cuối bản ghi; nhánh dùng TORAI A chỉ có kết quả sau cuối file |

Ngoại lệ ở dòng cuối (V2-R3): TORAI A dùng bin của tác giả phủ tới t+305 và ngưỡng `tracets_lat` tính trên toàn file (mục 6.6); BOCPD bỏ cột hằng và min–max trên cả bản ghi trước khi xác định điểm đổi (mục 7.2). Các nhánh này là hồi cứu: không gắn kết quả của chúng với thời điểm t+300 hay t̂+300, và không gọi chúng là cùng giới hạn thông tin với các nhánh khác.

Nhãn chỉ được nối sau khi đầu ra đã ghi ra file. Đổi locator mà giữ nội dung dữ liệu phải cho đầu ra giống hệt (mục 11).

## 5. Chế độ (a) — biết trước thời điểm

### 5.1 Cửa sổ thông tin

N = [t−300, t), A = [t, t+300), theo timestamp, nửa mở (Q-64; Q-74 Q2). Ranker chạy sau t+300. Mỗi ca RE2-TT là một bản ghi riêng, mốc ở giây 720 của 1.441 điểm (30/30 ca, `runs/allowlist-001/kiem-allowlist.json`), nên 300 s trước mốc không chồng lần tiêm nào. Giới hạn thông tin t+300 áp cho mọi nhánh trừ TORAI A (bin tới t+305, ngưỡng `tracets_lat` toàn file; xem ngoại lệ ở mục 4).

### 5.2 Cắt từng nguồn

| Nguồn | Điều kiện vào cửa sổ |
|---|---|
| Metric | `time` ∈ [t−300, t+300) |
| Span | `startTime` ≥ t−300 **và** `startTime + duration` < t+300 (µs đổi sang s) [D2] |
| Log | `timestamp` ∈ [t−300, t+300) |
| TORAI A | 20 dòng `logts`/`tracets` mỗi phía theo `time < t` (`main.py:381–393`); metric theo dòng trên |
| TORAI B | dựng lại theo mục 6.6 |

Span bắt đầu trước t−300 bị bỏ, kể cả khi kết thúc trong cửa sổ.

### 5.3 Thứ tự cắt và tiền xử lý [D1]

Runner cắt trước. Tiền xử lý của tác giả (ví dụ `main.py:297–309`: bỏ `_latency-50`, `inf → NaN`, `ffill`, điền 0) chạy sau, chỉ trên dữ liệu trong cửa sổ. Khác `main.py` chỉ ở ô trống đầu cửa sổ: `main.py` lấy giá trị từ trước t−300, bản này điền 0. T-030 đếm số ô khác nhau ở 30 ca (không cần nhãn) và ghi lại.

### 5.4 Chia N/A bên trong phương pháp: giữ của tác giả

| Phương pháp | Cách chia nội bộ | Nguồn |
|---|---|---|
| BARO | `time < t` → N | `RCAEval/e2e/baro.py:22–24` |
| SimpleRCA | metric, log theo thời điểm; span theo `startTime < t` | `src/simplerca/adapter.py:55–82` |
| MicroRank | span theo thời điểm kết thúc `< t` | `src/microrank/__init__.py:49–50` |
| TraceRCA | span theo thời điểm kết thúc `< t` | `RCAEval/e2e/tracerca.py:53–54` |
| CIRCA RHT | train 111 điểm [t−120, t−10], test 10 điểm cuối tới `current` | `RCAEval/classes/data.py:175–176`; mục 6.5 |
| TORAI | 20 bin 15 s mỗi phía | `main.py:381–393`; mục 6.6 |

### 5.5 Thiếu dữ liệu

Ghi số dòng và số giây thực của N, A cho từng nguồn. Không kéo dài cửa sổ để bù.

## 6. Phương pháp tầng 1

Môi trường: `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-flashticket/src`. TORAI: `py38-rcdlock`, tiến trình riêng. Dựng `logts` cho TORAI B: `T-016-cong-cu` (có drain3). Không sửa môi trường hay code phương pháp đã có.

### 6.1 BARO (RobustScorer)

- Code: RCAEval `259ea41` `e2e/baro.py`, tham số mặc định. Tiền xử lý `main.py:297–309` trên cửa sổ (mục 5.3).
- Khóa xếp hạng: `max` robust z của mỗi cột. Hàm chỉ trả tên (`baro.py:54–55`), nên adapter tính lại điểm bằng đúng các lời gọi `preprocess` và `RobustScaler` của hàm, rồi kiểm: sắp lại bằng `sorted` ổn định phải ra **đúng** danh sách chính thức [D10]. Không khớp → ERROR runner, không chấm.
- Thực thể: tiền tố trước `_`; điểm thực thể = điểm cột cao nhất.

### 6.2 SimpleRCA (M4, quy ước T-017)

- Code `src/simplerca`, cấu hình WHY-17: metric 3σ (ddof 0, một phía, `>`), đơn vị alert "events"; trace P95 tỉ lệ 3; log từ khóa ERROR/FAIL/EXCEPTION, ngưỡng 0; tổng điểm toàn 0 → abstain.
- Cửa sổ theo mục 5.2. Adapter T-017 lọc span chỉ theo `startTime` (`src/simplerca/adapter.py:63–69`), nên runner P3 lọc span trước khi gọi `prepare`. Vì vậy số `results/T-017/runs/run-dev-005/` không dùng lại nguyên trạng.
- Khóa: điểm service; hòa theo nhóm điểm bằng nhau (WHY-17).
- Abstain → NO_EVIDENCE.

### 6.3 MicroRank-RCAEval sửa đầu vào

- Code `src/microrank`, `PYTHONHASHSEED=0`; kiểm thêm seed 1 trên ca pilot.
- Xếp đầy đủ (`full_ranks`, `scores`) làm chính; báo kèm `service_ranks_top11` (`src/microrank/__init__.py:99–103`).
- Thực thể: `serviceName` qua `operation_services` (`:47`); điểm thực thể = điểm operation cao nhất. Khóa = điểm đó.
- Hợp đồng trạng thái giữ như code: `ValueError` (operation mới sau mốc, std nền NaN, ID trùng khác nội dung, khóa mơ hồ, điểm không hữu hạn: `:31–56, 97–98`) → ERROR, giữ nguyên thông điệp; trả về bình thường với `missing_window`, `no_anomalous_traces`, `no_normal_traces` (`:51, 68–70`) → NO_EVIDENCE, giữ status gốc [D12].
- **Bước đầu của T-030:** chạy MicroRank trên 30 ca ở cửa sổ mục 5.2, chỉ đọc trạng thái (không chạy evaluator), đếm ca ERROR theo nguyên nhân. Báo Minh trước pilot [D6].

### 6.4 TraceRCA lọc hữu hạn

- Code RCAEval `e2e/tracerca.py`, gọi nguyên trạng. Adapter đọc `ji_dict` lúc hàm trả về bằng `sys.setprofile` (cùng cách `src/circa_kien_truc/scoring.py:60–65` đọc `DAScorer`), không sửa code [D11].
- Giữ operation có `ji` hữu hạn; sắp giảm dần theo `ji`. `ji` NaN (support 0, hoặc tổng span bất thường A = 0) → không xếp.
- Kiểm: danh sách chính thức phải bằng danh sách sắp từ `ji_dict` khi không có NaN; trên ca pilot, `ji` phải khớp phép tính độc lập `results/T-015/scripts/check_tracerca.py`.
- Thực thể: `serviceName` của span, lấy từ bảng cặp (operation, serviceName) trong dữ liệu; một operation ứng nhiều service → ERROR, như MicroRank (`src/microrank/__init__.py:46`). Điểm thực thể = `ji` cao nhất. Khóa = điểm đó.
- Trạng thái: `KeyError` khi operation mới sau mốc (`tracerca.py:59`) → ERROR; danh sách rỗng → NO_EVIDENCE.

### 6.5 CIRCA đồ thị kiến trúc

- Builder `src/circa_kien_truc` với CIRCA `0215e18`; chạy với `PYTHONHASHSEED=0` đặt trước khi khởi Python.
- Đồ thị gọi từ span có `startTime ≥ t−300` và kết thúc `< t` (chỉ dữ liệu bình thường đã kết thúc trước mốc) [D3].
- Giữ metric cô lập làm ứng viên không cha (như T-014).
- Scorer chính: RHT + DA (θ = 3). Báo kèm RHT-only, cùng lượt.
- `current` = thời điểm quan sát thật cuối cùng của metric trong A (trên lưới 1 s là t+299) [D3]. Test = 10 điểm cuối tới `current`; không có điểm điền ở biên phải. `score_graph` nhận `current` (`src/circa_kien_truc/scoring.py:22, 38`).
- **Mô hình khóa trước khi chạy (Q-74 Q6):** SVR nếu qua K-SVR, không thì OLS [D5].
  - K-SVR1: cấu hình đúng bài: `ANMRegressor(regressor=SVR(kernel="sigmoid"))`, tham số khác mặc định sklearn 1.6.0 (`CIRCA/circa/experiment/comparison/models.py:583–586`); dùng lớp RCAEval `RHTScorer(regressor=…)` (`RCAEval/graph_heads/rht.py:155–164`), không sửa code. `score_graph` cố định LinearRegression, nên T-030 viết đường gọi SVR trong `src/p3`.
  - K-SVR2: 30/30 ca chạy không ném lỗi, mọi z hữu hạn; ghi route từng nút theo ba loại của T-014: `no_effective_parents` (không cha hiệu lực, z-score trực tiếp, hợp lệ theo code tác giả), hồi quy thành công, `value_error_fallback` (kèm thông điệp lỗi). Nút có cha hiệu lực mà rơi `value_error_fallback` dưới SVR thì K-SVR2 không đạt. Lý do: RHT bắt `ValueError` của hồi quy, ghi cảnh báo rồi trả z-score trực tiếp, không ném lên (`RCAEval/graph_heads/rht.py:118–124`); SVR có lỗi riêng mà OLS không có (sklearn 1.6.0 `svm/_base.py:275`, hệ số không hữu hạn), nên đầu ra hữu hạn không chứng minh SVR đã chạy (REVIEW V2-T1).
  - K-SVR3: chạy hai lần cho đầu ra giống hệt.
  - K-SVR4: tổng 30 ca ≤ 3 giờ trên laptop (Q-40).
  - Không chạy evaluator trên đầu ra CIRCA trước khi mô hình được khóa và ghi LOG. Số SVR mà T-014 đã thấy trên 25 ca MEM fse-OB không được dùng làm căn cứ.
  - Tên ghi trong bảng: "CIRCA kiến trúc, SVR(sigmoid)+RHT+DA, cấu hình P3" hoặc "CIRCA kiến trúc, OLS+RHT+DA, cấu hình P3".
  - Route hồi quy (V2-T1): mô hình được khóa, cả OLS, ghi route và thông điệp lỗi từng nút như `src/circa_kien_truc/scoring.py:44–57` (OLS dùng cùng đường bắt lỗi, `rht.py:135`). Số nút `value_error_fallback` báo cạnh bảng CIRCA, như giới hạn của cấu hình; không phải cổng. `ValueError` do kiểm đầu vào (NaN/inf) xảy ra như nhau với OLS, nên K-SVR2 trượt vì lý do này thì chuyển OLS không bỏ được nhánh dự phòng; ghi điều đó.
- **Sửa 06/10/2026 (Q-80, WHY-30 ghi chú T-031):** mô hình khóa là OLS; SVR(sigmoid) chỉ báo làm cấu hình phụ vì gần như không hồi quy trên RE2-TT (dự đoán gần hằng; nguyên nhân gồm kernel bão hòa và `epsilon` so với thang y, chưa tách định lượng; WHY-30). Tên trong bảng: "CIRCA kiến trúc, OLS+RHT+DA, cấu hình P3".
- **Lỗi làm tròn (Q-82, WHY-36):** chỉ dùng bản OLS gốc, không biến thể sửa. Ca có ít nhất một nút điểm RHT > 1e10 ghi là "ca lỗi làm tròn" (luật tách không dùng nhãn, chốt trước khi chấm). Nguyên nhân mới được xác nhận ở 11 ca dev (`results/T-031/chan-doan-diem-lon.json`). Ở ca khác, tên nhóm chỉ có nghĩa là vượt ngưỡng. Bảng CIRCA báo trên mọi ca, kèm riêng kết quả trên các ca không vượt ngưỡng.
- **Kiểm độ nhạy builder (Q-74 Q6):** dựng lại đồ thị với hash seed 1 và 2 ở 30 ca; đếm ca đổi cạnh và ca đổi thứ hạng DA (so thứ hạng, không dùng nhãn). Không chọn seed theo kết quả.
- Khóa: DA dùng `key = (score, −index, z-score)` (`RCAEval/graph_heads/rht.py:285`; `src/circa_kien_truc/scoring.py:66–68`); RHT-only dùng `score`. Thực thể: tiền tố của nút metric; khóa thực thể = khóa nút cao nhất.

### 6.6 TORAI bản sửa

- Code `src/torai/torai_sua.py` (WHY-19); seed {0, 1, 2}, `np.random.seed(s)` trước mỗi lời gọi (WHY-20). Không truyền `service`, `fault_type`, `case`.
- **Nguồn A (dữ liệu tác giả):** `logts.csv`, `tracets_err.csv`, `tracets_lat.csv` của torai-TT; cắt 20 dòng mỗi phía theo `time < t`. Ghi lệch lưới từng ca (ở auth_cpu_1: N phủ [t−295, t+5)) và ngưỡng `tracets_lat` toàn file.
- **Nguồn B (tự dựng từ parquet RE2):**
  - Lưới 15 s gốc ở t−300: bin k = [t−300+15k, t−300+15k+15), k = 0..39; N = bin 0..19, A = bin 20..39.
  - Span lọc theo mục 5.2, xếp bin theo `startTime // 10⁶` (`results/T-016/dung-logts-tracets.md:23`).
  - Tên cột trace TT (N1; khác quy tắc OB ở `dung-logts-tracets.md:24`): cột = service + `_` + operation chuẩn hóa. Chuẩn hóa `operationName`: bỏ `/api/v1/`, bỏ `{` và `}`, đổi `_` thành `-`, đổi mỗi chuỗi dấu cách hoặc `/` thành một `-`, bỏ `-` ở hai đầu. Service: `serviceName` của span; riêng span có `operationName` chỉ là phương thức HTTP (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) lấy `serviceName` của span con (span có `parentSpanID` bằng `spanID` của nó), không có con thì giữ service của span. Ở ca dev `re2tt_ts-auth-service_cpu_1`, luật này cho đúng 157/157 tên cột của `tracets_err.csv` tác giả, không thừa, không thiếu (LOG phiên 4, 03:01). **Chưa kiểm:** 29 ca còn lại và giá trị ô; K-B1 kiểm cả hai.
  - `tracets_err` = tổng `statusCode` mỗi (cột, bin) (`dung-logts-tracets.md:25`).
  - `tracets_lat` = số span có `duration > μ + 3σ`; μ, σ (ddof 1) học trên span có `startTime ≥ t−300` và kết thúc `< t`. Cột có < 2 span như vậy thì bỏ, ghi số cột bỏ.
  - `logts`: Drain riêng mỗi service (drain3 0.9.11, chế độ B, ngưỡng 0,4), học trên log trong cửa sổ theo thứ tự thời gian; đếm theo `timestamp` của dòng log; cột `<service>_<id>` (`dung-logts-tracets.md:73`). Ca không có `logs.parquet` thì không có cột log.
  - Metric: `metrics.parquet`, cột `ts-*`, cắt theo mục 5.2.
- **Phép kiểm K-B, khai báo trước, không dùng nhãn [D4].** B làm dòng chính khi qua cả ba; không qua thì A làm dòng chính. Cả A và B đều chạy và báo. Không đổi sau khi thấy số.
  - K-B1 (dựng trace đúng): dựng `tracets_err`, `tracets_lat` theo quy ước tác giả (lưới của file tác giả, ngưỡng toàn file) và luật tên cột ở trên cho 30 ca; so với file tác giả **theo đúng tên cột** (cột, bin), không gộp về service, như S9 của T-016 (`tasks/T-016-ho-so-torai/SPEC.md:95`). Mọi ô của cột không ghép được tên (có ở một bên) tính là sai. Đạt khi tỉ lệ ô trùng ≥ 95 % cho từng chuỗi, gộp 30 ca; ngưỡng 95 % lấy từ S9. Được thử tối đa 3 cách dựng (AGENTS §5a.1), giữ mọi lần thử, chỉ so với file tác giả, chưa chạy TORAI. Lý do không gộp về service: TORAI tính z từng cột, lấy max |z|, chia tổng cả nguồn rồi mới cộng theo service (`src/torai/torai_sua.py:176–200, 206–235`), nên tổng (service, bin) trùng vẫn có thể cho điểm khác (REVIEW V2-R1). Nếu luật tên cột không đúng ở ca khác mà 3 lần thử không sửa được, K-B1 để OPEN và trình Minh; không đổi đơn vị so sánh để đạt, không gọi phép so tổng (service, bin) là kiểm dựng đúng đặc trưng TORAI.
  - K-B2 (dựng log tự nhất quán): tổng đếm mỗi service trong `logts` B bằng số dòng log của service đó trong cửa sổ, ở cả 30 ca. Ghi thêm, không tính đạt/không đạt: tổng log toàn file mỗi service của parquet so với file tác giả.
  - K-B3 (chạy được): TORAI sửa chạy trên B ở 30 ca × 3 seed không lỗi; ghi tỉ lệ cụm rơi nhánh dự phòng.
- **Khóa xếp hạng hai cấp [D10]:** TORAI chỉ trả thứ tự (`torai_sua.py:360–366`). Code sắp cụm theo điểm cụm (`:296`, sắp ổn định trên chỉ số cụm GMM, không mang thông tin) rồi nối **trọn từng khối cụm** (`:300–360`). Adapter dựng lại từ biến cục bộ (`cluster_rank`, `y_pred`, `y_train`, `service_list`) và giá trị trả về của mỗi lần gọi `_rcd_multimodal`, bắt bằng `sys.setprofile`:
  - Cấp 1 (khối): mỗi cụm là một khối, khóa khối = điểm cụm.
  - Cấp 2 (trong khối): thứ tự RCD nếu cụm đi nhánh RCD; `y_train` nếu rơi nhánh dự phòng (các service có `y_train` bằng nhau thì hòa trong khối).
  - Kiểm: nối các khối theo thứ tự `cluster_rank` của code, trong khối theo thứ tự của code, phải trùng `ranks` chính thức. Không sắp phẳng theo tuple (điểm cụm, thứ tự trong cụm): khi hai cụm cùng điểm, sắp phẳng trộn service của hai khối và khác danh sách của code.
  - Hòa giữa khối: các cụm cùng điểm là hòa ở cấp khối; chỉ hoán vị **cả khối**, giữ thứ tự trong khối. Cách tính kỳ vọng ở mục 8.4. Hòa bên trong RCD: chưa kiểm, ghi giới hạn.
- Thực thể: `<service>_A` → `<service>`.

## 7. Chế độ (b) — tự phát hiện, hồi cứu

### 7.1 Tên gọi và chuỗi đầu vào

Đây là **phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố** (Q-74 Q11). Bộ phát hiện nhận cả bản ghi 1.441 điểm, một lần, không khởi động lại, không mang trạng thái giữa ca. Lý do: Q-74 Q11 chọn cả bản ghi; cách này không phải chọn độ dài và bước đoạn; SPEC T-022 cấm chia đoạn để vừa chi phí. Giới hạn: mốc RE2-TT luôn ở giây 720, nên mọi ca có đúng 720 s nền trước lỗi; điều này đúng cho cả bản ghi lẫn mọi lịch chia đoạn theo vị trí, nên không phải lý do để chọn giữa chúng (N2). Số phát hiện chỉ nói cho cấu hình nền 720 s cố định này.

### 7.2 BOCPD

- Cột: tên chứa `latency-50` hoặc `_error`, bỏ `queue-master`, `rabbitmq_` (Q-67; `baro/reproducibility.py:139–145`). 25–48 cột thô mỗi ca (`cot-bocpd-dev.csv`).
- Tiền xử lý giữ code tác giả trên cả chuỗi: bỏ cột hằng, `ffill`, điền 0, min–max, `ffill`, điền 0 (`reproducibility.py:147–154`). Min–max và bỏ cột hằng dùng cả chuỗi: đó là look-ahead, khai báo.
- Gọi `online_changepoint_detection(data, partial(constant_hazard, 50), MultivariateT(dims=d))` như `reproducibility.py:161–166`, không sửa code.
- **Sửa lệch chỉ số (Q-74 Q11):** hàm trả cả R (`_bocpd.py:227`). Adapter tính `m[i] = argmax R[:, i+1]` với i = 0..T−1, tức run length sau khi thấy `x_i`. Điểm đổi = mọi i ≥ 1 có `|m[i] − m[i−1]| > 1` (luật `find_cps`, `baro/utility.py:208–214`). Không có phần tử thứ T, nên không còn sentinel.
- **Kiểm posterior (V2-S1):** trước `argmax`, mọi phần tử R[:, 1..T] phải hữu hạn. Không đạt → `ERROR` (mục 8.3), ghi chỉ số cột hỏng đầu tiên; không chấm điểm đổi, không chạy RCA; ca ở mẫu số, tính trượt (Q-74 Q9). Không điền 0 vào R, không cắt chuỗi tại chỗ hỏng, không sửa recurrence hay prior. Lý do: `_bocpd.py:220` chia cột cho tổng; tổng bằng 0 (mọi mật độ tràn dưới, `MultivariateT.pdf` trả mật độ chứ không phải log, `:86–108`) hoặc bằng ∞ cho cả cột NaN, và NaN lan sang mọi cột sau (`:211`); NumPy `argmax` trên cột toàn NaN trả 0, nên có thể sinh một điểm đổi giả hoặc "không báo động" giả (`results/T-013/kiem-tra.json`, check `N3-positive-mass-condition`). Điều kiện hữu hạn là đủ, không cần ngưỡng sai số: cột chia cho tổng hữu hạn dương thì hữu hạn và tổng bằng 1. Tần suất trên 30 ca dev: chưa kiểm.
- Ghi kèm điểm đổi của `maxes` gốc (có sentinel) để đối chiếu; không dùng để chấm.
- Điểm đổi ở chỉ số i ↔ `time[i]`. Do min–max toàn chuỗi, gọi là "vị trí điểm đổi hồi cứu", không gọi là thời điểm cảnh báo.

### 7.3 N-Sigma

- Cột: chính = tập cột BOCPD; đối chứng = mọi cột trừ `time` (Q-74 Q12).
- Tiền xử lý [D9]: `inf → NaN`, `ffill` (chỉ dùng quá khứ). Không min–max, không bỏ cột hằng: luật |x − mean| > 3·std không đổi dưới biến đổi affine, và cột hằng không bao giờ báo.
- Hàm `baro/anomaly_detection.py:7–35`, k = 3, `startsfrom = 100`. Mean/std chỉ dùng điểm trước i (nhân quả). Báo động gộp mọi cột, sắp thời gian, bỏ trùng.

### 7.4 Chấm phát hiện bằng báo động thô (Q-74 Q13) [D8]

- Nhãn proxy, chỉ evaluator: bất thường = [t_tiêm, cuối file], bình thường = [đầu file, t_tiêm) (README RCAEval, `hf-README.md:97`). Thời điểm lỗi thật bắt đầu, kết thúc: chưa biết.
- Báo động thô: mỗi timestamp có báo động. Không gộp episode khi chấm phát hiện.
- Cửa sổ 60 s tính từ đầu file (quy ước nhóm): cửa sổ k = [t0+60k, t0+60k+60). Cửa sổ dương nếu có ít nhất một báo động; nhãn cửa sổ dương nếu nằm trong đoạn bất thường. Không point-adjust. Vì mốc ở giây 720, biên cửa sổ trùng mốc; đây là đặc điểm RE2-TT, ghi lại.
- Cửa sổ chỉ được chấm khi mọi điểm của nó được bộ phát hiện đánh giá: N-Sigma từ chỉ số 100, BOCPD từ chỉ số 1. Cửa sổ cuối chỉ có 1 điểm (chỉ số 1.440): không chấm theo cửa sổ.
- Theo ca: ca được phát hiện nếu có ít nhất một báo động trong đoạn bất thường. Mỗi ca tối đa một sự kiện; báo động lặp là thông báo lặp.
- Báo động sai mỗi giờ: số báo động thô trong đoạn bình thường chia cho số giờ bình thường **được đánh giá** của bộ đó (N-Sigma 620 s/ca, BOCPD 719 s/ca).
- Độ trễ: báo động đầu tiên ≥ t_tiêm trừ t_tiêm. N-Sigma: "độ trễ từ lúc tiêm". BOCPD: "độ lệch vị trí điểm đổi hồi cứu so với mốc tiêm".

### 7.5 Lượt RCA và thành công chung (Q-74 Q13, Q14) [D7]

- Lượt RCA: báo động đầu tiên của ca mở lượt RCA ở t̂. Báo động trong 300 s sau đó không mở lượt mới. Báo động sau thời gian trơ mở một thông báo mới; P3 đếm số thông báo (theo ca, theo giờ bình thường) nhưng không chạy RCA ở các thông báo sau.
- Ranker ở chế độ (b): BARO, CIRCA kiến trúc, TORAI. Tên: "tích hợp P3: `<ranker>[<bộ phát hiện>]`". TORAI dùng nguồn đã làm chính theo K-B.
- Cửa sổ RCA quanh t̂: như mục 5 với t̂ thay t; cắt ở biên file, ghi độ dài thực. N quá ngắn làm phương pháp lỗi thì ghi ERROR, vẫn ở mẫu số.
- Thành công chung: báo động đầu ghép đúng sự kiện (t̂ ≥ t_tiêm) **và** RCA tại t̂ xếp root ở hạng ≤ k (theo quy tắc hòa mục 8.4). Báo động đầu sai (t̂ < t_tiêm) thì ca tính trượt.
- Thứ hạng tại báo động đầu, kể cả khi báo động sai, được lưu và báo riêng để phân tích; không cộng vào thành công chung.

## 8. Tập ứng viên và chấm

### 8.1 Bốn tập (Q-74 Q4)

| Tập | Định nghĩa |
|---|---|
| Inventory | U = 68 thực thể `ts-*` từ metadata 30 ca dev (`mappings/universe-re2tt-dev.json`): 41 `-service`, 26 DB, `ts-ui-dashboard`. `istio-init` (1 ca) ngoài U |
| Tập quan sát | thực thể có ít nhất một tín hiệu đầu vào của phương pháp trong cửa sổ, sau tiền xử lý của phương pháp |
| Tập chấm | U; cả 5 service gốc của dev thuộc U |
| Tập trả về | thực thể trong danh sách của phương pháp sau ánh xạ và bỏ trùng; thực thể ngoài U giữ chỗ, đếm riêng |

Phương pháp không có bằng chứng cho một thực thể thì không xếp thực thể đó. Không điền phần thiếu.

### 8.2 Ánh xạ về thực thể

Metric: tiền tố trước `_` đầu tiên (`main.py:560`; `.replace("-db", "")` không đổi gì trên RE2-TT vì không thực thể nào chứa `-db`). Span: `serviceName`. TORAI: `<service>_A`. Bỏ trùng giữ lần xuất hiện đầu. Điểm thực thể = khóa cao nhất của các phần tử thuộc thực thể.

### 8.3 Trạng thái (Q-74 Q9) [D12]

- `OK`: danh sách khác rỗng.
- `NO_EVIDENCE`: phương pháp trả về bình thường với danh sách rỗng (giữ status gốc: `no_anomalous_traces`, `no_normal_traces`, `missing_window`, abstain, A = 0).
- `ERROR`: phương pháp ném ngoại lệ (giữ thông điệp), hoặc đầu ra vi phạm điều kiện hợp lệ đã khai trước (posterior BOCPD không hữu hạn, mục 7.2).
- `TIMEOUT`: vượt giới hạn thời gian mỗi lượt, khai trong SPEC của task chạy (T-030 pilot, T-024, T-025) trước khi chạy; không chọn sau khi thấy thời gian chạy (N3). Ngân sách tổng (Q-40; Q-72 cho BOCPD): nếu phép chiếu từ pilot đã vượt ngân sách thì quyết trước khi chạy, như Q-67 với CIRCA-PC ("không chạy đủ trong ngân sách", không báo số); nếu đã cam kết chạy đủ cohort mà hết ngân sách giữa chừng thì ca chưa chạy là `TIMEOUT` (Q-74 Q9).
- `UNSUPPORTED`: phương pháp không nhận loại dữ liệu của ca.
- Mọi trạng thái khác `OK` ở mẫu số, tính trượt (hạng ∞).
- Lỗi dữ liệu (hash sai, file hỏng) và lỗi runner (đọc sai, cắt sai) không phải trạng thái phương pháp: sửa trước bảng khoa học, giữ lượt hỏng.
- Báo số ca theo trạng thái cạnh mỗi bảng. Số trên riêng ca `OK` chỉ là phân tích có điều kiện.

### 8.4 Hòa (Q-74 Q10)

- Hai phần tử hòa khi khóa xếp hạng thật của phương pháp bằng nhau (so đúng giá trị float/tuple):

| Phương pháp | Khóa | Cách lấy |
|---|---|---|
| BARO | max robust z | tính lại trung thành, kiểm khớp thứ tự (mục 6.1) |
| SimpleRCA | điểm service | đầu ra |
| MicroRank | điểm operation | đầu ra `scores` |
| TraceRCA | `ji` | `ji_dict` bắt lúc trả về (mục 6.4) |
| CIRCA DA / RHT-only | `(score, −index, z-score)` / `score` | đầu ra `ranks_da` / `ranks` |
| TORAI | hai cấp: khối = cụm (điểm cụm); trong khối = thứ tự RCD hoặc `y_train` | dựng lại từ biến cục bộ (mục 6.6) |

- Root thuộc nhóm hòa chiếm hạng a..b (g = b − a + 1): mọi độ đo tính kỳ vọng khi thứ tự trong nhóm ngẫu nhiên đều. E[Hit@k] = min(max(k − a + 1, 0), g)/g; E[RR] = (1/g)·Σ_{r=a..b} 1/r; E[DCG@5] = (1/g)·Σ_{r=a..min(b,5)} 1/log₂(1+r). Với các độ đo đơn điệu theo hạng root (Hit@k, MRR, NDCG@5, Avg@5, Retrieval@K), báo kèm cận lạc quan (root ở a) và bi quan (root ở b). Rerank@1 là tỉ số gộp, mẫu số đổi theo hạng nên không đơn điệu (ví dụ hai ca, K = 5: root ca 1 ở hạng 1, root ca 2 hòa hạng 5–6; giá trị chính 2/3, đặt ở hạng 5 cho 1/2, ở hạng 6 cho 1): chỉ báo giá trị chính và bootstrap, không báo cận do hòa (V2-S2).
- **TORAI (V2-R2):** không dùng quy tắc trên trực tiếp cho khóa tuple. Gọi S là tập s khối cùng điểm cụm với khối j chứa root, a là hạng đầu tiên mà S chiếm, p là vị trí root trong khối j (p chạy đều trên nhóm hòa trong khối nếu có). Hạng root = a − 1 + (tổng cỡ các khối của S đứng trước j) + p. Kỳ vọng tính chính xác bằng cách duyệt mọi tập con B ⊆ S \ {j} các khối đứng trước j, xác suất |B|!·(s − 1 − |B|)!/s!, rồi lấy trung bình theo p. Ví dụ hai khối cùng điểm AB và CD, root A: E[RR] = (1 + 1/3)/2 = 2/3, E[Hit@1] = 1/2 (không phải 25/48 và 1/4 nếu coi cả bốn service là một nhóm hòa). Cận lạc quan và bi quan lấy theo hạng nhỏ nhất và lớn nhất trong phân phối đó, chỉ cho các độ đo đơn điệu nêu trên.
- Root vắng khỏi danh sách: mọi độ đo bằng 0.

### 8.5 Bảng chính

Cùng một quy tắc hòa cho mọi độ đo: MRR, NDCG@5, Hit@1/3/5, Avg@5, Retrieval@5/10, Rerank@1 (K = 5, 10). Ở mức thực thể với một root: Hit@k = AC@k; Retrieval@K = Hit@K; Rerank@1(K) = ΣE[Hit@1] / ΣE[Hit@K] trên các ca (tỉ số gộp như RCAEval, `evaluation.py:203–210`). Đây là các cách trình bày của cùng thứ hạng, không phải bằng chứng độc lập (WHY-06). NDCG@5 với một root = 1/log₂(1+r) nếu r ≤ 5.

### 8.6 Bảng RCAEval riêng (Q-65)

`Evaluator(max_k=10)` (mặc định `max_k=5` trả `None` cho K = 10, `evaluation.py:9, 162–166`), nạp thứ tự gốc của phương pháp, bỏ trùng như `main.py:560–571`. Ca không `OK` nạp danh sách rỗng, nên ở mẫu số; khác `main.py:552–553` (bỏ ca lỗi). Báo AC@1/3/5, Avg@5, `retrieval_service(5/10)`, `rerank_service(1, 5/10)`. Bảng này không dùng để kết luận khi có hòa.

### 8.7 Mức ngẫu nhiên

Theo ca: xếp ngẫu nhiên trên tập quan sát O của phương pháp (gồm cả thực thể ngoài U nếu phương pháp có xếp): E[Hit@k] = min(k, |O|)/|O| nếu root ∈ O, bằng 0 nếu không. Báo thêm mức ngẫu nhiên trên U.

### 8.8 Bootstrap (Q-74 Q10)

- Đơn vị: 10 ô dev (root × loại lỗi), mỗi ô mang cả 3 ca. Lấy lại 10 ô có hoàn lại, B = 10.000, seed 20261005, khoảng phân vị 95 %.
- Theo cặp: khi so hai phương pháp, dùng cùng các mẫu lấy lại.
- Độ đo tỉ số (Rerank) tính lại trên từng mẫu; mẫu có Retrieval = 0 thì Rerank là N/A, đếm số mẫu N/A.
- Phương pháp nhiều seed: trung bình theo seed của từng ca trước khi bootstrap; báo khoảng giữa các seed riêng.
- Giới hạn: 10 cụm là ít; khoảng phân vị có thể hẹp hơn thực. Khoảng chỉ nói về tập ô này.

### 8.9 Cách báo

Theo loại lỗi, theo ô, theo nhóm vị trí root (`nhom_vi_tri_p75` của T-021) và từng ca; số ca theo trạng thái; bốn tập ở mục 8.1.

## 9. Seed và tham số

- Ngân sách nhãn root = 0 (Q-66): không học, không chọn cấu hình, không chọn ca bằng nhãn.
- TORAI seed {0, 1, 2} (WHY-20). MicroRank `PYTHONHASHSEED=0`, kiểm seed 1. CIRCA builder `PYTHONHASHSEED=0`, kiểm seed 1 và 2 (mục 6.5).
- Phương pháp tất định chạy một lần; kiểm lặp lại và hoán vị trên ca pilot.
- Tham số giữ mặc định tác giả: hazard 1/50; k = 3, `startsfrom = 100`; θ DA = 3; 25 vòng PageRank, d = 0,85, α = 0,01.

## 10. Bộ cột (Q-74 Q5)

- Mỗi ca dùng cột có trong file của ca, qua tiền xử lý của từng phương pháp. Không bỏ `_error`. Không điền cột vắng. Không chạy L\*.
- Schema là một kênh thông tin: số và loại cột đổi theo ca và tương quan root (T-018 D1); nó đổi số alert SimpleRCA, số chiều BOCPD, tập ứng viên BARO, đồ thị CIRCA. Ở chế độ (a), cột bị bỏ vì hằng trong cửa sổ được xác định từ dữ liệu có sẵn lúc t+300. Ở chế độ (b), tập cột BOCPD/N-Sigma lấy theo tên cột có trong file của cả bản ghi. Với BOCPD, cùng bước bỏ cột hằng và min–max trên cả bản ghi, đây là thông tin hồi cứu. Với N-Sigma, danh sách cột này không đổi báo động tới mọi thời điểm τ (V2-S3): hàm xét từng cột riêng, báo động ở i chỉ dùng giá trị trước i và tại i của cột đó (`baro/anomaly_detection.py:24–34`); tiền xử lý D9 nhân quả; cột chưa có dữ liệu trước τ cho mean/std NaN nên không báo trước τ. Vì vậy báo động tới τ giống hệt khi chỉ dùng các cột đã xuất hiện tới τ, và kết quả N-Sigma có lúc t̂+300 (mục 4). Trường hợp này có trên dữ liệu dev: trong tập cột BOCPD, 53 cột-ca bắt đầu bằng NaN, 17 cột-ca toàn NaN (đếm chỉ đọc, LOG T-022 "Phiên 5 (tiếp)"). Lập luận chỉ giữ khi T-030 cài N-Sigma đúng D9, không thêm bước dùng thống kê cả chuỗi.
- Evaluator ghi audit: số cột, danh sách cột vắng so với hợp 30 ca, cho P4 kiểm tương quan với nhãn. Không đưa dấu vắng vào phương pháp.

## 11. Kiểm đúng đắn T-030 phải cài

1. Selector từ chối: ca ngoài allowlist, đường dẫn trong `data/locked/`, path traversal, mã sai dạng, hash sai.
2. Đổi locator giữ nội dung → đầu ra giống hệt.
3. Cắt cửa sổ: fixture có span vượt biên t+300, span bắt đầu trước t−300, log và metric ở đúng biên; ô trống đầu cửa sổ (mục 5.3).
4. Evaluator, fixture biết đáp án: hạng đúng, hòa ở nhiều vị trí, danh sách ngắn, trùng thực thể, root vắng, điểm không hữu hạn, mọi trạng thái. Tính độc lập rồi đối chiếu `Evaluator` RCAEval trên danh sách không hòa.
5. Xếp hạng ngẫu nhiên: kỳ vọng Hit@k theo mục 8.7, kiểm bằng nhiều seed với sai số chuẩn.
6. Lấy khóa: BARO tính lại khớp thứ tự chính thức; TraceRCA `ji_dict` khớp danh sách chính thức khi không NaN và khớp T-015 trên ca pilot; TORAI thứ tự dựng lại khớp `ranks`; CIRCA `current` đúng điểm quan sát cuối.
7. BOCPD: fixture biết đáp án cho chỉ số `m[i]`, không sentinel, đổi chỉ số → timestamp; R có cột NaN → `ERROR` (mục 7.2); N-Sigma: warm-up, sắp và bỏ trùng.
8. Chế độ (b): đổi nhãn hoặc mốc tiêm phía evaluator không đổi báo động; bộ phát hiện không nhận tên ca, đường dẫn.
9. Hai cửa sổ đều bình thường (trong 720 s đầu): ghi điểm và trạng thái; không chỉnh ngưỡng.
10. Hoán vị dòng/cột phù hợp từng phương pháp: thứ hạng bất biến ngoài nhóm hòa.
11. MicroRank: đếm ca lỗi ở 30 ca (mục 6.3). CIRCA: K-SVR, độ nhạy builder. TORAI: K-B1–K-B3.

## 12. Chọn ca pilot (Q-74 "Thêm")

Mỗi phương pháp tối đa 3 ca: nhỏ nhất, trung vị dưới, lớn nhất theo yếu tố chi phí **sau tiền xử lý**, tính không dùng nhãn; hòa thì lấy mã mờ nhỏ hơn. Không chọn theo root, loại lỗi hay accuracy.

| Phương pháp | Yếu tố |
|---|---|
| BOCPD | số cột còn lại sau chọn cột Q-67 và bỏ cột hằng trên cả bản ghi (T = 1.441 cố định) |
| N-Sigma | như BOCPD; đối chứng: mọi cột |
| BARO | số cột còn ở cả hai nửa sau tiền xử lý |
| SimpleRCA | số cột metric, số span, số dòng log trong cửa sổ |
| MicroRank, TraceRCA | số span trong cửa sổ (sau lọc mục 5.2) và số operation |
| CIRCA | số nút và cạnh của đồ thị metric dựng từ N; cỡ tập cha lớn nhất |
| TORAI | số biến vào bước nhân quả: cột metric + `logts` + `tracets` sau cắt (A và B riêng) |

Chiếu chi phí: dựng quan hệ chi phí theo yếu tố từ các ca pilot, rồi cộng trên phân bố yếu tố của cả 30 ca; không lấy ca trung vị nhân 30. Ghi giả định và trường hợp sai; chưa chạy đủ 30 ca thì phép chiếu là "chưa kiểm". BOCPD pilot: một lượt ≤ 1 giờ trên laptop; chạm giới hạn thì chỉ báo cận dưới (SPEC T-022 bước 4). Chạy đủ ở T-025 trên EC2. Q-79 (06/10/2026) bỏ trần 20 giờ của Q-72: Minh theo dõi và dừng khi thấy quá lâu; các điều kiện khác của Q-72 giữ nguyên.

## 13. Bản ghi mỗi lượt

```json
{
  "run_id": "...", "opaque_id": "dev-…", "method": "baro", "method_version": "RCAEval 259ea41 e2e/baro.py",
  "variant": "native|svr|ols|A|B|top11|full", "mode": "a|b", "detector": null, "detector_columns": null,
  "seed": null, "hashseed": null, "config_id": "…", "why_ids": ["WHY-…"],
  "window": {"t": 0, "N": [0, 0], "A": [0, 0], "rows_N": 0, "rows_A": 0, "seconds_N": 0, "seconds_A": 0, "circa_current": null},
  "input_shape": {"metric_cols": 0, "metric_cols_after_preprocess": 0, "spans": 0, "operations": 0, "log_rows": 0},
  "status": "OK|NO_EVIDENCE|ERROR|UNSUPPORTED|TIMEOUT", "method_status_raw": null, "error": null,
  "ranking_native": ["ts-x_cpu", "…"],
  "ranking": [{"item": "ts-x_cpu", "entity": "ts-x", "key": [0.0]}],
  "entity_ranking": [{"entity": "ts-x", "key": [0.0], "tie_group": 0}],
  "sets": {"observed": 0, "returned": 0, "returned_outside_U": []},
  "diagnostics": {"fallback_clusters": null, "regression_routes": null, "key_check": "pass|fail", "rank_equals_column_order": false},
  "cost": {"wall_s": 0.0, "peak_rss_mb": null, "read_bytes": 0, "write_bytes": 0, "exit_code": 0},
  "input_sha256": {"metrics.parquet": "…"}
}
```

Không có trường nhãn. Evaluator ghi file riêng có nhãn.

## 14. Giới hạn đã biết

- RE2-TT có 5 service gốc ở vị trí cố định; đồ thị gần như hằng giữa các ca (LESSONS ST3). Không khái quát cho topology khác.
- Cửa sổ ±300 s khác ±600 s của các phép tái lập MicroRank/TraceRCA (T-007, WHY-16); số P3 không so trực tiếp với Bảng 2 bài TORAI.
- Cùng 300 + 300 s không có nghĩa cùng thông tin với `main.py --length 10`: khác thứ tự ffill, điểm cuối CIRCA, lưới TORAI A, ngưỡng `tracets_lat`.
- TORAI A: lệch lưới (đã kiểm 1/30 ca) và ngưỡng toàn file. TORAI B: dựng log khác tác giả (≤ 50,2 % ô khớp trên OB, `dung-logts-tracets.md` §4); ca `re2tt_ts-auth-service_cpu_1` không có log parquet nhưng file tác giả có 223.924 lượt log.
- Chế độ (b) chỉ là hồi cứu; 720 s bình thường mỗi ca (6 giờ cho 30 ca); BOCPD dùng min–max toàn chuỗi; nhãn proxy giả định lỗi kéo dài tới cuối file (chưa kiểm).
- Bootstrap 10 cụm; khoảng có thể hẹp hơn thực.
- Chi phí BOCPD trên 1.441 điểm với tập cột Q-67: chưa đo.

## 15. Chi tiết thực thi chưa có trong Q-74 — chờ Minh xác nhận cùng văn bản WHY

| Mã | Chi tiết | Đề xuất | Phương án khác |
|---|---|---|---|
| D1 | Thứ tự cắt/tiền xử lý | Cắt trước, tiền xử lý tác giả sau, trong cửa sổ | Giữ thứ tự `main.py` (ffill toàn file): dùng giá trị trước t−300 |
| D2 | Span vào cửa sổ | `startTime ≥ t−300` và kết thúc `< t+300` | Chỉ đòi kết thúc trong cửa sổ (nhận span bắt đầu trước t−300) |
| D3 | CIRCA | `current` = điểm quan sát cuối < t+300; đồ thị từ span kết thúc `< t` | Đồ thị từ span bắt đầu trong N (có span kéo sang A) |
| D4 | Phép kiểm K-B cho TORAI B | K-B1 (≥ 95 % ô theo tên cột, luật tên cột TT ở mục 6.6, cột không ghép tính sai), K-B2, K-B3 như mục 6.6 (sửa sau V2-R1, N1) | Ngưỡng khác; gộp về ô (service, bin) (bản trước; không kiểm được đặc trưng TORAI dùng, REVIEW V2-R1) |
| D5 | Phép kiểm K-SVR cho CIRCA | K-SVR1–4 như mục 6.5; K-SVR2 tính route từng nút, nút có cha rơi `value_error_fallback` là không đạt; ghi route cho mô hình được khóa, cả OLS (sửa sau V2-T1) | Thêm phép kiểm hai cửa sổ bình thường (cần chọn ngưỡng z, chưa có căn cứ); K-SVR2 chỉ xét lỗi ném ra và z hữu hạn (bản trước; không phân biệt SVR chạy được với z-score dự phòng, REVIEW V2-T1) |
| D6 | "Nhiều" ca MicroRank lỗi | Báo Minh số ca lỗi trong mọi trường hợp; dừng chờ Minh nếu ≥ 1 ca | Ngưỡng 3 ca (một ô) |
| D7 | Lượt RCA chế độ (b) | Chỉ RCA ở báo động đầu; thông báo sau chỉ đếm | RCA ở mọi thông báo; thành công = thông báo ghép đúng đầu tiên |
| D8 | Cửa sổ chấm phát hiện | Chỉ chấm cửa sổ mà mọi điểm được bộ phát hiện đánh giá; bỏ cửa sổ cuối 1 điểm | Chấm mọi cửa sổ, coi điểm chưa đánh giá là âm |
| D9 | Tiền xử lý N-Sigma | `inf → NaN`, `ffill`; không min–max | Min–max như runner T-006 (dùng tương lai) |
| D10 | Lấy khóa BARO, TORAI | Tính lại trung thành (BARO); TORAI khóa hai cấp (khối cụm, thứ tự trong khối), hòa giữa khối chỉ hoán vị cả khối (mục 6.6, 8.4; sửa sau V2-R2); kiểm khớp thứ tự chính thức | Coi như không hòa (giữ thứ tự cột làm bằng chứng); TORAI: coi mọi service của các cụm cùng điểm là một nhóm hòa (bản trước) |
| D11 | Đọc `ji_dict` TraceRCA | `sys.setprofile` lúc trả về | Cài lại công thức (cầu nối), đối chiếu T-015 |
| D12 | Ánh xạ trạng thái | Trả về rỗng → NO_EVIDENCE (giữ status gốc); ném lỗi hoặc posterior BOCPD không hữu hạn (V2-S1) → ERROR | Mọi trạng thái rỗng tính ERROR |
