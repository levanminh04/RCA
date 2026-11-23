# Những gì Claude và Codex đã thống nhất; điểm còn mở

Ghi 20/11/2026 bởi phiên Claude điều phối cũ (trước khi Minh đổi account). Nguồn nguyên văn ở `lich-su/` (02–13). Sửa lần 1 (20/11, Minh duyệt) theo lượt Codex soát gói (`12`) và phần đáp (`13`): câu W7 hạ xuống ứng viên; trình ba phương án tải; giới hạn câu về nhãn gateway. Codex `12` đồng tình giữ: hai lượt dán để tự soát trước; Q1 là ngoại lệ demo chờ Minh; Q2 theo giá trị đích; Q5 hoãn; Q6 mức demo; Q7 tách lượt kiểm và nghiệm thu T-069.

**Thống nhất** ở đây nghĩa là Claude và Codex cùng ý kiến ở vai trò người soạn và người phản biện. Đó **không phải** là Minh đã duyệt. Mọi quyền tạo task, sửa dữ liệu, chạy máy, bật lịch, nghiệm thu và commit vẫn chờ Minh.

**Kế hoạch hiệu lực** = mục "2. Kế hoạch điều phối bản 4" trong `lich-su/08-claude-ke-hoach-ban-4.md`, **cộng các sửa ở mục 1 dưới đây**. Khi hai nguồn lệch nhau, mục 1 thắng.

## 1. Đã thống nhất

### 1.1. T-069

| Nội dung | Nguồn |
|---|---|
| Hồ sơ chuẩn là `results/T-069/dinh-chinh-1.md` và LOG phiên 3. Kết luận W3: một ô tụt vượt ngưỡng và tái lập (CPU-BOOK-1 1 → 3 ở lượt chính và lượt lặp); D1–D5 không kích hoạt. Bước xếp hạng giải thích được (điểm z một mẫu max chia IQR trên kênh op gộp). **Nguồn sinh mẫu đuôi là ứng viên, chưa phân xử:** DB lớn, code đường mua vé đổi, tranh chấp CPU, dao động mẫu đuôi. Câu "DB là nguyên nhân gốc" trong `phan-tich-nguyen-nhan.md` đã bị đính chính | `dinh-chinh-1.md` §1–2; `07` Q3 |
| P7, V060, V061, V066, V082 cùng hạng trên 3 gói đã so (`phan-tich/bien-the/hang.txt`), nên thành phần riêng của V082 không gây ra và cũng không sửa được việc đổi hạng | `dinh-chinh-1.md` §4; `07` Q1 |
| **Q1 (chờ Minh):** đề nghị duyệt ngoại lệ dùng V082 cho demo, công khai CPU-BOOK-1. Câu "không bản nào tốt hơn" chỉ đúng cho 5 bản đã thử trên các ca đã kiểm. Ca nghiệm thu W5 khai trước, giữ kết quả lần đầu kể cả khi trượt. Kết luận khoa học về nguyên nhân vẫn mở | `07` Q1; `08` §1; `09` Q1 |
| **Q7 (chờ Minh):** chỉ một phiên giữ T-069. Nối dòng đính chính hash vào LOG: `410d9923…` (ghi ở bước 9) là danh sách khi nhật ký máy dừng ở M11; bản cuối thêm M12, M13 và dòng kiểm DB chỉ đọc. Thứ tự: gửi Codex kiểm lại kết quả (prompt ở `tasks/T-069-v082-ban-ghim/LOG.md`, mục "Prompt cho Codex — kiểm lại phản hồi và sửa T-069"), rồi Minh nghiệm thu, rồi duyệt file commit, rồi push. Khi commit chỉ lấy phần T-069 trong file chung (STATE chỉ dòng T-069). Ba `raw.json` (tổng 198.855.654 byte, có trong cả `SHA256SUMS` và `SHA256SUMS-2`) để ngoài Git, ghi nguồn trên exp-obs, đường đích và hash (đã có trong `thu/*/nhan.sha256`) | `07` Q7; `08` §2.7; `09` Q7 |
| Kiểm toàn vẹn: 318/318 (`SHA256SUMS`) và 348/348 (`SHA256SUMS-2`) khớp | `07`; `09` |

### 1.2. Dữ liệu hệ thống và mốc DB

| Nội dung | Nguồn |
|---|---|
| **Q2:** đồng bộ ngày sự kiện ở `ticket_db.tbl_event_access_snapshots` và `payment_db.tbl_event_finance_snapshots` **theo giá trị đích đã có ở Event/Booking** (không "+14 ngày"). Lưu giá trị cũ, kiểm đúng dòng, đọc lại hai phía. Không gấp và **không phải hạn chót phát W4**. Code dùng các ngày này cho check-in và điều kiện đối soát (`FinanceServiceImpl` dòng 195); `PaymentWorker` không có job tự trả tiền. Câu "phải làm trước 20/11 22:16Z, có thể sinh payout" (trong `04` lúc đầu và trong kế hoạch của phiên fork) là **sai** | `04`; `07` Q2; `08`; `09` Q2 |
| **Q3:** chụp mốc DB **sau Q2**; ghi thời điểm, số dòng thật và trạng thái giao dịch/hàng đợi/mock lúc chụp. W4 **không** khôi phục DB giữa các khoảng (để DB tích lũy và đo độ trôi). W6 mới kiểm việc khôi phục có tái lập được điều kiện không. Bỏ lập luận "mốc nhỏ hơn = xóa dữ liệu", vì có thể dựng mốc nhỏ trên một bản sao riêng nếu cần phân xử | `07` Q3; `09` Q3 |
| Số đo hiện có: `tbl_orders` 40.069 dòng lúc 02:31Z 20/11 (hoàn tất 26.166, hủy 6.586, hết hạn 7.317). Truy vấn nền chậm dần trong lượt chính T-069 (worker hết hạn đơn p50 18,5 → 26,5 → 31,0 ms; giao vé 18,3 → 26,9 → 31,2 ms; `results/T-069/phan-tich/troi-trong-luot.txt`). Con số "+41,5%" chỉ là của riêng `tbl_orders` và **chưa** nói gì về p95 route hay số cảnh báo | `04`; `05` (Codex bản 2) |
| *(Trả lời của Claude cho Minh, Codex chưa đồng tình riêng)* Khôi phục DB **có thể** là sửa kết quả nếu chọn sau khi xem kết quả, áp không đều, hoặc chọn theo lợi cho một phương pháp. Hợp lệ khi khai trước, áp đều, không chọn theo kết quả, và báo cáo cả hiện tượng trôi | `04` mục 5 |
| **Ứng viên, chưa thống nhất:** W7 khôi phục DB về mốc trước đợt và trộn thứ tự ô là **đề xuất của Claude** (`04` mục 5), để W6 trình Minh. Codex chỉ đồng tình chụp mốc sau Q2, giữ DB tích lũy qua W4 và để W6 kiểm khả năng tái lập (`07` Q3; `12`) | `04`; `07`; `12` |

### 1.3. W4 (nền và luật cảnh báo)

| Nội dung | Nguồn |
|---|---|
| Nền là hệ thống có tải bình thường, không tiêm lỗi; để im không dùng được. **"Không tiêm" ≠ "khỏe"**: giờ khỏe phải đạt tiêu chí độc lập (k6: hành trình xong, `dropped_iterations`, 429, lỗi HTTP; cộng kiểm backend) | `02`; `05`; `07` |
| Bộ tải: mỗi lượt tối đa 3600 s (`tai_linux.py:340`, `purchase-journey.js:18`); hệ số 1–3; một lần tăng bậc mỗi lượt. Tăng bậc chỉ được khi `minRefreshRemaining > step + 60` (`tai_linux.py:234`); 24/24 lượt T-069 có 1784–1787 s. **Bậc ở phút 40 (cần > 2460 s) không chạy được** | `05`; `07` Q4; `08` |
| **Q4:** lượt ×1 dài 60 phút, xen lượt flash 1800 s tăng lên ×3 ở 600 s (đúng cấu hình đã chạy khỏe, ca `124242f0`). Lịch lượt, số phút khỏe cần thu theo từng mức tải, quy tắc biên, mất dữ liệu, quota và suy giảm thật đều khai trước. Flash chỉ mô tả (số sự cố, thời gian quan sát), không có tiêu chí đạt/trượt | `07` Q4; `08` §2.3; `09` Q4 |
| Liveness phân biệt ba trạng thái: dò tốt, dò lỗi, thiếu hẳn lần dò. `httpcheck_error` chỉ có chuỗi khi có lỗi | `06` N7; `07` |
| Không mặc định việc cấp phiên đăng nhập mới làm bảng Keycloak tăng, cũng không áp hệ số ×3 cho cả DB. Các điểm này chỉ là lý do để đo | `07` Q4, Q8 |
| **E2:** tập dữ liệu chọn ngưỡng và ngân sách **cố định trước khi phát**. Không kéo dài theo tiến độ viết luật; luat-w4 chậm thì nen-w4 dừng ở ngân sách đã duyệt, luat-w4 dùng dữ liệu đã xuất | `07` mục "Ba chỗ cần sửa" 1; `08` §2.4 |
| **E3/E4:** chỉ tính khoảng 2 sau giờ luật thực sự có hiệu lực (ghi lại giờ đó). Kiểm webhook bằng một tín hiệu dương có kiểm soát, **ngoài** khoảng chấm. Ghi riêng: mất quan sát, chuyển lượt, tải bị giới hạn, suy giảm thật. Nếu trôi buộc đổi ngưỡng hoặc khôi phục DB, giữ kết quả lần đầu và kiểm bản sửa trên một khoảng mới | `05`; `07`; `08` §2.4 |
| Ngưỡng "≤ 1 sự cố mỗi 6 giờ khỏe ×1" chỉ là **ứng viên vận hành**, Minh duyệt trong SPEC | `07`; `08` |
| Phân tích nặng chỉ chạy trên dữ liệu đã xuất riêng; Prometheus đang phục vụ đo nền có thể quá tải kể cả khi truy vấn đoạn lịch sử | `07` I3–I5; `08` I3 |
| Một chủ theo khung giờ cho exp-app, máy tải AWS, Grafana và phần exp-obs chịu tải. Thay đổi Grafana chỉ ở khoảng chuyển. Code đang phát triển ở nhánh hoặc checkout riêng (bộ tải đòi `/opt/rca-lab` sạch ở `load`, `campaigns`, `inventory`: `tai_linux.py:119–128`) | `07`; `08` §2.3 |
| Không cam kết giờ xong W4 khi chưa đo khoảng chuyển lượt | `05` |

### 1.4. W5, W6, W8, Q5, Q8

| Nội dung | Nguồn |
|---|---|
| **W5:** bản ghi cảnh báo tách ba mốc: t̂ (luật chuyển sang firing theo lần đánh giá), giờ webhook tới, dữ liệu lõi thực nhận. Lõi phải nhận đủ `[t̂−300, t̂)` và `[t̂, t̂+300)`, kèm liveness theo lần dò mới nhất. Đo thời gian trên dev rồi khai N phút **trước khi tiêm**. Ghi riêng: bỏ sót, thiếu dữ liệu, lỗi xử lý. Chế độ (b) không đọc sổ tiêm. Con số ~31 phút chỉ là thời lượng chu kỳ cũ, không thay cho phép đo. Khi bàn giao máy ở E5, ghi cả quyền dùng máy tải, exp-obs và Grafana nếu W5 cần. W4 có thể kiểm giao nhận webhook bằng một bộ nhận nhẹ | `05`; `07`; `09` |
| **W6:** kiểm soát DB (mốc, khôi phục, trộn thứ tự ô); đo khôi phục khi exp-app rảnh, **không nằm trên đường găng W9a**; runner W7 đóng gói đầu vào không phụ thuộc đầu ra P7 (bài học T-069 Bước 0, mục 0.8); điểm yếu "chấm theo một mẫu max trên kênh gộp" là ứng viên chưa kiểm; kiểm hạn bán (02/12). Task W6 giữ mức **High**; nếu sai lặp lại hoặc tăng mức có vẻ không giúp, đưa ví dụ để Minh quyết | `05`; `07`; `09` |
| **W8 (Q6):** mức demo: giải thích từ gói bằng chứng, dẫn lại tín hiệu, gợi ý bước xử lý, được trả lời "không đủ bằng chứng", không đổi thứ hạng RCA. Chất lượng giải thích trên nhiều ca là câu hỏi riêng. Cần chỉ rõ ai giữ phần code chạy được trong repo lab | `07` Q6; `09` |
| **Q5:** hoãn thử tải tối đa. Bộ tải chỉ tới ×3. PSI `some avg60` là tỉ lệ thời gian tác vụ chờ CPU, **không** phải mức dùng CPU hay công suất còn dư. NV1 vẫn mở, cần SPEC riêng nếu Minh giao | `05`; `07`; `09` |
| **Q8:** Claude soạn bản nháp báo nhóm FlashTicket về các truy vấn quét tuần tự, có số đo và giới hạn quy nguyên nhân; Minh gửi | `07`; `09` |

### 1.5. Khôi phục sau gián đoạn và tính độc lập

| Nội dung | Nguồn |
|---|---|
| "Lỗi chỉ mất tối đa một lượt" chỉ đúng với lỗi cục bộ. Sai nguồn chung, sai luật, mất telemetry nhiều giờ có thể hỏng nhiều lượt. Với một khoảng 7 giờ, lỗi nguồn chung phát hiện ở 10%, 50%, 99% ảnh hưởng 42 phút, 3 giờ 30 và gần 6 giờ 56 đã thu; mất kết nối khi nhận file mà nguồn còn nguyên thì 0 phát lại | `07`; `09` CHẶN 2 |
| Trước khi phát lại: kiểm tag, container, log, manifest trên server, rồi nhận lại đầu ra. **Không gọi lại nguyên lịch** (runner sinh mã ca mới, `runner4.py:249`); chỉ bù phần thiếu bằng lịch con | `07`; `08` §2.6 |
| Laptop mất mạng không mất lượt nào nếu việc đã giao cho server: lượt lặp T-069 xong 4/4 khi bộ theo dõi trên laptop thoát mã 4 | `07`; `09` |
| Lượt N1–N10 của Claude (`06`) **không** độc lập (Claude đã đọc phản biện trước). Phiên mới tự soát trước, rồi mới đọc phản biện | `09`; `10` |

### 1.6. Không làm bây giờ
Thử tải tối đa; phép tách DB khỏi code (~1 giờ 30 phút, chỉ khi W6 cần); sửa lõi M1 hay V082; sửa bộ tải; bật lại lịch M1 cũ.

## 2. Còn mở: ba điểm Codex CHẶN ở bản 4 (Claude chưa đáp chính thức)

1. **Lịch tự tiếp nhận.** Phải trình hai nhánh:
   - Phiên chủ còn chạy: báo đúng mã việc và phát việc độc lập đã đủ điều kiện.
   - Phiên chủ đã dừng: phiên tiếp nhận (Minh cho phép) kiểm chủ cũ và các lệnh nền, nhận quyền điều phối đúng một lần, tiếp tục từ checkpoint.

   Nếu ứng dụng, mạng hoặc usage không cho tiếp nhận, báo Minh kèm bước khôi phục. `list_task_runs` chỉ xác nhận lịch đã chạy, không xác nhận đã tiếp nhận. (`09` CHẶN 1)
2. **Ai chạy lượt kế tiếp khi laptop mất mạng.** Giao cả danh sách lượt đã duyệt của E2 (hoặc E4) cho một tiến trình trên server; ghi mã từng lượt trước khi phát. E3 vẫn là bước khóa ngưỡng riêng. SPEC tính chi phí theo luật 21. (`09` CHẶN 2)
   - **Ba phương án, chưa chọn; phiên điều phối mới trình Minh** (đã sửa theo Codex `12`; trước đó `10` ghi phương án B như đã giải xong):
     - **(A) Chuỗi lượt 60 phút như bản 4:** 6 lượt ×1 × 3600 s + 2 lượt flash 1800 s (bậc 600 s) = 8 lượt, 380 phút ×1 và 40 phút ×3 theo tải danh nghĩa. **Chưa có tiến trình trên server chạy cả chuỗi:** `tai_linux.py` chỉ phát từng lượt, nên cần laptop phát từng lượt hoặc một script mới (phải có SPEC).
     - **(B) `runner4.py` với `RCA_PHASE=600`:** lịch gồm 12 ô `BINH-THUONG` + 2 ô `FLASH-HEALTHY`, chu kỳ 30 phút (`runner4.py:155`: tải `3 × PHASE`; flash tăng bậc ở `PHASE` = 600 s). Runner chạy cả danh sách trên server, ghi mã ca vào sổ trước mỗi chu kỳ, đã đo 31,3 phút/chu kỳ. Cùng tổng phút tải như (A) nhưng **14 lượt thay vì 8, thêm 6 lần chuyển lượt** (biên bị loại khỏi giờ khỏe). Runner vẫn chạy đầu dò `inj3` và **xếp M1 (P7, V082) lên exp-obs trong lúc đo** (`runner4.py:275`); muốn tắt phải sửa code.
     - **(C) `runner4.py` với `RCA_PHASE=1200`:** lượt ×1 dài 3600 s (6 lượt như A, chạy trên server). Lượt flash khi đó tăng bậc ở 1200 s, vẫn qua điều kiện token (1784 > 1260), nhưng chạy **×3 trong 40 phút — cấu hình chưa từng chạy**, khác cấu hình flash đã thống nhất. Vẫn có M1 và đầu dò như (B). Một lần gọi runner chỉ có một `RCA_PHASE`, nên muốn trộn hai cấu hình phải gọi runner hai lần.
3. **Dữ liệu và mẫu số W4.** W4 cần **p95 theo route tại gateway**. Bộ xuất M1 có p50/p90 theo service; bộ xuất bổ sung có lưu lượng và 5xx theo route; chưa dựng lại được p95 theo route. Trước E2: T-072 (luật) chốt biểu thức, nhãn, nhịp đánh giá, khoảng nhìn lùi; T-071 (nền) xác nhận xuất đúng các chuỗi đó xuyên suốt hai khoảng. Mỗi khoảng có 380 phút ×1 và 40 phút ×3 theo tải thực, trước khi loại biên và thời gian thiếu quan sát. Dưới 360 phút ×1 sau loại trừ thì báo "chưa đủ sáu giờ khỏe ×1". Khai trước cách đếm sự cố vắt qua biên. (`09` CHẶN 3)
   - **Số liệu Claude đã kiểm (chưa phản biện):** Prometheus có `http_server_request_duration_seconds_bucket{service_name="api-gateway", http_route=…}`. **Trong một giờ đã truy vấn** (20/11 ~04:2xZ, cửa sổ 1 giờ), `http_route` có 7 nhóm: mã route của gateway (`booking`, `event`, `payment`, `ticket`, `user`), `/actuator/health/{*path}`, và chuỗi không có nhãn. Đây là mã route, không phải từng đường dẫn API. Độ phủ suốt E2/E4 vẫn phải giải trong SPEC. (`10`; `12`)

## 3. Mã task dự kiến (chưa cấp; kiểm lại danh mục trước khi dùng)

Trong `08` §2.2: T-070 điều phối; T-071 W4a (nền); T-072 W4b (luật); T-073 W5; T-074 W6; T-075 W8. Trong `09`, Codex nhắc "T-073" cho W5 và "T-074" cho W6, khớp bảng này. Chưa có thư mục task nào được tạo.
