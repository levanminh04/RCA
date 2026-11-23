**Đề nghị tiếp tục một lượt đáp của Claude. Tôi chưa đề nghị phát E6 theo nháp hiện tại hoặc khóa W7 theo bản 4.** Phần số học của tám phương án thu cơ sở khớp. Các điểm chặn nằm ở quyền và đường hoàn tác E6, cách tính thời gian nền nhiễm lỗi, điều kiện chạy D13 và việc giữ đầu vào W7 khi một phương pháp lỗi.

Q8 ngày 23/11 là quyết định có điều kiện của Minh, khi T-074 trình bản đã qua hai phiên Codex. CX-15/15b đánh giá **bản 3**. Lượt này tôi đánh giá **bản 4 và nháp E6**. Q9 vẫn cho E7 đi trước nếu đủ điều kiện đã ghi. Tại mốc hồ sơ máy gần nhất tôi đọc, 05:34:30Z, T-073 đã dừng bộ điều phối và chuyển exp-obs sang H trong lúc hoàn tác S4. Dòng này chưa bàn giao S5. `STATE` và `TRANG-THAI.json` còn ghi trạng thái E5 cũ. Khi phát máy, điều phối cần dùng bàn giao theo I4. [Quyết định Q8–Q9](D:/RCA-flashticket/docs/DECISIONS.md:781) · [Lịch máy](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md) · [Hợp đồng I4](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md:28)

### Các điểm chặn

**1. CHẶN phát E6. Bước thực hiện cần nhiều quyền hơn bảng S5, kể cả khi bỏ phép đo K2.**

S5 hiện giao exp-app và quyền dùng nhẹ exp-obs, cột máy tải là `—`. Nháp ghi chỉ cần máy tải và runner nếu chạy 6(c), nhưng bước 5 yêu cầu tải ×1, bước 7 đọc đồng hồ ba máy, bước 3 có phương án mua bằng k6. Riêng 6(c) còn xung đột với mục “không thu ca RCA”. Ở `407b4f5` và `81a9273`, `runner4.py` đưa cả `BINH-THUONG` vào hàng đợi M1. Worker stage ca, chạy P7, xuất gói rồi chạy V082. Một chu kỳ khỏe qua đúng runner được dẫn vẫn tạo ca RCA và ghi ngoài danh sách đầu ra E6. Ở chiều ngược lại, nếu E6b sau đó thêm quota/proxy, hash cấu hình ở bước 7 chỉ chứng minh trạng thái **trước E6b**. [Nháp E6, quyền máy và bước 0–8](D:/RCA-flashticket/results/T-074/e6-spec-nhap.md:56) · [Runner, nhánh đưa ca vào hàng đợi](D:/Project/flashticket-rca-lab/campaigns/runner/runner4.py:276) · [Runner, worker](D:/Project/flashticket-rca-lab/campaigns/runner/runner4.py:212)

**Sửa tối thiểu:** tôi đề xuất K0, bỏ 5–6(c) khỏi lượt xin phát đầu tiên, chỉ rõ đường mua của bước 3 và quyền đọc đồng hồ ở bước 7. Nếu dùng máy tải thì điều phối phải giao đúng phần đó. Nếu Minh giữ K2, ghi riêng tải ngắn và quyền máy của nó. Có thể bỏ 6(c) vì 6(a)(b) đã là tiêu chí K2 của chính nháp. Khóa cấu hình W7 ở trạng thái sau thay đổi cuối cùng được duyệt.

**2. CHẶN phát phần sửa DB và kết luận K2. Mốc W7 đang đòi một quan sát từng bị từ chối, còn phương án lỗi 99% quay về chính trạng thái chưa chứng minh khôi phục được.**

`moc-db.json#/bo_sung_luot_2/redis/ket_qua` ghi `INFO keyspace` trả `NOAUTH`. Bước 4 lại yêu cầu Redis keyspace ngay cả ở K0. Nháp đã ghi hạn chế xác thực MongoDB nhưng chưa nêu đường được phép để lấy bằng chứng Redis. Ở K2, bước 5 còn cần xóa một số khóa Redis và dừng/khởi động dịch vụ. Phạm vi ghi mới nêu các bảng/cột và khôi phục DB. Đếm keyspace cũng chưa chỉ được khóa giữ chỗ nào mồ côi. [Mốc E1](D:/RCA-flashticket/results/T-071/e1/moc-db.json) · [Đầu ra và phạm vi E6](D:/RCA-flashticket/results/T-074/e6-spec-nhap.md:45)

Bảng 10/50/99% có đủ ba hàng. Tuy nhiên, ở 99%, “đưa hệ về mốc W7 đã kiểm” chưa phải đường phục hồi khi kiểm nhất quán của chính lần restore vừa trượt. “0 thu thêm” không tính thời gian sửa trạng thái và xác nhận hệ bán vé dùng lại được. Ở 50%, restore lại dump trước sửa có thể trả hạn bán và sức chứa về giá trị cũ. Bước 3 còn tạo một giao dịch mua trước khi dump từng DB ở bước 4. Sự vắng mặt của bộ phát tải chưa bảo đảm outbox, consumer và giao dịch mua đã yên tại thời điểm chụp. [Bước 3–6](D:/RCA-flashticket/results/T-074/e6-spec-nhap.md:67) · [Lỗi giữa chừng](D:/RCA-flashticket/results/T-074/e6-spec-nhap.md:103)

**Sửa tối thiểu:** với K0, ghi rõ mốc PostgreSQL và giới hạn Redis nếu chưa có đường đọc được duyệt. Với K2, nêu quyền Redis/service cụ thể, trạng thái yên cần đạt **trước** dump, nơi có thể lui về khi restore dở, phần ngày/sức chứa phải làm lại và chi phí khôi phục dịch vụ. Nếu kiểm 6(a) trượt và chưa phục hồi được trạng thái nhất quán thì giữ máy ở điều phối, chưa giao K0 chạy trên trạng thái ấy. Thời gian restore thật là số cần đo trong E6 nếu Minh chọn nhánh này. Không có căn cứ để điền số thực từ tốc độ dump E1.

**3. CHẶN khóa bảng diễn giải chế độ (b). Công thức `giay_N_nhiem` sai ngay theo lịch đã khai.**

Bản 4 §7 dùng `min(t̂−t,300)` cho cả cửa sổ ghép, trong khi lỗi theo lịch ở `[t,t+600)` và G1 cho ghép tới trước `t+970`. Lấy `t̂=t+900`. N là `[t+600,t+900)`, giao với khoảng tiêm theo lịch bằng **0 giây**. Công thức ghi **300 giây** và xếp ca vào nhóm “N nằm trọn trong đoạn lỗi”. Điều này có thể đảo nghĩa bảng so (a)/(b), nhất là khi cảnh báo đến sau gỡ. Ba nhóm hiện còn trùng biên tại 60 và 180 giây. [Công thức bản 4](D:/RCA-flashticket/results/T-074/thiet-ke-w6-4.md:150) · [Cửa sổ ghép G1](D:/RCA-flashticket/results/T-074/thiet-ke-w6-3.md:17)

**Sửa tối thiểu:** chấm sau khi băm đầu ra, dùng độ dài giao `max(0, min(t̂, t_stop) − max(t̂−300, t_start))`, ghi rõ đây là giao với khoảng **theo lịch** hay **theo mốc xác nhận**. Dư âm sau gỡ có thể kéo dài, cần bằng chứng tín hiệu riêng. Dùng các khoảng nhóm không chồng biên. Phần lọc tải/N của W7 cũng cần phân biệt nền trước tiêm dùng xét tính hợp lệ của **ca** với N quanh `t̂` dùng cho **phương pháp**. Dùng tình trạng suy giảm sau tiêm để loại ca sẽ loại đúng các ca (b) mà phép so phải đo.

**4. CHẶN khẳng định D13 khả thi khi `g ≤ 300 s`. Bản 4 dùng lệch mốc và gộp hai gói có độ dài khác nhau.**

D13 đã duyệt lấy `t_p` lúc Grafana lần đầu rời Normal, thường là Pending. Nền lùi là `[t_p−g−300,t_p−g)`. Gói cơ sở của E5 bắt đầu ở `t̂−600`. Để phủ đầu trái cần `g + (t̂−t_p) ≤ 300`, ngoài các điều kiện về lịch sử trạng thái, phiên bản và biểu thức. Ví dụ `g=300`, Pending trước `t̂` 20 giây thì gói cơ sở thiếu 20 giây. `startsAt` trên webhook E5 được ghi là nguồn phụ. Nó không tự cung cấp mốc Pending. [D13 trong SPEC nguồn](D:/RCA-flashticket/tasks/T-043-thiet-ke-rca-m1/SPEC.md:329) · [Điều kiện UNSUPPORTED](D:/RCA-flashticket/tasks/T-043-thiet-ke-rca-m1/SPEC.md:344) · [Khẳng định ở W6](D:/RCA-flashticket/results/T-074/thiet-ke-w6-4.md:129)

Còn một giới hạn thực thi. `stage_b.py` lấy dữ liệu cơ sở tới ±600 giây. `orchestrator.py` gọi bộ xuất bổ sung chỉ với `--t`, mặc định ±300 giây. Trên ca `7577dd5b`, `prometheus-bo-sung.json#/cua_so` đúng bằng `[1795400010,1795400610]` quanh `t̂=1795400310`. H5 còn đọc cả mẫu đúng biên phải. Nới gói bổ sung rồi truyền nguyên vào H5 sẽ thay hành vi bản khóa. [Bộ xuất bổ sung](D:/Project/flashticket-rca-lab/campaigns/runner/xuat_bo_sung.py:103) · [H5 đọc N/A](D:/RCA-flashticket/src/m1_ft/thanh_phan/h4_h5.py:119) · [Gói bổ sung E5](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b/srv/rca-lab/m1/bo-sung/7577dd5b/prometheus-bo-sung.json)

**Sửa tối thiểu:** giữ D13 là dòng độ nhạy tùy chọn. Khai `SUPPORTED/UNSUPPORTED` theo luật, hai mốc, từng nguồn cần và khoảng thực có. Dùng cùng N′ cho baseline. Với bản cần H5, phải chỉ ra cách dựng đúng N′ và giữ đúng A. Có thể giữ lượt chính nguyên trạng và ghi D13 thiếu dữ liệu. Điểm này không chặn lượt chính của D14.

**5. CHẶN khóa đường thu W7. Bất đồng bộ với runner chưa giải quyết việc gói đầu vào còn phụ thuộc P7.**

Ở `81a9273`, `orchestrator.py` chạy tuần tự `stage → P7 → bổ sung → V082 → kiểm → G1`. Chỉ ngoại lệ P7 đã nhận diện mới được đi tiếp. Một ngoại lệ P7 khác sau stage vẫn có thể làm thiếu gói bổ sung của ca. `safe_export.py` hiện đòi `outputs/<id>/summary.json`. Bản 2 §8.2 đã nhận đúng vấn đề và đề xuất `case-input`. Bản 4 §6 lại dùng việc bộ điều phối E5 có PID riêng để kết luận chi phí chờ bằng 0. PID riêng chứng minh runner có thể đi tiếp. Nó chưa chứng minh gói thô được niêm độc lập, hoặc từng sự cố được phục vụ đúng `t̂+750` khi có hàng chờ. [Yêu cầu T1–T4](D:/RCA-flashticket/results/T-074/thiet-ke-w6-2.md:307) · [Tuyến E5 ở revision `81a9273`](D:/RCA-flashticket/results/T-073/e5.diff) · [Điều kiện xuất gói](D:/Project/flashticket-rca-lab/campaigns/runner/safe_export.py:66)

**Sửa tối thiểu:** trong thiết kế, chỉ định T1b dùng bộ gom và bộ chụp của W5 để xuất **cả gói cơ sở lẫn bổ sung**, niêm trước khi gọi phương pháp. P7/V082/G1 thuộc tuyến tương ứng sau đó. Ghi `0` cho phần **runner phải chờ nối tiếp** nếu chọn cách này. Độ trễ hàng chờ và khả năng giữ đủ capture ở ×3 còn phụ thuộc pilot đã dự kiến. Cùng vấn đề ở pilot: `chay_d2` hiện gọi `start_load(...)` không truyền `mult`, mặc định ×1. Dự toán ghi pilot hai mức tải. Gói code W7 cần một đường thực sự chọn ×3 và kiểm hệ số thực chạy. Đây là yêu cầu thiết kế, chưa cần cài hoặc chạy trong T-074.

**6. CHẶN khóa adapter và tiêu chí nghiệm thu baseline. Còn một bước làm hỏng tên sau khi đã chuẩn hóa đúng.**

`SimpleRCA.prepare(..., aliases=...)` có thể đưa `booking-db` về `booking_db` trước khi cộng phiếu. Nhưng wrapper P3 đang dùng `prepare(metric_win,tr,logs,t)` không truyền `aliases`. Sau `diagnose`, nó lại gọi `thuc_the_metric(s)` trên **tên thực thể** ở cả `observed_entities` và `items`. Hàm đó trả `s.split('_')[0]`. Với `booking_db`, kết quả là `booking`. Thêm alias đúng ở đầu mà tái dùng nguyên đoạn cuối vẫn làm mất tên khi chấm. Đơn vị được ghi “chưa kiểm” trong §5 cũng đã có đáp án tĩnh: `prepare` chia `startTime` cho `1e6`, `normalize_spans` trả `start_us,duration_us`. [Wrapper SimpleRCA](D:/RCA-flashticket/src/p3/adapters/simplerca.py:16) · [Hàm tách tên cột metric](D:/RCA-flashticket/src/p3/ban_ghi.py:7) · [Hợp đồng thời gian SimpleRCA](D:/RCA-flashticket/src/simplerca/adapter.py:61) · [Nguồn span FlashTicket](D:/RCA-flashticket/src/m1/adapter_flashticket.py:203)

Với BARO, §10 yêu cầu “thứ hạng không trùng thứ tự cột”. Code tác giả sắp giảm dần theo điểm, ổn định khi hòa. Một cột còn lại, các điểm hòa, hoặc các cột vốn đã theo thứ tự điểm đều có thể trùng hợp lệ. Dùng điều kiện này để bác adapter sẽ bác cả kết quả đúng. [Tiêu chí W6](D:/RCA-flashticket/results/T-074/thiet-ke-w6-4.md:174) · [BARO ở revision đã đối chiếu `259ea41`](D:/RCA-ext/src/RCAEval/RCAEval/e2e/baro.py:39) · [Kiểm khóa điểm tại adapter](D:/RCA-flashticket/src/p3/adapters/baro.py:38)

**Sửa tối thiểu:** quy định ánh xạ trước `prepare`, giữ nguyên tên thực thể chuẩn sau `diagnose`, và đối chiếu tên qua cả `items` lẫn tập quan sát. Với BARO, giữ `rank_equals_column_order` làm chẩn đoán. Tiêu chí đạt là tái dựng khớp điểm, thứ tự chính thức và quy tắc hòa. Phép kiểm trên gói dev đã nằm trong câu 6.

**7. CHẶN khóa quy tắc bù ca nếu cho phép dùng đầu dò sạch muộn làm bằng chứng “chưa tiêm”.**

Điểm sửa đúng ở §2 là mất phản hồi thì giữ ca chưa xác nhận. Tuy nhiên, hàng “xác nhận chưa tiêm” vẫn cho dùng quan sát “không toxic, không pause, không lease”. Chính bộ tiêm có hẹn giờ tự gỡ. Một đầu dò sạch **sau** khi hẹn giờ chạy tương thích cả với “chưa tiêm” lẫn “đã tiêm rồi tự gỡ”. `StartedAt` không đổi cũng không giúp phân biệt hai khả năng của thao tác pause. Phân loại nhầm sẽ bù thêm một ca và đổi mẫu số. [Bảng phân loại](D:/RCA-flashticket/results/T-074/thiet-ke-w6-4.md:51) · [Hẹn giờ phía đích](D:/Project/flashticket-rca-lab/faults/injectors/docker/inj3.py:142)

**Sửa tối thiểu:** cho bù ở nhánh này khi có bằng chứng theo **loại can thiệp và thời điểm**, chẳng hạn phía đích từ chối trước bước tác động. Đầu dò sạch muộn dùng để quyết định chạy chu kỳ kế. Nếu chỉ có nó, giữ nhánh chưa xác nhận và không bù.

### E5 đã phân xử được gì cho W6/W7

| Điểm | Kết luận độc lập |
|---|---|
| **N4 — tập ứng viên** | **Đúng với P7, sai nếu suy sang V082 trên ca này.** Đếm `#/entity_ranking` của hai `method-output-1.json` cho P7 có 16 tên, thiếu `payment-service`. V082 có 17 tên và có `payment-service`. Vì vậy “Payment vắng khỏi danh sách V082” đã được bác bỏ trên ca E5. [Đầu ra P7](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b/srv/rca-lab/m1/outputs/7577dd5b/method-output-1.json) · [Đầu ra V082](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b/srv/rca-lab/m1/v082/7577dd5b/method-output-1.json) |
| **N5 — H5 ở mốc tự phát hiện** | **Đúng và đã kiểm trên ca này.** Lọc `#/bundles` theo `channel=live-down`, cổng `8083`, rồi tách tại `#/t`. N có 20 mẫu, ba mẫu bằng 1 ở `t̂−45`, `−30`, `−15` giây. A nửa mở có 20 mẫu bằng 1, và còn một mẫu đúng `t̂+300`. Trong code, `any(x != 0 for x in N)` loại Payment **trước khi xét A**. Đầu ra ghi `H5-liveness.chet_im.thanh_phan={}`. Giữ hay bỏ mẫu biên phải không đổi quyết định H5 đối với Payment ở ca này. Điều đã giải thích là **vì sao H5 không nâng Payment**, chưa giải thích toàn bộ lý do Booking hạng đầu. W7 nên ghi riêng trạng thái điều kiện nền H5 khi so (a)/(b) và bản che. Giữ bản khóa. [Chuỗi đầu dò](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b/srv/rca-lab/m1/bo-sung/7577dd5b/prometheus-bo-sung.json) · [Điều kiện H5](D:/RCA-flashticket/src/m1_ft/thanh_phan/h4_h5.py:125) · [Phân tích ca](D:/RCA-flashticket/results/T-073/dap-cx21/phan-tich-ca.json) |
| **N6 — nguồn hash** | **Đúng, KHÔNG CHẶN W6.** Q6 đã quyết cách xử lý chú thích trên trang demo. W7 cần lấy hash đầu ra từ hiện vật của chính lượt W7. Phần hiển thị thuộc W8/W9a. [Q6](D:/RCA-flashticket/docs/DECISIONS.md:779) |
| **N7 — mốc giờ** | **Đúng, ảnh hưởng §1 và §7 bản 4.** Sổ được điều phối đối chiếu cho `t̂−fault-start = 55,767 s`. Khoảng 60 giây tính từ lúc laptop bắt đầu gửi lệnh. Mốc dashboard mà Q2 nhận là cận trên **898,8 s** sau `t̂`. W6 đang dẫn khoảng 14,8 phút của mốc API. Thay đúng tên mốc, giữ nguyên nghiệm thu chức năng một ô. [Đính chính E5 §1](D:/RCA-flashticket/results/T-073/dap-cx21/dinh-chinh-e5-1.md:9) · [Q2](D:/RCA-flashticket/docs/DECISIONS.md:775) |

**Phủ dữ liệu.** Tôi tách đồng hồ native của CPU/mem khỏi thời điểm đánh giá truy vấn HTTP. Trên `prometheus.json`, CPU/mem Payment có 16 mẫu trong lõi, mẫu cuối khoảng `t̂−65`, mẫu trở lại khoảng `t̂+565`. Bốn kênh HTTP Payment có 20 mẫu, mẫu cuối `t̂−15`, trở lại `t̂+555`. Trong cùng lõi, các kênh tương ứng của Booking có 40 mẫu. Hai độ dài lỗ là **364,999 s** và **315 s**. Dữ liệu củng cố việc thiếu tập trung vào Payment trong khoảng pause. Gói chỉ lưu kết quả truy vấn HTTP dẫn xuất, nên chưa tách hẳn mất mẫu thô với truy vấn không sinh điểm. Giữ ca, báo riêng lớp thiếu và bằng chứng thời gian. Đừng dùng một con số 365 s cho sáu kênh, hoặc dùng kiểm phủ đầu vào P7 thay cho hai kênh H5. [Chuỗi cơ sở](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b/srv/rca-lab/m1/cases/7577dd5b/prometheus.json) · [Độ phủ từng nguồn tại `#/du_lieu_loi/phu/nguon`](D:/RCA-flashticket/results/T-073/e5/su-co/bbc0a6d44f.json) · [Đối chiếu hàng metric V082](D:/RCA-flashticket/results/T-073/dap-cx21/so-hang-metric.json)

### Đối chiếu các lượt trước

| Điểm trước | Kết luận trên hồ sơ hiện tại |
|---|---|
| CX-06 #7 | **Đúng, đã xử lý phần chính.** D2 giữ cấu hình qua E4. R9 đặt việc sửa ngày và sức chứa ở E6. K0 vẫn là đề xuất. W4 chưa phân xử ảnh hưởng riêng của DB ở từng ca. |
| CX-06 #8, CX-08 #1 | **Đúng về mâu thuẫn cũ.** G1/G2, TP đầu tiên và báo trùng đã tách. TP phát hiện độc lập với việc RCA đủ phủ. Lỗi giao khoảng của §7 là lỗi mới, chi tiết ở điểm 3. |
| CX-06 #9, CX-08 #3, CX-15/15b #3 | **Đúng. Phản hồi bản 4 đúng một phần.** BARO bỏ cột hằng riêng ở hai nửa rồi lấy giao. Tính lại sổ được 14/17 mốc lệch lưới epoch 15 giây. Tách native rồi neo tại `t/t̂` sửa lỗi biên. Còn lỗi tên ở wrapper SimpleRCA và tiêu chí thứ tự BARO, điểm 6. |
| CX-08 #2, CX-15/15b #1–2 | **Đúng một phần ở phần sửa.** Dùng lịch thực chạy sửa lỗi gán ×3 cố định thành ×1 ở `phan_loai_phut.py:189`. Tách ba lớp thiếu tín hiệu là đúng. Còn phải xác định N dùng để xét ca, và phân biệt “sạch lúc kiểm” với “chưa từng tiêm”, điểm 3 và 7. |
| CX-08 #4 | **Đúng, đã xử lý ở mức thiết kế.** G-live che cả `live-down`, `live-ms` và dẫn xuất, giữ gói đúng schema. Dev còn phải xác nhận nhánh rỗng như bản 3 §E đã khai. Ca E5 bổ sung được bằng chứng về một điều kiện H5 không kích hoạt. |
| CX-08 #5, CX-15/15b #6 và N4 | **Đúng về số học và hiệu lực JSON.** Tính độc lập khớp 8/8 phương án về chu kỳ, giờ cơ sở, đơn K0 và nhu cầu mỗi khối K2. Riêng **câu 8 và nháp E6 vẫn dùng nhu cầu cả đợt K0** để đặt sức chứa dù chọn K2. Đây có thể là dự phòng cố ý để quay về K0, nhưng phải nói rõ. Nếu chưa xác nhận nhất quán K2 thì chưa được lấy sức chứa mỗi khối làm căn cứ giảm vé. |
| CX-08 #6–7 | **Đúng.** BARO–V082 và E2–E4 chỉ hỗ trợ mô tả các khác biệt đã nêu. Tôi kiểm một `Point` `http_req_duration` trong `t3-124242f0/raw.json` đã khớp hash, có `time`, `value`, `route`, `routeId`, `status`, `step`. Có thể thiết kế nhãn độc lập mức endpoint ngoại tuyến. Cần quy tắc trước khi chấm, và endpoint chỉ trả lời ở cấp endpoint. |
| CX-15/15b #4 | **Đúng về ba mốc thời gian, phản hồi chưa đủ về đường thực thi và D13.** Mốc `S+2320` là lúc sớm có thể bắt đầu chụp theo giả định đã khai, còn thời điểm phục vụ thực phụ thuộc hàng chờ. Xem điểm 4–5. |
| CX-15/15b #5 | **Đúng, đã sửa bảng RQ5.** Tách tăng/giữ/tụt hạng và kích hoạt thành phần loại được trường hợp hòa mà bị diễn giải hai cách. Không lấy so sánh mức tuyệt đối với dev khác ô làm bằng chứng chuyển giao thành công. |
| CX-15b N1–N3, N5 | **N1 đúng** về mốc lịch và mốc bộ tiêm, nhưng §1 bản 4 còn dùng mốc E5 cũ. **N2 đúng**, lấy giao với phút Grafana thực đánh giá. **N3 đúng** về BARO chỉ xếp hạng, phép kiểm thay thế còn sai ở điểm 6. **N5 đúng**, WHY-17 không cho lấy top-1 của chương trình tác giả làm bằng chứng cho M4 trên FlashTicket. |
| CX-06 #1–6, #10 | Thuộc các đường W4/W5/điều phối. Với #1–2, E4 đã có bảng chấm và 383 phút khỏe được Q2 nhận. Với #3, code hiện hành có nhánh selector B2 rỗng và thiếu mẫu theo container. Với #4, E5 đã có bản ghi cảnh báo thật. Với #5, `81a9273` đi tiếp qua lỗi P7 đã nhận diện. Với #6, Q2 tách nghiệm thu chức năng khỏi phủ metric. Với #10, lịch máy và bản tóm tắt vẫn có thể lệch thời điểm như quan sát đầu báo cáo. Tôi không tái xét các quyết định W4/W5 đã có. |

Đối chiếu dùng bản CX-15 đã phục hồi mã hóa. Kết luận hợp nhất §3 về **bản 3** phù hợp với việc phải sửa thiết kế. Nó chưa giải quyết các phản ví dụ mới của bản 4. [CX-06](D:/RCA-flashticket/results/T-070/codex/CX-06-tin-cuoi.md) · [CX-08](D:/RCA-flashticket/results/T-070/codex/CX-08-tin-cuoi.md) · [CX-15](D:/RCA-flashticket/results/T-070/codex/CX-15-tin-cuoi.md) · [CX-15b](D:/RCA-flashticket/results/T-070/codex/CX-15b-tin-cuoi.md) · [Hợp nhất §3](D:/RCA-flashticket/results/T-070/hop-nhat-cx13-16.md:33)

### Đạt SPEC và quyết định cần Minh

**T-074 đạt phần lập hồ sơ** gồm ma trận, D14 ở hai chế độ, các baseline, dự toán có số, các lựa chọn có trạng thái và một danh sách quyết định. **Chưa đạt phần hồ sơ đủ để phát E6 và khóa thiết kế W7** vì các điểm trên thay đổi quyền máy, khả năng giữ ca, mẫu số hoặc xếp hạng. SPEC T-074 là thiết kế. Chưa có kết quả W7 là đúng phạm vi. [Tiêu chí xong](D:/RCA-flashticket/tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md) · [Yêu cầu gốc §8.3](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:144)

Với **RQ3d**, bản 4 §12 thu hẹp kết luận đúng. Span còn mang định danh và quan hệ cha–con, log/metric còn gắn với thực thể. `DC-bo-quan-he` tắt E1/E2/E5, giữ các đặc trưng và đầu vào còn lại. C-d1 dùng quan hệ gọi giữa nút có cờ. C-d2 xếp theo khởi phát/khóa nút. C-d3 dùng đường có hướng, có trạng thái không đích hoặc chu trình. Phép so trả lời tác dụng của các bước dùng quan hệ đến **xếp hạng trên các ca thu được**. Độ đúng vùng, lợi của topology thật và vai trò đồ thị trong phát báo động vẫn cần bằng chứng riêng. Tôi chưa thấy đường truyền tên ô, root hoặc giờ tiêm vào phương pháp (b) trong thiết kế. Phần rủi ro đã chỉ ra là dùng thông tin sau tiêm để **chọn ca chấm**, một vấn đề khác với rò nhãn vào thuật toán. [RQ3d](D:/RCA-flashticket/docs/MRP.md:82) · [Đối chứng V082](D:/RCA-flashticket/src/m1_ft/thanh_phan/dc_bo_quan_he.py) · [C-d1–d3](D:/RCA-flashticket/src/m1/doi_chung.py:46)

Với **RQ5 và DT18**, A+CPU-EVENT cho bằng chứng vị trí mới về bốn ô được đề xuất. Nó để trống các ô cạnh mạng/dữ liệu mới và chưa đại diện hết lỗi phụ thuộc, bù trừ Saga hoặc tác động khi tải tăng ngay trong một ca lỗi. Đề nghị giữ rõ giới hạn này trong hồ sơ G6. Các lựa chọn W6-A…N đang là WHY đề xuất. Việc chưa ghi chúng vào `docs/WHY.md` ở lượt thiết kế phù hợp với SPEC. Chỉ những lựa chọn Minh chốt mới cần ghi chính thức trước thu. WHY-111 đã ghi rõ phần lý do được bổ sung sau E5. [MRP P10](D:/RCA-flashticket/docs/MRP.md:303) · [DT18-NV2/NV3](D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md) · [WHY-111](D:/RCA-flashticket/docs/WHY.md:1521)

| Câu của Minh | Đề xuất của tôi trong lượt này |
|---|---|
| **1, 8, 12 — DB, giá trị đích, E6** | Chọn **K0** cho đợt đầu. Nó tránh phụ thuộc vào restore đa hệ chưa chứng minh được, đổi lại phải báo DB tích lũy. Giữ ngày đích như ứng viên theo lịch W7 thực. Dùng tồn kho đo ở E6 và ngân sách cả đợt nếu muốn đủ đường quay về K0. **Chưa phát phần sửa DB** theo nháp này. Nếu ưu tiên K2, cần giải quyết điểm 1–2 rồi mới dùng số theo khối. |
| **2, 3 — ô và quota** | Chọn **A+CPU-EVENT** nếu Minh nhận phạm vi RQ5 hẹp. Dòng dùng lại đối chứng là 33 chu kỳ, 17,3 giờ cơ sở, 43.416 đơn theo mô hình. Quota Event cần E6b và làm đổi nền so với W4. Nếu câu quyết định là hiệu quả trên cạnh ở vị trí mới, chọn thêm B và chấp nhận proxy/topology mới. 46.402 là dư theo giả định bảo thủ cũ, chưa phải phép đếm tại E6. [Dự toán `#/phuong_an/2`](D:/RCA-flashticket/results/T-074/du-toan-4.json) |
| **4, 6, 7, 11 — bản che và baseline** | Giữ lỗi đa chuỗi thành trạng thái riêng trong mẫu số, báo cả số lỗi adapter. Chọn M4 + BARO và dùng lại 17 gói dev sau khi có adapter đúng. Mặt trái là so cả đường tích hợp, và thiếu baseline trace/đồ thị độc lập trên FlashTicket. Thêm baseline họ đó khi Minh cần chính kết luận so sánh ấy. |
| **5 — độ trễ và vùng** | Dùng độ trễ theo lịch làm chính, ghi thêm mốc phía đích và loại mốc. Tôi đề xuất làm phần endpoint ngoại tuyến trước W7 nếu muốn báo độ đúng vùng. Dữ liệu k6 đã có, ước lượng của người làm là 0,5–1 ngày phân tích. Nếu chưa chọn, chỉ báo đồ thị con nghi ngờ. |
| **9, 10 — ghép và tải** | Giữ G1 chính/G2 phụ, không kéo dài tải cho đợt cơ sở. Mặt trái là dễ ghép cảnh báo không liên quan và có phần A ngoài lượt tải. Dùng giao thời gian thực của từng ca. Ở ×3, giữ “sự cố trên giờ quan sát đủ điều kiện”, công bố điều kiện nhận phút và ca trước W7. Muốn gọi là báo giả trên giờ khỏe cần định nghĩa khỏe ×3 độc lập. |

### Báo cáo cuối lượt

1. **Đã làm.** Tự soát nguồn, thiết kế kế thừa, code đúng revision và dữ liệu trung gian trước khi đối chiếu các nhận xét trước. Đã lần tới đúng ba mẫu làm H5 bỏ Payment trong N.
2. **File.** Không sửa file nào, không commit, không SSH, không dùng subagent, không mở dữ liệu khóa. Các file bản 4 nằm trong `SHA256SUMS-4`. Nếu Minh duyệt sửa, đề nghị Claude trình bản kế tiếp trong `results/T-074/` và manifest riêng. Đổi tại chỗ sẽ làm lệch hash bản 4. Không có bằng chứng quy cho người làm một thay đổi ngoài phạm vi. Checkout dùng chung có file chưa theo dõi và `STATE` đang thay đổi nên không thể quy tác giả từ `git status`.
3. **Kiểm đã chạy.** `Get-FileHash` khớp T-074 **5/5, 3/3, 4/4, 5/5** và gói ca E5 **58/58**, cùng các mục T-069/T-071/T-072 dùng làm bằng chứng. Tính độc lập bằng PowerShell khớp **8/8** dòng dự toán ở các trường đã nêu. Trên 16 khoảng giữa 17 `load-start` T-069, lấy `S[k+1]−S[k]−1800` được **80,81–97,87 s**, trung bình **85,47 s**. Đây là khoảng suy từ mốc runner và thời lượng tải danh nghĩa. Trong mười phút UTC đầu được gắn với từng lượt E4, cả chín lượt cho **3 `bien`, 7 `khoe_x1`**. Hai phép tính dùng dữ liệu đã lưu, chưa phát lượt pilot. [Sổ T-069](D:/RCA-flashticket/results/T-069/thu/t069-chinh/so.jsonl) · [Phân loại phút E4 `#/phut`](D:/RCA-flashticket/results/T-071/e4/phan-loai-phut.json)
4. **Phần chờ quyết.** Đề nghị Claude đáp các điểm 1–7 và trình phạm vi thay đổi theo file. Minh quyết K0/K2, phạm vi ô và phần endpoint. Khi các điểm về **quyền và đường lui E6** đã được giải quyết, có thể xét riêng việc phát E6 theo Q8/I4. Việc khóa W7 còn phụ thuộc hợp đồng thời gian, đóng gói và chấm baseline. **Đề nghị tiếp tục phản biện**, giữ kết quả chức năng E5 đã nhận và giữ nguyên các bản khóa.

### Prompt bàn giao cho Claude

Minh có thể gửi khối dưới đây cùng nguyên văn nhận xét trên. Khối công đoạn là **người làm đáp phản biện**. Khối trọng tâm dùng đúng khối khóa thiết kế như lượt Minh giao. Phạm vi của lượt bàn giao là trả lời trong chat.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074, tasks/T-074-w6-thiet-ke-danh-gia/, thiết kế W6 bản 4 và nháp SPEC bổ sung E6.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9/P10, W6 chuẩn bị W7, chuẩn bị G6.
- Người làm và người phản biện chính thức: Claude là người làm T-074, Codex là người phản biện.
- Tài liệu gốc: tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; results/T-074/thiet-ke-w6*.md, de-xuat-why*.md, cau-hoi-minh*.md, e6-spec-nhap.md, du-toan-4.json, du_toan_4.py, SHA256SUMS*.
- Phản biện và phản hồi trước: results/T-070/codex/CX-06-tin-cuoi.md, CX-08-tin-cuoi.md, CX-15-tin-cuoi.md, CX-15b-tin-cuoi.md; results/T-070/hop-nhat-cx13-16.md §3; tasks/T-074-w6-thiet-ke-danh-gia/LOG.md; lượt Codex soát bản 4 và các đề xuất trong chat do Minh chuyển kèm.
- Code và kết quả liên quan: tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md, LICH-MAY.md, TRANG-THAI.json; tasks/T-043-thiet-ke-rca-m1/SPEC.md; D:/Project/flashticket-rca-lab tại 407b4f5, ecdeed2 và 81a9273; src/m1/, src/m1_ft/, src/simplerca/, src/p3/; D:/RCA-ext/src/RCAEval tại 259ea41; results/T-069/, results/T-071/e1/, results/T-071/e4/, results/T-072/, results/T-073/e5/ và results/T-073/dap-cx21/, cùng manifest tương ứng.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, chỉ đọc trên laptop, không SSH, không dùng subagent hay agent con.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```