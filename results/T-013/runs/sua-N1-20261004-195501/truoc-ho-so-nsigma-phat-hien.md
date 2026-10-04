# N-Sigma phát hiện — luật ngưỡng độ lệch chuẩn

Ngày 04/10/2026. Code `D:/RCA-ext/src/baro/baro/anomaly_detection.py:7–35`. Revision/hash trong manifest. Đây là detector, khác N-Sigma RCA.

## 1. Bài toán và đầu vào

Nhận DataFrame có `time` và metric numeric theo thời gian. Hàm chạy mọi cột trừ đúng tên `time`; không tự chọn latency/error. Nó trả timestamp cho mỗi metric vượt ngưỡng. Không nhận mốc tiêm, root service, loại lỗi hay nhãn huấn luyện.

## 2. Từng bước và công thức

Từ chỉ số \(i\ge100\), với từng metric \(j\), dùng toàn mẫu trước \(i\):

\[
\mu_{j,i}=\operatorname{mean}(x_{j,0:i}),\quad
s_{j,i}=\sqrt{\frac{\sum_{u<i}(x_{j,u}-\mu_{j,i})^2}{n_{j,i}-1}},\quad
a_{j,i}=\mathbf1\{|x_{j,i}-\mu_{j,i}|>3s_{j,i}\}.
\]

Mean/std bỏ qua NaN; \(n\) là số mẫu hữu hạn thích hợp của pandas. Đây là sample std (ddof=1), khác population std (ddof=0) ở N-Sigma RCA. Dữ liệu sự cố đã quan sát cũng đi vào nền bước sau; không phải chỉ học từ đoạn normal cố định.

Vòng ngoài theo cột rồi vòng trong theo thời gian. Vì vậy list trả về **không sắp thời gian và không bỏ trùng**. Hợp timestamp tương đương OR cảnh báo của các metric, nhưng `anomalies[0]` không nhất thiết sớm nhất. T-006 runner thêm `sorted(set(...))` tại `scripts/nsigma_phat_hien.py:64`; đó không là hành vi raw của hàm tác giả. Khi nối với scorer còn phải đổi timestamp sang index hợp lệ.

## 3. Đồ thị dùng ở đâu

Không dùng graph ở sáu vai trò K1 §3. Mỗi metric chấm độc lập; nhiều metric trên một service chỉ tạo nhiều alarm, không tạo điểm xếp hạng service. Không cộng số alarm thành rank trong task này.

## 4. Tham số mặc định, có file:dòng

`k=3, startsfrom=100` tại dòng7. `mean()` dòng31, `std()` dòng32 dùng pandas ddof=1. `startsfrom` là **chỉ số đầu được chấm**, còn lịch sử luôn bắt đầu ở dòng0; không phải bỏ100 điểm đầu khỏi nền. Hàm không tự sắp time, điền missing, chuẩn hóa hay làm sạch tên cột. `T<=100` trả rỗng. Khi chọn `startsfrom` nhỏ, cần ít nhất hai giá trị hợp lệ để std hữu hạn; đây là điều kiện số học, chưa đủ bảo đảm nền đại diện normal.

## 5. Code khác bài và khác N-Sigma RCA

Bài [BARO §2.3, §4.5](https://arxiv.org/html/2405.09330v1) dùng N-Sigma làm baseline phát hiện. Bài không cho đủ cấu hình để tái tạo từng list `nsigma.json` tác giả; T-006 có sai lệch ở SS và danh sách alarm khác. Không tự chọn cấu hình sau khi nhìn kết quả để ép khớp.

RCA dùng max z có dấu trên hậu kỳ, không ngưỡng k, nền cố định và ddof=0; detector ở đây dùng abs, k=3, nền mở rộng và ddof=1. Sai lệch giữa hai loại không được quy thành lỗi môi trường.

Cách chấm tái lập T-006 nhận window quanh injection hoặc full snapshot; TP nếu ca có alarm, FP nếu alarm đầu trước injection. P/R/F1 này không là P/R/F1 window của MRP. R = 1 ở những ca đã chạy vì mọi ca có alarm, không phải bảo đảm của detector hoặc mọi dữ liệu; synthetic ngắn/hằng trả rỗng.

## 6. Giả định và điều kiện thất bại do tác giả nêu

BARO §4.5 cho rằng N-Sigma dễ báo sai trên time series phức tạp. Về cơ chế, mean/std quá khứ phải đại diện nền để ngưỡng có ý nghĩa; code không kiểm normality (phân phối chuẩn) hay stationarity (tính ổn định). Đây là phân tích từ công thức, không nhận là tỷ lệ hỏng P4.

Past có gai/sự cố/drift có thể tăng std làm bỏ sót; nền gần hằng khiến ngưỡng nhỏ, tăng alarm. Với std=0, bất kỳ giá trị khác mean đều vượt ngưỡng. NaN hiện tại làm so sánh false, không có nghĩa hệ bình thường. Nhiều metric làm có nhiều cơ hội alarm. Nguyên nhân khác gồm missing, cadence, đơn vị, tên cột và chọn k/startsfrom; phải xét trước khi quy lỗi cho bản thân phương pháp.

## 7. Ví dụ tính tay

Hai ca chọn trước rank có file `*-nsigma-detail.csv`: value, mean quá khứ, sample std, threshold và hit từng điểm cần trình bày; list official bằng list độc lập. Synthetic hai cột có alarm 108 ở cột đầu và alarm 100 ở cột sau chứng minh điểm đầu list khác thời điểm sớm nhất. Xem `vi-du-tinh-tay.md`, `kiem-tra.json`. Chuỗi≤100 điểm và hai đoạn bình thường được kiểm riêng; không gọi list không rỗng là chẩn đoán có nghĩa.

## 8. Đường nhãn có thể lọt

Raw function chỉ dùng quá khứ. Runner có thể cắt quanh injection và min–max toàn window; snapshot đối xứng cũng cho biết điểm giữa. Tuy nhiên không quy mọi thay đổi alarm cho min–max: với affine cố định \(x'=(x-a)/b,b>0\), điều kiện hai phía giữ nguyên vì mean/std cùng biến đổi. Missing, range=0 và sai số số học có thể phá bất biến. BOCPD prior cố định không có cùng bảo đảm này. Khả năng phát hiện tự động và online của pipeline phải kiểm theo nguồn đầu vào, không chỉ chữ ký detector.

## 9. Yêu cầu dataset khác

Time numeric đúng đơn vị, các cột numeric đã kiểm, thứ tự/cadence rõ, lịch sử trước điểm đầu đại diện normal; không cần nhãn để học. Recording chọn độc lập sự cố và có các khoảng âm đủ đo false alarms/h; nhãn onset/injection chỉ dùng sau alarm để chấm. Nếu chỉ có snapshot quanh lỗi thì chỉ báo hiệu quả trên incident-conditioned recording (bản ghi đã được chọn vì có sự cố), không suy ra khả năng giám sát liên tục.

Code tính lại mean/std prefix mỗi điểm: O(dT²), memory ngoài bảng chủ yếu list alarm O(dT). Không mặc định N-Sigma nhẹ ở mọi quy mô. Window/cột/k/startsfrom P3 còn OPEN (**chờ WHY, xem `de-xuat-tai-lieu-chung.md`**); T-013 mô tả mặc định và cơ chế, không thiết kế detector mới.
