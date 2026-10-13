# T-033 — Checkpoint sau chặng tính, phiên 6

Ngữ cảnh bị nén; dừng nghiên cứu và chuyển phiên theo AGENTS §5a.2. Codex làm, Claude phản biện. Chặng tính đã tự kiểm đạt; task, đọc tay, tổng hợp và RQ2/G2 còn OPEN. Đây là bàn giao kỹ thuật, không là báo cáo cơ chế.

## Kết quả và nơi đọc

- Sáu run pilot/rest PASS: N-Sigma 60 đơn vị ca × bộ cột; BOCPD 30 ca; kênh 30 ca. Chi tiết cùng time/RAM/byte ở coverage-resources.json và ../session6-open-001/*.observation.json. Pilot được kiểm đạt trước rest; đơn vị PASS không khởi lại.
- 299 file mới, 237026299 byte: artifact-inventory.json chỉ đường trong artifacts/. Hash hai đầu PASS, stream trực tiếp; không tạo archive EC2 hoặc xóa thêm.
- Nguồn và trung gian cũ: ../checkpoint-handoff-001/artifact-locator.json, artifact-inventory.json, artifacts/. Tự kiểm đầu phiên 825 file cũ và native/raw có bằng chứng ../session6-open-001/fresh-laptop-integrity.json, fresh-preflight-002.stdout; kiểm EC2 cuối ở final-preflight-001.stdout. Không thay native, tham số hoặc tiêu chí.
- Khóa nhóm mới: artifacts/runs/session6-groups-001/bao-phu-nhom.json; bản nhóm gốc được giữ trong đó và file gốc không đổi. Nhóm/ca đã khóa trước diễn giải; chọn điểm đối chứng và đánh giá điều kiện ghép/coverage cần làm trước đọc tay. Mẫu số từng loại ở verification.json; input trùng là quan hệ theo cặp, không cộng cờ chồng lấn thành nguyên nhân. Không kênh/lỗi/contrast không định nghĩa giữ riêng.
- Script staged session6-001 giữ nguyên. Prep đã làm đổi line ending của core; phát hiện trước pilot. session6-002 dùng core bytes chính xác bản cũ; stage002-verification.json và unchanged-computation-ast.json xác minh. Giữ các diff/payload. Bộ lọc worker đã sửa đúng thư mục và quan sát lặp dùng tên mới trước khi có poll lặp; không có bằng chứng bị ghi đè hoặc worker trùng.

## Hạch toán và EC2

Q-132: 28800 giây cũ là dự phòng chưa kiểm, thời gian thực tế cũ OPEN. Trần xử lý mới 14400 giây. Snapshot cuối: ../session6-final-budget-001/ledger.json, bản sao final-ledger.json. Đã cộng 248.718535898019 giây mới; còn 14151.281464101981 giây. Tất cả lệnh kiểm/lượt hỏng/truyền và toàn bộ job shell được đo; bounds SSH gồm cả mạng/IO, overlap điều khiển tính riêng theo hướng bảo thủ. Không coi số này là thời gian CPU nghiên cứu, không lấy subtotal status hay lịch để cấp giờ. Không sửa ledger lịch sử.

Kiểm EC2 cuối 2026-10-11T09:24:33.183391+07:00: không worker T-033/tmux, archive không tồn tại, byte/RAM/disk ghi trong checkpoint.json cùng bằng chứng. Laptop có thể đóng; không có run đang chờ xong. Agent không bật/tắt EC2. Trạng thái này có mốc kiểm, không thay kiểm mới nếu phiên sau cần dùng EC2.

Mọi xử lý EC2 tiếp theo, kể cả đọc kiểm/hash, phải đo và cộng từ snapshot cuối trước run tiếp. SSH: ubuntu@3.107.246.249, key D:/RCA-ext/keys/keys.pem; known_hosts results/T-033/runs/prepare-001/known_hosts, StrictHostKeyChecking=yes, BatchMode=yes. Python pin /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8; native/env/T-025 chỉ đọc. Lệnh xem nếu cần: `tail -n 20 ~/rca/T-033/trang-thai.txt`; thời gian toàn SSH vẫn phải ghi ledger.

## Bước tiếp

Minh mở phiên mới bằng prompt-next-session.md. Đọc AGENTS, STATE, toàn SPEC và LOG cuối; trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, LESSONS, WHY-41. Kiểm manifest checkpoint và inventory trước dùng đầu ra. Tiếp đọc tay có đối chứng, rồi tổng hợp đủ nguồn/SPEC. Những câu chưa phân xử giữ OPEN, trình đúng bằng chứng thiếu/phạm vi/chi phí; không tự đổi thiết kế hoặc chạy vượt quyền. Chưa soạn prompt phản biện Claude vì task chưa hoàn tất.

Manifest.json pin các file mới và bằng chứng phiên 6; scope-verification.json kiểm LOG chỉ nối, STATE duy nhất T-033, nguồn/ledger/script gốc giữ nguyên. approved-docs.diff là toàn diff hai file tài liệu so baseline mở phiên. Lệnh chốt laptop: `C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8 results/T-033/scripts/finish_session6.py`. Lệnh EC2 cuối và payload/timer ở checkpoint.json. Không cần Minh quyết ngân sách cho chặng đã làm; Minh cần mở phiên mới do nén ngữ cảnh.
