# T-065 L7 — kiểm liên kết sau UI06

## Kết luận R1

**12/12 luồng mẫu đạt.** Đã đủ bằng chứng cho phạm vi kiểm R1 được Minh duyệt: chín luồng trên trang chính và ba luồng trên trang phát lại. Đề nghị Claude kiểm lại R1; Minh quyết việc chấp nhận kết quả. L7 xong phần kiểm này, T-065 vẫn đạt một phần vì G-c chưa có bản M1-FT cuối.

| Bản / ca | Service | Panel 4 chính | Panel 22 | Panel 23 | Panel 4 phát lại |
|---|---|---|---|---|---|
| p7 / 1ad3afeb | event-service | Đạt, bấm 1 | Đạt, bấm 8 | Đạt, bấm 5 | Đạt, bấm 6 |
| V032-H5b / 46aab4be | payment-service | Đạt, bấm 10 | Đạt, bấm 12 | Đạt, bấm 15 | Đạt, bấm 14 |
| V041-R1-H1c+H5b+H8s1 / 2e2a5541 | booking-service | Đạt, bấm 16 | Đạt, bấm 17 | Đạt, bấm 19; bằng chứng nối 21 | Đạt, bấm 18 |

## Quan sát

- Hai file provisioning trên exp-obs khớp hash của hai bản UI06 lưu ở repo. Rà JSON theo panel và đường dẫn cho đúng bốn data link dùng hai biến thời gian. Xem [mẫu và liên kết](mau-chon.json).
- Mẫu được chốt trước khi bấm. Nguồn của mỗi ca dẫn từ chỉ mục T-064 đến đầu ra đã đối chiếu SHA-256, rồi so cửa sổ với bản xuất T-065. So URL và request theo biên mili giây, với to bằng mốc kết thúc loại trừ trừ 1 ms.
- Query Inspector của panel 31 ghi PromQL thực, from/to, mã trả về và số điểm từng chuỗi. Các luồng đạt có dữ liệu. Chi tiết từng lần bấm và dòng thu bằng chứng ở [đối chiếu](doi-chieu-dich.json) và [nhật ký](nhat-ky-bam.jsonl).
- Panel 34 kiểm theo một trang đích cho mỗi ca. Có 72/72 Start time đọc được trong cửa sổ. Đây là các dòng thấy trong DOM, bảng có thể ảo hóa. Xem [đối chiếu trace](doi-chieu-trace.json).
- Hai lần bấm nút payment_db của V032 mở đúng service, đúng ID và cửa sổ. Tiêu đề ban đầu hiện ID. Đối chứng trên cùng URL ghi hàng Thao tác = payment_db và NO_A trong panel 24. Mở lại cùng tham số ghi tiêu đề đổi từ ID sang tên khi Grafana tải xong. Xem [đối chứng V032](v032-doi-chung-panel24.json).
- Nhật ký giữ lần công cụ chọn nhầm Inspector, chờ menu quá hạn và lần kiểm coi var-dv_svc bắt buộc có trong URL. Panel 31 và PromQL ở cùng đích xác nhận service khi Grafana lược tham số này. Các dòng nối mang trường doi_chieu_lan_bam.
- Ổ D: đầy khi lưu ảnh đầu V041. Ảnh và bản ghi được giữ tạm trong bộ nhớ rồi lưu khi có chỗ. Tệp 0 byte mang hậu tố loi-thu-bang-chung được giữ làm dấu vết ENOSPC, không dùng làm ảnh bằng chứng.
- Grafana dùng 359,2 MiB ở đầu lượt, 424,5 MiB tại checkpoint và 296,8 MiB khi tiếp nhận trước Inspector. Nhật ký ghi runner đang hoạt động khi bắt đầu V041 và khi tiếp nhận. Xem [kiểm máy](may.jsonl).
- Kiểm sau Inspector lúc 12:19:14Z: Grafana 377,1 MiB/768 MiB; hai STOP chưa bật, RestartCount 0, StartedAt giữ nguyên, OOMKilled=false, không có Docker event của Grafana từ checkpoint. Các tiến trình M1 vẫn chạy; lượt này chỉ đọc trạng thái, không thay tiến trình hay thư mục lô.
- Tiếp nhận đúng tab 217961091, View panel 31, service booking-service và thao tác OrderExpiryWorker.expireDueOrders. Không bấm lại panel 23. Refresh đầu phiên cho cây lỗi “Unexpected error”; kiểm local cho thấy không còn listener 13000 và PID tunnel cũ đã mất. Docker không ghi sự kiện restart/OOM từ checkpoint; RestartCount vẫn 0, StartedAt giữ nguyên. Đã dựng lại đúng tunnel theo brief, không sửa file máy chủ. Sau đó Refresh Inspector trên cùng đích trả mã 200. Giữ [cây lỗi](19-inspector-loi-request-response.txt) và [biên bản tunnel](19-su-co-tunnel.json). Không có ảnh hợp lệ của lỗi đầu vì API chụp ảnh timeout; không dùng ảnh cũ thay ảnh lỗi.
- Lần 19 có [cây request/response đầy đủ](19-inspector-request-response.txt), [bản trích xuất](19-inspector-trich-xuat.json), [ảnh truy vấn](anh/19-2e2a5541-inspector-p31.jpg) và [ảnh biên request/response](anh/19-2e2a5541-inspector-bien-response.jpg). Bản trích xuất giữ toàn bộ mảng thời gian và giá trị đọc từ Inspector; đây không phải JSON transport lấy từ clipboard. Request panel 31 dùng PromQL `sum by (http_request_method, http_route) (rate(http_server_request_duration_seconds_count{service_name="booking-service"}[1m]))`, from `1794435513000`, to `1794436112999`, step 15 s. Trường `response.results.A.status` bằng 200; hai chuỗi, mỗi chuỗi 41 điểm, tổng 82 điểm. Chuỗi GET /actuator/health và GET /api/v1/orders/{orderId} đều có dữ liệu. Xem `doi-chieu-dich.json#/lan_bam/14/query_inspector` và `19-inspector-trich-xuat.json#/response/results/A`.
- Giờ đọc cây Inspector là 12:15:02.455Z ngày 14/11/2026; giờ bấm 19 chính xác vẫn chưa biết. Dòng 19 gốc giữ `utc: null`; dòng 20 giữ lỗi thu bằng chứng, dòng 21 nối Inspector qua `doi_chieu_lan_bam: 19`. Không coi hai dòng nối là lượt bấm mới. Checkpoint cũ được giữ nguyên làm lịch sử.

## Suy luận và phần còn mở

- URL và request Grafana dùng đúng cửa sổ tại các đích đã kiểm. Mỗi chuỗi Prometheus có một điểm đầu sớm hơn from, phù hợp với việc căn lưới step 15 s. Lượt này chưa kiểm cơ chế căn lưới. Mốc request và các điểm đầu/cuối đều được lưu trong JSON.
- Panel 23 lấy service từ detail__chu và ID từ trường id. Biến op lấy cặp ten/id ở Infinity. Panel 24 và 25 lọc theo ID; tiêu đề dùng op:text. Đối chứng V032 phù hợp với giai đoạn Grafana chưa ánh xạ ID sang tên. Không thấy sai mapping ID/cửa sổ nên chưa đề xuất sửa liên kết.
- Lần 19 đã đủ bằng chứng đúng service, operation ID/tên và cửa sổ. Request dùng `2026-11-11T22:18:33.000Z` đến `2026-11-11T22:28:32.999Z`. Nguồn phương pháp `/window` ghi đơn vị ns, nền N nối tiếp cửa sổ A; toàn khoảng nửa mở kết thúc tại `22:28:33.000Z`. To trên URL/request bằng kết thúc loại trừ trừ 1 ms. Điểm đầu mỗi chuỗi ở `22:18:30.000Z`, sớm hơn from 3 s; điểm cuối ở `22:28:30.000Z`. Như các lượt trước, quan sát này phù hợp căn lưới 15 s nhưng chưa xác nhận cơ chế căn lưới. Không dùng panel HTTP theo service này để khẳng định có metric riêng của job; phép kiểm R1 yêu cầu một panel sống tại đúng đích.
- Không phát hiện lỗi liên kết trong 12 luồng mẫu sau UI06 nên không đề xuất sửa dashboard. Kết quả mẫu không thay mọi bằng chứng lịch sử của L5 và không giải quyết các điểm khác của REVIEW-2. Lỗi Inspector đầu phiên đi cùng tunnel local mất, sau khôi phục cùng request trả dữ liệu; chuỗi này hỗ trợ giải thích gián đoạn kết nối. Không coi lỗi ấy là kết quả khoa học hoặc lỗi mapping của data link.
- G-c chờ bản M1-FT đề xuất cuối từ T-064, cùng chỉ mục và hash. L7 hỗ trợ phần minh họa của DT18. RQ5 vẫn phụ thuộc thực nghiệm trên FlashTicket.
