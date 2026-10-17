# T-040 — Tổng hợp P5b và bàn giao P6/P9

- **Trạng thái:** ĐÃ DUYỆT TẠO SPEC ngày 17/10/2026; chờ soát SPEC, chưa duyệt triển khai (Q-168).
- **Người làm:** Claude.
- **Người phản biện:** Codex, phiên sạch độc lập với phiên chuẩn bị tài liệu.
- **Thuộc gói MRP:** P5b — **Cổng:** chuẩn bị G3.
- **Phân công:** Minh đổi từ phương án vai trò dự kiến trong chat sang Claude làm, Codex phản biện. Codex ghi gói chuẩn bị theo quyền riêng tại Q-168; phiên này không thực hiện phản biện.

## Mục tiêu

Tổng hợp bằng chứng kiến trúc và đối chiếu đồ thị của FlashTicket, Train Ticket và Online Boutique thành đầu vào có thể sử dụng cho P6 và P9.

Nguồn chi phối: phần mục tiêu, RQ3/RQ5, P5–P6/P9 trong `docs/MRP.md`; DT18 và hướng dẫn của cô tại `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` và `docs/reference/sources/advisor-2026-09-23.md`; các quyết định và lý do hiện hành trong `docs/DECISIONS.md`, `docs/WHY.md`.

Đây là **task tổng hợp bằng chứng và xác định phần còn thiếu**. Task trả lời:

- Đang có những đồ thị, tín hiệu và quan hệ nào, với mức bằng chứng nào?
- Đối chiếu nguồn tĩnh với trace đã chứng minh được gì, chưa chứng minh được gì?
- P6 có thể sử dụng đầu vào nào; FlashTicket cần bổ sung quan sát gì cho P9?

Task không chọn phương pháp RCA, không xác nhận lợi ích của đồ thị và không tự đóng RQ3/RQ5 hoặc G3.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn yêu cầu | Điều cần phân xử; giải thích khác | Phép kiểm và bằng chứng | Kết quả được phép kết luận | Phần thiếu và bước phụ thuộc |
|---|---|---|---|---|
| Ba nhánh có cùng nghĩa biểu diễn để tổng hợp không? — P5 | Cùng phiên bản công cụ chưa chắc cùng phạm vi, mức đồ thị hoặc cách ánh xạ | Đối chiếu hợp đồng, revision, manifest, namespace, loại cạnh, projection và exclusions | Chỉ rõ phần tương thích và phần không thể gộp | Sai lệch cần sửa ở task nguồn; không tự sửa trong T-040 |
| Chênh lệch nguồn tĩnh–trace nói lên điều gì? — P5/RQ3 | Có thể do workload, lineage, ánh xạ, giao thức, thiếu quan sát hoặc lỗi trích nguồn | Đọc tập thành viên, điều kiện nguồn và trung gian hiện có; đối chiếu nhóm chênh và nhóm khớp tương ứng | Quan sát đã xác nhận; giải thích được phân xử hoặc vẫn OPEN | Bằng chứng runtime/lineage còn thiếu; không mặc nhiên quy lỗi collector |
| Đầu vào nào hỗ trợ thiết kế P6? — RQ3/P6 | Quan hệ có thể bổ sung thông tin, nhưng chưa chắc cải thiện phát hiện/xếp hạng | Nối bản đồ hạn chế P4 đã có với nút, cạnh, tín hiệu và phép tính ứng viên; tách căn cứ P4, DT18 và kỹ thuật | Đủ căn cứ đề xuất ứng viên nào; đầu vào nào chưa đủ | Chọn cơ chế, mức đồ thị và đánh giá lợi ích thuộc SPEC P6 |
| FlashTicket cần ghi nhận thêm gì? — RQ5/P9 | Thiếu schema, thiếu instrumentation, thiếu cấu hình hay chưa có dữ liệu chạy thật | Đối chiếu T-037 với B16; lập yêu cầu có vị trí thu, trường dữ liệu, khóa liên kết và cách kiểm | Danh sách yêu cầu quan sát có căn cứ và phần đã đáp ứng theo thiết kế | P9 triển khai/thu dữ liệu; đối chiếu runtime và đánh giá thuộc task tiếp theo |

## Đầu vào

Chỉ đọc các nguồn được phép:

- SPEC, LOG, kết quả và trạng thái phản biện của T-035–T-039.
- Hợp đồng chung hiện hành của T-036, gồm gói SMTP V2 tại `results/T-036/runs/doi-chieu-smtp-001/`.
- Các đầu ra hiện hành của T-037, T-038, T-039, kiểm theo manifest tương ứng.
- Bản đồ hạn chế và bàn giao G2 của T-034; lần theo kết quả P4 gốc khi một nhận định cụ thể cần bằng chứng.
- Nguồn FlashTicket tại `D:/Project/flash-ticket-platform`, chỉ đọc; đặc biệt `docs/architecture/B16-observability-baseline.md` và các tài liệu được T-037 dẫn.
- AGENTS, STATE, MRP, WHY, DECISIONS, LESSONS và nguồn DT18/cô.

Khi bắt đầu, ghi rõ revision, manifest, đầu ra hiện hành và trạng thái chấp nhận của từng nguồn. Không coi file mới nhất theo thời gian là bản chính thức.

**Phụ thuộc tại thời điểm đề xuất SPEC (16/10/2026), phải kiểm lại khi bắt đầu:**

- T-038: bản sửa của reviewer tại `results/T-038/runs/reviewer-r1-fix-20261016-001/apply-plan.json` chưa được tiếp nhận vào đầu ra chính thức. Chỉ tổng hợp chính thức phần bị ảnh hưởng sau khi có bản nguồn hợp lệ và quyết định xử lý tương ứng.
- Gói sửa chung T-036 và T-035: giữ đúng trạng thái phản biện/nghiệm thu hiện hành; không suy việc các nhánh dùng được là toàn bộ gói đã nghiệm thu.
- Phần tóm tắt “Task đang mở” trong STATE chưa khớp các mốc mới. Không dùng đoạn này thay quyết định và bàn giao nguồn.

Không đọc test, dữ liệu giữ ngoài, nội dung telemetry đã cách ly hoặc dữ liệu thô mới.

## Đầu ra

Tất cả trong `results/T-040/`:

| File | Nội dung |
|---|---|
| `dau-vao.json` | Nguồn, revision, manifest, trạng thái sử dụng, phạm vi và đường dẫn bằng chứng |
| `tong-hop.json` | Bảng đối chiếu ba hệ thống; từng số có đường dẫn nguồn và con trỏ JSON |
| `bao-cao-p5b.md` | P5b đã trả lời gì, bằng chứng, giới hạn và phần chưa hoàn thành |
| `ban-giao-p6.md` | Đầu vào sẵn có, ngữ nghĩa nút/cạnh/tín hiệu, vai trò tính toán ứng viên, điều kiện thất bại và quyết định còn thiếu |
| `yeu-cau-quan-sat-p9.md` | Yêu cầu quan sát FlashTicket và đầu vào chuẩn hóa cho P9a/P9b |
| `con-mo.json` | Câu hỏi mở, bằng chứng thiếu, người/phần việc cần cung cấp và quyết định phụ thuộc |
| `tong_hop.py`, `kiem_tra.py` | Mã tổng hợp và kiểm kết quả đã lưu |
| `kiem-dung-dan.md`, `manifest.json`, `runs/` | Kiểm chứng, tài nguyên thực đo, mọi lượt chạy kể cả lỗi và lịch sử đầu ra |

Không sao chép toàn bộ kết quả nguồn; lưu con trỏ và bằng chứng đủ tái lập.

## Phạm vi ghi

Sau khi SPEC được duyệt triển khai:

- `results/T-040/`.
- Nối thêm `tasks/T-040-p5b-tong-hop/LOG.md`.
- Chỉ dòng T-040 trong `docs/STATE.md`.

Không sửa SPEC đã khóa, kết quả T-035–T-039, code dùng chung, tài liệu quyết định hoặc repo FlashTicket. Nếu cần thay đổi những nơi đó, trình riêng.

Người phản biện chỉ ghi bản phản biện được Minh cho phép; không tự cấp quyền bằng SPEC này.

## Các bước

1. **Chốt ảnh chụp đầu vào.** Kiểm hash, revision, trạng thái và liên kết bản hiện hành. Nguồn mâu thuẫn hoặc hash lệch thì dừng phần phụ thuộc.
2. **Đối chiếu hợp đồng ba nhánh.** Kiểm mức thực thể/thao tác, chiều và loại cạnh, ánh xạ, projection, tín hiệu và điều kiện nguồn.
3. **Tổng hợp kết quả đã lưu.** Bao phủ toàn bộ index được phép, tách theo hệ thống, họ dữ liệu, mức đồ thị và miền quan sát. Không chạy lại RCA hoặc dựng lại toàn bộ nguồn.
4. **Diễn giải chênh lệch.** Lần theo đầu vào → trích/ánh xạ → mô hình → đối chiếu. Với nhận định quan trọng, xem nhóm khớp có điều kiện tương ứng; nếu chưa phân xử được nguyên nhân, giữ OPEN.
5. **Lập bàn giao P6/P9.** Mỗi đề xuất nối được tới câu hỏi nguồn, bằng chứng và quyết định tiếp theo.
6. **Tự kiểm và báo cáo.** Kiểm toàn bộ số dẫn, phạm vi kết luận, diff và file đầu ra; ghi LOG và prompt phản biện.

Có thể chuẩn bị khung, phần FlashTicket/Online Boutique và bàn giao độc lập trong khi chờ T-038. Không tự thay bản chính thức bằng bản sửa dự kiến để hoàn thành báo cáo.

## Kiểm đúng đắn

- Tính lại các tập và mẫu số từ thành viên đã lưu, độc lập với bảng tóm tắt nguồn; kiểm giao, hiệu, phần loại trừ và mẫu số rỗng.
- Tách đối chiếu đầu mút với đối chiếu loại cạnh; tách cạnh thực thể, thao tác, projection và quan hệ chỉ ở mức thực thể.
- Không cộng cửa sổ lặp như bằng chứng độc lập; nếu nhóm các đồ thị giống nhau phải giữ danh sách thành viên.
- Không lấy trung bình tỷ lệ giữa các miền không tương đương. Tỷ lệ phủ trên tập trace đủ điều kiện không có nghĩa phủ toàn bộ runtime.
- Không biến quan hệ thiết kế, binding tín hiệu hoặc quan hệ chưa rõ loại thành cạnh tính toán đã xác nhận.
- Giữ phân biệt database logic/instance/tài nguyên dùng chung; sender/receiver của messaging; SMTP chấp nhận thư và thư được giao.
- Với Online Boutique, giữ đúng miền dữ liệu adapter đã cho phép; metadata không tự trở thành đồ thị thiết kế. Không tự coi `Node` là host.
- Kiểm các trường hợp dễ làm sai tổng hợp: mẫu số rỗng, loại cạnh unknown, nguồn không cùng phiên bản và bản dự kiến lẫn bản hiện hành.
- Giới hạn lịch sử đã được Minh chấp nhận ở task nguồn vẫn được dẫn rõ; không mở lại nghiệm thu hoặc mô tả dữ liệu dựng lại như bản gốc.

## Tiêu chí xong

1. Mọi kết luận và số liệu truy được tới nguồn đã kiểm; không còn mâu thuẫn đầu vào chưa xử lý ảnh hưởng kết luận đang trình.
2. Ba hệ thống được tổng hợp đúng phạm vi bằng chứng; không trộn thiết kế, nguồn tham chiếu, dữ liệu quan sát và lợi ích RCA.
3. Mỗi chênh lệch quan trọng có giải thích được chứng minh hoặc câu hỏi OPEN cụ thể; không chỉ gắn cờ.
4. Bàn giao P6 chỉ rõ đầu vào, nút/cạnh, nơi gắn tín hiệu và phép tính ứng viên sử dụng cạnh; chưa chốt cơ chế trước đánh giá.
5. Mỗi yêu cầu P9 có: lý do → trường/khóa cần có → vị trí thu → cách kiểm → quyết định phụ thuộc. Phân biệt việc collector làm được với thông tin ứng dụng chưa từng ghi.
6. Báo cáo nêu rõ phần mục tiêu P5/RQ3/RQ5 đã bao phủ và phần còn thiếu; không nhận P5 hoàn tất chỉ vì T-040 đủ file.
7. Nếu lỗi nguồn T-038 vẫn chặn phần tổng hợp cốt lõi, bàn giao phần đã làm và phụ thuộc; **chưa báo T-040 hoàn thành toàn phạm vi**.

Các câu hỏi runtime hoặc lợi ích đồ thị thuộc bước sau có thể tiếp tục OPEN; không yêu cầu giải quyết chúng để hoàn thành một task tổng hợp đúng phạm vi.

## Không làm

- Không sửa thay T-038 hoặc nghiệm thu thay Minh.
- Không chọn thuật toán, tín hiệu, ngưỡng hay cấu hình P6.
- Không chạy baseline, đối chứng cấu trúc hoặc đánh giá mới. Những việc này cần SPEC P6 và quyền dữ liệu riêng.
- Không triển khai collector, sửa kiến trúc/nghiệp vụ FlashTicket hoặc thu runtime mới. T-040 bàn giao yêu cầu cho P9.
- Không tải repo/dataset, bật EC2, mở test, commit hoặc push.
- Không bỏ nghĩa vụ nghiên cứu vì thiếu đầu vào: ghi đúng bằng chứng cần bổ sung, phạm vi và quyết định chịu ảnh hưởng.

## Chi phí ước lượng

**Ước lượng chưa đo:** một phiên khoảng 3–4 giờ làm việc, chưa gồm chờ sửa nguồn và phản biện; xử lý máy dự kiến dưới 30 phút.

Chạy trên laptop, đọc tuần tự kết quả đã lưu. Không GPU, không EC2, không tải dữ liệu. Dung lượng mới dự kiến dưới 200 MB và RAM tăng thêm dưới 1 GB, gồm log và lượt lỗi; phải ghi số thực đo.

Giả định đầu ra nguồn có thể đọc trực tiếp và không cần dựng lại. Nếu giả định sai hoặc khối lượng vượt một phiên, trình tách phần bổ sung; không giảm độ sâu kiểm để vừa thời gian.

## Rủi ro và điều chưa chắc

- T-038 và gói sửa chung có thể đổi trước lúc triển khai: phải kiểm lại bản hiện hành.
- Lineage từ source đến deployment/dataset chưa đủ thì chỉ kết luận về nguồn tham chiếu.
- FlashTicket hiện có bằng chứng thiết kế; khả năng thu và liên kết runtime chưa được xác nhận.
- Quan hệ biểu diễn được không chứng minh quan hệ đó cải thiện RCA.
- Thiếu dữ liệu chưa từng ghi không thể được giải quyết chỉ bằng collector.
- Các quyết định và nghiệm thu ở task nguồn không tự cấp quyền chọn P6 hoặc mở test.

## Prompt bàn giao

Prompt soát SPEC theo nguyên văn Prompt chung + Soát SPEC + G3 trong `docs/review-prompt.md` được lưu tại LOG.md, Phiên 1. Minh chuyển thủ công sang phiên Codex sạch; lượt đó chỉ đọc và trả lời trong chat nếu chưa có quyền ghi bản phản biện riêng.

Sau triển khai, người làm Claude phải soạn prompt soát kết quả theo bản hiện hành của `docs/review-prompt.md`.
