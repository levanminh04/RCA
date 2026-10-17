# T-032 — Thiết kế bản 013: các phép kiểm còn lại (KT-1, KT-2, KT-12, KT-8 nửa TraceRCA, bảng nối cho nhánh ghép MicroRank, KT-9)

Người làm: Claude, phiên 13, 11/10/2026. File này viết **trước khi chạy** lượt nào của sáu phép dưới đây.

**Căn cứ.** Hai lời Minh trong chat ngày 11/10/2026, ghi nguyên văn ở LOG, mục "Phiên 12 (tiếp) — Minh duyệt chạy hết; prompt cho phiên 13": "DUYỆT TOÀN BỘ PHÉP THỬ TRÊN EC2 / DUYỆT KT-9 CHẠY TRÊN LAPTOP / DUYỆT CHẠY HẾT / … / DUYỆT ĐỌC TAY HẾT / …". Mô tả ban đầu của từng phép: `kiem-tiep.md`.

**Điều kiện chung.** Không sửa file nào trong `src/`, dữ liệu, môi trường, số đã chấm. EC2 chỉ ghi trong `~/rca/T-032/`. Mỗi phép có nhánh giữ nguyên hoặc tự kiểm với nguồn đã có; lệch thì dừng riêng phép đó. Giữ mọi lượt kể cả hỏng. Mọi đại lượng tính cho mọi thực thể trước, nhãn root nối sau cùng. Số của nhánh phép đổi đo tác động của một bước tính trên dev, không phải thành tích của một phương pháp. Các mốc đọc dưới đây do người làm đặt trước khi chạy; không mốc nào là ngưỡng của phương pháp.

**Điều tôi đã thấy trước khi viết file này.** Toàn bộ kết quả phiên 9–12 (các file `ket-qua-phien-*.md`). Riêng từng phép ghi ở mục "đã thấy trước" của phép đó. Trong phiên 13, trước khi viết, tôi chỉ đọc mã (các script cũ, `src/circa_kien_truc/scoring.py`, `src/p3/adapters/*.py`, `RCAEval/classes/data.py`, `RCAEval/graph_heads/rht.py`, `RCAEval/e2e/tracerca.py`) và danh sách file; chưa mở số của lượt nào mới.

## 1. KT-1 và KT-2 — mốc giả trên bảng span RE2-TT

**Câu hỏi.** KT-1: vì sao khoảng một nửa trace sau mốc bị xếp bất thường dù phần lớn không gắn với root. KT-2: thao tác đông span có 2–9% span mang cờ là mức tự nhiên hay do sự cố.

**Nguồn.** Bảng span adapter đã lưu của 26 ca RE2-TT có lượt phát lại TraceRCA khớp từng bit (như bảng A). Bốn ca nguồn ERROR không có bảng đã lưu, ghi N/A. Nezha-OB không làm: đoạn nền chỉ 41–97 giây. Không gọi phương pháp. Script `scripts/fake_marker_v1.py`, chạy trên EC2.

**Bước bị đổi: chỉ vị trí và độ dài hai cửa sổ.** Luật cờ (thời lượng ≥ mean + 3·std của thao tác ở đoạn nền, biểu thức của bản thư viện), cách gộp thao tác, luật "trace bất thường khi có ít nhất một span mang cờ" giữ nguyên. Span thuộc cửa sổ nào tính theo thời điểm kết thúc, như bản thư viện.

| Tên | Đoạn nền | Đoạn xét | Vai trò |
|---|---|---|---|
| `real300` | [t−300, t) | [t, t+300) | Giữ nguyên. Tự kiểm: tổng cờ bằng H_native; số trace bất thường và bình thường bằng số của lượt `chain-spanpass-001` |
| `real150` | [t−150, t) | [t, t+150) | Mốc thật, hai cửa sổ 150 giây |
| `fake150` | [t−300, t−150) | [t−150, t) | Mốc giả, hai cửa sổ 150 giây; không có lỗi nào được tiêm trong đoạn xét |
| `real100` | [t−100, t) | [t, t+100) | Mốc thật, hai cửa sổ 100 giây |
| `fake100a` | [t−300, t−200) | [t−200, t−100) | Mốc giả thứ nhất, 100 giây |
| `fake100b` | [t−200, t−100) | [t−100, t) | Mốc giả thứ hai, 100 giây |

**Sửa so với chữ của `kiem-tiep.md`.** Mục KT-1 ghi "giữ cố định độ dài cửa sổ nền". Điều đó không làm được với mốc giả: dữ liệu trước mốc chỉ có 300 giây. Vì vậy mốc giả được so với mốc thật **cùng độ dài cửa sổ** (`real150`, `real100`), không so với `real300`.

**Đại lượng (mỗi cấu hình, mỗi ca).** Số trace trong đoạn xét; số trace bất thường; với mỗi thao tác: n (span có nền), a (span mang cờ). Tỷ lệ trace bất thường dự đoán nếu các span vượt ngưỡng độc lập nhau: trung bình trên trace của 1 − Π(1 − a_o/n_o) lấy trên mọi span của trace; tính với tỷ lệ a_o/n_o của chính cấu hình, và cho `real150` tính thêm với tỷ lệ của `fake150` (tức "nếu sau mốc thật các thao tác chỉ vượt ngưỡng như lúc không có lỗi"). Sau khi nối nhãn: tách trace có và không có span của root; tách thao tác theo vị trí của dịch vụ so với root (đồ thị gọi của lượt `chain-spanpass-001`).

**Ba giải thích của KT-1 và mốc đọc** (tính trên trung vị qua các ca; R = tỷ lệ trace bất thường trong các trace **không** có span của root ở `real150`; F = tỷ lệ trace bất thường ở `fake150`):

- (a) thuần xác suất, không cần sự cố: F ≥ 0,8·R, và tỷ lệ dự đoán theo độc lập ở `fake150` nằm trong ±20% tỷ lệ thật của `fake150`.
- (b) sự cố làm nhiều trace không qua root vượt ngưỡng: F ≤ 0,5·R.
- (c) đoạn nền không đại diện: tỷ lệ ở mốc giả đã cao (trung vị từ 20%) **và** đổi theo vị trí mốc: |`fake100a` − `fake100b`| lớn hơn 0,5 lần giá trị lớn hơn ở từ nửa số ca.
- Nằm giữa các mốc: ghi "không phân xử rõ", kèm số. (a) và (c) có thể cùng đạt; (b) loại trừ (a).

**Hai giải thích của KT-2 và mốc đọc** (thao tác "đông span": n ≥ 200 ở đoạn xét của cả `fake150` và `real150`; không phải thao tác của root):

- (a) mức tự nhiên: ở `fake150`, từ nửa số thao tác đông span có a/n ≥ 2%.
- (b) do sự cố: ở `fake150`, từ 3/4 số thao tác đông span có a/n < 1%, và trung vị a/n ở `real150` gấp từ 2 lần trung vị ở `fake150`.
- Ngoài ra in riêng: thao tác cao nhất của các thực thể không liên hệ đứng trên root trong bản ghi TraceRCA đã chấm (danh sách từ `runs/slow-call-flag-link-001/cases.json`), với a/n ở `real300` (phải bằng số đã lưu), `real150`, `fake150`.

**Mẫu số.** 26 ca; ca thiếu trace ở một cửa sổ ghi riêng. Đếm thao tác gộp qua các ca và theo ca.

**Đã thấy trước.** Tỷ lệ trace bất thường trung vị 50% ở RE2-TT (KQ9 mục 2); 504/755 trace bất thường không qua root ở một ca; a/n 2–9% ở hai ca đã đọc. Phiên 10 đã chạy phép thử giả của bảng A (`runs/root-signal-placebo-002`, `-003`), có lưu tổng số cờ dưới mốc giả; trong phiên này tôi chưa mở lại các số đó, nhưng phiên 10 đã thấy root không đứng đầu thường xuyên hơn ngẫu nhiên dưới mốc giả. Chưa ai tính tỷ lệ trace bất thường hay a/n theo thao tác dưới mốc giả.

**Giới hạn.** Cửa sổ 100–150 giây ngắn hơn giao thức, độ lệch chuẩn ước kém hơn; kết luận là về cơ chế tạo cờ, không phải về số đã chấm. Phép độc lập giữa các span là giả định để so, không phải mô hình của dữ liệu. Chỉ RE2-TT.

## 2. KT-12 — cột độ trễ của root phản ứng ở ca này, không ở ca kia cùng ô

**Câu hỏi.** Ba cặp ca cùng ô (`doc-tay.md` mục 3.1, 3.4, 4.3): `ts-auth-service`, lỗi delay (`dev-746fd74313` so với `dev-57546fd87b`; ca thứ ba cùng ô `dev-f81f88234e` in kèm); `recommendationservice`, network_delay (`dev-5467884de4` so với `dev-63c30faf34`); `checkoutservice`, network_delay (`dev-2bfc97b01e` so với `dev-607751ac0a`). Vì sao cột độ trễ của root phản ứng ở ca này mà không ở ca kia?

**Không đổi bước tính nào.** Bảy tiến trình con trên EC2, mỗi ca một tiến trình, chạy đúng đường phát lại BARO native với một lớp bọc chỉ-đọc quanh hàm adapter để lưu bảng metric mà phương pháp nhận. **Tự kiểm:** bản ghi của mỗi tiến trình phải khớp bản đóng băng BARO từng bit; lệch thì không dùng ca đó. Script `scripts/root_latency_series_v1.py`.

**Đại lượng.** Với mỗi cột của root và của các dịch vụ gọi trực tiếp root (theo đồ thị `chain-spanpass-001`): số mẫu ở đoạn nền và đoạn sau; số mẫu thiếu; số giá trị khác nhau; số mẫu khác 0; trung vị và độ lệch chuẩn nền; trung vị, lớn nhất sau mốc; z kiểu BARO (trung vị, IQR); số mẫu sau mốc vượt mean + 3·std; giây đầu tiên vượt. In nguyên chuỗi của các cột độ trễ của root. Đối chiếu với bảng lời gọi chậm đã có (`runs/call-slow-001`): số lời gọi tới root trước và sau mốc, tỷ lệ lời gọi chậm, phần nằm trong span của root.

**Ba giải thích và mốc đọc, theo từng cặp** ("ca phản ứng" là ca có z của cột độ trễ của root lớn hơn):

- (b) ít mẫu: ở ca không phản ứng, số mẫu khác 0 hoặc số giá trị khác nhau của cột độ trễ của root ở đoạn sau dưới một nửa ca phản ứng.
- (c) cường độ khác nhau: tỷ lệ lời gọi chậm tới root ở ca không phản ứng dưới một nửa ca phản ứng.
- (a) cột đo sai chỗ (đo phía được gọi, lỗi nằm trước đó): tỷ lệ lời gọi chậm và số mẫu của hai ca tương đương (trong 1,5 lần), phần chậm nằm trong span của root dưới 20% ở cả hai, mà cột của root vẫn phản ứng ở một ca. Khi đó phần "vì sao một ca phản ứng" **vẫn chưa giải thích**; ghi OPEN, không chọn nguyên nhân.
- Mỗi cặp đọc riêng; ba cặp không cộng thành tỷ lệ.

**Đã thấy trước.** Các số z và số phiếu trong `doc-tay.md`; ở cặp checkoutservice tỷ lệ lời gọi chậm 9% so với 26% (đã ghi trong KT-12). Vậy với cặp đó mốc (c) đã biết trước là đạt; hai cặp kia chưa xem.

**Giới hạn.** Ba cặp, bảy ca; mô tả, không phải phép đổi. Không có metric phía mạng nên (a) chỉ suy được gián tiếp.

## 3. KT-8, nửa TraceRCA — bốn ca ERROR khi bỏ thao tác không có ở đoạn nền

**Câu hỏi.** Ở 4 ca RE2-TT mà TraceRCA dừng vì thao tác sau mốc không có ở đoạn nền, nếu bỏ span của thao tác đó thì root xếp thứ mấy?

**Bước bị đổi (đổi đầu vào, không phải đổi bước tính).** Trước khi gọi hàm adapter `p3.adapters.tracerca.chay` nguyên trạng: bỏ khỏi bảng span các span kết thúc từ mốc trở đi thuộc thao tác không có span nào kết thúc trước mốc. Mọi bước sau là mã native. Chạy trên EC2 (nơi TraceRCA phát lại khớp từng bit 52/52). Script `scripts/tracerca_dropnew_v1.py`.

**Tự kiểm.** Ở 48 ca không có thao tác mới, không span nào bị bỏ; thứ hạng theo thực thể phải trùng bản ghi đóng băng ở 48/48 ca (so hạng tốt nhất, hạng xấu nhất của mọi thực thể). Lệch thì không dùng kết quả 4 ca.

**Không có dự đoán về hạng.** Ghi: số span và trace bị ảnh hưởng, trạng thái, hạng root, thực thể đứng đầu, số thực thể trên root. Kết quả chỉ trả lời câu "4 ca này ghi là phương pháp trượt hay không chạy được vì đầu vào"; không thay số đã chấm.

**Đã thấy trước.** Nửa MicroRank: root hạng 2, 2, 3, 12; `ts-station-service` đứng đầu 4/4. Chưa tính điểm TraceRCA cho 4 ca này.

## 4. Bảng nối theo cây span cho nhánh ghép của MicroRank (`mo15c1`, `mo1p50c1`)

**Câu hỏi.** Ở các ca root chưa hạng 1 dưới nhánh ghép, thao tác cao nhất của thực thể đứng đầu có gắn với root trong cây span không? Riêng Nezha-OB: `frontend` đứng đầu ở 14/16 và 11/14 ca còn sai.

**Không chạy phương pháp.** Thứ hạng và thao tác cao nhất lấy từ bản ghi của lượt laptop `runs/microrank-kt3-001` (chép sang EC2 dạng rút gọn, kiểm hash hai đầu). Trên EC2 dựng lại hai tập trace của nhánh ghép từ bảng span đã lưu theo đúng luật ở hàm móc của `laptop_contrast_v7.py` (span đầu, mức nền như code gốc, hai luật gọi nguyên hàm của `src/microrank/detectors.py`). Script `scripts/microrank_merged_link_v1.py`.

**Tự kiểm trước khi dùng (theo ca và luật).** Số trace sau mốc, số trace bất thường mới, số trace bất thường mới cũng bất thường theo native, và bảng số trace bất thường theo dịch vụ phải trùng số lưu ở `check.json → /info/calls/0` của lượt laptop. Ca nào lệch: không dùng, ghi riêng. Phần cây span dùng lại hàm `subtree` của `chain_spanpass_v1.py` (đã có 13 trường hợp tự dựng) và thêm trường hợp tự dựng cho "lời gọi trực tiếp".

**Đại lượng.** Cho mỗi ca, mỗi luật, mỗi thực thể E đứng đầu (hạng tốt nhất bằng 1) khi root chưa hạng 1, với O là thao tác cao nhất của E. Tập F = các span mang cờ của O nằm trong trace bất thường mới (đúng các span tạo ra số đếm riêng của O). Trên F, với root R:

- `direct`: span có span con trực tiếp thuộc R (chính nó là span phía gọi của lời gọi tới R);
- `below`: có span của R nằm dưới trong cây;
- `slow`: bao một lời gọi chậm tới R (định nghĩa của bảng C2; chỉ khi cạnh tới R đủ 20 lời gọi mỗi phía);
- `flag_below`: có span mang cờ của R nằm dưới;
- `linked` = `slow` hoặc `flag_below`.

Cùng các tỷ lệ đó trên các span **không** mang cờ của O ở đoạn sau mốc (mức nền của O), và giá trị lớn nhất của `linked` đối với một dịch vụ khác không phải R và không nằm phía trên R (độ đặc hiệu). Mức trace: trong các trace bất thường mới mà O có span mang cờ, tỷ lệ có span của R, có span mang cờ của R.

**Mốc đọc theo ca.** "Gắn với root": `linked` trên F từ 50% **và** lớn hơn giá trị của dịch vụ khác tốt nhất. "Không gắn": `linked` dưới 20%. Còn lại: "không rõ". Ca mà cạnh tới R không đủ lời gọi: chỉ dùng `flag_below`, đánh dấu riêng.

**Dự đoán phân biệt (trên các ca Nezha-OB còn sai có `frontend` đứng đầu).** Nếu từ 2/3 số ca "gắn với root": phần còn lại ở Nezha-OB cùng cơ chế với H4, H7 (tín hiệu ở span phía gọi được tính cho dịch vụ gọi). Nếu không quá 1/3: là cơ chế khác, ghi "chưa giải thích" kèm mô tả O là thao tác gì. Ở giữa: không phân xử rõ. RE2-TT lập cùng bảng, đọc theo ca, không có dự đoán gộp.

**Đã thấy trước.** Kiểm theo tên thao tác (LOG phiên 12 tiếp): thao tác cao nhất của `frontend` là lời gọi tới root ở 3/14 ca (luật của bài) và 3/11 ca (luật của code). Tức tôi đã biết `direct` theo tên là thiểu số; `below`, `slow`, `flag_below` chưa xem. Dự đoán ở trên viết sau khi biết điều này.

**Giới hạn.** `frontend` ở đầu mọi yêu cầu nên `below` gần như luôn cao; vì vậy mốc đọc dùng `linked` và so với dịch vụ khác. Nezha-OB có rất ít trace bất thường dưới bộ chia mới; ca có F dưới 5 span ghi riêng, không xếp loại.

## 5. KT-9 — CIRCA: đổi độ dài đoạn học và vị trí đoạn chấm (laptop)

**Câu hỏi.** Hồi quy theo nút cha làm tăng điểm ở 3.285/4.526 nút, tỷ số tăng theo số nút cha (1,05 với 1 cha tới 8,43 với từ 8 cha; KQ10 mục 1.4). Do (a) quá khớp vì chỉ học trên 111 điểm, hay (b) đoạn chấm là 10 điểm cuối cửa sổ, cách đoạn học gần 300 giây?

**Đường native** (`RCAEval/classes/data.py`, `graph_heads/rht.py`, `src/p3/adapters/circa.py`): chuỗi nạp từ t−120 tới điểm quan sát cuối của đoạn sau mốc; học trên 111 điểm đầu (t−120 … t−10); chấm trên 10 điểm cuối.

**Hai bước bị đổi, mỗi nhánh một bước.**

| Nhánh | Đoạn học | Đoạn chấm | Đồ thị | Chỗ móc |
|---|---|---|---|---|
| `shamw` | native | native | native | Cả hai chỗ móc đặt nhưng truyền đúng giá trị native. Phải khớp bản đóng băng từng bit ở 30/30 ca, cả hai bản ghi (RHT + DA và RHT) |
| `tf` | **291 điểm (t−300 … t−10)** | native | native | `CaseData(..., lookup_window=300)` thay cho 120 |
| `tfk2` | 291 điểm | native | không cạnh | như `tf` + bỏ mọi cạnh (như nhánh `k2` đã có) |
| `t0` | native | **10 điểm t … t+9** | native | truyền `current = t + 9` vào `score_graph` |
| `t0k2` | native | 10 điểm t … t+9 | không cạnh | như `t0` + bỏ mọi cạnh |

Nhánh không cạnh của đường native đã có ở lượt `runs/circa-laptop-k2-001` (nhánh `k2`), dùng lại. Script `scripts/laptop_contrast_v8.py` (v7 cộng năm nhánh; không sửa `src/`). Đây là nhánh chẩn đoán: cửa sổ đã khóa (Q-80, Q-82) và số đã chấm không đổi.

**Đại lượng.** Trên các nút có ít nhất một nút cha hiệu dụng ở nhánh có cạnh và có mặt ở cả nhánh không cạnh tương ứng: tỷ số điểm (có cạnh / không cạnh); số nút tăng, giảm; trung vị tỷ số theo số nút cha (1; 2–3; 4–7; từ 8); số nút có |điểm| > 1e10 và số ca có nút như vậy. Mô tả thêm (không phải mốc): hạng root theo RHT và RHT + DA ở từng nhánh.

**Dự đoán phân biệt** (so với đường native: tỷ lệ nút tăng 3.285/4.526 = 72,6%; trung vị tỷ số nhóm từ 8 cha 8,43):

- (a) quá khớp vì ít điểm học: ở `tf`, trung vị tỷ số của nhóm từ 8 cha giảm còn dưới một nửa (dưới 4,2) **và** tỷ lệ nút tăng giảm từ 10 điểm phần trăm.
- (b) đoạn chấm xa đoạn học: ở `t0`, cùng hai mốc đó.
- Cả hai có thể cùng đạt. Nếu không nhánh nào đạt: việc hồi quy làm tăng điểm không do hai lựa chọn cửa sổ này; ghi đúng như vậy, phần "vì sao" để mở.

**Mẫu số.** 30 ca RE2-TT; tách 11 ca có nút vượt 1e10 ở đường native và 19 ca không có.

**Đã thấy trước.** KQ10 mục 1.3, 1.4, 7 (cơ chế nút đứng yên rồi đổi cho điểm cỡ 1e16; phần tăng chủ yếu từ cạnh cùng dịch vụ); KT-15. Thời gian đo thật của lượt tương tự: 90 tiến trình con hết 595 giây và 407 giây; lượt này 150 tiến trình con, ước 12–17 phút.

**Giới hạn.** Ở `t0`, lỗi có thể chưa hiện ra trong 10 giây đầu sau mốc, nên điểm tuyệt đối thấp hơn; vì vậy mốc đọc dùng tỷ số có cạnh / không cạnh trên cùng nhánh, không dùng hạng root. Ở `tf`, tập nút còn lại sau bước bỏ cột hằng có thể khác; so trên nút chung và ghi số nút khác. Chỉ RE2-TT.

## 6. Thứ tự và chi phí

EC2 (2 nhân, 7,6 GB): KT-1/KT-2, KT-8 nửa TraceRCA, KT-12, bảng nối: mỗi phép một lượt nền riêng, ước dưới 10 phút mỗi lượt theo thời gian đã đo của `chain-spanpass-001` (0,8–10,7 giây mỗi ca). Laptop: KT-9, ước 12–17 phút. Không lượt nào dự kiến quá 1 giờ. Dung lượng mới ước dưới 300 MB.
