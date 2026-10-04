# BARO — RobustScorer, kèm biến thể N-Sigma RCA

Ngày 04/10/2026. Hồ sơ P1 phục vụ RQ1 và nhận xét đầu tiên của cô. **FACT** là điều đã đối chiếu code hoặc phép kiểm; **OPEN** là lựa chọn G1. Revision/hash đầy đủ ở `manifest.json`. BR = `D:/RCA-ext/src/baro`; RE = `D:/RCA-ext/src/RCAEval`. Không dùng hồ sơ này để chốt cửa sổ P3.

## 1. Bài toán và đầu vào

BARO trong bài là chuỗi phát hiện BOCPD → xác định điểm tách → RobustScorer xếp metric → gộp lên service. `RE:RCAEval/e2e/baro.py:19–60` chỉ cài **phần xếp hạng**. Nó không gọi detector.

Scorer nhận bảng các metric cùng trục `time`. Có hai cách tách: timestamp `inject_time` với `time<inject_time` là nền; hoặc `anomalies[0]` làm **số dòng** cho `head/tail`. Cách thứ nhất là chế độ (a), biết mốc sự cố. Cách thứ hai không tự bảo đảm là chế độ (b): nguồn điểm tách và nguồn cửa sổ cũng phải độc lập nhãn. Nhãn service/loại lỗi không cần cho scorer.

Một metric là một ứng viên. CPU/memory/latency/error/workload/diskio đều có thể được chấm khi không bật bộ chọn riêng. Chỉ dùng metric, không cần trace/log/graph. Đây là BARO đơn nguồn; `mmbaro` trong RCAEval là biến thể đa nguồn ngoài phạm vi hồ sơ này.

## 2. Từng bước và công thức chấm điểm

Gọi \(N_j\) là mẫu nền, \(A_j\) là mẫu sau điểm tách của metric \(j\).

1. Tách trước/sau mốc. Hàm không tự sắp thời gian.
2. Tiền xử lý từng nửa riêng. Bỏ cột thời gian, bỏ cột hằng, đổi cột `_mem` từ byte sang MB trong nhánh thông thường. Nếu metric hằng ở một nửa, nó có thể mất dù nửa còn lại có biến động lớn.
3. Lấy giao tên cột của hai nửa, giữ thứ tự cột nền.
4. Học median (trung vị) và IQR (khoảng tứ phân vị) trên nền:

\[
m_j=Q_{0.5}(N_j),\qquad d_j=Q_{0.75}(N_j)-Q_{0.25}(N_j).
\]

Quantile của DataFrame dùng nội suy mặc định NumPy/sklearn. Nếu \(d_j<10\epsilon\), sklearn đặt scale hiệu dụng \(\tilde d_j=1\). Vì vậy “scale=1” không tự chứng minh IQR=0; IQR thật có thể bằng 1 hoặc rất nhỏ. Khi IQR=0, điểm giữ đơn vị của metric sau tiền xử lý, có thể cạnh tranh không công bằng với điểm đã chuẩn hóa ở metric khác.

5. Code DataFrame tính:

\[
z_{j,t}=(x_{j,t}-m_j)/\tilde d_j,\qquad s_j=\max_{t\in A_j}z_{j,t}.
\]

Đây là **cực đại có dấu**, không phải trị tuyệt đối. Hậu kỳ giảm hoàn toàn có thể cho điểm âm. Hàm trả thứ hạng, không trả p-value hay quyết định bác bỏ “không có nguyên nhân”. Vì vậy hai cửa sổ bình thường vẫn ra danh sách; danh sách ấy không chứng minh có sự cố.

6. Sắp metric giảm dần theo điểm. Stable sort (sắp ổn định) giữ thứ tự cột khi hòa. Bỏ trùng service theo lần xuất hiện đầu, tương đương dùng metric có điểm cao nhất của mỗi service. Không cộng hay lấy trung bình các metric.

Nguồn: BR `baro/root_cause_analysis.py:285–323`; RE `RCAEval/e2e/baro.py:22–60`; sklearn ghim `_data.py:1587–1595,1640–1661`; BR `baro/utility.py:191–199`.

### Biến thể N-Sigma RCA

Pipeline giống DataFrame RobustScorer trong các cấu hình đã kiểm, nhưng học \(\mu_j\) và \(\sigma_j=\sqrt{\operatorname{var}_{ddof=0}(N_j)}\) bằng StandardScaler:

\[
s_j^{N\text{-}Sigma}=\max_{t\in A_j}(x_{j,t}-\mu_j)/\tilde\sigma_j.
\]

Scale hằng được đặt 1. StandardScaler còn có xử lý phương sai gần hằng theo sai số số học; không được thay mọi trường hợp bằng điều kiện `std==0`. Code BR `root_cause_analysis.py:147–185`; RE `e2e/__init__.py:109–148`; sklearn `_data.py:820–824,1030–1038`. Nó cũng dùng **max có dấu**, không có ngưỡng \(k\). N-Sigma phát hiện là hàm khác, hai phía, `ddof=1`, cập nhật nền theo toàn quá khứ; xem hồ sơ riêng.

## 3. Đồ thị dùng ở đâu

Không ở vai trò nào trong sáu vai trò K1 §3: không topology, ngữ cảnh feature, đối tượng bất thường, lan truyền, giả định nhân quả hay xếp hạng trên graph. Scorer mỗi metric độc lập. Việc gộp tên metric lên service chỉ là ánh xạ tên, không phải cạnh phụ thuộc. Covariance của BOCPD cũng không là đồ thị nhân quả.

## 4. Tham số mặc định, có file:dòng

| Tham số | Mặc định và ý nghĩa | Nguồn |
|---|---|---|
| `inject_time`, `anomalies` | `None`; phải cung cấp một cách tách hợp lệ; chỉ đọc điểm đầu của anomalies | BR `root_cause_analysis.py:235–237,285–291`; RE `baro.py:19–26` |
| `dataset` | `None`; hành vi BR/RE khác nhau, bảng dưới | BR `root_cause_analysis.py:96–118`; RE `io/time_series.py:99–115` |
| `dk_select_useful` | False khi không truyền; khi True loại extra/near constant và lọc CPU/mem/lat50 | BR `root_cause_analysis.py:113–118`; RE `time_series.py:107–111` |
| RobustScaler | center/scale True, quantile (25,75), `unit_variance=False` | sklearn `_data.py:1587–1595`; lời gọi BR:312/RE:49 |
| StandardScaler | center/std True, variance `ddof=0` | sklearn `_data.py:855–859,1030–1038`; RE `e2e/__init__.py:137` |
| `--length` của runner | 20; mỗi phía `L*60//2` **dòng** | RE `main.py:122,276–279,314–315` |

Ở 1 Hz, L10 là 300+300 dòng. Ở cadence khác, đây không còn là tổng 10 phút. L không là tham số của chính scorer; scorer dùng toàn hai nửa đã được truyền. P3 vẫn OPEN theo Q-54.

## 5. Code khác bài và hai code khác nhau

Bài [BARO §3.4, Algorithm 1](https://arxiv.org/html/2405.09330v1) viết \(\max_t|x_{j,t}-m_j|/IQR_j\). Hai DataFrame implementation dùng max có dấu. Phản ví dụ giảm và điểm từng metric được lưu ở `kiem-tra.json`, không coi là lỗi do Windows hoặc adapter. Số hiệu quả tập cũ có thể vẫn khớp vì lỗi làm metric tăng; điều đó không chứng minh hai công thức tương đương.

| Khía cạnh | BR | RE | Ảnh hưởng |
|---|---|---|---|
| `dataset=None` | Vẫn bỏ time/hằng, đổi memory | Trả nguyên bảng | RE có thể xếp cả `time` |
| `causalrca-sock-shop` | Pipeline thông thường | Chỉ bỏ time | Tập metric và scale khác |
| Cột thời gian | Bỏ time, Time, timestamp | Bỏ time.1, rồi time hoặc Time; giữ timestamp | Khác candidate nếu tên không chuẩn |
| Nửa rỗng | BR drop_constant có guard | RE dùng iloc[0] | RE có thể lỗi; BR không tự bảo đảm đầu ra có nghĩa |
| Gộp service | `split('_')[0]`, dedup | Thêm bỏ `-db` | Có thể nhập DB vào service chủ |
| Input dict | Có nhánh riêng | Hàm baro chỉ DataFrame | Không xem hai dạng là cùng công thức |

Nguồn BR `utility.py:64–84,191–199`; RE `time_series.py:4–20,99–115`, `main.py:560–572`. Với bảng sạch, `time` chuẩn, dataset thông thường khác None và `dk=False`, hai DataFrame scorer khớp trên hai ca T-013; không mở rộng sang mọi nhánh mặc định.

**Nhánh dict BR:** cần ít nhất 4 mẫu trước và một mẫu sau (`root_cause_analysis.py:213–230`). Median là phần tử chỉ số `n//2`; tứ phân vị là phần tử ở chỉ số nguyên `int(n*.25/.75)`. Điểm là `abs(max(post)-median)/IQR`, đặt IQR = 0 thành 1. Khác nội suy DataFrame và khác `max(abs(...))`. Nó không bỏ hằng/đổi MB như DataFrame. Khi hậu có một giảm lớn và một giá trị bằng median, điểm dict có thể bằng 0. Kiểm này có script độc lập, không chép implementation tác giả.

## 6. Giả định và điều kiện thất bại do tác giả nêu

Tác giả giả định sự cố hiện ở metric rồi ảnh hưởng latency/error; nếu tải/tài nguyên tăng mà hai tín hiệu đó không xấu thì detector có thể coi bình thường (§3.1). Bài dùng một cấu hình triển khai và thu thập cho mỗi hệ, bốn loại lỗi; khả năng khái quát khác chưa được bảo đảm (§5). Với lỗi tương quan, nhóm service bị ảnh hưởng có thể cùng lên hạng (§3.4.3).

Phân tích riêng từ code: metric giảm, IQR = 0, missing, tên cột/mapping và hằng từng nửa có thể làm mất hoặc đổi candidate. Đây là cơ chế đã kiểm bằng ví dụ, không phải tỷ lệ hạn chế P4. Nguyên nhân khác của rank sai gồm thiếu tín hiệu service gốc, symptom ở service khác, baseline có gai, scale gần0 hoặc mapping sai. Không quy một rank cho đồ thị khi scorer không dùng graph.

## 7. Ví dụ tính tay

`vi-du-tinh-tay.md` trình bày một ca dev TT và một ca OB được chọn theo rule SPEC trước rank. Mọi metric có trung gian và điểm official/độc lập trong CSV của run được trỏ bởi `kiem-tra.json`. Nhánh độc lập không gọi helper tác giả. Mốc A tập OB được dùng lại từ `trung-gian/T006-moc-A-reused.json`, không gọi một ca mới là tái lập cả bảng.

## 8. Đường nhãn có thể lọt

Mốc tiêm và cắt cửa sổ là đầu vào hợp lệ chỉ trong chế độ (a). Tên ca/file nhãn không vào hàm T-013; nhãn root chỉ được nối sau khi lưu ranks. Runner RE có SLI suy từ service gốc; BARO/N-Sigma không đọc SLI ở revision này, nhưng vẫn không truyền nó. Biên file đối xứng có thể lộ mốc khi dùng detector. `anomalies[0]` lấy từ list chưa sắp hoặc timestamp epoch còn tạo lỗi đơn vị; không nhầm lỗi đơn vị với bằng chứng RCA.

## 9. Yêu cầu khi chạy dataset khác

Bảng numeric đồng bộ, time chuẩn cùng đơn vị với mốc, thứ tự thời gian đúng; schema metric→service rõ và không suy từ root label. Cần nền/hậu không rỗng và đủ biến động để còn candidate; một con số “tối thiểu đủ tốt” không được code/bài bảo đảm. Đổi cadence phải đổi cách diễn giải số dòng. Đổi preprocessing, mapping, rule hòa hay cửa sổ là lựa chọn G1 (**chờ WHY, xem `de-xuat-tai-lieu-chung.md`**), chưa chốt bởi T-013. Chi phí xếp hạng nhẹ so BOCPD; thời gian T-013 trên máy bận chỉ là tham khảo.
