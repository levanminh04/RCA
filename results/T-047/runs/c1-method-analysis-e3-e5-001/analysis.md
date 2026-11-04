# Người làm: phân tích E3/E5 trên dev T-047

Không phải phản biện chính thức. Không đổi thiết kế, ngưỡng, ma trận hoặc lựa chọn. Hai hash K thật/C-e và LOG được kiểm trước nhãn trong `preflight.json`. Số dưới đây lấy từ `facts-all-pairs.json`; từng ca có snapshot/native pointer và hash. `index-and-common-upward-verified.json` đối chiếu đủ 52 ca của mỗi cặp với index cơ chế cuối, không chỉ dùng bản trích tạm.

## Phạm vi và phép phân xử

Đọc đủ 52 ca cho bốn cặp: E1+E2→+E3 (HẠI tại cấu hình thắng), E1+E2→+E5, E1→+E5, E2→+E5 (ba cặp đổi kết cục so T-045). Đọc ca tụt, lên và giữ đúng. Không lấy cặp R0→nhiều thành phần để gán tác động riêng; phần đó do root tổng hợp.

Ngoài native, tái dựng raw log→Drain→số đếm→D1/nhánh trực tiếp ở bốn ca, gồm ca hại, ca giúp và counterpart đúng. Dữ liệu raw được selector/adapter kiểm allowlist/hash. Không chạy lại toàn chuỗi M1. Giữ raw lượt đầu và lượt bổ sung trong `raw-e3/` và `raw-refine-002/`.

## E3 tại E1+E2

**FACT — kết cục và phạm vi.** 29 ca RR tụt, 5 lên, 18 giữ. UV-6: 18 ca đang đúng bị hỏng, 3 ca lỗi mã được sửa. ΔMRR RE2-TT = −10657/25200; Nezha-OB = −3/55. Kết cục vẫn HẠI như T-045. Lượt mới có thêm vế C-e: N1 trung bình 499/30→683/30, tăng 92/15 trên 30 cửa sổ hợp lệ. Hai lý do HẠI là UV-6 và mốc giả. Nguồn: `facts-all-pairs.json#/pairs/E1+E2|E1+E2+E3`; vế từng thế giới đầy đủ ở `pairs-preliminary.json`.

**FACT — thay đổi không nằm ở cổng hướng lên dùng chung.** Đối chiếu cả 52 ca cho thấy cùng mã đơn vị phân vị, n_N/n_A, h/l, r_len_N/r_len_A, p_len, F_raw_len, e_len đều khớp giữa hai nhánh. E3 mở thêm hướng xuống và thay đường log, nên không được quy mọi tác động cho Drain hoặc cho G3. Coverage giữ nguyên trong cặp 52/52. Nguồn: `index-and-common-upward-verified.json#/E3_common_upward` và từng file `pairs/E1+E2__E1+E2+E3/`.

**Chuỗi ở ca hại RE2-TT dev-b8bd0abf60.** Root theo nhãn chấm là ts-route-service. RR 1→1/8. Root vẫn tầng 1; max s = 0,986666… giữ nguyên và không mất F_I. Nhiều đối thủ có kênh log mới đạt s = 1. Phần max s trong khóa S1 đặt họ trước root; không phải root bị loại vì thiếu kênh.

- Raw ts-basic-service có 12.235 dòng N và 11.613 dòng A; A vẫn có dữ liệu. Một mẫu đã học, `log|ts-basic-service|mau:68`, có n_N = 25, n_A = 0. Tái tính φ_D1 ≈ 25. Native và API cùng đi nhánh STOPPED, F_raw_xuong = 1, s = 1; p_xuong = 2,9802322387695312e-8 được ghi từ nhị thức.
- `log|ts-order-other-service|mau_moi` có n_N = 0 do định nghĩa mẫu học trên N, n_A = 25. Replay matching xác nhận cả 25 dòng không khớp được phân lớp KHONG_LOI theo quy tắc từ khóa. NEW_OP mở F_raw_len = 1, s = 1.
- Đây là cơ chế tính toán đã lần được. KHONG_LOI là kết quả bộ phân lớp văn bản, không xác nhận các dòng hay hoạt động thực sự là lành. STOPPED của mẫu cũng không có nghĩa cả service ngừng ghi log. Riêng một số service khác thực sự không có dòng A; chưa phân xử đó là thiếu thu hay thay đổi vận hành. Không gộp chúng thành một nguyên nhân dữ liệu.

Nguồn chi tiết: `raw-refine-002/raw-e3/dev-b8bd0abf60.json#/units`, `#/entities`, và `pairs/E1+E2__E1+E2+E3/dev-b8bd0abf60.json#/current/rivals_newly_before_root`.

**Chuỗi hại và counterpart cùng điều kiện trên Nezha-OB.** dev-63c30faf34 có root recommendationservice, network_delay, RR 1→1/4. Khóa root giữ nguyên. Checkoutservice có 562 dòng N/1.092 dòng A; 32 dòng A không khớp, đều phân lớp KHONG_LOI theo severity. NEW_OP s = 1 đặt checkoutservice trước root có max s ≈ 0,9251. Một đường khác là mẫu productcatalogservice: n_N = 2.426, n_A = 2, φ_D1 ≈ 120,7441; D1 p_xuong ≈ 1,0303e-7 và s ≈ 0,99933. Vì vậy không chỉ nhánh mới/mất mẫu mới tạo đối thủ.

Counterpart đúng dev-607751ac0a được index chọn theo cùng chữ ký quan sát, dataset và loại lỗi; root là checkoutservice nên không là cặp can thiệp cùng root. Nó có 912 dòng N/886 dòng A, 24 dòng không khớp đều KHONG_LOI; NEW_OP làm max s của chính root tăng lên 1 và root vẫn đứng đầu. Do đó “có dòng không khớp” hoặc “severity info” riêng lẻ không giải thích chiều đổi hạng. Cần xét dòng ấy thuộc root hay đối thủ, các kênh khác và khóa cuối. Nguồn: hai file raw tương ứng trong `raw-refine-002/raw-e3/`; counterpart pointer trong file pair của dev-63c30faf34.

**Ca E3 giúp, để bác bỏ cách giải thích một chiều.** dev-3b92690644, checkoutservice/return, RR 1/2→1. Raw A có 734 dòng: 32 LOI và 702 KHONG_LOI; replay xác nhận ô mẫu mới 100 dòng gồm 32 LOI và 68 KHONG_LOI. Root đã có max s = 1 trước E3. Phần max m của khóa tăng 3,023958…→4,129780…, vượt frontend có max m = 3,692500…; số kênh và tổng s của root giữ nguyên. Ca này không chứng minh lợi ích do tách được dòng lỗi riêng: mẫu mới gộp cả hai lớp. Nguồn: raw file dev-3b92690644 và snapshot T047 của E1+E2/E1+E2+E3. Không có counterpart đúng cùng toàn bộ chữ ký cho ca này; giữ giới hạn matching, không gọi so sánh với ca khác là nhân quả.

**Nhánh trực tiếp có đúng đặc tả không?** T-046 SPEC mục B2 ghi rõ “e, λ, NEW_OP, STOPPED, count_min giữ nguyên”; WHY-67 chọn D1 theo B2. `src/m1/e4.py` mục `cham_dem` giữ NEW_OP/STOPPED và trả s = 1 trực tiếp sau điều kiện đếm/hướng, trước vòng p_D1. Ở hai nhánh này p nhị thức là số được báo, không phải điều kiện p < α mở cờ. Phi không được áp vào nhánh trực tiếp là hành vi đã khai, không tự là bug cài đặt. Các trường hợp đếm thường mới dùng p_D1 < α và chênh dương để mở cờ. Raw/API/native khớp ở cả 298 đơn vị liên quan của bốn ca; không sửa quy tắc sau khi thấy số.

**Phân loại giới hạn E3.** Trong các ca đã tái dựng, đường cài đặt/adapter khớp nguồn và API. Bằng chứng xác nhận nơi phát sinh thay đổi: matching hoặc số đếm theo mẫu → cờ/điểm → khóa → thứ hạng. Giả thuyết còn cần phân xử là quy tắc novelty/mất mẫu và điểm tối đa không phân biệt đủ biến động hoạt động với dấu hiệu cần ưu tiên cho RCA. Chưa xác nhận tất cả mẫu biến mất là lỗi matching, tất cả dòng info là nhiễu hoặc thiếu thu là nguyên nhân. Cần phân tích nghĩa của dòng không khớp/mẫu biến mất theo từng nhóm và đối chiếu điều kiện vận hành; không thể suy phần đó chỉ từ nhãn root, severity hoặc cờ. Kết luận hiệu quả trên dữ liệu độc lập vẫn chờ P7.

## E5: ba cặp đổi kết cục

| Cặp | T-045 → T-047 | RR tụt/lên/giữ | ΔMRR RE2-TT | ΔMRR Nezha-OB |
|---|---|---|---|---|
| E1+E2→+E5 | HẠI → TRÁI CHIỀU DATASET | 6/9/37 | −5651/55440 | +23/220 |
| E1→+E5 | HẠI → TRÁI CHIỀU DATASET | 6/9/37 | −53/720 | +133/1320 |
| E2→+E5 | GIÚP → TRÁI CHIỀU DATASET | 7/13/32 | −50623/1201200 | +59/440 |

Nguồn: `facts-all-pairs.json#/pairs` và `pairs-preliminary.json`. Các kết cục đổi như nhau ở ba thế giới. Luật C xét trái chiều dataset trước HẠI gộp/GIÚP. Vì vậy E1+E2→+E5 có ΔMRR gộp âm vẫn trả TRÁI CHIỀU DATASET; không phải chỉ đổi tên hoặc C-e cứu E5. Ở E2→+E5, RE2 từ −2207/277200 lên mức âm vượt −1/30 ở lượt mới, làm vế trái chiều kích hoạt dù gộp còn dương.

**FACT — tính toán trong cặp.** Cả ba cặp đều giữ raw channels, đơn vị phân vị/đếm và coverage 52/52. Tái chạy riêng API `e5.phan_loai` trên raw channel và đồ thị native, đúng `co_vong`, khớp F_I ở 156/156 ca. Đã kiểm đồ thị không có đầu mút ngoài U cho các replay này. Đây là bằng chứng cài đặt phân loại F_I khớp, không chứng minh “kế thừa” là quan hệ nhân quả thật. Nguồn: `e5-FI-api-replay.json`.

**Ví dụ hại tại cấu hình thắng.** dev-a5cabe5fa7, ts-travel-service/loss, RR 1→1/12. E5 giữ K_raw max s = 0,95 nhưng hạ F_I của latency-50/latency-90 theo các kênh giải thích qua nhóm vòng, gồm E2 ở ts-seat-service. K_I max s của root giảm 0,95→0,436666…; root vẫn tầng 1. Nhiều thực thể khác đứng trước. M5 vẫn false: cờ M5 chỉ xét đối thủ có đường tới root trong G_N, không bao mọi ca tụt hạng. Không gọi M5 sai hoặc không đổi nghĩa của nó để bao ca này.

dev-f36d0647d5, ts-order-service/loss, có đường thường khác: latency-90 bị giải thích bởi kênh E2 ở ts-station-service; K_I max s 0,916666…→0,151472…, RR 1→1/11, M5 false→true. Đó là hai đường tính toán cụ thể, không phải mọi ca E5 hại đều do cùng một nhóm vòng.

**Ví dụ giúp và bằng chứng phản bác.** dev-3b92690644, checkoutservice/return, E5 cho RR 1/2→1 và M5 true→false; khóa/kênh tự sinh của root giữ nguyên, các đối thủ được hạ. dev-5467884de4, recommendationservice/network_delay, mất ba kênh F_I của root nhưng vẫn RR 1/2→1: chỉ đếm root bị hạ F_I không phân xử được hại. Cần so cả các đối thủ và khóa cuối. Tại cặp winner, 17 ca có kênh root được tái phân loại, trong khi chỉ 6 ca tụt RR; M5 phát sinh ở 2 ca và mất ở 6 ca. Vì số M5 tổng giảm nên điều kiện riêng E5 không HẠI; không suy ra E5 không gây hại từng ca.

Nguồn từng ví dụ: `pairs/E1+E2__E1+E2+E5/<oid>.json#/current`; giải thích kênh/đường và các khóa được giữ tại đó. Các file tương tự của hai cặp còn lại giữ đủ ca lên/tụt/đúng và counterpart, gồm trường không có matching chính xác.

**Nguồn thay đổi giữa T-045 và T-047.** Đã xác nhận số RR từng ca và điểm dừng luật đổi. G3/D1/S1 đổi cùng gói làm nền tín hiệu và thứ tự khác; bảng 2×2 của root phân tách cổng/thang tại P. Không quy toàn bộ đổi kết cục E5 cho một cổng hoặc cho thang chỉ từ ba chênh tổng. E5 giả định các kênh đủ điều kiện ở quan hệ gọi có thể giải thích kênh lan; các ca mất tín hiệu root ở trên chỉ ra hệ quả cụ thể của giả định này. Chưa xác nhận nguyên nhân vật lý của mỗi cặp kênh giải thích là đúng hay sai; cần đối chiếu thời gian/quan sát tương ứng. Không có bằng chứng mới về lỗi cài đặt E5 hoặc phép kiểm M5 trong phạm vi replay.

**C-e/N1.** Tại winner, E5 làm N1 trung bình giảm 29/15 trên 30 cửa sổ hợp lệ; E1→+E5 cũng giảm 29/15; E2→+E5 giảm 8/3. Vế xét tăng N1 không kích hoạt, đúng giới hạn đã khai của E5. Không coi đây là bằng chứng an toàn. Tương tác E3+E5→E1+E3+E5 có N1 17,1→20,5, Δ = 17/5, 26 cửa sổ tăng/1 giảm/3 giữ; chỉ vế mốc giả gây HẠI. `ce-E1-E3-E5-interaction.json` giữ từng cửa sổ. Root nhận phân tích đường E1 đổi lớp và F_I trong tương tác này; không gán tác động đó riêng cho E3/E5.

## Phần đã phân xử và phần còn mở

- Đã xác định đường tính toán tại các ca E3 hại/giúp và E5 hại/giúp; đã đối chiếu tất cả ca của bốn cặp, kiểm raw/API trên ca trọng điểm và replay F_I cả ba cặp E5. Có căn cứ mô tả kết cục dev và các bước làm đổi thứ hạng, không chỉ bảng cờ.
- Không thấy bằng chứng cần sửa cài đặt, test, công thức hoặc SPEC trong phạm vi đã kiểm. Hành vi NEW_OP/STOPPED phù hợp B2; chưa có quyền đổi nó. Coverage giữ nguyên trong cặp không chứng minh collector không thiếu sự kiện; dữ kiện hiện tại không cho quy mọi ca vào dataset.
- OPEN: ý nghĩa vận hành của mẫu log có/mất; cơ chế vật lý khiến các kênh giải thích E5 cùng bật; tác động riêng của các thay đổi trong gói ở từng thế giới non-P; hiệu quả độc lập. Tầng/khóa/inherited_by non-P không được native lưu riêng, dù channels/F_I non-P đã giữ. Những giới hạn này ảnh hưởng khẳng định cơ chế chung/khả năng chuyển sang hệ mới, không thay luật chọn đã duyệt trên dev.
- Các ứng viên xử lý novelty/STOPPED, quan hệ kế thừa hoặc điểm s = 1 cần SPEC/WHY và thí nghiệm riêng nếu Minh muốn đổi. Không suy việc đọc thêm này thành quyết định thay thiết kế hoặc tự mở task.

File/lượt lỗi đã giữ: `preliminary-print-error.txt` ghi lỗi in Fraction ở lượt đầu; các tệp dữ kiện đã ghi trước lỗi vẫn hợp lệ. `facts-all-pairs.json` là trích FACT tự động; diễn giải của người làm nằm ở báo cáo này. Những khóa `UV6_hong/sua` do script đếm ở mọi cặp chỉ có nghĩa điều kiện UV-6 khi thành phần là E3; không áp chúng làm luật E5.
