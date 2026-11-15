# T-065 L8c — Kiểm Chrome cho G-c

2026-11-14T22:53:09Z · Codex, người làm, Windows/Chrome. Claude, người phản biện.

## Kết quả

G-c đạt trên chín tổ hợp mẫu của L8c. T-065 chờ Claude kiểm lại L6–L8c và Minh quyết nghiệm thu. Không có quyết định nghiên cứu mới.

- Hai UID `t065-l8b-rca` và `t065-l8b-phat-lai` có đủ 18/18 trang mẫu khớp bản, mã ca, trạng thái chạy và cửa sổ. Đổi bản qua bộ chọn trên cùng ca. Hàng bắt đầu và kết thúc metadata khớp `[t−300,t+300)`. URL Grafana ghi điểm cuối bao gồm, nhỏ hơn cận trên loại trừ 1 ms. Đối chiếu từng trang ở `doi-chieu.json#/matched_pages`.
- Đối chiếu đúng các dòng Chrome đã dựng của bảng thực thể, cờ và cạnh trên 9/9 tổ hợp trang RCA. Số dòng DOM tại vị trí kiểm và số dòng toàn bảng nguồn được ghi riêng ở `doi-chieu.json#/tables`. L8b đã kiểm toàn bộ các bảng qua dữ liệu/API.
- P7/`ebd5ef38` hiện `LOI_CHAY`, đường dẫn `results/T-064/cham/dau-ra-dev3/P7/ebd5ef38/loi-chay.json`, ô service giải thích lỗi và bảng hạng/cờ rỗng. Nhãn service mẫu còn lại hiện tên dạng chuỗi. V082 hiện “không có đầu ra cạnh”. V071 hiện bảng cạnh theo thứ tự/hạng nguồn. Cửa sổ điều hướng P7 lỗi lấy từ V082 cùng ca theo chỉ mục.
- Bấm mã ca → service → thao tác → chi tiết → Explore cho `86dea661`, `ebd5ef38`, `00eaea92`. Mỗi ca mở một đích Tempo, Loki và Prometheus. Với hai thao tác mẫu nền, bảng bằng chứng cấp Tempo/Loki. Đã chọn thao tác HTTP cùng service để mở Prometheus. `doi-chieu.json#/explore` dẫn từng thao tác, query, cửa sổ, request/response và ảnh.
- 9/9 request Inspector khớp query/cửa sổ nguồn và trả HTTP 200. Tám truy vấn có dữ liệu. Loki của `00eaea92` trả 0 dòng tại lần kiểm. Đây là truy vấn sống trên Explore. Bảng snapshot trên dashboard ghi giờ truy vấn trước đó. Bằng chứng hiện có chưa phân xử nguyên nhân Loki rỗng. Cần đối chiếu log đã lưu với nhãn và cấu hình retention tại cùng thời điểm để phân xử.
- Phát lại của `00eaea92` hiện lớp đáp án T-062 tách riêng với nguồn và cảnh báo ghép sau chấm. Trang RCA của cùng mẫu không có lớp đó. Hai ca dev ở phát lại chỉ hiện giới hạn chưa cấp nguồn đáp án.

## Trạng thái tải và bằng chứng

Phát lại `86dea661`, đổi V071 sang V082 khi đang ở phần đáp án, có thể giữ hàng cũ trong DOM của panel metadata nằm trên khung nhìn. `02-v082-86dea661-replay-offscreen-measure.json` ghi đáy panel ở khoảng −361 px và ảnh trước khi cuộn cho thấy phần đang hiện đã chuyển sang trạng thái V082. Sau khi đưa panel metadata vào khung, hàng tại vị trí nhìn thấy ghi V082. Bằng chứng ở `02-v082-86dea661-replay-onscreen-measure.json` và ảnh trước/sau. Khi đổi bản với metadata đang trong khung, đã thấy bản cập nhật đúng. Quan sát chỉ xác lập hành vi trên các thao tác đã kiểm. Cơ chế thực thi của Grafana khi panel nằm ngoài khung còn chưa xác định.

Lưu 29 ảnh cùng cây DOM, trạng thái đang tải, lỗi phương pháp và lần chụp quá thời gian. Bốn ảnh Explore bổ sung bằng cách bấm lại đúng link và dùng khung ảnh nhỏ hơn, có biên nhận `image-retries.jsonl`. Inspector yêu cầu Refresh để thu request/response. Hồ sơ giữ cây request/response đã mở rộng của các lượt Inspector, gồm các cây Loki dài. Không có lượt chạy lại M1, raw hay bộ kiểm API L8b.

## Toàn vẹn và bàn giao

Trước lượt, lệnh `& ./results/T-065/codex/l8b-local.ps1 -Action verify` xác nhận 9.022 checksum và LOG. Đối chiếu 10 pin nguồn dùng trong mẫu, gồm 8 đầu ra có kết quả, chỉ mục và cấu hình đề xuất. Hai hash provisioning khớp mốc L8b trước và sau lượt, đối chiếu `../006-gc-cuoi/may-sau.json#/new_dashboards`. STOP local/remote vắng tại các lần kiểm ranh giới. Cổng 13000 ban đầu trống. Tunnel SSH loopback PID 25432 chuyển tới Grafana exp-obs trên 10.0.0.215:3000. Không thay đổi cấu hình máy hoặc động tới các tab có trước.

Giao diện đáp ứng phần minh họa và truy vết đầu ra cuối thuộc phạm vi T-065. Hiệu quả phương pháp trên FlashTicket và RQ5/P10 tiếp tục theo hồ sơ nghiên cứu. Claude kiểm lại theo `../../prompt-ban-giao.md`.


- [Đối chiếu 18 trang, bảng và Explore](doi-chieu.json)
- [Ảnh lỗi chạy P7](04-p7-ebd5ef38-rca.jpg)
- [Ảnh V082 vắng đầu ra cạnh](05-v082-ebd5ef38-rca.jpg)
- [Ảnh bảng cạnh V071](03-v071-86dea661-edges.jpg)
- [Ảnh lớp đáp án T-062](09-v071-00eaea92-replay-answer.jpg)
