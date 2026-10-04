# Bàn giao T-015 — Minh chốt kết quả, 04/10/2026

## A. Đã làm

Đã sửa R1–R3/N1–N7 theo đề xuất mà Minh duyệt: giải thích detector→nhóm trace→spectrum; ghi độ nhạy số vòng, phạm vi3/30dev, phương án baseline trong WHY nháp; bổ sung mặc định/chi phí và guard thời gian hữu hạn.

Hoàn thành hồ sơ MicroRank, TraceRCA RCAEval và hai bộ phát hiện, đủ7+2mục. Cài **MicroRank-RCAEval sửa đầu vào**; so90ca RE2-OB với kết quả T007 đã lưu. Chạy3ca dev Train Ticket đã chọn trước, kiểm tập ứng viên, ví dụ độc lập và tính khả thi suy schema cho bản gốc. Đề xuất biến thể này cho giao thức span hiện có ở P3 theo cơ chế/QT2; đây là CANDIDATE, không chọn theo điểm cao hơn (chờ WHY, xem de-xuat-tai-lieu-chung.md).

## B. File đã thay đổi

Khi đóng task: chỉ bổ sung LOG, cập nhật trạng thái báo cáo/nháp quyết định và manifest, cùng đúng dòngT015 trong STATE. Không thay code, dữ liệu, số liệu, nội dung phản biện hoặc file trên EC2.

Phiên sửa: SPEC chỉ thêm mục; LOG ghi quyền/tiến độ; ba file hồ sơ, ví dụ, kiểm ứng viên, CSV đầu vào/tiêu chí, nháp chung và báo cáo; guard trong `src/microrank/__init__.py`, `detectors.py`; các script kiểm độc lập/toy; script/artifact mới trong `runs/review-response/`; manifest và đúng dòngSTATE. Danh sách file thay và đầu ra mới so với manifest bàn giao đầu ở `runs/review-response/repair-validation.json`; file mới trên EC2hai ở `remote-changes.json` cùng thư mục; toàn bộ đầu ra ở manifest. REVIEW giữ nội dung reviewer và phản hồi đã ghi. Không đổi file ngoài repo trong phiên sửa; trên EC2hai chỉ thêm scripts/quét/inventory dưới T015, giữ failure lần1.

`tasks/T-015-ho-so-microrank/SPEC.md`, `LOG.md`; mọi file trong `results/T-015/`; sáu file trong `src/microrank/`; đúng dòngT015 trong `docs/STATE.md`. Danh sách từng file, gồm scripts, logs, mọi lượt hỏng, source versions và kết quả: `manifest-ban-giao.json`.

Ngoài repo: `D:/RCA-ext/work/T-015/known_hosts`, `uv-linux`. Trên hai EC2: mọi file tạo trong `/home/ubuntu/rca/T-015/`, danh sách từng đường dẫn trong manifest. Máy hai có runtime/env/cache/tmp,189file input, code và runs; máy đầu giữ pilot/lượt hỏng. File `/home/ubuntu/.sudo_as_admin_successful` trên máy đầu đã xóa đúng một lần theo quyền có sẵn và kiểm absent. Không sửa clone/env/data chung, file task cũ, WHY/DECISIONS hoặc commit/push.

## C. Kiểm tra đã chạy và kết quả

Sửa guard:27phản ví dụ bị từ chối; validtoy khớp adapter frozen và công thứcAST gốc. Quét93raw/cửa sổ đã dùng:0nonfinite/âm,93hashkhớp; không chạy ranker mới. Chẩn đoán cùngsnapshotauth25/26/50/100/101:25khớp0;26/50/100đổi top11,101giữtop11 nhưng đổi full; chưa hội tụ. Tính lại độ dài từ3snapshot xác nhận median5/179 và quan hệ grouping; không suy causal. Nguồn `runs/review-response/guard-tests.json`, `ec2-second/input-time-audit/summary.json`, `iteration-probe.json`, `trace-length-stats.csv`.

90đầu ra OB hợp lệ, hữu hạn, không ô phổ âm/không overlap; ledger110lượt gồm hai failure ban đầu. Independent TT4383giá trị khớp0, probe2729trace+298operation PPV khớp0, nguyên hàm MIT không đổi. Hai rerun duplicate có8328/9345giá trị khớp0. Seed/cột/dòng, graph gốc, root nullable, edgecases và hai cửa sổ300/600s đã kiểm. Train Ticket33check/204dòng ứng viên: vắng trace không xếp; service không cạnh vẫn có thể xếp qua incidence; auth full hạng9 nhưng vắng top11operation. Control trước tiêm vẫn báo2814span: báo giả theo giả định pre-injection bình thường, không nguyên nhân có nghĩa. TraceRCA tái dựng90NaN và79ca sắp sai; adapter lọc hữu hạn trước sort và tie canonical. Nguồn chi tiết: `kiem-dung-dan.md`, `runs/final-scientific-audit.json`, `tieu-chi-xong.csv`.

## D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM

DC01:T001 gọi detector TraceRCA gốc3σ, nhưng multiplier mặc định1; đã kiểm AST/toy và sửa hồ sơ T015. DC02: câu tuyệt đối trong MRP/WHY bỏ quan hệ cha–con dùng học SLO self-time; đã đọc đúng source, tách rõ PageRank với tiền xử lý detector và viết nháp sửa. Phạm vi phản bác được ghi: K1 nói riêng PageRank là đúng; Ochiai/66% của bài cũng đúng. Không sửa file cũ. Bằng chứng, hệ quả và đoạn cũ→mới ở `dinh-chinh-task-cu.md` và `de-xuat-tai-lieu-chung.md`.

## E. Chỗ lệch khỏi SPEC và lý do

Minh đổi reviewer sangClaude và cho giữ detector span của biến thể; lý do trước kết quả đã ghi. Chuyển EC2 thứhai do thiếu RAM/máy đầu bận; TT còn3ca trước nhìn ranking vì người làm áp cap1GB bảo thủ cho cảcopy; không phải Minh bắt buộc thu30→3. Đây là thu hẹp kế hoạch kiểm; chỉ kết luận3/30dev, chưa kiểm27ca. Sửa audit token nullable và guard exact-copy theo source gốc, giữ lỗi/lượt cũ. ShellCRLF hỏng trước method; controlTraceRCA ban đầu có11span qua mốc đã được đính chính; không giấu là normal nghiêm. Một lần tìm kiếm quá rộng artifact đã dừng, không dùng để kết luận ngoài whitelist. Mọi thay đổi có mục bổ sung SPEC/LOG; không chọn cấu hình theo root score. Phép thay số vòng đã thiếu ở bàn giao đầu; nay đã bổ sung chẩn đoán/lưu artifact nhưng vẫn giữ25. Lượt quét time lần1 thiếu manifest trên EC2, giữ failure; lần2 đúng nguồn đạt.

## F. Đề xuất cho tài liệu chung

Nháp trong `de-xuat-tai-lieu-chung.md`: lưu quyền/vai trò/EC2 theo lời Minh; WHY về biến thể, exact-copy và TraceRCA finite/tie; làm rõ cha–con trong K1/MRP/WHY02; sửa default TraceRCA T001; cập nhật việc dọn EC2 ở dòng chung. Chưa ghi các file đó. Nháp WHY đã thêm phương án baseline trước mốc và giới hạn độ dài/số vòng; nháp DECISIONS thêm quyền sửa nguyên lời Minh. Minh đã chốt kết quả T-015 ngày04/10/2026. STATE chỉ dòngT015 chuyển “Xong (04/10/2026), chưa commit”. Các nháp G1/P3 vẫn chờ quyết định riêng; không tự tạo vòng phản biện mới.

## G. Phần chưa kiểm và lý do

Chưa tái lập toàn bộ số bài MicroRank/full detector gốc: datasetA/B/C và schema kind/pod/root thật không có trong dữ liệu được phép. Giả định công thức code đủ đại diện bài có thể sai vì các khác biệt đã chỉ ra; kiểm bằng artifact/giao thức tác giả khi được phép, không gán số của bài cho biến thể. Chưa cài phương án suy schema: Minh chỉ duyệt đánh giá; root cấu trúc làm được nhưng kind/pod không nhận diện duy nhất từ11cột. Giả định metadata bổ sung có thể phục hồi sẽ sai nếu exporter đã bỏ trường; cần đối chiếu gold instrumentation độc lập nhãn. Đơn vị raw TraceRCA gốc còn OPEN vì module upstream không nằm trong clone đúngrevision; phải phục hồi nguồn encoder để kiểm, không đoán từ RE2.

Không có thời gian benchmark chính thức vì máy dùng chung; logs chỉ theo dõi ngân sách. Chưa kiểm27/30dev TT;3ca là kiểm cơ chế đã định trước, không bảo đảm ca khác. Capcopy do người làm diễn giải, phạm vi mở rộng chưa được chọn. Không benchmark P3/P4. Control giả định trước tiêm bình thường có thể sai do workload drift/sự cố chưa nhãn; cần reference sạch và ground truth riêng ở giao thức sau. Các thiếu kiểm này không được gọi là chờ quyền cho phần task đã làm được.

## H. Cần Minh quyết

Minh đã duyệt kết quả và đóng T-015 bằng câu “chốt” ngày04/10/2026. Việc mở rộng27TT hoặc giữ kiểm cơ chế3ca còn cần quyết riêng. Chốt ởG1: baselineP3 dùng biến thể nào; cửa sổ tham chiếu; inventory và full ranking hay output11operation; quy tắc finite/tie TraceRCA; có nguồn kind/pod thật để đi tiếp phương án full-original không. Duyệt các nháp tài liệu chung nếu phù hợp. T015 chưa tự chốt các lựa chọn này.
