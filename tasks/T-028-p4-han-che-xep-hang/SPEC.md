# T-028 — P4: hạn chế của phương pháp xếp hạng (chế độ a)

- **Trạng thái:** đề xuất (07/10/2026), chưa duyệt. Claude soạn theo yêu cầu Minh; Codex rà SPEC trước khi làm.
- **Người làm:** Codex (Minh giao 07/10/2026; `docs/PLAN-P3-G2.md:29` dự kiến Claude làm — đổi theo lời Minh, ghi LOG khi duyệt).
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** P4 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ2 (MRP §3) và yêu cầu của cô "chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có" (`docs/reference/sources/advisor-2026-09-23.md`; MRP bảng dòng 31: hạn chế phải có ca nào, phương pháp nào, cơ chế nào). Trả lời:

1. Ở chế độ (a), mỗi phương pháp tầng 1 xếp sai ở những ca nào, trên dataset nào?
2. Mỗi ca sai thuộc cơ chế nào, theo tiêu chí đo được khai trước, kèm bằng chứng từ dữ liệu đo của chính ca đó?
3. Với mỗi nhóm cơ chế: bao nhiêu ca trên tổng số, các nguyên nhân khả thi khác (Q-33), cái nào đã loại được, cái nào chưa kiểm?

Đầu ra là phần xếp hạng của bản đồ hạn chế (MRP P4). Phần phát hiện và chế độ (b) thuộc T-029. Không kết luận đồ thị có ích hay không; chỉ ghi các dữ kiện cấu trúc (quan hệ gọi, vị trí) mà P5–P6 có thể trỏ tới.

Các giả thuyết ở MRP P4 (nhầm triệu chứng lan với nguyên nhân; lỗi không hiện ở loại tín hiệu phương pháp dùng; root không có tín hiệu hoặc không có cạnh) là **ứng viên chưa kiểm**, không phải kết luận phải chứng minh. Mọi nhận xét trong các REVIEW trước (ví dụ REVIEW T-026) cũng chỉ là ứng viên, được kiểm như mọi ứng viên khác, không được ưu tiên.

## Điều kiện bắt đầu

- Phần RE2-TT (T-024 đã đóng): bắt đầu được sau khi Minh duyệt SPEC.
- Phần Nezha-OB: chỉ sau khi Minh đóng T-026. Điều kiện này đã đạt: Minh đóng T-026 ngày 07/10/2026, ghi tại `tasks/T-026-nezha-ob-che-do-a/LOG.md`, phiên 8. Nếu khi tiếp nhận không có xác nhận đóng thì dừng, ghi LOG, báo Minh; không dùng số T-026 chưa được chấp nhận.
- Eadro: không dùng (Q-83).

## Đầu vào

- Bản ghi và chấm chế độ (a): `results/T-024/cham-a.json`, `results/T-024/ban-ghi-dua-vao-cham.json`; `results/T-026/cham-a.json`, `results/T-026/ban-ghi-dua-vao-cham.json`. Bảng chính là `cohorts.dev30` (30 ca dev RE2-TT, sáu phương pháp chính) và `tables.main` (22 ca dev Nezha-OB; bốn phương pháp chạy, CIRCA/TORAI B UNSUPPORTED theo Q-85). Giữ đủ trạng thái của sáu phương pháp; UNSUPPORTED không là kết quả chất lượng xếp hạng hay bằng chứng root không có tín hiệu.
- RE2-TT: `cohorts.dev19` chỉ dùng dòng CIRCA theo Q-82/WHY-36, báo có điều kiện và giữ nhóm 11 ca lỗi đã xác nhận; không thay mẫu chính dev30, không phân tích các phương pháp khác trên dev19. Nezha-OB: các bảng `sensitivity_A`, `sensitivity_B`, `trace_guard` chỉ đọc số đã có để đánh dấu ca đổi trạng thái/Hit so với main; ca không thuộc bảng B ghi không thuộc cohort, không coi là lỗi. Không tính đặc trưng mới hoặc gán cơ chế cho các cửa sổ độ nhạy này. Dòng phụ (CIRCA RHT-only/SVR, TORAI A, MicroRank top11) chỉ đọc khi cần đối chiếu cơ chế, không tính vào bảng chính.
- TORAI: gộp Hit của seed 0, 1, 2 theo từng ca như T-024; ca là mẫu số, không coi 90 lượt là 90 ca. Giữ bằng chứng đã có theo từng seed; cách tổng hợp đặc trưng/gán khi seed khác nhau khai trong codebook trước tính.
- Nhãn dev: `results/T-022/nhan-dev.json` (RE2-TT), `results/T-026/nhan-dev.json` (Nezha-OB). Nhãn chỉ dùng để phân tích và chấm, không đưa vào phương pháp (luật cứng 6).
- Dữ liệu đo dev, chỉ đọc, qua bộ đọc có guard đã có: `src/p3/` (RE2-TT, allowlist T-022), `src/p3/nezha.py` (allowlist T-026, cửa sổ Q-63). Không mở 60 ca test RE2-TT, 34 ca test Nezha-OB, `data/locked/`.
- Vị trí root và ô: `results/T-021/vi-tri-root.csv`, `results/T-021/runs/vi-tri-001/vi-tri-theo-ca.csv`, `results/T-021/chia-theo-o/A-phan-tang.csv`.
- Hồ sơ phương pháp P1 (đầu vào, kênh, công thức): `results/T-013`–`T-017`, `docs/knowledge/K1-phuong-phap-rca.md`; giao thức `results/T-022/giao-thuc-v2.md`; WHY-22–37; Q-61–Q-85; `docs/LESSONS.md` (QT3, QT5, QT15, QT16).

## Đầu ra

Trong `results/T-028/`:
- `codebook.md`: tiêu chí đo được cho từng cơ chế, ngưỡng và các ngưỡng độ nhạy nơi có ngưỡng số tự chọn, thứ tự gán, nhãn "chưa phân loại", phép đo tập trung/biến thiên đầu ra, nháp mục WHY. **Khai và chốt trước khi tính bằng chứng theo ca** (bước 2).
- `ca-sai.json` (và `.csv` chỉ chứa mã mờ, số, nhãn cơ chế): mỗi phương pháp × dataset × ca của bảng chính: trạng thái, hạng root (khoảng hòa), Hit@1/Hit@5, cột sai hạng 1 và sai hạng 5 riêng, các đặc trưng bằng chứng, cơ chế gán, nguồn. TORAI giữ bằng chứng từng seed. Đặc trưng thiếu hoặc không áp dụng ghi N/A kèm lý do. Dòng CIRCA dev19 báo riêng có điều kiện; đánh dấu đổi trạng thái/Hit của các bảng Nezha độ nhạy chỉ từ số có sẵn.
- `ban-do-han-che-xep-hang.md`: bảng cơ chế × phương pháp × dataset (số ca/tổng), tách theo ô, loại lỗi, vị trí root; với mỗi nhóm: ví dụ ca, bằng chứng, nguyên nhân khả thi khác và trạng thái kiểm; tác giả phương pháp có tự nêu hạn chế đó không. Báo riêng rào cản kiểm trực tiếp từ pipeline và cơ chế ứng viên/chưa kiểm nhân quả; có phần schema từ audit đã có.
- `runs/<run-id>/` (mọi lượt, kể cả hỏng), `scripts/`, `chi-phi.md`.

## Phạm vi ghi

- `results/T-028/` (tạm ở `results/T-028/work/`, xóa payload trước bàn giao).
- `tasks/T-028-p4-han-che-xep-hang/LOG.md`; dòng T-028 trong `docs/STATE.md`.

Không sửa `src/`, code phương pháp, `results/T-0xx` của task khác, `docs/` (trừ dòng STATE nêu trên), `data/`, SPEC này. Riêng mục WHY của codebook: chỉ ghi vào `docs/WHY.md` sau khi Minh duyệt đúng văn bản và phạm vi ở bước 2; duyệt codebook không mặc nhiên cấp quyền sửa WHY. Python không ghi bytecode. Không đưa vào git dữ liệu dẫn xuất từ Nezha ở mức chuỗi giá trị, span hay log (Q-59); chỉ lưu thống kê tổng hợp theo ca × service × kênh và manifest (đường dẫn, số dòng, SHA-256).

## Các bước

0. **Rà SPEC, chỉ đọc.** Ghi mục "Rà SPEC" vào LOG. Có lỗi chặn thì dừng, đề xuất sửa (file, cũ → mới, lý do).
1. **Lập danh sách ca sai, chỉ từ file chấm đã có** (không chạy lại phương pháp). Với k=1,5, đếm trực tiếp số ca OK có Hit@k kỳ vọng theo hòa < 1; non-OK báo riêng theo trạng thái. Sai hạng 1 và sai hạng 5 là hai cột riêng, không cộng thành hai ca. Báo riêng tổng mức trượt kỳ vọng Σca(1−Hit@k_ca), giữ non-OK có Hit=0. Kiểm tổng này bằng n×(1−Hit@k_bảng) trên đúng cohort và quy tắc gộp seed của bảng nguồn; không đồng nhất nó với số ca sai. Bước này chỉ trích danh sách/độ đo đã chấm theo phạm vi đầu vào; chưa tính mức tập trung hoặc đặc trưng mới.
2. **Viết và chốt `codebook.md` trước khi tính bằng chứng theo ca.** Mỗi cơ chế ứng viên có: định nghĩa; đặc trưng đo được (ví dụ độ lệch A so với N của root trên từng loại tín hiệu mà phương pháp nhận; thực thể xếp trên root có là service gọi root theo đồ thị gọi dựng từ trace N của chính ca không; root có trong tập quan sát O không; hòa ở vị trí root); thứ tự gán khi một ca khớp nhiều cơ chế, và báo cả gán đa nhãn; nhãn "chưa phân loại". Với đặc trưng có ngưỡng số tự chọn: khai ngưỡng chính và ít nhất hai ngưỡng độ nhạy (QT3), có lý do. Với membership (thuộc tập), trạng thái hoặc hòa theo giao thức: dẫn quy tắc có hiệu lực, ghi N/A cho độ nhạy ngưỡng; không tự thêm tolerance đổi nghĩa hòa. Ngưỡng lấy từ N hoặc từ quy ước đã có, không chọn theo số ca rơi vào nhóm.
   - Khai đặc trưng theo đúng tín hiệu, tiền xử lý và cách chia N/A (normal/anomalous — bình thường/bất thường) của từng phương pháp trong giao thức và code đã dùng. RE2: SimpleRCA chia trace theo start; MicroRank/TraceRCA theo end; CIRCA graph N dùng end<t, cửa sổ train/test metric theo adapter. Nezha: bộ đọc lấy outer window; wrapper của từng phương pháp chia N/A, main dùng guard=0. Không lấy chung start<t làm N cho mọi phương pháp. Đồ thị/độ lệch raw là bằng chứng phân tích, không mặc nhiên là đặc trưng phương pháp thực nhận. Thiếu dữ liệu hoặc đặc trưng không áp dụng ghi N/A kèm lý do, không điền 0 hay suy thành "không hiện lỗi". Không tính đặc trưng cho các cửa sổ Nezha độ nhạy.
   - Khai phép đo mức tập trung/biến thiên đầu ra của mọi phương pháp bằng cùng một phép đo: k, đơn vị cặp ca/ô, xử lý hòa/danh sách ngắn/non-OK/seed, đối chứng và ý nghĩa kết luận. Đối chứng nêu điều kiện tập ứng viên O và chiều dài danh sách; U nếu dùng thì báo riêng, không thay đối chứng có cùng điều kiện. Phương pháp không có đầu ra xếp hạng ghi N/A. Không chọn lại phép đo theo kết quả; sự tập trung không tự chứng minh thuật toán bỏ qua dữ liệu ca.
   - Dùng `raw_column_audit` có sẵn trong `results/T-024/cham-a.json` để báo số/loại/cột vắng theo ca/ô và liên hệ với nhãn dev; đặt cạnh O/tập trả về sau tiền xử lý. Không đưa dấu cột vắng vào phương pháp, không chạy L*, không gọi liên hệ schema–root là tác động nhân quả đã tách.
   - Ghi nháp WHY trong codebook: chọn gì, vì sao, phương án đã xét, bằng chứng, kết luận phụ thuộc. Thêm dòng LOG có giờ máy: "chốt codebook". **Dừng, trình Minh duyệt codebook cùng văn bản WHY và phạm vi ghi mục tương ứng** (luật cứng 3). Chỉ sang bước 3 sau khi codebook được duyệt và văn bản WHY đã được Minh duyệt, ghi vào `docs/WHY.md`. Việc ghi WHY chỉ thực hiện khi Minh duyệt đúng nội dung và phạm vi đó.
3. **Tính đặc trưng bằng chứng cho mọi ca dev của bảng chính** (cả ca đúng để có đối chứng), và phép đo tập trung/biến thiên đầu ra đã khai ở bước 2. Đặc trưng chỉ cho RE2 dev30 và Nezha main; dòng CIRCA dev19 dùng lại bằng chứng từ dev30. TORAI giữ từng seed và tổng hợp theo codebook. Gán cơ chế không phụ thuộc vào việc đặc trưng có phân biệt được ca sai/đúng hay không; so sánh chỉ là bằng chứng liên hệ quan sát. Chạy trên RAM, chỉ ghi thống kê. — kiểm bằng: tính lại độc lập một đặc trưng mỗi loại trên 3 ca bằng mã riêng; soi giá trị trung gian theo QT5.
4. **Gán cơ chế theo codebook đã chốt**, không sửa codebook sau khi thấy phân bố. Muốn sửa thì dừng, trình Minh, giữ bản cũ và kết quả cũ.
5. **Đọc tay**: mỗi nhóm cơ chế có ≥ 1 ca, đọc kỹ tối thiểu 2 ca (hoặc toàn bộ nếu ít hơn) và mọi ca "chưa phân loại" nếu ≤ 10 ca (nhiều hơn thì lấy mẫu theo quy tắc khai trong codebook, không chọn theo kết quả). Ghi điều đọc được có khớp tiêu chí tự động không. Nếu phép tính hoặc gán không thực hiện đúng codebook: sửa triển khai trong `scripts/` thuộc phạm vi, giữ codebook và mọi lượt cũ, tính lại đúng các đầu ra bị ảnh hưởng; không chạy lại phương pháp. Nếu đã thực hiện đúng mà đọc tay chưa hỗ trợ giải thích cơ chế: giữ gán theo tiêu chí, báo cơ chế ứng viên/chưa kiểm và giới hạn codebook. Muốn đổi tiêu chí thì theo bước 4: dừng trình Minh, giữ bản/kết quả cũ.
6. **Viết `ban-do-han-che-xep-hang.md`**: tách theo ca và ô trước khi nêu mẫu hình (QT15); mẫu số luôn ghi; một ô không là mẫu hình; mỗi nhóm có mục "nguyên nhân khả thi khác" (Q-33) với trạng thái đã loại / chưa kiểm kèm lý do (Q-41). Phân biệt rào cản kiểm trực tiếp từ pipeline với cơ chế ứng viên/chưa kiểm nhân quả; báo đối chứng theo mục kiểm đúng đắn. Báo phần schema từ audit đã có theo bước 2. CIRCA dev19 và các đánh dấu đổi trạng thái/Hit của Nezha độ nhạy báo riêng theo giới hạn đầu vào, không chọn bảng theo kết quả. So sánh giữa hai dataset chỉ ở mức mô tả, kèm khác biệt cadence, U, loại lỗi, độ dài N (WHY-37).

## Kiểm đúng đắn

- Kiểm danh sách ca sai OK bằng từng Hit@k<1 trong bảng chính; non-OK tách riêng. Tổng mức trượt kỳ vọng khớp n×(1−Hit@k_bảng) theo đúng cohort/gộp seed, không dùng công thức đó để đếm ca sai. Dòng CIRCA dev19 và dấu đổi trạng thái/Hit của các bảng Nezha độ nhạy đối chiếu số có sẵn, không tính đặc trưng mới.
- Đặc trưng được tính lại độc lập trên mẫu ca; mọi số trong báo cáo có đường dẫn nguồn.
- Đối chứng ca đúng/sai: với mỗi cơ chế, báo riêng k=1,5 cùng phương pháp và bảng chính. Ca đúng là OK có Hit@k=1; ca sai ranking là OK có Hit@k<1; non-OK tách riêng. Báo tỉ lệ và mẫu số khi cả hai nhóm có ca; thiếu nhóm ghi N/A và giới hạn không có đối chứng. Chênh tỉ lệ chỉ là bằng chứng liên hệ quan sát, không là điều kiện đủ hoặc bắt buộc để khẳng định nguyên nhân. Gán theo codebook đã chốt; không chọn/bỏ cơ chế hay đổi ngưỡng theo độ phân biệt.
- Độ nhạy ngưỡng: với đặc trưng có ngưỡng số tự chọn, báo số ca mỗi nhóm ở ngưỡng chính và các ngưỡng độ nhạy; nhóm đổi lớn thì báo có điều kiện. Thuộc tính rời rạc/hòa theo giao thức ghi N/A; không thêm tolerance.
- Kiểm rò nhãn: nhãn chỉ được nối sau khi đặc trưng không cần nhãn đã ghi ra file; đặc trưng nào cần biết root (ví dụ độ lệch của root) ghi rõ là đặc trưng phân tích, không bao giờ là đầu vào phương pháp.
- Đối chiếu tác giả: hạn chế nào tác giả đã tự nêu (theo hồ sơ P1) thì dẫn nguồn.
- Không kiểm được trong task: tính đại diện cho phần test; mọi cơ chế cần chạy lại phương pháp với đầu vào khác (ghi "chưa kiểm", nêu phép thử sẽ phân xử và vì sao không làm ở đây).

## Tiêu chí xong

- `codebook.md` có dòng chốt trong LOG trước lượt tính bằng chứng đầu tiên, có lời duyệt codebook của Minh ghi trong LOG; văn bản WHY tương ứng được Minh duyệt và ghi vào `docs/WHY.md` trước bước 3.
- `ca-sai.json` parse được; phủ mọi phương pháp × ca dev × dataset của bảng chính; mỗi ca sai có cơ chế hoặc "chưa phân loại", non-OK giữ trạng thái riêng. TORAI gộp ba seed theo ca và giữ bằng chứng từng seed; thiếu đặc trưng ghi N/A kèm lý do. CIRCA dev19 và dấu đổi trạng thái/Hit Nezha độ nhạy báo riêng, đúng phạm vi đầu vào.
- `ban-do-han-che-xep-hang.md` có bảng số ca/tổng, đối chứng ca đúng/sai (N/A khi thiếu nhóm), độ nhạy ngưỡng nơi áp dụng, nguyên nhân khả thi khác cho mọi nhóm, phân biệt rào cản trực tiếp và cơ chế chưa kiểm nhân quả, phần schema dùng audit đã có; mỗi số có nguồn.
- Không mở test, `data/locked/`; không chạy lại phương pháp; không dữ liệu dẫn xuất Nezha ngoài thống kê tổng hợp.
- LOG đủ để agent khác làm tiếp; dòng STATE cập nhật; prompt phản biện cuối LOG theo `docs/review-prompt.md`.

## Không làm

Không chạy lại hay sửa phương pháp, không thử cấu hình hoặc nguồn nền mới (việc đó cần task riêng và quyết định của Minh). Không phân tích phát hiện hay chế độ (b) (T-029). Không định nghĩa nhãn "lan" chính thức (MRP P4: chỉ khi cơ chế này đáng kể, và khóa ở G3). Không kết luận về giá trị đồ thị. Không sửa DECISIONS, giao thức; WHY chỉ ghi đúng mục codebook sau duyệt riêng nội dung/phạm vi như bước 2.

## Chi phí ước lượng

**Chưa kiểm.** PLAN-P3-G2: công agent 3–5 giờ; máy 10–45 phút (đọc lại cửa sổ dev 30 + 22 ca, đặc trưng thống kê); RAM 0,5–2 GB; đĩa 0,1–0,3 GB. Không tải dữ liệu, không EC2. Có một điểm dừng chờ Minh duyệt codebook + WHY; điều kiện T-026 đóng đã đạt theo LOG T-026 phiên 8. Minh duyệt ngoại lệ hai phiên riêng T-028 ngày 07/10/2026: phiên 1 bước 0–2 đến điểm duyệt codebook + WHY; phiên 2 bước 3–6. Không tách task, không suy ngoại lệ cho task khác. Lượt nào dự kiến > 1 giờ thì báo trước và chờ Minh đồng ý.

## Rủi ro và điều chưa chắc

- Cơ chế suy từ dữ liệu quan sát là tương quan; nhiều cơ chế chỉ kiểm được bằng chạy lại có can thiệp (ngoài phạm vi) → ghi "chưa kiểm".
- Nezha-OB: metric 5 điểm mỗi phía, trace N 41–97 s, mốc tiêm và đồng hồ OPEN (Q-84); đặc trưng độ lệch trên đó yếu. RE2-TT: đồ thị gần như hằng giữa các ca (LESSONS ST3), ít root (5 service).
- Ca sai ít ở một số phương pháp, nhiều ở phương pháp khác; nhóm nhỏ không đủ nêu mẫu hình.
- Người làm và người phản biện đều đã thấy kết quả T-024/T-026; codebook chốt trước bằng chứng theo ca và phép thử phân biệt ca sai/ca đúng là cách giảm neo, không loại hết.
