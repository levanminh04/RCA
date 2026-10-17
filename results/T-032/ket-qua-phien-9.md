# T-032 — Kết quả phiên 9 (đêm 10–11/10/2026)

Người làm: Claude. File này gom bằng chứng thu được trong phiên 9, chưa phải báo cáo nghiệm thu. T-032 chưa xong; RQ2 và G2 chưa đóng.

**Trạng thái của các phép đổi:** thiết kế nằm ở `thiet-ke-phep-doi-001.md` và `thiet-ke-phep-doi-002.md`, viết trước khi chạy. Minh đã cho nối đoạn WHY ngày 11/10/2026 (WHY-44), nên số của các phép đổi được dùng trong báo cáo chính. Hai phép B-2 và S-1 được nghĩ ra sau khi xem bảng mô tả trên dev; kết quả của chúng chỉ là bằng chứng trên dev cho một ứng viên. A′ đã có trong WHY-40. Phân rã SimpleRCA, phân rã khối TORAI B và so hai bản ghi CIRCA chỉ đọc kết quả đã đóng băng hoặc trung gian đã khớp, không đổi phép tính nào.

**Cách đọc các số:** mọi số là trên tập dev (30 ca RE2-TT, 22 ca Nezha-OB). Hit@1 và Hit@5 tính bi quan khi hòa. Số của nhánh phép đổi đo tác động của một bước tính, không phải thành tích của một phương pháp. Các cột bằng chứng có thể chồng lấn, không cộng thành tỷ lệ nguyên nhân. Mỗi ô của dev chỉ có vài ca, nên không rút mẫu hình theo ô.

Đường dẫn dưới đây tính từ `results/T-032/`. File tổng hợp đã chép về laptop, hash hai đầu khớp; bảng chi tiết từng ca còn trên EC2 ở `~/rca/T-032/runs/<tên lượt>/cases/`.

## 1. Trung gian dùng được tới đâu

| Phương pháp | Số ca phát lại khớp từng bit với bản đóng băng | Nguồn |
|---|---|---|
| BARO | 52/52 | `runs/inherit-verify-001/result.json` → `/summary/baro` |
| SimpleRCA | 52/52 | cùng file → `/summary/simplerca` |
| MicroRank | 52/52 (48 OK, 4 ERROR tái lập đúng ERROR) | `runs/microrank-laptop-verify-001/result.json` → `/summary` |
| TraceRCA | xem mục 3 | EC2 `runs/tracerca-cohort-simple-001/segments/*/terminal.json` |
| CIRCA | chưa có; EC2 lệch bản đóng băng ở bit cuối | `runs/circa-k2-test-001/cases/dev-a5cabe5fa7/sham/check.json` |
| TORAI B | chưa phát lại; dùng 90 bản ghi đóng băng | `runs/torai-block-decomposition-001/summary.json` |

Ba dòng đầu là do tôi tự so lại bằng mã riêng, không dùng lại bộ kiểm của người làm trước.

## 2. MicroRank (biến thể "MicroRank-RCAEval sửa đầu vào")

Nguồn: `runs/microrank-core-aprime-c1-002/summary.json`. 48 ca OK; nhánh giữ nguyên trọng số tái lập điểm và thứ tự native từng bit ở 48/48; hạng root trùng T-028 ở 48/48.

**Quan sát.**

- Native xếp root hạng 1 ở 2/48 ca (RE2 2/26, Nezha 0/22); trong 5 hạng đầu ở 21/48 ca (`/summary/w_unit/all/hit1`, `/hit5`).
- Có 252 cặp (thực thể đứng trên root, root). Thực thể đó là caller của root ở 20 cặp, là dịch vụ được root gọi ở 46 cặp, không có quan hệ gọi trực tiếp với root ở 186 cặp (`runs/derived-tables-001/derived.json` → `/microrank/*/pairs_by_relation`).
- Tỷ lệ trace sau mốc bị xếp vào nhóm bất thường A: trung vị 0,50 ở RE2, 0,33 ở Nezha. Tỷ lệ trace A không chứa dịch vụ root: trung vị 0,53 ở RE2, 0,87 ở Nezha. Tỷ lệ trace A mà dịch vụ root có span vượt ngưỡng: trung vị 0,42 ở RE2, 0,08 ở Nezha (`runs/derived-tables-001/derived.json` → `/microrank/*/share_of_*`).
- Operation cho điểm cao nhất của thực thể đứng trên root có số trace "chỉ ngữ cảnh" (có mặt trong trace bất thường nhưng bản thân không vượt ngưỡng) lớn hơn số trace tự vượt ngưỡng ở 251/252 cặp; trong đó 9 cặp có số trace tự vượt ngưỡng bằng 0 (cùng file → `/microrank/*/max_operation_composition`).

**Phép A′, trọng số đơn vị** (`/summary/w_unit`). Root tăng hạng 12 ca, không đổi 31, giảm 5. Hit@1 từ 2 lên 11, toàn bộ ở RE2. 28/252 cặp không còn đứng trên root (RE2 25/132, Nezha 3/120). Không cặp caller nào đổi.

**Phép M-C1, đếm riêng thay đếm phủ** (`/summary/c1`). Root tăng hạng 33 ca, không đổi 10, giảm 5. Hit@1 từ 2 lên 19 (RE2 2 → 17, Nezha 0 → 2). Hit@5 từ 21 lên 33. 115/252 cặp không còn đứng trên root (RE2 89/132, Nezha 26/120). Cặp caller: 2/20 đổi.

**Kết luận ở mức tính toán.**

- RE2-TT: trong điều kiện khoảng một nửa trace sau mốc bị xếp vào A, bước đếm phủ của spectrum (tính một operation cho mọi trace A chứa nó) làm thông tin "operation nào tự bất thường" bị pha loãng: operation có mặt ở hầu hết trace nhận điểm cao. Đổi riêng bước này đưa root lên hạng 1 ở 15 trong 24 ca sai. Bước trọng số PageRank cũng tạo ưu thế ở 25/132 cặp; đổi riêng bước này đưa root lên hạng 1 ở 9 ca.
- Nezha-OB: trọng số không phải nơi tạo ưu thế. Đếm phủ giải thích 26/120 cặp. Phần còn lại chưa giải thích bằng hai bước này.
- Caller đứng trên root không do đếm phủ hay trọng số: 18/20 cặp caller giữ nguyên dưới M-C1, 20/20 dưới A′.

**Chưa trả lời.**

- Vì sao ở Nezha dịch vụ root hiếm khi có span vượt ngưỡng (trung vị 8% trace A). Các giải thích còn mở: tín hiệu nằm ở span phía gọi; lỗi không làm đổi thời lượng span của root; quy tắc 3σ theo từng operation không bắt được. Phép T-D ở mục 3 và phần ngữ nghĩa trace (Q-120) phân xử một phần.
- Bước chia trace bằng "một span vượt 3σ" thuộc bản RCAEval, không thuộc bài MicroRank gốc. Chưa biết bộ chia của bài gốc có cho tỷ lệ A khác không; muốn biết phải quyết định cách lấy thời lượng cả trace trên hai dataset này.
- Phép M-D (cờ theo thời lượng chưa được span con phủ) chưa chạy: cần chạy PageRank trên laptop mới tái lập được từng bit, chờ Minh quyết nơi tính.

## 3. TraceRCA (RCAEval `e2e/tracerca.py`, bản lọc hữu hạn)

Nguồn: `runs/tracerca-core-td-001/summary.json`; lượt phát lại ở `runs/tracerca-cohort-simple-001/segments/003/terminal.json` (52/52 khớp từng bit: 48 OK, 4 ERROR tái lập đúng ERROR). Bảng lõi dựng lại ji từ đầu vào của adapter và trùng ji native từng bit ở 48/48 ca; đẳng thức ji = 2a/(n + H) đúng ở 48/48, với a là số span vượt ngưỡng của operation, n là số span của nó sau mốc, H là tổng số span vượt ngưỡng. Một ca Nezha (`dev-7b7c973198`) root không có ji hữu hạn nên không được xếp; mẫu số còn 47.

**Quan sát.** Hit@1 23/47 (RE2 21/26, Nezha 2/21); Hit@5 36/47. Điểm của TraceRCA chỉ dùng span vượt ngưỡng của chính operation, không đếm ngữ cảnh. Có 90 cặp (thực thể đứng trên root, root): caller của root 22 cặp, dịch vụ được root gọi 16 cặp, không quan hệ gọi trực tiếp 52 cặp. Trung vị 64% tổng thời lượng span nằm trong khoảng được span con phủ.

**Phép T-D, cờ theo thời lượng chưa được span con phủ** (`/summary/all`, `/by_dataset`). Kiểm phép tính khoảng trên 8 trường hợp tự dựng đạt (`runs/tracerca-core-td-001/interval-fixtures.json`). Root tăng hạng 9 ca, không đổi 36, giảm 2. Hit@1 từ 23 lên 25; Hit@5 từ 36 lên 38. Số ca có caller đứng trên root từ 20 xuống 17. Trong 22 cặp caller: 18 cặp vẫn đứng trên root, 4 cặp không còn (RE2 3/5, Nezha 1/17).

**Kết luận ở mức tính toán.**

- Nezha-OB: giả thuyết "span của caller vượt ngưỡng vì khoảng thời gian của span con dài ra" bị bác bỏ ở 16/17 cặp caller. Phần của span caller không được span con phủ vẫn vượt ngưỡng.
- RE2-TT: giả thuyết đó được hỗ trợ ở 3/5 cặp caller. Mẫu nhỏ, chỉ là quan sát.
- TraceRCA xếp sai chủ yếu ở Nezha (19/21 ca sai hạng 1), và đa số thực thể đứng trên root không phải caller của root (58/75 cặp ở Nezha).

**Chưa trả lời.** Phần chưa được phủ của span caller dài ra vì đâu: thời gian giữa span phía gọi và span phía được gọi (mạng, hàng đợi trước khi dịch vụ được gọi bắt đầu xử lý), xử lý tại caller, hay span con không được ghi. Dữ liệu trace hiện có không phân biệt được ba khả năng này; cần ngữ nghĩa instrumentation đúng phiên bản dataset (Q-120). Hệ quả cho FlashTicket: muốn tách được thì phải ghi cả span phía gọi lẫn span phía được gọi cho mỗi lời gọi, kèm thời điểm bắt đầu xử lý ở phía được gọi.

## 4. SimpleRCA (M4)

Nguồn: `runs/simplerca-decomposition-002/summary.json`. Không can thiệp; phân rã cộng chính xác, đã kiểm bằng số ở 52/52 ca: điểm = phiếu metric + phiếu trace + phiếu log; phiếu metric của dịch vụ = tổng phiếu các cột.

**Quan sát.** Hit@1 32/52 (RE2 25/30, Nezha 7/22); Hit@5 47/52. Ở 20 ca sai hạng 1 có 64 cặp (thực thể đứng trên root, root). Cả 64 cặp có chênh phiếu metric dương. Ở 60/64 cặp, riêng kênh metric đã quyết định. Root có phiếu trace ở 27 ca và phiếu log ở 10 ca; root không có phiếu metric nào ở 4 ca Nezha.

**Kết luận ở mức tính toán.** Trong điều kiện một dịch vụ khác có nhiều mẫu metric vượt ngưỡng hơn root, phép cộng không cùng thang (phiếu metric đếm số mẫu, từ 0 tới 300 mỗi cột và cộng qua mọi cột; phiếu trace và log chỉ 0 hoặc 1) làm bằng chứng trace và log của root không thể bù. Đây là hạn chế của cách tính điểm.

**Quan sát thêm theo cột** (`runs/derived-tables-001/derived.json` → `/simplerca/summary`).

- RE2-TT, 20 cặp: thực thể đứng trên root không có quan hệ gọi trực tiếp với root ở 14 cặp, là caller ở 6 cặp. Cột có nhiều phiếu nhất của thực thể đó là cột mem ở 15 cặp, latency ở 5 cặp. Cột đó vượt ngưỡng ở trung vị 288 trên 300 mẫu sau mốc, tức gần như suốt cửa sổ. Ở 10/20 cặp, riêng một cột đó đã nhiều phiếu hơn tổng điểm của root.
- Nezha-OB, 44 cặp: metric chỉ có 5 mẫu sau mốc nên phiếu rất nhỏ (cột nhiều phiếu nhất có trung vị 2). Root có trung vị 0 phiếu metric. Thực thể đứng trên root có nhiều cột có phiếu hơn root ở 37/44 cặp.

**Phép S-1, đếm theo cột thay cho đếm theo mẫu** (`runs/simplerca-s1-001/summary.json` → `/summary`; nhánh giữ nguyên khớp bản đóng băng từng bit ở 52/52). Ở RE2, 16/20 cặp đứng trên root biến mất, nhưng 21 cặp mới xuất hiện và số nhóm hòa giảm từ 1.440 xuống 207 trên 2.041 thực thể: điểm trở thành số nguyên nhỏ, rất nhiều dịch vụ hòa nhau. Hit@1 tính bi quan theo hòa giảm từ 25 xuống 10 ở RE2 (tính lạc quan: 25 xuống 23). Ở Nezha, 8/44 cặp biến mất, Hit@1 từ 7 xuống 5.

**Kết luận ở mức tính toán.** Ở RE2, đếm theo số mẫu đúng là bước tạo ưu thế cho 16/20 cặp đứng trên root. Nhưng chính bước đó cũng là thứ cho SimpleRCA khả năng phân biệt: bỏ nó thì root hòa với nhiều dịch vụ khác. Hạn chế nằm ở chỗ điểm không tách được "một cột lệch kéo dài" khỏi "nhiều kênh cùng lệch", không sửa được bằng cách đổi cách đếm.

**Chưa trả lời.** Vì sao cột mem của dịch vụ khác vượt ngưỡng gần suốt cửa sổ ở RE2. Ứng viên: nền của cột mem gần như phẳng nên ngưỡng mean + 3·std rất sát, một dịch chuyển nhỏ cũng vượt. Chưa có phép đổi nào kiểm ứng viên này. Số cột metric nhiều hơn không phải lời giải thích ở RE2 (1/20 cặp).

## 5. BARO

Nguồn: `runs/baro-b1-001/summary.json`. Nhánh giữ nguyên khớp bản đóng băng từng bit ở 52/52 ca.

**Quan sát.** Hit@1 29/52 (RE2 21/30, Nezha 8/22); Hit@5 42/52. Ở 9 ca sai của RE2, cột cho điểm cao nhất của các thực thể đứng trên root là mem ở 55 lượt, latency 24, cpu 23 (`runs/derived-tables-001/derived.json` → `/baro/summary/RE2-TT/entity_best_column_kind`). Ở Nezha chủ yếu là các cột latency phía client/server và lưu lượng mạng.

**Phép B-1, không lọc cột hằng.** Hạng root không đổi ở 52/52 ca. Root có thêm cột được giữ lại ở 38 ca, nhưng cột tốt nhất của root không lần nào là cột đó.

**Kết luận ở mức tính toán.** Giả thuyết "bước lọc cột hằng làm mất kênh quyết định hạng của root" bị bác bỏ trên 52 ca dev, dưới chính quy tắc scale của thư viện. Bước lọc có bỏ cột của root, nhưng không phải bước làm root mất hạng.

**Quan sát thêm về thang chuẩn hóa** (`runs/derived-tables-001/derived.json` → `/baro/summary`; median và IQR lấy từ chuỗi BARO đã lưu của 52 lượt phát lại).

- RE2-TT, 103 cặp ở 9 ca sai: cột thắng của thực thể đứng trên root có IQR nền bằng trung vị 0,4% của median nền, và mức lệch tại đỉnh bằng trung vị 3,5% của median nền. Khi root đứng hạng 1, cột thắng của root lệch gấp trung vị 96 lần median nền.
- Ở 54/103 cặp RE2, thực thể đứng trên root có mức lệch tương đối nhỏ hơn root nhưng z lớn hơn. Ở 63/103 cặp, tỷ lệ IQR trên median của nó nhỏ hơn của root.
- Nezha-OB, 59 cặp: tỷ lệ IQR trên median của thực thể đứng trên root nhỏ hơn của root ở 41 cặp; mức lệch tương đối lớn hơn root ở 32 cặp.
- Đỉnh z của thực thể đứng trên root xuất hiện trước đỉnh của root ở 65/103 cặp RE2 và 25/59 cặp Nezha.

**Phép B-2, thang độ lệch chuẩn thay cho thang IQR** (`runs/baro-b2-001/summary.json` → `/summary`). Ở RE2: root tăng hạng 7 ca, không đổi 22, giảm 1; Hit@1 từ 21 lên 24, không ca đúng nào mất hạng 1; 43/103 cặp đứng trên root biến mất, 6 cặp mới xuất hiện. Ở Nezha (metric chỉ có 5 mẫu mỗi phía): tăng 7, không đổi 8, giảm 7; Hit@1 từ 8 xuống 7.

**Kết luận ở mức tính toán.** Ở RE2, trong điều kiện cột của dịch vụ khác gần như phẳng ở đoạn nền, việc chia cho IQR nền tạo ưu thế cho 43/103 cặp đứng trên root; đổi riêng thang đưa root lên hạng 1 ở 3 trong 9 ca sai. 60/103 cặp còn lại vẫn đứng trên root dưới thang độ lệch chuẩn, nên phần này không riêng của IQR. Ở Nezha phép đổi không cho kết luận, vì 5 mẫu không đủ để ước lượng thang nào ổn định.

**Chưa trả lời.** Các thay đổi nhỏ ở mem/cpu của dịch vụ khác là do sự cố hay là trôi tự nhiên; kiểm được bằng xu hướng của chính cột đó trong đoạn nền.

## 6. CIRCA (chỉ RE2-TT)

Nguồn: `runs/circa-k1-002/k1.json`, so hai bản ghi đóng băng `ols+rht` và `ols+rht_da` của cùng lượt chấm. Hạng root của nhánh DA do tôi suy ra trùng T-028 ở 30/30 ca.

**Quan sát.** Thêm bước DA (điều chỉnh theo hậu duệ): root tăng hạng 5 ca, không đổi 15, giảm 10. Hit@1 từ 12 lên 16; Hit@5 từ 26 lên 27. Nút của `ts-admin-travel-service` mang giá trị vượt 1e10 và đứng trên root ở bảng không DA trong 11 ca.

- Ba ca root tăng hạng có root `ts-travel-service`, dịch vụ được `ts-admin-travel-service` gọi: khóa DA của root nhận giá trị cỡ 1e16 và lên hạng 1.
- Bảy ca root giảm hạng có root `ts-train-service` hoặc `ts-route-service`: các caller của root (`ts-travel-service`, `ts-travel2-service`) nhận giá trị cực lớn đó và vượt root.

**Suy luận, chưa xác nhận.** Bước DA cộng điểm của hậu duệ vào tổ tiên trong đồ thị metric, nên một giá trị cực lớn do lỗi số học đã biết (Q-82) kéo cả chuỗi tổ tiên lên. Ít nhất 10 trong 15 ca DA làm đổi hạng root chịu tác động này (`runs/derived-tables-001/derived.json` → `/circa_k1_changed_cases`). Vì vậy không đọc được "cấu trúc gọi giúp" hay "hại" từ số Hit của nhánh DA khi chưa tách phần do giá trị cực lớn.

**Chưa làm được.** Lõi CIRCA và phép K-2 (đồ thị không cạnh): EC2 không tái lập bản đóng băng từng bit ở ca thử `dev-a5cabe5fa7` (264 và 149 trường khác ở hai biến thể; hai ví dụ đã xem lệch 1 và 4 đơn vị ở bit cuối của điểm RHT). Bản đóng băng sinh trên laptop. Cần Minh quyết nơi phát lại.

## 7. TORAI B (chỉ RE2-TT, ba seed)

Nguồn: `runs/torai-block-decomposition-001/summary.json`, 90 bản ghi đóng băng. Hạng root dựng từ khối trùng T-028 ở 90/90.

**Quan sát.** Ba seed cho cùng hạng và cùng nhánh ở 30/30 ca. Hit@1 26/30 ca. Khối của root là cụm một dịch vụ ở 81/90 đơn vị, do nhánh dự phòng xếp ở 9, do nhánh nhân quả RCD xếp ở 0. Trên toàn bộ có 342 khối nhiều dịch vụ, 302 khối rơi nhánh dự phòng. Bốn ca sai: ba ca do khối của root không đứng đầu, một ca do nhóm khác đứng trước trong khối đầu.

**Kết luận ở mức mô tả.** Trên dev RE2-TT, vị trí của root do điểm cụm và nhánh dự phòng quyết định; bước RCD không quyết định thứ tự của root ở đơn vị nào.

**Chưa trả lời.** Vì sao cụm của root có điểm thấp ở ba ca. Cần điểm severity từng dịch vụ, không có trong bản ghi. Việc cần chạy: phát lại TORAI B trên EC2 cho bốn ca sai và đối chứng đúng cùng ô, lưu `y_train`, `y_pred`, `cluster_rank`.

## 8. Câu trọng tâm: caller đứng trên root

Nguồn: `runs/caller-root-phien9-001/caller-root.json`. Quan hệ gọi lấy từ cặp span cha–con khác dịch vụ của chính ca đó. Cách xác định này khác cờ M5 của T-028, nên số ca không trùng số M5; đây là mô tả vị trí, không phải nhãn lan.

| Phương pháp | RE2-TT: ca có caller trên root / ca xét được | Nezha-OB | Số cặp caller |
|---|---|---|---|
| MicroRank | 5/26 | 15/22 | 20 |
| TraceRCA | 4/26 | 16/21 | 22 |
| SimpleRCA | 5/26 | 9/22 | 15 |
| BARO | 2/26 | 7/22 | 13 |
| CIRCA (có DA) | 9/30 | không hỗ trợ | 17 |

Con trỏ: `/summary/<phương pháp>/<dataset>`. Bốn ca RE2 mà TraceRCA trả ERROR không có bảng span nên bị loại khỏi mẫu số của bốn phương pháp đầu.

Trả lời câu P4 "phương pháp chấm thời gian chờ dịch vụ phụ thuộc thành bất thường của caller, hay cách chấm đã ưu tiên caller", ở mức tính toán và chỉ trên dev (`/summary/evidence`):

- **Cách chấm không ưu tiên caller.** MicroRank: 20/20 cặp caller giữ nguyên khi bỏ trọng số, 18/20 giữ nguyên khi chỉ đếm trace tự vượt ngưỡng; cả 20 caller đều có span tự vượt ngưỡng. SimpleRCA: 15/15 cặp caller có nhiều mẫu metric vượt ngưỡng hơn root. BARO không nhận quan hệ gọi nào trong đầu vào.
- **Thời gian của span con giải thích ít.** TraceRCA: 18/22 cặp caller vẫn đứng trên root khi chỉ tính phần span không được span con phủ.
- **Còn mở:** phần không được phủ của span caller là gì về mặt vật lý. Chưa có bằng chứng nào trong phiên này xác lập "caller chờ root".
- **Caller không phải nhóm chính.** Ở cả hai phương pháp trace, đa số thực thể đứng trên root không có quan hệ gọi trực tiếp với root (MicroRank 186/252 cặp, TraceRCA 52/90 cặp).

Hệ quả cho P5–P6, ở mức đề xuất ứng viên, chưa phải lựa chọn thiết kế:

- Ứng viên "tách bất thường tự sinh và kế thừa theo đồ thị" (MRP P6 tầng 2) không nhắm trúng phần lớn ca sai của MicroRank trên RE2; ở đó bước đếm phủ mới là nơi mất thông tin.
- Ở Nezha, tín hiệu của root hiếm khi nằm trong span của chính root. Một phương pháp chỉ gắn điểm vào nút sẽ thiếu thông tin; thông tin gắn vào cạnh gọi (span phía gọi của lời gọi tới root) là ứng viên cần xét.
- CIRCA cho thấy lan điểm theo cấu trúc rất nhạy với giá trị cực lớn ở một nút. Thành phần lan điểm trên đồ thị phải có cách chặn giá trị không hợp lệ.
