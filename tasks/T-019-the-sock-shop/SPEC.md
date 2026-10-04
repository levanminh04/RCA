# T-019 — Thẻ Sock Shop của họ RCAEval

- **Trạng thái:** tự duyệt theo ủy quyền Minh ngày 04/10/2026; chưa đóng G1.
- **Người làm:** Codex. **Người phản biện:** Claude.
- **Thuộc gói MRP:** P2 — **Cổng:** G1. Intent: EXECUTE.

## Mục tiêu

Kiểm RE2-SS, RE3-SS và mô tả ngắn RE1-SS. Cung cấp bằng chứng để G1 trả lời vì sao dùng hoặc không dùng Sock Shop theo MRP §4, DT18-NV2/NV3 và bước 3 của cô. Không chọn dataset, không chia dev/test, không chạy RCA hay bộ phát hiện. Mọi nguồn cũ là đầu vào cần kiểm lại.

## Đầu vào

- AGENTS.md; docs/{STATE,LESSONS,MRP,WHY,DECISIONS,review-prompt}.md; hai nguồn DT18/advisor trong docs/reference/sources/.
- tasks/_MAU/{SPEC,LOG}.md; results/T-002/mau-the-dataset.md; toàn kết quả và SPEC/LOG/REVIEW T-002; results/T-003/bang-tieu-chi.md.
- data/rcaeval/re2ss_orders_loss_2 và re3ss_carts_f1_1; public-metadata/run-002 của T-002 (HF revision trong manifest).
- D:/RCA-ext/data/{fse-ss,torai-SS,RE1-SS,fse-ob,torai-OB}; kết quả T-006/T-007. Các kết quả T-000–T-012 liên quan đến nhận định dữ liệu/lineage.

## Đầu ra

- results/T-019/the-sock-shop.md: đúng 10 mục mẫu, bảng đủ 9 tiêu chí, tách toàn release và file thực đọc.
- results/T-019/so-ca-da-nhin.csv: từng ca, nguồn, task chạy, bằng chứng trùng hoặc chưa xác lập. Không tự gán test.
- results/T-019/dinh-chinh-task-cu.md: finding có file:dòng, bằng chứng, ảnh hưởng, bản sửa trong T-019 và đoạn cũ→mới; không sửa task cũ.
- results/T-019/de-xuat-tai-lieu-chung.md: bản nháp nguyên văn cho tài liệu chung; không ghi vào nguồn chung.
- results/T-019/: script tải/kiểm, census/files/cells, manifest/hash/revision, schema/boundary/probe/overlap, source snapshot, tự phản biện SPEC, kiểm cuối và danh sách đầu ra. Giữ lượt hỏng.

## Phạm vi ghi

- tasks/T-019-the-sock-shop/{SPEC,LOG}.md.
- results/T-019/.
- data/T-019/ (ngoài git) và D:/RCA-ext/work/T-019/.
- Đúng một dòng T-019 trong docs/STATE.md: đọc ngay trước; thay chuỗi chính xác hoặc chèn dưới dòng cuối bảng; ghi đoạn byte của dòng, không ghi lại cả file; đọc ngay sau và kiểm phần còn lại không đổi.
- Không ghi nguồn chung hoặc task khác; không sửa môi trường/src ngoài task. Dùng Python đã có, không cài thêm nếu không cần.

## Edge case — kiểm và xử lý trước triển khai

| Trường hợp | Cách kiểm | Cách xử lý và hệ quả |
|---|---|---|
| Ca thiếu file | Inventory toàn tree, mỗi ca từng modality | Báo danh sách thiếu; không đồng nhất vắng file và file rỗng |
| Trace rỗng hoặc không có trace | Inventory và số hàng/footer nếu có file | Không tạo graph giả; parent/linkage không áp dụng khi không có span; kiến trúc là ứng viên riêng |
| Nhãn trùng/lặp lệch | Khóa dataset/root/fault/repetition và bảng ô | Giữ bản gốc và collision; không gộp âm thầm; mốc cùng không đủ chứng minh trùng |
| Alias service | Giữ tên raw từng nguồn, so theo nội dung/cột và mapping công bố | Chỉ normalize có bằng chứng; tên giống không đủ lineage |
| Injection ngoài dữ liệu | Min/max timestamp, số điểm pre/post từng file | Không probe ca đó; không gán trước file là normal |
| HF revision khác giữa file | SHA256 LFS hoặc git-blob SHA1 theo tree ghim | Không tái dùng file lệch; tải đúng revision trong trần; ghi mismatch thay vì sửa nguồn |
| Clock/đơn vị sai | Kiểm epoch magnitude, schema, thời gian giữa log/metric | Giữ đơn vị nguồn; báo lệch; không tự chỉnh để khớp |
| Metric hằng/NaN/trùng time | Count, quantile band, duplicate timestamp | Band zero báo riêng; không chia 0; loại kênh không đủ điểm và ghi mẫu số |
| Log chứa ID trong payload | Rà cột lẫn payload; ghép ID nếu có span | Không gọi regex là link thật; không có trace thì linkage không xác lập |
| Hash giống hoặc chuyển CSV→parquet khác byte | Hash toàn file, injection, so nội dung/time/shape/cột từng ca | Tách identical-byte, identical-content, time-only; không suy toàn ca từ cùng mốc |
| File tải lỗi/truncated | Size+hash, parse/footer | Giữ lượt lỗi, không dùng kết quả; tối đa 3 thử cùng chỗ |
| Nhiều phiên sửa file chung | Snapshot byte STATE ngay trước/sau, chỉ dòng T-019 | Dừng nếu dòng mục tiêu đổi; không khôi phục phiên khác bằng bản cũ |

## Các bước — phụ thuộc và lệnh kiểm

0. Đọc nguồn quản trị và kiểm đầu vào, HEAD, trạng thái không sạch. Kiểm: `git status --short`, `git rev-parse HEAD`, đọc file bắt buộc; snapshot hash nguồn cũ dùng lại. Không ghi log task cũ.
1. Từ bước 0: viết SPEC/LOG, tự phản biện SPEC trước telemetry, lưu những sửa. Kiểm: đối chiếu từng yêu cầu prompt, edge case và lỗi SL25/26/27/31/32, T003 R1/R2, ghi đè WHY-16.
2. Từ metadata đã kiểm bước 0: census toàn RE1/2/3-SS, danh sách ca/file/modality, root×fault×repeat, số công bố và size. Kiểm: cộng theo ca/root/fault/cell ra cùng tổng; parse toàn 3 trang tree có hash, pin revision và HEAD nguồn công khai. Nguồn công bố và số đo giữ riêng nếu lệch.
3. Độc lập bước 2: audit T-000–T-012 và nguồn tác giả/license/injector/collector; đọc T006/T007 để xác lập ca phương pháp đã nhìn. Kiểm: trích file:dòng, dữ liệu/nguồn phản bác finding. Tối đa hai subagent, chỉ vùng riêng trong results/T-019/, không dùng họ làm reviewer Claude.
4. Từ bước 2: lập kế hoạch tải/tái dùng và ghi LOG nguồn/revision/byte trước tải. Ưu tiên dữ liệu có sẵn khớp hash; có thể đọc đủ SS khi tổng dưới 1 GB. Phần OB chỉ tải metadata và metric cần so lineage, không trace/log toàn OB. Kiểm: tổng mọi byte mạng (kể cả nguồn và retry) ≤1.000.000.000; SHA256 LFS hoặc git-blob SHA1 từng file. Lệnh tải lại nằm trong results/T-019/.
5. Từ bước 4: schema thật, null/constant/time, parent span và log-trace nếu trace thực có; đọc đủ 8 root_cause.txt RE3-SS; đo biên quanh tiêm từng file thực đọc. Kiểm: parse parquet/CSV/nhãn, min/max/offset/pre/post, cột và payload. Không thể dựng graph trace khi inventory không có trace; phải ghi đó là giới hạn dữ liệu chứ không thiếu quyền.
6. Từ bước 5 và nhãn bước 2: khảo sát metric thô theo cách T002 mục 6: 2/3 pre làm reference, 1/3 pre làm control, post làm quan sát; q=.95,.99,.995 hai phía; band zero riêng; OR theo service, báo theo kênh/ca/ô và cả control. Nhãn root chỉ gắn sau khảo sát tất cả service. Kiểm: mẫu số, rate trong [0,1], reference/control/post không chồng nhau; không chạy một bộ phát hiện, không tạo nhãn lan. Bậc root chỉ đo khi có cạnh nguồn thật; không tự biến tương quan metric thành cạnh.
7. Từ bước 3/4: sổ ca đã nhìn fse/torai/RE1 SS và fse/torai OB với RE1/RE2 public. Kiểm: nội dung/injection/hash từng ca; ghi task đã chạy bằng run manifests/ranks có sẵn, không chạy lại phương pháp; T007 toàn 90 RE2-OB ghi rõ. Nếu time-only còn chưa đủ identity, giữ mức bằng chứng thay vì nói chắc.
8. Từ bước 2–7: viết thẻ, đính chính và nháp chung; kiểm đủ mẫu 10 mục/9 tiêu chí, số truy về artifacts, Q33. Kiểm: script verify + đọc toàn đầu ra; mọi phần được phép làm thì làm, phần không thể có từ release ghi OPEN kèm lý do/giả định/đầu vào/người giải quyết.
9. Từ bước 8: báo cáo A–H, kết thúc LOG đủ 6 ý, prompt nguyên văn chung+G1; inventory đủ mọi file ngoài repo; cập nhật duy nhất dòng T019 thành chờ phản biện (04/10/2026). Kiểm: final manifest, `git diff --check` giới hạn file task, nguồn cũ dùng lại giữ hash, STATE phần ngoài dòng giữ byte. Không dùng git diff làm phạm vi review.

## Kiểm đúng đắn

Tách FACT nguồn công bố, FACT metadata và FACT file thật. Tree phải kiểm checksum snapshot, phân trang và revision; file tái dùng/tải kiểm size/hash theo nguồn. Toàn census không suy từ hai mẫu. Các ca được probe có đủ pre/control/post; báo số riêng kênh để tránh OR/memory drift bị hiểu là lan. Nhận định vắng trace giới hạn đúng release ghim; graph kiến trúc không là graph quan sát. Kiểm giả là control bình thường của cùng ca, không chạy RCA. Nhãn detail đọc nguyên văn, không tự suy root/span từ fault. Sổ trùng cần phân biệt cùng mốc và cùng nội dung.

Phép kiểm không thực hiện: không chạy phương pháp hoặc detector (Minh cấm), vì vậy không khẳng định phương pháp dùng được/đã loại rò; không đo nhãn onset/vùng nếu nguồn không có, nên RQ3a/c còn điều kiện; không đọc dữ liệu khóa hay RE2-TT ngoài dev; không chọn dataset/chia test. Parent và log-trace không áp dụng khi release không có trace, không ghi “chờ quyền”. Không tự dựng đồ thị kiến trúc từ code mới vì task chỉ thẻ và dữ liệu không chứng minh cạnh runtime; vị trí root runtime vẫn OPEN.

## Tiêu chí xong

1. Thẻ đúng 10 mục, đủ 9 tiêu chí, RE2/RE3 tách riêng, RE1 ngắn; mọi số có nguồn artifacts.
2. Census toàn revision của ba SS: một hàng mỗi ca, file inventory và root×fault×repeat; collision/missing được báo.
3. Toàn file tải/tái dùng có revision+size+hash; tổng tải ≤1 GB; đủ 8 root_cause.txt được đọc và mô tả loại nhãn.
4. Schema/biên/normal/log-ID đo trên tất cả file SS được kiểm, parent/graph áp dụng đúng trace inventory; không suy đồ thị từ một mẫu hoặc tạo graph thiếu nguồn.
5. Probe ba q có control/post, theo kênh/ca/ô, ca bị loại có lý do; không gọi thành nhãn lan hay detector.
6. Sổ từng ca đã chạy T006/T007, SS và OB, có bằng chứng identity hoặc mức OPEN cụ thể; không chia dev/test.
7. Hai file đính chính/nháp chung tồn tại, ghi “không có” nếu rỗng; mọi finding được kiểm và chỉ sửa trong T019.
8. Final checklist từng tiêu chí; LOG sáu ý+A–H+prompt nguyên văn với mọi file; STATE chỉ dòng T019; không commit/push, không source chung bị ghi đè.

## Không làm

Các giới hạn prompt Minh giữ nguyên: không EC2/deep research, tối đa 2 subagent, không gửi tin ngoài, không repo lưu trữ, không data/locked, không RE2-TT ngoài dev, không RCA/detector, không ghi file chung trừ dòng STATE, không cài quyền admin, không commit/push.

## Chi phí ước lượng

Toàn SS metadata cho thấy khoảng 149,3 MB (RE1 15,4; RE2 101,1; RE3 32,7); ưu tiên tái dùng/so CSV tránh tải thừa. OB metric/metadata dự kiến <100 MB. Ngân sách tổng tải cứng 1 GB, tổng chạy script dự kiến 5–25 phút chia lượt có tiến độ, mỗi lượt <1 giờ; CPU thấp, một reader parquet từng ca, RAM dự kiến <1 GB ngoài tiến trình agent. Hai subagent làm phần đọc/lineage độc lập theo quyền prompt. Không đo hiệu năng RCA, Q40 không áp vào benchmark phương pháp ở đây.

## Rủi ro và điều chưa chắc

License dữ liệu khác license code, provenance alias, injection≠onset, biên file có thể lộ mốc, hash/chuyển đổi CSV/parquet và clock. Chưa kiểm tại lúc viết SPEC; bước 2–7 xử lý trong phạm vi. Nội dung cần ghi WHY/DECISIONS/data README chỉ nháp; không tạo quyết định vật chất mới để lấp ô. Việc vượt giới hạn ghi LOG/Cần Minh quyết rồi tiếp phần độc lập.

## Thay đổi trong lúc làm — chỉ ghi thêm

- 04/10: reader `.venv` không có requests; dùng urllib chuẩn, không cài gói. Lượt inspection đầu lỗi serialization numpy.bool; giữ partial, sửa ép bool và chạy lượt2 đủ245ca. Không đổi phép khảo sát.
- Làm rõ metric hằng (một giá trị hữu hạn khác nhau) và all-null (không giá trị hữu hạn). Đọc lại riêng metric245ca bằng finalize_evidence.py, giữ số gộp cũ trong output và ghi quality-refinement.json; không đổi bands/probe. Tại lần cuối kiểm được nên làm ngay.
- Thêm `--run` cho acquire/inspect và cache-reuse sau hash để lệnh tải lại chạy trên repo đã có lượt cũ. Không xóa/đè run. Đây là hỗ trợ tái lập trong phạm vi kết quả, không đổi source revision/dataset/chiến lược thí nghiệm.
- Parent/degree runtime không thể đo vì toàn release vắng trace; kiểm hình nguồn và báo bậc liên hệ tĩnh thay vì tạo graph từ metric. Hướng năm nét frontend không có mũi tên giữ OPEN. Phần này chỉ bổ sung mô tả nguồn, không chọn kịch bản graph ở G1.
- Rà cuối phát hiện có kênh đủ reference nhưng control/post toàn null; phải giữ tỷ lệ không xác định và chỉ so cùng entity có mẫu số dương ở cả hai cửa sổ. Bổ sung paired-entity-exclusions.csv, cập nhật tổng hợp từ rates đã đo; giữ tổng hợp trước sửa trong inspection-summary-001-before-paired/. Không đổi quantile/band/raw data hoặc tạo nhãn lan. Đây là làm đầy đủ kiểm thiếu dữ liệu đã giao, không chọn ngưỡng theo kết quả.
