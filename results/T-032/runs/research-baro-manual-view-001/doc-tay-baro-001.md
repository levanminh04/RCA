# T-032 — Đọc tay chuỗi BARO

Đây là phần đọc của người làm, chưa là báo cáo tổng hợp hoặc nghiệm thu T-032. Đã đọc bảng scalar của root, các caller nguồn và cột root giữ/bỏ trên đủ 52 ca. Đã đọc riêng mười ca có M5, gồm 3 RE2-TT và 7 Nezha-OB, cùng các đối chứng cùng ô được khóa từ trước khi diễn giải. Chưa đọc xong mọi lớp đối chứng; không chứng nhận toàn bộ nhóm hoặc cơ chế vật lý.

Nguồn số là `results/T-032/runs/research-baro-006/closed/baro-saved-chains.json` (gọi là **S**) và bản chiếu `results/T-032/runs/research-baro-manual-view-001/reading-view.json` (gọi là **V**). Hash S và V khớp manifest và receipt hai đầu trước khi đọc. `manual-review-001.json` trong thư mục bản chiếu giữ giá trị nguyên bản, con trỏ từng ca/caller/đối chứng, trạng thái đã đọc và phần chưa đọc. S `/counts` ghi 52 ca, 30 RE2, 22 Nezha, 10 ca M5 union, 33 yêu cầu cặp và 501 liên kết lớp đối chứng. Đây là số đơn vị khác nhau; không cộng số k hoặc số liên kết thành số ca/nguyên nhân.

## Bước tính đã kiểm và phạm vi kết luận

Đã đọc code có hash khớp S `/runtime_code_pins`: `src/p3/adapters/baro.py`, `src/p3/cua_so.py`, `src/p3/ban_ghi.py`, checkout phương pháp `D:/RCA-ext/src/RCAEval/RCAEval/e2e/baro.py` và `RCAEval/io/time_series.py`. Pin sklearn runtime do trình đọc EC2 kiểm; lượt này không đọc trực tiếp file sklearn trên EC2, không suy một ngưỡng gần zero. Mẫu số hiệu dụng và trạng thái fallback lấy đúng trung gian đã ghi.

Chuỗi thật là: cắt F → bỏ latency-50/đổi tên latency-90, forward fill rồi điền zero → chia N/A → bỏ cột constant riêng mỗi phía → giao cột → fit median/IQR trên N → transform A → max robust-z có dấu trên A → max khóa metric của mỗi entity → hạng và nhóm hòa. Native BARO và lần dựng khóa sẵn có của adapter đều đã khớp đóng băng trước khi dùng chuỗi. Trình đọc saved-chain không fit hay chạy lại phương pháp.

Điểm ở đây là mức lệch chuẩn hóa, không có ngưỡng kích hoạt native để gọi một service “tự bất thường”. BARO không nhận log, trace, ancestor hay cạnh làm đầu vào chấm. Caller/root của T-028 là ngữ cảnh phân tích sau tính toán. Vì vậy quan sát một caller có điểm cao xác định được metric của chính caller tạo khóa; chưa biết nguồn vật lý của metric ấy.

Ở bảng root cả 52 ca, entity root vẫn có khóa và hạng. Điều này bác bỏ giải thích “toàn entity root bị loại khỏi ứng viên” trên các lượt BARO này. Nó không bác bỏ mất một cột, thông tin chưa từng được ghi, hoặc sai khác cách biểu diễn tín hiệu. Mọi ca M5 dưới đây có chênh điểm strict giữa caller đang đứng trên và root; khóa hòa không tạo chênh lệch của các cặp đó. Mẫu số hiệu dụng của các metric thắng được dẫn dưới đây bằng IQR thật, không qua fallback. Đây là kết quả theo ca, không là quy luật về mọi metric hoặc mọi phương pháp.

## RE2-TT: caller trên root không chỉ do latency

**dev-a5cabe5fa7**, S `/cases/19`: root travel vẫn có các metric và khóa 17,285714 từ mem, hạng 16. Median N 281,575424; Q25/Q75 281,53856/281,595904; IQR 0,057344; tử số tại max 0,991232. Food đứng hạng 9 với khóa 45,459443 từ latency: median 0,08, IQR 0,009513974823166335, tử số 0,4325. Seat đứng hạng 11 với latency 25,120567. Các caller còn lại được giữ đầy đủ ở V `/cases/19/caller_root`; không phải tất cả caller đều trên root. Winner top-1 thực tế là order-other latency 211,276692 (S `/cases/19/entity_ranking/0` và `/cases/19/metric_chains/269`), khác hai caller vừa nêu. M5 cho biết có caller trên root, không đồng nghĩa caller ấy quyết định top-1 sai.

Đối chứng cùng ô travel|loss **dev-7f1b6b071d**, S `/cases/15`, đã khóa trong V `/locked_controls/8`, `/locked_controls/11`: root mem 103,25, hạng 1, tử số 10,149888/IQR 0,098304. Food vẫn có latency 42,727881, preserve latency 92 và seat latency 72,266209, nhưng dưới root. Cùng công thức max và caller latency cao có cả trong ca đúng; không đủ quy chúng thành nguyên nhân chung của ca sai. Có khác biệt tử số và mẫu số root giữa hai ca. Metadata coverage khác 68 trường theo nguồn; đây không là cặp can thiệp chỉ một yếu tố. Lượt này chưa phân tách đóng góp nhân quả của numerator, denominator, mất cột error hoặc đầu vào khác.

**dev-a915aa2424**, S `/cases/20`: root travel CPU 4,812832, hạng 29, median 3,0080788737138366, IQR 1,2474608635322486, tử số 6,003819712851552. Preserve latency 182, seat mem 161,619048, food latency 19,213056, travel2 latency 11,113348, admin-travel mem 8,1 và preserve-other CPU 7,424408 đều trên root. Winner top-1 là auth mem 189 (S `/cases/20/entity_ranking/0`, `/cases/20/metric_chains/76`), không phải quan hệ caller đến travel. Đây là phản ví dụ cho việc gán mọi ưu thế caller M5 thành “chấm thời gian chờ”: mem và CPU cũng tạo khóa cao hơn. Chưa biết vì sao các tín hiệu này thay đổi trong hệ thống. Đối chứng travel|loss ở S `/cases/15` được khóa tại V `/locked_controls/9`, `/locked_controls/12`; root thắng bằng mem, khác metric thắng ở ca sai. Nguồn ghi 100 khác biệt metadata, không phải giữ mọi đầu vào còn lại cố định.

**dev-f36d0647d5**, S `/cases/26`: root order còn metric, diskio thắng với 77,074966, hạng 4; IQR 27096,849777858217 và tử số 2088488,7672441273. Travel2 mem 270, security latency 151,238095 và seat latency 90,330251 đứng trên. Travel2 là winner top-1 thật. Cả độ lệch tài nguyên và latency cùng tham gia vào so sánh; không có bằng chứng chờ từ phép max này. Đối chứng cùng order|loss **dev-20acb4402d** và **dev-260d332c8d** ở S `/cases/6`, `/cases/7`, V `/locked_controls/10/control_classes/0`, `/locked_controls/10/control_classes/1`: root thắng bằng latency 4209,481569 và 5307,411003, hạng 1. IQR lần lượt 0,0006181318681318763 và 0,0007022727272727285; tử số 2,602014705882354 và 3,7272499999999993. Caller được quan sát của hai ca đúng không có cùng tập quan hệ như ca sai. Nguồn ghi khác coverage 220/216 trường. Kết luận đủ hẹp: metric và tập quan sát khác làm điều kiện so sánh khác; chưa nhận đây là tác động riêng của kiểu lỗi, IQR hay cạnh.

## Nezha-OB: tách khóa caller, khóa root và winner toàn bộ

Metric Nezha đã vào adapter dưới dạng 5 mẫu N + 5 mẫu A theo thứ tự. Marker ở S/V không được dùng như thời điểm span hoặc mẫu đồng thời. Cả bảy ca M5 dưới đây giữ root trong ứng viên; không nhận thời gian chờ từ tên latency.

| Ca; con trỏ S | Root: metric thắng; điểm; hạng | Caller strict trên root; metric thắng; điểm | Phần đã phân xử và giới hạn |
|---|---|---|---|
| dev-27252dca60; `/cases/32` | productcatalog workload; 3,2251980228734562; 7 | recommendation client latency P90; 26,303030303029693 | Max metric riêng recommendation tạo ưu thế caller. Winner cả bảng là cart server latency P95 28,482288371201896, không phải caller này. Cột successrate và memory của root bị lọc; chưa biết giữ chúng có đổi endpoint. Không có đối chứng đúng cùng ô productcatalog|exception; các lớp khác ô vẫn giữ. |
| dev-5467884de4; `/cases/38` | recommendation server latency P99; 64,09803921568745; 4 | frontend client latency P95; 177,3082078349991 | Frontend là winner top-1. Cùng ô có ca đạt top-5 nhưng không có ca đúng top-1; không thay endpoint khi làm đối chứng. Wait và nguồn vật lý latency OPEN. |
| dev-55f99f3e0a; `/cases/39` | checkout client latency P99; 14,159663865546555; 4 | frontend FrontLatencyP99 và PodServerLatencyP99 cùng max; 156,82638888889505 | Hai metric frontend bằng điểm đúng giá trị, nhưng điểm frontend strict trên root. Winner toàn bộ là productcatalog client latency P99 492,499999999945. Đối chứng cùng ô dev-b0f8b2e3ac có root server latency P99 194,49999999999764, hạng 1, frontend 23,800201517306785. Công thức chung không ép frontend thắng. |
| dev-63c30faf34; `/cases/42` | recommendation NetworkReceiveBytes; 8,861347416669172; 7 | frontend client latency P95; 73,3287144629281 | Root latency không phải metric thắng. Đối chứng cùng ô đúng k=5 là dev-5467884de4, root 64,09803921568745 hạng 4; nó vẫn có M5 và sai k=1. Cặp này phân biệt endpoint k=5, không phải cặp “không caller ưu thế”. Winner ca sai là productcatalog server latency P90 215,59456638559064. |
| dev-6c9afc9822; `/cases/43` | email client latency P99; 98,20440881763528; 2 | checkout server latency P99; 150,00000000000153 | Checkout là winner. Frontend 27,750417827298705 dưới root. Không có đối chứng đúng k=1 cùng email|network_delay; giữ lớp cùng dataset/F/adapter khác ô, chưa quy lỗi cho latency ở caller. |
| dev-8ecd9880ed; `/cases/47` | checkout client latency P95; 4,219827586206892; 8 | frontend client latency P95; 7,138845927958274 | Frontend chỉ hạng 7. Winner ad client latency P99 523,3333333333328. Đối chứng cùng checkout|return đúng k=5 dev-3b92690644 có root client latency P99 40,00000000000073 hạng 3, frontend FrontLatencyP50 26,095852534562376 hạng 4. Ca đối chứng vẫn sai k=1; không gọi là đúng mọi k. |
| dev-9fd793feb7; `/cases/50` | shipping client latency P90; 50,38461538461538; 4 | checkout client latency P95; 99,5429975429982 | Checkout hạng 3, winner productcatalog client latency P99 247,49999999999292. Không có đối chứng đúng k=1 cùng shipping|cpu_consumed; CPU-contention là lớp khác, không thay nhãn để ghép. |

Chuỗi scalar nguyên bản của từng cặp nằm trong V `/cases/i/caller_root/j`, gồm median, quantiles, IQR, mẫu số hiệu dụng, vị trí max, giá trị input và source fit/transform/score. Không làm tròn hoặc lấy điểm từ bảng Markdown để tính tiếp. Bảng trên chỉ để đọc; JSON là nguồn số.

Đối chứng dev-b0f8b2e3ac được khóa tại V `/locked_controls/25/control_classes/0`; metadata chỉ ghi khác metric_cols_after_preprocess 132/136. Điều này không xác nhận giá trị hai input giống nhau: metadata ưu tiên được khóa không chứa toàn bộ giá trị metric. Root thắng bằng metric khác và cả input scalar khác. Tương tự, dev-63c30faf34 so dev-5467884de4 tại `/locked_controls/31/control_classes/0` chỉ ghi khác số cột 137/136; không suy các giá trị khác đều giữ cố định. Cặp dev-8ecd9880ed so dev-3b92690644 tại `/locked_controls/32/control_classes/0` ghi thêm khác coverage email. Các khác biệt giữ nguyên; không dùng chúng làm khoảng cách chọn cặp.

## Bước lọc làm mất cột có thật, nhưng chưa chứng minh gây sai

Code bỏ constant riêng N/A rồi lấy giao. S/V `/cases/i/column_stages` chỉ đúng cột ra khỏi mỗi bước. Ví dụ travel|loss dev-a915: error còn sau N nhưng bị bỏ A và mất khỏi giao; dev-7f1b6b071d đúng có error bị bỏ N dù còn A và cũng mất khỏi giao. Cột này không tham gia fit/score của cả hai, nhưng root đều còn. Không thể từ “error bị bỏ” kết luận cột ấy gây sai ở một ca và không gây sai ở ca kia.

Trong Nezha, PodSuccessRate của root bị bỏ riêng N/A ở những ca đã đọc, kể cả ca sai dev-27252dca60 và ca đúng dev-b0f8b2e3ac. Cột frontend FrontSuccessRate trong dev-1ac905bc95/dev-5ada15752d bị bỏ N rồi bị giao loại khỏi A. Đây là mất tín hiệu tại tiền xử lý tính toán có thể định vị; chưa có phép giữ cột để biết hạng đáp ứng ra sao, cũng chưa kiểm toàn giá trị thô để gọi lỗi dataset. Một cột constant trong một phía có thể mang thông tin thay đổi giữa hai phía; thay quy tắc lọc/scale cần thiết kế và duyệt riêng, không tự khôi phục trong BARO.

Các ca M0 ngoài caller/root cũng có khóa root thấp hơn một entity khác dù không có caller được nguồn đánh dấu. Ví dụ route|mem dev-14372e1209: root mem 3907,4188034195304 hạng 2 dưới consign-price latency 7065,624933967951; hai đối chứng cùng ô dev-16870e660c và dev-4f8a844308 vẫn dùng root mem, hạng 1. Auth không có caller được giải quyết trong nguồn của các ca ở đây; không đổi “không có quan hệ quan sát” thành “không có phụ thuộc thật”. Những ca M0 vẫn cần phân xử nguyên nhân của numerator/scale hoặc thiếu quan sát; cờ M0 không là kết luận không có cơ chế.

## Câu nghiên cứu đã trả lời tới đâu

**FACT — tính toán:** có thể chỉ chính xác metric, mẫu N, median/IQR/mẫu số và max A nào tạo khóa root/caller. Trong các ca M5 được đọc, root vẫn còn; caller thắng nhờ khóa own-metric lớn hơn, có cả latency và tài nguyên. Không có phép truyền điểm theo cạnh hay ưu tiên tên caller trong code BARO. Đây là bước quyết định thứ tự đã xác nhận, chưa là chứng minh công thức đánh giá sai một tín hiệu vật lý cụ thể.

**FACT — đối chứng:** cùng công thức, caller latency cao và lọc constant có cả trong ca đúng. Các cặp đã khóa khác giá trị đầu vào, đôi khi khác metric thắng/coverage/tập caller. Vì vậy chưa gán tính chất chung của BARO thành nguyên nhân riêng của mọi ca sai; cũng chưa quy IQR nhỏ là nguyên nhân duy nhất. Những đại lượng numerator và denominator đều phải giữ trong chuỗi.

**OPEN — vật lý:** caller chờ đồng bộ, xử lý tại caller, tài nguyên chung, thiếu span và bất đồng bộ chưa phân xử. Trace capability hiện chỉ đo một phần; phần này chưa đọc trực tiếp geometry/clock/semantics vào từng cặp metric. Không đặt nhãn lan, tỷ lệ lan, self-time hoặc await. Tính toán BARO cũng chưa cho biết quan hệ sẽ sửa được lỗi nào hay có tăng chất lượng RCA.

**CANDIDATE — P5/P6:** quan hệ gọi có thể bổ sung ngữ cảnh để so tín hiệu ở caller với thành phần downstream, thay vì diễn giải độc lập một scalar. Nếu phát triển ứng viên, cần nêu service/component là nút, cạnh gọi/nhắn tin/phụ thuộc dữ liệu có provenance, metric ở nút và phép tính thật sử dụng cạnh. Trước khi chọn cơ chế tách chờ phải có wait semantics; đồ thị phân tích T-028 hiện không là bằng chứng sẵn có về chờ. Phương án khác là bảo toàn cột qua hai phía, sửa quan sát hoặc chẩn đoán scale/max. Chưa chạy, chưa chọn hoặc chứng minh lợi ích của các phương án này.

## Phần đọc còn lại và kiểm tiếp cụ thể

`manual-review-001.json` giữ từng 501 link với trạng thái. Các cặp cùng ô bên trên đã đối chiếu scalar và những khác biệt metadata nguồn hiển thị; chưa đọc hết full preferred metadata từng link và chưa kiểm actual runtime path tương ứng từng cặp. Việc xem root/caller trên 52 ca không thay cho đọc toàn metric matrix, log/trace, hoặc xác nhận cơ chế mọi đơn vị/nhóm đã khóa. Không cập nhật bao-phu-nhom thành hoàn tất từ file này.

1. Đọc tiếp lớp đối chứng đã khóa còn thiếu và actual runtime paths, kể cả lớp khác ô. Giữ F/config/adapter và endpoint k đúng nguồn. Phần này dùng trung gian hiện có, không cần chạy BARO; root xếp tiếp trong ngân sách đã duyệt. Mục đích là xem đường lọc, metric thắng hoặc fallback nào phân biệt ca sai/đúng. Nếu không khác biệt có tính phân xử, giữ kết luận ở mức scalar.
2. Với cột bị lọc nhưng có thay đổi liên cửa sổ, cần đọc giá trị prepared/N/A đã hash trên EC2 và thiết kế đối chiếu chỉ đổi quyết định giữ cột, giữ nguyên F/input khác/mapping và khai quy tắc scale cho nền constant. Dự đoán cạnh tranh: thứ hạng nhạy với giữ cột hỗ trợ hạn chế lọc; thứ hạng không đổi không chứng minh mọi tín hiệu ấy vô ích. Chưa có quyền can thiệp BARO; phải trình phạm vi/chi phí đo trước chạy, không lấy thông số mới để làm đẹp Hit.
3. Với ca caller ưu thế latency, nối max-row metric với trace đúng semantics/clock nếu có, không coi các mẫu Nezha ordinal là đồng thời. Giải thích chờ cần parent/request resolution, đồng bộ/await và coverage; xử lý caller/tải chung cần kênh CPU/resource phù hợp cùng khoảng. Thiếu instrumentation thì phương pháp đọc hiện có không phân xử; đề nghị thu trên FlashTicket, không hứa collector khôi phục metadata chưa ghi.
4. Nếu muốn tách ảnh hưởng max/scale, phải trình contrast giữ dữ liệu/F/cột/mapping và thay đúng thành phần đã khai; prediction phải ghi điểm và metric thắng ngoài Hit. Chưa có số đo chạy/chi phí của contrast mới; file này không cấp quyền hoặc coi phương án là thiết kế đã chọn. Quyết định tổng hợp G2/P5–P6 về cơ chế này còn phụ thuộc các phần đọc/kiểm trên.


## Sổ đọc scalar đủ 52 ca

Bảng chỉ chép scalar đã đọc; chưa biến mỗi dòng thành một cơ chế đã xác nhận. Con trỏ S `/cases/i/root_score_chain` giữ median/IQR/max và con trỏ nguồn. JSON bên cạnh giữ toàn caller, không chọn bỏ caller dưới root.

| i; ca | Dataset; ô nguồn | Root: metric max; score; rank | M5 k nguồn |
|---|---|---|---|
| 0; dev-03d4910932 | RE2-TT; ts-route-service\|socket | ts-route-service_mem; 803.9999999991951; 1..1 | [] |
| 1; dev-12a1a88069 | RE2-TT; ts-order-service\|disk | ts-order-service_diskio; 488346.9281628153; 1..1 | [] |
| 2; dev-14372e1209 | RE2-TT; ts-route-service\|mem | ts-route-service_mem; 3907.4188034195304; 2..2 | [] |
| 3; dev-16597725c1 | RE2-TT; ts-auth-service\|cpu | ts-auth-service_mem; 47.48000000000497; 4..4 | [] |
| 4; dev-16870e660c | RE2-TT; ts-route-service\|mem | ts-route-service_mem; 9738.500000001522; 1..1 | [] |
| 5; dev-1e6d61b5ec | RE2-TT; ts-order-service\|disk | ts-order-service_diskio; 568989.4013078625; 1..1 | [] |
| 6; dev-20acb4402d | RE2-TT; ts-order-service\|loss | ts-order-service_latency; 4209.481568627397; 1..1 | [] |
| 7; dev-260d332c8d | RE2-TT; ts-order-service\|loss | ts-order-service_latency; 5307.411003236236; 1..1 | [] |
| 8; dev-3ae0a6c15a | RE2-TT; ts-train-service\|cpu | ts-train-service_latency; 1882.7374317907058; 1..1 | [] |
| 9; dev-3defe3d34b | RE2-TT; ts-auth-service\|cpu | ts-auth-service_mem; 382.333333332954; 1..1 | [] |
| 10; dev-4e68956051 | RE2-TT; ts-train-service\|delay | ts-train-service_latency; 8131.705430224151; 1..1 | [] |
| 11; dev-4f8a844308 | RE2-TT; ts-route-service\|mem | ts-route-service_mem; 38037.66666680458; 1..1 | [] |
| 12; dev-57546fd87b | RE2-TT; ts-auth-service\|delay | ts-auth-service_mem; 3.105726872246616; 41..41 | [] |
| 13; dev-59f696a169 | RE2-TT; ts-auth-service\|cpu | ts-auth-service_mem; 102.54545454548047; 2..2 | [] |
| 14; dev-746fd74313 | RE2-TT; ts-auth-service\|delay | ts-auth-service_latency; 30.68613180352903; 3..3 | [] |
| 15; dev-7f1b6b071d | RE2-TT; ts-travel-service\|loss | ts-travel-service_mem; 103.25000000001648; 1..1 | [] |
| 16; dev-8017c6dc70 | RE2-TT; ts-order-service\|disk | ts-order-service_diskio; 520871.5182156458; 1..1 | [] |
| 17; dev-98bc73c499 | RE2-TT; ts-train-service\|cpu | ts-train-service_latency; 609.5732880456266; 1..1 | [] |
| 18; dev-a505ab3f65 | RE2-TT; ts-train-service\|delay | ts-train-service_latency; 25035.619515801132; 1..1 | [] |
| 19; dev-a5cabe5fa7 | RE2-TT; ts-travel-service\|loss | ts-travel-service_mem; 17.28571428571457; 16..16 | [1, 5] |
| 20; dev-a915aa2424 | RE2-TT; ts-travel-service\|loss | ts-travel-service_cpu; 4.81283212032114; 29..29 | [1, 5] |
| 21; dev-b8bd0abf60 | RE2-TT; ts-route-service\|socket | ts-route-service_latency; 987.4527448772192; 1..1 | [] |
| 22; dev-ba831dbeb8 | RE2-TT; ts-train-service\|cpu | ts-train-service_latency; 464.46036799668826; 1..1 | [] |
| 23; dev-bcbd4f46ae | RE2-TT; ts-route-service\|socket | ts-route-service_mem; 101.4074074074104; 1..1 | [] |
| 24; dev-db293894ab | RE2-TT; ts-travel-service\|disk | ts-travel-service_diskio; 514304.58647720725; 1..1 | [] |
| 25; dev-de89e2f9e9 | RE2-TT; ts-travel-service\|disk | ts-travel-service_diskio; 596241.3974909716; 1..1 | [] |
| 26; dev-f36d0647d5 | RE2-TT; ts-order-service\|loss | ts-order-service_diskio; 77.07496570138956; 4..4 | [1] |
| 27; dev-f81f88234e | RE2-TT; ts-auth-service\|delay | ts-auth-service_latency; 4.887212977968917; 11..11 | [] |
| 28; dev-f9a8e05ed7 | RE2-TT; ts-travel-service\|disk | ts-travel-service_diskio; 640830.4840839492; 1..1 | [] |
| 29; dev-fbc45b0c67 | RE2-TT; ts-train-service\|delay | ts-train-service_latency; 18498.855870791547; 1..1 | [] |
| 30; dev-14701a3bbb | Nezha-OB; shippingservice\|cpu_contention | shippingservice_CpuUsageRate-pct; 341.725758793045; 1..1 | [] |
| 31; dev-1ac905bc95 | Nezha-OB; frontend\|return | frontend_NetworkTransmitBytes; 1.1889938916035074; 10..10 | [] |
| 32; dev-27252dca60 | Nezha-OB; productcatalogservice\|exception | productcatalogservice_PodWorkload-Ops; 3.2251980228734562; 7..7 | [1, 5] |
| 33; dev-2bfc97b01e | Nezha-OB; checkoutservice\|network_delay | checkoutservice_PodServerLatencyP99-s; 94.00000000000095; 2..2 | [] |
| 34; dev-396c8dbf7d | Nezha-OB; emailservice\|cpu_consumed | emailservice_CpuUsageRate-pct; 688.4850650019675; 1..1 | [] |
| 35; dev-3b92690644 | Nezha-OB; checkoutservice\|return | checkoutservice_PodClientLatencyP99-s; 40.00000000000073; 3..3 | [] |
| 36; dev-3e27669440 | Nezha-OB; adservice\|cpu_contention | adservice_MemoryUsage-Mi; 3477.777777777778; 1..1 | [] |
| 37; dev-515c5f2190 | Nezha-OB; recommendationservice\|cpu_consumed | recommendationservice_PodServerLatencyP90-s; 982.4790850365321; 1..1 | [] |
| 38; dev-5467884de4 | Nezha-OB; recommendationservice\|network_delay | recommendationservice_PodServerLatencyP99-s; 64.09803921568745; 4..4 | [1] |
| 39; dev-55f99f3e0a | Nezha-OB; checkoutservice\|exception | checkoutservice_PodClientLatencyP99-s; 14.159663865546555; 4..4 | [1] |
| 40; dev-5ada15752d | Nezha-OB; frontend\|return | frontend_SyscallRead; 3.933649289099526; 8..8 | [] |
| 41; dev-607751ac0a | Nezha-OB; checkoutservice\|network_delay | checkoutservice_NetworkReceiveBytes; 5.014259252537352; 8..8 | [] |
| 42; dev-63c30faf34 | Nezha-OB; recommendationservice\|network_delay | recommendationservice_NetworkReceiveBytes; 8.861347416669172; 7..7 | [1, 5] |
| 43; dev-6c9afc9822 | Nezha-OB; emailservice\|network_delay | emailservice_PodClientLatencyP99-s; 98.20440881763528; 2..2 | [1] |
| 44; dev-70629373f9 | Nezha-OB; paymentservice\|cpu_contention | paymentservice_NetworkReceiveBytes; 735.5159429383294; 1..1 | [] |
| 45; dev-7b7c973198 | Nezha-OB; emailservice\|network_delay | emailservice_PodClientLatencyP90-s; 10.358974358974356; 4..4 | [] |
| 46; dev-7d3c2fe6d1 | Nezha-OB; shippingservice\|cpu_contention | shippingservice_PodServerLatencyP95-s; 6885.264705882348; 1..1 | [] |
| 47; dev-8ecd9880ed | Nezha-OB; checkoutservice\|return | checkoutservice_PodClientLatencyP95-s; 4.219827586206892; 8..8 | [1, 5] |
| 48; dev-95e164235f | Nezha-OB; paymentservice\|cpu_contention | paymentservice_CpuUsage-m; 1404.1746026427618; 1..1 | [] |
| 49; dev-9b9397a4dc | Nezha-OB; recommendationservice\|cpu_consumed | recommendationservice_PodServerLatencyP90-s; 115.34463585195282; 2..2 | [] |
| 50; dev-9fd793feb7 | Nezha-OB; shippingservice\|cpu_consumed | shippingservice_PodClientLatencyP90-s; 50.38461538461538; 4..4 | [1] |
| 51; dev-b0f8b2e3ac | Nezha-OB; checkoutservice\|exception | checkoutservice_PodServerLatencyP99-s; 194.49999999999764; 1..1 | [] |
