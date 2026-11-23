# Claude: kế hoạch hợp nhất bản 3 (đáp phản biện bản 2)

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 1220). Không biên tập.

Đã đối chiếu thực tế. Lưu ý quy trình: bản phản biện của Codex được dán cùng yêu cầu, nên phần tự soát dưới đây **không độc lập**. Tôi chỉ ghi những điểm Codex chưa nêu. Lượt này không sửa file nào.

## 1. Tự soát lại plan bản 2 (điểm Codex chưa nêu)

| # | Mức | Vấn đề | Xử lý trong plan hợp nhất |
|---|---|---|---|
| N1 | CHẶN | Trạng thái T-069 trên đĩa đã đổi. Phiên fork (phiên 3) đã sửa theo duyệt: `dinh-chinh-1.md` hạ "DB là nguyên nhân gốc" xuống **ứng viên**, đếm lại tỉ lệ bảng tại đúng thời điểm từng ca (4,8×, 7,2×, 6,2×, không phải ~10×), xác nhận code đường mua vé của Booking **có đổi**, và chạy phép bỏ từng thành phần (V060/V061/V066 cùng hạng). Các câu tôi viết lúc trước ("nguyên nhân gốc đã lần được", "không do code") đã lỗi thời. | Plan hợp nhất lấy `dinh-chinh-1.md` và LOG phiên 3 làm chuẩn. |
| N2 | CHẶN | Hai phiên Claude cùng ghi vào T-069 (fork và phiên này) dễ ghi đè lên nhau. | Chỉ một phiên giữ T-069: phiên điều phối này. Phiên fork dừng ghi; lưu trữ khi Minh đồng ý. |
| N3 | KHÔNG CHẶN | Cổng W3 ("V082 tụt thì dừng, trình Minh") chỉ chặn việc **chọn V082 cho demo** (W5, W9a). Nó không chặn W4 (cảnh báo không phụ thuộc phương pháp RCA) và W6. | W4 và W6 khởi động ngay. W5 viết code ngay; phần chọn bản cho demo chờ quyết định Q1. |
| N4 | KHÔNG CHẶN | Mỗi lượt tải cấp mới 20 phiên đăng nhập. Mười mấy lượt mỗi ngày làm `keycloak_db` lớn dần, trong khi Keycloak `SELECT OUTBOX_ENTRY` chính là một kênh vượt Booking ở CPU-BOOK-1. | Lượt nền ghi số dòng `keycloak_db` cùng các bảng đơn/vé mỗi lượt. |
| N5 | KHÔNG CHẶN | Các đợt flash ×3 trong nền làm DB lớn nhanh gấp 3 lần trong đoạn đó. | Ghi số dòng theo từng lượt, kèm mức tải của lượt. |
| N6 | KHÔNG CHẶN | Span mồ côi tăng ở 16/17 cặp; tác động "batch" của Collector agent chưa xác định (T-067). W5 dựng ca từ trace theo t̂. | SPEC W5 kiểm độ đầy đủ trace trong cửa sổ t̂ trước khi nghiệm thu. |
| N7 | KHÔNG CHẶN | `httpcheck_error` chỉ có chuỗi khi có lỗi (đã thấy ở T-069 Bước 0). Luật liveness phải xử lý được chuỗi vắng. | Đưa vào SPEC luật W4. |
| N8 | KHÔNG CHẶN | Nạp luật cảnh báo (W4) và dashboard của T-068 (đang chờ Codex) cùng chạm Grafana. | Mọi thay đổi Grafana chỉ làm ở khoảng chuyển giữa các khoảng đo. |
| N9 | KHÔNG CHẶN | Lỗi ghi chép của tôi: LOG bước 9 ghi `SHA256SUMS` = `410d9923…`, nhưng sau đó tôi sinh lại file khi nối M12/M13 vào `thay-doi-may.md` (Codex tìm thấy). | Nối một dòng đính chính vào LOG T-069 (cần duyệt). |
| N10 | KHÔNG CHẶN | Mỗi gói cần SPEC duyệt và một lượt Codex, nên Minh là nút thắt khi mở nhiều gói cùng lúc. | Phiên điều phối gom câu hỏi và soát chéo giao diện giữa các SPEC trước khi trình, để Minh duyệt theo lô. |

## 2. Kiểm từng điểm của Codex

| Điểm | Kết luận | Bằng chứng riêng |
|---|---|---|
| Không chạy được tải liên tục 12 giờ, nhiều đợt flash | **Đúng** | `tai_linux.py:340–342`: `--seconds` 1–3600, `--multiplier` 1–3, `--buoc-tai` một bậc; `purchase-journey.js:18` chặn `seconds > 3600`. Nối lượt 1 giờ là cách duy nhất không phải sửa bộ tải. |
| Cam kết "W4 xong 15–16Z"; chưa khai báo giả chấp nhận, đơn vị sự cố, mẫu số giờ khỏe, thời điểm luật có hiệu lực | **Đúng** | Tôi đưa giờ xong khi chưa đo khoảng chuyển lượt và chưa có tiêu chí. Rút lại mốc giờ. |
| Báo động giả khi flash cần bằng chứng sức khỏe độc lập và phân loại khai trước | **Đúng** | Ca `124242f0` khỏe là bằng chứng chọn (b), nhưng không thay được tiêu chí khỏe cho từng lượt nền. |
| Nghiệm thu W5 chưa phân biệt ca mới với ca phát lại; cần bản ghi cảnh báo có t̂, luật, tín hiệu, giờ nhận webhook | **Đúng** | `stage_m1.py` nhận `--t` từ ngoài; chế độ (b) cần t̂ từ cảnh báo, không từ sổ tiêm. |
| Thử tải tối đa: hệ số tối đa 3; PSI không phải mức dùng CPU | **Đúng** | Hệ số ×4, ×6 không chạy được. Tôi đã dùng PSI (tỉ lệ thời gian tác vụ phải chờ CPU) như thể nó cho biết máy gần bão hòa; suy luận đó sai. Hoãn. |
| Con số 41,5% chỉ là của riêng `tbl_orders`, chưa nói gì về p95 hay cảnh báo | **Đúng.** Có thêm bằng chứng mới Codex chưa có | `phan-tich/troi-trong-luot.txt`: trong lượt chính, p50 của các truy vấn nền tăng khoảng 1,7× sau 8,5 giờ (worker hết hạn đơn 18,5 → 31,0 ms; giao vé 18,3 → 31,2 ms). Đây là truy vấn nền, chưa phải p95 route. |
| Đồng bộ ngày ở Ticket/Payment nên tách khỏi hạn W4 | **Đúng** | Tôi đã đọc code: không có quyết toán tự động (`PaymentWorker` không có job này); ngày chỉ dùng cho check-in và màn hình đối soát. Mục 2 trong kế hoạch của phiên fork ("phải trước 22:16Z, có thể sinh payout") là **sai**, cùng lỗi tôi đã tự đính chính. |
| Chênh hash `SHA256SUMS` trong LOG | **Đúng** | Xem N9. |

## 3. Kế hoạch hợp nhất (bản 3, thay mọi bản trước của cả hai phiên)

### 3.1. Minh quyết một lượt

| # | Câu hỏi | Đề xuất | Mặt trái |
|---|---|---|---|
| Q1 | W3: chấp nhận ô tụt CPU-BOOK-1 như ngoại lệ có ghi rõ, dùng V082 cho demo? | **Chấp nhận.** D1–D5 không chạm; P7 và mọi biến thể tụt y hệt, nên không bản nào tốt hơn (WHY-102). | Khi demo ép CPU Booking, kết quả có thể xếp Ticket hoặc Keycloak lên trên Booking. Nên chọn ô demo khác. |
| Q2 | Đồng bộ ngày sự kiện ở Ticket/Payment +14 ngày? | **Có, nhưng không gấp.** Làm ngay trước khi chụp mốc DB, để mốc chụp ở trạng thái nhất quán. Dump dòng cũ, kiểm đúng 1 dòng mỗi bảng. | Thêm một lần sửa dữ liệu nghiệp vụ. |
| Q3 | Mốc DB tham chiếu | Chụp dump **sau Q2**, ở trạng thái hiện tại (~40k đơn). W4 **không** khôi phục giữa lượt (đo trôi). Cách khôi phục và thời gian khôi phục đưa vào SPEC W6, đo khi exp-app rảnh. | Mốc lớn thì truy vấn nền chậm; nhưng chọn mốc nhỏ hơn là xóa dữ liệu, dễ bị hiểu là chọn điều kiện có lợi. |
| Q4 | Hồ sơ tải nền W4 | **(b) chuỗi lượt 1 giờ:** phần lớn lượt ×1 đều; một số lượt ×1 rồi lên ×3 ở phút 40 (`--buoc-tai 2400`). Lịch, tỉ lệ lượt flash và tiêu chí giờ khỏe khai trước trong SPEC. | Có khoảng chuyển lượt không tải; phải loại khỏi mẫu số và xử lý cảnh báo ở biên. |
| Q5 | Thử tải tối đa | **Hoãn.** Bộ tải chỉ tới ×3. Nếu Minh giao NV1 thì soạn SPEC riêng. | NV1 vẫn mở. |
| Q6 | Mức W8 (P8) | Mức demo tối thiểu như §8.2. | Chưa đánh giá chất lượng giải thích của LLM. |
| Q7 | Đóng T-069 | Phiên này giữ T-069: nối dòng đính chính N9 vào LOG; commit `tasks/T-069…`, `results/T-069/` (bỏ 3 file `raw.json`), `docs/DECISIONS.md`, `docs/WHY.md`; Minh chọn có đưa `docs/STATE.md` (đang lẫn thay đổi T-066/67/68) không; gửi Codex prompt kiểm lại ở LOG phiên 3. | — |
| Q8 | Báo nhóm FlashTicket về truy vấn quét tuần tự | Phiên điều phối soạn bản nháp có số đo và nói rõ giới hạn quy nguyên nhân; Minh gửi. | — |

### 3.2. Các phiên

| Phiên | Task (SPEC riêng) | Việc | Dùng exp-app? | Khởi động |
|---|---|---|---|---|
| **Điều phối (phiên này)** | T-069 (đóng), không làm code nhiệm vụ | Giữ lịch exp-app; chốt các hợp đồng I1–I5 dưới đây; soát chéo các SPEC trước khi trình; gom câu hỏi cho Minh; DECISIONS; bản nháp gửi FlashTicket | Không | Ngay |
| **nen-w4** | T-070: W4a, đo nền | Q2, chụp mốc; chuỗi lượt 1 giờ hai khoảng; ghi số dòng DB (gồm `keycloak_db`), CPU PostgreSQL, chuỗi lỗi/p95/liveness theo đúng nhịp luật; phân loại giờ khỏe | **Có, sở hữu duy nhất** | Ngay |
| **luat-w4** | T-071: W4b, luật cảnh báo | Luật `provisioning/alerting`, quy tắc gom, script chấm luật trên dữ liệu đã lưu (thử trước trên lượt 1 giờ của T-067 và các ca khỏe của T-069), bộ nhận webhook nhẹ, tiêu chí báo giả | Chỉ ở khoảng chuyển | Ngay |
| **rca-w5** | T-072: W5, RCA trực tuyến | Bộ xuất theo cửa sổ bất kỳ (gồm R9), G1 0.3 mang t̂/luật/tín hiệu, bộ điều phối, đo thời gian trên dev rồi khai N phút, nghiệm thu theo D3 | Chỉ ở khung nghiệm thu | Ngay (chọn bản cho demo chờ Q1) |
| **danh-gia-w6** | T-073: W6, thiết kế đánh giá | Khóa bản, D14, ma trận ô, baseline; runner W7 đóng gói đầu vào không phụ thuộc đầu ra P7 (bài học T-069 Bước 0, mục 0.8); kiểm soát DB (mốc, khôi phục, trộn thứ tự ô); điểm yếu chấm z là ứng viên; kiểm hạn bán (02/12) | Một khung ngắn đo khôi phục, sau W4 | Ngay |
| **llm-w8** | T-074: W8 | LLM mức demo trên đầu ra G1 đã có | Không | Sau Q6 |

### 3.3. Hợp đồng giữa các phiên (phiên điều phối chốt trước khi trình các SPEC)

- **I1 — Bản ghi cảnh báo (W4b → W5):** t̂ (lúc chuyển sang firing), mã luật, nhãn và giá trị tín hiệu kích hoạt, giờ webhook tới (lưu riêng). Chế độ (b) không đọc sổ tiêm.
- **I2 — Lịch tải và giờ khỏe (W4a ↔ W4b):** khai trước từng lượt (×1 hay flash), khoảng chuyển lượt; một giờ tính là khỏe khi đạt tiêu chí độc lập từ k6 (hành trình xong, không 5xx ngoài dự kiến, `dropped_iterations`, 429) cùng các kiểm backend. Báo giả tính theo sự cố sau khi gom, chia cho giờ khỏe, báo riêng theo mức tải. Ngưỡng báo giả chấp nhận được do Minh duyệt trong SPEC; đề xuất ≤ 1 sự cố mỗi 6 giờ khỏe ×1, flash báo riêng.
- **I3 — Prometheus:** trong khoảng đo, không phiên nào chạy truy vấn nặng (W5 dev, chấm ngưỡng). Truy vấn nặng làm trên đoạn đã đóng.
- **I4 — Grafana:** mọi thay đổi chỉ ở khoảng chuyển; ghi giờ luật thực sự có hiệu lực.
- **I5 — exp-app và máy tải:** chỉ nen-w4 phát lượt; các phiên khác xin khung qua phiên điều phối.

### 3.4. Thứ tự dùng exp-app (tuần tự; không cam kết giờ)

| Bước | Việc | Điều kiện vào | Thời lượng (đo hoặc ước) |
|---|---|---|---|
| E1 | Q2 + chụp mốc DB | Minh duyệt Q2, Q3, SPEC T-070 | ước ~30 phút, chưa đo |
| E2 | **Khoảng 1:** chuỗi lượt 1 giờ, chỉ thu dữ liệu | I2 đã khai | **tối thiểu 6 lượt**; kéo dài thêm lượt cho tới khi T-071 sẵn sàng (độ dài phụ thuộc tiến độ code, không phụ thuộc kết quả) |
| E3 | Chuyển khoảng: chốt ngưỡng, nạp luật, xác nhận Grafana đang đánh giá, kiểm webhook bằng một tín hiệu dương có kiểm soát **ngoài** khoảng chấm | T-071 xong ngưỡng trên dữ liệu khoảng 1 | ước 30–60 phút |
| E4 | **Khoảng 2:** luật chạy thật, đo báo giả | Đã ghi giờ luật có hiệu lực | tối thiểu 6 lượt |
| E5 | Nghiệm thu W5: tiêm lỗi, cảnh báo, RCA tự hiện | Luật W4 chạy; T-072 sẵn sàng; Q1 | 1–3 chu kỳ × ~31 phút (đã đo) |
| E6 | W6: đo thời gian khôi phục mốc DB | SPEC T-073 | chưa đo |
| E7 | Diễn tập W9a | W4, W5, W8 xong | — |

Mỗi lượt tối đa 1 giờ, nên lỗi ở 10%, 50% hay 99% chỉ mất tối đa một lượt: giữ đoạn hợp lệ và kết quả của lượt lỗi, chỉ bù lượt thiếu. Nếu trôi ở khoảng 2 buộc đổi ngưỡng hoặc khôi phục DB, giữ kết quả đầu và dùng một khoảng mới để kiểm phương án sửa (theo Codex).

### 3.5. Không làm bây giờ
- Thử tải tối đa.
- Phép tách DB khỏi code (~1 giờ 30 phút); chỉ làm nếu W6 cần.
- Sửa lõi M1 hay V082.
- Sửa bộ tải để chạy liên tục.

## 4. Prompt cho Codex — kiểm lại phản hồi và kế hoạch hợp nhất

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch hợp nhất bản 3 cho W4, W5, W6, W8 sau T-069 và phản hồi của người soạn cho bản phản biện kế hoạch bản 2, đang trong chat; nguyên văn kế hoạch:
  "Q1 W3: chấp nhận ô tụt CPU-BOOK-1 như ngoại lệ ghi rõ, dùng V082 cho demo (WHY-102). Q2 đồng bộ ngày sự kiện ticket_db/payment_db +14 ngày, không gấp, làm ngay trước khi chụp mốc DB, dump dòng cũ, kiểm đúng 1 dòng. Q3 chụp dump DB sau Q2 ở trạng thái hiện tại (~40k đơn) làm mốc; W4 không khôi phục giữa lượt (đo trôi); cách và thời gian khôi phục vào SPEC W6. Q4 tải nền W4 = chuỗi lượt 1 giờ (giới hạn tai_linux.py 3600 s, hệ số 1–3, một bậc), phần lớn ×1 đều, một số lượt ×1 rồi ×3 ở phút 40 (--buoc-tai 2400), lịch, tỉ lệ flash và tiêu chí giờ khỏe khai trước. Q5 hoãn thử tải tối đa; NV1 SPEC riêng nếu giao. Q6 W8 mức demo tối thiểu. Q7 phiên điều phối giữ T-069: dòng đính chính hash SHA256SUMS vào LOG, commit trừ 3 raw.json, Minh chọn có đưa docs/STATE.md, gửi Codex prompt LOG phiên 3. Q8 phiên điều phối soạn bản nháp báo nhóm FlashTicket về truy vấn quét tuần tự. Phiên: điều phối (giữ lịch exp-app, chốt hợp đồng I1–I5, soát chéo SPEC, gom câu hỏi); nen-w4 T-070 W4a (Q2, chụp mốc, chuỗi lượt hai khoảng, ghi số dòng DB gồm keycloak_db, CPU PostgreSQL, chuỗi lỗi/p95/liveness theo nhịp luật, phân loại giờ khỏe; sở hữu duy nhất exp-app và máy tải); luat-w4 T-071 W4b (luật provisioning/alerting, quy tắc gom, script chấm trên dữ liệu đã lưu, thử trước trên lượt 1 giờ T-067 và ca khỏe T-069, bộ nhận webhook nhẹ, tiêu chí báo giả); rca-w5 T-072 W5 (bộ xuất theo cửa sổ bất kỳ gồm R9, G1 0.3 mang t̂/luật/tín hiệu, bộ điều phối, đo thời gian trên dev rồi khai N phút, nghiệm thu D3 với lõi nhận dữ liệu [t̂−300, t̂) và [t̂, t̂+300); chọn bản demo chờ Q1); danh-gia-w6 T-073 W6 (khóa bản, D14, ma trận ô, baseline, runner W7 đóng gói đầu vào không phụ thuộc đầu ra P7, kiểm soát DB gồm mốc, khôi phục, trộn thứ tự ô, điểm yếu chấm z là ứng viên, kiểm hạn bán 02/12); llm-w8 T-074 sau Q6. Hợp đồng: I1 bản ghi cảnh báo gồm t̂, mã luật, nhãn và giá trị tín hiệu, giờ webhook tới lưu riêng, chế độ (b) không đọc sổ tiêm; I2 lịch tải và giờ khỏe theo tiêu chí độc lập từ k6 và backend, báo giả tính theo sự cố sau gom trên giờ khỏe, báo riêng theo mức tải, ngưỡng chấp nhận Minh duyệt (đề xuất ≤ 1 sự cố mỗi 6 giờ khỏe ×1, flash báo riêng); I3 không truy vấn Prometheus nặng trong khoảng đo; I4 thay đổi Grafana chỉ ở khoảng chuyển, ghi giờ luật có hiệu lực; I5 chỉ nen-w4 phát lượt. Thứ tự exp-app: E1 Q2 + chụp mốc; E2 khoảng 1 tối thiểu 6 lượt, kéo dài tới khi T-071 sẵn sàng; E3 chuyển khoảng: chốt ngưỡng, nạp luật, xác nhận đánh giá, kiểm webhook bằng tín hiệu dương có kiểm soát ngoài khoảng chấm; E4 khoảng 2 tối thiểu 6 lượt; E5 nghiệm thu W5; E6 đo khôi phục DB cho W6; E7 diễn tập W9a. Lỗi mất tối đa một lượt; trôi buộc sửa thì giữ kết quả đầu, kiểm sửa trên khoảng mới. Không làm bây giờ: thử tải tối đa, phép tách DB khỏi code, sửa lõi M1/V082, sửa bộ tải."
- Công đoạn: người phản biện kiểm lại phản hồi và sửa.
- Gói/cổng: kế hoạch giai đoạn 2 §8, chuẩn bị G6; đề xuất ngoài task.
- Người làm và người phản biện chính thức: ngoài task; người soạn Claude (phiên điều phối), người phản biện dự kiến Codex.
- Tài liệu gốc: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8; docs/STATE.md; tasks/T-069-v082-ban-ghim/SPEC.md và LOG.md (phiên 1–3); results/T-069/dinh-chinh-1.md, results/T-069/phan-tich-nguyen-nhan.md, results/T-069/phan-tich/ (gồm troi-trong-luot.txt, kiem-db.txt); docs/WHY.md WHY-102; docs/DECISIONS.md mục T-069; SPEC và LOG của T-043, T-059, T-066, T-067, T-068 theo phần liên quan.
- Phản biện và phản hồi trước: bản phản biện kế hoạch bản 2 của Codex (chat, Minh chuyển); phản hồi của người soạn trong chat (cùng lượt với kế hoạch bản 3).
- Code và kết quả liên quan: results/T-069/ (SHA256SUMS, SHA256SUMS-2); D:/Project/flashticket-rca-lab commit 407b4f5 (load/controller/tai_linux.py, load/scenarios/purchase-journey.js, campaigns/runner/, observability/grafana/); D:/Project/flash-ticket-platform revision 36a3725d (services/payment-service FinanceServiceImpl, PaymentWorker; services/ticket-service TicketService; services/booking-service OrderExpiryWorker, OrderRepository).
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
```

```text
Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.
```

`docs/review-prompt.md` chưa có khối trọng tâm cho cổng G6, nên prompt không có khối cổng.
