**Đề xuất Minh giữ quyết định ngày 24/11, chưa chọn v2e để tự phân xử độ đầy đủ của lưới, và chưa duyệt nguyên văn WHY-110 §2.** Tôi tái hiện được hai lỗi ngược chiều. V2e có thể chốt **0 sự cố / 3 phút** khi dữ liệu còn cho phép **1 / 3**. V2e cũng có thể trả **“chưa phân xử”** trên lưới đủ. Cả hai lỗi nằm ở bước nhận diện độ phủ, trước quyết định có được dùng tỷ lệ hay không. [Bộ chấm v2e, hàm `luoi_khuyet`](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2e.py:292) · [Quyết định của Minh](D:/RCA-flashticket/docs/DECISIONS.md:794)

**Đề xuất dừng phản biện R5 của E4.** Hồ sơ đã khóa ghi **0 sự cố hệ thống / 383 phút khỏe ×1**. Tôi kiểm trực tiếp chín bản xuất E4. Hợp lưới có 2.868 bước, pha 0, không thiếu bước trong 383 phút khỏe, không có khúc truy vấn lỗi. Tại 7.073 lượt trùng theo cặp luật–thời điểm, tập chuỗi và giá trị nhất quán. Phép kiểm này chỉ đối chiếu đầu vào, không chấm lại E4. [Bảng E4, `#/mau_so`, `#/ty_le_khoe_x1`, `#/ba_nguon`](D:/RCA-flashticket/results/T-072/bang-bao-dong-gia.json) · [Manifest và danh sách bản xuất E4](D:/RCA-flashticket/results/T-072/SHA256SUMS-e4)

### 1. Đã kiểm và phát hiện gì

Tôi nạp tài liệu giả bằng `Du.them()` rồi gọi `cham()` của đúng hai bản đã ghim. Các ca dưới đây dùng ba phút khỏe `[0,180)`, bước 10 giây, `for=60 s`, đầu chấm ở giây 0.

| Mức và bước chịu ảnh hưởng | Phản ví dụ đã chạy | Hậu quả và xử lý tối thiểu |
|---|---|---|
| **CHẶN chọn v2e — thiếu bước ở mép phút khỏe** | Lưới `0,10,…,160`. Tín hiệu đúng từ 110 đến 160. V2e trả `luoi_khuyet=None`, **0/3**. Bổ sung duy nhất bước 170 bằng sai cho **0/3**. Bổ sung bằng đúng cho **1/3**, `t_hat=170`. Hai lịch sử khớp toàn bộ dữ liệu đã thấy. | `day_du` dừng ở bước cuối đã xuất. Phút `[120,180)` chỉ cần một bước để qua phép `any()`. Vì vậy bước 170 mất khỏi cả việc phát hiện lỗ lẫn số đếm riêng. **Cần người làm** nếu Minh muốn dùng v2e tự phân xử. Phần cần sửa là so các bước dự kiến trong phút khỏe trọn với độ phủ thực, kể cả hai mép. [Mã xác định hai biên và phép `any()`](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2e.py:299) |
| **CHẶN bảo đảm giữ v2d khi lưới đủ — lệch pha** | Lưới `6,16,…,176` có đủ sáu bước mỗi phút. Không bước nào vượt ngưỡng. V2d trả **0/3**. V2e trả `su_co=null`, `phut_khoe_x1=null`, đếm **3 phút ngoài lưới** và **0 bước hệ thống khuyết**. Tôi thử đủ các pha nguyên `0…9`. Pha 0 đếm 0 phút ngoài lưới. Từng pha `1…9` đếm 3. | Dòng 309 dò ở giây `0,10,…` tính từ đầu phút UTC. Bộ xuất cho phép chọn giây bắt đầu, và bản xuất E3 thật có `pha_luoi_xuat_s=6`. **Cần người làm** nếu sửa. Dùng pha của lưới xuất để lập các bước dự kiến trong từng phút. Hai lỗi đầu có thể xử lý cùng chỗ, không cần sửa phép liệt kê lỗ của v2d. [Phép dò](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2e.py:309) · [Quy ước lưới `#/mo_phong_offline/luoi_danh_gia`](D:/RCA-flashticket/results/T-072/quy-tac-gom.json) · [Pha E3 `#/pha_luoi_xuat_s`](D:/RCA-flashticket/results/T-072/e3-doi-chieu-offline.json) |
| **CHẶN dùng nhiều bản xuất có quan sát mâu thuẫn** | Hai bản cùng tín hiệu, cùng lưới, không báo lỗi truy vấn. A trả 0, B trả 1 ở từng bước. Nạp A rồi B cho **1/3**, nạp B rồi A cho **0/3**. Cả hai trả `luoi_khuyet=None`. | Phép gán `d[int(t)] = float(v)` lấy giá trị nạp sau. Bản sửa CX-40b xử lý đúng tình huống **một bản lỗi, một bản hợp lệ**. Khi hai bản hợp lệ bất đồng, thứ tự đối số quyết định tử số. **Cần người làm** nếu hỗ trợ đầu vào đó. Xử lý tối thiểu là báo xung đột tại chuỗi và bước liên quan, dừng chốt tỷ lệ. Tôi không tìm thấy xung đột này trong các bản xuất E2/E4 đã đối chiếu. [Chỗ hợp nhất mẫu](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2e.py:64) |
| **KHÔNG CHẶN R5 — báo cáo thiếu dữ liệu quan sát** | Giữ luật hệ thống đủ. Cho riêng luật `quan-sat` lỗi truy vấn ở giây 80. V2e trả `luoi_khuyet=None` và **0/3**. Hàm đã ghi bước đó vào `theo_luat`, rồi trả `None` vì `khuyet_ht` rỗng. | Luật quan sát được gom riêng nên ca này không bác tử số hệ thống. Tuy nhiên, đầu ra làm mất thông tin cần để diễn giải số sự cố quan sát và cờ chồng thời gian. **Cần người làm** nếu dùng phần báo cáo đó. Giữ số khuyết theo luật quan sát kể cả khi tỷ lệ hệ thống vẫn xác định được. [Nhánh trả sớm](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2e.py:301) · [Quy tắc `#/gom_su_co/lop_quan_sat`](D:/RCA-flashticket/results/T-072/quy-tac-gom.json) |

Có thêm một giới hạn đầu vào đáng ghi cùng lỗi độ phủ. Một tài liệu thiếu hẳn khóa tín hiệu hệ thống và một tài liệu có khóa đó với kết quả truy vấn rỗng đều cho **0/3** trong ca giả. Bộ xuất chuẩn tạo khóa ngay cả khi kết quả rỗng. Vì vậy chỉ trường hợp thứ hai có căn cứ áp chính sách `NoData`. Tôi không thấy khóa luật bị bỏ trong các file E2/E4. Nếu nhận file thiếu khóa, xử lý tối thiểu là báo thiếu đầu vào. [Bộ xuất](D:/RCA-flashticket/results/T-072/xuat_tin_hieu.py:22) · [Chỗ mặc định sang tập rỗng](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2e.py:139)

**CHẶN duyệt nguyên văn WHY-110, chỉ ở câu bảo đảm về v2e.** Phần chính đã sửa đúng. Với p95, bảy mẫu đủ và cùng vượt ngưỡng mô tả trạng thái Alerting tại bước đang xét. `t̂` là bước đầu đủ `for` của dãy đó. Phạm vi bảo đảm đã giới hạn vào bước khỏe E2 đủ mẫu. Phần 5xx cũng đúng về điều kiện `≥30` request và điều kiện bổ sung `≥3` lỗi. Phương án tối ưu tỷ lệ trên E2 đã ghi đúng việc khai trước mục tiêu vẫn giữ E4 độc lập. Câu còn vượt bằng chứng là “Khi lưới xuất khuyết, bộ chấm (v2e…) trả ‘chưa phân xử’ và đếm riêng phần khuyết”. Ca mất bước 170 bác trực tiếp câu này. [Chữ trình WHY-110](D:/RCA-flashticket/results/T-072/dap-cx40.md:33) · [Biểu thức 5xx](D:/RCA-flashticket/results/T-072/bieu-thuc.json:431)

**Chữ đề nghị Minh duyệt** cho riêng câu đó là “Theo quyết định ngày 24/11, khi xác định lưới xuất bị khuyết, báo ‘chưa phân xử’ và đếm riêng phần khuyết. Muốn chốt tử số cần lịch sử trạng thái Grafana đủ phủ khoảng liên quan. Mẫu số lấy theo phân loại phút T-071 và đối chiếu thời gian Grafana thực sự đánh giá.” Câu này dùng được ngay cả khi Minh giữ quyết định dừng sửa logic lỗ. Mặt trái là chưa thể giao cho v2e tự quyết đầu vào nào đủ phủ. [Quyết định mục 2–3](D:/RCA-flashticket/docs/DECISIONS.md:794) · [Cách xác định mẫu số đã dùng](D:/RCA-flashticket/results/T-072/bang-bao-dong-gia.json:14)

### 2. File và quyền ghi

**Không sửa file nào.** Tôi tự thực hiện trên laptop, không dùng subagent, không SSH, không commit, không mở dữ liệu khóa. LOG T-070 có giao T-072 làm v2e và trình lại chữ WHY. Các file lượt 15 được kê thuộc `results/T-072/`, LOG task và dòng T-072 trong STATE. Tôi không thấy bằng chứng lượt này đã ghi chữ đề xuất vào `docs/WHY.md`. Trạng thái Git của các đường dẫn liên quan khớp giữa đầu và cuối lượt kiểm. [Giao việc của điều phối](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:393) · [Kết thúc lượt 15](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/LOG.md:453) · [WHY-110 hiện hành](D:/RCA-flashticket/docs/WHY.md:1511)

### 3. Kiểm đã chạy và đối chiếu phản hồi trước

Tôi chạy ba chương trình `thu_ca_gia_v2c.py`, `thu_ca_gia_v2d.py`, `thu_ca_gia_v2e.py` bằng Python 3.12.14 với `-X utf8 -B`, không dùng `--ghi`. Cả ba thoát mã 0, stdout trùng từng byte với biên bản tương ứng. Với v2e, tám ca lưới đủ của người làm khớp v2d ở **ba trường được so** là `ty_le_khoe_x1`, `su_co`, `khoang_chay`. Chúng đều dùng pha 0. Cụm “trùng từng trường” trong LOG rộng hơn phép so thực tế. [Phép so tám ca](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia_v2e.py:51) · [Biên bản v2e](D:/RCA-flashticket/results/T-072/v2/ra/thu-ca-gia-v2e.txt)

| Điểm trước | Kết luận lượt này |
|---|---|
| **CX-33 A, CX-33b D, CX-36 và CX-36b** | **Đúng** về lỗi phút đầu và hai phản ví dụ cho v2c. Ca bắt đầu ở giây 70 cho `0/1` khi Alerting ở 80, `1/1` khi Alerting ở 120. **Claude đúng khi bác kỳ vọng D4 cũ của Codex.** Bước sai ở 120 đặt lại Pending, nhưng khoảng đã cháy `[90,120)` còn có thể ghép với cảnh báo ở 190 theo quy tắc 300 giây. Hai lịch sử cho 0 và 1. [Ca A, D và đối chứng](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia_v2d.py:43) |
| **CX-40 CHẶN 1–2** | **Đúng và đã xử lý trên các ca được nêu.** Với hai ca lỗ dài và ca mất trọn phút ở giữa, v2e trả “chưa phân xử”, bỏ tử số, mẫu số và danh sách tử số khả dĩ. Chính sách bảo thủ này khớp quyết định 24/11, kể cả khi một cách phân tích sâu hơn có thể phân xử một ca cụ thể. **Đúng một phần** đối với tuyên bố tổng quát của phản hồi, do phản ví dụ ở mép phút. [Ca CX-40](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia_v2e.py:72) |
| **CX-40b, hai file chồng và cờ Pending** | **Đúng** trên ca gốc. Một bản có mẫu ở giây 80, bản kia báo lỗi ở 80. Cả hai thứ tự đều cho `[80,90)` và **1/3**. Chỉ giữ file lỗi thì chưa phân xử. Ba ca trước/sau Pending chạy đạt. Phần còn lại là hai quan sát hợp lệ mâu thuẫn như trên. [Ca chồng file và cờ](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia_v2e.py:123) |
| **CX-33 B, CX-40 CHẶN 3, CX-40b mục 3** | **Đúng** về sửa phạm vi p95, phân biệt trạng thái với lần chuyển và đổi tên phương án hiệu chỉnh trên E2. Đầu ra đã khóa cho **0 sự cố, 356 phút khỏe** trên E2. Kết luận R5 dùng E4. Câu bảo đảm về v2e còn bị chặn riêng. [E2 `#/ty_le_khoe_x1`](D:/RCA-flashticket/results/T-072/e2/cham-trong-mau.json) · [Chữ thay thế](D:/RCA-flashticket/results/T-072/dap-cx40.md:33) |
| **CX-33 C, đơn vị Ticket** | **Đúng, đã đính chính.** `1,0424` là kỳ vọng số **cửa sổ 5 phút vượt ngưỡng** trong 72 cửa sổ rời. Tần suất sự cố còn mở vì cùng xác suất biên có thể cho vượt rời rạc hoặc kéo dài. Muốn phân xử phải có chuỗi thời gian ở chế độ tải tương ứng để áp `for=60 s` và ghép 300 s. Bảng xác suất hiện có không cung cấp chuỗi ấy. Chưa có lý do thu thêm chỉ để quyết R5. [Mô hình `#/route/ticket/theo_ty_le/max_luot_x1`](D:/RCA-flashticket/results/T-072/troi-p95-rui-ro.json) · [Đính chính §3](D:/RCA-flashticket/results/T-072/dap-cx40.md:43) |
| **F1–F2 và mức khớp E3** | **Đúng** về giới hạn. Bốn luật thử có một khoảng mỗi phía và một cặp webhook `firing/resolved` mỗi luật. Đếm `#/theo_uid` cho 12 độ lệch bằng −4 s. Mười một luật thật cho 0/0 khoảng. Độ lệch phù hợp với lệch pha. Thiếu thời điểm mẫu trở nên khả dụng ở từng nhịp để tách phần trễ nạp. [Đối chiếu E3](D:/RCA-flashticket/results/T-072/e3-doi-chieu-offline.json) · [Webhook `#/theo_luat`](D:/RCA-flashticket/results/T-072/e3/b9-doi-chieu.json) |
| **Trình tự tự soát, bàn giao và quyền ghi tạm** | **Đúng** về thứ tự lượt 14. LOG ghi đọc CX-36b lúc 18:09Z và tự kiểm lúc 18:11Z. Lượt 15 cũng ghi đọc CX-40/40b ở mục mở lượt, không có mục tự soát độc lập đi trước. Các ca chạy lại vẫn là bằng chứng kỹ thuật. **F6 đúng một phần** vì LOG đã có prompt nhưng `buoc_tiep` của điều phối còn trỏ CX-24b. **K1 đúng** về việc có ghi tạm. **Chưa kiểm được** phê duyệt trước cho thư mục đó từ nguồn được dẫn. Đề xuất ghi đúng giới hạn hồ sơ, không dùng điểm này để mở lại R5 hay B2 của T-071. [LOG lượt 14](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/LOG.md:332) · [Bản đáp K1](D:/RCA-flashticket/results/T-072/dap-cx19.md:25) · [Trạng thái điều phối](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/TRANG-THAI.json:65) |

**KHÔNG CHẶN kết quả chạy lại — JSON tự kiểm dẫn hash mã khác.** Manifest lượt 15 khớp **13/13** file, nhưng `tu-kiem-v2e.json#/dau_vao_sha256` ghi mã chấm bắt đầu `f9dc540e`, còn mã v2e thực tế và biên bản ca giả ghi `13491dd4`. Tôi dừng dùng JSON đó làm bằng chứng cho phiên bản hiện tại. Lần gọi `tu_kiem()` trên mã hiện tại trong bộ ca trả `[]`. Đây là **lỗi hồ sơ nhỏ có thể đính chính cơ học** bằng cách dẫn biên bản đúng hash. Quyền lượt này chỉ cho trả lời trong chat. File JSON, mã chấm và bản đáp đều đã ghim. Ghi đè bất kỳ file nào trong ba file sẽ làm lệch manifest lượt 15. [JSON tự kiểm](D:/RCA-flashticket/results/T-072/v2/ra/tu-kiem-v2e.json) · [Manifest](D:/RCA-flashticket/results/T-072/SHA256SUMS-dap-cx40) · [Biên bản đúng mã](D:/RCA-flashticket/results/T-072/v2/ra/thu-ca-gia-v2e.txt)

Manifest E4 khớp **21/21**, bản đáp CX-33 khớp **10/10**, đối chiếu E3 khớp **6/6**, phân tích Ticket khớp **5/5**. Ở manifest E2 lịch sử, ba file `de-xuat-commit-lab.{md,diff,tsv}` và `sinh_luat_thu_e3.py` hiện khác hash. Trong manifest D1–D4, `ke-hoach-e3.md` hiện khác hash. Tôi loại các bản hiện tại đó khỏi bằng chứng lịch sử. Các đầu ra E2 và các quy tắc dùng cho kết luận trên khớp mục ghim tương ứng. [Manifest E2](D:/RCA-flashticket/results/T-072/SHA256SUMS-e2-nguong) · [Manifest D1–D4](D:/RCA-flashticket/results/T-072/SHA256SUMS-d1-d4)

### 4. Phần đạt, phần còn mở và điều cần Minh quyết

- **SPEC W4.** Có bằng chứng cho ba tiêu chí gốc gồm khai trước quy tắc, thử webhook dương ngoài khoảng chấm và so R5 theo lớp phút trên E4. Bản gom 3 bổ sung cơ cấu E4 trước E4. Tôi không thấy đường đưa nhãn nguyên nhân hoặc thời điểm tiêm vào máy trạng thái cảnh báo. Lớp phút T-071 phục vụ chọn ngưỡng nền và xác định tập phút được chấm. W4 cung cấp bằng chứng báo động giả ở mức hệ thống. Độ nhạy trên ca lỗi, xếp hạng nguyên nhân và lợi ích của đồ thị vẫn phụ thuộc phép đánh giá của các gói tương ứng. [Tiêu chí SPEC](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/SPEC.md) · [MRP §2.3](D:/RCA-flashticket/docs/MRP.md:48) · [Nhiệm vụ DT18](D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md)
- **Cần Minh quyết.** Tôi đề xuất **dừng vòng sửa logic lỗ và giữ v2d cho lưới đã xác định đủ**, theo quyết định hiện hành. Với ca khuyết hoặc nguồn bất đồng, ghi chưa phân xử và đếm riêng. Mặt trái là một số ca có thể phải đối chiếu lịch sử Grafana hoặc để mở nếu lịch sử cũng thiếu. Phương án khác là giao Claude sửa riêng bước kiểm độ phủ và hợp nhất, rồi thử bằng ca giả trên laptop. Các phản ví dụ đã đủ để lựa chọn giữa hai hướng, không cần chạy E2/E4 hay dùng máy từ xa.
- **Cần người làm.** Nếu Minh muốn tiếp tục chọn v2e để tự động chấm lần sau, đề xuất **một lượt đáp hẹp** về hai biên, pha lưới và xung đột bản xuất. Nếu Minh giữ v2d và chấp nhận giới hạn, có thể **dừng phản biện bộ chấm tại đây**. Với WHY-110, đề xuất duyệt phần khoa học đã sửa sau khi thay đúng câu bảo đảm nêu trên. Không có sửa mã nào thuộc loại Codex được phép làm ngay trong lượt chỉ đọc này.

### Prompt bàn giao cho Claude

`docs/review-prompt.md` hiện có các khối G0–G4. Chưa có khối G6 để chép. Dưới đây là Prompt chung và đúng khối “Người làm đáp phản biện”. Minh có thể gửi cùng bản phản biện này. [Nguồn prompt](D:/RCA-flashticket/docs/review-prompt.md:27)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-072, tasks/T-072-w4b-luat-canh-bao/, phản biện kiểm lại lượt 15 do Minh chuyển kèm trong chat.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P10 (W4), chuẩn bị G6.
- Người làm và người phản biện chính thức: Claude là người làm, Codex là người phản biện.
- Tài liệu gốc: tasks/T-072-w4b-luat-canh-bao/SPEC.md và LOG.md, docs/DECISIONS.md khối 24/11 mục 2–3, docs/WHY.md mục WHY-110, results/T-072/quy-tac-gom.json, results/T-072/quy-tac-chon-nguong.json, results/T-072/bieu-thuc.json.
- Phản biện và phản hồi trước: results/T-070/codex/CX-33-tin-cuoi.md, CX-33b-tin-cuoi.md, CX-36-tin-cuoi.md, CX-36b-tin-cuoi.md, CX-40-tin-cuoi.md, CX-40b-tin-cuoi.md trong cùng thư mục; results/T-072/dap-cx19.md, dap-cx33.md, dap-cx40.md; LOG T-072 lượt 13–15; bản phản biện và các đề xuất trong chat do Minh chuyển kèm.
- Code và kết quả liên quan: results/T-072/xuat_tin_hieu.py, results/T-072/v2/, results/T-072/v2/ra/, results/T-072/SHA256SUMS-dap-cx40, results/T-072/SHA256SUMS-dap-cx33, results/T-072/e3-doi-chieu-offline.json, results/T-072/bang-bao-dong-gia.json, results/T-072/troi-p95-rui-ro.json; lệnh ca giả py -3 -X utf8 -B results/T-072/v2/thu_ca_gia_v2e.py.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc trên laptop, không SSH, không dùng subagent hay agent con, không chấm lại E4.

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