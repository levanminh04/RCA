Nguồn từng số và con trỏ JSON: [ban-do-han-che-phat-hien.md — bảng nguồn](runs/review4-repair-001/ban-do-han-che-phat-hien.md.bindings.json). Dấu nguồn ẩn trong bản Markdown để V8 kiểm từng lần xuất hiện.

# Bản đồ hạn chế phát hiện ở chế độ (b)

Báo động đầu thường nằm trước mốc tiêm theo nhãn proxy. Trên mẫu đã kiểm, tiền xử lý toàn chuỗi của BOCPD cho báo đầu muộn hơn hoặc bằng so với I1 cắt sau mốc; tổng số điểm đổi nền ít hơn nhưng có ca ngược chiều. B2 cho biết vị trí báo đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý, chưa giải thích sự tồn tại của báo động trước mốc. N-Sigma có nhiều báo động nền, nhưng các cờ chưa tách được nguyên nhân thống kê. B4 mô tả bước nhảy telemetry và cũng phổ biến ở điểm không báo; không dùng riêng cờ này làm lời giải thích. Bản đồ phân biệt bằng chứng can thiệp, liên hệ, đọc tay và phần chưa kiểm.

Phạm vi: <!--v8:0-->90<!--/v8--> cặp, mỗi bộ <!--v8:1-->30<!--/v8--> ca dev RE2-TT. Mốc chung, lưới và các ngưỡng theo [SPEC đã khóa](../../tasks/T-029-p4-han-che-phat-hien/SPEC.md). Root/loại lỗi/ô chỉ nối sau khi [đặc trưng được lưu và băm](runs/step5-001/features-frozen.json). I1/I2/I3 dùng nhãn thời gian cho phân tích; không đổi số P3, không là đầu vào triển khai detector.

## C1 — Thất bại ở đâu (liên hệ/mô tả)

S nghĩa là báo động đầu sau mốc; E-gần/E-xa tách theo cửa sổ RCA có chứa mốc. Miss là không có báo trong đoạn sau mốc, khác với báo động đầu sai. Độ trễ BOCPD là độ lệch vị trí điểm đổi hồi cứu. Độ trễ N-Sigma phải đặt cạnh r_obs trong Nv; báo dày từ trước mốc có thể tiếp tục qua mốc.

Các ca S của BOCPD có điều kiện theo tiền xử lý toàn chuỗi: cả <!--v8:6131-->3<!--/v8--> ca đều có báo động trước mốc trong I1. Bảng sau giữ từng ca; không đổi phân loại hay số T-025. I1 vẫn nhìn trước bên trong tiền tố, nên đây không là chất lượng online.

| Ca / ô | Báo đầu full | Báo đầu I1 | Điểm đổi Nv full | Điểm đổi Nv I1 |
|---|---|---|---|---|
| dev-3defe3d34b / ts-auth-service / cpu | <!--v8:6132-->748<!--/v8--> | <!--v8:6133-->246<!--/v8--> | <!--v8:6134-->0<!--/v8--> | <!--v8:6135-->12<!--/v8--> |
| dev-98bc73c499 / ts-train-service / cpu | <!--v8:6136-->761<!--/v8--> | <!--v8:6137-->238<!--/v8--> | <!--v8:6138-->0<!--/v8--> | <!--v8:6139-->11<!--/v8--> |
| dev-f36d0647d5 / ts-order-service / loss | <!--v8:6140-->752<!--/v8--> | <!--v8:6141-->214<!--/v8--> | <!--v8:6142-->0<!--/v8--> | <!--v8:6143-->16<!--/v8--> |

Nguồn: `runs/review4-repair-001/summary.json#/intervention/S`; số gốc `bocpd-can-thiep.json#/cases/<ca>/{full,I1,cp_counts_Nv}`.

Nguồn bảng: `theo-ca.json#/per_detector/<bộ>/cell/<ô>` và `runs/report-main-001/summary.json#/delay`.

| Bộ | S | E-gần | E-xa | Miss | Tổng | Độ trễ nhỏ nhất / trung vị / lớn nhất | Số độ trễ bằng không |
|---|---|---|---|---|---|---|---|
| BOCPD | <!--v8:2-->3<!--/v8--> | <!--v8:3-->9<!--/v8--> | <!--v8:4-->18<!--/v8--> | <!--v8:5-->0<!--/v8--> | <!--v8:6-->30<!--/v8--> | <!--v8:7-->2<!--/v8--> / <!--v8:8-->34<!--/v8--> / <!--v8:9-->317<!--/v8--> | <!--v8:10-->0<!--/v8--> |
| N-Sigma chính | <!--v8:11-->0<!--/v8--> | <!--v8:12-->1<!--/v8--> | <!--v8:13-->29<!--/v8--> | <!--v8:14-->0<!--/v8--> | <!--v8:15-->30<!--/v8--> | <!--v8:16-->0<!--/v8--> / <!--v8:17-->9<!--/v8--> / <!--v8:18-->54<!--/v8--> | <!--v8:19-->11<!--/v8--> |
| N-Sigma đối chứng | <!--v8:20-->0<!--/v8--> | <!--v8:21-->0<!--/v8--> | <!--v8:22-->30<!--/v8--> | <!--v8:23-->0<!--/v8--> | <!--v8:24-->30<!--/v8--> | <!--v8:25-->0<!--/v8--> / <!--v8:26-->0<!--/v8--> / <!--v8:27-->0<!--/v8--> | <!--v8:28-->30<!--/v8--> |

| Bộ / ô | S | E-gần | E-xa | Miss / tổng |
|---|---|---|---|---|
| BOCPD / ts-auth-service / cpu | <!--v8:29-->1<!--/v8--> | <!--v8:30-->0<!--/v8--> | <!--v8:31-->2<!--/v8--> | <!--v8:32-->0<!--/v8-->/<!--v8:33-->3<!--/v8--> |
| BOCPD / ts-auth-service / delay | <!--v8:34-->0<!--/v8--> | <!--v8:35-->0<!--/v8--> | <!--v8:36-->3<!--/v8--> | <!--v8:37-->0<!--/v8-->/<!--v8:38-->3<!--/v8--> |
| BOCPD / ts-order-service / disk | <!--v8:39-->0<!--/v8--> | <!--v8:40-->0<!--/v8--> | <!--v8:41-->3<!--/v8--> | <!--v8:42-->0<!--/v8-->/<!--v8:43-->3<!--/v8--> |
| BOCPD / ts-order-service / loss | <!--v8:44-->1<!--/v8--> | <!--v8:45-->0<!--/v8--> | <!--v8:46-->2<!--/v8--> | <!--v8:47-->0<!--/v8-->/<!--v8:48-->3<!--/v8--> |
| BOCPD / ts-route-service / mem | <!--v8:49-->0<!--/v8--> | <!--v8:50-->1<!--/v8--> | <!--v8:51-->2<!--/v8--> | <!--v8:52-->0<!--/v8-->/<!--v8:53-->3<!--/v8--> |
| BOCPD / ts-route-service / socket | <!--v8:54-->0<!--/v8--> | <!--v8:55-->2<!--/v8--> | <!--v8:56-->1<!--/v8--> | <!--v8:57-->0<!--/v8-->/<!--v8:58-->3<!--/v8--> |
| BOCPD / ts-train-service / cpu | <!--v8:59-->1<!--/v8--> | <!--v8:60-->2<!--/v8--> | <!--v8:61-->0<!--/v8--> | <!--v8:62-->0<!--/v8-->/<!--v8:63-->3<!--/v8--> |
| BOCPD / ts-train-service / delay | <!--v8:64-->0<!--/v8--> | <!--v8:65-->1<!--/v8--> | <!--v8:66-->2<!--/v8--> | <!--v8:67-->0<!--/v8-->/<!--v8:68-->3<!--/v8--> |
| BOCPD / ts-travel-service / disk | <!--v8:69-->0<!--/v8--> | <!--v8:70-->1<!--/v8--> | <!--v8:71-->2<!--/v8--> | <!--v8:72-->0<!--/v8-->/<!--v8:73-->3<!--/v8--> |
| BOCPD / ts-travel-service / loss | <!--v8:74-->0<!--/v8--> | <!--v8:75-->2<!--/v8--> | <!--v8:76-->1<!--/v8--> | <!--v8:77-->0<!--/v8-->/<!--v8:78-->3<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | <!--v8:79-->0<!--/v8--> | <!--v8:80-->0<!--/v8--> | <!--v8:81-->3<!--/v8--> | <!--v8:82-->0<!--/v8-->/<!--v8:83-->3<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | <!--v8:84-->0<!--/v8--> | <!--v8:85-->1<!--/v8--> | <!--v8:86-->2<!--/v8--> | <!--v8:87-->0<!--/v8-->/<!--v8:88-->3<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | <!--v8:89-->0<!--/v8--> | <!--v8:90-->0<!--/v8--> | <!--v8:91-->3<!--/v8--> | <!--v8:92-->0<!--/v8-->/<!--v8:93-->3<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | <!--v8:94-->0<!--/v8--> | <!--v8:95-->0<!--/v8--> | <!--v8:96-->3<!--/v8--> | <!--v8:97-->0<!--/v8-->/<!--v8:98-->3<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | <!--v8:99-->0<!--/v8--> | <!--v8:100-->0<!--/v8--> | <!--v8:101-->3<!--/v8--> | <!--v8:102-->0<!--/v8-->/<!--v8:103-->3<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | <!--v8:104-->0<!--/v8--> | <!--v8:105-->0<!--/v8--> | <!--v8:106-->3<!--/v8--> | <!--v8:107-->0<!--/v8-->/<!--v8:108-->3<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | <!--v8:109-->0<!--/v8--> | <!--v8:110-->0<!--/v8--> | <!--v8:111-->3<!--/v8--> | <!--v8:112-->0<!--/v8-->/<!--v8:113-->3<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | <!--v8:114-->0<!--/v8--> | <!--v8:115-->0<!--/v8--> | <!--v8:116-->3<!--/v8--> | <!--v8:117-->0<!--/v8-->/<!--v8:118-->3<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | <!--v8:119-->0<!--/v8--> | <!--v8:120-->0<!--/v8--> | <!--v8:121-->3<!--/v8--> | <!--v8:122-->0<!--/v8-->/<!--v8:123-->3<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | <!--v8:124-->0<!--/v8--> | <!--v8:125-->0<!--/v8--> | <!--v8:126-->3<!--/v8--> | <!--v8:127-->0<!--/v8-->/<!--v8:128-->3<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | <!--v8:129-->0<!--/v8--> | <!--v8:130-->0<!--/v8--> | <!--v8:131-->3<!--/v8--> | <!--v8:132-->0<!--/v8-->/<!--v8:133-->3<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | <!--v8:134-->0<!--/v8--> | <!--v8:135-->0<!--/v8--> | <!--v8:136-->3<!--/v8--> | <!--v8:137-->0<!--/v8-->/<!--v8:138-->3<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | <!--v8:139-->0<!--/v8--> | <!--v8:140-->0<!--/v8--> | <!--v8:141-->3<!--/v8--> | <!--v8:142-->0<!--/v8-->/<!--v8:143-->3<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | <!--v8:144-->0<!--/v8--> | <!--v8:145-->0<!--/v8--> | <!--v8:146-->3<!--/v8--> | <!--v8:147-->0<!--/v8-->/<!--v8:148-->3<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | <!--v8:149-->0<!--/v8--> | <!--v8:150-->0<!--/v8--> | <!--v8:151-->3<!--/v8--> | <!--v8:152-->0<!--/v8-->/<!--v8:153-->3<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | <!--v8:154-->0<!--/v8--> | <!--v8:155-->0<!--/v8--> | <!--v8:156-->3<!--/v8--> | <!--v8:157-->0<!--/v8-->/<!--v8:158-->3<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | <!--v8:159-->0<!--/v8--> | <!--v8:160-->0<!--/v8--> | <!--v8:161-->3<!--/v8--> | <!--v8:162-->0<!--/v8-->/<!--v8:163-->3<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | <!--v8:164-->0<!--/v8--> | <!--v8:165-->0<!--/v8--> | <!--v8:166-->3<!--/v8--> | <!--v8:167-->0<!--/v8-->/<!--v8:168-->3<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | <!--v8:169-->0<!--/v8--> | <!--v8:170-->0<!--/v8--> | <!--v8:171-->3<!--/v8--> | <!--v8:172-->0<!--/v8-->/<!--v8:173-->3<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | <!--v8:174-->0<!--/v8--> | <!--v8:175-->0<!--/v8--> | <!--v8:176-->3<!--/v8--> | <!--v8:177-->0<!--/v8-->/<!--v8:178-->3<!--/v8--> |

### Theo từng ca: giữ mọi cặp

Nguồn: `theo-ca.json#/rows/<dòng>`. Danh sách cờ là đa nhãn ở cấu hình chính, không là thứ tự nguyên nhân trội hoặc số ca đã giải thích. Với nhóm E, D0 là một phần của nhóm chưa giải thích; có cờ chưa đồng nghĩa đã giải thích sự tồn tại của báo động trước mốc. D0 ở S có thể do các cờ BOCPD không có miền hợp lệ, nên phải tách S/E và không gộp D0 ở S thành thất bại báo sớm.

| Ca | Bộ | Ô | Nhóm | t̂ | t̂⁺ | Độ trễ | Báo sai trong Nv | r_obs Nv | d | Cờ chính |
|---|---|---|---|---|---|---|---|---|---|---|
| dev-03d4910932 | BOCPD | ts-route-service / socket | E-gần | <!--v8:179-->684<!--/v8--> | <!--v8:180-->724<!--/v8--> | <!--v8:181-->4<!--/v8--> | <!--v8:182-->3<!--/v8--> | <!--v8:183-->N/A<!--/v8--> | <!--v8:184-->28<!--/v8--> | B2 |
| dev-03d4910932 | N-Sigma chính | ts-route-service / socket | E-xa | <!--v8:185-->125<!--/v8--> | <!--v8:186-->728<!--/v8--> | <!--v8:187-->8<!--/v8--> | <!--v8:188-->292<!--/v8--> | <!--v8:189-->0.470968<!--/v8--> | <!--v8:190-->34<!--/v8--> | N3 |
| dev-03d4910932 | N-Sigma đối chứng | ts-route-service / socket | E-xa | <!--v8:191-->100<!--/v8--> | <!--v8:192-->720<!--/v8--> | <!--v8:193-->0<!--/v8--> | <!--v8:194-->618<!--/v8--> | <!--v8:195-->0.996774<!--/v8--> | <!--v8:196-->361<!--/v8--> | N2 |
| dev-12a1a88069 | BOCPD | ts-order-service / disk | E-xa | <!--v8:197-->128<!--/v8--> | <!--v8:198-->782<!--/v8--> | <!--v8:199-->62<!--/v8--> | <!--v8:200-->4<!--/v8--> | <!--v8:201-->N/A<!--/v8--> | <!--v8:202-->33<!--/v8--> | B2+B4 |
| dev-12a1a88069 | N-Sigma chính | ts-order-service / disk | E-xa | <!--v8:203-->101<!--/v8--> | <!--v8:204-->768<!--/v8--> | <!--v8:205-->48<!--/v8--> | <!--v8:206-->182<!--/v8--> | <!--v8:207-->0.293548<!--/v8--> | <!--v8:208-->44<!--/v8--> | N1+N3 |
| dev-12a1a88069 | N-Sigma đối chứng | ts-order-service / disk | E-xa | <!--v8:209-->100<!--/v8--> | <!--v8:210-->720<!--/v8--> | <!--v8:211-->0<!--/v8--> | <!--v8:212-->603<!--/v8--> | <!--v8:213-->0.972581<!--/v8--> | <!--v8:214-->371<!--/v8--> | N2 |
| dev-14372e1209 | BOCPD | ts-route-service / mem | E-xa | <!--v8:215-->252<!--/v8--> | <!--v8:216-->818<!--/v8--> | <!--v8:217-->98<!--/v8--> | <!--v8:218-->3<!--/v8--> | <!--v8:219-->N/A<!--/v8--> | <!--v8:220-->29<!--/v8--> | D0 |
| dev-14372e1209 | N-Sigma chính | ts-route-service / mem | E-xa | <!--v8:221-->107<!--/v8--> | <!--v8:222-->774<!--/v8--> | <!--v8:223-->54<!--/v8--> | <!--v8:224-->29<!--/v8--> | <!--v8:225-->0.0467742<!--/v8--> | <!--v8:226-->34<!--/v8--> | N1+N3 |
| dev-14372e1209 | N-Sigma đối chứng | ts-route-service / mem | E-xa | <!--v8:227-->100<!--/v8--> | <!--v8:228-->720<!--/v8--> | <!--v8:229-->0<!--/v8--> | <!--v8:230-->574<!--/v8--> | <!--v8:231-->0.925806<!--/v8--> | <!--v8:232-->363<!--/v8--> | N1+N2 |
| dev-16597725c1 | BOCPD | ts-auth-service / cpu | E-xa | <!--v8:233-->239<!--/v8--> | <!--v8:234-->722<!--/v8--> | <!--v8:235-->2<!--/v8--> | <!--v8:236-->5<!--/v8--> | <!--v8:237-->N/A<!--/v8--> | <!--v8:238-->34<!--/v8--> | B2+B4 |
| dev-16597725c1 | N-Sigma chính | ts-auth-service / cpu | E-xa | <!--v8:239-->100<!--/v8--> | <!--v8:240-->720<!--/v8--> | <!--v8:241-->0<!--/v8--> | <!--v8:242-->289<!--/v8--> | <!--v8:243-->0.466129<!--/v8--> | <!--v8:244-->40<!--/v8--> | N3 |
| dev-16597725c1 | N-Sigma đối chứng | ts-auth-service / cpu | E-xa | <!--v8:245-->100<!--/v8--> | <!--v8:246-->720<!--/v8--> | <!--v8:247-->0<!--/v8--> | <!--v8:248-->616<!--/v8--> | <!--v8:249-->0.993548<!--/v8--> | <!--v8:250-->367<!--/v8--> | N2 |
| dev-16870e660c | BOCPD | ts-route-service / mem | E-gần | <!--v8:251-->614<!--/v8--> | <!--v8:252-->754<!--/v8--> | <!--v8:253-->34<!--/v8--> | <!--v8:254-->3<!--/v8--> | <!--v8:255-->N/A<!--/v8--> | <!--v8:256-->28<!--/v8--> | D0 |
| dev-16870e660c | N-Sigma chính | ts-route-service / mem | E-xa | <!--v8:257-->102<!--/v8--> | <!--v8:258-->720<!--/v8--> | <!--v8:259-->0<!--/v8--> | <!--v8:260-->182<!--/v8--> | <!--v8:261-->0.293548<!--/v8--> | <!--v8:262-->34<!--/v8--> | N3 |
| dev-16870e660c | N-Sigma đối chứng | ts-route-service / mem | E-xa | <!--v8:263-->100<!--/v8--> | <!--v8:264-->720<!--/v8--> | <!--v8:265-->0<!--/v8--> | <!--v8:266-->614<!--/v8--> | <!--v8:267-->0.990323<!--/v8--> | <!--v8:268-->361<!--/v8--> | N2 |
| dev-1e6d61b5ec | BOCPD | ts-order-service / disk | E-xa | <!--v8:269-->119<!--/v8--> | <!--v8:270-->734<!--/v8--> | <!--v8:271-->14<!--/v8--> | <!--v8:272-->12<!--/v8--> | <!--v8:273-->N/A<!--/v8--> | <!--v8:274-->23<!--/v8--> | B2+B4 |
| dev-1e6d61b5ec | N-Sigma chính | ts-order-service / disk | E-xa | <!--v8:275-->154<!--/v8--> | <!--v8:276-->759<!--/v8--> | <!--v8:277-->39<!--/v8--> | <!--v8:278-->151<!--/v8--> | <!--v8:279-->0.243548<!--/v8--> | <!--v8:280-->25<!--/v8--> | N3 |
| dev-1e6d61b5ec | N-Sigma đối chứng | ts-order-service / disk | E-xa | <!--v8:281-->100<!--/v8--> | <!--v8:282-->720<!--/v8--> | <!--v8:283-->0<!--/v8--> | <!--v8:284-->611<!--/v8--> | <!--v8:285-->0.985484<!--/v8--> | <!--v8:286-->340<!--/v8--> | N2 |
| dev-20acb4402d | BOCPD | ts-order-service / loss | E-xa | <!--v8:287-->280<!--/v8--> | <!--v8:288-->726<!--/v8--> | <!--v8:289-->6<!--/v8--> | <!--v8:290-->9<!--/v8--> | <!--v8:291-->N/A<!--/v8--> | <!--v8:292-->22<!--/v8--> | B2+B4 |
| dev-20acb4402d | N-Sigma chính | ts-order-service / loss | E-xa | <!--v8:293-->149<!--/v8--> | <!--v8:294-->720<!--/v8--> | <!--v8:295-->0<!--/v8--> | <!--v8:296-->259<!--/v8--> | <!--v8:297-->0.417742<!--/v8--> | <!--v8:298-->30<!--/v8--> | N3 |
| dev-20acb4402d | N-Sigma đối chứng | ts-order-service / loss | E-xa | <!--v8:299-->100<!--/v8--> | <!--v8:300-->720<!--/v8--> | <!--v8:301-->0<!--/v8--> | <!--v8:302-->619<!--/v8--> | <!--v8:303-->0.998387<!--/v8--> | <!--v8:304-->345<!--/v8--> | N2 |
| dev-260d332c8d | BOCPD | ts-order-service / loss | E-xa | <!--v8:305-->126<!--/v8--> | <!--v8:306-->916<!--/v8--> | <!--v8:307-->196<!--/v8--> | <!--v8:308-->8<!--/v8--> | <!--v8:309-->N/A<!--/v8--> | <!--v8:310-->22<!--/v8--> | B2+B4 |
| dev-260d332c8d | N-Sigma chính | ts-order-service / loss | E-xa | <!--v8:311-->104<!--/v8--> | <!--v8:312-->771<!--/v8--> | <!--v8:313-->51<!--/v8--> | <!--v8:314-->158<!--/v8--> | <!--v8:315-->0.254839<!--/v8--> | <!--v8:316-->30<!--/v8--> | N3 |
| dev-260d332c8d | N-Sigma đối chứng | ts-order-service / loss | E-xa | <!--v8:317-->100<!--/v8--> | <!--v8:318-->720<!--/v8--> | <!--v8:319-->0<!--/v8--> | <!--v8:320-->611<!--/v8--> | <!--v8:321-->0.985484<!--/v8--> | <!--v8:322-->345<!--/v8--> | N2 |
| dev-3ae0a6c15a | BOCPD | ts-train-service / cpu | E-gần | <!--v8:323-->649<!--/v8--> | <!--v8:324-->755<!--/v8--> | <!--v8:325-->35<!--/v8--> | <!--v8:326-->3<!--/v8--> | <!--v8:327-->N/A<!--/v8--> | <!--v8:328-->36<!--/v8--> | D0 |
| dev-3ae0a6c15a | N-Sigma chính | ts-train-service / cpu | E-xa | <!--v8:329-->100<!--/v8--> | <!--v8:330-->737<!--/v8--> | <!--v8:331-->17<!--/v8--> | <!--v8:332-->304<!--/v8--> | <!--v8:333-->0.490323<!--/v8--> | <!--v8:334-->43<!--/v8--> | N2 |
| dev-3ae0a6c15a | N-Sigma đối chứng | ts-train-service / cpu | E-xa | <!--v8:335-->100<!--/v8--> | <!--v8:336-->720<!--/v8--> | <!--v8:337-->0<!--/v8--> | <!--v8:338-->619<!--/v8--> | <!--v8:339-->0.998387<!--/v8--> | <!--v8:340-->370<!--/v8--> | N2 |
| dev-3defe3d34b | BOCPD | ts-auth-service / cpu | S | <!--v8:341-->748<!--/v8--> | <!--v8:342-->748<!--/v8--> | <!--v8:343-->28<!--/v8--> | <!--v8:344-->0<!--/v8--> | <!--v8:345-->N/A<!--/v8--> | <!--v8:346-->30<!--/v8--> | D0 |
| dev-3defe3d34b | N-Sigma chính | ts-auth-service / cpu | E-xa | <!--v8:347-->100<!--/v8--> | <!--v8:348-->741<!--/v8--> | <!--v8:349-->21<!--/v8--> | <!--v8:350-->232<!--/v8--> | <!--v8:351-->0.374194<!--/v8--> | <!--v8:352-->42<!--/v8--> | N3 |
| dev-3defe3d34b | N-Sigma đối chứng | ts-auth-service / cpu | E-xa | <!--v8:353-->100<!--/v8--> | <!--v8:354-->720<!--/v8--> | <!--v8:355-->0<!--/v8--> | <!--v8:356-->614<!--/v8--> | <!--v8:357-->0.990323<!--/v8--> | <!--v8:358-->369<!--/v8--> | N1+N2+N4 |
| dev-4e68956051 | BOCPD | ts-train-service / delay | E-gần | <!--v8:359-->675<!--/v8--> | <!--v8:360-->743<!--/v8--> | <!--v8:361-->23<!--/v8--> | <!--v8:362-->1<!--/v8--> | <!--v8:363-->N/A<!--/v8--> | <!--v8:364-->28<!--/v8--> | B2+B4 |
| dev-4e68956051 | N-Sigma chính | ts-train-service / delay | E-xa | <!--v8:365-->100<!--/v8--> | <!--v8:366-->736<!--/v8--> | <!--v8:367-->16<!--/v8--> | <!--v8:368-->269<!--/v8--> | <!--v8:369-->0.433871<!--/v8--> | <!--v8:370-->31<!--/v8--> | N3 |
| dev-4e68956051 | N-Sigma đối chứng | ts-train-service / delay | E-xa | <!--v8:371-->100<!--/v8--> | <!--v8:372-->720<!--/v8--> | <!--v8:373-->0<!--/v8--> | <!--v8:374-->617<!--/v8--> | <!--v8:375-->0.995161<!--/v8--> | <!--v8:376-->358<!--/v8--> | N2 |
| dev-4f8a844308 | BOCPD | ts-route-service / mem | E-xa | <!--v8:377-->218<!--/v8--> | <!--v8:378-->733<!--/v8--> | <!--v8:379-->13<!--/v8--> | <!--v8:380-->2<!--/v8--> | <!--v8:381-->N/A<!--/v8--> | <!--v8:382-->39<!--/v8--> | B2+B4 |
| dev-4f8a844308 | N-Sigma chính | ts-route-service / mem | E-xa | <!--v8:383-->103<!--/v8--> | <!--v8:384-->722<!--/v8--> | <!--v8:385-->2<!--/v8--> | <!--v8:386-->189<!--/v8--> | <!--v8:387-->0.304839<!--/v8--> | <!--v8:388-->46<!--/v8--> | N3 |
| dev-4f8a844308 | N-Sigma đối chứng | ts-route-service / mem | E-xa | <!--v8:389-->100<!--/v8--> | <!--v8:390-->720<!--/v8--> | <!--v8:391-->0<!--/v8--> | <!--v8:392-->609<!--/v8--> | <!--v8:393-->0.982258<!--/v8--> | <!--v8:394-->373<!--/v8--> | N2 |
| dev-57546fd87b | BOCPD | ts-auth-service / delay | E-xa | <!--v8:395-->415<!--/v8--> | <!--v8:396-->743<!--/v8--> | <!--v8:397-->23<!--/v8--> | <!--v8:398-->4<!--/v8--> | <!--v8:399-->N/A<!--/v8--> | <!--v8:400-->28<!--/v8--> | B2 |
| dev-57546fd87b | N-Sigma chính | ts-auth-service / delay | E-xa | <!--v8:401-->100<!--/v8--> | <!--v8:402-->720<!--/v8--> | <!--v8:403-->0<!--/v8--> | <!--v8:404-->159<!--/v8--> | <!--v8:405-->0.256452<!--/v8--> | <!--v8:406-->31<!--/v8--> | N3 |
| dev-57546fd87b | N-Sigma đối chứng | ts-auth-service / delay | E-xa | <!--v8:407-->100<!--/v8--> | <!--v8:408-->720<!--/v8--> | <!--v8:409-->0<!--/v8--> | <!--v8:410-->607<!--/v8--> | <!--v8:411-->0.979032<!--/v8--> | <!--v8:412-->358<!--/v8--> | N2 |
| dev-59f696a169 | BOCPD | ts-auth-service / cpu | E-xa | <!--v8:413-->162<!--/v8--> | <!--v8:414-->763<!--/v8--> | <!--v8:415-->43<!--/v8--> | <!--v8:416-->18<!--/v8--> | <!--v8:417-->N/A<!--/v8--> | <!--v8:418-->27<!--/v8--> | B2+B4 |
| dev-59f696a169 | N-Sigma chính | ts-auth-service / cpu | E-xa | <!--v8:419-->100<!--/v8--> | <!--v8:420-->720<!--/v8--> | <!--v8:421-->0<!--/v8--> | <!--v8:422-->264<!--/v8--> | <!--v8:423-->0.425806<!--/v8--> | <!--v8:424-->40<!--/v8--> | N2 |
| dev-59f696a169 | N-Sigma đối chứng | ts-auth-service / cpu | E-xa | <!--v8:425-->100<!--/v8--> | <!--v8:426-->720<!--/v8--> | <!--v8:427-->0<!--/v8--> | <!--v8:428-->620<!--/v8--> | <!--v8:429-->1<!--/v8--> | <!--v8:430-->367<!--/v8--> | N2 |
| dev-746fd74313 | BOCPD | ts-auth-service / delay | E-xa | <!--v8:431-->102<!--/v8--> | <!--v8:432-->751<!--/v8--> | <!--v8:433-->31<!--/v8--> | <!--v8:434-->3<!--/v8--> | <!--v8:435-->N/A<!--/v8--> | <!--v8:436-->32<!--/v8--> | B4 |
| dev-746fd74313 | N-Sigma chính | ts-auth-service / delay | E-xa | <!--v8:437-->100<!--/v8--> | <!--v8:438-->720<!--/v8--> | <!--v8:439-->0<!--/v8--> | <!--v8:440-->197<!--/v8--> | <!--v8:441-->0.317742<!--/v8--> | <!--v8:442-->44<!--/v8--> | N2 |
| dev-746fd74313 | N-Sigma đối chứng | ts-auth-service / delay | E-xa | <!--v8:443-->100<!--/v8--> | <!--v8:444-->720<!--/v8--> | <!--v8:445-->0<!--/v8--> | <!--v8:446-->620<!--/v8--> | <!--v8:447-->1<!--/v8--> | <!--v8:448-->371<!--/v8--> | N2+N4 |
| dev-7f1b6b071d | BOCPD | ts-travel-service / loss | E-xa | <!--v8:449-->355<!--/v8--> | <!--v8:450-->746<!--/v8--> | <!--v8:451-->26<!--/v8--> | <!--v8:452-->7<!--/v8--> | <!--v8:453-->N/A<!--/v8--> | <!--v8:454-->33<!--/v8--> | D0 |
| dev-7f1b6b071d | N-Sigma chính | ts-travel-service / loss | E-xa | <!--v8:455-->106<!--/v8--> | <!--v8:456-->731<!--/v8--> | <!--v8:457-->11<!--/v8--> | <!--v8:458-->245<!--/v8--> | <!--v8:459-->0.395161<!--/v8--> | <!--v8:460-->34<!--/v8--> | N3 |
| dev-7f1b6b071d | N-Sigma đối chứng | ts-travel-service / loss | E-xa | <!--v8:461-->100<!--/v8--> | <!--v8:462-->720<!--/v8--> | <!--v8:463-->0<!--/v8--> | <!--v8:464-->620<!--/v8--> | <!--v8:465-->1<!--/v8--> | <!--v8:466-->361<!--/v8--> | N2 |
| dev-8017c6dc70 | BOCPD | ts-order-service / disk | E-xa | <!--v8:467-->271<!--/v8--> | <!--v8:468-->726<!--/v8--> | <!--v8:469-->6<!--/v8--> | <!--v8:470-->11<!--/v8--> | <!--v8:471-->N/A<!--/v8--> | <!--v8:472-->22<!--/v8--> | B2+B4 |
| dev-8017c6dc70 | N-Sigma chính | ts-order-service / disk | E-xa | <!--v8:473-->101<!--/v8--> | <!--v8:474-->723<!--/v8--> | <!--v8:475-->3<!--/v8--> | <!--v8:476-->197<!--/v8--> | <!--v8:477-->0.317742<!--/v8--> | <!--v8:478-->25<!--/v8--> | N1+N3 |
| dev-8017c6dc70 | N-Sigma đối chứng | ts-order-service / disk | E-xa | <!--v8:479-->100<!--/v8--> | <!--v8:480-->720<!--/v8--> | <!--v8:481-->0<!--/v8--> | <!--v8:482-->620<!--/v8--> | <!--v8:483-->1<!--/v8--> | <!--v8:484-->340<!--/v8--> | N2 |
| dev-98bc73c499 | BOCPD | ts-train-service / cpu | S | <!--v8:485-->761<!--/v8--> | <!--v8:486-->761<!--/v8--> | <!--v8:487-->41<!--/v8--> | <!--v8:488-->0<!--/v8--> | <!--v8:489-->N/A<!--/v8--> | <!--v8:490-->32<!--/v8--> | D0 |
| dev-98bc73c499 | N-Sigma chính | ts-train-service / cpu | E-xa | <!--v8:491-->102<!--/v8--> | <!--v8:492-->733<!--/v8--> | <!--v8:493-->13<!--/v8--> | <!--v8:494-->199<!--/v8--> | <!--v8:495-->0.320968<!--/v8--> | <!--v8:496-->42<!--/v8--> | N1+N3 |
| dev-98bc73c499 | N-Sigma đối chứng | ts-train-service / cpu | E-xa | <!--v8:497-->100<!--/v8--> | <!--v8:498-->720<!--/v8--> | <!--v8:499-->0<!--/v8--> | <!--v8:500-->620<!--/v8--> | <!--v8:501-->1<!--/v8--> | <!--v8:502-->369<!--/v8--> | N2 |
| dev-a505ab3f65 | BOCPD | ts-train-service / delay | E-xa | <!--v8:503-->384<!--/v8--> | <!--v8:504-->759<!--/v8--> | <!--v8:505-->39<!--/v8--> | <!--v8:506-->3<!--/v8--> | <!--v8:507-->N/A<!--/v8--> | <!--v8:508-->31<!--/v8--> | B2+B4 |
| dev-a505ab3f65 | N-Sigma chính | ts-train-service / delay | E-xa | <!--v8:509-->106<!--/v8--> | <!--v8:510-->720<!--/v8--> | <!--v8:511-->0<!--/v8--> | <!--v8:512-->242<!--/v8--> | <!--v8:513-->0.390323<!--/v8--> | <!--v8:514-->44<!--/v8--> | N3 |
| dev-a505ab3f65 | N-Sigma đối chứng | ts-train-service / delay | E-xa | <!--v8:515-->100<!--/v8--> | <!--v8:516-->720<!--/v8--> | <!--v8:517-->0<!--/v8--> | <!--v8:518-->620<!--/v8--> | <!--v8:519-->1<!--/v8--> | <!--v8:520-->371<!--/v8--> | N2 |
| dev-a5cabe5fa7 | BOCPD | ts-travel-service / loss | E-gần | <!--v8:521-->471<!--/v8--> | <!--v8:522-->813<!--/v8--> | <!--v8:523-->93<!--/v8--> | <!--v8:524-->6<!--/v8--> | <!--v8:525-->N/A<!--/v8--> | <!--v8:526-->30<!--/v8--> | B2+B4 |
| dev-a5cabe5fa7 | N-Sigma chính | ts-travel-service / loss | E-xa | <!--v8:527-->100<!--/v8--> | <!--v8:528-->733<!--/v8--> | <!--v8:529-->13<!--/v8--> | <!--v8:530-->273<!--/v8--> | <!--v8:531-->0.440323<!--/v8--> | <!--v8:532-->32<!--/v8--> | N3 |
| dev-a5cabe5fa7 | N-Sigma đối chứng | ts-travel-service / loss | E-xa | <!--v8:533-->100<!--/v8--> | <!--v8:534-->720<!--/v8--> | <!--v8:535-->0<!--/v8--> | <!--v8:536-->618<!--/v8--> | <!--v8:537-->0.996774<!--/v8--> | <!--v8:538-->359<!--/v8--> | N2 |
| dev-a915aa2424 | BOCPD | ts-travel-service / loss | E-gần | <!--v8:539-->679<!--/v8--> | <!--v8:540-->897<!--/v8--> | <!--v8:541-->177<!--/v8--> | <!--v8:542-->1<!--/v8--> | <!--v8:543-->N/A<!--/v8--> | <!--v8:544-->32<!--/v8--> | B4 |
| dev-a915aa2424 | N-Sigma chính | ts-travel-service / loss | E-xa | <!--v8:545-->100<!--/v8--> | <!--v8:546-->720<!--/v8--> | <!--v8:547-->0<!--/v8--> | <!--v8:548-->277<!--/v8--> | <!--v8:549-->0.446774<!--/v8--> | <!--v8:550-->41<!--/v8--> | N2 |
| dev-a915aa2424 | N-Sigma đối chứng | ts-travel-service / loss | E-xa | <!--v8:551-->100<!--/v8--> | <!--v8:552-->720<!--/v8--> | <!--v8:553-->0<!--/v8--> | <!--v8:554-->617<!--/v8--> | <!--v8:555-->0.995161<!--/v8--> | <!--v8:556-->368<!--/v8--> | N2 |
| dev-b8bd0abf60 | BOCPD | ts-route-service / socket | E-gần | <!--v8:557-->502<!--/v8--> | <!--v8:558-->738<!--/v8--> | <!--v8:559-->18<!--/v8--> | <!--v8:560-->3<!--/v8--> | <!--v8:561-->N/A<!--/v8--> | <!--v8:562-->32<!--/v8--> | B4 |
| dev-b8bd0abf60 | N-Sigma chính | ts-route-service / socket | E-xa | <!--v8:563-->107<!--/v8--> | <!--v8:564-->730<!--/v8--> | <!--v8:565-->10<!--/v8--> | <!--v8:566-->186<!--/v8--> | <!--v8:567-->0.3<!--/v8--> | <!--v8:568-->48<!--/v8--> | N3 |
| dev-b8bd0abf60 | N-Sigma đối chứng | ts-route-service / socket | E-xa | <!--v8:569-->100<!--/v8--> | <!--v8:570-->720<!--/v8--> | <!--v8:571-->0<!--/v8--> | <!--v8:572-->615<!--/v8--> | <!--v8:573-->0.991935<!--/v8--> | <!--v8:574-->375<!--/v8--> | N2 |
| dev-ba831dbeb8 | BOCPD | ts-train-service / cpu | E-gần | <!--v8:575-->548<!--/v8--> | <!--v8:576-->750<!--/v8--> | <!--v8:577-->30<!--/v8--> | <!--v8:578-->3<!--/v8--> | <!--v8:579-->N/A<!--/v8--> | <!--v8:580-->36<!--/v8--> | B4 |
| dev-ba831dbeb8 | N-Sigma chính | ts-train-service / cpu | E-xa | <!--v8:581-->115<!--/v8--> | <!--v8:582-->720<!--/v8--> | <!--v8:583-->0<!--/v8--> | <!--v8:584-->201<!--/v8--> | <!--v8:585-->0.324194<!--/v8--> | <!--v8:586-->41<!--/v8--> | N3 |
| dev-ba831dbeb8 | N-Sigma đối chứng | ts-train-service / cpu | E-xa | <!--v8:587-->100<!--/v8--> | <!--v8:588-->720<!--/v8--> | <!--v8:589-->0<!--/v8--> | <!--v8:590-->617<!--/v8--> | <!--v8:591-->0.995161<!--/v8--> | <!--v8:592-->368<!--/v8--> | N2 |
| dev-bcbd4f46ae | BOCPD | ts-route-service / socket | E-xa | <!--v8:593-->205<!--/v8--> | <!--v8:594-->759<!--/v8--> | <!--v8:595-->39<!--/v8--> | <!--v8:596-->3<!--/v8--> | <!--v8:597-->N/A<!--/v8--> | <!--v8:598-->28<!--/v8--> | B2+B4 |
| dev-bcbd4f46ae | N-Sigma chính | ts-route-service / socket | E-xa | <!--v8:599-->100<!--/v8--> | <!--v8:600-->759<!--/v8--> | <!--v8:601-->39<!--/v8--> | <!--v8:602-->51<!--/v8--> | <!--v8:603-->0.0822581<!--/v8--> | <!--v8:604-->34<!--/v8--> | N3 |
| dev-bcbd4f46ae | N-Sigma đối chứng | ts-route-service / socket | E-xa | <!--v8:605-->100<!--/v8--> | <!--v8:606-->720<!--/v8--> | <!--v8:607-->0<!--/v8--> | <!--v8:608-->609<!--/v8--> | <!--v8:609-->0.982258<!--/v8--> | <!--v8:610-->361<!--/v8--> | N1+N3 |
| dev-db293894ab | BOCPD | ts-travel-service / disk | E-xa | <!--v8:611-->212<!--/v8--> | <!--v8:612-->763<!--/v8--> | <!--v8:613-->43<!--/v8--> | <!--v8:614-->11<!--/v8--> | <!--v8:615-->N/A<!--/v8--> | <!--v8:616-->31<!--/v8--> | B2+B4 |
| dev-db293894ab | N-Sigma chính | ts-travel-service / disk | E-xa | <!--v8:617-->100<!--/v8--> | <!--v8:618-->738<!--/v8--> | <!--v8:619-->18<!--/v8--> | <!--v8:620-->203<!--/v8--> | <!--v8:621-->0.327419<!--/v8--> | <!--v8:622-->33<!--/v8--> | N3 |
| dev-db293894ab | N-Sigma đối chứng | ts-travel-service / disk | E-xa | <!--v8:623-->100<!--/v8--> | <!--v8:624-->720<!--/v8--> | <!--v8:625-->0<!--/v8--> | <!--v8:626-->611<!--/v8--> | <!--v8:627-->0.985484<!--/v8--> | <!--v8:628-->360<!--/v8--> | N2 |
| dev-de89e2f9e9 | BOCPD | ts-travel-service / disk | E-gần | <!--v8:629-->465<!--/v8--> | <!--v8:630-->774<!--/v8--> | <!--v8:631-->54<!--/v8--> | <!--v8:632-->3<!--/v8--> | <!--v8:633-->N/A<!--/v8--> | <!--v8:634-->30<!--/v8--> | D0 |
| dev-de89e2f9e9 | N-Sigma chính | ts-travel-service / disk | E-xa | <!--v8:635-->105<!--/v8--> | <!--v8:636-->737<!--/v8--> | <!--v8:637-->17<!--/v8--> | <!--v8:638-->140<!--/v8--> | <!--v8:639-->0.225806<!--/v8--> | <!--v8:640-->39<!--/v8--> | N3 |
| dev-de89e2f9e9 | N-Sigma đối chứng | ts-travel-service / disk | E-xa | <!--v8:641-->100<!--/v8--> | <!--v8:642-->720<!--/v8--> | <!--v8:643-->0<!--/v8--> | <!--v8:644-->620<!--/v8--> | <!--v8:645-->1<!--/v8--> | <!--v8:646-->366<!--/v8--> | N2 |
| dev-f36d0647d5 | BOCPD | ts-order-service / loss | S | <!--v8:647-->752<!--/v8--> | <!--v8:648-->752<!--/v8--> | <!--v8:649-->32<!--/v8--> | <!--v8:650-->0<!--/v8--> | <!--v8:651-->N/A<!--/v8--> | <!--v8:652-->33<!--/v8--> | D0 |
| dev-f36d0647d5 | N-Sigma chính | ts-order-service / loss | E-xa | <!--v8:653-->116<!--/v8--> | <!--v8:654-->720<!--/v8--> | <!--v8:655-->0<!--/v8--> | <!--v8:656-->130<!--/v8--> | <!--v8:657-->0.209677<!--/v8--> | <!--v8:658-->46<!--/v8--> | N1+N2 |
| dev-f36d0647d5 | N-Sigma đối chứng | ts-order-service / loss | E-xa | <!--v8:659-->100<!--/v8--> | <!--v8:660-->720<!--/v8--> | <!--v8:661-->0<!--/v8--> | <!--v8:662-->605<!--/v8--> | <!--v8:663-->0.975806<!--/v8--> | <!--v8:664-->373<!--/v8--> | N2 |
| dev-f81f88234e | BOCPD | ts-auth-service / delay | E-xa | <!--v8:665-->179<!--/v8--> | <!--v8:666-->1037<!--/v8--> | <!--v8:667-->317<!--/v8--> | <!--v8:668-->4<!--/v8--> | <!--v8:669-->N/A<!--/v8--> | <!--v8:670-->28<!--/v8--> | B2+B4 |
| dev-f81f88234e | N-Sigma chính | ts-auth-service / delay | E-gần | <!--v8:671-->490<!--/v8--> | <!--v8:672-->742<!--/v8--> | <!--v8:673-->22<!--/v8--> | <!--v8:674-->41<!--/v8--> | <!--v8:675-->0.066129<!--/v8--> | <!--v8:676-->32<!--/v8--> | N2 |
| dev-f81f88234e | N-Sigma đối chứng | ts-auth-service / delay | E-xa | <!--v8:677-->100<!--/v8--> | <!--v8:678-->720<!--/v8--> | <!--v8:679-->0<!--/v8--> | <!--v8:680-->607<!--/v8--> | <!--v8:681-->0.979032<!--/v8--> | <!--v8:682-->359<!--/v8--> | N2+N4 |
| dev-f9a8e05ed7 | BOCPD | ts-travel-service / disk | E-xa | <!--v8:683-->117<!--/v8--> | <!--v8:684-->824<!--/v8--> | <!--v8:685-->104<!--/v8--> | <!--v8:686-->6<!--/v8--> | <!--v8:687-->N/A<!--/v8--> | <!--v8:688-->31<!--/v8--> | B2+B4 |
| dev-f9a8e05ed7 | N-Sigma chính | ts-travel-service / disk | E-xa | <!--v8:689-->100<!--/v8--> | <!--v8:690-->720<!--/v8--> | <!--v8:691-->0<!--/v8--> | <!--v8:692-->210<!--/v8--> | <!--v8:693-->0.33871<!--/v8--> | <!--v8:694-->38<!--/v8--> | N3 |
| dev-f9a8e05ed7 | N-Sigma đối chứng | ts-travel-service / disk | E-xa | <!--v8:695-->100<!--/v8--> | <!--v8:696-->720<!--/v8--> | <!--v8:697-->0<!--/v8--> | <!--v8:698-->619<!--/v8--> | <!--v8:699-->0.998387<!--/v8--> | <!--v8:700-->365<!--/v8--> | N1+N2 |
| dev-fbc45b0c67 | BOCPD | ts-train-service / delay | E-xa | <!--v8:701-->289<!--/v8--> | <!--v8:702-->754<!--/v8--> | <!--v8:703-->34<!--/v8--> | <!--v8:704-->4<!--/v8--> | <!--v8:705-->N/A<!--/v8--> | <!--v8:706-->28<!--/v8--> | B4 |
| dev-fbc45b0c67 | N-Sigma chính | ts-train-service / delay | E-xa | <!--v8:707-->100<!--/v8--> | <!--v8:708-->721<!--/v8--> | <!--v8:709-->1<!--/v8--> | <!--v8:710-->282<!--/v8--> | <!--v8:711-->0.454839<!--/v8--> | <!--v8:712-->31<!--/v8--> | N3 |
| dev-fbc45b0c67 | N-Sigma đối chứng | ts-train-service / delay | E-xa | <!--v8:713-->100<!--/v8--> | <!--v8:714-->720<!--/v8--> | <!--v8:715-->0<!--/v8--> | <!--v8:716-->619<!--/v8--> | <!--v8:717-->0.998387<!--/v8--> | <!--v8:718-->358<!--/v8--> | N2 |

## C2 và C6 — Bản đồ hạn chế và nguồn tác giả

Bảng HP dùng số cờ đúng / cặp hợp lệ / tổng cặp, có N/A riêng. Dòng “phạm vi khảo sát” không là số ca bị lỗi. Đây là kết quả trên dev và các ngưỡng phân tích khóa trước, không là định nghĩa mới của detector.

| Mã | Bộ / cơ chế | Mức bằng chứng | Kết luận được phép | Giải thích khác / chưa kiểm | Tác giả |
|---|---|---|---|---|---|
| HP-1 | N-Sigma / N1: lịch sử ngắn | liên hệ + đọc tay | Có tỉ lệ báo khoảng đầu cao hơn khoảng cuối ở các ca có N1. | Drift, tải và ffill có thể khác theo thời gian; chưa có can thiệp độ dài lịch sử. | BARO nêu baseline khó với chuỗi phức tạp; chưa thấy cơ chế N1 riêng trong nguồn đã khảo sát. |
| HP-2 | N-Sigma / N2: cột báo dày | liên hệ + đọc tay | Chỉ ra cột đóng góp vào báo động đầu; số thay mạnh theo tập cột. | p_j cao chưa tách đuôi không chuẩn, nền không dừng hoặc lịch sử hữu hạn. | [BARO, đánh giá phát hiện](https://arxiv.org/html/2405.09330v1#S4.SS5) nêu báo sai baseline; chưa thấy N2 riêng. |
| HP-3 | N-Sigma / N3: E không có cột báo dày tại t̂ | liên hệ + đọc tay | Phần còn lại sau N2; ba tỉ lệ là mô tả. | Không chứng minh cộng dồn, độc lập hoặc phân phối chuẩn; một cột thưa cũng đủ gây báo. | Chưa thấy trong nguồn đã khảo sát; công thức OR nằm trong code/hồ sơ N-Sigma. |
| HP-4 | N-Sigma / N4: std bằng không | liên hệ + đọc tay | Trung gian xác nhận ngưỡng bằng không tại cột gây báo. | Độ phân giải, tải hoặc nền hằng; chưa phân xử ý nghĩa vận hành của socket. | Code tác giả có phép so này; chưa thấy tác giả nêu riêng như hạn chế trong bài đã khảo sát. |
| HP-5 | BOCPD / B1: đầu NaN điền không | liên hệ + đọc tay | Không có cờ B1 ở báo động đầu E của dev này. | Không kiểm mọi dạng missing hoặc tác động điền trước; B1 âm không bác ảnh hưởng thiếu dữ liệu. | Code có fillna; chưa thấy trong nguồn đã khảo sát như hạn chế thực nghiệm. |
| HP-6 | BOCPD / B2: dữ liệu sau mốc qua tiền xử lý | can thiệp I1 + đọc tay | Vị trí báo đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý; cắt sau mốc làm mất điểm đổi quanh t̂ ở các ca B2 nhưng có báo đầu sớm hơn. B2 chưa giải thích vì sao tồn tại báo động trước mốc; chiều can thiệp và điều kiện của S được báo riêng dưới đây. | I1 đổi bộ cột và min–max, kéo theo số chiều của prior; vẫn nhìn dữ liệu sau t̂ trong tiền tố. B2 sai chưa loại look-ahead; không suy bỏ nhìn trước sẽ giảm báo sai. | Code tiền xử lý toàn chuỗi; chưa thấy tác giả nêu hạn chế này trong nguồn đã khảo sát. |
| HP-7 | BOCPD / B3: hazard | can thiệp I2 + đọc tay | Không có B3 đúng trên miền được chấm. Số điểm đổi khác vẫn có thể đổi. | Chỉ kiểm trước mốc; chưa chạy toàn bản ghi với hazard khác theo giới hạn chi phí SPEC. | Hazard thay thế có trong code; chưa thấy phân tích B3 trên giao thức này trong nguồn đã khảo sát. |
| HP-8 | BOCPD / B4: bước nhảy telemetry trước mốc | liên hệ, V7 + đọc tay | Mô tả bước median lớn. Cờ phổ biến ở điểm không báo và đổi chiều theo ô/độ nhạy; không dùng B4 riêng làm lời giải thích sự tồn tại của báo động trước mốc. | Nền không sạch, biến động tải, MAD nhỏ, nhiều cơ hội qua nhiều cột; chưa có nhãn nền độc lập. | [BARO, giả định đầu vào](https://arxiv.org/html/2405.09330v1#S3.SS1) nêu bất thường hiện ở latency/error; chưa thấy phân xử B4/V7 này. |
| HP-9 | D0: không có cờ chính | đọc tay; chưa giải thích | Với E, D0 thuộc nhóm chưa giải thích nhưng không bao hết nhóm đó: có cờ cũng chưa chắc đã giải thích. Với S, D0 có thể do miền N/A; không tính thành thất bại báo sớm. Không ép vào cơ chế; N/A không là cờ âm. | Covariance/prior, drift và bước nhỏ vẫn có thể góp phần; chưa có can thiệp phân xử chúng. | Chưa thấy trong nguồn đã khảo sát. |
| HP-10 | Đầu ra detector và định vị service | liên hệ / thiết kế | N-Sigma cho cột, phân tích E thêm mapping/thứ tự; BOCPD không native attribution. | Báo động kéo dài qua mốc, hòa, root hết cột; chưa chứng minh onset, nhân quả hoặc lan. | [BARO, pipeline](https://arxiv.org/html/2405.09330v1#S3.SS2) tách detector với ranker; chưa thấy rank E như đầu ra native. |
| HP-11 | RCA phụ thuộc điểm chạy | can thiệp I3 | Chênh ghép cặp có dấu; bảng G cho kết quả có điều kiện theo ô và cohort. | Đổi cửa sổ cũng đổi nền, cột ứng viên và graph CIRCA; chưa tách riêng các đường tác động. | [BARO, độ nhạy thời điểm](https://arxiv.org/html/2405.09330v1#S4.SS8.SSS1) có nêu; chưa thấy phân rã G của T-029. |
| HP-12 | Nhãn proxy / thời lượng lỗi D | chưa kiểm D; liên hệ P1 | Nguồn chưa xác nhận D; chưa chấm lại P/R/F1. Timeline chỉ mô tả telemetry. | Metric phục hồi không đồng nghĩa lỗi đã hết; root có cột thiếu, Nv khác cho quantile khác. | [RCAEval, tạo dữ liệu](https://arxiv.org/html/2412.17015v2#S3.SS3) mô tả mốc và thu thập; chưa thấy D cho các ca này. |
| HP-13 | Schema và nhãn | liên hệ P2 | Không có cột đạt phân hoạch root hoàn toàn; có vắng cột liên hệ một root trong dev. | Root và loại lỗi chưa giao chéo đầy đủ; triển khai/thu thập và tổ hợp schema còn có thể giải thích. | Chưa thấy trong nguồn đã khảo sát. |
| HP-14 | N-Sigma / N6: nền mở rộng nhận dữ liệu sau mốc | thiết kế + mô tả; chưa kiểm nhân quả | Code nhận dữ liệu đã quan sát vào mean/std; timeline báo thay đổi mật độ. | Giảm báo có thể do phục hồi, đổi tải, ngưỡng tăng hoặc biến động cột; chưa can thiệp cố định nền. | Code tác giả, [hồ sơ N-Sigma](../T-013/ho-so-nsigma-phat-hien.md); không dùng số bài thay kết quả này. |

Nguồn tác giả đã khảo sát: bài BARO bản v1 (phần giả định, mô hình, phát hiện, độ nhạy thời điểm, giới hạn); code BARO ở revision trong [manifest T-013](../T-013/manifest.json), hồ sơ BOCPD/N-Sigma/cửa sổ; nguồn công bố RCAEval đã lưu cho P1. “Chưa thấy” chỉ áp các nguồn đã khảo sát, không là tuyên bố mọi tài liệu đều không có.

### Chiều can thiệp I1: theo ô và tổng gộp

| Ô | Ca | Điểm đổi Nv full | I1 | I2 | Báo đầu I1 sớm / bằng / muộn | Số điểm đổi I1 tăng / bằng / giảm |
|---|---|---|---|---|---|---|
| ts-auth-service / cpu | <!--v8:6144-->3<!--/v8--> | <!--v8:6145-->23<!--/v8--> | <!--v8:6146-->41<!--/v8--> | <!--v8:6147-->40<!--/v8--> | <!--v8:6148-->3<!--/v8--> / <!--v8:6149-->0<!--/v8--> / <!--v8:6150-->0<!--/v8--> | <!--v8:6151-->3<!--/v8--> / <!--v8:6152-->0<!--/v8--> / <!--v8:6153-->0<!--/v8--> |
| ts-auth-service / delay | <!--v8:6154-->3<!--/v8--> | <!--v8:6155-->11<!--/v8--> | <!--v8:6156-->24<!--/v8--> | <!--v8:6157-->24<!--/v8--> | <!--v8:6158-->2<!--/v8--> / <!--v8:6159-->1<!--/v8--> / <!--v8:6160-->0<!--/v8--> | <!--v8:6161-->2<!--/v8--> / <!--v8:6162-->1<!--/v8--> / <!--v8:6163-->0<!--/v8--> |
| ts-order-service / disk | <!--v8:6164-->3<!--/v8--> | <!--v8:6165-->27<!--/v8--> | <!--v8:6166-->26<!--/v8--> | <!--v8:6167-->26<!--/v8--> | <!--v8:6168-->3<!--/v8--> / <!--v8:6169-->0<!--/v8--> / <!--v8:6170-->0<!--/v8--> | <!--v8:6171-->1<!--/v8--> / <!--v8:6172-->0<!--/v8--> / <!--v8:6173-->2<!--/v8--> |
| ts-order-service / loss | <!--v8:6174-->3<!--/v8--> | <!--v8:6175-->17<!--/v8--> | <!--v8:6176-->41<!--/v8--> | <!--v8:6177-->39<!--/v8--> | <!--v8:6178-->3<!--/v8--> / <!--v8:6179-->0<!--/v8--> / <!--v8:6180-->0<!--/v8--> | <!--v8:6181-->3<!--/v8--> / <!--v8:6182-->0<!--/v8--> / <!--v8:6183-->0<!--/v8--> |
| ts-route-service / mem | <!--v8:6184-->3<!--/v8--> | <!--v8:6185-->8<!--/v8--> | <!--v8:6186-->22<!--/v8--> | <!--v8:6187-->22<!--/v8--> | <!--v8:6188-->3<!--/v8--> / <!--v8:6189-->0<!--/v8--> / <!--v8:6190-->0<!--/v8--> | <!--v8:6191-->2<!--/v8--> / <!--v8:6192-->1<!--/v8--> / <!--v8:6193-->0<!--/v8--> |
| ts-route-service / socket | <!--v8:6194-->3<!--/v8--> | <!--v8:6195-->9<!--/v8--> | <!--v8:6196-->34<!--/v8--> | <!--v8:6197-->34<!--/v8--> | <!--v8:6198-->3<!--/v8--> / <!--v8:6199-->0<!--/v8--> / <!--v8:6200-->0<!--/v8--> | <!--v8:6201-->2<!--/v8--> / <!--v8:6202-->1<!--/v8--> / <!--v8:6203-->0<!--/v8--> |
| ts-train-service / cpu | <!--v8:6204-->3<!--/v8--> | <!--v8:6205-->6<!--/v8--> | <!--v8:6206-->41<!--/v8--> | <!--v8:6207-->39<!--/v8--> | <!--v8:6208-->3<!--/v8--> / <!--v8:6209-->0<!--/v8--> / <!--v8:6210-->0<!--/v8--> | <!--v8:6211-->3<!--/v8--> / <!--v8:6212-->0<!--/v8--> / <!--v8:6213-->0<!--/v8--> |
| ts-train-service / delay | <!--v8:6214-->3<!--/v8--> | <!--v8:6215-->8<!--/v8--> | <!--v8:6216-->46<!--/v8--> | <!--v8:6217-->45<!--/v8--> | <!--v8:6218-->3<!--/v8--> / <!--v8:6219-->0<!--/v8--> / <!--v8:6220-->0<!--/v8--> | <!--v8:6221-->3<!--/v8--> / <!--v8:6222-->0<!--/v8--> / <!--v8:6223-->0<!--/v8--> |
| ts-travel-service / disk | <!--v8:6224-->3<!--/v8--> | <!--v8:6225-->20<!--/v8--> | <!--v8:6226-->29<!--/v8--> | <!--v8:6227-->29<!--/v8--> | <!--v8:6228-->3<!--/v8--> / <!--v8:6229-->0<!--/v8--> / <!--v8:6230-->0<!--/v8--> | <!--v8:6231-->1<!--/v8--> / <!--v8:6232-->0<!--/v8--> / <!--v8:6233-->2<!--/v8--> |
| ts-travel-service / loss | <!--v8:6234-->3<!--/v8--> | <!--v8:6235-->14<!--/v8--> | <!--v8:6236-->34<!--/v8--> | <!--v8:6237-->34<!--/v8--> | <!--v8:6238-->3<!--/v8--> / <!--v8:6239-->0<!--/v8--> / <!--v8:6240-->0<!--/v8--> | <!--v8:6241-->3<!--/v8--> / <!--v8:6242-->0<!--/v8--> / <!--v8:6243-->0<!--/v8--> |

Khi cắt sau mốc theo I1, báo đầu sớm hơn ở <!--v8:6244-->29<!--/v8-->/<!--v8:6245-->30<!--/v8--> ca, bằng ở <!--v8:6246-->1<!--/v8--> ca và muộn hơn ở <!--v8:6247-->0<!--/v8--> ca. Số điểm đổi trong Nv tăng/bằng/giảm so với bản đầy đủ lần lượt ở <!--v8:6248-->23<!--/v8-->/<!--v8:6249-->3<!--/v8-->/<!--v8:6250-->4<!--/v8--> ca; tổng full/I1/I2 là <!--v8:6251-->143<!--/v8-->/<!--v8:6252-->338<!--/v8-->/<!--v8:6253-->332<!--/v8-->. Hai đại lượng phải đọc riêng; các ca ngược chiều chỉ thuộc số điểm đổi nền, không thuộc báo đầu trên mẫu này. Cả <!--v8:6254-->17<!--/v8-->/<!--v8:6255-->17<!--/v8--> ca B2 chính có báo đầu sớm hơn trong I1. Đây là tác động lên đầu ra detector qua tiền xử lý, không xác nhận nguyên nhân vận hành của báo sớm.

Nguồn: `runs/review4-repair-001/summary.json#/intervention`; từng ca gốc ở `bocpd-can-thiep.json#/cases` và bảng B5/I1/I2 cuối báo cáo. I1 không loại nhìn trước bên trong tiền tố.

### Số HP theo từng ô

Nguồn: `runs/report-main-001/summary.json#/HP_cells`; mỗi ô = đúng / hợp lệ / tổng (N/A).

| HP | Bộ | Ô | Đúng / hợp lệ / tổng | N/A |
|---|---|---|---|---|
| HP-1 | N-Sigma chính | ts-auth-service / cpu | <!--v8:719-->0<!--/v8--> / <!--v8:720-->3<!--/v8--> / <!--v8:721-->3<!--/v8--> | <!--v8:722-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-auth-service / delay | <!--v8:723-->0<!--/v8--> / <!--v8:724-->3<!--/v8--> / <!--v8:725-->3<!--/v8--> | <!--v8:726-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-order-service / disk | <!--v8:727-->2<!--/v8--> / <!--v8:728-->3<!--/v8--> / <!--v8:729-->3<!--/v8--> | <!--v8:730-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-order-service / loss | <!--v8:731-->1<!--/v8--> / <!--v8:732-->3<!--/v8--> / <!--v8:733-->3<!--/v8--> | <!--v8:734-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-route-service / mem | <!--v8:735-->1<!--/v8--> / <!--v8:736-->3<!--/v8--> / <!--v8:737-->3<!--/v8--> | <!--v8:738-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-route-service / socket | <!--v8:739-->0<!--/v8--> / <!--v8:740-->3<!--/v8--> / <!--v8:741-->3<!--/v8--> | <!--v8:742-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-train-service / cpu | <!--v8:743-->1<!--/v8--> / <!--v8:744-->3<!--/v8--> / <!--v8:745-->3<!--/v8--> | <!--v8:746-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-train-service / delay | <!--v8:747-->0<!--/v8--> / <!--v8:748-->3<!--/v8--> / <!--v8:749-->3<!--/v8--> | <!--v8:750-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-travel-service / disk | <!--v8:751-->0<!--/v8--> / <!--v8:752-->3<!--/v8--> / <!--v8:753-->3<!--/v8--> | <!--v8:754-->0<!--/v8--> |
| HP-1 | N-Sigma chính | ts-travel-service / loss | <!--v8:755-->0<!--/v8--> / <!--v8:756-->3<!--/v8--> / <!--v8:757-->3<!--/v8--> | <!--v8:758-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:759-->1<!--/v8--> / <!--v8:760-->3<!--/v8--> / <!--v8:761-->3<!--/v8--> | <!--v8:762-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-auth-service / delay | <!--v8:763-->0<!--/v8--> / <!--v8:764-->3<!--/v8--> / <!--v8:765-->3<!--/v8--> | <!--v8:766-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-order-service / disk | <!--v8:767-->0<!--/v8--> / <!--v8:768-->3<!--/v8--> / <!--v8:769-->3<!--/v8--> | <!--v8:770-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-order-service / loss | <!--v8:771-->0<!--/v8--> / <!--v8:772-->3<!--/v8--> / <!--v8:773-->3<!--/v8--> | <!--v8:774-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-route-service / mem | <!--v8:775-->1<!--/v8--> / <!--v8:776-->3<!--/v8--> / <!--v8:777-->3<!--/v8--> | <!--v8:778-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-route-service / socket | <!--v8:779-->1<!--/v8--> / <!--v8:780-->3<!--/v8--> / <!--v8:781-->3<!--/v8--> | <!--v8:782-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-train-service / cpu | <!--v8:783-->0<!--/v8--> / <!--v8:784-->3<!--/v8--> / <!--v8:785-->3<!--/v8--> | <!--v8:786-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-train-service / delay | <!--v8:787-->0<!--/v8--> / <!--v8:788-->3<!--/v8--> / <!--v8:789-->3<!--/v8--> | <!--v8:790-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-travel-service / disk | <!--v8:791-->1<!--/v8--> / <!--v8:792-->3<!--/v8--> / <!--v8:793-->3<!--/v8--> | <!--v8:794-->0<!--/v8--> |
| HP-1 | N-Sigma đối chứng | ts-travel-service / loss | <!--v8:795-->0<!--/v8--> / <!--v8:796-->3<!--/v8--> / <!--v8:797-->3<!--/v8--> | <!--v8:798-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-auth-service / cpu | <!--v8:799-->1<!--/v8--> / <!--v8:800-->3<!--/v8--> / <!--v8:801-->3<!--/v8--> | <!--v8:802-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-auth-service / delay | <!--v8:803-->2<!--/v8--> / <!--v8:804-->3<!--/v8--> / <!--v8:805-->3<!--/v8--> | <!--v8:806-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-order-service / disk | <!--v8:807-->0<!--/v8--> / <!--v8:808-->3<!--/v8--> / <!--v8:809-->3<!--/v8--> | <!--v8:810-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-order-service / loss | <!--v8:811-->1<!--/v8--> / <!--v8:812-->3<!--/v8--> / <!--v8:813-->3<!--/v8--> | <!--v8:814-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-route-service / mem | <!--v8:815-->0<!--/v8--> / <!--v8:816-->3<!--/v8--> / <!--v8:817-->3<!--/v8--> | <!--v8:818-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-route-service / socket | <!--v8:819-->0<!--/v8--> / <!--v8:820-->3<!--/v8--> / <!--v8:821-->3<!--/v8--> | <!--v8:822-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-train-service / cpu | <!--v8:823-->1<!--/v8--> / <!--v8:824-->3<!--/v8--> / <!--v8:825-->3<!--/v8--> | <!--v8:826-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-train-service / delay | <!--v8:827-->0<!--/v8--> / <!--v8:828-->3<!--/v8--> / <!--v8:829-->3<!--/v8--> | <!--v8:830-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-travel-service / disk | <!--v8:831-->0<!--/v8--> / <!--v8:832-->3<!--/v8--> / <!--v8:833-->3<!--/v8--> | <!--v8:834-->0<!--/v8--> |
| HP-2 | N-Sigma chính | ts-travel-service / loss | <!--v8:835-->1<!--/v8--> / <!--v8:836-->3<!--/v8--> / <!--v8:837-->3<!--/v8--> | <!--v8:838-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:839-->3<!--/v8--> / <!--v8:840-->3<!--/v8--> / <!--v8:841-->3<!--/v8--> | <!--v8:842-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-auth-service / delay | <!--v8:843-->3<!--/v8--> / <!--v8:844-->3<!--/v8--> / <!--v8:845-->3<!--/v8--> | <!--v8:846-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-order-service / disk | <!--v8:847-->3<!--/v8--> / <!--v8:848-->3<!--/v8--> / <!--v8:849-->3<!--/v8--> | <!--v8:850-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-order-service / loss | <!--v8:851-->3<!--/v8--> / <!--v8:852-->3<!--/v8--> / <!--v8:853-->3<!--/v8--> | <!--v8:854-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-route-service / mem | <!--v8:855-->3<!--/v8--> / <!--v8:856-->3<!--/v8--> / <!--v8:857-->3<!--/v8--> | <!--v8:858-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-route-service / socket | <!--v8:859-->2<!--/v8--> / <!--v8:860-->3<!--/v8--> / <!--v8:861-->3<!--/v8--> | <!--v8:862-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-train-service / cpu | <!--v8:863-->3<!--/v8--> / <!--v8:864-->3<!--/v8--> / <!--v8:865-->3<!--/v8--> | <!--v8:866-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-train-service / delay | <!--v8:867-->3<!--/v8--> / <!--v8:868-->3<!--/v8--> / <!--v8:869-->3<!--/v8--> | <!--v8:870-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-travel-service / disk | <!--v8:871-->3<!--/v8--> / <!--v8:872-->3<!--/v8--> / <!--v8:873-->3<!--/v8--> | <!--v8:874-->0<!--/v8--> |
| HP-2 | N-Sigma đối chứng | ts-travel-service / loss | <!--v8:875-->3<!--/v8--> / <!--v8:876-->3<!--/v8--> / <!--v8:877-->3<!--/v8--> | <!--v8:878-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-auth-service / cpu | <!--v8:879-->2<!--/v8--> / <!--v8:880-->3<!--/v8--> / <!--v8:881-->3<!--/v8--> | <!--v8:882-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-auth-service / delay | <!--v8:883-->1<!--/v8--> / <!--v8:884-->3<!--/v8--> / <!--v8:885-->3<!--/v8--> | <!--v8:886-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-order-service / disk | <!--v8:887-->3<!--/v8--> / <!--v8:888-->3<!--/v8--> / <!--v8:889-->3<!--/v8--> | <!--v8:890-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-order-service / loss | <!--v8:891-->2<!--/v8--> / <!--v8:892-->3<!--/v8--> / <!--v8:893-->3<!--/v8--> | <!--v8:894-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-route-service / mem | <!--v8:895-->3<!--/v8--> / <!--v8:896-->3<!--/v8--> / <!--v8:897-->3<!--/v8--> | <!--v8:898-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-route-service / socket | <!--v8:899-->3<!--/v8--> / <!--v8:900-->3<!--/v8--> / <!--v8:901-->3<!--/v8--> | <!--v8:902-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-train-service / cpu | <!--v8:903-->2<!--/v8--> / <!--v8:904-->3<!--/v8--> / <!--v8:905-->3<!--/v8--> | <!--v8:906-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-train-service / delay | <!--v8:907-->3<!--/v8--> / <!--v8:908-->3<!--/v8--> / <!--v8:909-->3<!--/v8--> | <!--v8:910-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-travel-service / disk | <!--v8:911-->3<!--/v8--> / <!--v8:912-->3<!--/v8--> / <!--v8:913-->3<!--/v8--> | <!--v8:914-->0<!--/v8--> |
| HP-3 | N-Sigma chính | ts-travel-service / loss | <!--v8:915-->2<!--/v8--> / <!--v8:916-->3<!--/v8--> / <!--v8:917-->3<!--/v8--> | <!--v8:918-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:919-->0<!--/v8--> / <!--v8:920-->3<!--/v8--> / <!--v8:921-->3<!--/v8--> | <!--v8:922-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-auth-service / delay | <!--v8:923-->0<!--/v8--> / <!--v8:924-->3<!--/v8--> / <!--v8:925-->3<!--/v8--> | <!--v8:926-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-order-service / disk | <!--v8:927-->0<!--/v8--> / <!--v8:928-->3<!--/v8--> / <!--v8:929-->3<!--/v8--> | <!--v8:930-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-order-service / loss | <!--v8:931-->0<!--/v8--> / <!--v8:932-->3<!--/v8--> / <!--v8:933-->3<!--/v8--> | <!--v8:934-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-route-service / mem | <!--v8:935-->0<!--/v8--> / <!--v8:936-->3<!--/v8--> / <!--v8:937-->3<!--/v8--> | <!--v8:938-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-route-service / socket | <!--v8:939-->1<!--/v8--> / <!--v8:940-->3<!--/v8--> / <!--v8:941-->3<!--/v8--> | <!--v8:942-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-train-service / cpu | <!--v8:943-->0<!--/v8--> / <!--v8:944-->3<!--/v8--> / <!--v8:945-->3<!--/v8--> | <!--v8:946-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-train-service / delay | <!--v8:947-->0<!--/v8--> / <!--v8:948-->3<!--/v8--> / <!--v8:949-->3<!--/v8--> | <!--v8:950-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-travel-service / disk | <!--v8:951-->0<!--/v8--> / <!--v8:952-->3<!--/v8--> / <!--v8:953-->3<!--/v8--> | <!--v8:954-->0<!--/v8--> |
| HP-3 | N-Sigma đối chứng | ts-travel-service / loss | <!--v8:955-->0<!--/v8--> / <!--v8:956-->3<!--/v8--> / <!--v8:957-->3<!--/v8--> | <!--v8:958-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-auth-service / cpu | <!--v8:959-->0<!--/v8--> / <!--v8:960-->3<!--/v8--> / <!--v8:961-->3<!--/v8--> | <!--v8:962-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-auth-service / delay | <!--v8:963-->0<!--/v8--> / <!--v8:964-->3<!--/v8--> / <!--v8:965-->3<!--/v8--> | <!--v8:966-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-order-service / disk | <!--v8:967-->0<!--/v8--> / <!--v8:968-->3<!--/v8--> / <!--v8:969-->3<!--/v8--> | <!--v8:970-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-order-service / loss | <!--v8:971-->0<!--/v8--> / <!--v8:972-->3<!--/v8--> / <!--v8:973-->3<!--/v8--> | <!--v8:974-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-route-service / mem | <!--v8:975-->0<!--/v8--> / <!--v8:976-->3<!--/v8--> / <!--v8:977-->3<!--/v8--> | <!--v8:978-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-route-service / socket | <!--v8:979-->0<!--/v8--> / <!--v8:980-->3<!--/v8--> / <!--v8:981-->3<!--/v8--> | <!--v8:982-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-train-service / cpu | <!--v8:983-->0<!--/v8--> / <!--v8:984-->3<!--/v8--> / <!--v8:985-->3<!--/v8--> | <!--v8:986-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-train-service / delay | <!--v8:987-->0<!--/v8--> / <!--v8:988-->3<!--/v8--> / <!--v8:989-->3<!--/v8--> | <!--v8:990-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-travel-service / disk | <!--v8:991-->0<!--/v8--> / <!--v8:992-->3<!--/v8--> / <!--v8:993-->3<!--/v8--> | <!--v8:994-->0<!--/v8--> |
| HP-4 | N-Sigma chính | ts-travel-service / loss | <!--v8:995-->0<!--/v8--> / <!--v8:996-->3<!--/v8--> / <!--v8:997-->3<!--/v8--> | <!--v8:998-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:999-->1<!--/v8--> / <!--v8:1000-->3<!--/v8--> / <!--v8:1001-->3<!--/v8--> | <!--v8:1002-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-auth-service / delay | <!--v8:1003-->2<!--/v8--> / <!--v8:1004-->3<!--/v8--> / <!--v8:1005-->3<!--/v8--> | <!--v8:1006-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-order-service / disk | <!--v8:1007-->0<!--/v8--> / <!--v8:1008-->3<!--/v8--> / <!--v8:1009-->3<!--/v8--> | <!--v8:1010-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-order-service / loss | <!--v8:1011-->0<!--/v8--> / <!--v8:1012-->3<!--/v8--> / <!--v8:1013-->3<!--/v8--> | <!--v8:1014-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-route-service / mem | <!--v8:1015-->0<!--/v8--> / <!--v8:1016-->3<!--/v8--> / <!--v8:1017-->3<!--/v8--> | <!--v8:1018-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-route-service / socket | <!--v8:1019-->0<!--/v8--> / <!--v8:1020-->3<!--/v8--> / <!--v8:1021-->3<!--/v8--> | <!--v8:1022-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-train-service / cpu | <!--v8:1023-->0<!--/v8--> / <!--v8:1024-->3<!--/v8--> / <!--v8:1025-->3<!--/v8--> | <!--v8:1026-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-train-service / delay | <!--v8:1027-->0<!--/v8--> / <!--v8:1028-->3<!--/v8--> / <!--v8:1029-->3<!--/v8--> | <!--v8:1030-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-travel-service / disk | <!--v8:1031-->0<!--/v8--> / <!--v8:1032-->3<!--/v8--> / <!--v8:1033-->3<!--/v8--> | <!--v8:1034-->0<!--/v8--> |
| HP-4 | N-Sigma đối chứng | ts-travel-service / loss | <!--v8:1035-->0<!--/v8--> / <!--v8:1036-->3<!--/v8--> / <!--v8:1037-->3<!--/v8--> | <!--v8:1038-->0<!--/v8--> |
| HP-5 | BOCPD | ts-auth-service / cpu | <!--v8:1039-->0<!--/v8--> / <!--v8:1040-->2<!--/v8--> / <!--v8:1041-->3<!--/v8--> | <!--v8:1042-->1<!--/v8--> |
| HP-5 | BOCPD | ts-auth-service / delay | <!--v8:1043-->0<!--/v8--> / <!--v8:1044-->3<!--/v8--> / <!--v8:1045-->3<!--/v8--> | <!--v8:1046-->0<!--/v8--> |
| HP-5 | BOCPD | ts-order-service / disk | <!--v8:1047-->0<!--/v8--> / <!--v8:1048-->3<!--/v8--> / <!--v8:1049-->3<!--/v8--> | <!--v8:1050-->0<!--/v8--> |
| HP-5 | BOCPD | ts-order-service / loss | <!--v8:1051-->0<!--/v8--> / <!--v8:1052-->2<!--/v8--> / <!--v8:1053-->3<!--/v8--> | <!--v8:1054-->1<!--/v8--> |
| HP-5 | BOCPD | ts-route-service / mem | <!--v8:1055-->0<!--/v8--> / <!--v8:1056-->3<!--/v8--> / <!--v8:1057-->3<!--/v8--> | <!--v8:1058-->0<!--/v8--> |
| HP-5 | BOCPD | ts-route-service / socket | <!--v8:1059-->0<!--/v8--> / <!--v8:1060-->3<!--/v8--> / <!--v8:1061-->3<!--/v8--> | <!--v8:1062-->0<!--/v8--> |
| HP-5 | BOCPD | ts-train-service / cpu | <!--v8:1063-->0<!--/v8--> / <!--v8:1064-->2<!--/v8--> / <!--v8:1065-->3<!--/v8--> | <!--v8:1066-->1<!--/v8--> |
| HP-5 | BOCPD | ts-train-service / delay | <!--v8:1067-->0<!--/v8--> / <!--v8:1068-->3<!--/v8--> / <!--v8:1069-->3<!--/v8--> | <!--v8:1070-->0<!--/v8--> |
| HP-5 | BOCPD | ts-travel-service / disk | <!--v8:1071-->0<!--/v8--> / <!--v8:1072-->3<!--/v8--> / <!--v8:1073-->3<!--/v8--> | <!--v8:1074-->0<!--/v8--> |
| HP-5 | BOCPD | ts-travel-service / loss | <!--v8:1075-->0<!--/v8--> / <!--v8:1076-->3<!--/v8--> / <!--v8:1077-->3<!--/v8--> | <!--v8:1078-->0<!--/v8--> |
| HP-6 | BOCPD | ts-auth-service / cpu | <!--v8:1079-->2<!--/v8--> / <!--v8:1080-->2<!--/v8--> / <!--v8:1081-->3<!--/v8--> | <!--v8:1082-->1<!--/v8--> |
| HP-6 | BOCPD | ts-auth-service / delay | <!--v8:1083-->2<!--/v8--> / <!--v8:1084-->3<!--/v8--> / <!--v8:1085-->3<!--/v8--> | <!--v8:1086-->0<!--/v8--> |
| HP-6 | BOCPD | ts-order-service / disk | <!--v8:1087-->3<!--/v8--> / <!--v8:1088-->3<!--/v8--> / <!--v8:1089-->3<!--/v8--> | <!--v8:1090-->0<!--/v8--> |
| HP-6 | BOCPD | ts-order-service / loss | <!--v8:1091-->2<!--/v8--> / <!--v8:1092-->2<!--/v8--> / <!--v8:1093-->3<!--/v8--> | <!--v8:1094-->1<!--/v8--> |
| HP-6 | BOCPD | ts-route-service / mem | <!--v8:1095-->1<!--/v8--> / <!--v8:1096-->3<!--/v8--> / <!--v8:1097-->3<!--/v8--> | <!--v8:1098-->0<!--/v8--> |
| HP-6 | BOCPD | ts-route-service / socket | <!--v8:1099-->2<!--/v8--> / <!--v8:1100-->3<!--/v8--> / <!--v8:1101-->3<!--/v8--> | <!--v8:1102-->0<!--/v8--> |
| HP-6 | BOCPD | ts-train-service / cpu | <!--v8:1103-->0<!--/v8--> / <!--v8:1104-->2<!--/v8--> / <!--v8:1105-->3<!--/v8--> | <!--v8:1106-->1<!--/v8--> |
| HP-6 | BOCPD | ts-train-service / delay | <!--v8:1107-->2<!--/v8--> / <!--v8:1108-->3<!--/v8--> / <!--v8:1109-->3<!--/v8--> | <!--v8:1110-->0<!--/v8--> |
| HP-6 | BOCPD | ts-travel-service / disk | <!--v8:1111-->2<!--/v8--> / <!--v8:1112-->3<!--/v8--> / <!--v8:1113-->3<!--/v8--> | <!--v8:1114-->0<!--/v8--> |
| HP-6 | BOCPD | ts-travel-service / loss | <!--v8:1115-->1<!--/v8--> / <!--v8:1116-->3<!--/v8--> / <!--v8:1117-->3<!--/v8--> | <!--v8:1118-->0<!--/v8--> |
| HP-7 | BOCPD | ts-auth-service / cpu | <!--v8:1119-->0<!--/v8--> / <!--v8:1120-->0<!--/v8--> / <!--v8:1121-->3<!--/v8--> | <!--v8:1122-->3<!--/v8--> |
| HP-7 | BOCPD | ts-auth-service / delay | <!--v8:1123-->0<!--/v8--> / <!--v8:1124-->1<!--/v8--> / <!--v8:1125-->3<!--/v8--> | <!--v8:1126-->2<!--/v8--> |
| HP-7 | BOCPD | ts-order-service / disk | <!--v8:1127-->0<!--/v8--> / <!--v8:1128-->0<!--/v8--> / <!--v8:1129-->3<!--/v8--> | <!--v8:1130-->3<!--/v8--> |
| HP-7 | BOCPD | ts-order-service / loss | <!--v8:1131-->0<!--/v8--> / <!--v8:1132-->0<!--/v8--> / <!--v8:1133-->3<!--/v8--> | <!--v8:1134-->3<!--/v8--> |
| HP-7 | BOCPD | ts-route-service / mem | <!--v8:1135-->0<!--/v8--> / <!--v8:1136-->2<!--/v8--> / <!--v8:1137-->3<!--/v8--> | <!--v8:1138-->1<!--/v8--> |
| HP-7 | BOCPD | ts-route-service / socket | <!--v8:1139-->0<!--/v8--> / <!--v8:1140-->1<!--/v8--> / <!--v8:1141-->3<!--/v8--> | <!--v8:1142-->2<!--/v8--> |
| HP-7 | BOCPD | ts-train-service / cpu | <!--v8:1143-->0<!--/v8--> / <!--v8:1144-->2<!--/v8--> / <!--v8:1145-->3<!--/v8--> | <!--v8:1146-->1<!--/v8--> |
| HP-7 | BOCPD | ts-train-service / delay | <!--v8:1147-->0<!--/v8--> / <!--v8:1148-->1<!--/v8--> / <!--v8:1149-->3<!--/v8--> | <!--v8:1150-->2<!--/v8--> |
| HP-7 | BOCPD | ts-travel-service / disk | <!--v8:1151-->0<!--/v8--> / <!--v8:1152-->1<!--/v8--> / <!--v8:1153-->3<!--/v8--> | <!--v8:1154-->2<!--/v8--> |
| HP-7 | BOCPD | ts-travel-service / loss | <!--v8:1155-->0<!--/v8--> / <!--v8:1156-->2<!--/v8--> / <!--v8:1157-->3<!--/v8--> | <!--v8:1158-->1<!--/v8--> |
| HP-8 | BOCPD | ts-auth-service / cpu | <!--v8:1159-->2<!--/v8--> / <!--v8:1160-->2<!--/v8--> / <!--v8:1161-->3<!--/v8--> | <!--v8:1162-->1<!--/v8--> |
| HP-8 | BOCPD | ts-auth-service / delay | <!--v8:1163-->2<!--/v8--> / <!--v8:1164-->3<!--/v8--> / <!--v8:1165-->3<!--/v8--> | <!--v8:1166-->0<!--/v8--> |
| HP-8 | BOCPD | ts-order-service / disk | <!--v8:1167-->3<!--/v8--> / <!--v8:1168-->3<!--/v8--> / <!--v8:1169-->3<!--/v8--> | <!--v8:1170-->0<!--/v8--> |
| HP-8 | BOCPD | ts-order-service / loss | <!--v8:1171-->2<!--/v8--> / <!--v8:1172-->2<!--/v8--> / <!--v8:1173-->3<!--/v8--> | <!--v8:1174-->1<!--/v8--> |
| HP-8 | BOCPD | ts-route-service / mem | <!--v8:1175-->1<!--/v8--> / <!--v8:1176-->3<!--/v8--> / <!--v8:1177-->3<!--/v8--> | <!--v8:1178-->0<!--/v8--> |
| HP-8 | BOCPD | ts-route-service / socket | <!--v8:1179-->2<!--/v8--> / <!--v8:1180-->3<!--/v8--> / <!--v8:1181-->3<!--/v8--> | <!--v8:1182-->0<!--/v8--> |
| HP-8 | BOCPD | ts-train-service / cpu | <!--v8:1183-->1<!--/v8--> / <!--v8:1184-->2<!--/v8--> / <!--v8:1185-->3<!--/v8--> | <!--v8:1186-->1<!--/v8--> |
| HP-8 | BOCPD | ts-train-service / delay | <!--v8:1187-->3<!--/v8--> / <!--v8:1188-->3<!--/v8--> / <!--v8:1189-->3<!--/v8--> | <!--v8:1190-->0<!--/v8--> |
| HP-8 | BOCPD | ts-travel-service / disk | <!--v8:1191-->2<!--/v8--> / <!--v8:1192-->3<!--/v8--> / <!--v8:1193-->3<!--/v8--> | <!--v8:1194-->0<!--/v8--> |
| HP-8 | BOCPD | ts-travel-service / loss | <!--v8:1195-->2<!--/v8--> / <!--v8:1196-->3<!--/v8--> / <!--v8:1197-->3<!--/v8--> | <!--v8:1198-->0<!--/v8--> |

| HP / Bộ | Ô | Số ca / tổng và ý nghĩa |
|---|---|---|
| HP-9 / BOCPD | ts-auth-service / cpu | <!--v8:1199-->1<!--/v8-->/<!--v8:1200-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-auth-service / delay | <!--v8:1201-->0<!--/v8-->/<!--v8:1202-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-order-service / disk | <!--v8:1203-->0<!--/v8-->/<!--v8:1204-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-order-service / loss | <!--v8:1205-->1<!--/v8-->/<!--v8:1206-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-route-service / mem | <!--v8:1207-->2<!--/v8-->/<!--v8:1208-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-route-service / socket | <!--v8:1209-->0<!--/v8-->/<!--v8:1210-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-train-service / cpu | <!--v8:1211-->2<!--/v8-->/<!--v8:1212-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-train-service / delay | <!--v8:1213-->0<!--/v8-->/<!--v8:1214-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-travel-service / disk | <!--v8:1215-->1<!--/v8-->/<!--v8:1216-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / BOCPD | ts-travel-service / loss | <!--v8:1217-->1<!--/v8-->/<!--v8:1218-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-auth-service / cpu | <!--v8:1219-->0<!--/v8-->/<!--v8:1220-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-auth-service / delay | <!--v8:1221-->0<!--/v8-->/<!--v8:1222-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-order-service / disk | <!--v8:1223-->0<!--/v8-->/<!--v8:1224-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-order-service / loss | <!--v8:1225-->0<!--/v8-->/<!--v8:1226-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-route-service / mem | <!--v8:1227-->0<!--/v8-->/<!--v8:1228-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-route-service / socket | <!--v8:1229-->0<!--/v8-->/<!--v8:1230-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-train-service / cpu | <!--v8:1231-->0<!--/v8-->/<!--v8:1232-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-train-service / delay | <!--v8:1233-->0<!--/v8-->/<!--v8:1234-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-travel-service / disk | <!--v8:1235-->0<!--/v8-->/<!--v8:1236-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma chính | ts-travel-service / loss | <!--v8:1237-->0<!--/v8-->/<!--v8:1238-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:1239-->0<!--/v8-->/<!--v8:1240-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-auth-service / delay | <!--v8:1241-->0<!--/v8-->/<!--v8:1242-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-order-service / disk | <!--v8:1243-->0<!--/v8-->/<!--v8:1244-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-order-service / loss | <!--v8:1245-->0<!--/v8-->/<!--v8:1246-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-route-service / mem | <!--v8:1247-->0<!--/v8-->/<!--v8:1248-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-route-service / socket | <!--v8:1249-->0<!--/v8-->/<!--v8:1250-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-train-service / cpu | <!--v8:1251-->0<!--/v8-->/<!--v8:1252-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-train-service / delay | <!--v8:1253-->0<!--/v8-->/<!--v8:1254-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-travel-service / disk | <!--v8:1255-->0<!--/v8-->/<!--v8:1256-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-9 / N-Sigma đối chứng | ts-travel-service / loss | <!--v8:1257-->0<!--/v8-->/<!--v8:1258-->3<!--/v8--> D0; xem nhóm S/E từng ca |
| HP-10 / BOCPD | ts-auth-service / cpu | <!--v8:1259-->3<!--/v8-->/<!--v8:1260-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-auth-service / delay | <!--v8:1261-->3<!--/v8-->/<!--v8:1262-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-order-service / disk | <!--v8:1263-->3<!--/v8-->/<!--v8:1264-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-order-service / loss | <!--v8:1265-->3<!--/v8-->/<!--v8:1266-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-route-service / mem | <!--v8:1267-->3<!--/v8-->/<!--v8:1268-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-route-service / socket | <!--v8:1269-->3<!--/v8-->/<!--v8:1270-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-train-service / cpu | <!--v8:1271-->3<!--/v8-->/<!--v8:1272-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-train-service / delay | <!--v8:1273-->3<!--/v8-->/<!--v8:1274-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-travel-service / disk | <!--v8:1275-->3<!--/v8-->/<!--v8:1276-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / BOCPD | ts-travel-service / loss | <!--v8:1277-->3<!--/v8-->/<!--v8:1278-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-auth-service / cpu | <!--v8:1279-->3<!--/v8-->/<!--v8:1280-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-auth-service / delay | <!--v8:1281-->3<!--/v8-->/<!--v8:1282-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-order-service / disk | <!--v8:1283-->3<!--/v8-->/<!--v8:1284-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-order-service / loss | <!--v8:1285-->3<!--/v8-->/<!--v8:1286-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-route-service / mem | <!--v8:1287-->3<!--/v8-->/<!--v8:1288-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-route-service / socket | <!--v8:1289-->3<!--/v8-->/<!--v8:1290-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-train-service / cpu | <!--v8:1291-->3<!--/v8-->/<!--v8:1292-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-train-service / delay | <!--v8:1293-->3<!--/v8-->/<!--v8:1294-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-travel-service / disk | <!--v8:1295-->3<!--/v8-->/<!--v8:1296-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma chính | ts-travel-service / loss | <!--v8:1297-->3<!--/v8-->/<!--v8:1298-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:1299-->3<!--/v8-->/<!--v8:1300-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-auth-service / delay | <!--v8:1301-->3<!--/v8-->/<!--v8:1302-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-order-service / disk | <!--v8:1303-->3<!--/v8-->/<!--v8:1304-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-order-service / loss | <!--v8:1305-->3<!--/v8-->/<!--v8:1306-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-route-service / mem | <!--v8:1307-->3<!--/v8-->/<!--v8:1308-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-route-service / socket | <!--v8:1309-->3<!--/v8-->/<!--v8:1310-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-train-service / cpu | <!--v8:1311-->3<!--/v8-->/<!--v8:1312-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-train-service / delay | <!--v8:1313-->3<!--/v8-->/<!--v8:1314-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-travel-service / disk | <!--v8:1315-->3<!--/v8-->/<!--v8:1316-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-10 / N-Sigma đối chứng | ts-travel-service / loss | <!--v8:1317-->3<!--/v8-->/<!--v8:1318-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-auth-service / cpu | <!--v8:1319-->3<!--/v8-->/<!--v8:1320-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-auth-service / delay | <!--v8:1321-->3<!--/v8-->/<!--v8:1322-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-order-service / disk | <!--v8:1323-->3<!--/v8-->/<!--v8:1324-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-order-service / loss | <!--v8:1325-->3<!--/v8-->/<!--v8:1326-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-route-service / mem | <!--v8:1327-->3<!--/v8-->/<!--v8:1328-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-route-service / socket | <!--v8:1329-->3<!--/v8-->/<!--v8:1330-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-train-service / cpu | <!--v8:1331-->3<!--/v8-->/<!--v8:1332-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-train-service / delay | <!--v8:1333-->3<!--/v8-->/<!--v8:1334-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-travel-service / disk | <!--v8:1335-->3<!--/v8-->/<!--v8:1336-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / BOCPD | ts-travel-service / loss | <!--v8:1337-->3<!--/v8-->/<!--v8:1338-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-auth-service / cpu | <!--v8:1339-->3<!--/v8-->/<!--v8:1340-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-auth-service / delay | <!--v8:1341-->3<!--/v8-->/<!--v8:1342-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-order-service / disk | <!--v8:1343-->3<!--/v8-->/<!--v8:1344-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-order-service / loss | <!--v8:1345-->3<!--/v8-->/<!--v8:1346-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-route-service / mem | <!--v8:1347-->3<!--/v8-->/<!--v8:1348-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-route-service / socket | <!--v8:1349-->3<!--/v8-->/<!--v8:1350-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-train-service / cpu | <!--v8:1351-->3<!--/v8-->/<!--v8:1352-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-train-service / delay | <!--v8:1353-->3<!--/v8-->/<!--v8:1354-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-travel-service / disk | <!--v8:1355-->3<!--/v8-->/<!--v8:1356-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-11 / N-Sigma chính | ts-travel-service / loss | <!--v8:1357-->3<!--/v8-->/<!--v8:1358-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-auth-service / cpu | <!--v8:1359-->3<!--/v8-->/<!--v8:1360-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-auth-service / delay | <!--v8:1361-->3<!--/v8-->/<!--v8:1362-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-order-service / disk | <!--v8:1363-->3<!--/v8-->/<!--v8:1364-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-order-service / loss | <!--v8:1365-->3<!--/v8-->/<!--v8:1366-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-route-service / mem | <!--v8:1367-->3<!--/v8-->/<!--v8:1368-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-route-service / socket | <!--v8:1369-->3<!--/v8-->/<!--v8:1370-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-train-service / cpu | <!--v8:1371-->3<!--/v8-->/<!--v8:1372-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-train-service / delay | <!--v8:1373-->3<!--/v8-->/<!--v8:1374-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-travel-service / disk | <!--v8:1375-->3<!--/v8-->/<!--v8:1376-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-12 / BOCPD | ts-travel-service / loss | <!--v8:1377-->3<!--/v8-->/<!--v8:1378-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-auth-service / cpu | <!--v8:1379-->3<!--/v8-->/<!--v8:1380-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-auth-service / delay | <!--v8:1381-->3<!--/v8-->/<!--v8:1382-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-order-service / disk | <!--v8:1383-->3<!--/v8-->/<!--v8:1384-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-order-service / loss | <!--v8:1385-->3<!--/v8-->/<!--v8:1386-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-route-service / mem | <!--v8:1387-->3<!--/v8-->/<!--v8:1388-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-route-service / socket | <!--v8:1389-->3<!--/v8-->/<!--v8:1390-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-train-service / cpu | <!--v8:1391-->3<!--/v8-->/<!--v8:1392-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-train-service / delay | <!--v8:1393-->3<!--/v8-->/<!--v8:1394-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-travel-service / disk | <!--v8:1395-->3<!--/v8-->/<!--v8:1396-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / BOCPD | ts-travel-service / loss | <!--v8:1397-->3<!--/v8-->/<!--v8:1398-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-auth-service / cpu | <!--v8:1399-->3<!--/v8-->/<!--v8:1400-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-auth-service / delay | <!--v8:1401-->3<!--/v8-->/<!--v8:1402-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-order-service / disk | <!--v8:1403-->3<!--/v8-->/<!--v8:1404-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-order-service / loss | <!--v8:1405-->3<!--/v8-->/<!--v8:1406-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-route-service / mem | <!--v8:1407-->3<!--/v8-->/<!--v8:1408-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-route-service / socket | <!--v8:1409-->3<!--/v8-->/<!--v8:1410-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-train-service / cpu | <!--v8:1411-->3<!--/v8-->/<!--v8:1412-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-train-service / delay | <!--v8:1413-->3<!--/v8-->/<!--v8:1414-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-travel-service / disk | <!--v8:1415-->3<!--/v8-->/<!--v8:1416-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma chính | ts-travel-service / loss | <!--v8:1417-->3<!--/v8-->/<!--v8:1418-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:1419-->3<!--/v8-->/<!--v8:1420-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-auth-service / delay | <!--v8:1421-->3<!--/v8-->/<!--v8:1422-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-order-service / disk | <!--v8:1423-->3<!--/v8-->/<!--v8:1424-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-order-service / loss | <!--v8:1425-->3<!--/v8-->/<!--v8:1426-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-route-service / mem | <!--v8:1427-->3<!--/v8-->/<!--v8:1428-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-route-service / socket | <!--v8:1429-->3<!--/v8-->/<!--v8:1430-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-train-service / cpu | <!--v8:1431-->3<!--/v8-->/<!--v8:1432-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-train-service / delay | <!--v8:1433-->3<!--/v8-->/<!--v8:1434-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-travel-service / disk | <!--v8:1435-->3<!--/v8-->/<!--v8:1436-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-13 / N-Sigma đối chứng | ts-travel-service / loss | <!--v8:1437-->3<!--/v8-->/<!--v8:1438-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-auth-service / cpu | <!--v8:1439-->3<!--/v8-->/<!--v8:1440-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-auth-service / delay | <!--v8:1441-->3<!--/v8-->/<!--v8:1442-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-order-service / disk | <!--v8:1443-->3<!--/v8-->/<!--v8:1444-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-order-service / loss | <!--v8:1445-->3<!--/v8-->/<!--v8:1446-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-route-service / mem | <!--v8:1447-->3<!--/v8-->/<!--v8:1448-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-route-service / socket | <!--v8:1449-->3<!--/v8-->/<!--v8:1450-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-train-service / cpu | <!--v8:1451-->3<!--/v8-->/<!--v8:1452-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-train-service / delay | <!--v8:1453-->3<!--/v8-->/<!--v8:1454-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-travel-service / disk | <!--v8:1455-->3<!--/v8-->/<!--v8:1456-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma chính | ts-travel-service / loss | <!--v8:1457-->3<!--/v8-->/<!--v8:1458-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-auth-service / cpu | <!--v8:1459-->3<!--/v8-->/<!--v8:1460-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-auth-service / delay | <!--v8:1461-->3<!--/v8-->/<!--v8:1462-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-order-service / disk | <!--v8:1463-->3<!--/v8-->/<!--v8:1464-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-order-service / loss | <!--v8:1465-->3<!--/v8-->/<!--v8:1466-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-route-service / mem | <!--v8:1467-->3<!--/v8-->/<!--v8:1468-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-route-service / socket | <!--v8:1469-->3<!--/v8-->/<!--v8:1470-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-train-service / cpu | <!--v8:1471-->3<!--/v8-->/<!--v8:1472-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-train-service / delay | <!--v8:1473-->3<!--/v8-->/<!--v8:1474-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-travel-service / disk | <!--v8:1475-->3<!--/v8-->/<!--v8:1476-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |
| HP-14 / N-Sigma đối chứng | ts-travel-service / loss | <!--v8:1477-->3<!--/v8-->/<!--v8:1478-->3<!--/v8--> phạm vi khảo sát; không đếm tất cả là ca hỏng |

### Độ nhạy cờ (mọi cấu hình đã khai)

Nguồn: `theo-ca.json#/per_detector/<bộ>/cell/<ô>/flags`. N1/N2/N3 có thể đổi tập ca; B2 đổi theo dung sai; B3 N/A khi B2 đúng; B4 đổi cả ngưỡng và miền theo w. Không chọn cấu hình có số thuận hơn. Bảng dưới giữ đủ đúng/hợp lệ/tổng và N/A theo từng ô.

| Bộ | Ô | Cờ / cấu hình | Đúng / hợp lệ / tổng | N/A |
|---|---|---|---|---|
| BOCPD | ts-auth-service / cpu | B1 | <!--v8:1479-->0<!--/v8-->/<!--v8:1480-->2<!--/v8-->/<!--v8:1481-->3<!--/v8--> | <!--v8:1482-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B2/2 | <!--v8:1483-->2<!--/v8-->/<!--v8:1484-->2<!--/v8-->/<!--v8:1485-->3<!--/v8--> | <!--v8:1486-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B2/5 | <!--v8:1487-->2<!--/v8-->/<!--v8:1488-->2<!--/v8-->/<!--v8:1489-->3<!--/v8--> | <!--v8:1490-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B2/10 | <!--v8:1491-->2<!--/v8-->/<!--v8:1492-->2<!--/v8-->/<!--v8:1493-->3<!--/v8--> | <!--v8:1494-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B3/2 | <!--v8:1495-->0<!--/v8-->/<!--v8:1496-->0<!--/v8-->/<!--v8:1497-->3<!--/v8--> | <!--v8:1498-->3<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B3/5 | <!--v8:1499-->0<!--/v8-->/<!--v8:1500-->0<!--/v8-->/<!--v8:1501-->3<!--/v8--> | <!--v8:1502-->3<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B3/10 | <!--v8:1503-->0<!--/v8-->/<!--v8:1504-->0<!--/v8-->/<!--v8:1505-->3<!--/v8--> | <!--v8:1506-->3<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w15/k2 | <!--v8:1507-->1<!--/v8-->/<!--v8:1508-->2<!--/v8-->/<!--v8:1509-->3<!--/v8--> | <!--v8:1510-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w15/k3 | <!--v8:1511-->1<!--/v8-->/<!--v8:1512-->2<!--/v8-->/<!--v8:1513-->3<!--/v8--> | <!--v8:1514-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w15/k5 | <!--v8:1515-->0<!--/v8-->/<!--v8:1516-->2<!--/v8-->/<!--v8:1517-->3<!--/v8--> | <!--v8:1518-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w30/k2 | <!--v8:1519-->2<!--/v8-->/<!--v8:1520-->2<!--/v8-->/<!--v8:1521-->3<!--/v8--> | <!--v8:1522-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w30/k3 | <!--v8:1523-->2<!--/v8-->/<!--v8:1524-->2<!--/v8-->/<!--v8:1525-->3<!--/v8--> | <!--v8:1526-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w30/k5 | <!--v8:1527-->1<!--/v8-->/<!--v8:1528-->2<!--/v8-->/<!--v8:1529-->3<!--/v8--> | <!--v8:1530-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w60/k2 | <!--v8:1531-->2<!--/v8-->/<!--v8:1532-->2<!--/v8-->/<!--v8:1533-->3<!--/v8--> | <!--v8:1534-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w60/k3 | <!--v8:1535-->2<!--/v8-->/<!--v8:1536-->2<!--/v8-->/<!--v8:1537-->3<!--/v8--> | <!--v8:1538-->1<!--/v8--> |
| BOCPD | ts-auth-service / cpu | B4/w60/k5 | <!--v8:1539-->1<!--/v8-->/<!--v8:1540-->2<!--/v8-->/<!--v8:1541-->3<!--/v8--> | <!--v8:1542-->1<!--/v8--> |
| BOCPD | ts-auth-service / delay | B1 | <!--v8:1543-->0<!--/v8-->/<!--v8:1544-->3<!--/v8-->/<!--v8:1545-->3<!--/v8--> | <!--v8:1546-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B2/2 | <!--v8:1547-->2<!--/v8-->/<!--v8:1548-->3<!--/v8-->/<!--v8:1549-->3<!--/v8--> | <!--v8:1550-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B2/5 | <!--v8:1551-->2<!--/v8-->/<!--v8:1552-->3<!--/v8-->/<!--v8:1553-->3<!--/v8--> | <!--v8:1554-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B2/10 | <!--v8:1555-->1<!--/v8-->/<!--v8:1556-->3<!--/v8-->/<!--v8:1557-->3<!--/v8--> | <!--v8:1558-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B3/2 | <!--v8:1559-->0<!--/v8-->/<!--v8:1560-->1<!--/v8-->/<!--v8:1561-->3<!--/v8--> | <!--v8:1562-->2<!--/v8--> |
| BOCPD | ts-auth-service / delay | B3/5 | <!--v8:1563-->0<!--/v8-->/<!--v8:1564-->1<!--/v8-->/<!--v8:1565-->3<!--/v8--> | <!--v8:1566-->2<!--/v8--> |
| BOCPD | ts-auth-service / delay | B3/10 | <!--v8:1567-->0<!--/v8-->/<!--v8:1568-->2<!--/v8-->/<!--v8:1569-->3<!--/v8--> | <!--v8:1570-->1<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w15/k2 | <!--v8:1571-->3<!--/v8-->/<!--v8:1572-->3<!--/v8-->/<!--v8:1573-->3<!--/v8--> | <!--v8:1574-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w15/k3 | <!--v8:1575-->2<!--/v8-->/<!--v8:1576-->3<!--/v8-->/<!--v8:1577-->3<!--/v8--> | <!--v8:1578-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w15/k5 | <!--v8:1579-->1<!--/v8-->/<!--v8:1580-->3<!--/v8-->/<!--v8:1581-->3<!--/v8--> | <!--v8:1582-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w30/k2 | <!--v8:1583-->3<!--/v8-->/<!--v8:1584-->3<!--/v8-->/<!--v8:1585-->3<!--/v8--> | <!--v8:1586-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w30/k3 | <!--v8:1587-->2<!--/v8-->/<!--v8:1588-->3<!--/v8-->/<!--v8:1589-->3<!--/v8--> | <!--v8:1590-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w30/k5 | <!--v8:1591-->2<!--/v8-->/<!--v8:1592-->3<!--/v8-->/<!--v8:1593-->3<!--/v8--> | <!--v8:1594-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w60/k2 | <!--v8:1595-->3<!--/v8-->/<!--v8:1596-->3<!--/v8-->/<!--v8:1597-->3<!--/v8--> | <!--v8:1598-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w60/k3 | <!--v8:1599-->2<!--/v8-->/<!--v8:1600-->3<!--/v8-->/<!--v8:1601-->3<!--/v8--> | <!--v8:1602-->0<!--/v8--> |
| BOCPD | ts-auth-service / delay | B4/w60/k5 | <!--v8:1603-->2<!--/v8-->/<!--v8:1604-->3<!--/v8-->/<!--v8:1605-->3<!--/v8--> | <!--v8:1606-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B1 | <!--v8:1607-->0<!--/v8-->/<!--v8:1608-->3<!--/v8-->/<!--v8:1609-->3<!--/v8--> | <!--v8:1610-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B2/2 | <!--v8:1611-->3<!--/v8-->/<!--v8:1612-->3<!--/v8-->/<!--v8:1613-->3<!--/v8--> | <!--v8:1614-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B2/5 | <!--v8:1615-->3<!--/v8-->/<!--v8:1616-->3<!--/v8-->/<!--v8:1617-->3<!--/v8--> | <!--v8:1618-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B2/10 | <!--v8:1619-->3<!--/v8-->/<!--v8:1620-->3<!--/v8-->/<!--v8:1621-->3<!--/v8--> | <!--v8:1622-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B3/2 | <!--v8:1623-->0<!--/v8-->/<!--v8:1624-->0<!--/v8-->/<!--v8:1625-->3<!--/v8--> | <!--v8:1626-->3<!--/v8--> |
| BOCPD | ts-order-service / disk | B3/5 | <!--v8:1627-->0<!--/v8-->/<!--v8:1628-->0<!--/v8-->/<!--v8:1629-->3<!--/v8--> | <!--v8:1630-->3<!--/v8--> |
| BOCPD | ts-order-service / disk | B3/10 | <!--v8:1631-->0<!--/v8-->/<!--v8:1632-->0<!--/v8-->/<!--v8:1633-->3<!--/v8--> | <!--v8:1634-->3<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w15/k2 | <!--v8:1635-->3<!--/v8-->/<!--v8:1636-->3<!--/v8-->/<!--v8:1637-->3<!--/v8--> | <!--v8:1638-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w15/k3 | <!--v8:1639-->1<!--/v8-->/<!--v8:1640-->3<!--/v8-->/<!--v8:1641-->3<!--/v8--> | <!--v8:1642-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w15/k5 | <!--v8:1643-->1<!--/v8-->/<!--v8:1644-->3<!--/v8-->/<!--v8:1645-->3<!--/v8--> | <!--v8:1646-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w30/k2 | <!--v8:1647-->3<!--/v8-->/<!--v8:1648-->3<!--/v8-->/<!--v8:1649-->3<!--/v8--> | <!--v8:1650-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w30/k3 | <!--v8:1651-->3<!--/v8-->/<!--v8:1652-->3<!--/v8-->/<!--v8:1653-->3<!--/v8--> | <!--v8:1654-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w30/k5 | <!--v8:1655-->1<!--/v8-->/<!--v8:1656-->3<!--/v8-->/<!--v8:1657-->3<!--/v8--> | <!--v8:1658-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w60/k2 | <!--v8:1659-->3<!--/v8-->/<!--v8:1660-->3<!--/v8-->/<!--v8:1661-->3<!--/v8--> | <!--v8:1662-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w60/k3 | <!--v8:1663-->3<!--/v8-->/<!--v8:1664-->3<!--/v8-->/<!--v8:1665-->3<!--/v8--> | <!--v8:1666-->0<!--/v8--> |
| BOCPD | ts-order-service / disk | B4/w60/k5 | <!--v8:1667-->3<!--/v8-->/<!--v8:1668-->3<!--/v8-->/<!--v8:1669-->3<!--/v8--> | <!--v8:1670-->0<!--/v8--> |
| BOCPD | ts-order-service / loss | B1 | <!--v8:1671-->0<!--/v8-->/<!--v8:1672-->2<!--/v8-->/<!--v8:1673-->3<!--/v8--> | <!--v8:1674-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B2/2 | <!--v8:1675-->2<!--/v8-->/<!--v8:1676-->2<!--/v8-->/<!--v8:1677-->3<!--/v8--> | <!--v8:1678-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B2/5 | <!--v8:1679-->2<!--/v8-->/<!--v8:1680-->2<!--/v8-->/<!--v8:1681-->3<!--/v8--> | <!--v8:1682-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B2/10 | <!--v8:1683-->2<!--/v8-->/<!--v8:1684-->2<!--/v8-->/<!--v8:1685-->3<!--/v8--> | <!--v8:1686-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B3/2 | <!--v8:1687-->0<!--/v8-->/<!--v8:1688-->0<!--/v8-->/<!--v8:1689-->3<!--/v8--> | <!--v8:1690-->3<!--/v8--> |
| BOCPD | ts-order-service / loss | B3/5 | <!--v8:1691-->0<!--/v8-->/<!--v8:1692-->0<!--/v8-->/<!--v8:1693-->3<!--/v8--> | <!--v8:1694-->3<!--/v8--> |
| BOCPD | ts-order-service / loss | B3/10 | <!--v8:1695-->0<!--/v8-->/<!--v8:1696-->0<!--/v8-->/<!--v8:1697-->3<!--/v8--> | <!--v8:1698-->3<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w15/k2 | <!--v8:1699-->2<!--/v8-->/<!--v8:1700-->2<!--/v8-->/<!--v8:1701-->3<!--/v8--> | <!--v8:1702-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w15/k3 | <!--v8:1703-->1<!--/v8-->/<!--v8:1704-->2<!--/v8-->/<!--v8:1705-->3<!--/v8--> | <!--v8:1706-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w15/k5 | <!--v8:1707-->0<!--/v8-->/<!--v8:1708-->2<!--/v8-->/<!--v8:1709-->3<!--/v8--> | <!--v8:1710-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w30/k2 | <!--v8:1711-->2<!--/v8-->/<!--v8:1712-->2<!--/v8-->/<!--v8:1713-->3<!--/v8--> | <!--v8:1714-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w30/k3 | <!--v8:1715-->2<!--/v8-->/<!--v8:1716-->2<!--/v8-->/<!--v8:1717-->3<!--/v8--> | <!--v8:1718-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w30/k5 | <!--v8:1719-->0<!--/v8-->/<!--v8:1720-->2<!--/v8-->/<!--v8:1721-->3<!--/v8--> | <!--v8:1722-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w60/k2 | <!--v8:1723-->2<!--/v8-->/<!--v8:1724-->2<!--/v8-->/<!--v8:1725-->3<!--/v8--> | <!--v8:1726-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w60/k3 | <!--v8:1727-->1<!--/v8-->/<!--v8:1728-->2<!--/v8-->/<!--v8:1729-->3<!--/v8--> | <!--v8:1730-->1<!--/v8--> |
| BOCPD | ts-order-service / loss | B4/w60/k5 | <!--v8:1731-->0<!--/v8-->/<!--v8:1732-->2<!--/v8-->/<!--v8:1733-->3<!--/v8--> | <!--v8:1734-->1<!--/v8--> |
| BOCPD | ts-route-service / mem | B1 | <!--v8:1735-->0<!--/v8-->/<!--v8:1736-->3<!--/v8-->/<!--v8:1737-->3<!--/v8--> | <!--v8:1738-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B2/2 | <!--v8:1739-->1<!--/v8-->/<!--v8:1740-->3<!--/v8-->/<!--v8:1741-->3<!--/v8--> | <!--v8:1742-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B2/5 | <!--v8:1743-->1<!--/v8-->/<!--v8:1744-->3<!--/v8-->/<!--v8:1745-->3<!--/v8--> | <!--v8:1746-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B2/10 | <!--v8:1747-->1<!--/v8-->/<!--v8:1748-->3<!--/v8-->/<!--v8:1749-->3<!--/v8--> | <!--v8:1750-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B3/2 | <!--v8:1751-->0<!--/v8-->/<!--v8:1752-->2<!--/v8-->/<!--v8:1753-->3<!--/v8--> | <!--v8:1754-->1<!--/v8--> |
| BOCPD | ts-route-service / mem | B3/5 | <!--v8:1755-->0<!--/v8-->/<!--v8:1756-->2<!--/v8-->/<!--v8:1757-->3<!--/v8--> | <!--v8:1758-->1<!--/v8--> |
| BOCPD | ts-route-service / mem | B3/10 | <!--v8:1759-->0<!--/v8-->/<!--v8:1760-->2<!--/v8-->/<!--v8:1761-->3<!--/v8--> | <!--v8:1762-->1<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w15/k2 | <!--v8:1763-->1<!--/v8-->/<!--v8:1764-->3<!--/v8-->/<!--v8:1765-->3<!--/v8--> | <!--v8:1766-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w15/k3 | <!--v8:1767-->1<!--/v8-->/<!--v8:1768-->3<!--/v8-->/<!--v8:1769-->3<!--/v8--> | <!--v8:1770-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w15/k5 | <!--v8:1771-->1<!--/v8-->/<!--v8:1772-->3<!--/v8-->/<!--v8:1773-->3<!--/v8--> | <!--v8:1774-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w30/k2 | <!--v8:1775-->3<!--/v8-->/<!--v8:1776-->3<!--/v8-->/<!--v8:1777-->3<!--/v8--> | <!--v8:1778-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w30/k3 | <!--v8:1779-->1<!--/v8-->/<!--v8:1780-->3<!--/v8-->/<!--v8:1781-->3<!--/v8--> | <!--v8:1782-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w30/k5 | <!--v8:1783-->1<!--/v8-->/<!--v8:1784-->3<!--/v8-->/<!--v8:1785-->3<!--/v8--> | <!--v8:1786-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w60/k2 | <!--v8:1787-->2<!--/v8-->/<!--v8:1788-->3<!--/v8-->/<!--v8:1789-->3<!--/v8--> | <!--v8:1790-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w60/k3 | <!--v8:1791-->2<!--/v8-->/<!--v8:1792-->3<!--/v8-->/<!--v8:1793-->3<!--/v8--> | <!--v8:1794-->0<!--/v8--> |
| BOCPD | ts-route-service / mem | B4/w60/k5 | <!--v8:1795-->1<!--/v8-->/<!--v8:1796-->3<!--/v8-->/<!--v8:1797-->3<!--/v8--> | <!--v8:1798-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B1 | <!--v8:1799-->0<!--/v8-->/<!--v8:1800-->3<!--/v8-->/<!--v8:1801-->3<!--/v8--> | <!--v8:1802-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B2/2 | <!--v8:1803-->3<!--/v8-->/<!--v8:1804-->3<!--/v8-->/<!--v8:1805-->3<!--/v8--> | <!--v8:1806-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B2/5 | <!--v8:1807-->2<!--/v8-->/<!--v8:1808-->3<!--/v8-->/<!--v8:1809-->3<!--/v8--> | <!--v8:1810-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B2/10 | <!--v8:1811-->1<!--/v8-->/<!--v8:1812-->3<!--/v8-->/<!--v8:1813-->3<!--/v8--> | <!--v8:1814-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B3/2 | <!--v8:1815-->0<!--/v8-->/<!--v8:1816-->0<!--/v8-->/<!--v8:1817-->3<!--/v8--> | <!--v8:1818-->3<!--/v8--> |
| BOCPD | ts-route-service / socket | B3/5 | <!--v8:1819-->0<!--/v8-->/<!--v8:1820-->1<!--/v8-->/<!--v8:1821-->3<!--/v8--> | <!--v8:1822-->2<!--/v8--> |
| BOCPD | ts-route-service / socket | B3/10 | <!--v8:1823-->0<!--/v8-->/<!--v8:1824-->2<!--/v8-->/<!--v8:1825-->3<!--/v8--> | <!--v8:1826-->1<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w15/k2 | <!--v8:1827-->2<!--/v8-->/<!--v8:1828-->3<!--/v8-->/<!--v8:1829-->3<!--/v8--> | <!--v8:1830-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w15/k3 | <!--v8:1831-->2<!--/v8-->/<!--v8:1832-->3<!--/v8-->/<!--v8:1833-->3<!--/v8--> | <!--v8:1834-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w15/k5 | <!--v8:1835-->2<!--/v8-->/<!--v8:1836-->3<!--/v8-->/<!--v8:1837-->3<!--/v8--> | <!--v8:1838-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w30/k2 | <!--v8:1839-->2<!--/v8-->/<!--v8:1840-->3<!--/v8-->/<!--v8:1841-->3<!--/v8--> | <!--v8:1842-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w30/k3 | <!--v8:1843-->2<!--/v8-->/<!--v8:1844-->3<!--/v8-->/<!--v8:1845-->3<!--/v8--> | <!--v8:1846-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w30/k5 | <!--v8:1847-->1<!--/v8-->/<!--v8:1848-->3<!--/v8-->/<!--v8:1849-->3<!--/v8--> | <!--v8:1850-->0<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w60/k2 | <!--v8:1851-->2<!--/v8-->/<!--v8:1852-->2<!--/v8-->/<!--v8:1853-->3<!--/v8--> | <!--v8:1854-->1<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w60/k3 | <!--v8:1855-->2<!--/v8-->/<!--v8:1856-->2<!--/v8-->/<!--v8:1857-->3<!--/v8--> | <!--v8:1858-->1<!--/v8--> |
| BOCPD | ts-route-service / socket | B4/w60/k5 | <!--v8:1859-->0<!--/v8-->/<!--v8:1860-->2<!--/v8-->/<!--v8:1861-->3<!--/v8--> | <!--v8:1862-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B1 | <!--v8:1863-->0<!--/v8-->/<!--v8:1864-->2<!--/v8-->/<!--v8:1865-->3<!--/v8--> | <!--v8:1866-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B2/2 | <!--v8:1867-->2<!--/v8-->/<!--v8:1868-->2<!--/v8-->/<!--v8:1869-->3<!--/v8--> | <!--v8:1870-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B2/5 | <!--v8:1871-->0<!--/v8-->/<!--v8:1872-->2<!--/v8-->/<!--v8:1873-->3<!--/v8--> | <!--v8:1874-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B2/10 | <!--v8:1875-->0<!--/v8-->/<!--v8:1876-->2<!--/v8-->/<!--v8:1877-->3<!--/v8--> | <!--v8:1878-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B3/2 | <!--v8:1879-->0<!--/v8-->/<!--v8:1880-->0<!--/v8-->/<!--v8:1881-->3<!--/v8--> | <!--v8:1882-->3<!--/v8--> |
| BOCPD | ts-train-service / cpu | B3/5 | <!--v8:1883-->0<!--/v8-->/<!--v8:1884-->2<!--/v8-->/<!--v8:1885-->3<!--/v8--> | <!--v8:1886-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B3/10 | <!--v8:1887-->0<!--/v8-->/<!--v8:1888-->2<!--/v8-->/<!--v8:1889-->3<!--/v8--> | <!--v8:1890-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w15/k2 | <!--v8:1891-->1<!--/v8-->/<!--v8:1892-->2<!--/v8-->/<!--v8:1893-->3<!--/v8--> | <!--v8:1894-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w15/k3 | <!--v8:1895-->1<!--/v8-->/<!--v8:1896-->2<!--/v8-->/<!--v8:1897-->3<!--/v8--> | <!--v8:1898-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w15/k5 | <!--v8:1899-->1<!--/v8-->/<!--v8:1900-->2<!--/v8-->/<!--v8:1901-->3<!--/v8--> | <!--v8:1902-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w30/k2 | <!--v8:1903-->1<!--/v8-->/<!--v8:1904-->2<!--/v8-->/<!--v8:1905-->3<!--/v8--> | <!--v8:1906-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w30/k3 | <!--v8:1907-->1<!--/v8-->/<!--v8:1908-->2<!--/v8-->/<!--v8:1909-->3<!--/v8--> | <!--v8:1910-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w30/k5 | <!--v8:1911-->0<!--/v8-->/<!--v8:1912-->2<!--/v8-->/<!--v8:1913-->3<!--/v8--> | <!--v8:1914-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w60/k2 | <!--v8:1915-->2<!--/v8-->/<!--v8:1916-->2<!--/v8-->/<!--v8:1917-->3<!--/v8--> | <!--v8:1918-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w60/k3 | <!--v8:1919-->1<!--/v8-->/<!--v8:1920-->2<!--/v8-->/<!--v8:1921-->3<!--/v8--> | <!--v8:1922-->1<!--/v8--> |
| BOCPD | ts-train-service / cpu | B4/w60/k5 | <!--v8:1923-->1<!--/v8-->/<!--v8:1924-->2<!--/v8-->/<!--v8:1925-->3<!--/v8--> | <!--v8:1926-->1<!--/v8--> |
| BOCPD | ts-train-service / delay | B1 | <!--v8:1927-->0<!--/v8-->/<!--v8:1928-->3<!--/v8-->/<!--v8:1929-->3<!--/v8--> | <!--v8:1930-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B2/2 | <!--v8:1931-->2<!--/v8-->/<!--v8:1932-->3<!--/v8-->/<!--v8:1933-->3<!--/v8--> | <!--v8:1934-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B2/5 | <!--v8:1935-->2<!--/v8-->/<!--v8:1936-->3<!--/v8-->/<!--v8:1937-->3<!--/v8--> | <!--v8:1938-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B2/10 | <!--v8:1939-->2<!--/v8-->/<!--v8:1940-->3<!--/v8-->/<!--v8:1941-->3<!--/v8--> | <!--v8:1942-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B3/2 | <!--v8:1943-->0<!--/v8-->/<!--v8:1944-->1<!--/v8-->/<!--v8:1945-->3<!--/v8--> | <!--v8:1946-->2<!--/v8--> |
| BOCPD | ts-train-service / delay | B3/5 | <!--v8:1947-->0<!--/v8-->/<!--v8:1948-->1<!--/v8-->/<!--v8:1949-->3<!--/v8--> | <!--v8:1950-->2<!--/v8--> |
| BOCPD | ts-train-service / delay | B3/10 | <!--v8:1951-->0<!--/v8-->/<!--v8:1952-->1<!--/v8-->/<!--v8:1953-->3<!--/v8--> | <!--v8:1954-->2<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w15/k2 | <!--v8:1955-->3<!--/v8-->/<!--v8:1956-->3<!--/v8-->/<!--v8:1957-->3<!--/v8--> | <!--v8:1958-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w15/k3 | <!--v8:1959-->2<!--/v8-->/<!--v8:1960-->3<!--/v8-->/<!--v8:1961-->3<!--/v8--> | <!--v8:1962-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w15/k5 | <!--v8:1963-->0<!--/v8-->/<!--v8:1964-->3<!--/v8-->/<!--v8:1965-->3<!--/v8--> | <!--v8:1966-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w30/k2 | <!--v8:1967-->3<!--/v8-->/<!--v8:1968-->3<!--/v8-->/<!--v8:1969-->3<!--/v8--> | <!--v8:1970-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w30/k3 | <!--v8:1971-->3<!--/v8-->/<!--v8:1972-->3<!--/v8-->/<!--v8:1973-->3<!--/v8--> | <!--v8:1974-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w30/k5 | <!--v8:1975-->2<!--/v8-->/<!--v8:1976-->3<!--/v8-->/<!--v8:1977-->3<!--/v8--> | <!--v8:1978-->0<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w60/k2 | <!--v8:1979-->2<!--/v8-->/<!--v8:1980-->2<!--/v8-->/<!--v8:1981-->3<!--/v8--> | <!--v8:1982-->1<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w60/k3 | <!--v8:1983-->2<!--/v8-->/<!--v8:1984-->2<!--/v8-->/<!--v8:1985-->3<!--/v8--> | <!--v8:1986-->1<!--/v8--> |
| BOCPD | ts-train-service / delay | B4/w60/k5 | <!--v8:1987-->1<!--/v8-->/<!--v8:1988-->2<!--/v8-->/<!--v8:1989-->3<!--/v8--> | <!--v8:1990-->1<!--/v8--> |
| BOCPD | ts-travel-service / disk | B1 | <!--v8:1991-->0<!--/v8-->/<!--v8:1992-->3<!--/v8-->/<!--v8:1993-->3<!--/v8--> | <!--v8:1994-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B2/2 | <!--v8:1995-->2<!--/v8-->/<!--v8:1996-->3<!--/v8-->/<!--v8:1997-->3<!--/v8--> | <!--v8:1998-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B2/5 | <!--v8:1999-->2<!--/v8-->/<!--v8:2000-->3<!--/v8-->/<!--v8:2001-->3<!--/v8--> | <!--v8:2002-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B2/10 | <!--v8:2003-->2<!--/v8-->/<!--v8:2004-->3<!--/v8-->/<!--v8:2005-->3<!--/v8--> | <!--v8:2006-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B3/2 | <!--v8:2007-->0<!--/v8-->/<!--v8:2008-->1<!--/v8-->/<!--v8:2009-->3<!--/v8--> | <!--v8:2010-->2<!--/v8--> |
| BOCPD | ts-travel-service / disk | B3/5 | <!--v8:2011-->0<!--/v8-->/<!--v8:2012-->1<!--/v8-->/<!--v8:2013-->3<!--/v8--> | <!--v8:2014-->2<!--/v8--> |
| BOCPD | ts-travel-service / disk | B3/10 | <!--v8:2015-->0<!--/v8-->/<!--v8:2016-->1<!--/v8-->/<!--v8:2017-->3<!--/v8--> | <!--v8:2018-->2<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w15/k2 | <!--v8:2019-->2<!--/v8-->/<!--v8:2020-->3<!--/v8-->/<!--v8:2021-->3<!--/v8--> | <!--v8:2022-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w15/k3 | <!--v8:2023-->2<!--/v8-->/<!--v8:2024-->3<!--/v8-->/<!--v8:2025-->3<!--/v8--> | <!--v8:2026-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w15/k5 | <!--v8:2027-->2<!--/v8-->/<!--v8:2028-->3<!--/v8-->/<!--v8:2029-->3<!--/v8--> | <!--v8:2030-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w30/k2 | <!--v8:2031-->2<!--/v8-->/<!--v8:2032-->3<!--/v8-->/<!--v8:2033-->3<!--/v8--> | <!--v8:2034-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w30/k3 | <!--v8:2035-->2<!--/v8-->/<!--v8:2036-->3<!--/v8-->/<!--v8:2037-->3<!--/v8--> | <!--v8:2038-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w30/k5 | <!--v8:2039-->1<!--/v8-->/<!--v8:2040-->3<!--/v8-->/<!--v8:2041-->3<!--/v8--> | <!--v8:2042-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w60/k2 | <!--v8:2043-->3<!--/v8-->/<!--v8:2044-->3<!--/v8-->/<!--v8:2045-->3<!--/v8--> | <!--v8:2046-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w60/k3 | <!--v8:2047-->3<!--/v8-->/<!--v8:2048-->3<!--/v8-->/<!--v8:2049-->3<!--/v8--> | <!--v8:2050-->0<!--/v8--> |
| BOCPD | ts-travel-service / disk | B4/w60/k5 | <!--v8:2051-->2<!--/v8-->/<!--v8:2052-->3<!--/v8-->/<!--v8:2053-->3<!--/v8--> | <!--v8:2054-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B1 | <!--v8:2055-->0<!--/v8-->/<!--v8:2056-->3<!--/v8-->/<!--v8:2057-->3<!--/v8--> | <!--v8:2058-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B2/2 | <!--v8:2059-->1<!--/v8-->/<!--v8:2060-->3<!--/v8-->/<!--v8:2061-->3<!--/v8--> | <!--v8:2062-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B2/5 | <!--v8:2063-->1<!--/v8-->/<!--v8:2064-->3<!--/v8-->/<!--v8:2065-->3<!--/v8--> | <!--v8:2066-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B2/10 | <!--v8:2067-->1<!--/v8-->/<!--v8:2068-->3<!--/v8-->/<!--v8:2069-->3<!--/v8--> | <!--v8:2070-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B3/2 | <!--v8:2071-->0<!--/v8-->/<!--v8:2072-->2<!--/v8-->/<!--v8:2073-->3<!--/v8--> | <!--v8:2074-->1<!--/v8--> |
| BOCPD | ts-travel-service / loss | B3/5 | <!--v8:2075-->0<!--/v8-->/<!--v8:2076-->2<!--/v8-->/<!--v8:2077-->3<!--/v8--> | <!--v8:2078-->1<!--/v8--> |
| BOCPD | ts-travel-service / loss | B3/10 | <!--v8:2079-->0<!--/v8-->/<!--v8:2080-->2<!--/v8-->/<!--v8:2081-->3<!--/v8--> | <!--v8:2082-->1<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w15/k2 | <!--v8:2083-->2<!--/v8-->/<!--v8:2084-->3<!--/v8-->/<!--v8:2085-->3<!--/v8--> | <!--v8:2086-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w15/k3 | <!--v8:2087-->1<!--/v8-->/<!--v8:2088-->3<!--/v8-->/<!--v8:2089-->3<!--/v8--> | <!--v8:2090-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w15/k5 | <!--v8:2091-->0<!--/v8-->/<!--v8:2092-->3<!--/v8-->/<!--v8:2093-->3<!--/v8--> | <!--v8:2094-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w30/k2 | <!--v8:2095-->3<!--/v8-->/<!--v8:2096-->3<!--/v8-->/<!--v8:2097-->3<!--/v8--> | <!--v8:2098-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w30/k3 | <!--v8:2099-->2<!--/v8-->/<!--v8:2100-->3<!--/v8-->/<!--v8:2101-->3<!--/v8--> | <!--v8:2102-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w30/k5 | <!--v8:2103-->2<!--/v8-->/<!--v8:2104-->3<!--/v8-->/<!--v8:2105-->3<!--/v8--> | <!--v8:2106-->0<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w60/k2 | <!--v8:2107-->2<!--/v8-->/<!--v8:2108-->2<!--/v8-->/<!--v8:2109-->3<!--/v8--> | <!--v8:2110-->1<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w60/k3 | <!--v8:2111-->2<!--/v8-->/<!--v8:2112-->2<!--/v8-->/<!--v8:2113-->3<!--/v8--> | <!--v8:2114-->1<!--/v8--> |
| BOCPD | ts-travel-service / loss | B4/w60/k5 | <!--v8:2115-->0<!--/v8-->/<!--v8:2116-->2<!--/v8-->/<!--v8:2117-->3<!--/v8--> | <!--v8:2118-->1<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N1/1.5 | <!--v8:2119-->1<!--/v8-->/<!--v8:2120-->3<!--/v8-->/<!--v8:2121-->3<!--/v8--> | <!--v8:2122-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N1/2.0 | <!--v8:2123-->0<!--/v8-->/<!--v8:2124-->3<!--/v8-->/<!--v8:2125-->3<!--/v8--> | <!--v8:2126-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N1/3.0 | <!--v8:2127-->0<!--/v8-->/<!--v8:2128-->3<!--/v8-->/<!--v8:2129-->3<!--/v8--> | <!--v8:2130-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N2/5 | <!--v8:2131-->2<!--/v8-->/<!--v8:2132-->3<!--/v8-->/<!--v8:2133-->3<!--/v8--> | <!--v8:2134-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N2/10 | <!--v8:2135-->1<!--/v8-->/<!--v8:2136-->3<!--/v8-->/<!--v8:2137-->3<!--/v8--> | <!--v8:2138-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N2/20 | <!--v8:2139-->0<!--/v8-->/<!--v8:2140-->3<!--/v8-->/<!--v8:2141-->3<!--/v8--> | <!--v8:2142-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N3/5 | <!--v8:2143-->1<!--/v8-->/<!--v8:2144-->3<!--/v8-->/<!--v8:2145-->3<!--/v8--> | <!--v8:2146-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N3/10 | <!--v8:2147-->2<!--/v8-->/<!--v8:2148-->3<!--/v8-->/<!--v8:2149-->3<!--/v8--> | <!--v8:2150-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N3/20 | <!--v8:2151-->3<!--/v8-->/<!--v8:2152-->3<!--/v8-->/<!--v8:2153-->3<!--/v8--> | <!--v8:2154-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / cpu | N4 | <!--v8:2155-->0<!--/v8-->/<!--v8:2156-->3<!--/v8-->/<!--v8:2157-->3<!--/v8--> | <!--v8:2158-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N1/1.5 | <!--v8:2159-->1<!--/v8-->/<!--v8:2160-->3<!--/v8-->/<!--v8:2161-->3<!--/v8--> | <!--v8:2162-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N1/2.0 | <!--v8:2163-->0<!--/v8-->/<!--v8:2164-->3<!--/v8-->/<!--v8:2165-->3<!--/v8--> | <!--v8:2166-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N1/3.0 | <!--v8:2167-->0<!--/v8-->/<!--v8:2168-->3<!--/v8-->/<!--v8:2169-->3<!--/v8--> | <!--v8:2170-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N2/5 | <!--v8:2171-->3<!--/v8-->/<!--v8:2172-->3<!--/v8-->/<!--v8:2173-->3<!--/v8--> | <!--v8:2174-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N2/10 | <!--v8:2175-->2<!--/v8-->/<!--v8:2176-->3<!--/v8-->/<!--v8:2177-->3<!--/v8--> | <!--v8:2178-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N2/20 | <!--v8:2179-->2<!--/v8-->/<!--v8:2180-->3<!--/v8-->/<!--v8:2181-->3<!--/v8--> | <!--v8:2182-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N3/5 | <!--v8:2183-->0<!--/v8-->/<!--v8:2184-->3<!--/v8-->/<!--v8:2185-->3<!--/v8--> | <!--v8:2186-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N3/10 | <!--v8:2187-->1<!--/v8-->/<!--v8:2188-->3<!--/v8-->/<!--v8:2189-->3<!--/v8--> | <!--v8:2190-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N3/20 | <!--v8:2191-->1<!--/v8-->/<!--v8:2192-->3<!--/v8-->/<!--v8:2193-->3<!--/v8--> | <!--v8:2194-->0<!--/v8--> |
| N-Sigma chính | ts-auth-service / delay | N4 | <!--v8:2195-->0<!--/v8-->/<!--v8:2196-->3<!--/v8-->/<!--v8:2197-->3<!--/v8--> | <!--v8:2198-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N1/1.5 | <!--v8:2199-->3<!--/v8-->/<!--v8:2200-->3<!--/v8-->/<!--v8:2201-->3<!--/v8--> | <!--v8:2202-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N1/2.0 | <!--v8:2203-->2<!--/v8-->/<!--v8:2204-->3<!--/v8-->/<!--v8:2205-->3<!--/v8--> | <!--v8:2206-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N1/3.0 | <!--v8:2207-->0<!--/v8-->/<!--v8:2208-->3<!--/v8-->/<!--v8:2209-->3<!--/v8--> | <!--v8:2210-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N2/5 | <!--v8:2211-->2<!--/v8-->/<!--v8:2212-->3<!--/v8-->/<!--v8:2213-->3<!--/v8--> | <!--v8:2214-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N2/10 | <!--v8:2215-->0<!--/v8-->/<!--v8:2216-->3<!--/v8-->/<!--v8:2217-->3<!--/v8--> | <!--v8:2218-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N2/20 | <!--v8:2219-->0<!--/v8-->/<!--v8:2220-->3<!--/v8-->/<!--v8:2221-->3<!--/v8--> | <!--v8:2222-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N3/5 | <!--v8:2223-->1<!--/v8-->/<!--v8:2224-->3<!--/v8-->/<!--v8:2225-->3<!--/v8--> | <!--v8:2226-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N3/10 | <!--v8:2227-->3<!--/v8-->/<!--v8:2228-->3<!--/v8-->/<!--v8:2229-->3<!--/v8--> | <!--v8:2230-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N3/20 | <!--v8:2231-->3<!--/v8-->/<!--v8:2232-->3<!--/v8-->/<!--v8:2233-->3<!--/v8--> | <!--v8:2234-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / disk | N4 | <!--v8:2235-->0<!--/v8-->/<!--v8:2236-->3<!--/v8-->/<!--v8:2237-->3<!--/v8--> | <!--v8:2238-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N1/1.5 | <!--v8:2239-->1<!--/v8-->/<!--v8:2240-->3<!--/v8-->/<!--v8:2241-->3<!--/v8--> | <!--v8:2242-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N1/2.0 | <!--v8:2243-->1<!--/v8-->/<!--v8:2244-->3<!--/v8-->/<!--v8:2245-->3<!--/v8--> | <!--v8:2246-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N1/3.0 | <!--v8:2247-->1<!--/v8-->/<!--v8:2248-->3<!--/v8-->/<!--v8:2249-->3<!--/v8--> | <!--v8:2250-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N2/5 | <!--v8:2251-->3<!--/v8-->/<!--v8:2252-->3<!--/v8-->/<!--v8:2253-->3<!--/v8--> | <!--v8:2254-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N2/10 | <!--v8:2255-->1<!--/v8-->/<!--v8:2256-->3<!--/v8-->/<!--v8:2257-->3<!--/v8--> | <!--v8:2258-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N2/20 | <!--v8:2259-->0<!--/v8-->/<!--v8:2260-->3<!--/v8-->/<!--v8:2261-->3<!--/v8--> | <!--v8:2262-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N3/5 | <!--v8:2263-->0<!--/v8-->/<!--v8:2264-->3<!--/v8-->/<!--v8:2265-->3<!--/v8--> | <!--v8:2266-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N3/10 | <!--v8:2267-->2<!--/v8-->/<!--v8:2268-->3<!--/v8-->/<!--v8:2269-->3<!--/v8--> | <!--v8:2270-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N3/20 | <!--v8:2271-->3<!--/v8-->/<!--v8:2272-->3<!--/v8-->/<!--v8:2273-->3<!--/v8--> | <!--v8:2274-->0<!--/v8--> |
| N-Sigma chính | ts-order-service / loss | N4 | <!--v8:2275-->0<!--/v8-->/<!--v8:2276-->3<!--/v8-->/<!--v8:2277-->3<!--/v8--> | <!--v8:2278-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N1/1.5 | <!--v8:2279-->1<!--/v8-->/<!--v8:2280-->3<!--/v8-->/<!--v8:2281-->3<!--/v8--> | <!--v8:2282-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N1/2.0 | <!--v8:2283-->1<!--/v8-->/<!--v8:2284-->3<!--/v8-->/<!--v8:2285-->3<!--/v8--> | <!--v8:2286-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N1/3.0 | <!--v8:2287-->1<!--/v8-->/<!--v8:2288-->3<!--/v8-->/<!--v8:2289-->3<!--/v8--> | <!--v8:2290-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N2/5 | <!--v8:2291-->1<!--/v8-->/<!--v8:2292-->3<!--/v8-->/<!--v8:2293-->3<!--/v8--> | <!--v8:2294-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N2/10 | <!--v8:2295-->0<!--/v8-->/<!--v8:2296-->3<!--/v8-->/<!--v8:2297-->3<!--/v8--> | <!--v8:2298-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N2/20 | <!--v8:2299-->0<!--/v8-->/<!--v8:2300-->3<!--/v8-->/<!--v8:2301-->3<!--/v8--> | <!--v8:2302-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N3/5 | <!--v8:2303-->2<!--/v8-->/<!--v8:2304-->3<!--/v8-->/<!--v8:2305-->3<!--/v8--> | <!--v8:2306-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N3/10 | <!--v8:2307-->3<!--/v8-->/<!--v8:2308-->3<!--/v8-->/<!--v8:2309-->3<!--/v8--> | <!--v8:2310-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N3/20 | <!--v8:2311-->3<!--/v8-->/<!--v8:2312-->3<!--/v8-->/<!--v8:2313-->3<!--/v8--> | <!--v8:2314-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / mem | N4 | <!--v8:2315-->0<!--/v8-->/<!--v8:2316-->3<!--/v8-->/<!--v8:2317-->3<!--/v8--> | <!--v8:2318-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N1/1.5 | <!--v8:2319-->1<!--/v8-->/<!--v8:2320-->3<!--/v8-->/<!--v8:2321-->3<!--/v8--> | <!--v8:2322-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N1/2.0 | <!--v8:2323-->0<!--/v8-->/<!--v8:2324-->3<!--/v8-->/<!--v8:2325-->3<!--/v8--> | <!--v8:2326-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N1/3.0 | <!--v8:2327-->0<!--/v8-->/<!--v8:2328-->3<!--/v8-->/<!--v8:2329-->3<!--/v8--> | <!--v8:2330-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N2/5 | <!--v8:2331-->0<!--/v8-->/<!--v8:2332-->3<!--/v8-->/<!--v8:2333-->3<!--/v8--> | <!--v8:2334-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N2/10 | <!--v8:2335-->0<!--/v8-->/<!--v8:2336-->3<!--/v8-->/<!--v8:2337-->3<!--/v8--> | <!--v8:2338-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N2/20 | <!--v8:2339-->0<!--/v8-->/<!--v8:2340-->3<!--/v8-->/<!--v8:2341-->3<!--/v8--> | <!--v8:2342-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N3/5 | <!--v8:2343-->3<!--/v8-->/<!--v8:2344-->3<!--/v8-->/<!--v8:2345-->3<!--/v8--> | <!--v8:2346-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N3/10 | <!--v8:2347-->3<!--/v8-->/<!--v8:2348-->3<!--/v8-->/<!--v8:2349-->3<!--/v8--> | <!--v8:2350-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N3/20 | <!--v8:2351-->3<!--/v8-->/<!--v8:2352-->3<!--/v8-->/<!--v8:2353-->3<!--/v8--> | <!--v8:2354-->0<!--/v8--> |
| N-Sigma chính | ts-route-service / socket | N4 | <!--v8:2355-->0<!--/v8-->/<!--v8:2356-->3<!--/v8-->/<!--v8:2357-->3<!--/v8--> | <!--v8:2358-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N1/1.5 | <!--v8:2359-->2<!--/v8-->/<!--v8:2360-->3<!--/v8-->/<!--v8:2361-->3<!--/v8--> | <!--v8:2362-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N1/2.0 | <!--v8:2363-->1<!--/v8-->/<!--v8:2364-->3<!--/v8-->/<!--v8:2365-->3<!--/v8--> | <!--v8:2366-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N1/3.0 | <!--v8:2367-->1<!--/v8-->/<!--v8:2368-->3<!--/v8-->/<!--v8:2369-->3<!--/v8--> | <!--v8:2370-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N2/5 | <!--v8:2371-->2<!--/v8-->/<!--v8:2372-->3<!--/v8-->/<!--v8:2373-->3<!--/v8--> | <!--v8:2374-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N2/10 | <!--v8:2375-->1<!--/v8-->/<!--v8:2376-->3<!--/v8-->/<!--v8:2377-->3<!--/v8--> | <!--v8:2378-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N2/20 | <!--v8:2379-->0<!--/v8-->/<!--v8:2380-->3<!--/v8-->/<!--v8:2381-->3<!--/v8--> | <!--v8:2382-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N3/5 | <!--v8:2383-->1<!--/v8-->/<!--v8:2384-->3<!--/v8-->/<!--v8:2385-->3<!--/v8--> | <!--v8:2386-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N3/10 | <!--v8:2387-->2<!--/v8-->/<!--v8:2388-->3<!--/v8-->/<!--v8:2389-->3<!--/v8--> | <!--v8:2390-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N3/20 | <!--v8:2391-->3<!--/v8-->/<!--v8:2392-->3<!--/v8-->/<!--v8:2393-->3<!--/v8--> | <!--v8:2394-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / cpu | N4 | <!--v8:2395-->0<!--/v8-->/<!--v8:2396-->3<!--/v8-->/<!--v8:2397-->3<!--/v8--> | <!--v8:2398-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N1/1.5 | <!--v8:2399-->1<!--/v8-->/<!--v8:2400-->3<!--/v8-->/<!--v8:2401-->3<!--/v8--> | <!--v8:2402-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N1/2.0 | <!--v8:2403-->0<!--/v8-->/<!--v8:2404-->3<!--/v8-->/<!--v8:2405-->3<!--/v8--> | <!--v8:2406-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N1/3.0 | <!--v8:2407-->0<!--/v8-->/<!--v8:2408-->3<!--/v8-->/<!--v8:2409-->3<!--/v8--> | <!--v8:2410-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N2/5 | <!--v8:2411-->1<!--/v8-->/<!--v8:2412-->3<!--/v8-->/<!--v8:2413-->3<!--/v8--> | <!--v8:2414-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N2/10 | <!--v8:2415-->0<!--/v8-->/<!--v8:2416-->3<!--/v8-->/<!--v8:2417-->3<!--/v8--> | <!--v8:2418-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N2/20 | <!--v8:2419-->0<!--/v8-->/<!--v8:2420-->3<!--/v8-->/<!--v8:2421-->3<!--/v8--> | <!--v8:2422-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N3/5 | <!--v8:2423-->2<!--/v8-->/<!--v8:2424-->3<!--/v8-->/<!--v8:2425-->3<!--/v8--> | <!--v8:2426-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N3/10 | <!--v8:2427-->3<!--/v8-->/<!--v8:2428-->3<!--/v8-->/<!--v8:2429-->3<!--/v8--> | <!--v8:2430-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N3/20 | <!--v8:2431-->3<!--/v8-->/<!--v8:2432-->3<!--/v8-->/<!--v8:2433-->3<!--/v8--> | <!--v8:2434-->0<!--/v8--> |
| N-Sigma chính | ts-train-service / delay | N4 | <!--v8:2435-->0<!--/v8-->/<!--v8:2436-->3<!--/v8-->/<!--v8:2437-->3<!--/v8--> | <!--v8:2438-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N1/1.5 | <!--v8:2439-->0<!--/v8-->/<!--v8:2440-->3<!--/v8-->/<!--v8:2441-->3<!--/v8--> | <!--v8:2442-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N1/2.0 | <!--v8:2443-->0<!--/v8-->/<!--v8:2444-->3<!--/v8-->/<!--v8:2445-->3<!--/v8--> | <!--v8:2446-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N1/3.0 | <!--v8:2447-->0<!--/v8-->/<!--v8:2448-->3<!--/v8-->/<!--v8:2449-->3<!--/v8--> | <!--v8:2450-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N2/5 | <!--v8:2451-->1<!--/v8-->/<!--v8:2452-->3<!--/v8-->/<!--v8:2453-->3<!--/v8--> | <!--v8:2454-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N2/10 | <!--v8:2455-->0<!--/v8-->/<!--v8:2456-->3<!--/v8-->/<!--v8:2457-->3<!--/v8--> | <!--v8:2458-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N2/20 | <!--v8:2459-->0<!--/v8-->/<!--v8:2460-->3<!--/v8-->/<!--v8:2461-->3<!--/v8--> | <!--v8:2462-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N3/5 | <!--v8:2463-->2<!--/v8-->/<!--v8:2464-->3<!--/v8-->/<!--v8:2465-->3<!--/v8--> | <!--v8:2466-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N3/10 | <!--v8:2467-->3<!--/v8-->/<!--v8:2468-->3<!--/v8-->/<!--v8:2469-->3<!--/v8--> | <!--v8:2470-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N3/20 | <!--v8:2471-->3<!--/v8-->/<!--v8:2472-->3<!--/v8-->/<!--v8:2473-->3<!--/v8--> | <!--v8:2474-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / disk | N4 | <!--v8:2475-->0<!--/v8-->/<!--v8:2476-->3<!--/v8-->/<!--v8:2477-->3<!--/v8--> | <!--v8:2478-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N1/1.5 | <!--v8:2479-->1<!--/v8-->/<!--v8:2480-->3<!--/v8-->/<!--v8:2481-->3<!--/v8--> | <!--v8:2482-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N1/2.0 | <!--v8:2483-->0<!--/v8-->/<!--v8:2484-->3<!--/v8-->/<!--v8:2485-->3<!--/v8--> | <!--v8:2486-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N1/3.0 | <!--v8:2487-->0<!--/v8-->/<!--v8:2488-->3<!--/v8-->/<!--v8:2489-->3<!--/v8--> | <!--v8:2490-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N2/5 | <!--v8:2491-->2<!--/v8-->/<!--v8:2492-->3<!--/v8-->/<!--v8:2493-->3<!--/v8--> | <!--v8:2494-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N2/10 | <!--v8:2495-->1<!--/v8-->/<!--v8:2496-->3<!--/v8-->/<!--v8:2497-->3<!--/v8--> | <!--v8:2498-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N2/20 | <!--v8:2499-->1<!--/v8-->/<!--v8:2500-->3<!--/v8-->/<!--v8:2501-->3<!--/v8--> | <!--v8:2502-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N3/5 | <!--v8:2503-->1<!--/v8-->/<!--v8:2504-->3<!--/v8-->/<!--v8:2505-->3<!--/v8--> | <!--v8:2506-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N3/10 | <!--v8:2507-->2<!--/v8-->/<!--v8:2508-->3<!--/v8-->/<!--v8:2509-->3<!--/v8--> | <!--v8:2510-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N3/20 | <!--v8:2511-->2<!--/v8-->/<!--v8:2512-->3<!--/v8-->/<!--v8:2513-->3<!--/v8--> | <!--v8:2514-->0<!--/v8--> |
| N-Sigma chính | ts-travel-service / loss | N4 | <!--v8:2515-->0<!--/v8-->/<!--v8:2516-->3<!--/v8-->/<!--v8:2517-->3<!--/v8--> | <!--v8:2518-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N1/1.5 | <!--v8:2519-->1<!--/v8-->/<!--v8:2520-->3<!--/v8-->/<!--v8:2521-->3<!--/v8--> | <!--v8:2522-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N1/2.0 | <!--v8:2523-->1<!--/v8-->/<!--v8:2524-->3<!--/v8-->/<!--v8:2525-->3<!--/v8--> | <!--v8:2526-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N1/3.0 | <!--v8:2527-->0<!--/v8-->/<!--v8:2528-->3<!--/v8-->/<!--v8:2529-->3<!--/v8--> | <!--v8:2530-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N2/5 | <!--v8:2531-->3<!--/v8-->/<!--v8:2532-->3<!--/v8-->/<!--v8:2533-->3<!--/v8--> | <!--v8:2534-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N2/10 | <!--v8:2535-->3<!--/v8-->/<!--v8:2536-->3<!--/v8-->/<!--v8:2537-->3<!--/v8--> | <!--v8:2538-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N2/20 | <!--v8:2539-->2<!--/v8-->/<!--v8:2540-->3<!--/v8-->/<!--v8:2541-->3<!--/v8--> | <!--v8:2542-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N3/5 | <!--v8:2543-->0<!--/v8-->/<!--v8:2544-->3<!--/v8-->/<!--v8:2545-->3<!--/v8--> | <!--v8:2546-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N3/10 | <!--v8:2547-->0<!--/v8-->/<!--v8:2548-->3<!--/v8-->/<!--v8:2549-->3<!--/v8--> | <!--v8:2550-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N3/20 | <!--v8:2551-->1<!--/v8-->/<!--v8:2552-->3<!--/v8-->/<!--v8:2553-->3<!--/v8--> | <!--v8:2554-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / cpu | N4 | <!--v8:2555-->1<!--/v8-->/<!--v8:2556-->3<!--/v8-->/<!--v8:2557-->3<!--/v8--> | <!--v8:2558-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N1/1.5 | <!--v8:2559-->2<!--/v8-->/<!--v8:2560-->3<!--/v8-->/<!--v8:2561-->3<!--/v8--> | <!--v8:2562-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N1/2.0 | <!--v8:2563-->0<!--/v8-->/<!--v8:2564-->3<!--/v8-->/<!--v8:2565-->3<!--/v8--> | <!--v8:2566-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N1/3.0 | <!--v8:2567-->0<!--/v8-->/<!--v8:2568-->3<!--/v8-->/<!--v8:2569-->3<!--/v8--> | <!--v8:2570-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N2/5 | <!--v8:2571-->3<!--/v8-->/<!--v8:2572-->3<!--/v8-->/<!--v8:2573-->3<!--/v8--> | <!--v8:2574-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N2/10 | <!--v8:2575-->3<!--/v8-->/<!--v8:2576-->3<!--/v8-->/<!--v8:2577-->3<!--/v8--> | <!--v8:2578-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N2/20 | <!--v8:2579-->2<!--/v8-->/<!--v8:2580-->3<!--/v8-->/<!--v8:2581-->3<!--/v8--> | <!--v8:2582-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N3/5 | <!--v8:2583-->0<!--/v8-->/<!--v8:2584-->3<!--/v8-->/<!--v8:2585-->3<!--/v8--> | <!--v8:2586-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N3/10 | <!--v8:2587-->0<!--/v8-->/<!--v8:2588-->3<!--/v8-->/<!--v8:2589-->3<!--/v8--> | <!--v8:2590-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N3/20 | <!--v8:2591-->1<!--/v8-->/<!--v8:2592-->3<!--/v8-->/<!--v8:2593-->3<!--/v8--> | <!--v8:2594-->0<!--/v8--> |
| N-Sigma đối chứng | ts-auth-service / delay | N4 | <!--v8:2595-->2<!--/v8-->/<!--v8:2596-->3<!--/v8-->/<!--v8:2597-->3<!--/v8--> | <!--v8:2598-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N1/1.5 | <!--v8:2599-->1<!--/v8-->/<!--v8:2600-->3<!--/v8-->/<!--v8:2601-->3<!--/v8--> | <!--v8:2602-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N1/2.0 | <!--v8:2603-->0<!--/v8-->/<!--v8:2604-->3<!--/v8-->/<!--v8:2605-->3<!--/v8--> | <!--v8:2606-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N1/3.0 | <!--v8:2607-->0<!--/v8-->/<!--v8:2608-->3<!--/v8-->/<!--v8:2609-->3<!--/v8--> | <!--v8:2610-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N2/5 | <!--v8:2611-->3<!--/v8-->/<!--v8:2612-->3<!--/v8-->/<!--v8:2613-->3<!--/v8--> | <!--v8:2614-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N2/10 | <!--v8:2615-->3<!--/v8-->/<!--v8:2616-->3<!--/v8-->/<!--v8:2617-->3<!--/v8--> | <!--v8:2618-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N2/20 | <!--v8:2619-->3<!--/v8-->/<!--v8:2620-->3<!--/v8-->/<!--v8:2621-->3<!--/v8--> | <!--v8:2622-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N3/5 | <!--v8:2623-->0<!--/v8-->/<!--v8:2624-->3<!--/v8-->/<!--v8:2625-->3<!--/v8--> | <!--v8:2626-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N3/10 | <!--v8:2627-->0<!--/v8-->/<!--v8:2628-->3<!--/v8-->/<!--v8:2629-->3<!--/v8--> | <!--v8:2630-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N3/20 | <!--v8:2631-->0<!--/v8-->/<!--v8:2632-->3<!--/v8-->/<!--v8:2633-->3<!--/v8--> | <!--v8:2634-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / disk | N4 | <!--v8:2635-->0<!--/v8-->/<!--v8:2636-->3<!--/v8-->/<!--v8:2637-->3<!--/v8--> | <!--v8:2638-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N1/1.5 | <!--v8:2639-->1<!--/v8-->/<!--v8:2640-->3<!--/v8-->/<!--v8:2641-->3<!--/v8--> | <!--v8:2642-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N1/2.0 | <!--v8:2643-->0<!--/v8-->/<!--v8:2644-->3<!--/v8-->/<!--v8:2645-->3<!--/v8--> | <!--v8:2646-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N1/3.0 | <!--v8:2647-->0<!--/v8-->/<!--v8:2648-->3<!--/v8-->/<!--v8:2649-->3<!--/v8--> | <!--v8:2650-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N2/5 | <!--v8:2651-->3<!--/v8-->/<!--v8:2652-->3<!--/v8-->/<!--v8:2653-->3<!--/v8--> | <!--v8:2654-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N2/10 | <!--v8:2655-->3<!--/v8-->/<!--v8:2656-->3<!--/v8-->/<!--v8:2657-->3<!--/v8--> | <!--v8:2658-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N2/20 | <!--v8:2659-->2<!--/v8-->/<!--v8:2660-->3<!--/v8-->/<!--v8:2661-->3<!--/v8--> | <!--v8:2662-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N3/5 | <!--v8:2663-->0<!--/v8-->/<!--v8:2664-->3<!--/v8-->/<!--v8:2665-->3<!--/v8--> | <!--v8:2666-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N3/10 | <!--v8:2667-->0<!--/v8-->/<!--v8:2668-->3<!--/v8-->/<!--v8:2669-->3<!--/v8--> | <!--v8:2670-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N3/20 | <!--v8:2671-->1<!--/v8-->/<!--v8:2672-->3<!--/v8-->/<!--v8:2673-->3<!--/v8--> | <!--v8:2674-->0<!--/v8--> |
| N-Sigma đối chứng | ts-order-service / loss | N4 | <!--v8:2675-->0<!--/v8-->/<!--v8:2676-->3<!--/v8-->/<!--v8:2677-->3<!--/v8--> | <!--v8:2678-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N1/1.5 | <!--v8:2679-->3<!--/v8-->/<!--v8:2680-->3<!--/v8-->/<!--v8:2681-->3<!--/v8--> | <!--v8:2682-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N1/2.0 | <!--v8:2683-->1<!--/v8-->/<!--v8:2684-->3<!--/v8-->/<!--v8:2685-->3<!--/v8--> | <!--v8:2686-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N1/3.0 | <!--v8:2687-->0<!--/v8-->/<!--v8:2688-->3<!--/v8-->/<!--v8:2689-->3<!--/v8--> | <!--v8:2690-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N2/5 | <!--v8:2691-->3<!--/v8-->/<!--v8:2692-->3<!--/v8-->/<!--v8:2693-->3<!--/v8--> | <!--v8:2694-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N2/10 | <!--v8:2695-->3<!--/v8-->/<!--v8:2696-->3<!--/v8-->/<!--v8:2697-->3<!--/v8--> | <!--v8:2698-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N2/20 | <!--v8:2699-->2<!--/v8-->/<!--v8:2700-->3<!--/v8-->/<!--v8:2701-->3<!--/v8--> | <!--v8:2702-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N3/5 | <!--v8:2703-->0<!--/v8-->/<!--v8:2704-->3<!--/v8-->/<!--v8:2705-->3<!--/v8--> | <!--v8:2706-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N3/10 | <!--v8:2707-->0<!--/v8-->/<!--v8:2708-->3<!--/v8-->/<!--v8:2709-->3<!--/v8--> | <!--v8:2710-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N3/20 | <!--v8:2711-->1<!--/v8-->/<!--v8:2712-->3<!--/v8-->/<!--v8:2713-->3<!--/v8--> | <!--v8:2714-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / mem | N4 | <!--v8:2715-->0<!--/v8-->/<!--v8:2716-->3<!--/v8-->/<!--v8:2717-->3<!--/v8--> | <!--v8:2718-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N1/1.5 | <!--v8:2719-->2<!--/v8-->/<!--v8:2720-->3<!--/v8-->/<!--v8:2721-->3<!--/v8--> | <!--v8:2722-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N1/2.0 | <!--v8:2723-->1<!--/v8-->/<!--v8:2724-->3<!--/v8-->/<!--v8:2725-->3<!--/v8--> | <!--v8:2726-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N1/3.0 | <!--v8:2727-->0<!--/v8-->/<!--v8:2728-->3<!--/v8-->/<!--v8:2729-->3<!--/v8--> | <!--v8:2730-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N2/5 | <!--v8:2731-->3<!--/v8-->/<!--v8:2732-->3<!--/v8-->/<!--v8:2733-->3<!--/v8--> | <!--v8:2734-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N2/10 | <!--v8:2735-->2<!--/v8-->/<!--v8:2736-->3<!--/v8-->/<!--v8:2737-->3<!--/v8--> | <!--v8:2738-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N2/20 | <!--v8:2739-->1<!--/v8-->/<!--v8:2740-->3<!--/v8-->/<!--v8:2741-->3<!--/v8--> | <!--v8:2742-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N3/5 | <!--v8:2743-->0<!--/v8-->/<!--v8:2744-->3<!--/v8-->/<!--v8:2745-->3<!--/v8--> | <!--v8:2746-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N3/10 | <!--v8:2747-->1<!--/v8-->/<!--v8:2748-->3<!--/v8-->/<!--v8:2749-->3<!--/v8--> | <!--v8:2750-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N3/20 | <!--v8:2751-->2<!--/v8-->/<!--v8:2752-->3<!--/v8-->/<!--v8:2753-->3<!--/v8--> | <!--v8:2754-->0<!--/v8--> |
| N-Sigma đối chứng | ts-route-service / socket | N4 | <!--v8:2755-->0<!--/v8-->/<!--v8:2756-->3<!--/v8-->/<!--v8:2757-->3<!--/v8--> | <!--v8:2758-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N1/1.5 | <!--v8:2759-->0<!--/v8-->/<!--v8:2760-->3<!--/v8-->/<!--v8:2761-->3<!--/v8--> | <!--v8:2762-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N1/2.0 | <!--v8:2763-->0<!--/v8-->/<!--v8:2764-->3<!--/v8-->/<!--v8:2765-->3<!--/v8--> | <!--v8:2766-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N1/3.0 | <!--v8:2767-->0<!--/v8-->/<!--v8:2768-->3<!--/v8-->/<!--v8:2769-->3<!--/v8--> | <!--v8:2770-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N2/5 | <!--v8:2771-->3<!--/v8-->/<!--v8:2772-->3<!--/v8-->/<!--v8:2773-->3<!--/v8--> | <!--v8:2774-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N2/10 | <!--v8:2775-->3<!--/v8-->/<!--v8:2776-->3<!--/v8-->/<!--v8:2777-->3<!--/v8--> | <!--v8:2778-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N2/20 | <!--v8:2779-->3<!--/v8-->/<!--v8:2780-->3<!--/v8-->/<!--v8:2781-->3<!--/v8--> | <!--v8:2782-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N3/5 | <!--v8:2783-->0<!--/v8-->/<!--v8:2784-->3<!--/v8-->/<!--v8:2785-->3<!--/v8--> | <!--v8:2786-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N3/10 | <!--v8:2787-->0<!--/v8-->/<!--v8:2788-->3<!--/v8-->/<!--v8:2789-->3<!--/v8--> | <!--v8:2790-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N3/20 | <!--v8:2791-->0<!--/v8-->/<!--v8:2792-->3<!--/v8-->/<!--v8:2793-->3<!--/v8--> | <!--v8:2794-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / cpu | N4 | <!--v8:2795-->0<!--/v8-->/<!--v8:2796-->3<!--/v8-->/<!--v8:2797-->3<!--/v8--> | <!--v8:2798-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N1/1.5 | <!--v8:2799-->0<!--/v8-->/<!--v8:2800-->3<!--/v8-->/<!--v8:2801-->3<!--/v8--> | <!--v8:2802-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N1/2.0 | <!--v8:2803-->0<!--/v8-->/<!--v8:2804-->3<!--/v8-->/<!--v8:2805-->3<!--/v8--> | <!--v8:2806-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N1/3.0 | <!--v8:2807-->0<!--/v8-->/<!--v8:2808-->3<!--/v8-->/<!--v8:2809-->3<!--/v8--> | <!--v8:2810-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N2/5 | <!--v8:2811-->3<!--/v8-->/<!--v8:2812-->3<!--/v8-->/<!--v8:2813-->3<!--/v8--> | <!--v8:2814-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N2/10 | <!--v8:2815-->3<!--/v8-->/<!--v8:2816-->3<!--/v8-->/<!--v8:2817-->3<!--/v8--> | <!--v8:2818-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N2/20 | <!--v8:2819-->1<!--/v8-->/<!--v8:2820-->3<!--/v8-->/<!--v8:2821-->3<!--/v8--> | <!--v8:2822-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N3/5 | <!--v8:2823-->0<!--/v8-->/<!--v8:2824-->3<!--/v8-->/<!--v8:2825-->3<!--/v8--> | <!--v8:2826-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N3/10 | <!--v8:2827-->0<!--/v8-->/<!--v8:2828-->3<!--/v8-->/<!--v8:2829-->3<!--/v8--> | <!--v8:2830-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N3/20 | <!--v8:2831-->2<!--/v8-->/<!--v8:2832-->3<!--/v8-->/<!--v8:2833-->3<!--/v8--> | <!--v8:2834-->0<!--/v8--> |
| N-Sigma đối chứng | ts-train-service / delay | N4 | <!--v8:2835-->0<!--/v8-->/<!--v8:2836-->3<!--/v8-->/<!--v8:2837-->3<!--/v8--> | <!--v8:2838-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N1/1.5 | <!--v8:2839-->2<!--/v8-->/<!--v8:2840-->3<!--/v8-->/<!--v8:2841-->3<!--/v8--> | <!--v8:2842-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N1/2.0 | <!--v8:2843-->1<!--/v8-->/<!--v8:2844-->3<!--/v8-->/<!--v8:2845-->3<!--/v8--> | <!--v8:2846-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N1/3.0 | <!--v8:2847-->0<!--/v8-->/<!--v8:2848-->3<!--/v8-->/<!--v8:2849-->3<!--/v8--> | <!--v8:2850-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N2/5 | <!--v8:2851-->3<!--/v8-->/<!--v8:2852-->3<!--/v8-->/<!--v8:2853-->3<!--/v8--> | <!--v8:2854-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N2/10 | <!--v8:2855-->3<!--/v8-->/<!--v8:2856-->3<!--/v8-->/<!--v8:2857-->3<!--/v8--> | <!--v8:2858-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N2/20 | <!--v8:2859-->2<!--/v8-->/<!--v8:2860-->3<!--/v8-->/<!--v8:2861-->3<!--/v8--> | <!--v8:2862-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N3/5 | <!--v8:2863-->0<!--/v8-->/<!--v8:2864-->3<!--/v8-->/<!--v8:2865-->3<!--/v8--> | <!--v8:2866-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N3/10 | <!--v8:2867-->0<!--/v8-->/<!--v8:2868-->3<!--/v8-->/<!--v8:2869-->3<!--/v8--> | <!--v8:2870-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N3/20 | <!--v8:2871-->1<!--/v8-->/<!--v8:2872-->3<!--/v8-->/<!--v8:2873-->3<!--/v8--> | <!--v8:2874-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / disk | N4 | <!--v8:2875-->0<!--/v8-->/<!--v8:2876-->3<!--/v8-->/<!--v8:2877-->3<!--/v8--> | <!--v8:2878-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N1/1.5 | <!--v8:2879-->0<!--/v8-->/<!--v8:2880-->3<!--/v8-->/<!--v8:2881-->3<!--/v8--> | <!--v8:2882-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N1/2.0 | <!--v8:2883-->0<!--/v8-->/<!--v8:2884-->3<!--/v8-->/<!--v8:2885-->3<!--/v8--> | <!--v8:2886-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N1/3.0 | <!--v8:2887-->0<!--/v8-->/<!--v8:2888-->3<!--/v8-->/<!--v8:2889-->3<!--/v8--> | <!--v8:2890-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N2/5 | <!--v8:2891-->3<!--/v8-->/<!--v8:2892-->3<!--/v8-->/<!--v8:2893-->3<!--/v8--> | <!--v8:2894-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N2/10 | <!--v8:2895-->3<!--/v8-->/<!--v8:2896-->3<!--/v8-->/<!--v8:2897-->3<!--/v8--> | <!--v8:2898-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N2/20 | <!--v8:2899-->3<!--/v8-->/<!--v8:2900-->3<!--/v8-->/<!--v8:2901-->3<!--/v8--> | <!--v8:2902-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N3/5 | <!--v8:2903-->0<!--/v8-->/<!--v8:2904-->3<!--/v8-->/<!--v8:2905-->3<!--/v8--> | <!--v8:2906-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N3/10 | <!--v8:2907-->0<!--/v8-->/<!--v8:2908-->3<!--/v8-->/<!--v8:2909-->3<!--/v8--> | <!--v8:2910-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N3/20 | <!--v8:2911-->0<!--/v8-->/<!--v8:2912-->3<!--/v8-->/<!--v8:2913-->3<!--/v8--> | <!--v8:2914-->0<!--/v8--> |
| N-Sigma đối chứng | ts-travel-service / loss | N4 | <!--v8:2915-->0<!--/v8-->/<!--v8:2916-->3<!--/v8-->/<!--v8:2917-->3<!--/v8--> | <!--v8:2918-->0<!--/v8--> |

### Những ca đổi cờ khi thay cấu hình

Nguồn: `runs/report-main-001/summary.json#/sensitivity_changes`. “Đổi” bao gồm True/False và miền N/A; bảng chỉ ghi khác biệt, danh sách đầy đủ cờ nằm ở theo-ca.json.

| Bộ | Cấu hình so với chính | Ca đổi / tổng | Mã ca và chuyển trạng thái |
|---|---|---|---|
| BOCPD | B2/2 so B2/5 | <!--v8:2919-->3<!--/v8-->/<!--v8:2920-->30<!--/v8--> | dev-3ae0a6c15a: False → True; dev-b8bd0abf60: False → True; dev-ba831dbeb8: False → True |
| BOCPD | B2/10 so B2/5 | <!--v8:2921-->2<!--/v8-->/<!--v8:2922-->30<!--/v8--> | dev-03d4910932: True → False; dev-57546fd87b: True → False |
| BOCPD | B3/2 so B3/5 | <!--v8:2923-->3<!--/v8-->/<!--v8:2924-->30<!--/v8--> | dev-3ae0a6c15a: False → None; dev-b8bd0abf60: False → None; dev-ba831dbeb8: False → None |
| BOCPD | B3/10 so B3/5 | <!--v8:2925-->2<!--/v8-->/<!--v8:2926-->30<!--/v8--> | dev-03d4910932: None → False; dev-57546fd87b: None → False |
| BOCPD | B4/w15/k2 so B4/w30/k3 | <!--v8:2927-->4<!--/v8-->/<!--v8:2928-->30<!--/v8--> | dev-57546fd87b: False → True; dev-59f696a169: True → False; dev-7f1b6b071d: False → True; dev-a5cabe5fa7: True → False |
| BOCPD | B4/w15/k3 so B4/w30/k3 | <!--v8:2929-->8<!--/v8-->/<!--v8:2930-->30<!--/v8--> | dev-1e6d61b5ec: True → False; dev-20acb4402d: True → False; dev-4e68956051: True → False; dev-57546fd87b: False → True; dev-59f696a169: True → False; dev-8017c6dc70: True → False; dev-a5cabe5fa7: True → False; dev-f81f88234e: True → False |
| BOCPD | B4/w15/k5 so B4/w30/k3 | <!--v8:2931-->12<!--/v8-->/<!--v8:2932-->30<!--/v8--> | dev-16597725c1: True → False; dev-1e6d61b5ec: True → False; dev-20acb4402d: True → False; dev-260d332c8d: True → False; dev-4e68956051: True → False; dev-59f696a169: True → False; dev-8017c6dc70: True → False; dev-a505ab3f65: True → False; dev-a5cabe5fa7: True → False; dev-a915aa2424: True → False; dev-f81f88234e: True → False; dev-fbc45b0c67: True → False |
| BOCPD | B4/w30/k2 so B4/w30/k3 | <!--v8:2933-->4<!--/v8-->/<!--v8:2934-->30<!--/v8--> | dev-14372e1209: False → True; dev-16870e660c: False → True; dev-57546fd87b: False → True; dev-7f1b6b071d: False → True |
| BOCPD | B4/w30/k5 so B4/w30/k3 | <!--v8:2935-->9<!--/v8-->/<!--v8:2936-->30<!--/v8--> | dev-16597725c1: True → False; dev-1e6d61b5ec: True → False; dev-20acb4402d: True → False; dev-260d332c8d: True → False; dev-8017c6dc70: True → False; dev-b8bd0abf60: True → False; dev-ba831dbeb8: True → False; dev-db293894ab: True → False; dev-fbc45b0c67: True → False |
| BOCPD | B4/w60/k2 so B4/w30/k3 | <!--v8:2937-->8<!--/v8-->/<!--v8:2938-->30<!--/v8--> | dev-03d4910932: False → None; dev-14372e1209: False → True; dev-3ae0a6c15a: False → True; dev-4e68956051: True → None; dev-57546fd87b: False → True; dev-7f1b6b071d: False → True; dev-a915aa2424: True → None; dev-de89e2f9e9: False → True |
| BOCPD | B4/w60/k3 so B4/w30/k3 | <!--v8:2939-->7<!--/v8-->/<!--v8:2940-->30<!--/v8--> | dev-03d4910932: False → None; dev-14372e1209: False → True; dev-20acb4402d: True → False; dev-4e68956051: True → None; dev-7f1b6b071d: False → True; dev-a915aa2424: True → None; dev-de89e2f9e9: False → True |
| BOCPD | B4/w60/k5 so B4/w30/k3 | <!--v8:2941-->10<!--/v8-->/<!--v8:2942-->30<!--/v8--> | dev-03d4910932: False → None; dev-16597725c1: True → False; dev-20acb4402d: True → False; dev-260d332c8d: True → False; dev-4e68956051: True → None; dev-a5cabe5fa7: True → False; dev-a915aa2424: True → None; dev-b8bd0abf60: True → False; dev-bcbd4f46ae: True → False; dev-fbc45b0c67: True → False |
| N-Sigma chính | N1/1.5 so N1/2.0 | <!--v8:2943-->7<!--/v8-->/<!--v8:2944-->30<!--/v8--> | dev-1e6d61b5ec: False → True; dev-3ae0a6c15a: False → True; dev-3defe3d34b: False → True; dev-4e68956051: False → True; dev-746fd74313: False → True; dev-7f1b6b071d: False → True; dev-b8bd0abf60: False → True |
| N-Sigma chính | N1/3.0 so N1/2.0 | <!--v8:2945-->2<!--/v8-->/<!--v8:2946-->30<!--/v8--> | dev-12a1a88069: True → False; dev-8017c6dc70: True → False |
| N-Sigma chính | N2/5 so N2/10 | <!--v8:2947-->11<!--/v8-->/<!--v8:2948-->30<!--/v8--> | dev-12a1a88069: False → True; dev-16597725c1: False → True; dev-16870e660c: False → True; dev-1e6d61b5ec: False → True; dev-20acb4402d: False → True; dev-260d332c8d: False → True; dev-57546fd87b: False → True; dev-98bc73c499: False → True; dev-a5cabe5fa7: False → True; dev-f9a8e05ed7: False → True; dev-fbc45b0c67: False → True |
| N-Sigma chính | N2/20 so N2/10 | <!--v8:2949-->3<!--/v8-->/<!--v8:2950-->30<!--/v8--> | dev-3ae0a6c15a: True → False; dev-59f696a169: True → False; dev-f36d0647d5: True → False |
| N-Sigma chính | N3/5 so N3/10 | <!--v8:2951-->11<!--/v8-->/<!--v8:2952-->30<!--/v8--> | dev-12a1a88069: True → False; dev-16597725c1: True → False; dev-16870e660c: True → False; dev-1e6d61b5ec: True → False; dev-20acb4402d: True → False; dev-260d332c8d: True → False; dev-57546fd87b: True → False; dev-98bc73c499: True → False; dev-a5cabe5fa7: True → False; dev-f9a8e05ed7: True → False; dev-fbc45b0c67: True → False |
| N-Sigma chính | N3/20 so N3/10 | <!--v8:2953-->3<!--/v8-->/<!--v8:2954-->30<!--/v8--> | dev-3ae0a6c15a: False → True; dev-59f696a169: False → True; dev-f36d0647d5: False → True |
| N-Sigma đối chứng | N1/1.5 so N1/2.0 | <!--v8:2955-->8<!--/v8-->/<!--v8:2956-->30<!--/v8--> | dev-12a1a88069: False → True; dev-16870e660c: False → True; dev-4f8a844308: False → True; dev-57546fd87b: False → True; dev-b8bd0abf60: False → True; dev-db293894ab: False → True; dev-f36d0647d5: False → True; dev-f81f88234e: False → True |
| N-Sigma đối chứng | N1/3.0 so N1/2.0 | <!--v8:2957-->4<!--/v8-->/<!--v8:2958-->30<!--/v8--> | dev-14372e1209: True → False; dev-3defe3d34b: True → False; dev-bcbd4f46ae: True → False; dev-f9a8e05ed7: True → False |
| N-Sigma đối chứng | N2/5 so N2/10 | <!--v8:2959-->1<!--/v8-->/<!--v8:2960-->30<!--/v8--> | dev-bcbd4f46ae: False → True |
| N-Sigma đối chứng | N2/20 so N2/10 | <!--v8:2961-->8<!--/v8-->/<!--v8:2962-->30<!--/v8--> | dev-03d4910932: True → False; dev-16597725c1: True → False; dev-4e68956051: True → False; dev-4f8a844308: True → False; dev-57546fd87b: True → False; dev-a505ab3f65: True → False; dev-db293894ab: True → False; dev-f36d0647d5: True → False |
| N-Sigma đối chứng | N3/5 so N3/10 | <!--v8:2963-->1<!--/v8-->/<!--v8:2964-->30<!--/v8--> | dev-bcbd4f46ae: True → False |
| N-Sigma đối chứng | N3/20 so N3/10 | <!--v8:2965-->8<!--/v8-->/<!--v8:2966-->30<!--/v8--> | dev-03d4910932: False → True; dev-16597725c1: False → True; dev-4e68956051: False → True; dev-4f8a844308: False → True; dev-57546fd87b: False → True; dev-a505ab3f65: False → True; dev-db293894ab: False → True; dev-f36d0647d5: False → True |

### V7: báo động cạnh điểm không báo

Bằng nhau đúng số chỉ là dấu mô tả để chọn ca đọc tay, không là kiểm định tương đương. Chưa bằng nhau không chứng minh cờ phân biệt; không đặt ngưỡng gần bằng. B4 vẫn giữ trong cờ cấu hình chính để mô tả, không là số ca đã giải thích. B1 chỉ xét cửa sổ quanh i nằm trong Nv. B4 chỉ xét đủ MAD và hai cửa sổ nằm trong nền, cùng miền cho báo động và đối chứng. Mẫu số báo động là ca có t̂ hợp lệ; mẫu số đối chứng là điểm không báo trong miền của từng w. Các ca S vẫn có điểm đối chứng nền nhưng không có t̂ hợp lệ; hai quần thể này không đồng nhất. Đây là tỉ lệ mô tả, không là kiểm định thống kê. N1–N4, B2/B3 V7 N/A vì chứa điều kiện báo động.

Nguồn: `runs/step5-001/V7.json#/aggregate/<cấu hình>/{all,cell}/<nhóm>`.

| Phạm vi | Cờ | Đúng tại t̂ / ca hợp lệ | Tỉ lệ tại t̂ | Đúng đối chứng / điểm hợp lệ | Tỉ lệ đối chứng |
|---|---|---|---|---|---|
| all | B1 | <!--v8:2967-->0<!--/v8-->/<!--v8:2968-->27<!--/v8--> | <!--v8:2969-->0<!--/v8--> | <!--v8:2970-->90<!--/v8-->/<!--v8:2971-->21308<!--/v8--> | <!--v8:2972-->0.00422377<!--/v8--> |
| ts-auth-service / cpu | B1 | <!--v8:2973-->0<!--/v8-->/<!--v8:2974-->2<!--/v8--> | <!--v8:2975-->0<!--/v8--> | <!--v8:2976-->5<!--/v8-->/<!--v8:2977-->2122<!--/v8--> | <!--v8:2978-->0.00235627<!--/v8--> |
| ts-auth-service / delay | B1 | <!--v8:2979-->0<!--/v8-->/<!--v8:2980-->3<!--/v8--> | <!--v8:2981-->0<!--/v8--> | <!--v8:2982-->15<!--/v8-->/<!--v8:2983-->2134<!--/v8--> | <!--v8:2984-->0.00702905<!--/v8--> |
| ts-order-service / disk | B1 | <!--v8:2985-->0<!--/v8-->/<!--v8:2986-->3<!--/v8--> | <!--v8:2987-->0<!--/v8--> | <!--v8:2988-->10<!--/v8-->/<!--v8:2989-->2119<!--/v8--> | <!--v8:2990-->0.00471921<!--/v8--> |
| ts-order-service / loss | B1 — không phân biệt đúng số | <!--v8:2991-->0<!--/v8-->/<!--v8:2992-->2<!--/v8--> | <!--v8:2993-->0<!--/v8--> | <!--v8:2994-->0<!--/v8-->/<!--v8:2995-->2128<!--/v8--> | <!--v8:2996-->0<!--/v8--> |
| ts-route-service / mem | B1 | <!--v8:2997-->0<!--/v8-->/<!--v8:2998-->3<!--/v8--> | <!--v8:2999-->0<!--/v8--> | <!--v8:3000-->15<!--/v8-->/<!--v8:3001-->2137<!--/v8--> | <!--v8:3002-->0.00701919<!--/v8--> |
| ts-route-service / socket | B1 | <!--v8:3003-->0<!--/v8-->/<!--v8:3004-->3<!--/v8--> | <!--v8:3005-->0<!--/v8--> | <!--v8:3006-->10<!--/v8-->/<!--v8:3007-->2136<!--/v8--> | <!--v8:3008-->0.00468165<!--/v8--> |
| ts-train-service / cpu | B1 | <!--v8:3009-->0<!--/v8-->/<!--v8:3010-->2<!--/v8--> | <!--v8:3011-->0<!--/v8--> | <!--v8:3012-->5<!--/v8-->/<!--v8:3013-->2139<!--/v8--> | <!--v8:3014-->0.00233754<!--/v8--> |
| ts-train-service / delay | B1 — không phân biệt đúng số | <!--v8:3015-->0<!--/v8-->/<!--v8:3016-->3<!--/v8--> | <!--v8:3017-->0<!--/v8--> | <!--v8:3018-->0<!--/v8-->/<!--v8:3019-->2137<!--/v8--> | <!--v8:3020-->0<!--/v8--> |
| ts-travel-service / disk | B1 | <!--v8:3021-->0<!--/v8-->/<!--v8:3022-->3<!--/v8--> | <!--v8:3023-->0<!--/v8--> | <!--v8:3024-->25<!--/v8-->/<!--v8:3025-->2125<!--/v8--> | <!--v8:3026-->0.0117647<!--/v8--> |
| ts-travel-service / loss | B1 | <!--v8:3027-->0<!--/v8-->/<!--v8:3028-->3<!--/v8--> | <!--v8:3029-->0<!--/v8--> | <!--v8:3030-->5<!--/v8-->/<!--v8:3031-->2131<!--/v8--> | <!--v8:3032-->0.00234632<!--/v8--> |
| all | B4/w15/k2 | <!--v8:3033-->20<!--/v8-->/<!--v8:3034-->27<!--/v8--> | <!--v8:3035-->0.740741<!--/v8--> | <!--v8:3036-->14178<!--/v8-->/<!--v8:3037-->19666<!--/v8--> | <!--v8:3038-->0.72094<!--/v8--> |
| ts-auth-service / cpu | B4/w15/k2 | <!--v8:3039-->1<!--/v8-->/<!--v8:3040-->2<!--/v8--> | <!--v8:3041-->0.5<!--/v8--> | <!--v8:3042-->1486<!--/v8-->/<!--v8:3043-->1958<!--/v8--> | <!--v8:3044-->0.758938<!--/v8--> |
| ts-auth-service / delay | B4/w15/k2 | <!--v8:3045-->3<!--/v8-->/<!--v8:3046-->3<!--/v8--> | <!--v8:3047-->1<!--/v8--> | <!--v8:3048-->1344<!--/v8-->/<!--v8:3049-->1969<!--/v8--> | <!--v8:3050-->0.68258<!--/v8--> |
| ts-order-service / disk | B4/w15/k2 | <!--v8:3051-->3<!--/v8-->/<!--v8:3052-->3<!--/v8--> | <!--v8:3053-->1<!--/v8--> | <!--v8:3054-->1302<!--/v8-->/<!--v8:3055-->1955<!--/v8--> | <!--v8:3056-->0.665985<!--/v8--> |
| ts-order-service / loss | B4/w15/k2 | <!--v8:3057-->2<!--/v8-->/<!--v8:3058-->2<!--/v8--> | <!--v8:3059-->1<!--/v8--> | <!--v8:3060-->1176<!--/v8-->/<!--v8:3061-->1965<!--/v8--> | <!--v8:3062-->0.598473<!--/v8--> |
| ts-route-service / mem | B4/w15/k2 | <!--v8:3063-->1<!--/v8-->/<!--v8:3064-->3<!--/v8--> | <!--v8:3065-->0.333333<!--/v8--> | <!--v8:3066-->1278<!--/v8-->/<!--v8:3067-->1973<!--/v8--> | <!--v8:3068-->0.647745<!--/v8--> |
| ts-route-service / socket | B4/w15/k2 | <!--v8:3069-->2<!--/v8-->/<!--v8:3070-->3<!--/v8--> | <!--v8:3071-->0.666667<!--/v8--> | <!--v8:3072-->1349<!--/v8-->/<!--v8:3073-->1973<!--/v8--> | <!--v8:3074-->0.68373<!--/v8--> |
| ts-train-service / cpu | B4/w15/k2 | <!--v8:3075-->1<!--/v8-->/<!--v8:3076-->2<!--/v8--> | <!--v8:3077-->0.5<!--/v8--> | <!--v8:3078-->1581<!--/v8-->/<!--v8:3079-->1974<!--/v8--> | <!--v8:3080-->0.800912<!--/v8--> |
| ts-train-service / delay | B4/w15/k2 | <!--v8:3081-->3<!--/v8-->/<!--v8:3082-->3<!--/v8--> | <!--v8:3083-->1<!--/v8--> | <!--v8:3084-->1676<!--/v8-->/<!--v8:3085-->1972<!--/v8--> | <!--v8:3086-->0.849899<!--/v8--> |
| ts-travel-service / disk | B4/w15/k2 | <!--v8:3087-->2<!--/v8-->/<!--v8:3088-->3<!--/v8--> | <!--v8:3089-->0.666667<!--/v8--> | <!--v8:3090-->1399<!--/v8-->/<!--v8:3091-->1961<!--/v8--> | <!--v8:3092-->0.713412<!--/v8--> |
| ts-travel-service / loss | B4/w15/k2 | <!--v8:3093-->2<!--/v8-->/<!--v8:3094-->3<!--/v8--> | <!--v8:3095-->0.666667<!--/v8--> | <!--v8:3096-->1587<!--/v8-->/<!--v8:3097-->1966<!--/v8--> | <!--v8:3098-->0.807223<!--/v8--> |
| all | B4/w15/k3 | <!--v8:3099-->14<!--/v8-->/<!--v8:3100-->27<!--/v8--> | <!--v8:3101-->0.518519<!--/v8--> | <!--v8:3102-->8810<!--/v8-->/<!--v8:3103-->19666<!--/v8--> | <!--v8:3104-->0.447981<!--/v8--> |
| ts-auth-service / cpu | B4/w15/k3 | <!--v8:3105-->1<!--/v8-->/<!--v8:3106-->2<!--/v8--> | <!--v8:3107-->0.5<!--/v8--> | <!--v8:3108-->902<!--/v8-->/<!--v8:3109-->1958<!--/v8--> | <!--v8:3110-->0.460674<!--/v8--> |
| ts-auth-service / delay | B4/w15/k3 | <!--v8:3111-->2<!--/v8-->/<!--v8:3112-->3<!--/v8--> | <!--v8:3113-->0.666667<!--/v8--> | <!--v8:3114-->833<!--/v8-->/<!--v8:3115-->1969<!--/v8--> | <!--v8:3116-->0.423057<!--/v8--> |
| ts-order-service / disk | B4/w15/k3 | <!--v8:3117-->1<!--/v8-->/<!--v8:3118-->3<!--/v8--> | <!--v8:3119-->0.333333<!--/v8--> | <!--v8:3120-->807<!--/v8-->/<!--v8:3121-->1955<!--/v8--> | <!--v8:3122-->0.412788<!--/v8--> |
| ts-order-service / loss | B4/w15/k3 | <!--v8:3123-->1<!--/v8-->/<!--v8:3124-->2<!--/v8--> | <!--v8:3125-->0.5<!--/v8--> | <!--v8:3126-->701<!--/v8-->/<!--v8:3127-->1965<!--/v8--> | <!--v8:3128-->0.356743<!--/v8--> |
| ts-route-service / mem | B4/w15/k3 | <!--v8:3129-->1<!--/v8-->/<!--v8:3130-->3<!--/v8--> | <!--v8:3131-->0.333333<!--/v8--> | <!--v8:3132-->650<!--/v8-->/<!--v8:3133-->1973<!--/v8--> | <!--v8:3134-->0.329448<!--/v8--> |
| ts-route-service / socket | B4/w15/k3 | <!--v8:3135-->2<!--/v8-->/<!--v8:3136-->3<!--/v8--> | <!--v8:3137-->0.666667<!--/v8--> | <!--v8:3138-->849<!--/v8-->/<!--v8:3139-->1973<!--/v8--> | <!--v8:3140-->0.430309<!--/v8--> |
| ts-train-service / cpu | B4/w15/k3 | <!--v8:3141-->1<!--/v8-->/<!--v8:3142-->2<!--/v8--> | <!--v8:3143-->0.5<!--/v8--> | <!--v8:3144-->1036<!--/v8-->/<!--v8:3145-->1974<!--/v8--> | <!--v8:3146-->0.524823<!--/v8--> |
| ts-train-service / delay | B4/w15/k3 | <!--v8:3147-->2<!--/v8-->/<!--v8:3148-->3<!--/v8--> | <!--v8:3149-->0.666667<!--/v8--> | <!--v8:3150-->1216<!--/v8-->/<!--v8:3151-->1972<!--/v8--> | <!--v8:3152-->0.616633<!--/v8--> |
| ts-travel-service / disk | B4/w15/k3 | <!--v8:3153-->2<!--/v8-->/<!--v8:3154-->3<!--/v8--> | <!--v8:3155-->0.666667<!--/v8--> | <!--v8:3156-->908<!--/v8-->/<!--v8:3157-->1961<!--/v8--> | <!--v8:3158-->0.463029<!--/v8--> |
| ts-travel-service / loss | B4/w15/k3 | <!--v8:3159-->1<!--/v8-->/<!--v8:3160-->3<!--/v8--> | <!--v8:3161-->0.333333<!--/v8--> | <!--v8:3162-->908<!--/v8-->/<!--v8:3163-->1966<!--/v8--> | <!--v8:3164-->0.461851<!--/v8--> |
| all | B4/w15/k5 | <!--v8:3165-->8<!--/v8-->/<!--v8:3166-->27<!--/v8--> | <!--v8:3167-->0.296296<!--/v8--> | <!--v8:3168-->4278<!--/v8-->/<!--v8:3169-->19666<!--/v8--> | <!--v8:3170-->0.217533<!--/v8--> |
| ts-auth-service / cpu | B4/w15/k5 | <!--v8:3171-->0<!--/v8-->/<!--v8:3172-->2<!--/v8--> | <!--v8:3173-->0<!--/v8--> | <!--v8:3174-->411<!--/v8-->/<!--v8:3175-->1958<!--/v8--> | <!--v8:3176-->0.209908<!--/v8--> |
| ts-auth-service / delay | B4/w15/k5 | <!--v8:3177-->1<!--/v8-->/<!--v8:3178-->3<!--/v8--> | <!--v8:3179-->0.333333<!--/v8--> | <!--v8:3180-->406<!--/v8-->/<!--v8:3181-->1969<!--/v8--> | <!--v8:3182-->0.206196<!--/v8--> |
| ts-order-service / disk | B4/w15/k5 | <!--v8:3183-->1<!--/v8-->/<!--v8:3184-->3<!--/v8--> | <!--v8:3185-->0.333333<!--/v8--> | <!--v8:3186-->412<!--/v8-->/<!--v8:3187-->1955<!--/v8--> | <!--v8:3188-->0.210742<!--/v8--> |
| ts-order-service / loss | B4/w15/k5 | <!--v8:3189-->0<!--/v8-->/<!--v8:3190-->2<!--/v8--> | <!--v8:3191-->0<!--/v8--> | <!--v8:3192-->311<!--/v8-->/<!--v8:3193-->1965<!--/v8--> | <!--v8:3194-->0.15827<!--/v8--> |
| ts-route-service / mem | B4/w15/k5 | <!--v8:3195-->1<!--/v8-->/<!--v8:3196-->3<!--/v8--> | <!--v8:3197-->0.333333<!--/v8--> | <!--v8:3198-->318<!--/v8-->/<!--v8:3199-->1973<!--/v8--> | <!--v8:3200-->0.161176<!--/v8--> |
| ts-route-service / socket | B4/w15/k5 | <!--v8:3201-->2<!--/v8-->/<!--v8:3202-->3<!--/v8--> | <!--v8:3203-->0.666667<!--/v8--> | <!--v8:3204-->510<!--/v8-->/<!--v8:3205-->1973<!--/v8--> | <!--v8:3206-->0.25849<!--/v8--> |
| ts-train-service / cpu | B4/w15/k5 | <!--v8:3207-->1<!--/v8-->/<!--v8:3208-->2<!--/v8--> | <!--v8:3209-->0.5<!--/v8--> | <!--v8:3210-->442<!--/v8-->/<!--v8:3211-->1974<!--/v8--> | <!--v8:3212-->0.223911<!--/v8--> |
| ts-train-service / delay | B4/w15/k5 | <!--v8:3213-->0<!--/v8-->/<!--v8:3214-->3<!--/v8--> | <!--v8:3215-->0<!--/v8--> | <!--v8:3216-->610<!--/v8-->/<!--v8:3217-->1972<!--/v8--> | <!--v8:3218-->0.309331<!--/v8--> |
| ts-travel-service / disk | B4/w15/k5 | <!--v8:3219-->2<!--/v8-->/<!--v8:3220-->3<!--/v8--> | <!--v8:3221-->0.666667<!--/v8--> | <!--v8:3222-->580<!--/v8-->/<!--v8:3223-->1961<!--/v8--> | <!--v8:3224-->0.295767<!--/v8--> |
| ts-travel-service / loss | B4/w15/k5 | <!--v8:3225-->0<!--/v8-->/<!--v8:3226-->3<!--/v8--> | <!--v8:3227-->0<!--/v8--> | <!--v8:3228-->278<!--/v8-->/<!--v8:3229-->1966<!--/v8--> | <!--v8:3230-->0.141404<!--/v8--> |
| all | B4/w30/k2 | <!--v8:3231-->24<!--/v8-->/<!--v8:3232-->27<!--/v8--> | <!--v8:3233-->0.888889<!--/v8--> | <!--v8:3234-->16726<!--/v8-->/<!--v8:3235-->18769<!--/v8--> | <!--v8:3236-->0.89115<!--/v8--> |
| ts-auth-service / cpu | B4/w30/k2 | <!--v8:3237-->2<!--/v8-->/<!--v8:3238-->2<!--/v8--> | <!--v8:3239-->1<!--/v8--> | <!--v8:3240-->1784<!--/v8-->/<!--v8:3241-->1870<!--/v8--> | <!--v8:3242-->0.954011<!--/v8--> |
| ts-auth-service / delay | B4/w30/k2 | <!--v8:3243-->3<!--/v8-->/<!--v8:3244-->3<!--/v8--> | <!--v8:3245-->1<!--/v8--> | <!--v8:3246-->1631<!--/v8-->/<!--v8:3247-->1879<!--/v8--> | <!--v8:3248-->0.868015<!--/v8--> |
| ts-order-service / disk | B4/w30/k2 | <!--v8:3249-->3<!--/v8-->/<!--v8:3250-->3<!--/v8--> | <!--v8:3251-->1<!--/v8--> | <!--v8:3252-->1532<!--/v8-->/<!--v8:3253-->1866<!--/v8--> | <!--v8:3254-->0.821008<!--/v8--> |
| ts-order-service / loss | B4/w30/k2 | <!--v8:3255-->2<!--/v8-->/<!--v8:3256-->2<!--/v8--> | <!--v8:3257-->1<!--/v8--> | <!--v8:3258-->1521<!--/v8-->/<!--v8:3259-->1875<!--/v8--> | <!--v8:3260-->0.8112<!--/v8--> |
| ts-route-service / mem | B4/w30/k2 | <!--v8:3261-->3<!--/v8-->/<!--v8:3262-->3<!--/v8--> | <!--v8:3263-->1<!--/v8--> | <!--v8:3264-->1541<!--/v8-->/<!--v8:3265-->1883<!--/v8--> | <!--v8:3266-->0.818375<!--/v8--> |
| ts-route-service / socket | B4/w30/k2 | <!--v8:3267-->2<!--/v8-->/<!--v8:3268-->3<!--/v8--> | <!--v8:3269-->0.666667<!--/v8--> | <!--v8:3270-->1631<!--/v8-->/<!--v8:3271-->1883<!--/v8--> | <!--v8:3272-->0.866171<!--/v8--> |
| ts-train-service / cpu | B4/w30/k2 | <!--v8:3273-->1<!--/v8-->/<!--v8:3274-->2<!--/v8--> | <!--v8:3275-->0.5<!--/v8--> | <!--v8:3276-->1805<!--/v8-->/<!--v8:3277-->1884<!--/v8--> | <!--v8:3278-->0.958068<!--/v8--> |
| ts-train-service / delay | B4/w30/k2 | <!--v8:3279-->3<!--/v8-->/<!--v8:3280-->3<!--/v8--> | <!--v8:3281-->1<!--/v8--> | <!--v8:3282-->1812<!--/v8-->/<!--v8:3283-->1882<!--/v8--> | <!--v8:3284-->0.962806<!--/v8--> |
| ts-travel-service / disk | B4/w30/k2 | <!--v8:3285-->2<!--/v8-->/<!--v8:3286-->3<!--/v8--> | <!--v8:3287-->0.666667<!--/v8--> | <!--v8:3288-->1698<!--/v8-->/<!--v8:3289-->1871<!--/v8--> | <!--v8:3290-->0.907536<!--/v8--> |
| ts-travel-service / loss | B4/w30/k2 | <!--v8:3291-->3<!--/v8-->/<!--v8:3292-->3<!--/v8--> | <!--v8:3293-->1<!--/v8--> | <!--v8:3294-->1771<!--/v8-->/<!--v8:3295-->1876<!--/v8--> | <!--v8:3296-->0.94403<!--/v8--> |
| all | B4/w30/k3 | <!--v8:3297-->20<!--/v8-->/<!--v8:3298-->27<!--/v8--> | <!--v8:3299-->0.740741<!--/v8--> | <!--v8:3300-->12235<!--/v8-->/<!--v8:3301-->18769<!--/v8--> | <!--v8:3302-->0.651873<!--/v8--> |
| ts-auth-service / cpu | B4/w30/k3 | <!--v8:3303-->2<!--/v8-->/<!--v8:3304-->2<!--/v8--> | <!--v8:3305-->1<!--/v8--> | <!--v8:3306-->1280<!--/v8-->/<!--v8:3307-->1870<!--/v8--> | <!--v8:3308-->0.684492<!--/v8--> |
| ts-auth-service / delay | B4/w30/k3 | <!--v8:3309-->2<!--/v8-->/<!--v8:3310-->3<!--/v8--> | <!--v8:3311-->0.666667<!--/v8--> | <!--v8:3312-->1199<!--/v8-->/<!--v8:3313-->1879<!--/v8--> | <!--v8:3314-->0.638105<!--/v8--> |
| ts-order-service / disk | B4/w30/k3 | <!--v8:3315-->3<!--/v8-->/<!--v8:3316-->3<!--/v8--> | <!--v8:3317-->1<!--/v8--> | <!--v8:3318-->1081<!--/v8-->/<!--v8:3319-->1866<!--/v8--> | <!--v8:3320-->0.579314<!--/v8--> |
| ts-order-service / loss | B4/w30/k3 | <!--v8:3321-->2<!--/v8-->/<!--v8:3322-->2<!--/v8--> | <!--v8:3323-->1<!--/v8--> | <!--v8:3324-->1027<!--/v8-->/<!--v8:3325-->1875<!--/v8--> | <!--v8:3326-->0.547733<!--/v8--> |
| ts-route-service / mem | B4/w30/k3 | <!--v8:3327-->1<!--/v8-->/<!--v8:3328-->3<!--/v8--> | <!--v8:3329-->0.333333<!--/v8--> | <!--v8:3330-->978<!--/v8-->/<!--v8:3331-->1883<!--/v8--> | <!--v8:3332-->0.519384<!--/v8--> |
| ts-route-service / socket | B4/w30/k3 | <!--v8:3333-->2<!--/v8-->/<!--v8:3334-->3<!--/v8--> | <!--v8:3335-->0.666667<!--/v8--> | <!--v8:3336-->1280<!--/v8-->/<!--v8:3337-->1883<!--/v8--> | <!--v8:3338-->0.679766<!--/v8--> |
| ts-train-service / cpu | B4/w30/k3 | <!--v8:3339-->1<!--/v8-->/<!--v8:3340-->2<!--/v8--> | <!--v8:3341-->0.5<!--/v8--> | <!--v8:3342-->1446<!--/v8-->/<!--v8:3343-->1884<!--/v8--> | <!--v8:3344-->0.767516<!--/v8--> |
| ts-train-service / delay | B4/w30/k3 | <!--v8:3345-->3<!--/v8-->/<!--v8:3346-->3<!--/v8--> | <!--v8:3347-->1<!--/v8--> | <!--v8:3348-->1520<!--/v8-->/<!--v8:3349-->1882<!--/v8--> | <!--v8:3350-->0.807651<!--/v8--> |
| ts-travel-service / disk | B4/w30/k3 | <!--v8:3351-->2<!--/v8-->/<!--v8:3352-->3<!--/v8--> | <!--v8:3353-->0.666667<!--/v8--> | <!--v8:3354-->1160<!--/v8-->/<!--v8:3355-->1871<!--/v8--> | <!--v8:3356-->0.619989<!--/v8--> |
| ts-travel-service / loss | B4/w30/k3 | <!--v8:3357-->2<!--/v8-->/<!--v8:3358-->3<!--/v8--> | <!--v8:3359-->0.666667<!--/v8--> | <!--v8:3360-->1264<!--/v8-->/<!--v8:3361-->1876<!--/v8--> | <!--v8:3362-->0.673774<!--/v8--> |
| all | B4/w30/k5 | <!--v8:3363-->11<!--/v8-->/<!--v8:3364-->27<!--/v8--> | <!--v8:3365-->0.407407<!--/v8--> | <!--v8:3366-->6379<!--/v8-->/<!--v8:3367-->18769<!--/v8--> | <!--v8:3368-->0.339869<!--/v8--> |
| ts-auth-service / cpu | B4/w30/k5 | <!--v8:3369-->1<!--/v8-->/<!--v8:3370-->2<!--/v8--> | <!--v8:3371-->0.5<!--/v8--> | <!--v8:3372-->667<!--/v8-->/<!--v8:3373-->1870<!--/v8--> | <!--v8:3374-->0.356684<!--/v8--> |
| ts-auth-service / delay | B4/w30/k5 | <!--v8:3375-->2<!--/v8-->/<!--v8:3376-->3<!--/v8--> | <!--v8:3377-->0.666667<!--/v8--> | <!--v8:3378-->715<!--/v8-->/<!--v8:3379-->1879<!--/v8--> | <!--v8:3380-->0.380522<!--/v8--> |
| ts-order-service / disk | B4/w30/k5 | <!--v8:3381-->1<!--/v8-->/<!--v8:3382-->3<!--/v8--> | <!--v8:3383-->0.333333<!--/v8--> | <!--v8:3384-->661<!--/v8-->/<!--v8:3385-->1866<!--/v8--> | <!--v8:3386-->0.354234<!--/v8--> |
| ts-order-service / loss | B4/w30/k5 | <!--v8:3387-->0<!--/v8-->/<!--v8:3388-->2<!--/v8--> | <!--v8:3389-->0<!--/v8--> | <!--v8:3390-->569<!--/v8-->/<!--v8:3391-->1875<!--/v8--> | <!--v8:3392-->0.303467<!--/v8--> |
| ts-route-service / mem | B4/w30/k5 | <!--v8:3393-->1<!--/v8-->/<!--v8:3394-->3<!--/v8--> | <!--v8:3395-->0.333333<!--/v8--> | <!--v8:3396-->410<!--/v8-->/<!--v8:3397-->1883<!--/v8--> | <!--v8:3398-->0.217738<!--/v8--> |
| ts-route-service / socket | B4/w30/k5 | <!--v8:3399-->1<!--/v8-->/<!--v8:3400-->3<!--/v8--> | <!--v8:3401-->0.333333<!--/v8--> | <!--v8:3402-->624<!--/v8-->/<!--v8:3403-->1883<!--/v8--> | <!--v8:3404-->0.331386<!--/v8--> |
| ts-train-service / cpu | B4/w30/k5 | <!--v8:3405-->0<!--/v8-->/<!--v8:3406-->2<!--/v8--> | <!--v8:3407-->0<!--/v8--> | <!--v8:3408-->702<!--/v8-->/<!--v8:3409-->1884<!--/v8--> | <!--v8:3410-->0.372611<!--/v8--> |
| ts-train-service / delay | B4/w30/k5 | <!--v8:3411-->2<!--/v8-->/<!--v8:3412-->3<!--/v8--> | <!--v8:3413-->0.666667<!--/v8--> | <!--v8:3414-->842<!--/v8-->/<!--v8:3415-->1882<!--/v8--> | <!--v8:3416-->0.447396<!--/v8--> |
| ts-travel-service / disk | B4/w30/k5 | <!--v8:3417-->1<!--/v8-->/<!--v8:3418-->3<!--/v8--> | <!--v8:3419-->0.333333<!--/v8--> | <!--v8:3420-->696<!--/v8-->/<!--v8:3421-->1871<!--/v8--> | <!--v8:3422-->0.371994<!--/v8--> |
| ts-travel-service / loss | B4/w30/k5 | <!--v8:3423-->2<!--/v8-->/<!--v8:3424-->3<!--/v8--> | <!--v8:3425-->0.666667<!--/v8--> | <!--v8:3426-->493<!--/v8-->/<!--v8:3427-->1876<!--/v8--> | <!--v8:3428-->0.262793<!--/v8--> |
| all | B4/w60/k2 | <!--v8:3429-->23<!--/v8-->/<!--v8:3430-->24<!--/v8--> | <!--v8:3431-->0.958333<!--/v8--> | <!--v8:3432-->16013<!--/v8-->/<!--v8:3433-->16987<!--/v8--> | <!--v8:3434-->0.942662<!--/v8--> |
| ts-auth-service / cpu | B4/w60/k2 | <!--v8:3435-->2<!--/v8-->/<!--v8:3436-->2<!--/v8--> | <!--v8:3437-->1<!--/v8--> | <!--v8:3438-->1660<!--/v8-->/<!--v8:3439-->1694<!--/v8--> | <!--v8:3440-->0.979929<!--/v8--> |
| ts-auth-service / delay | B4/w60/k2 | <!--v8:3441-->3<!--/v8-->/<!--v8:3442-->3<!--/v8--> | <!--v8:3443-->1<!--/v8--> | <!--v8:3444-->1583<!--/v8-->/<!--v8:3445-->1699<!--/v8--> | <!--v8:3446-->0.931725<!--/v8--> |
| ts-order-service / disk | B4/w60/k2 | <!--v8:3447-->3<!--/v8-->/<!--v8:3448-->3<!--/v8--> | <!--v8:3449-->1<!--/v8--> | <!--v8:3450-->1458<!--/v8-->/<!--v8:3451-->1688<!--/v8--> | <!--v8:3452-->0.863744<!--/v8--> |
| ts-order-service / loss | B4/w60/k2 | <!--v8:3453-->2<!--/v8-->/<!--v8:3454-->2<!--/v8--> | <!--v8:3455-->1<!--/v8--> | <!--v8:3456-->1526<!--/v8-->/<!--v8:3457-->1697<!--/v8--> | <!--v8:3458-->0.899234<!--/v8--> |
| ts-route-service / mem | B4/w60/k2 | <!--v8:3459-->2<!--/v8-->/<!--v8:3460-->3<!--/v8--> | <!--v8:3461-->0.666667<!--/v8--> | <!--v8:3462-->1564<!--/v8-->/<!--v8:3463-->1704<!--/v8--> | <!--v8:3464-->0.91784<!--/v8--> |
| ts-route-service / socket | B4/w60/k2 | <!--v8:3465-->2<!--/v8-->/<!--v8:3466-->2<!--/v8--> | <!--v8:3467-->1<!--/v8--> | <!--v8:3468-->1606<!--/v8-->/<!--v8:3469-->1705<!--/v8--> | <!--v8:3470-->0.941935<!--/v8--> |
| ts-train-service / cpu | B4/w60/k2 | <!--v8:3471-->2<!--/v8-->/<!--v8:3472-->2<!--/v8--> | <!--v8:3473-->1<!--/v8--> | <!--v8:3474-->1694<!--/v8-->/<!--v8:3475-->1705<!--/v8--> | <!--v8:3476-->0.993548<!--/v8--> |
| ts-train-service / delay | B4/w60/k2 | <!--v8:3477-->2<!--/v8-->/<!--v8:3478-->2<!--/v8--> | <!--v8:3479-->1<!--/v8--> | <!--v8:3480-->1658<!--/v8-->/<!--v8:3481-->1703<!--/v8--> | <!--v8:3482-->0.973576<!--/v8--> |
| ts-travel-service / disk | B4/w60/k2 | <!--v8:3483-->3<!--/v8-->/<!--v8:3484-->3<!--/v8--> | <!--v8:3485-->1<!--/v8--> | <!--v8:3486-->1608<!--/v8-->/<!--v8:3487-->1693<!--/v8--> | <!--v8:3488-->0.949793<!--/v8--> |
| ts-travel-service / loss | B4/w60/k2 | <!--v8:3489-->2<!--/v8-->/<!--v8:3490-->2<!--/v8--> | <!--v8:3491-->1<!--/v8--> | <!--v8:3492-->1656<!--/v8-->/<!--v8:3493-->1699<!--/v8--> | <!--v8:3494-->0.974691<!--/v8--> |
| all | B4/w60/k3 | <!--v8:3495-->20<!--/v8-->/<!--v8:3496-->24<!--/v8--> | <!--v8:3497-->0.833333<!--/v8--> | <!--v8:3498-->12532<!--/v8-->/<!--v8:3499-->16987<!--/v8--> | <!--v8:3500-->0.737741<!--/v8--> |
| ts-auth-service / cpu | B4/w60/k3 | <!--v8:3501-->2<!--/v8-->/<!--v8:3502-->2<!--/v8--> | <!--v8:3503-->1<!--/v8--> | <!--v8:3504-->1260<!--/v8-->/<!--v8:3505-->1694<!--/v8--> | <!--v8:3506-->0.743802<!--/v8--> |
| ts-auth-service / delay | B4/w60/k3 | <!--v8:3507-->2<!--/v8-->/<!--v8:3508-->3<!--/v8--> | <!--v8:3509-->0.666667<!--/v8--> | <!--v8:3510-->1288<!--/v8-->/<!--v8:3511-->1699<!--/v8--> | <!--v8:3512-->0.758093<!--/v8--> |
| ts-order-service / disk | B4/w60/k3 | <!--v8:3513-->3<!--/v8-->/<!--v8:3514-->3<!--/v8--> | <!--v8:3515-->1<!--/v8--> | <!--v8:3516-->1036<!--/v8-->/<!--v8:3517-->1688<!--/v8--> | <!--v8:3518-->0.613744<!--/v8--> |
| ts-order-service / loss | B4/w60/k3 | <!--v8:3519-->1<!--/v8-->/<!--v8:3520-->2<!--/v8--> | <!--v8:3521-->0.5<!--/v8--> | <!--v8:3522-->1046<!--/v8-->/<!--v8:3523-->1697<!--/v8--> | <!--v8:3524-->0.616382<!--/v8--> |
| ts-route-service / mem | B4/w60/k3 | <!--v8:3525-->2<!--/v8-->/<!--v8:3526-->3<!--/v8--> | <!--v8:3527-->0.666667<!--/v8--> | <!--v8:3528-->1139<!--/v8-->/<!--v8:3529-->1704<!--/v8--> | <!--v8:3530-->0.668427<!--/v8--> |
| ts-route-service / socket | B4/w60/k3 | <!--v8:3531-->2<!--/v8-->/<!--v8:3532-->2<!--/v8--> | <!--v8:3533-->1<!--/v8--> | <!--v8:3534-->1346<!--/v8-->/<!--v8:3535-->1705<!--/v8--> | <!--v8:3536-->0.789443<!--/v8--> |
| ts-train-service / cpu | B4/w60/k3 | <!--v8:3537-->1<!--/v8-->/<!--v8:3538-->2<!--/v8--> | <!--v8:3539-->0.5<!--/v8--> | <!--v8:3540-->1475<!--/v8-->/<!--v8:3541-->1705<!--/v8--> | <!--v8:3542-->0.865103<!--/v8--> |
| ts-train-service / delay | B4/w60/k3 | <!--v8:3543-->2<!--/v8-->/<!--v8:3544-->2<!--/v8--> | <!--v8:3545-->1<!--/v8--> | <!--v8:3546-->1401<!--/v8-->/<!--v8:3547-->1703<!--/v8--> | <!--v8:3548-->0.822666<!--/v8--> |
| ts-travel-service / disk | B4/w60/k3 | <!--v8:3549-->3<!--/v8-->/<!--v8:3550-->3<!--/v8--> | <!--v8:3551-->1<!--/v8--> | <!--v8:3552-->1233<!--/v8-->/<!--v8:3553-->1693<!--/v8--> | <!--v8:3554-->0.728293<!--/v8--> |
| ts-travel-service / loss | B4/w60/k3 | <!--v8:3555-->2<!--/v8-->/<!--v8:3556-->2<!--/v8--> | <!--v8:3557-->1<!--/v8--> | <!--v8:3558-->1308<!--/v8-->/<!--v8:3559-->1699<!--/v8--> | <!--v8:3560-->0.769865<!--/v8--> |
| all | B4/w60/k5 | <!--v8:3561-->11<!--/v8-->/<!--v8:3562-->24<!--/v8--> | <!--v8:3563-->0.458333<!--/v8--> | <!--v8:3564-->6354<!--/v8-->/<!--v8:3565-->16987<!--/v8--> | <!--v8:3566-->0.374051<!--/v8--> |
| ts-auth-service / cpu | B4/w60/k5 | <!--v8:3567-->1<!--/v8-->/<!--v8:3568-->2<!--/v8--> | <!--v8:3569-->0.5<!--/v8--> | <!--v8:3570-->571<!--/v8-->/<!--v8:3571-->1694<!--/v8--> | <!--v8:3572-->0.337072<!--/v8--> |
| ts-auth-service / delay | B4/w60/k5 | <!--v8:3573-->2<!--/v8-->/<!--v8:3574-->3<!--/v8--> | <!--v8:3575-->0.666667<!--/v8--> | <!--v8:3576-->767<!--/v8-->/<!--v8:3577-->1699<!--/v8--> | <!--v8:3578-->0.451442<!--/v8--> |
| ts-order-service / disk | B4/w60/k5 | <!--v8:3579-->3<!--/v8-->/<!--v8:3580-->3<!--/v8--> | <!--v8:3581-->1<!--/v8--> | <!--v8:3582-->560<!--/v8-->/<!--v8:3583-->1688<!--/v8--> | <!--v8:3584-->0.331754<!--/v8--> |
| ts-order-service / loss | B4/w60/k5 | <!--v8:3585-->0<!--/v8-->/<!--v8:3586-->2<!--/v8--> | <!--v8:3587-->0<!--/v8--> | <!--v8:3588-->595<!--/v8-->/<!--v8:3589-->1697<!--/v8--> | <!--v8:3590-->0.350619<!--/v8--> |
| ts-route-service / mem | B4/w60/k5 | <!--v8:3591-->1<!--/v8-->/<!--v8:3592-->3<!--/v8--> | <!--v8:3593-->0.333333<!--/v8--> | <!--v8:3594-->499<!--/v8-->/<!--v8:3595-->1704<!--/v8--> | <!--v8:3596-->0.29284<!--/v8--> |
| ts-route-service / socket | B4/w60/k5 | <!--v8:3597-->0<!--/v8-->/<!--v8:3598-->2<!--/v8--> | <!--v8:3599-->0<!--/v8--> | <!--v8:3600-->695<!--/v8-->/<!--v8:3601-->1705<!--/v8--> | <!--v8:3602-->0.407625<!--/v8--> |
| ts-train-service / cpu | B4/w60/k5 | <!--v8:3603-->1<!--/v8-->/<!--v8:3604-->2<!--/v8--> | <!--v8:3605-->0.5<!--/v8--> | <!--v8:3606-->759<!--/v8-->/<!--v8:3607-->1705<!--/v8--> | <!--v8:3608-->0.445161<!--/v8--> |
| ts-train-service / delay | B4/w60/k5 | <!--v8:3609-->1<!--/v8-->/<!--v8:3610-->2<!--/v8--> | <!--v8:3611-->0.5<!--/v8--> | <!--v8:3612-->802<!--/v8-->/<!--v8:3613-->1703<!--/v8--> | <!--v8:3614-->0.470934<!--/v8--> |
| ts-travel-service / disk | B4/w60/k5 | <!--v8:3615-->2<!--/v8-->/<!--v8:3616-->3<!--/v8--> | <!--v8:3617-->0.666667<!--/v8--> | <!--v8:3618-->566<!--/v8-->/<!--v8:3619-->1693<!--/v8--> | <!--v8:3620-->0.334318<!--/v8--> |
| ts-travel-service / loss | B4/w60/k5 | <!--v8:3621-->0<!--/v8-->/<!--v8:3622-->2<!--/v8--> | <!--v8:3623-->0<!--/v8--> | <!--v8:3624-->540<!--/v8-->/<!--v8:3625-->1699<!--/v8--> | <!--v8:3626-->0.317834<!--/v8--> |

Ở cấu hình chính B4, tỉ lệ tại t̂ cao hơn tỉ lệ đối chứng toàn mẫu; điều đó chưa phân xử cơ chế. Khi hạ ngưỡng ở w30/k2, dấu chênh toàn mẫu âm. Các ô có thể khác dấu; bảng tiếp giữ mọi hướng và mọi đổi chiều đã khai. Cờ phổ biến ở điểm không báo không tự thành lời giải thích. Những ca bằng nhau đúng số đã được đọc tay, gồm B4/w60/k2 ở dev-16597725c1 và dev-746fd74313; xem doc-tay.

| Phạm vi | Nhóm | Cấu hình B4 | Chênh tỉ lệ tại t̂ − đối chứng | Hướng |
|---|---|---|---|---|
| all | all — có đổi chiều | B4/w15/k2 | <!--v8:3627-->+0.019801<!--/v8--> | + |
| all | all — có đổi chiều | B4/w15/k3 | <!--v8:3628-->+0.0705372<!--/v8--> | + |
| all | all — có đổi chiều | B4/w15/k5 | <!--v8:3629-->+0.0787635<!--/v8--> | + |
| all | all — có đổi chiều | B4/w30/k2 | <!--v8:3630-->-0.00226141<!--/v8--> | - |
| all | all — có đổi chiều | B4/w30/k3 | <!--v8:3631-->+0.088868<!--/v8--> | + |
| all | all — có đổi chiều | B4/w30/k5 | <!--v8:3632-->+0.0675385<!--/v8--> | + |
| all | all — có đổi chiều | B4/w60/k2 | <!--v8:3633-->+0.0156713<!--/v8--> | + |
| all | all — có đổi chiều | B4/w60/k3 | <!--v8:3634-->+0.0955927<!--/v8--> | + |
| all | all — có đổi chiều | B4/w60/k5 | <!--v8:3635-->+0.0842826<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w15/k2 | <!--v8:3636-->-0.258938<!--/v8--> | - |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w15/k3 | <!--v8:3637-->+0.0393258<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w15/k5 | <!--v8:3638-->-0.209908<!--/v8--> | - |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w30/k2 | <!--v8:3639-->+0.0459893<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w30/k3 | <!--v8:3640-->+0.315508<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w30/k5 | <!--v8:3641-->+0.143316<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w60/k2 | <!--v8:3642-->+0.0200708<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w60/k3 | <!--v8:3643-->+0.256198<!--/v8--> | + |
| cell | ts-auth-service / cpu — có đổi chiều | B4/w60/k5 | <!--v8:3644-->+0.162928<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w15/k2 | <!--v8:3645-->+0.31742<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w15/k3 | <!--v8:3646-->+0.243609<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w15/k5 | <!--v8:3647-->+0.127137<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w30/k2 | <!--v8:3648-->+0.131985<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w30/k3 | <!--v8:3649-->+0.0285613<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w30/k5 | <!--v8:3650-->+0.286145<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w60/k2 | <!--v8:3651-->+0.0682755<!--/v8--> | + |
| cell | ts-auth-service / delay — có đổi chiều | B4/w60/k3 | <!--v8:3652-->-0.0914263<!--/v8--> | - |
| cell | ts-auth-service / delay — có đổi chiều | B4/w60/k5 | <!--v8:3653-->+0.215225<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w15/k2 | <!--v8:3654-->+0.334015<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w15/k3 | <!--v8:3655-->-0.0794544<!--/v8--> | - |
| cell | ts-order-service / disk — có đổi chiều | B4/w15/k5 | <!--v8:3656-->+0.122592<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w30/k2 | <!--v8:3657-->+0.178992<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w30/k3 | <!--v8:3658-->+0.420686<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w30/k5 | <!--v8:3659-->-0.0209003<!--/v8--> | - |
| cell | ts-order-service / disk — có đổi chiều | B4/w60/k2 | <!--v8:3660-->+0.136256<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w60/k3 | <!--v8:3661-->+0.386256<!--/v8--> | + |
| cell | ts-order-service / disk — có đổi chiều | B4/w60/k5 | <!--v8:3662-->+0.668246<!--/v8--> | + |
| cell | ts-order-service / loss — có đổi chiều | B4/w15/k2 | <!--v8:3663-->+0.401527<!--/v8--> | + |
| cell | ts-order-service / loss — có đổi chiều | B4/w15/k3 | <!--v8:3664-->+0.143257<!--/v8--> | + |
| cell | ts-order-service / loss — có đổi chiều | B4/w15/k5 | <!--v8:3665-->-0.15827<!--/v8--> | - |
| cell | ts-order-service / loss — có đổi chiều | B4/w30/k2 | <!--v8:3666-->+0.1888<!--/v8--> | + |
| cell | ts-order-service / loss — có đổi chiều | B4/w30/k3 | <!--v8:3667-->+0.452267<!--/v8--> | + |
| cell | ts-order-service / loss — có đổi chiều | B4/w30/k5 | <!--v8:3668-->-0.303467<!--/v8--> | - |
| cell | ts-order-service / loss — có đổi chiều | B4/w60/k2 | <!--v8:3669-->+0.100766<!--/v8--> | + |
| cell | ts-order-service / loss — có đổi chiều | B4/w60/k3 | <!--v8:3670-->-0.116382<!--/v8--> | - |
| cell | ts-order-service / loss — có đổi chiều | B4/w60/k5 | <!--v8:3671-->-0.350619<!--/v8--> | - |
| cell | ts-route-service / mem — có đổi chiều | B4/w15/k2 | <!--v8:3672-->-0.314411<!--/v8--> | - |
| cell | ts-route-service / mem — có đổi chiều | B4/w15/k3 | <!--v8:3673-->+0.00388579<!--/v8--> | + |
| cell | ts-route-service / mem — có đổi chiều | B4/w15/k5 | <!--v8:3674-->+0.172157<!--/v8--> | + |
| cell | ts-route-service / mem — có đổi chiều | B4/w30/k2 | <!--v8:3675-->+0.181625<!--/v8--> | + |
| cell | ts-route-service / mem — có đổi chiều | B4/w30/k3 | <!--v8:3676-->-0.186051<!--/v8--> | - |
| cell | ts-route-service / mem — có đổi chiều | B4/w30/k5 | <!--v8:3677-->+0.115596<!--/v8--> | + |
| cell | ts-route-service / mem — có đổi chiều | B4/w60/k2 | <!--v8:3678-->-0.251174<!--/v8--> | - |
| cell | ts-route-service / mem — có đổi chiều | B4/w60/k3 | <!--v8:3679-->-0.00176056<!--/v8--> | - |
| cell | ts-route-service / mem — có đổi chiều | B4/w60/k5 | <!--v8:3680-->+0.040493<!--/v8--> | + |
| cell | ts-route-service / socket — có đổi chiều | B4/w15/k2 | <!--v8:3681-->-0.0170637<!--/v8--> | - |
| cell | ts-route-service / socket — có đổi chiều | B4/w15/k3 | <!--v8:3682-->+0.236357<!--/v8--> | + |
| cell | ts-route-service / socket — có đổi chiều | B4/w15/k5 | <!--v8:3683-->+0.408177<!--/v8--> | + |
| cell | ts-route-service / socket — có đổi chiều | B4/w30/k2 | <!--v8:3684-->-0.199504<!--/v8--> | - |
| cell | ts-route-service / socket — có đổi chiều | B4/w30/k3 | <!--v8:3685-->-0.0130997<!--/v8--> | - |
| cell | ts-route-service / socket — có đổi chiều | B4/w30/k5 | <!--v8:3686-->+0.00194725<!--/v8--> | + |
| cell | ts-route-service / socket — có đổi chiều | B4/w60/k2 | <!--v8:3687-->+0.0580645<!--/v8--> | + |
| cell | ts-route-service / socket — có đổi chiều | B4/w60/k3 | <!--v8:3688-->+0.210557<!--/v8--> | + |
| cell | ts-route-service / socket — có đổi chiều | B4/w60/k5 | <!--v8:3689-->-0.407625<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w15/k2 | <!--v8:3690-->-0.300912<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w15/k3 | <!--v8:3691-->-0.0248227<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w15/k5 | <!--v8:3692-->+0.276089<!--/v8--> | + |
| cell | ts-train-service / cpu — có đổi chiều | B4/w30/k2 | <!--v8:3693-->-0.458068<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w30/k3 | <!--v8:3694-->-0.267516<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w30/k5 | <!--v8:3695-->-0.372611<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w60/k2 | <!--v8:3696-->+0.00645161<!--/v8--> | + |
| cell | ts-train-service / cpu — có đổi chiều | B4/w60/k3 | <!--v8:3697-->-0.365103<!--/v8--> | - |
| cell | ts-train-service / cpu — có đổi chiều | B4/w60/k5 | <!--v8:3698-->+0.0548387<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w15/k2 | <!--v8:3699-->+0.150101<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w15/k3 | <!--v8:3700-->+0.0500338<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w15/k5 | <!--v8:3701-->-0.309331<!--/v8--> | - |
| cell | ts-train-service / delay — có đổi chiều | B4/w30/k2 | <!--v8:3702-->+0.0371945<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w30/k3 | <!--v8:3703-->+0.192349<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w30/k5 | <!--v8:3704-->+0.21927<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w60/k2 | <!--v8:3705-->+0.026424<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w60/k3 | <!--v8:3706-->+0.177334<!--/v8--> | + |
| cell | ts-train-service / delay — có đổi chiều | B4/w60/k5 | <!--v8:3707-->+0.0290664<!--/v8--> | + |
| cell | ts-travel-service / disk — có đổi chiều | B4/w15/k2 | <!--v8:3708-->-0.0467449<!--/v8--> | - |
| cell | ts-travel-service / disk — có đổi chiều | B4/w15/k3 | <!--v8:3709-->+0.203638<!--/v8--> | + |
| cell | ts-travel-service / disk — có đổi chiều | B4/w15/k5 | <!--v8:3710-->+0.370899<!--/v8--> | + |
| cell | ts-travel-service / disk — có đổi chiều | B4/w30/k2 | <!--v8:3711-->-0.240869<!--/v8--> | - |
| cell | ts-travel-service / disk — có đổi chiều | B4/w30/k3 | <!--v8:3712-->+0.0466774<!--/v8--> | + |
| cell | ts-travel-service / disk — có đổi chiều | B4/w30/k5 | <!--v8:3713-->-0.0386603<!--/v8--> | - |
| cell | ts-travel-service / disk — có đổi chiều | B4/w60/k2 | <!--v8:3714-->+0.0502067<!--/v8--> | + |
| cell | ts-travel-service / disk — có đổi chiều | B4/w60/k3 | <!--v8:3715-->+0.271707<!--/v8--> | + |
| cell | ts-travel-service / disk — có đổi chiều | B4/w60/k5 | <!--v8:3716-->+0.332349<!--/v8--> | + |
| cell | ts-travel-service / loss — có đổi chiều | B4/w15/k2 | <!--v8:3717-->-0.140556<!--/v8--> | - |
| cell | ts-travel-service / loss — có đổi chiều | B4/w15/k3 | <!--v8:3718-->-0.128518<!--/v8--> | - |
| cell | ts-travel-service / loss — có đổi chiều | B4/w15/k5 | <!--v8:3719-->-0.141404<!--/v8--> | - |
| cell | ts-travel-service / loss — có đổi chiều | B4/w30/k2 | <!--v8:3720-->+0.0559701<!--/v8--> | + |
| cell | ts-travel-service / loss — có đổi chiều | B4/w30/k3 | <!--v8:3721-->-0.00710732<!--/v8--> | - |
| cell | ts-travel-service / loss — có đổi chiều | B4/w30/k5 | <!--v8:3722-->+0.403873<!--/v8--> | + |
| cell | ts-travel-service / loss — có đổi chiều | B4/w60/k2 | <!--v8:3723-->+0.025309<!--/v8--> | + |
| cell | ts-travel-service / loss — có đổi chiều | B4/w60/k3 | <!--v8:3724-->+0.230135<!--/v8--> | + |
| cell | ts-travel-service / loss — có đổi chiều | B4/w60/k5 | <!--v8:3725-->-0.317834<!--/v8--> | - |
| root | ts-auth-service — có đổi chiều | B4/w15/k2 | <!--v8:3726-->+0.0793481<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w15/k3 | <!--v8:3727-->+0.158187<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w15/k5 | <!--v8:3728-->-0.00804686<!--/v8--> | - |
| root | ts-auth-service — có đổi chiều | B4/w30/k2 | <!--v8:3729-->+0.0890904<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w30/k3 | <!--v8:3730-->+0.138757<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w30/k5 | <!--v8:3731-->+0.231368<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w60/k2 | <!--v8:3732-->+0.0442087<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w60/k3 | <!--v8:3733-->+0.0490421<!--/v8--> | + |
| root | ts-auth-service — có đổi chiều | B4/w60/k5 | <!--v8:3734-->+0.205659<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w15/k2 | <!--v8:3735-->+0.367857<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w15/k3 | <!--v8:3736-->+0.0153061<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w15/k5 | <!--v8:3737-->+0.0155612<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w30/k2 | <!--v8:3738-->+0.183908<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w30/k3 | <!--v8:3739-->+0.436514<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w30/k5 | <!--v8:3740-->-0.128789<!--/v8--> | - |
| root | ts-order-service — có đổi chiều | B4/w60/k2 | <!--v8:3741-->+0.118464<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w60/k3 | <!--v8:3742-->+0.184934<!--/v8--> | + |
| root | ts-order-service — có đổi chiều | B4/w60/k5 | <!--v8:3743-->+0.258789<!--/v8--> | + |
| root | ts-route-service — có đổi chiều | B4/w15/k2 | <!--v8:3744-->-0.165737<!--/v8--> | - |
| root | ts-route-service — có đổi chiều | B4/w15/k3 | <!--v8:3745-->+0.120122<!--/v8--> | + |
| root | ts-route-service — có đổi chiều | B4/w15/k5 | <!--v8:3746-->+0.290167<!--/v8--> | + |
| root | ts-route-service — có đổi chiều | B4/w30/k2 | <!--v8:3747-->-0.00893964<!--/v8--> | - |
| root | ts-route-service — có đổi chiều | B4/w30/k3 | <!--v8:3748-->-0.0995751<!--/v8--> | - |
| root | ts-route-service — có đổi chiều | B4/w30/k5 | <!--v8:3749-->+0.0587715<!--/v8--> | + |
| root | ts-route-service — có đổi chiều | B4/w60/k2 | <!--v8:3750-->-0.129891<!--/v8--> | - |
| root | ts-route-service — có đổi chiều | B4/w60/k3 | <!--v8:3751-->+0.0710472<!--/v8--> | + |
| root | ts-route-service — có đổi chiều | B4/w60/k5 | <!--v8:3752-->-0.150249<!--/v8--> | - |
| root | ts-train-service — có đổi chiều | B4/w15/k2 | <!--v8:3753-->-0.0253928<!--/v8--> | - |
| root | ts-train-service — có đổi chiều | B4/w15/k3 | <!--v8:3754-->+0.0292955<!--/v8--> | + |
| root | ts-train-service — có đổi chiều | B4/w15/k5 | <!--v8:3755-->-0.0665991<!--/v8--> | - |
| root | ts-train-service — có đổi chiều | B4/w30/k2 | <!--v8:3756-->-0.160435<!--/v8--> | - |
| root | ts-train-service — có đổi chiều | B4/w30/k3 | <!--v8:3757-->+0.012427<!--/v8--> | + |
| root | ts-train-service — có đổi chiều | B4/w30/k5 | <!--v8:3758-->-0.00998407<!--/v8--> | - |
| root | ts-train-service — có đổi chiều | B4/w60/k2 | <!--v8:3759-->+0.0164319<!--/v8--> | + |
| root | ts-train-service — có đổi chiều | B4/w60/k3 | <!--v8:3760-->-0.0938967<!--/v8--> | - |
| root | ts-train-service — có đổi chiều | B4/w60/k5 | <!--v8:3761-->+0.0419601<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w15/k2 | <!--v8:3762-->-0.0937102<!--/v8--> | - |
| root | ts-travel-service — có đổi chiều | B4/w15/k3 | <!--v8:3763-->+0.0375605<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w15/k5 | <!--v8:3764-->+0.114846<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w30/k2 | <!--v8:3765-->-0.092474<!--/v8--> | - |
| root | ts-travel-service — có đổi chiều | B4/w30/k3 | <!--v8:3766-->+0.0197491<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w30/k5 | <!--v8:3767-->+0.182679<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w60/k2 | <!--v8:3768-->+0.0377358<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w60/k3 | <!--v8:3769-->+0.250884<!--/v8--> | + |
| root | ts-travel-service — có đổi chiều | B4/w60/k5 | <!--v8:3770-->+0.0739387<!--/v8--> | + |
| fault | cpu — có đổi chiều | B4/w15/k2 | <!--v8:3771-->-0.28001<!--/v8--> | - |
| fault | cpu — có đổi chiều | B4/w15/k3 | <!--v8:3772-->+0.00712106<!--/v8--> | + |
| fault | cpu — có đổi chiều | B4/w15/k5 | <!--v8:3773-->+0.0330621<!--/v8--> | + |
| fault | cpu — có đổi chiều | B4/w30/k2 | <!--v8:3774-->-0.206047<!--/v8--> | - |
| fault | cpu — có đổi chiều | B4/w30/k3 | <!--v8:3775-->+0.0238412<!--/v8--> | + |
| fault | cpu — có đổi chiều | B4/w30/k5 | <!--v8:3776-->-0.114678<!--/v8--> | - |
| fault | cpu — có đổi chiều | B4/w60/k2 | <!--v8:3777-->+0.0132392<!--/v8--> | + |
| fault | cpu — có đổi chiều | B4/w60/k3 | <!--v8:3778-->-0.0546484<!--/v8--> | - |
| fault | cpu — có đổi chiều | B4/w60/k5 | <!--v8:3779-->+0.108708<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w15/k2 | <!--v8:3780-->+0.233697<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w15/k3 | <!--v8:3781-->+0.146748<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w15/k5 | <!--v8:3782-->-0.0911359<!--/v8--> | - |
| fault | delay — có đổi chiều | B4/w30/k2 | <!--v8:3783-->+0.084552<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w30/k3 | <!--v8:3784-->+0.110387<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w30/k5 | <!--v8:3785-->+0.252681<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w60/k2 | <!--v8:3786-->+0.0473251<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w60/k3 | <!--v8:3787-->+0.0095826<!--/v8--> | + |
| fault | delay — có đổi chiều | B4/w60/k5 | <!--v8:3788-->+0.138801<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w15/k2 | <!--v8:3789-->+0.143599<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w15/k3 | <!--v8:3790-->+0.0620531<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w15/k5 | <!--v8:3791-->+0.24668<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w30/k2 | <!--v8:3792-->-0.0309963<!--/v8--> | - |
| fault | disk — có đổi chiều | B4/w30/k3 | <!--v8:3793-->+0.233654<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w30/k5 | <!--v8:3794-->-0.0297922<!--/v8--> | - |
| fault | disk — có đổi chiều | B4/w60/k2 | <!--v8:3795-->+0.0931677<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w60/k3 | <!--v8:3796-->+0.328897<!--/v8--> | + |
| fault | disk — có đổi chiều | B4/w60/k5 | <!--v8:3797-->+0.500296<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w15/k2 | <!--v8:3798-->+0.0971254<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w15/k3 | <!--v8:3799-->-0.00931061<!--/v8--> | - |
| fault | loss — có đổi chiều | B4/w15/k5 | <!--v8:3800-->-0.149835<!--/v8--> | - |
| fault | loss — có đổi chiều | B4/w30/k2 | <!--v8:3801-->+0.122367<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w30/k3 | <!--v8:3802-->+0.18923<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w30/k5 | <!--v8:3803-->+0.116875<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w60/k2 | <!--v8:3804-->+0.0630153<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w60/k3 | <!--v8:3805-->+0.0568316<!--/v8--> | + |
| fault | loss — có đổi chiều | B4/w60/k5 | <!--v8:3806-->-0.334217<!--/v8--> | - |
| fault | mem — có đổi chiều | B4/w15/k2 | <!--v8:3807-->-0.314411<!--/v8--> | - |
| fault | mem — có đổi chiều | B4/w15/k3 | <!--v8:3808-->+0.00388579<!--/v8--> | + |
| fault | mem — có đổi chiều | B4/w15/k5 | <!--v8:3809-->+0.172157<!--/v8--> | + |
| fault | mem — có đổi chiều | B4/w30/k2 | <!--v8:3810-->+0.181625<!--/v8--> | + |
| fault | mem — có đổi chiều | B4/w30/k3 | <!--v8:3811-->-0.186051<!--/v8--> | - |
| fault | mem — có đổi chiều | B4/w30/k5 | <!--v8:3812-->+0.115596<!--/v8--> | + |
| fault | mem — có đổi chiều | B4/w60/k2 | <!--v8:3813-->-0.251174<!--/v8--> | - |
| fault | mem — có đổi chiều | B4/w60/k3 | <!--v8:3814-->-0.00176056<!--/v8--> | - |
| fault | mem — có đổi chiều | B4/w60/k5 | <!--v8:3815-->+0.040493<!--/v8--> | + |
| fault | socket — có đổi chiều | B4/w15/k2 | <!--v8:3816-->-0.0170637<!--/v8--> | - |
| fault | socket — có đổi chiều | B4/w15/k3 | <!--v8:3817-->+0.236357<!--/v8--> | + |
| fault | socket — có đổi chiều | B4/w15/k5 | <!--v8:3818-->+0.408177<!--/v8--> | + |
| fault | socket — có đổi chiều | B4/w30/k2 | <!--v8:3819-->-0.199504<!--/v8--> | - |
| fault | socket — có đổi chiều | B4/w30/k3 | <!--v8:3820-->-0.0130997<!--/v8--> | - |
| fault | socket — có đổi chiều | B4/w30/k5 | <!--v8:3821-->+0.00194725<!--/v8--> | + |
| fault | socket — có đổi chiều | B4/w60/k2 | <!--v8:3822-->+0.0580645<!--/v8--> | + |
| fault | socket — có đổi chiều | B4/w60/k3 | <!--v8:3823-->+0.210557<!--/v8--> | + |
| fault | socket — có đổi chiều | B4/w60/k5 | <!--v8:3824-->-0.407625<!--/v8--> | - |

### N5/N6: mô tả theo ca và ô

Nguồn: `n-sigma-cot.json#/cases/<ca>/<bộ>` và `runs/report-main-001/summary.json#/NS_descriptive`. r_obs/r_ind/r_nom không tách nhân quả. r_obs≈r_ind chưa chứng minh độc lập; r_ind khác r_nom có nhiều giải thích. N5 phân loại từ hậu tố; mạng rỗng không chứng minh không có telemetry mạng vì socket/diskio/workload thuộc “khác”. N6 là mật độ từng phút sau mốc; code nền mở rộng hấp thu mọi dữ liệu đã thấy, nhưng giảm báo chưa chứng minh hấp thu gây bỏ sót.

| Ca | Bộ | r_obs | r_ind | r_nom | Tỉ lệ lịch sử đầu / giữa / cuối | Loại cột gây báo |
|---|---|---|---|---|---|---|
| dev-03d4910932 | N-Sigma chính | <!--v8:3825-->0.470968<!--/v8--> | <!--v8:3826-->0.45579<!--/v8--> | <!--v8:3827-->0.0878257<!--/v8--> | <!--v8:3828-->0.00382353<!--/v8--> / <!--v8:3829-->0.0277941<!--/v8--> / <!--v8:3830-->0.0148897<!--/v8--> | latency |
| dev-03d4910932 | N-Sigma đối chứng | <!--v8:3831-->0.996774<!--/v8--> | <!--v8:3832-->0.998939<!--/v8--> | <!--v8:3833-->0.623192<!--/v8--> | <!--v8:3834-->0.0206925<!--/v8--> / <!--v8:3835-->0.0219945<!--/v8--> / <!--v8:3836-->0.0154519<!--/v8--> | cpu, latency, mem |
| dev-12a1a88069 | N-Sigma chính | <!--v8:3837-->0.293548<!--/v8--> | <!--v8:3838-->0.330398<!--/v8--> | <!--v8:3839-->0.112157<!--/v8--> | <!--v8:3840-->0.0140909<!--/v8--> / <!--v8:3841-->0.00943182<!--/v8--> / <!--v8:3842-->0.00696023<!--/v8--> | latency |
| dev-12a1a88069 | N-Sigma đối chứng | <!--v8:3843-->0.972581<!--/v8--> | <!--v8:3844-->0.995039<!--/v8--> | <!--v8:3845-->0.633243<!--/v8--> | <!--v8:3846-->0.0180054<!--/v8--> / <!--v8:3847-->0.0161995<!--/v8--> / <!--v8:3848-->0.0112449<!--/v8--> | cpu, latency, mem |
| dev-14372e1209 | N-Sigma chính | <!--v8:3849-->0.0467742<!--/v8--> | <!--v8:3850-->0.0522602<!--/v8--> | <!--v8:3851-->0.0878257<!--/v8--> | <!--v8:3852-->0.00705882<!--/v8--> / <!--v8:3853-->0.00132353<!--/v8--> / <!--v8:3854-->0<!--/v8--> | latency |
| dev-14372e1209 | N-Sigma đối chứng | <!--v8:3855-->0.925806<!--/v8--> | <!--v8:3856-->0.98086<!--/v8--> | <!--v8:3857-->0.625224<!--/v8--> | <!--v8:3858-->0.0176584<!--/v8--> / <!--v8:3859-->0.0142975<!--/v8--> / <!--v8:3860-->0.00618113<!--/v8--> | khac, mem |
| dev-16597725c1 | N-Sigma chính | <!--v8:3861-->0.466129<!--/v8--> | <!--v8:3862-->0.461933<!--/v8--> | <!--v8:3863-->0.102504<!--/v8--> | <!--v8:3864-->0.00325<!--/v8--> / <!--v8:3865-->0.020625<!--/v8--> / <!--v8:3866-->0.015<!--/v8--> | latency |
| dev-16597725c1 | N-Sigma đối chứng | <!--v8:3867-->0.993548<!--/v8--> | <!--v8:3868-->0.998321<!--/v8--> | <!--v8:3869-->0.629255<!--/v8--> | <!--v8:3870-->0.0120436<!--/v8--> / <!--v8:3871-->0.0238692<!--/v8--> / <!--v8:3872-->0.0141008<!--/v8--> | khac, latency |
| dev-16870e660c | N-Sigma chính | <!--v8:3873-->0.293548<!--/v8--> | <!--v8:3874-->0.293204<!--/v8--> | <!--v8:3875-->0.0878257<!--/v8--> | <!--v8:3876-->0.0135294<!--/v8--> / <!--v8:3877-->0.00338235<!--/v8--> / <!--v8:3878-->0.0128676<!--/v8--> | latency |
| dev-16870e660c | N-Sigma đối chứng | <!--v8:3879-->0.990323<!--/v8--> | <!--v8:3880-->0.998704<!--/v8--> | <!--v8:3881-->0.623192<!--/v8--> | <!--v8:3882-->0.0252632<!--/v8--> / <!--v8:3883-->0.0194598<!--/v8--> / <!--v8:3884-->0.0146555<!--/v8--> | khac, latency, mem |
| dev-1e6d61b5ec | N-Sigma chính | <!--v8:3885-->0.243548<!--/v8--> | <!--v8:3886-->0.250759<!--/v8--> | <!--v8:3887-->0.0653576<!--/v8--> | <!--v8:3888-->0.0168<!--/v8--> / <!--v8:3889-->0.008<!--/v8--> / <!--v8:3890-->0.010875<!--/v8--> | latency |
| dev-1e6d61b5ec | N-Sigma đối chứng | <!--v8:3891-->0.985484<!--/v8--> | <!--v8:3892-->0.998041<!--/v8--> | <!--v8:3893-->0.601179<!--/v8--> | <!--v8:3894-->0.0211765<!--/v8--> / <!--v8:3895-->0.0166176<!--/v8--> / <!--v8:3896-->0.0175276<!--/v8--> | cpu, mem |
| dev-20acb4402d | N-Sigma chính | <!--v8:3897-->0.417742<!--/v8--> | <!--v8:3898-->0.476391<!--/v8--> | <!--v8:3899-->0.0779073<!--/v8--> | <!--v8:3900-->0.0216667<!--/v8--> / <!--v8:3901-->0.0238333<!--/v8--> / <!--v8:3902-->0.0184375<!--/v8--> | latency |
| dev-20acb4402d | N-Sigma đối chứng | <!--v8:3903-->0.998387<!--/v8--> | <!--v8:3904-->0.99801<!--/v8--> | <!--v8:3905-->0.606534<!--/v8--> | <!--v8:3906-->0.0231014<!--/v8--> / <!--v8:3907-->0.0175362<!--/v8--> / <!--v8:3908-->0.0156884<!--/v8--> | cpu, khac, mem |
| dev-260d332c8d | N-Sigma chính | <!--v8:3909-->0.254839<!--/v8--> | <!--v8:3910-->0.255942<!--/v8--> | <!--v8:3911-->0.0779073<!--/v8--> | <!--v8:3912-->0.01<!--/v8--> / <!--v8:3913-->0.0111667<!--/v8--> / <!--v8:3914-->0.00854167<!--/v8--> | latency |
| dev-260d332c8d | N-Sigma đối chứng | <!--v8:3915-->0.985484<!--/v8--> | <!--v8:3916-->0.998915<!--/v8--> | <!--v8:3917-->0.606534<!--/v8--> | <!--v8:3918-->0.0166667<!--/v8--> / <!--v8:3919-->0.0223188<!--/v8--> / <!--v8:3920-->0.0180525<!--/v8--> | cpu, khac, mem |
| dev-3ae0a6c15a | N-Sigma chính | <!--v8:3921-->0.490323<!--/v8--> | <!--v8:3922-->0.477304<!--/v8--> | <!--v8:3923-->0.109754<!--/v8--> | <!--v8:3924-->0.0232558<!--/v8--> / <!--v8:3925-->0.00918605<!--/v8--> / <!--v8:3926-->0.015407<!--/v8--> | latency |
| dev-3ae0a6c15a | N-Sigma đối chứng | <!--v8:3927-->0.998387<!--/v8--> | <!--v8:3928-->0.999355<!--/v8--> | <!--v8:3929-->0.63225<!--/v8--> | <!--v8:3930-->0.0188919<!--/v8--> / <!--v8:3931-->0.0177432<!--/v8--> / <!--v8:3932-->0.0202534<!--/v8--> | cpu, latency, mem |
| dev-3defe3d34b | N-Sigma chính | <!--v8:3933-->0.374194<!--/v8--> | <!--v8:3934-->0.447427<!--/v8--> | <!--v8:3935-->0.107343<!--/v8--> | <!--v8:3936-->0.0121429<!--/v8--> / <!--v8:3937-->0.0238095<!--/v8--> / <!--v8:3938-->0.00796131<!--/v8--> | latency |
| dev-3defe3d34b | N-Sigma đối chứng | <!--v8:3939-->0.990323<!--/v8--> | <!--v8:3940-->0.999262<!--/v8--> | <!--v8:3941-->0.631254<!--/v8--> | <!--v8:3942-->0.0302168<!--/v8--> / <!--v8:3943-->0.0207182<!--/v8--> / <!--v8:3944-->0.0144224<!--/v8--> | cpu, khac, latency, mem |
| dev-4e68956051 | N-Sigma chính | <!--v8:3945-->0.433871<!--/v8--> | <!--v8:3946-->0.474497<!--/v8--> | <!--v8:3947-->0.080397<!--/v8--> | <!--v8:3948-->0.0316129<!--/v8--> / <!--v8:3949-->0.0151613<!--/v8--> / <!--v8:3950-->0.0195565<!--/v8--> | latency |
| dev-4e68956051 | N-Sigma đối chứng | <!--v8:3951-->0.995161<!--/v8--> | <!--v8:3952-->0.99954<!--/v8--> | <!--v8:3953-->0.620123<!--/v8--> | <!--v8:3954-->0.0290782<!--/v8--> / <!--v8:3955-->0.0180028<!--/v8--> / <!--v8:3956-->0.0199633<!--/v8--> | cpu, khac, latency, mem |
| dev-4f8a844308 | N-Sigma chính | <!--v8:3957-->0.304839<!--/v8--> | <!--v8:3958-->0.318607<!--/v8--> | <!--v8:3959-->0.116945<!--/v8--> | <!--v8:3960-->0.00391304<!--/v8--> / <!--v8:3961-->0.0109783<!--/v8--> / <!--v8:3962-->0.00767663<!--/v8--> | latency |
| dev-4f8a844308 | N-Sigma đối chứng | <!--v8:3963-->0.982258<!--/v8--> | <!--v8:3964-->0.997028<!--/v8--> | <!--v8:3965-->0.63522<!--/v8--> | <!--v8:3966-->0.024504<!--/v8--> / <!--v8:3967-->0.0140349<!--/v8--> / <!--v8:3968-->0.0130027<!--/v8--> | cpu, latency, mem |
| dev-57546fd87b | N-Sigma chính | <!--v8:3969-->0.256452<!--/v8--> | <!--v8:3970-->0.268425<!--/v8--> | <!--v8:3971-->0.080397<!--/v8--> | <!--v8:3972-->0.0116129<!--/v8--> / <!--v8:3973-->0.00725806<!--/v8--> / <!--v8:3974-->0.0108871<!--/v8--> | latency |
| dev-57546fd87b | N-Sigma đối chứng | <!--v8:3975-->0.979032<!--/v8--> | <!--v8:3976-->0.994544<!--/v8--> | <!--v8:3977-->0.620123<!--/v8--> | <!--v8:3978-->0.0241061<!--/v8--> / <!--v8:3979-->0.0111453<!--/v8--> / <!--v8:3980-->0.0129539<!--/v8--> | cpu, khac, latency, mem |
| dev-59f696a169 | N-Sigma chính | <!--v8:3981-->0.425806<!--/v8--> | <!--v8:3982-->0.443923<!--/v8--> | <!--v8:3983-->0.102504<!--/v8--> | <!--v8:3984-->0.014<!--/v8--> / <!--v8:3985-->0.010125<!--/v8--> / <!--v8:3986-->0.0167188<!--/v8--> | latency |
| dev-59f696a169 | N-Sigma đối chứng | <!--v8:3987-->1<!--/v8--> | <!--v8:3988-->0.999557<!--/v8--> | <!--v8:3989-->0.629255<!--/v8--> | <!--v8:3990-->0.0166757<!--/v8--> / <!--v8:3991-->0.0236921<!--/v8--> / <!--v8:3992-->0.0194142<!--/v8--> | cpu, khac, latency, mem |
| dev-746fd74313 | N-Sigma chính | <!--v8:3993-->0.317742<!--/v8--> | <!--v8:3994-->0.403548<!--/v8--> | <!--v8:3995-->0.112157<!--/v8--> | <!--v8:3996-->0.0168182<!--/v8--> / <!--v8:3997-->0.01375<!--/v8--> / <!--v8:3998-->0.0084517<!--/v8--> | latency |
| dev-746fd74313 | N-Sigma đối chứng | <!--v8:3999-->1<!--/v8--> | <!--v8:4000-->0.999131<!--/v8--> | <!--v8:4001-->0.633243<!--/v8--> | <!--v8:4002-->0.0204313<!--/v8--> / <!--v8:4003-->0.0188275<!--/v8--> / <!--v8:4004-->0.0175623<!--/v8--> | cpu, khac, latency, mem |
| dev-7f1b6b071d | N-Sigma chính | <!--v8:4005-->0.395161<!--/v8--> | <!--v8:4006-->0.360214<!--/v8--> | <!--v8:4007-->0.0878257<!--/v8--> | <!--v8:4008-->0.0144118<!--/v8--> / <!--v8:4009-->0.0172059<!--/v8--> / <!--v8:4010-->0.00955882<!--/v8--> | latency |
| dev-7f1b6b071d | N-Sigma đối chứng | <!--v8:4011-->1<!--/v8--> | <!--v8:4012-->0.999928<!--/v8--> | <!--v8:4013-->0.623192<!--/v8--> | <!--v8:4014-->0.0269529<!--/v8--> / <!--v8:4015-->0.015277<!--/v8--> / <!--v8:4016-->0.0310509<!--/v8--> | cpu, khac, mem |
| dev-8017c6dc70 | N-Sigma chính | <!--v8:4017-->0.317742<!--/v8--> | <!--v8:4018-->0.327996<!--/v8--> | <!--v8:4019-->0.0653576<!--/v8--> | <!--v8:4020-->0.0232<!--/v8--> / <!--v8:4021-->0.0202<!--/v8--> / <!--v8:4022-->0.010125<!--/v8--> | latency |
| dev-8017c6dc70 | N-Sigma đối chứng | <!--v8:4023-->1<!--/v8--> | <!--v8:4024-->0.999989<!--/v8--> | <!--v8:4025-->0.601179<!--/v8--> | <!--v8:4026-->0.0294412<!--/v8--> / <!--v8:4027-->0.0321912<!--/v8--> / <!--v8:4028-->0.0325<!--/v8--> | cpu, mem |
| dev-98bc73c499 | N-Sigma chính | <!--v8:4029-->0.320968<!--/v8--> | <!--v8:4030-->0.465995<!--/v8--> | <!--v8:4031-->0.107343<!--/v8--> | <!--v8:4032-->0.0197619<!--/v8--> / <!--v8:4033-->0.032381<!--/v8--> / <!--v8:4034-->0.00186012<!--/v8--> | latency |
| dev-98bc73c499 | N-Sigma đối chứng | <!--v8:4035-->1<!--/v8--> | <!--v8:4036-->0.99985<!--/v8--> | <!--v8:4037-->0.631254<!--/v8--> | <!--v8:4038-->0.021897<!--/v8--> / <!--v8:4039-->0.0284959<!--/v8--> / <!--v8:4040-->0.0198933<!--/v8--> | cpu, mem |
| dev-a505ab3f65 | N-Sigma chính | <!--v8:4041-->0.390323<!--/v8--> | <!--v8:4042-->0.373218<!--/v8--> | <!--v8:4043-->0.112157<!--/v8--> | <!--v8:4044-->0.00795455<!--/v8--> / <!--v8:4045-->0.0118182<!--/v8--> / <!--v8:4046-->0.0102983<!--/v8--> | latency |
| dev-a505ab3f65 | N-Sigma đối chứng | <!--v8:4047-->1<!--/v8--> | <!--v8:4048-->0.997549<!--/v8--> | <!--v8:4049-->0.633243<!--/v8--> | <!--v8:4050-->0.0199191<!--/v8--> / <!--v8:4051-->0.0148383<!--/v8--> / <!--v8:4052-->0.0149511<!--/v8--> | cpu, khac, latency, mem |
| dev-a5cabe5fa7 | N-Sigma chính | <!--v8:4053-->0.440323<!--/v8--> | <!--v8:4054-->0.559886<!--/v8--> | <!--v8:4055-->0.0828799<!--/v8--> | <!--v8:4056-->0.011875<!--/v8--> / <!--v8:4057-->0.0059375<!--/v8--> / <!--v8:4058-->0.0402344<!--/v8--> | latency |
| dev-a5cabe5fa7 | N-Sigma đối chứng | <!--v8:4059-->0.996774<!--/v8--> | <!--v8:4060-->0.999509<!--/v8--> | <!--v8:4061-->0.621148<!--/v8--> | <!--v8:4062-->0.0283008<!--/v8--> / <!--v8:4063-->0.0169638<!--/v8--> / <!--v8:4064-->0.0203952<!--/v8--> | cpu, khac, latency, mem |
| dev-a915aa2424 | N-Sigma chính | <!--v8:4065-->0.446774<!--/v8--> | <!--v8:4066-->0.500268<!--/v8--> | <!--v8:4067-->0.104927<!--/v8--> | <!--v8:4068-->0.0107317<!--/v8--> / <!--v8:4069-->0.00780488<!--/v8--> / <!--v8:4070-->0.0237043<!--/v8--> | latency |
| dev-a915aa2424 | N-Sigma đối chứng | <!--v8:4071-->0.995161<!--/v8--> | <!--v8:4072-->0.999828<!--/v8--> | <!--v8:4073-->0.630256<!--/v8--> | <!--v8:4074-->0.0210054<!--/v8--> / <!--v8:4075-->0.0231793<!--/v8--> / <!--v8:4076-->0.0231233<!--/v8--> | cpu, khac, latency, mem |
| dev-b8bd0abf60 | N-Sigma chính | <!--v8:4077-->0.3<!--/v8--> | <!--v8:4078-->0.44442<!--/v8--> | <!--v8:4079-->0.121707<!--/v8--> | <!--v8:4080-->0.0177083<!--/v8--> / <!--v8:4081-->0.01<!--/v8--> / <!--v8:4082-->0.0113281<!--/v8--> | latency |
| dev-b8bd0abf60 | N-Sigma đối chứng | <!--v8:4083-->0.991935<!--/v8--> | <!--v8:4084-->0.999133<!--/v8--> | <!--v8:4085-->0.637188<!--/v8--> | <!--v8:4086-->0.0250933<!--/v8--> / <!--v8:4087-->0.0173733<!--/v8--> / <!--v8:4088-->0.016675<!--/v8--> | cpu, khac, mem |
| dev-ba831dbeb8 | N-Sigma chính | <!--v8:4089-->0.324194<!--/v8--> | <!--v8:4090-->0.34812<!--/v8--> | <!--v8:4091-->0.104927<!--/v8--> | <!--v8:4092-->0.00390244<!--/v8--> / <!--v8:4093-->0.0191463<!--/v8--> / <!--v8:4094-->0.00647866<!--/v8--> | latency |
| dev-ba831dbeb8 | N-Sigma đối chứng | <!--v8:4095-->0.995161<!--/v8--> | <!--v8:4096-->0.999898<!--/v8--> | <!--v8:4097-->0.630256<!--/v8--> | <!--v8:4098-->0.0252717<!--/v8--> / <!--v8:4099-->0.0145924<!--/v8--> / <!--v8:4100-->0.029127<!--/v8--> | cpu, khac, latency, mem |
| dev-bcbd4f46ae | N-Sigma chính | <!--v8:4101-->0.0822581<!--/v8--> | <!--v8:4102-->0.0885506<!--/v8--> | <!--v8:4103-->0.0878257<!--/v8--> | <!--v8:4104-->0.00441176<!--/v8--> / <!--v8:4105-->0<!--/v8--> / <!--v8:4106-->0.00376838<!--/v8--> | latency |
| dev-bcbd4f46ae | N-Sigma đối chứng | <!--v8:4107-->0.982258<!--/v8--> | <!--v8:4108-->0.984402<!--/v8--> | <!--v8:4109-->0.623192<!--/v8--> | <!--v8:4110-->0.0214681<!--/v8--> / <!--v8:4111-->0.00867036<!--/v8--> / <!--v8:4112-->0.00961738<!--/v8--> | cpu, khac, latency, mem |
| dev-db293894ab | N-Sigma chính | <!--v8:4113-->0.327419<!--/v8--> | <!--v8:4114-->0.41463<!--/v8--> | <!--v8:4115-->0.0853561<!--/v8--> | <!--v8:4116-->0.0163636<!--/v8--> / <!--v8:4117-->0.0110606<!--/v8--> / <!--v8:4118-->0.0185606<!--/v8--> | latency |
| dev-db293894ab | N-Sigma đối chứng | <!--v8:4119-->0.985484<!--/v8--> | <!--v8:4120-->0.997794<!--/v8--> | <!--v8:4121-->0.622171<!--/v8--> | <!--v8:4122-->0.0235278<!--/v8--> / <!--v8:4123-->0.018625<!--/v8--> / <!--v8:4124-->0.0130208<!--/v8--> | cpu, khac, latency, mem |
| dev-de89e2f9e9 | N-Sigma chính | <!--v8:4125-->0.225806<!--/v8--> | <!--v8:4126-->0.21579<!--/v8--> | <!--v8:4127-->0.100074<!--/v8--> | <!--v8:4128-->0.00512821<!--/v8--> / <!--v8:4129-->0.005<!--/v8--> / <!--v8:4130-->0.00713141<!--/v8--> | latency |
| dev-de89e2f9e9 | N-Sigma đối chứng | <!--v8:4131-->1<!--/v8--> | <!--v8:4132-->0.999012<!--/v8--> | <!--v8:4133-->0.628251<!--/v8--> | <!--v8:4134-->0.019071<!--/v8--> / <!--v8:4135-->0.0194126<!--/v8--> / <!--v8:4136-->0.0174522<!--/v8--> | cpu, khac, latency, mem |
| dev-f36d0647d5 | N-Sigma chính | <!--v8:4137-->0.209677<!--/v8--> | <!--v8:4138-->0.238644<!--/v8--> | <!--v8:4139-->0.116945<!--/v8--> | <!--v8:4140-->0.0156522<!--/v8--> / <!--v8:4141-->0.00597826<!--/v8--> / <!--v8:4142-->0.00264946<!--/v8--> | latency |
| dev-f36d0647d5 | N-Sigma đối chứng | <!--v8:4143-->0.975806<!--/v8--> | <!--v8:4144-->0.994183<!--/v8--> | <!--v8:4145-->0.63522<!--/v8--> | <!--v8:4146-->0.0168365<!--/v8--> / <!--v8:4147-->0.0179893<!--/v8--> / <!--v8:4148-->0.00958445<!--/v8--> | cpu, latency, mem |
| dev-f81f88234e | N-Sigma chính | <!--v8:4149-->0.066129<!--/v8--> | <!--v8:4150-->0.066129<!--/v8--> | <!--v8:4151-->0.0828799<!--/v8--> | <!--v8:4152-->0<!--/v8--> / <!--v8:4153-->0<!--/v8--> / <!--v8:4154-->0.00400391<!--/v8--> | latency |
| dev-f81f88234e | N-Sigma đối chứng | <!--v8:4155-->0.979032<!--/v8--> | <!--v8:4156-->0.982158<!--/v8--> | <!--v8:4157-->0.621148<!--/v8--> | <!--v8:4158-->0.0166852<!--/v8--> / <!--v8:4159-->0.0103621<!--/v8--> / <!--v8:4160-->0.00952298<!--/v8--> | cpu, khac, mem |
| dev-f9a8e05ed7 | N-Sigma chính | <!--v8:4161-->0.33871<!--/v8--> | <!--v8:4162-->0.354338<!--/v8--> | <!--v8:4163-->0.0976373<!--/v8--> | <!--v8:4164-->0.0113158<!--/v8--> / <!--v8:4165-->0.0128947<!--/v8--> / <!--v8:4166-->0.0101151<!--/v8--> | latency |
| dev-f9a8e05ed7 | N-Sigma đối chứng | <!--v8:4167-->0.998387<!--/v8--> | <!--v8:4168-->0.999726<!--/v8--> | <!--v8:4169-->0.627245<!--/v8--> | <!--v8:4170-->0.036274<!--/v8--> / <!--v8:4171-->0.0254384<!--/v8--> / <!--v8:4172-->0.0149401<!--/v8--> | cpu, latency, mem |
| dev-fbc45b0c67 | N-Sigma chính | <!--v8:4173-->0.454839<!--/v8--> | <!--v8:4174-->0.475821<!--/v8--> | <!--v8:4175-->0.080397<!--/v8--> | <!--v8:4176-->0.0245161<!--/v8--> / <!--v8:4177-->0.0164516<!--/v8--> / <!--v8:4178-->0.0212702<!--/v8--> | latency |
| dev-fbc45b0c67 | N-Sigma đối chứng | <!--v8:4179-->0.998387<!--/v8--> | <!--v8:4180-->0.999954<!--/v8--> | <!--v8:4181-->0.620123<!--/v8--> | <!--v8:4182-->0.027067<!--/v8--> / <!--v8:4183-->0.0223743<!--/v8--> / <!--v8:4184-->0.0293209<!--/v8--> | cpu, latency, mem |

| Bộ / ô | Loại cột | Báo cột-giây / tổng cột-giây | Tỉ lệ |
|---|---|---|---|
| N-Sigma chính / all | latency | <!--v8:4185-->8106<!--/v8-->/<!--v8:4186-->505920<!--/v8--> | <!--v8:4187-->0.0160223<!--/v8--> |
| N-Sigma chính / all | error | <!--v8:4188-->148<!--/v8-->/<!--v8:4189-->181040<!--/v8--> | <!--v8:4190-->0.000817499<!--/v8--> |
| N-Sigma chính / all | cpu | <!--v8:4191-->0<!--/v8-->/<!--v8:4192-->0<!--/v8--> | <!--v8:4193-->N/A<!--/v8--> |
| N-Sigma chính / all | mem | <!--v8:4194-->0<!--/v8-->/<!--v8:4195-->0<!--/v8--> | <!--v8:4196-->N/A<!--/v8--> |
| N-Sigma chính / all | mang | <!--v8:4197-->0<!--/v8-->/<!--v8:4198-->0<!--/v8--> | <!--v8:4199-->N/A<!--/v8--> |
| N-Sigma chính / all | khac | <!--v8:4200-->0<!--/v8-->/<!--v8:4201-->0<!--/v8--> | <!--v8:4202-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | latency | <!--v8:4203-->1079<!--/v8-->/<!--v8:4204-->52080<!--/v8--> | <!--v8:4205-->0.0207181<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | error | <!--v8:4206-->0<!--/v8-->/<!--v8:4207-->23560<!--/v8--> | <!--v8:4208-->0<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | cpu | <!--v8:4209-->0<!--/v8-->/<!--v8:4210-->0<!--/v8--> | <!--v8:4211-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | mem | <!--v8:4212-->0<!--/v8-->/<!--v8:4213-->0<!--/v8--> | <!--v8:4214-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | mang | <!--v8:4215-->0<!--/v8-->/<!--v8:4216-->0<!--/v8--> | <!--v8:4217-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | khac | <!--v8:4218-->0<!--/v8-->/<!--v8:4219-->0<!--/v8--> | <!--v8:4220-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | latency | <!--v8:4221-->508<!--/v8-->/<!--v8:4222-->52080<!--/v8--> | <!--v8:4223-->0.00975422<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | error | <!--v8:4224-->36<!--/v8-->/<!--v8:4225-->14260<!--/v8--> | <!--v8:4226-->0.00252454<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | cpu | <!--v8:4227-->0<!--/v8-->/<!--v8:4228-->0<!--/v8--> | <!--v8:4229-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | mem | <!--v8:4230-->0<!--/v8-->/<!--v8:4231-->0<!--/v8--> | <!--v8:4232-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | mang | <!--v8:4233-->0<!--/v8-->/<!--v8:4234-->0<!--/v8--> | <!--v8:4235-->N/A<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | khac | <!--v8:4236-->0<!--/v8-->/<!--v8:4237-->0<!--/v8--> | <!--v8:4238-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | latency | <!--v8:4239-->652<!--/v8-->/<!--v8:4240-->44640<!--/v8--> | <!--v8:4241-->0.0146057<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | error | <!--v8:4242-->0<!--/v8-->/<!--v8:4243-->13640<!--/v8--> | <!--v8:4244-->0<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | cpu | <!--v8:4245-->0<!--/v8-->/<!--v8:4246-->0<!--/v8--> | <!--v8:4247-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | mem | <!--v8:4248-->0<!--/v8-->/<!--v8:4249-->0<!--/v8--> | <!--v8:4250-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | mang | <!--v8:4251-->0<!--/v8-->/<!--v8:4252-->0<!--/v8--> | <!--v8:4253-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | khac | <!--v8:4254-->0<!--/v8-->/<!--v8:4255-->0<!--/v8--> | <!--v8:4256-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | latency | <!--v8:4257-->730<!--/v8-->/<!--v8:4258-->44640<!--/v8--> | <!--v8:4259-->0.016353<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | error | <!--v8:4260-->0<!--/v8-->/<!--v8:4261-->21080<!--/v8--> | <!--v8:4262-->0<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | cpu | <!--v8:4263-->0<!--/v8-->/<!--v8:4264-->0<!--/v8--> | <!--v8:4265-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | mem | <!--v8:4266-->0<!--/v8-->/<!--v8:4267-->0<!--/v8--> | <!--v8:4268-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | mang | <!--v8:4269-->0<!--/v8-->/<!--v8:4270-->0<!--/v8--> | <!--v8:4271-->N/A<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | khac | <!--v8:4272-->0<!--/v8-->/<!--v8:4273-->0<!--/v8--> | <!--v8:4274-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | latency | <!--v8:4275-->474<!--/v8-->/<!--v8:4276-->52080<!--/v8--> | <!--v8:4277-->0.00910138<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | error | <!--v8:4278-->0<!--/v8-->/<!--v8:4279-->18600<!--/v8--> | <!--v8:4280-->0<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | cpu | <!--v8:4281-->0<!--/v8-->/<!--v8:4282-->0<!--/v8--> | <!--v8:4283-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | mem | <!--v8:4284-->0<!--/v8-->/<!--v8:4285-->0<!--/v8--> | <!--v8:4286-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | mang | <!--v8:4287-->0<!--/v8-->/<!--v8:4288-->0<!--/v8--> | <!--v8:4289-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | khac | <!--v8:4290-->0<!--/v8-->/<!--v8:4291-->0<!--/v8--> | <!--v8:4292-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | latency | <!--v8:4293-->709<!--/v8-->/<!--v8:4294-->52080<!--/v8--> | <!--v8:4295-->0.0136137<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | error | <!--v8:4296-->66<!--/v8-->/<!--v8:4297-->19840<!--/v8--> | <!--v8:4298-->0.00332661<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | cpu | <!--v8:4299-->0<!--/v8-->/<!--v8:4300-->0<!--/v8--> | <!--v8:4301-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | mem | <!--v8:4302-->0<!--/v8-->/<!--v8:4303-->0<!--/v8--> | <!--v8:4304-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | mang | <!--v8:4305-->0<!--/v8-->/<!--v8:4306-->0<!--/v8--> | <!--v8:4307-->N/A<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | khac | <!--v8:4308-->0<!--/v8-->/<!--v8:4309-->0<!--/v8--> | <!--v8:4310-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | latency | <!--v8:4311-->1029<!--/v8-->/<!--v8:4312-->52080<!--/v8--> | <!--v8:4313-->0.0197581<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | error | <!--v8:4314-->0<!--/v8-->/<!--v8:4315-->26040<!--/v8--> | <!--v8:4316-->0<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | cpu | <!--v8:4317-->0<!--/v8-->/<!--v8:4318-->0<!--/v8--> | <!--v8:4319-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | mem | <!--v8:4320-->0<!--/v8-->/<!--v8:4321-->0<!--/v8--> | <!--v8:4322-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | mang | <!--v8:4323-->0<!--/v8-->/<!--v8:4324-->0<!--/v8--> | <!--v8:4325-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | khac | <!--v8:4326-->0<!--/v8-->/<!--v8:4327-->0<!--/v8--> | <!--v8:4328-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | latency | <!--v8:4329-->1059<!--/v8-->/<!--v8:4330-->52080<!--/v8--> | <!--v8:4331-->0.0203341<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | error | <!--v8:4332-->0<!--/v8-->/<!--v8:4333-->13640<!--/v8--> | <!--v8:4334-->0<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | cpu | <!--v8:4335-->0<!--/v8-->/<!--v8:4336-->0<!--/v8--> | <!--v8:4337-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | mem | <!--v8:4338-->0<!--/v8-->/<!--v8:4339-->0<!--/v8--> | <!--v8:4340-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | mang | <!--v8:4341-->0<!--/v8-->/<!--v8:4342-->0<!--/v8--> | <!--v8:4343-->N/A<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | khac | <!--v8:4344-->0<!--/v8-->/<!--v8:4345-->0<!--/v8--> | <!--v8:4346-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | latency | <!--v8:4347-->720<!--/v8-->/<!--v8:4348-->52080<!--/v8--> | <!--v8:4349-->0.0138249<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | error | <!--v8:4350-->15<!--/v8-->/<!--v8:4351-->16120<!--/v8--> | <!--v8:4352-->0.000930521<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | cpu | <!--v8:4353-->0<!--/v8-->/<!--v8:4354-->0<!--/v8--> | <!--v8:4355-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | mem | <!--v8:4356-->0<!--/v8-->/<!--v8:4357-->0<!--/v8--> | <!--v8:4358-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | mang | <!--v8:4359-->0<!--/v8-->/<!--v8:4360-->0<!--/v8--> | <!--v8:4361-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | khac | <!--v8:4362-->0<!--/v8-->/<!--v8:4363-->0<!--/v8--> | <!--v8:4364-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | latency | <!--v8:4365-->1146<!--/v8-->/<!--v8:4366-->52080<!--/v8--> | <!--v8:4367-->0.0220046<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | error | <!--v8:4368-->31<!--/v8-->/<!--v8:4369-->14260<!--/v8--> | <!--v8:4370-->0.00217391<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | cpu | <!--v8:4371-->0<!--/v8-->/<!--v8:4372-->0<!--/v8--> | <!--v8:4373-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | mem | <!--v8:4374-->0<!--/v8-->/<!--v8:4375-->0<!--/v8--> | <!--v8:4376-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | mang | <!--v8:4377-->0<!--/v8-->/<!--v8:4378-->0<!--/v8--> | <!--v8:4379-->N/A<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | khac | <!--v8:4380-->0<!--/v8-->/<!--v8:4381-->0<!--/v8--> | <!--v8:4382-->N/A<!--/v8--> |
| N-Sigma đối chứng / all | latency | <!--v8:4383-->18928<!--/v8-->/<!--v8:4384-->1.01184e+06<!--/v8--> | <!--v8:4385-->0.0187065<!--/v8--> |
| N-Sigma đối chứng / all | error | <!--v8:4386-->148<!--/v8-->/<!--v8:4387-->181040<!--/v8--> | <!--v8:4388-->0.000817499<!--/v8--> |
| N-Sigma đối chứng / all | cpu | <!--v8:4389-->30583<!--/v8-->/<!--v8:4390-->1.2648e+06<!--/v8--> | <!--v8:4391-->0.0241801<!--/v8--> |
| N-Sigma đối chứng / all | mem | <!--v8:4392-->47567<!--/v8-->/<!--v8:4393-->1.26542e+06<!--/v8--> | <!--v8:4394-->0.0375899<!--/v8--> |
| N-Sigma đối chứng / all | mang | <!--v8:4395-->0<!--/v8-->/<!--v8:4396-->0<!--/v8--> | <!--v8:4397-->N/A<!--/v8--> |
| N-Sigma đối chứng / all | khac | <!--v8:4398-->28355<!--/v8-->/<!--v8:4399-->3.01754e+06<!--/v8--> | <!--v8:4400-->0.00939673<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | latency | <!--v8:4401-->2055<!--/v8-->/<!--v8:4402-->104160<!--/v8--> | <!--v8:4403-->0.0197293<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | error | <!--v8:4404-->0<!--/v8-->/<!--v8:4405-->23560<!--/v8--> | <!--v8:4406-->0<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | cpu | <!--v8:4407-->2910<!--/v8-->/<!--v8:4408-->126480<!--/v8--> | <!--v8:4409-->0.0230076<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | mem | <!--v8:4410-->4990<!--/v8-->/<!--v8:4411-->126480<!--/v8--> | <!--v8:4412-->0.0394529<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | mang | <!--v8:4413-->0<!--/v8-->/<!--v8:4414-->0<!--/v8--> | <!--v8:4415-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | khac | <!--v8:4416-->2873<!--/v8-->/<!--v8:4417-->303180<!--/v8--> | <!--v8:4418-->0.00947622<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | latency | <!--v8:4419-->1454<!--/v8-->/<!--v8:4420-->104160<!--/v8--> | <!--v8:4421-->0.0139593<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | error | <!--v8:4422-->36<!--/v8-->/<!--v8:4423-->14260<!--/v8--> | <!--v8:4424-->0.00252454<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | cpu | <!--v8:4425-->2675<!--/v8-->/<!--v8:4426-->126480<!--/v8--> | <!--v8:4427-->0.0211496<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | mem | <!--v8:4428-->3296<!--/v8-->/<!--v8:4429-->126480<!--/v8--> | <!--v8:4430-->0.0260595<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | mang | <!--v8:4431-->0<!--/v8-->/<!--v8:4432-->0<!--/v8--> | <!--v8:4433-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | khac | <!--v8:4434-->2361<!--/v8-->/<!--v8:4435-->303180<!--/v8--> | <!--v8:4436-->0.00778745<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | latency | <!--v8:4437-->1480<!--/v8-->/<!--v8:4438-->89280<!--/v8--> | <!--v8:4439-->0.0165771<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | error | <!--v8:4440-->0<!--/v8-->/<!--v8:4441-->13640<!--/v8--> | <!--v8:4442-->0<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | cpu | <!--v8:4443-->3215<!--/v8-->/<!--v8:4444-->126480<!--/v8--> | <!--v8:4445-->0.025419<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | mem | <!--v8:4446-->5854<!--/v8-->/<!--v8:4447-->126480<!--/v8--> | <!--v8:4448-->0.046284<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | mang | <!--v8:4449-->0<!--/v8-->/<!--v8:4450-->0<!--/v8--> | <!--v8:4451-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | khac | <!--v8:4452-->3139<!--/v8-->/<!--v8:4453-->295740<!--/v8--> | <!--v8:4454-->0.0106141<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | latency | <!--v8:4455-->1857<!--/v8-->/<!--v8:4456-->89280<!--/v8--> | <!--v8:4457-->0.0207997<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | error | <!--v8:4458-->0<!--/v8-->/<!--v8:4459-->21080<!--/v8--> | <!--v8:4460-->0<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | cpu | <!--v8:4461-->2772<!--/v8-->/<!--v8:4462-->126480<!--/v8--> | <!--v8:4463-->0.0219165<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | mem | <!--v8:4464-->3950<!--/v8-->/<!--v8:4465-->126480<!--/v8--> | <!--v8:4466-->0.0312302<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | mang | <!--v8:4467-->0<!--/v8-->/<!--v8:4468-->0<!--/v8--> | <!--v8:4469-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | khac | <!--v8:4470-->2382<!--/v8-->/<!--v8:4471-->295740<!--/v8--> | <!--v8:4472-->0.00805437<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | latency | <!--v8:4473-->1403<!--/v8-->/<!--v8:4474-->104160<!--/v8--> | <!--v8:4475-->0.0134697<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | error | <!--v8:4476-->0<!--/v8-->/<!--v8:4477-->18600<!--/v8--> | <!--v8:4478-->0<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | cpu | <!--v8:4479-->2662<!--/v8-->/<!--v8:4480-->126480<!--/v8--> | <!--v8:4481-->0.0210468<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | mem | <!--v8:4482-->3430<!--/v8-->/<!--v8:4483-->127100<!--/v8--> | <!--v8:4484-->0.0269866<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | mang | <!--v8:4485-->0<!--/v8-->/<!--v8:4486-->0<!--/v8--> | <!--v8:4487-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | khac | <!--v8:4488-->2425<!--/v8-->/<!--v8:4489-->303800<!--/v8--> | <!--v8:4490-->0.00798223<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | latency | <!--v8:4491-->1620<!--/v8-->/<!--v8:4492-->104160<!--/v8--> | <!--v8:4493-->0.015553<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | error | <!--v8:4494-->66<!--/v8-->/<!--v8:4495-->19840<!--/v8--> | <!--v8:4496-->0.00332661<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | cpu | <!--v8:4497-->2953<!--/v8-->/<!--v8:4498-->126480<!--/v8--> | <!--v8:4499-->0.0233476<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | mem | <!--v8:4500-->3855<!--/v8-->/<!--v8:4501-->126480<!--/v8--> | <!--v8:4502-->0.0304791<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | mang | <!--v8:4503-->0<!--/v8-->/<!--v8:4504-->0<!--/v8--> | <!--v8:4505-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | khac | <!--v8:4506-->2383<!--/v8-->/<!--v8:4507-->303180<!--/v8--> | <!--v8:4508-->0.00786002<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | latency | <!--v8:4509-->2247<!--/v8-->/<!--v8:4510-->104160<!--/v8--> | <!--v8:4511-->0.0215726<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | error | <!--v8:4512-->0<!--/v8-->/<!--v8:4513-->26040<!--/v8--> | <!--v8:4514-->0<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | cpu | <!--v8:4515-->3490<!--/v8-->/<!--v8:4516-->126480<!--/v8--> | <!--v8:4517-->0.0275933<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | mem | <!--v8:4518-->6253<!--/v8-->/<!--v8:4519-->126480<!--/v8--> | <!--v8:4520-->0.0494386<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | mang | <!--v8:4521-->0<!--/v8-->/<!--v8:4522-->0<!--/v8--> | <!--v8:4523-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | khac | <!--v8:4524-->3114<!--/v8-->/<!--v8:4525-->303180<!--/v8--> | <!--v8:4526-->0.0102711<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | latency | <!--v8:4527-->2342<!--/v8-->/<!--v8:4528-->104160<!--/v8--> | <!--v8:4529-->0.0224846<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | error | <!--v8:4530-->0<!--/v8-->/<!--v8:4531-->13640<!--/v8--> | <!--v8:4532-->0<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | cpu | <!--v8:4533-->2999<!--/v8-->/<!--v8:4534-->126480<!--/v8--> | <!--v8:4535-->0.0237113<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | mem | <!--v8:4536-->5354<!--/v8-->/<!--v8:4537-->126480<!--/v8--> | <!--v8:4538-->0.0423308<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | mang | <!--v8:4539-->0<!--/v8-->/<!--v8:4540-->0<!--/v8--> | <!--v8:4541-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | khac | <!--v8:4542-->3467<!--/v8-->/<!--v8:4543-->303180<!--/v8--> | <!--v8:4544-->0.0114355<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | latency | <!--v8:4545-->1785<!--/v8-->/<!--v8:4546-->104160<!--/v8--> | <!--v8:4547-->0.0171371<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | error | <!--v8:4548-->15<!--/v8-->/<!--v8:4549-->16120<!--/v8--> | <!--v8:4550-->0.000930521<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | cpu | <!--v8:4551-->3287<!--/v8-->/<!--v8:4552-->126480<!--/v8--> | <!--v8:4553-->0.0259883<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | mem | <!--v8:4554-->4647<!--/v8-->/<!--v8:4555-->126480<!--/v8--> | <!--v8:4556-->0.036741<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | mang | <!--v8:4557-->0<!--/v8-->/<!--v8:4558-->0<!--/v8--> | <!--v8:4559-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | khac | <!--v8:4560-->3043<!--/v8-->/<!--v8:4561-->303180<!--/v8--> | <!--v8:4562-->0.0100369<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | latency | <!--v8:4563-->2685<!--/v8-->/<!--v8:4564-->104160<!--/v8--> | <!--v8:4565-->0.0257776<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | error | <!--v8:4566-->31<!--/v8-->/<!--v8:4567-->14260<!--/v8--> | <!--v8:4568-->0.00217391<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | cpu | <!--v8:4569-->3620<!--/v8-->/<!--v8:4570-->126480<!--/v8--> | <!--v8:4571-->0.0286211<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | mem | <!--v8:4572-->5938<!--/v8-->/<!--v8:4573-->126480<!--/v8--> | <!--v8:4574-->0.0469481<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | mang | <!--v8:4575-->0<!--/v8-->/<!--v8:4576-->0<!--/v8--> | <!--v8:4577-->N/A<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | khac | <!--v8:4578-->3168<!--/v8-->/<!--v8:4579-->303180<!--/v8--> | <!--v8:4580-->0.0104492<!--/v8--> |

| Bộ / ô | Đoạn sau mốc | Giây báo / tổng giây ca | Mật độ báo |
|---|---|---|---|
| N-Sigma chính / all | [<!--v8:4581-->720<!--/v8-->, <!--v8:4582-->780<!--/v8-->) | <!--v8:4583-->1201<!--/v8-->/<!--v8:4584-->1800<!--/v8--> | <!--v8:4585-->0.667222<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4586-->780<!--/v8-->, <!--v8:4587-->840<!--/v8-->) | <!--v8:4588-->1563<!--/v8-->/<!--v8:4589-->1800<!--/v8--> | <!--v8:4590-->0.868333<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4591-->840<!--/v8-->, <!--v8:4592-->900<!--/v8-->) | <!--v8:4593-->1176<!--/v8-->/<!--v8:4594-->1800<!--/v8--> | <!--v8:4595-->0.653333<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4596-->900<!--/v8-->, <!--v8:4597-->960<!--/v8-->) | <!--v8:4598-->744<!--/v8-->/<!--v8:4599-->1800<!--/v8--> | <!--v8:4600-->0.413333<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4601-->960<!--/v8-->, <!--v8:4602-->1020<!--/v8-->) | <!--v8:4603-->640<!--/v8-->/<!--v8:4604-->1800<!--/v8--> | <!--v8:4605-->0.355556<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4606-->1020<!--/v8-->, <!--v8:4607-->1080<!--/v8-->) | <!--v8:4608-->727<!--/v8-->/<!--v8:4609-->1800<!--/v8--> | <!--v8:4610-->0.403889<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4611-->1080<!--/v8-->, <!--v8:4612-->1140<!--/v8-->) | <!--v8:4613-->666<!--/v8-->/<!--v8:4614-->1800<!--/v8--> | <!--v8:4615-->0.37<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4616-->1140<!--/v8-->, <!--v8:4617-->1200<!--/v8-->) | <!--v8:4618-->663<!--/v8-->/<!--v8:4619-->1800<!--/v8--> | <!--v8:4620-->0.368333<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4621-->1200<!--/v8-->, <!--v8:4622-->1260<!--/v8-->) | <!--v8:4623-->598<!--/v8-->/<!--v8:4624-->1800<!--/v8--> | <!--v8:4625-->0.332222<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4626-->1260<!--/v8-->, <!--v8:4627-->1320<!--/v8-->) | <!--v8:4628-->517<!--/v8-->/<!--v8:4629-->1800<!--/v8--> | <!--v8:4630-->0.287222<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4631-->1320<!--/v8-->, <!--v8:4632-->1380<!--/v8-->) | <!--v8:4633-->512<!--/v8-->/<!--v8:4634-->1800<!--/v8--> | <!--v8:4635-->0.284444<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4636-->1380<!--/v8-->, <!--v8:4637-->1440<!--/v8-->) | <!--v8:4638-->660<!--/v8-->/<!--v8:4639-->1800<!--/v8--> | <!--v8:4640-->0.366667<!--/v8--> |
| N-Sigma chính / all | [<!--v8:4641-->1440<!--/v8-->, <!--v8:4642-->1441<!--/v8-->) | <!--v8:4643-->9<!--/v8-->/<!--v8:4644-->30<!--/v8--> | <!--v8:4645-->0.3<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4646-->720<!--/v8-->, <!--v8:4647-->780<!--/v8-->) | <!--v8:4648-->117<!--/v8-->/<!--v8:4649-->180<!--/v8--> | <!--v8:4650-->0.65<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4651-->780<!--/v8-->, <!--v8:4652-->840<!--/v8-->) | <!--v8:4653-->180<!--/v8-->/<!--v8:4654-->180<!--/v8--> | <!--v8:4655-->1<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4656-->840<!--/v8-->, <!--v8:4657-->900<!--/v8-->) | <!--v8:4658-->152<!--/v8-->/<!--v8:4659-->180<!--/v8--> | <!--v8:4660-->0.844444<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4661-->900<!--/v8-->, <!--v8:4662-->960<!--/v8-->) | <!--v8:4663-->66<!--/v8-->/<!--v8:4664-->180<!--/v8--> | <!--v8:4665-->0.366667<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4666-->960<!--/v8-->, <!--v8:4667-->1020<!--/v8-->) | <!--v8:4668-->73<!--/v8-->/<!--v8:4669-->180<!--/v8--> | <!--v8:4670-->0.405556<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4671-->1020<!--/v8-->, <!--v8:4672-->1080<!--/v8-->) | <!--v8:4673-->35<!--/v8-->/<!--v8:4674-->180<!--/v8--> | <!--v8:4675-->0.194444<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4676-->1080<!--/v8-->, <!--v8:4677-->1140<!--/v8-->) | <!--v8:4678-->84<!--/v8-->/<!--v8:4679-->180<!--/v8--> | <!--v8:4680-->0.466667<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4681-->1140<!--/v8-->, <!--v8:4682-->1200<!--/v8-->) | <!--v8:4683-->104<!--/v8-->/<!--v8:4684-->180<!--/v8--> | <!--v8:4685-->0.577778<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4686-->1200<!--/v8-->, <!--v8:4687-->1260<!--/v8-->) | <!--v8:4688-->86<!--/v8-->/<!--v8:4689-->180<!--/v8--> | <!--v8:4690-->0.477778<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4691-->1260<!--/v8-->, <!--v8:4692-->1320<!--/v8-->) | <!--v8:4693-->66<!--/v8-->/<!--v8:4694-->180<!--/v8--> | <!--v8:4695-->0.366667<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4696-->1320<!--/v8-->, <!--v8:4697-->1380<!--/v8-->) | <!--v8:4698-->31<!--/v8-->/<!--v8:4699-->180<!--/v8--> | <!--v8:4700-->0.172222<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4701-->1380<!--/v8-->, <!--v8:4702-->1440<!--/v8-->) | <!--v8:4703-->72<!--/v8-->/<!--v8:4704-->180<!--/v8--> | <!--v8:4705-->0.4<!--/v8--> |
| N-Sigma chính / ts-auth-service / cpu | [<!--v8:4706-->1440<!--/v8-->, <!--v8:4707-->1441<!--/v8-->) | <!--v8:4708-->1<!--/v8-->/<!--v8:4709-->3<!--/v8--> | <!--v8:4710-->0.333333<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4711-->720<!--/v8-->, <!--v8:4712-->780<!--/v8-->) | <!--v8:4713-->158<!--/v8-->/<!--v8:4714-->180<!--/v8--> | <!--v8:4715-->0.877778<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4716-->780<!--/v8-->, <!--v8:4717-->840<!--/v8-->) | <!--v8:4718-->163<!--/v8-->/<!--v8:4719-->180<!--/v8--> | <!--v8:4720-->0.905556<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4721-->840<!--/v8-->, <!--v8:4722-->900<!--/v8-->) | <!--v8:4723-->64<!--/v8-->/<!--v8:4724-->180<!--/v8--> | <!--v8:4725-->0.355556<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4726-->900<!--/v8-->, <!--v8:4727-->960<!--/v8-->) | <!--v8:4728-->56<!--/v8-->/<!--v8:4729-->180<!--/v8--> | <!--v8:4730-->0.311111<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4731-->960<!--/v8-->, <!--v8:4732-->1020<!--/v8-->) | <!--v8:4733-->59<!--/v8-->/<!--v8:4734-->180<!--/v8--> | <!--v8:4735-->0.327778<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4736-->1020<!--/v8-->, <!--v8:4737-->1080<!--/v8-->) | <!--v8:4738-->45<!--/v8-->/<!--v8:4739-->180<!--/v8--> | <!--v8:4740-->0.25<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4741-->1080<!--/v8-->, <!--v8:4742-->1140<!--/v8-->) | <!--v8:4743-->3<!--/v8-->/<!--v8:4744-->180<!--/v8--> | <!--v8:4745-->0.0166667<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4746-->1140<!--/v8-->, <!--v8:4747-->1200<!--/v8-->) | <!--v8:4748-->44<!--/v8-->/<!--v8:4749-->180<!--/v8--> | <!--v8:4750-->0.244444<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4751-->1200<!--/v8-->, <!--v8:4752-->1260<!--/v8-->) | <!--v8:4753-->32<!--/v8-->/<!--v8:4754-->180<!--/v8--> | <!--v8:4755-->0.177778<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4756-->1260<!--/v8-->, <!--v8:4757-->1320<!--/v8-->) | <!--v8:4758-->28<!--/v8-->/<!--v8:4759-->180<!--/v8--> | <!--v8:4760-->0.155556<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4761-->1320<!--/v8-->, <!--v8:4762-->1380<!--/v8-->) | <!--v8:4763-->18<!--/v8-->/<!--v8:4764-->180<!--/v8--> | <!--v8:4765-->0.1<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4766-->1380<!--/v8-->, <!--v8:4767-->1440<!--/v8-->) | <!--v8:4768-->9<!--/v8-->/<!--v8:4769-->180<!--/v8--> | <!--v8:4770-->0.05<!--/v8--> |
| N-Sigma chính / ts-auth-service / delay | [<!--v8:4771-->1440<!--/v8-->, <!--v8:4772-->1441<!--/v8-->) | <!--v8:4773-->0<!--/v8-->/<!--v8:4774-->3<!--/v8--> | <!--v8:4775-->0<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4776-->720<!--/v8-->, <!--v8:4777-->780<!--/v8-->) | <!--v8:4778-->66<!--/v8-->/<!--v8:4779-->180<!--/v8--> | <!--v8:4780-->0.366667<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4781-->780<!--/v8-->, <!--v8:4782-->840<!--/v8-->) | <!--v8:4783-->123<!--/v8-->/<!--v8:4784-->180<!--/v8--> | <!--v8:4785-->0.683333<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4786-->840<!--/v8-->, <!--v8:4787-->900<!--/v8-->) | <!--v8:4788-->55<!--/v8-->/<!--v8:4789-->180<!--/v8--> | <!--v8:4790-->0.305556<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4791-->900<!--/v8-->, <!--v8:4792-->960<!--/v8-->) | <!--v8:4793-->27<!--/v8-->/<!--v8:4794-->180<!--/v8--> | <!--v8:4795-->0.15<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4796-->960<!--/v8-->, <!--v8:4797-->1020<!--/v8-->) | <!--v8:4798-->26<!--/v8-->/<!--v8:4799-->180<!--/v8--> | <!--v8:4800-->0.144444<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4801-->1020<!--/v8-->, <!--v8:4802-->1080<!--/v8-->) | <!--v8:4803-->41<!--/v8-->/<!--v8:4804-->180<!--/v8--> | <!--v8:4805-->0.227778<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4806-->1080<!--/v8-->, <!--v8:4807-->1140<!--/v8-->) | <!--v8:4808-->11<!--/v8-->/<!--v8:4809-->180<!--/v8--> | <!--v8:4810-->0.0611111<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4811-->1140<!--/v8-->, <!--v8:4812-->1200<!--/v8-->) | <!--v8:4813-->14<!--/v8-->/<!--v8:4814-->180<!--/v8--> | <!--v8:4815-->0.0777778<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4816-->1200<!--/v8-->, <!--v8:4817-->1260<!--/v8-->) | <!--v8:4818-->45<!--/v8-->/<!--v8:4819-->180<!--/v8--> | <!--v8:4820-->0.25<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4821-->1260<!--/v8-->, <!--v8:4822-->1320<!--/v8-->) | <!--v8:4823-->67<!--/v8-->/<!--v8:4824-->180<!--/v8--> | <!--v8:4825-->0.372222<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4826-->1320<!--/v8-->, <!--v8:4827-->1380<!--/v8-->) | <!--v8:4828-->67<!--/v8-->/<!--v8:4829-->180<!--/v8--> | <!--v8:4830-->0.372222<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4831-->1380<!--/v8-->, <!--v8:4832-->1440<!--/v8-->) | <!--v8:4833-->79<!--/v8-->/<!--v8:4834-->180<!--/v8--> | <!--v8:4835-->0.438889<!--/v8--> |
| N-Sigma chính / ts-order-service / disk | [<!--v8:4836-->1440<!--/v8-->, <!--v8:4837-->1441<!--/v8-->) | <!--v8:4838-->2<!--/v8-->/<!--v8:4839-->3<!--/v8--> | <!--v8:4840-->0.666667<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4841-->720<!--/v8-->, <!--v8:4842-->780<!--/v8-->) | <!--v8:4843-->76<!--/v8-->/<!--v8:4844-->180<!--/v8--> | <!--v8:4845-->0.422222<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4846-->780<!--/v8-->, <!--v8:4847-->840<!--/v8-->) | <!--v8:4848-->114<!--/v8-->/<!--v8:4849-->180<!--/v8--> | <!--v8:4850-->0.633333<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4851-->840<!--/v8-->, <!--v8:4852-->900<!--/v8-->) | <!--v8:4853-->134<!--/v8-->/<!--v8:4854-->180<!--/v8--> | <!--v8:4855-->0.744444<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4856-->900<!--/v8-->, <!--v8:4857-->960<!--/v8-->) | <!--v8:4858-->114<!--/v8-->/<!--v8:4859-->180<!--/v8--> | <!--v8:4860-->0.633333<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4861-->960<!--/v8-->, <!--v8:4862-->1020<!--/v8-->) | <!--v8:4863-->89<!--/v8-->/<!--v8:4864-->180<!--/v8--> | <!--v8:4865-->0.494444<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4866-->1020<!--/v8-->, <!--v8:4867-->1080<!--/v8-->) | <!--v8:4868-->152<!--/v8-->/<!--v8:4869-->180<!--/v8--> | <!--v8:4870-->0.844444<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4871-->1080<!--/v8-->, <!--v8:4872-->1140<!--/v8-->) | <!--v8:4873-->135<!--/v8-->/<!--v8:4874-->180<!--/v8--> | <!--v8:4875-->0.75<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4876-->1140<!--/v8-->, <!--v8:4877-->1200<!--/v8-->) | <!--v8:4878-->109<!--/v8-->/<!--v8:4879-->180<!--/v8--> | <!--v8:4880-->0.605556<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4881-->1200<!--/v8-->, <!--v8:4882-->1260<!--/v8-->) | <!--v8:4883-->124<!--/v8-->/<!--v8:4884-->180<!--/v8--> | <!--v8:4885-->0.688889<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4886-->1260<!--/v8-->, <!--v8:4887-->1320<!--/v8-->) | <!--v8:4888-->47<!--/v8-->/<!--v8:4889-->180<!--/v8--> | <!--v8:4890-->0.261111<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4891-->1320<!--/v8-->, <!--v8:4892-->1380<!--/v8-->) | <!--v8:4893-->69<!--/v8-->/<!--v8:4894-->180<!--/v8--> | <!--v8:4895-->0.383333<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4896-->1380<!--/v8-->, <!--v8:4897-->1440<!--/v8-->) | <!--v8:4898-->135<!--/v8-->/<!--v8:4899-->180<!--/v8--> | <!--v8:4900-->0.75<!--/v8--> |
| N-Sigma chính / ts-order-service / loss | [<!--v8:4901-->1440<!--/v8-->, <!--v8:4902-->1441<!--/v8-->) | <!--v8:4903-->2<!--/v8-->/<!--v8:4904-->3<!--/v8--> | <!--v8:4905-->0.666667<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4906-->720<!--/v8-->, <!--v8:4907-->780<!--/v8-->) | <!--v8:4908-->122<!--/v8-->/<!--v8:4909-->180<!--/v8--> | <!--v8:4910-->0.677778<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4911-->780<!--/v8-->, <!--v8:4912-->840<!--/v8-->) | <!--v8:4913-->144<!--/v8-->/<!--v8:4914-->180<!--/v8--> | <!--v8:4915-->0.8<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4916-->840<!--/v8-->, <!--v8:4917-->900<!--/v8-->) | <!--v8:4918-->162<!--/v8-->/<!--v8:4919-->180<!--/v8--> | <!--v8:4920-->0.9<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4921-->900<!--/v8-->, <!--v8:4922-->960<!--/v8-->) | <!--v8:4923-->116<!--/v8-->/<!--v8:4924-->180<!--/v8--> | <!--v8:4925-->0.644444<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4926-->960<!--/v8-->, <!--v8:4927-->1020<!--/v8-->) | <!--v8:4928-->88<!--/v8-->/<!--v8:4929-->180<!--/v8--> | <!--v8:4930-->0.488889<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4931-->1020<!--/v8-->, <!--v8:4932-->1080<!--/v8-->) | <!--v8:4933-->64<!--/v8-->/<!--v8:4934-->180<!--/v8--> | <!--v8:4935-->0.355556<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4936-->1080<!--/v8-->, <!--v8:4937-->1140<!--/v8-->) | <!--v8:4938-->46<!--/v8-->/<!--v8:4939-->180<!--/v8--> | <!--v8:4940-->0.255556<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4941-->1140<!--/v8-->, <!--v8:4942-->1200<!--/v8-->) | <!--v8:4943-->17<!--/v8-->/<!--v8:4944-->180<!--/v8--> | <!--v8:4945-->0.0944444<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4946-->1200<!--/v8-->, <!--v8:4947-->1260<!--/v8-->) | <!--v8:4948-->11<!--/v8-->/<!--v8:4949-->180<!--/v8--> | <!--v8:4950-->0.0611111<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4951-->1260<!--/v8-->, <!--v8:4952-->1320<!--/v8-->) | <!--v8:4953-->67<!--/v8-->/<!--v8:4954-->180<!--/v8--> | <!--v8:4955-->0.372222<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4956-->1320<!--/v8-->, <!--v8:4957-->1380<!--/v8-->) | <!--v8:4958-->56<!--/v8-->/<!--v8:4959-->180<!--/v8--> | <!--v8:4960-->0.311111<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4961-->1380<!--/v8-->, <!--v8:4962-->1440<!--/v8-->) | <!--v8:4963-->73<!--/v8-->/<!--v8:4964-->180<!--/v8--> | <!--v8:4965-->0.405556<!--/v8--> |
| N-Sigma chính / ts-route-service / mem | [<!--v8:4966-->1440<!--/v8-->, <!--v8:4967-->1441<!--/v8-->) | <!--v8:4968-->1<!--/v8-->/<!--v8:4969-->3<!--/v8--> | <!--v8:4970-->0.333333<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:4971-->720<!--/v8-->, <!--v8:4972-->780<!--/v8-->) | <!--v8:4973-->123<!--/v8-->/<!--v8:4974-->180<!--/v8--> | <!--v8:4975-->0.683333<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:4976-->780<!--/v8-->, <!--v8:4977-->840<!--/v8-->) | <!--v8:4978-->159<!--/v8-->/<!--v8:4979-->180<!--/v8--> | <!--v8:4980-->0.883333<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:4981-->840<!--/v8-->, <!--v8:4982-->900<!--/v8-->) | <!--v8:4983-->118<!--/v8-->/<!--v8:4984-->180<!--/v8--> | <!--v8:4985-->0.655556<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:4986-->900<!--/v8-->, <!--v8:4987-->960<!--/v8-->) | <!--v8:4988-->36<!--/v8-->/<!--v8:4989-->180<!--/v8--> | <!--v8:4990-->0.2<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:4991-->960<!--/v8-->, <!--v8:4992-->1020<!--/v8-->) | <!--v8:4993-->9<!--/v8-->/<!--v8:4994-->180<!--/v8--> | <!--v8:4995-->0.05<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:4996-->1020<!--/v8-->, <!--v8:4997-->1080<!--/v8-->) | <!--v8:4998-->44<!--/v8-->/<!--v8:4999-->180<!--/v8--> | <!--v8:5000-->0.244444<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5001-->1080<!--/v8-->, <!--v8:5002-->1140<!--/v8-->) | <!--v8:5003-->10<!--/v8-->/<!--v8:5004-->180<!--/v8--> | <!--v8:5005-->0.0555556<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5006-->1140<!--/v8-->, <!--v8:5007-->1200<!--/v8-->) | <!--v8:5008-->68<!--/v8-->/<!--v8:5009-->180<!--/v8--> | <!--v8:5010-->0.377778<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5011-->1200<!--/v8-->, <!--v8:5012-->1260<!--/v8-->) | <!--v8:5013-->22<!--/v8-->/<!--v8:5014-->180<!--/v8--> | <!--v8:5015-->0.122222<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5016-->1260<!--/v8-->, <!--v8:5017-->1320<!--/v8-->) | <!--v8:5018-->53<!--/v8-->/<!--v8:5019-->180<!--/v8--> | <!--v8:5020-->0.294444<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5021-->1320<!--/v8-->, <!--v8:5022-->1380<!--/v8-->) | <!--v8:5023-->86<!--/v8-->/<!--v8:5024-->180<!--/v8--> | <!--v8:5025-->0.477778<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5026-->1380<!--/v8-->, <!--v8:5027-->1440<!--/v8-->) | <!--v8:5028-->61<!--/v8-->/<!--v8:5029-->180<!--/v8--> | <!--v8:5030-->0.338889<!--/v8--> |
| N-Sigma chính / ts-route-service / socket | [<!--v8:5031-->1440<!--/v8-->, <!--v8:5032-->1441<!--/v8-->) | <!--v8:5033-->1<!--/v8-->/<!--v8:5034-->3<!--/v8--> | <!--v8:5035-->0.333333<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5036-->720<!--/v8-->, <!--v8:5037-->780<!--/v8-->) | <!--v8:5038-->137<!--/v8-->/<!--v8:5039-->180<!--/v8--> | <!--v8:5040-->0.761111<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5041-->780<!--/v8-->, <!--v8:5042-->840<!--/v8-->) | <!--v8:5043-->177<!--/v8-->/<!--v8:5044-->180<!--/v8--> | <!--v8:5045-->0.983333<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5046-->840<!--/v8-->, <!--v8:5047-->900<!--/v8-->) | <!--v8:5048-->123<!--/v8-->/<!--v8:5049-->180<!--/v8--> | <!--v8:5050-->0.683333<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5051-->900<!--/v8-->, <!--v8:5052-->960<!--/v8-->) | <!--v8:5053-->110<!--/v8-->/<!--v8:5054-->180<!--/v8--> | <!--v8:5055-->0.611111<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5056-->960<!--/v8-->, <!--v8:5057-->1020<!--/v8-->) | <!--v8:5058-->70<!--/v8-->/<!--v8:5059-->180<!--/v8--> | <!--v8:5060-->0.388889<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5061-->1020<!--/v8-->, <!--v8:5062-->1080<!--/v8-->) | <!--v8:5063-->117<!--/v8-->/<!--v8:5064-->180<!--/v8--> | <!--v8:5065-->0.65<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5066-->1080<!--/v8-->, <!--v8:5067-->1140<!--/v8-->) | <!--v8:5068-->104<!--/v8-->/<!--v8:5069-->180<!--/v8--> | <!--v8:5070-->0.577778<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5071-->1140<!--/v8-->, <!--v8:5072-->1200<!--/v8-->) | <!--v8:5073-->88<!--/v8-->/<!--v8:5074-->180<!--/v8--> | <!--v8:5075-->0.488889<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5076-->1200<!--/v8-->, <!--v8:5077-->1260<!--/v8-->) | <!--v8:5078-->86<!--/v8-->/<!--v8:5079-->180<!--/v8--> | <!--v8:5080-->0.477778<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5081-->1260<!--/v8-->, <!--v8:5082-->1320<!--/v8-->) | <!--v8:5083-->54<!--/v8-->/<!--v8:5084-->180<!--/v8--> | <!--v8:5085-->0.3<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5086-->1320<!--/v8-->, <!--v8:5087-->1380<!--/v8-->) | <!--v8:5088-->15<!--/v8-->/<!--v8:5089-->180<!--/v8--> | <!--v8:5090-->0.0833333<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5091-->1380<!--/v8-->, <!--v8:5092-->1440<!--/v8-->) | <!--v8:5093-->59<!--/v8-->/<!--v8:5094-->180<!--/v8--> | <!--v8:5095-->0.327778<!--/v8--> |
| N-Sigma chính / ts-train-service / cpu | [<!--v8:5096-->1440<!--/v8-->, <!--v8:5097-->1441<!--/v8-->) | <!--v8:5098-->0<!--/v8-->/<!--v8:5099-->3<!--/v8--> | <!--v8:5100-->0<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5101-->720<!--/v8-->, <!--v8:5102-->780<!--/v8-->) | <!--v8:5103-->156<!--/v8-->/<!--v8:5104-->180<!--/v8--> | <!--v8:5105-->0.866667<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5106-->780<!--/v8-->, <!--v8:5107-->840<!--/v8-->) | <!--v8:5108-->180<!--/v8-->/<!--v8:5109-->180<!--/v8--> | <!--v8:5110-->1<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5111-->840<!--/v8-->, <!--v8:5112-->900<!--/v8-->) | <!--v8:5113-->138<!--/v8-->/<!--v8:5114-->180<!--/v8--> | <!--v8:5115-->0.766667<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5116-->900<!--/v8-->, <!--v8:5117-->960<!--/v8-->) | <!--v8:5118-->59<!--/v8-->/<!--v8:5119-->180<!--/v8--> | <!--v8:5120-->0.327778<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5121-->960<!--/v8-->, <!--v8:5122-->1020<!--/v8-->) | <!--v8:5123-->73<!--/v8-->/<!--v8:5124-->180<!--/v8--> | <!--v8:5125-->0.405556<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5126-->1020<!--/v8-->, <!--v8:5127-->1080<!--/v8-->) | <!--v8:5128-->75<!--/v8-->/<!--v8:5129-->180<!--/v8--> | <!--v8:5130-->0.416667<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5131-->1080<!--/v8-->, <!--v8:5132-->1140<!--/v8-->) | <!--v8:5133-->58<!--/v8-->/<!--v8:5134-->180<!--/v8--> | <!--v8:5135-->0.322222<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5136-->1140<!--/v8-->, <!--v8:5137-->1200<!--/v8-->) | <!--v8:5138-->68<!--/v8-->/<!--v8:5139-->180<!--/v8--> | <!--v8:5140-->0.377778<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5141-->1200<!--/v8-->, <!--v8:5142-->1260<!--/v8-->) | <!--v8:5143-->57<!--/v8-->/<!--v8:5144-->180<!--/v8--> | <!--v8:5145-->0.316667<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5146-->1260<!--/v8-->, <!--v8:5147-->1320<!--/v8-->) | <!--v8:5148-->13<!--/v8-->/<!--v8:5149-->180<!--/v8--> | <!--v8:5150-->0.0722222<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5151-->1320<!--/v8-->, <!--v8:5152-->1380<!--/v8-->) | <!--v8:5153-->104<!--/v8-->/<!--v8:5154-->180<!--/v8--> | <!--v8:5155-->0.577778<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5156-->1380<!--/v8-->, <!--v8:5157-->1440<!--/v8-->) | <!--v8:5158-->116<!--/v8-->/<!--v8:5159-->180<!--/v8--> | <!--v8:5160-->0.644444<!--/v8--> |
| N-Sigma chính / ts-train-service / delay | [<!--v8:5161-->1440<!--/v8-->, <!--v8:5162-->1441<!--/v8-->) | <!--v8:5163-->2<!--/v8-->/<!--v8:5164-->3<!--/v8--> | <!--v8:5165-->0.666667<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5166-->720<!--/v8-->, <!--v8:5167-->780<!--/v8-->) | <!--v8:5168-->90<!--/v8-->/<!--v8:5169-->180<!--/v8--> | <!--v8:5170-->0.5<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5171-->780<!--/v8-->, <!--v8:5172-->840<!--/v8-->) | <!--v8:5173-->143<!--/v8-->/<!--v8:5174-->180<!--/v8--> | <!--v8:5175-->0.794444<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5176-->840<!--/v8-->, <!--v8:5177-->900<!--/v8-->) | <!--v8:5178-->115<!--/v8-->/<!--v8:5179-->180<!--/v8--> | <!--v8:5180-->0.638889<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5181-->900<!--/v8-->, <!--v8:5182-->960<!--/v8-->) | <!--v8:5183-->57<!--/v8-->/<!--v8:5184-->180<!--/v8--> | <!--v8:5185-->0.316667<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5186-->960<!--/v8-->, <!--v8:5187-->1020<!--/v8-->) | <!--v8:5188-->65<!--/v8-->/<!--v8:5189-->180<!--/v8--> | <!--v8:5190-->0.361111<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5191-->1020<!--/v8-->, <!--v8:5192-->1080<!--/v8-->) | <!--v8:5193-->69<!--/v8-->/<!--v8:5194-->180<!--/v8--> | <!--v8:5195-->0.383333<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5196-->1080<!--/v8-->, <!--v8:5197-->1140<!--/v8-->) | <!--v8:5198-->95<!--/v8-->/<!--v8:5199-->180<!--/v8--> | <!--v8:5200-->0.527778<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5201-->1140<!--/v8-->, <!--v8:5202-->1200<!--/v8-->) | <!--v8:5203-->47<!--/v8-->/<!--v8:5204-->180<!--/v8--> | <!--v8:5205-->0.261111<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5206-->1200<!--/v8-->, <!--v8:5207-->1260<!--/v8-->) | <!--v8:5208-->31<!--/v8-->/<!--v8:5209-->180<!--/v8--> | <!--v8:5210-->0.172222<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5211-->1260<!--/v8-->, <!--v8:5212-->1320<!--/v8-->) | <!--v8:5213-->17<!--/v8-->/<!--v8:5214-->180<!--/v8--> | <!--v8:5215-->0.0944444<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5216-->1320<!--/v8-->, <!--v8:5217-->1380<!--/v8-->) | <!--v8:5218-->40<!--/v8-->/<!--v8:5219-->180<!--/v8--> | <!--v8:5220-->0.222222<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5221-->1380<!--/v8-->, <!--v8:5222-->1440<!--/v8-->) | <!--v8:5223-->13<!--/v8-->/<!--v8:5224-->180<!--/v8--> | <!--v8:5225-->0.0722222<!--/v8--> |
| N-Sigma chính / ts-travel-service / disk | [<!--v8:5226-->1440<!--/v8-->, <!--v8:5227-->1441<!--/v8-->) | <!--v8:5228-->0<!--/v8-->/<!--v8:5229-->3<!--/v8--> | <!--v8:5230-->0<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5231-->720<!--/v8-->, <!--v8:5232-->780<!--/v8-->) | <!--v8:5233-->156<!--/v8-->/<!--v8:5234-->180<!--/v8--> | <!--v8:5235-->0.866667<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5236-->780<!--/v8-->, <!--v8:5237-->840<!--/v8-->) | <!--v8:5238-->180<!--/v8-->/<!--v8:5239-->180<!--/v8--> | <!--v8:5240-->1<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5241-->840<!--/v8-->, <!--v8:5242-->900<!--/v8-->) | <!--v8:5243-->115<!--/v8-->/<!--v8:5244-->180<!--/v8--> | <!--v8:5245-->0.638889<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5246-->900<!--/v8-->, <!--v8:5247-->960<!--/v8-->) | <!--v8:5248-->103<!--/v8-->/<!--v8:5249-->180<!--/v8--> | <!--v8:5250-->0.572222<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5251-->960<!--/v8-->, <!--v8:5252-->1020<!--/v8-->) | <!--v8:5253-->88<!--/v8-->/<!--v8:5254-->180<!--/v8--> | <!--v8:5255-->0.488889<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5256-->1020<!--/v8-->, <!--v8:5257-->1080<!--/v8-->) | <!--v8:5258-->85<!--/v8-->/<!--v8:5259-->180<!--/v8--> | <!--v8:5260-->0.472222<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5261-->1080<!--/v8-->, <!--v8:5262-->1140<!--/v8-->) | <!--v8:5263-->120<!--/v8-->/<!--v8:5264-->180<!--/v8--> | <!--v8:5265-->0.666667<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5266-->1140<!--/v8-->, <!--v8:5267-->1200<!--/v8-->) | <!--v8:5268-->104<!--/v8-->/<!--v8:5269-->180<!--/v8--> | <!--v8:5270-->0.577778<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5271-->1200<!--/v8-->, <!--v8:5272-->1260<!--/v8-->) | <!--v8:5273-->104<!--/v8-->/<!--v8:5274-->180<!--/v8--> | <!--v8:5275-->0.577778<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5276-->1260<!--/v8-->, <!--v8:5277-->1320<!--/v8-->) | <!--v8:5278-->105<!--/v8-->/<!--v8:5279-->180<!--/v8--> | <!--v8:5280-->0.583333<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5281-->1320<!--/v8-->, <!--v8:5282-->1380<!--/v8-->) | <!--v8:5283-->26<!--/v8-->/<!--v8:5284-->180<!--/v8--> | <!--v8:5285-->0.144444<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5286-->1380<!--/v8-->, <!--v8:5287-->1440<!--/v8-->) | <!--v8:5288-->43<!--/v8-->/<!--v8:5289-->180<!--/v8--> | <!--v8:5290-->0.238889<!--/v8--> |
| N-Sigma chính / ts-travel-service / loss | [<!--v8:5291-->1440<!--/v8-->, <!--v8:5292-->1441<!--/v8-->) | <!--v8:5293-->0<!--/v8-->/<!--v8:5294-->3<!--/v8--> | <!--v8:5295-->0<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5296-->720<!--/v8-->, <!--v8:5297-->780<!--/v8-->) | <!--v8:5298-->1800<!--/v8-->/<!--v8:5299-->1800<!--/v8--> | <!--v8:5300-->1<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5301-->780<!--/v8-->, <!--v8:5302-->840<!--/v8-->) | <!--v8:5303-->1800<!--/v8-->/<!--v8:5304-->1800<!--/v8--> | <!--v8:5305-->1<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5306-->840<!--/v8-->, <!--v8:5307-->900<!--/v8-->) | <!--v8:5308-->1800<!--/v8-->/<!--v8:5309-->1800<!--/v8--> | <!--v8:5310-->1<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5311-->900<!--/v8-->, <!--v8:5312-->960<!--/v8-->) | <!--v8:5313-->1782<!--/v8-->/<!--v8:5314-->1800<!--/v8--> | <!--v8:5315-->0.99<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5316-->960<!--/v8-->, <!--v8:5317-->1020<!--/v8-->) | <!--v8:5318-->1782<!--/v8-->/<!--v8:5319-->1800<!--/v8--> | <!--v8:5320-->0.99<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5321-->1020<!--/v8-->, <!--v8:5322-->1080<!--/v8-->) | <!--v8:5323-->1793<!--/v8-->/<!--v8:5324-->1800<!--/v8--> | <!--v8:5325-->0.996111<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5326-->1080<!--/v8-->, <!--v8:5327-->1140<!--/v8-->) | <!--v8:5328-->1797<!--/v8-->/<!--v8:5329-->1800<!--/v8--> | <!--v8:5330-->0.998333<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5331-->1140<!--/v8-->, <!--v8:5332-->1200<!--/v8-->) | <!--v8:5333-->1783<!--/v8-->/<!--v8:5334-->1800<!--/v8--> | <!--v8:5335-->0.990556<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5336-->1200<!--/v8-->, <!--v8:5337-->1260<!--/v8-->) | <!--v8:5338-->1778<!--/v8-->/<!--v8:5339-->1800<!--/v8--> | <!--v8:5340-->0.987778<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5341-->1260<!--/v8-->, <!--v8:5342-->1320<!--/v8-->) | <!--v8:5343-->1744<!--/v8-->/<!--v8:5344-->1800<!--/v8--> | <!--v8:5345-->0.968889<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5346-->1320<!--/v8-->, <!--v8:5347-->1380<!--/v8-->) | <!--v8:5348-->1748<!--/v8-->/<!--v8:5349-->1800<!--/v8--> | <!--v8:5350-->0.971111<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5351-->1380<!--/v8-->, <!--v8:5352-->1440<!--/v8-->) | <!--v8:5353-->1731<!--/v8-->/<!--v8:5354-->1800<!--/v8--> | <!--v8:5355-->0.961667<!--/v8--> |
| N-Sigma đối chứng / all | [<!--v8:5356-->1440<!--/v8-->, <!--v8:5357-->1441<!--/v8-->) | <!--v8:5358-->28<!--/v8-->/<!--v8:5359-->30<!--/v8--> | <!--v8:5360-->0.933333<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5361-->720<!--/v8-->, <!--v8:5362-->780<!--/v8-->) | <!--v8:5363-->180<!--/v8-->/<!--v8:5364-->180<!--/v8--> | <!--v8:5365-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5366-->780<!--/v8-->, <!--v8:5367-->840<!--/v8-->) | <!--v8:5368-->180<!--/v8-->/<!--v8:5369-->180<!--/v8--> | <!--v8:5370-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5371-->840<!--/v8-->, <!--v8:5372-->900<!--/v8-->) | <!--v8:5373-->180<!--/v8-->/<!--v8:5374-->180<!--/v8--> | <!--v8:5375-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5376-->900<!--/v8-->, <!--v8:5377-->960<!--/v8-->) | <!--v8:5378-->176<!--/v8-->/<!--v8:5379-->180<!--/v8--> | <!--v8:5380-->0.977778<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5381-->960<!--/v8-->, <!--v8:5382-->1020<!--/v8-->) | <!--v8:5383-->178<!--/v8-->/<!--v8:5384-->180<!--/v8--> | <!--v8:5385-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5386-->1020<!--/v8-->, <!--v8:5387-->1080<!--/v8-->) | <!--v8:5388-->180<!--/v8-->/<!--v8:5389-->180<!--/v8--> | <!--v8:5390-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5391-->1080<!--/v8-->, <!--v8:5392-->1140<!--/v8-->) | <!--v8:5393-->180<!--/v8-->/<!--v8:5394-->180<!--/v8--> | <!--v8:5395-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5396-->1140<!--/v8-->, <!--v8:5397-->1200<!--/v8-->) | <!--v8:5398-->180<!--/v8-->/<!--v8:5399-->180<!--/v8--> | <!--v8:5400-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5401-->1200<!--/v8-->, <!--v8:5402-->1260<!--/v8-->) | <!--v8:5403-->180<!--/v8-->/<!--v8:5404-->180<!--/v8--> | <!--v8:5405-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5406-->1260<!--/v8-->, <!--v8:5407-->1320<!--/v8-->) | <!--v8:5408-->180<!--/v8-->/<!--v8:5409-->180<!--/v8--> | <!--v8:5410-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5411-->1320<!--/v8-->, <!--v8:5412-->1380<!--/v8-->) | <!--v8:5413-->180<!--/v8-->/<!--v8:5414-->180<!--/v8--> | <!--v8:5415-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5416-->1380<!--/v8-->, <!--v8:5417-->1440<!--/v8-->) | <!--v8:5418-->180<!--/v8-->/<!--v8:5419-->180<!--/v8--> | <!--v8:5420-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / cpu | [<!--v8:5421-->1440<!--/v8-->, <!--v8:5422-->1441<!--/v8-->) | <!--v8:5423-->3<!--/v8-->/<!--v8:5424-->3<!--/v8--> | <!--v8:5425-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5426-->720<!--/v8-->, <!--v8:5427-->780<!--/v8-->) | <!--v8:5428-->180<!--/v8-->/<!--v8:5429-->180<!--/v8--> | <!--v8:5430-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5431-->780<!--/v8-->, <!--v8:5432-->840<!--/v8-->) | <!--v8:5433-->180<!--/v8-->/<!--v8:5434-->180<!--/v8--> | <!--v8:5435-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5436-->840<!--/v8-->, <!--v8:5437-->900<!--/v8-->) | <!--v8:5438-->180<!--/v8-->/<!--v8:5439-->180<!--/v8--> | <!--v8:5440-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5441-->900<!--/v8-->, <!--v8:5442-->960<!--/v8-->) | <!--v8:5443-->170<!--/v8-->/<!--v8:5444-->180<!--/v8--> | <!--v8:5445-->0.944444<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5446-->960<!--/v8-->, <!--v8:5447-->1020<!--/v8-->) | <!--v8:5448-->166<!--/v8-->/<!--v8:5449-->180<!--/v8--> | <!--v8:5450-->0.922222<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5451-->1020<!--/v8-->, <!--v8:5452-->1080<!--/v8-->) | <!--v8:5453-->180<!--/v8-->/<!--v8:5454-->180<!--/v8--> | <!--v8:5455-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5456-->1080<!--/v8-->, <!--v8:5457-->1140<!--/v8-->) | <!--v8:5458-->180<!--/v8-->/<!--v8:5459-->180<!--/v8--> | <!--v8:5460-->1<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5461-->1140<!--/v8-->, <!--v8:5462-->1200<!--/v8-->) | <!--v8:5463-->175<!--/v8-->/<!--v8:5464-->180<!--/v8--> | <!--v8:5465-->0.972222<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5466-->1200<!--/v8-->, <!--v8:5467-->1260<!--/v8-->) | <!--v8:5468-->174<!--/v8-->/<!--v8:5469-->180<!--/v8--> | <!--v8:5470-->0.966667<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5471-->1260<!--/v8-->, <!--v8:5472-->1320<!--/v8-->) | <!--v8:5473-->152<!--/v8-->/<!--v8:5474-->180<!--/v8--> | <!--v8:5475-->0.844444<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5476-->1320<!--/v8-->, <!--v8:5477-->1380<!--/v8-->) | <!--v8:5478-->162<!--/v8-->/<!--v8:5479-->180<!--/v8--> | <!--v8:5480-->0.9<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5481-->1380<!--/v8-->, <!--v8:5482-->1440<!--/v8-->) | <!--v8:5483-->156<!--/v8-->/<!--v8:5484-->180<!--/v8--> | <!--v8:5485-->0.866667<!--/v8--> |
| N-Sigma đối chứng / ts-auth-service / delay | [<!--v8:5486-->1440<!--/v8-->, <!--v8:5487-->1441<!--/v8-->) | <!--v8:5488-->3<!--/v8-->/<!--v8:5489-->3<!--/v8--> | <!--v8:5490-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5491-->720<!--/v8-->, <!--v8:5492-->780<!--/v8-->) | <!--v8:5493-->180<!--/v8-->/<!--v8:5494-->180<!--/v8--> | <!--v8:5495-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5496-->780<!--/v8-->, <!--v8:5497-->840<!--/v8-->) | <!--v8:5498-->180<!--/v8-->/<!--v8:5499-->180<!--/v8--> | <!--v8:5500-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5501-->840<!--/v8-->, <!--v8:5502-->900<!--/v8-->) | <!--v8:5503-->180<!--/v8-->/<!--v8:5504-->180<!--/v8--> | <!--v8:5505-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5506-->900<!--/v8-->, <!--v8:5507-->960<!--/v8-->) | <!--v8:5508-->180<!--/v8-->/<!--v8:5509-->180<!--/v8--> | <!--v8:5510-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5511-->960<!--/v8-->, <!--v8:5512-->1020<!--/v8-->) | <!--v8:5513-->180<!--/v8-->/<!--v8:5514-->180<!--/v8--> | <!--v8:5515-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5516-->1020<!--/v8-->, <!--v8:5517-->1080<!--/v8-->) | <!--v8:5518-->180<!--/v8-->/<!--v8:5519-->180<!--/v8--> | <!--v8:5520-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5521-->1080<!--/v8-->, <!--v8:5522-->1140<!--/v8-->) | <!--v8:5523-->180<!--/v8-->/<!--v8:5524-->180<!--/v8--> | <!--v8:5525-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5526-->1140<!--/v8-->, <!--v8:5527-->1200<!--/v8-->) | <!--v8:5528-->180<!--/v8-->/<!--v8:5529-->180<!--/v8--> | <!--v8:5530-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5531-->1200<!--/v8-->, <!--v8:5532-->1260<!--/v8-->) | <!--v8:5533-->178<!--/v8-->/<!--v8:5534-->180<!--/v8--> | <!--v8:5535-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5536-->1260<!--/v8-->, <!--v8:5537-->1320<!--/v8-->) | <!--v8:5538-->178<!--/v8-->/<!--v8:5539-->180<!--/v8--> | <!--v8:5540-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5541-->1320<!--/v8-->, <!--v8:5542-->1380<!--/v8-->) | <!--v8:5543-->178<!--/v8-->/<!--v8:5544-->180<!--/v8--> | <!--v8:5545-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5546-->1380<!--/v8-->, <!--v8:5547-->1440<!--/v8-->) | <!--v8:5548-->176<!--/v8-->/<!--v8:5549-->180<!--/v8--> | <!--v8:5550-->0.977778<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / disk | [<!--v8:5551-->1440<!--/v8-->, <!--v8:5552-->1441<!--/v8-->) | <!--v8:5553-->3<!--/v8-->/<!--v8:5554-->3<!--/v8--> | <!--v8:5555-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5556-->720<!--/v8-->, <!--v8:5557-->780<!--/v8-->) | <!--v8:5558-->180<!--/v8-->/<!--v8:5559-->180<!--/v8--> | <!--v8:5560-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5561-->780<!--/v8-->, <!--v8:5562-->840<!--/v8-->) | <!--v8:5563-->180<!--/v8-->/<!--v8:5564-->180<!--/v8--> | <!--v8:5565-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5566-->840<!--/v8-->, <!--v8:5567-->900<!--/v8-->) | <!--v8:5568-->180<!--/v8-->/<!--v8:5569-->180<!--/v8--> | <!--v8:5570-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5571-->900<!--/v8-->, <!--v8:5572-->960<!--/v8-->) | <!--v8:5573-->176<!--/v8-->/<!--v8:5574-->180<!--/v8--> | <!--v8:5575-->0.977778<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5576-->960<!--/v8-->, <!--v8:5577-->1020<!--/v8-->) | <!--v8:5578-->180<!--/v8-->/<!--v8:5579-->180<!--/v8--> | <!--v8:5580-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5581-->1020<!--/v8-->, <!--v8:5582-->1080<!--/v8-->) | <!--v8:5583-->180<!--/v8-->/<!--v8:5584-->180<!--/v8--> | <!--v8:5585-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5586-->1080<!--/v8-->, <!--v8:5587-->1140<!--/v8-->) | <!--v8:5588-->180<!--/v8-->/<!--v8:5589-->180<!--/v8--> | <!--v8:5590-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5591-->1140<!--/v8-->, <!--v8:5592-->1200<!--/v8-->) | <!--v8:5593-->180<!--/v8-->/<!--v8:5594-->180<!--/v8--> | <!--v8:5595-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5596-->1200<!--/v8-->, <!--v8:5597-->1260<!--/v8-->) | <!--v8:5598-->180<!--/v8-->/<!--v8:5599-->180<!--/v8--> | <!--v8:5600-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5601-->1260<!--/v8-->, <!--v8:5602-->1320<!--/v8-->) | <!--v8:5603-->180<!--/v8-->/<!--v8:5604-->180<!--/v8--> | <!--v8:5605-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5606-->1320<!--/v8-->, <!--v8:5607-->1380<!--/v8-->) | <!--v8:5608-->180<!--/v8-->/<!--v8:5609-->180<!--/v8--> | <!--v8:5610-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5611-->1380<!--/v8-->, <!--v8:5612-->1440<!--/v8-->) | <!--v8:5613-->180<!--/v8-->/<!--v8:5614-->180<!--/v8--> | <!--v8:5615-->1<!--/v8--> |
| N-Sigma đối chứng / ts-order-service / loss | [<!--v8:5616-->1440<!--/v8-->, <!--v8:5617-->1441<!--/v8-->) | <!--v8:5618-->3<!--/v8-->/<!--v8:5619-->3<!--/v8--> | <!--v8:5620-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5621-->720<!--/v8-->, <!--v8:5622-->780<!--/v8-->) | <!--v8:5623-->180<!--/v8-->/<!--v8:5624-->180<!--/v8--> | <!--v8:5625-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5626-->780<!--/v8-->, <!--v8:5627-->840<!--/v8-->) | <!--v8:5628-->180<!--/v8-->/<!--v8:5629-->180<!--/v8--> | <!--v8:5630-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5631-->840<!--/v8-->, <!--v8:5632-->900<!--/v8-->) | <!--v8:5633-->180<!--/v8-->/<!--v8:5634-->180<!--/v8--> | <!--v8:5635-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5636-->900<!--/v8-->, <!--v8:5637-->960<!--/v8-->) | <!--v8:5638-->180<!--/v8-->/<!--v8:5639-->180<!--/v8--> | <!--v8:5640-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5641-->960<!--/v8-->, <!--v8:5642-->1020<!--/v8-->) | <!--v8:5643-->180<!--/v8-->/<!--v8:5644-->180<!--/v8--> | <!--v8:5645-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5646-->1020<!--/v8-->, <!--v8:5647-->1080<!--/v8-->) | <!--v8:5648-->178<!--/v8-->/<!--v8:5649-->180<!--/v8--> | <!--v8:5650-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5651-->1080<!--/v8-->, <!--v8:5652-->1140<!--/v8-->) | <!--v8:5653-->180<!--/v8-->/<!--v8:5654-->180<!--/v8--> | <!--v8:5655-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5656-->1140<!--/v8-->, <!--v8:5657-->1200<!--/v8-->) | <!--v8:5658-->178<!--/v8-->/<!--v8:5659-->180<!--/v8--> | <!--v8:5660-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5661-->1200<!--/v8-->, <!--v8:5662-->1260<!--/v8-->) | <!--v8:5663-->172<!--/v8-->/<!--v8:5664-->180<!--/v8--> | <!--v8:5665-->0.955556<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5666-->1260<!--/v8-->, <!--v8:5667-->1320<!--/v8-->) | <!--v8:5668-->176<!--/v8-->/<!--v8:5669-->180<!--/v8--> | <!--v8:5670-->0.977778<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5671-->1320<!--/v8-->, <!--v8:5672-->1380<!--/v8-->) | <!--v8:5673-->174<!--/v8-->/<!--v8:5674-->180<!--/v8--> | <!--v8:5675-->0.966667<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5676-->1380<!--/v8-->, <!--v8:5677-->1440<!--/v8-->) | <!--v8:5678-->175<!--/v8-->/<!--v8:5679-->180<!--/v8--> | <!--v8:5680-->0.972222<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / mem | [<!--v8:5681-->1440<!--/v8-->, <!--v8:5682-->1441<!--/v8-->) | <!--v8:5683-->3<!--/v8-->/<!--v8:5684-->3<!--/v8--> | <!--v8:5685-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5686-->720<!--/v8-->, <!--v8:5687-->780<!--/v8-->) | <!--v8:5688-->180<!--/v8-->/<!--v8:5689-->180<!--/v8--> | <!--v8:5690-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5691-->780<!--/v8-->, <!--v8:5692-->840<!--/v8-->) | <!--v8:5693-->180<!--/v8-->/<!--v8:5694-->180<!--/v8--> | <!--v8:5695-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5696-->840<!--/v8-->, <!--v8:5697-->900<!--/v8-->) | <!--v8:5698-->180<!--/v8-->/<!--v8:5699-->180<!--/v8--> | <!--v8:5700-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5701-->900<!--/v8-->, <!--v8:5702-->960<!--/v8-->) | <!--v8:5703-->180<!--/v8-->/<!--v8:5704-->180<!--/v8--> | <!--v8:5705-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5706-->960<!--/v8-->, <!--v8:5707-->1020<!--/v8-->) | <!--v8:5708-->180<!--/v8-->/<!--v8:5709-->180<!--/v8--> | <!--v8:5710-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5711-->1020<!--/v8-->, <!--v8:5712-->1080<!--/v8-->) | <!--v8:5713-->178<!--/v8-->/<!--v8:5714-->180<!--/v8--> | <!--v8:5715-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5716-->1080<!--/v8-->, <!--v8:5717-->1140<!--/v8-->) | <!--v8:5718-->180<!--/v8-->/<!--v8:5719-->180<!--/v8--> | <!--v8:5720-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5721-->1140<!--/v8-->, <!--v8:5722-->1200<!--/v8-->) | <!--v8:5723-->176<!--/v8-->/<!--v8:5724-->180<!--/v8--> | <!--v8:5725-->0.977778<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5726-->1200<!--/v8-->, <!--v8:5727-->1260<!--/v8-->) | <!--v8:5728-->180<!--/v8-->/<!--v8:5729-->180<!--/v8--> | <!--v8:5730-->1<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5731-->1260<!--/v8-->, <!--v8:5732-->1320<!--/v8-->) | <!--v8:5733-->164<!--/v8-->/<!--v8:5734-->180<!--/v8--> | <!--v8:5735-->0.911111<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5736-->1320<!--/v8-->, <!--v8:5737-->1380<!--/v8-->) | <!--v8:5738-->160<!--/v8-->/<!--v8:5739-->180<!--/v8--> | <!--v8:5740-->0.888889<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5741-->1380<!--/v8-->, <!--v8:5742-->1440<!--/v8-->) | <!--v8:5743-->165<!--/v8-->/<!--v8:5744-->180<!--/v8--> | <!--v8:5745-->0.916667<!--/v8--> |
| N-Sigma đối chứng / ts-route-service / socket | [<!--v8:5746-->1440<!--/v8-->, <!--v8:5747-->1441<!--/v8-->) | <!--v8:5748-->3<!--/v8-->/<!--v8:5749-->3<!--/v8--> | <!--v8:5750-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5751-->720<!--/v8-->, <!--v8:5752-->780<!--/v8-->) | <!--v8:5753-->180<!--/v8-->/<!--v8:5754-->180<!--/v8--> | <!--v8:5755-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5756-->780<!--/v8-->, <!--v8:5757-->840<!--/v8-->) | <!--v8:5758-->180<!--/v8-->/<!--v8:5759-->180<!--/v8--> | <!--v8:5760-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5761-->840<!--/v8-->, <!--v8:5762-->900<!--/v8-->) | <!--v8:5763-->180<!--/v8-->/<!--v8:5764-->180<!--/v8--> | <!--v8:5765-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5766-->900<!--/v8-->, <!--v8:5767-->960<!--/v8-->) | <!--v8:5768-->180<!--/v8-->/<!--v8:5769-->180<!--/v8--> | <!--v8:5770-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5771-->960<!--/v8-->, <!--v8:5772-->1020<!--/v8-->) | <!--v8:5773-->180<!--/v8-->/<!--v8:5774-->180<!--/v8--> | <!--v8:5775-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5776-->1020<!--/v8-->, <!--v8:5777-->1080<!--/v8-->) | <!--v8:5778-->180<!--/v8-->/<!--v8:5779-->180<!--/v8--> | <!--v8:5780-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5781-->1080<!--/v8-->, <!--v8:5782-->1140<!--/v8-->) | <!--v8:5783-->179<!--/v8-->/<!--v8:5784-->180<!--/v8--> | <!--v8:5785-->0.994444<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5786-->1140<!--/v8-->, <!--v8:5787-->1200<!--/v8-->) | <!--v8:5788-->180<!--/v8-->/<!--v8:5789-->180<!--/v8--> | <!--v8:5790-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5791-->1200<!--/v8-->, <!--v8:5792-->1260<!--/v8-->) | <!--v8:5793-->179<!--/v8-->/<!--v8:5794-->180<!--/v8--> | <!--v8:5795-->0.994444<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5796-->1260<!--/v8-->, <!--v8:5797-->1320<!--/v8-->) | <!--v8:5798-->180<!--/v8-->/<!--v8:5799-->180<!--/v8--> | <!--v8:5800-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5801-->1320<!--/v8-->, <!--v8:5802-->1380<!--/v8-->) | <!--v8:5803-->174<!--/v8-->/<!--v8:5804-->180<!--/v8--> | <!--v8:5805-->0.966667<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5806-->1380<!--/v8-->, <!--v8:5807-->1440<!--/v8-->) | <!--v8:5808-->162<!--/v8-->/<!--v8:5809-->180<!--/v8--> | <!--v8:5810-->0.9<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / cpu | [<!--v8:5811-->1440<!--/v8-->, <!--v8:5812-->1441<!--/v8-->) | <!--v8:5813-->2<!--/v8-->/<!--v8:5814-->3<!--/v8--> | <!--v8:5815-->0.666667<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5816-->720<!--/v8-->, <!--v8:5817-->780<!--/v8-->) | <!--v8:5818-->180<!--/v8-->/<!--v8:5819-->180<!--/v8--> | <!--v8:5820-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5821-->780<!--/v8-->, <!--v8:5822-->840<!--/v8-->) | <!--v8:5823-->180<!--/v8-->/<!--v8:5824-->180<!--/v8--> | <!--v8:5825-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5826-->840<!--/v8-->, <!--v8:5827-->900<!--/v8-->) | <!--v8:5828-->180<!--/v8-->/<!--v8:5829-->180<!--/v8--> | <!--v8:5830-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5831-->900<!--/v8-->, <!--v8:5832-->960<!--/v8-->) | <!--v8:5833-->180<!--/v8-->/<!--v8:5834-->180<!--/v8--> | <!--v8:5835-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5836-->960<!--/v8-->, <!--v8:5837-->1020<!--/v8-->) | <!--v8:5838-->178<!--/v8-->/<!--v8:5839-->180<!--/v8--> | <!--v8:5840-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5841-->1020<!--/v8-->, <!--v8:5842-->1080<!--/v8-->) | <!--v8:5843-->180<!--/v8-->/<!--v8:5844-->180<!--/v8--> | <!--v8:5845-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5846-->1080<!--/v8-->, <!--v8:5847-->1140<!--/v8-->) | <!--v8:5848-->180<!--/v8-->/<!--v8:5849-->180<!--/v8--> | <!--v8:5850-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5851-->1140<!--/v8-->, <!--v8:5852-->1200<!--/v8-->) | <!--v8:5853-->174<!--/v8-->/<!--v8:5854-->180<!--/v8--> | <!--v8:5855-->0.966667<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5856-->1200<!--/v8-->, <!--v8:5857-->1260<!--/v8-->) | <!--v8:5858-->177<!--/v8-->/<!--v8:5859-->180<!--/v8--> | <!--v8:5860-->0.983333<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5861-->1260<!--/v8-->, <!--v8:5862-->1320<!--/v8-->) | <!--v8:5863-->174<!--/v8-->/<!--v8:5864-->180<!--/v8--> | <!--v8:5865-->0.966667<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5866-->1320<!--/v8-->, <!--v8:5867-->1380<!--/v8-->) | <!--v8:5868-->180<!--/v8-->/<!--v8:5869-->180<!--/v8--> | <!--v8:5870-->1<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5871-->1380<!--/v8-->, <!--v8:5872-->1440<!--/v8-->) | <!--v8:5873-->177<!--/v8-->/<!--v8:5874-->180<!--/v8--> | <!--v8:5875-->0.983333<!--/v8--> |
| N-Sigma đối chứng / ts-train-service / delay | [<!--v8:5876-->1440<!--/v8-->, <!--v8:5877-->1441<!--/v8-->) | <!--v8:5878-->2<!--/v8-->/<!--v8:5879-->3<!--/v8--> | <!--v8:5880-->0.666667<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5881-->720<!--/v8-->, <!--v8:5882-->780<!--/v8-->) | <!--v8:5883-->180<!--/v8-->/<!--v8:5884-->180<!--/v8--> | <!--v8:5885-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5886-->780<!--/v8-->, <!--v8:5887-->840<!--/v8-->) | <!--v8:5888-->180<!--/v8-->/<!--v8:5889-->180<!--/v8--> | <!--v8:5890-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5891-->840<!--/v8-->, <!--v8:5892-->900<!--/v8-->) | <!--v8:5893-->180<!--/v8-->/<!--v8:5894-->180<!--/v8--> | <!--v8:5895-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5896-->900<!--/v8-->, <!--v8:5897-->960<!--/v8-->) | <!--v8:5898-->180<!--/v8-->/<!--v8:5899-->180<!--/v8--> | <!--v8:5900-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5901-->960<!--/v8-->, <!--v8:5902-->1020<!--/v8-->) | <!--v8:5903-->180<!--/v8-->/<!--v8:5904-->180<!--/v8--> | <!--v8:5905-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5906-->1020<!--/v8-->, <!--v8:5907-->1080<!--/v8-->) | <!--v8:5908-->177<!--/v8-->/<!--v8:5909-->180<!--/v8--> | <!--v8:5910-->0.983333<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5911-->1080<!--/v8-->, <!--v8:5912-->1140<!--/v8-->) | <!--v8:5913-->178<!--/v8-->/<!--v8:5914-->180<!--/v8--> | <!--v8:5915-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5916-->1140<!--/v8-->, <!--v8:5917-->1200<!--/v8-->) | <!--v8:5918-->180<!--/v8-->/<!--v8:5919-->180<!--/v8--> | <!--v8:5920-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5921-->1200<!--/v8-->, <!--v8:5922-->1260<!--/v8-->) | <!--v8:5923-->178<!--/v8-->/<!--v8:5924-->180<!--/v8--> | <!--v8:5925-->0.988889<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5926-->1260<!--/v8-->, <!--v8:5927-->1320<!--/v8-->) | <!--v8:5928-->180<!--/v8-->/<!--v8:5929-->180<!--/v8--> | <!--v8:5930-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5931-->1320<!--/v8-->, <!--v8:5932-->1380<!--/v8-->) | <!--v8:5933-->180<!--/v8-->/<!--v8:5934-->180<!--/v8--> | <!--v8:5935-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5936-->1380<!--/v8-->, <!--v8:5937-->1440<!--/v8-->) | <!--v8:5938-->180<!--/v8-->/<!--v8:5939-->180<!--/v8--> | <!--v8:5940-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / disk | [<!--v8:5941-->1440<!--/v8-->, <!--v8:5942-->1441<!--/v8-->) | <!--v8:5943-->3<!--/v8-->/<!--v8:5944-->3<!--/v8--> | <!--v8:5945-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5946-->720<!--/v8-->, <!--v8:5947-->780<!--/v8-->) | <!--v8:5948-->180<!--/v8-->/<!--v8:5949-->180<!--/v8--> | <!--v8:5950-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5951-->780<!--/v8-->, <!--v8:5952-->840<!--/v8-->) | <!--v8:5953-->180<!--/v8-->/<!--v8:5954-->180<!--/v8--> | <!--v8:5955-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5956-->840<!--/v8-->, <!--v8:5957-->900<!--/v8-->) | <!--v8:5958-->180<!--/v8-->/<!--v8:5959-->180<!--/v8--> | <!--v8:5960-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5961-->900<!--/v8-->, <!--v8:5962-->960<!--/v8-->) | <!--v8:5963-->180<!--/v8-->/<!--v8:5964-->180<!--/v8--> | <!--v8:5965-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5966-->960<!--/v8-->, <!--v8:5967-->1020<!--/v8-->) | <!--v8:5968-->180<!--/v8-->/<!--v8:5969-->180<!--/v8--> | <!--v8:5970-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5971-->1020<!--/v8-->, <!--v8:5972-->1080<!--/v8-->) | <!--v8:5973-->180<!--/v8-->/<!--v8:5974-->180<!--/v8--> | <!--v8:5975-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5976-->1080<!--/v8-->, <!--v8:5977-->1140<!--/v8-->) | <!--v8:5978-->180<!--/v8-->/<!--v8:5979-->180<!--/v8--> | <!--v8:5980-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5981-->1140<!--/v8-->, <!--v8:5982-->1200<!--/v8-->) | <!--v8:5983-->180<!--/v8-->/<!--v8:5984-->180<!--/v8--> | <!--v8:5985-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5986-->1200<!--/v8-->, <!--v8:5987-->1260<!--/v8-->) | <!--v8:5988-->180<!--/v8-->/<!--v8:5989-->180<!--/v8--> | <!--v8:5990-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5991-->1260<!--/v8-->, <!--v8:5992-->1320<!--/v8-->) | <!--v8:5993-->180<!--/v8-->/<!--v8:5994-->180<!--/v8--> | <!--v8:5995-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:5996-->1320<!--/v8-->, <!--v8:5997-->1380<!--/v8-->) | <!--v8:5998-->180<!--/v8-->/<!--v8:5999-->180<!--/v8--> | <!--v8:6000-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:6001-->1380<!--/v8-->, <!--v8:6002-->1440<!--/v8-->) | <!--v8:6003-->180<!--/v8-->/<!--v8:6004-->180<!--/v8--> | <!--v8:6005-->1<!--/v8--> |
| N-Sigma đối chứng / ts-travel-service / loss | [<!--v8:6006-->1440<!--/v8-->, <!--v8:6007-->1441<!--/v8-->) | <!--v8:6008-->3<!--/v8-->/<!--v8:6009-->3<!--/v8--> | <!--v8:6010-->1<!--/v8--> |

Số từng phút từng ca nằm trong `n-sigma-cot.json#/cases/<ca>/<bộ>/N6_minutes`; không gộp phút cuối ngắn thành một phút đầy đủ. Đường cong quan sát có thể giảm hoặc tăng trở lại; chưa có D độc lập để gọi đoạn sau là bình thường.

### B5 và I1/I2: số chiều, số điểm đổi theo ca

Nguồn: `bocpd-can-thiep.json#/cases/<ca>`. d có thể đi cùng root/schema và prior; bảng này không quy tác động riêng cho dimension.

| Ô | Ca | d | Điểm đổi Nv đầy đủ | I1 | I2 |
|---|---|---|---|---|---|
| ts-route-service / socket | dev-03d4910932 | <!--v8:6011-->28<!--/v8--> | <!--v8:6012-->3<!--/v8--> | <!--v8:6013-->15<!--/v8--> | <!--v8:6014-->15<!--/v8--> |
| ts-order-service / disk | dev-12a1a88069 | <!--v8:6015-->33<!--/v8--> | <!--v8:6016-->4<!--/v8--> | <!--v8:6017-->6<!--/v8--> | <!--v8:6018-->6<!--/v8--> |
| ts-route-service / mem | dev-14372e1209 | <!--v8:6019-->29<!--/v8--> | <!--v8:6020-->3<!--/v8--> | <!--v8:6021-->3<!--/v8--> | <!--v8:6022-->3<!--/v8--> |
| ts-auth-service / cpu | dev-16597725c1 | <!--v8:6023-->34<!--/v8--> | <!--v8:6024-->5<!--/v8--> | <!--v8:6025-->8<!--/v8--> | <!--v8:6026-->8<!--/v8--> |
| ts-route-service / mem | dev-16870e660c | <!--v8:6027-->28<!--/v8--> | <!--v8:6028-->3<!--/v8--> | <!--v8:6029-->13<!--/v8--> | <!--v8:6030-->13<!--/v8--> |
| ts-order-service / disk | dev-1e6d61b5ec | <!--v8:6031-->23<!--/v8--> | <!--v8:6032-->12<!--/v8--> | <!--v8:6033-->11<!--/v8--> | <!--v8:6034-->11<!--/v8--> |
| ts-order-service / loss | dev-20acb4402d | <!--v8:6035-->22<!--/v8--> | <!--v8:6036-->9<!--/v8--> | <!--v8:6037-->13<!--/v8--> | <!--v8:6038-->13<!--/v8--> |
| ts-order-service / loss | dev-260d332c8d | <!--v8:6039-->22<!--/v8--> | <!--v8:6040-->8<!--/v8--> | <!--v8:6041-->12<!--/v8--> | <!--v8:6042-->10<!--/v8--> |
| ts-train-service / cpu | dev-3ae0a6c15a | <!--v8:6043-->36<!--/v8--> | <!--v8:6044-->3<!--/v8--> | <!--v8:6045-->13<!--/v8--> | <!--v8:6046-->11<!--/v8--> |
| ts-auth-service / cpu | dev-3defe3d34b | <!--v8:6047-->30<!--/v8--> | <!--v8:6048-->0<!--/v8--> | <!--v8:6049-->12<!--/v8--> | <!--v8:6050-->11<!--/v8--> |
| ts-train-service / delay | dev-4e68956051 | <!--v8:6051-->28<!--/v8--> | <!--v8:6052-->1<!--/v8--> | <!--v8:6053-->13<!--/v8--> | <!--v8:6054-->13<!--/v8--> |
| ts-route-service / mem | dev-4f8a844308 | <!--v8:6055-->39<!--/v8--> | <!--v8:6056-->2<!--/v8--> | <!--v8:6057-->6<!--/v8--> | <!--v8:6058-->6<!--/v8--> |
| ts-auth-service / delay | dev-57546fd87b | <!--v8:6059-->28<!--/v8--> | <!--v8:6060-->4<!--/v8--> | <!--v8:6061-->7<!--/v8--> | <!--v8:6062-->7<!--/v8--> |
| ts-auth-service / cpu | dev-59f696a169 | <!--v8:6063-->27<!--/v8--> | <!--v8:6064-->18<!--/v8--> | <!--v8:6065-->21<!--/v8--> | <!--v8:6066-->21<!--/v8--> |
| ts-auth-service / delay | dev-746fd74313 | <!--v8:6067-->32<!--/v8--> | <!--v8:6068-->3<!--/v8--> | <!--v8:6069-->13<!--/v8--> | <!--v8:6070-->13<!--/v8--> |
| ts-travel-service / loss | dev-7f1b6b071d | <!--v8:6071-->33<!--/v8--> | <!--v8:6072-->7<!--/v8--> | <!--v8:6073-->16<!--/v8--> | <!--v8:6074-->16<!--/v8--> |
| ts-order-service / disk | dev-8017c6dc70 | <!--v8:6075-->22<!--/v8--> | <!--v8:6076-->11<!--/v8--> | <!--v8:6077-->9<!--/v8--> | <!--v8:6078-->9<!--/v8--> |
| ts-train-service / cpu | dev-98bc73c499 | <!--v8:6079-->32<!--/v8--> | <!--v8:6080-->0<!--/v8--> | <!--v8:6081-->11<!--/v8--> | <!--v8:6082-->11<!--/v8--> |
| ts-train-service / delay | dev-a505ab3f65 | <!--v8:6083-->31<!--/v8--> | <!--v8:6084-->3<!--/v8--> | <!--v8:6085-->18<!--/v8--> | <!--v8:6086-->18<!--/v8--> |
| ts-travel-service / loss | dev-a5cabe5fa7 | <!--v8:6087-->30<!--/v8--> | <!--v8:6088-->6<!--/v8--> | <!--v8:6089-->8<!--/v8--> | <!--v8:6090-->8<!--/v8--> |
| ts-travel-service / loss | dev-a915aa2424 | <!--v8:6091-->32<!--/v8--> | <!--v8:6092-->1<!--/v8--> | <!--v8:6093-->10<!--/v8--> | <!--v8:6094-->10<!--/v8--> |
| ts-route-service / socket | dev-b8bd0abf60 | <!--v8:6095-->32<!--/v8--> | <!--v8:6096-->3<!--/v8--> | <!--v8:6097-->16<!--/v8--> | <!--v8:6098-->16<!--/v8--> |
| ts-train-service / cpu | dev-ba831dbeb8 | <!--v8:6099-->36<!--/v8--> | <!--v8:6100-->3<!--/v8--> | <!--v8:6101-->17<!--/v8--> | <!--v8:6102-->17<!--/v8--> |
| ts-route-service / socket | dev-bcbd4f46ae | <!--v8:6103-->28<!--/v8--> | <!--v8:6104-->3<!--/v8--> | <!--v8:6105-->3<!--/v8--> | <!--v8:6106-->3<!--/v8--> |
| ts-travel-service / disk | dev-db293894ab | <!--v8:6107-->31<!--/v8--> | <!--v8:6108-->11<!--/v8--> | <!--v8:6109-->10<!--/v8--> | <!--v8:6110-->10<!--/v8--> |
| ts-travel-service / disk | dev-de89e2f9e9 | <!--v8:6111-->30<!--/v8--> | <!--v8:6112-->3<!--/v8--> | <!--v8:6113-->14<!--/v8--> | <!--v8:6114-->14<!--/v8--> |
| ts-order-service / loss | dev-f36d0647d5 | <!--v8:6115-->33<!--/v8--> | <!--v8:6116-->0<!--/v8--> | <!--v8:6117-->16<!--/v8--> | <!--v8:6118-->16<!--/v8--> |
| ts-auth-service / delay | dev-f81f88234e | <!--v8:6119-->28<!--/v8--> | <!--v8:6120-->4<!--/v8--> | <!--v8:6121-->4<!--/v8--> | <!--v8:6122-->4<!--/v8--> |
| ts-travel-service / disk | dev-f9a8e05ed7 | <!--v8:6123-->31<!--/v8--> | <!--v8:6124-->6<!--/v8--> | <!--v8:6125-->5<!--/v8--> | <!--v8:6126-->5<!--/v8--> |
| ts-train-service / delay | dev-fbc45b0c67 | <!--v8:6127-->28<!--/v8--> | <!--v8:6128-->4<!--/v8--> | <!--v8:6129-->15<!--/v8--> | <!--v8:6130-->14<!--/v8--> |

## C3 — Có chỉ ra vùng không

**Liên hệ/thiết kế.** [Định vị](dinh-vi.md) giữ từng ca, từng ô, mức nền ngẫu nhiên đều và mọi độ nhạy bỏ cột N2. N-Sigma cung cấp danh sách cột, còn xếp dịch vụ là phân tích thêm mapping. Thứ tự báo động đầu sau mốc chưa phải khởi phát; loại N2 không loại mọi báo động kéo qua mốc. BOCPD không chỉ ra cột hoặc service; bảng bước nhảy tại t̂⁺ là heuristic (quy tắc phân tích), không là output BOCPD. Mức nền giữ toàn universe, gồm dịch vụ không có cột và không thể báo; chênh lệch với mức nền chưa tách giá trị detector khỏi thông tin tập cột. Coverage từng ca/bộ/độ nhạy được bổ sung ở định vị; không thay mức nền đã khóa. Không kết luận nhân quả, lan hoặc giá trị đồ thị từ bảng này.

## C4 — Phụ thuộc mốc biết trước

**Can thiệp I3.** [Bảng G](a-so-b.md) so ghép cặp Hit@1/Hit@5 ở mốc, t̂⁺ và t̂, giữ non-OK trong mẫu số, TORAI từng seed/ca và CIRCA vượt ngưỡng từng điểm. Δ cửa sổ = Hit(t̂⁺) − Hit(a); Δ sự kiện = Hit(t̂) − Hit(t̂⁺). Dấu âm/dương đều được giữ. I3 chọn nhờ nhãn mốc, không là cận trên hoặc xác nhận lỗi thật. Các chênh đổi cửa sổ còn đổi nền, graph và ứng viên; không là phân xử hai nguyên nhân độc lập.

Kết luận phụ thuộc cohort: bảng G có trường hợp CIRCA DA/BOCPD chênh sự kiện Hit@5 dương trên toàn mẫu nhưng âm ở cohort không vượt tại mọi điểm. Trung bình bằng nhau cũng có thể có ca lên và ca xuống; đọc các bảng ghép cặp thay vì gọi “không ảnh hưởng”.

## C5 — Nhãn proxy và schema

**P1 liên hệ; D chưa kiểm.** [Nhãn proxy và schema](nhan-proxy-va-schema.md) giữ timeline ngoài quantile / cột đủ, đủ/tổng và danh sách thiếu ở cả Nv. Nguồn chưa xác nhận D. Không suy D từ telemetry để chấm lại P/R/F1; số T-025 giữ theo proxy đã khai. Median quay về vùng nền chưa chứng minh lỗi kết thúc.

**P2 liên hệ.** Không có cột tách root hoàn toàn theo định nghĩa khóa, nhưng schema vẫn liên hệ một phần với root trong dev. Root và fault chưa giao chéo đầy đủ; không thể quy riêng cho chúng hoặc phủ nhận thông tin trong tổ hợp schema. Không đưa dấu vắng vào phương pháp.

## Giới hạn và trạng thái

Không có số công bố về phát hiện trên cùng RE2-TT và giao thức window để tái lập trực tiếp. Nguồn BARO là đối chiếu định tính. V1–V7 đã có kiểm từ các lượt lưu và hash tiếp nhận; V8 và kiểm V1 cuối được lưu trong lượt kiểm cuối báo cáo. [Đọc tay](doc-tay.md) giữ nguồn, trung gian, mọi S/D0 và ca V7 không phân biệt đúng số.

OPEN: D, clock tuyệt đối, nền sạch và nhãn mốc sự cố thật; ảnh hưởng hazard lên đoạn sau mốc chưa kiểm vì SPEC không chạy toàn bản ghi với hazard khác. Phạm vi chỉ là dev, bản ghi đã chọn vì có sự cố, nền cố định của SPEC. Không áp cho test, dataset giữ ngoài, Nezha, online hoặc nền khác. Không thiết kế P5/P6 ở task này; các phần sau chỉ trỏ HP-n. Chưa phản biện thay Claude hoặc tự đóng task.
