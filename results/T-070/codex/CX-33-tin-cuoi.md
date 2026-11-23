**Giữ kết quả R5 Minh đã nhận theo Q2.** Trên E4 có **0 sự cố hệ thống trong 383 phút khỏe ×1**. Khoảng tin cậy Poisson 95% là **[0; 3,47] sự cố mỗi 6 giờ khỏe ×1**. Lịch sử Grafana, webhook và đầu ra ngoại tuyến nhất quán ở phép đếm này. Tử số, mẫu số và tiêu chí chấp nhận đều có trong hồ sơ đã khóa. [Bảng R5, `#/mau_so` và `#/ty_le_khoe_x1`](D:/RCA-flashticket/results/T-072/bang-bao-dong-gia.json) · [Đối chiếu lúc chấm](D:/RCA-flashticket/results/T-072/e4/k2-grafana-luc-cham.txt:7) · [Quyết định Q2](D:/RCA-flashticket/docs/DECISIONS.md:775)

**Đề xuất tiếp tục một lượt đáp hẹp trước khi chọn bộ chấm v2 và duyệt chữ WHY-110.** Tôi tái hiện được một lỗi tử số–mẫu số của v2 và tìm được phản ví dụ ngay trong E2 cho một câu của bản nháp WHY. Cả hai xử lý được trên laptop. Không cần phát lại E2–E4.

## 1. Đã làm gì và phát hiện gì

### A. CHẶN chọn `v2_claude` để chấm khoảng có sự cố ở phút đầu

`quy_ve()` đếm sự cố theo phút chứa thời điểm vào Alerting, ký hiệu t̂. Nhưng `cham()` chỉ đưa vào mẫu số các phút có **đầu phút** từ `bat_dau` trở đi. Khi `bat_dau` nằm giữa một phút khỏe, sự cố ở phần còn lại của phút đó có thể vào tử số dù chính phút đó đã bị bỏ khỏi mẫu số. Ca tự kiểm mẫu số dùng `bat_dau=1200`, đúng biên phút, và không có sự cố. [Quy lớp sự cố](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2_claude.py:190) · [Tử số và mẫu số](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2_claude.py:235) · [Ca tự kiểm](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2_claude.py:352)

Tôi gọi trực tiếp `cham()` trong bộ nhớ với ba phút khỏe `[0,180)`, bước 10 giây, `bat_dau=70`, Pending ở giây 20, Alerting ở giây 80 và hết ở giây 100. Kết quả thực là `su_co=1`, `phut_khoe_x1=1`, `moi_6_gio=360`. Phút duy nhất trong mẫu số là `[120,180)`. Sự cố lại nằm trong `[60,120)`. Đây là lỗi đã tái hiện. Ở E4, giờ hiệu lực `06:06:10Z` nằm trước toàn bộ các phút được phân loại, nên lỗi này không đổi số **0/383**. [Quy tắc tử số và mẫu số](D:/RCA-flashticket/results/T-072/quy-tac-gom.json) · [Cửa sổ E4, `#/tom_tat/cua_so`](D:/RCA-flashticket/results/T-071/e4/phan-loai-phut.json)

**Đề xuất cho Minh:** giữ đơn vị phút khỏe trọn. Dùng cùng một tập phút đủ điều kiện cho cả tử số và mẫu số R5. Sự cố ở phần phút đầu vẫn xuất hiện trong danh sách với t̂ và lớp gốc. Mặt trái là bỏ phần quan sát chưa tròn một phút khỏi tỷ lệ. Phương án tính theo số giây phơi nhiễm giữ được phần đó nhưng đổi đơn vị của giao thức đã khóa. Đề nghị Claude trình cách xử lý trước khi dùng cho lần chấm sau. `cham_offline_v2_claude.py`, script sinh nó và bản đáp đều đã ghim trong `SHA256SUMS-dap-cx19`. Nếu Minh duyệt sửa, nên lập bản kế tiếp để còn tái hiện được lượt 13. [Manifest lượt 13](D:/RCA-flashticket/results/T-072/SHA256SUMS-dap-cx19) · [Phạm vi đã duyệt, mục 5.2](D:/RCA-flashticket/results/T-070/de-xuat-quyet-2026-11-23-ban5.md:12)

### B. CHẶN duyệt nguyên văn WHY-110 về bảo đảm của ngưỡng p95

`dap-cx19.md` §2 nói mệnh đề “khi và chỉ khi” đúng cho p95 **trên E2**. Chữ đề nghị ở §4 vẫn dùng phạm vi đó. Trong khi ấy, `M` chỉ lấy trên các bước có **phút kết thúc cửa sổ thuộc lớp khỏe ×1**. Chính định nghĩa `M` và phần “Chọn gì” của WHY-110 đã ghi điều kiện này. Lỗi nằm ở chỗ bỏ điều kiện khi rút ra kết luận. [Bản đáp, §2](D:/RCA-flashticket/results/T-072/dap-cx19.md:20) · [Định nghĩa `M`, `#/thong_ke/M`](D:/RCA-flashticket/results/T-072/quy-tac-chon-nguong.json) · [WHY-110](D:/RCA-flashticket/docs/WHY.md:1511)

Booking cho phản ví dụ trên dữ liệu thật. `M` khỏe ×1 là `0,047481884 s`. Xét ngưỡng minh họa `0,050 s`, cao hơn `M`. Tại `18:21:50Z` ngày 20/11, thuộc phút flash, giá trị **nhỏ nhất** của bảy mẫu Booking từ `t−60` đến `t` là `0,050750 s`. Điều kiện vượt ngưỡng đã duy trì đủ 60 giây. Ngưỡng triển khai thực tế là `0,098 s`; phản ví dụ kiểm mệnh đề tổng quát, không thay kết quả đã chạy. [Giá trị `#/chi_tiet/theta_p95_booking/M` và `#/nguong/theta_p95_booking`](D:/RCA-flashticket/results/T-072/nguong.json) · [Chuỗi Booking của lượt flash E2-04](D:/RCA-flashticket/results/T-072/e2/xuat/t071-e2-04-fl.t072.json) · [Lớp phút E2](D:/RCA-flashticket/results/T-072/e2/phut.json)

**Chữ đề nghị:** “Trên các bước E2 có phút thuộc lớp khỏe ×1 và đủ mẫu trong cửa sổ `for`, θ ≥ M bảo đảm p95 không vượt θ liên tục suốt cửa sổ kết thúc ở bước đó. Số sự cố trên toàn E2 được xác định bằng chạy bộ chấm với ngưỡng đã chọn.” Với 5xx, Claude đúng khi rút điều kiện **cần**. Cần sửa thêm chi tiết đầu vào: chuỗi dùng tính `M` **đã chặn ≥30 request**. Chặn bổ sung của luật thật là `≥3` lỗi 5xx. Ví dụ 2 lỗi trên 32 request vẫn đứng vững. Sửa diễn giải trong hồ sơ, giữ bản JSON đã khóa. [Biểu thức tính tỷ lệ dùng chọn ngưỡng](D:/RCA-flashticket/results/T-072/bieu-thuc.json:431) · [Kết quả đã chấm trong mẫu](D:/RCA-flashticket/results/T-072/e2/cham-trong-mau.json)

### C. KHÔNG CHẶN R5 — số cửa sổ vượt ngưỡng của Ticket đang được đem so với số sự cố

Mô hình tính `72 × P(cửa sổ 5 phút vượt θ)`. Ở tỷ lệ chậm cao nhất, đầu ra là **1,0424 cửa sổ vượt mỗi 6 giờ**. Script không mô phỏng điều kiện duy trì 60 giây trên lưới trượt, cũng không gom các lần cháy cách nhau tối đa 300 giây. Vì vậy câu “chạm ngưỡng R5” và cách ghi “rủi ro ≈ 1/6 giờ” trong STATE có thể làm người đọc hiểu sai đại lượng. Bảng nguồn gọi đúng là *số cửa sổ vượt* và đã nêu giả định Poisson. Sai lệch xuất hiện khi chuyển từ bảng sang kết luận. [Công thức mô hình](D:/RCA-flashticket/results/T-072/troi_p95_rui_ro.py:23) · [Đầu ra `#/route/ticket/theo_ty_le/max_luot_x1`](D:/RCA-flashticket/results/T-072/troi-p95-rui-ro.json) · [Câu so với R5](D:/RCA-flashticket/results/T-072/troi-p95-e2-e4.md:67)

**Đề xuất:** trong chữ trình WHY và khi dẫn kết quả vào hồ sơ G6, ghi “với 72 request/5 phút và giả định bucket của mô hình, 4 request chậm đủ làm **p95 của một cửa sổ** vượt `0,112 s`”. Giữ số 1,0424 ở đơn vị cửa sổ. Muốn ước lượng số sự cố ở chế độ tải đó phải có diễn biến theo thời gian đủ để áp `for` và quy tắc gom. Bảng xác suất biên hiện có không phân biệt được các cửa sổ vượt rời rạc với một đợt kéo dài. Bản phân tích cũ đã ghim trong `SHA256SUMS-troi-p95`; một đính chính dẫn nguồn đủ cho hồ sơ W4. [Giả định mô hình](D:/RCA-flashticket/results/T-072/troi_p95_rui_ro.py:3) · [Manifest phân tích](D:/RCA-flashticket/results/T-072/SHA256SUMS-troi-p95)

### Đối chiếu từng ý của các lượt trước

| Điểm | Kết luận sau kiểm lại |
|---|---|
| **F1 · CX-25/25b, giờ hiệu lực** | **Đúng.** Nhịp đầu là `06:06:00Z`, kiểm tra sức khỏe thành công lúc `06:06:01Z`. Nhóm 10 giây đầu nằm trọn sau đó bắt đầu lúc `06:06:10Z`, có 11 truy vấn. Bản đính chính giữ đúng giới hạn của log tổng hợp. Dùng mốc này trong hồ sơ dẫn xuất. [Log Grafana](D:/RCA-flashticket/results/T-072/e3/b10-restart-g.txt:14) · [Đính chính T-072](D:/RCA-flashticket/results/T-072/dinh-chinh-cx19-co-hoc.md) |
| **F2, độ khớp ngoại tuyến–Grafana** | **Đúng.** Tôi đếm theo từng UID. Bốn luật thử đều có 1/1 khoảng cháy, cả 12 hiệu Pending, Alerting và kết thúc đều là −4 giây. Mười một luật thật đều 0/0. Booking đạt cực đại `0,093125 s`, dưới ngưỡng thật `0,098 s`. Không thể tách chênh pha khỏi trễ nạp nếu thiếu thời điểm mẫu khả dụng ở từng nhịp. Để trả lời riêng câu hỏi cơ chế mới cần ghi đồng thời hai thời điểm trong một lượt được duyệt. R5 đã có lịch sử Grafana trực tiếp. [Đối chiếu `#/theo_uid`](D:/RCA-flashticket/results/T-072/e3-doi-chieu-offline.json) · [Chuỗi E3](D:/RCA-flashticket/results/T-071/e3/xuat-tin-hieu.json) |
| **F3, hai phương án ngưỡng** | **Đúng một phần như phản hồi của Claude.** Chọn trên E2 theo mục tiêu khai trước vẫn giữ E4 độc lập. Một bước vượt phân vị chưa đủ sinh sự cố sau `for`. Nếu viện dẫn phương án chọn theo R5, nên gọi đúng là dùng *mục tiêu tỷ lệ* khi hiệu chỉnh. E2 chỉ có 356 phút khỏe, dưới yêu cầu 360 phút để kết luận R5. Lỗi phạm vi còn lại ở điểm B. [Bản đáp §4](D:/RCA-flashticket/results/T-072/dap-cx19.md:38) · [E2, `#/ty_le_khoe_x1`](D:/RCA-flashticket/results/T-072/e2/cham-trong-mau.json) |
| **F4 · CX-25/25b, B2** | **Đúng.** Đọc thành viên trong hai gói gốc cho cùng 12 tên có chuỗi restart. Mọi giá trị đã lưu của 12 tên đều bằng 0. Collector vắng ở cả hai tập, phù hợp `excluded_images` tại commit lab `407b4f5`. `OOMKilled` đọc từ trạng thái k6 theo lượt. Tôi đồng ý kết thúc phần phản biện B2 của T-071. [Đính chính T-071](D:/RCA-flashticket/results/T-071/dinh-chinh-cx19-co-hoc.md) · [Cách lập tập B2](D:/RCA-flashticket/results/T-071/phan_loai_phut.py:117) |
| **F5 · CX-24/24b, ba nhánh của bộ chấm** | **Đúng về ba lỗi gốc, đúng một phần về mức đã sửa.** Nhánh `<8` và cờ giao hai khoảng nửa mở đạt các ca kỹ thuật. Claude đã sửa việc đồng nhất Pending ở đầu lưới với sự cố cháy trước đầu khoảng. Điểm A vẫn chặn tái sử dụng. Nhận xét của CX-24b về `bool(khoang_chay)` còn đúng tại chính ca `8,7,7,7`. Ca đếm chính xác Claude bổ sung dùng đầu vào mất mẫu khác. Đây là giới hạn của ca thử, không bác số khoảng đã đếm độc lập. [Ca cửa sổ của Codex](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia.py:21) · [Ca bổ sung của Claude](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2_claude.py:355) |
| **F6, bàn giao** | **Đúng tại thời điểm CX-19, đã xử lý một phần.** `khung_mo` hiện ghi đã đóng S4. Nhưng `buoc_tiep` của T-071 còn chờ CX-25/25b và của T-072 còn chờ CX-24b, dù các lượt đó đã xong. LOG T-072 có prompt kiểm lại. Mục cuối LOG T-071 kết thúc sau bảng đáp, thiếu prompt bàn giao. **KHÔNG CHẶN R5**, nhưng dùng riêng hai trường `buoc_tiep` sẽ giao lại việc đã làm. Đề nghị điều phối cập nhật hai dòng theo kết quả lượt này. Prompt chung ở cuối câu trả lời bao phủ cả hai task. [Trạng thái điều phối](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/TRANG-THAI.json:45) · [Cuối LOG T-071](D:/RCA-flashticket/tasks/T-071-w4a-nen/LOG.md:365) |
| **K1, phạm vi ghi** | **Đúng về thao tác ghi, phản hồi chưa đủ về quyền.** K1 thực sự tạo `grafana-log-e4.txt` trong vùng `t072-*`. Lệnh đọc log Docker, phù hợp hạn chế về truy vấn Prometheus lúc đó. Riêng `dap-cx19.md` xác nhận đã ghi script, bản đột biến và dữ liệu giải nén vào scratchpad ngoài repo trên laptop. Đường dẫn này nằm ngoài danh sách ghi của SPEC. I9 quy định vùng ghi **trên server**. Tôi chưa thấy phê duyệt riêng cho scratchpad trong nguồn được dẫn. **KHÔNG CHẶN số đo, nhưng chưa thể xác nhận tiêu chí “không ghi ngoài phạm vi”.** Đề nghị ghi ngoại lệ theo bằng chứng hiện có, hoặc dẫn đúng phê duyệt có trước nếu có. [Bản đáp §3](D:/RCA-flashticket/results/T-072/dap-cx19.md:25) · [Phạm vi SPEC](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/SPEC.md) · [I9](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md:48) |
| **N1, thiếu ngưỡng nhưng thoát thành công** | **Đúng, đã sửa trong v2.** Tôi chạy lại ca bỏ riêng p95 Ticket. Tiến trình con thoát mã 1 và báo `ticket (p95, 0 bước)`. Nhánh này dừng trước khi ghi JSON. Tám ngưỡng trên E2 thật đều tái lập được. [Ca kiểm CLI](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia.py:59) · [Ngưỡng E2](D:/RCA-flashticket/results/T-072/nguong.json) |
| **N2, điều kiện cần cho 5xx** | **Đúng về kết luận “chỉ đủ”, đúng một phần về lý do.** Phản ví dụ 2/32 hợp lệ. Cần phân biệt chặn lưu lượng đã có ở cả hai chuỗi với chặn số lỗi chỉ có ở luật thật. Bốn `M` lỗi bằng 0 và bốn ngưỡng lỗi thực đều bằng 5%. [Biểu thức](D:/RCA-flashticket/results/T-072/bieu-thuc.json:431) · [Chi tiết theo route, `#/chi_tiet`](D:/RCA-flashticket/results/T-072/nguong.json) |

Một đính chính nhỏ của T-071 có ý nghĩa cho kiểm kê lượt nhận. Bảng đáp ghi **17 lượt** nhưng liệt kê E2 có 8, E3 có 1, E4 có 9, tổng là **18**. Riêng hai khoảng tính mẫu số có 17 lượt. LOG E3 ghi rõ `receive` đã thành công. Đề nghị dùng đúng phạm vi khi dẫn số lượt; sai số kiểm kê này không đổi mẫu số E4. [Bảng đáp T-071](D:/RCA-flashticket/tasks/T-071-w4a-nen/LOG.md:365)

## 2. File đã thay đổi

**Không sửa file nào.** Tôi tự làm trên laptop, không dùng subagent, không SSH, không mở dữ liệu khóa, không commit và không gửi prompt sang agent khác. Các phép kiểm Python chạy với `-B`. Tôi gọi hàm trong bộ nhớ khi điểm vào dòng lệnh mặc định ghi JSON.

## 3. Kiểm đã chạy và kết quả

| Phép kiểm | Kết quả |
|---|---|
| SHA-256 theo manifest | T-071 `SHA256SUMS-sau-e4` **84/84**. T-072 `SHA256SUMS-dap-cx19` **8/8**, `-e4` **21/21**, `-e4-grafana` **3/3**, `-e3-offline` **6/6**, `-cx09` **11/11**. Hash hai bản đính chính khớp giá trị CX-25 công bố. [Manifest T-071](D:/RCA-flashticket/results/T-071/SHA256SUMS-sau-e4) · [Manifest phản hồi T-072](D:/RCA-flashticket/results/T-072/SHA256SUMS-dap-cx19) |
| Manifest lịch sử | Có **4/19** đường dẫn của `-e2-nguong` khác bản hiện tại, **1/6** ở `-d1-d4`, và **4/4** ở `-e3-chuan-bi` khác hoặc thiếu. Tôi dừng sử dụng các đường dẫn đó làm bằng chứng cho phiên bản cũ. Kế hoạch E3 hiện dùng khớp `-cx09`. Kiểm commit lab N/G cho thấy luật thử được gỡ và file 11 luật thật không đổi giữa hai commit. [Manifest ngưỡng ban đầu](D:/RCA-flashticket/results/T-072/SHA256SUMS-e2-nguong) · [Manifest CX-09](D:/RCA-flashticket/results/T-072/SHA256SUMS-cx09) |
| Dữ liệu gốc → chuyển đổi → ngưỡng | Băm trực tiếp từng thành viên `ra.tgz` theo `ra-SHA256SUMS` được **377/377 E2**, **424/424 E4**. So từng cặp biểu thức–lượt trước/sau chuyển định dạng được **192/192** và **216/216** bằng nhau về nhãn, thời điểm và giá trị. Tính lại E2 cho **8/8 ngưỡng** và phần `chi_tiet` khớp. Trường tên phiên bản cũ trong `nguong.json` vẫn ghi bản 1; hash và kết quả tính xác nhận công thức bản 2. [Manifest thành viên E2](D:/RCA-flashticket/results/T-071/e2/ra-SHA256SUMS) · [Manifest thành viên E4](D:/RCA-flashticket/results/T-071/e4/ra-SHA256SUMS) · [Ngưỡng và hash đầu vào](D:/RCA-flashticket/results/T-072/nguong.json) |
| Nhãn phút → R5 | Đếm lại từ từng hàng được E2 **356 khỏe, 38 biên, 38 flash**; E4 **383 khỏe, 43 biên, 38 flash**. Cả **896** trường `canh_bao` đều là `null`. Số 0 sự cố đến từ phép chấm và lịch sử vận hành. Tôi không thấy tên ca, nhãn lỗi hay mốc tiêm đi vào biểu thức cảnh báo. Nhãn khỏe ×1 được dùng đúng ở bước chọn ngưỡng E2 và lập mẫu số. [Phân loại E2](D:/RCA-flashticket/results/T-071/e2/phan-loai-phut.json) · [Phân loại E4](D:/RCA-flashticket/results/T-071/e4/phan-loai-phut.json) · [Đầu ra chấm E4](D:/RCA-flashticket/results/T-072/e4/cham-offline.json) |
| Bộ chấm và webhook | `thu_ca_gia.py` đạt **9/9**. `tu_kiem()` của cả hai bản v2 trả `[]`. Phản ví dụ A vẫn xuất hiện trên bản Claude. Ở E3, mỗi luật thử có đúng một tin `firing` và một tin `resolved`. Tôi không phát lại tải hay chấm lại toàn E4. [Ca giả](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia.py) · [Webhook đối chiếu theo luật](D:/RCA-flashticket/results/T-072/e3/b9-doi-chieu.json) |

**Đối với tiêu chí xong:** T-071 có hồ sơ E1 trước/sau, kết luận sức chứa, mốc dump, gói E2/E4 và mẫu số. Năm dump trên máy chủ chỉ được xác nhận qua hồ sơ hash trên laptop. T-072 có biểu thức và quy tắc chọn ngưỡng trước E2; bản gom 3 bổ sung cơ cấu chín lượt trước E4, sau khi E2 bắt đầu. E3 có bằng chứng webhook dương. E4 có phép so R5 theo khai trước. Các kết quả đó đáp ứng phần W4 về vận hành luật và báo động giả. Điểm A ảnh hưởng lựa chọn bộ chấm **cho lần sau**. Điểm B, C và K1 ảnh hưởng nội dung nghiệm thu. [SPEC T-071](D:/RCA-flashticket/tasks/T-071-w4a-nen/SPEC.md) · [SPEC T-072](D:/RCA-flashticket/tasks/T-072-w4b-luat-canh-bao/SPEC.md) · [Mốc DB](D:/RCA-flashticket/results/T-071/e1/moc-db.json) · [Phần bổ sung của quy tắc gom](D:/RCA-flashticket/results/T-072/quy-tac-gom.json)

## 4. Điều cần Minh quyết

- **R5 và T-071/B2:** đề xuất dừng phản biện hai phần này. Số đo đã được Q2 nhận. Không có bất đồng còn lại về mẫu số hoặc phạm vi của 12 container.
- **Bộ chấm và WHY-110:** đề xuất để Claude đáp A–C trong một lượt, ưu tiên sửa cách tính tử số theo tập phút đủ điều kiện và thu hẹp câu bảo đảm về p95. Trong thời gian đó, giữ bản khóa làm nguồn cho R5. Đổi trực tiếp bản v2 hiện có sẽ làm mất khớp manifest lượt 13.
- **Phạm vi ghi và bàn giao:** đề xuất ghi nhận scratchpad là ngoại lệ chưa có căn cứ duyệt trong hồ sơ đã đọc, đồng thời cập nhật hai trường `buoc_tiep` khi điều phối có quyền. Cách này giữ được bằng chứng và tránh giao trùng việc. Không cần xóa hiện vật hay mở lại lượt chạy.
- **Phần mục tiêu DT18/cô còn mở:** W4 đã đo báo động giả của luật cục bộ dưới tải nền. Bảy luật còn thiếu bằng chứng dương thật trong hồ sơ W4; độ nhạy, độ trễ với lỗi thật và tác dụng tính toán của đồ thị cần các ca lỗi và đối chứng tương ứng ở gói sau. Riêng nguyên nhân đuôi trễ Ticket còn có các giải thích DB, CPU/GC hoặc biến động request giữa lượt. Nếu cần kết luận cơ chế, hồ sơ đã nêu phép so span DB và tín hiệu tài nguyên của E4-06 với các lượt đối chiếu, ước **30–60 phút công** cho phần DB nếu dữ liệu còn lưu. Tôi đề xuất giữ giới hạn này trong báo cáo, chưa cấp thêm giờ máy chỉ để chốt W4. [MRP §2.3 và P10](D:/RCA-flashticket/docs/MRP.md) · [Bằng chứng dương theo luật](D:/RCA-flashticket/results/T-072/ke-hoach-e3-duong.md) · [Các phép phân xử còn thiếu](D:/RCA-flashticket/results/T-072/troi-p95-e2-e4.md:50)

## Prompt bàn giao cho Claude

Mẫu hiện có khối cổng G0–G4, chưa có khối G6. Dưới đây là **Prompt chung** và khối **Người làm đáp phản biện**. Minh có thể chuyển cùng bản kiểm lại trong chat này. [Mẫu gốc](D:/RCA-flashticket/docs/review-prompt.md:27)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-071 và T-072 (W4), tasks/T-071-w4a-nen/ và tasks/T-072-w4b-luat-canh-bao/.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P10 (W4), chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: SPEC và LOG của T-071, T-072; tasks/T-070-dieu-phoi-giai-doan-2/{HOP-DONG.md,LICH-MAY.md,TRANG-THAI.json}; docs/DECISIONS.md khối 23/11; docs/WHY.md phần W4; results/T-070/de-xuat-quyet-2026-11-23-ban5.md mục 5.2.
- Phản biện và phản hồi trước: results/T-070/codex/CX-19-tin-cuoi.md, CX-19b-tin-cuoi.md, CX-25-tin-cuoi.md, CX-25b-tin-cuoi.md, CX-24-tin-cuoi.md, CX-24b-tin-cuoi.md; LOG T-071 phiên 7, LOG T-072 lượt 13, results/T-072/dap-cx19.md; bản kiểm lại và các đề xuất do Minh chuyển kèm trong chat.
- Code và kết quả liên quan: results/T-071/{phan_loai_phut.py,e2/,e3/,e4/,dinh-chinh-cx19-co-hoc.md,SHA256SUMS-sau-e4}; results/T-072/{bieu-thuc.json,quy-tac-gom.json,quy-tac-chon-nguong.json,nguong.json,cham_offline.py,e4_giai_thich_khac.py,v2/,e2/,e3/,e4/,e3-doi-chieu-offline.json,bang-bao-dong-gia.json,troi-p95-e2-e4.md,troi-p95-rui-ro.json,troi_p95_rui_ro.py,dinh-chinh-cx19-co-hoc.md,SHA256SUMS*}.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc trên laptop, không SSH, không dùng subagent hay agent con.

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