# Người làm — E1/E2, tương tác và thay đổi kết cục

Đây là phân tích của người làm, không là phản biện chính thức. Không đổi thiết kế hoặc lựa chọn sau khi nhìn số. `facts.json#/pairs` giữ đủ 52 ca cho sáu cặp, bốn nhánh cũ/mới × tắt/bật, hash snapshot, đơn vị/cờ, F_I, tầng/khóa, RR/M5 và counterpart. Mọi số bên dưới dẫn tới các file này; raw/API bổ sung ở `raw-api/`, `raw-api-002/`, không chạy lại M1.

## Đổi kết cục không đồng nghĩa đổi cơ chế riêng

Ba cặp thêm E1 có kết cục khác T-045:

| Cặp | T-045 → T-047 | RR mới tụt/lên/giữ | Điểm quyết định đã kiểm |
|---|---|---|---|
| E2+E5 → E1+E2+E5 | HẠI → KHÔNG TÁC DỤNG | 1/1/50 | M+M′ từ 3+1 còn 1+0; C-e mới tăng 13/30, không vượt 1; P=M=1 |
| E3 → E1+E3 | GIÚP → KHÔNG TÁC DỤNG | 1/8/43 | P/M/P′/M′ từ 7/3/0/2 thành 4/1/0/0; C-e tăng 1/5, không kích hoạt |
| E3+E5 → E1+E3+E5 | GIÚP → HẠI | 7/4/41 | Chỉ vế C-e gây HẠI: N1 tăng 17/5 trên 30 cửa sổ hợp lệ |

Nguồn: `facts.json#/pairs/<cặp>/outcomes`, `#/effects`; toàn bộ bước luật và RR theo ô ở `../../khoi-k.json#/cap`. Kết cục giống nhau ở ba thế giới. Đây là phân xử của luật đã khóa, không chứng minh một thành phần có cùng tác dụng trong mọi tổ hợp. G3/D1/S1 và vế C-e mới thay cùng lượt; không gán chênh tổng cho riêng một thay đổi. Bảng 2×2 tại P tách cổng và thang ở phần xếp hạng, nhưng không tách G3 khỏi D1.

## E1 trên nền E2+E5: một đường mất tác hại và một ca còn hại

Ca Nezha-OB `dev-1ac905bc95`, frontend/return: ở T-045, thêm E1 làm RR 1/3→1/5. Trong T-047, cả hai nhánh RR=1. Root có kênh log cùng s=1, nhưng F_I đổi 0→1 giữa hai lượt, tầng 2→1. Window, coverage và graph trong các nhánh đã đối chiếu; không có bằng chứng tập dữ liệu bị thay để đạt hạng này.

Đường cụ thể đã tái dựng: op `currencyservice/hipstershop.CurrencyService/Carry` có p G0=0,0084257833, F_raw=1; trên cùng mẫu thô, G3 cho p=0,0204897551, F_raw=0. API tái lập n_N/n_A, ngưỡng, tỷ lệ vượt, p, e và cờ native ở cả hai chế độ, không có trường lệch. Đây là một kênh giải thích thô bị cổng mới bỏ; các kênh giải thích khác và đường `inherited_by` nằm trong snapshot. Không quy toàn bộ thay đổi F_I của root chỉ cho một kênh này. Nguồn: `raw-api-002/dev-1ac905bc95.json#/native`, `#/recomputed`, `#/differences`; file case tương ứng ở `cases/E2+E5__E1+E2+E5/`.

Counterpart đúng cùng chữ ký là `dev-8ecd9880ed`, checkoutservice/return. Nó cũng có kênh log s=1, F_I cũ 0/mới 1; RR cũ 1/7 ở cả hai nhánh, mới 1 ở cả hai. Điều này bác bỏ cách nói E1 tự làm root mới đúng trong tất cả ca: ở đây đổi nền giải thích E5/cổng đã thay vị trí root trước khi thêm E1. Matching này cùng dataset/loại lỗi/chữ ký, không là can thiệp cùng root.

Ca còn hại `dev-a505ab3f65`, ts-train-service/delay, vẫn RR 1/2→1/3 ở cả hai lượt, M5 giữ true. Root còn tầng 1 và thay K_I/đối thủ theo mẫu độc quyền. Các ca loss `dev-7f1b6b071d` và `dev-f36d0647d5` không còn phần tụt nhỏ của lượt cũ; ca `dev-20acb4402d` có RR mới tăng 1/13→1/6 nhưng vẫn sai. Vì thế không gọi KHÔNG TÁC DỤNG là E1 không đổi gì, hoặc số ca hại giảm là mọi ca được sửa đúng. Nguồn: năm file case tương ứng và `facts.json`.

## E1 trên nền E3: mẫu đổi và cổng có thể làm mất kênh root

Ở `dev-63c30faf34`, recommendationservice/network_delay, thêm E1 đổi mẫu thao tác từ thời lượng đầy đủ sang độc quyền U và bỏ span bọc theo code. Nhánh mới trước E1 có hai kênh thao tác hướng xuống của root; sau E1 chúng không còn mang cờ, root từ tầng 1 xuống tầng 3. RR mới 1/5→2131/15120, M5 giữ true. Đây không phải chỉ là đối thủ đổi chỗ trong khi root giữ nguyên tín hiệu.

Đã tái dựng riêng raw→mẫu U→G0/G3 của `/hipstershop.RecommendationService/ListRecommendations`. Cùng mẫu U, p_xuong G0=0,0001218433 và F_raw=1; G3=0,0124937531 và F_raw=0. Hai API đều khớp native ở mọi trường chung đã kiểm. Nguồn: `raw-api-002/dev-63c30faf34.json`. Đường này phân biệt phần mẫu độc quyền với quyết định cổng trên chính mẫu đó; không gọi mọi mất kênh E1 là lỗi dữ liệu hoặc lỗi cài đặt.

Các ca đúng đối chiếu trong `facts.json#/pairs/E3|E1+E3/counterparts`, gồm nhóm CPU Nezha `dev-14701a3bbb`, `dev-7d3c2fe6d1`, `dev-95e164235f`, không có cùng đường mất root như ca trên. Không có ca đúng khớp toàn bộ chữ ký của ca hại network_delay này; phần đối chiếu chính xác còn thiếu được giữ OPEN. Những ca E1 giúp trên RE2 vẫn có trong cả bảng ca, không chỉ chọn ví dụ xấu. Việc P/M và mức chênh giảm làm bằng chứng GIÚP cũ không giữ, chứ không xác nhận E1 là thành phần hại trên mọi nền E3.

## E1 × E3 × E5 trên cửa sổ giả: phân xử vế HẠI mới

`ce-E1-E3-E5.json` đối chiếu toàn bộ 30 cửa sổ. Window, coverage, graph, đơn vị log/metric giữ nguyên khi bật E1; thay đổi thuộc mẫu thao tác/lớp kênh và hệ quả E5. Tái chạy đúng API E5 trên kênh thô và graph khớp F_I 60/60 nhánh. Không chạy một thiết kế đối chứng mới hoặc thay tham số.

N1 trung bình 17,1→20,5; 26 cửa sổ tăng, một giảm, ba giữ. Trong `dev-14372e1209`, N1 17→28. Hai kênh thao tác hướng xuống của ts-admin-basic-info-service vẫn có cờ nhưng đổi lớp `lan_nguoc`→`khong_lan`, F_I 0→1. Thực thể từ tầng 2 lên tầng 1; ts-admin-travel-service có đường tương tự. E5 không giải thích kênh `khong_lan` theo quy tắc đang dùng. Vậy vế C-e tăng N1 có đường tính toán cụ thể; không chỉ là tổng đếm vô cớ.

Không phải mọi cửa sổ đều tăng: `dev-de89e2f9e9` giảm 19→18 do một thực thể mất kênh sau đổi mẫu; `dev-16597725c1` giữ 15. Tương tác gồm cả đổi giá trị/mẫu và đổi lớp, không thể gán riêng 17/5 cho một trong hai chỉ từ chênh tổng. Raw mẫu đầy đủ cho tất cả các đơn vị thao tác chưa được tái dựng; native chỉ được replay ở lớp E5. Điều này giới hạn khẳng định cơ chế thống kê của từng cổng, không phủ nhận đường lớp→F_I→tầng đã kiểm.

Ca thật tương ứng `dev-16597725c1`, ts-auth-service/cpu, có root giữ tầng 1 và max s=0,966666…, nhưng RR 1→1/3. Kênh log mới s=1 của ts-order-service/ts-order-other-service đổi F_I 0→1; chúng đứng trước root. Counterpart đúng `dev-3defe3d34b` có cùng chữ ký trước bật E1, root vẫn RR=1; các kênh/cạnh khác nhau nên không là matching nhân quả. Nguồn: hai file `cases/E3+E5__E1+E3+E5/`. Không gọi đây là E1 làm mất tín hiệu root: ở ca hại này root không mất max s, đối thủ đổi tính tự sinh.

## E2 tại cấu hình thắng và bằng chứng phản bác

E1→E1+E2 có 7 ca tăng RR, 45 giữ, không ca giảm; kết cục GIÚP ở cả hai lượt. E2→E1+E2 có 8 tăng, 1 giảm, 43 giữ; không suy hai thành phần giúp độc lập. Trên `dev-6c9afc9822`, emailservice/network_delay, E1 không có F_raw, cả 10 ứng viên tầng 3. E2 thêm đơn vị cạnh checkoutservice→emailservice, gán kênh không lan cho bên được gọi: root lên tầng 1 và RR từ 7381/25200 lên 1.

Raw span→mẫu cạnh→cổng đã tái lập ở cả G0/G3, p_len cùng 7,0264e-13, cờ giữ 1, không có trường lệch. Đây là một trường hợp quan hệ cha/con cung cấp mẫu cạnh mà nhánh E1 không giữ, không chỉ đổi khóa xếp hạng. Nguồn: `raw-api-002/dev-6c9afc9822.json`, code `span.mau_canh`, `e2.gan_canh`, `chuoi._chay`, và file case `cases/E1__E1+E2/`.

Không phải thêm E2 sửa mọi ca: `dev-27252dca60` vẫn RR=1/5 ở hai nhánh mới, và các ca sai khác được giữ trong bảng đủ 52. C-d1/C-d3 đều dùng đồ thị, không là đối chứng bỏ quan hệ. Các phép so ở đây đủ mô tả đường tính và lựa chọn dev, chưa đủ tách lợi ích của quan hệ khỏi mọi thay đổi tín hiệu hoặc xác nhận quan hệ gọi biểu diễn nhân quả vật lý.

## Phân loại nguồn vấn đề và phần chưa kiểm

- Trong các ca raw/API đã tái dựng, adapter và cài đặt khớp native; không có sai lệch buộc sửa src hoặc đổi SPEC. Các cửa sổ/coverage trong cặp giữ nguyên; điều đó không chứng minh thu thập đầy đủ mọi sự kiện.
- Việc mất cờ ở G3 là quyết định của phép tính đã khai trên mẫu thật, không tự là bug. Hiệu chuẩn và ổn định trên chuỗi gần hằng vẫn OPEN; C1 chỉ sửa tính tất định theo thứ tự.
- Đổi lớp kênh khi dùng mẫu độc quyền và việc E5 coi kênh ấy không lan là giả định phương pháp có hệ quả đã quan sát. Chưa xác nhận hệ quả đó phản ánh đúng tự xử lý hoặc nguyên nhân vật lý trong mọi ca song song/thiếu span.
- Kết quả ba thế giới: kiểm riêng từng ca RR/Hit1/M5 của đủ 832 bản ghi không có chênh với P (`results/T-047/runs/c1-tong-hop-so-001/world-scoring.json`). Kênh/khóa số vẫn có khác; không dùng khóa P thay non-P. Native không lưu riêng tầng/khóa/inherited_by non-P, nên cơ chế chi tiết ngoài P vẫn OPEN.
- Với các cặp R0→nhiều thành phần, chỉ kết hợp bảng 2×2, điểm dừng luật, chuỗi đủ từng ca của index 15 cặp và các phân tích thành phần trên/E3-E5. Không ép một nguyên nhân riêng cho chênh của cả gói. Muốn tách G3/D1 hoặc thành phần của tương tác cần thí nghiệm được duyệt riêng; không tự đổi thiết kế sau nhìn dev.

Phần đã trả lời là đường tính toán và mức căn cứ cho lựa chọn trong task. Phần chưa trả lời là cơ chế vật lý chung, hiệu quả độc lập, độ hiệu chuẩn cảnh báo và khả năng chuyển sang FlashTicket. Các câu đó ảnh hưởng khóa thiết kế/G3 và các task sau, không được đóng bằng test qua hoặc hai agent cùng nhận định.
