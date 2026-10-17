# T-032 — Thiết kế các phép đổi tất định (bản 001)

Viết ngày 11/10/2026, trước khi chạy bất kỳ phép đổi nào trong file này. Người viết: Claude (người làm T-032).

## 1. Căn cứ và phạm vi

- **Quyền:** lời Minh trong chat khuya 10/10/2026: "những phần đề xuất duyệt thuật toán thì tôi cần bạn vạch ra chính xác nhất từ đầu luôn rồi triển khai luôn, không cần chờ tôi duyệt". A′ đã có trong SPEC (Q-92, Q-93, Q-119).
- **Nguồn yêu cầu:** MRP P4 ("trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z"); SPEC T-032, bảng câu hỏi dòng 2: cần can thiệp để phân xử thì nêu nhóm ca, thành phần giữ/đổi, dự đoán đối lập, chi phí.
- **Vì sao cần phép đổi:** bảng trung gian và đối chứng chỉ cho biết chênh lệch xuất hiện ở bước nào. Muốn nói "bước Y làm đổi hạng" thì phải đổi đúng bước đó, giữ phần còn lại, và xem hạng có đổi không.
- **Không phải:** đánh giá phương pháp mới; thay số P3; chọn cấu hình theo accuracy; định nghĩa nhãn lan; bằng chứng nguyên nhân vật lý.

## 2. Điều tôi đã thấy trước khi viết (để người đọc biết thiết kế có thể bị ảnh hưởng)

- Một ca MicroRank Nezha `dev-14701a3bbb`: số own/context và điểm của mọi operation (LOG phiên 9).
- Phần đọc BARO của Codex: hai ca `travel|loss`, gồm việc cột `ts-travel-service_error` bị lọc.
- Chưa thấy kết quả của bất kỳ phép đổi nào dưới đây. Chưa thấy trung gian TraceRCA, CIRCA, TORAI.

## 3. Quy tắc chung cho mọi phép đổi

1. **Một bước.** Mỗi phép đổi đúng một bước của chuỗi tính; mọi bước khác dùng code hoặc công thức native.
2. **Không dùng nhãn trong định nghĩa.** Phép đổi áp cho mọi thực thể theo một quy tắc cấu trúc. Nhãn root chỉ nối sau khi đã tính xong cho mọi ca.
3. **J0 và sham.** Đầu vào là trung gian của lượt phát lại đã khớp tuyệt đối với bản đóng băng (J0). Trước khi diễn giải, nhánh "không đổi gì" (sham) phải tái lập điểm và thứ tự native từng bit. Sham lệch thì phép đổi đó vô hiệu.
4. **Toàn bộ ca.** Tính cho mọi ca OK của phương pháp, cả ca đúng lẫn ca sai, không chỉ ca có cờ M5. Ca ERROR/UNSUPPORTED giữ trong mẫu số với trạng thái N/A.
5. **Chỉ số khai trước.** Với mỗi ca và mỗi nhánh:
   - hạng root (rank_min, rank_max theo quy tắc hòa của giao thức P3);
   - tập thực thể đứng trên root;
   - với từng thực thể e: margin m_e = (s_e − s_root) / (|s_e| + |s_root|), mẫu số 0 thì N/A;
   - Δ = m_e(native) − m_e(nhánh đổi).
   Hit@1 và Hit@5 chỉ là chỉ số phụ.
6. **Cách đọc.** Margin native > 0 và nhánh đổi ≤ 0: bước đó tạo ưu thế của e so với root trong ca này. Cả hai > 0: bước đó không đủ để giải thích. Báo cả ca đúng bị hỏng đi dưới nhánh đổi. Không gọi "nguyên nhân chủ yếu". Không cộng các phép đổi thành tỷ lệ.
7. **Giữ mọi lượt.** Kết quả ở thư mục lượt mới, không ghi đè lõi. Lượt lỗi giữ nguyên.

## 4. MicroRank (biến thể "MicroRank-RCAEval sửa đầu vào", WHY-31)

Chuỗi tính và nơi trong code:

1. Cờ span: `duration/1000 >= mean + 3*std` theo từng operation; mean, std lấy từ đoạn nền N, làm tròn 2 chữ số (`src/microrank/__init__.py`, dòng tính `stats` và `after['abnormal']`).
2. Chia trace: trace vào nhóm A nếu có ít nhất một span mang cờ; còn lại vào nhóm N của cửa sổ sau mốc.
3. Đồ thị và độ phủ từng nhóm (`src/microrank/graph.py`): `operation_trace` là trace → operation, `trace_operation` là operation → trace.
4. PageRank cho từng nhóm → trọng số operation (`official.trace_pagerank`).
5. Spectrum DStar2 (`official.calculate_spectrum_without_delay_list`): ef = w_A·cov_A, nf = w_A·(|A| − cov_A), ep = w_N·cov_N; điểm = ef² / (ep + nf).
6. Điểm service = điểm operation cao nhất của service (adapter P3).

Lưu ý phân loại: bước 1–2 là bộ chia trace của bản RCAEval. Bài MicroRank gốc chia theo thời lượng kỳ vọng của cả trace (`src/microrank/detectors.py`). Hạn chế tìm thấy ở bước 1–2 phải ghi là của biến thể, không gán cho bài gốc.

### M-A′ — trọng số đơn vị (đã có trong SPEC)

Đổi bước 4: mọi operation có trong từ điển trọng số của một nhóm nhận trọng số 1. Thực hiện đúng mục A′ của SPEC, không thêm bớt.

### M-C1 — đếm riêng thay cho đếm phủ

- **Đổi (bước 5, đầu vào):** số đếm nhóm A của operation o, từ cov_A(o) = số trace trong A có chứa o, thành own_A(o) = số trace trong A mà chính o có ít nhất một span mang cờ.
- **Giữ:** cờ span, phân hoạch A/N, |A|, |N|, cov_N, trọng số native của J0, công thức DStar2, nhánh thiếu nhóm, phép max service.
- **Trường hợp biên:** own_A(o) = 0 thì ef = 0, điểm 0; không thêm operation vắng mặt.
- **Dự đoán đối lập:**
  - H-ngữ-cảnh: thực thể e đứng trên root nhờ operation chỉ có mặt trong trace bất thường của operation khác. Khi đó margin của e đổi dấu dưới M-C1.
  - H-riêng: e tự có nhiều trace mang cờ hơn root. Khi đó margin vẫn dương.
- **Không phân xử:** vì sao span của e mang cờ (chờ, xử lý tại chỗ, mạng). Phần đó thuộc M-D và phần ngữ nghĩa trace.

### M-D — cờ theo thời lượng chưa được span con phủ

- **Đại lượng mới:** với mỗi span p, u(p) = duration(p) − độ dài hợp các khoảng [start, end] của span con trực tiếp, sau khi cắt mỗi khoảng con vào khoảng của p. Con được tìm trong cùng trace, trên toàn bộ span của cửa sổ ngoài mà phương pháp nhận.
- **Đổi (bước 1):** dùng u thay cho duration ở cả thống kê nền (mean, std theo operation, vẫn làm tròn 2 chữ số) và ở cờ span sau mốc.
- **Giữ:** span nào thuộc trước/sau mốc vẫn tính theo thời điểm kết thúc gốc; ngưỡng 3·std; các bước 2–6 chạy lại bằng đúng code native trên phân hoạch mới.
- **Dự đoán đối lập:**
  - H-con: span của caller vượt ngưỡng vì khoảng con dài ra. Khi đó số cờ của caller giảm mạnh, margin caller so với root giảm hoặc đổi dấu.
  - H-phần-chưa-phủ: phần của caller không được con phủ tự dài ra (xử lý tại caller, thời gian giữa span phía gọi và span phía được gọi, con không được ghi). Khi đó caller vẫn đứng trên root.
- **Vì sao không hiển nhiên:** với lỗi mạng hoặc lỗi nằm giữa hai dịch vụ, tín hiệu chỉ có ở span phía gọi, nên H-phần-chưa-phủ có thật. Hai kết cục dẫn tới hai hướng thiết kế khác nhau: gắn tín hiệu vào nút hay vào cạnh.
- **Giới hạn:** u không phải thời gian tự xử lý và không chứng minh chờ đồng bộ. Con chạy song song được tính theo hợp khoảng. Con vượt ra ngoài cha bị cắt. Span không tìm được cha hoặc có con nằm ngoài cửa sổ được đếm và báo riêng. Phép này đổi phân hoạch nên kết quả là tác động tổng của việc đổi đại lượng cờ, không tách riêng PageRank.
- **Nơi chạy:** bước 4 dùng numpy float32 và BLAS, chỉ laptop tái lập được native từng bit. M-D vì vậy chạy trên laptop, sau khi sham đạt.
- **Kiểm phép tính khoảng (SPEC, mục kiểm đúng đắn):** thử trên các trường hợp tự dựng: lồng nhau, song song chồng lấn, con vượt cha, thiếu cha, span chạm biên cửa sổ.

## 5. TraceRCA (RCAEval `e2e/tracerca.py`, bản lọc hữu hạn, WHY-32)

Chuỗi tính: cờ span như MicroRank bước 1 (`tracerca.py`, đoạn "TRACE ANOMALY DETECTION"); với mỗi operation: a = số span mang cờ, n = số span sau mốc, H = tổng span mang cờ; support s = a/H; confidence c = a/n; ji = 2sc/(s + c); bỏ ji không hữu hạn; điểm service = ji cao nhất.

- **Phân rã (không phải can thiệp):** ji = 2a/(n + H) khi a > 0. Đẳng thức này phải được kiểm bằng số trên J0 trước khi dùng. Bảng lõi ghi a, n, H cho mọi operation.
- **TraceRCA không đếm ngữ cảnh:** điểm chỉ dùng span mang cờ của chính operation. Vì vậy không có phép tương ứng M-C1.

### T-D — cờ theo thời lượng chưa được span con phủ

Cùng định nghĩa u và cùng quy tắc như M-D. Tính lại a, H, ji bằng bản sao công thức. Sham: với duration gốc, bản sao phải tái lập ji native từng bit. Dự đoán như M-D. TraceRCA là nơi phép này sạch nhất vì không có bước nào khác chen giữa cờ và điểm.

## 6. BARO (RCAEval `e2e/baro.py`)

Chuỗi tính: tiền xử lý chung của adapter → `preprocess` riêng cho N và cho A: `drop_time`, `drop_constant`, đổi đơn vị mem (`io/time_series.py`) → lấy giao tập cột (`baro.py`, đoạn "intersect") → `RobustScaler` khớp trên N (median, IQR) → z của A, lấy max theo cột → xếp cột; điểm service = cột cao nhất (adapter P3).

### B-1 — không lọc cột hằng

- **Đổi:** bỏ `drop_constant` ở cả N và A.
- **Giữ:** `drop_time`, đổi đơn vị mem, phép giao, `RobustScaler`, max theo cột, max theo service.
- **Hành vi thư viện đã đọc:** scikit-learn 1.6.0, `RobustScaler` gọi `_handle_zeros_in_scale`, đặt scale = 1 khi IQR bằng 0 (`sklearn/preprocessing/_data.py`). Cột hằng ở N cho z = x − median, đơn vị thô. Cột hằng ở cả N và A cho z = 0.
- **Dự đoán đối lập:**
  - H-lọc: root có cột hằng ở N và đổi ở A (ví dụ tỷ lệ lỗi từ 0 lên dương), bước lọc làm mất cột đó. Khi đó root tăng hạng dưới B-1 ở các ca như vậy.
  - H-khác: hạng root không đổi.
- **Phải báo kèm:** số ca đúng bị hỏng đi dưới B-1, vì z thô không cùng thang với z chuẩn hóa.
- **Giới hạn:** B-1 chỉ trả lời "cột bị lọc có mang tín hiệu đủ đổi hạng dưới chính quy tắc scale của thư viện không". Nó không đề xuất cách chuẩn hóa cho cột hằng.
- **Bảng mô tả đi kèm (không can thiệp):** với mỗi ca, các cột của root bị bỏ ở N, ở A, hoặc mất do phép giao, cùng giá trị của chúng.

## 7. SimpleRCA (M4, `src/simplerca/core.py`)

Điểm = số phiếu metric + phiếu trace + phiếu log. Phiếu metric của một cột là số mẫu sau mốc vượt mean + 3·std của nền; phiếu trace và log là 0 hoặc 1.

- **Không cần phép đổi.** Phép cộng cho phân rã chính xác: chênh giữa hai service bằng tổng chênh từng kênh, và trong kênh metric bằng tổng chênh từng cột. Bảng lõi ghi phiếu theo từng cột, số cột metric của mỗi service, phiếu trace, phiếu log.
- Cấu hình `metric_aggregation='channels'` là một lựa chọn độ nhạy có sẵn trong `Config`, không dùng để phân xử cơ chế ở đây.

## 8. CIRCA (chỉ RE2-TT; Nezha UNSUPPORTED)

Chuỗi tính: tiền xử lý → đồ thị metric dựng từ lời gọi trong đoạn nền → hồi quy OLS từng nút theo các nút cha → điểm RHT (z của phần dư) → điều chỉnh theo hậu duệ DA (θ = 3) → khóa xếp hạng (`src/circa_kien_truc/scoring.py`, `src/p3/adapters/circa.py`).

### K-1 — có và không có bước DA (không chạy gì mới)

Bản ghi `ols+rht` và `ols+rht_da` của cùng một ca đã đóng băng trong T-024, sinh từ cùng một lượt chấm. So hai bản ghi cho biết tác dụng của bước DA lên hạng root và từng thực thể. Bản đóng băng cũng lưu cho từng nút: điểm RHT, đường hồi quy, danh sách cha.

### K-2 — chấm RHT với đồ thị không cạnh

- **Đổi:** truyền cho `score_graph` cùng tập nút nhưng không có cạnh. Mọi nút đi đường `no_effective_parents`.
- **Giữ:** frame, cửa sổ train/test, `current`, cách chuẩn hóa phần dư, cách xếp.
- **Dự đoán đối lập:**
  - H-giải-thích: hồi quy theo cha làm giảm điểm của nút bị cha giải thích. Khi đó điểm native của caller thấp hơn điểm không cạnh.
  - H-không-dùng: điểm bằng nhau; cấu trúc không thực sự tác động vào nút đó.
- **Điều kiện:** cần lõi CIRCA phát lại khớp tuyệt đối (sham tái lập `ols+rht` từng bit). Lõi CIRCA chưa có, nên K-2 chờ lõi. Bản đóng băng CIRCA sinh trên laptop; nếu EC2 không tái lập từng bit thì cần Minh quyết nơi chạy.
- Lỗi làm tròn của CIRCA giữ nguyên theo Q-82; các ca có nút vượt 1e10 báo riêng.

## 9. TORAI B (chỉ RE2-TT, ba seed)

Chưa định phép đổi. Lý do: chưa có trung gian (severity, cụm, nhánh RCD hay nhánh dự phòng theo từng seed) và tôi chưa đọc `src/torai`. Việc phải làm trước: wrapper lõi, rồi bảng phân rã theo nhánh và theo seed. Chỉ có một đơn vị M5 ở TORAI B, nên phép đổi nếu có sẽ nhắm vào nhóm ca sai khác. Mục này sẽ được viết thành bản 002 của file, trước khi chạy.

## 10. Thứ tự và chi phí

| Phép | Cần trước | Nơi chạy | Chi phí máy ước lượng (chưa đo) |
|---|---|---|---|
| T-D | 52 ca TraceRCA khớp | EC2 | dưới 30 phút |
| B-1 | kiểm lại 52 ca BARO | EC2 | dưới 20 phút |
| K-1 | không | EC2, đọc bản đóng băng | vài phút |
| M-A′, M-C1 | 52 ca MicroRank khớp | số học trên trung gian đã lưu | vài phút |
| M-D | 52 ca MicroRank khớp, sham đạt | laptop | dưới 30 phút |
| K-2 | lõi CIRCA | chờ quyết nơi chạy | chưa ước |

## 11. Nháp đoạn WHY (chưa nối vào `docs/WHY.md`; cần Minh cho phép nối trước khi kết quả vào báo cáo)

**Chọn:** ngoài A′, thêm các phép đổi tất định M-C1, M-D, T-D, B-1, K-1, K-2 như trên; SimpleRCA dùng phân rã cộng, không can thiệp; TORAI B định sau khi có trung gian.

**Vì sao:** P4 đòi chỉ ra bước làm mất hoặc đánh giá sai thông tin. Quan sát chênh lệch ở một bước chưa cho biết bước đó có làm đổi hạng hay không. Đổi đúng một bước trên trung gian đã khớp, với dự đoán ghi trước, phân biệt được hai giải thích dẫn tới hai hướng thiết kế khác nhau.

**Phương án đã xét:** chỉ đọc bảng và đối chứng (không phân biệt được "nơi chênh xuất hiện" với "bước gây đổi hạng"); hạ duration hoặc xóa caller theo nhãn (dùng nhãn, kết quả hiển nhiên; WHY-40 đã bác); đổi nhiều bước cùng lúc (không quy được cho bước nào); chạy lại bộ chia trace của bài MicroRank gốc (cần quyết định adapter về thời lượng của cả trace, để riêng).

**Bằng chứng:** code ở các file đã dẫn; chưa có kết quả. Đây là kế hoạch kiểm, không phải xác nhận giả thuyết.

**Kết luận phụ thuộc:** phần "hạn chế thuộc giả định/cách tính" của bản đồ P4 và căn cứ đề xuất ứng viên P5–P6. Nguyên nhân vật lý và lợi ích của đồ thị vẫn cần bằng chứng riêng.
