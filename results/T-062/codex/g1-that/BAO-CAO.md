G1-THAT ĐẠT MỘT PHẦN

Đã kiểm Grafana exp-obs THẬT, dashboard version 4. Danh sách, bản ghi, đồ thị, hạng hiển thị và bằng chứng khớp nguồn cho 9/9 ca. Explore từ menu nút hoạt động. Explore từ bảng bằng chứng không đạt: 47/47 liên kết bị mã hóa hai lần; mở thử Tempo và Prometheus dẫn đến trạng thái mặc định, truy vấn trống và “No data”. Đây là kiểm vận hành, không phải phản biện chính thức hoặc nghiệm thu T-062/M1.

**Cách kiểm.** Đo từ 2026-11-12T01:29:49.374Z đến 2026-11-12T01:45:25.492Z, 15.6 phút. Grafana 13.3.0; Edge headless 157.0.4341.46, Playwright Core 1.65.0. Dùng Edge có sẵn; chỉ cài Playwright Core vào thư mục tạm, không tải browser hoặc dataset. Context không lưu bền, đăng nhập và cookie chỉ trong bộ nhớ. Chỉ đọc cấu hình/dashboard, truy vấn qua /api/ds/query và xem UI; không lưu cấu hình. Múi giờ UTC. Biến t_tu/t_den khớp cửa sổ nền/sự cố của từng file; 9 lựa chọn ca, 17 lựa chọn thành phần, đúng service ở cả 9 ca.

Cổng 13000 tại 127.0.0.1 đã do SSH PID 29216 chiếm từ trước. Đường hầm riêng nghe 127.0.0.2:13000, PID 27668; không dùng 3000 trên laptop và không tác động SSH cũ. Đã đóng browser/context và đường hầm riêng. Kiểm socket sau đóng chỉ còn 127.0.0.1:13000 của PID 29216. STOP không tồn tại ở các lần kiểm.

**Toàn vẹn và thay đổi đồng thời.** Đầu lượt: 26 file liên quan khớp results/T-062/manifest.json; 18 file kết quả chính/phát lại từ public/rca khớp hash local. Hai bộ panel trên Grafana khớp dashboard local lúc bắt đầu. Cuối lượt: Grafana vẫn version 4, panel không đổi. Tuy nhiên dung-dashboard.py và hai JSON dashboard local đã đổi trong lúc đo. Phiên này không ghi ba file đó; không xác định tác nhân/lý do. Dừng kết luận phụ thuộc bản local mới: kết quả chỉ áp dụng Grafana v4 đã đo. Không nói bản local mới đạt hoặc còn lỗi. Xem kiem-hash.json, toan-ven-ket-thuc.json và dashboard-live-v4-*.json.

**Bảng 9 ca.** Đồ thị ghi số nút/cạnh. Bằng chứng ghi số kênh của thành phần hạng 1, đã khớp đơn vị, tên kênh và điểm s. Menu 3/3 nghĩa là URL ba datasource đúng service và cửa sổ; chỉ hai ca bên dưới được mở thật cả ba loại.

| Ca | Danh sách | Đồ thị | Hạng | Bằng chứng hạng 1 | Explore | Phát lại |
|---|---|---|---|---|---|---|
| e8661e0a | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 2 | Menu 3/3; bảng lỗi 2/2 | Khớp trường phát lại** |
| 00eaea92 | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 4 | Menu 3/3; bảng lỗi 4/4 | Khớp trường phát lại** |
| bf17acbf | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 15 | Menu 3/3; bảng lỗi 14/14 | Khớp trường phát lại** |
| f728fce2 | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 1 | Menu 3/3; bảng không có link | Khớp trường phát lại** |
| 6c1a9fd8 | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 1 | Menu 3/3; bảng lỗi 1/1 | Khớp trường phát lại** |
| 2e2a5541 | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 8 | Menu 3/3; bảng lỗi 8/8 | Khớp trường phát lại** |
| a89954d1 | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 4 | Menu 3/3; bảng lỗi 3/3 | Khớp trường phát lại** |
| 1ad3afeb | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 13 | Menu 3/3; bảng lỗi 13/13 | Khớp trường phát lại** |
| a5539fba | Đạt: 9 dòng | Đạt: 17/14 | Đạt*: 17 dòng | Đạt: 2 | Menu 3/3; bảng lỗi 2/2 | Khớp trường phát lại** |

* Nhóm nghi nguồn/kéo theo khớp nut[].hang; màu/chữ theo vai_tro khớp cả 17 nút. Dashboard để trống số hạng nhóm bình thường dù JSON có hang. Vì vậy không coi là hiển thị đủ mọi giá trị hang của JSON. Bảng hạng có 17 dòng qua API; một số dòng cần cuộn trên UI.

** Phát lại khớp thanh_phan_tiem và vai trò/hạng của thành phần đó. Không đồng nhất trường này với toàn bộ root/tap_chap_nhan hoặc hang_tot_nhat trong bang-cham.json. Đánh dấu đúng 9/9 ca: 4 ca null không có nút đáp án, 5 ca lỗi đánh dấu một nút.

| Ca | Cột ĐÁP ÁN | Họ lỗi hiển thị | M1 xếp đáp án là | hang_tot_nhat nguồn |
|---|---|---|---|---|
| e8661e0a | — | — — root = null (ca bình thường) | — | null |
| 00eaea92 | — | D9-11 — root = null (tải tăng khỏe) | — | null |
| bf17acbf | booking-service | D9-08 — booking-service | nghi là nguồn #1 | 1 |
| f728fce2 | api-gateway | D9-07 — api-gateway → booking-service (http) | bị kéo theo #4 | 1 |
| 6c1a9fd8 | — | — — root = null (ca bình thường) | — | null |
| 2e2a5541 | booking-service | D9-06 — booking-service | nghi là nguồn #1 | 1 |
| a89954d1 | event-service | D9-05 — event-service | nghi là nguồn #1 | 1 |
| 1ad3afeb | event-service | D9-01 — event-service → event_db (data) | nghi là nguồn #1 | 1 |
| a5539fba | — | — — root = null (ca bình thường) | — | null |

EVENT-DB-LAT: root nguồn là event-service → event_db (data), tập chấp nhận gồm event-service và event_db, còn cột ĐÁP ÁN chỉ ghi event-service. NET-GW-BOOK: root nguồn là api-gateway → booking-service (http), tập chấp nhận gồm api-gateway và booking-service; cột ĐÁP ÁN ghi api-gateway, vai trò/hạng là bị kéo theo #4. Nhận xét phát lại ghi hạng tốt nhất trong tập là #1 và hạng 1 của M1 là booking-service. Đây là các giá trị quan sát, không đổi thành cách diễn giải khác. Bản ghi phát lại có root/nhận xét. 4 ca root=null: cột đáp án/vai trò dùng —, họ lỗi/nhận xét ghi root=null.


**Lỗi Explore tái hiện được.** Panel 6, Bằng chứng của … — các kênh M1 gắn cờ: API trả URL panes=%7B..., nhưng href thật trong DOM là panes=%257B.... Đã đọc đủ 47 liên kết trong View panel, tất cả mã hóa hai lần, phân bố theo bảng 9 ca. Panel bằng chứng không báo lỗi truy vấn; lỗi xảy ra khi mở link. Mở nguyên văn link Tempo của e8661e0a và Prometheus của a89954d1: Explore dùng Prometheus mặc định, truy vấn trống và “No data”. Ảnh ca a89954d1 ghi nguyên văn:

> Could not parse Explore URL
> The requested URL contains invalid parameters, a default Explore state has been loaded.

Bằng chứng: lien-ket-bang-bang-chung.json; explore-e8661e0a-bang-bang-chung.json; explore-bang-prometheus-loi-a89954d1.json; hai ảnh lỗi Explore. Không sửa dashboard trong lượt này.

Ba bằng chứng không có link theo nguồn: bf17acbf và f728fce2, kênh E2:api-gateway->booking-service, hiện: loại đơn vị “canh” chưa có truy vấn hoặc định danh từ nguồn; a89954d1, kênh log_loi, hiện: loại đơn vị “log” chưa có truy vấn hoặc định danh từ nguồn. Không coi thiếu link này là lỗi mạng/datasource. Chữ trong file UI giữ dấu nháy nguyên văn.

**Explore mở có dữ liệu.** Dùng đúng href menu nút, không sửa query/window:

| Ca/thành phần | Tempo | Loki | Prometheus |
|---|---|---|---|
| a89954d1 / event-service | 50 trace | 749 log qua cùng query/window; UI có log ERROR | 3 chuỗi × 41 điểm |
| a5539fba / keycloak | 50 trace | 12 log | 6 chuỗi × 41 điểm |

Cả sáu lần mở HTTP 200, có dữ liệu, không có lỗi datasource. Trace giới hạn 50; số log phụ thuộc giới hạn query, không phải tổng dữ liệu gốc. Lần mở Loki a89954d1 nhận phản hồi log-volume trước; đã kiểm riêng đúng query log trong cùng cửa sổ, đếm 749 dòng với maxLines=1000. Chỉ lưu query/số lượng của lần bổ sung, không lưu nội dung log. Cửa sổ/query cụ thể ở explore-*.json và ket-qua-kiem.json#/lokiLogQueries.

**Panel trống quan sát được.** Thông báo nguyên văn “No data”. Panel 11: Lỗi 5xx/giây theo thao tác — <service>. Panel 13: Log của <service> có chữ error/exception/warn. API đúng query/window cũng trả 0 dòng/điểm ở các ô này, không báo lỗi. Không suy diễn đó là hỏng hệ thống hoặc bằng chứng hoàn toàn không có lỗi.

| Ca | Panel báo No data |
|---|---|
| e8661e0a | 13 |
| 00eaea92 | 11, 13 |
| bf17acbf | 11, 13 |
| f728fce2 | 11, 13 |
| 6c1a9fd8 | 13 |
| 2e2a5541 | 11, 13 |
| a89954d1 | không |
| 1ad3afeb | 13 |
| a5539fba | 11 |

Panel 9/10 có dữ liệu cả 9 ca; panel 12 trả 50 trace/ca. Panel 7 hiện “Không có: M1 không coi thành phần này là bị kéo theo.” khi chọn thành phần hạng 1; đây là giải thích trống, không phải lỗi. Không có lỗi API Infinity/datasource trong các truy vấn kiểm. Số đo ở lop-thao-tac-api.json; chữ UI ở ui-chot-<mã>.json#/livePanels.

**Trang chính và đáp án.** Không thấy trường/giá trị đáp án trong bản ghi, đồ thị, hạng hoặc bằng chứng trang chính; target truy vấn không trỏ phat-lai/ hoặc khối phat_lai. Tuy nhiên điều kiện nguyên văn không có chữ/trường đáp án KHÔNG đạt: đầu trang có link “Trang phát lại (có đáp án — chỉ mở khi chấm xong)”. Phân biệt chữ ở link điều hướng với giá trị đáp án của ca. Ảnh danh sách thể hiện đúng chữ này.

**Ảnh chính**, trong anh/, chụp trên Grafana thật:

- [anh/danh-sach-du-9-ca-phong-to-panel.png](anh/danh-sach-du-9-ca-phong-to-panel.png)
- [anh/do-thi-hang-chot-CPU-BOOK-bf17acbf.png](anh/do-thi-hang-chot-CPU-BOOK-bf17acbf.png)
- [anh/do-thi-hang-chot-NET-GW-BOOK-f728fce2.png](anh/do-thi-hang-chot-NET-GW-BOOK-f728fce2.png)
- [anh/do-thi-hang-chot-SLOW-BOOK-2e2a5541.png](anh/do-thi-hang-chot-SLOW-BOOK-2e2a5541.png)
- [anh/do-thi-hang-chot-HTTP5-EVENT-a89954d1.png](anh/do-thi-hang-chot-HTTP5-EVENT-a89954d1.png)
- [anh/do-thi-hang-chot-EVENT-DB-LAT-1ad3afeb.png](anh/do-thi-hang-chot-EVENT-DB-LAT-1ad3afeb.png)
- [anh/explore-prometheus-a89954d1.png](anh/explore-prometheus-a89954d1.png)
- [anh/explore-prometheus-a5539fba.png](anh/explore-prometheus-a5539fba.png)
- [anh/loi-explore-bang-prometheus-a89954d1.png](anh/loi-explore-bang-prometheus-a89954d1.png)
- [anh/loi-explore-tu-bang-bang-chung-e8661e0a.png](anh/loi-explore-tu-bang-bang-chung-e8661e0a.png)
- [anh/phat-lai-f728fce2.png](anh/phat-lai-f728fce2.png)
- [anh/phat-lai-1ad3afeb.png](anh/phat-lai-1ad3afeb.png)
- [anh/phat-lai-a5539fba.png](anh/phat-lai-a5539fba.png)

Ảnh danh sách dùng View panel để thấy đủ 9 dòng. Ảnh bố cục mặc định ban đầu chỉ thấy 5 dòng và cần cuộn bảng; giữ 01-trang-chinh-danh-sach-9-ca.png làm ảnh ban đầu, không dùng nó chứng minh 9 dòng cùng hiện. Hai ảnh do-thi-hang-CPU-BOOK-… và do-thi-hang-NET-GW-BOOK-… là trung gian; dùng bộ do-thi-hang-chot-… cho kết luận cuối. Giữ mọi ảnh/lượt thử.

**Chưa kiểm và giới hạn.** Chưa kiểm bản local mới phát sinh giữa lượt, hoặc Grafana sau thời điểm kết thúc nếu được triển khai tiếp. Không mở mọi trace/span hoặc mọi link trong 47 link lỗi: đã đọc href cả 47, mở đại diện hai loại có lỗi; menu mở ba loại cho hai ca. Không kiểm riêng mẫu T-061, ERROR/NO_EVIDENCE, quyền user khác, thao tác sửa/lưu. Một số lượt chuyển ca trong trang giữ thành phần đang chọn; phép đo cuối chỉ rõ ca/thành phần hạng 1 bằng URL để tránh đọc nhầm. Chưa xác nhận mọi đường chuyển biến nhanh đều tự chọn lại hạng 1. Không đánh giá cơ chế khoa học M1, không thay phản biện G1 riêng. Không đọc dữ liệu khóa/sổ tiêm.

**Lượt thử và tự kiểm.** api-<mã>.json là phản hồi main/replay/variables thật. ui-chot-<mã>.json và lien-ket-bang-bang-chung.json là UI cuối. ui-<mã>.json là trung gian khi thử điều hướng, không dùng để kết luận bằng chứng hạng 1. markerMatches=false trong phat-lai-<mã>.json là lỗi so prototype của mảng giữa các môi trường JavaScript trong bộ kiểm; không phải lỗi Grafana. So trực tiếp phần tử đúng 9/9 trong doi-chieu-phat-lai-chot.json. Giữ file trung gian để không mất lượt hỏng. Không ghi mật khẩu/cookie/token vào file, báo cáo hoặc ảnh; có rà mẫu nhạy cảm trên đầu ra.

**Bàn giao.** Chỉ tạo file trong results/T-062/codex/g1-that/ và gói npm tạm theo quyền brief. Không sửa docs/tasks/src/ket-qua/giao-dien; không commit/push hoặc ghi cấu hình exp-obs. Không thêm/đổi quyết định nghiên cứu. Báo cáo/ảnh lỗi cần phiên điều phối tiếp nhận; sửa/triển khai và lưu quyết định chính thức do Minh quyết. Bước tiếp theo phụ thuộc bản dashboard mới Minh muốn kiểm: kiểm lại phần chịu ảnh hưởng sau triển khai, dùng kết quả ca/dữ liệu còn hợp lệ, không chạy lại thực nghiệm RCA.

Prompt bàn giao vận hành, không phải prompt phản biện chính thức: Đọc results/T-062/codex/g1-that/BAO-CAO.md và ket-qua-kiem.json. Đây là phép kiểm chỉ đọc trên Grafana exp-obs version 4, không thay lượt phản biện G1. Đối chiếu bằng chứng URL/ảnh và phần thay đổi nguồn giữa lượt với giao diện hiện tại. Báo Minh phạm vi cần kiểm lại; không tự sửa/triển khai nếu chưa có quyền tương ứng. Không đọc/chạm kết luận các bản phản biện G1 cho việc vận hành này.
