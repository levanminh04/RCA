# Checkpoint phiên8 — T-033

Checkpoint do ngữ cảnh nén theo AGENTS §5a.2. Codex người làm, Claude người phản biện. Task chưa hoàn tất; đọc tay toàn nhóm, tổng hợp SPEC và câu hỏi nguồn vẫn OPEN. Không cần duyệt lại trần5GiB hoặc bản tríchv2.

1. **Đã đạt:** pilot1/rest29 có 210 đường ca/968 điểm khóa; readback/scalar/time/post_indices/NaN/flags/BO-MAP/CP/theta/source-after PASS. Không chạy detector. Các kho nhận mới có hash hai đầu PASS: extraction40file, evidence10file, stats+workload4file. Nguồn/raw89/native/env cuối PASS; không worker T-033 hay tmux ở thời điểm final-preflight.
2. **Đã ghi:** script phiên8, runs/metadata/receiver mới trong results/T-033; LOG chỉ nối; chỉ dòngT-033 STATE. Danh sách chính xác trong manifest.json. File cũ và tài liệu bảo vệ không đổi so baseline mở phiên. Không xóa thêm/commit/push, không thay nguồn/phương pháp/SPEC hay quyết định.
3. **Kiểm/ngân sách:** dùng ledger.json, integrity.json, scope-verification.json và manifest.json. Charged mới cumulative 584.1345083981271s; còn 13815.865491601873s/14400s. Bao gồm lỗi SSH, kiểm, tính từ saved arrays và transport; fullSSH elapsed là upper bound bảo thủ. 28800s cũ chỉ là dự phòng chưa kiểm, actual cũ OPEN. EC2 logical 4388065964byte <5368709120byte; diskfree 1572712448byte. Lệnh cuối EC2 có timer/ledger là session8-final-preflight-001, chỉ đọc. Không xử lý EC2 sau đó khi chốt.
4. **Còn làm:** đọc tay toàn64nhóm/210đường theo khóa, đối chứng cùng cột/điểm/ca, cạnh tranh giải thích, duration còn trongNPZ, kiểm các thiếu theta/NaN/input-identical/range0/interaction, mọi đầu ra SPEC và năm loại kết quảP4. Nguồn vật lý/onset/tải/collector và lợi ích/chọn thiết kế đồ thị không tự được xác nhận. Ghi đúng bằng chứng thiếu và phụ thuộcP6; không giảm nghĩa vụ nghiên cứu cho vừa phiên.

## Đường dẫn tiếp nhận

- results/T-033/runs/session8-extraction-001/artifacts/runs/session7-manual-pilot-001 và session7-manual-rest-001: gzip full point_source. Inventory/hash ở thư mục receiver.
- results/T-033/runs/session8-evidence-receive-001/artifacts/runs/session8-evidence-001: chuoi-bang-chung.json, bao-phu-nhom.json, phan-ra-tien-xu-ly.json, do-tre-sau-moc.json, nsigma-nguong-co-dinh.json, doi-chieu.json, tai-log.json, digest.json, source-verification.json, manifest.json. Đây là quan sát tính từ dữ liệu đã lưu; manual_interpretation OPEN. Root bao-phu-nhom.json cũ chưa thay.
- results/T-033/runs/session8-stats-receive-001/artifacts/runs/session8-stats-001: stats.json, workload-at-locked-points.json, verification.json, manifest.json. Workload là telemetry quan sát, không là bằng chứng tải ngoài/coverage đầy đủ.
- session8-open-001: input/payload/stdout/stderr/timer, kiểm extraction, baseline và helper-readonly-notes.md. Notes trợ lý không thay tự soát của người làm. Native/source/điểm được kiểm và giữ nguyên. Chuỗi rút gọn không có đầy đủ cột noalarm/duration; đọc gzip/NPZ đầy đủ theo notes, không gọi là thiếu dữ liệu nguồn.
- session6-compute-checkpoint-001/artifacts: nguồn context/factorial/delay/fixed và nhóm đã khóa; checkpoint-handoff-001/artifacts: nguồn gốc/core. Kiểm inventory tương ứng trước dùng. Nhóm/matching/point locks phiên7 giữ nguyên.

## Thực hiện phiên mới

Mở phiên Codex mới trong D:/RCA-flashticket bằng prompt-next-session.md. Đầu tiên đọc các nguồn và kiểm hash, không mở thêm run detector. Runtime laptop metadata/tài liệu: C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8. Python EC2/SSH pin trong scripts/session8_control.py; controller đó chỉ đúng với base/timer phiên8, không gọi lại nguyên trạng ở phiên9. Nối ledger checkpoint mới + timer phiên mới trước bất kỳ EC2 mới; quan sát process/hash cuối là lịch sử, cần kiểm mới có đo nếu dùng EC2.

Manifest pin cả LOG/STATE tại checkpoint; các bản LOG.md.after và STATE.md.after là snapshot bất biến cho kiểm lịch sử ở phiên sau. Không so pin lịch sử với live LOG đã nối hoặc STATE có dòng khác đổi. Lệnh cuối laptop: python bundled -B -X utf8 results/T-033/scripts/finish_session8.py (metadata/hash/tài liệu, không nghiên cứu/SSH). Kiểm toàn phạm vi nằm trong scope-verification.json.

Lượt lỗi local do gọi lại session8_open đã dừng mkdir, không EC2. Lượt SSH sandbox lỗi255 được đo. Stream lần đầu bị automatic approval review từ chối trước process; đã đọc quyền nhận đúngpayload/đích và provenance công khai, retry cùng hành động được duyệt rồi PASS. Giữ mọi timer/lượt lỗi và các bản lỗi phiên7; không xóa thêm.

Chưa prompt Claude chính thức vì task chưa xong. Minh không cần quyết lại dung lượng/thời gian; cần mở phiên tiếp theo do nén ngữ cảnh. Chưa có quyết định khoa học chính thức mới. Nội dung nghiên cứu cần đưa vào tài liệu chính thức sau tự kiểm/đủ chuỗi vẫn chưa tổng hợp. Đề xuất commit sau khi hoàn thiện và phản biện: T-033: trích trung gian đã lưu, phân xử cơ chế và tổng hợp P4; chưa commit/push.
