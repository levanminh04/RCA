# BOCPD — Bayesian Online Change Point Detection (phát hiện điểm đổi Bayes)

Ngày 04/10/2026. BR=`D:/RCA-ext/src/baro`; revision/hash ở manifest. Phân biệt thuật toán Bayes, wrapper batch của BARO và cách chấm artifact. “Khớp tác giả” không tự chứng minh không có lỗi code.

## 1. Bài toán và đầu vào

Nhận \(X\in\mathbb R^{T\times d}\) các metric numeric, ước lượng run length (độ dài đoạn từ điểm đổi gần nhất). `baro/anomaly_detection.py:77–151` chọn tên chứa latency hoặc `_error`, bỏ queue-master/rabbitmq_; nếu không có thì dùng mọi cột trừ đúng tên `time`. Vì vậy tên cột là một phần điều kiện đầu vào. Đầu ra wrapper là **chỉ số dòng**, không phải timestamp dù docstring gọi timestamp.

Trong RCAEval revision được giao, `baro` là ranker; detector này thuộc repo BR. Full BARO nối điểm tách từ detector sang RobustScorer; không dùng nhãn root để học.

## 2. Từng bước và công thức

Wrapper bỏ cột hằng toàn file, forward fill (điền từ giá trị trước), điền thiếu đầu chuỗi thành 0, min–max theo **toàn dữ liệu**, rồi điền thiếu lại. Điều đó dùng tương lai so với mỗi điểm cần phát hiện.

Gọi \(q_{t-1}(r)=P(r_{t-1}=r\mid x_{1:t-1})\), hazard \(H(r)=1/50\) và predictive density \(\pi_t(r)=p(x_t\mid r,x_{1:t-1})\). Code `_bocpd.py:198–223`:

\[
\tilde q_t(r+1)=q_{t-1}(r)\pi_t(r)(1-H(r)),\quad
\tilde q_t(0)=\sum_rq_{t-1}(r)\pi_t(r)H(r),\quad
q_t(r)=\tilde q_t(r)/\sum_u\tilde q_t(u).
\]

Với hazard hằng và tổng mass (khối xác suất trước chuẩn hóa) **dương và hữu hạn**, \(q_t(0)=0.02\). Nếu mật độ bị underflow (nhỏ đến mức máy tính lưu thành 0), tổng có thể bằng 0 dù hữu hạn; phép chia ở `_bocpd.py:220` khi đó cho NaN và không còn suy được đẳng thức trên. Không thể coi riêng hàng 0 này là anomaly score biến thiên. Code quyết định bằng mode của run length.

Likelihood đa biến Student-t dùng \(m=\nu-d+1\), location \(\mu\), scale \(\Sigma=(\kappa+1)S^{-1}/(\kappa m)\):

\[
\pi(x)=\frac{\Gamma((m+d)/2)}{\Gamma(m/2)(m\pi)^{d/2}|\Sigma|^{1/2}}
\left(1+\frac{(x-\mu)^T\Sigma^{-1}(x-\mu)}m\right)^{-(m+d)/2}.
\]

Mỗi giả thuyết run length cập nhật:

\[
\kappa'=\kappa+1,\quad\nu'=\nu+1,\quad
\mu'=(\kappa\mu+x)/(\kappa+1),\quad
S'=\left[S^{-1}+\frac{\kappa}{\kappa+1}(x-\mu)(x-\mu)^T\right]^{-1}.
\]

Thêm lại prior ở vị trí 0 cho đoạn mới. Nguồn `_bocpd.py:86–137`. T-013 cài lại bằng công thức log-density và lưu covariance inverse, không gọi lớp likelihood tác giả trong nhánh độc lập.

Sau đó lấy \(s_i=\arg\max_rq_i(r)\) và điểm đổi nếu \( |s_i-s_{i-1}|>1\) (`utility.py:208–214`). Không phải một ngưỡng trực tiếp trên xác suất. `np.argmax` chọn index nhỏ nhất khi hòa.

**Lỗi biên:** `maxes` dài T+1 nhưng chỉ gán phần 0..T−1; phần tử T còn 0 (`_bocpd.py:196,225`). Mode thật của posterior cuối không được gán. Rule diff có thể tạo điểm T, ngoài dữ liệu 0..T−1. Các điểm hợp lệ trước đó và sentinel phải được phân biệt; T-013 lưu cả đầu ra nguyên code và danh sách bỏ riêng sentinel để kiểm ảnh hưởng, không sửa source.

## 3. Đồ thị dùng ở đâu

Không dựng/dùng graph ở bất kỳ vai trò K1 §3 nào. Covariance mô hình tương quan metric, không cho hướng gọi service hoặc quan hệ nhân quả. Không suy đa biến đồng nghĩa graph-based detector.

## 4. Mặc định, có file:dòng

| Tham số | Giá trị | Nguồn |
|---|---|---|
| Hazard wrapper | \(1/50\), theo **mẫu**, không giây | `anomaly_detection.py:142–145` |
| Prior | \(\nu_0=d+1,\kappa_0=1,\mu_0=0,S_0=I\) | `_bocpd.py:39–84` |
| Predictive ban đầu | \(m_0=2,\Sigma_0=I\) | `_bocpd.py:97–104` |
| Rule điểm đổi | độ nhảy mode >1 | `utility.py:212` |
| warm-up | Không có ngưỡng warm-up khai báo ở wrapper | `anomaly_detection.py:77–151` |

Biến hazard 250 tại `_bocpd.py:184` không được wrapper dùng. Prior phụ thuộc dimension; khác số metric không chỉ khác tốc độ. Không chọn hazard/prior mới bằng nhãn trong task này.

## 5. Code khác bài

[BARO PDF](https://arxiv.org/pdf/2405.09330), trang8 §3.3, mô tả mean cố định0 và covariance inverse-Wishart; code học mean và dùng defaults ở trên. Trang9 Algorithm1 dùng \(s_t\le s_{t-1}\), code dùng abs-diff>1: khác khi plateau, giảm 1 hoặc tăng hơn 1. Sentinel cuối là thêm sai lệch code, không được thuật toán bài yêu cầu.

`reproduce_bocpd` không giống `bocpd`: chỉ lấy latency-50 hoặc `_error`, và cắt 300 điểm trước +300 điểm sau **mốc tiêm** (`reproducibility.py:132–145`). Code chấm ca có bất kỳ điểm đổi thành TP, thêm FP nếu điểm đầu trước 300; một ca có thể vừa TP vừa FP (`:168–181`). Không phải confusion matrix theo window của MRP. Ca rỗng còn gặp truy cập `cps[0]` tại:173. Bài §4.5 mô tả trung bình theo ca; chưa xác minh bản thực nghiệm nào tạo bảng bài.

## 6. Giả định và thất bại do tác giả nêu

Bài BARO §3.1 giả định lỗi hiện ở latency/error và dùng bất thường đầu tiên ước lượng mốc sự cố. §5 giới hạn deployment và cách thu thập. Đây không là bảo đảm mọi changepoint là sự cố hay mọi sự cố đổi covariance.

Phân tích riêng từ code: không còn cột thì `[]`; missing→0 có thể tạo điểm đổi; mật độ quá nhỏ có thể underflow làm tổng0; điểm sát cuối thiếu bằng chứng tương lai; thay min–max nhưng prior cố định có thể đổi posterior. Các nguyên nhân khác gồm noise/tải đổi, dimension, hazard, tên metric khác, và lỗi sentinel. Không suy tỷ lệ thất bại ngoài ví dụ đã kiểm.

## 7. Ví dụ tính tay

Một chiều, prior \(t_2(0,1)\), tại \(x_1=0\) có density \(0.35355339059327384\). Mass đổi đoạn là 0.02×density; mass kéo dài là 0.98×density; chuẩn hóa được \((0.02,0.98)\). Hai ca thật dùng prefix cố định ≤120 để kiểm posterior và maxes với code official; `vi-du-tinh-tay.md` cùng NPZ lưu mọi posterior. Đây là ví dụ cơ chế, không phải đánh giá hiệu quả toàn ca TT.

Tái dùng T-007 mốc A có 100 ca OB trùng tác giả. Audit chỉ các ca OB ở `trung-gian/T007-bocpd-allowed-records.json`:99/100 có điểm 600 ngoài window 600, nhưng không ca nào chỉ có sentinel hoặc lấy sentinel làm điểm đầu; bỏ riêng sentinel không đổi P/R/F1 tập đó. Không quy Recall = 1 của OB cho sentinel.

## 8. Đường nhãn có thể lọt

Ba đường độc lập: min–max toàn-window dùng tương lai; window quanh injection dùng nhãn trực tiếp; biên snapshot đối xứng vẫn lộ mốc khi bỏ file nhãn. Bản recurrence Bayes dùng quá khứ không làm toàn wrapper trở thành trực tuyến. Xem `cua-so-va-che-do-b.md` để phân biệt phát hiện hồi cứu không biết mốc với cảnh báo online.

## 9. Dataset khác và chi phí toàn tập

Cần trục thời gian/mapping index→timestamp, metric numeric, cadence, schema latency/error, missing rõ và biên recording độc lập sự cố. Chấm online cần preprocessing từ lịch sử hợp lệ; wrapper hiện tại chưa đáp ứng. Chấm hồi cứu không biết mốc có thể dùng recording chọn độc lập lỗi nhưng phải khai báo look-ahead (dùng tương lai); không gọi thời điểm phát hiện là thời điểm báo động online.

Một run có \(T(T+1)/2\) predictive evaluations. Tổng dataset là \(\sum_iT_i(T_i+1)/2\), không chỉ chi phí một ca. Ma trận R dùng 8(T+1)² byte; trạng thái covariance còn O(Td²), runtime code xấp xỉ O(T²d³) do inverse và density từng run length. RAM tuần tự lấy **max** chi phí ca, không cộng peak mọi ca. Số kịch bản và ngoại suy T-005 nằm trong `trung-gian/chi-phi-va-sentinel.json`. T-013 không chạy BOCPD full TT đã vượt 1 giờ và không benchmark cả dataset. Ngoại suy chưa kiểm: giả định cùng T,d, thư viện và độ bận máy; sai nếu chúng khác. Muốn kiểm runtime chính thức cần lượt riêng sau G1 trên máy rảnh, trong ngân sách đã duyệt.
