# T-063 — Bổ sung quan sát, B16 bản 2 và thu dữ liệu phát triển bản 2

- **Trạng thái:** đã duyệt (13/11/2026, Minh duyệt tổng thể gói chiến dịch: "tổng thể đề xuất đã ổn …").
- **Người làm:** Claude. **Người phản biện:** Codex.
- **Bổ sung đã duyệt 13/11/2026:** áp dụng phần bổ sung cuối file về phụ thuộc, thu dữ liệu và tiếp tục nhiều ngày. Căn cứ ở `docs/DECISIONS.md`, mục “Bổ sung quyền điều phối chiến dịch nhiều ngày”.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 1a, 1b (phần quan sát), 3 (ô phát triển), chuẩn bị chặng 4. Hồ sơ chiến dịch: `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`.

## Mục tiêu

Làm cho dữ liệu FlashTicket đủ và giàu cho các hướng H1–H8 của T-064, rồi thu **một đợt** dữ liệu phát triển trên tải có mua vé. Nguyên tắc kế hoạch giai đoạn 2 §1: dữ liệu đủ trước, phương pháp sau. Task là cài đặt + mô tả + phân xử cơ chế ở vài điểm (span gốc, CPU-BOOK, ca nền); không đánh giá phương pháp.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép kiểm | Kết quả có thể | Quyết định phụ thuộc |
|---|---|---|---|
| Span gốc nào là hợp lệ, span nào mất ngữ cảnh? | Phân loại trên 9 ca T-062 và trên tải mới: gốc hợp lệ theo B16 §3 (job) / điểm vào / có mã cha nhưng thiếu bản ghi / chưa phân xử; đọc thuộc tính span trong `raw-traces.jsonl` (câu lệnh, luồng, thời điểm) | Cho phép "chưa phân xử" kèm bằng chứng thiếu | Bổ sung instrumentation ở đâu |
| CPU-BOOK lan chậm do tranh CPU hay do phụ thuộc? | CPU từng container ở nền và lúc lỗi (từ `_metric-bo-sung` trước, đo thêm nếu thiếu), throttling khi đã thu | Xác định / chưa phân xử | Cường độ ô CPU (giảm là **ứng viên**, không chốt trước) |
| 3 ca bình thường bị cờ do đầu dò (H1) hay ngẫu nhiên (H3)? | Thời gian độc quyền E1 theo từng 10 s bằng code M1 trên `method-input.json`; thêm mốc dời | H1 / H3 / chưa phân xử | Lịch đầu dò của bộ chạy mới |
| Dữ liệu cần cho từng hướng H1–H8 đã có trong gói ca chưa? | Bảng hướng → tín hiệu → có trên kho? → có trong gói? | Đủ / thiếu | Điều kiện đóng băng |
| R-04, R-09, R-05, R-07 trên tải giao dịch? | Chạy lại `results/T-062/kiem-du-lieu/kiem-r.py` (bản mở rộng) | Đạt / thiếu / chưa phân xử | Điều kiện đóng băng |

## Đầu vào

`results/T-062/` (9 ca, `ca/_metric-bo-sung/`, `chay/runner.py`, `kiem-du-lieu/kiem-r.py`, `tiem-loi/`, `chay/thu-gia/LAN-CA-NEN.md`, `viec-cho-duyet.md`); tải mới từ phụ lục 2 T-062; `results/T-059/danh-muc-loi.json`; B16; `results/T-058/so-khac-phuc.md` (KP-19 cách A); M1 bản P7 trên `exp-obs` (`/opt/flash-ticket-rca`, script ghim T-058 — chỉ dùng, không sửa).

## Đầu ra (`results/T-063/`)

- `dieu-phoi/`: script gọi Codex, cách nhận biết hết hạn mức, tiến trình chờ, biên bản thử "hết hạn → chờ → gọi lại".
- `span-goc/`: bảng phân loại, cơ chế từng nhóm, đề xuất và kết quả bổ sung instrumentation.
- `cpu-book/`, `ca-nen/`: phân tích theo bảng trên; chú thích thao tác nền cho 9 ca cũ.
- `quan-sat/`: bảng hướng → tín hiệu; thay đổi Collector (cách A), Prometheus (retention, scrape), metric mới (throttling, queue ready/unacked, pool), log hạ tầng; `thay-doi-may.md`.
- `b16-ban-2.md`: tự phản biện B16 theo ba nhóm (thiếu đặc tả / đặc tả có mà triển khai chưa đạt / chưa xác định cơ chế), đối chiếu tài liệu chính thức OTel, Spring, Grafana, Prometheus (dẫn nguồn), đề xuất bản 2 không phụ thuộc cách chạy (Docker hay K3s). Là **tài liệu đề xuất** cho Minh; không tự đưa vào repo FlashTicket.
- `dong-goi/`: bộ đóng gói mở rộng (thêm metric cần cho H1–H8, xuất ngay sau mỗi chu kỳ), wrapper phục hồi khi M1/stage lỗi (stage lại cùng `t` với mã mới, giữ lần cũ), kiểm đúng tình huống thư mục đã tồn tại.
- `o-dev-bo-sung.md` (+ `.json`): ô dev mới cho pool, queue, "chết im", "tải tăng kèm lỗi" — vị trí khác ô đánh giá T-059; cách tiêm, đầu dò độc lập, tập chấp nhận, điều kiện xác nhận.
- `dong-bang.md`: commit, image digest, kịch bản tải, cấu hình Collector/Prometheus, hash.
- `chay/`: bộ chạy bản 2, `HO-SO-LUOT.md` (luật 21: lỗi ở 10/50/99%), sổ tiêm lỗi có hash nối dòng, nhật ký, xác nhận can thiệp từng ô.
- `ca/<mã mờ>/`: gói ca, đầu ra P7 (hai lần, trùng SHA); `manifest.json`.
- `bao-cao.md`.

## Phạm vi ghi

`results/T-063/`; `tasks/T-063-quan-sat-thu-dev-2/`; dòng T-063 trong `docs/STATE.md`; `docs/WHY.md` và `docs/DECISIONS.md` theo quyền ở `CHIEN-DICH-M1-FT.md` mục 6; nhánh `rca/quan-sat-log` của repo FlashTicket (instrumentation, `deploy/rca-test/`, `deploy/observability/`, cấu hình — **không** code nghiệp vụ); `exp-app`; phần Collector/Prometheus của `exp-obs`. Việc cần mật khẩu giao Codex.

## Các bước (phụ thuộc thật)

1. `dieu-phoi/` — không phụ thuộc. Kiểm: một lần thử gọi lại thành công.
2. Phân tích trên dữ liệu cũ (span gốc, CPU-BOOK, ca nền, bảng tín hiệu) — không phụ thuộc, 0 giờ máy.
3. Tăng retention Prometheus và thêm metric còn thiếu trên `exp-obs` — không phụ thuộc; làm sớm. Kiểm: cờ retention mới, metric mới có mẫu.
4. B16 bản 2 — sau bước 2.
5. Collector cách A, instrumentation (span bọc lượt outbox Keycloak, tên queue…) trên `exp-app` — sau khi L1 xong phần `exp-app`. Kiểm: log đủ sau khi tạo lại container; span mới có trong Tempo.
6. Bộ kiểm R trên tải giao dịch — cần phụ lục 2 T-062.
7. Bộ đóng gói mở rộng + wrapper; chốt lịch đầu dò (ngoài cửa sổ phương pháp hoặc đối xứng, theo kết quả bước 2).
8. Ô dev bổ sung: cài cách tiêm + đầu dò.
9. Đóng băng → xác nhận can thiệp từng ô (2–5 phút/ô) → hồ sơ lượt → thu một đợt → băm.

## Kiểm đúng đắn

Mỗi tín hiệu mới: có mẫu trong cửa sổ, đúng thành phần, đơn vị hợp lý (soi giá trị trung gian). Gói ca: đếm span/log/metric theo service, so với gói T-062. P7 chạy hai lần trùng SHA. Can thiệp: đầu dò độc lập xác nhận; không xác nhận thì ô bị loại khỏi tập chọn, giữ bản ghi. Cách ly nhãn: bộ đọc M1 không thấy sổ tiêm lỗi.

## Tiêu chí xong

Mỗi hướng H1–H8 có tín hiệu cần thiết trong gói ca, hoặc ghi rõ thiếu gì, vì sao không bổ sung được. Đợt thu chính xong, băm, có đầu ra P7 từng ca. Ba câu hỏi cơ chế có kết luận hoặc "chưa phân xử" kèm bằng chứng thiếu. Không nhận là đã đánh giá phương pháp.

## Không làm

Không chọn, không chỉnh M1 (việc của T-064); không dùng ô đánh giá; không sửa code nghiệp vụ; không merge/push `main`; không chạm máy 84.

## Chi phí ước lượng

Chưa kiểm: chuẩn bị 3–4 ngày; đợt thu 14–16 chu kỳ × 30 phút ≈ 7–8 giờ máy (đã báo Minh, đã duyệt). Thu bổ sung/thu lại: theo `CHIEN-DICH-M1-FT.md` mục 6.

## Rủi ro và điều chưa chắc

Chưa kiểm: metric throttling lấy từ nguồn nào trên ARM; `rabbitmq_message_current` có tách queue/trạng thái; span bọc `OutboxDrainerTask` có làm được từ SPI mà không sửa Keycloak; truy vấn nặng có thể làm Prometheus khởi động lại (đã xảy ra 12/11 19:16Z, xem `results/T-062/ca/_metric-bo-sung/SU-CO.md`) → luôn cắt khúc truy vấn.

## Bổ sung đã duyệt — phụ thuộc và tự chủ, 13/11/2026

Phần này cụ thể hóa và thay thế phụ thuộc chờ toàn bộ L1 ở bước 5, thứ tự một chiều của các bước 5–9 và cách xử lý ô chưa xác nhận ở mục “Kiểm đúng đắn”. Nội dung trước bổ sung giữ làm lịch sử.

- Điều phối, phân tích dữ liệu cũ, retention, thiết kế đóng gói và chuẩn bị ô dev làm song song khi độc lập. M0 chưa xong chỉ giới hạn khả năng khẳng định cơ chế tự phục hồi đã được kiểm, không chặn các việc độc lập đã cấp quyền.
- L2 nhận từng đầu ra L1 đã kiểm. Thay đổi container/cấu hình trên `exp-app` được phối hợp từng lượt. Có một giao dịch chạy trọn thì kiểm R-04/R-09 trên giao dịch đó, tự sửa thiếu hụt quan sát trong quyền rồi kiểm lại phần chịu ảnh hưởng. R-05/R-07 được hoàn thiện tương ứng.
- Trước lượt thu chính, xác nhận trên cùng cấu hình cuối các phần tải, quan sát, đóng gói, phục hồi và lịch đầu dò. Ghép revision, image, workload và cấu hình vào hồ sơ đóng băng, xác nhận can thiệp từng ô rồi thu. B16 bản 2 tiếp tục được hoàn thiện song song, những bổ sung quan sát cần cho H1–H8 phải có trước khi thu phần sử dụng chúng.
- Ô có can thiệp chưa được đầu dò xác nhận giữ ngoài tập chọn trong thời gian chẩn đoán. Agent sửa cơ chế tiêm, cấu hình hoặc đầu dò trong quyền rồi xác nhận lại. Nếu vẫn chưa xác nhận được, báo bằng chứng thiếu, tác động tới hướng nghiên cứu và phần thực sự cần quyền bổ sung. Không dùng trạng thái này để tự đóng phần còn thiếu của H1–H8.
- Claude tự quyết xuất bù, thu bổ sung hoặc thu lại phần cần thiết cho H1–H8 hoặc phần bị sai, sau khi kiểm dữ liệu và checkpoint đã có. Ghi lý do, phạm vi, chi phí và giữ các lượt cũ. Quyền lượt dài theo hồ sơ chiến dịch và hồ sơ luật 21 đã duyệt. Mỗi ca một lần thu chính, việc chạy lặp để sau.
- Một nhánh bị chặn thì tiếp tục nhánh độc lập. Báo cáo sáng và các mốc chuẩn bị 3–4 ngày chỉ cập nhật tiến độ, công việc tiếp tục tới mục tiêu đã giao trong quyền.
