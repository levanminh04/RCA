**Đề xuất tiếp tục phản biện một lượt đáp của Claude, chỉ trong chat. Giữ `service-graph-5` và các link Minh đã chọn.** Bản sửa khắc phục các lỗi đã tái hiện về cạnh ngoài `classes`, loại span DB, thiếu gói giữa lô và URL của nút chú thích. Tôi tìm được hai kết luận sai trong hồ sơ nghiệm thu. Một kết luận liên quan trực tiếp đến thông tin người xem nhận được khi bấm nút DB. Kết luận kia nằm trong WHY-101. Cả hai đều phân xử được bằng file hiện có, không cần chạy lại M1.

### 1. Đã làm gì và tìm thấy gì

**F1 — CHẶN dùng “trang DB có bằng chứng cờ M1” làm căn cứ nghiệm thu điểm 4.** Panel 10 đọc `du-lieu/${ban}/vue/${ca}.json`, lọc `bang_chung[thuc_the="${dv}"]`, rồi mới mở các `lien_ket`. Tôi kiểm hash và đếm trên đủ **84 file `vue` lịch sử**. Với năm DB logic `event_db`, `booking_db`, `ticket_db`, `payment_db`, `keycloak_db`, có **0/84 cặp** có `co_m1[].thuc_the` bằng một trong năm tên và **0/84 cặp** có `bang_chung[].thuc_the` như vậy. Có ba liên kết ở thực thể `postgresql-shared-instance`. Kết quả này phân biệt được DB logic với instance. [Truy vấn panel 10 ở revision được kiểm](D:/Project/flashticket-rca-lab/observability/grafana/dashboards/20-incidents/t065-l8b-rca.json:1525) · [Kết luận cần đính chính](D:/RCA-flashticket/results/T-068/kiem/BAO-CAO.md:105)

Phản ví dụ cụ thể là V082/`ebd5ef38`. Cờ mang tên thao tác `SELECT booking_db`, nhưng `thuc_the` là `booking-service`. Người xem chọn `booking_db` sẽ không thấy dòng này ở panel 10. HTTP 200, file trang DB tồn tại và cạnh `booking-service → booking_db` có số span đều có thể đúng cùng lúc với việc bảng cờ của DB rỗng. Tôi không xác định được phép đếm trong chat đã sinh dãy `30/15/14/11/3`. Dù dãy đó đếm đại lượng nào, nó không phải số cặp có dòng khớp bộ lọc của panel. Phản ví dụ nằm trong `#/co_m1`, tra theo `don_vi = "op|booking-service|SELECT booking_db"`. [File ca](D:/RCA-flashticket/results/T-065/may-l11/du-lieu/V082-V066+H8a/ebd5ef38.json) · [Phản hồi của người làm](D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:671)

**Đề xuất tối thiểu:** giữ quyết định “Giữ link” của Minh. Claude nên trình đính chính `BAO-CAO.md` và nối LOG, ghi rõ link mở được trang thực thể, còn bằng chứng gọi DB nằm ở cạnh và ở dịch vụ sở hữu span client. Với `1ad3afeb/booking_db`, file thao tác thực sự có `thao_tac=[]`. Tôi đồng ý để W5 sửa câu giải thích theo loại thực thể. Nếu cần dùng trang này để thuyết trình trước W5, phương án nhẹ hơn là chú thích panel rằng thao tác DB được ghi phía dịch vụ gọi. Sửa bộ xuất và sinh lại file lịch sử sẽ ảnh hưởng hồi quy byte T-066, trong khi đính chính kết luận không cần việc đó. [Trang thao tác của ca](D:/RCA-flashticket/results/T-065/may-l11/du-lieu/V082-V066+H8a/thao-tac-vue/1ad3afeb/booking_db.json) · [Quyết định của Minh](D:/RCA-flashticket/docs/DECISIONS.md:708)

**F2 — CHẶN nhận WHY-101 là giải thích đúng về phương án đã loại.** WHY-101 viết `__khong_co__` chỉ là giá trị của `op` và đặt cho `dv` sẽ gọi file không tồn tại. Chính cặp mà WHY dùng làm ví dụ bác bỏ cả hai vế. Ở P7/`ebd5ef38`, `#/service_options/0/ma` bằng `__khong_co__`. File `thao-tac-vue/ebd5ef38/__khong_co__.json` tồn tại, khớp manifest T-065 và trả thông báo lỗi chạy. Phản hồi trước của Claude cũng từng xác nhận giá trị này thuộc `services` của cặp đó. [WHY-101](D:/RCA-flashticket/docs/WHY.md:1446) · [Đầu vào thật của biến `dv`](D:/RCA-flashticket/results/T-065/may-l11/du-lieu/p7/vue/ebd5ef38.json) · [File đích](D:/RCA-flashticket/results/T-065/may-l11/du-lieu/p7/thao-tac-vue/ebd5ef38/__khong_co__.json) · [Xác nhận trước](D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:240)

Bản sửa URL vẫn có căn cứ. `dv=` là chuỗi rỗng và có thể tạo đường dẫn `.../.json`. Bỏ hai biến cho Grafana chọn giá trị hợp lệ của đúng bản–ca. Hai URL v5 đã kiểm đều giữ bản, ca, cửa sổ và panel 3. **Đề xuất** sửa riêng lý do trong WHY-101 thành “bỏ biến để dùng lựa chọn mặc định của từng ca, tránh gắn cứng giá trị đặc biệt của P7”. Giữ nguyên code và quyết định giao diện. [Hai URL đã sinh](D:/RCA-flashticket/results/T-068/a/service-graph-5/p7/ebd5ef38.json)

**F3 — CHẶN duyệt đề xuất “chép danh sách hash và kết quả kiểm rồi xóa phần còn lại” như đang viết.** `service-graph-4-bak/` là bản dùng để hoàn tác. JSON kiểm riêng cho cặp thứ 85 được dẫn bằng đường trên exp-obs. Danh sách hash xác minh được một bản sao, nhưng không khôi phục được nội dung đã xóa. Ước lượng “vài chục MB” cũng không bao phủ cả hai thư mục. Hồ sơ trước ghi riêng `t068-thu` khoảng 385 MiB, gồm hai bản sao `du-lieu`. Đây là vấn đề của **đề xuất dọn**, chưa có bằng chứng việc xóa đã xảy ra. [Đề xuất ngày 19/11](D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:757) · [Bản sao và đường hoàn tác](D:/RCA-flashticket/results/T-068/thay-doi-may.md:37) · [Phạm vi thư mục thử ban đầu](D:/RCA-flashticket/results/T-068/thay-doi-may.md:5)

**Đề xuất** giữ hai thư mục ở lượt này. Nếu Minh cần thu hồi dung lượng, Claude có thể trình riêng phần tải trung chuyển đã xác nhận trùng byte, vị trí giữ nội dung hoàn tác và hồ sơ các lượt hỏng. Lần được phép đọc máy, `du -sh` trên hai thư mục và chép về JSON kiểm v5 của `7ffb2305` là đủ để phân xử dung lượng và hoàn thiện chứng cứ laptop. Chi phí là một lần đọc metadata và một file kết quả nhỏ. Nghiệm thu phần hiển thị không phụ thuộc việc dọn.

**F4 — KHÔNG CHẶN đồ thị hiện có. Cần thu hẹp ba cam kết kỹ thuật.**

| Cam kết | Mã và bằng chứng thực sự hỗ trợ |
|---|---|
| `--tat-ca` gặp bất kỳ lỗi nào cũng không ghi file | Thiếu gói, sai hash và lỗi dựng xảy ra trước vòng ghi. Đối chứng 10a/10b có `file_ghi=[]`. Sau đó `write_graphs` thay từng JSON và từng status. Lỗi đĩa giữa vòng này có thể để lại một phần lô. Tương tự, `sau_v082` thay được đồ thị cũ khi nạp được module và ghi được file lỗi. Code có nhánh riêng khi chính việc ghi file lỗi thất bại. Đây là giới hạn hạ tầng, chưa thấy xảy ra ở lô đã phục vụ. [Bộ dựng](D:/Project/flashticket-rca-lab/campaigns/g1/service_graph.py:382) · [Đối chứng](D:/RCA-flashticket/results/T-068/a/doi-chung-am-2.json) |
| WHY-100 nói đổi quy tắc cửa sổ thì kiểm chéo sẽ dừng | Kiểm chéo dừng khi tổng quan hệ theo chủ, pha hoặc tổng cùng chủ thay đổi. Nếu thay đổi chỉ đưa vào hoặc loại một span DB không có quan hệ cha–con trong cửa sổ, các tổng được so có thể giữ nguyên. Mục 6 của đối chứng chứng minh một lần dịch cửa sổ bị phát hiện. [WHY-100](D:/RCA-flashticket/docs/WHY.md:1439) · [Điều kiện dừng](D:/Project/flashticket-rca-lab/campaigns/g1/service_graph.py:268) |
| `span_khong_ve` là số span phân biệt không vẽ được | Trong chính đối chứng 8/9, một span của `x` đóng góp hai lần, một lần cho chủ ngoài `classes` và một lần cho quan hệ `a → x`. Cộng thêm span DB loại SERVER cho kết quả 3 lượt lý do trên 2 span liên quan. Các dòng lý do riêng vẫn đúng. Không dùng tổng này làm số span duy nhất hoặc tỷ lệ mất trace. [Đối chứng, `#/muc/8_db_kind_server/chi_tiet`](D:/RCA-flashticket/results/T-068/a/doi-chung-am-2.json) · [Phép cộng](D:/Project/flashticket-rca-lab/campaigns/g1/service_graph.py:343) |

Tôi đề xuất làm rõ phạm vi cam kết trong tài liệu khi Minh duyệt đính chính. Bằng chứng hiện tại không đòi cơ chế ghi giao dịch cho cả lô hoặc sinh lại 85 đồ thị.

**F5 — KHÔNG CHẶN nghiệm thu kỹ thuật, ảnh hưởng bàn giao.** Dòng T-068 trong STATE vẫn yêu cầu Minh duyệt WHY-100/101, DECISIONS và commit. Commit `3874f34` đã chứa các mục đó. LOG sau commit ghi Minh đã duyệt và commit đã push. Phần đang chờ là phản hồi lượt kiểm và quyết định nghiệm thu. Đề xuất chỉ cập nhật dòng T-068 khi Minh duyệt. `docs/WHY.md` và `docs/STATE.md` từng được băm trong snapshot T-020 tại một commit cũ. Sửa tài liệu hiện hành sẽ đổi hash hiện hành. Giữ nguyên snapshot lịch sử và các manifest T-065/T-066. [STATE](D:/RCA-flashticket/docs/STATE.md:19) · [LOG sau commit](D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:750) · [Manifest lịch sử](D:/RCA-flashticket/results/T-020/manifest.json:34)

### 2. File đã thay đổi

**Không sửa file nào.** Tôi tự thực hiện lượt kiểm trong vai trò Codex phản biện. Không dùng agent con, không SSH, không mở dữ liệu khóa, không chạy thực nghiệm mới, không commit. Đầu ra của lượt này chỉ ở chat.

### 3. Kiểm đã chạy và kết quả

| Phạm vi | Kết quả độc lập |
|---|---|
| Nguồn trace | Băm lại **28/28** nguồn lịch sử trên laptop, đối chiếu theo manifest T-062, chuỗi `manifest-2.json → SHA256SUMS` của T-063 hoặc danh sách archive tương ứng. Băm phía nguồn **71/71** file của 26 gói trong `trace-goi.sha256`. Hash `ca-manifest.json` của `7ffb2305` khớp `e2e-001/SHA256SUMS`. Raw trace và đồ thị v5 riêng của ca này ở exp-obs. [Bản đồ nguồn](D:/RCA-flashticket/results/T-068/a/nguon-trace.json) · [Danh sách chuyển](D:/RCA-flashticket/results/T-068/trace-goi.sha256) · [Manifest ca thứ 29](D:/RCA-flashticket/results/T-066/e2e-001/ca-manifest.json) |
| 84 cặp lịch sử | **168/168** JSON đồ thị và status v5 khớp `sg5-laptop.sha256`. Đối chiếu `nguon_file_sha256` với file ca và manifest T-065 đạt **84/84**. So v4 với v5 trên đủ 168 file, khác đúng 168 giá trị phiên bản và hai URL chú thích của P7/`ebd5ef38`. P7 có **27 OK, 1 LOI_CHAY**. `status=ok` của bộ dựng ở cặp lỗi chỉ có nghĩa đã dựng được hình chú thích. [Hash v5](D:/RCA-flashticket/results/T-068/a/sg5-laptop.sha256) · [Hash v4](D:/RCA-flashticket/results/T-068/a/sg4-laptop.sha256) |
| Cạnh, nút, hạng | Đếm lại **1.386** cạnh cha–con, **664** cạnh DB, **168 gửi + 168 nhận**. Trên 83 cặp có đầu ra, đối chiếu lại **1.000/1.000** cạnh DB/RabbitMQ theo loại, hai đầu và tổng N+A với bảng rà trace từng ca, không có lệch. Kiểm đầu cạnh, thành viên nút dữ liệu, hạng và màu theo file ca không thấy sai. Có 27 cặp mang ghi chú thiếu RabbitMQ. [Đầu ra kiểm, `#/tong`](D:/RCA-flashticket/results/T-068/kiem/dem-doc-lap-v5-laptop-2.json) · [Trung gian trace](D:/RCA-flashticket/results/T-068/a/ra-soat) |
| Hồi quy có ý nghĩa cho demo | V082/`ebd5ef38` có **35** kênh cờ của `payment-service`. V071 có **24** cạnh xếp hạng phương pháp. Với `1ad3afeb`, `keycloak` là hạng 2 `tu_sinh` ở P7 và hạng 3 `binh_thuong` ở V071/V082. Đây là hạng có sẵn trong đầu ra phương pháp. [File ca lịch sử](D:/RCA-flashticket/results/T-065/may-l11/du-lieu) · [Đồ thị v5](D:/RCA-flashticket/results/T-068/a/service-graph-5) |
| Dashboard và tiêu chí SPEC 1, 4, 5 | Có bốn provider. Sáu JSON lưu trữ không đổi từ `ab1c52c` tới `ee91432`. So cấu trúc đủ **23 panel cũ** của trang sự cố, 19 panel dịch `y` thêm 42, bốn panel giữ vị trí, nội dung cũ khớp. Trang phát lại chỉ khác `title`, `tags`. Snapshot trước có **9 UID từ file + 2 UID tạo tay**, hai bản xuất tạo tay khớp SHA. Ở thời điểm đã lưu trong cửa sổ `7ffb2305`, lượng gọi có **7** chuỗi, p90 có **7**, truy vấn 5xx thô có **1**, `api-gateway = 0,26/s`. Dữ liệu hỗ trợ tiêu chí có cả ba tín hiệu. Trạng thái API sau xóa và kết quả bấm thật là quan sát lịch sử. Lượt này không có tunnel đang nghe ở cổng 3000. [Snapshot UID](D:/RCA-flashticket/results/T-068/truoc/grafana-truoc.json) · [Số liệu, `#/app_rps`, `#/app_p90`, `#/app_5xx`](D:/RCA-flashticket/results/T-068/truoc/prometheus-ca-7ffb2305.json) |
| Toàn vẹn và phạm vi | Trong danh sách trước sửa, **2.143** dòng đối chiếu T-065 và **5** dòng đối chiếu T-066 khớp. So danh sách trước/sau có hai file đổi hash và hai `.bak-t066` thêm đúng tên. Bốn mốc `a-truoc`, `a-sau`, `p3-truoc`, `p3-sau` trùng byte, gồm **200** dòng bảo vệ và **2.184** dòng `du-lieu`. Diff lab `6a0def7..ee91432` có ba file thuộc phạm vi đã duyệt. Vị trí bổ sung `trace-goi/` có quyết định riêng. Việc ghi `t068-thu` ban đầu ngoài phạm vi đã được Minh ghi nhận. LOG còn ghi các lượt thử ở `scratchpad` laptop ngoài các đường ghi liệt kê trong SPEC. Tôi không có nguyên văn đề xuất tám bước để xác nhận quyền riêng cho vị trí đó. [Mốc trước](D:/RCA-flashticket/results/T-068/p3-truoc.sha256) · [Mốc sau](D:/RCA-flashticket/results/T-068/p3-sau.sha256) · [Nhật ký thử](D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:653) |

**Đối chiếu phản hồi các lượt trước**

| Điểm | Kết luận lượt này |
|---|---|
| A1 — `classes`, loại span DB | **Đúng** về lỗi v4. V5 kiểm hai chủ của cạnh cha–con và chỉ vẽ DB CLIENT. Trung gian của 29 ca ghi mọi span DB quan sát được có kind 3. Mục 8/9 phân xử hai nhánh không xuất hiện trong dữ liệu thật. Cam kết về mọi nút vẫn phụ thuộc `ranking_rows` nhất quán với `classes`, vì `build()` thêm thẳng thực thể có hạng. Trên 84 file lịch sử không thấy vi phạm. |
| A2 — `--tat-ca` ghi trước khi gặp gói thiếu | **Đúng, đã sửa** cho lỗi nguồn và lỗi dựng. `10a`, `10b` ghi 0 file. `10c` ghi đủ 4 file. Giới hạn đối với lỗi ghi nằm ở F4. |
| A3 — lệnh hoàn tác | **Đúng, đã đính chính.** V3 có thể dựng từ file ca. V4/v5 cần `--goi`, và `.tgz` cần hash ngoài. Có chỉ dẫn sao lưu, checkout đúng revision và lưu ý runner khi hoàn tác nhãn. Khả năng chạy `--tat-ca` cho toàn bộ chỉ mục trực tiếp trên exp-obs vẫn mới có bằng chứng về nguồn và đường code. |
| A4 — link hạ tầng và link chú thích | **Đúng một phần.** Link DB có đích thật. Hai link chú thích v5 đúng cửa sổ, và đối chứng 11/12 bắt mất URL hoặc thêm `var-dv=`. Phản bác việc phải bỏ link là hợp lý. Lý do về cờ DB và phương án `dv` đặc biệt sai theo F1/F2. |
| A5 — đồ thị cũ sau lỗi | **Đúng, đã sửa cho nhánh đã thử.** Sau lỗi dựng, runner gọi `error_graph` rồi ghi status. LOG ghi thử gói thiếu và phục hồi được hash cũ. Lỗi nạp module hoặc lỗi ghi có giới hạn ở F4. |
| A6 — JSON đối chứng và mã thoát | **Đúng.** File v1 còn dòng `DAT` ngoài JSON, script cũ chỉ in trạng thái. File v2 phân tích được, có **16/16 mục `dat=true`** gồm cả đối chứng dương. Script v2 trả mã 1 khi không đạt. [Kết quả đối chứng](D:/RCA-flashticket/results/T-068/a/doi-chung-am-2.json) |
| A7 — p95, CRLF và lượt hỏng | **Đúng.** Tính lại với `n=1…99.999` cho 0 chênh lệch giữa hai công thức hạng p95 đã nêu. Sáu hash sau đổi LF khớp bảng LOG. Chuyển sang số nguyên không chứng minh đã sửa một giá trị p95 sai. Lượt hỏng đã xóa không có bản sao theo LOG. Việc ghi nhận vi phạm bảo toàn kết quả và việc WHY được bổ sung sau sử dụng không khôi phục được thứ tự lịch sử. |
| A8 — vị trí gói | **Đúng phía nguồn laptop.** Danh sách 26 gói, 71 file khớp byte. Việc chép tới exp-obs và hai gói đã có sẵn ở đó được ghi nhận lịch sử. Tôi không xác nhận lại ổ đĩa máy chủ trong lượt này. |
| Lỗi 400 và thời gian tải | **Đúng một phần.** Biến phát truy vấn `.../${dv}.json` là `op`. Link chú thích v5 bỏ `dv` rỗng. Kết quả HTTP 200 ở lần bấm ngày 19/11 phù hợp với mã. Nguyên nhân đầy đủ của độ trễ cũ chưa phân xử được giữa trạng thái pane, khởi động trình duyệt và thời gian truy vấn. Bảng đo mỗi ô một lần, không có cặp ẩn/hiện cùng điều kiện. Đề xuất giữ số đo lịch sử và bỏ quy nguyên nhân. Chỉ cần đo ghép cặp nếu Minh cần quyết định tối ưu giao diện. |
| R1–R6 trước phương án A | **R1, R2, R3, R5, R6 đúng** trong phạm vi lịch sử đã ghi. Link cạnh đã bỏ, ví dụ provider đã sửa, Minh đã ghi nhận `t068-thu`, điều kiện `classes` và hướng dẫn hoàn tác đã bổ sung. R2 chưa được thử bằng cách nạp lại sáu dashboard. **R4 đúng:** có ba nhánh xuất theo hai quy ước, trong đó trường đích đã xuất làm mất `db.name`. Trace gốc còn giữ tên DB. WHY-100 nên phân biệt số **toàn gói** `190.917/201.743` với số **trong cửa sổ** `96.299/101.689` của `7ffb2305`. [Trung gian, `#/so_span_co_khoa`](D:/RCA-flashticket/results/T-068/a/ra-soat/7ffb2305.json) · [Đính chính ba nhánh](D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:238) |

### 4. Phần còn mở và điều cần Minh quyết

- **Nghiệm thu T-068.** Đề xuất giữ bản lab `ee91432`, giữ link và cho Claude đáp F1/F2 trước khi chốt hồ sơ. Bản thân đồ thị lịch sử đã qua các phép kiểm nêu trên. Ca thứ 85 có manifest gốc và trung gian rà soát trên laptop, còn JSON kiểm v5 và đồ thị phục vụ nằm trên máy. Kết quả **84/84 tôi đối chiếu tại laptop** và **1/1 người làm ghi nhận trên exp-obs** cần được báo đúng nguồn. `kiem/dem-doc-lap-may.json` là kết quả bản cũ, không thay cho JSON v5 của ca này.
- **Dọn máy.** Đề xuất chưa duyệt xóa theo mô tả hiện tại. Giữ bản hoàn tác có chi phí đĩa, nhưng tránh mất nội dung mà một danh sách hash không dựng lại được. Nếu cần dọn, xử lý riêng các bản chuyển trùng sau khi xác định bản nào còn dùng.
- **Phạm vi khoa học.** DT18 yêu cầu đồ thị phụ thuộc và giao diện minh họa. T-068 cung cấp phần hiển thị quan hệ quan sát và hạng của bản đã chọn. Theo đường code, trace tạo cạnh cho panel, còn `ranking_rows` cung cấp màu và hạng sau khi phương pháp đã chạy. Tôi không thấy đường đưa nhãn đáp án hoặc cạnh hiển thị ngược vào điểm, tập ứng viên hay xếp hạng. T-068 không có phép so sánh bỏ đồ thị và không cung cấp bằng chứng mới về lợi ích quan hệ, RQ5 hay toàn bộ G6. Không có căn cứ yêu cầu chạy lại benchmark cho hai đính chính này. [SPEC](D:/RCA-flashticket/tasks/T-068-don-grafana/SPEC.md) · [MRP P10](D:/RCA-flashticket/docs/MRP.md:303)

**Bất đồng còn lại với Claude** là căn cứ thực tế của điểm 4, lý do loại phương án trong WHY-101 và phạm vi có thể xóa sau nghiệm thu. Tôi đề xuất tiếp tục đúng một lượt đáp trên các bằng chứng này. Minh quyết việc sửa, dừng hay nghiệm thu.

### Prompt bàn giao cho Claude

Mẫu hiện có khối cổng đến G4, chưa có khối G6. Dưới đây là Prompt chung và khối **Người làm đáp phản biện**. [Mẫu gốc](D:/RCA-flashticket/docs/review-prompt.md)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md, gồm mục bổ sung đã duyệt ngày 18/11; repo lab D:/Project/flashticket-rca-lab, git diff 8dccb34..ee91432 -- campaigns observability, git diff 6a0def7..ee91432 và git diff ab1c52c..ee91432 -- observability/grafana; repo RCA commit 3874f34 và phần LOG sau commit.
- Phản biện và phản hồi trước: các lượt trong chat ngày 18/11; tasks/T-068-don-grafana/LOG.md theo thứ tự phiên; results/T-068/kiem/BAO-CAO.md; phần còn mở và đề xuất của người làm ngày 19/11 ở LOG; lượt kiểm lại cùng các đề xuất của Codex ngày 22/11 do Minh chuyển kèm, đầu ra phiên điều phối ở results/T-070/codex/CX-14.jsonl.
- Code và kết quả liên quan: results/T-068/; results/T-065/manifest.json, may-l11/, xuat-du-lieu.mjs, l4-raw.mjs; results/T-062/manifest.json; results/T-063/manifest-2.json; D:/RCA-archive/hash-lists/exp-obs-cases.sha256; results/T-066/e2e-001/ và results/T-066/bao-ve.tsv; repo lab ở ee91432, campaigns/g1/service_graph.py, campaigns/g1/l8b-xuat.py, campaigns/runner/sau_v082.py và observability/grafana/; môi trường chỉ đọc, không SSH, không dùng subagent.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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