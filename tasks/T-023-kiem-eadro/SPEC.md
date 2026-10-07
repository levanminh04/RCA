# T-023 — Kiểm điều kiện dùng Eadro-TT

- **Trạng thái:** SPEC đề xuất ngày 05/10/2026. Minh cho phép soạn; chưa duyệt nội dung SPEC hoàn chỉnh, danh sách phiên đọc hoặc chạy task.
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Người soạn bản nháp:** Codex theo yêu cầu Minh; chưa mở phiên kiểm dữ liệu.
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ1/RQ2 và DT18-NV3: kiểm điều kiện Q-61/Q-64 để Minh quyết Eadro dùng được phần nào. Trả lời trace có thuộc đúng phiên/cửa sổ không, và nguồn no-fault có phù hợp làm reference/control không. Không benchmark, không bắt Eadro phải đạt và không tự chọn nhánh.

## Đầu vào

- AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md Q-61–Q-70; docs/WHY.md; docs/LESSONS.md; docs/PLAN-P3-G2.md.
- Đề tài/hướng dẫn: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, advisor-2026-09-23.md.
- Thẻ và metadata cũ: results/T-009/the-dataset.md; sources/Readme.md; runs/run-001/labels.json, normal_intervals.json, inventory.json; runs/inspect-004/raw-sessions.json, nested-inventory.json, logical-member-sizes.json, validation.json.
- Nguồn tải: results/T-009/runs/download-001/manifest.json và archive-directory.json; ZIP TT đã có trong data/ngoai-rcaeval/eadro/train-ticket/.
- Bảng chia cũ chỉ dùng đối chiếu metadata: results/T-021/chia-theo-o/A-phan-tang.csv; runs/kiem-phien-001/ket-qua.json.
- Parser T-009 và code tác giả đã lưu: results/T-009/scripts/inspect_files.py; sources/codes/preprocess/align.py, single_process.py, util.py. Chỉ đọc code; không chạy inspector all-session nguyên trạng.
- Yêu cầu phương pháp trong hồ sơ T-013–T-017 để kết luận khả năng đầu vào; không chọn theo accuracy.

## Điều kiện đọc số đo: chia phiên trước

Q-63 đã chọn Eadro chia theo phiên. Tuy nhiên, bảng chia ô cũ có dev/test trong cả chín phiên fault TT; không phiên nào được mặc định mở trọn chỉ vì chứa một ca dev.

Bước metadata tạo phương án chia toàn phiên và allowlist cụ thể, trình Minh duyệt trước mọi đọc mới metric/trace/log. Không chuyển ca giữa hai phía theo kết quả số đo. Hai phiên có nhãn faults=[] là ứng viên reference/control; phiên không có nhãn vẫn OPEN.

Metadata cho thấy mỗi root nằm trong một phiên; chia phiên làm tập root hai phía khác nhau. Trình giới hạn này cùng phương án; không dùng vị trí root hoặc triệu chứng để cố cân bằng sau khi xem dữ liệu. Trong trường hợp chưa được duyệt allowlist, hoàn thành phần metadata và dừng phần telemetry; không báo phép kiểm Q-61 đã hoàn tất.

## Đầu ra

Chỉ trong results/T-023/:
1. de-xuat-chia-phien.csv và de-xuat-chia-phien.md — phiên, sự kiện, member archive, dev/test đề xuất, seed/tỷ lệ/tiêu chí và giới hạn theo root; trạng thái duyệt rõ.
2. allowlist-phien.json — danh sách phiên fault và no-fault được Minh cho đọc, provenance và phạm vi member; không tự nâng proposed thành approved.
3. ke-hoach-kiem.md — cách nhận diện session, clock/unit, bằng chứng ghép và điều kiện cần theo từng phương pháp, viết trước đọc số đo mới.
4. kiem-eadro.md và bang-dieu-kien.csv — bằng chứng theo phiên/cửa sổ/kênh; PASS/FAIL/OPEN, hệ quả và phạm vi đề xuất cho T-027.
5. de-xuat-why.md — chia theo phiên, nguồn bình thường, clock/mapping nếu cần và các lựa chọn còn cho Minh.
6. scripts/ và runs/<run-id>/ — selector/streaming inspector, kiểm độc lập, stdout/stderr, thời gian/byte/RAM khi có, bảng intermediate và manifest. Giữ lượt hỏng.

## Phạm vi ghi

Sau Minh duyệt SPEC:
- results/T-023/
- tasks/T-023-kiem-eadro/LOG.md
- dòng T-023 trong docs/STATE.md.

Không sửa SPEC đã duyệt, code/src dùng chung, task/kết quả cũ, docs/WHY.md, docs/DECISIONS.md hoặc data/README.md. Đề xuất sửa nguồn chung nằm trong results/T-023/, cần Minh duyệt riêng. Scratch/cache/tmp chỉ trong results/T-023/work/; không giải nén dữ liệu vào cây input hoặc ghi bytecode vào code cũ.

## Các bước và kiểm

0. **Tự soát.** Kiểm phạm vi đọc, nhãn metadata, archive/runtime đã có và chi phí vừa một phiên. — kiểm: LOG, danh sách OPEN; không mở archive telemetry lúc tự soát.
1. **Metadata và allowlist.** Lập phiên → sự kiện → member từ manifest/nhãn đã lưu; trình phương án chia toàn phiên và reference/control cho Minh. — kiểm: 81 sự kiện TT, 27 root × ba loại lỗi, chín phiên fault theo metadata; mỗi phiên ở một phía; không dùng CSV chia ô làm quyền đọc raw.
2. **Selector trước inspector.** Sau Minh duyệt danh sách cụ thể, selector chỉ stream member thuộc allowlist; xác minh hash/identity theo nguồn cũ và nested duplicate. — kiểm: fixture từ chối test, phiên không có quyền và member không xác định được phiên. Không tự last-wins hoặc sửa input.
3. **Kiểm trace–phiên–mốc.** Ghi timestamp native và unit; coverage theo toàn phiên dev được phép và từng cửa sổ Q-64. Đối chiếu trace/span ID có scope và log “Span reported” nếu có để phân biệt offset clock với trace export lịch sử. — kiểm: distribution chênh thời gian, identity match và lý do alternate; trùng tên file hoặc min/max giao nhau không đủ để kết luận khớp.
4. **Kiểm cấu trúc identity.** Exact-copy, conflict, orphan và ambiguous parent sau xử lý đúng policy, theo từng phiên/cửa sổ. — kiểm: đếm độc lập; lưu conflict, không gộp ID khác nội dung. Root thiếu trace không tự thành service cô lập.
5. **Kiểm no-fault.** Reference/control khác phiên nếu có quyền; kiểm service/kênh, cadence, missing, hằng, warm-up, drift/load và sample coverage. — kiểm: toàn bộ phần bình thường được phép; không chọn reference theo root accuracy. Nhãn faults=[] không tự chứng minh normal sạch.
6. **Kết luận theo chức năng.** Nêu trace/metric/log/normal dùng được với phương pháp nào, giả định chưa xác minh và thiếu schema gì. Trình Minh: đủ điều kiện → phạm vi T-027; không đủ/OPEN → metric/log hoặc bỏ. — kiểm: từng kết luận có bảng bằng chứng và giới hạn, không mặc định chạy mọi phương pháp.
7. **Bàn giao.** LOG đủ tiếp nhận; thống kê chi phí thực; cập nhật dòng task chờ phản biện khi đủ. Prompt phản biện kết quả cho Claude theo mẫu repo. — kiểm: file set, selector log và kết luận không mở test.

Bước 1 có thể cùng lúc với phần đọc/soạn T-022. Bước 3–5 có thể dùng cùng một lượt streaming để tránh đọc archive lặp, nếu vẫn lưu riêng bằng chứng. Không parsing nặng cùng lúc đo pilot cost T-022; chi phí ghi là quan sát nếu máy có việc khác.

Để giao kiểm số đo lúc Minh ngủ, hoàn tất đề xuất chia phiên/reference/control và được duyệt allowlist trước đêm chạy. Điểm chờ sau bước 1 là phụ thuộc lịch thật; khi chưa có duyệt thì chỉ làm metadata/chuẩn bị độc lập, không tự sang telemetry. Thời gian chờ này không nằm trong dự toán công hoặc thời gian máy. Nếu dự kiến vượt một phiên, trình tách trước triển khai; không coi có điểm chờ là bằng chứng chắc chắn cần hai task.

## Kiểm đúng đắn

- Các nhóm/mốc/unit lấy từ metadata hoặc nguồn schema, không đoán +8 giờ cho đúng hình.
- Session split/allowlist khóa trước raw; loader không thấy root/fault label như đầu vào phương pháp. Nhãn chỉ cho ghép/chấm/audit đã khai báo.
- Kiểm window không chồng lần tiêm trước theo Q-64. Khi normal của cùng phiên không đủ, không giả vờ có đủ 300 s; nguồn no-fault phải có evidence về tính phù hợp.
- Known-answer fixture cho time units, repeated identity và nested duplicates; raw kiểm theo toàn phần dev được phép, không lấy một session tốt thay toàn bộ.
- Selector ghi member thực mở; kiểm không có phiên test/không duyệt. Không mở cả file đo chứa test rồi mới lọc sau.
- Các lỗi thực đã biết từ T-009 giữ thành bằng chứng cần kiểm theo phiên, không tự gọi chúng là clock offset hoặc giới hạn vô hại.
- Không chấm ranking, không chạy baseline, không chỉnh ngưỡng/clock theo root accuracy.

## Tiêu chí xong

- Có phương án chia phiên và allowlist đã được Minh duyệt trước telemetry; selector chứng minh không mở test.
- Có bảng ghép trace và kiểm normal trên toàn phần dev/no-fault được phép; đánh giá identity, units, thời gian và coverage theo từng phương pháp.
- Kết luận PASS/FAIL/OPEN có bằng chứng, ảnh hưởng và phương án cho Minh; không yêu cầu Eadro phải PASS.
- Có nháp WHY, script/manifest/run log và LOG đủ làm tiếp. Nếu chưa có quyền đọc, chỉ báo phần metadata xong, task còn OPEN; không nâng thành xong.

## Không làm

Không tải mới, mở SN hoặc test/RE3; không benchmark hoặc tự chọn nhánh Eadro; không chạy inspector cũ toàn dataset; không sửa clock/input cho khớp; không hỏi tác giả/gửi thông điệp; không EC2, commit/push hoặc ghi tài liệu chung.

## Chi phí ước lượng

CANDIDATE, **chưa kiểm**: 2–4 giờ công agent; 10–30 phút máy cho streaming và joins; RAM 0,5–2 GB; đĩa tăng 0,1–0,5 GB, không giải nén toàn archive. ZIP TT đã có 48.923.113 byte. Logical mọi representation TT 1,478 GB, không phải lượng sẽ giải nén.

Giả định tái dùng parser và không cần tìm nguồn clock ngoài. Sai nếu parser cần sửa lớn, joins vượt RAM, hoặc thiếu bằng chứng xác minh. Chưa đo vì lượt này chỉ tạo SPEC. Không cần GPU/EC2/tải thêm; nếu dự kiến một lượt trên 1 giờ hay task vượt một phiên thì báo Minh trước.

## Rủi ro và điều chưa chắc

Danh sách phiên chưa được duyệt là phụ thuộc thật. Clock/lineage, nhãn normal và đơn vị một số kênh còn OPEN; không điền giả định để đủ checklist. T-023 chỉ quyết khả năng dữ liệu và phạm vi đề xuất, không xác nhận causal graph hay cơ chế lỗi. Q-61/Q-64 đã chốt; dữ liệu không phù hợp phải trình Minh chọn nhánh, không tự đổi dataset.
