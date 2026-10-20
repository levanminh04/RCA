SimpleRCA tạo ưu thế caller qua tổng số mẫu metric vượt ngưỡng, trong khi trace và log mỗi kênh chỉ góp tối đa một phiếu. Chuỗi scalar và thứ hạng đã lưu cho 52 ca đã khớp nguồn; 14 ca M5 được đọc riêng. Kết quả này giải thích bước tính tạo chênh điểm. Nó chưa xác nhận caller chờ root, chưa xác định nguyên nhân vật lý và chưa đủ để chọn cách sửa trọng số hoặc đồ thị.

**Phạm vi và nguồn**

Bản này phục vụ P4 của MRP và NV2/NV3 của DT18: lần từ đầu vào tới bước xử lý tạo thứ hạng, cùng ca đúng có điều kiện tương ứng. Đây là phần việc của người làm, không phải phản biện chính thức. Nguồn là reading-view.json trong cùng thư mục. Pin và kết quả kiểm hash nằm tại manual-review-001.json#/source_checks. View giữ scalar không làm tròn, dẫn full row-witness tại EC2. Full chain chỉ giữ trên EC2; không tải hoặc tính lại trên laptop. Receipt closed của research-simple-004 xác nhận saved reader PASS, 52 ca và 14 ca M5; không đồng nghĩa đọc tay toàn bộ arrays.

Đã đọc metadata của 25 yêu cầu đối chứng và 331 liên kết class khóa, không chọn lại theo điểm/hạng. Điểm endpoint của một ca được đọc một lần rồi dẫn lại ở các class dùng chung. Các đối chứng khác preferred metadata, gồm coverage hoặc cell; không gọi chúng là input giống nhau hoặc can thiệp giữ mọi yếu tố. Đã diễn giải chi tiết các cặp ghi bên dưới. Full row-witness và actual runtime condition của mọi liên kết chưa đọc xong; manual_complete vẫn false.

Nhãn root/fault/cell chỉ nối sau khi phương pháp đã lưu kết quả. Phần đọc này không gọi phương pháp, không mở raw dataset, test hoặc dữ liệu khóa. Khả năng đo chờ hiện có là trạng thái tạm: instrumentation chưa đọc nên không lấy wait_cause_established=0 làm kết luận khoa học cuối.

**Đường tính trên code đúng pin**

| Bước | Cách thực thi | Thông tin còn hoặc mất |
|---|---|---|
| Đầu vào | RE2 adapter cắt N=[t−300,t), A=[t,t+300); trace nhận serviceName/startTime/duration. Nezha giữ N/A từng cột có sẵn, nhóm duration theo service và cắt log A. | Native không nhận root, fault hoặc quan hệ caller. Parent/child/self-work/wait không truyền vào diagnose; chưa khẳng định raw nguồn không có chúng. |
| Metric | core.py:62–74 bỏ nonfinite, yêu cầu N≥2 và A có mẫu; dùng μN+3σN, đếm strict A>threshold; config events cộng mỗi mẫu vượt của từng cột. | Giữ số lần tăng vượt; không giữ độ lớn vượt trong điểm, không cho giảm thấp hơn nền một phiếu, không chuẩn hóa theo số cột/mẫu hoặc quan hệ phụ thuộc. |
| Trace | core.py:75–86 lấy p95 tuyến tính N/A, thêm 1 khi p95 A >3p95N. | Giữ một cờ tăng; mọi độ lớn đã vượt cùng một phiếu. Duration riêng không cho biết chờ đồng bộ hay own work. |
| Log | core.py:87–98 đếm dòng chứa ERROR/FAIL/EXCEPTION, không phân biệt hoa thường; count>0 thêm 1. | Sau bước phiếu, số lượng log và ngữ nghĩa ngoài keyword không ảnh hưởng điểm. |
| Điểm/rank | core.py:100–112 cộng metric+trace+log, giảm dần theo điểm; tên chỉ hiển thị trong hòa exact; all-zero abstain. | Tập hòa giữ nguyên; thứ tự chữ không chứng minh hơn/kém trong hòa. Điểm là heuristic candidate ranking, không là xác suất căn nguyên. |
| Entity | RE2 dùng tiền tố trước underscore đầu tiên rồi max khóa từng entity; Nezha identity. ban_ghi.py:19–38 giữ hòa exact. | Root/caller của 14 ca M5 mỗi endpoint có một native member; max mapping không tạo chênh của các cặp này. |

Con trỏ preparation_call_pointers của từng ca và hash code nằm trong JSON. Graph T-028 gắn vai trò caller cho phân tích sau kết quả; đó không phải graph đi vào phép chấm SimpleRCA.

**Toàn bộ 52 ca: scalar root và hạng**

M/T/L là metric events/trace vote/log vote đã lưu; không tính lại nghiên cứu trên laptop. Khoảng hạng giữ nhóm hòa native/entity. Bảng đọc root và điểm service, không tuyên bố đọc mọi mẫu của mọi kênh. Mỗi dòng dẫn reading-view.json#/cases/i; native source, hash, frozen record và pointer nằm trong dòng JSON tương ứng.

| View case | Dataset / ca | Root | M/T/L → điểm | Hạng root | M5 theo nguồn tại k |
|---|---|---|---|---|---|
| /cases/0 | RE2-TT / dev-03d4910932 | ts-route-service | 1454/1/0 → 1455 | 1 | — |
| /cases/1 | RE2-TT / dev-12a1a88069 | ts-order-service | 1374/0/0 → 1374 | 1 | — |
| /cases/2 | RE2-TT / dev-14372e1209 | ts-route-service | 1715/1/0 → 1716 | 1 | — |
| /cases/3 | RE2-TT / dev-16597725c1 | ts-auth-service | 1392/0/0 → 1392 | 1 | — |
| /cases/4 | RE2-TT / dev-16870e660c | ts-route-service | 1754/1/0 → 1755 | 1 | — |
| /cases/5 | RE2-TT / dev-1e6d61b5ec | ts-order-service | 1441/1/0 → 1442 | 1 | — |
| /cases/6 | RE2-TT / dev-20acb4402d | ts-order-service | 240/1/0 → 241 | 15 | 1,5 |
| /cases/7 | RE2-TT / dev-260d332c8d | ts-order-service | 595/1/0 → 596 | 1 | — |
| /cases/8 | RE2-TT / dev-3ae0a6c15a | ts-train-service | 1320/1/0 → 1321 | 1 | — |
| /cases/9 | RE2-TT / dev-3defe3d34b | ts-auth-service | 1440/0/0 → 1440 | 1 | — |
| /cases/10 | RE2-TT / dev-4e68956051 | ts-train-service | 1177/1/0 → 1178 | 1 | — |
| /cases/11 | RE2-TT / dev-4f8a844308 | ts-route-service | 1446/1/1 → 1448 | 1 | — |
| /cases/12 | RE2-TT / dev-57546fd87b | ts-auth-service | 509/0/0 → 509 | 1 | — |
| /cases/13 | RE2-TT / dev-59f696a169 | ts-auth-service | 1343/0/0 → 1343 | 1 | — |
| /cases/14 | RE2-TT / dev-746fd74313 | ts-auth-service | 870/1/0 → 871 | 1 | — |
| /cases/15 | RE2-TT / dev-7f1b6b071d | ts-travel-service | 885/1/1 → 887 | 3 | 1 |
| /cases/16 | RE2-TT / dev-8017c6dc70 | ts-order-service | 1670/1/0 → 1671 | 1 | — |
| /cases/17 | RE2-TT / dev-98bc73c499 | ts-train-service | 1290/1/0 → 1291 | 1 | — |
| /cases/18 | RE2-TT / dev-a505ab3f65 | ts-train-service | 1104/1/0 → 1105 | 2 | 1 |
| /cases/19 | RE2-TT / dev-a5cabe5fa7 | ts-travel-service | 884/1/0 → 885 | 1 | — |
| /cases/20 | RE2-TT / dev-a915aa2424 | ts-travel-service | 803/1/0 → 804 | 2 | 1 |
| /cases/21 | RE2-TT / dev-b8bd0abf60 | ts-route-service | 1503/1/0 → 1504 | 1 | — |
| /cases/22 | RE2-TT / dev-ba831dbeb8 | ts-train-service | 1307/1/1 → 1309 | 1 | — |
| /cases/23 | RE2-TT / dev-bcbd4f46ae | ts-route-service | 1441/1/0 → 1442 | 1 | — |
| /cases/24 | RE2-TT / dev-db293894ab | ts-travel-service | 1160/0/0 → 1160 | 1 | — |
| /cases/25 | RE2-TT / dev-de89e2f9e9 | ts-travel-service | 1428/0/0 → 1428 | 1 | — |
| /cases/26 | RE2-TT / dev-f36d0647d5 | ts-order-service | 664/1/0 → 665 | 1 | — |
| /cases/27 | RE2-TT / dev-f81f88234e | ts-auth-service | 696/0/0 → 696 | 1 | — |
| /cases/28 | RE2-TT / dev-f9a8e05ed7 | ts-travel-service | 1297/0/0 → 1297 | 1 | — |
| /cases/29 | RE2-TT / dev-fbc45b0c67 | ts-train-service | 838/1/0 → 839 | 3 | 1 |
| /cases/30 | Nezha-OB / dev-14701a3bbb | shippingservice | 27/1/0 → 28 | 1 | — |
| /cases/31 | Nezha-OB / dev-1ac905bc95 | frontend | 0/0/1 → 1 | 5–6 | — |
| /cases/32 | Nezha-OB / dev-27252dca60 | productcatalogservice | 9/0/1 → 10 | 1 | — |
| /cases/33 | Nezha-OB / dev-2bfc97b01e | checkoutservice | 16/0/0 → 16 | 1 | — |
| /cases/34 | Nezha-OB / dev-396c8dbf7d | emailservice | 31/1/0 → 32 | 2 | 1 |
| /cases/35 | Nezha-OB / dev-3b92690644 | checkoutservice | 17/0/1 → 18 | 2 | 1 |
| /cases/36 | Nezha-OB / dev-3e27669440 | adservice | 32/1/0 → 33 | 1 | — |
| /cases/37 | Nezha-OB / dev-515c5f2190 | recommendationservice | 2/1/0 → 3 | 2 | — |
| /cases/38 | Nezha-OB / dev-5467884de4 | recommendationservice | 3/0/0 → 3 | 5 | 1 |
| /cases/39 | Nezha-OB / dev-55f99f3e0a | checkoutservice | 10/0/1 → 11 | 2 | 1 |
| /cases/40 | Nezha-OB / dev-5ada15752d | frontend | 0/0/1 → 1 | 6 | — |
| /cases/41 | Nezha-OB / dev-607751ac0a | checkoutservice | 0/0/0 → 0 | 9–10 | 1,5 |
| /cases/42 | Nezha-OB / dev-63c30faf34 | recommendationservice | 0/0/0 → 0 | 8–10 | 1,5 |
| /cases/43 | Nezha-OB / dev-6c9afc9822 | emailservice | 5/0/0 → 5 | 4 | 1 |
| /cases/44 | Nezha-OB / dev-70629373f9 | paymentservice | 38/0/0 → 38 | 1 | — |
| /cases/45 | Nezha-OB / dev-7b7c973198 | emailservice | 6/0/0 → 6 | 3 | — |
| /cases/46 | Nezha-OB / dev-7d3c2fe6d1 | shippingservice | 34/1/0 → 35 | 1 | — |
| /cases/47 | Nezha-OB / dev-8ecd9880ed | checkoutservice | 3/0/1 → 4 | 4–5 | — |
| /cases/48 | Nezha-OB / dev-95e164235f | paymentservice | 34/0/0 → 34 | 1 | — |
| /cases/49 | Nezha-OB / dev-9b9397a4dc | recommendationservice | 6/0/0 → 6 | 2–3 | — |
| /cases/50 | Nezha-OB / dev-9fd793feb7 | shippingservice | 16/1/0 → 17 | 2 | 1 |
| /cases/51 | Nezha-OB / dev-b0f8b2e3ac | checkoutservice | 18/0/1 → 19 | 3 | 1 |

**14 ca M5: từng cặp caller/root**

Bảng giữ các caller T-028 xác nhận đứng trước root, kể cả caller gián tiếp. JSON giữ cả caller có đường tới root nhưng đứng dưới. M5 là cờ quan sát khóa, không tự là nguyên nhân. Điểm, hạng và quan hệ nguồn có con trỏ trong /M5_caller_root; margin chuẩn hóa giữ giá trị nguồn, không dùng làm ngưỡng chọn ca.

| Ca / case pointer | Caller | M/T/L → điểm caller | M/T/L → điểm root | Chênh điểm nguồn | Quan hệ |
|---|---|---|---|---|---|
| dev-20acb4402d /cases/6 | ts-inside-payment-service | 293/1/1 → 295 | 240/1/0 → 241 | 54.0 | trực tiếp |
| dev-7f1b6b071d /cases/15 | ts-admin-travel-service | 954/1/1 → 956 | 885/1/1 → 887 | 69.0 | trực tiếp |
| dev-7f1b6b071d /cases/15 | ts-seat-service | 917/1/1 → 919 | 885/1/1 → 887 | 32.0 | trực tiếp |
| dev-a505ab3f65 /cases/18 | ts-travel 2-service | 1128/1/0 → 1129 | 1104/1/0 → 1105 | 24.0 | trực tiếp |
| dev-a915aa2424 /cases/20 | ts-admin-travel-service | 813/1/0 → 814 | 803/1/0 → 804 | 10.0 | trực tiếp |
| dev-fbc45b0c67 /cases/29 | ts-admin-travel-service | 896/1/0 → 897 | 838/1/0 → 839 | 58.0 | đường dài 2 |
| dev-fbc45b0c67 /cases/29 | ts-travel 2-service | 1012/1/0 → 1013 | 838/1/0 → 839 | 174.0 | trực tiếp |
| dev-396c8dbf7d /cases/34 | checkoutservice | 37/1/0 → 38 | 31/1/0 → 32 | 6.0 | trực tiếp |
| dev-3b92690644 /cases/35 | frontend | 31/0/1 → 32 | 17/0/1 → 18 | 14.0 | trực tiếp |
| dev-5467884de4 /cases/38 | frontend | 28/1/0 → 29 | 3/0/0 → 3 | 26.0 | trực tiếp |
| dev-55f99f3e0a /cases/39 | frontend | 17/0/1 → 18 | 10/0/1 → 11 | 7.0 | trực tiếp |
| dev-607751ac0a /cases/41 | frontend | 4/0/0 → 4 | 0/0/0 → 0 | 4.0 | trực tiếp |
| dev-63c30faf34 /cases/42 | frontend | 26/1/0 → 27 | 0/0/0 → 0 | 27.0 | trực tiếp |
| dev-6c9afc9822 /cases/43 | checkoutservice | 10/1/0 → 11 | 5/0/0 → 5 | 6.0 | trực tiếp |
| dev-9fd793feb7 /cases/50 | checkoutservice | 19/0/0 → 19 | 16/1/0 → 17 | 2.0 | trực tiếp |
| dev-b0f8b2e3ac /cases/51 | frontend | 21/0/1 → 22 | 18/0/1 → 19 | 3.0 | trực tiếp |

**RE2-TT / dev-20acb4402d — reading-view.json#/cases/6**

Inside-payment 293/1/1=295 vượt order 240/1/0=241. Caller mem count 195, root 17; latency-50/90 caller 27/71 lại thấp hơn root 30/180. Tổng đa cột tạo chênh; không phải caller luôn nhiều latency. Root/caller mỗi endpoint một native member, không bị lọc. Own channel rule-cross chưa xác nhận own physical work.

Đối chứng khóa: Cùng cell order|loss, dev-260d332c8d root 595/1/0=596, inside-payment330/1/1=332. Caller trace/log vẫn báo nhưng root thắng; preferred metadata khác 26 trường. View /locked_controls/0/control_classes/0; catalog /counterpart_pairs/13. Không xem số trường khác nhau như khoảng cách để chọn lớp.

Đối chứng khóa: Cùng class dev-260d332c8d ở k5; không đếm thêm ca. View /locked_controls/5/control_classes/0; catalog /counterpart_pairs/18. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**RE2-TT / dev-7f1b6b071d — reading-view.json#/cases/15**

Admin-travel 954/1/1=956 và seat 917/1/1=919 vượt travel 885/1/1=887; food/preserve-other/preserve/travel 2 ở dưới root. Trace/log đồng phiếu nên metric event sum quyết định. Seat error unavailable nhưng caller vẫn thắng; không quy mọi sai cho thiếu kênh. Ngưỡng gần hằng ở N giữ số native exact, không thêm epsilon.

Đối chứng khóa: Cùng cell travel|loss, dev-a5cabe5fa7 root 884/1/0=885, admin 821/1/0=822, seat 711/1/0=712. Root error unavailable vẫn thắng; preferred metadata khác 73 trường. View /locked_controls/1/control_classes/0; catalog /counterpart_pairs/14. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**RE2-TT / dev-a505ab3f65 — reading-view.json#/cases/18**

Travel2 1128/1/0=1129 vượt train 1104/1/0=1105. Metric root latency-50/90 281/283, mem 256/socket 284; caller 289/289, mem 270/socket 280. N/A endpoint đều300 finite; lợi thế đa cột, không do root thiếu tất cả metric. Caller khác ở dưới root.

Đối chứng khóa: Cùng cell train|delay, dev-4e68956051 root 1177/1/0=1178, travel 2 1027/1/0=1028, admin 761/1/0=762. Preferred metadata khác 141 trường; cùng rule không phải cùng input. View /locked_controls/2/control_classes/0; catalog /counterpart_pairs/15. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**RE2-TT / dev-a915aa2424 — reading-view.json#/cases/20**

Admin 813/1/0=814 vượt travel 803/1/0=804. Caller mem 296/root 229, nhưng latency-50/90 caller 281/236 thấp hơn root 300/266. Tổng events đa cột tạo ưu thế, không riêng latency. Các caller khác dưới root; nguyên nhân nền/tải/chờ chưa biết.

Đối chứng khóa: Cùng cell travel|loss, dev-a5cabe5fa7 root 885 vượt admin 822; preferred metadata khác 113 trường. View /locked_controls/3/control_classes/0; catalog /counterpart_pairs/16. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**RE2-TT / dev-fbc45b0c67 — reading-view.json#/cases/29**

Travel2 1012/1/0=1013 và admin 896/1/0=897 vượt train 838/1/0=839. Travel2 trực tiếp, admin đường dài 2. Root mem 0/caller travel 2 mem 166/adminmem 263; trace 1 / log 0 ở root, travel 2 và admin. Seat825/1/0 dưới root. Root CPU/disk thiếu 2 mẫu A không tự chứng minh nguyên nhân sai.

Đối chứng khóa: Cùng cell train|delay, dev-4e68956051 root 1178 vượt travel 2 1028/admin 762; preferred metadata khác 68 trường. View /locked_controls/4/control_classes/0; catalog /counterpart_pairs/17. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**Nezha-OB / dev-396c8dbf7d — reading-view.json#/cases/34**

Checkout 37/1/0=38 vượt email 31/1/0=32; frontend 11 dưới root. Root có CPU/mem events; caller nhiều client/server latency events hơn. Trace p95 A  root 999680.9/caller 1066920.75 đều1. Không root absent hoặc trace unavailable. Own channel alert không xác nhận own physical work.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/13/control_classes/0, catalog /counterpart_pairs/134. Cùng cell: không; preferred metadata khác 17 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Nezha-OB / dev-3b92690644 — reading-view.json#/cases/35**

Frontend 31/0/1=32 vượt checkout 17/0/1=18. Log64/32 đều thành 1; trace 0 cả hai. Metric cộng từng cột tạo chênh. Scalar tương đương FrontLatency/PodServerLatency chưa xác nhận raw arrays trùng, chưa gọi duplication.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/14/control_classes/0, catalog /counterpart_pairs/135. Cùng cell: không; preferred metadata khác 23 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Nezha-OB / dev-5467884de4 — reading-view.json#/cases/38**

Frontend 28/1/0=29 vượt recommendation 3/0/0=3, root hạng 5. Root chỉ client P99 count 1 / server P99 count 2; trace A 31159.35 không vượt threshold 120242.25. Caller có nhiều event latency và trace 1. Root đúng k5 không có nghĩa đúng k1 hay triệt tiêu lợi thế caller.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/15/control_classes/0, catalog /counterpart_pairs/136. Cùng cell: không; preferred metadata khác 17 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Nezha-OB / dev-55f99f3e0a — reading-view.json#/cases/39**

Frontend 17/0/1=18 vượt checkout 10/0/1=11. Log82/41 đều phiếu 1, trace 0 cả hai; metric sum quyết định. Threshold CPU/mem root vượt maxA theo scalar, chưa chứng minh nền bị nhiễm hay fault absent.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/16/control_classes/0, catalog /counterpart_pairs/137. Cùng cell: không; preferred metadata khác 35 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Nezha-OB / dev-607751ac0a — reading-view.json#/cases/41**

Frontend 4/0/0=4 vượt checkout 0/0/0=0, root hạng 9–10. Root metric/trace/log available nhưng không vượt; caller chỉ PodClientLatencyP99count 1/Sysread1/Syswrite2. Không cần caller latency tăng ở mọi cột. Root zero do gate, nguyên nhân phân bố N/A còn OPEN.

Đối chứng khóa: Cùng cell checkout|network_delay, dev-2bfc97b01e root 16/0/0, frontend 1/0/0. Root CPU2+2/mem 5+5/netreceive2, latency0; preferred metadata khác 10 trường. View /locked_controls/17/control_classes/0; catalog /counterpart_pairs/138. Không xem số trường khác nhau như khoảng cách để chọn lớp.

Đối chứng khóa: Cùng class checkout|network_delay ở k5; không tạo ca mới. View /locked_controls/23/control_classes/0; catalog /counterpart_pairs/144. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**Nezha-OB / dev-63c30faf34 — reading-view.json#/cases/42**

Frontend 26/1/0=27 vượt recommendation 0/0/0=0, root hạng 8–10. Root metric status ok count 0, trace A 7769<threshold 105232. Zero do native gate không phải unavailable. Instrumentation chưa đọc: không gọi khả năng đo chờ đã final hoặc fault absent.

Đối chứng khóa: Cùng cell recommendation|network_delay ở k5, dev-5467884de4 root 3 hạng 5 vẫn dưới frontend 29; không đúng k1 và không đảo caller advantage. Preferred metadata khác 10 trường. View /locked_controls/24/control_classes/0; catalog /counterpart_pairs/145. Không xem số trường khác nhau như khoảng cách để chọn lớp.

**Nezha-OB / dev-6c9afc9822 — reading-view.json#/cases/43**

Checkout 10/1/0=11 vượt email 5/0/0=5; frontend 0 dưới root. Caller metric chỉ hai memory count 5 mỗi cột, các latencycount 0. TraceA927688.7>threshold 583481.4 cho 1. Bác bỏ gán mọi M5 cho metric latency; chưa biết memory tăng vì own work/tải/chờ.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/19/control_classes/0, catalog /counterpart_pairs/140. Cùng cell: không; preferred metadata khác 17 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Nezha-OB / dev-9fd793feb7 — reading-view.json#/cases/50**

Checkout 19/0/0=19 vượt shipping 16/1/0=17. Root trace  p95 A 577830.45>threshold 1487.55 vẫn chỉ1; caller trace 0 nhưng metric19 thắng. Mất độ lớn vượt khỏi rank là FACT từ code; chưa thử đổi weighting, không chứng minh cách mới tốt hơn.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/20/control_classes/0, catalog /counterpart_pairs/141. Cùng cell: không; preferred metadata khác 17 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Nezha-OB / dev-b0f8b2e3ac — reading-view.json#/cases/51**

Frontend 21/0/1=22 vượt checkout 18/0/1=19. Currency22 hòa frontend hạng 1–2; caller/root strict. Log96/48 cùng1; metric frontend nhiều cột latency cộng. Không dùng alphabet tie để giải thích caller/root; raw duplication chưa kiểm.

Class đầu khóa: Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single tại view /locked_controls/21/control_classes/0, catalog /counterpart_pairs/142. Cùng cell: không; preferred metadata khác 35 trường. Điểm endpoint đọc lại từ /cases/30. Đây là đối chứng mô tả cùng giao thức, chưa phải cùng input hoặc cùng runtime đầy đủ. Không dùng class khác cell để quy cơ chế vật lý của ca này.

**Danh mục đối chứng khóa: giữ mọi liên kết**

Bảng giữ đủ 25 yêu cầu. manual-review-001.json#/locked_controls giữ đủ 331 class với source, mandatory conditions, differences, endpoint và trạng thái đọc. Class đúng tại k=5 có thể vẫn sai tại k=1. Khác cell được ghi rõ; không dùng nó thay chứng cứ cùng loại lỗi. Phần full witness/runtime thiếu giữ OPEN, không loại nhóm khỏi nghiên cứu.

| View request | Ca cần đối chứng | k | Catalog pointer | Số class | Class đầu khóa / cùng cell |
|---|---|---|---|---|---|
| /locked_controls/0 | RE2-TT\|simplerca\|dev-20acb4402d\|seed=single | 1 | /counterpart_pairs/13 | 25 | RE2-TT\|simplerca\|dev-260d332c8d\|seed=single / có |
| /locked_controls/1 | RE2-TT\|simplerca\|dev-7f1b6b071d\|seed=single | 1 | /counterpart_pairs/14 | 25 | RE2-TT\|simplerca\|dev-a5cabe5fa7\|seed=single / có |
| /locked_controls/2 | RE2-TT\|simplerca\|dev-a505ab3f65\|seed=single | 1 | /counterpart_pairs/15 | 25 | RE2-TT\|simplerca\|dev-4e68956051\|seed=single / có |
| /locked_controls/3 | RE2-TT\|simplerca\|dev-a915aa2424\|seed=single | 1 | /counterpart_pairs/16 | 25 | RE2-TT\|simplerca\|dev-a5cabe5fa7\|seed=single / có |
| /locked_controls/4 | RE2-TT\|simplerca\|dev-fbc45b0c67\|seed=single | 1 | /counterpart_pairs/17 | 25 | RE2-TT\|simplerca\|dev-4e68956051\|seed=single / có |
| /locked_controls/5 | RE2-TT\|simplerca\|dev-20acb4402d\|seed=single | 5 | /counterpart_pairs/18 | 29 | RE2-TT\|simplerca\|dev-260d332c8d\|seed=single / có |
| /locked_controls/6 | Nezha-OB\|simplerca\|dev-1ac905bc95\|seed=single | 1 | /counterpart_pairs/127 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/7 | Nezha-OB\|simplerca\|dev-515c5f2190\|seed=single | 1 | /counterpart_pairs/128 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/8 | Nezha-OB\|simplerca\|dev-5ada15752d\|seed=single | 1 | /counterpart_pairs/129 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/9 | Nezha-OB\|simplerca\|dev-7b7c973198\|seed=single | 1 | /counterpart_pairs/130 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/10 | Nezha-OB\|simplerca\|dev-8ecd9880ed\|seed=single | 1 | /counterpart_pairs/131 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/11 | Nezha-OB\|simplerca\|dev-9b9397a4dc\|seed=single | 1 | /counterpart_pairs/132 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/12 | Nezha-OB\|simplerca\|dev-1ac905bc95\|seed=single | 5 | /counterpart_pairs/133 | 18 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/13 | Nezha-OB\|simplerca\|dev-396c8dbf7d\|seed=single | 1 | /counterpart_pairs/134 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/14 | Nezha-OB\|simplerca\|dev-3b92690644\|seed=single | 1 | /counterpart_pairs/135 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/15 | Nezha-OB\|simplerca\|dev-5467884de4\|seed=single | 1 | /counterpart_pairs/136 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/16 | Nezha-OB\|simplerca\|dev-55f99f3e0a\|seed=single | 1 | /counterpart_pairs/137 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/17 | Nezha-OB\|simplerca\|dev-607751ac0a\|seed=single | 1 | /counterpart_pairs/138 | 7 | Nezha-OB\|simplerca\|dev-2bfc97b01e\|seed=single / có |
| /locked_controls/18 | Nezha-OB\|simplerca\|dev-63c30faf34\|seed=single | 1 | /counterpart_pairs/139 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/19 | Nezha-OB\|simplerca\|dev-6c9afc9822\|seed=single | 1 | /counterpart_pairs/140 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/20 | Nezha-OB\|simplerca\|dev-9fd793feb7\|seed=single | 1 | /counterpart_pairs/141 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/21 | Nezha-OB\|simplerca\|dev-b0f8b2e3ac\|seed=single | 1 | /counterpart_pairs/142 | 7 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/22 | Nezha-OB\|simplerca\|dev-5ada15752d\|seed=single | 5 | /counterpart_pairs/143 | 18 | Nezha-OB\|simplerca\|dev-14701a3bbb\|seed=single / không |
| /locked_controls/23 | Nezha-OB\|simplerca\|dev-607751ac0a\|seed=single | 5 | /counterpart_pairs/144 | 18 | Nezha-OB\|simplerca\|dev-2bfc97b01e\|seed=single / có |
| /locked_controls/24 | Nezha-OB\|simplerca\|dev-63c30faf34\|seed=single | 5 | /counterpart_pairs/145 | 18 | Nezha-OB\|simplerca\|dev-5467884de4\|seed=single / có |

**Cơ chế tính toán và giới hạn**

Trong điều kiện caller có nhiều mẫu ở nhiều cột vượt ngưỡng riêng hơn root, bước cộng events tạo điểm metric cao hơn; tổng score và sort giữ ưu thế đó. Cả 14 ca M5 có chuỗi scalar đã lưu từ threshold/count tới thành phần và rank. Cùng cell order|loss, travel|loss, train|delay và checkout|network_delay có ca root thắng qua cùng quy tắc. Vì vậy không có prior vô điều kiện ưu tiên caller. Đối chứng khác coverage và giá trị; chưa quy một đặc tính dữ liệu cụ thể là căn nguyên của mọi ca sai.

Trong điều kiện trace hoặc log đã vượt, bước chuyển sang 0/1 làm mất độ lớn trace vượt và tần suất log khỏi khóa xếp hạng. dev-9fd793feb7 có root trace vượt mạnh nhưng chỉ góp 1; caller không có trace vote nhưng metric19 đứng trên root 16+1. dev-3b92690644, dev-55f99f3e0a và dev-b0f8b2e3ac có log caller/root khác count nhưng cùng1. Đối chứng dev-260d332c8d vẫn có caller trace/log alert trong khi root thắng. Chưa thử đổi weighting; không gọi frequency/severity là căn nguyên đáng tin hơn.

Đối chứng khác cell dev-27252dca60 (/cases/32) có root productcatalog log keyword 768 và frontend 1512, mỗi bên cùng log vote 1; root metric9+log 1 thắng frontend log 1. Nguồn là /cases/32/root_score_chain và /cases/32/logs; ca này cho thấy nhiều keyword không luôn đồng nghĩa rank cao. Nó không phân xử cùng fault cho các ca checkout exception/return.

Trong điều kiện root có mẫu finite nhưng không vượt ngưỡng, bước gate trả 0. dev-607751ac0a và dev-63c30faf34 giữ root trong tập ứng viên, không bỏ root hoặc thiếu tất cả kênh. Cùng cell dev-2bfc97b01e có root thắng bằng CPU/mem/network events dù trace/log 0. Vì sao nền hoặc dữ liệu A dẫn tới zero chưa biết; scalar không chứng minh nền bị nhiễm, fault absent hay collector sai.

Adapter không truyền parent/child hoặc phần chờ/self-work vào diagnose. Đây là thiếu thông tin ở phép tính hiện hành. Instrumentation nguồn chưa đọc nên chưa kết luận trace thô thiếu khả năng phân biệt chờ. Rule-cross tại kênh caller chỉ xác nhận native thấy tăng tại kênh đó, không xác nhận own physical work.

Một số cặp FrontLatency và PodServerLatency của frontend có scalar mean/std/threshold/count/max giống nhau trong các ca đã đọc. Native cộng từng cột; array chưa so nên chỉ ghi scalar tương đương và khả năng lặp tín hiệu OPEN. Không dùng ứng viên này làm nguyên nhân đã xác nhận hoặc tự sửa cách chấm.

**Phần còn thiếu và bước cần bằng chứng**

Câu tính toán đã có bằng chứng về các phép nén/cộng và chênh điểm quan sát. Câu vật lý chưa phân xử. Đọc 52 scalar, 14 ca và metadata của 331 links chưa đóng toàn bộ SPEC. Còn full eligible row-witness và runtime path của các lớp đối chứng khóa, kiểm điều kiện tương ứng và nhánh unavailable; instrumentation/timing, nguồn nền và các cột scalar tương đương vẫn OPEN. JSON#/open_items chỉ đúng phần thiếu và kết luận bị chặn.

Căn cứ hiện tại cho phép mô tả hạn chế của representation/scoring và đề xuất ứng viên nghiên cứu. Chưa chọn thiết kế, chưa chứng minh graph có ích hoặc collector sửa được dữ liệu chưa từng ghi. Không cộng cờ M5 hoặc giải thích chồng lấn thành tỷ lệ căn nguyên.

Đã tạo đúng hai file được giao. Kiểm nguồn hash theo manifest/plan, giữ catalog và tất cả class; không sửa code, SPEC, WHY, STATE, LOG hoặc master outputs. Root phải soát trước khi dùng trong ba master và ghi LOG theo vai trò người làm. Helper không SSH, không khởi job EC2/laptop, không gọi native, không commit/push.
