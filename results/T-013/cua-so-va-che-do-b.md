# Cửa sổ và điều kiện tự phát hiện

## 1. Cửa sổ làm đổi điều gì

`--length L` trong RE `main.py:276–279,314–315` lấy L×30 **dòng** mỗi phía. Tại 25 ca fse-ob DELAY đã chạy ở T-006, mỗi file có 360 dòng trước mốc và 361 dòng sau mốc, cadence 1 giây. L10 dùng 300+300; L20 dùng cả 360+361, không đủ 20 phút. Vì vậy hai endpoint chỉ khác 60 dòng đầu vào nền và 61 dòng cuối vào hậu. TT trong ví dụ cũ vẫn có thể lấy 600+600 ở L20. Không chọn cửa sổ P3 từ phân tích này.

**Kiểm lại đúng ô DELAY.** `scripts/kiem_cua_so_delay.py` chỉ đọc 25 CSV fse-ob DELAY và 50 JSON rank T-006 đã có; không gọi phương pháp chính thức hoặc chạy benchmark. Tiền xử lý giữ cùng runner: bỏ time.1/latency-50, thay inf bằng NaN, ffill/fill0 trước khi cắt, đổi tên latency-90; hai nửa bỏ hằng riêng, đổi _mem sang MB rồi lấy giao cột. Nhánh độc lập tính mean, variance ddof=0 bằng hai lượt có bù sai số, kiểm gần hằng theo sai số số học, max z có dấu, sort ổn định rồi gộp service như `main.py:560–572`. Nhãn root chỉ dùng ở bước chấm, sau khi tính điểm/rank; không là đối số của hàm số học. Cả 50 endpoint khớp **từng metric rank và service rank** T-006; Avg@5 khớp 0,936 và 0,680, chênh 0,256. Nguồn: `trung-gian/cua-so-delay-summary.json`, `trung-gian/cua-so-delay-ca.csv`; manifest/hash và kiểm từng endpoint tại `results/T-013/runs/sua-R1-20261004-195903/`.

Để tách cơ chế, tính bốn phối hợp: N300–A300 là L10; N360–A300 chỉ thêm nền; N300–A361 chỉ thêm hậu; N360–A361 là L20. Giữ nguyên dữ liệu, xử lý và cách chấm. Thêm nền có thể đổi mean/std **và** cột được giữ; thêm hậu có thể đổi max **và** cột được giữ. Vì thế không gọi toàn tác động của nền là riêng tác động std.

| Phối hợp | Avg@5 trên 25 ca |
|---|---:|
| N300-A300 | 0.936 |
| N360-A300 | 0.712 |
| N300-A361 | 0.936 |
| N360-A361 | 0.680 |

Đi theo thứ tự thêm nền rồi hậu: 0,936→0,712→0,680, tức −0,224 rồi −0,032. Đổi thứ tự: 0,936→0,936→0,680, tức 0 rồi −0,256. Hậu dài hơn một mình không đổi hạng root ở cả 25 ca; nó làm giảm thêm khi nền đã đổi ở một số ca. Đây là tương tác, không nên gán 0,256 duy nhất cho nền hoặc hậu. Nếu chỉ cần phân bổ cộng được và không ưu tiên thứ tự, lấy trung bình hai thứ tự (Shapley): nền −0,240; hậu −0,016. Đó là quy ước hạch toán **tác động số học của biên**, không phải tỷ lệ nguyên nhân vật lý. Lựa chọn phân bổ này **chờ WHY, xem `de-xuat-tai-lieu-chung.md`**; không dùng nó để chọn cửa sổ G1. Với đóng góp ca c(r)=max(0,6−r)/5, E_N=[(cN−c0)+(cNA−cA)]/2 và E_A=[(cA−c0)+(cNA−cN)]/2; tổng mỗi ca bằng cNA−c0. Cột đóng góp và cả hai thứ tự có trong CSV ca.

**Tách toàn ô theo ca.** Có 15/25 ca đổi hạng: 13 tụt, 2 lên; 10 giữ nguyên. Bảng ghi hạng service gốc ở đủ bốn phối hợp; cột Δc là đóng góp Avg@5 của ca ở L20 trừ L10, chưa chia 25. Tổng Δc/25 bằng −0,256.

| Ca DELAY | N300–A300 | N360–A300 | N300–A361 | N360–A361 | Δc | Tập metric đổi |
|---|---:|---:|---:|---:|---:|---|
| cartservice_delay_1 | 1 | 1 | 1 | 1 | 0.0 | không |
| cartservice_delay_2 | 1 | 3 | 1 | 3 | -0.4 | không |
| cartservice_delay_3 | 1 | 3 | 1 | 3 | -0.4 | không |
| cartservice_delay_4 | 1 | 3 | 1 | 3 | -0.4 | có |
| cartservice_delay_5 | 1 | 1 | 1 | 2 | -0.2 | không |
| checkoutservice_delay_1 | 1 | 1 | 1 | 1 | 0.0 | không |
| checkoutservice_delay_2 | 1 | 4 | 1 | 4 | -0.6 | không |
| checkoutservice_delay_3 | 1 | 5 | 1 | 5 | -0.8 | không |
| checkoutservice_delay_4 | 1 | 3 | 1 | 3 | -0.4 | không |
| checkoutservice_delay_5 | 1 | 3 | 1 | 3 | -0.4 | không |
| currencyservice_delay_1 | 2 | 1 | 2 | 1 | 0.2 | có |
| currencyservice_delay_2 | 2 | 4 | 2 | 4 | -0.4 | không |
| currencyservice_delay_3 | 1 | 1 | 1 | 1 | 0.0 | không |
| currencyservice_delay_4 | 1 | 5 | 1 | 6 | -1.0 | không |
| currencyservice_delay_5 | 2 | 5 | 2 | 7 | -0.8 | có |
| paymentservice_delay_1 | 1 | 1 | 1 | 1 | 0.0 | không |
| paymentservice_delay_2 | 1 | 1 | 1 | 1 | 0.0 | không |
| paymentservice_delay_3 | 1 | 1 | 1 | 1 | 0.0 | không |
| paymentservice_delay_4 | 1 | 2 | 1 | 3 | -0.4 | không |
| paymentservice_delay_5 | 1 | 1 | 1 | 1 | 0.0 | không |
| productcatalogservice_delay_1 | 2 | 2 | 2 | 2 | 0.0 | không |
| productcatalogservice_delay_2 | 2 | 1 | 2 | 1 | 0.2 | không |
| productcatalogservice_delay_3 | 1 | 4 | 1 | 4 | -0.6 | có |
| productcatalogservice_delay_4 | 2 | 2 | 2 | 2 | 0.0 | không |
| productcatalogservice_delay_5 | 3 | 3 | 3 | 3 | 0.0 | không |

Tập metric đổi ở bốn ca, đều thêm cột: cartservice_delay_4 thêm main_mem và recommendationservice_mem; currencyservice_delay_1 thêm emailservice_mem; currencyservice_delay_5 thêm recommendationservice_mem; productcatalogservice_delay_3 thêm main_mem. Những cột này bị bỏ hằng ở nửa ngắn nhưng có biến động ở phần thêm. CSV metric ghi cả cột bị bỏ: `candidate=False`, cờ hằng từng nửa và score trống, tránh coi chúng là đã được chấm. 21 ca còn lại giữ tập metric; 25 ca đều giữ metric thắng của root là root_latency ở hai endpoint. Gộp service vẫn có cạnh tranh từ metric cao nhất ở service khác. Nguồn: `trung-gian/cua-so-delay-metric.csv`, `trung-gian/cua-so-delay-variants.csv`, rankings/checks của run.

**Ba ca cụ thể.** Bảng dưới lấy đúng mean/std/max và điểm độc lập từ CSV metric. std là population std có bù sai số; điểm ở đây không dùng nhánh scale gần hằng.

| Ca / metric | mean N300 | std N300 | mean N360 | std N360 | max A300 | max A361 | s L10 | s thêm nền | s thêm hậu | s L20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| currencyservice_delay_4 / currencyservice_latency | 0.0043570167 | 5.0760481e-05 | 0.0064682742 | 0.015644498 | 0.22136946 | 0.22136946 | 4275.2243 | 13.736534 | 4275.2243 | 13.736534 |
| currencyservice_delay_4 / cartservice_latency | 0.0045284804 | 8.1449728e-05 | 0.0045557466 | 9.836828e-05 | 0.0052324245 | 0.054761905 | 8.6426813 | 6.8790253 | 616.74146 | 510.38971 |
| currencyservice_delay_5 / currencyservice_latency | 0.0038908422 | 0.0001079776 | 0.0059237265 | 0.015055971 | 0.22099641 | 0.23436163 | 2010.6539 | 14.284876 | 2134.4315 | 15.172578 |
| currencyservice_delay_5 / emailservice_mem | 42.336433 | 0.00083397171 | 42.336404 | 0.00076417682 | 42.340352 | 42.446848 | 4.6986086 | 5.1664599 | 132.39599 | 144.52688 |
| checkoutservice_delay_3 / checkoutservice_latency | 0.043294083 | 0.0021854533 | 0.11744868 | 0.3843508 | 4.4954545 | 4.4954545 | 2037.1794 | 11.390651 | 2037.1794 | 11.390651 |
| checkoutservice_delay_3 / emailservice_mem | 41.91602 | 0.0020093607 | 41.91513 | 0.0031766421 | 42.340352 | 42.340352 | 211.17759 | 133.85886 | 211.17759 | 133.85886 |

- **currencyservice_delay_4, hạng 1→5→6 khi thêm nền rồi hậu:** std root tăng từ khoảng 0,00005076 lên 0,0156445, còn max root không đổi; điểm root giảm 4275,22→13,7365. Candidate không đổi. Sau đó max cartservice_latency tăng 0,0052324→0,0547619 trong 61 dòng hậu thêm; trên nền N360, điểm cart tăng 6,879→510,390 và đẩy root từ hạng 5 xuống 6. Nếu chỉ thêm hậu trên N300, root vẫn hạng 1 vì điểm root còn rất lớn.

- **currencyservice_delay_5, hạng 2→5→7:** thêm nền làm std root tăng 0,0001080→0,015056, điểm giảm 2010,65→14,2849. Thêm hậu làm max root tăng ít, điểm L20 lên 15,1726; nhưng max emailservice_mem tăng 42,340352→42,446848 MB, điểm trên N360 tăng 5,16646→144,527. Vì vậy root cải thiện điểm mà vẫn tụt thêm hạng do đối thủ tăng mạnh hơn. Ca này còn thêm recommendationservice_mem vào tập candidate; CSV cho phép xét riêng từng metric.

- **checkoutservice_delay_3, hạng 1→5:** max root không đổi ở hậu dài hơn; mean/std nền đổi từ 0,0432941/0,00218545 sang 0,117449/0,384351, điểm root giảm 2037,18→11,3907. emailservice_mem cũng giảm điểm 211,178→133,859 khi đổi nền, nhưng vẫn vượt root và đứng đầu L20. Như vậy memory đứng đầu không nhất thiết do memory tăng điểm hoặc do 61 dòng hậu thêm. Hậu dài hơn không đổi hạng ca này.

Trong 13 ca tụt, 9 ca có metric _mem đứng đầu L20. Pattern này khớp đầu ra cũ, nhưng chỉ mô tả metric thắng. Nó không chứng minh memory là nguồn lỗi. Phân rã trên cho thấy cả scale nền root, max hậu đối thủ, thay candidate và tương tác cạnh tranh có thể quyết định thứ hạng. Nguồn của gai nền hoặc hậu vẫn **chưa kiểm**: có thể tải, warm-up, dao động tự nhiên, ảnh hưởng snapshot hoặc lỗi quan sát; dữ liệu metric và nhãn tiêm riêng không phân xử được nhân quả. Thêm 60 dòng trước tiêm không đồng nghĩa đã thêm dữ liệu sự cố vào nền. Không suy tác dụng đồ thị từ scorer không dùng graph, và không suy cửa sổ tối ưu từ ô này.

Kiểm lặp lại/đảo cột ở 100 phối hợp giữ điểm; 50 endpoint metric/service rank khớp chính xác JSON. Các hòa nếu có giữ thứ tự cột, không đòi thứ hạng tuyệt đối bất biến. Script, trung gian từng metric, cả candidate bị bỏ, checks và thời gian từng ca đã lưu. Phân tích này giải thích **cơ chế số học riêng của ô DELAY**; hai ví dụ TT/OB CPU cũ vẫn chỉ minh họa cơ chế ở các ca khác.

## 2. Ba vấn đề cần tách

| Vấn đề | BOCPD | N-Sigma phát hiện | Hệ quả |
|---|---|---|---|
| Min–max toàn window | Wrapper dùng tương lai; prior cố định nên scale có thể đổi posterior | Raw hàm không normalize; runner T-006 có dùng tương lai. Affine cố định giữ inequality nếu hữu hạn/range>0 | Không gọi thời gian này là cảnh báo online; không quy mọi alarm N-Sigma cho min–max |
| Window quanh injection | `reproduce_bocpd` lấy 300+300 từ mốc nhãn | Runner w300 làm tương tự | Detector không nhận tên `inject_time` vẫn nhận window do nhãn chọn |
| File đối xứng quanh injection | Chạy full snapshot vẫn biết sự cố ở gần giữa | Tương tự | Bỏ file nhãn không làm recording độc lập nhãn |

Biên là **đường thông tin có thể lộ**, không chứng minh code hiện tại cố ý dùng midpoint để đoán lỗi. Dataset đã chọn record vì biết có lỗi cũng thiếu các khoảng âm cần đo giám sát liên tục. Không bỏ các giới hạn này chỉ vì posterior recurrence dùng quá khứ.

## 3. Dataset nào chấm được chế độ (b)

MRP chế độ (b) nghĩa là không đưa mốc tiêm vào phương pháp. Cần xác định thêm đang chấm hồi cứu hay online; đây là OPEN của G1 (**chờ WHY, xem `de-xuat-tai-lieu-chung.md`**).

- **Hồi cứu, không biết mốc:** có thể dùng recording liên tục hoặc block được chọn bằng lịch/quy tắc độc lập lỗi; bảng numeric, time/cadence/missing/mapping rõ. Full-window normalization dùng tương lai phải khai báo; nó không tự là label leak nếu biên độc lập nhãn, nhưng không đo cảnh báo tại thời gian thực.
- **Online:** tại mỗi dự đoán chỉ có lịch sử đến lúc đó và preprocessing/scale/prior xác định không nhờ dữ liệu tương lai hay injection. Raw N-Sigma đáp ứng tính nhân quả của phép tính nếu lịch sử đầu vào hợp lệ; wrapper BOCPD hiện tại normalize toàn input nên chưa đáp ứng. Điều kiện này chưa được triển khai thành detector mới trong T-013.
- **Chấm độ đo:** cần cả thời gian bình thường và sự cố, recording duration để tính false alarms/h, nhãn onset hoặc injection cùng đơn vị và độ phân giải. Nhãn chỉ nối sau dự đoán. Injection-only cho “độ trễ từ lúc tiêm”, không biến thành onset thật.

Snapshot RCAEval/fse hiện tại cắt quanh lỗi chỉ hỗ trợ tái lập hoặc bài toán phát hiện trong recording đã biết có sự cố. Không tự dùng P/R/F1 case-level của tác giả làm P/R/F1 theo window trong MRP. Không nối các snapshot quanh lỗi rồi gọi là dòng giám sát độc lập, vì đường chọn biên vẫn tồn tại.

## 4. Chi phí cũng phụ thuộc cửa sổ

BOCPD lưu R kích thước(T+1)²; số density là T(T+1)/2 và mỗi density còn phụ thuộc dimension. Vì vậy gấp đôi T xấp xỉ gấp bốn phần run-length, không chỉ thêm hai lần số dòng. Memory tổng của dataset chạy tuần tự là peak của một ca, runtime là tổng các ca. N-Sigma raw cũng tính lại mean/std toàn prefix, nên O(dT²).

Các kịch bản30 ca T=600/T=1441 và ngoại suy12/36 giờ từ T-005 là `trung-gian/chi-phi-va-sentinel.json`; ghi rõ chưa kiểm vì cùng quy mô/load chỉ là giả định. T-007: 100 ca OB trên EC2 có dimension/source khác, không dùng để khẳng định laptop nhanh tương tự. Không chốt window từ phép ngoại suy này.
