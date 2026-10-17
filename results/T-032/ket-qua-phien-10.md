# T-032 — Kết quả phiên 10 (rạng sáng 11/10/2026)

Người làm: Claude. File này gom bằng chứng thu được trong phiên 10 cho mục 1–6 của kế hoạch 8 mục (cuối LOG phiên 9). Đây chưa phải báo cáo nghiệm thu; báo cáo chính (`nguyen-nhan-xep-hang.md`) được viết ở phiên sau theo quyết định Q-131 mục 13. T-032 chưa xong; RQ2 và G2 chưa đóng. File nối tiếp `ket-qua-phien-9.md`, không thay nó.

**Cách đọc các số.** Mọi số là trên tập dev (30 ca RE2-TT, 22 ca Nezha-OB). Hit@1, Hit@5 tính bi quan khi hòa. Số của nhánh phép đổi đo tác động của một bước tính, không phải thành tích của một phương pháp. Các cột bằng chứng có thể chồng lấn, không cộng thành tỷ lệ nguyên nhân. Mỗi ô của dev chỉ có vài ca, nên không rút mẫu hình theo ô. Đường dẫn tính từ `results/T-032/`; con trỏ JSON ghi sau dấu `→`.

**Thiết kế viết trước khi chạy:** `thiet-ke-phep-doi-003.md` (cách thực hiện K-2 và M-D trên laptop, nhánh quan sát CIRCA), `thiet-ke-bang-mo-ta-004.md` (các bảng mô tả A, B, C, C2 và phép thử giả), `thiet-ke-phep-doi-005.md` (K-2 theo loại cạnh), `thiet-ke-phep-doi-006.md` (phép đổi nguồn log của TORAI B). Mỗi file ghi rõ điều tôi đã thấy trước khi viết; phần nào được thêm sau khi đã xem kết quả đều ghi mốc thời gian và lý do.

**Tự soát:** 145 con số của mục 1–6 và các con số của mục 7–8 được so với file kết quả bằng `scripts/self_check_phien10_v1.py` (kết quả ở `runs/self-check-phien10-001/`). Các chỗ kết luận đã sửa sau khi soát được ghi ở LOG phiên 10, mục "tự soát".

## 1. CIRCA trên laptop (chỉ RE2-TT, 30 ca)

Nguồn: lượt `runs/circa-laptop-k2-001/` (script `scripts/laptop_contrast_v1.py`); tổng hợp `runs/circa-laptop-k2-001/collect-001/summary.json` và `runs/circa-laptop-k2-001/collect-002/regression-decomposition.json`.

### 1.1 Lõi CIRCA nay đã có

- Nhánh sham (đường native nguyên vẹn) tái lập hai bản ghi `ols+rht_da` và `ols+rht` trùng bản đóng băng từng bit ở 30/30 ca (`collect-001/summary.json` → `/summary/sham_exact`). Nhánh quan sát (thêm lớp bọc chỉ-đọc quanh `score_graph`) cũng trùng từng bit ở 30/30 ca (`/summary/obs_exact`); điểm RHT trong trung gian trùng điểm trong bản ghi ở 30/30 ca (`/summary/obs/snapshot_rht_equals_record`).
- Hạng root của bản ghi có DA trùng hạng đã chấm ở T-028 ở 30/30 ca (`/summary/self_check_da_rank_equals_t028`). Tác dụng của DA lên hạng root tính lại từ lượt này (tăng 5, không đổi 15, giảm 10; `/summary/da_effect_on_root`) trùng kết quả K-1 của phiên 9.
- Phiên 9 ghi EC2 lệch bản đóng băng ở bit cuối; trên laptop không lệch ở ca nào. Lõi CIRCA dùng được.

### 1.2 Giá trị cực lớn sinh ra ở bước nào

**Quan sát** (`collect-001/summary.json` → `/summary/obs`):

- 11/30 ca có đúng một nút mang điểm RHT vượt 1e10, và ở cả 11 ca đó là nút `ts-admin-travel-service_latency` (`/huge_node_names`).
- Ở cả 11 nút, y của đoạn train chỉ gồm 2 giá trị khác nhau (`/huge_node_train_y_n_unique`), độ lệch chuẩn từ 7,5e-17 tới 1,3e-16 (`/huge_node_train_y_std`): cột này đứng yên ở đoạn train, chỉ dao động ở mức làm tròn.
- Scale của phần dư train từ 1,3e-17 tới 2,4e-17 (`/huge_node_residual_scale`). Ở đoạn test, giá trị lệch khỏi mức train từ 0,205 tới 9,27 đơn vị, trung vị 0,67 (`/huge_node_test_shift_abs`): có thay đổi thật ở đoạn test, nhưng mẫu số ở mức làm tròn.
- Khi bỏ mọi cạnh (K-2), nút đó không còn cực lớn ở ca nào: 0/11 (`/huge_nodes_still_huge_without_edges`; `/summary/k2_all/node_counts_total/huge_k2` = 0).

**Kết luận ở mức tính toán.** Trong điều kiện một cột metric đứng yên ở 111 điểm train rồi đổi ở 10 điểm test, bước "hồi quy nút theo các nút cha rồi chuẩn hóa phần dư test theo độ lệch chuẩn phần dư train" làm mất thang của độ lệch: một thay đổi cỡ 0,2–9,3 đơn vị thành điểm cỡ 1e16. Bằng chứng can thiệp: cùng nút, cùng dữ liệu, không có cha thì điểm hữu hạn ở 11/11 ca. Đây là xác nhận trên lượt OLS đã khóa cho điều WHY-36 đã ghi từ chẩn đoán trên lượt SVR. Hạn chế này thuộc cách tính (phép kiểm cột hằng của thư viện áp trên phần dư chứ không trên y), có ở cả code CIRCA gốc lẫn RCAEval theo WHY-36.

### 1.3 Giá trị cực lớn đi qua bước DA như thế nào

**Quan sát** (`/summary/obs/da_huge_by_source_total`, `/summary/da_changed_cases_by_huge`):

- 52 nút mang khóa DA vượt 1e10: 11 nút tự có, 41 nút nhận qua `child_score`, 0 nút không rõ nguồn.
- Root có nút mang khóa DA cực lớn ở 3 ca (`/cases_root_has_da_huge_node`); cả ba là các ca root tăng hạng khi thêm DA và ở cả ba root nhận qua `child_score` (`/cases/*/obs/root_da_huge_source`).
- Trong 10 ca root giảm hạng khi thêm DA, 7 ca có thực thể đứng trên root mang khóa cực lớn; ở cả 7 ca, thực thể đó không đứng trên root ở bảng không có DA (tính từ `/cases/*/views/native_rht/above_root` và `/native_da/above_root`).

**Kết luận ở mức tính toán.** Suy luận của phiên 9 (bước DA cộng điểm của hậu duệ vào tổ tiên, nên một giá trị cực lớn kéo cả chuỗi tổ tiên lên) được xác nhận ở mức từng nút và không có phản ví dụ: không nút nào mang khóa cực lớn mà thiếu nguồn. Ở 3 trong 5 ca "DA giúp", root lên hạng nhờ nhận giá trị cực lớn; ở 7 trong 10 ca "DA hại", thực thể vượt root là thực thể vừa nhận giá trị cực lớn qua DA. Mười ca này vì vậy không đọc được như tác dụng của cấu trúc gọi. Năm ca đổi hạng còn lại (2 tăng, 3 giảm) không dính giá trị cực lớn; số quá ít để kết luận.

**Hướng cạnh.** Trong 30 đồ thị metric có 7.220 cạnh nối hai metric của cùng dịch vụ, 1.642 cạnh đi từ metric của dịch vụ được gọi sang metric của dịch vụ gọi, 1.344 cạnh theo chiều ngược lại, 125 cạnh giữa hai dịch vụ gọi lẫn nhau, 598 cạnh giữa hai dịch vụ không có lời gọi trực tiếp trong đoạn nền (`/summary/obs/edge_direction_vs_calls_total`).

### 1.4 Phép K-2: chấm RHT với đồ thị không cạnh

Thiết kế: bản 001 mục 8, bản 003 mục 2. Bước duy nhất bị đổi: bỏ mọi cạnh của đồ thị metric, giữ tập nút (220–556 cạnh mỗi ca; tập nút giống native ở 30/30 ca).

**Quan sát** (`collect-001/summary.json` → `/summary/k2_all`, `/k2_cases_with_huge_node`, `/k2_cases_without_huge_node`):

| Nhóm ca | Bỏ cạnh làm root tăng hạng / không đổi / giảm hạng | Hit@1 có cạnh → không cạnh | Hit@5 có cạnh → không cạnh |
|---|---|---|---|
| Cả 30 ca | 12 / 14 / 4 | 12 → 21 | 26 → 24 |
| 11 ca có nút vượt 1e10 | 10 / 1 / 0 | 0 → 9 | 9 → 9 |
| 19 ca còn lại | 2 / 13 / 4 | 12 → 12 | 17 → 15 |

- Ở mức nút: trong 4.526 nút có hồi quy theo cha, điểm native cao hơn điểm không cạnh ở 3.285 nút, thấp hơn ở 1.161 nút, bằng nhau ở 80 nút (`/summary/k2_all/node_counts_total`).
- Cặp (thực thể đứng trên root ở bảng RHT native, root): với thực thể là caller của root, 7 cặp còn và 8 cặp mất khi bỏ cạnh (cả 8 thuộc nhóm ca có nút cực lớn); với thực thể không có lời gọi trực tiếp với root, 54 còn và 17 mất (`/pairs_above_root_native_rht_under_k2`).
- Phân rã đại số của điểm (`collect-002/regression-decomposition.json` → `/summary`), tính được cho 4.407 nút (loại 11 nút cực lớn, 82 nút có tử hoặc mẫu bằng 0, 26 nút dựng lại lệch điểm thật quá 1e-6): tỷ số điểm = f_num / f_den, với f_den = scale phần dư train / độ lệch chuẩn y train và f_num = độ lệch lớn nhất của phần dư test / độ lệch lớn nhất của y test. Trung vị f_den 0,93; f_num ≥ 1 ở 2.588/4.407 nút. Trung vị tỷ số điểm tăng theo số cha: 1,05 với 1 cha (3.256 nút), 1,22–1,46 với 2–4 cha (372 nút), 2,99 với 5 cha (382 nút), 3,44 với 6 cha (150 nút), 6,27 với 7 cha (56 nút), 8,43 với từ 8 cha trở lên (191 nút) (`/by_n_parents`; khóa "8" gộp mọi nút có từ 8 cha).

**Kết luận ở mức tính toán.**

- Dự đoán H-giải-thích của thiết kế (hồi quy theo cha làm giảm điểm của nút được cha giải thích) không đúng với phần lớn nút trên dữ liệu này: hồi quy làm tăng điểm ở 3.285/4.526 nút. Cơ chế theo phân rã: trong điều kiện fit trên 111 điểm trước mốc và chấm trên 10 điểm cuối cửa sổ, hồi quy làm scale phần dư train nhỏ đi, còn phần dư test không nhỏ đi tương ứng (ở 2.588/4.407 nút phần dư test còn lớn hơn độ lệch thô của y).
- Ở 19 ca không có nút cực lớn, bỏ cạnh không đổi Hit@1 (12 → 12) và làm Hit@5 giảm 2 ca (17 → 15): hồi quy theo cấu trúc có giúp root ở 4 ca và làm root kém đi ở 2 ca. Mẫu nhỏ; không kết luận được cấu trúc có lợi hay hại.
- Ở 11 ca có nút cực lớn, có cạnh thì root không lần nào đứng hạng 1 ở bảng RHT; bỏ cạnh thì 9/11. Ở 6 trong 11 ca, thực thể duy nhất đứng trên root là thực thể mang giá trị cực lớn, và cả 6 ca đó root lên hạng 1 khi bỏ cạnh: với 6 ca này nguyên nhân là giá trị cực lớn ở mục 1.2. Ở 3 ca lên hạng 1 còn lại còn có thực thể khác đứng trên root, nên phần tăng không quy riêng được cho giá trị cực lớn.

**Chưa trả lời, và phép kiểm cụ thể.**

- K-2 bỏ mọi cạnh cùng lúc nên không cho biết loại cạnh nào tạo ra phần tăng điểm. Đã chạy hai nhánh theo loại cạnh sau khi Minh duyệt; kết quả ở mục 7.
- Chưa tách "hồi quy tăng điểm" là do số điểm train ít so với số cha hay do đoạn test nằm cuối cửa sổ. Phép kiểm cần đổi cửa sổ train/test của CIRCA, tức đổi giao thức đã khóa; không làm trong T-032.

## 2. MicroRank, phép M-D: cờ theo thời lượng chưa được span con phủ

Nguồn: lượt `runs/microrank-md-001/` (script `scripts/laptop_contrast_v1.py` cho 58 tiến trình con đầu, `_v2.py` cho phần còn lại; v2 chỉ khác ở đường báo lỗi của ca nguồn ERROR); tổng hợp `runs/microrank-md-001/collect-001/summary.json`. Thiết kế: bản 001 mục 4, bản 003 mục 3.

**Kiểm.** Nhánh sham (hàm `microrank` dựng lại từ mã nguồn native với cột cờ bằng `duration`) trùng bản đóng băng từng bit ở 52/52 ca: 48 OK và 4 ERROR tái lập đúng ERROR (`/summary/sham_exact`, `/sham_exact_by_source_status`). Hạng root native trùng T-028 ở 48/48 (`/summary/self_check_native_rank_equals_t028`). Tám trường hợp khoảng tự dựng của hàm `uncovered` đạt ở mọi lượt con của nhánh md. Bốn ca nguồn ERROR cũng ERROR dưới M-D (lỗi thiếu nền của operation không phụ thuộc đại lượng cờ); mẫu số còn 48.

**Quan sát** (`/summary/all`, `/RE2-TT`, `/Nezha-OB`):

| | RE2-TT (26 ca) | Nezha-OB (22 ca) | Cộng (48 ca) |
|---|---|---|---|
| Root tăng hạng / không đổi / giảm hạng | 1 / 20 / 5 | 2 / 15 / 5 | 3 / 35 / 10 |
| Hit@1 native → M-D | 2 → 3 | 0 → 1 | 2 → 4 |
| Hit@5 native → M-D | 13 → 12 | 8 → 8 | 21 → 20 |
| Cặp caller đứng trên root: còn / mất | 5 / 0 | 14 / 1 | 19 / 1 |
| Mọi cặp đứng trên root: còn / mất | 131 / 1 | 117 / 3 | 248 / 4 |
| Cặp mới xuất hiện | 11 | 6 | 17 |
| Số span mang cờ, M-D so với native (trung vị) | 0,66 | 0,79 | 0,74 |
| Tỷ lệ trace vào nhóm A, native → M-D (trung vị) | 0,50 → 0,51 | 0,33 → 0,39 | 0,42 → 0,47 |

**Kết luận ở mức tính toán.** Trong điều kiện một trace vào nhóm bất thường khi có bất kỳ span nào mang cờ, đổi đại lượng cờ từ thời lượng span sang phần chưa được span con phủ làm số span mang cờ giảm còn trung vị 74% nhưng gần như không đổi phân hoạch trace và thứ hạng: 248/252 cặp đứng trên root giữ nguyên. Giả thuyết H-con (caller đứng trên root vì span của nó dài ra theo span con) không được hỗ trợ ở MicroRank: 19/20 cặp caller giữ nguyên. Thứ hạng của MicroRank vì vậy ít nhạy với việc span của dịch vụ nào mang cờ. Trong các phép đổi đã chạy, phép làm đổi nhiều cặp nhất vẫn là đếm riêng thay đếm phủ (M-C1 của phiên 9: 115/252 cặp); 137 cặp còn lại chưa được phép đổi nào giải thích.

**Giới hạn.** M-D đổi cả phân hoạch nên là tác động tổng. Nó không cho biết phần chưa được phủ của span caller là gì về mặt vật lý.

## 3. Bảng A — tín hiệu của root nằm ở đâu trong trace (mô tả, không phải phương pháp)

Nguồn: `runs/root-signal-location-001/summary.json` (EC2, script `scripts/root_signal_location_v1.py`); phép thử giả `runs/root-signal-placebo-002/summary.json` (mốc giả t − 150 s, script `_v3.py`) và `runs/root-signal-placebo-003/summary.json` (mốc giả ở điểm giữa đoạn nền, script `_v4.py`). Định nghĩa viết trước khi chạy: `thiet-ke-bang-mo-ta-004.md` mục 2; phép thử giả ở mục 4 và 4b, viết sau khi thấy kết quả chính và trước khi chạy phép thử.

**Năm vị trí.** `own_d`: span của chính dịch vụ, cờ theo thời lượng (đúng cờ của hai phương pháp trace). `own_u`: span của chính dịch vụ, cờ theo phần chưa được span con phủ. `in_d`, `in_u`: span phía gọi của các lời gọi tới dịch vụ đó, theo hai đại lượng trên. `in_d_edge`: như `in_d` nhưng nền lấy theo cặp (operation phía gọi, dịch vụ được gọi). Mỗi dịch vụ có tỷ lệ span mang cờ ở từng vị trí; "root đứng đầu" nghĩa là tỷ lệ của root lớn hơn hẳn mọi dịch vụ khác trong ca.

**Kiểm.** 48 ca có bảng span (26 RE2-TT, 22 Nezha-OB); 4 ca RE2 nguồn ERROR không có bảng span, giữ trong mẫu số với trạng thái N/A. Tổng số cờ `own_d` và `own_u` tính lại bằng đúng tổng H của lượt T-D ở 48/48 ca (`/summary/self_check`). Mỗi span phía gọi có đúng một span con thuộc dịch vụ khác ở mọi ca (`/cases/*/structure/caller_side_spans_by_cross_children`).

**Quan sát** (`/summary/by_dataset/<dataset>/positions/<vị trí>`; cột "thử giả" lấy từ lượt 003, cùng con trỏ):

| Vị trí | RE2-TT: root đứng đầu / ca root có span ở vị trí đó | RE2-TT thử giả | Nezha-OB: root đứng đầu / ca có span | Nezha-OB thử giả |
|---|---|---|---|---|
| own_d | 8/26 | 1/26 | 9/22 | 4/22 |
| own_u | 26/26 | 0/26 | 10/22 | 3/22 |
| in_d | 18/20 | 2/20 | 11/20 | 0/20 |
| in_u | 19/20 | 1/20 | 13/20 | 4/20 |
| in_d_edge | 18/20 | 0/20 | 11/20 | 0/20 |

- Trung vị tỷ lệ span mang cờ của root ở bảng chính: RE2-TT `own_d` 15,8%, `own_u` 11,2%, `in_d` 37,6%; Nezha-OB `own_d` 6,0%, `own_u` 4,9%, `in_d` 77,3%, `in_u` 47,8% (`/positions/*/share/median`). Ở phép thử giả các tỷ lệ này từ 0% tới 2,3%.
- Ghép vị trí (`/summary/by_dataset/*/cross`): RE2-TT có 18/26 ca root đứng đầu ở ít nhất một vị trí "phía gọi" nhưng không đứng đầu theo `own_d`, 6 ca chỉ đứng đầu theo `own_d`, 2 ca cả hai. Nezha-OB: 8/22 chỉ phía gọi, 2 chỉ `own_d`, 7 cả hai, 5 không vị trí nào.
- Theo loại lỗi ở Nezha-OB (`/summary/by_dataset_fault`): `network_delay` (6 ca) có `own_d` đứng đầu 1/6, `in_u` đứng đầu 5/6, trung vị tỷ lệ `own_d` 2,6% so với `in_u` 96,3%; `cpu_contention` (5 ca) có cả ba vị trí phía gọi đứng đầu 5/5, `own_d` 2/5; `return` (4 ca) có 3/4 ca root không đứng đầu ở vị trí nào và trung vị tỷ lệ dưới 2% ở mọi vị trí; `exception` (3 ca) `own_d` 2/3; `cpu_consumed` (4 ca) `own_d` 3/4.
- Dữ kiện về dữ liệu, thấy khi chạy phép thử giả: bảng span của Nezha-OB chỉ phủ từ 41,5 tới 97,0 giây trước mốc (trung vị 77,8 giây) và từ 84 tới 140 giây sau mốc; RE2-TT phủ đủ 300 giây mỗi phía (`runs/root-signal-placebo-003/summary.json` → `/cases/*/structure/earliest_start_minus_t_s`, `latest_end_minus_t_s`).

**Phép thử giả.** Ở RE2-TT, với mốc giả lùi 150 giây (không có lỗi trong khoảng xét), root đứng đầu 0–2 ca ở mỗi vị trí, đúng cỡ ngẫu nhiên (27 dịch vụ). Ở Nezha-OB, phép thử t − 150 s không áp dụng được vì không có span nào trước mốc giả; với mốc giả ở điểm giữa đoạn nền (nền chỉ còn khoảng 20–48 giây), root đứng đầu 0–4 ca, mức ngẫu nhiên khoảng 2/22 với 10 dịch vụ. Vậy bảng chính không thiên vị root về cấu trúc ở RE2-TT; ở Nezha-OB phép thử yếu hơn vì nền ngắn, và 3–4 ca đứng đầu ở `own_d`, `own_u`, `in_u` cao hơn mức ngẫu nhiên một chút.

**Kết luận ở mức mô tả, chỉ trên dev.**

- RE2-TT: trong 26 ca có bảng span, phần chưa được span con phủ của span của chính root (`own_u`) tách được root ở 26/26 ca, trong khi cờ theo thời lượng mà hai phương pháp trace đang dùng (`own_d`) chỉ tách được 8/26. Thông tin để định vị root có trong trace. Ở 18 ca root không đứng đầu theo `own_d`, dịch vụ đứng đầu là `ts-admin-travel-service` ở 14 ca, `ts-inside-payment-service` ở 3 ca, `ts-preserve-service` ở 1 ca; đó là dịch vụ gọi trực tiếp root ở 9/18 ca (tính từ `/cases/*/top_service_by_position/own_d` và `/root_callers`). Cờ theo thời lượng vì vậy đẩy lên các dịch vụ nằm phía trên trong chuỗi gọi, không chỉ dịch vụ gọi trực tiếp root.
- Nezha-OB: với lỗi trễ mạng, tín hiệu nằm ở span phía gọi của lời gọi tới root (5/6 ca), gần như không nằm ở span của root. Với lỗi `return`, trace không mang tín hiệu thời lượng ở vị trí nào (3/4 ca). Đây là câu trả lời cho câu phiên 9 để mở "vì sao ở Nezha span của root hiếm khi vượt ngưỡng": với 6 ca trễ mạng tín hiệu nằm trên lời gọi; với 4 ca `return` lỗi không làm đổi thời lượng; 12 ca còn lại root có tín hiệu ở span của mình ở mức khác nhau.
- Đối chiếu với kênh metric (cùng file, `/cases/*/baro`, `/simplerca`, `/tracerca_t028`): trên 26 ca RE2 này BARO xếp root hạng 1 ở 18 ca, SimpleRCA 21, TraceRCA 21. Ở Nezha-OB, 5 ca root không đứng đầu ở vị trí trace nào cũng là các ca BARO xếp sai cả 5 và SimpleRCA xếp đúng 1; phiếu metric của root ở 5 ca đó là 0, 9, 0, 3, 6. Với các ca này tín hiệu của root yếu ở cả trace lẫn metric.
- Ứng viên cho đầu ra P4 số 4, chưa phải lựa chọn thiết kế: quan hệ gọi bổ sung được đúng thông tin "span phía gọi của lời gọi tới X vượt nền" và "phần của span không do span con phủ". Một cách chấm chỉ nhìn span của từng dịch vụ sẽ gán tín hiệu của lời gọi cho dịch vụ gọi.

**Giới hạn.** "Root đứng đầu theo một vị trí" là mô tả nơi có thông tin, không phải Hit@1 của một phương pháp, và không so được với Hit của sáu phương pháp. Các định nghĩa vị trí được đặt sau khi đã thấy kết quả T-D của phiên 9. 26 và 22 ca dev, 6 và 5 loại lỗi; chưa có ca test nào. Quan hệ cha–con khác dịch vụ không chứng minh chờ đồng bộ. Con số 26/26 không được dùng làm dự báo độ chính xác của phương pháp đồ thị.

## 4. Bảng B — xu hướng nền của cột thắng ở BARO và SimpleRCA (chỉ RE2-TT)

Nguồn: `runs/baseline-trend-001/summary.json` (EC2, script `scripts/baseline_trend_v1.py`). Định nghĩa và mốc chia nhóm viết trước: `thiet-ke-bang-mo-ta-004.md` mục 3. Nezha-OB không làm vì metric chỉ có 5 mẫu mỗi phía.

**Kiểm.** Từ chính các chuỗi script lấy ra, z cực đại theo cột trùng khóa trong bản ghi BARO đóng băng từng bit ở 30/30 ca; phiếu metric theo dịch vụ trùng `runs/simplerca-decomposition-002/summary.json` ở 30/30 ca (`/summary/baro_z_bit_exact`, `/simple_votes_match_decomposition`).

**Đại lượng.** `drift_ratio` = mức dịch mà đường thẳng khớp trên đoạn nền suy ra cho 300 giây, chia cho mức dịch thật giữa trung vị hai đoạn. Gần 1: mức dịch là phần kéo dài của xu hướng nền. Gần 0: mức dịch không có trong xu hướng nền. Nhóm `trôi nền`: 0,5 ≤ drift_ratio ≤ 1,5 và r² của đường thẳng trên nền ≥ 0,5. Nhóm `bậc tại mốc`: |drift_ratio| < 0,5 và mức nhảy quanh mốc (60 giây mỗi bên) ≥ một nửa mức dịch.

**Quan sát không cần nhãn** (`/summary/all_columns_no_label/baro_view`): trong 1.966 cột mem của 30 ca, trung vị drift_ratio là 0,94 và trung vị r² là 0,50; 574 cột thuộc nhóm `trôi nền`, 142 thuộc `bậc tại mốc`, 169 không dịch, 1.081 không thuộc nhóm nào. Các loại cột khác có trung vị r² từ 0,02 tới 0,09 và trung vị drift_ratio gần 0. Số cột mem có từ 250 mẫu vượt ngưỡng trở lên là 226/1.966; trong đó 24 là cột mem của root (trên 30 cột mem của root).

**Quan sát sau khi nối nhãn** (`/summary/winning_columns`):

| Cột thắng của | BARO: n | BARO: trôi nền / bậc tại mốc / khác | BARO: trung vị drift_ratio | SimpleRCA: n | SimpleRCA: trôi nền / bậc tại mốc / khác | SimpleRCA: trung vị drift_ratio |
|---|---|---|---|---|---|---|
| Root, ca đúng hạng 1 | 21 | 0 / 9 / 12 | 0,00 | 25 | 0 / 12 / 13 | 0,00 |
| Root, ca sai hạng 1 | 9 | 1 / 4 / 4 | 0,03 | 5 | 0 / 3 / 2 | 0,02 |
| Thực thể đứng trên root | 103 | 19 / 14 / 66 (4 không dịch) | 0,61 | 20 | 6 / 6 / 8 | 0,24 |

- Riêng cột mem thắng của thực thể đứng trên root: BARO 55 cột, gồm 19 `trôi nền`, 6 `bậc tại mốc`, 28 khác, 2 không dịch; SimpleRCA 15 cột, gồm 6 `trôi nền`, 4 `bậc tại mốc`, 5 khác (`/by_kind_group`).

**Kết luận ở mức mô tả.**

- Kênh mem của RE2-TT trôi gần tuyến tính ngay trong đoạn nền ở phần lớn dịch vụ, bất kể ca đúng hay sai. Đây là đặc tính của dữ liệu, không phải dấu hiệu riêng của ca sai.
- Cột thắng của root gần như không có thành phần trôi (trung vị drift_ratio 0,00–0,03): mức dịch của root xuất hiện tại mốc. Cột thắng của thực thể đứng trên root có thành phần trôi lớn hơn rõ (trung vị 0,61 ở BARO, 0,24 ở SimpleRCA).
- Ứng viên "thực thể khác vượt root vì trôi tự nhiên của mem bị chuẩn hóa theo độ biến thiên nền thổi lên" được hỗ trợ một phần: 19/55 cột mem thắng ở BARO và 6/15 ở SimpleRCA thuộc nhóm `trôi nền`. Nó không giải thích hết: 6/55 và 4/15 cột mem có bậc tại mốc, và 28/55, 5/15 không thuộc nhóm nào. Với cột latency và cpu (47 trong 103 cột thắng ở BARO) trôi nền không phải lời giải thích (0 cột).

**Chưa trả lời, và phép kiểm cụ thể.** Các cột có bậc tại mốc ở dịch vụ khác root là do lan theo lời gọi, tải chung hay tác dụng phụ của công cụ tiêm lỗi. Bảng này không phân biệt được. Phép kiểm: với từng cột thuộc nhóm `bậc tại mốc`, đối chiếu dịch vụ của nó với quan hệ gọi tới root (đã có trong `runs/tracerca-core-td-001/summary.json`) và với số lời gọi đi qua nó trước và sau mốc (bảng span đã lưu). Chi phí khoảng 15 phút máy trên EC2. Chưa chạy trong phiên này vì cần định nghĩa "tải chung" trước; ghi vào danh sách cho `kiem-tiep.md`.

## 5. TORAI B (chỉ RE2-TT, 30 ca × 3 seed)

Nguồn: lượt phát lại `runs/torai-core-obs-001/` trên EC2 (script `scripts/torai_core_obs_v1.py`, `scripts/torai_obs_worker_py38.py`); bảng `runs/torai-severity-table-003/summary.json` (script `scripts/torai_severity_table_v3.py`) và `runs/torai-log-source-001/summary.json` (script `scripts/torai_log_source_v1.py`). Hai file tổng hợp đã chép về laptop, hash hai đầu khớp. Không có phép đổi nào ở mục này: chỉ phát lại, quan sát và phân rã.

**Chuỗi tính của TORAI bản sửa** (`src/torai/torai_sua.py`): mỗi nguồn (metric, log, trace_lat, trace_err) chấm từng cột bằng |z| lớn nhất của đoạn sau mốc theo mean, std của đoạn trước mốc, rồi chia cho tổng điểm mọi cột của nguồn đó. Lên mức dịch vụ: metric và trace cộng các cột, log lấy cột cao nhất. Mỗi dịch vụ có một vectơ bốn số; severity là trung bình bốn số. Phân cụm Gaussian mixture trên vectơ bốn số; cụm xếp theo severity trung bình; trong cụm nhiều dịch vụ dùng RCD, RCD không trả đủ thì xếp theo severity.

**Kiểm.** Lượt phát lại: 90/90 đơn vị cho bản ghi trùng bản đóng băng từng bit; ở 90/90 đơn vị kết quả của nhánh quan sát trùng nhánh native (`runs/torai-core-obs-001/progress.jsonl`, `terminal-20261010T200613Z.json`; 3.009,5 s). Bảng: severity bằng trung bình hàng của ma trận bốn nguồn ở 90/90; điểm cụm dựng lại trùng từng bit ở 90/90; thứ tự khối dựng lại trùng bản ghi ở 90/90; hạng root trùng T-028 ở 90/90 (`runs/torai-severity-table-003/summary.json` → `/summary/checks`, `/summary/self_check_rank_equals_t028`). Trung gian trước bước RCD giống nhau giữa ba seed ở 30/30 ca (`/summary/cases_three_seeds_same_pre_rcd_intermediates`), nên các số dưới đây lấy theo seed 0. Điểm log chuẩn hóa tính lại từ bảng `logts.csv` trùng trung gian ở 29/29 ca có cột log (`runs/torai-log-source-001/summary.json` → `/summary/rebuild_ok`).

**Quan sát** (`runs/torai-severity-table-003/summary.json` → `/summary/seed0`):

- Hit@1 26/30. Root có severity cao nhất trong ca ở đúng 26 ca đó; ở cả 4 ca sai root không có severity cao nhất (`/root_severity_rank_is_1_among_hit1`, `/root_severity_rank_is_1_among_wrong`).
- Ở 4 ca sai có 7 cặp (thực thể đứng trên root, root). Cả 7 thực thể có severity lớn hơn root; 2 trong 7 nằm cùng cụm với root (`/pairs_above_root`, `/pairs_above_root_with_lower_or_equal_severity`, `/pairs_above_root_same_cluster`).
- Phân rã cộng của severity theo bốn nguồn: ở 7/7 cặp, nguồn có chênh lớn nhất nghiêng về thực thể kia là log (`/pairs_above_root_largest_source_difference`). Chênh nguồn log từ 0,109 tới 0,175, trong khi nguồn log của root chỉ 0,015–0,029 (`/wrong_cases/*/above_root/*/difference_by_source`, `/wrong_cases/*/root_vector`).
- Nguồn trace_err rỗng ở 30/30 ca: không cột nào còn lại sau bước bỏ cột hằng (`/trace_err_columns`, `/root_source_value_is_zero/trace_err`). Severity vì vậy thực chất là (metric + log + trace_lat)/4.
- Root đứng đầu theo riêng nguồn metric ở 23/30 ca, theo riêng trace_lat ở 22/30, theo riêng log ở 2/30 (`/root_source_rank_is_1`).
- Cụm của root chỉ gồm một dịch vụ ở 27/30 ca (`/root_cluster_size`). Số cụm từ 2 tới 10, trung vị 5; cụm lớn nhất chứa 24 tới 61 dịch vụ.

**Nguồn log tạo điểm như thế nào** (`runs/torai-log-source-001/summary.json` → `/summary`):

- Dịch vụ đứng đầu theo nguồn log là `ts-order-other-service` ở 14/29 ca và `ts-travel2-service` ở 5/29; root đứng đầu theo log ở 2/29 ca (`/top_service_by_log`, `/top_service_is_root`). `ts-order-other-service` và `ts-seat-service` nằm trong ba dịch vụ đầu theo log ở 22 và 21 ca (`/top3_membership`); cả hai không là root ở ca dev nào.
- Ở 20/29 ca, cột log cao nhất của dịch vụ đứng đầu là cột không đổi ở 20 bin trước mốc (`/top_service_top_column_std_N_zero`). Trung vị 27% số cột log được chấm có nền toàn 0, và các cột đó mang trung vị 55% tổng điểm của nguồn log (`/share_of_scored_columns_all_zero_N`, `/log_mass_on_std_N_zero_columns`).
- Ở 7/7 cặp đứng trên root, cột log cao nhất của thực thể kia có nền không đổi (`/wrong_cases/pairs_where_entity_top_log_column_has_std_N_zero`).
- Một ví dụ đã xem (ca `dev-16597725c1`): cột `ts-order-other-service_267` bằng 0 ở cả 20 bin trước mốc và nhận 8, 12, 12, 22, 30, 17 ở sáu bin sau mốc.

**Kết luận ở mức tính toán.** Trong điều kiện một mẫu log (template do Drain gán) không xuất hiện ở đoạn trước mốc nhưng xuất hiện sau mốc, bước chấm z theo mean và std của nền cho z bằng chính số đếm thô (std bằng 0 thì thư viện đặt scale bằng 1), tức mất thang so sánh với các cột có nền dao động. Sau khi chia cho tổng, các cột như vậy chiếm quá nửa điểm của nguồn log, và điểm log dồn về vài dịch vụ có mẫu log đổi theo thời gian, không phụ thuộc root. Ở 4 ca TORAI B sai, nguồn log là nguồn nghiêng về thực thể kia nhiều nhất ở 7/7 cặp. Riêng chênh nguồn log đủ để đảo dấu chênh severity ở 4/7 cặp (2 ca: bỏ chênh log thì root có severity cao hơn); ở 3/7 cặp còn lại (2 ca) thực thể kia vẫn cao hơn root kể cả khi bỏ chênh log, vì metric hoặc trace_lat cũng nghiêng về nó (tính từ `/summary/seed0/wrong_cases/*/above_root/*/difference_by_source`). Vậy nguồn log giải thích trọn 2 trong 4 ca sai và góp phần ở 2 ca còn lại. Đây là phân rã cộng của severity, chưa phải phép đổi: bỏ nguồn log sẽ làm đổi cả bước phân cụm. Bước phân cụm và bước RCD không quyết định vị trí của root ở ca nào trong lượt gốc: hạng root đi theo thứ tự severity. Phép đổi thật ở mục 8 cho kết quả khác với điều phân rã gợi ý ở hai điểm: bỏ riêng các cột log có nền không đổi không trả lại hạng cho root (1/4 ca), còn bỏ hẳn nguồn log thì 2/4 ca sai thành đúng ở cả ba seed và thêm một ca ở seed 0. Kết luận về nguồn log lấy theo mục 8.

**Phân loại sơ bộ (sẽ soát ở mục 6).** Cách chấm cột có nền hằng thuộc cách tính của phương pháp. Việc mẫu log mới xuất hiện sau mốc thuộc cách dựng bảng log của nguồn B (Drain riêng từng dịch vụ, đánh số theo thứ tự xuất hiện, WHY-29); chưa kiểm bảng log của tác giả (nguồn A) có cùng hiện tượng không.

**Phép thử giả cho nguồn log** (`runs/torai-log-placebo-001/summary.json` → `/summary`; script `scripts/torai_log_placebo_v1.py`, định nghĩa ghi trong đầu script trước khi chạy, sau khi đã thấy bảng nguồn log). Mốc giả lùi 150 giây, chỉ dùng 20 bin trước mốc thật, không có lỗi nào trong khoảng đó. Dịch vụ đứng đầu theo log vẫn là `ts-order-other-service` ở 20/29 ca; `ts-order-other-service`, `ts-seat-service`, `ts-order-service` nằm trong ba dịch vụ đầu ở 24, 22, 21 ca (`/placebo_top_service_by_log`, `/placebo_top3_membership`). Cột có nền không đổi mang trung vị 39% tổng điểm log (bảng chính 55%) (`/placebo_log_mass_on_std_zero_columns`). Vậy việc mẫu log "chỉ xuất hiện sau mốc" là đặc tính của log theo thời gian ở vài dịch vụ, có cả khi không có lỗi.

**Nguồn trace_err.** Bảng `tracets_err.csv` của 30/30 ca có 77 tới 168 cột, mọi cột không đổi và tổng mọi ô bằng 0 (`/summary/trace_err`): trong cửa sổ của 30 ca dev không span nào mang mã trạng thái khác 0, nên bước bỏ cột hằng loại hết. Đây là đặc tính của dữ liệu dev, không phải lỗi của adapter.

**Chưa trả lời, và phép kiểm cụ thể.**

- Bảng log của tác giả (nguồn A) có cùng hiện tượng không. Phép kiểm: phát lại nguồn A có quan sát rồi chạy `torai_log_source_v1.py` trên đó; khoảng 25–50 phút máy trên EC2. Chưa chạy vì kế hoạch và SPEC chỉ nêu TORAI B là cấu hình chính; ghi cho `kiem-tiep.md`.
- Vì sao Drain tách mẫu mới liên tục ở `ts-order-other-service` và `ts-seat-service` (nội dung log chứa giá trị thay đổi, hay tải đổi dần). Phép kiểm: đọc các dòng log thuộc những cột đó trong `logs.parquet` của vài ca dev. Chưa làm; không đổi kết luận về bước tính, chỉ cần cho đề xuất cách dựng bảng log.

## 6. Ngữ nghĩa trace (Q-120): gắn phiên bản mã nguồn, cách tạo span, và mức đo được "dịch vụ gọi chờ root"

Nguồn: mã nguồn công khai tải về EC2 `~/rca/T-032/sources/instrumentation-002/` (ba kho, 253.615.767 byte; commit ghi ở LOG phiên 10). Các bảng: `runs/source-fingerprint-001/fingerprint.json` (script `scripts/source_fingerprint_v1.py`), `runs/trace-semantics-002/semantics.json` (`scripts/trace_semantics_v2.py`), `runs/call-interval-001/summary.json` và `inventory.json` (`scripts/call_interval_table_v1.py`), `runs/call-slow-001/summary.json` (`scripts/call_slow_table_v1.py`). Định nghĩa viết trước khi chạy: `thiet-ke-bang-mo-ta-004.md` mục 5 và 5b; tiêu chí mức đo được ghi ở đầu `trace_semantics_v2.py`. Không chạy mã nào của ba kho, không gọi phương pháp nào.

### 6.1 Gắn phiên bản mã nguồn với dataset

**Các lần thử và kết quả.**

1. Bài RCAEval (arXiv 2412.17015v2, mục 3.1, 3.3): chỉ dẫn kho `FudanSELab/train-ticket`, ghi 64 dịch vụ, trace thu bằng Jaeger; không nêu phiên bản, commit, tỷ lệ lấy mẫu hay kho triển khai. Kho RCAEval 259ea41 cũng không có thông tin này.
2. Kho `IntelligentDDS/Augmented-OnlineBoutique`: README ghi kho được mở kèm bài Nezha; chỉ có một commit (94a01ba4, 17/08/2023), kho tạo ngày 31/07/2023, sau ngày thu dữ liệu (22–23/08/2022).
3. Đối chiếu tên span (`fingerprint.json`): lấy mọi cặp (dịch vụ, tên span) xuất hiện trong 48 ca dev có bảng span, rồi kiểm mã nguồn ở từng phiên bản có sinh được tên đó không.

**Kết quả đối chiếu tên span.**

- **Nezha-OB** (`/online_boutique`): 55 tên span. 19 tên là chuỗi nguyên văn trong mã của đúng dịch vụ, và cả 19 không có trong kho gốc `microservices-demo` ở tag v0.3.9 (tag gần nhất trước ngày thu dữ liệu). 31 tên là rpc trong `pb/demo.proto`, do thư viện gRPC tạo span. 5 tên còn lại phép kiểm tự động không bắt được; đọc mã cho thấy cả 5 có nguồn: hai span tự đặt của `currencyservice` viết bằng dấu nháy đơn (`server.js:69`, `:94`), `SELECT addatabase.aditems` (truy vấn JDBC, `AdService.java:239`, `:256`), `sql.conn.query` và `sql.rows` (thư viện otelsql, `productcatalogservice/server.go:54`, `:193`). Kho còn chứa 8 file của công cụ tiêm lỗi Failpoint ở bốn dịch vụ (`trace-semantics-002/semantics.json` → `/source_scan/facts/augmented_ob_failpoint_files`), khớp với công cụ bài Nezha nêu.
- **RE2-TT** (`/train_ticket/tags`): 58 route, 39 span repository, 27 dịch vụ.

| Tag | Ngày | Route khớp / 58 | Span repository khớp / 39 | Thư mục dịch vụ / 27 |
|---|---|---|---|---|
| 0.0.1 | 20/05/2019 | 0 | 36 | 25 |
| 0.0.2, 0.0.3, 0.0.4, 0.1.0, v0.1.0, v0.2.0, v0.2.1 | 05/2019 – 09/2021 | 58 | 39 | 27 |
| v1.0.0, HEAD | 08/2022, 11/2022 | 54 | 37 | 25 |

**Kết luận về gắn phiên bản.**

- Nezha-OB: commit công khai duy nhất sinh được đủ 55/55 tên span quan sát, trong đó 19 tên chỉ có ở bản này. Đây là mức gắn mạnh nhất có được từ nguồn công khai. Nó không chứng minh từng dòng mã lúc thu dữ liệu trùng commit công bố một năm sau.
- RE2-TT: **không gắn được một phiên bản duy nhất.** Bảy tag từ 0.0.2 tới v0.2.1 đều khớp đủ; v1.0.0 và HEAD bị loại (thiếu `ts-food-map-service`, `ts-ticketinfo-service`). Phép đối chiếu tên span không phân biệt được bảy tag này. Vì vậy mọi kết luận dưới đây về Train Ticket được kiểm trên **cả bảy** tag.
- Span của RE2-TT được tạo ở đâu: **chưa xác định được chắc chắn.** Bảy tag ứng viên khác nhau về thư viện tracing (lệnh `git grep` trên các file `pom.xml` của từng tag): 0.0.2 có sleuth/zipkin; 0.0.3 và 0.0.4 có `opentracing-spring-jaeger-web-starter` trong `ts-common/pom.xml`; từ 0.1.0 tới v0.2.1 không có thư viện tracing nào trong pom, và bản triển khai kèm Jaeger của kho dùng image dựng sẵn tên `...-with-jaeger`. Dữ liệu RE2-TT có span repository (`XRepository.method`, 39 tên) và span cơ sở dữ liệu (`find ts.station`, 32 tên), cùng tên span HTTP theo quy ước OpenTelemetry (phía server "METHOD route", phía gọi "METHOD"; đặc tả `opentelemetry.io/docs/specs/semconv/http/http-spans`). **Suy luận, chưa kiểm:** span do một agent gắn lúc triển khai tạo, nhiều khả năng là OpenTelemetry Java agent, vì thư viện web-starter nói trên không tạo span repository hay span cơ sở dữ liệu. Giả định này có thể sai: tôi chưa đối chiếu được tên span repository với tài liệu hiện hành của agent (trang supported-libraries hiện ghi Spring Data không sinh telemetry), và công cụ cùng phiên bản không được công bố. Lý do không kiểm được trong task: chỉ nhóm tác giả RCAEval biết cấu hình triển khai. Kết luận phụ thuộc vào giả định này: thời điểm bắt đầu và kết thúc chính xác của span phía gọi; kết luận "lời gọi là chặn" ở mục 6.2 không phụ thuộc, vì nó đọc từ mã ứng dụng.

### 6.2 Lời gọi được viết thế nào trong mã nguồn

(`runs/trace-semantics-002/semantics.json` → `/source_scan`)

- **Train Ticket:** 63 loại lời gọi quan sát được (dịch vụ gọi → route của dịch vụ được gọi; 55 cặp dịch vụ). Ở cả bảy tag ứng viên, 63/63 loại có chỗ gọi trong mã của dịch vụ gọi, và mọi chỗ gọi là `restTemplate.exchange(...)`: lời gọi HTTP chặn, luồng gọi đứng chờ trả lời rồi mới chạy tiếp (`/train_ticket/call_kinds_synchronous_in_every_candidate` = 63). Hai lưu ý đã đọc tay: ở tag 0.0.2 file của `ts-inside-payment-service` có một dòng gọi bất đồng bộ nhưng đã bị chú thích (`InsidePaymentServiceImpl.java:107`); ở tag v0.2.1 `ts-travel-service` có thêm API `trips/left_parallel` chạy song song bằng `ExecutorService`, nhưng dữ liệu chỉ có route `trips/left` (hàm `query`, gọi tuần tự), không có `left_parallel` (`/facts`).
- **Augmented-OnlineBoutique:** 18 loại lời gọi (13 cặp dịch vụ). 18/18 có chỗ gọi là lời gọi gRPC unary chặn qua stub, không nằm trong goroutine; dịch vụ gọi có gắn interceptor phía gọi của OpenTelemetry (`frontend/main.go:238`, `checkoutservice/main.go:327`, `recommendationservice/recommendation_server.py:104`). Span phía được gọi do interceptor phía server tạo (`checkoutservice/main.go:170`, `productcatalogservice/server.go:174`).
- Theo đặc tả OpenTelemetry, span phía gọi bắt đầu trước khi gửi byte đầu của yêu cầu và kết thúc sau khi đọc xong phần đầu của trả lời; nó có thể gồm hoặc không gồm thời gian tạo kết nối.

**Kết luận ở mức mã nguồn.** Ở mọi phiên bản ứng viên, mỗi lời gọi giữa hai dịch vụ quan sát được trong dev là lời gọi yêu cầu–trả lời chặn. Thời lượng span phía gọi vì vậy là thời gian dịch vụ gọi chờ lời gọi đó trả về.

### 6.3 Dữ liệu trace có khớp cách ghi đó không (bảng C)

(`runs/call-interval-001/summary.json`; với mỗi lời gọi: `d_p` là span phía gọi, `d_c` là span phía được gọi, `gap = d_p − d_c`)

- Mỗi span phía gọi có đúng một span con thuộc dịch vụ khác ở mọi ca (bảng A).
- Nezha-OB, đoạn nền: trung vị 99,7% lời gọi có span phía được gọi nằm trọn trong span phía gọi; `gap` âm ở 0% lời gọi.
- RE2-TT, đoạn nền: trung vị 85,1% nằm trọn. 14,8% lời gọi có span phía được gọi kết thúc sau span phía gọi, nhưng `gap` âm chỉ ở 0,25%; trung vị độ lệch đầu 1,5 ms, cuối 0,55 ms. Giải thích khả dĩ: đồng hồ hai máy lệch dưới một mili giây, hoặc span server đóng sau khi trả lời đã gửi; dữ liệu không phân biệt hai khả năng. Hệ quả: ở RE2-TT không dùng riêng độ lệch đầu và cuối, chỉ dùng `gap` và `d_p`.

### 6.4 Thời gian chờ root có tăng không, và tăng ở đâu (bảng C2)

(`runs/call-slow-001/summary.json` → `/summary`. Lời gọi chậm: `d_p` vượt phân vị 95 của chính cạnh đó ở đoạn nền, nên ở nền khoảng 5% lời gọi là chậm. Chỉ xét cạnh có từ 20 lời gọi mỗi phía.)

| | RE2-TT | Nezha-OB |
|---|---|---|
| Ca có ít nhất một cạnh gọi tới root đủ lời gọi | 21/30 | 16/22 |
| Trong đó: có cạnh tới root mà từ 50% lời gọi sau mốc là chậm | 19/21 | 10/16 |
| Trong đó: có cạnh tới root mà từ 20% lời gọi sau mốc là chậm | 20/21 | 12/16 |
| Tỷ lệ chậm ở đoạn nền của các cạnh tới root (trung vị) | 5,1% | 5,6% |
| Trung vị tỷ lệ chậm sau mốc của các cạnh không dính root, theo loại lỗi | 4,9% – 12,2% | 4,2% – 5,9% |
| Ca mà trung vị các cạnh không dính root đạt 50% | 0 | 0 |

Trong các lời gọi chậm tới root, phần vượt nằm trong span của root chiếm (`/by_fault/*/slow_calls_inside_root_span_share`):

- RE2-TT: delay 97%, disk 79%, loss 76%, cpu 74%, mem 56%, socket 42%.
- Nezha-OB: cpu_consumed 91%, cpu_contention 48%, network_delay 0,5%. Với `exception` và `return` gần như không có lời gọi chậm (1 lời gọi mỗi loại).

Root không phải lúc nào cũng có cạnh chậm nhất. Ở 13/21 ca RE2-TT và 7/16 ca Nezha-OB có một cạnh không dính root với tỷ lệ chậm bằng hoặc cao hơn cạnh tới root; trong đó ở 9/13 và 3/7 ca, cạnh chậm nhất ấy là cạnh gọi tới một dịch vụ gọi trực tiếp root (ví dụ `ts-admin-travel-service→ts-travel2-service` khi root là `ts-route-service`), tức chờ theo dây chuyền (tính từ `/cases/*/other_edges/top` và `/edges_to_root`). Trung vị của mọi cạnh không dính root vẫn gần mức nền, nên đây là chậm theo chuỗi gọi qua root, không phải chậm toàn hệ thống. 4 và 4 ca còn lại chưa xem là cạnh nào.

Bảng C (so trung vị từng phần) cho cùng hướng nhưng che mất các ca lỗi mem: ở cạnh basic→route của ba ca đó trung vị `d_p` tăng khoảng 11–12 lần (ví dụ 4,8 ms lên 58 ms) trong khi trung vị `d_c` và `gap` đều tăng dưới 2 lần, vì lời gọi chậm chia thành hai nhóm (`runs/trace-semantics-002/semantics.json` → `/cases/*/edges/*/median_d_p_before_us`, `median_d_p_after_us`). Bảng C2 phân rã theo từng lời gọi nên không bị che.

### 6.5 Mức đo được theo từng ca

(`runs/trace-semantics-002/semantics.json` → `/summary`, `/cases`. Tiêu chí: C1 có cạnh gọi tới root với từ 20 lời gọi mỗi phía; C2 ở nền `gap` âm không quá 1% lời gọi; C3 mọi chỗ gọi của cặp đó là lời gọi chặn ở mọi phiên bản ứng viên.)

| Mức | RE2-TT (30 ca) | Nezha-OB (22 ca) |
|---|---|---|
| Đo được, có điều kiện | 21 | 16 |
| Đo được một phần | 0 | 0 |
| Không đo được | 9 | 6 |

- Không đo được ở RE2-TT: 6 ca root `ts-auth-service` (không dịch vụ nào gọi nó trong trace) và 3 ca root `ts-order-service` có cạnh dưới 20 lời gọi ở một phía. Ở Nezha-OB: 2 ca root `frontend` (là điểm vào, không có dịch vụ gọi) và 4 ca cạnh dưới 20 lời gọi (`checkoutservice` 3, `paymentservice` 1).
- 4 ca RE2 mà TraceRCA trả ERROR không có bảng span đã lưu; ở bảng này chúng được tính từ file trace gốc qua đúng bước cắt cửa sổ của runner, và cả 4 thuộc nhóm đo được.
- **"Đo được, có điều kiện" nghĩa là:** đo được thời gian dịch vụ gọi chờ lời gọi tới root trả về (thời lượng span phía gọi), và tách được phần nằm trong span của root với phần ngoài. **Điều kiện:** mã đã triển khai gọi theo cùng cách với các phiên bản ứng viên; span phía gọi do thư viện hoặc agent tạo bao quanh lời gọi.
- **Không đo được ở ca nào:** phần ngoài span của root gồm những gì (đường truyền, hàng đợi trước khi span của root bắt đầu, hay xử lý ở phía gọi quanh lời gọi). Dữ liệu chỉ có hai span cho mỗi lời gọi.

### 6.6 Trả lời câu trọng tâm của SPEC ở mức hiện có

Câu hỏi: tín hiệu của dịch vụ gọi có phải thời gian chờ dịch vụ phụ thuộc không.

- **Quan sát:** ở 19/21 ca RE2-TT và 10/16 ca Nezha-OB đo được, ít nhất một cạnh gọi tới root có từ một nửa số lời gọi sau mốc chậm hơn phân vị 95 của nền; các cạnh không dính root giữ tỷ lệ gần mức nền.
- **Suy luận có căn cứ mã nguồn:** vì lời gọi là chặn ở mọi phiên bản ứng viên, phần dài ra của span phía gọi là thời gian dịch vụ gọi chờ root. Đây là lần đầu trong T-032 có bằng chứng cho "dịch vụ gọi chờ root", thay cho câu "chưa có bằng chứng nào" ở `ket-qua-phien-9.md` mục 8.
- **Giới hạn của suy luận:** nó nói span phía gọi dài ra vì chờ root; nó không nói điểm cao của dịch vụ gọi ở một phương pháp cụ thể là do các span này. Việc nối hai điều đó (span phía gọi của lời gọi tới root có phải là span mang cờ đẩy dịch vụ gọi lên trên root ở MicroRank và TraceRCA hay không) chưa làm; phép kiểm: nối `runs/call-slow-001/cases/` với bảng cờ theo operation của `runs/tracerca-core-td-001/cases/` theo từng ca, khoảng 20 phút máy trên EC2. Để cho mục 7.
- **Hệ quả cho yêu cầu quan sát của FlashTicket (P9a), ở mức đề xuất:** (a) ghi đủ span phía gọi và span phía được gọi cho mọi lời gọi giữa hai dịch vụ; (b) để tách phần ngoài span của dịch vụ được gọi, cần thêm một mốc thời gian ở phía được gọi lúc yêu cầu tới (trước hàng đợi), vì hai span hiện có không tách được đường truyền với hàng đợi; (c) đoạn nền phải đủ dài: Nezha-OB chỉ có 41–97 giây nền; (d) không dựa vào từng độ lệch đầu, cuối giữa hai máy nếu đồng hồ không đồng bộ dưới mili giây.

## 7. CIRCA: K-2 theo loại cạnh (bổ sung cho mục 1.4; Minh duyệt chạy ngày 11/10)

Nguồn: lượt `runs/circa-laptop-k2-edges-001/` trên laptop (script `scripts/laptop_contrast_v3.py` cho 29 nhánh sham đầu, `_v4.py` cho phần còn lại; v4 chỉ khác cách ước RAM của bộ điều phối); tổng hợp `runs/circa-laptop-k2-edges-001/collect-001/summary.json` (script `scripts/laptop_contrast_collect_v3.py`). Thiết kế viết trước khi chạy: `thiet-ke-phep-doi-005.md`. Nhánh không cạnh (`k2`) lấy từ lượt `circa-laptop-k2-001`.

**Hai nhánh.** `k2x`: bỏ mọi cạnh nối metric của hai dịch vụ khác nhau (3.709 cạnh trên 30 ca), giữ 7.220 cạnh cùng dịch vụ. `k2s`: ngược lại. Mọi thứ khác native.

**Kiểm.** Nhánh sham chạy lại trong lượt này khớp bản đóng băng từng bit ở 30/30 ca. Tập nút của bốn nhánh giống nhau ở 30/30 ca (`/summary/node_sets_equal`). 90/90 tiến trình con thoát mã 0; RAM hệ thống đỉnh 94,8%, không lần nào chạm mốc 95% (`progress.jsonl`, `terminal-20261011T005456Z.json`).

**Quan sát** (`/summary/all`, `/cases_with_huge_node`, `/cases_without_huge_node`; bảng RHT, không DA):

| | native | `k2x` (chỉ còn cạnh cùng dịch vụ) | `k2s` (chỉ còn cạnh giữa hai dịch vụ) | `k2` (không cạnh) |
|---|---|---|---|---|
| Số ca có nút vượt 1e10 | 11 | 11 | 11 | 0 |
| Nút có điểm cao hơn điểm không cạnh, trên 4.526 nút có hồi quy ở native | 3.285 | 2.920 | 687 | — |
| Nút còn có cha | 4.526 | 3.968 | 986 | 0 |
| Hit@1, cả 30 ca | 12 | 13 | 12 | 21 |
| Hit@5, cả 30 ca | 26 | 24 | 25 | 24 |
| Hit@1, 19 ca không có nút cực lớn | 12 | 13 | 12 | 12 |
| Hit@5, 19 ca không có nút cực lớn | 17 | 15 | 16 | 15 |
| Hit@1, 11 ca có nút cực lớn | 0 | 0 | 0 | 9 |

- Root so với native (`/effect_vs_native`): `k2x` tăng hạng 7, không đổi 19, giảm 4; `k2s` tăng 3, không đổi 19, giảm 8.
- Cặp caller đứng trên root ở native (15 cặp): còn 10 dưới `k2x`, còn 14 dưới `k2s`, còn 7 khi không cạnh (`/pairs_above_root_native`).

**Kết luận ở mức tính toán, đối chiếu với dự đoán khai trước.**

- **Giá trị cực lớn:** còn nguyên ở 11/11 ca dưới cả hai nhánh. Dự đoán "chỉ cần nút đó còn bất kỳ cha nào là đủ sinh giá trị cực lớn" đúng; không riêng loại cạnh nào gây ra. Vì vậy ở 11 ca này Hit@1 vẫn bằng 0 cho tới khi bỏ hết cạnh.
- **Phần tăng điểm do hồi quy:** phần lớn đến từ cạnh cùng dịch vụ. Chỉ giữ cạnh cùng dịch vụ thì 2.920 nút vẫn có điểm cao hơn điểm không cạnh (so với 3.285 ở native); chỉ giữ cạnh giữa hai dịch vụ thì còn 687. Dự đoán H-nội-bộ được hỗ trợ; cạnh giữa hai dịch vụ cũng đóng một phần nhỏ hơn. Lưu ý hai loại cạnh không cân nhau về số lượng (7.220 so với 3.709), nên đây là so sánh về tổng tác động, không phải tác động trên mỗi cạnh.
- **Hạng root ở 19 ca không có nút cực lớn:** Hit@1 gần như không đổi dưới mọi nhánh (12, 13, 12, 12). Hit@5 cao nhất ở native (17) và thấp hơn khi bỏ bất kỳ loại cạnh nào (15, 16, 15). Chênh 1–2 ca trên 19 ca, không đủ để nói loại cạnh nào giúp định vị root.
- **Cặp caller:** bỏ cạnh giữa hai dịch vụ làm 5/15 cặp caller rời vị trí trên root; bỏ cạnh cùng dịch vụ chỉ làm 1/15. Cả 5 cặp đó thuộc nhóm ca có nút cực lớn (`/cases_with_huge_node/pairs_above_root_native/k2x`); ở nhóm 19 ca còn lại không cặp caller nào đổi dưới nhánh nào.

**Giới hạn.** Bảng chỉ xét RHT, không xét DA. Hai nhánh được nghĩ ra sau khi xem kết quả K-2. Phép đổi không đánh giá chất lượng của đồ thị gọi và không phải phương pháp mới.

## 8. TORAI B: phép đổi nguồn log (bổ sung cho mục 5)

Nguồn: lượt `runs/torai-log-contrast-001/` trên EC2 (script `scripts/torai_log_contrast_v1.py`; 30 ca, seed 0) và hai lượt kiểm seed 1, 2: `runs/torai-log-contrast-seeds-001/`, `-002/` (script `scripts/torai_log_contrast_seeds_v1.py`, `_v2.py`). Ba file `summary.json` đã chép về laptop, hash hai đầu khớp. Thiết kế viết trước khi chạy: `thiet-ke-phep-doi-006.md` (mục 8 của file đó ghi hai lần bổ sung kiểm seed, viết sau khi thấy kết quả seed 0).

**Hai nhánh.** `tl2`: bỏ các cột log không đổi ở 20 bin trước mốc. `tl1`: bỏ mọi cột log. Chỉ bảng `logts.csv` bị đổi, bằng cách bỏ cột; ba bảng còn lại và mọi bước của TORAI giữ nguyên.

**Kiểm.** Nhánh sham (chép nguyên bốn bảng, chạy cùng đường) cho `ket_qua` trùng lượt gốc từng bit ở 30/30 ca; hạng root của sham trùng T-028 ở 30/30 (`/summary/sham_equals_native`, `/self_check_sham_rank_equals_t028`). 90/90 lượt con trạng thái OK; 1.114 giây.

**Quan sát** (`/summary/sham`, `/tl2`, `/tl1`):

| | native | `tl2` (bỏ cột log nền không đổi) | `tl1` (bỏ nguồn log) |
|---|---|---|---|
| Số cột log (trung vị) | 382 | 263 | 0 |
| Hit@1 | 26/30 | 26/30 | 29/30 |
| Hit@5 | 30/30 | 29/30 | 30/30 |
| Root tăng hạng / không đổi / giảm hạng so với native | — | 1 / 27 / 2 | 3 / 27 / 0 |
| Trong 4 ca native sai: thành hạng 1 | — | 1 | 3 |
| Trong 26 ca native đúng: mất hạng 1 | — | 1 | 0 |

- `tl2` theo ca: `dev-16597725c1` từ hạng 3 lên 1; `dev-59f696a169` từ hạng 3 xuống 6; `dev-a5cabe5fa7` và `dev-f36d0647d5` giữ nguyên; ca đúng `dev-57546fd87b` từ hạng 1 xuống 2 (`/tl2/native_wrong/rows`, `/native_hit1/rows_lost`).
- `tl1` theo ca, seed 0: ba ca sai lên hạng 1 (`dev-16597725c1`, `dev-59f696a169`, `dev-a5cabe5fa7`); `dev-f36d0647d5` giữ hạng 3.
- **Kiểm seed 1 và 2.** Seed chỉ đổi thứ tự bên trong cụm nhiều dịch vụ, nên chỉ cần kiểm các cặp (ca, nhánh) mà ở seed 0 có khối do nhánh RCD xếp (11 cặp) hoặc root nằm trong cụm nhiều dịch vụ (thêm 10 cặp). Ở 20/21 cặp, hạng root giống nhau ở ba seed (`runs/torai-log-contrast-seeds-001/summary.json` và `-002/summary.json` → `/summary/root_rank_same_across_seeds`). Cặp duy nhất khác là `dev-a5cabe5fa7` dưới `tl1`: hạng 1 ở seed 0, hạng 2 ở seed 1 và seed 2 (`seeds-001` → `/summary/differing`). Vậy dưới `tl1` Hit@1 là 29/30 ở seed 0 và 28/30 ở seed 1, 2; dưới `tl2` là 26/30 ở cả ba seed.

**Kết luận ở mức tính toán, đối chiếu với dự đoán khai trước.**

- **H-nền-hằng bị bác ở dạng đã khai.** Dự đoán là dưới `tl2` root lên hạng 1 ở ít nhất 2 ca và không ca đúng nào hỏng. Thực tế: 1 ca lên hạng 1, 1 ca sai tệ hơn, 1 ca đúng mất hạng 1. Cột log có nền không đổi là nơi điểm log dồn về (mục 5), nhưng bỏ riêng chúng không trả lại hạng cho root: các cột log còn lại vẫn nghiêng về cùng những dịch vụ đó.
- **Nguồn log, như được dựng ở nguồn B, là nơi làm root mất hạng 1 ở 2 trong 4 ca sai, ổn định qua ba seed; ca thứ ba chỉ ở seed 0.** Bỏ hẳn nguồn log thì hai ca `ts-auth-service|cpu` thành đúng ở cả ba seed, ca `dev-a5cabe5fa7` thành đúng ở một trong ba seed, và không ca đúng nào hỏng (Hit@1 từ 26 lên 28 hoặc 29). Trên 30 ca dev, bỏ nguồn log không làm ca nào tệ đi, tức nguồn log không giúp định vị root ở ca nào.
- **Vì sao phải làm phép đổi.** Ở ca `dev-a5cabe5fa7`, phân rã cộng của mục 5 cho thấy thực thể đứng trên root (`ts-order-other-service`) vẫn có severity cao hơn root kể cả khi bỏ chênh log, vậy mà dưới `tl1` root lên hạng 1. Đọc khối của ca này (`runs/torai-log-contrast-001/cases/dev-a5cabe5fa7/*/ket-qua.json` trên EC2): ở lượt gốc hai dịch vụ là hai cụm đơn, `ts-order-other-service` đứng trước; dưới `tl1` chúng rơi vào cùng một cụm hai dịch vụ đứng đầu, và thứ tự trong cụm do nhánh RCD xếp, root đứng trước. Vậy bỏ nguồn log làm đổi cả bước phân cụm lẫn nhánh xếp trong cụm; phân rã không thấy được điều này, và câu "hạng root đi theo thứ tự severity" của mục 5 chỉ đúng cho lượt gốc. Vì nhánh RCD dùng seed, ca này được kiểm thêm ở seed 1 và 2: root chỉ đứng trước ở seed 0.
- Ca `dev-f36d0647d5` (`ts-order-service|loss`) vẫn sai dưới cả hai nhánh: ở ca này metric và trace_lat cũng nghiêng về `ts-travel2-service` và `ts-seat-service`.

**Chưa trả lời, và phép kiểm cụ thể.**

- Vì sao các cột log còn lại (nền có dao động) vẫn nghiêng về `ts-order-other-service` và `ts-seat-service`. Phép kiểm: bảng điểm theo cột log của hai dịch vụ này sau `tl2`, đối chiếu với dòng log gốc; khoảng 15 phút máy EC2. Chưa làm.
- Bảng log của tác giả (nguồn A) có làm root mất hạng theo cùng cách không: chưa kiểm (xem mục 5).

**Giới hạn.** Lượt đủ 30 ca chỉ chạy seed 0; seed 1 và 2 chỉ chạy cho 21 cặp mà seed có thể đổi hạng root, các cặp còn lại được suy từ việc root nằm trong cụm một dịch vụ. Bảng log là bảng của nguồn B do ta dựng (WHY-29), nên đây chưa là kết luận về TORAI của tác giả. `tl1` không phải đề xuất bỏ log; nó chỉ cho biết bước nào làm đổi hạng trên dev.
