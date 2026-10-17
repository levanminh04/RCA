# T-032 — Kết quả phiên 11 (11/10/2026): các việc của gói bổ sung 007

Người làm: Claude. File này gom bằng chứng của bảy việc trong gói bổ sung (`goi-bo-sung-007.md`, Q-134, Q-135). Chưa phải báo cáo nghiệm thu; T-032 chưa xong; RQ2 và G2 chưa đóng. File nối tiếp `ket-qua-phien-9.md` (KQ9) và `ket-qua-phien-10.md` (KQ10), không thay hai file đó.

**Cách đọc các số.** Mọi số là trên tập dev (30 ca RE2-TT, 22 ca Nezha-OB). Các bảng ở mục 1 và 2 là bảng mô tả: không gọi phương pháp, không chấm Hit mới. Các cột bằng chứng có thể chồng lấn, không cộng thành tỷ lệ nguyên nhân, và không cột nào là nhãn "lan". Mỗi ô của dev chỉ có vài ca nên không rút mẫu hình theo ô. Đường dẫn tính từ `results/T-032/`; con trỏ JSON ghi sau dấu `→`.

**Từ dùng trong file.** "Root" là dịch vụ gốc của sự cố theo nhãn. "Thực thể đứng trên root" là thực thể mà phương pháp xếp hạng tốt hơn root. "Phía trên root" là dịch vụ gọi root trực tiếp hoặc qua dịch vụ khác; "phía dưới" là dịch vụ được root gọi. "Span mang cờ" là span có thời lượng vượt mức nền theo đúng luật của hai phương pháp trace.

**Thiết kế viết trước khi chạy:** `thiet-ke-vi-tri-chuoi-goi-008.md` cho mục 1 và 2 (file tạo lúc 02:56Z, lượt đầu tiên chạy lúc 02:59Z; dòng đầu của file ghi "khoảng 03:15Z" là ước sai). Phần nào thêm sau khi đã xem kết quả đều ghi rõ.

## Tóm tắt bảy việc của gói và hai phép kiểm ngoài gói

| Việc | Câu hỏi | Trả lời trên dev, kèm mục có số | Trạng thái |
|---|---|---|---|
| 1 | Sai lầm của các phương pháp có nằm dọc chuỗi gọi phía trên root không | Khác nhau theo phương pháp. Tập trung phía trên root ở CIRCA, SimpleRCA và TraceRCA trên Nezha-OB. Ngang mức ngẫu nhiên ở BARO và MicroRank trên Nezha-OB. Thấp hơn mức ngẫu nhiên ở MicroRank trên RE2-TT (mục 1) | Xong |
| 2 | "Nhầm triệu chứng với nguyên nhân" có thật không | TraceRCA: có, ở mức tính toán, cho 4/4 cặp phía trên xét được ở RE2-TT và 9/15 ở Nezha-OB; nhưng đặc tính này cũng có ở ca đúng. MicroRank: không (0/10 và 4/16). Thêm: điểm của TraceRCA nghiêng về số span mang cờ tuyệt đối (mục 2) | Xong |
| 3 | Bất thường metric ở dịch vụ khác có đi theo quan hệ gọi không | Một phần nhỏ. Ở RE2-TT chỉ 5/103 cặp của BARO vừa nằm trên chuỗi gọi vừa có cột đổi tại mốc; 82/103 nằm ngoài chuỗi gọi hoặc không có span (mục 3) | Xong |
| 4 | Hạn chế lớn nhất của MicroRank thuộc bài gốc hay bản thư viện | Thuộc bước chia trace của bản thư viện. Thay riêng bước đó bằng công thức của bài gốc (với span đầu do ta quy ước): tỷ lệ trace bất thường từ 50% xuống 10–12% (RE2-TT) và từ 33% xuống 1,5–2,6% (Nezha-OB); Hit@1 từ 2/47 lên 21–22 (mục 4) | Xong |
| 5 | Tác giả TraceRCA có tự nêu hạn chế này không | Có. Bài gốc mô tả hiện tượng và có một bước xếp hạng xét hướng lan; bản thư viện bỏ bước đó. Hai hạn chế tìm thấy thuộc bản thư viện (mục 5) | Xong |
| 6 | Hạn chế ở nguồn log thuộc TORAI hay thuộc bảng log ta dựng | Thuộc bảng log ta dựng: với bảng của tác giả hiện tượng không lặp lại; các cột log còn lại vẫn nghiêng vì mẫu log hiếm mang dữ liệu thay đổi. Root vẫn mất hạng ở bước severity ở cả hai nguồn (mục 6) | Xong |
| 7 | Phần đối chiếu metric chia theo loại lỗi | Ở Nezha-OB, lỗi `return` có 3/4 ca không kênh nào thấy root; lỗi trễ mạng 0, 1, 0 trên 6 ca ở ba phương pháp dù trace có tín hiệu ở 6/6 ca (mục 7) | Xong |
| Ngoài gói 1 | Công thức điểm của TraceRCA bản thư viện có phải bước làm đổi hạng không | Có: xếp theo tỷ lệ làm mất 11/15 và 43–46/75 cặp đứng trên root. Nhưng tỷ lệ không phải cách chữa: ở RE2-TT Hit@1 giảm từ 21 xuống 13–14 (mục 8) | Xong |
| Ngoài gói 2 | Bước xếp hạng xét hướng lan của bài TraceRCA gốc có tách được root khỏi dịch vụ gọi đang chờ nó không | Không, ở bản cài theo lời văn của bài: 0/4 và 0/8 cặp theo mặc định của bài; hiệu số lấy trị tuyệt đối nên không mang hướng (mục 9) | Xong |

Ba điều bất lợi cho hướng "dùng quan hệ gọi tới root", ghi đúng như đã thấy: (a) phần lớn cặp sai của MicroRank và BARO không nằm phía trên root; (b) "span chờ root" có cả ở ca đúng, nên tự nó không phân biệt ca sai; (c) với kênh metric ở RE2-TT, quan hệ gọi chỉ chạm tới một phần nhỏ các cặp. Hai điều thuận: (d) với TraceRCA, chuỗi bằng chứng "dịch vụ gọi chờ root rồi bị chấm bất thường" đủ bốn khâu; (e) với MicroRank, chỗ hỏng lớn nhất là bước chia trace của bản thư viện, không phải phần dùng đồ thị của bài gốc. Một điều bất lợi thêm, thấy ở phép kiểm ngoài gói thứ hai: (f) bước xét hướng lan có sẵn trong bài TraceRCA gốc, khi cài theo lời văn của bài, không tách được root khỏi dịch vụ gọi đang chờ nó, vì hiệu số lấy trị tuyệt đối không mang hướng của cạnh gọi.

## 1. Việc 1 — thực thể đứng trên root nằm đâu so với chuỗi gọi

Nguồn: `runs/chain-position-002/summary.json` và `units.json` (script `scripts/chain_position_v1.py`); đồ thị gọi theo ca từ `runs/chain-spanpass-001/` (script `scripts/chain_spanpass_v1.py`); góc nhìn bổ sung `runs/chain-position-cond-001/summary.json` (script `scripts/chain_position_cond_v1.py`). Thứ hạng lấy từ 372 bản ghi đóng băng mà `results/T-028/runs/phan-hoi-review-001/ca-sai.json` trỏ tới.

**Kiểm.**

- Lượt đọc bảng span: 52/52 ca đạt mọi tự kiểm. Tổng số cờ bằng `H_native` của lượt T-D ở 48/48 ca; số trace bất thường, số trace bình thường và số span mang cờ bằng số của lượt MicroRank phiên 9 ở 48/48 ca; cạnh đủ lời gọi và số lời gọi chậm trùng bảng C2 ở 52/52 ca; hai cách tính cờ (TraceRCA, MicroRank) không khác nhau ở span nào (`runs/chain-spanpass-001/summary.json` → `/cases/*/self_check`, `/flags_differ_total`). Mười ba phép kiểm trên trường hợp tự dựng của phép "nhìn xuống cây span" đạt (`/fixtures`).
- Hạng root tính lại từ bản ghi trùng hạng T-028 ở mọi đơn vị OK (`runs/chain-position-002/summary.json` → `/summary/*/*/self_check_rank_equals_reference`, không có giá trị `false` nào). Số cặp trùng KQ9: MicroRank 132 + 120, TraceRCA 15 + 75, SimpleRCA 20 + 44, BARO 103 + 59, CIRCA có DA 110, TORAI B 7.
- Đổi sang đồ thị chỉ gồm cạnh đã có trước mốc: 0 cặp đổi lớp ở mọi phương pháp (`/pairs_class_changes_with_baseline_only_graph`).
- Lượt hỏng giữ lại: ba lượt thử đầu của script đọc bảng span (`runs/chain-spanpass-test-001` tới `-003` trên EC2) hỏng ở bước ghi file kết quả trường hợp tự dựng (kiểu số của numpy); `runs/chain-position-001` hỏng vì dòng Nezha-OB của T-028 không có trường hạng theo seed. Cả hai là lỗi công cụ, chưa cho ra số nào.

**Quan sát.** Cột "quan sát / kỳ vọng" là số thực thể đứng trên root nằm phía trên root, so với số kỳ vọng nếu rút ngẫu nhiên cùng số thực thể từ tập ứng viên của từng ca. Cột "rút ngẫu nhiên" là tỷ lệ trong 20.000 lần rút có số "phía trên" không nhỏ hơn số quan sát. Con trỏ: `/summary/<dataset>/<phương pháp>/groups/phia_tren`, `/top1_when_root_rank_min_gt_1`; góc nhìn chỉ thực thể có span ở `runs/chain-position-cond-001/summary.json` → `/summary/<dataset>/<phương pháp>/groups/phia_tren`, `/cases`.

RE2-TT:

| Phương pháp | Ca có thực thể đứng trên root | Số cặp | Phía trên: quan sát / kỳ vọng (tỷ số; rút ngẫu nhiên) | Như trên, chỉ thực thể có span | Thực thể đứng đầu nằm phía trên root |
|---|---|---|---|---|---|
| BARO | 9 | 103 | 8 / 3,1 (2,58; 0,2%) | 8 / 4,9 (1,62; 3,8%) | 1/9 ca |
| SimpleRCA | 5 | 20 | 6 / 0,8 (7,58; 0,0%) | 6 / 1,9 (3,21; 0,1%) | 4/5 |
| MicroRank | 24 | 132 | 4 / 18,5 (0,22; 100%) | như cột trước | 0/24 |
| TraceRCA | 5 | 15 | 4 / 1,9 (2,10; 7,7%) | như cột trước | 3/5 |
| CIRCA có DA | 14 | 110 | 25 / 3,5 (7,19; 0,0%) | 25 / 9,0 (2,79; 0,0%) | 9/14 |
| CIRCA không DA (góc nhìn phụ) | 18 | 86 | 22 / 3,1 (7,09; 0,0%) | 22 / 7,2 (3,04; 0,0%) | 13/18 |
| TORAI B (ba seed giống nhau) | 4 | 7 | 2 / 0,3 (6,09; 3,2%) | 2 / 0,8 (2,36; 18,1%) | 1/4 |

Nezha-OB (mọi thực thể đều có span):

| Phương pháp | Ca có thực thể đứng trên root | Số cặp | Phía trên: quan sát / kỳ vọng (tỷ số; rút ngẫu nhiên) | Thực thể đứng đầu nằm phía trên root |
|---|---|---|---|---|
| BARO | 14 | 59 | 7 / 6,9 (1,02; 58,4%) | 2/14 |
| SimpleRCA | 15 | 44 | 9 / 4,7 (1,93; 0,8%) | 7/15 |
| MicroRank | 22 | 120 | 20 / 19,2 (1,04; 45,8%) | 0/22 |
| TraceRCA | 18 | 75 | 20 / 12,6 (1,58; 0,0%) | 12/18 |

Các lớp còn lại (`/above_by_class`, `/candidates_by_class`, `/groups/phia_duoi`, `/groups/khong_lien_he`, `/groups/khong_co_span`):

- BARO ở RE2-TT: 44/103 thực thể đứng trên root không có span nào (thực thể cơ sở dữ liệu và tương tự), 38 không liên hệ với root trên đồ thị gọi. Khi BARO sai hạng 1, thực thể đứng đầu thuộc lớp "rời" ở 7/9 ca.
- MicroRank ở RE2-TT: phía dưới root 35 so với kỳ vọng 14,1 (tỷ số 2,49); không liên hệ 87 so với 97,1. Thực thể đứng đầu khi sai là `ts-station-service` ở 21/24 ca và `ts-route-service` ở 3/24 ca, bất kể root là dịch vụ nào.
- MicroRank ở Nezha-OB: thực thể đứng đầu khi sai là `currencyservice` ở 13/22 ca, `cartservice` 5, `productcatalogservice` 4; không lần nào nằm phía trên root.
- TraceRCA ở Nezha-OB: thực thể đứng đầu khi sai là `frontend` ở 11/18 ca.
- CIRCA có DA: 0 thực thể phía dưới root; `ts-travel2-service` và `ts-travel-service` đứng đầu ở 9/14 ca sai.
- Số ca sai mà root không có dịch vụ phía trên nào trong tập ứng viên (`runs/chain-position-cond-001/summary.json` → `/cases/root_has_no_upstream_candidates`): BARO RE2-TT 5/9, CIRCA có DA 4/14, MicroRank RE2-TT 4/24, TORAI B 2/4; ở Nezha-OB 2 ca ở mỗi phương pháp (root là `frontend`).

**Đối chiếu với cách đọc khai trước** (từ 1,5 lần kỳ vọng và rút ngẫu nhiên không quá 5%: tập trung phía trên; tỷ số 0,8–1,25: ngang nền):

- **Tập trung phía trên root:** CIRCA (có và không có DA), SimpleRCA ở cả hai dataset, TraceRCA ở Nezha-OB. BARO ở RE2-TT đạt mốc ở cả hai góc nhìn, nhưng chỉ là 8 trên 103 cặp, nằm trong 3/9 ca sai.
- **Ngang tỷ lệ nền:** BARO và MicroRank ở Nezha-OB (tỷ số 1,02 và 1,04).
- **Thấp hơn nền:** MicroRank ở RE2-TT (tỷ số 0,22). Thực thể đứng trên root ở đây nghiêng về phía dưới root.
- **Không rõ:** TraceRCA ở RE2-TT (tỷ số 2,10 nhưng rút ngẫu nhiên 7,7%, chỉ 15 cặp trong 5 ca); TORAI B (2 cặp).

**Kết luận ở mức mô tả, chỉ trên dev.**

- Câu "sai lầm có nằm dọc chuỗi gọi phía trên root không" có câu trả lời khác nhau theo phương pháp. Với CIRCA, SimpleRCA và TraceRCA: có, ở mức vị trí. Với MicroRank và với BARO ở Nezha-OB: không; ở MicroRank RE2-TT còn ít hơn mức ngẫu nhiên.
- Hệ quả cho đầu ra P4 số 4: thông tin "dịch vụ này nằm phía trên root" chỉ nhắm trúng một phần các cặp sai. Tính trên mọi cặp: MicroRank 24/252 (kể cả 6 cặp hai chiều: 30/252), TraceRCA 24/90 (25/90), SimpleRCA 15/64 (16/64), BARO 15/162 (18/162), CIRCA có DA 25/110 (26/110). Phần lớn cặp sai của MicroRank và BARO nằm ngoài chuỗi gọi phía trên root, nên một thành phần chỉ "trừ phần kế thừa từ phía dưới" không chạm tới chúng.
- Với CIRCA, việc tập trung phía trên khớp với cơ chế đã xác nhận ở KQ10 mục 1.3 (giá trị cực lớn đi từ hậu duệ lên tổ tiên); bảng không DA cũng tập trung phía trên (tỷ số 3,04 trên thực thể có span), nên hiện tượng không riêng của bước DA.

**Điều thêm sau khi đã xem kết quả, ghi rõ.** Cột "chỉ thực thể có span" không có trong thiết kế. Tôi thêm vì thấy ở RE2-TT các phương pháp metric xếp hạng 68 thực thể, trong đó khoảng 42 thực thể không có span; chúng không thể nằm trên chuỗi gọi và hiếm khi đứng trên root, nên mốc nền tính trên mọi ứng viên làm tỷ số phình. Cả hai cột được giữ; khi hai cột cho hai cách đọc khác nhau (TORAI B) tôi ghi "không rõ".

**Giới hạn.** Rút ngẫu nhiên coi các thực thể đứng trên root là độc lập; thực tế chúng không độc lập, nên tỷ lệ chỉ là mốc tham chiếu, không phải kiểm định. Đồ thị gọi của RE2-TT gần như giống nhau giữa các ca, nên vị trí chủ yếu do root là dịch vụ nào quyết định (5 dịch vụ gốc). Vị trí trên đồ thị chưa nói gì về cơ chế; cơ chế xem mục 2.

## 2. Việc 2 — span làm thực thể đứng trên root có phải là span chờ root không (TraceRCA, MicroRank)

Nguồn: `runs/slow-call-flag-link-001/summary.json` và `cases.json` (script `scripts/slow_call_flag_link_v1.py`); bảng theo thao tác và theo trace từ `runs/chain-spanpass-001/cases/` (trên EC2). Thao tác cao nhất của mỗi thực thể lấy từ mục `ranking` của bản ghi đóng băng.

**Kiểm.** Tập thực thể đứng trên root trùng lượt phiên 9 ở 26/26 và 21/21 ca (TraceRCA), 26/26 và 22/22 ca (MicroRank). Với TraceRCA, thao tác cao nhất, số span mang cờ và số span sau mốc của mọi thực thể đứng trên root và của root trùng lượt T-D. Với MicroRank, thao tác cao nhất, số trace bất thường chứa nó và số trace nó tự mang cờ trùng lượt phiên 9 (`/summary/*/*/self_check`).

**Điều kiện xét được.** Lời gọi chậm tới root chỉ định nghĩa được ở ca có cạnh tới root đủ 20 lời gọi mỗi phía: 17/26 ca RE2-TT và 15/21 (TraceRCA), 16/22 (MicroRank) ca Nezha-OB (`/cases_root_edge_measurable`). Các cặp ở ca còn lại ghi "không xét được".

### 2.1 TraceRCA

Đại lượng chính: trong các span mang cờ của thao tác cao nhất của thực thể, tỷ lệ span mà lời gọi chậm tới root (ở chính span hoặc dưới nó trong cây span) chiếm từ 50% phần vượt của span. Con trỏ: `/summary/<dataset>/tracerca/groups/<nhóm>/main`, `/main_quantiles`.

| Nhóm | RE2-TT: số thực thể; đạt từ 50%; trung vị | Nezha-OB: số thực thể; đạt từ 50%; trung vị |
|---|---|---|
| Đứng trên root, nằm phía trên root, ca xét được (`above_upstream_measurable`) | 4; 4/4; 0,85 | 15; 9/15; 0,88 |
| Đứng trên root, không nằm phía trên root, ca xét được (`above_not_upstream_measurable`) | 3; 0/3; 0 | 36; 0/36; 0 |
| Nằm phía trên root nhưng **không** đứng trên root, ca sai (`not_above_upstream_measurable_wrong_cases`) | 21; 11/21; 0,57 | 4; 4/4; 1,00 |
| Nằm phía trên root, ca root đứng hạng 1 (`not_above_upstream_measurable_root_rank1_cases`) | 96; 83/96; 0,96 | 3; 2/3; 0,93 |

- Mốc so trên span không mang cờ của cùng thao tác (`/groups/above_upstream_measurable/share_slow_nonflag_quantiles`): tỷ lệ span bao một lời gọi chậm tới root có trung vị 1,5% ở RE2-TT (lớn nhất 5,1%) và 0% ở Nezha-OB (lớn nhất 10,8%). Span mang cờ vì vậy đúng là các span bao lời gọi chậm tới root, không phải mọi span của thao tác đó.
- Theo ca (`/wrong_cases*`): RE2-TT có 5 ca sai, 4 ca xét được, 3 ca có thực thể phía trên đứng trên root và thuộc loại "chủ yếu là chờ root"; ở cả 3 ca đó mọi thực thể đứng trên root đều như vậy. Nezha-OB có 19 ca sai, 13 xét được, 16 ca có thực thể phía trên đứng trên root, 8 ca có cặp "chủ yếu là chờ root", 5 ca mà mọi thực thể đứng trên root đều như vậy.
- Theo loại lỗi ở Nezha-OB (`/wrong_cases_by_fault`): `cpu_contention` 4/5 ca sai, `network_delay` 3/5, `cpu_consumed` 1/2, `exception` 0/3, `return` 0/4.
- Bốn cặp của RE2-TT (đọc từ `cases.json`): `ts-seat-service` trên root `ts-order-service` lỗi disk (tỷ lệ 0,985) và lỗi loss (0,605); `ts-travel-service` trên `ts-order-service` lỗi loss (0,846); `ts-seat-service` trên `ts-travel-service` lỗi disk (0,862; cặp hai chiều). Ở cả bốn, số span mang cờ của dịch vụ gọi lớn hơn của root (130 so với 86; 147 và 104 so với 99; 545 so với 247).
- Mười một cặp còn lại của RE2-TT nằm ở hai ca `ts-order-service` lỗi loss (`dev-20acb4402d`, `dev-260d332c8d`): 9 thực thể lớp "rời", 1 phía dưới, 1 dịch vụ gọi trực tiếp ở ca không xét được. Ở hai ca này root chỉ có 46 và 39 span sau mốc ở thao tác cao nhất, với 11 và 6 span mang cờ; 9 trong 11 thực thể đứng trên có 14–48 span mang cờ trên 450–1.674 span, hai thực thể còn lại (`ts-inside-payment-service`, `ts-consign-service`) có 7/39 và 6/35.

**Kết luận ở mức tính toán.**

- Trong điều kiện dịch vụ gọi có span bao lời gọi tới root và lời gọi đó chậm đi, bước gắn cờ theo thời lượng cả span của TraceRCA chấm thời gian chờ root thành bất thường của dịch vụ gọi. Ở các cặp xét được, điều này đúng với 4/4 cặp phía trên của RE2-TT (3/5 ca sai) và 9/15 cặp phía trên của Nezha-OB (8/19 ca sai). Đây là xác nhận ở mức tính toán cho giả thuyết "nhầm triệu chứng với nguyên nhân" của kế hoạch nghiên cứu, kèm điều kiện về cách ghi span ở KQ10 mục 6.5.
- **Đặc tính này không riêng của ca sai.** Ở 21 ca RE2-TT mà TraceRCA xếp root hạng 1, 83/96 dịch vụ phía trên root cũng có phần lớn span mang cờ là span chờ root. Thứ khác nhau giữa ca đúng và ca sai là số span mang cờ của dịch vụ gọi có vượt số của root hay không, không phải việc có chờ hay không.
- Giả thuyết không giải thích phần còn lại: 11/15 cặp của RE2-TT và 66/75 cặp của Nezha-OB (40 cặp "chung phía trên", 15 phía dưới, 6 phía trên có tỷ lệ dưới 50%, 5 phía trên ở ca không xét được).

**Thêm sau khi xem bảng trên: điểm của TraceRCA nghiêng về số span mang cờ tuyệt đối.** Nguồn: `runs/tracerca-ratio-vs-count-001/summary.json` (script `scripts/tracerca_ratio_vs_count_v1.py`; chỉ ghép hai file kết quả đã có). Điểm của TraceRCA là 2a/(n + H), với a là số span mang cờ của thao tác, n là số span sau mốc của nó, H là tổng số span mang cờ của cả ca (đẳng thức đã kiểm ở 48/48 ca, KQ9 mục 3). Tự kiểm: điểm tính lại từ a, n, H của thực thể đứng trên root lớn hơn của root ở 15/15 và 75/75 cặp (`/summary/*/ji_larger_than_root`).

- Ở RE2-TT, 12/15 thực thể đứng trên root có tỷ lệ a/n **thấp hơn** root nhưng số span mang cờ a **lớn hơn** root (`/summary/RE2-TT/ratio_lower_and_a_larger`). Ở 3/5 ca sai, root có tỷ lệ a/n cao hơn mọi thực thể đứng trên nó (`/cases_where_root_has_top_ratio_among_above_and_root`). Ở Nezha-OB: 39/75 cặp và 5/18 ca.
- Ở năm ca sai của RE2-TT, H gấp 5,5 tới 11,4 lần n của root (`/cases/*/H_over_root_n`). Khi H lớn hơn n nhiều lần, mẫu số gần như không phụ thuộc n, nên thứ tự đi theo a. Ví dụ ca `dev-20acb4402d`: root có 11 span mang cờ trên 46 span (24%), thực thể đứng trên có 48 trên 1.066 (4,5%); H = 414.
- Hai trong ba ca "chủ yếu là chờ root" cũng thuộc nhóm này: tỷ lệ của dịch vụ gọi thấp hơn root (130/1.286 so với 86/494; 545/3.921 so với 247/804). Ở các cặp đó hai điều cùng cần: span chờ root được gắn cờ, và công thức điểm đếm theo số tuyệt đối.

**Kết luận ở mức tính toán (thêm).** Trong điều kiện thao tác của root có ít span hơn thao tác của dịch vụ khác, bước tính điểm 2a/(n + H) làm mất thông tin "tỷ lệ span của thao tác này vượt nền": thao tác đông span thắng dù tỷ lệ thấp hơn. Đây là hạn chế của cách tính trong bản TraceRCA của thư viện. Các con số ở đoạn này là quan sát trên trung gian đã khớp. Phép đổi tương ứng (xếp theo a/n thay cho công thức gốc, mọi thứ khác giữ nguyên) đã chạy sau đó; kết quả và giới hạn ở mục 8.

### 2.2 MicroRank

Đại lượng chính: trong các trace bất thường chứa thao tác cao nhất của thực thể, tỷ lệ trace có "bất thường gắn với root" (trace có span mang cờ của chính root, hoặc có span mang cờ bao một lời gọi chậm tới root). Con trỏ: `/summary/<dataset>/microrank/groups/<nhóm>/main`, `/main_quantiles`.

| Nhóm | RE2-TT: số thực thể; đạt từ 50%; trung vị | Nezha-OB: số thực thể; đạt từ 50%; trung vị |
|---|---|---|
| Đứng trên root, nằm phía trên root, ca xét được | 10; 0/10; 0,17 | 16; 4/16; 0,21 |
| Đứng trên root, không nằm phía trên root, ca xét được | 66; 18/66; 0,29 | 71; 16/71; 0,13 |
| Nằm phía trên root nhưng **không** đứng trên root, ca sai | 112; 103/112; 0,99 | 9; 7/9; 0,95 |

- Thực thể đứng đầu ở 24 ca sai của RE2-TT (`cases.json`, thực thể có `rank_min` = 1): tỷ lệ trên có trung vị 0,32; tỷ lệ trace bất thường mà thao tác đó tự mang cờ có trung vị 0,23.
- Mốc so với dịch vụ khác root và không nằm phía trên root (`/groups/*/other_x_top_share_linked_quantiles`): dịch vụ có tỷ lệ cao nhất đạt trung vị 0,52–0,53 ở RE2-TT và 0,50–0,51 ở Nezha-OB. Tức trong các trace bất thường chứa thao tác của thực thể đứng trên root, khoảng một nửa gắn với một dịch vụ không phải root.
- Theo ca: số ca sai có thực thể phía trên đứng trên root và thuộc loại "chủ yếu gắn với root" là 0/24 ở RE2-TT và 4/22 ở Nezha-OB (`/wrong_cases_with_above_upstream_mostly_waiting`).
- Ở mức span, 3/5 dịch vụ gọi trực tiếp đứng trên root ở RE2-TT có phần lớn span mang cờ của chính nó là span bao lời gọi chậm tới root (`/groups/above_direct_caller_measurable/span_share_slow`), nhưng chỉ 24–38% trace bất thường chứa thao tác đó gắn với root.

**Kết luận ở mức tính toán.**

- Với MicroRank, giả thuyết "dịch vụ gọi đứng trên root vì chờ root" **không được hỗ trợ** ở RE2-TT (0/10 cặp phía trên, 0/24 ca sai) và chỉ được hỗ trợ ở 4/16 cặp phía trên của Nezha-OB (4/22 ca sai). Điểm của thực thể đứng trên root đến chủ yếu từ các trace bất thường không gắn với root.
- Chiều ngược lại rõ hơn: ở RE2-TT, 103/112 dịch vụ phía trên root có gần hết trace bất thường gắn với root, và chúng được xếp **dưới** root. Thứ đứng trên root là các thao tác có mặt ở rất nhiều trace bất thường không liên quan tới root; `ts-station-service` đứng đầu ở 21/24 ca sai.
- Điều này khớp với KQ9 mục 2 (khoảng một nửa trace sau mốc bị xếp vào nhóm bất thường; bước đếm phủ cho điểm cao cho thao tác có mặt ở hầu hết trace) và nói thêm một điều KQ9 chưa có: phần lớn các trace bất thường đó không dính tới root.
- Ở 18/66 cặp không nằm phía trên root của RE2-TT và 16/71 của Nezha-OB, phần lớn trace bất thường chứa thao tác của thực thể gắn với root: thực thể được điểm nhờ "đi cùng trace" với chuỗi của root. Đây là quan hệ theo trace, không phải quan hệ gọi tới root.

### 2.3 Trả lời câu trọng tâm của đề bài task ở mức hiện có

Câu hỏi: ở những ca dịch vụ gọi đứng trên root, phương pháp chấm thời gian chờ dịch vụ phụ thuộc thành bất thường của dịch vụ gọi, hay cách chấm tự ưu tiên dịch vụ gọi.

- **TraceRCA: chấm thời gian chờ.** Có chuỗi bằng chứng đủ bốn khâu: lời gọi là chặn trong mã nguồn (KQ10 mục 6.2); lời gọi tới root chậm đi sau mốc (KQ10 mục 6.4); span mang cờ của dịch vụ gọi là các span bao lời gọi chậm đó và lời gọi chậm chiếm từ nửa phần vượt (mục 2.1); đổi cờ sang phần không được span con phủ làm 3/5 cặp dịch vụ gọi của RE2-TT biến mất (KQ9 mục 3). Ở Nezha-OB phép đổi đó chỉ làm 1/17 cặp biến mất, vì với lỗi trễ mạng phần chờ nằm ngoài span của root (KQ10 mục 3 và 6.4).
- **MicroRank: không phải chờ, cũng không phải ưu tiên dịch vụ gọi.** Dịch vụ gọi hiếm khi đứng trên root (4 cặp phía trên trong 132 cặp ở RE2-TT). Thứ đứng trên root là thao tác phủ nhiều trace bất thường không liên quan tới root.
- **Còn mở:** vì sao khoảng một nửa trace sau mốc mang cờ dù không dính tới root (ứng viên: mỗi trace có nhiều span, mỗi span có xác suất nhỏ vượt 3 lần độ lệch chuẩn, nên xác suất "có ít nhất một span vượt" lớn; chưa kiểm). Mục 4.2 cho thấy khi thay bước chia bằng công thức của bài gốc, tỷ lệ trace bất thường còn 10–12% (RE2-TT) và 1,5–2,6% (Nezha-OB); riêng ứng viên về xác suất "có ít nhất một span vượt" chưa được kiểm tách riêng.
- **Giới hạn:** "bao một lời gọi chậm tới root" là điều kiện về cấu trúc và thời lượng, không đo trạng thái luồng. Mốc phân vị 95, mốc 50% và mốc 20 lời gọi do tôi đặt; số thô nằm trong `cases.json`. Kết quả không phải nhãn lan và không cho tỷ lệ "lan có đáng kể".

## 3. Việc 3 — kênh metric: cột thắng của thực thể đứng trên root nằm đâu so với chuỗi gọi

Nguồn: `runs/metric-chain-001/summary.json` (script `scripts/metric_chain_v1.py`, ghép các bảng đã có) và `runs/service-traffic-001/summary.json` (script `scripts/service_traffic_v1.py`, đếm span theo dịch vụ trước và sau mốc, không dùng nhãn). Thiết kế viết trước: `thiet-ke-kenh-metric-010.md` mục 2. Không định nghĩa nhãn "lan".

**Kiểm.** Loại cột thắng tính lại trùng `runs/derived-tables-001/derived.json` ở 123/123 cặp của RE2-TT (103 cặp BARO, 20 cặp SimpleRCA; `/self_check`). Số cặp trùng KQ9 (BARO 103 + 59, SimpleRCA 20 + 44).

**Quan sát ở RE2-TT** (`/summary/RE2-TT/<phương pháp>/above_position_by_trend_group`, `/step_at_t`, `/above_traffic_changed_by_position`).

Nhóm xu hướng của cột thắng (định nghĩa ở KQ10 mục 4): `bậc tại mốc` là cột đổi tại mốc sự cố; `trôi nền` là cột đã trôi từ trước mốc.

| Vị trí của thực thể đứng trên root | BARO: số cặp; bậc tại mốc / trôi nền / khác / không dịch | SimpleRCA: số cặp; bậc tại mốc / trôi nền / khác |
|---|---|---|
| Phía trên root | 8; 3 / 0 / 5 / 0 | 6; 3 / 0 / 3 |
| Hai chiều | 3; 0 / 0 / 3 / 0 | 1; 0 / 0 / 1 |
| Phía dưới root | 10; 2 / 1 / 5 / 2 | 0 |
| Không liên hệ | 38; 3 / 6 / 27 / 2 | 6; 1 / 1 / 4 |
| Không có span | 44; 6 / 12 / 26 / 0 | 7; 2 / 5 / 0 |
| Cộng | 103; 14 / 19 / 66 / 4 | 20; 6 / 6 / 8 |

- Trên mọi thực thể của 30 ca (không chỉ thực thể đứng trên root), tỷ lệ thực thể có cột thắng thuộc nhóm `bậc tại mốc`: 19,5% ở thực thể nằm trên chuỗi gọi qua root (41/210), 11,2% ở thực thể không liên hệ (59/528), 9,3% ở thực thể không có span (118/1.272) theo góc nhìn của BARO; 22,4%, 11,9% và 5,7% theo góc nhìn của SimpleRCA (`/step_at_t/share_step_among_*`, `/all_entities_position_by_trend_group`).
- Lưu lượng: trong 100 thực thể có span và có cột thắng `bậc tại mốc` (BARO), 19 thực thể có số span đổi quá khoảng 0,8–1,25 so với trung vị của ca, 81 không đổi (`/step_at_t/traffic_changed_among_step_with_span`). Ở các thực thể đứng trên root: phía trên 1/8 đổi, phía dưới 0/10, hai chiều 0/3, không liên hệ 10/38.
- Theo loại lỗi, 14 cặp `bậc tại mốc` của BARO nằm ở lỗi loss (9), delay (3), cpu (2) (`/step_at_t/by_fault_above`).

**Quan sát ở Nezha-OB** (không có nhóm xu hướng vì metric chỉ 5 mẫu mỗi phía; `/summary/Nezha-OB/<phương pháp>/above_position_by_kind`, `/above_traffic_changed_by_position`).

- BARO, 59 cặp: phía dưới root 28, không liên hệ 24, phía trên 7. Ở nhóm phía dưới, cột thắng là lưu lượng mạng nhận hoặc gửi ở 10/28 cặp, độ trễ ở 10/28. Ở nhóm phía trên, cả 7 cột thắng là cột độ trễ.
- Lưu lượng của thực thể đứng trên root đổi ở 14/28 thực thể phía dưới, 6/24 không liên hệ, 1/7 phía trên. Trên mọi thực thể: 23/52 phía dưới, 20/116 không liên hệ, 4/30 phía trên (`/all_traffic_changed_by_position`).
- SimpleRCA, 44 cặp: phía dưới 16 (lưu lượng đổi 8/16), không liên hệ 19 (4/19), phía trên 9 (1/9); ở nhóm phía trên, 5/9 cột thắng là cột độ trễ phía trước (`FrontLatency`).

**Đối chiếu với cách đọc khai trước.**

- Cột đổi thật tại mốc có nghiêng về chuỗi gọi qua root: tỷ lệ gấp khoảng 1,7–2 lần so với thực thể không liên hệ ở RE2-TT. Vậy một phần bất thường metric ở dịch vụ khác có đi theo quan hệ gọi.
- Nhưng phần đó nhỏ so với toàn bộ: trong 103 cặp của BARO ở RE2-TT chỉ 5 cặp vừa nằm trên chuỗi gọi vừa có cột thắng `bậc tại mốc`; 82 cặp nằm ngoài chuỗi gọi hoặc không có span. Dự đoán "phần lớn không đi theo quan hệ gọi" đúng với RE2-TT.
- Ở Nezha-OB có một hiện tượng theo quan hệ gọi rõ hơn, theo chiều **xuôi**: lưu lượng qua các dịch vụ được root gọi đổi ở khoảng một nửa số thực thể (23/52), gấp khoảng 2,5 lần nhóm không liên hệ (20/116), và cột thắng của các thực thể đó hay là cột lưu lượng mạng. Đây là mô tả; chưa có phép kiểm nào xác lập rằng lưu lượng đổi là do root.

**Kết luận ở mức mô tả, chỉ trên dev.**

- Ở RE2-TT, thứ làm BARO và SimpleRCA xếp dịch vụ khác trên root phần lớn không nằm trên chuỗi gọi qua root: cột trôi từ trước mốc (19/103 và 6/20), cột của thực thể không có span (44/103 và 7/20), cột thuộc nhóm "khác" của thực thể không liên hệ. Quan hệ gọi tới root không giải thích được các cặp này; khử xu hướng nền và thang chuẩn hóa (KQ9 mục 5, KQ10 mục 4) mới là chỗ chạm tới chúng.
- Phần đi theo quan hệ gọi gồm hai dạng. Phía trên root: cột thắng là cột độ trễ ở 5/8 cặp BARO và 4/6 cặp SimpleRCA của RE2-TT (`/above_position_by_kind`), và thuộc nhóm `bậc tại mốc` ở 3/8 và 3/6 cặp; cả 7 cặp phía trên của BARO ở Nezha-OB là cột độ trễ. Điều này khớp với việc dịch vụ gọi chờ root (mục 2.1), nhưng bảng không nối từng cột với từng lời gọi. Phía dưới root ở Nezha-OB: lưu lượng đổi.
- Hệ quả cho đầu ra P4 số 4, ở mức ứng viên: với kênh metric, quan hệ gọi bổ sung được thông tin cho hai dạng trên; nó không thay được bước xử lý trôi nền, và không nói gì về thực thể không có span.

**Chưa trả lời, và phép kiểm cụ thể.** Các cột `bậc tại mốc` của thực thể không liên hệ và không có span (59 + 118 thực thể theo BARO) đổi tại mốc vì đâu: tài nguyên chung của máy, tải chung, hay tác dụng phụ của công cụ tiêm lỗi. Dữ liệu dev không có thông tin dịch vụ nào chạy trên máy nào (RE2-TT không công bố), nên **không phân xử được bằng dữ liệu hiện có**. Yêu cầu quan sát rút ra cho FlashTicket: ghi quan hệ dịch vụ–máy và metric mức máy, để tách "cùng máy" khỏi "cùng chuỗi gọi".

**Giới hạn.** Mốc 0,8–1,25 cho lưu lượng và các mốc chia nhóm xu hướng do tôi đặt. 9 ca sai của BARO và 5 ca sai của SimpleRCA ở RE2-TT; Nezha-OB không có nhóm xu hướng. Tỷ lệ trên mọi thực thể gộp 30 ca có cùng đồ thị gọi, nên không phải 30 quan sát độc lập.

## 4. Việc 4 — bộ chia trace theo công thức của bài MicroRank gốc, với span đầu do ta quy ước

Thiết kế viết trước: `thiet-ke-phep-doi-009.md`; bản sửa việc 4 và kết quả kiểm với code gốc ở cuối `goi-bo-sung-007.md` (Q-135). Tên gọi của mọi kết quả ở mục này: "công thức của bài gốc với span đầu do ta quy ước". Không phải MicroRank gốc.

### 4.1 Bước đếm (xong; không chạy phương pháp, không dùng nhãn)

Nguồn: `runs/trace-root-census-001/summary.json` (script `scripts/trace_root_census_v1.py`, EC2, 52 bảng span như lượt `chain-spanpass-001`). Con trỏ: `/summary/<dataset>/<trường>`, `/cases/*`.

| | RE2-TT (30 ca) | Nezha-OB (22 ca) |
|---|---|---|
| Ca đạt mốc 90% trace sau mốc có đúng một span đầu | 29 | 22 |
| Tỷ lệ đó theo ca: nhỏ nhất; trung vị | 83,5%; 99,9% | 97,6%; 99,8% |
| Trace sau mốc: tổng; không có span đầu; đúng một; từ hai | 39.724; 261; 39.463; 0 | 19.080; 0; 19.022; 58 |
| Trace sau mốc có span mất cha; trace vắt qua mốc | 997; 35 | 58; 61 |
| Trace một span đầu mà span đầu bao trọn mọi span khác | 39.256/39.463 | 18.761/19.022 |
| Trace đủ span mà tổng "thời lượng trừ tổng span con" bằng thời lượng span đầu | 38.727/38.727 | 19.022/19.022 |
| Span mà "trừ tổng span con" khác "trừ phần được span con che" | 227.470/9.514.577 | 278.798/1.421.887 |
| Span có "thời lượng trừ tổng span con" âm | 5.340 | 90.779 |
| Trace nền: tổng; dùng được; bỏ vì không có span đầu; bỏ vì mất cha; bỏ vì span đầu sau trừ dài hơn 1 giây | 41.886; 40.699; 254; 759; 174 | 13.504; 13.462; 0; 42; 0 |
| Số trace nền dùng được theo ca: nhỏ nhất; lớn nhất | 388; 1.566 | 348; 861 |
| Ca có thao tác cần mà không có mức nền | 5 | 0 |
| Dịch vụ của span đầu | 13 dịch vụ, không có `frontend` | chỉ `frontend` |

**Đọc bảng.**

- **Mốc dừng đã duyệt:** RE2-TT đạt ở 29/30 ca, Nezha-OB đạt ở 22/22 ca; không dataset nào phải dừng. Ca không đạt là `dev-746fd74313` (83,5%): 949/1.293 trace sau mốc của ca này có span mất cha, và 86 thao tác không có mức nền. Ca này ghi N/A cho hai nhánh; đây là hạn chế của dữ liệu ở riêng ca đó.
- **Quy ước span đầu dùng được:** hai dataset đều đánh dấu span đầu tường minh (trường cha trống ở RE2-TT, chữ `root` ở Nezha-OB), nên phân biệt được span đầu thật với span mất cha. Ở Nezha-OB mọi span đầu thuộc `frontend`, gần với luật của code gốc. Ở RE2-TT span đầu thuộc 13 dịch vụ mà bộ sinh tải gọi vào.
- **Phép tự kiểm của công thức đạt:** đẳng thức ở dòng 6 đúng ở mọi trace đủ span. Đây là lý do code gốc trừ tổng thời lượng span con: chỉ như vậy "mức dự kiến của cả yêu cầu" mới so được với thời lượng span đầu.
- **Hai cách trừ khác nhau đáng kể ở Nezha-OB:** 19,6% span cho kết quả khác, 6,4% span có giá trị âm (span con chạy chồng nhau). Ở RE2-TT là 2,4% và 0,06%. Đây là lý do bản sửa việc 4 yêu cầu làm theo code gốc thay vì "phần không được span con che".
- **Bốn ca nguồn ERROR của RE2-TT vẫn ERROR:** cùng thiếu mức nền của thao tác `ts-order-other-service_getMore ts.orders`, như ở bản đang dùng.
- **Giới hạn đã thấy ngay ở bước đếm:** mức nền chỉ học trên 348–1.566 trace mỗi ca (tác giả khuyên khoảng một giờ dữ liệu); bộ lọc 1 giây của code gốc bỏ 174 trace nền ở RE2-TT.

### 4.2 Hai nhánh chia trace (xong sau khi Minh giải phóng RAM laptop)

Nguồn: lượt `runs/microrank-partition-001/` trên laptop (script `scripts/laptop_contrast_v5.py` cho 28 nhánh đầu, `scripts/laptop_contrast_v6.py` cho phần còn lại; v6 chỉ thêm tùy chọn lọc theo dataset, phần tính toán giống hệt); tổng hợp `runs/microrank-partition-001/collect-001/summary.json` (script `scripts/laptop_contrast_collect_v4.py`). Bước duy nhất bị đổi: hai tập trace "bất thường" và "bình thường"; đồ thị, PageRank, đếm phủ, spectrum và ánh xạ sang dịch vụ giữ nguyên.

**Kiểm.** Nhánh giữ nguyên đi qua đúng chỗ móc khớp bản đóng băng từng bit ở 52/52 ca (48 OK, 4 ERROR tái lập đúng ERROR); hạng root của nhánh giữ nguyên trùng T-028 ở mọi ca OK (`/summary/self_check`). 156/156 tiến trình con xong, 653 giây, RAM hệ thống đỉnh 84,7%, không lần giết nào (`terminal-*.json`). Lượt bị dừng giữa chừng lúc 05:44Z vì RAM (mục LOG phiên 11); chạy tiếp lúc 06:25Z bỏ qua 28 nhánh đã xong.

**Trạng thái theo ca** (`/summary/<dataset>/<nhánh>/state`): RE2-TT 25 ca tính được, 4 ca nguồn ERROR (thiếu mức nền của một thao tác, như bản đang dùng), 1 ca N/A theo mốc 90% của bước đếm. Nezha-OB 22 ca tính được. Không ca nào rơi vào trạng thái "một nhóm rỗng".

**Quan sát** (`/summary/<dataset>/<nhánh>`; `mo15` là luật của bài, `mo1p50` là luật chia nhóm của code; cột "gốc" là bản đang dùng trên cùng các ca tính được):

| | RE2-TT gốc | `mo15` | `mo1p50` | Nezha-OB gốc | `mo15` | `mo1p50` |
|---|---|---|---|---|---|---|
| Tỷ lệ trace sau mốc bị xếp bất thường (trung vị) | 50,1% | 10,0% | 12,3% | 33,0% | 1,5% | 2,6% |
| Số trace bất thường mỗi ca: nhỏ nhất; trung vị | | 55; 139 | 54; 163 | | 2; 12 | 1; 21 |
| Tỷ lệ trace bất thường có span của root (trung vị) | 51,7% | 70,3% | 62,7% | 29,1% | 52,0% | 53,4% |
| Root tăng / không đổi / giảm hạng | | 19 / 3 / 3 | 20 / 2 / 3 | | 15 / 3 / 4 | 13 / 5 / 4 |
| Hit@1 | 2/25 | 14 | 15 | 0/22 | 7 | 7 |
| Hit@5 | 13/25 | 23 | 23 | 8/22 | 14 | 14 |
| Cặp đứng trên root của bản gốc: còn / mất | 123 cặp | 13 / 110 | 12 / 111 | 120 cặp | 53 / 67 | 55 / 65 |
| Cặp mới xuất hiện | | 17 | 13 | | 13 | 12 |

- Thực thể đứng đầu khi root không hạng 1 (`/top_entity_when_root_not_first`): ở bản gốc là `ts-station-service` 20 ca và `ts-route-service` 3 ca (RE2-TT), `currencyservice` 13, `cartservice` 5, `productcatalogservice` 4 (Nezha-OB). Dưới `mo15`: `ts-auth-service` 7, `ts-admin-travel-service` 2, hai dịch vụ khác mỗi dịch vụ 1 (RE2-TT); `cartservice` 7, `frontend` 2, `adservice` 2, `recommendationservice` 1 (Nezha-OB).
- Theo loại lỗi dưới `mo15`, số ca root hạng 1 trên số ca tính được (`/by_fault`): RE2-TT cpu 3/6, delay 3/4, disk 3/6, loss 2/5, mem 2/2, socket 1/2; Nezha-OB cpu_consumed 2/4, cpu_contention 1/5, exception 1/3, network_delay 1/6, return 2/4. Dưới `mo1p50` ở Nezha-OB: 3/4, 1/5, 1/3, 2/6, 0/4.
- Các trace bất thường theo luật mới phần lớn cũng bất thường theo bản gốc: trung vị 76% ở RE2-TT, 100% ở Nezha-OB (đọc từ `/cases/*/branches/*/call`).

**Đối chiếu với dự đoán khai trước.**

- **Dự đoán "hạn chế thuộc bước chia của bản thư viện" được hỗ trợ.** Tỷ lệ trace bất thường giảm mạnh (50% xuống 10–12% ở RE2-TT; 33% xuống 1,5–2,6% ở Nezha-OB), phần còn lại chứa root nhiều hơn, và root tăng hạng ở 19–20/25 ca RE2-TT và 13–15/22 ca Nezha-OB. Gộp hai dataset: Hit@1 từ 2/47 lên 21 (`mo15`) hoặc 22 (`mo1p50`); 176–177 trong 243 cặp đứng trên root biến mất (`/summary/all`).
- **Dự đoán "thuộc cách tính của bài" không được hỗ trợ** cho phần lớn ca: thứ hạng đổi mạnh khi chỉ đổi bước chia. Phần còn lại (25–26/47 ca root chưa hạng 1) chưa có phép đổi nào giải thích.
- Hai luật cho kết quả gần nhau; không chọn luật nào.

**Kết luận ở mức tính toán.** Trong điều kiện một trace có nhiều span, bước chia "có bất kỳ span nào vượt mức nền cộng 3 lần độ lệch chuẩn" của bản thư viện xếp khoảng một nửa trace vào nhóm bất thường, phần lớn không gắn với root (mục 2.2); thông tin "trace nào thật sự chậm" bị mất trước khi tới bước đếm phủ. Thay riêng bước chia bằng công thức của bài gốc (so thời gian cả yêu cầu với tổng mức nền của các thao tác) trả lại thông tin đó. Đây là hạn chế thuộc **bản thư viện** (loại adapter hoặc biến thể), không gán được cho bài MicroRank gốc. So với hai phép đổi trước của KQ9 trên MicroRank: bỏ trọng số PageRank đưa Hit@1 từ 2 lên 11, đếm riêng thay đếm phủ lên 19 (trên 48 ca); đổi bước chia lên 21–22 (trên 47 ca) và là phép duy nhất có tác dụng rõ ở Nezha-OB (0 lên 7).

**Giới hạn, phải đọc kèm.**

- Kết quả là của "công thức của bài gốc với span đầu do ta quy ước", không phải MicroRank gốc: không có nhãn loại span, định danh thao tác của biến thể đang dùng, mức nền học trên 348–1.566 trace thay cho khoảng một giờ dữ liệu.
- Ở Nezha-OB số trace bất thường rất ít (trung vị 12, có ca chỉ 1–2 trace). Thứ hạng dựng trên vài trace kém ổn định; ví dụ lỗi `return` được 2/4 ca hạng 1 dưới `mo15` nhưng 0/4 dưới `mo1p50`, trong khi mục 7 cho thấy loại lỗi này không để lại tín hiệu thời lượng. Không đọc số Nezha-OB theo từng loại lỗi.
- Hai nhánh được nghĩ ra sau khi đã xem kết quả dev của bản đang dùng; đây là bằng chứng trên dev, không phải số đo trên test.
- Phép đổi làm đổi cả tập trace lẫn số trace của hai nhóm, nên là tác động tổng của bước chia.

## 5. Việc 5 — đọc toàn văn bài TraceRCA gốc

**Nguồn.** Li và cộng sự, "Practical Root Cause Localization for Microservice Systems via Trace Analysis", IWQoS 2021. Bản PDF lấy từ trang của nhóm tác giả (`netman.aiops.org/wp-content/uploads/2021/05/1570705191.pdf`, 386 KB, sha256 771c24d0…); tôi đọc bản chữ trích bằng `pdftotext`. Không chép toàn văn vào repo; dưới đây là tóm tắt bằng lời của tôi, kèm số mục của bài. Kho mã của tác giả (`github.com/NetManAIOps/TraceRCA`) chỉ xem trang giới thiệu, không chạy.

**Bài gốc làm gì, theo từng bước (Mục III của bài).**

1. **Đơn vị là lời gọi, không phải span.** Mỗi lời gọi thuộc một cặp (dịch vụ gọi, dịch vụ được gọi). Mức nền (trung bình, độ lệch chuẩn) học riêng cho từng cặp và từng đặc trưng (III-A).
2. **Nhiều đặc trưng, có bước chọn.** Với Train-Ticket bài dùng độ trễ và mã trạng thái HTTP của lời gọi, cùng CPU, bộ nhớ, mạng, đĩa của dịch vụ. Với mỗi sự cố chỉ giữ đặc trưng có mức lệch trung bình sau sự cố tăng hơn 10% so với trước. Lời gọi là bất thường khi lệch quá 1 lần độ lệch chuẩn ở bất kỳ đặc trưng được giữ nào. Trace là bất thường khi có ít nhất một lời gọi bất thường (III-A).
3. **Hai chỉ số định nghĩa trên trace và trên tập dịch vụ.** Support là tỷ lệ trace bất thường đi qua mọi dịch vụ của tập; confidence là tỷ lệ trace bất thường trong các trace đi qua tập. Tập ứng viên lấy bằng khai phá tập phổ biến với ngưỡng support 10%, rồi xếp theo chỉ số Jaccard giữa "trace đi qua tập" và "trace bất thường", giữ 100 tập đầu (III-B).
4. **Bước xếp hạng dịch vụ có xét hướng lan.** Trong mỗi tập, điểm của một dịch vụ là hiệu giữa số trace có lời gọi bất thường **đi vào** nó và số trace có lời gọi bất thường **đi ra** từ nó. Dịch vụ có cả lời gọi vào và lời gọi ra bất thường được coi là chỉ bị ảnh hưởng, bất thường đi qua nó. Điểm cuối là tích của chỉ số Jaccard của tập và điểm trong tập, lấy lớn nhất qua các tập (III-C).

**Tác giả tự nêu những giới hạn nào.**

- Bước xét hướng lan bị hạn chế khi bất thường truyền theo cả hai chiều; bài viết: "our method is limited when the anomaly propagates both upstream and downstream" (III-C), và cho rằng trường hợp đó hiếm với lỗi hạ tầng.
- Không mô phỏng được trường hợp lỗi chỉ bị kích hoạt khi trace đi qua một tập dịch vụ cụ thể, do giới hạn của việc tiêm lỗi (III-B).
- Kết quả phụ thuộc chất lượng bước phát hiện trace bất thường; bài thử bằng cách đảo ngẫu nhiên kết quả phát hiện (IV-C).
- Ở phần bài học triển khai (Mục V), tác giả mô tả đúng hiện tượng T-032 đang xét: với các dịch vụ phía gọi, độ trễ phản hồi tăng khi chúng phải chờ dịch vụ lỗi; và metric bất thường khác nhau giữa các dịch vụ dù cùng một sự cố.

**Bản trong thư viện RCAEval khác bài gốc ở đâu** (đối chiếu với `results/T-015/tracerca-rcaeval.md` và mục 2.1 ở trên).

| Bước | Bài gốc | Bản RCAEval đang dùng |
|---|---|---|
| Đơn vị | lời gọi theo cặp dịch vụ | span theo thao tác của một dịch vụ |
| Đặc trưng | nhiều đặc trưng, chọn theo từng sự cố | chỉ thời lượng span, không chọn |
| Ngưỡng | lệch quá 1 lần độ lệch chuẩn | mức nền cộng 3 lần độ lệch chuẩn |
| Support, confidence | trên trace và tập dịch vụ | trên span của một thao tác: a/H và a/n |
| Điểm | chỉ số Jaccard của tập × hiệu số lời gọi bất thường vào và ra | trung bình điều hòa 2a/(n + H), lấy lớn nhất theo dịch vụ |
| Xét hướng lan | có (bước 4 ở trên) | **không có** |

**Hệ quả cho bảng đối chiếu (thay ô "chưa đối chiếu được" của dòng 4).**

- Hạn chế "chấm thời gian chờ root thành bất thường của dịch vụ gọi" (mục 2.1) thuộc **bản thư viện**, không gán được cho bài gốc: bài gốc nhận ra hiện tượng lan giữa dịch vụ gọi và dịch vụ được gọi, và có riêng một bước để xử lý. Bản thư viện bỏ bước đó.
- Hạn chế "điểm nghiêng về số span mang cờ tuyệt đối" (mục 2.1) cũng thuộc bản thư viện: support của bài gốc đếm trace đi qua dịch vụ, không đếm span.
- Tác giả có nêu giới hạn của chính bước xét hướng lan (lan hai chiều). Bản cài theo lời văn của bài đã chạy sau đó (mục 9): trên dev, bước này không tách được root khỏi dịch vụ gọi đang chờ nó. Mã của tác giả vẫn chưa chạy (kho mã nhận định dạng dữ liệu riêng, `tracerca-rcaeval.md` mục 9).
- Ý nghĩa cho P5–P6, ở mức ứng viên: bước "hiệu số lời gọi bất thường vào và ra" của bài gốc là một phép tính dùng cạnh gọi có hướng để tách dịch vụ gây ra khỏi dịch vụ bị ảnh hưởng. Đây là phương án có sẵn trong tài liệu, cần được xét cùng ứng viên "tách bất thường tự sinh và kế thừa" của kế hoạch nghiên cứu, không phải ý mới của T-032. Mục 9 cho thấy dạng lấy trị tuyệt đối của bài không đủ; phép tính phải giữ hướng của cạnh.

**Giới hạn của việc đọc.** Tôi đọc bản chữ trích tự động, công thức bị vỡ dòng; các định nghĩa trên lấy từ phần lời văn và ví dụ Hình 2 của bài. Chưa đọc mã nguồn của tác giả để kiểm bài và mã có khớp nhau không.

## 6. Việc 6 — TORAI với bảng của tác giả (nguồn A): hiện tượng ở nguồn log có lặp lại không

Nguồn: lượt phát lại EC2 `runs/torai-a-obs-001/` (script `scripts/torai_core_obs_a_v1.py`, tạo từ bản của nguồn B, khác đúng ba điểm ghi ở đầu file); bảng `runs/torai-severity-table-a-001/summary.json`, `runs/torai-log-source-a-001/summary.json`, `runs/torai-log-placebo-a-001/summary.json` (ba script tạo từ bản của nguồn B bằng phép thay đường dẫn). Số của nguồn B lấy từ KQ10 mục 5 và các file `runs/torai-severity-table-003`, `runs/torai-log-source-001`, `runs/torai-log-placebo-001`.

**Lưu ý trước khi đọc.** Nguồn A nằm ngoài cấu hình chính đã khóa. Bảng của tác giả lệch cửa sổ so với các phương pháp khác (WHY-29), nên ở đây **chỉ so hiện tượng, không so độ chính xác**. Số Hit@1 của nguồn A chỉ để định vị ca sai, không dùng để xếp hạng phương pháp.

**Kiểm.** Phát lại: 90/90 đơn vị cho bản ghi trùng 90 bản ghi đóng băng của nguồn A từng bit; nhánh quan sát trùng nhánh giữ nguyên ở 90/90; 2.769 giây (`runs/torai-a-obs-001/progress.jsonl`, `terminal-*.json` trên EC2). Bảng: severity bằng trung bình hàng 90/90; điểm cụm dựng lại 90/90; thứ tự khối 90/90; trung gian trước bước RCD giống nhau giữa ba seed ở 30/30 ca (`/summary/checks`, `/cases_three_seeds_same_pre_rcd_intermediates`). Điểm log tính lại từ bảng log trùng trung gian ở 30/30 ca. Đối chiếu ngoài: tổng Hit@1 của nguồn A trong file chấm đóng băng `results/T-024/cham-a.json` → `/methods/torai_A/per_case` là 21 trên 30 ca, trùng bảng mới. Trường `self_check_rank_equals_t028` của bảng nguồn A so với hạng của TORAI B nên không phải tự kiểm (66/90 trùng); ghi rõ ở đầu script.

**Quan sát, seed 0** (`/summary/seed0` của hai bảng severity; `/summary` của hai bảng log):

| | Nguồn B (bảng ta dựng) | Nguồn A (bảng của tác giả) |
|---|---|---|
| Ca root không đứng hạng 1 | 4/30 | 9/30 |
| Root có severity cao nhất: ở ca đúng; ở ca sai | 26/26; 0/4 | 21/21; 0/9 |
| Số cặp (thực thể đứng trên root, root) | 7 | 22 |
| Nguồn nghiêng nhiều nhất về thực thể kia: log / trace_lat / metric | 7 / 0 / 0 | 5 / 13 / 4 |
| Ca root đứng đầu theo riêng từng nguồn: metric / log / trace_lat | 23 / 2 / 22 | 23 / 4 / 10 |
| Dịch vụ đứng đầu theo log nhiều ca nhất | `ts-order-other-service` 14/29 | `ts-preserve-other-service` 7/30 |
| Ca mà cột log cao nhất của dịch vụ đứng đầu có nền không đổi | 20/29 | 7/30 |
| Tỷ lệ cột log có nền không đổi (trung vị; lớn nhất) | 27%; 57% | 0%; 20% |
| Phần điểm log nằm ở các cột đó (trung vị; lớn nhất) | 55%; 90% | 0%; 87% |
| Cặp đứng trên root mà cột log cao nhất của thực thể có nền không đổi | 7/7 | 2/22 |
| Phép thử giả (mốc lùi 150 giây): dịch vụ đứng đầu theo log trùng bảng chính | 12/29 | 2/30 |
| Nguồn trace_err rỗng | 30/30 | 30/30 |

- Ở nguồn A, 6/9 ca sai có root `ts-auth-service` (ba ca cpu, ba ca delay); ba ca còn lại là `ts-travel-service` lỗi loss (2 ca) và `ts-order-service` lỗi loss (`/summary/seed0/wrong_cases`).
- Ở nguồn A, bảng trace_err có cột khác 0 ở 10/30 ca nhưng mọi cột đều không đổi trong cửa sổ, nên vẫn bị loại hết (`runs/torai-log-placebo-a-001/summary.json` → `/summary/trace_err`).

**Đối chiếu với cách đọc khai trước** (hiện tượng lặp lại: của phương pháp; không lặp lại: của đầu vào ta dựng).

- **Hiện tượng "điểm log dồn về vài dịch vụ có mẫu log mới xuất hiện sau mốc" không lặp lại ở bảng của tác giả.** Ở nguồn A, cột log có nền không đổi hiếm (trung vị 0% số cột, 0% điểm), dịch vụ đứng đầu theo log không cố định, phép thử giả không cho cùng dịch vụ, và log chỉ là nguồn nghiêng nhiều nhất ở 5/22 cặp. Vậy hiện tượng mô tả ở KQ10 mục 5 và 8 thuộc **bảng log do ta dựng cho nguồn B** (tách mẫu log riêng từng dịch vụ, đánh số theo thứ tự xuất hiện; WHY-29), không gán được cho TORAI của tác giả.
- **Điều lặp lại ở cả hai nguồn** là cấu trúc của phương pháp: root mất hạng ở bước severity (0/4 và 0/9 ca sai có root đứng đầu theo severity; đứng đầu ở đúng các ca đúng), còn bước phân cụm và bước RCD không quyết định vị trí root. Cách chấm "cột có nền không đổi thì z bằng số đếm thô" vẫn có trong phương pháp và vẫn có thể chiếm tới 87% điểm log ở một ca của nguồn A; nó chỉ không phải thứ quyết định ở đa số ca.
- **Ở nguồn A, nguồn nghiêng nhiều nhất là trace_lat (13/22 cặp)**, và root chỉ đứng đầu theo trace_lat ở 10/30 ca, so với 22/30 ở nguồn B. Chưa biết vì sao: bảng trace của tác giả được dựng với cửa sổ và cách gộp khác. Đây là quan sát, chưa có giải thích; không thuộc câu hỏi của việc 6.

**Kết luận dùng được cho bảng đối chiếu (dòng 14).** Hạn chế của TORAI B về nguồn log là hạn chế của **đầu vào do ta dựng** (loại adapter), không phải của phương pháp theo bảng của tác giả. Câu nói được trước giảng viên: "ở cấu hình chính, bỏ nguồn log thì hai trong bốn ca sai của TORAI thành đúng, và nguồn log đó là bảng do chúng em dựng; với bảng log của tác giả hiện tượng đó không còn, nhưng phương pháp sai ở những ca khác, nơi nguồn trace nghiêng về dịch vụ khác". Không rút kết luận nào về đồ thị nhân quả từ TORAI ở cả hai nguồn.

**Phần "các cột log còn lại" của việc 6 (làm sau, cùng phiên).** Nguồn: `runs/torai-log-remaining-001/summary.json` (script `scripts/torai_log_remaining_v1.py`, EC2; định nghĩa ghi ở đầu script trước khi chạy, theo phép kiểm đã nêu ở KQ10 mục 8). Bảng log của nguồn B được dựng lại đúng như hàm của adapter, có giữ thêm văn bản mẫu log; bảng dựng lại trùng bảng đã lưu của lượt phát lại ở mọi ô, 29/29 ca có log (`/summary/rebuild_equals_saved`).

- Sau khi bỏ các cột có nền không đổi, dịch vụ đứng đầu theo log vẫn là `ts-order-other-service` ở 9/29 ca (trước khi bỏ: 14/29), `ts-order-service` 4, `ts-seat-service` 4; trong ba dịch vụ đầu: `ts-order-other-service` 16 ca, `ts-seat-service` 15, `ts-order-service` 12. Dịch vụ đứng đầu là root ở 1/29 ca (`/summary/top_service_kept_columns`, `/top3_membership_kept`, `/top_service_kept_is_root`).
- Cột cao nhất của dịch vụ đứng đầu: ở 17/29 ca cột đó chỉ khác 0 ở không quá 3 trong 20 bin trước mốc (trung vị 1 bin), và tăng sau mốc ở 23/29 ca (`/summary/top_column_of_top_service`). Riêng 31 cột cao nhất của `ts-order-other-service` và `ts-seat-service`: 22/31 chỉ khác 0 ở không quá 3 bin, 29/31 tăng sau mốc (`/summary/top_columns_order_other_and_seat`).
- Các mẫu log đó là dòng mang dữ liệu của từng yêu cầu, ví dụ mẫu của `SeatServiceImpl` in kết quả vé đã đặt, mẫu của `OrderOtherServiceImpl` in thông tin vé còn và danh sách ga. Bộ tách mẫu không gộp được các dòng này nên sinh nhiều mẫu hiếm.

**Trả lời câu KQ10 mục 8 để mở.** Mốc "nền không đổi" (độ lệch chuẩn bằng 0) không phải ranh giới của hiện tượng. Mẫu log hiếm, chỉ xuất hiện ở một vài bin trước mốc, có độ lệch chuẩn rất nhỏ nhưng khác 0, nên vẫn cho z rất lớn khi xuất hiện thêm vài lần sau mốc. Vì vậy bỏ riêng cột nền không đổi không trả lại hạng cho root. Hiện tượng vẫn thuộc cách dựng bảng log (dòng log mang dữ liệu thay đổi bị tách thành nhiều mẫu), khớp với kết luận ở trên rằng nó không lặp lại ở bảng của tác giả.

**Giới hạn.** Chỉ 30 ca dev RE2-TT. So hai nguồn chỉ ở mức hiện tượng vì cửa sổ khác nhau. Các số theo seed 0; trung gian trước bước RCD giống nhau giữa ba seed, và tổng Hit@1 trong file chấm đóng băng cho thấy ba seed cho cùng Hit@1 ở mọi ca của nguồn A.

## 7. Việc 7 — chia theo loại lỗi phần đối chiếu metric của bảng vị trí tín hiệu

Nguồn: `runs/root-signal-by-fault-001/summary.json` (script `scripts/root_signal_by_fault_v1.py`), chỉ đếm lại từ `runs/root-signal-location-001/summary.json`. Thiết kế: `thiet-ke-kenh-metric-010.md` mục 3. Tự kiểm: tổng theo dataset trùng KQ10 mục 3 (trên 26 ca RE2-TT có bảng span: BARO xếp root hạng 1 ở 18 ca, SimpleRCA 21, TraceRCA 21; `/totals`).

Cột "vị trí trace" là số ca root đứng đầu ở ít nhất một trong năm vị trí của bảng A; "chỉ phía gọi" là số ca root chỉ đứng đầu ở vị trí span phía gọi. Con trỏ: `/by_dataset_fault/<dataset>|<loại lỗi>`.

| Dataset, loại lỗi | Số ca (có bảng span) | Root hạng 1: BARO / SimpleRCA / TraceRCA | Vị trí trace (chỉ phía gọi) | Phiếu metric của root: trung vị (nhỏ nhất) | Không kênh nào thấy root |
|---|---|---|---|---|---|
| RE2-TT cpu | 6 (6) | 4 / 6 / 6 | 6 (0) | 1.331,5 (1.290) | 0 |
| RE2-TT delay | 6 (5) | 2 / 3 / 5 | 5 (0) | 838 (509) | 0 |
| RE2-TT disk | 6 (6) | 6 / 6 / 4 | 6 (0) | 1.401 (1.160) | 0 |
| RE2-TT loss | 6 (5) | 3 / 2 / 2 | 5 (0) | 664 (240) | 0 |
| RE2-TT mem | 3 (2) | 1 / 2 / 2 | 2 (0) | 1.580,5 (1.446) | 0 |
| RE2-TT socket | 3 (2) | 2 / 2 / 2 | 2 (0) | 1.472 (1.441) | 0 |
| Nezha-OB cpu_consumed | 4 (4) | 2 / 0 / 2 | 3 (0) | 11 (2) | 1 |
| Nezha-OB cpu_contention | 5 (5) | 5 / 5 / 0 | 5 (3) | 34 (27) | 0 |
| Nezha-OB exception | 3 (3) | 1 / 1 / 0 | 2 (0) | 10 (9) | 0 |
| Nezha-OB network_delay | 6 (6) | 0 / 1 / 0 | 6 (4) | 4 (0) | 0 |
| Nezha-OB return | 4 (4) | 0 / 0 / 0 | 1 (0) | 1,5 (0) | 3 |

Các số của ba phương pháp trong bảng chỉ tính trên ca có bảng span; 4 ca RE2-TT không có bảng span không nằm trong các cột đó.

**Đọc bảng, chỉ ở mức mô tả.**

- Nezha-OB, lỗi trễ mạng: cả ba phương pháp gần như không xếp được root hạng 1 (0, 1, 0 trên 6 ca), trong khi trace có tín hiệu ở cả 6 ca và ở 4 ca tín hiệu chỉ nằm ở span phía gọi. Kênh metric của root yếu (trung vị 4 phiếu, 2 ca không có phiếu nào).
- Nezha-OB, lỗi `return`: 3/4 ca không kênh nào thấy root (không đứng đầu ở vị trí trace nào, BARO và SimpleRCA đều sai). Đây là giới hạn của dữ liệu với loại lỗi này, không phải của một phương pháp.
- Nezha-OB, lỗi tranh chấp CPU: metric thấy root ở 5/5 ca (BARO, SimpleRCA), TraceRCA 0/5; ở 3/5 ca tín hiệu trace chỉ nằm ở span phía gọi.
- RE2-TT: không loại lỗi nào mà root thiếu tín hiệu ở mọi kênh. Lỗi loss là nơi cả ba phương pháp kém nhất (3, 2, 2 trên 5 ca) và phiếu metric của root thấp nhất.
- Mỗi ô chỉ có 2–6 ca; bảng dùng để biết ca nào thuộc loại "dữ liệu không mang tín hiệu", không dùng để rút mẫu hình theo loại lỗi.

## 8. Phép kiểm ngoài gói thứ nhất — đổi công thức điểm của TraceRCA bản thư viện sang tỷ lệ (Minh duyệt trong chat ngày 11/10)

Nguồn: `runs/tracerca-score-contrast-001/summary.json` (script `scripts/tracerca_score_contrast_v1.py`, EC2). Thiết kế viết trước: `thiet-ke-phep-doi-011.md` mục 2. Bước duy nhất bị đổi là điểm của thao tác; cờ từng span, tập thao tác ứng viên, phép lấy lớn nhất theo dịch vụ và cách xếp hạng giữ nguyên.

**Kiểm.** Nhánh giữ nguyên (điểm 2a/(n + H) tính bằng phân số chính xác) cho hạng của mọi dịch vụ trùng bản ghi đóng băng ở 48/48 ca OK (`/summary/self_check`). Bốn phép kiểm trên trường hợp tự dựng đạt (`/fixtures`).

**Quan sát** (`/summary/<dataset>/<nhánh>`; mẫu số là số ca root được xếp ở bản gốc):

| | RE2-TT: gốc | tỷ lệ a/n | tỷ lệ, chỉ thao tác từ 20 span | số tuyệt đối a | Nezha-OB: gốc | tỷ lệ a/n | tỷ lệ, từ 20 span | số tuyệt đối a |
|---|---|---|---|---|---|---|---|---|
| Hit@1 | 21/26 | 13 | 14 | 14 | 2/21 | 6 | 7 | 2 |
| Hit@5 | 25/26 | 16 | 17 | 21 | 11/21 | 16 | 17 | 12 |
| Root tăng / không đổi / giảm hạng | | 4 / 11 / 11 | 4 / 11 / 11 | 0 / 16 / 10 | | 10 / 4 / 7 | 11 / 4 / 6 | 3 / 10 / 8 |
| Ca sai ở bản gốc thành hạng 1 | | 3/5 | 3/5 | 0/5 | | 6/19 | 6/19 | 0/19 |
| Ca đúng ở bản gốc mất hạng 1 | | 11/21 | 10/21 | 7/21 | | 2/2 | 1/2 | 0/2 |
| Cặp đứng trên root của bản gốc: còn / mất | | 4 / 11 | 4 / 11 | 14 / 1 | | 32 / 43 | 29 / 46 | 68 / 7 |
| Cặp mới xuất hiện | | 71 | 61 | 22 | | 12 | 11 | 13 |
| Ca có thực thể đứng đầu trùng bản gốc | | 10/26 | 11/26 | 17/26 | | 8/22 | 9/22 | 15/22 |

**Đối chiếu với dự đoán khai trước.**

- **Công thức điểm đúng là một bước làm đổi hạng.** Đổi riêng nó sang tỷ lệ làm mất 11/15 cặp đứng trên root ở RE2-TT và 43–46/75 cặp ở Nezha-OB; ba trong năm ca sai của RE2-TT và 6/19 ca sai của Nezha-OB thành hạng 1.
- **Thứ tự của bản gốc ở các cặp đứng trên root gần như là thứ tự theo số span mang cờ tuyệt đối:** xếp theo a giữ lại 14/15 và 68/75 cặp. Câu "điểm nghiêng về số tuyệt đối" ở mục 2.1 vì vậy được xác nhận bằng can thiệp, không còn chỉ là quan sát.
- **Nhưng tỷ lệ không phải cách chữa.** Ở RE2-TT, xếp theo tỷ lệ làm 10–11 trong 21 ca đang đúng mất hạng 1 và sinh 61–71 cặp mới; Hit@1 giảm từ 21 xuống 13–14. Ở Nezha-OB tỷ lệ có lợi (Hit@1 từ 2 lên 6–7, Hit@5 từ 11 lên 16–17). Dự đoán "không làm hỏng các ca đang đúng" **không đúng** ở RE2-TT.

**Kết luận ở mức tính toán.** Hạn chế của công thức điểm trong bản thư viện là nó trộn "tỷ lệ span của thao tác vượt nền" với "khối lượng span của thao tác" thành một số. Trong điều kiện root ít span (hai ca lỗi loss của RE2-TT, phần lớn ca Nezha-OB), khối lượng lấn át và root thua. Trong điều kiện có nhiều thao tác ít span với tỷ lệ cao do ngẫu nhiên (RE2-TT), bỏ khối lượng lại làm root thua theo cách khác. Cả hai cực đều kém ở một dataset; không cực nào được đề xuất làm phương pháp.

**Giới hạn.** Hai nhánh tỷ lệ được nghĩ ra sau khi xem bảng ở mục 2.1. Mốc 20 span do tôi đặt. 26 và 21 ca dev.

## 9. Phép kiểm ngoài gói thứ hai — bước xếp hạng của bài TraceRCA gốc, cài theo lời văn của bài trên dữ liệu của ta

Nguồn: `runs/tracerca-original-ranking-001/summary.json` và `cases.json` (script `scripts/tracerca_original_ranking_v1.py`, EC2). Thiết kế viết trước: `thiet-ke-phep-doi-011.md` mục 3. **Đây không phải mã của tác giả và không tái lập bài gốc**: chỉ có một đặc trưng (độ trễ lời gọi), nền chỉ 300 giây hoặc 41–97 giây, cài theo lời văn Mục III của bài.

**Ba nhánh.** `to_p`: độ trễ là thời lượng span phía gọi, ngưỡng 1 lần độ lệch chuẩn (mặc định của bài). `to_c`: như trên nhưng dùng span phía được gọi. `to_p3`: như `to_p` với ngưỡng 3 lần độ lệch chuẩn; nhánh này thêm trước khi chạy, lý do ghi trong thiết kế.

**Kiểm.** Không có bản đóng băng để so. Sáu phép kiểm trên trường hợp tự dựng đạt, gồm ví dụ Hình 2 của bài: dịch vụ A có điểm trong tập 3 (3 trace có lời gọi ra bất thường, 0 có lời gọi vào), dịch vụ B có điểm 0, A đứng đầu (`/fixtures`). Một trường hợp tự dựng cho thấy trước điều sẽ gặp: khi chỉ có một lời gọi A→B bất thường, A và B **hòa** nhau, vì hiệu số lấy trị tuyệt đối.

**Quan sát** (`/summary/<dataset>/<nhánh>`):

| | RE2-TT `to_p` | RE2-TT `to_p3` | Nezha-OB `to_p` | Nezha-OB `to_p3` |
|---|---|---|---|---|
| Ca xếp hạng được / ca "không có đặc trưng hữu ích" | 22 / 8 | 22 / 8 | 11 / 11 | 11 / 11 |
| Trong ca xếp được: root có điểm dương | 14 | 15 | 7 | 11 |
| Root hạng 1 (tính bi quan khi hòa) | 12 | 12 | 0 | 2 |
| Root trong 5 hạng đầu | 12 | 14 | 7 | 11 |
| Thực thể đứng đầu nhiều ca nhất | `ts-route-service` 8 | `ts-route-service` 11 | `frontend` 11/11 | `frontend` 9/11 |
| Cặp (root, dịch vụ gọi trực tiếp): root trên / hòa / root dưới | 40 / 22 / 6 | 41 / 21 / 6 | 3 / 4 / 7 | 8 / 1 / 5 |
| Riêng các cặp "chủ yếu là chờ root" của bản thư viện (mục 2.1): root trên / hòa / root dưới | 0 / 1 / 3 | 0 / 1 / 3 | 0 / 1 / 7 | 2 / 1 / 5 |
| Tỷ lệ lời gọi bị gắn cờ: trước mốc → sau mốc (trung vị theo ca) | 10,7% → 18,3% | 1,7% → 11,7% | 7,3% → 9,2% | 2,4% → 3,9% |
| So với bản thư viện trên cùng ca: root hạng 1 ở bản thư viện → ở nhánh này | 13 → 9 (18 ca) | 13 → 9 (18 ca) | 1 → 0 (10 ca) | 1 → 2 (10 ca) |

Nhánh `to_c` cho kết quả gần `to_p` (RE2-TT: 22 ca xếp được, root hạng 1 ở 12; Nezha-OB: 9 ca xếp được, root hạng 1 ở 1).

**Đối chiếu với dự đoán khai trước.**

- **Bước "hiệu số lời gọi bất thường vào và ra" không tách được root khỏi dịch vụ gọi đang chờ nó trên dev.** Ở các cặp mà bản thư viện xếp dịch vụ gọi trên root vì chờ, root đứng trên dịch vụ gọi đó ở 0/4 cặp của RE2-TT và 0/8 cặp của Nezha-OB theo mặc định của bài; với ngưỡng 3 lần độ lệch chuẩn là 0/4 và 2/8.
- **Lý do nằm ở chính công thức, đã thấy trước ở trường hợp tự dựng:** hiệu số lấy trị tuyệt đối nên không mang hướng. Dịch vụ ở đầu trên của chuỗi (chỉ có lời gọi ra bất thường) nhận điểm như dịch vụ ở đầu dưới (chỉ có lời gọi vào bất thường). Ở Nezha-OB, `frontend` là đầu vào của mọi yêu cầu và đứng đầu ở 11/11 ca xếp được; đây đúng là dự đoán ghi trong thiết kế trước khi chạy.
- **Bước chọn đặc trưng của bài loại 8/30 ca RE2-TT và 11/22 ca Nezha-OB** ngay từ đầu: độ lệch trung bình sau mốc không tăng quá 10%. Với một đặc trưng và nền ngắn, ngưỡng này không đạt ở nhiều ca.
- Dịch vụ giữa chuỗi thì bước này có tách: ở RE2-TT root đứng trên dịch vụ gọi trực tiếp nó ở 40/68 cặp.

**Kết luận ở mức tính toán, chỉ cho bản cài theo lời văn này.** Trong điều kiện root nằm ở cuối một chuỗi gọi và các dịch vụ phía trên chờ nó, bước xếp hạng theo hiệu số tuyệt đối của bài gốc không chứa thông tin "ai chờ ai", nên không ưu tiên được root so với đầu trên của chuỗi. Muốn dùng cạnh gọi để tách root, phép tính phải giữ **hướng** của cạnh (ví dụ: lời gọi đi vào bất thường mà lời gọi đi ra bình thường). Đó là một ứng viên cho P5–P6, **chưa được kiểm ở đây**; T-032 chỉ cho thấy phương án có sẵn trong tài liệu không đủ.

**Giới hạn, phải đọc kèm.** Không kết luận được về TraceRCA gốc đầy đủ: bài dùng nhiều đặc trưng (có mã trạng thái và metric tài nguyên), nền nhiều ngày, và mã của tác giả chưa được đối chiếu. Số Hit@1 ở bảng không dùng để xếp hạng phương pháp. Nhánh `to_p3` được thêm sau khi đã thấy kết quả ở mục 8.
