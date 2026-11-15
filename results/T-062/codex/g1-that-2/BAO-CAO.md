G1-THAT ĐẠT MỘT PHẦN

Kiểm vận hành chỉ đọc trên Grafana exp-obs, T-062/G1, lượt 2. Đây không phải phản biện chính thức và không nghiệm thu T-062. Không đọc/ghi REVIEW-G1*.md hay prompt-phan-bien-g1*.md; không sửa dashboard, hạ tầng, LOG hoặc STATE.

Cách kiểm và phiên bản

- Trình duyệt headless (không giao diện) Edge 157.0.4341.46, Playwright Core; Grafana 13.3.0 thật qua SSH 127.0.0.1:13000 → 10.0.0.215:3000. Hai dashboard uid rca-g2 và rca-g2-phat-lai đều version **6**, đầu/cuối lượt giống nhau: dashboard-live-*.json, dashboard-ket-thuc.json, kiem-ket-thuc.json.
- Đăng nhập bằng hai khóa được Minh cho phép, chỉ trong bộ nhớ. Browser context tạm, không xuất cookie/storage state. Không tạo API key. Chỉ API đọc và POST /api/ds/query; /login dùng cho đăng nhập.
- Đối chiếu 24 file dữ liệu/dashboard với manifest T-062 hiện tại: không lệch. So 18 file ca/phát lại và 2 chỉ mục trên public/rca với local: 20/20 khớp byte. Đầu vào không đổi cuối lượt. Hash ở kiem-hash-nguon.json, kiem-hash-remote.json và kiem-ket-thuc.json.
- Đọc đủ 11 panel có truy vấn × 9 ca bằng API với đúng target và biến dashboard; 99 nhóm truy vấn hợp lệ, không lỗi. Đọc giao diện chính và phát lại đủ 9 ca, cuộn để nạp panel, kiểm màu SVG thật; bấm danh sách đủ 9 ca. Chi tiết request/response: api-panel-<mã>.json, api-phat-lai-dung-<mã>.json; văn bản UI: ui-<mã>.json, ui-phat-lai-<mã>.json.
- Mốc giờ trong browser đặt UTC. Danh sách/bấm ca dùng t ±15 phút; menu Explore và bằng chứng dùng từ đầu nền đến cuối sự cố (t ±5 phút), so trực tiếp su_co.cua_so_nen.tu_ms / su_co.cua_so_su_co.den_ms hoặc bang_chung[].lien_ket[].cua_so_ms.
- Khoảng 20 phút vận hành từ bước ghi hash nguồn đến đóng đường hầm; không tải browser, chỉ cài playwright-core vào thư mục tạm (<1 GB). STOP không tồn tại ở các ranh giới đã kiểm.

Kết quả 9 ca

| Ca | Danh sách | Đồ thị | Hạng | Bằng chứng hạng 1 | Explore | Phát lại |
|---|---|---|---|---|---|---|
| e8661e0a | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 2 dòng² | Đạt URL 3 menu; bảng tempo; menu loki; menu prometheus; menu tempo | Đạt |
| 00eaea92 | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 4 dòng² | Đạt URL 3 menu; bảng prometheus; bảng tempo | Đạt |
| bf17acbf | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 15 dòng² | Đạt URL 3 menu; chưa bấm | Đạt |
| f728fce2 | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 1 dòng² | Đạt URL 3 menu; chưa bấm | Đạt |
| 6c1a9fd8 | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 1 dòng² | Đạt URL 3 menu; chưa bấm | Đạt |
| 2e2a5541 | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 8 dòng² | Đạt URL 3 menu; bảng prometheus | Đạt |
| a89954d1 | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 4 dòng² | Đạt URL 3 menu; bảng prometheus; bảng tempo; menu loki; menu prometheus; menu tempo | Đạt |
| 1ad3afeb | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 13 dòng² | Đạt URL 3 menu; chưa bấm | Đạt |
| a5539fba | Đạt 9/9; bấm chọn đúng | Đạt 17 nút/14 cạnh | Đạt 17 dòng¹ | Đạt 2 dòng² | Đạt URL 3 menu; menu loki | Đạt |

¹ Vai trò, số kênh, hạng nhóm nghi nguồn/kéo theo khớp nut[].hang. Hạng nhóm bình thường được chủ ý để trống trên nút/bảng theo chú thích giao diện, dù JSON nguồn có hạng chung; không ghi là hiển thị đủ hạng số của mọi nút. Không ca nào có nút thiếu dữ liệu để thử trạng thái tím ?. Đã so đúng 153 màu nút render và 126 cạnh có hướng; doi-chieu-9-ca.json, doi-chieu-menu-va-mau.json.

² Ca f728fce2 có đúng 1 dòng hạng 1 nhưng là bằng chứng cạnh không có URL; nguyên văn “loại đơn vị "canh" chưa có truy vấn hoặc định danh từ nguồn”. Có dòng không đồng nghĩa mở được dữ liệu gốc. Số dòng top lần lượt là số trong bảng, so bang_chung[thuc_the = top].

Bằng chứng và Explore thật

- Toàn bộ thành phần có bằng chứng: **132 dòng**, **123 URL** (92 Tempo, 31 Prometheus), **9 dòng không có URL**, **0 URL Loki**. Tất cả 123 URL giải mã được đúng một lần, đúng datasource, cửa sổ và truy vấn nguồn. Lệnh kiểm nằm trong request của bang-chung-tat-ca-<mã>.json; đối chiếu từng dòng ở doi-chieu-lien-ket-bang.json.
- Đã bấm **13 liên kết thật**, không chỉ dựng URL hay gọi API thay cho thao tác: bảng Tempo ở e8661e0a / a89954d1 / 00eaea92, mỗi liên kết trả 50 trace (giới hạn truy vấn 50, không phải tổng trace). Bảng Prometheus ở a89954d1 / 00eaea92 / 2e2a5541, mỗi liên kết trả 1 chuỗi × 41 mẫu.
- Menu e8661e0a: Tempo 50 trace; Prometheus 3 chuỗi ×41 mẫu; Loki **0 dòng**. Menu a89954d1: Tempo 50 trace; Prometheus 3×41 mẫu; Loki **749 dòng**. Menu Loki a5539fba: **12 dòng**. Mọi phép bấm này đúng datasource và t ±5 phút; không “Could not parse Explore URL”, không lỗi query. Chi tiết từng phép ở explore-tom-tat.json và explore-(bang|menu)-*.json, gồm URL, query thực gửi, response và văn bản nhìn thấy.
- **Chưa thể đạt yêu cầu bấm Loki từ bảng ở 3 ca:** bảng không cung cấp URL Loki. Hai bằng chứng log ở a89954d1 không có lien_ket trong nguồn; ô mở dữ liệu gốc ghi “loại đơn vị "log" chưa có truy vấn hoặc định danh từ nguồn”. Không tự thay bằng link menu rồi nhận là đã kiểm link bảng.

Phát lại và cách hiện đáp án

- 9/9 ca khớp root, họ lỗi, tập chấp nhận, dấu ◆ và hạng tốt nhất với ket-qua/phat-lai/<mã>.phat-lai.json#/phat_lai và bang-cham.json#/ca. Vai trò/hạng từng thành viên tập chấp nhận ở cột M1 trong tập khớp nut[]. Không dùng sổ tiêm lỗi. Chi tiết: doi-chieu-phat-lai.json; trường list chứa nguyên văn cột hiển thị.
- f728fce2: root “api-gateway → booking-service (http)”; tập “api-gateway, booking-service”; cột M1 “api-gateway: #4 bị kéo theo; booking-service: #1 nghi là nguồn”; dấu ◆ ở cả hai nút; hạng tốt nhất #1. Không còn diễn giải đầu tiên là nơi tiêm đơn lẻ.
- 1ad3afeb: root “event-service → event_db (data)”; tập “event-service, event_db”; cột M1 “event-service: #1 nghi là nguồn; event_db: bình thường (M1 xếp hạng #4, nhóm 14 thành phần)”; dấu ◆ ở cả hai nút; hạng tốt nhất #1.
- Nhãn hạng tốt nhất ghi rõ “theo e2, mức nút; không phải kết luận M1 định vị đúng cạnh”. Các ca root null hiện tập rỗng, không đánh dấu nút; M1 vẫn có nghi nguồn như file kết quả. Đây là hiển thị số đã có, không kiểm tính đúng khoa học của phương pháp hay nhãn.
- Trang chính: 9/9 văn bản UI không chứa “đáp án”, dap_an, tap_chap_nhan hay root_khai_truoc; chỉ hiện dự đoán. Các truy vấn chính đọc thư mục chính, không đọc phat-lai. Việc tên dự đoán trùng tên đáp án ở một ca không được dùng làm bằng chứng rò nhãn. Cấu hình organize dùng chung còn ánh xạ tên detail__dap_an sang “◆ Tập chấp nhận (phát lại)”; schema trả về không có trường đó, UI không hiện cột/giá trị này. Ghi rõ khác biệt giữa tên ánh xạ trong cấu hình và trường dữ liệu thực ở kiem-trang-chinh.json.

Panel rỗng và thông báo nguyên văn

| Ca (thành phần hạng 1) | Panel 11: 5xx | Panel 13: log có lọc |
|---|---|---|
| e8661e0a | có chuỗi | No data |
| 00eaea92 | No data | No data |
| bf17acbf | No data | No data |
| f728fce2 | No data | No data |
| 6c1a9fd8 | có chuỗi | No data |
| 2e2a5541 | No data | No data |
| a89954d1 | có chuỗi | có log |
| 1ad3afeb | có chuỗi | No data |
| a5539fba | No data | có log |

- **5/9** panel 5xx và **7/9** panel log hiện đúng chữ **“No data”**, API trả thành công nhưng không có chuỗi/dòng. Không thấy lỗi datasource ở 99 nhóm truy vấn hợp lệ. Không suy ra service khỏe, không có lỗi hay collector hỏng từ kết quả rỗng này.
- Mô tả có điều kiện chỉ hiện khi rê chuột vào biểu tượng thông tin. Đã hover thật và chụp: “Nếu truy vấn thành công nhưng không trả dữ liệu: chưa có chuỗi metric HTTP server 5xx khớp service và khung giờ đang chọn. Không suy ra service không có lỗi.”; tương tự log: “chưa có dòng log khớp service, khung giờ và bộ lọc error/exception/warn. Không suy ra service không có lỗi.” Nguyên văn đầy đủ ở panel-rong-tooltip-5xx.json và panel-rong-tooltip-log.json.
- Thử thành phần bình thường booking-service ở e8661e0a: bảng bằng chứng hiện **“Không có: M1 không gắn cờ kênh nào của thành phần này.”** Khi không có giải thích E5, thông báo quan sát ở các ca: **“Không có: M1 không coi thành phần này là bị kéo theo.”** Đây là thông báo riêng của panel, khác “No data” của query sống.

Hành vi có thể gây hiểu nhầm

- Mục ① nằm dưới nhóm “Trong trang này”, ghi “Xem bằng chứng và thao tác … (cuộn xuống)” nhưng mở tab mới. Tab mới chọn đúng booking-service; chọn qua bảng hạng cũng đúng. Hai quan sát ban đầu chỉ theo dõi tab cũ nên đã nhầm thành lỗi chọn nút; đã kiểm lại tab mới và bác bỏ nhận định lỗi đó. Chon-nut-booking-truoc/sau.json giữ quan sát ban đầu; **chon-nut-booking-ket-luan.json** là kết luận đã phân xử. Không đề xuất sửa dựa trên quan sát nhầm.
- Bố cục thường chỉ nhìn thấy một phần dòng của bảng (có cuộn nội bộ); dữ liệu vẫn đủ 9/17. Ảnh 02 dùng **View panel** chỉ đọc để hiện đủ 9 ca, không đổi cấu hình. Cột dài trong bảng phát lại có thể bị cắt trên màn hình; bản ghi View panel của hai root cạnh được chụp riêng.

Lượt kiểm hỏng / giới hạn

- Giữ các phép gọi kiểm ban đầu: api-<mã>.json bị 400 query.duplicateRefId vì gộp các panel cùng ref A; api-phat-lai-<mã>.json dùng nhầm thu_muc=rca nên nhận lỗi parse HTML. Đây là lỗi script kiểm, không phải lỗi dashboard. Kết luận chỉ dùng api-panel-*.json và api-phat-lai-dung-*.json, đúng biến của từng trang.
- Ba lời gọi node_repl bị hết thời gian khi gom quá nhiều thao tác hoặc chờ phần tử sai vai trò; phiên headless được mở lại, giữ file đã ghi, chỉ làm phần còn thiếu. Không chạy lại RCA. Một lỗi cú pháp tổng hợp đã sửa trước khi chạy. Không có kết quả hỏng nào bị xóa.
- Chưa bấm mọi URL Explore (đã kiểm cấu trúc 123 URL bằng chứng và bấm mẫu nêu trên); không thể bấm URL Loki không tồn tại trong bảng. Chưa phân xử vì sao dữ liệu sống rỗng, chưa kiểm trạng thái ERROR/NO_EVIDENCE hay nút thiếu dữ liệu vì 9 ca thật không có trạng thái đó. Không dựng dữ liệu giả lên Grafana.
- Tác vụ đã trả lời khả năng hiển thị và đường mở dữ liệu trên bản 6 trong 9 ca này; không xác nhận cơ chế RCA, tính đúng nhãn hoặc nghiệm thu chặng nghiên cứu. Không bổ sung quyết định nghiên cứu. Việc chấp nhận giới hạn liên kết log/bằng chứng cạnh thuộc Minh; kết quả hiện tại hỗ trợ kết luận **đạt một phần**, chưa hỗ trợ tuyên bố đủ chuỗi ba loại từ bảng bằng chứng.

Ảnh

Tất cả trong anh/ (40 ảnh). Đã xem trực tiếp ảnh danh sách, đồ thị, phát lại root cạnh, tooltip No data và Explore để kiểm nội dung; không có trang đăng nhập điền mật khẩu.

- [anh/01-danh-sach-9-ca.png](anh/01-danh-sach-9-ca.png)
- [anh/02-danh-sach-du-9-ca-panel-view.png](anh/02-danh-sach-du-9-ca-panel-view.png)
- [anh/chinh-00eaea92.png](anh/chinh-00eaea92.png)
- [anh/chinh-1ad3afeb.png](anh/chinh-1ad3afeb.png)
- [anh/chinh-2e2a5541.png](anh/chinh-2e2a5541.png)
- [anh/chinh-6c1a9fd8.png](anh/chinh-6c1a9fd8.png)
- [anh/chinh-a5539fba.png](anh/chinh-a5539fba.png)
- [anh/chinh-a89954d1.png](anh/chinh-a89954d1.png)
- [anh/chinh-bf17acbf.png](anh/chinh-bf17acbf.png)
- [anh/chinh-e8661e0a.png](anh/chinh-e8661e0a.png)
- [anh/chinh-f728fce2.png](anh/chinh-f728fce2.png)
- [anh/chon-nut-booking-sau.png](anh/chon-nut-booking-sau.png)
- [anh/explore-bang-00eaea92-prometheus.png](anh/explore-bang-00eaea92-prometheus.png)
- [anh/explore-bang-00eaea92-tempo.png](anh/explore-bang-00eaea92-tempo.png)
- [anh/explore-bang-2e2a5541-prometheus.png](anh/explore-bang-2e2a5541-prometheus.png)
- [anh/explore-bang-a89954d1-prometheus.png](anh/explore-bang-a89954d1-prometheus.png)
- [anh/explore-bang-a89954d1-tempo.png](anh/explore-bang-a89954d1-tempo.png)
- [anh/explore-bang-e8661e0a-tempo.png](anh/explore-bang-e8661e0a-tempo.png)
- [anh/explore-menu-a5539fba-loki.png](anh/explore-menu-a5539fba-loki.png)
- [anh/explore-menu-a89954d1-loki.png](anh/explore-menu-a89954d1-loki.png)
- [anh/explore-menu-a89954d1-prometheus.png](anh/explore-menu-a89954d1-prometheus.png)
- [anh/explore-menu-a89954d1-tempo.png](anh/explore-menu-a89954d1-tempo.png)
- [anh/explore-menu-e8661e0a-loki.png](anh/explore-menu-e8661e0a-loki.png)
- [anh/explore-menu-e8661e0a-prometheus.png](anh/explore-menu-e8661e0a-prometheus.png)
- [anh/explore-menu-e8661e0a-tempo.png](anh/explore-menu-e8661e0a-tempo.png)
- [anh/panel-rong-00eaea92.png](anh/panel-rong-00eaea92.png)
- [anh/panel-rong-khong-bang-chung.png](anh/panel-rong-khong-bang-chung.png)
- [anh/panel-rong-tooltip-5xx.png](anh/panel-rong-tooltip-5xx.png)
- [anh/panel-rong-tooltip-log.png](anh/panel-rong-tooltip-log.png)
- [anh/phat-lai-00eaea92.png](anh/phat-lai-00eaea92.png)
- [anh/phat-lai-1ad3afeb-ban-ghi.png](anh/phat-lai-1ad3afeb-ban-ghi.png)
- [anh/phat-lai-1ad3afeb.png](anh/phat-lai-1ad3afeb.png)
- [anh/phat-lai-2e2a5541.png](anh/phat-lai-2e2a5541.png)
- [anh/phat-lai-6c1a9fd8.png](anh/phat-lai-6c1a9fd8.png)
- [anh/phat-lai-a5539fba.png](anh/phat-lai-a5539fba.png)
- [anh/phat-lai-a89954d1.png](anh/phat-lai-a89954d1.png)
- [anh/phat-lai-bf17acbf.png](anh/phat-lai-bf17acbf.png)
- [anh/phat-lai-e8661e0a.png](anh/phat-lai-e8661e0a.png)
- [anh/phat-lai-f728fce2-ban-ghi.png](anh/phat-lai-f728fce2-ban-ghi.png)
- [anh/phat-lai-f728fce2.png](anh/phat-lai-f728fce2.png)

Phạm vi ghi và kết thúc

Chỉ thêm file trong results/T-062/codex/g1-that-2/. Không sửa đầu vào, g1-that/ cũ, giao-dien/, ket-qua/, tasks/, docs/, src/; không commit/push. Browser và đường hầm riêng đã đóng. Danh sách đầu ra và hash ở manifest.json; kiểm cuối ở kiem-ket-thuc.json, kiem-dau-ra.json. Không tự kích hoạt hay tác động lượt phản biện G1 khác.
