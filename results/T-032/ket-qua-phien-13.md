# T-032 — Kết quả phiên 13 (11/10/2026): sáu phép kiểm còn lại và đọc tay nốt

Người làm: Claude. Các phép này Minh duyệt chạy ngày 11/10/2026 (Q-141; lời duyệt ghi ở LOG phiên 12). Thiết kế viết trước khi chạy: `thiet-ke-phep-doi-013.md` (lý do chọn: WHY-48). File này nối tiếp `ket-qua-phien-12.md`; viết tắt KQ13.

**Cách đọc các số.** Mọi số là trên tập dev (30 ca RE2-TT, 22 ca Nezha-OB). Số của nhánh phép đổi đo tác động của một bước tính, không phải thành tích của một phương pháp. Các "mốc đọc" là mốc người làm đặt trước khi chạy để tự buộc mình; mốc không đạt thì ghi không đạt. Phần ghi "tính sau khi xem kết quả" là mô tả thêm, không phải mốc. Đường dẫn tính từ `results/T-032/`; con trỏ JSON ghi sau dấu `→`. Hạng 1 tính bi quan khi hòa.

**Tóm tắt một dòng cho mỗi phép.**

| Phép | Câu hỏi | Trả lời |
|---|---|---|
| KT-1 | Vì sao nửa số trace bị xếp bất thường dù không gắn với root | Phần lớn là mức tự nhiên của luật "một span vượt là cả trace bất thường": không có lỗi nào vẫn có 37% trace bị xếp bất thường (mục 1) |
| KT-2 | 2–9% span mang cờ ở thao tác đông span là tự nhiên hay do sự cố | Cả hai: mức tự nhiên trung vị 1,0%, có thao tác tới 8%; sự cố làm tăng rõ ở thao tác **phía trên root**, gần như không đổi ở thao tác không liên hệ (mục 2) |
| KT-12 | Cột độ trễ của root phản ứng ở ca này, không ở ca kia | Ba cặp, ba lý do khác nhau; hai trong ba là sản phẩm của thang z (nền dao động rộng; IQR tính trên 5 mẫu) (mục 3) |
| KT-8, nửa TraceRCA | Bốn ca ERROR: bỏ thao tác thiếu nền thì root hạng mấy | Hạng 2, 1, 1, 1 (mục 4) |
| Bảng nối nhánh ghép | Thực thể đứng đầu của phần MicroRank còn sai có gắn với root không | RE2-TT: 5/8 và 3/6 ca có; Nezha-OB: `frontend` chỉ gắn ở 3/14 và 3/11 ca, dự đoán "cùng cơ chế H4, H7" **không đạt** cho phần lớn ca (mục 5) |
| KT-9 | CIRCA: hồi quy làm tăng điểm là do cửa sổ? | Một phần: hai nhánh cửa sổ đều giảm khoảng một nửa mức tăng ở nút nhiều cha, nhưng hồi quy vẫn làm tăng điểm ở 67–73% nút; mốc khai trước **không đạt** ở cả hai nhánh (mục 6) |

## 1. KT-1 — mốc giả: tỷ lệ trace bị xếp bất thường khi không có lỗi

Nguồn: lượt `runs/fake-marker-001/` trên EC2 (script `scripts/fake_marker_v1.py`), 172 giây; `summary.json`. Đại lượng tính thêm: `runs/tong-hop-phien-13-001/derived-013.json → /kt1` (script `scripts/phien13_derive_v1.py`). Không gọi phương pháp. 26 ca RE2-TT có bảng span đã lưu; 4 ca nguồn ERROR ghi N/A.

**Kiểm** (`summary.json → /summary/self_check`). Ở cấu hình giữ nguyên `real300`: tổng số cờ bằng H_native ở 26/26 ca; số trace bất thường, số trace bình thường và số cờ theo biểu thức của MicroRank bằng số của lượt `chain-spanpass-001` ở 26/26; a và n của mọi thao tác bằng số đã lưu ở 26/26. Hai biểu thức cờ (TraceRCA, MicroRank) không khác nhau ở span nào trong cả sáu cấu hình (`→ /summary/configs/*/flags_differ_total` đều bằng 0).

**Quan sát** (trung vị qua 26 ca; `→ /summary/configs/<tên>`):

| Cấu hình | Tỷ lệ trace bất thường | Trong các trace không có span của root | Trong các trace có span của root | Tỷ lệ span mang cờ |
|---|---|---|---|---|
| `real300` (giữ nguyên) | 50,2% | 17,3% | 92,4% | 1,8% |
| `real150` (mốc thật, 150 giây) | 51,9% | 20,8% | 93,5% | 2,0% |
| `fake150` (mốc giả, 150 giây) | **36,6%** | **15,9%** | 46,7% | 1,1% |
| `real100` | 53,1% | 22,2% | 95,2% | 2,2% |
| `fake100a` (mốc giả thứ nhất) | 35,5% | 18,6% | 46,8% | 1,1% |
| `fake100b` (mốc giả thứ hai) | 38,4% | 18,9% | 45,9% | 1,2% |

- Khi **không có lỗi nào** trong đoạn xét, luật "trace bất thường khi có ít nhất một span vượt mean + 3·std" vẫn xếp 11–43% trace là bất thường, trung vị 36,6%; ở 20/26 ca tỷ lệ này từ 20% trở lên (`derived-013.json → /kt1/fake_all`, `/kt1/cases_fake_all_ge_0.20`).
- Ở mốc thật, trung vị 54% số trace bất thường là trace không có span của root (`→ /kt1/share_of_real_abnormal_traces_without_root`).
- Hai vị trí mốc giả cho tỷ lệ gần nhau: hiệu `fake100a` − `fake100b` có trung vị −1,8 điểm phần trăm (từ −12,4 tới +6,8); không ca nào chênh quá nửa giá trị lớn hơn (`summary.json → /summary/kt1/fake_position_unstable_cases` = 0/26).
- Giả định "các span vượt ngưỡng độc lập nhau" dự đoán tỷ lệ cao hơn thật: trung vị 47,1% so với 36,6%; tỷ số dự đoán/thật từ 1,20 tới 2,00 (`derived-013.json → /kt1/predicted_over_actual_fake_by_case`). Tức cờ dồn vào một số trace nhiều hơn mức ngẫu nhiên.

**Đối chiếu với ba mốc khai trước** (`summary.json → /summary/kt1`; R = tỷ lệ ở các trace không có root của `real150`, F = tỷ lệ của `fake150` trên mọi trace).

- (a) "thuần xác suất": cần F ≥ 0,8·R **và** dự đoán theo độc lập nằm trong ±20% tỷ lệ thật. Vế đầu đạt (F = 36,6% so với R = 20,8%; đạt ở 18/26 ca). Vế sau **không đạt** (chỉ 1/26 ca trong ±20%). Theo đúng chữ đã khai: mốc (a) **không đạt**.
- (b) "do sự cố": cần F ≤ 0,5·R. **Không đạt** (0/26 ca).
- (c) "nền không đại diện": cần tỷ lệ ở mốc giả từ 20% **và** đổi theo vị trí mốc. Vế đầu đạt, vế sau **không đạt** (0/26). Mốc (c) không đạt.
- Vậy theo mốc đã khai, kết luận là **"không phân xử rõ"**. Tôi ghi đúng như vậy, và ghi thêm một lỗi trong mốc của chính tôi: mốc (a) và (b) so F trên **mọi** trace với R trên trace **không có root**, tức so hai tập trace khác loại.

**So cùng loại trace (tính sau khi xem kết quả;** `derived-013.json → /kt1`**).**

- Trace không có root: 15,9% ở mốc giả, 20,8% ở mốc thật. Tỷ số theo ca (giả/thật) có trung vị 0,93, từ 0,65 tới 1,26; từ 0,8 trở lên ở 18/26 ca; không ca nào dưới 0,5.
- Trace có root: 46,7% ở mốc giả, 93,5% ở mốc thật; tỷ số theo ca có trung vị 0,53.

**Đọc, ở mức mô tả.** Trong điều kiện RE2-TT (trace có hàng chục tới hàng trăm span, mỗi thao tác có khoảng 1% span vượt ngưỡng một cách tự nhiên), bước chia trace của bản thư viện xếp một trace không dính tới root vào nhóm bất thường với tần suất gần bằng lúc không có sự cố. Phần sự cố thêm vào là nhỏ ở trace không có root (khoảng 5 điểm phần trăm ở trung vị) và lớn ở trace có root (47% lên 94%). Giải thích (a) về bản chất được hỗ trợ; phần "độc lập" của nó thì không: cờ dồn theo trace. Giải thích (b) chỉ đóng phần nhỏ. Giải thích (c) không được hỗ trợ.

**Giới hạn.** Cửa sổ 100–150 giây, ngắn hơn giao thức. Chỉ RE2-TT; Nezha-OB không kiểm được (nền 41–97 giây). Phần "so cùng loại trace" nghĩ ra sau khi xem kết quả. Đây là kết luận về bước chia trace của bản thư viện (MicroRank-RCAEval), không phải về MicroRank gốc.

## 2. KT-2 — mốc giả: tỷ lệ span mang cờ theo thao tác

Nguồn: cùng lượt; `summary.json → /summary/kt2`; `derived-013.json → /kt2`. "Thao tác đông span": có từ 200 span ở đoạn xét của cả `fake150` lẫn `real150`, không phải thao tác của root. Có 1.021 cặp (thao tác, ca) như vậy trên 26 ca.

**Quan sát.**

| Nhóm thao tác theo vị trí của dịch vụ so với root | Số cặp | Trung vị a/n ở mốc giả | Trung vị a/n ở mốc thật | Số cặp có a/n mốc giả từ 2% | Số cặp có a/n mốc thật gấp từ 2 lần mốc giả |
|---|---|---|---|---|---|
| Mọi thao tác đông span | 1.021 | 1,0% | 1,6% | 230 | 340 |
| Phía trên root (gọi trực tiếp hoặc gián tiếp) | 236 | 0,8% | **6,2%** | 47 | 161 |
| Không liên hệ với root | 614 | 1,1% | 1,2% | 134 | 145 |
| Phía dưới root hoặc hai chiều | 171 | 1,2% | 1,4% | 49 | 34 |

- Mức tự nhiên: trung vị 1,0%, lớn nhất 8,1% (`derived-013.json → /kt2/all`). Với phân phối chuẩn, tỷ lệ vượt mean + 3·std là 0,13%; mức thấy ở đây cao hơn khoảng 8 lần, tức thời lượng span có đuôi dài.
- Chín cặp "thực thể không liên hệ đứng trên root" trong bản ghi TraceRCA đã chấm (hai ca order|loss; a, n ở `real300` trùng số đã lưu ở 9/9): a/n ở mốc giả từ 0% tới 3,8%, trung vị 1,9%; từ 2% trở lên ở 4/9. Sau mốc thật, 5/9 cặp tăng gấp từ 2 lần, 4/9 giữ nguyên mức (`→ /kt2/pairs`). Ví dụ giữ nguyên: `ts-basic-service` 20/520 ở mốc giả và 18/534 sau mốc thật. Ví dụ tăng: thao tác đăng nhập của `ts-auth-service` 2/228 và 4/216 ở mốc giả, 21/233 và 23/231 sau mốc thật.

**Đối chiếu với hai mốc khai trước.** (a) "mức tự nhiên: từ nửa số thao tác đông span có a/n ≥ 2% ở mốc giả": **không đạt** (230/1.021). (b) "do sự cố: từ 3/4 số thao tác có a/n < 1% ở mốc giả, và trung vị mốc thật gấp từ 2 lần": **không đạt** (492/1.021 dưới 1%; trung vị 1,6% so với 1,0%). Theo mốc: "không phân xử rõ"; hai giải thích cùng có mặt.

**Đọc, ở mức mô tả.** (1) Một thao tác đông span không liên hệ với root có 1–4% span mang cờ là chuyện bình thường của dữ liệu này, có hay không có sự cố; đây là nguồn của đường thất bại "khối lượng lấn át" ở TraceRCA. (2) Sự cố làm tăng tỷ lệ cờ **có chọn lọc theo chuỗi gọi**: ở thao tác phía trên root tăng gần 8 lần (0,8% lên 6,2%), ở thao tác không liên hệ gần như không đổi (1,1% lên 1,2%). Đây là bằng chứng mô tả cho việc dịch vụ gọi dài ra theo root, đo trên cùng thao tác trước và sau, có đối chứng là thao tác không liên hệ. Nó không nói span dài ra vì chờ hay vì lý do khác; phần đó xem mức đo được của trace ở báo cáo chính mục 2. (3) Có ngoại lệ: một số thao tác không liên hệ tăng thật sau mốc (145/614 cặp), rõ nhất là đăng nhập của `ts-auth-service` ở các ca order|loss; lý do vật lý không phân xử được bằng dữ liệu hiện có (`kiem-tiep.md` mục KT-6).

**Giới hạn.** Như mục 1. Bảng theo vị trí dùng đồ thị gọi dựng từ trace của chính ca đó. Nhóm theo vị trí được tính sau khi nối nhãn root.

## 3. KT-12 — cột độ trễ của root ở ba cặp ca cùng ô

Nguồn: lượt `runs/root-latency-001/` trên EC2 (script `scripts/root_latency_series_v1.py`), 83 giây; `summary.json`. Mỗi ca chạy đúng đường phát lại BARO native với lớp bọc chỉ-đọc lưu bảng metric mà phương pháp nhận.

**Kiểm.** Bản ghi của cả 7 tiến trình con khớp bản đóng băng BARO từng bit (`→ /self_check`: 7/7). z kiểu BARO tính lại cho cột bằng đúng điểm trong bản ghi (trường `frozen_score` cạnh `robust_z_max` ở `→ /pairs/*/comparisons`).

**Cặp 1: `ts-auth-service`, lỗi delay (RE2-TT, 300 mẫu mỗi phía).** Cột `ts-auth-service_latency` (`→ /cases/<mã>/columns`):

| Ca | Trung vị nền → sau mốc | IQR nền | z kiểu BARO | Số mẫu sau mốc vượt mean + 3·std | Giây đầu tiên vượt |
|---|---|---|---|---|---|
| `dev-746fd74313` | 0,244 → 0,950 | 0,023 | 30,7 | 284/300 | 16 |
| `dev-f81f88234e` | 0,771 → 1,375 | 0,240 | 4,9 | 158/300 | 52 |
| `dev-57546fd87b` | 0,692 → 1,600 | 0,537 | 2,4 | 0/300 | không |

Cột của root **tăng ở cả ba ca** (trung vị gấp 3,9; 1,8; 2,3 lần). Khác nhau nằm ở nền: IQR nền của hai ca sau lớn gấp 10 và 23 lần ca đầu; trung vị theo từng đoạn 50 giây của nền ở `dev-57546fd87b` chạy từ 0,47 tới 1,54. Không ai gọi `ts-auth-service` trong trace nên không có bảng lời gọi chậm; mốc (c) và (a) không tính được; mốc (b) không đạt (300 mẫu ở cả ba ca). **Đọc:** không giải thích nào trong ba giải thích khai trước mô tả đúng. Điều thấy được, ghi sau khi xem kết quả: cùng loại lỗi làm cột tăng 2–4 lần ở cả ba ca, còn z (và số phiếu của SimpleRCA) khác nhau vì nền của cột trước mốc dao động khác nhau. Vì sao nền của hai ca dao động rộng: chưa biết; dữ liệu không ghi tải trước mốc theo dịch vụ.

**Cặp 2: `recommendationservice`, network_delay (Nezha-OB, 5 mẫu mỗi phía).**

- Lời gọi tới root chậm ở 97,5% (`dev-5467884de4`) và 96,7% (`dev-63c30faf34`) lời gọi; phần chậm nằm trong span của root: 0% ở cả hai (`→ /cases/<mã>/calls_into_root_total`).
- Cột độ trễ phía server P99 của root: ở `dev-5467884de4` nền 0,088; 0,093; 0,086; 0,096; 0,078 và sau mốc 0,117; 0,041; 0,064; 0,043; **0,555**; z = 64 đến từ một mẫu. Ở `dev-63c30faf34` sau mốc 0,040; 0,058; 0,021; 0,026; 0,021, thấp hơn nền; z âm. Trung vị của cả sáu cột độ trễ của root **giảm** sau mốc ở cả hai ca.
- Mốc (a) "cột đo sai chỗ" **đạt** theo chữ đã khai (cường độ và số mẫu tương đương, phần trong span của root dưới 20% ở cả hai). Mốc (b), (c) không đạt. **Đọc:** với lỗi trễ mạng, cột độ trễ của root không ghi được sự cố ở cả hai ca; "ca phản ứng" khác "ca không phản ứng" ở đúng một mẫu P99. Theo thiết kế, phần "vì sao có mẫu đó" để **mở**.

**Cặp 3: `checkoutservice`, network_delay (Nezha-OB).**

- Lời gọi tới root chậm ở 25,8% (`dev-2bfc97b01e`, 31 lời gọi) và 9,1% (`dev-607751ac0a`, 33 lời gọi). Mốc (c) "cường độ khác nhau" **đạt** theo chữ; điều này đã biết trước khi chạy (ghi ở thiết kế).
- Nhưng chuỗi cho thấy z = 94 của "ca phản ứng" không phải phản ứng: cột độ trễ phía server P99 của root có nền 0,495; 0,495; 0,970; 0,244; 0,490 và sau mốc 0,480; 0,493; 0,498; 0,249; 0,965. Hai chuỗi gần như trùng nhau; z lớn vì IQR của 5 mẫu nền là 0,005. z tính theo độ lệch chuẩn của cùng cột là 1,8.
- **Đọc:** ở cặp này cả hai ca đều không có phản ứng thật ở cột độ trễ của root; khác biệt z = 94 so với z ≈ 0 là sản phẩm của thang IQR trên 5 mẫu. Câu "cùng ô, root có tín hiệu ở ca này và không có ở ca kia" trong `doc-tay.md` mục 4.3 đúng về số phiếu, nhưng không nên đọc là cột độ trễ của root nhạy với cường độ lỗi.

**Kết luận chung của KT-12.** Ba cặp không có chung một lý do. Ở hai cặp (1 và 3), khác biệt giữa hai ca là do cách chuẩn hóa theo nền, không do root phản ứng khác nhau. Ở cặp 2, cột độ trễ phía được gọi không ghi được lỗi trễ mạng; tín hiệu nằm ở phía gọi. Hệ quả cho phân loại: các ca này thuộc "cách chuẩn hóa" (phương pháp) và "cột đo ở phía được gọi" (dữ liệu, kéo theo yêu cầu quan sát), không thuộc "cường độ lỗi khác nhau".

**Giới hạn.** Ba cặp, bảy ca; mô tả. Nezha-OB chỉ có 5 mẫu mỗi phía. Không có metric phía mạng.

## 4. KT-8, nửa TraceRCA — bốn ca ERROR khi bỏ thao tác không có ở đoạn nền

Nguồn: lượt `runs/tracerca-dropnew-001/` trên EC2 (script `scripts/tracerca_dropnew_v1.py`), 494 giây; `summary.json → /summary`. Đổi đầu vào rồi gọi adapter TraceRCA nguyên trạng. Không thay số đã chấm.

**Kiểm.** Ở 48 ca nguồn OK: không span nào bị bỏ ở 48/48; hạng (tốt nhất, xấu nhất) của mọi thực thể trùng bản ghi đóng băng ở 48/48 (`→ /summary/self_check`). Số span và số trace bị bỏ ở 4 ca trùng số của nửa MicroRank chạy trên laptop (KQ12 mục 2): 527/195, 444/167, 339/130, 210/71.

**Quan sát** (`→ /summary/error_source_cases`; cột MicroRank chép từ KQ12 mục 2; hai cột cạnh nhau ở `derived-013.json → /kt8`):

| Ca | Ô | Span bị bỏ | TraceRCA: hạng root; thực thể đứng đầu | MicroRank: hạng root; thực thể đứng đầu |
|---|---|---|---|---|
| `dev-03d4910932` | route, socket | 527 | 2; `ts-travel2-service` | 2; `ts-station-service` |
| `dev-16870e660c` | route, mem | 444 | **1** | 2; `ts-station-service` |
| `dev-4e68956051` | train, delay | 339 | **1** | 3; `ts-station-service` |
| `dev-a5cabe5fa7` | travel, loss | 210 | **1** | 12; `ts-station-service` |

**Đọc.** Với TraceRCA, cách ghi 4 ca này **có đổi con số**: hiện 4 ca tính là trượt; nếu bỏ thao tác thiếu nền thì 3/4 ca root hạng 1 và 4/4 trong 5 hạng đầu. Với MicroRank thì ở hạng 1 không đổi (0/4). Đây không phải đề nghị sửa số đã chấm: giao thức đã khóa ghi ERROR là trượt. Điều cần ghi ở bảng G2: Hit@1 của TraceRCA trên RE2-TT thấp hơn 3 ca (trên 30) so với khi coi lỗi này là lỗi đầu vào; thao tác gây lỗi là một thao tác của `ts-order-other-service`, không thuộc root của ca nào trong bốn ca.

**Giới hạn.** Bốn ca. Đổi đầu vào sau khi đã biết lý do lỗi. Thao tác bị bỏ có 210–527 span trong 123.487–174.798 span sau mốc.

## 5. Bảng nối theo cây span cho nhánh ghép của MicroRank

Nguồn: lượt `runs/microrank-merged-link-001/` trên EC2 (script `scripts/microrank_merged_link_v1.py`), 315 giây; `summary.json`; gộp đếm ở `derived-013.json → /merged_link`. Thứ hạng và thao tác cao nhất lấy từ lượt laptop `runs/microrank-kt3-001` qua file rút gọn `runs/microrank-merged-link-input-001/kt3-rankings.json` (sha256 trùng ở hai đầu, ghi ở `summary.json → /sources`). Không chạy phương pháp.

**Kiểm** (`→ /summary/self_check`). Hai tập trace của nhánh ghép dựng lại trên EC2 trùng lượt laptop ở 47/47 ca cho cả hai luật, trên 14 con số mỗi ca (số trace sau mốc, số trace bất thường mới, số trace bất thường mới cũng bất thường theo native, bảng số trace bất thường theo dịch vụ, số trace có span mang cờ, tổng số đếm riêng…). 13 trường hợp tự dựng của cây span và 4 trường hợp cho "lời gọi trực tiếp" đạt (`→ /fixtures`).

**Quan sát theo ca còn sai** (thực thể đứng đầu; cách đọc theo mốc đã khai: "gắn với root" khi từ 50% span mang cờ của thao tác cao nhất bao một lời gọi chậm tới root hoặc có span mang cờ của root nằm dưới, và cao hơn dịch vụ khác tốt nhất; "không gắn" khi dưới 20%):

| Dataset, luật | Ca root chưa hạng 1 | Gắn với root | Không gắn | Không rõ | Dưới 5 span |
|---|---|---|---|---|---|
| RE2-TT, luật của bài | 8 | 5 | 3 | 0 | 0 |
| RE2-TT, luật của code | 6 | 3 | 3 | 0 | 0 |
| Nezha-OB, luật của bài | 16 | 5 | 6 | 1 | 4 |
| Nezha-OB, luật của code | 14 | 5 | 5 | 1 | 3 |

- **Nezha-OB, `frontend` đứng đầu** (`→ /summary/prediction_nezha_frontend`): 14 ca (luật của bài) và 11 ca (luật của code). "Gắn với root" ở **3/14 và 3/11**; "không gắn" 6 và 5; không rõ hoặc dưới 5 span: 5 và 3. Ba ca gắn (`dev-3e27669440`, `dev-5467884de4`, `dev-63c30faf34`) là đúng ba ca mà phép kiểm theo tên thao tác đã chỉ ra: thao tác cao nhất của `frontend` là span phía gọi của lời gọi tới root, và 97–100% span mang cờ của nó có span con trực tiếp thuộc root. Cây span **không** tìm thêm được ca gián tiếp nào.
- Ở các ca "không gắn" của Nezha-OB, thao tác cao nhất của `frontend` là lời gọi tới `productcatalogservice` hoặc `currencyservice` (hoặc span đầu của yêu cầu); số span mang cờ tạo ra điểm của nó chỉ 5–12 (một ca 51); và ở 6/6 ca (luật của bài) và 4/5 ca (luật của code) **không trace nào** trong các trace đó có span của root (`derived-013.json → /merged_link/by_dataset/Nezha-OB/*/not_attached_with_zero_root_traces`).
- **Nezha-OB, `checkoutservice` đứng đầu** (2 và 3 ca; root `emailservice`, lỗi network_delay): ở 2 ca dưới cả hai luật, 90–92% span mang cờ của thao tác cao nhất bao một lời gọi chậm tới root; ở 3 trong 4 lượt đó thao tác chính là span phía gọi của lời gọi tới root, lượt còn lại là thao tác bao ngoài nó.
- **RE2-TT:** ca "gắn với root" có thực thể đứng đầu là dịch vụ gọi trực tiếp root (`ts-inside-payment-service`, `ts-travel-service`, `ts-seat-service`) hoặc phía trên gián tiếp (`ts-admin-travel-service`, hai ca train|cpu, 99–100% span mang cờ bao lời gọi chậm tới root). Ba ca "không gắn" dưới cả hai luật đều có `ts-auth-service` đứng đầu bằng thao tác đăng nhập (`dev-20acb4402d`, `dev-260d332c8d`, `dev-bcbd4f46ae`); không trace nào trong 28, 41 và 12 trace tạo ra điểm của nó có root.

**Đối chiếu với dự đoán khai trước** (mốc: từ 2/3 số ca `frontend` đứng đầu là "gắn với root" thì đọc "cùng cơ chế H4, H7"; không quá 1/3 thì đọc "cơ chế khác, chưa giải thích"). 3/14 và 3/11 đều không quá 1/3. **Dự đoán "cùng cơ chế H4, H7" không đạt.** Câu tôi viết ở KQ12 mục 1 ("khớp với hạn chế H4, H7") sai cho phần lớn ca; đã sửa ở ba file (mục 8).

**Đọc, ở mức mô tả.** Có ba dạng quan sát trong phần MicroRank còn sai sau ghép hai phép đổi; chúng không bao phủ mọi ca và chưa là ba nguyên nhân đã xác nhận:

1. **Thao tác cao nhất của thực thể đứng đầu bao lời gọi chậm tới root** (thực thể là dịch vụ gọi root, trực tiếp hoặc gián tiếp; thời gian của lời gọi được tính cho nó): 5/8 và 3/6 ca RE2-TT; 5/16 và 5/14 ca Nezha-OB. Đây là phần mà thông tin cạnh gọi chạm tới được.
2. **Các trace tạo số đếm cho thao tác đứng đầu không chứa root:**3 ca RE2-TT và 6 ca Nezha-OB theo luật bài, 4 ca theo luật code. Đây là tập trace gắn với thao tác cao nhất có cờ, không phải toàn bộ nhóm trace bất thường. Một ca không gắn theo luật code vẫn có root trong trace xét; xem phần chưa rõ dưới đây.
3. **Quá ít trace bất thường để xếp:** 3–4 ca Nezha-OB có dưới 5 span tạo ra điểm của thực thể đứng đầu.

**Phần chưa rõ và giới hạn.** dev-14701a3bbb (shippingservice, cpu_contention) là cùng một ca chưa rõ dưới cả hai luật: tỷ lệ gắn root 2/5 và 8/15, thấp hơn tỷ lệ gắn currencyservice 4/5 và 13/15. Với dev-607751ac0a (checkoutservice, network_delay), luật code cho 0/6 span gắn root theo cây con nhưng 2/6 trace vẫn chứa root, một trace có root mang cờ. Vì vậy không đồng nhất không gắn với root vắng mặt. Cả 14 ca Nezha theo luật code gồm 5 gắn, 5 không gắn, 1 chưa rõ, 3 ít span; trong 5 không gắn chỉ 4 ca vắng root ở tập trace xét. Cần lần theo đồ thị, trọng số và số đếm của các ca chưa rõ để phân xử; không gọi là dạng cơ chế thứ tư đã xác nhận. Nhánh ghép là chẩn đoán, mốc 50%/20% do người làm đặt; dự đoán viết sau kết quả kiểm tên thao tác. Nguồn: runs/microrank-merged-link-001/summary.json → /cases (case_id và từng nhánh); derived-013.json → /merged_link/by_dataset/Nezha-OB.

## 6. KT-9 — CIRCA: đổi độ dài đoạn học và vị trí đoạn chấm

Nguồn: lượt `runs/circa-kt9-001/` trên laptop (script `scripts/laptop_contrast_v8.py`), 150/150 tiến trình con, 985 giây, RAM hệ thống đỉnh 76,5%, không lần chờ hay giết nào (`runs/circa-kt9-001-launch/stdout.txt`, dòng cuối). Tổng hợp: `runs/circa-kt9-001/collect-001/summary.json` (script `scripts/laptop_contrast_collect_v6.py`). Nhánh không cạnh của đường native lấy từ lượt `runs/circa-laptop-k2-001`. Đây là nhánh chẩn đoán; cửa sổ đã khóa và số đã chấm không đổi.

**Kiểm** (`→ /summary/self_check`). Nhánh giữ nguyên `shamw` (hai chỗ móc đặt nhưng truyền giá trị native) khớp bản đóng băng từng bit ở 30/30 ca, cả hai bản ghi. Chỗ móc nhận đúng giá trị: đoạn học 111 điểm ở `shamw`, 291 điểm ở `tf` và `tfk2` (30/30); đoạn chấm kết thúc ở t + 9 ở `t0` và `t0k2` (30/30); hai nhánh không cạnh có 0 cạnh (30/30). Cách tính của file này tái lập số của KQ10 mục 1.4 trên đường native: 4.526 nút có hồi quy, điểm cao hơn điểm không cạnh ở 3.285, thấp hơn ở 1.161.

**Một điểm lệch so với số dẫn trong thiết kế.** Thiết kế dẫn "trung vị tỷ số nhóm từ 8 cha là 8,43" từ KQ10; số đó tính trên 191 nút sau khi loại thêm một số nút ở bước phân rã. Tính trực tiếp tỷ số điểm trên 202 nút có tỷ số xác định, đường native cho **7,54**. Mốc "giảm còn dưới một nửa" được xét với cả hai số (dưới 4,2 và dưới 3,77).

**Quan sát** (`→ /summary/all/<nhánh>`; 30 ca):

| | native | học 291 điểm (`tf`) | chấm t … t+9 (`t0`) |
|---|---|---|---|
| Nút có hồi quy, có mặt ở nhánh không cạnh | 4.526 | 4.534 | 4.435 |
| Điểm có cạnh cao hơn / thấp hơn điểm không cạnh | 3.285 / 1.161 | 3.051 / 1.451 | 3.241 / 1.187 |
| Tỷ lệ nút tăng | 72,6% | 67,3% | 73,1% |
| Trung vị tỷ số, 1 cha | 1,05 | 1,03 | 1,07 |
| Trung vị tỷ số, 2–4 cha | 1,33 | 1,12 | 1,47 |
| Trung vị tỷ số, 5 cha | 2,97 | 1,81 | 2,13 |
| Trung vị tỷ số, 6 cha | 3,44 | 2,01 | 2,16 |
| Trung vị tỷ số, 7 cha | 7,21 | 3,62 | 5,47 |
| Trung vị tỷ số, từ 8 cha | **7,54** | **3,40** | **3,64** |
| Số ca có nút vượt 1e10 | 11 | 9 | 2 |
| Hạng 1 theo RHT / RHT không cạnh / RHT + DA (mô tả, không phải mốc) | 12 / 21 / 16 | 15 / 21 / 18 | 12 / 14 / 13 |

**Đối chiếu với mốc khai trước** (`→ /summary/marks`; mỗi nhánh cần cả hai: trung vị tỷ số nhóm từ 8 cha dưới một nửa native, và tỷ lệ nút tăng giảm từ 10 điểm phần trăm).

- (a) quá khớp vì ít điểm học, nhánh `tf`: vế đầu **đạt** (3,40, dưới cả 4,2 lẫn 3,77); vế sau **không đạt** (72,6% xuống 67,3%, giảm 5,3 điểm). Mốc (a) **không đạt**.
- (b) đoạn chấm xa đoạn học, nhánh `t0`: vế đầu **đạt** (3,64); vế sau **không đạt** (73,1%, không giảm). Mốc (b) **không đạt**.
- Theo mốc đã khai, cả hai nhánh không đạt trọn. Quan sát: trung vị tỷ số ở nút nhiều cha giảm từ 7,54 xuống 3,40 và 3,64; hồi quy vẫn làm tăng điểm ở đa số nút. Không dùng điều này để bác bỏ mọi ảnh hưởng của cửa sổ hoặc tách riêng nguyên nhân: tập nút, phân phối nền và giai đoạn lỗi cùng đổi. Ở tf, tỷ số vẫn tăng từ 1,03 tới 3,40 theo số cha.

**Quan sát thêm, không có mốc** (`→ /cases`).

- Giá trị cực lớn: học trên 291 điểm chỉ bỏ được 2/11 ca (`dev-03d4910932`, `dev-3ae0a6c15a`); nút cực lớn ở 9 ca còn lại vẫn là `ts-admin-travel-service_latency`. Chấm ngay sau mốc còn 2 ca; nhưng ở nhánh đó lỗi chưa hiện ra ở nhiều ca (số ca hạng 1 không cạnh tụt từ 21 xuống 14), nên không đọc đây là cách chữa.
- Ba ca root `ts-auth-service` mà DA làm tụt hạng (KQ12 mục 3): hạng sau DA ở native → `tf` là 15 → **1** (`dev-16597725c1`), 22 → 6 (`dev-f81f88234e`), 46 → 37 (`dev-57546fd87b`). Tức điểm lớn của nút không liên quan (`ts-preserve-service_latency`) mà KT-15 thấy **phụ thuộc độ dài đoạn học**: học trên 291 điểm thì hiện tượng mất ở ca rõ nhất. Câu "điểm nguồn là thay đổi thật ở dịch vụ không liên quan" ở KQ12 mục 3 và `kiem-tiep.md` mục KT-15 viết quá tay; đúng hơn: điểm đó lớn dưới đoạn học 111 điểm. Đã sửa (mục 8).
- Số ca hạng 1 theo RHT + DA: 16 (native), 18 (`tf`), 13 (`t0`). Đây là mô tả của nhánh chẩn đoán trên dev, không phải số chấm.

**Đọc, ở mức tính toán.** Hai phép đổi xác nhận điểm và thứ hạng nhạy với cửa sổ. Chúng chưa tách được ba nguyên nhân độc lập: học 291 điểm đổi cả độ dài và dữ liệu nền; chấm ngay sau mốc đổi cả giai đoạn lỗi, có ca lỗi chưa hiện rõ; bước lọc cột làm tập nút khác nhau. Bởi vậy 7,54 → 3,40/3,64 là kết quả của hai cấu hình chẩn đoán, không phải tỷ lệ phần nguyên nhân do ít điểm học hay chấm xa. Phần dư còn cao và tăng theo số cha phù hợp với quan sát KQ10 mục 1.4, nhưng chưa có phép đổi riêng phân xử phần còn lại.

**Giới hạn.** Chỉ RE2-TT. Hai nhánh đổi cửa sổ đã khóa nên chỉ là chẩn đoán. Tập nút sau bước bỏ cột hằng đổi theo cửa sổ (8.605, 8.655 và 8.353 nút qua 30 ca), nên ba cột không so trên cùng tập nút tuyệt đối. Nghĩ ra sau khi xem kết quả dev.

## 7. Đọc tay nốt

- Đã đọc 68 đơn vị OK xếp sai còn lại: BARO 7, SimpleRCA 6, TraceRCA 10, MicroRank 28, CIRCA 8, TORAI B 9. 48 đơn vị không chạy được ghi theo lý do, đã soát dòng lý do của cả 48 phiếu (42 UNSUPPORTED theo hai lý do của Q-85; 6 ERROR cùng một thao tác thiếu nền). Nội dung: `doc-tay.md` mục 8. Phiếu: `runs/tong-hop-phien-13-001/phieu-gon-chua-doc/` (script `scripts/phieu_gon_v2.py`; không tính gì mới so với bảng của phiên 12).
- Sau phiên 13: 168 đơn vị đọc tay không trùng (144 đơn vị sai hoặc không OK và 24 đối chứng đúng); 48 đơn vị không chạy được ghi theo lý do; 156 đơn vị đúng ở hạng 1 không thuộc diện đọc.
- Phần đọc nốt thêm các điều chỉnh về thang BARO, độ dao động nền auth|delay, chờ qua hai tầng, T-D theo cạnh và TORAI nguồn log (doc-tay mục 8). Với MicroRank, ba dạng chỉ là dạng quan sát; bảng nối còn ca chưa rõ và một ca không gắn nhưng root có trong trace. Không nhận là đã xác định hết đường thất bại.

## 8. Những câu đã viết ở các file trước bị kết quả phiên 13 sửa

| Câu cũ | Ở đâu | Sửa thành | Căn cứ |
|---|---|---|---|
| "frontend đứng đầu … khớp với H4, H7" | KQ12 mục 1; KT-3; báo cáo mục 5.1 | Chỉ 3/14 và 3/11 gắn theo bảng nối; các ca khác gồm không gắn, ít span và chưa rõ. Không gắn không luôn là root vắng mặt | Mục 5 và đính chính sau REVIEW |
| "DA … điểm nguồn là thay đổi thật ở dịch vụ không liên quan" | KQ12 mục 3; `kiem-tiep.md` mục KT-15; `doc-tay.md` mục 5.3 | Điểm đó lớn dưới đoạn học 111 điểm; học trên 291 điểm thì root của ca rõ nhất về hạng 1 | Mục 6 |
| "Chưa phân xử: vì sao thao tác không liên hệ có 3–6% span vượt ngưỡng" | `doc-tay.md` mục 1.3; `kiem-tiep.md` mục KT-2, KT-4 | Mức tự nhiên trung vị 1,0%, tới 8%; 4/9 cặp đã đọc giữ mức tự nhiên, 5/9 tăng sau mốc | Mục 2 |
| "Root gần như không có tín hiệu metric" (auth, delay) | `doc-tay.md` mục 3.1 | Cột latency của root tăng 1,8–3,9 lần ở cả ba ca; z nhỏ vì nền dao động rộng | Mục 3 |
| "Cùng ô, cột độ trễ của root phản ứng ở ca này, không ở ca kia" (checkoutservice) | `doc-tay.md` mục 3.4, 4.3 | Không ca nào phản ứng; z = 94 là do IQR của 5 mẫu | Mục 3 |
| "4 ca ERROR tính là trượt không làm lệch kết luận nào" | KQ12 mục 2 (viết cho MicroRank) | Đúng cho MicroRank ở hạng 1; với TraceRCA thì 3/4 ca sẽ là hạng 1 | Mục 4 |
| "Phần chậm nằm ngoài span của root nên T-D không gỡ được" (một cách hiểu) | `doc-tay.md` mục 1.2 | Không được hỗ trợ: ca T-D không gỡ được có 83% lời gọi chậm nằm trong span của root, ca gỡ được có 74% | `doc-tay.md` mục 8.3 điểm 10 |

Các file cũ `ket-qua-phien-9.md` tới `ket-qua-phien-12.md` là bản ghi theo thời điểm; tôi chỉ sửa câu "H4, H7" ở KQ12 theo đúng chỉ đạo của Minh và thêm dòng trỏ tới file này. Những câu còn lại được sửa ở báo cáo chính, `kiem-tiep.md` và `doc-tay.md`.

**Đính chính sau REVIEW, Minh duyệt 11/10.** Không suy từ root không hạng 1 sang không có tín hiệu do lỗi; không bác bỏ chờ trong MicroRank chỉ vì M-D gần giữ hạng; giữ ca chưa rõ và ca không gắn nhưng root hiện diện; không tách ba nguyên nhân của CIRCA từ hai phép đổi cửa sổ. Bản trước và bằng chứng sửa ở runs/sua-review-001/. Self-check E cũ kiểm mục 1–6; mục 7 và doc-tay mục 8 được đối chiếu riêng trong kiem-so/ của lượt sửa này. Bản lịch sử ở mục 9 mô tả chi phí và cách chạy của phiên 13, không phải lượt sửa này.

## 9. Chi phí và điều kiện dừng

- Lượt máy dài nhất: 985 giây (KT-9, laptop). EC2: 172, 494, 83 và 315 giây. Không lượt nào chạm mốc 1 giờ.
- RAM laptop đỉnh 76,5%. Không nhánh giữ nguyên nào lệch bản đóng băng. Không chỗ nào hỏng 3 lần.
- Ca thử trước mỗi lượt đủ, chạy sau khi file thiết kế đã ghi (pins ở các thư mục `*-launch/`): `runs/circa-kt9-test-001`, `runs/fake-marker-test-001`, `runs/tracerca-dropnew-test-001`, `-002`, `runs/root-latency-test-001`, `runs/microrank-merged-link-test-001`, `-002`. File thiết kế không đổi sau khi chạy.
- Không mở test, không đụng `data/locked/`, không sửa `src/`, không commit, không subagent.

## Bổ sung sau REVIEW: cờ và nhóm trace MicroRank

**Bằng chứng M-D bổ sung sau REVIEW.** Bảng cờ theo trace khớp nguồn ở 48 ca chạy được, 4 ca ERROR giữ N/A; không chạy PageRank. Cả 20 ca có caller trực tiếp trên root ở native đều có trace mất toàn bộ cờ của một caller nhưng vẫn A do root/dịch vụ khác; 19 ca còn caller trên root dưới M-D. Ví dụ dev-5467884de4 có 7 trace như vậy, root hạng 5 → 5; tổng A cùng 484 nhưng có 1 A → N và 1 N → A. Do đó tổng nhóm/hạng gần giữ chưa bác bỏ chờ. Nhóm A/N là nhóm yêu cầu/trace, không gộp các dịch vụ thành một nguyên nhân. Thiếu đối chứng native đúng cùng dataset/fault cho 20 ca; chưa tách tác dụng trọng số khi nhóm đổi. Nguồn: runs/sua-review-001/md-partition/attempt-003/summary.json → /cases (postanalysis, transitions); kiểm độc lập kiem-md-doc-lap.json. Chi phí cả ba lượt 4 phút 47 giây, giữ cả hai lượt lỗi.

Bằng chứng đầy đủ, giới hạn đối chứng và các lượt chạy được giữ ở runs/sua-review-001/bo-sung-sau-review.md. Đây là bổ sung sau phiên 13, không đổi số hay nhận xét lịch sử về chi phí/môi trường của chính phiên 13.
