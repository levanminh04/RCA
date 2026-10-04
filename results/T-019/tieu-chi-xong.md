# Đối chiếu từng tiêu chí xong của SPEC

| TC | Kết quả | Bằng chứng |
|---|---|---|
| 1 | Đạt: mỗi RE2/RE3 đủ10mục/9tiêu chí; RE1 ngắn | the-sock-shop.md; card-measurements.json; final-checks.json |
| 2 | Đạt:245ca toàn release,618file, root×fault×repeat; collision0, danh sách modality từng ca | census-cases/cells.csv; file-inventory.csv; source census độc lập |
| 3 | Đạt: từng618SS+180OBfile source hash/revision;8nhãn đủ đọc;161.824.212byte tổng mạng | acquisition/manifest.json; lineage/download-manifest.json; sources-audit/*manifest; runner-source/manifest.json |
| 4 | Đạt phần khả thi: schema/null/constant/all-null, logID, biên/normal245SS; trace toàn release không có, parent/log-trace/runtime degree N/A | inspection/cases/schemas/hash-recheck; boundaries.csv; source architecture chỉ tĩnh và áp dụng OPEN |
| 5 | Đạt:3q/control/post, từng kênh/ca/ô; tỷ lệ finite paired; exclusions có lý do; không nhãn lan | inspection/channel-bands/entity-rates/probe-cases/probe-cells/probe-summary/probe-exclusions/channel-exclusions/paired-entity-exclusions.csv |
| 6 | Đạt:405cặp nội dung; sáu archive đã parse;1245hàng sổ quan hệ và exposure, không chia test | so-ca-da-nhin.csv; ledger-summary.json; lineage/report/verification/source-file-integrity |
| 7 | Đạt: finding điều hướng T003 có phản bác/đề xuất; source discrepancy phân biệt lỗi task; nháp chung nguyên văn | dinh-chinh-task-cu.md; de-xuat-tai-lieu-chung.md |
| 8 | Đạt sau sửa R1 (04/10/2026): manifest, danh sách file và prompt khớp LOG hiện tại; kiểm bản hiện hành ở handoff-checks.json. Hai bản cũ được giữ riêng, không dùng PASS cũ để chứng nhận LOG mới. Minh duyệt đóng T-019 ngày 04/10/2026. | artifact-manifest.json; output-files.csv; handoff-checks.json; handoff-before-R1/{artifact-manifest,handoff-checks}.json; handoff-before-close/{artifact-manifest,handoff-checks}.json; state-start/finish.json |

## Việc chưa làm đã rà

- Không có phép kiểm telemetry/metadata/hash/lineage cần làm thêm mà còn thực hiện được trong giới hạn đã giao.
- Parent/join/degree runtime không thể đo: release ghim không có trace. Hình architecture chỉ là nguồn tĩnh, không pin deployment. Cần trace/deployment mới từ tác giả hoặc G1 chọn kịch bản tĩnh; không gọi là chờ quyền đọc file hiện có.
- Onset/end/normal sạch/vùng ảnh hưởng/nhân quả lan chưa có nhãn độc lập để xác lập; metric pre không tự là healthy gold. Giả định normal sai khi warm-up/drift/tải/lỗi trước; thiếu nguồn timeline/load độc lập để phân xử.
- Code-line nguyên nhân và annotation detail sai chưa có source converter/injector/deployment cho ca SS. Một duplicate có thể là chép nhãn/sai clock/association; không tự sửa label. Minh quyết việc dùng nhãn ở G1.
- Không RCA/detector/selection/split/adapter benchmarking theo giới hạn prompt. Không đưa việc bị cấm vào trạng thái phép kiểm còn đang chờ cho task này.
