**Chưa đủ để Minh duyệt v2d làm bộ chấm cho lần sau, hoặc duyệt nguyên văn chữ sửa WHY-110.** Hai ca trọng tâm CX‑36b đã đạt. Claude cũng đúng khi bác kỳ vọng D4 của Codex. Tuy nhiên, tôi tái hiện được hai trường hợp khác làm v2d chốt sai tỷ lệ khi lưới xuất bị khuyết.

**Giữ kết quả R5 Minh đã nhận.** E4 ghi nhận **0 sự cố trong 383 phút khỏe ×1**, khoảng tin cậy Poisson 95% **[0; 3,47] sự cố/6 giờ**. Tôi kiểm tra lưới của 9 file xuất E4 và không thấy bước khuyết hay khúc truy vấn lỗi. Tôi không chấm lại E4. [Kết quả E4, `#/mau_so`, `#/ty_le_khoe_x1` và `#/ba_nguon`](D:/RCA-flashticket/results/T-072/bang-bao-dong-gia.json) · [Quyết định Q2](D:/RCA-flashticket/docs/DECISIONS.md:775)

## 1. Đã làm gì và phát hiện gì

Tôi đối chiếu quy tắc đã khóa với đường chạy `đọc lưới → Pending → Alerting → gom 300 s → quy phút → tử số và mẫu số`. Tôi lập phản ví dụ trên mã và đầu ra gốc trước khi đối chiếu các bản đáp. Các số dưới đây là kết quả gọi trực tiếp bộ chấm trong bộ nhớ.

### CHẶN 1 — Vượt 14 bước khuyết, v2d có thể chốt 1 khi tử số cũng có thể bằng 0

Tôi dùng một luật hệ thống, một khóa chuỗi, `for=60 s`, lưới 10 giây từ 0 đến 350, bắt đầu chấm ở giây 180. Có 15 bước lỗi từ giây 10 đến 150. Giây 160 thấy điều kiện sai. Từ 170 đến 260 thấy điều kiện đúng. **Mẫu số là 3 phút ở cả ba lần gọi.**

| Dữ liệu đưa vào `cham()` | Khoảng Alerting | Tử số |
|---|---|---:|
| Giữ 15 bước khuyết | Bảng liệt kê `[230,270)` | **1**, kèm ghi chú mọi cách điền cho cùng tử số |
| Điền 15 bước là sai | `[230,270)` | **1** |
| Điền 15 bước là đúng | `[70,160)` và `[230,270)` | **0** |

Ở dòng cuối, hai khoảng cách nhau 70 giây nên phải gom. Sự cố bắt đầu ở giây 70, trước khoảng chấm. V2d bỏ sót đúng mối nối này vì phép tìm khoảng gần loại mọi khoảng cùng `(uid, khoa)`. Bảng dùng để tìm khoảng gần cũng chỉ chứa cách điền mặc định. Vì vậy, chỉ bỏ điều kiện so UID vẫn chưa bao phủ khoảng chỉ xuất hiện ở một cách điền khác. [Nhánh vượt giới hạn](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2d.py:320) · [Quy tắc `#/gom_su_co`](D:/RCA-flashticket/results/T-072/quy-tac-gom.json)

Cùng nhánh còn có thể trả **danh sách tử số thiếu**. Tôi giữ nguyên lưới và 15 bước lỗi, bắt đầu chấm ở 0, cho mọi bước quan sát là sai. V2d trả `chua-phan-xu`, `tu_so_kha_di=[0]`. Hai chuỗi đầy đủ cho **0/6** và **1/6**. Trường danh sách do đó không đủ để người đọc loại giá trị 1. [Chỗ xuất `tu_so_kha_di`](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2d.py:331)

**Đề xuất tối thiểu:** khi có đơn vị hệ thống vượt giới hạn mà chưa chứng minh được nó vô can sau phép gom, trả `chua-phan-xu` và để `tu_so_kha_di=null`. Có thể áp dụng ngay cách bảo thủ này cho mọi đơn vị hệ thống vượt giới hạn. Mặt trái là một số ca thực sự có tử số duy nhất cũng phải đối chiếu Grafana. Tăng giới hạn 14 chỉ dời phản ví dụ sang lỗ dài hơn.

### CHẶN 2 — Mất trọn một phút xuất làm một phút khỏe đã phân loại biến mất khỏi cả tử số lẫn mẫu số

Tôi dùng ba phút `[0,180)` đều được T‑071 phân loại khỏe, bắt đầu chấm ở 0. Điều kiện đúng ở các bước 20–50, thiếu toàn bộ sáu bước 60–110, sai từ 120. Kết quả từ hàm `chay()` của bộ ca v2d:

| Đầu vào | Kết quả |
|---|---|
| Lưới thiếu sáu bước | **0/2**, kèm ghi chú mọi cách điền cho cùng tử số |
| Chuỗi đủ, điền sáu bước là sai | **0/3** |
| Chuỗi đủ, đúng đến giây 80, sai từ 90 | **1/3**, Alerting ở giây 80 |

Đây là lỗi **ngay trong giới hạn liệt kê**. V2d dựng tập phút khỏe từ `du.luoi` trước khi xét các cách điền. Mốc Alerting 80 có thể được dựng lại, nhưng phút 60 đã bị loại khỏi tập được đếm. Quy tắc khóa lấy mẫu số từ các phút khỏe trong khoảng chấm. Quy tắc chỉ loại phút khỏi số đếm Grafana khi có căn cứ Grafana ngừng đánh giá. Một lỗ trong bản xuất ngoại tuyến chưa cung cấp căn cứ đó. [Cách lập `phut_khoe`](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2d.py:289) · [Quy tắc `#/ty_le_bao_dong_gia/mau_so` và `#/gian_doan_grafana`](D:/RCA-flashticket/results/T-072/quy-tac-gom.json)

**Đề xuất tối thiểu:** trong biên khoảng chấm, lấy các phút khỏe trọn đủ điều kiện từ bảng phân loại T‑071. Giữ cách xử lý phút đầu của CX‑33 A. Với ca trên, trả mẫu số **3**, tử số khả dĩ **`[0,1]`**. Nếu có bằng chứng vận hành cho thấy Grafana thực sự ngừng đánh giá, áp điều khoản riêng cho nguồn Grafana. Loại phút chỉ vì file xuất bị đứt sẽ làm thay đổi đại lượng R5.

### CHẶN 3 — Chữ WHY-110 còn đồng nhất trạng thái Alerting với thời điểm chuyển vào Alerting

Bản mới đã giới hạn đúng phạm vi ở **bước E2 thuộc phút khỏe ×1, đủ bảy mẫu, trên lưới xuất**. Phần còn sai là câu “luật **vào** Alerting tại t khi và chỉ khi S(t) > θ”. Tôi cho tín hiệu vượt ngưỡng liên tục ở các bước 20–110, với `for=60 s`. V2d trả đúng một khoảng **`[80,120)`**. Tại 90, `S(90)>θ`, nhưng lần chuyển vào Alerting đã xảy ra ở 80. Phân biệt này có hệ quả vì thời điểm chuyển là `t_hat` dùng để quy sự cố về phút. [Chữ đề nghị ở §2 và §3](D:/RCA-flashticket/results/T-072/dap-cx33.md:30) · [Máy trạng thái](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2d.py:99)

Tôi đề xuất Minh duyệt **nội dung** sau cho phần p95, sau khi Claude đáp:

> Trên lưới xuất E2, tại bước t thuộc phút khỏe ×1 có đủ bảy mẫu trong [t−60 s, t], S(t) > θ khi và chỉ khi điều kiện p95 vượt θ đã duy trì suốt cửa sổ đó. Với θ ≥ M, không bước nào trong tập xét thỏa điều kiện này. Thời điểm chuyển vào Alerting là bước đầu tiên đủ `for` của một dãy vượt ngưỡng. Bộ chấm với ngưỡng đã chọn ghi nhận 0 sự cố trên toàn E2.

Phần 5xx đã sửa **đúng**. Chuỗi dùng tính M đã chặn `≥30` request. Luật thật chặn thêm `≥3` lỗi. Ví dụ 2/32 vượt 5% nhưng thiếu số lỗi, nên `θ ≥ M` là điều kiện đủ trên tập bước đang xét. Câu trong WHY dự kiến bảo đảm v2d trả `chua-phan-xu` khi tử số không duy nhất cũng cần bỏ hoặc thu hẹp cho tới khi xử lý hai điểm chặn trên. [Biểu thức đầu vào 5xx](D:/RCA-flashticket/results/T-072/bieu-thuc.json:431) · [Kết quả E2, `#/trong_mau`](D:/RCA-flashticket/results/T-072/nguong.json)

### KHÔNG CHẶN R5 — CX‑33 C còn thiếu trong bảng đáp và đơn vị rủi ro Ticket vẫn dễ bị dùng sai

Đầu ra mô hình là **1,0424 cửa sổ 5 phút vượt ngưỡng trên 6 giờ** ở tỷ lệ chậm cao nhất. Mô hình lấy 72 request/cửa sổ và giả định các request chậm nằm trong bucket `(0,1; 0,25]` giây. Số 4 là số request chậm đủ làm **p95 của một cửa sổ** vượt 0,112 s theo giả định đó. Mô hình chưa áp `for=60 s` trên lưới trượt hay ghép 300 s thành sự cố. Câu “chạm ngưỡng R5” ở báo cáo cũ và “rủi ro ≈ 1/6 giờ” trong STATE còn có thể bị hiểu thành số sự cố. Bảng đáp lượt 14 có A, B, D và hai ca CX‑36b, thiếu C. [Mô hình, `#/gia_dinh` và `#/route/ticket/theo_ty_le/max_luot_x1`](D:/RCA-flashticket/results/T-072/troi-p95-rui-ro.json) · [Câu so với R5](D:/RCA-flashticket/results/T-072/troi-p95-e2-e4.md:67) · [Bảng đáp](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/LOG.md:339)

**Đề xuất:** dùng đúng đơn vị cửa sổ trong chữ trình WHY và hồ sơ G6, dẫn đính chính cho báo cáo đã ghim. Tần suất sự cố ở kịch bản mô hình còn mở vì cùng số cửa sổ vượt có thể tạo nhiều đợt rời hoặc một đợt kéo dài. Muốn ước lượng đại lượng đó cần chuỗi thời gian tương ứng rồi áp `for` và gom. Việc sửa đơn vị chỉ cần đối chiếu file đã lưu.

### KHÔNG CHẶN tử số — Cờ `pending-sau-lo-luoi` có thể mô tả ngược thứ tự thời gian

Với Pending ở 20, Alerting ở 80 và **bước lỗi đầu tiên ở 90**, bảng mặc định của v2d trả `[80,90)` và gắn `pending-sau-lo-luoi`. V2c trả cùng khoảng, chỉ gắn cờ lỗ xuất và cửa sổ lấn. Nguyên nhân là v2d gắn cờ cho mọi Pending thuộc đơn vị có lỗ, kể cả khi lỗ xảy ra sau khi cảnh báo đã cháy. Vì vậy câu “bảng liệt kê … trùng hành vi cũ” chỉ đúng cho mốc của ca này. Đề xuất giữ cờ Pending sau lỗ cho trường hợp lỗ thực sự đứng trước đầu dãy tương ứng. [Chỗ lập và dùng `dv_tp`](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2d.py:292)

## 2. File và phạm vi

**Tôi không sửa file nào.** Tôi tự thực hiện trên laptop, không dùng subagent, không SSH, không mở dữ liệu khóa, không commit. Các phép thử dùng dữ liệu giả trong bộ nhớ. Khi chạy script hồi quy tôi dùng Python 3.12.14 với `-B`, không truyền `--ghi`.

Các đầu ra lượt 14 mà Claude kê nằm trong `results/T-072/`, LOG của task và dòng T‑072 trong STATE. LOG có prompt bàn giao. Riêng trình tự tự soát, LOG ghi đã đọc CX‑36b lúc 18:09Z rồi mới ghi tự kiểm lúc 18:11Z. Vì thế hồ sơ chứng minh có kiểm lại trên code, nhưng **không chứng minh đã ghi nhận xét độc lập trước khi đọc kết luận**. Lượt này tôi đã kiểm độc lập hai ca đó. Ngoại lệ scratchpad ngoài repo từ lượt cũ vẫn chưa có phê duyệt có trước trong nguồn được dẫn. I9 ở server không giải quyết quyền ghi trên laptop. Hai điểm này không làm thay đổi số E4. [LOG lượt 14](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/LOG.md:331) · [Bản đáp về scratchpad](D:/RCA-flashticket/results/T-072/dap-cx19.md:25) · [Phạm vi SPEC](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/SPEC.md)

## 3. Kiểm đã chạy và đối chiếu các lượt trước

| Điểm | Kết luận độc lập |
|---|---|
| **CX‑36b‑1** | **Đúng, đã sửa.** Thiếu bước 80. Điền sai cho **0/2**, điền đúng cho **1/2** với `t_hat=80`. V2d trả `chua-phan-xu`, `[0,1]`. |
| **CX‑36b‑2** | **Đúng, đã sửa.** Thiếu bước 110. Hai cách điền cho `t_hat=110` hoặc `180`. Cả hai thuộc phút khỏe và cho **1/4**. V2d chốt 1. |
| **CX‑33 A, CX‑33b D, CX‑36 D1–D7** | **A và phản ví dụ D gốc đúng. Claude đúng khi bác D4 của Codex.** Ở D4, bước sai 120 đặt lại Pending của luật, nhưng khoảng `[90,120)` vẫn có thể ghép với cảnh báo ở 190. Hai lịch sử cho 0 và 1. Sửa kỳ vọng D4 có căn cứ từ quy tắc đã khóa. Các kết luận rộng hơn về mọi lỗ còn bị chặn ở trên. |
| **CX‑24/24b, CX‑19 F5 và CX‑19b N1** | **Đúng đối với các ca đã nêu.** Chạy lại `thu_ca_gia.py`, `thu_ca_gia_v2c.py`, `thu_ca_gia_v2d.py` đều thoát 0. Cả ba stdout khớp **từng byte** với biên bản tương ứng. V2d đạt 9/9 ca gốc, số khoảng thực `[0,1,2,2,2,2,2,2]`. Thiếu riêng p95 Ticket làm CLI thoát 1. `tu_kiem()` của v2, v2_claude, v2c, v2d đều trả `[]`. Năm đột biến tôi dựng trong bộ nhớ theo năm loại ghi ở LOG đều bị ca D bắt. [Ca và đối chứng](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia_v2d.py) |
| **CX‑19/19b F1–F2** | **Đúng.** `health_ok=06:06:01Z`. Nhóm truy vấn đầu nằm trọn sau đó bắt đầu `06:06:10Z`. Đếm theo UID được 4 luật thử có 1/1 khoảng, **12/12** độ lệch bằng −4 s, mỗi luật có một webhook `firing` và một `resolved`. 11 luật thật cho 0/0. Các mốc phù hợp với lệch pha. Thiếu thời điểm mẫu khả dụng ở từng tick để tách độ trễ nạp. Giới hạn này ảnh hưởng giải thích E3. [Log G](D:/RCA-flashticket/results/T-072/e3/b10-restart-g.txt:4) · [Đối chiếu `#/theo_uid`](D:/RCA-flashticket/results/T-072/e3-doi-chieu-offline.json) · [Webhook `#/theo_luat`](D:/RCA-flashticket/results/T-072/e3/b9-doi-chieu.json) |
| **F3, CX‑33 B/C, N2** | **Đúng một phần đối với chữ đề nghị.** Chọn trên E2 theo mục tiêu khai trước vẫn giữ E4 độc lập. Một bước vượt phân vị chưa đủ tạo cảnh báo. Khi nêu phương án thay thế, nên viết “tối ưu một mục tiêu tỷ lệ trên E2” vì E2 chỉ có 356 phút khỏe, dưới 360 phút để kết luận đạt R5. Tôi lấy lại đúng 7 mẫu Booking lúc 18:21:50Z ở lượt flash, min **0,050750 s**, cao hơn M khỏe **0,047482 s**. Phạm vi khỏe đã sửa đúng. Phân biệt trạng thái với lần chuyển và đơn vị Ticket còn thiếu như trên. [E2, `#/ty_le_khoe_x1`](D:/RCA-flashticket/results/T-072/e2/cham-trong-mau.json) · [M Booking, `#/chi_tiet/theta_p95_booking/M`](D:/RCA-flashticket/results/T-072/nguong.json) |
| **F4, F6, K1** | **F4 đúng.** Đọc các thành viên `doc-lap__restarts.json.gz` trong 8 lượt E2 và 9 lượt E4 cho 12 tên ở mỗi khoảng, các giá trị đã lưu đều bằng 0, không có Collector. `OOMKilled` lấy từ trạng thái k6. **F6 đúng một phần ở hiện trạng** vì LOG T‑072 có prompt nhưng `buoc_tiep` của điều phối còn chờ CX‑24b. **K1 đúng về thao tác ghi** vì script chuyển hướng `docker logs` vào file. Quyền scratchpad được phân biệt ở mục 2. [Bộ phân loại](D:/RCA-flashticket/results/T-071/phan_loai_phut.py:117) · [Trạng thái điều phối](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/TRANG-THAI.json:65) · [Lệnh K1](D:/RCA-flashticket/results/T-072/e4/k1-kiem.sh:19) |

**Toàn vẹn.** Kiểm SHA‑256 khớp **10/10** ở `SHA256SUMS-dap-cx33`, **8/8** ở `-dap-cx19`, **5/5** ở `-troi-p95`, **21/21** ở `-e4`, **3/3** ở `-e4-grafana`, **6/6** ở `-e3-offline` và **11/11** ở `-cx09`. Có **4/19** đường dẫn khác byte so với manifest lịch sử `-e2-nguong`, gồm ba file đề xuất commit lab và script sinh luật thử. Tôi dừng dùng bốn bản hiện tại làm đại diện cho bản lịch sử. Các file ngưỡng, phút và chuỗi E2 dùng ở trên khớp mục ghim tương ứng. [Manifest lượt 14](D:/RCA-flashticket/results/T-072/SHA256SUMS-dap-cx33) · [Manifest E2](D:/RCA-flashticket/results/T-072/SHA256SUMS-e2-nguong)

**Tiêu chí SPEC và mục tiêu nguồn.** Có dấu vết khóa biểu thức, quy tắc chọn ngưỡng và cách gom trước E2. Bản gom 3 bổ sung lịch E4 sau E2, trước E4. E3 có bằng chứng webhook dương. E4 có bảng theo lớp và phép so R5 đã khai trước. Đếm hợp lưới từ `cua_so` và `step_s` cho **2.676 bước E2, 2.868 bước E4**, cả hai có 0 bước khuyết và 0 `loi_khuc`. Tôi không thấy sổ tiêm, nhãn nguyên nhân hay thời điểm tiêm đi vào bộ chấm. Nhãn phút T‑071 dùng để chọn ngưỡng trên nền và xác định mẫu số. W4 cung cấp bằng chứng về báo động giả cho P10. Độ nhạy phát hiện, chất lượng xếp hạng RCA và lợi ích của đồ thị cần bằng chứng của gói tương ứng. [SPEC T‑072](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/SPEC.md) · [Quy tắc chọn ngưỡng](D:/RCA-flashticket/results/T-072/quy-tac-chon-nguong.json) · [MRP P10](D:/RCA-flashticket/docs/MRP.md:303)

## 4. Điều cần Minh quyết

**Đề xuất tiếp tục một lượt đáp hẹp của Claude.** Minh có thể nhận hai sửa CX‑36b và chấp nhận đổi kỳ vọng D4 ngay. Tôi đề xuất **hoãn chọn v2d và hoãn ghi nguyên văn §3 vào WHY‑110** cho đến khi Claude đáp hai sai lệch tỷ lệ và câu về thời điểm vào Alerting. Nếu cần dùng kết quả cho hồ sơ G6 ngay, dùng số E4 đã khóa với đơn vị và giới hạn ở trên. Các phản ví dụ mới chỉ cần ca giả trên laptop. Không cần giờ máy hay dữ liệu thật bổ sung để phân xử.

V2d, script sinh, ca thử, biên bản và `dap-cx33.md` đã được ghim. Nếu Minh duyệt sửa, đề xuất lập bản kế tiếp cho phần sửa, giữ các bản ghim để tái hiện lượt 14. Mặt trái là thêm một phiên bản cần đối chiếu. Sửa trực tiếp các file này sẽ làm lệch manifest hiện tại. Quyết định chọn bộ chấm và duyệt chữ WHY vẫn thuộc Minh. [Manifest phạm vi bị ảnh hưởng](D:/RCA-flashticket/results/T-072/SHA256SUMS-dap-cx33)

## Prompt bàn giao cho Claude

Minh có thể gửi kèm bản nhận xét trong chat này. Mẫu hiện có các khối trọng tâm G0–G4, chưa có khối G6. Dưới đây là Prompt chung và đúng khối **Người làm đáp phản biện**. [Mẫu bàn giao](D:/RCA-flashticket/docs/review-prompt.md)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-072 lượt 14, tasks/T-072-w4b-luat-canh-bao/, results/T-072/v2/, results/T-072/dap-cx33.md và bản kiểm lại do Minh chuyển kèm trong chat.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P10 (W4), chuẩn bị G6.
- Người làm và người phản biện chính thức: Claude là người làm T-072; Codex là người phản biện.
- Tài liệu gốc: tasks/T-072-w4b-luat-canh-bao/SPEC.md, LOG.md của task, docs/WHY.md, results/T-072/quy-tac-*.json, results/T-072/bieu-thuc.json.
- Phản biện và phản hồi trước: results/T-070/codex/CX-19-tin-cuoi.md, CX-19b-tin-cuoi.md, CX-24-tin-cuoi.md, CX-24b-tin-cuoi.md, results/T-072/dap-cx19.md, results/T-070/codex/CX-33-tin-cuoi.md, CX-33b-tin-cuoi.md, CX-36-tin-cuoi.md, CX-36b-tin-cuoi.md, results/T-072/dap-cx33.md, LOG T-072 lượt 14 và bản kiểm lại trong chat do Minh chuyển.
- Code và kết quả liên quan: results/T-072/v2/cham_offline_v2*.py, thu_ca_gia*.py và ra/ trong cùng thư mục, results/T-072/SHA256SUMS-dap-cx33, SHA256SUMS-dap-cx19, SHA256SUMS-troi-p95, results/T-072/e4/, results/T-072/troi-p95-*.json. Laptop Windows, Python với -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc trên laptop, không SSH, không dùng subagent, không chấm lại E4.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```